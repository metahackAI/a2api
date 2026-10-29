# 검토 설정과 계약 빌더

구현일: 2026-10-29. 비활성 import IR과 별도의 검토 JSON에서 실행 가능한 조회 capability와 재검증 가능한 빌드 묶음을 생성한다.

현재 방향에서 이 문서는 선택적인 전체 계약 관리 경로의 구현 안내다. 간편 전환·호출 모듈의 개발 기준은 [제품 방향](00-product-direction.ko.md)을 따른다. 모든 API의 첫 호출에 이 절차를 요구하지 않는 방향으로 정리한다.

```text
OpenAPI → import-openapi → 비활성 source IR ─┐
                                           ├→ build → mvp 실행 계약 → MCP discover/describe/invoke
별도로 작성·보존하는 검토 설정 ──────────────┘
```

a2api 전용 검토 형식이며 OpenAPI Overlay 표준 구현이나 임의 JSON patch 병합기는 아니다. 검토자가 업무 의미·권한·효과·입출력 매핑을 명시한다. 빌더는 source IR을 수정하지 않고 새 실행 계약을 만든다.

## 실행

저장소 루트에서 실행한다. JSON import와 builder는 기본 의존성으로 동작하며, MCP 검증에는 선택 의존성이 필요하다.

```bash
python -m pip install -e ".[mcp]"
python -m a2api review-demo
python -m a2api review-demo --order-id ORD-1002
python -m a2api review-demo --sample-user bob --order-id ORD-2001
```

`review-demo`는 패키지의 OpenAPI에서 두 operation을 import하고, 검토 설정으로 계약을 빌드한 뒤 공식 MCP SDK의 실제 stdio 클라이언트로 세 도구를 호출한다. 정상 주문 `ORD-1001`은 배송 두 건과 backend HTTP 호출 세 번, 빈 배송 주문 `ORD-1002`는 호출 한 번이다. 외부 서비스·LLM 키는 필요 없다. 데이터와 reviewedAt은 고정 fixture다.

각 단계의 파일을 확인하려면 새 출력 경로를 지정한다.

```bash
python -m a2api import-openapi src/a2api/sample/order-shipping.openapi.json \
  --namespace legacy_orders --output artifacts/orders-imports
python -m a2api build --imports artifacts/orders-imports \
  --review src/a2api/sample/order-shipping.review.json --output artifacts/orders-built
python -m a2api mcp-demo --build artifacts/orders-built
```

MCP 호스트의 stdio 명령은 `python -m a2api mcp --build /absolute/path/to/orders-built`다. 이 CLI는 `scope=sample`, `namespace=legacy_orders`인 로컬 주문·배송 빌드만 허용하고 임시 loopback backend와 데모 identity를 사용한다. stdout에는 MCP 메시지만 기록한다. 일반 배포에는 라이브러리에서 검증한 identity와 deployment를 제공한다.

## 검토 설정

- [OpenAPI 샘플](../src/a2api/sample/order-shipping.openapi.json): 원래 필드와 타입을 기술한다. 추가 응답 필드를 허용하는 legacy 객체를 포함한다.
- [검토 설정](../src/a2api/sample/order-shipping.review.json): 담당자, 업무·권한·입출력 매핑과 관계 검사를 명시한다.
- [검토 schema](../src/a2api/schemas/review.schema.json): 필수 항목과 지원하는 설정을 제한한다.

| 항목 | 내용 |
|---|---|
| `a2apiReview` | 형식 버전 `0.1` |
| `review` | 검토 상태·검토자·시각·sample/source 범위 |
| `source` | 원본 문서 SHA-256과 importer namespace |
| `semanticTypes` | 업무 식별자의 base type과 namespace |
| `operations` | source operation과 digest, 필드 매핑·의미 annotation·효과 |
| `capabilities` | 업무 입출력·owner·정책·DAG·반환 필드·표시 방법·operationIds |

operation 설정 일부:

