# a2api 완성 계획: 4개 언어·소규모/대규모·단순/복잡 작업에서 일반 API 명세 전달보다 효율적인 호출

작성일: 2026-10-31 · 상태: **확정 계획(이 순서대로 개발)** · 기준: 사용자 2026-10-31 지시

이 문서는 00/03 문서의 방향을 유지하면서 사용자가 확정한 완성 목표와 범위를 고정한다. 아래 단계 밖의 기능은 추가하지 않는다. 단계 안의 작은 구현 선택만 진행 중에 결정하고, 계획 변경이 필요하면 이 문서의 "변경 기록"에 이유와 영향을 남긴다.

## 1. 완성 목표

**Python, Java/Spring, Go, Rust로 구현된 API를 a2api 프로토콜로 연결했을 때, 소규모·대규모 API와 단순·복잡 작업 모두에서 LLM이 일반적인 API 명세를 전달받는 방식보다 정확도·컨텍스트 크기·속도·안정성 면에서 효율적으로 호출하도록 완성한다.**

| 축 | 측정 지표(실제 모델 실행) | 완성 판정 |
|---|---|---|
| 정확도 | 작업별 엄격 통과율(정확한 인자·선행 결과 사용·의도한 쓰기만·최종 값 일치) | 모든 규모에서 a2api ≥ 각 기준선, 대규모에서 a2api > 기준선 |
| 컨텍스트 크기 | 첫 요청 prompt 토큰(초기 문맥), 작업당 provider 전체 토큰 | 모든 규모에서 a2api < 각 기준선(작업당 전체 토큰 중앙값) |
| 속도 | 작업당 wall time 중앙값, 모델 요청 수 | 중·대규모에서 a2api < 기준선, 소규모는 기준선 대비 +10% 이내 |
| 안정성 | 언어 4종·2반복의 통과 일관성, 장애/누락 입력 작업 통과, 의도하지 않은 쓰기 0건, host/context 오류 수 | a2api의 일관성·장애 작업 통과율 ≥ 기준선, 의도하지 않은 쓰기 0 |

판정은 **고정 holdout 작업의 최종 실행**으로만 한다. 미달한 항목은 미달로 보고하며 채점·질문·기준선을 약화하지 않는다. 바이트를 토큰으로, 합성 API 결과를 모든 실제 API의 결과로 바꿔 말하지 않는다.

## 2. 비교 대상(기준선)과 공정성 규칙

"일반적인 API 명세 전달"을 다음 두 가지 대표 방식으로 고정한다. 둘 다 같은 OpenAPI 명세(각 언어 구현과 동일한 API를 기술)를 사용한다.

| 모드 | 모델에 주는 정보 | 실행 |
|---|---|---|
| `spec-tools` | 명세의 모든 operation을 function tool 하나씩으로 변환(operationId 이름, summary/description, path·query 평탄화 + `body`, `$ref` 해소). 일반적인 OpenAPI→function calling 변환 | 실제 언어 서버로 HTTP 호출, **원본 응답 전체**와 HTTP 상태 반환 |
| `spec-prompt` | system prompt에 OpenAPI 문서(compact JSON) 전체 + 범용 `http_request(method, path, query, body)` 도구 1개 | 실제 언어 서버로 HTTP 호출, 원본 응답 전체 |
| `a2api` | `ToolSession`(a2api-tools)이 고른 function tool. 소규모는 전체 준비, 대규모는 검색. 호스트가 정한 공개 필드·요약·검색어 | Spring/Go/Rust는 **소스 importer → convert**, Python은 **`@capability` 등록 함수** |

- 모든 모드가 같은 모델·system 지침의 공통 부분·질문·턴/시간 제한·채점기를 사용한다. 모드 순서는 작업마다 교대한다.
- 기준선의 명세는 구현과 같은 정의에서 생성해 정확하다. 내부 필드(tenantId, audit 등)도 실제 응답에 있으므로 명세에 포함된다. a2api가 공개 필드를 줄이는 것은 호스트 설정으로 제공하는 프로토콜 기능이며 비교 대상 효과에 포함한다.
- 요약 문장은 명세 summary와 a2api summary에 같은 문장을 사용한다. 검색 keywords는 a2api 메타데이터로만 존재한다.
- 기준선이 모델 context(65,536)를 넘으면 provider 오류를 그대로 `CONTEXT_OVERFLOW` 실패로 기록한다. 기준선을 임의로 잘라 성공시키지 않는다.
- a2api 평가는 in-process `ToolSession`(같은 wire dispatch)으로 실행해 기준선 executor와 프로세스 조건을 맞춘다. MCP stdio 경로는 생성 앱의 통합 검사로 따로 검증한다.
- Python의 기준선은 같은 서비스 함수와 store를 쓰는 Python HTTP 서버(평가 프로세스의 스레드)로 호출하고, a2api는 같은 함수를 `@capability`로 in-process 호출한다.

