# a2api 1.0 완성 평가 결과

2026-10-31 · 기준: [완성 계획](33-completion-plan.ko.md). 이 문서는 고정 holdout 실행의 판정과, 그 뒤의 원인 분석·개선을 구분해 기록한다. 실패와 provider 오류를 지우지 않았다.

## 1. 무엇을 비교했나

같은 상거래 API(고객·주문·배송·지원 티켓·상담원 + 방해 리소스)를 하나의 정의에서 **Python·Spring Boot 4·Go net/http·Rust Axum**으로 생성했다. 규모는 small 19 / medium 55 / large 235 업무 operation이다. 4개 구현은 같은 seed와 상태 코드를 쓰며, 정의한 요청 46개까지 상태·성공 본문·최종 상태가 일치함을 실행 전에 확인했다(단, 아래 6절의 빈 query 값 차이는 holdout에서 발견됐다).

| 방식 | 모델이 받는 정보 | 실행 |
|---|---|---|
| `spec-tools` | OpenAPI의 **모든 operation을 function tool로**(operationId 이름, summary, path·query 평탄화 + body, `$ref` 해소) | 언어 서버 HTTP, 원본 응답 전체 |
| `spec-prompt` | system prompt에 **OpenAPI 문서 전체** + 범용 `http_request` 도구 | 언어 서버 HTTP, 원본 응답 전체 |
| `a2api` | `ToolSession.auto(요청)`: 6KB 이하 카탈로그는 전체, 그 외는 호스트가 사용자 요청으로 미리 찾은 8개 + `a2api_search` | Spring/Go/Rust는 **소스 importer → convert**, Python은 **`@capability` 함수** |

- 같은 모델·공통 system 지침·질문·제한(요청 12회, 180초)·채점기를 사용했다. 모드 순서는 작업마다 교대했다.
- 요약 문장은 명세 summary와 a2api summary에 같은 문장을 썼다. a2api의 공개 필드 선택(내부 tenantId/internalNote/audit 제외)은 호스트 설정으로 제공되는 프로토콜 기능이며 비교 효과에 포함된다.
- 채점: 최종 JSON 값, 실행 전/후 store 상태 diff(의도한 변경만), 업무 호출 로그(장애 endpoint 재호출 ≤ 2, 누락 입력 시 호출 0). 실행 전 짧은 모델 응답 확인으로 장애 중 시작만 막고, 시작한 run은 재시도하지 않았다.
- 모델 `nvidia/Muse-Glimmer-30B-NVFP4`(vLLM, max_model_len 65,536), temperature 0, max_tokens 2048. 실행 환경: Python 3.14, OpenJDK 25.0.4, Maven 3.9.12, Go 1.26.8, Rust 1.93.1, tree-sitter 0.25.2, mcp 2.3.0.

정적 크기(UTF-8 compact JSON 바이트, 토큰 아님):

| 규모 | spec-tools 도구 정의 | spec-prompt system | a2api 첫 요청 도구(사전 선택 8 + 검색) |
|---|---:|---:|---:|
| small | 9,910 | 22,730 | 약 4,000 |
| medium | 28,396 | 57,014 | 약 4,000 |
| large | 118,388 | 222,817 | 약 4,000 |

## 2. 고정 holdout 판정

holdout 10작업(단순 4·복잡 4·장애 1·누락 입력 1) × 3규모 × 4언어 × 3방식 × **2반복 = 720 run**. 작업 fingerprint `sha256:571ef713…cdf7`은 실행 전에 [33 문서](33-completion-plan.ko.md)에 기록했다. 1반복은 commit `30a059d`, 2반복은 `2629200`(차이는 평가기의 반복 번호 옵션뿐, 라이브러리·작업 동일)에서 깨끗한 작업 트리로 실행했다. 2반복 중 provider가 1–2분간 502/500을 반환해 a2api run 1건이 `MODEL_HTTP_500`으로 실패했고 그대로 실패로 셌다.

