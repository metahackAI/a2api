# a2api 1.1 개선 결과: 실제 레거시 API부터 비교하며

2026-11-01 · 계획: [38 문서](38-improvement-execution-plan.ko.md) · 후보: [37 문서](37-next-improvement-plan.ko.md) · 모델: `nvidia/Muse-Glimmer-30B-NVFP4`(vLLM, 문맥 64k)

사용자 지시: "제안한 개선 계획을 모두 진행하되 호출 로직, 기존 API를 쉽게 호출하도록 변환하는 로직, 결정된 API를 호출하는 전체 과정을 개선하면서 다양한 방법으로 레거시 호출과 a2api의 성능을 비교·테스트하고, 다양한 API도 함께 테스트. 먼저 a-commerce(Rust)부터."

실패와 provider 오류를 지우지 않았다. 개선은 design/dev 작업만 보고 했고 held_out/holdout은 판정에만 썼다. a-commerce 저장소는 수정하지 않았다.

## 1. 한 일과 상태

| 영역 | 항목 | 상태 |
|---|---|---|
| 변환 | 도구 목록·이름 호출 importer(`ToolCatalogImporter`), 본문 envelope, camelCase 이름의 단어 보존 | 완료 |
| 변환 | 레거시 표현 `vocabulary`(rename·codes·describe) | 완료 |
| 변환 | Spring: 타입 없는 `ResponseEntity` 추론, Jackson 설정, advice 규칙 정밀화 | 완료 |
| 변환 | Go Gin, Rust Axum(merge·nest·`:param`·context extractor·generic 기본값·문자열 Serialize), Python FastAPI(새 importer) | 완료 |
| 변환 | `untyped_output='open'`, 같은 ID handler를 전체 중단 대신 개별 보고, Go `_test.go` 제외 | 완료 |
| 변환 | OpenAPI 선택 nullable parameter(생략 = null) | 완료(GitHub 1,228 → 1,230/1,254) |
| 호출 과정 | 호스트 요청 값(`request_values`), 원 서버 오류 문장(`error_detail`), 쓰기 멱등성 헤더(`idempotency_header`, `request_id`) | 완료 |
| 호출 로직 | 함수 목록 순서 고정(prefix cache), 검색 `added`와 "새 함수 없음" 안내, 반복 실패·반복 조회 안내, body string 필드의 정수 ID | 완료 |
| 호출 로직 | 사전 선택 재현율(37 P3-1 값 유형 신호, P3-2 다중 의도 분할) | **기각**(5절) |
| 운영 | CI(3.11–3.14 테스트, wheel 검사), 영어 문서 3종, 레거시 예제(`legacy_screens.py`) | 완료 |
| 측정 | 다른 모델·provider(37 P1-1) | **미실시**: 이 환경에서 쓸 수 있는 모델이 하나뿐이다 |
| 측정 | 서버 prompt cache 적중 | **측정 불가**: vLLM 응답의 `prompt_tokens_details`가 비어 있다 |
| 측정 | 공개 RealWorld 구현 서버의 빌드·실행 | **하지 않음**: 실행 환경 정책이 사용자가 지정하지 않은 외부 코드의 빌드를 막았다. 코드는 정적으로만 읽고, 호출은 명세를 따르는 자체 서버로 했다(3절) |

## 2. 기존 API를 a2api로 바꾸는 변환

### 2.1 실제 공개 코드(RealWorld/Conduit, 코드만)

같은 API를 구현한 공개 프로젝트 4개를 **빌드·실행 없이** 읽어 공식 OpenAPI 19개 operation과 비교했다(`examples/realworld/compare.py`, 결과 `artifacts/realworld/conversion-reject.json`).

| 프로젝트 | 1.0 | 1.1 | 필드 이름 일치 | 남은 차이(실제 구현의 동작) |
|---|---|---|---|---|
| Spring Boot | 0/19 — 전역 `@RestControllerAdvice` 때문에 전부 거부 | 19/19 | 18/19 | 글 수정이 `tagList`를 받지 않음 |
| Go Gin | 0 — Gin 미지원 | 19/19 | 16/19 | 가입이 bio/image도 받음, 삭제 응답이 200 `{"article":"delete success"}` |
| Rust Axum | 가져오기 전체 중단 — handler 이름 충돌 | 19/19 | 18/19 | 글 수정이 `tagList`를 받지 않음 |
| Python FastAPI | importer 없음 | 19/19 | 18/19 | 글 수정이 `tagList`를 받지 않음 |