## 3. 벤치마크 API(4개 언어 × 3개 규모)

`examples/benchmark/`에 하나의 도메인 정의에서 **OpenAPI 명세 + Spring/Go/Rust 소스 + Python 서비스 모듈**을 결정적으로 생성한다. 생성물은 ignored `artifacts/benchmark/`에 만들고 생성기와 정의만 저장소에 둔다.

- **핵심 리소스(소규모, 약 22개 operation)**: customers, orders, shipments, tickets, agents. 목록(필터·page/limit·total/hasMore), 단건 조회, 검색(POST), 생성, 부분 수정, 주문 취소 action(상태 조건 409), 배송 실시간 추적(항상 503: 장애 작업용).
- **중규모(약 60개)**: 핵심 + 이름·의미가 가까운 방해 리소스 6종(purchase-orders, returns, suppliers 등).
- **대규모(약 240개)**: 핵심 + 방해/일반 업무 리소스 약 36종.
- 모든 응답 객체에는 실제 서비스처럼 내부 필드(tenantId, internalNote, audit 객체 등)가 있다.
- 관리 route(`/__admin/reset`, `/__admin/state`)는 평가기 전용이며 명세·a2api 선택 모두에서 제외한다.
- 생성 소스는 기존 importer 지원 문법 안에서 작성한다. 생성 코드가 importer로 **미지원 0건**이 되어야 하며, 4개 언어 모두 같은 seed 데이터·동작(상태 코드 포함)을 직접 HTTP 동등성 검사로 확인한다.

## 4. 작업 세트와 채점

같은 작업 세트를 3개 규모에서 그대로 사용한다(규모만 변수). 작업은 개발용 dev 10개와 판정용 holdout 10개이며, holdout은 **최종 실행 전 파일 해시를 기록하고 이후 수정하지 않는다**. 개선 작업은 dev 결과만 본다.

| 유형 | dev 예 | holdout 예 |
|---|---|---|
| 단순 조회 | 주문 상태·총액 | 배송 예상 도착·상태 |
| 단순 필터 목록 | gold 고객 최대 3명 | open·high 티켓 최대 2개 |
| 단순 생성 | 고객 티켓 생성 | 신규 고객 등록 |
| 단순 검색 | 이메일로 고객 찾기 | 이름으로 고객 찾기 |
| 복잡 연쇄 | 이메일→최근 주문→배송 상태 | 티켓→고객→미배송 주문 |
| 조건부 쓰기 | 조건 불충족이면 취소하지 않음 | 조건 충족 시 취소 |
| 다중 쓰기 | 팀의 활성 상담원 배정+우선순위 변경 | 고객 등급 변경+열린 티켓 일괄 종료 |
| 집계(페이지) | 고객의 전체 주문 합계(2페이지) | 배송 상태·택배사별 개수(2페이지) |
| 장애 | 추적 503을 실패로 보고 | 추적 실패 후 배송 상태로 대체 보고 |
| 누락 입력 | 대상 없는 취소 요청에 질문 | 대상 없는 등급 변경에 질문 |

- 질문 끝에 최종 답변 JSON의 키를 지정한다(모든 모드 동일). 채점기는 최종 JSON 값, 실행 전/후 store 상태 diff(의도한 변경만 존재), 정규화한 업무 호출 로그(같은 쓰기 중복 금지, 장애 endpoint 재호출 ≤ 2, 누락 입력 시 업무 호출 0)를 검사한다.
- 실행마다 서버 상태를 reset한다. 실패도 비용·시간에 포함한다. 임의 재실행으로 실패를 지우지 않는다.
- 모델: `nvidia/Muse-Glimmer-30B-NVFP4` @ `https://qwen-api-xgen.x2bee.com/v1/`, temperature=0, max_tokens=2048, 작업당 모델 요청 12회·180초 제한.

## 5. 개발 단계(이 순서대로 수행)