| 규모 | 방식 | 통과 | 작업당 토큰(중앙값) | 첫 요청 prompt 토큰(중앙값) | 작업 시간(중앙값, 초) | 모델 요청(평균) | 오류(provider/host) |
|---|---|---:|---:|---:|---:|---:|---|
| large | a2api | 80/80 | 4,970 | 1,914 | 10.746 | 2.575 | - |
| large | spec-prompt | 80/80 | 103,331 | 51,124 | 18.84 | 2.575 | - |
| large | spec-tools | 78/80 | 75,236 | 37,085 | 14.791 | 2.587 | - |
| medium | a2api | 79/80 | 4,776 | 1,910 | 10.595 | 2.562 | MODEL_HTTP_500 1 |
| medium | spec-prompt | 80/80 | 28,193 | 13,539 | 11.256 | 2.6 | - |
| medium | spec-tools | 80/80 | 19,612 | 9,275 | 9.829 | 2.525 | - |
| small | a2api | 80/80 | 4,926 | 1,874 | 10.692 | 2.6 | - |
| small | spec-prompt | 80/80 | 12,574 | 5,735 | 10.247 | 2.55 | - |
| small | spec-tools | 79/80 | 8,114 | 3,543 | 9.362 | 2.55 | - |

| 규모 | 방식 | 모든 언어·반복에서 통과한 작업 | 장애/누락 입력 통과 | 의도하지 않은 쓰기 | 실패 endpoint 반복 | 실패한 업무 호출 |
|---|---|---:|---:|---:|---:|---:|
| large | a2api | 10/10 | 16/16 | 0 | 0 | 8 |
| large | spec-prompt | 10/10 | 16/16 | 0 | 0 | 8 |
| large | spec-tools | 9/10 | 16/16 | 0 | 0 | 8 |
| medium | a2api | 9/10 | 15/16 | 0 | 0 | 8 |
| medium | spec-prompt | 10/10 | 16/16 | 0 | 0 | 8 |
| medium | spec-tools | 10/10 | 16/16 | 0 | 0 | 8 |
| small | a2api | 10/10 | 16/16 | 0 | 0 | 8 |
| small | spec-prompt | 10/10 | 16/16 | 0 | 0 | 8 |
| small | spec-tools | 9/10 | 16/16 | 0 | 0 | 8 |

| 언어 | 방식 | 통과 | 작업당 토큰(중앙값) | 작업 시간(중앙값, 초) |
|---|---|---:|---:|---:|
| go | a2api | 59/60 | 4,742 | 10.844 |
| go | spec-prompt | 60/60 | 30,211 | 14.833 |
| go | spec-tools | 60/60 | 20,214 | 11.156 |
| python | a2api | 60/60 | 5,082 | 10.591 |
| python | spec-prompt | 60/60 | 30,145 | 12.637 |
| python | spec-tools | 60/60 | 20,824 | 10.331 |
| rust | a2api | 60/60 | 4,889 | 11.147 |
| rust | spec-prompt | 60/60 | 30,198 | 14.751 |
| rust | spec-tools | 58/60 | 20,228 | 11.52 |
| spring | a2api | 60/60 | 5,084 | 10.079 |
| spring | spec-prompt | 60/60 | 30,124 | 11.925 |
| spring | spec-tools | 59/60 | 20,230 | 10.241 |

| 작업 유형 | 방식 | 통과 | 작업당 토큰(중앙값) | 작업 시간(중앙값, 초) |
|---|---|---:|---:|---:|
| complex | a2api | 96/96 | 7,233 | 14.076 |
| complex | spec-prompt | 96/96 | 49,066 | 16.988 |
| complex | spec-tools | 96/96 | 29,017 | 13.711 |
| fault | a2api | 23/24 | 6,908 | 15.405 |
| fault | spec-prompt | 24/24 | 41,976 | 17.295 |
| fault | spec-tools | 24/24 | 28,773 | 9.965 |
| missing | a2api | 24/24 | 1,970 | 3.836 |
| missing | spec-prompt | 24/24 | 13,688 | 3.68 |
| missing | spec-tools | 24/24 | 9,408 | 4.189 |
| simple | a2api | 96/96 | 4,195 | 6.809 |
| simple | spec-prompt | 96/96 | 27,632 | 10.441 |
| simple | spec-tools | 93/96 | 19,079 | 8.861 |

평균·꼬리 지연과 실패를 포함한 통과당 토큰(provider usage 합 ÷ 통과 수):

