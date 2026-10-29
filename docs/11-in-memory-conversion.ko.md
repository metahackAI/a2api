# P0-1: OpenAPI를 메모리에서 변환하고 바로 호출하기

구현 범위: 선택한 OpenAPI GET/HEAD operation의 1:1 전환과 라이브러리 호출. review/build 파일·중간 산출물·별도 registry가 필요하지 않다. P0-2 코드 등록과 P0-3 MCP 경량화는 이 변경에 포함하지 않는다.

## 바로 실행

저장소 루트에서 기본 패키지만 설치한다. 이 예제에 MCP·LLM 키는 필요 없다.

```bash
python -m pip install -e .
python examples/direct-orders/convert_and_invoke.py
python examples/direct-orders/convert_and_invoke.py --order-id ORD-1002
```

첫 호출은 주문 한 번과 배송 두 번, `ORD-1002`는 주문 한 번과 빈 배송 목록을 반환한다. 예제는 로컬 API만 실행하고 파일을 생성하지 않는다. 두 원자 API를 호출하는 클라이언트 코드이며 자동 업무 그래프나 native 함수 등록을 구현한 예제가 아니다.

## 자기 API 연결

```python
from a2api import HTTPDeployment, convert
from a2api.importers import OpenAPIImporter

source = OpenAPIImporter.from_file("orders.openapi.json", namespace="legacy")
app = convert(
    source,
    operations={
        "getOrder": {
            "effect": "read",
            "select": ["orderId", "orderState", "shipmentIds"],
        },
    },
    deployment=HTTPDeployment(
        "https://orders.example.internal",
        credential_provider=credentials_for_user,
    ),
)
description = app.describe("legacy.getorder")
result = app.invoke(
    "legacy.getorder",
    {"path": {"orderId": "ORD-1001"}},
    context=authenticated_caller,
)
```

`credentials_for_user`와 `authenticated_caller`는 기존 호스트가 제공하는 값이다. 후자는 기존 `ExecutionContext(actor, tenant, scopes)`다. credential provider는 해당 context로 HTTP 헤더를 반환하며, 모델의 업무 입력으로 받지 않는다. 예제에 필요한 전체 호스트·샘플 설정은 [실행 코드](../examples/direct-orders/convert_and_invoke.py)에 있다.

원본 OpenAPI의 servers/security를 자동으로 배포 주소나 credential로 채택하지 않는다. 실제 사용자를 대신하는 credential·기존 호스트 정책·backend 객체 권한을 유지해야 한다. `effect=read`나 `select`는 객체 접근 권한을 부여하지 않는다. OpenAPI만으로 업무 scope나 주문-배송 관계 검사를 자동 생성하지 않는다.

## 공개 인터페이스

| 인터페이스 | 의미 |
|---|---|
| `convert(source, operations=..., deployment=...)` | 선택한 operation을 검증·연결한 `ConvertedAPI` 반환. HTTP 요청·파일 생성 없음 |
| `app.describe(id)` | 해당 호출의 id/version/summary/effects/inputSchema/outputSchema만 반환 |
| `app.invoke(id, input, context=...)` | 단일 API를 실행하고 성공/실패 envelope 반환 |
| `app.profile` | 경량 연결 profile `a2api-call/0.1` |

`operations` 키는 **원본 operationId**, invoke의 ID는 **describe의 capability ID**다. 기존 importer의 namespace/정규화 규칙을 재사용하므로 `getOrder`는 위 예제에서 `legacy.getorder`가 된다. 신규 이름 규칙이나 버전 관리 절차는 추가하지 않았다. 변환한 객체가 원본 schema와 binding을 고정하므로 별도 version/catalogVersion 입력 없이 직접 호출한다.

각 설정에는 `effect: read`를 명시한다. GET이라는 사실만으로 효과를 확정하지 않는다. `select`는 선택 사항이며 **최상위 객체 응답 필드명 목록**이다. 지정하면 원래 이름을 유지한 필드만 반환하고, 생략하면 원본 JSON 응답을 그대로 반환한다. 반환 필드를 제한해야 할 API에는 명시적으로 지정한다. 추가 필드가 있는 원본 객체도 선택 필드만 남긴다.