### 1단계: 핵심 라이브러리 보완
1. **HTTPDeployment 실행 제한 설정**: `timeout_ms`, `deadline_ms`, `max_response_bytes`(기본값은 기존과 동일). 자동 재시도 없음. `conversion.py`의 고정값 제거.
2. **중첩·배열 공개 필드 선택**: `select`에 `items[].id`, `owner.login` 같은 경로를 허용한다. 원본 응답 전체 검증 → 선택 → 공개 schema 검증 순서와 required/null/참조 보존을 유지한다. 기존 최상위 이름 선택은 그대로 동작한다.
3. **Python 쓰기·비동기 함수**: `@capability(effect="write")`, `async def` 등록. 기존 read 동작과 오류 형식을 유지하고 쓰기는 자동 재시도하지 않는다.
4. **입력 오류 교정 정보**: `INVALID_INPUT`의 issues에 schema에서 유도한 기대값(누락 필드 이름, 허용 enum, 기대 타입)을 추가한다. 원본/backend 데이터는 넣지 않는다.
5. **a2api-tools/0.4 호스트 표현**: (a) 읽기 쉬운 function 이름(capability ID 기반, 충돌 시 hash 접미사), (b) HTTP 입력의 path/query/headers/body를 충돌이 없을 때 평탄화하고 호출 시 원래 구조로 복원, (c) compact 결과 렌더링(`render_result`), (d) `auto` 전략: 전체 도구가 예산 안이면 모두 준비하고 검색 생략, 아니면 사용자 질문으로 호스트가 첫 검색을 수행한 뒤 검색 도구 제공, (e) 비재시도성 실패(대상 없음·권한·장애)에 짧은 안내. wire(a2api-call)와 MCP 세 도구는 바꾸지 않는다.
6. 단위/통합 테스트와 11/12/20/24 문서 갱신.

### 2단계: 4개 언어 벤치마크 API
1. 도메인 정의·seed·작업에 필요한 데이터 관계 작성.
2. 생성기: OpenAPI 3.1, Spring Boot 4, Go net/http, Rust Axum, Python 서비스(+`@capability` 등록, HTTP 서버).
3. 3개 규모 × 4개 언어 빌드·실행, importer 미지원 0건, 언어 간 직접 HTTP 동등성, a2api 직접 호출과 MCP stdio 스모크 검사.
4. 호스트 설정(`application.py`): 노출 operation·effect·공개 필드·요약·검색어.

### 3단계: 평가 하네스
1. 세 모드의 실행기(spec-tools, spec-prompt, a2api)와 공통 모델 루프(사용량·시간·호출·오류 기록).
2. dev/holdout 작업 정의와 채점기, 상태 diff, 요약 집계(언어·규모·유형·모드별).
3. 가짜 모델 HTTP fixture로 하네스·채점기를 결정적으로 검사한다(실제 LLM 성능 증거로 쓰지 않음).

### 4단계: dev 평가와 개선(최대 3회 반복)
1. dev 10작업 × 3규모 × 3모드를 1개 언어로 먼저 실행해 실패 원인을 분류한다.
2. 원인이 a2api 쪽 일반 기능(검색 순위·도구 표현·결과 전달·오류 안내)이면 작업 특정 규칙 없이 개선하고 다시 dev를 실행한다. 반복마다 원문을 새 파일로 보존한다.
3. 4개 언어 dev 전체를 1회 실행해 언어별 importer 차이로 인한 실패를 확인·수정한다.

### 5단계: 최종 holdout 평가
1. holdout 해시를 기록하고 4언어 × 3규모 × 10작업 × 3모드 × **2반복**을 실행한다.
2. 1장의 판정 기준으로 집계하고 `docs/34-completion-results.ko.md`와 `docs/evidence/`에 실패를 포함해 기록한다.

### 6단계: 프로토콜 1.0과 패키지 정리
1. 결과 반영 후 `a2api-call/1.0`(wire 변경 없음), `a2api-tools/1.0`으로 확정하고 버전 `1.0.0`.
2. MIT `LICENSE`, pyproject 메타데이터(license, authors, urls, classifiers), PyPI용 영어 설명 `PYPI.md`, README·00/03·AGENTS 갱신.
3. 새 venv에서 wheel 설치 후 시작 예제(직접/MCP/ToolSession) 재현.

### 7단계: 배포 환경 구축(업로드하지 않음)
1. `.venv`에 build/twine 설치, `~/.pypirc`(권한 600, 저장소 밖)에 PyPI 토큰 설정.
2. `scripts/release.sh`: 정리 → 테스트 → sdist/wheel 빌드 → `twine check` → 새 venv 설치 검사, 업로드는 `--upload`를 명시할 때만.
3. `docs/35-release.ko.md`에 사용자가 직접 테스트·배포하는 절차를 기록한다. 이번 작업에서는 `twine upload`를 실행하지 않는다.