| 규모 | 방식 | 평균 시간(초) | p90 시간(초) | 통과당 토큰 | 작업당 평균 prompt 토큰 | 작업당 평균 출력 토큰 |
|---|---|---:|---:|---:|---:|---:|
| small | a2api | 10.76 | 17.9 | 6,004 | 5,427 | 577 |
| small | spec-tools | 8.47 | 13.7 | 10,187 | 9,575 | 485 |
| small | spec-prompt | 10.22 | 18.1 | 15,798 | 15,207 | 591 |
| medium | a2api | 11.17 | 19.0 | 6,047 | 5,420 | 552 |
| medium | spec-tools | 10.80 | 18.6 | 24,475 | 23,946 | 530 |
| medium | spec-prompt | 12.32 | 21.7 | 36,402 | 35,811 | 591 |
| large | a2api | 11.02 | 19.2 | 6,007 | 5,443 | 564 |
| large | spec-tools | 16.57 | 25.4 | 99,511 | 96,516 | 507 |
| large | spec-prompt | 20.13 | 28.8 | 132,786 | 132,242 | 544 |

실패 4건: `spec-tools`의 H2 3건(large Spring·Rust, small Rust — 모델이 `customerId: ""`를 보냈고 Spring/Rust 구현이 빈 값을 필터로 처리, 6절), a2api의 H9 1건(provider 500).


## 3. 기준별 판정

| 기준(33 문서 1장) | 판정 | 근거 |
|---|---|---|
| 정확도: 모든 규모 a2api ≥ 각 기준선 | **부분 충족** | small 80/80(≥79, 80), large 80/80(≥78, 80). medium 79/80은 provider 500 한 건으로 기준선 80/80보다 1건 낮다. 이를 제외한 업무 실패는 0건 |
| 정확도: 대규모 a2api > 기준선 | **부분 충족** | spec-tools 78/80보다 높지만 spec-prompt 80/80과 같다. 이 모델은 235개 operation 명세(약 37k–51k 토큰)도 64k 문맥 안에서 정확히 사용했다 |
| 컨텍스트: 모든 규모 a2api < 각 기준선 | **충족** | 작업당 토큰 중앙값 small 4,927 / medium 4,776 / large 4,970로 규모와 거의 무관. spec-tools 대비 −39% / −76% / −93%, spec-prompt 대비 −61% / −83% / −95%. 첫 요청 prompt 1.9k 대 3.5k–51k |
| 속도: 중·대규모 a2api < 기준선 | **대규모만 충족** | large 중앙값 10.7초 대 14.8초(−27%)·18.8초(−43%). medium은 10.6초로 spec-prompt(11.3초)보다 빠르지만 spec-tools(9.8초)보다 8% 느리다 |
| 속도: 소규모 +10% 이내 | **미충족** | small 10.7초로 spec-prompt(10.2초) 대비 +4%지만 spec-tools(9.4초) 대비 +14% |
| 안정성 | **충족(인프라 1건 제외)** | 의도하지 않은 쓰기 0건(모든 방식), 실패 endpoint 반복 0건, 4개 언어·2반복 모두 통과한 작업: a2api small 10/10·medium 9/10(provider 500)·large 10/10, spec-tools 9/10·10/10·9/10 |

요약: **컨텍스트 크기는 모든 규모에서 크게 줄었고, 지연은 명세가 큰 대규모에서만 분명히 줄었다. 정확도는 세 방식 모두 상한(98.8–100%)에 가까워 차이가 작았고, 소·중규모 속도는 spec-tools보다 느렸다.**


## 4. dev에서 찾은 원인과 반영한 개선

dev 10작업으로만 개선했다. holdout 질문은 판정 실행 전까지 보지 않았다. 모든 회차 원문은 `artifacts/benchmark/runs/dev-*.jsonl`에 보존했다.

