# a2api 방향 재정렬: 전환해서 바로 호출하는 프로토콜 모듈

작성일: 2026-10-29 · 상태: 개발 기준 설계 · P0-1/P0-2/P0-3 구현 완료

이 문서와 [개발 계획](03-roadmap-and-evaluation.ko.md)이 이후 개발의 기준이다. 최초 아키텍처·프로토콜 초안은 배경 자료로 보존한다. P0-1의 실제 사용법은 [메모리 전환 안내](11-in-memory-conversion.ko.md)에 있다. 기존 구현을 삭제하거나 전체 계약의 승인 규칙을 우회하지 않는다.

P0-2의 현재 사용법은 [Python 함수·신규 API 등록](12-python-functions.ko.md)에 있다.

두 경로의 실제 stdio 연결과 공통 도구 경량화는 [P0-3 MCP 안내](13-lightweight-mcp.ko.md)에 있다.

현재 경량 wire의 기준은 [a2api-call/0.1 명세](20-call-protocol.ko.md)와 패키지 JSON Schema다. [선택적 설명·탐색 설정](21-discovery-metadata.ko.md), [설치부터 실제 모델 호출까지](22-quickstart-and-model.ko.md)가 기존 방향을 구현한다. 이 마무리의 개발 범위는 [세 작업 계획](19-protocol-completion-plan.ko.md)으로 고정한다.

## 1. 제품의 목적과 순서

**a2api의 목표는 API 규모와 관계없이 LLM이 필요한 기능을 찾고 정확한 인자로 호출하는 데 드는 전체 비용을 줄이는 프로토콜을 정립하는 것이다.** 기존 API·함수를 같은 호출 계약으로 전환하는 라이브러리가 이를 구현한다. 비용은 탐색·설명·실행·오류 수정·후속 요청을 포함하며, 사용자 조건을 지킨 성공 여부를 먼저 평가한다. 도구 수나 최초 schema 크기만으로 효과를 판단하지 않는다.

2026-10-30에 확정한 후속 개발은 [전체 호출 비용 계획](23-total-call-cost-plan.ko.md)을 따른다. 같은 계약의 필요한 입력 schema만 호스트가 모델 도구로 제공하고 식별자·계약 버전은 호스트가 관리한다. 기능을 이미 아는 요청에는 모델의 discover/describe를 강제하지 않는다. 모르는 기능은 호스트가 기존 discover/describe를 처리해 다음 모델 요청에 선택한 도구를 제공한다. 기존 3도구 wire는 보존한다.

실제 GitHub GET 8개/633개 [검증 결과](27-real-github-evaluation-results.ko.md)에서는 큰 카탈로그의 탐색이 실패했다. 현재 바인딩의 구현 완료와 제품 목표 전체의 달성을 구별한다. [다음 개선 계획](28-cost-improvement-plan.ko.md)은 검색·전달 정보·재검증으로 한정했고 아직 구현하지 않았다.

사용자가 처음 해야 할 일은 사용할 API를 선택하고 연결하는 것이다. import 산출물·검토 파일·빌드 폴더·변경 기록·재승인 절차를 모두 운영하는 것이 기본 사용법이 되어서는 안 된다.

기본 사용 흐름은 다음 하나다.

```text
OpenAPI 또는 명시적으로 등록한 코드
              ↓ importer: 사실과 타입을 읽음
        메모리 안의 API 정의
              ↓ converter: 호출 계약과 실행 연결을 생성
         바로 호출 가능한 a2api 객체
              ↓ 라이브러리 호출 또는 선택적 MCP 연결
          기존 API/함수 실행 → 필요한 결과
```

이 세 화살표는 라이브러리 내부 책임 구분이다. 사용자가 세 번 파일을 생성하거나 검토 절차를 밟아야 한다는 뜻이 아니다. 일반 경로는 로드·변환과 호출 코드로 끝내며 중간 산출물 저장은 선택 사항이다.

첫 완료 목표는 **지원 범위 안의 API를 작은 설정으로 전환하고 실제 호출할 수 있는 모듈**이다. API 관리 플랫폼, 배포 파이프라인, 변경 승인 플랫폼을 먼저 완성하는 방향으로 가지 않는다.

## 2. 최초 목표와 현재 구현을 다시 대조한 결과

처음 목표에는 언어에 독립적인 레거시 연결, 공통 IR, 필요한 기능만 탐색, 업무에 맞는 입출력과 조립이 있었다. 이 방향은 유지한다. 다만 처음부터 다음 모든 기능을 필수 사용 경로에 놓은 것은 과했다.

| 현재 상태/문제 | 조정하는 방향 |
|---|---|
| OpenAPI import는 되지만 실행까지 별도 큰 review 설정과 build가 필요 | 지원하는 operation은 작은 연결 설정으로 실행 계약까지 변환 |
| 단순 조회에도 업무 composition과 여러 정책 필드가 필수 | API 하나를 capability 하나로 연결하는 형태를 먼저 제공 |
| 전체 IR을 `describe`로 반환 | 에이전트용 호출 설명만 반환하고 실행 상세는 서버에 보관 |
| MCP `invoke.outputSchema`에 모든 노출 capability의 결과 schema를 나열 | 공통 envelope만 광고하고 선택한 계약의 실제 결과는 서버에서 검증 |
| 바뀐 API의 관리 기능이 기본 사용법처럼 보임 | diff·증분·재승인은 선택적인 관리 기능으로 보존 |
| CI·버전 정책·배포 확장이 다음 핵심 작업으로 제안됨 | 쉬운 전환·직접 호출 경로가 끝나기 전에는 진행하지 않음 |

