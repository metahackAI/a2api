# 주문·배송 조회 MVP

구현일: 2026-10-28 · Python 3.11+ · 조회 전용

## 실행

저장소 루트에서 다음을 실행한다.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m a2api demo
python -m unittest discover -s tests -v
```

`demo`는 두 개의 로컬 HTTP 서버를 시작한다. 하나는 주문·배송 backend이고, 다른 하나는 a2api gateway다. gateway가 실제 HTTP로 주문을 조회하고 배송별로 병렬 조회한 뒤 결과를 조립한다. 실행이 끝나면 서버를 종료한다.

## 구현한 구성

| 구성 | 파일 | 역할 |
|---|---|---|
| Capability IR | `src/a2api/ir.py` | 불변 capability·operation·step·의미 타입 참조와 실행 context |
| 계약 검사·컴파일 | `src/a2api/contracts.py` | manifest 검증, 의존성 정렬, 매핑·활성화 조건 검사 |
| schema profile | `src/a2api/schema.py`, `schemas/capability.schema.json` | 지원 범위를 제한한 JSON Schema 검사 |
| 카탈로그 | `src/a2api/catalog.py` | scope별 공개, 키워드 검색, cursor, snapshot hash |
| HTTP adapter | `src/a2api/http_adapter.py` | 운영자가 등록한 GET endpoint 호출과 크기·timeout 제한 |
| 실행 런타임 | `src/a2api/runtime.py` | 단계 실행, bounded foreach, 결과 검사·projection·근거 |
| 로컬 gateway | `src/a2api/server.py` | POST `/discover`, `/describe`, `/invoke` |
| 샘플 API | `src/a2api/sample/` | 주문·배송 fixture와 테스트용 인증 |

초기 기술 제안의 TypeScript 대신 실행 환경에서 사용할 수 있는 Python과 `jsonschema`로 첫 MVP를 구현했다. 계약은 JSON이므로 backend 구현 언어와 무관하게 HTTP로 연결한다.

## 라이브러리 사용

```python
from a2api import Catalog, ExecutionContext, HTTPAdapter, HTTPRoute, Runtime, load_contract

capability = load_contract("src/a2api/sample/order-shipping.json")
catalog = Catalog([capability], allow_samples=True)
adapter = HTTPAdapter({
    ("demo-orders", "getOrder"): HTTPRoute(
        "http://127.0.0.1:8001", "/orders/{id}", {"id": "/orderId"},
        {"Authorization": "Bearer local-sample-service-token"},
    ),
    ("demo-shipping", "getShipment"): HTTPRoute(
        "http://127.0.0.1:8001", "/shipments/{id}", {"id": "/shipmentId"},
        {"Authorization": "Bearer local-sample-service-token"},
    ),
})
runtime = Runtime(catalog, adapter)
# 실제 애플리케이션에서는 검증한 인증 결과에서 context를 만든다.
context = ExecutionContext("alice", "tenant-a", frozenset({"orders:read", "shipments:read"}))
found = runtime.discover("배송 조회", context)
description = runtime.describe("order.shipping_status", "0.1.0", context)
result = runtime.invoke(
    "order.shipping_status", "0.1.0", found["catalogVersion"],
    {"orderId": "ORD-1001"}, context, request_id="my-request-1",
)
print(result["data"])
```

샘플 계약은 `provenance.kind: sample`이다. `allow_samples=True`를 명시하지 않은 catalog에서는 발견하거나 실행할 수 없다. 샘플의 `reviewed`는 로컬 fixture에 대한 검증이며 운영 서비스 담당자의 승인을 뜻하지 않는다. 원래의 비활성 illustrative 계약도 별도로 보존했다.

## HTTP 흐름

서버를 유지하려면 다음을 실행한다.

```bash
python -m a2api serve --port 8000 --backend-port 8001
```

모든 endpoint는 JSON POST와 `Authorization: Bearer demo-alice`를 사용한다.

```http
POST /discover
{"query":"배송 조회"}

POST /describe
{"id":"order.shipping_status","version":"0.1.0"}