| 회차 | 범위 | 관찰 | 반영 |
|---|---|---|---|
| sanity | Go small, 2작업 | Go importer는 query 값을 string으로 표기하는데 모델이 `page: 1`을 보내 같은 INVALID_INPUT을 5회 반복 | 평탄한 path/query/header 문자열 인자의 JSON 숫자·불리언을 텍스트로 전달 |
| 1 | Go, 90 run | 정확도 30/30(세 방식). 토큰 a2api 6.8k 대 18.9k/27.3k. 중규모 a2api 12.1초 대 spec-tools 7.6초: 사전 선택(상위 3)이 필요한 기능을 놓쳐 검색 왕복 증가. 한국어 조사("주문을")가 검색 index와 맞지 않음 | 비ASCII 단어 뒤 짧은 조사 허용(`field-search/2`), 호스트 사전 검색 8개, 단건 조회 요약에 반환 필드 이름(명세에도 같은 요약) |
| 2 | Go, 90 run | 중규모 a2api 8.1초(−33%), 토큰 4.4k. 소규모는 19개 함수를 모두 줘서 토큰이 spec-tools와 비슷(−8%) | `auto(all_bytes=6000)`: 사전 선택보다 크게 비싸지 않은 카탈로그만 전체 제공 |
| 3 | Go a2api, 30 run | 소규모 토큰 −36%. D5에서 모델 검색 page 3개가 고객 검색 기능을 잘라 35k 토큰 | 모델 검색 page 기본 5 |
| 4 | Go a2api, 30 run | 앱의 JSON 형식 지시가 사전 검색 질의를 오염(재현율 10/13→12/13). 503 뒤 상태와 무관한 detail 때문에 대체 탐색·재호출 | 호스트 사전 검색에는 사용자 요청만 전달, backend 상태별 detail(본문 미전달)과 "이번 요청에서 다시 호출하지 말 것" 안내 |
| 전체 | 4언어, 360 run | 세 방식 모두 120/120, 의도하지 않은 쓰기 0. 토큰 a2api 4.5k 대 19.2k/27.8k. 속도 small 9.2 대 9.7초, medium 9.2 대 8.5초, large 9.5 대 14.6초 | 남은 구조적 원인은 D5(질문에 이메일 값만 있어 고객 검색 미선택) 하나. 값 유형 규칙은 과적합 위험으로 추가하지 않고 고정 |

dev 360 run 결과는 holdout과 같은 방향이다(정확도 상한, 컨텍스트 대폭 감소, 소·중규모 속도 비슷하거나 느림, 대규모 속도 개선).


## 5. holdout 이후 분석과 개선

사용자 지시("차이가 작으면 원인을 분석하고 개선")에 따라 holdout 판정 뒤 원인을 분석했다. **이 절의 변경은 holdout 결과를 본 뒤에 이뤄졌으므로 아래 사후 실행은 깨끗한 holdout이 아니다.** 판정은 2·3절이다.

### 5.1 차이가 작은 원인

1. **정확도 상한**: 이 모델은 235개 operation(도구 정의 약 37k 토큰, 명세 전체 약 51k 토큰)도 64k 문맥 안에서 정확히 골랐다. 이름이 규칙적인 CRUD API여서 기준선도 98.8–100%였다. a2api가 앞설 수 있는 경우는 문맥 초과·모호한 기능 구분·잘못된 인자 교정처럼 이번 작업에 거의 없던 상황이다.
2. **소·중규모 속도는 왕복 수가 아니라 모델 추론 길이에서 갈렸다.** holdout에서 세 방식의 평균 모델 요청 수는 2.55–2.60으로 같았다(사전 선택이 거의 모든 작업에서 필요한 기능을 담아 검색 왕복이 없었다). 대신 첫 단계 출력 토큰 평균이 a2api 305, spec-tools 248, spec-prompt 315였다. 단계 시간 ÷ 출력 토큰은 a2api 19.2ms, spec-tools 23.6ms, spec-prompt 24.7ms로, 기준선 쪽이 긴 prompt의 prefill을 더 냈지만 소·중규모에서는 그 차이가 출력 길이 차이를 넘지 못했다. 모델의 추론 원문은 "ID 순서가 보장되나", "page가 문자열인가" 같은 작업 해석이 대부분이었고, 검색 도구나 일부만 보이는 함수 목록을 고민하는 내용은 확인하지 못했다. 같은 질문에서도 길이가 크게 달라 a2api 표현 때문이라고 단정할 수 없다.
3. **큰 정적 prompt의 비용이 prefix cache로 숨겨진다.** spec-tools의 도구 정의는 모든 요청에서 같아 서버가 재사용한다. 그래서 9k 토큰(중규모)까지는 지연 차이가 거의 없고, 37k–51k(대규모)에서야 a2api가 27–43% 빨랐다.
4. **기준선 실패 원인은 구현 차이였다.** spec-tools의 3건은 모델이 빈 `customerId`를 보낸 경우로, Spring/Rust 구현이 빈 문자열을 필터 값으로 처리했다(Python/Go는 "필터 없음"). a2api 모드의 모델은 이번에 빈 값을 보내지 않았지만, 이것을 a2api의 구조적 장점으로 해석하지 않는다.

### 5.2 반영한 개선

