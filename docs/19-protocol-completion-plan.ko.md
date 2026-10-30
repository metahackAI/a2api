# 경량 프로토콜 마무리: 확정 개발 범위

작성일: 2026-10-30. 기준은 [현재 제품 방향](00-product-direction.ko.md)이다. 사용자 요청에 따라 아래 세 작업만 1 → 2 → 3 순서로 구현하고 검증한다. 이 문서에서 아직 완료하지 않은 API·명령은 구현 예정이며 사용법은 각 결과 문서에서 확정한다.

## 1. 현재 경량 호출 계약을 기준 명세로 확정

목표: 기존 요청/응답을 바꾸지 않고 다른 언어의 클라이언트가 독립적으로 구현할 수 있는 명세와 기계 판독 스키마를 제공한다.

- `docs/20-call-protocol.ko.md`: `a2api-call/0.1`의 범위, 6개 descriptor 필드, discover/describe/invoke, JSON Schema 범위, defaults/null/누락, cursor/catalogVersion, context·인증 책임, 성공·사전 오류·실행 실패를 정의한다.
- `requestId`는 추적용이며 멱등성을 보장하지 않는다. `OUTCOME_UNKNOWN`은 효과가 확정되지 않은 오류다. failed/응답 검증 실패를 backend rollback으로 해석하지 않는다. completeness는 조회한 응답 범위이며 전체 페이지 수집 성공이 아니다.
- `src/a2api/schemas/call.schema.json`과 `src/a2api/protocol.py`: 실행과 공개 문서가 공유하는 요청·응답·descriptor의 기준 스키마를 제공한다. 구조 스키마와 실제 업무 schema 검증을 구분한다.
- `api.input_schema`, `mcp_schemas.output_schemas`는 기존 함수·인자와 wire 형식을 유지하며 기준 스키마를 사용한다. 전체 manifest Runtime의 추가 결과 필드는 기존 허용 범위를 유지한다.
- `tests/fixtures/call-protocol.json`, `tests/test_protocol.py`: 정상·잘못된 wire 예제, 기존 형태 일치, 패키지 접근, 기존 실제 MCP 교환을 검사한다. CI나 별도 사용자 검토/빌드 명령은 추가하지 않는다.

완료 기준: 기존 wire 형태를 보존하며, 공개 JSON Schema와 문서만으로 요청·응답의 필드/의미를 알 수 있고 기존 MCP 검사도 같은 스키마를 사용한다.

## 2. 설명과 검색용 metadata를 작은 선택 설정으로 보완

목표: 명시한 업무 표현으로 API를 찾도록 하되 전체 schema를 공통 도구 목록에 넣지 않는다.

- `conversion.py`에 선택적 `summary`, `keywords`를 추가한다. 미지정 시 기존 설명과 동작을 유지한다. `native.py`는 기존 summary와 선택적 keywords를 제공하되 Python 함수는 read 전용을 유지한다.
- importer가 이미 읽은 OpenAPI 설명/태그와 source 제목을 서버 검색에 재사용한다. 새로운 언어 분석·주석 의미 추론·LLM 설명 생성은 추가하지 않는다.
- 검색 metadata는 메모리 안의 호스트 정보로 보관한다. keywords는 descriptor/MCP tools/list의 새 필드가 아니다. summary는 기존 필드의 값만 바꾼다.
- `mcp_application.py`의 기존 문자열 검색·정렬·페이지 제한을 사용한다. 검색용 metadata 변경도 카탈로그/cursor를 구분한다. vector DB, 번역/의미 검색 서비스, 자동 전체 목록 fallback은 추가하지 않는다.
- `examples/source-http/application.py`에 작은 한국어 설명/검색어를 명시한다. 검증 비교를 위한 기존 설명 모드는 예제 옵션으로 보존한다. API 선택·효과·응답 필드·입출력 검증은 유지한다.
- `tests/test_discovery_metadata.py`에서 한국어 검색·순위, 미등록 검색어의 빈 결과, 잘못된 설정, 숨겨진 metadata·도구 목록의 고정성, 카탈로그/cursor 변경, Python/OpenAPI/source 경로를 검사한다. 사용법은 `docs/21-discovery-metadata.ko.md`에 기록한다.

완료 기준: 등록한 한국어 표현으로 해당 capability를 찾는다. 검색어·전체 업무 schema가 공통 도구에 누적되지 않는다. 미등록 데이터값이나 임의 의미까지 검색된다고 주장하지 않는다.

## 3. 저장소만 받아 재현 가능한 시작·모델 연결 예제

목표: 현재 로컬 artifacts에 있는 검증 경험을 작고 공개적인 예제로 제공한다. 새로운 agent SDK/관리 서비스는 만들지 않는다.