HTTP adapter, importer의 schema 처리, 실제 MCP 연결, 입력·응답 검증은 재사용할 자산이다. 이미 구현한 관리 기능도 보존한다. 이를 첫 사용의 선행 조건으로 요구하지 않는 방향으로 공개 인터페이스를 정리한다.

### 현재 구현과 목표를 혼동하지 않는다

**현재 구현:** Python 조회 MVP, OpenAPI 3.0/3.1 importer, 여러 HTTP 메서드의 transport, 고정 세 도구 MCP bridge, review/build, 변경 영향·부분 승인. 활성 runtime은 GET/HEAD 중심이고 CLI MCP 데모는 로컬 fixture를 사용한다.

**P0-1에서 추가한 구현:** `convert(OpenAPIImporter, operations=..., deployment=...)`가 `ConvertedAPI`를 반환하며 메모리에서 GET/HEAD를 호출한다. `ConvertedAPI.describe(id)`는 경량 호출 설명만 제공한다. 별도 review/build 파일을 생성하지 않는다.

**P0-2에서 추가한 구현:** `@capability`와 `Application`이 명시적으로 등록한 동기 Python 함수의 타입 힌트·TypedDict에서 schema를 만들고 같은 형식으로 호출한다.

**P0-3에서 추가한 구현:** 두 경로를 같은 MCP bridge에 연결하며 도구 목록은 공통 schema만 제공한다. MCP describe는 경량 descriptor를 반환하고 실제 업무 출력은 선택한 schema로 서버에서 검증한다. 전체 Runtime 계약의 라이브러리 조회는 유지한다.

## 3. importer·converter·protocol·runtime의 역할

| 구성 | 입력 → 출력 | 맡지 않는 일 |
|---|---|---|
| importer | OpenAPI 또는 등록한 함수·타입 → source operation 정의 | 업무 관계·권한·부작용을 알아서 확정 |
| converter | source 정의 + 작은 노출 설정 → 호출 계약과 binding | 새로운 배포/검토 플랫폼 운영 |
| protocol | 입력·설명·호출·결과·오류의 공통 형식 | HTTP 주소·credential·검토 이력의 LLM 전송 |
| runtime | 계약에 맞는 요청 → 연결된 HTTP/함수 실행 → 검증한 결과 | 임의 URL/코드 실행, 업무 성공 여부의 무근거 추측 |
| MCP bridge | 위 인터페이스를 MCP 도구로 전달 | 도구마다 계약 전체를 중복 적재 |

라이브러리의 낮은 수준 API는 importer와 converter를 따로 사용할 수 있게 한다. 기본 예제는 하나의 `convert(...)` 결과를 호출하는 형태로 제공한다. 별도 중앙 registry·서버·DB는 요구하지 않는다. MCP 서버가 필요한 사용자는 같은 객체를 bridge에 연결한다.

### 같은 정의에서 세 가지 표현을 만든다

```text
개발자 작성/생성 정의 한 개
    ├─ 호출 설명: id, summary, inputSchema, outputSchema, effect
    ├─ 실행 정보: handler/HTTP route, 값 매핑, 인증 연결, 검증 규칙
    └─ 선택적 관리 정보: 원본 위치, hash, 검토/변경 이력
```

세 종류의 파일을 사람이 따로 작성하라는 뜻이 아니다. converter가 필요한 표현을 만들며, 같은 입출력 schema를 여러 곳에 손으로 복사하지 않는다. 내부 IR과 저장 파일이 커지는 것과 모델 문맥이 커지는 것은 구분한다.

## 4. 최소 호출 계약

다음은 **경량 descriptor 형태 예시**다. 기존 전체 manifest schema를 그대로 이 형식이라고 부르지 않는다. 실제 schema는 importer가 생성한 제약과 필요한 내부 정의를 보존한다.

```json
{
  "id": "legacy.getorder",
  "version": "0.1.0",
  "summary": "주문 번호로 주문 상태와 연결된 배송 번호를 조회한다.",
  "effects": {"kind": "read"},
  "inputSchema": {
    "type": "object",
    "properties": {
      "path": {
        "type": "object",
        "properties": {"orderId": {"type": "string", "minLength": 1}},
        "required": ["orderId"], "additionalProperties": false
      }
    },
    "required": ["path"], "additionalProperties": false
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "orderId": {"type": "string"},
      "orderState": {"type": "string"},
      "shipmentIds": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["orderId", "orderState", "shipmentIds"],
    "additionalProperties": false
  }
}
```

`inputSchema`와 `outputSchema`는 정확한 호출·검증에 필요한 정보라서 토큰을 줄이려고 생략하지 않는다. 문장을 짧게 한다는 이유로 enum·필수값·범위·의미를 잃지 않는다. 큰 schema 자체가 업무에 필요한 경우 비용이 커질 수 있음을 그대로 표시한다.

인증 주체, tenant, token, backend URL, HTTP 매핑, 내부 owner 필드, 단계별 실행 그래프, reviewer와 source snapshot은 이 설명에 넣지 않는다. 사용자 입력이 인증 context를 덮어쓸 수 없게 한다.

일반 호출 설명의 필수 항목은 ID·짧은 용도·입출력·효과다. 현재 wire의 version/catalogVersion은 선택한 설명과 실행을 일치시키는 값으로 유지한다. owner·intent의 여러 목록·presentation·provenance·전체 execution 규칙은 경량 계약의 필수 작성 항목으로 두지 않는다.