실패 원인과 바꾼 규칙: Spring은 예외 처리만 하는 advice까지 막았고(이제 body를 바꾸는 `ResponseBodyAdvice`·binder advice만 막음), 실제 controller의 `ResponseEntity`(타입 인자 없음)를 읽지 못했다(서비스 필드 반환형·`HashMap` put·`Optional.map(lambda)`·helper를 따라감). `UNWRAP_ROOT_VALUE`+`@JsonRootName`으로 본문이 `{"article": {...}}`로 감싸지는 설정을 `application.properties`에서 읽는다. Go는 group prefix가 등록 함수 인자로 패키지를 건너 전달되고, 입력은 검증 객체의 `Bind(c)` → `common.Bind(c, s)` → `ShouldBindWith`로 들어온다. 수정 화면은 저장 값으로 미리 채운 검증 객체를 bind하므로 `binding:"required"`가 부분 수정을 막지 않는다(이 경우 required를 빼도록 고침). Rust는 `merge`를 `nest`와 같이 거부했고 `:param` 경로, 모듈 경로의 handler, 인증 extractor(`AuthUser: FromRequest`), `ArticleBody<T = Article>` 기본 generic, 문자열로 직렬화하는 `Timestamptz`를 읽지 못했다. FastAPI는 `ast`로만 읽으며 `include_router` prefix(설정 클래스 기본값 `/api` 포함), `Depends` 안의 path/query, `Body(embed, alias)`, Pydantic의 사용자 정의 camelCase `alias_generator`와 mixin 상속을 따라간다.

**실제 호출 검증(모델 없음)**: 각 구현이 코드에 선언한 차이(생성 상태 코드, 빈 bio의 `""`/`null`, 삭제 응답)를 재현하는 명세 준수 서버(`examples/realworld/conduit.py`)에서 변환한 모든 operation을 호출했다. 처음 실행에서 Spring 18/19, Go 3/19, Rust 13/19, FastAPI 15/19였고, 원인은 (a) 서버 flavor가 구현의 실제 상태 코드·null 처리를 아직 따르지 않은 것(예: Spring `createArticle`은 `ResponseEntity.ok`라 200, Rust·Go·FastAPI의 bio는 null이 아닌 문자열)과 (b) Go 수정 form의 required(위 규칙)였다. 둘을 고친 뒤 OpenAPI·Spring·Go·Rust·FastAPI **5개 경로 모두 19/19**가 입력·원본 응답·공개 응답 검증을 통과했다(`evaluate.py verify`).

### 2.2 기존에 처리하던 코드의 회귀

4언어 벤치마크의 생성 소스(Spring·Go·Rust × small/medium/large, 945 operation)를 1.0(`a2c7201`)과 1.1 importer로 각각 변환해 비교했다: 상태·ID·경로·메서드·입력 schema·출력 schema **차이 0건**. `examples/benchmark/verify.py`(4개 구현의 HTTP 동등성 131요청 불일치 0, 언어별 a2api 직접 호출·MCP)도 통과했다.

### 2.3 그 밖의 변환 범위

- GitHub REST 전체 메서드 1,254개: 1,228 → **1,230** 변환(선택 nullable query 2개). 남은 24개는 redirect만 있는 operation 15개, 비JSON 응답 3개, 비JSON 본문 2개 등이다.
- a-commerce: `GET /v1/tools`의 A-Commerce 도구 253개와 레거시 화면 facade 19개를 모두 `ToolCatalogImporter`로 가져왔다(미지원 0).

## 3. a-commerce: 레거시 호출과 a2api 비교