- **벤치마크 구현 일치**: Spring/Rust도 빈 query 값을 "필터 없음"으로 처리하도록 생성기를 고쳤고, 빈 값 probe를 동등성 검사에 추가했다(small 38 / medium 45 / large 48 요청, 불일치 0).
- **함수 설명 기본값 `hints="none"`**: 반환 이름 목록을 빼고 요약과 `[write]` 표시만 둔다. 4개 언어 dev 360 run(교차 실행)에서:

| dev, 4언어 | 통과 | 작업당 토큰(중앙값) | 첫 요청 prompt | 작업 시간(중앙값) | 모델 요청(평균) |
|---|---:|---:|---:|---:|---:|
| a2api, `shape` | 120/120 | 4,486 | 1,875 | 9.48초 | 2.49 |
| a2api, `none` | 120/120 | 4,104 | 1,675 | 8.94초 | 2.48 |
| spec-tools | 119/120(provider 500 1) | 19,197 | 9,275 | 9.22초 | 2.39 |

  토큰은 8.5% 줄었고 정확도는 같았다. 시간은 중앙값이 줄었지만 소규모 평균은 늘어 일관된 속도 개선으로 보지 않는다.
- 사전 선택 규칙·검색 page·오류 안내는 holdout 이후 바꾸지 않았다.

- **작은 카탈로그 전체 제공 `auto(all_bytes=10000)`**: 함수 설명을 줄인 뒤 19개 카탈로그 전체가 약 7.3–8.3KB가 됐다. 4개 언어 dev 교차 실행(240 run)에서:

| dev, 4언어 | 통과 | 작업당 토큰(중앙값) | 작업 시간(중앙값 / 평균) |
|---|---:|---:|---:|
| small, 사전 선택 | 40/40 | 4,167 | 9.30 / 10.77초 |
| small, 전체 제공 | 40/40 | 6,654 | 7.88 / 9.34초 |
| small, spec-tools | 40/40 | 7,997 | 9.34 / 9.26초 |
| medium, 사전 선택 | 40/40 | 4,076 | 9.37 / 11.31초 |
| medium, 전체 제공(55개) | 40/40 | 15,602 | 10.55 / 10.81초 |
| medium, spec-tools | 40/40 | 19,203 | 8.50 / 9.37초 |

  작은 카탈로그는 매 요청 같은 도구 묶음(서버 cache 재사용)과 적은 왕복 덕분에 전체 제공이 빨랐고, 55개 카탈로그는 이점이 없어 기준을 10KB(약 20개 함수)로 정했다. 전체 제공일 때 존재하지 않는 검색 도구를 system 지침에서 언급하던 하네스 문제도 고쳤다(dev small: a2api 8.29초 대 spec-tools 8.61초).

### 5.3 사후 확인(holdout 질문, 개선 후 코드 — 판정 아님)

사후 1회차(360 run, `hints="none"`·빈 query 수정, 소규모는 아직 사전 선택):

| 규모 | 방식 | 통과 | 작업당 토큰(중앙값) | 첫 요청 prompt 토큰(중앙값) | 작업 시간(중앙값, 초) | 모델 요청(평균) | 오류(provider/host) |
|---|---|---:|---:|---:|---:|---:|---|
| large | a2api | 40/40 | 4,550 | 1,722 | 11.099 | 2.6 | - |
| large | spec-prompt | 40/40 | 103,305 | 51,124 | 18.424 | 2.525 | - |
| large | spec-tools | 40/40 | 75,154 | 37,085 | 17.499 | 2.575 | - |
| medium | a2api | 40/40 | 4,564 | 1,718 | 10.547 | 2.625 | - |
| medium | spec-prompt | 40/40 | 28,128 | 13,539 | 10.079 | 2.6 | - |
| medium | spec-tools | 40/40 | 19,544 | 9,275 | 9.471 | 2.6 | - |
| small | a2api | 40/40 | 4,496 | 1,683 | 11.318 | 2.6 | - |
| small | spec-prompt | 40/40 | 12,571 | 5,735 | 10.282 | 2.5 | - |
| small | spec-tools | 40/40 | 8,153 | 3,543 | 10.033 | 2.6 | - |

최종 설정의 소규모 사후 확인(120 run, 전체 제공 + 지침 수정):