## 6. 범위 밖

CI/CD, 자동 재배포, 새 언어/프레임워크 importer, 운영 권한·승인 플랫폼, vector DB/embedding 검색, LLM router, GitHub 실 API 재평가, 기존 관리 기능(review/build/diff/재승인) 변경. 기존 기능은 보존한다.

## 7. 변경 기록

단계 안의 작은 조정만 기록한다. 범위를 넓히는 새 기능은 추가하지 않았다.

- **2단계 – tree-sitter 0.26.0 충돌**: 생성한 Rust 소스(긴 `.route` 체인)를 읽을 때 py-tree-sitter 0.26.0이 Python 3.12/3.14 모두에서 segfault를 냈다. 0.25.2에서는 정상이라 `source` extra를 `tree-sitter>=0.25,<0.26`으로 좁혔다. Rust importer는 `Node.parent` 대신 위에서 내려가며 조상 목록을 넘기도록 바꿨다(지원 문법 변화 없음).
- **2단계 – Rust 생성 handler**: 검증 오류가 있는 생성 API는 Axum의 흔한 `Result<(StatusCode, Json<T>), StatusCode>` 반환을 쓴다. 기존 importer가 tuple만 받았으므로 이 Result 감싸기를 같은 성공 status 규칙으로 읽도록 보완했다.
- **2단계 – nullable 선택 경로**: Go slice/pointer와 Java 참조 타입은 `anyOf: [X, null]`로 생성된다. `select` 경로와 반환 설명이 이 nullable 감싸기를 통과하도록 했다(그 외 조합 schema는 계속 거부).
- **2단계 – backend 오류 분류**: HTTP 400은 `UPSTREAM_VALIDATION_FAILED`(422), 503은 `UPSTREAM_UNAVAILABLE`(503)로 분류해 Python 경로와 같은 코드·안내를 준다. 다른 상태는 기존과 같다.
- **2단계 – 리소스 이름**: 생성 언어의 상태 타입 `Store`와 겹치는 방해 리소스 클래스를 `RetailStore`로, Java 예약어인 상태값 `new`를 `incoming`으로 바꿨다.
- **3·4단계 – 모델 view 크기**: 소규모 전체 도구가 명세 기준선보다 컸던 원인(장황한 반환 설명, `$schema`, null 허용 선택 인자의 `anyOf`+`default:null`)을 줄였다. 0.4 기본 반환 설명은 `Returns {items:[{id,...}],total}` 형태의 이름 목록이고, 0.3 형식은 `hints="typed"`로 유지한다.
- **4단계 – 텍스트 HTTP 인자**: Go importer는 query 값을 문자열로 정확히 표기하지만 모델은 `page: 1`처럼 숫자를 보내 같은 오류를 반복했다(sanity 실행). 평탄화한 path/query/header의 문자열 인자에 한해 JSON 숫자/불리언을 텍스트로 바꿔 전달한다. body는 바꾸지 않는다.
- **4단계 – 검색 사전 선택**: dev 1회차에서 정확도는 세 방식 모두 30/30이었지만, a2api는 중규모에서 호스트 사전 선택에 필요한 기능이 빠질 때 검색 왕복이 늘어 느렸다. dev 질문의 재현율로만 판단해 (a) 호스트 사전 검색 후보를 모델 검색(3)과 분리해 8개로, (b) 비ASCII 단어 뒤 짧은 조사·어미를 허용하는 일치(`field-search/2`), (c) 생성 API의 단건 조회 요약에 반환 필드 이름을 넣었다(명세 기준선도 같은 요약을 받음). holdout 질문은 보지 않았다.
- **진행 순서 조정 – 모델 서비스 장애**: 2026-10-31 01:41(KST)부터 지정 모델 endpoint의 vLLM 엔진이 멈췄다(`/health` 200, 생성 토큰 카운터 정지, chat 요청 시간 초과). dev 2회차는 장애 중 시작돼 중단하고 부분 기록을 `dev-go-2-aborted-outage.jsonl`로 보존했다. 이후 run 시작 전 짧은 모델 응답 확인으로 장애 중 시작을 막는다(시작한 run은 재시도하지 않음). 모델이 필요 없는 6·7단계의 프로토콜 1.0 명칭·버전·패키지·배포 환경 작업을 먼저 진행했고, 평가 결과가 필요한 문서는 5단계 뒤에 작성한다. 범위 변경은 없다.