```json
{
  "id": "demo.getOrder",
  "source": {
    "capabilityId": "legacy_orders.getorder",
    "operationId": "getOrder",
    "digest": "<검토한 source contract와 HTTP binding의 SHA-256>"
  },
  "effects": {"kind": "read", "externalWrites": false},
  "inputs": {"orderId": {"pointer": "/path/orderId"}},
  "outputs": {
    "orderId": {"pointer": "/result/orderId"},
    "ownerId": {"pointer": "/result/ownerId"},
    "tenantId": {"pointer": "/result/tenantId"}
  },
  "semanticAnnotations": [
    {"schema": "input", "pointer": "/properties/orderId", "semanticType": "sales.OrderId"},
    {"schema": "output", "pointer": "/properties/orderId", "semanticType": "sales.OrderId"}
  ]
}
```

이는 형식 설명용 일부다. 실제 샘플에는 주문 상태·배송 ID 목록 등 조립 필드가 더 있다. inputs/outputs의 pointer는 source 값, semanticAnnotations의 pointer는 생성할 JSON Schema의 위치다. 임의 식·코드·문자열 보간을 실행하지 않는다.

검토 대상의 해시는 다음처럼 확인한다.

```python
from a2api import source_digest
from a2api.importers import OpenAPIImporter

source = OpenAPIImporter.from_file("openapi.json", namespace="legacy")
print(source.source_hash)
for record in source.iter_operations():
    if record.capability:
        print(record.capability.id, record.operation_id, source_digest(record))
```

검토 파일은 importer 출력과 별도로 유지한다. importer와 builder는 이 파일을 읽기만 하며 상태·digest를 자동 갱신하지 않는다. 재생성은 새 출력 폴더를 사용한다.

## 파생 schema와 실행

필드 타입·enum·길이·배열 상한 등은 선택한 source schema에서 파생한다. 검토 설정으로 개별 필드의 타입을 임의로 바꾸지 못한다. 의미 annotation은 base type과 함께 검사한다.

선택한 유한한 내부 `$ref`를 해소하되 기존 `mvp` schema로 표현할 수 있어야 한다. union/조건 schema·pattern·일반 format 등 미지원 검증 규칙을 버리지 않는다. 열린 객체 전체 선택은 거부하고 필요한 필드를 개별 pointer로 선택할 수 있다. 선택한 배열·객체 값 자체는 닫힌 MVP schema여야 한다.

필수 source 입력 누락·겹치는 입력 pointer·필수 입력의 optional 전환·optional 결과를 required로 약속하는 설정을 거부한다. GET/HEAD 외 메서드는 read로 표시해도 빌드하지 않는다. HEAD 등도 선택한 응답과 기존 actor/tenant 정책을 표현할 수 있어야 한다.

실행 순서:

1. `ReviewedHTTPAdapter`가 검토한 입력을 검사하고 source path/query/header로 매핑한다.
2. 원래 HTTP 어댑터가 source 입력·HTTP binding·원시 응답 schema를 검사한다.
3. 검토한 결과 필드만 선택하고 실행 operation의 닫힌 schema를 검사한다.
4. Runtime이 owner·tenant·요청 ID·주문-배송 관계를 검사한다.
5. 검사용 필드를 제외한 최종 업무 결과를 반환한다.

source의 새로운 비공개 필드는 선택하지 않으면 사용자 결과에 포함되지 않는다. 선언된 source 필드의 타입 위반은 계속 실패하며, 검사에 필요한 owner/tenant 필드를 먼저 버리지 않는다.

## 빌드와 로드

```text
orders-built/
  build.json
  review.json
  contracts/order.shipping_status.0.1.0.json
  imports/report.json
  imports/contracts/legacy_orders.getorder.json
  imports/contracts/legacy_orders.getorder.http.json
  imports/contracts/legacy_orders.getshipment.json
  imports/contracts/legacy_orders.getshipment.http.json
```

검토한 import 스냅샷과 설정을 포함한다. 새 빌드 형식 0.2는 `imports/source.snapshot.json`과 `imports/dependencies.json`에 원본 JSON과 의존성 index도 보관해 [증분 재생성](09-source-diff-and-regeneration.ko.md)에 사용한다. 기존 0.1 빌드도 계속 로드한다. 실행 계약 provenance에는 검토자·시각·원본 해시·검토 파일 해시·source operation digest가 들어간다. 실제 deployment origin과 credential은 호스트가 주입한다. 명세의 servers/security는 출처 정보로 남는다.