| 규모 | 방식 | 통과 | 작업당 토큰(중앙값) | 첫 요청 prompt 토큰(중앙값) | 작업 시간(중앙값, 초) | 모델 요청(평균) | 오류(provider/host) |
|---|---|---:|---:|---:|---:|---:|---|
| small | a2api | 40/40 | 6,795 | 2,884 | 10.893 | 2.525 | - |
| small | spec-prompt | 40/40 | 12,546 | 5,735 | 11.052 | 2.5 | - |
| small | spec-tools | 40/40 | 8,124 | 3,543 | 9.216 | 2.5 | - |

- 빈 query 처리를 맞춘 뒤 세 방식 모두 정확도 100%였다(사후 1회차 120/120씩, 소규모 사후 40/40씩).
- a2api 토큰은 holdout 판정 대비 small 4.9k→6.8k(전체 제공, spec-tools 대비 −16%), medium 4.8k→4.6k, large 5.0k→4.6k였다.
- **소규모 속도는 개선되지 않았다.** dev에서는 전체 제공이 spec-tools와 같거나 빨랐지만, holdout 질문에서는 사전 선택(11.3초)과 전체 제공(10.9초) 모두 spec-tools(10.0초, 9.2초)보다 13–18% 느렸다. 첫 단계 출력 토큰이 a2api 268, spec-tools 244로 남은 차이의 대부분을 설명한다. 같은 함수 수에서도 이 모델이 a2api 표현(이름 `shop_tickets_list`, 소스 importer 타입, compact 결과)일 때 조금 더 길게 추론했고, 이번 범위에서는 원인을 하나로 좁히지 못했다.
- medium 속도도 사전 선택 10.5초 대 spec-tools 9.5초로 판정 때와 같은 경향이었다. large는 11.1초 대 17.5초로 개선이 유지됐다.

### 5.4 정리

이번 모델과 작업에서 a2api의 확실한 효과는 **규모와 무관한 컨텍스트(작업당 약 4.5–7k 토큰)와, 명세가 큰 API에서의 지연·실패 비용 감소**다. 정확도는 이 모델이 큰 명세도 잘 다뤄 차이가 작았다. 소·중규모 지연은 서버 prefix cache와 모델 추론 길이 때문에 명세 function 방식보다 10–18% 느렸고, 표현·전략을 바꿔도 holdout에서는 뒤집히지 않았다. 문맥이 더 작은 모델, 캐시가 없는 provider, 토큰 과금이 비용의 중심인 환경에서는 a2api의 비용 이점이 더 커질 것으로 예상하지만 이번에 측정하지 않았다.



## 6. 한계

- 합성 API와 합성 업무다. 실제 서비스의 이름·문서 품질·오류 형태가 다르면 결과가 달라질 수 있다.
- 단일 모델(30B, 64k 문맥) 결과다. 이 모델은 235개 도구 정의(약 37k 토큰)도 문맥 안에서 처리했다. 문맥이 더 작은 모델이나 더 큰 API에서는 명세 전달 방식이 문맥 초과로 실패할 수 있지만 이번에 관찰하지 않았다.
- 서버의 prefix cache 때문에 매 요청 반복되는 큰 정적 prompt의 지연이 작게 나타난다. 속도 차이는 대부분 모델 왕복 수와 모델의 추론 출력 길이에서 생겼고, 추론 길이는 같은 질문에서도 실행마다 달랐다.
- 판정 실행 때 4개 구현은 빈 query 값(`customerId=`)을 다르게 처리했다(Spring/Rust는 값, Python/Go는 "필터 없음"). spec-tools 실패 3건의 원인이며, 생성기를 고친 뒤의 결과는 5절에 따로 표시한다.
- 사후 확인은 holdout 질문을 다시 쓴 실행이라 독립 검증이 아니다.
- 바이트와 토큰을 혼동하지 않는다. 토큰은 provider usage다.

## 7. 재현

```bash
python -m pip install -e ".[mcp,source]"
python examples/benchmark/generate.py && python examples/benchmark/verify.py
python examples/benchmark/evaluate.py --split holdout --output artifacts/benchmark/runs/holdout-rep1.jsonl
python examples/benchmark/evaluate.py --split holdout --first-repetition 1 --output artifacts/benchmark/runs/holdout-rep2.jsonl
python examples/benchmark/summarize.py artifacts/benchmark/runs/holdout-rep*.jsonl --markdown out.md
```

원문(JSONL)은 ignored `artifacts/benchmark/runs/`에 있고, 요약·실패 목록·원문 hash는 [evidence](evidence/completion-evaluation.json)에 있다.