`select`는 단순 객체 또는 유한한 내부 객체 참조에 적용한다. root 배열·scalar·null·union 등은 `select` 없이 원본 schema로 호출할 수 있다. 임의 JSON Pointer 매핑, 필드명 변경, 복잡한 object composition의 선택은 이번 범위가 아니며 지원하지 않는 선택을 오류로 보고한다. 참조 schema는 필요한 내부 `$defs`만 공개 출력에 포함한다.

## 입력과 검증

원본의 `path`, `query`, `headers`, `body` 구조와 required/enum/범위를 유지한다. 이 범위의 GET/HEAD request body는 importer/adapter에서 거부한다. path/query를 임의로 합치지 않으며, 선택 인자는 생략하면 전송하지 않는다. JSON Schema default를 자동으로 값에 주입하지 않는다.

실행 내부는 기존 HTTP adapter를 사용한다.

```text
JSON 입력 복사·검사 → HTTP 입력 schema 검증 → host credential/context 주입
→ 지정 origin의 HTTP 호출 → 원본 응답 schema 검증
→ select 필드 추출 → 공개 출력 schema 검증 → 결과
```

기존 추출 초안의 enabled/reviewState는 바꾸지 않는다. 전체 업무 계약 compiler와 독립적인 경량 연결 객체에서 명시적인 read 선택·schema·HTTP binding을 검증한다. 기존 review/build/증분/재승인 경로는 그대로다.

## 결과·오류와 제한

```json
{
  "status": "succeeded",
  "data": {"orderId":"ORD-1001","orderState":"shipped","shipmentIds":["SHP-501","SHP-502"]},
  "completeness": {"complete":true,"scope":"single_api_response"}
}
```

`complete`의 범위는 **한 번의 API 응답**이다. 모든 페이지를 읽었거나 업무 전체가 완료되었다는 의미가 아니다. 원본이 HEAD·빈 응답이면 data는 null이다. importer가 상태 구분을 생성한 operation은 실제 `httpStatus`도 반환하며 status별 응답 schema를 먼저 검증한다.

invoke 실패는 `status: failed`, `error`(기존 A2APIError의 code/detail/issues), `completeness.complete: false`로 반환한다. 예: 잘못된 입력 `INVALID_INPUT`, backend 권한 거부 `PERMISSION_DENIED`, 응답 불일치 `SCHEMA_MISMATCH`, credential 제공 실패 `CREDENTIALS_UNAVAILABLE`. 실패 응답에는 raw backend 데이터나 credential을 넣지 않는다. 변환 설정 오류와 describe의 미노출 ID는 `A2APIError`를 발생시킨다.

HTTP 호출 예산은 invoke당 1회이며 자동 재시도는 없다. 기존 응답 크기 제한 1 MiB, backend timeout 1.5초와 전체 예산 5초를 사용한다. 임의 URL·인증 헤더·호출자 context는 input으로 바꿀 수 없다.

HEAD를 선택할 때는 importer에도 `methods={"GET", "HEAD"}`를 지정한다. 기본 importer는 GET만 선택한다. 미지원·미선택·중복 operationId나 잘못된 select는 변환 시 거부한다. 선택하지 않은 미지원 API 때문에 선택한 지원 API의 전환을 막지 않는다. 외부 `$ref` 등 기존 importer의 미지원 범위는 유지한다.

검증은 주문·배송 실제 HTTP, 빈 결과, backend 권한 거부, 전송 전 입력 거부, 선택 전 원본 응답 검증, 내부 참조/union/배열/HEAD/상태별 응답, 고정 GitHub 명세의 선택 API를 로컬 fixture로 호출하는 경우를 포함한다. 전체 명세의 모든 API나 실제 LLM 성공률을 검증했다는 뜻은 아니다.

P0-1 검증 시 ResourceWarning도 오류로 처리한 전체 회귀 테스트 201개가 통과했다. 소스 폴더 밖에 추출한 wheel을 기본 의존성의 Python 3.14 환경에서 사용해 주문과 배송 두 건을 실제 로컬 HTTP로 조회했다. 실행 예제의 일반 주문과 빈 배송 주문도 각각 HTTP 3회·1회로 확인했다.