**효과 선언은 자동 승인 절차가 아니다.** 개발자가 노출할 API와 실제 효과를 명시하고 호스트가 연결한다. GET이라는 이유만으로 읽기 전용·무해하다고 확정하지 않는다. 최초 경량 실행 범위는 GET/HEAD와 명시적인 조회 함수다. 쓰기/효과 미확정 API는 importer에서 구별해 보고하고, 실행 지원을 별도로 구현하기 전에는 실행 가능하다고 안내하지 않는다.

### 원본 입력 위치를 보존한다

OpenAPI에서 가져온 operation은 기본적으로 `path`, `query`, `headers`, `body` 위치를 보존한다. 같은 이름의 path/query 필드를 임의로 합치지 않는다. 인증/관리 헤더는 업무 인자로 만들지 않는다. 간단한 주문 조회 입력은 `{"path":{"orderId":"ORD-1001"}}`이다.

업무용 wrapper나 native 함수는 `{"orderId":"ORD-1001"}`처럼 함수 인자를 직접 사용한다. 모든 operation을 보기 좋게 flatten하기 위해 사용자에게 매핑 설정을 강제하지 않는다.

### 결과와 오류

모델에 필요한 기본 결과는 실행 상태, 선택한 업무 데이터와 완전성이다. 예를 들어:

```json
{
  "status": "succeeded",
  "data": {"orderId": "ORD-1001", "orderState": "shipped", "shipmentIds": ["SHP-501"]},
  "completeness": {"complete": true}
}
```

실패는 구조화된 `error.code`와 필요한 입력 경로 등으로 알린다. 상세 stack trace·credential·전체 raw response를 보내지 않는다. `INVALID_INPUT`, `PERMISSION_DENIED`, `SCHEMA_MISMATCH`, backend 실패 등을 구별한다. 위 짧은 결과는 목표의 필수 부분을 보인 예시이며 기존 결과 envelope를 이번에 바꾸지 않는다.

개발자 debug에서는 전체 실행 기록을 볼 수 있다. 기본 LLM 결과에는 사용에 필요한 출처·기준 시각·누락 정보를 남기고, 정적인 큰 presentation 설정과 반복된 계약 설명은 계속 보내지 않는다. 페이지/개수 제한으로 일부만 반환했다면 전체 성공으로 표현하지 않는다.

## 5. 레거시 전환 A: OpenAPI가 있는 HTTP API

### 5.1 변환 전 코드와 응답

아래는 기존 업무를 단순화한 Python 코드다. Java·Node.js·Go 등으로 같은 HTTP endpoint가 구현되어 있어도 전환 경계는 동일하다.

```python
# 레거시 내부 구현 예시. a2api 코드가 아니다.
def get_order(order_id, caller):
    row = orders.load_visible_to(order_id, caller)
    return {
        "orderId": row.id, "orderState": row.state,
        "shipmentIds": row.shipment_ids,
        "ownerId": row.owner_id, "tenantId": row.tenant_id,
    }

def get_shipment(shipment_id, caller):
    row = shipments.load_visible_to(shipment_id, caller)
    return {
        "shipmentId": row.id, "orderId": row.order_id,
        "status": row.status, "estimatedArrival": row.eta,
        "asOf": row.observed_at,
        "ownerId": row.owner_id, "tenantId": row.tenant_id,
    }
```

예시 HTTP 인터페이스:

```text
GET /orders/ORD-1001
→ {orderId, orderState, shipmentIds, ownerId, tenantId}
GET /shipments/SHP-501
→ {shipmentId, orderId, status, estimatedArrival, asOf, ownerId, tenantId}
```

원본의 객체 권한 검사는 계속 필요하다. a2api가 origin에 연결됐다는 사실만으로 사용자별 접근 권한이 생기지 않는다.

### 5.2 대응하는 OpenAPI

아래는 위 인터페이스를 설명하는 설계용 명세 예시다. 실제 고정 fixture는 [기존 주문·배송 명세](../src/a2api/sample/order-shipping.openapi.json)에 있다.

```yaml
openapi: 3.1.0
info: {title: Orders and Shipping, version: 1.0.0}
paths:
  /orders/{orderId}:
    get:
      operationId: getOrder
      summary: 주문 상태와 연결된 배송 번호 조회
      parameters:
        - name: orderId
          in: path
          required: true
          schema: {type: string, minLength: 1}
      responses:
        '200':
          description: 조회 권한이 있는 주문
          content:
            application/json:
              schema: {$ref: '#/components/schemas/Order'}
  /shipments/{shipmentId}:
    get:
      operationId: getShipment
      summary: 배송 상태 조회
      parameters:
        - name: shipmentId
          in: path
          required: true
          schema: {type: string, minLength: 1}
      responses:
        '200':
          description: 조회 권한이 있는 배송
          content:
            application/json:
              schema: {$ref: '#/components/schemas/Shipment'}
components:
  schemas:
    Order:
      type: object
      required: [orderId, orderState, shipmentIds, ownerId, tenantId]
      properties:
        orderId: {type: string}
        orderState: {type: string}
        shipmentIds: {type: array, items: {type: string}, maxItems: 10}
        ownerId: {type: string}
        tenantId: {type: string}
    Shipment:
      type: object
      required: [shipmentId, orderId, status, estimatedArrival, asOf, ownerId, tenantId]
      properties:
        shipmentId: {type: string}
        orderId: {type: string}
        status: {type: string, enum: [pending, in_transit, delivered]}
        estimatedArrival: {type: [string, 'null']}
        asOf: {type: string}
        ownerId: {type: string}
        tenantId: {type: string}
```

### 5.3 importer가 읽는 것