[metahackAI/a-commerce](https://github.com/metahackAI/a-commerce)(Rust Axum, commit `7e1557b`)를 PostgreSQL 18+pgvector와 release 빌드로 실행하고, 이 저장소의 작업 세트(design 12, held_out 16)와 채점 규칙(`xtask/src/run_eval.rs`의 numbers/facts/tools/change set 규칙, `examples/acommerce/scoring.py`로 그대로 옮김)을 썼다. 상점 시각 2026-11-06 11:00 고정, 쓰기는 변경셋 미리보기(사람 승인 전)다.

### 3.1 비교한 방식

| 기호 | 방식 | 모델이 받는 도구 | 첫 요청 도구 정의 크기 |
|---|---|---|---|
| L1 | a-commerce 자체 에이전트 + **레거시 화면 facade** 19개 | 자체 도구 검색(BM25 + 관계 확장, 5–8개) | 자체 구성 |
| L2 | a-commerce 자체 에이전트 + **A-Commerce 도구** 253개 | 위와 같음 | 자체 구성 |
| L3 | 우리 하네스 + facade 19개를 원본 그대로 함수로 | 19개 전체 | 11,698B |
| L4 | 우리 하네스 + A-Commerce 253개를 원본 그대로 함수로 | 253개 전체 | 334,867B(약 10만 토큰, 문맥 64k 초과) |
| A1 | 우리 하네스 + a2api(`ToolCatalogImporter`, A-Commerce 253개) | 사전 선택 8개 + 검색 | 중앙값 10,976B |
| A2 | 우리 하네스 + a2api(facade 19개 + `vocabulary` + 화면 요약) | 사전 선택 + 검색 | 중앙값 5,056B |

우리 하네스(L3·L4·A1·A2)는 같은 모델·system prompt·한도(턴당 모델 호출 12, 도구 호출 20, 120초)·결과 6,000자 상한을 쓴다. a-commerce 자체 에이전트(L1·L2)는 계획기·UI block·자체 결과 요약을 가진 전용 에이전트이고 한도는 그 저장소 설정(모델 호출 12, 도구 호출 20, 60초)이다. **L1·L2와 우리 하네스의 차이에는 도구 표현(a2api)뿐 아니라 에이전트 설계 차이가 함께 들어 있다.** 같은 하네스 안의 L3·L4 대 A1·A2가 도구 표현만 바꾼 비교다. 채점은 같은 규칙이지만 자체 에이전트는 답변 + UI block의 숫자를, 우리 하네스는 답변 문장의 숫자만 본다(우리 쪽이 더 엄격).

### 3.2 design 결과(개선용, 각 1회)

원자료(저장소 미포함): 우리 하네스 `artifacts/acommerce/runs/ours-design-3*.jsonl`, 지표 [evidence](evidence/acommerce-ours-design.json); 자체 에이전트 `acom-own-design-2.md`, 지표 [evidence](evidence/acommerce-own-design.json).

| 방식 | 통과 | 오류(호스트/모델 한도) | 작업당 토큰 중앙값 (평균, p90) | prompt / completion (평균) | 첫 요청 prompt (중앙값) | 최대 prompt (중앙값) |
|---|---|---|---|---|---|---|
| L2 자체+A-Commerce | **6/12** | — | 10,031 (16,623, 41,933) | — | — | — |
| L1 자체+facade | 0/12 | — | 8,126 (8,253, 10,460) | — | — | — |
| L4 A-Commerce 전체 | 0/12 | 문맥 초과 12 | — | — | — | — |
| A1 a2api-acom | 3/12 | 모델 호출 한도 3, 출력 잘림 1 | 43,002 (45,456, 76,050) | 42,933 / 2,523 | 3,683 | 6,772 |
| L3 facade 전체 | 1/12 | 모델 호출 한도 8, 턴 시간 1, 출력 잘림 1 | 70,666 (68,119, 79,860) | 63,648 / 4,471 | 4,654 | 6,682 |
| A2 a2api-facade | 2/12 | 모델 호출 한도 4, 출력 잘림 2, 턴 시간 1 | 47,150 (48,254, 75,455) | 43,721 / 4,533 | 1,951 | 6,314 |

| 방식 | 작업 시간 중앙값 (평균, p90) | 모델 단계당 초(평균) | 출력 토큰당 ms | 모델 호출/작업 | 도구 호출/작업 | 검색/작업 | 실패한 업무 호출 | 호출당 결과 바이트(중앙값) |
|---|---|---|---|---|---|---|---|---|
| L2 자체+A-Commerce | 11.9 (21.5, 61.2) | — | — | 4.25 | 5.75 | — | 8/69 (12%) | — |
| L1 자체+facade | 13.2 (15.7, 28.2) | — | — | 4.83 | 2.67 | — | 25/32 (78%) | — |
| A1 a2api-acom | 38.9 (45.4, 82.6) | 6.70 | 17.9 | 6.75 | 7.00 | 2.25 | **0/56** | 506 |
| L3 facade 전체 | 74.6 (77.2, 117.5) | 7.02 | 17.0 | 10.83 | 10.58 | 0 | 77/127 (61%) | 164 |
| A2 a2api-facade | 76.9 (77.8, 119.5) | 8.38 | 17.1 | 9.25 | 12.25 | 5.75 | **1/73 (1%)** | 394 |

작업 종류별: A1 read 3/9·write 0/3, A2 read 2/9·write 0/3, L3 read 1/9·write 0/3. A1의 도구 precision 0.91, recall 0.81(필수 도구 중 성공 호출 비율 평균).

| 작업 | L2 | L1 | L3 | L4 | A1 | A2 |
|---|---|---|---|---|---|---|
| b1-vip-weekend-sale (쓰기, 2턴) | ✗ | ✗ | E | E | E | E |
| mk-whats-running-this-weekend | ✗ | ✗ | E | E | E | E |
| mk-hero-free-next-weekend | ✓ | ✗ | E | E | ✗ | ✓ |
| md-low-stock-before-weekend | ✗ | ✗ | ✓ | E | ✓ | ✓ |
| md-overcoat-runs-small | ✓ | ✗ | ✗ | E | ✓ | ✗ |
| md-end-of-season-markdown (쓰기) | ✓ | ✗ | E | E | ✗ | E |
| b2-returns-over-200 (쓰기, 3턴) | ✗ | ✗ | E | E | E | E |
| ops-wismo-tracking-stuck | ✓ | ✗ | E | E | ✗ | ✗ |
| ops-frequent-returner | ✓ | ✗ | E | E | ✓ | E |
| mgr-what-needs-me-today | ✗ | ✗ | E | E | ✗ | ✗ |
| mgr-what-changed-this-morning | ✓ | ✗ | E | E | E | E |
| b3-why-sales-dropped | ✗ | ✗ | E | E | ✗ | E |

(E: 호스트/모델 한도 오류로 끝남, ✗: 끝났지만 채점 실패)

**같은 하네스에서 도구 표현만 바꾼 결과**: A-Commerce 253개를 원본으로 주면 매번 문맥을 넘어 시작조차 못 했고(L4), a2api(A1)는 작업당 첫 요청 3.7k 토큰으로 실행해 3/12를 풀었다. 레거시 facade는 원본(L3)이 화면 코드값·약어·page 0 같은 입력으로 업무 호출의 61%를 실패했고, a2api(A2)는 vocabulary·필드 설명으로 실패 업무 호출이 73건 중 1건이었다. 두 경우 모두 a2api 쪽이 첫 요청 prompt가 작다(3,683 / 1,951 대 4,654). 다만 facade는 할인 상한·반품 기한 같은 규칙과 리뷰·작업·배송 추적 기능 자체가 없어 a2api로 바꿔도 대부분의 작업을 풀 수 없다(A2 2/12).

**자체 에이전트와의 차이**: L2가 6/12로 A1(3/12)보다 많이 풀었고 작업당 토큰(중앙값 10k 대 43k)·시간(11.9초 대 38.9초)·모델 호출(4.25 대 6.75)도 적었다. 실행 기록에서 A1은 (1) 답을 가진 뒤에도 정책·쿠폰을 더 조사하다 모델 호출 한도에 걸리고(mk-whats), (2) 대화형 긴 질문에서 사전 선택이 필요한 도구를 놓쳐 검색을 반복했다(5절). 자체 에이전트는 manifest의 `consumes`/`produces` 관계로 후보를 확장하고 계획기가 호출을 묶는다.

**design에서 찾아 고친 것**(모두 held_out 전에 반영):
- 문자열 ID 필드에 정수(`20431`)를 보낸 같은 호출을 11번 반복 → body string의 정수 변환과 반복 실패 안내.
- facade `page=0` 오류 14건 → 코드에서 읽은 필드 설명(`Page number, from 1.`). 수정 뒤 0건.
- 검색이 새 함수를 못 찾아도 다시 검색 → "새 함수 없음" 안내(수정 뒤 실행에서 5회 표시).
- 결과 6,000자 자르기가 미리보기 끝의 규칙 검사(`max_discount: 25% is over the 20% limit`)를 잘라 모델이 보지 못함(7,550자 중 6,904자부터) → `render(max_chars=...)`가 큰 배열부터 줄이고 생략 수를 표시. 효과는 3.3.
- 하네스 결함 두 가지: (1) 쓰기 작업 앞에서만 상점을 초기화해 facade의 즉시 쓰기가 다음 읽기 작업에 남음(첫 두 design 실행은 비교에 쓰지 않음, a-commerce 자체 평가도 같은 방식), (2) 120초 턴 한도에 걸린 요청을 연결 실패로 분류.
- 실행 사고: design 실행 중 a-commerce 스택이 실행 환경의 백그라운드 시간 한도로 종료됐다. 그 순간 실행 중이던 1건(ops-frequent-returner, A2)은 `UPSTREAM_UNAVAILABLE`가 섞여 제외하고 `artifacts/acommerce/runs/ours-design-3-outage.jsonl`(원자료 폴더, 저장소 미포함)에 보존했으며 스택을 분리 프로세스로 다시 올려 다시 실행했다.

### 3.3 결과 상한 개선 뒤 design 재실행(a2api 두 방식, 각 1회)

[evidence](evidence/acommerce-ours-design-4.json). md-end-of-season의 미리보기 결과는 3.2 실행에서 6,014B(6,000자에서 잘림, 규칙 검사 없음)였고 이번에는 4,068B(변경 25개 중 12개 + 생략 수, 규칙 검사 4개 모두 포함)로 모델에게 갔다. 모델은 상한 초과 검사를 받은 뒤에도 상품 재고를 더 조회하다 120초 턴 한도에 걸려 이 작업은 통과하지 못했다.

| 방식 | 통과 | 오류 | 작업당 토큰 중앙값 (평균, p90) | 작업 시간 중앙값 (평균, p90) | 모델 호출/작업 | 검색/작업 | 실패한 업무 호출 |
|---|---|---|---|---|---|---|---|
| A1 a2api-acom | 2/12 (3.2: 3/12) | 모델 호출 한도 4, 턴 시간 1, 출력 잘림 1 | 32,940 (43,291, 88,435) | 38.4 (44.3, 75.7) | 6.67 | 2.33 | 0/55 |
| A2 a2api-facade | 2/12 (3.2: 2/12) | 출력 잘림 2, 모델 호출 한도 4, 턴 시간 1 | 46,351 (48,658, 72,268) | 67.0 (74.5, 119.2) | 9.25 | 5.92 | 1/69 |

같은 코드에서도 md-low-stock(A1)이 3.2에서는 통과, 이번에는 조회 반복으로 모델 호출 한도였다. 1회 실행의 작업별 편차가 커서 held_out 판정은 2회 반복한다.

### 3.4 held_out 판정(각 2회, 16작업 × 2 = 32실행)

held_out 작업은 이 실행 전까지 열어 보지 않았다. 코드는 commit `38d156e`(3.3까지의 개선 포함, 그 뒤 코드 변경 없음). 원자료 `ours-heldout-1.jsonl`, 지표 [evidence](evidence/acommerce-ours-heldout.json). 실행 중 provider가 잠시 500을 반환해 A2의 2건이 `MODEL_HTTP_500`으로 끝났고 실패로 셌다(재시도 없음). a-commerce 자체 에이전트(L1·L2)의 held_out은 같은 장애 순간에 자체 평가기가 "모델 무응답"으로 중단해(17실행, 보고서 없음, 로그 `acom-own-heldout-1-aborted-model-outage.log` 보존) 다시 실행했다(3.5).

| 방식 | 통과 | 오류 제외 통과율 | 오류 | 작업당 토큰 중앙값 (평균, p90) | prompt / completion (평균) | 첫 요청 prompt (중앙값) | 최대 prompt (중앙값) | 첫 요청 도구 정의 |
|---|---|---|---|---|---|---|---|---|
| L4 A-Commerce 전체 | 0/32 | — | 문맥 초과 32 | — | — | — | — | 334,867B |
| A1 a2api-acom | 3/32 (9%) | 19% | 모델 호출 한도 10, 턴 시간 5, 출력 잘림 1 | 61,355 (59,038, 93,131) | 55,424 / 3,615 | 3,938 | 7,382 | 11,794B |
| L3 facade 전체 | 4/32 (12%) | 40% | 모델 호출 한도 15, 턴 시간 5, 출력 잘림 2 | 65,966 (57,760, 92,887) | 53,938 / 3,822 | 4,650 | 6,227 | 11,698B |
| A2 a2api-facade | **5/32 (16%)** | 29% | 턴 시간 7, 모델 호출 한도 6, provider 500 2 | **30,925** (40,642, 77,721) | 37,271 / 3,371 | **1,782** | 5,198 | 4,236B |

| 방식 | 작업 시간 중앙값 (평균, p90) | 모델 단계당 초 | 출력 토큰당 ms | 모델 호출/작업 | 도구 호출/작업 | 검색/작업 | 실패한 업무 호출 | 호출당 결과 바이트(중앙값) |
|---|---|---|---|---|---|---|---|---|
| A1 a2api-acom | 72.0 (71.3, 120.1) | 8.47 | 19.2 | 8.19 | 11.69 | **7.97** | 1/118 (1%) | 484 |
| L3 facade 전체 | 68.9 (71.2, 120.0) | 7.83 | 18.1 | 8.81 | 8.44 | 0 | **189/270 (70%)** | 164 |
| A2 a2api-facade | **47.4** (64.5, 120.1) | 8.05 | 18.4 | 7.72 | 11.28 | 7.19 | 6/116 (5%) | 439 |

작업 종류별: A1 read 2/24·write 1/2·write_approval 0/6, A2 read 5/24·쓰기 0/8, L3 read 4/24·쓰기 0/8. A1 도구 precision 0.60·recall 0.60.

| 작업 | L3 | L4 | A1 | A2 |
|---|---|---|---|---|
| mk-pause-knit-until-monday | ✗ ✗ | E E | E ✓ | ✗ ✗ |
| mk-category-promotion | E E | E E | ✗ ✗ | E E |
| mk-winback | E E | E E | E E | E E |
| mk-viewed-not-purchased | ✓ ✓ | E E | ✓ E | ✓ ✓ |
| md-broken-sizes-outerwear | E E | E E | E E | E E |
| md-how-many-left | ✓ ✓ | E E | ✗ ✓ | ✗ ✓ |
| md-below-cost | E E | E E | E E | E E |
| md-best-sellers-this-month | E E | E E | E E | ✓ ✓ |
| md-out-of-stock-30-days | E E | E E | E E | E E |
| ops-unfulfilled-3-days | ✗ ✗ | E E | E E | ✗ ✗ |
| ops-photo-request | ✗ ✗ | E E | ✗ ✗ | E E |
| ops-cancel-delivered | E E | E E | ✗ ✗ | ✗ ✗ |
| ops-change-address-in-transit | E E | E E | ✗ ✗ | ✗ E |
| mgr-undo-banner | E E | E E | E E | E E |
| mgr-weekly-summary | E E | E E | ✗ ✗ | ✗ ✗ |
| mgr-how-is-business | E E | E E | ✗ ✗ | ✗ ✗ |

**a-commerce 자체 에이전트(L1·L2) held_out**: 다시 실행한 평가도 provider 502로 64실행 중 62번째에서 자체 평가기가 멈춰 보고서가 없다(로그 `acom-own-heldout-2.log`, 원인은 a-commerce 에이전트 로그의 `502 Bad Gateway`, 2026-10-31T19:19Z). 실행 행에서 집계했고, 장애로 0.1초에 끝난 2건을 뺐으며 facade의 마지막 작업(mgr-how-is-business) 2회는 실행되지 않았다. 실행 행에는 토큰이 없다. [evidence](evidence/acommerce-own-heldout.json)

| 방식 | 통과 | 작업 시간 중앙값 (평균, p90) | 모델 호출/작업 | 도구 호출/작업 |
|---|---|---|---|---|
| L2 자체+A-Commerce | **7/32 (22%)** | 11.1 (12.0, 18.1) | 3.56 | 2.00 |
| L1 자체+facade | 6/28 (21%) | 10.9 (11.9, 19.0) | 3.79 | 1.57 |

| 작업 | L2 | L1 |
|---|---|---|
| mk-pause-knit-until-monday | ✗ ✗ | ✗ ✗ |
| mk-category-promotion | ✗ ✗ | ✗ ✗ |
| mk-winback | ✗ ✗ | ✓ ✓ |
| mk-viewed-not-purchased | ✓ ✓ | ✓ ✓ |
| md-broken-sizes-outerwear | ✗ ✗ | ✗ ✗ |
| md-how-many-left | ✓ ✓ | ✗ ✗ |
| md-below-cost | ✗ ✗ | ✗ ✗ |
| md-best-sellers-this-month | ✗ ✗ | ✗ ✗ |
| md-out-of-stock-30-days | ✓ ✓ | ✓ ✓ |
| ops-unfulfilled-3-days | ✗ ✗ | ✗ ✗ |
| ops-photo-request | ✗ ✗ | ✗ ✗ |
| ops-cancel-delivered | ✗ ✗ | ✗ ✗ |
| ops-change-address-in-transit | ✓ ✗ | ✗ ✗ |
| mgr-undo-banner | ✗ ✗ | ✗ ✗ |
| mgr-weekly-summary | ✗ ✗ | 장애 2 |
| mgr-how-is-business | ✗ ✗ | 실행 안 됨 |

자체 평가기는 쓰기 작업 앞에서만 상점을 초기화하고(`run_eval.rs`, `reset && kind != "read"`) facade의 쓰기는 즉시 반영되므로, L1의 읽기 작업은 앞선 facade 쓰기의 영향을 받을 수 있다(우리 하네스는 매 실행 초기화).

**판정**:
- **a-commerce 자체 에이전트 대 우리 하네스**: L2(7/32)가 A1(3/32)보다, L1(6/28)이 A2(5/32)·L3(4/32)보다 많이 풀었고 시간(중앙값 11초 대 47–72초)과 모델 호출(3.6–3.8회 대 7.7–8.8회)도 적었다. 이 차이는 도구 표현만이 아니라 전용 에이전트(계획기, 관계 기반 후보, UI block 채점, 60초 한도에서 짧은 답)와 범용 하네스의 차이다. 도구 표현만 바꾼 비교는 아래 두 항목이다.
- **레거시 화면 facade**: a2api(A2)가 원본 전달(L3)보다 많이 풀었고(5/32 대 4/32), 작업당 토큰 중앙값 −53%(30.9k 대 66.0k), 첫 요청 prompt −62%(1,782 대 4,650), 작업 시간 중앙값 −31%(47.4초 대 68.9초), 실패한 업무 호출 5% 대 70%였다. 통과 수 차이(1건)는 2회 반복의 편차 안이다. 비용·호출 실패의 차이는 크다.
- **A-Commerce 253개 도구**: 원본 전달(L4)은 32회 모두 문맥을 넘어 시작하지 못했고 a2api(A1)는 실행해 3/32를 풀었다. 그러나 A1은 작업당 검색 7.97회로 design(2.3회)보다 훨씬 많이 검색하다 모델 호출 한도에 걸렸다.

**A1 실패의 원인(판정 뒤 분석)**: 검색 255회 중 191회가 다른 함수를 예산에서 밀어냈다. 모델이 한 단계에 검색을 여러 개 부르는데(md-best-sellers: 12단계에 도구 호출 22회), A-Commerce schema가 커서 16KB 예산에 11개 안팎만 들어가므로 뒤 검색이 앞 검색이 막 고른 함수(`get_sales_overview`)를 모델이 보기도 전에 밀어냈다. 모델은 그 함수를 한 번도 호출하지 못하고 같은 이름으로 다시 검색하는 순환에 빠졌다. **ToolSession의 결함**이므로 고쳤다: 마지막 `tools()` 이후 선택된(모델이 아직 보지 못한) 함수는 다른 검색이 밀어내지 못하고, 자리가 없으면 새 후보를 `SCHEMA_BUDGET`으로 제외한다(commit `30a8272`). 이 수정은 held_out 결과를 본 뒤의 변경이므로 3.6의 재실행은 판정이 아니다.

### 3.5 판정 뒤 수정(검색이 보지 못한 함수를 밀어내지 않음)의 확인 — 판정 아님

**design(각 1회)** [evidence](evidence/acommerce-ours-design-5.json): 회귀 없음.

| 방식 | 통과(3.2 / 3.3 / 수정 뒤) | 오류 | 작업당 토큰 중앙값 (평균, p90) | 작업 시간 중앙값 (평균, p90) | 모델 호출/작업 | 검색/작업 | 실패한 업무 호출 | 도구 precision / recall |
|---|---|---|---|---|---|---|---|---|
| A1 a2api-acom | 3 / 2 / **3**/12 | 모델 호출 한도 5, 턴 시간 1, 출력 잘림 1 | 38,926 (47,401, 93,290) | 46.2 (49.5, 108.6) | 7.17 | 2.92 | 1/59 | 0.82 / 0.82 |
| A2 a2api-facade | 2 / 2 / **2**/12 | 출력 잘림 2, 모델 호출 한도 4, 턴 시간 1 | 46,351 (53,461, 72,143) | 83.9 (80.3, 120.0) | 9.58 | 5.83 | 5/77 | — |

**held_out 사후 확인(각 2회, commit `30a8272`)** [evidence](evidence/acommerce-ours-heldout-posthoc.json): held_out을 본 뒤의 수정이라 판정이 아니다.

| 방식 | 통과(판정 → 사후) | 오류 | 작업당 토큰 중앙값 (평균, p90) | 작업 시간 중앙값 (평균, p90) | 모델 호출/작업 | 검색/작업 | 실패한 업무 호출 |
|---|---|---|---|---|---|---|---|
| A1 a2api-acom | 3 → **4**/32 | 모델 호출 한도 13, 출력 잘림 1, 턴 시간 1 | 49,459 (57,109, 98,478) | 64.7 (62.3, 104.3) | 8.12 | 7.41 | 3/122 |
| A2 a2api-facade | 5 → 4/32 | 턴 시간 7, 모델 호출 한도 6, provider 500 1, 출력 잘림 1 | 34,680 (42,630, 94,960) | 49.8 (65.2, 120.1) | 7.81 | 7.44 | 2/135 |

검색이 다른 함수를 밀어낸 비율은 191/255에서 157/237로 줄었고, 같은 단계 안의 밀어내기는 없어졌다(대신 29회는 새 후보를 `SCHEMA_BUDGET`으로 제외). 남은 실패는 **카탈로그에 질문에 딱 맞는 함수가 없을 때 표현을 바꿔 계속 검색하는 순환**이다. 예: md-best-sellers에서 모델은 `get_sales_overview`를 호출해 매출을 받은 뒤에도 상품별 순위 함수를 찾아 15번 더 검색하다 도구 호출 한도에 걸렸다. 밀려났다 다시 들어온 함수가 "새 함수"로 세어져 "새 함수 없음" 안내가 34/237회에만 붙었다. 이를 고쳤다(commit `5364000`): 검색 결과의 `new`는 이 세션에서 한 번도 제공하지 않은 함수만 세고, 호스트 옵션 `max_search_streak`(기본 꺼짐)은 함수 호출 없이 그 수만큼 검색한 뒤 `SEARCH_LIMIT`("가진 함수를 쓰거나 부족한 것을 말하라")를 준다. 효과는 design에서만 측정했다(3.6).

채점 형식의 한계: 숫자만 비교하므로 "2026-11-06T20:00"은 "6"을, "−20.4%"는 "20"을 맞히지 못한다(wismo, b3 — 자체 에이전트도 b3에서 같은 이유로 실패). 반대로 결론이 틀려도 숫자만 맞으면 통과한다(mk-hero 첫 실행에서 "비어 있지 않다"는 답이 통과). 숫자 규칙은 a-commerce 원본을 그대로 따랐다.

## 4. RealWorld: 명세 함수 대 코드에서 변환한 a2api

같은 Conduit API(19 operation)를 (1) 공식 OpenAPI 전체를 함수로 주는 방식(`spec-tools`, 일반적인 명세 전달), (2) 같은 OpenAPI를 a2api로 변환한 방식, (3) 공개 구현 4개의 **코드만** 읽어 a2api로 변환한 방식으로 호출했다. 서버는 명세를 따르고 각 구현의 선언된 차이를 재현하는 `conduit.py`(구현마다 그 flavor)다. 사용자 `jake`의 토큰은 호스트가 넣는다. 작업: dev 8(단순 3·복합 3·장애 1·누락 입력 1), holdout 8(질문 fingerprint `sha256:7900b9d3…f355`, 실행 전 기록). 채점은 서버 상태 변화(정확히 기대한 변경만)와 JSON 답변.

### 4.1 dev(각 1회)

[evidence](evidence/realworld-dev.json)

| 방식 | 통과 | 작업당 토큰 중앙값 (평균, p90) | prompt / completion (평균) | 첫 요청 prompt (중앙값) | 최대 prompt (중앙값) | 첫 요청 도구 정의 |
|---|---|---|---|---|---|---|
| spec-tools(OpenAPI → 함수) | 8/8 | 8,570 (8,270, 12,684) | 7,642 / 628 | 2,458 | 2,826 | 6,689B |
| a2api-openapi | 8/8 | 6,734 (8,157, 11,967) | 7,595 / 562 | 2,834 | 3,164 | 7,414B |
| a2api-spring(코드) | 8/8 | 7,613 (8,108, 12,293) | 7,519 / 588 | 2,554 | 2,892 | 6,319B |
| a2api-go(Gin 코드) | 8/8 | 5,694 (6,557, 9,340) | 6,034 / 523 | 2,356 | 2,666 | 5,804B |
| a2api-rust(Axum 코드) | 8/8 | 5,404 (6,666, 9,906) | 6,113 / 552 | 2,244 | 2,574 | 5,577B |
| a2api-python(FastAPI 코드) | 8/8 | 5,900 (7,861, 12,730) | 7,276 / 585 | 2,472 | 2,808 | 6,184B |

| 방식 | 작업 시간 중앙값 (평균, p90) | 모델 단계당 초 | 출력 토큰당 ms | 모델 호출/작업 | 도구 호출/작업 | 실패한 업무 호출 | 호출당 결과 바이트(중앙값) |
|---|---|---|---|---|---|---|---|
| spec-tools | 10.3 (10.8, 16.6) | 3.75 | 17.2 | 2.88 | 1.88 | 1/15 | 229 |
| a2api-openapi | 10.5 (9.8, 14.0) | 3.88 | 17.3 | 2.50 | 1.50 | 1/12 | 428 |
| a2api-spring | 10.2 (10.3, 17.2) | 3.89 | 17.4 | 2.62 | 1.62 | 2/13 | 422 |
| a2api-go | 9.2 (9.2, 13.2) | 3.84 | 17.4 | 2.38 | 1.38 | 1/11 | 432 |
| a2api-rust | 9.5 (9.6, 14.0) | 3.82 | 17.3 | 2.50 | 1.50 | 1/12 | 428 |
| a2api-python | 9.4 (10.2, 15.7) | 3.87 | 17.4 | 2.62 | 1.62 | 1/13 | 422 |

(실패한 업무 호출의 대부분은 장애 작업 RD7의 의도된 404다.)

19개 operation이라 a2api는 모든 방식에서 전체 제공(`strategy="all"`)이었다. 다섯 a2api 방식과 명세 함수 방식이 모두 dev 8/8을 통과했고, a2api는 작업당 토큰 중앙값이 21–37% 적었으며(5.4k–7.6k 대 8.6k) 모델 호출이 2.38–2.62회로 spec-tools(2.88)보다 적었다. 시간은 비슷하다(중앙값 9.2–10.5초 대 10.3초). 코드에서 읽은 변환은 OpenAPI에서 변환한 것과 같은 정확도였고, 구현마다 도구 정의 크기가 달랐다(Rust 5,577B ~ OpenAPI 7,414B: OpenAPI 쪽은 parameter마다 설명 문장이 있고, 코드 쪽은 설명 없이 실제 DTO 필드만 있다).

## 5. 기각한 개선: 사전 선택 재현율(37 P3)

a-commerce design 작업의 필수 도구가 첫 모델 요청 전에 제공되는 비율(`examples/acommerce/recall.py`, 모델 없음)과 GitHub 고정 검색어 top-3(회귀 확인)로 측정했다. 원자료: [evidence](evidence/preselection-experiments-2026-11-01.json).

| 변형 | 첫 턴 재현율 | 모든 턴 | 판정 |
|---|---|---|---|
| 기준(field-search/2, 사전 선택 8) | 57.1% | 61.9% | — |
| 영어 기능어 stoplist | 52.4% | 57.1% | 기각 |
| 식별자 앞 단어 신호("order 27184") | 57.1% (get_order 79위 → 30위) | 61.9% | 기각(효과 없음) |
| 둘 다 | 52.4% | 57.1% | 기각 |
| 절 분할(전체 8 + 절마다 1 / 2) | 57.1% / 52.4% | — | 기각 |
| 사전 선택 10·12 | 57.1% | — | 효과 없음(16KB 예산에 약 8개만 들어감) |
| 선언된 관계(catalog `consumes`/`produces`)로 상위 3개 결과의 앞뒤 단계 추가 | 47.6% | 47.6% | 기각 |
| 관계, 상위 1개·생산자만 / 상위 2·3개·생산자만 | 57.1% / 42.9%·47.6% | 61.9% / 47.6% | 효과 없음·기각 |

253개 도구에서 긴 대화형 질문은 일반 단어가 여러 도구에 약하게 일치해 coverage 우선 순위가 넓은 약한 일치를 고른다. 단어 목록을 바꾸면 다른 작업의 순위가 흔들렸다. a-commerce 자체 에이전트는 BM25에 manifest의 `consumes`/`produces` 관계로 앞뒤 단계를 끌어오는 방식을 쓰는데, a2api 순위에서는 이 질문들의 상위 결과가 필요한 도구가 아닌 경우가 많아 그 이웃이 더 나은 후보를 밀어냈다. 그래서 검색 순위와 사전 선택은 바꾸지 않았다. 모델이 짧은 검색어로 직접 검색해 일부를 보완한다(3절 실행 기록).

## 6. 4언어 벤치마크 회귀

(작성 중)

## 7. 결론

(작성 중)
