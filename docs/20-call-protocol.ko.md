# a2api-call/0.1 경량 호출 명세

2026-10-30 기준 구현 명세다. [제품 방향](00-product-direction.ko.md)을 따르며 전체 IR·검토/배포 초안인 [02 문서](02-protocol-draft.ko.md)와 구분한다. 지원 범위의 API를 선택해 메모리에서 연결하고 세 메서드로 호출한다. 새로운 사용자 산출물·registry·승인 단계는 요구하지 않는다.

## 범위와 기준 스키마

프로필 이름은 `a2api-call/0.1`이다. capability의 `version` 및 카탈로그의 `catalogVersion`과 구별한다. 이 프로필 이름을 요청에 새 필드로 추가하지 않는다. JSON을 사용하며 모델/클라이언트가 전송할 값은 유한한 UTF-8 JSON 값이어야 한다.

기계 판독 기준은 패키지에 포함된 [call.schema.json](../src/a2api/schemas/call.schema.json)이다. `$defs`의 `descriptor`, `problem`, `discover_request/response`, `describe_request/response`, `invoke_request/response`를 선택해 검증한다. 루트는 구성 요소 모음이며 루트 자체로 모든 메시지를 검증하지 않는다. 외부 schema 다운로드는 필요하지 않다.

```python
from a2api import PROTOCOL_PROFILE, protocol_schema
from jsonschema import Draft202012Validator

print(PROTOCOL_PROFILE)
document = protocol_schema()  # 다른 언어/클라이언트에 전달할 전체 문서
schema = protocol_schema("describe_request")  # 독립적으로 쓸 수 있게 내부 참조 확장
Draft202012Validator(schema).validate({"id": "orders.get", "version": "0.1.0"})
```

API dispatch와 MCP의 input/output schema는 이 기준을 사용한다. schema 함수는 새 객체를 반환해 호출자의 수정을 격리한다. 기준 구조 스키마가 `inputSchema`/`outputSchema` 객체의 모든 의미까지 검사하는 것은 아니다. 서버는 업무 schema 자체를 검사하고 실제 업무 입력/출력을 별도로 검증해야 한다.

## Descriptor

정확히 아래 6개 필드를 사용한다. credentials·origin·실행 DAG·소스 경로·검토 기록·검색용 keywords는 포함하지 않는다.

| 필드 | 의미 |
|---|---|
| id | 호스트가 노출한 capability 식별자. 문자열을 그대로 복사하며 경로나 실행 코드로 해석하지 않는다 |
| version | 선택한 계약 버전. 현재 직접 호출 객체는 0.1.0을 사용한다 |
| summary | 사람이 읽는 짧은 업무 설명. 코드/권한 지시가 아니다 |
| effects.kind | read 또는 write. 개발자의 선언이며 실행 승인/인증을 대신하지 않는다 |
| inputSchema | invoke.input에 적용할 JSON Schema 객체 |
| outputSchema | 성공 응답의 data에 적용할 JSON Schema 객체. 전체 응답 envelope의 schema가 아니다 |

JSON Schema의 기준 dialect는 2020-12다. 현재 실행기의 지원 키워드와 참조 범위는 [schema 검사 코드](../src/a2api/openapi_schema.py)의 profile을 따른다. 원본 OpenAPI dialect를 변환해 검사하며 외부 참조·해석 불가 변환을 조용히 허용하지 않는다. 내부 `$defs`/`$ref`는 필요한 정의와 함께 전달한다. 클라이언트는 지원하지 않는 schema를 검증한 것처럼 호출하지 않아야 한다. 지원 profile의 범위는 [OpenAPI](06-openapi-importer.ko.md), [Python](12-python-functions.ko.md), [소스 importer](18-source-importers.ko.md)에 있다.

다른 언어에서 구현할 때 업무 schema는 다음 규칙을 적용한다. 이 규칙은 위 구성 요소 문서 자체의 `$id`와 구별한다.