| 추출 사실 | 예시 | 변환 시 사용 |
|---|---|---|
| operation ID | getOrder | 안정적인 식별자와 기본 이름 |
| method/path | GET /orders/{orderId} | 서버 전용 HTTP binding |
| 입력 위치·타입 | path/orderId: string, required | 호출 schema와 직렬화 |
| 응답·참조 schema | 200 → Order | 결과 검증과 노출 schema 생성 |
| summary | 주문 상태 조회 | 기본 호출 설명 |
| 원본 security/servers | 선언이 있으면 읽음 | 참고 정보; 실제 credential·origin은 호스트가 선택 |

`shipmentIds`와 `shipmentId` 이름이 비슷하다는 것만으로 업무 관계나 객체 권한을 확정하지 않는다. 내부 `$ref`는 schema 관계이며 업무 호출 그래프와는 다르다. 동작을 모르는 필드는 모른다고 남긴다.

### 5.4 converter에 주는 작은 설정과 호출

다음 형태는 **P0-1에서 구현한 공개 API**다. 실제로는 자기 OpenAPI와 호스트의 credential/context를 제공한다. 원본의 유한한 단순 객체 필드를 선택하며 복잡한 projection은 오류로 보고한다.

```python
from a2api import convert                    # P0-1 메모리 변환
from a2api.importers import OpenAPIImporter   # 기존 parser 재사용
from a2api.reviewed_adapter import HTTPDeployment

source = OpenAPIImporter.from_file("orders.openapi.yaml", namespace="legacy")
app = convert(
    source,
    operations={
        "getOrder": {
            "effect": "read",
            "select": ["orderId", "orderState", "shipmentIds"],
        },
        "getShipment": {
            "effect": "read",
            "select": ["shipmentId", "orderId", "status", "estimatedArrival", "asOf"],
        },
    },
    deployment=HTTPDeployment(
        "https://orders.example.internal",
        credential_provider=credentials_for_user,  # 기존 호스트의 신뢰하는 함수
    ),
)
result = app.invoke(
    "legacy.getorder", {"path": {"orderId": "ORD-1001"}},
    context=authenticated_caller,
)
```

예시의 `credentials_for_user`와 `authenticated_caller`는 호스트가 제공하며 모델이 만드는 업무 인자가 아니다. 원 API의 사용자·테넌트 권한을 유지해야 한다. 하나의 높은 권한 token으로 모든 사용자를 대신하지 않는다. 서비스 credential만 있고 객체 권한 검사가 없는 시스템은 기존 호스트의 권한 검사를 유지해야 한다.

공개 설정의 `select`는 노출할 응답 필드만 지정한다. 예시는 원래 필드명을 유지하며 임의 변환 표현식을 도입하지 않는다. 원래부터 공개하기 적합한 JSON을 반환하는 단순 API는 그대로 노출할 수 있다. 내부 데이터가 있는 이 예제에서는 필드 목록을 명시한다. 표시 열을 숨기는 것으로 서버가 LLM 전송 전에 필드를 제거하는 처리를 대신하지 않는다.

위 코드를 실행하면 메모리에 다음 연결이 만들어진다.

```text
legacy.getorder    → 원본 요청·응답 schema → GET /orders/{orderId}
legacy.getshipment → 원본 요청·응답 schema → GET /shipments/{shipmentId}
```

전체 capability manifest 작성, 별도 review 파일 생성, build 파일 생성이나 registry 배포는 요구하지 않는다. 기존 기능을 통한 변환 결과 저장과 고급 검증은 선택할 수 있지만 첫 API 호출의 필수 절차는 아니다.

### 5.5 호출 내부에서 실제 일어나는 일

```text
app.invoke("legacy.getorder", {path: {orderId: "ORD-1001"}}, context)
  1. 연결한 앱 안에서 계약을 찾고 입력을 검증
  2. host credential provider가 신뢰하는 context로 credential 제공
  3. binding이 path/orderId를 /orders/{orderId}에 인코딩
  4. HTTP adapter가 host가 정한 origin 호출; backend가 객체 권한 검사
  5. 원본 응답 검증 → 선택한 필드 추출 → 공개 출력 검증
  6. status/data/completeness 반환; 내부 필드는 LLM에 전송하지 않음
```

이는 한 번의 호출 내부 처리이며 사용자가 실행할 여섯 개의 명령이 아니다. backend URL·token·ownerId를 모델 prompt에 넣을 필요가 없다.

### 5.6 API가 수백·수천 개일 때

같은 처리를 operation별로 반복하되 입력/응답 schema와 binding은 importer가 읽은 내용으로 생성한다. API마다 전체 manifest나 별도 검토 문서를 사람이 복사해 작성하지 않는다. 같은 서비스의 origin·credential 연결은 한 번 설정한다. 개발자가 선택할 것은 노출 대상과 필요한 출력 제한·효과 선언이다.

모든 source operation을 가져왔다는 것, 지원하는 operation을 변환했다는 것, 실제 호출을 검증했다는 것을 각각 보고한다. 미지원 항목은 operation ID와 사유로 남겨 부분 도입이 가능하게 한다. 관련 없는 API까지 모두 지원할 때까지 첫 호출을 막지 않는다.

변환된 모든 항목은 서버 카탈로그에서 찾을 수 있다. LLM에는 선택한 후보 요약과 호출할 항목의 설명만 보낸다. 문서의 전이 참조를 추적하는 일과 주문→배송 같은 업무 관계를 확정하는 일도 구별한다. 대규모 소스가 있더라도 기존 HTTP/OpenAPI 경계를 먼저 사용하며, 내부 함수 전체를 노출하지 않는다.

## 6. 레거시 전환 B: OpenAPI가 없고 코드만 있는 경우