`load_build`는 source/review로 계약을 다시 생성하고 metadata와 산출물 바이트를 대조한다. 수정·누락·외부로 나가는 파일 참조는 로드 실패다. 동일한 입력은 JSON object의 키 순서와 무관하게 같은 계약과 catalogVersion을 만든다.

```python
from a2api import HTTPDeployment, load_build
from a2api.mcp_bridge import serve_stdio

built = load_build("artifacts/orders-built")
# host_deployments와 context는 호스트가 구성·검증한다.
runtime = built.runtime(host_deployments, allow_samples=True)
# await serve_stdio(runtime, context)
```

deployment mapping은 source serviceRef별 `HTTPDeployment(base_url, path_prefix=..., credential_provider=...)`다. production source 검토에는 기본값 `allow_samples=False`를 사용한다. 샘플은 `reviewedBy=local-fixture-suite`, `scope=sample`이며 기본 카탈로그에서 숨긴다.

검토 파일은 신뢰하는 운영자가 관리하는 설정이다. 검토자 인증이나 서명된 승인 검증 기능은 아니다. 해시와 재구성은 검토 대상 고정과 파일 일관성 확인용이다. 실제 승인·설정 접근 제어·credential 관리는 호스트 책임이다.

## 오류와 후속 범위

| 코드 | 의미 |
|---|---|
| `INVALID_REVIEW` | 누락·알 수 없는 설정·잘못된 시각 |
| `REVIEW_REQUIRED` | 미검토 상태·검토자/담당자 미지정 |
| `SOURCE_DRIFT` | 원본 해시나 contract/binding digest 불일치 |
| `IMPORT_NOT_BUILDABLE` | 선택한 source 누락·중복·미지원 |
| `IMPORT_BUNDLE_INVALID` | report/contract/binding 불일치·경로 이탈 |
| `UNSUPPORTED_PROJECTION` | 미지원 schema/pointer·필수 매핑 누락 |
| `BUILD_WRITE_UNSUPPORTED` | 변경 메서드 활성화 시도 |
| `INVALID_CONTRACT` | 권한·의미 타입·DAG·예산 검사 실패 |
| `BUILD_DRIFT` | 산출물/metadata와 재구성 결과 불일치 |
| `OUTPUT_EXISTS` | 기존 출력 폴더 덮어쓰기 시도 |

모든 설정·매핑 검사를 통과한 뒤 출력 폴더를 만든다. 새 기준을 승인하는 `build`는 문서 전체 해시를 고정한다. 기존 검토를 보존하며 다음 원본으로 이동할 때에는 [diff·증분 재생성](09-source-diff-and-regeneration.ko.md)을 사용해 영향받는 capability만 재검토 대상으로 표시한다. 새로운 schema 실행 profile, 변경 업무 승인·멱등성·결과 대조는 후속 범위다.

## 검증

```bash
python -W error::ResourceWarning -m unittest discover -s tests -v
```

검토 차단·원본/바인딩 변경·미지원 매핑·권한 검사 누락·검토 파일 보존·결정적 빌드·로드 재검증을 확인한다. loopback HTTP에서 기존 수동 계약과 결과 비교, 빈 배송, 비공개 필드 제거, 다른 사용자·테넌트, scope 부족과 원본 schema 오류를 검증한다. CLI import/build 산출물을 공식 MCP stdio 클라이언트에 연결해 정상·빈 결과·권한 거부·수정된 빌드의 서버 시작 차단도 확인한다.

기존 대규모 GitHub importer·HTTP·MCP 테스트를 포함한 전체 **138개 테스트**가 통과했다. wheel에 검토 schema와 OpenAPI/검토 샘플이 포함되는지 확인하고, 소스 폴더 밖에서 Python 3.14.4의 기본 의존성으로 import/build를 검증했다. MCP 의존성을 갖춘 Python 3.12 환경에서는 설치된 wheel의 `review-demo`로 실제 stdio 전체 흐름을 확인했다. 의존성 검사와 `git diff --check`도 통과했다.