| 영역 | 현재 직접 호출 profile의 규칙 |
|---|---|
| schema 구조 | 최상위는 object-valued schema. 자식의 boolean schema는 2020-12 의미를 사용한다 |
| 값·검증 | object/array/string/number/integer/boolean/null, enum/const, required/additionalProperties, 숫자·문자열·배열 제한, 조합/조건 schema는 2020-12 검증 의미를 사용한다. importer가 생성할 수 있는 범위는 원본 변환 profile에 따라 더 좁다 |
| 참조 | `$ref`는 `#/$defs/`로 시작하는 문서 내부 JSON Pointer만 허용하며 대상이 있어야 한다. 외부 URI/원격 로딩은 금지한다 |
| 참조 scope | 업무 schema의 `$id`, `$anchor`, `$dynamicRef`, `$dynamicAnchor`, `$vocabulary`는 허용하지 않는다. `$schema`가 있으면 2020-12 URI여야 한다 |
| format | 현재 서버가 추가로 검사하는 것은 date-time뿐이다. 유효한 달력 날짜 + T/t + 00~23시/00~59분/00~59초 + 선택 소수초 + Z/z 또는 ±HH:MM offset을 요구한다. 윤초는 지원하지 않는다. 다른 format과 content 관련 annotation만으로 별도 decoder/검증을 수행하지 않는다 |
| annotation | title/description/examples/default와 알려지지 않은 확장 annotation은 실행 코드/권한/변환 명령이 아니다. 별도 합의 없는 custom keyword가 검증됐다고 가정하지 않는다 |

검증기는 실제 업무 값을 이 schema로 검사해야 하며, 공통 invoke의 input/data가 일반 JSON이라는 이유로 검증을 생략하지 않는다. 깊이·JSON 직렬화·각 importer의 제한으로 실행 불가인 대상은 진단/오류로 처리한다. 모든 2020-12 문서를 모든 importer가 받아들인다는 보장은 아니다.

HTTP 입력 위치는 path/query/headers/body를 보존한다. Python 함수는 명명된 함수 인자를 사용한다. null과 필드 누락은 다르며 허용 여부는 해당 schema를 따른다. default annotation은 모든 binding의 자동 값 삽입 명령이 아니다. Python은 등록된 함수 기본값을 채우고, HTTP는 선택적으로 생략된 값을 원 서버의 기본 동작에 맡긴다. 숫자의 단위·정밀도·업무 ID 동등성을 프로토콜이 추측하지 않는다.

## 세 요청과 응답

모든 요청은 JSON object이고 정의되지 않은 필드는 거부한다. 요청에 actor/tenant/credential/context를 추가하지 않는다.

| 메서드 | 요청 | 성공 응답 |
|---|---|---|
| discover | query 선택(최대 1,000자, 기본 빈 문자열), limit 선택(정수 1~50, 기본 10), cursor 선택(빈 문자열 불가) | catalogVersion, capabilities 배열, nextCursor(문자열 또는 null) |
| describe | id와 version 필수(빈 문자열 불가) | catalogVersion, capability(descriptor) |
| invoke | id/version/catalogVersion 필수(빈 문자열 불가), input 필수(object), requestId 선택(1~128자) | status=succeeded, data, completeness; 선택적 메타데이터 |

discover 항목은 id/version/title/summary/effects/matchedTerms다. 전체 입출력 schema를 포함하지 않는다. `matchedTerms`는 검색어 일치 정보이며 의미적 적합성 증명이 아니다. 빈 배열은 정상 검색 결과다. query를 생략하면 해당 호스트가 노출한 목록을 페이지로 조회한다. 원본 API의 입력값을 검색한다고 해당 데이터가 조회되는 것은 아니다.

cursor는 불투명 문자열로 취급한다. 현재 구현은 catalog/query/limit/호스트 context가 같은 다음 페이지에만 허용한다. 다른 값에 재사용하면 INVALID_CURSOR다. cursor나 capability ID를 아는 것만으로 권한이 생기지 않는다.