전체 저장소와 모든 언어를 자동 이해하는 작업을 첫 호출의 선행 조건으로 삼지 않는다. 실제 호출할 공개 경계를 기준으로 전환한다.

| 현재 상황 | 초기 전환 방법 | 첫 단계에서 보장하지 않는 것 |
|---|---|---|
| Java/Node.js/Python/Go/Rust/C#이 이미 HTTP 제공 | 기존 프레임워크에서 만든 OpenAPI 사용; 없으면 선택한 route의 최소 schema 보완 | 언어마다 완전한 정적 분석기 개발 |
| 호출 가능한 Python 함수에 타입·문서가 있음 | 함수를 명시적으로 등록하고 signature/지원 annotation을 읽어 callable 연결 | 소스 스캔만으로 업무 관계·권한 확정 |
| 타입 부족 또는 동적인 반환 객체 | 선택한 함수의 입출력 schema 작성 또는 작은 wrapper | 임의 동적 객체의 정확한 JSON schema 추측 |
| Java/Node/Go/Rust 등의 프로세스 내부 함수 | 기존 HTTP/로컬 서비스 경계를 우선 사용하고 필요한 wrapper만 제공 | Python 모듈이 다른 언어 메서드를 직접 실행 |
| C/C++ 포인터·native handle | 값 타입 인터페이스로 wrapper를 만든 뒤 그 경계에서 import | 포인터 자동 직렬화·범용 FFI/ABI 호환 |

### 코드 기반 전환 예시

```python
# 기존 코드: 외부에 그대로 노출하지 않아도 된다.
def find_order_in_legacy(order_id, caller):
    return legacy_repository.load_visible_to(order_id, caller)
```

다음은 **P0-2에서 구현한 등록 인터페이스**다. 수동 wrapper 하나로 입력 이름과 공개 결과를 분명히 한다.

```python
from typing import TypedDict
from a2api import capability, Application  # P0-2 명시적 함수 등록
from a2api import ExecutionContext        # 기존 호스트 context 재사용

class OrderView(TypedDict):
    orderId: str
    orderState: str
    shipmentIds: list[str]

@capability(id="orders.lookup", effect="read")
def lookup_order(orderId: str, *, context: ExecutionContext) -> OrderView:
    """주문 번호로 접근 가능한 주문 상태와 배송 번호를 조회한다."""
    row = find_order_in_legacy(orderId, context)
    return {
        "orderId": row.id,
        "orderState": row.state,
        "shipmentIds": row.shipment_ids,
    }

app = Application([lookup_order])
result = app.invoke("orders.lookup", {"orderId": "ORD-1001"}, context=caller)
```

이 경로의 importer는 개발자가 등록한 함수의 이름·docstring·지원하는 타입을 읽는다. converter는 schema와 callable binding을 만든다. `context`는 호스트 전용 예약 인자라서 모델의 inputSchema에 포함하지 않는다. 지원하지 않는 annotation은 명시적 schema를 요청하고 임의로 성공 처리하지 않는다.

기존 동적 코드 전체의 타입을 자동 복원한 것이 아니다. wrapper의 입출력을 명시해 선택한 경계를 전환한 것이다. 코드를 로드하는 것도 호스트의 명시적인 등록이며, LLM의 파일 경로로 임의 모듈을 import하지 않는다.

## 7. 여러 API를 조립하는 경우

단순 API마다 업무 workflow를 작성하지 않는다. 1:1 변환만 해도 사용할 수 있어야 한다. 주문에서 배송 번호를 얻어 다시 배송을 조회하는 업무는 두 가지로 연결할 수 있다.

### A. 모델이 원자 API를 연결

```text
orders.get → shipmentIds 획득
→ 각 shipmentId로 shipping.get 호출
→ 응답을 사용자에게 설명
```

모델은 두 descriptor와 앞 응답을 보고 인자를 만든다. 관계가 명확하지 않으면 이름이 비슷하다는 이유로 자동 연결하지 않는다. 데이터 중의 지시문은 호출 권한이 아니다.

### B. 개발자가 업무 wrapper를 한 번 제공

업무가 반복된다면 기존 서비스 함수나 작은 wrapper로 `order.shipping_status(orderId)`를 만든다. 아래는 업무 코드의 **설계용 의사 코드**다. client/예외 타입은 새 라이브러리 API가 아니다.

```python
def shipping_status(orderId, *, caller):
    order = legacy_client.get_order(orderId, caller=caller)
    ids = order["shipmentIds"]
    if len(ids) > 10:
        raise UnsupportedRange("이 기능은 배송 10건까지 지원한다")
    rows = []
    for shipment_id in ids:
        shipment = legacy_client.get_shipment(shipment_id, caller=caller)
        if shipment["orderId"] != orderId:
            raise RelationshipError("주문-배송 관계 불일치")
        rows.append({key: shipment[key] for key in
                     ["shipmentId", "status", "estimatedArrival", "asOf"]})
    return {"orderId": orderId, "orderState": order["orderState"], "shipments": rows}
```

이 함수를 이전 절의 명시적 schema/타입 등록 방식으로 노출한다. 그러면 LLM은 주문 번호 하나만 넘기고 런타임/기존 업무 코드가 내부 호출을 수행한다. shipmentIds가 비어 있으면 배송 호출 없이 빈 결과를 반환한다.

기존에 구현한 정적 composition DAG도 같은 업무를 표현할 때 재사용할 수 있다. 그러나 wrapper를 쓸지 DAG를 쓸지는 선택이며 양쪽을 모두 작성하지 않는다. 함수 wrapper의 내부 호출 그래프를 자동 추출했다고 표현하지 않는다.

