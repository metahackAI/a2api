# a2api 1.1 실행 계획: 실제 레거시 API부터 비교하며 개선

작성일: 2026-10-31 · 상태: **확정(사용자 지시, 이 순서로 진행)** · 근거: [37 문서](37-next-improvement-plan.ko.md)의 개선 후보 전체

사용자 지시: 37 문서의 개선을 모두 진행한다. 그 과정에서 (1) a2api의 호출 로직, (2) 기존 API(Python, Java/Spring, Go, Rust 등)를 a2api가 쉽게 호출하도록 바꾸는 변환 로직, (3) a2api로 고른 API를 실제로 호출하는 전체 과정을 개선한다. 레거시 호출 방식과 a2api를 여러 방법으로 비교하며 테스트하고, 여러 API를 함께 시험한다. **첫 대상은 `metahackAI/a-commerce`의 Rust API**다.

## 1. 첫 대상: a-commerce

| 항목 | 내용 |
|---|---|
| 구현 | Rust(Axum) 워크스페이스, PostgreSQL+pgvector, 13개 도메인, 에이전트용 툴 291개(operation 하나 = `ReadOp`/`WriteOp` 타입) |
| 노출 | 레지스트리가 REST 경로(`METHOD /v1/{domain}/...`), 툴 매니페스트(`GET /v1/tools`, 닫힌 입력 schema), 이름 호출(`POST /v1/tools/{tool}`)을 같은 정의에서 만든다. OpenAPI 문서는 없다 |
| 레거시 비교군 | 같은 백엔드 위에 일부러 만든 **화면형 파사드**(`?set=facade`: 약어 이름 `getPrdGridList`, 코드값 `T03`, 조회도 POST, 총수 없는 grid와 `…Cnt` 쌍, 일괄 저장, 버전 중복, 규칙 설명 없음) |
| 과업 | `eval/tasks/{design,held_out}`의 실제 운영 과업(MD·마케터·운영·스토어 주인, 다중 턴, 변경셋 기대값, 금지 툴). design은 개발용, held_out은 판정용 |
| 기존 결과 | 자체 하네스(툴 검색 5–8개 + planner + 승인 체크포인트)로 Glimmer에서 파사드 0%, A-Commerce 툴 58%(design) |

### 비교하는 방식(같은 과업·모델·채점)

| 방식 | 모델이 받는 것 | 실행 경로 |
|---|---|---|
| L1 레거시 파사드(자체 하네스) | 화면형 툴 | a-commerce 에이전트 서비스 |
| L2 A-Commerce 툴(자체 하네스) | AI용으로 다시 설계한 툴 + 자체 툴 검색 | a-commerce 에이전트 서비스 |
| L3 레거시 파사드 전체를 function으로 | 파사드 툴 전부 | 우리 하네스 |
| L4 A-Commerce 툴 전체를 function으로 | 291개 전부(문맥 초과 여부 포함) | 우리 하네스 |
| A1 a2api(A-Commerce 툴) | 매니페스트를 a2api로 변환 → `ToolSession` | 우리 하네스 |
| A2 a2api(레거시 파사드 변환) | 파사드를 a2api로 변환 + 호스트가 의미·코드표·공개 필드를 보탠 것 | 우리 하네스 |

채점은 a-commerce의 `cargo xtask eval` 규칙을 그대로 옮긴다: 필수 툴이 오류 없이 실행, 금지 툴 미호출, 기대 변경셋 상태·항목, 마지막 답의 사실 숫자. 파사드처럼 툴 이름이 다른 방식은 기존 평가와 같게 사실·변경셋으로만 판정한다. 자체 하네스(L1·L2)와 우리 하네스는 planner·답변 다듬기 등이 달라 **하네스 효과와 툴 레이어 효과가 섞인다**. 그래서 같은 하네스 안의 비교(L3↔A2, L4↔A1)와 시스템 전체 비교(L1/L2↔A1/A2)를 나눠 보고한다.

## 2. 개선 범위(세 영역)

### 2.1 변환 로직(기존 API → a2api)