- `examples/model-client/client.py`: 설정한 Chat Completions 호환 endpoint/model과 신뢰하는 MCP 실행 명령을 연결한다. 실제 tools/list의 3개 도구를 function 이름에 고정 매핑하고 JSON 인자를 그대로 MCP로 전달한다.
- 모델 URL/ID는 인자 또는 환경 설정으로 제공한다. 회사 hostname·토큰은 코드에 넣지 않는다. 선택적 인증은 환경 변수에서만 읽고 결과/오류에 credential과 원시 reasoning을 저장하지 않는다.
- 실행 횟수·시간·응답 크기를 제한한다. 실패를 기록하고 인자 보정·자동 재시도·다른 모델 fallback을 하지 않는다. 사용자에게 어떤 데이터가 모델에 전달되는지 설명한다.
- `examples/model-client/verify_sources.py`와 고정 시나리오 자료: 기존 Spring·Go·Rust 실제 서버/stdio 예제를 재사용한다. 기존 7개 한국어 질문, 동적 생성 ID 재사용, GET/HEAD/POST/PUT/PATCH/DELETE, 201/204/404, ID 없는 삭제의 무호출을 검사한다. 기대값은 모델 prompt에 넣지 않는다.
- 기존 로컬 모델 결과(7개 질문/24 invoke/빈 discover 10회)를 비교 기준으로 보존한다. 제공된 모델에서 metadata를 적용한 같은 질문을 실제 실행해 호출/빈 검색/답변을 비교한다. 개선되지 않은 결과도 그대로 보고한다. 답변은 실제 도구 결과와 따로 대조한다.
- `tests/test_model_client.py`는 작은 모델 HTTP fixture와 실제 MCP stdio로 연결·실패·비보정·정보 노출을 검사한다. fixture를 실제 LLM 성공 증거로 보고하지 않는다.
- `docs/22-quickstart-and-model.ko.md`와 README는 기존 `examples/native-orders`의 직접/MCP 시작 경로를 재사용한다. 새 venv/설치한 wheel에서 공개 스키마·기본 사용·시작 예제를 확인한다. source 예제에만 해당 언어 서버 런타임이 필요함을 구별한다.
- `docs/evidence/protocol-completion.json`에 자동 검사, 실제 모델 실행, 배포물 확인과 한계를 기록한다. 원시 결과는 ignored artifacts에 둔다. 전체 회귀 검사를 마친 뒤 사용자 Git 작성자로 커밋·정상 푸시한다.

완료 기준: 로컬 전용 테스트 파일 없이 저장소의 예제·문서로 API 하나를 전환해 직접/MCP/모델 호출을 재현할 수 있다. 공통 도구는 세 개이며 실제 입력/응답 검증이 유지된다.

## 범위 경계

이번에는 위 세 작업 안의 필요한 작은 수정만 한다. Python write/async, 다른 언어/프레임워크, 회사 운영 API, 승인 플랫폼, CI/CD·재배포·버전 정책·새 registry·범용 agent SDK를 추가하지 않는다. 기존 review/build/diff/재승인과 전체 Runtime은 선택 기능으로 보존한다. 사용자가 작성할 새 필수 파일이나 사용 단계를 늘리지 않는다.

## 완료 기록

| 순서 | 결과 | 근거 |
|---|---|---|
| 1. 경량 명세 | 완료 | 명세 20·패키지 JSON Schema·공개 protocol_schema, 이전 요청/응답 schema와 동일, 실제 MCP/정적 packet 검사 |
| 2. 설명·탐색 | 완료 | 선택적 summary/keywords, 원본 설명·태그 재사용, 서버 전용 metadata와 catalog/cursor, 한국어 검색/비노출 검사 |
| 3. 시작·모델 예제 | 완료 | 공개 client/verify_sources와 문서 22, 전체 272개 검사, 실제 모델 7개 질문/24 invoke, 새 venv의 wheel과 직접/Python/stdio/모델 시작 명령 재현 |

실제 모델의 빈 검색은 이전 10회에서 이번 3회, 전체 MCP 호출은 68회에서 65회, 모델 요청은 75회에서 72회였다. 같은 질문·시스템 지침의 한 번 비교다. Spring CRUD는 모델 요청이 16→20회, Go CRUD는 15→16회로 늘었다. 모든 질문의 성능이 개선됐거나 일반 성공률을 증명했다고 표현하지 않는다.

[완료 증거](evidence/protocol-completion.json)에 검사·설치·실행 범위와 한계를 기록했다. 최초 제한된 샌드박스의 MCP 테스트 대기는 해당 프로세스를 정리하고 읽기 제한 시간을 둔 검사로 재실행했다. 최종 검사는 모두 통과했다. 구현 범위를 세 작업 밖으로 확장하지 않았다. Git 반영은 이 변경의 커밋/원격 상태로 확인한다.