POST /invoke
{
  "id":"order.shipping_status",
  "version":"0.1.0",
  "catalogVersion":"discover 응답의 catalogVersion 값을 그대로 사용",
  "input":{"orderId":"ORD-1001"},
  "requestId":"demo-request-1"
}
```

`catalogVersion`은 계약 전체의 hash다. 이전 snapshot 값으로 실행하면 409 `CONTRACT_DRIFT`를 반환한다. ID·version을 정확히 지정해야 하며 최신 버전으로 자동 대체하지 않는다.

`discover`는 `limit`과 응답의 `nextCursor`를 지원한다. cursor는 query·caller·권한·snapshot에 결부되며, 이를 바꾼 요청에 재사용하면 거부한다. 검색은 키워드/부분 문자열 기반이다. 임베딩 검색이나 자연어 의미 판정은 구현하지 않았다.

## 샘플 결과

`demo-alice`로 `ORD-1001`을 조회하면 다음 업무 데이터를 반환한다.

```json
{
  "orderId": "ORD-1001",
  "orderState": "shipped",
  "shipments": [
    {
      "shipmentId": "SHP-501",
      "status": "in_transit",
      "estimatedArrival": "2026-10-29T18:00:00+09:00",
      "asOf": "2026-10-28T15:00:00+09:00"
    },
    {
      "shipmentId": "SHP-502",
      "status": "delivered",
      "estimatedArrival": null,
      "asOf": "2026-10-28T15:00:00+09:00"
    }
  ]
}
```

실제 envelope에는 `status`, `executionId`, `requestId`, `catalogVersion`, `completeness`, `presentation`, `evidence`, `stats.backendCalls`도 포함한다. 샘플의 업무 시각은 고정 fixture이며 `observedAt`은 실제 HTTP 조회 시각이다. `ORD-1002`는 배송이 없는 정상 주문이다.

## 계약과 실행의 보장 범위

- manifest 구조와 지원하지 않는 필드를 검사한다. 개별 입력·응답은 JSON Schema로 검사한다.
- operation/step 참조, 순환 의존성, required 매핑, JSON 타입·의미 ID 타입, collection 상한과 최악 호출 수를 컴파일 시 검사한다.
- 실행 중 각 operation의 세부 값 제약을 다시 검사한다. 일반적인 모든 JSON Schema의 포함 관계를 정적으로 증명하는 컴파일러는 아니다.
- step의 `checks`는 원시 응답의 `resultPointer`와 input/context/선행 결과를 비교한다. 소유자·테넌트·요청 ID·주문-배송 관계를 검사한다.
- `select`는 검사 이후 반환할 필드를 명시한다. 소유자·테넌트 등 검사용 내부 필드는 최종 결과로 전달하지 않는다.
- backend도 객체 권한을 검사한다. actor·tenant는 호스트 인증 context에서 HTTP header로 전달하며 모델 입력으로 덮어쓸 수 없다.
- foreach는 입력 순서를 유지하고 병렬 수를 제한한다. 기본 샘플은 최대 10개 배송, 병렬 수 5, 총 11회 상한, 재시도 0회다.
- 필수 단계가 실패하면 성공 데이터를 반환하지 않는다. 진행 중이던 GET은 끝날 수 있지만 대기 중 작업은 중단하며 변경 작업은 실행하지 않는다.
- 응답 body 크기와 socket timeout을 제한하고, 각 단계·body read에서 전체 deadline을 검사한다. DNS 및 느린 HTTP header의 강제 중단을 포함하는 운영용 hard deadline은 후속 transport 개선 범위다.
- HTTP redirect, 잘못된 MIME/JSON, 중복 JSON key, 비유한 수, 지원하지 않는 압축 응답은 거부한다.

업무 데이터용 schema profile은 `type`, 닫힌 object와 `properties/required`, `items`, 문자열·배열 길이, `uniqueItems`, 숫자 범위, `enum/const`, 설명 메타데이터, `date-time`, `x-a2api-semanticType`을 지원한다. 단순 nullable scalar union을 지원한다. `$ref`, 조건/조합 schema, 임의 format·pattern, literal mapping은 현재 거부한다. 시간 format은 시간대가 있는 RFC3339 형태의 일반 날짜·시간을 검증하며 윤초는 지원하지 않는다.

## 오류와 인증

실행 전 입력·권한·버전 오류는 `A2APIError`로 반환하며 HTTP에서는 Problem Details에 대응한다. 실행 시작 이후 실패는 `status: failed` envelope에 `error`와 확인한 근거를 넣는다. gateway는 그 오류에 해당하는 HTTP status를 사용한다. 실패 시 원시 backend body와 성공 데이터는 반환하지 않는다.

`demo-limited`는 배송 scope가 없어 catalog가 비어 있다. `demo-bob`은 `tenant-b`의 `ORD-2001`을 조회할 수 있다. `demo-alice`가 다른 사용자나 테넌트의 주문을 조회하면 거부한다. 데모 bearer token과 backend token은 공개 fixture이며, 운영 인증으로 사용할 수 없다. 운영 호스트는 검증한 사용자 identity를 `ExecutionContext`로 제공하고 downstream 위임도 별도로 구성해야 한다.

## 검증과 후속 범위

Python 3.14.4 / jsonschema 4.19.2 환경에서 실제 loopback HTTP를 사용하는 자동 테스트 40개와 CLI demo를 실행해 통과했다. 테스트는 정상·빈 배송·동시 호출, 계약/의미 ID 오류, 권한, schema drift, 관계 불일치, timeout, 크기 제한, 잘못된 JSON, redirect, cursor를 포함한다. wheel 패키지도 빌드하고 소스 폴더 밖에서 데모를 실행해 리소스 포함 여부를 확인했다.

전체 프로토콜 초안 중 변경 작업·prepare/commit·멱등 키·부분 결과·장기 실행 저장·조회/취소·MCP bridge·OpenAPI importer·일반 정책 엔진·LLM 성능 평가는 아직 구현하지 않았다. 표준 라이브러리 HTTP gateway는 로컬 시연용이며 운영 배포에는 별도 서버와 인증 통합이 필요하다.