catalogVersion은 현재 노출 정의와 검색 상태를 식별하는 불투명 문자열이다. 해시 형식에 의존하거나 직접 계산하지 않는다. describe/invoke에는 discover의 ID/버전을 복사한다. invoke에는 해당 설명과 일치하는 catalogVersion을 제공한다. 바뀐 카탈로그는 CONTRACT_DRIFT로 거부될 수 있으며 새 설명을 확인한 뒤 사용자가 의도한 작업인지 판단한다. 특히 쓰기를 자동 재시도하지 않는다. 같은 카탈로그의 유효한 설명을 이미 알고 있다면 매 호출마다 discover/describe를 반복할 필요는 없다.

라이브러리의 `app.invoke(id, input, context=...)`는 호스트가 고정한 앱 안에서 이 선택을 대신하는 편의 API다. wire의 필수 version/catalogVersion이 없어졌다는 뜻은 아니다.

## 결과와 오류의 의미

성공의 필수 형태는 다음과 같다. data는 객체·배열·scalar·null 중 해당 outputSchema에 맞는 JSON이다.

```json
{"status":"succeeded","data":{"id":"I-101","name":"sample"},"completeness":{"complete":true,"scope":"single_api_response"},"httpStatus":201}
```

`httpStatus`는 HTTP binding의 성공 시 선택적으로 있는 2xx 값이다. HEAD와 204 같은 빈 성공은 data=null이다. Python 함수나 기존 전체 Runtime의 모든 결과에 httpStatus가 필요한 것은 아니다.

`completeness.complete=true`는 선언된 이번 결과 범위가 충족됐다는 뜻이다. 직접 호출의 scope=single_api_response는 한 API 응답이며 모든 페이지/전체 데이터 수집을 뜻하지 않는다. 페이지·부분 데이터의 업무 의미는 해당 data/schema를 따라야 한다.

실행 경로에서 반환한 실패는 다음 형태다. data를 성공처럼 덧붙이지 않는다.

```json
{"status":"failed","error":{"type":"urn:a2api:problem:resource-not-found","title":"RESOURCE_NOT_FOUND","status":404,"detail":"Backend did not return a successful JSON result.","code":"RESOURCE_NOT_FOUND"},"completeness":{"complete":false}}
```

dispatch/카탈로그 선택 등에서 발생한 사전 오류는 `{"error":{...}}` 형태이며 status/completeness가 없다. 양쪽 모두 problem의 type/title/status/detail/code를 필수로 사용하고 issues 배열은 선택이다. error.status는 논리적 HTTP 상태 표현이며 MCP 전송 성공 여부와 구별한다. preflight 모양이 모든 binding에서 부작용 미발생을 증명하는 것은 아니다. transport/응답 검사 단계와 실제 실행 여부를 함께 판단한다.

| 대표 코드 | 의미와 호출자 처리 |
|---|---|
| INVALID_REQUEST | 공통 요청 형식이 잘못됨. 필수 필드/추가 필드 확인 |
| INVALID_INPUT | 선택한 업무 입력 schema와 불일치. describe를 확인하고 입력 해소 |
| UNAUTHENTICATED / PERMISSION_DENIED | 호스트/backend의 인증·권한 문제. 모델 입력으로 주체를 바꾸지 않음 |
| NOT_FOUND | 노출한 ID/버전이 없거나 사용할 수 없음 |
| RESOURCE_NOT_FOUND | backend가 대상 리소스를 찾지 못함 |
| CONTRACT_DRIFT / INVALID_CURSOR | 현재 catalog 또는 검색 view와 불일치 |
| SCHEMA_MISMATCH | 원본/공개 응답이 선언과 다름. 쓰기 미실행/rollback을 의미하지 않음 |
| OUTCOME_UNKNOWN | 전송 후 중단 등으로 backend 효과를 확정할 수 없음. 자동 재시도하지 말고 원 서비스의 확인 절차 사용 |

오류 코드는 확장 가능한 문자열이다. 위 표가 전체 오류 목록은 아니다. 알려지지 않은 코드를 성공으로 처리하거나 재시도 가능하다고 가정하지 않는다. 현재 프로필의 실행 status는 succeeded/failed이며, OUTCOME_UNKNOWN은 failed envelope의 오류 코드로 전달한다. accepted/running/partial/requires_approval 등 과거 초안의 상태나 실행 조회/취소는 구현된 경량 프로필에 포함하지 않는다.