이 업무 관계는 OpenAPI만으로 완성되지 않는다. ID 매핑, 주문-배송 관계 검사, 결과 필드와 개수 제한을 개발자가 제공해야 한다. 이는 필요한 업무 정의이며 모든 사용자에게 요구할 별도 승인 플랫폼은 아니다.

## 8. 신규 API를 처음부터 a2api로 만드는 경우

신규 API도 위 `@capability`와 명시적 입출력 타입을 작성하는 경로를 사용한다. 레거시 wrapper를 거치지 않고 실제 서비스 구현에 바로 연결하는 점만 다르다.

```text
신규 업무 함수 + 입출력 타입 + 짧은 용도/효과
                    ↓ 동일한 converter
          호출 descriptor + 함수 binding
                    ↓ 동일한 invoke/MCP
                사용자 결과
```

OpenAPI 작성 → 다시 import → review/build를 신규 함수의 필수 절차로 삼지 않는다. 이미 HTTP API 중심으로 개발하는 팀은 OpenAPI 경로를 그대로 사용할 수 있다. 코드 우선과 명세 우선은 같은 호출 형식으로 합류한다.

신규 Java/Go/Rust용 native SDK가 이미 있다는 뜻은 아니다. 첫 코드 등록 구현은 Python의 명시적 함수 경계로 제한하고, 다른 언어는 기존 HTTP 인터페이스를 사용한다. 필요한 언어가 확인되면 동일한 프로토콜에 맞는 얇은 exporter를 추가한다.

## 9. 모두 전환된 뒤 LLM은 어떻게 호출하는가

전환이 끝나면 서버 안에 선택한 API들의 카탈로그·binding·validator가 있다. 이 전체를 prompt에 붙이지 않는다. 사용자/권한에 따라 탐색 대상을 제한하고, 세 개의 공통 MCP 도구를 노출하는 경로를 기본 설계로 유지한다.

| 프로토콜 요청 | 필수 입력 | 반환 | 실행 여부 |
|---|---|---|---|
| discover | 없음; query/limit/cursor는 선택 | catalogVersion, 작은 후보 요약, nextCursor | 업무 API 호출 없음 |
| describe | id, version | catalogVersion, 선택한 경량 capability descriptor | 업무 API 호출 없음 |
| invoke | id, version, catalogVersion, input | status와 검증한 data 또는 구조화 error, 필요한 completeness | 연결한 handler/API 실행 |

requestId는 선택적인 추적 값이다. 별도의 멱등성 보장을 의미하지 않는다. library의 간편 `app.invoke(id, input, context=...)`는 앱 객체가 해당 id의 version/catalogVersion을 선택·고정하는 편의 인터페이스다. LLM/MCP가 보내는 위 wire 요청에서 이를 임의로 생략한다는 뜻은 아니다.

모델이 보내는 input은 입력 schema에 맞는 JSON 객체다. credential/context는 호스트의 호출 인자이며 wire의 업무 input으로 받지 않는다. 요청한 계약이나 현재 카탈로그가 다르면 실행 전에 오류를 반환하고 현재 설명을 다시 사용하도록 한다. 새로운 호환성 분석·자동 배포 절차를 이 확인에 덧붙이지 않는다.

### 9.1 처음 연결할 때

모델이 보는 것은 `a2api.discover`, `a2api.describe`, `a2api.invoke`의 짧은 정의와 고정 envelope다. 모든 API의 input/output/실행 그래프를 도구 목록에 합쳐 넣지 않는다. 상세한 business schema는 선택한 describe에서 받는다.

### 9.2 실제 대화와 도구 메시지 예시

다음은 업무 wrapper가 등록된 **목표 호출 흐름**이며 실제 LLM 성공률 측정이 아니다.

사용자: “ORD-1001 배송이 어떻게 되고 있어?”

**LLM → discover**

```json
{"query":"주문 배송 현황","limit":3}
```

**discover → LLM** — 작은 후보 목록만 반환한다.

```json
{
  "catalogVersion":"example-catalog",
  "capabilities":[
    {"id":"order.shipping_status","version":"0.1.0","summary":"주문 번호로 배송 상태와 예상 도착 시각을 조회한다."}
  ],
  "nextCursor":null
}
```

**LLM → describe**

```json
{"id":"order.shipping_status","version":"0.1.0"}
```

**describe → LLM** — 선택한 항목의 업무 입력·출력·효과·꼭 필요한 제약만 반환한다. 아래는 경량 형식의 완결된 예시다. 실행 DAG나 backend credential은 없다.

```json
{
  "catalogVersion":"example-catalog",
  "capability":{
    "id":"order.shipping_status",
    "version":"0.1.0",
    "summary":"접근 가능한 주문의 배송 상태를 최대 10건까지 조회한다. 예정 도착은 확정 시각이 아니다.",
    "effects":{"kind":"read"},
    "inputSchema":{
      "type":"object",
      "properties":{"orderId":{"type":"string","minLength":1}},
      "required":["orderId"],"additionalProperties":false
    },
    "outputSchema":{
      "type":"object",
      "properties":{
        "orderId":{"type":"string"},
        "orderState":{"type":"string"},
        "shipments":{
          "type":"array","maxItems":10,
          "items":{
            "type":"object",
            "properties":{
              "shipmentId":{"type":"string"},
              "status":{"type":"string","enum":["pending","in_transit","delivered"]},
              "estimatedArrival":{"type":["string","null"]},
              "asOf":{"type":"string"}
            },
            "required":["shipmentId","status","estimatedArrival","asOf"],
            "additionalProperties":false
          }
        }
      },
      "required":["orderId","orderState","shipments"],"additionalProperties":false
    }
  }
}
```

