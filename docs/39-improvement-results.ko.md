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

### 2.2 그 밖의 변환 범위

- GitHub REST 전체 메서드 1,254개: 1,228 → **1,230** 변환(선택 nullable query 2개). 남은 24개는 redirect만 있는 operation 15개, 비JSON 응답 3개, 비JSON 본문 2개 등이다.
- a-commerce: `GET /v1/tools`의 A-Commerce 도구 253개와 레거시 화면 facade 19개를 모두 `ToolCatalogImporter`로 가져왔다(미지원 0).

## 3. a-commerce: 레거시 호출과 a2api 비교

(작성 중 — design·held_out 실행 결과를 채운다)

## 4. RealWorld: 명세 함수 대 코드에서 변환한 a2api

(작성 중)

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

253개 도구에서 긴 대화형 질문은 일반 단어가 여러 도구에 약하게 일치해 coverage 우선 순위가 넓은 약한 일치를 고른다. 단어 목록을 바꾸면 다른 작업의 순위가 흔들렸다. 모델이 짧은 검색어로 직접 검색해 일부를 보완한다(3절 실행 기록).

## 6. 4언어 벤치마크 회귀

(작성 중)

## 7. 결론

(작성 중)