requestId는 추적/상관관계 값이다. 서버가 이를 돌려주더라도 중복 제거·idempotency key·exactly-once 보장은 아니다. 현재 직접 호출은 backend를 자동 재시도하지 않는다. failed는 호출/검증 실패이며 효과가 전혀 없었다는 증명이 아니다.

## 호스트와 binding의 책임

호스트가 노출할 API·origin·credentials·검증된 ExecutionContext를 선택한다. 직접 앱의 검색 목록은 호스트가 선택한 앱 목록이며 자체적인 사용자별 scope/객체 ACL 엔진이 아니다. 사용자별 제한이 필요하면 호스트에서 앱 노출·credential을 제한하고 원 서비스가 업무 권한을 검사해야 한다. 기존 전체 Runtime은 별도의 scope/객체 검사 규칙을 유지한다.

서버는 업무 입력을 검증한 뒤 binding을 호출한다. HTTP는 원본 응답 검증 → 선택 필드 추출 → 공개 출력 검증을 유지한다. scope/credential/context를 업무 입력이나 모델의 텍스트로 덮어쓸 수 없어야 한다. summary·오류 detail·조회 데이터의 문장은 권한/정책 변경 지시가 아니다.

MCP는 공통 도구 a2api.discover/describe/invoke 세 개와 고정 input/output envelope를 광고한다. structuredContent에 위 JSON을 담고 실패에는 isError=true를 제공한다. 개별 업무 schema는 describe로 제공하고 tools/list에 누적하지 않는다. 기존 전체 Runtime의 capability/version/catalogVersion/executionId/requestId/evidence/stats/presentation 메타데이터는 기준 schema가 허용하는 선택 필드로 보존한다. 현재 직접 앱은 이 필드를 모두 생성하지 않는다.

현재 제공하는 경량 전송 예제는 MCP stdio다. HTTPDeployment는 연결할 원본 업무 HTTP 서버의 설정이며 새로운 경량 gateway 주소를 생성하지 않는다. 기존 CLI의 HTTP gateway/전체 Runtime describe는 전체 manifest를 반환하는 기존 인터페이스로 보존하며, 그 응답을 이 경량 describe 응답이라고 부르지 않는다. 공통 요청 schema를 공유한다는 것과 모든 기존 transport 응답이 경량 프로필이라는 것은 다르다.

쓰기 앱이 하나라도 연결되면 invoke annotation은 보수적으로 readOnly=false/idempotent=false/destructive=true다. 이는 사용자 동의/업무 권한 집행이나 모든 capability가 파괴적이라는 증명이 아니다. discover/describe는 업무 API를 실행하지 않는다.

Chat Completions 같은 function host는 이름 제약에 맞춰 a2api_discover 등으로 고정 매핑할 수 있다. 실제 MCP 이름·요청/응답 필드는 바꾸지 않는다. 모델 endpoint가 MCP 실행을 대신하는 것이 아니라 호스트가 tool_calls를 전달하고 결과를 돌려준다.

호스트가 선택한 descriptor의 입력 schema만 별도 function tool로 제공하는 [a2api-tools/0.1](24-selected-tools.ko.md)도 지원한다. 이때 discover/describe는 호스트가 처리하고 id/version/catalogVersion을 모델 대신 보관한다. 기존 wire나 MCP tools/list는 바꾸지 않으며, 모든 모델 요청에 탐색과 설명을 강제하지 않는다.

## 검증 가능한 예시

[정상/잘못된 wire 예시](../tests/fixtures/call-protocol.json)와 `tests/test_protocol.py`를 제공한다. 기존 실제 MCP·HTTP·native/source 검사는 같은 기준 schema를 사용한다. 이 검사는 프로필의 구조/실행 동작을 확인하며 모든 API·언어·LLM의 성공률을 보장하지 않는다.