**LLM → invoke**

```json
{
  "id":"order.shipping_status",
  "version":"0.1.0",
  "catalogVersion":"example-catalog",
  "input":{"orderId":"ORD-1001"}
}
```

**서버 내부**: 입력/권한 확인 → 주문 HTTP 조회 → 연결된 배송 조회 → 관계/결과 확인 → 공개 필드만 반환.

**invoke → LLM**

```json
{
  "status":"succeeded",
  "data":{
    "orderId":"ORD-1001",
    "orderState":"shipped",
    "shipments":[
      {"shipmentId":"SHP-501","status":"in_transit","estimatedArrival":"2026-10-29T18:00:00+09:00","asOf":"2026-10-28T15:00:00+09:00"}
    ]
  },
  "completeness":{"complete":true}
}
```

LLM은 이 데이터로 “배송 중이며 예정 도착 시각은 …, 조회 기준 시각은 …”처럼 답한다. 예정값을 확정 도착으로 바꾸거나 실패를 성공으로 설명하지 않는다.

주문 번호가 없으면 사용자에게 필요한 값을 묻는다. 해당 작업/설명을 이미 알고 있고 동일한 catalogVersion이면 호스트가 캐시한 설명으로 바로 invoke할 수 있다. 매번 discover와 describe를 다시 실행하도록 강제하지 않는다. 라이브러리 직접 호출은 고정된 앱 객체가 버전/카탈로그를 고정할 수 있다.

원자 API만 등록했다면 선택 결과는 두 API가 되며, LLM이 주문 응답의 shipmentIds를 사용해 배송 조회를 따로 호출한다. 업무 wrapper를 제공하지 않았는데 wrapper가 자동으로 생겼다고 설명하지 않는다.

### 작은 API 집합에서는

이미 사용할 함수 몇 개를 정한 호스트는 descriptor에서 직접 타입화한 도구를 등록하는 방식도 선택할 수 있다. 이 경우 검색 단계를 생략할 수 있다. 다만 MCP 직접 도구 exporter를 별도 필수 개발 단계로 늘리지는 않는다. 우선 공통 호출 경로와 경량 설명을 완성한다.

## 10. 계약이 원본보다 길어지는 문제: 측정과 수정 방향

### P0-3 이전 코드에서 확인한 사실

- `Capability.describe()`는 전체 `manifest_json`을 반환하고 `Catalog.describe()`도 그 전체를 내보낸다.
- `mcp_schemas.output_schemas()`는 노출 가능한 capability마다 성공 응답 schema를 공통 `invoke`의 `oneOf`에 추가한다. 도구 세 개라는 사실만으로 문맥 비용이 일정해지지 않는다.
- MCP bridge는 같은 결과를 text와 structured content로 제공한다. 모델이 실제 어느 표현을 받는지는 호스트 구현에 달려 있어 토큰이 무조건 두 배라고 단정하지 않는다.

2026-10-29, commit `fc4b40b`에서 compact UTF-8 JSON의 길이를 측정했다. 공백·키 순서 조건은 [측정 기록](evidence/context-audit-2026-10-29.json)에 있다.

| 대상 | 바이트 |
|---|---:|
| 주문·배송 원본 OpenAPI 전체 | 2,028 |
| 현재 전체 shipping capability | 6,990 |
| 현재 describe 응답 | 7,096 |
| 같은 capability의 id/version/summary/inputSchema/outputSchema/effect만 추린 설계 비교본 | 1,356 |
| 현재 MCP tools/list: capability 1개 | 6,995 |
| 현재 MCP tools/list: capability 10개 | 23,420 |
| 현재 MCP tools/list: capability 100개 | 187,760 |

1/10/100개 비교는 같은 schema를 다른 ID로 반복한 합성 카탈로그다. 실제 100개 서비스의 평균 비용이 아니다. 원본 명세와 업무 계약은 정보량·역할이 달라 일반적인 우열 비교가 아니지만, 이번 샘플의 전체 계약이 더 길다는 문제는 확인할 수 있다.

1,356바이트 값은 필드 투영의 크기 비교이며 실제 경량 API 구현 결과가 아니다. 토큰 수·호스트 직렬화·대화 누적량·LLM 성공률·지연을 측정하지 않았다. “토큰 N% 절감”, “정확도 향상” 같은 표현으로 바꾸지 않는다.

### P0-3에서 반영한 것

1. describe 기본값은 agent descriptor로 제한하고 전체 실행 계약은 개발자용 조회에 남긴다.
2. MCP tools/list의 공통 invoke 출력은 고정 envelope로 만들고 모든 business schema를 나열하지 않는다. `data`의 실제 schema는 선택한 descriptor와 서버 validator가 검사한다.
3. discover는 제한된 후보 요약만 반환한다. 카탈로그 전체를 초기 문맥에 넣지 않는다.
4. 결과는 공개한 필드·필요한 근거만 반환한다. UI 전용 표시 설정과 debug 기록은 호스트 경로에서 사용한다.

P0-3은 새 직접 호출 객체의 작은 결과를 유지하고, 기존 Runtime invoke의 근거·표시·stats는 호환을 위해 보존한다. 현재 구현과 새 비용 비교는 [P0-3 사용 안내](13-lightweight-mcp.ko.md)에 있다. 아래 재현 코드는 현재 코드에서는 바뀐 MCP 목록 크기를 출력하며 과거 표는 당시 commit의 기록이다.

공통 invoke의 `input`/`data`가 일반 객체/JSON으로 표현되면 MCP 공통 schema만으로 개별 업무 타입을 알 수 없다. 그래서 선택한 describe와 runtime 검증은 남겨야 한다. 출력 schema를 빼고 검증까지 약화하는 방식으로 줄이지 않는다.

