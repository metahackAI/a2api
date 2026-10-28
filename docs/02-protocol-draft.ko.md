# a2api 프로토콜 초안

작성일: 2026-10-28 · 제안 버전: `0.1.0-draft.1`

이 문서의 a2api 필드·메서드·상태는 프로젝트 내부 제안이다. 구현·상호운용성·표준 적합성을 검증한 명세가 아니다. 아래 규칙은 구현 시 만족시킬 계약을 설명한다.

조회 전용 MVP의 실제 지원 범위와 제한은 [MVP 실행 안내](04-mvp.ko.md), 구현한 stdio MCP binding은 [MCP 브리지 안내](05-mcp-bridge.ko.md)에 정리했다. 전체 초안과 구현 범위는 구분한다.

## 1. 프로토콜의 범위

프로토콜은 다음 세 부분으로 나눈다.

1. **정적 계약:** capability의 의미·입출력·관계·실행·표시 규칙을 JSON/YAML로 표현한다.
2. **실행 의미:** 권한·상태 검사, 단계 실행, 실패와 재시도, 결과 근거를 정의한다.
3. **binding:** 라이브러리 함수, HTTP, MCP 등에서 이 계약을 전달하는 방법을 정의한다.

공통 직렬화 표현은 JSON이다. 입력·출력 구조에는 [JSON Schema 2020-12](https://json-schema.org/draft/2020-12)를 사용하되, 도메인 식별자·권한·상태 검사는 별도 처리한다. 지원하지 않는 스키마 키워드나 외부 참조를 조용히 무시하지 않는다.

OpenAPI 등에서 가져온 계약은 원래 dialect를 기록한다. nullable·union·discriminator·숫자 범위·직렬화 방식이 변환 중 달라지면 명시적으로 진단한다. 특히 int64, decimal 금액, byte 배열, 날짜, native pointer를 단순 JSON number/string으로 바꾸며 의미를 잃지 않도록 mapping 규칙을 둔다.

## 2. Capability IR의 최소 구성

| 필드 | 역할 | 조건 |
|---|---|---|
| `a2api` | 명세 버전 | 필수 |
| `id`, `version` | 도메인 포함 기능 ID와 계약 버전 | 필수, 실행 시 정확한 버전 지정 |
| `lifecycle`, `enabled` | draft/reviewed와 활성화 상태 | 필수, 미검토 계약은 비활성 |
| `title`, `intent` | 업무 목적·사용할 때·사용하지 않을 때 | 필수 |
| `owner` | 의미와 운영을 책임지는 담당 팀 | 활성화 전 필수 |
| `inputSchema`, `outputSchema` | 업무 입력과 성공/부분 결과의 `data` 구조 | 필수 |
| `contextRequirements` | 호스트에서 주입할 주체·테넌트 등 | 필요한 항목 명시 |
| `effects` | 읽기·변경·외부 전달·민감 데이터 접근 | 필수, 모르면 `unknown` |
| `policy` | 필요한 scope, 객체 권한, 승인 조건 | 필수 |
| `binding` | 원자 operation 또는 composition 참조 | 필수 |
| `execution` | deadline·호출 예산·재시도·실패 규칙 | 필수 |
| `errors` | 오류 코드·복구 가능 행동 | 필수 |
| `presentation` | 입력 해소 및 결과 표시 힌트 | 사용자 노출 기능에 필수 |
| `provenance` | 원본·revision·필드별 근거·검토 정보 | 활성화 전 필수 |
| `examples` | 사용 예, 기대 결과, 비사용 예 | 활성화 전 필수 |

명세 버전, capability 버전, backend API 버전, 카탈로그 snapshot 버전은 별개다. 동작·기본값·권한·단위·실행 효과 변경도 호환성 검토 대상이다. 단순히 JSON 필드가 유지된다고 업무 호환성이 보장되지는 않는다.

## 3. 의미 타입과 값의 출처

JSON Schema에 제안 확장인 `x-a2api-semanticType`을 붙인다. 예를 들어 `sales.OrderId`, `shipping.ShipmentId`를 구분한다. 이 확장을 붙인 것만으로 표준 JSON Schema validator가 의미를 검사하지는 않는다. a2api compiler/runtime의 추가 검사가 필요하다.

값의 출처는 `user`, `context`, `step`, `constant`로 구분한다. 사용자 입력과 모델 출력은 인증 context를 덮어쓸 수 없다. 리소스 handle과 실행 ID는 주체·테넌트에 결부하고, handle을 아는 것만으로 접근을 허용하지 않는다.

서로 다른 시스템의 식별자는 타입 이름·문자열이 같아도 자동 동등 취급하지 않는다. 명시적 crosswalk가 필요하다. 의미 타입이 같은 경우에도 객체 권한과 현재 상태를 다시 검사한다.

## 4. 관계와 composition

관계 제안과 실행 가능한 매핑을 분리한다. 실행용 매핑은 검토한 계약 버전과 근거를 참조한다. 컴파일 시 다음을 확인한다.

- 모든 operation·step·의미 타입 참조가 존재하는가.
- 입력 필수값을 제공하는가. 배열·optional·null을 올바르게 처리하는가.
- ID namespace, 통화·단위·시간대가 맞는가.
- 선행 조건과 branch의 모든 경로가 실행 가능한가.
- 순환 의존성이 없는가. fan-out과 총 호출 수가 유한한가.
- 원자 단계보다 전체 capability의 효과·권한을 약하게 선언하지 않았는가.

초기 composition은 고정 DAG와 상한이 있는 `foreach`를 지원하는 방향으로 설계한다. 동적 코드 실행, 임의 URL, 무제한 반복은 포함하지 않는다. 복잡한 workflow는 검토한 Arazzo 문서나 기존 업무 서비스에 위임한다.

예시의 매핑은 `{from, step?, pointer}` 형식이다. `from`은 `input`, `step`, `item`, `context`, `literal` 중 하나이며, `pointer`는 JSON Pointer다. `step`은 `from: step`일 때 필요하다. 상수는 `from: literal`과 `value`로 표현한다. 문자열을 코드나 템플릿으로 실행하지 않는다. 필드가 없으면 매핑 오류이며 `null`과 구별한다.

`foreach` 결과 순서는 입력 순서를 유지한다. 동시 실행 수·배열 길이·총 호출 예산을 모두 제한한다. 이 초안의 예시는 `failureMode: stop`으로 하나의 필수 단계라도 실패하면 전체 성공을 반환하지 않는다. 부분 결과가 필요한 capability는 별도 부분 결과 스키마와 집계 규칙을 명시해야 한다.

## 5. 실행 전후의 책임

호출마다 아래 순서를 적용한다.

1. caller의 인증 주체와 테넌트를 호스트 context로 확정한다.
2. 요청한 capability 버전·카탈로그 snapshot·활성 상태를 확인한다.
3. 입력 구조와 의미 타입, scope, 객체 권한, 현재 상태, 승인 필요 여부를 확인한다.
4. 전체 계획과 각 단계의 deadline·호출 수·데이터 전달 범위를 검사한다.
5. 승인한 binding으로만 backend를 호출하고 실행 기록을 남긴다.
6. 단계별 응답 구조·성공 조건·요청/응답 식별자 일치를 확인하고 후속 단계의 권한·상태를 다시 확인한다.
7. 결과를 검증·최소화·마스킹하고 근거·완전성·표시 모델을 반환한다.

예를 들어 주문에서 배송 ID를 얻었다면, 배송 조회의 객체 권한과 주문-배송 관계를 확인한다. 단지 앞 API가 ID를 반환했다는 이유로 다음 시스템 접근을 허용하지 않는다. 통합 서비스 계정을 쓰더라도 업무 사용자 권한을 보존하는 정책이 필요하다.

문서의 `effects`는 선언이고, 테스트·검토 근거 및 backend 정책으로 뒷받침해야 한다. HTTP 메서드만 보고 부작용이나 멱등성을 단정하지 않는다. 입력·출력 문구는 데이터이며 런타임 정책을 바꾸는 명령이 아니다.

## 6. 검색·설명·실행 인터페이스

아래 이름은 라이브러리 API와 binding의 공통 의미다. 아직 구현된 API가 아니다.

| 메서드 | 입력 핵심 | 반환 핵심 |
|---|---|---|
| `discover` | 업무 문구, 허용된 filter, cursor | 권한별 capability 요약, version, 적합 이유, cursor |
| `describe` | ID, version | 전체 스키마, 사용 조건, 효과, 관계, 예제 |
| `invoke` | ID, version, catalogVersion, input, requestId | 결과 envelope 또는 명시적 추가 입력·승인 요구 |
| `getExecution` | executionId | 실행 상태와 허용된 범위의 결과 |
| `cancelExecution` | executionId | 취소 요청 접수·가능 여부와 실제 상태 |

요약 검색 결과와 상세 계약을 함께 유지한다. 기본 탐색은 단계적으로 진행하되, 호스트가 지원하면 선택한 capability의 타입화된 도구를 직접 등록할 수 있다. 단일 `invoke` 방식의 모델 정확도와 개별 도구 방식의 정확도를 비교한다.

`requestId`는 추적 식별자다. 명시적 멱등성 계약이 없는 호출에서 중복 실행 방지를 보장하지 않는다. 실행 인자가 바뀌면 동일 요청의 재전송으로 취급하지 않는다.

### MCP binding

MCP에는 고정 도구 `a2api.discover`, `a2api.describe`, `a2api.invoke`, 필요 시 실행 조회·취소 도구를 노출하거나, 배포 시 선택한 capability별 도구를 노출할 수 있다. 어느 쪽이든 런타임은 실제 업무 입력·출력을 검증한다.

카탈로그 변화와 인증에 따른 차이는 처리하되, 대화 맥락에 따라 `tools/list`를 임의로 바꾸는 방식으로 단계적 공개를 구현하지 않는다. 상세 검색은 discovery 도구의 결과 또는 호스트 측 선택으로 처리한다. [MCP 2026-07-28 Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)의 목록 규칙에 맞춰 adapter를 구현하고 버전을 고정해 검증한다.

MCP `inputSchema`에는 업무 인자, `structuredContent`에는 결과 envelope를 연결하고, `outputSchema`는 envelope 전체를 기술한다. a2api 계약의 `outputSchema`는 envelope 내부 `data`만 기술하므로 bridge가 감싸는 스키마를 생성해야 한다. 지원하지 않는 schema 기능은 변환 오류로 보고한다.

MCP의 annotation은 호스트에 주는 힌트이며 a2api의 실제 권한·승인·재시도 집행을 대체하지 않는다. HTTP 인증과 downstream 자격 증명도 구분한다. [MCP Authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization) 및 [Security Best Practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)를 참고한다.

## 7. 결과와 비동기 상태

결과 envelope 예시는 다음과 같다. 주문·배송·시간·버전은 가상 값이다.

```json
{
  "capability": "order.shipping_status",
  "version": "0.1.0",
  "catalogVersion": "demo-catalog-1",
  "executionId": "exec-demo-001",
  "status": "succeeded",
  "data": {
    "orderId": "ORD-1001",
    "orderState": "shipped",
    "shipments": [
      {
        "shipmentId": "SHP-501",
        "status": "in_transit",
        "estimatedArrival": "2026-10-29T18:00:00+09:00",
        "asOf": "2026-10-28T15:00:00+09:00"
      }
    ]
  },
  "completeness": {"complete": true, "scope": "all shipments linked to this order"},
  "evidence": [
    {"step": "order", "source": "demo-orders", "observedAt": "2026-10-28T15:00:00+09:00"},
    {"step": "shipments", "source": "demo-shipping", "observedAt": "2026-10-28T15:00:00+09:00"}
  ],
  "presentation": {"view": "table", "locale": "ko-KR"}
}
```

`status` 후보는 다음처럼 구분한다.

| 상태 | 의미 |
|---|---|
| `requires_input` | 실행 전에 모호한 대상·누락 값 해소가 필요 |
| `requires_approval` | 해당 효과에 대해 정책상 필요한 승인이 없음 |
| `accepted`, `running` | 접수·처리 중이며 업무 완료 아님 |
| `succeeded` | 계약의 성공 조건을 확인 |
| `failed` | 실패를 확인, 관측한 효과와 복구 정보를 반환 |
| `partial` | 일부 결과·효과만 확인, 실패·성공 항목을 각각 표시 |
| `unknown` | timeout 등으로 실제 효과를 확정할 수 없음 |
| `cancelled` | 취소 완료를 확인, 이미 발생한 효과는 별도 표시 |

위 상태는 업무 상태인 `shipped`, `cancelled_order` 등과 별개다. `unknown`은 성공/실패로 강제 변환하지 않고 reconciliation으로 갱신한다. 취소 요청이 접수되었다는 사실과 실행이 취소되었다는 사실도 구분한다.

초기 MVP는 동기 조회부터 구현한다. 장기 실행 binding에서는 `executionId` 조회와 제한한 polling을 제공하고, callback·이벤트 완료 통지는 후속 범위로 둔다. 외부의 비동기 작업 ID와 내부 실행 ID의 관계를 기록한다.

## 8. 변경 작업의 prepare / commit

모든 API에 별도 prepare를 강제하지 않는다. 되돌리기 어렵거나 효과 범위를 사용자에게 보여줘야 하는 작업에서 사용할 공통 패턴으로 정의한다.

예를 들어 주문 취소를 준비하면 다음 정보를 반환한다.

- 실제 대상 주문, 현재 버전, 취소와 환불 등 발생할 효과.
- 적용 인자·금액·통화·수수료·수신 대상.
- 유효기간, 조건, 실행할 계약 버전, 서버에 저장한 `proposalId`.

호스트는 필요한 경우 이 구체적인 내용을 사용자에게 보여주고, 신뢰할 수 있는 승인 채널의 결과를 서버에 전달한다. 모델이 만든 `approved: true`나 문장으로 승인을 증명하지 않는다.

승인 기록은 주체·테넌트·대상·정규화한 인자·효과·계약 버전·유효기간에 결부한다. commit에서 이 값과 현재 backend 조건을 다시 확인한다. 대상·금액·수신자 등이 바뀌면 이전 승인을 재사용하지 않는다.

`prepare`가 backend를 잠그거나 상태를 예약한다면 그 자체의 효과·만료·해제 규칙도 선언해야 한다. 단순 미리보기와 예약 작업을 같은 의미로 취급하지 않는다. 승인과 무관하게 backend의 원자적 조건 검사 또는 적절한 동시성 제어가 필요하다.

## 9. 멱등성·재시도·실패 복구

멱등성 선언은 `none`, `backend_keyed`, `naturally_idempotent`, `unknown` 등 실제 근거를 구분한다. 변경 operation의 자동 재시도는 검증한 계약이 허용하는 경우에만 수행한다. [HTTP Semantics RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)의 재시도 규칙을 기본 근거로 삼는다.

backend가 키 기반 멱등성을 제공한다면 키의 scope를 주체·테넌트·operation·계약 버전과 결부하고, 같은 키의 다른 payload는 거부한다. 키의 보관 기간과 재전송 결과도 계약에 명시한다.

gateway의 실행 로그만으로 외부 시스템의 exactly-once 실행을 보장하지 않는다. backend 변경 성공 직후 gateway 기록 전에 장애가 날 수 있기 때문이다. 이 구간에는 backend 멱등 키, 결과 조회, 업무 고유 키 또는 상태 대조가 필요하다.

읽기 요청도 호출 예산·deadline·rate limit 안에서만 재시도한다. deadline은 모든 단계·재시도·대기 시간을 포함하고, 총 호출 수는 실제 시도 횟수를 센다. 일반 timeout을 임의로 재시도 가능한 업무 실패로 바꾸지 않는다.

보상은 별도 업무다. 이미 보낸 메일, 출고, 일부 환불처럼 원상 복구할 수 없거나 추가 효과가 있는 경우가 있다. 각 단계의 성공·실패·불명 상태와 보상 결과를 보존하고 필요한 후속 조치를 표시한다.

## 10. 오류 계약

HTTP binding에서는 [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html)의 Problem Details를 활용하고, 다른 binding에서는 대응하는 구조로 전달한다. 업무 오류의 확장 필드로 `code`, `executionId`, `effectState`, `recovery`를 제안한다.

| 코드 예 | 처리 |
|---|---|
| `INPUT_REQUIRED`, `AMBIGUOUS_ENTITY` | 누락 필드·허용된 후보를 반환하고 실행 보류 |
| `PERMISSION_DENIED` | 우회 도구를 제안하지 않고 접근 범위 안내 |
| `PRECONDITION_FAILED` | 최신 상태 조회 또는 새 proposal 필요 |
| `SCHEMA_MISMATCH`, `CONTRACT_DRIFT` | 잘못된 경로를 중지하고 계약 재검증 |
| `RATE_LIMITED`, `DEADLINE_EXCEEDED` | deadline·재시도 계약 내에서만 복구 |
| `PARTIAL_FAILURE` | 확인한 결과와 실패한 항목을 분리 |
| `EFFECT_UNKNOWN` | 자동 반복 대신 상태 대조·결과 조회 |

오류 메시지에 자격 증명·전체 stack trace·불필요한 개인정보를 넣지 않는다. 오류에서 제안하는 다음 capability도 caller가 볼 수 있고 실행할 수 있는 후보로 제한한다.

## 11. 사용자 표시 계약

`presentation`은 웹 UI 구현을 고정하지 않는 선언적 힌트다. 지원하지 않는 호스트는 스키마와 라벨을 이용해 텍스트로 표현한다.

입력은 라벨·설명·예시·단위·허용값·선택 후보를 제공한다. 후보가 여러 개인 경우 사용자에게 구분 가능한 정보만 보여주고 선택을 받는다. 주문 번호처럼 명확한 입력은 불필요한 확인 없이 처리할 수 있다.

결과는 카드·표·목록 등의 view, 표시할 JSON Pointer, 상태 라벨, 시간대와 단위를 정의한다. 예시에서 `rows`와 `contextFields`는 `data` 기준이고 `columns[].pointer`는 각 행 기준이다. 예측값은 예측으로 표시하고, 값 없음·접근 제한·아직 미조회·부분 실패를 구별한다. 데이터가 페이지 일부이면 전체 결과처럼 요약하지 않는다.

출처와 기준 시각은 구조화 결과에 남긴다. 모델이 만든 설명은 이 구조화 사실에 근거해야 한다. 숨김 필드·모델 비공개 필드는 전송 전에 서버가 제거하고, 사용자에게만 필요한 민감 정보는 별도 권한이 있는 UI 경로에서 전달한다.

## 12. 활성화와 적합성

`draft → reviewed → enabled → deprecated/disabled`의 수명주기를 둔다. `effects: unknown`, 해석 불가능한 스키마, 미검토 실행 매핑, 누락한 필수 policy는 활성화 실패 조건이다. 조회 기능도 민감 데이터·객체 권한을 검증해야 한다.

manifest와 실행 registry에는 자격 증명 값이나 임의 실행 코드를 넣지 않는다. 서비스 주소·credential reference는 운영자가 관리하는 deployment profile에서 해석한다. 검색 결과가 backend 주소를 지정하거나 새로운 권한을 만드는 일은 허용하지 않는다.

명세 적합성, backend 계약 적합성, 에이전트 업무 성공률은 서로 다른 검사다. 예시 JSON이 파싱된다는 사실만으로 이 세 가지를 통과했다고 판단하지 않는다.