1. **툴 매니페스트·이름 호출 서비스 가져오기**: `GET /v1/tools` 형태(이름, 설명, 닫힌 입력 schema, 메서드·경로, 종류)와 MCP 서버의 `tools/list`를 a2api capability로 바꾸는 importer. 호출은 이름 호출(`POST /tools/{name}`, 본문 `{"input": …}`) 또는 REST 경로 binding.
2. **호스트가 넣는 요청 값**: 사용자 인증 헤더 외에, 쓰기 미리보기 플래그·변경셋 ID 같은 호스트 소유 query/body 값을 binding에 넣는 기능(모델 입력이 아니다).
3. **레거시 의미 보완**: 코드값(`T03`)↔의미, 약어 필드↔이름, grid+count 짝처럼 레거시에 흔한 문제를 호스트 설정으로 보완(결과 코드 해석, 입력 enum 설명, 출력 필드 선택).
4. 37 문서 P4: OpenAPI multipart/비JSON 응답·nullable query, Go Gin/Echo/Chi·query 정수 추론, Rust Actix·nest/merge·Serde enum, 레지스트리형 Rust operation(`impl ReadOp`)의 소스 읽기 검토, TypeScript(NestJS/Express)·Python(FastAPI/Flask) 소스.

### 2.2 호출 로직(`a2api-call`/`a2api-tools`)

37 문서 P2·P3: cache 친화적 도구 배치, operation 이름 기반 함수 이름, 결과 표현 최소화, 다단계 왕복 감소(관계 선언·일괄 조회 설계), 값 유형 신호·다중 의도 분할로 사전 선택 재현율 개선.

### 2.3 전체 호출 과정(호스트)

변경셋·미리보기·승인 체크포인트가 있는 쓰기 흐름, 대화 턴 간 함수 재사용, 실패 뒤 다음 행동 안내, 결과 누적 크기 관리.

## 3. 진행 순서

| 단계 | 내용 | 완료 기준 |
|---|---|---|
| A | a-commerce 실행 환경(PostgreSQL 18+pgvector, Rust 1.99, commerce/agent/gateway 빌드, 데모 데이터)과 자체 평가 재현(L1·L2, design) | 자체 결과와 같은 범위의 수치 재현 |
| B | a-commerce용 변환 로직(2.1의 1–3)과 우리 하네스(채점 규칙 이식), L3·L4·A1·A2 design 실행 | 네 방식의 design 결과와 원인 분석 |
| C | 호출 로직·전체 과정 개선(2.2·2.3)을 design으로 반복, 기존 4언어 벤치마크로 회귀 확인 | 개선별 채택/기각 기록 |
| D | a-commerce held_out 판정(L1·L2·L3·L4·A1·A2) | 판정 표, 실패 포함 |
| E | 다른 실제 API로 확장(공개 GitHub REST, Spring·Go·Python 공개 프로젝트 중 실행 가능한 것)과 변환 범위(2.1의 4) | API별 변환률·호출 비교 |
| F | 운영 항목: 쓰기 멱등성 키, CI(테스트·wheel), 영어 문서, 결과 문서·배포 | 1.1 배포 준비 |

규칙: 개선은 design/dev 과업으로만 하고 판정은 held_out으로 한다. 실패·provider 오류를 지우지 않는다. a-commerce 저장소는 수정하지 않고 실행 대상으로만 쓴다(필요한 결과·하네스는 a2api 저장소에 둔다). wire(`a2api-call/1.0`)와 MCP 세 도구는 호환을 유지한다.

## 4. 진행 기록(2026-11-01)

| 단계 | 상태 | 비고 |
|---|---|---|
| A | 완료 | 네이티브 실행(PostgreSQL 18+pgvector, Rust 1.99.1 release build). 자체 평가 design: acom 6/12(공개 결과와 같은 범위), facade 0/12 |
| B | 완료 | `ToolCatalogImporter`, 호스트 요청 값, `vocabulary`, 원 서버 오류 문장. 우리 하네스에 a-commerce 채점 규칙(run_eval.rs)을 옮김. 첫 design 실행 뒤 하네스가 쓰기 작업 앞에서만 데모 상점을 초기화해 facade 쓰기가 다음 읽기 작업에 남는 문제를 발견해 매 실행 초기화로 고쳤다(a-commerce 자체 평가도 같은 방식이라 facade 결과에 같은 영향이 있을 수 있다) |
| C | 완료 | 채택: 목록 순서 고정, 검색 `added`/새 함수 없음 안내, 반복 실패·조회 안내, body string의 정수 ID, 쓰기 멱등성 헤더. 기각: 사전 선택 재현율 변형 전부(39 문서 5절) |
| D | 진행 | a-commerce held_out(L1–L4, A1, A2) |
| E | 진행 | 계획 변경: 공개 RealWorld 구현 4개(Spring·Gin·Axum·FastAPI)는 실행 환경 정책상 빌드·실행하지 않고 코드만 읽었다. 호출은 명세를 따르는 자체 서버(구현별 차이 재현)로 했다. Go Gin·FastAPI importer와 Spring·Rust 실제 코드 대응을 이 단계에서 구현 |
| F | 진행 | CI·영어 문서 완료. 1.1 배포 준비는 결과 문서 뒤 |