### 측정 재현

아래는 현재 코드에서 그대로 실행할 수 있는 **크기 측정 코드**다. 설계용 `convert` 예시와 다르다. MCP 선택 의존성이 설치된 환경에서 실행하며 외부 API를 호출하지 않는다. 카탈로그 ID를 바꾼 같은 schema의 반복은 크기 증가를 확인하기 위한 합성 자료다.

```python
import json
import anyio
from mcp import Client
from a2api import Catalog, Runtime, compile_contract
from a2api.sample import sample_runtime, TOKENS
from a2api.mcp_bridge import create_mcp_server

def compact_bytes(value):
    return len(json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":")).encode("utf-8"))

runtime = sample_runtime("http://127.0.0.1:1")  # 실제 요청하지 않음
manifest = runtime.catalog.capabilities[0].describe()
view = {key: manifest[key] for key in
        ["id", "version", "inputSchema", "outputSchema"]}
view.update(summary=manifest["intent"]["summary"],
            effects={"kind": manifest["effects"]["kind"]})
print("full/agent projection", compact_bytes(manifest), compact_bytes(view))

async def measure():
    for count in [1, 10, 100]:
        capabilities = []
        for index in range(count):
            item = json.loads(json.dumps(manifest))
            item["id"] = "benchmark.shipping_" + str(index)
            capabilities.append(compile_contract(item))
        copy = Runtime(Catalog(capabilities, allow_samples=True), runtime.adapter)
        server = create_mcp_server(copy, TOKENS["demo-alice"])
        async with Client(server) as client:
            tools = await client.list_tools()
            value = tools.model_dump(mode="json", by_alias=True, exclude_none=True)
            print("tools/list", count, compact_bytes(value))

anyio.run(measure)
```

### 항상 호출 수가 줄어드는 것은 아니다

| 상황 | LLM이 하는 일 | backend 호출 |
|---|---|---:|
| 원자 API를 이미 알고 있음 | 주문 1회 + 배송 2회 tool 호출 | 3 |
| 업무 capability를 처음 찾음 | discover + describe + invoke | 내부 3 |
| 업무 capability 설명이 유효하게 캐시됨 | invoke 1회 | 내부 3 |

처음 찾는 비용과 반복 호출 비용은 다르다. workflow를 서버로 옮겨도 backend 호출 자체가 줄어드는 것은 아니다. 소수 API만 사용하는 경우 a2api 검색 envelope가 오히려 추가 비용일 수 있다. 실제 호스트에서 전체 도구 정의+검색 결과+describe+invoke 결과를 합친 크기를 비교해야 한다.

## 11. 첫 프로토콜 모듈의 완료 범위

**완료란 지원하는 입력을 전환해 공개된 인터페이스로 실제 호출할 수 있다는 뜻이다. 모든 언어·모든 OpenAPI 기능을 자동 지원한다는 뜻이 아니다.**

| 첫 완료에 포함 | 첫 완료의 선행 조건에서 제외 |
|---|---|
| 작은 호출 계약과 공통 오류/결과 | diff·재승인·호환성/버전 정책 자동화 |
| 기존 OpenAPI parser를 사용한 GET/HEAD 간편 연결 | CI, 재배포 자동화, registry 운영 |
| 명시적으로 등록한 Python 조회 함수 | 모든 언어 AST/전체 소스 자동 분석 |
| 입력·응답 검증, host origin/credential/context 연결 | 별도 approval workflow 플랫폼 |
| 메모리 안에서 convert → invoke | 강제적인 중간 파일·snapshot 생성 |
| 경량 discover/describe/invoke와 MCP 연결 | 모든 API의 관계를 자동 추론하는 그래프 엔진 |
| 주문·배송과 기존 큰 명세의 선택 API 호출 예제 | 대형 평가 시스템·실제 LLM 성능 개선 보장 |

첫 단계의 미지원 schema·직렬화는 원인을 보고하고 해당 operation이 실행 가능한 것처럼 만들지 않는다. 기존 `openapi-draft`의 `enabled`만 켜서 기존 검토 규칙을 우회하지 않는다. 경량 계약/노출 연결을 별도 명확한 profile로 검증하고 기존 전체 계약을 사용하는 사용자 경로는 보존한다.

신규 DB/서비스/스케줄러는 이 범위에 필요하지 않다. 프로토콜에 필요하다는 이유만으로 별도의 관리 단계를 추가하지 않는다.

## 12. 이후 개발 판단 기준

개발 순서와 완료 조건은 [개발 계획](03-roadmap-and-evaluation.ko.md)에 한 곳에서 관리한다. 새 기능은 사용자가 그 범위를 요청하거나 현재 핵심 경로를 실제로 막는 문제가 확인되었을 때 다룬다.

- 현재 목표: 사용자가 적은 코드로 전환하고 바로 호출하기.
- 현재 검증: 지원 API의 실제 요청·응답과 LLM에 전달하는 payload 확인.
- 표현 기준: 계획·구현·fixture 검증·실제 LLM 실험을 구분.
- 범위 기준: 작은 문제에 새 승인 단계·배포 체계·평가 플랫폼을 자동 추가하지 않음.
- 계획 변경: 이유와 영향이 필요하며 사용자 지시 없이 다음 목표를 운영 기능으로 바꾸지 않음.

자동 전환 건수나 테스트 개수가 제품 사용성의 증거를 대신하지 않는다. 짧은 시작 예제를 보고 사용자가 자기 API 하나를 실제 호출할 수 있는지 먼저 확인한다.
