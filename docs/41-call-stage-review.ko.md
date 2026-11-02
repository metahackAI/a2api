# 모델 호출 설정 점검과 단계별 호출 평가

2026-11-02 · 앞선 과정은 [40 문서](40-problem-solving-process.ko.md) · 결과 요약은 [39 문서](39-improvement-results.ko.md)

사용자 요청(2026-11-02):
- API 모델 호출 코드를 점검해 설정과 최대 토큰 수를 바로잡는다.
- a2api로 API를 찾아 파라미터를 넣는 전체 과정을 리뷰한다.
- 평가할 때 전체 정확도만이 아니라 API를 잘 가져왔는지도 함께 본다.
- API는 잘 가져왔는데 입력이 틀렸다면 모델의 문제인지, 레거시 API를 변환하면서 정보가 빠지거나 부족했기 때문인지 확인한다.

## 1. 모델 호출 설정 점검

**확인한 것**
- 모델 카드(`nvidia/Muse-Glimmer-30B-NVFP4`, Hugging Face)의 권장값: `temperature=1.0`, `top_p=0.95`, `top_k=64`, 생각 모드 켬, 추론 강도 high(low / medium / high / xhigh). 문맥 최대 131K이고, 이 환경의 vLLM은 65,536으로 띄워져 있다. 최대 출력 토큰 권장값은 카드에 없다.
- 패키지된 채팅 템플릿(`chat_template.jinja`):
  - 추론 강도는 템플릿 변수 `reasoning_strength`(기본 `high`)로 system 메시지에 "Reasoning strength: high."로 들어간다.
  - assistant 메시지에 `reasoning_content`가 있으면 그 추론을 다시 프롬프트에 넣는다(`<|start|>assistant to=self<|message|>…`).
- 서버에 직접 확인:
  - `chat_template_kwargs: {"reasoning_strength": "low"}`이면 추론이 320자, high이면 763자로 바뀐다.
  - 이전 assistant 메시지에 `reasoning_content`(또는 `reasoning`)를 넣으면 프롬프트가 71 → 318토큰으로 늘어난다. 서버가 실제로 추론을 다시 넣는다.

**고칠 점**(2026-11-02 이전 하네스)

| 항목 | 이전 | 모델 카드·템플릿 | 이후 기본값 |
|---|---|---|---|
| temperature / top_p / top_k | 0 / — / — | 1.0 / 0.95 / 64 | 1.0 / 0.95 / 64 |
| 추론 강도 | 지정 안 함(템플릿 기본 high) | high | `reasoning_strength: high`를 명시 |
| 이전 단계의 추론 | 매 단계 버림 | 템플릿이 다시 넣도록 되어 있음 | **같은 사용자 턴 안에서는 다시 보냄**(턴이 바뀌면 뺀다) |
| 요청당 최대 출력 토큰 | 2,048(벤치마크·RealWorld), 없음(a-commerce, 11/01 저녁부터) | 언급 없음 | **8,192** |

- **최대 토큰 8,192의 근거:** 상한 없이 돌린 a-commerce 실행 2,265단계의 출력(숨은 추론 포함)이 중앙값 363, p99 2,248, p99.9 3,209, 최대 3,843토큰이었다. 8,192는 정상 단계를 자르지 않고 끝없는 출력만 막는다. 2,048은 p99와 비슷해 실제로 답을 잘랐다(40 문서 4단계).
- **어디에 적용했나:** `examples/benchmark/evaluate.py`의 `chat()`·`run_task()`를 a-commerce·RealWorld 하네스가 함께 쓴다. 세 하네스 모두 `--temperature --top-p --top-k --reasoning-strength --reasoning-history --max-tokens`를 받는다. 기본값은 위 표의 "이후"이고, 실행 기록 머리(`sampling`, `reasoningHistory`, `maxTokens`)에 남긴다. 이전 실행은 `--temperature 0 --reasoning-history none`으로 재현한다.
- 단계마다 모델에게 준 함수 목록(`offered`)도 기록한다. 아래의 "API를 가져왔는가"를 정확히 재기 위해서다.

## 2. 평가 방법: 전체 정확도를 단계로 나누기

`examples/acommerce/call_review.py`는 실행마다 **처음 막힌 단계**를 정한다. 과업의 필요한 도구(`tools.required`)를 기준으로 한다.

| 단계 | 뜻 | 주로 누구의 문제 |
|---|---|---|
| A0 | API에 그 기능이 없음(파사드에 대응 화면이 없음) | API 자체 |
| A | 필요한 함수를 모델이 받지 못함. 검색 방식은 검색이 못 찾았거나, 목차 방식은 모델이 불러오지 않음 | a2api 검색 / 모델의 선택 |
| B | 받았지만 부르지 않음 | 모델(계획) |
| C | 불렀지만 성공하지 못함 | 아래 호출 원인으로 나눔 |
| D | 부르기 전·답하기 전에 한도(모델 호출 12회, 120초)나 provider 오류로 끝남 | 모델(탐색 종료) + 하네스 한도 |
| E-write | 필요한 함수는 모두 성공했지만 쓰기 입력·change set이 기대와 다름 | 모델 / 과업 정의 |
| E-format | 답에 숫자는 있지만 채점이 읽는 형태가 아님(-20.35%, ISO 시각) | 채점 방식 |
| E-content | 답에서 사실이 빠짐 | 모델(답 구성) / 채점(마지막 턴만) |

파사드는 과업이 A-Commerce 도구 이름으로 되어 있다. 그래서 a-commerce 문서의 대응표(`docs/api/README.md` 7절, 예: `search_orders` ↔ `getOrdGridList`·`getOrdGridListCnt`)로 화면을 맞춘다. 대응 화면이 없으면 A0이다.

**실패한 업무 호출의 원인**

| 원인 | 판정 근거 |
|---|---|
| `model:schema` | 함수 schema(타입·enum·필수)를 어김. a2api는 보내기 전에 거절한다. 원본 파사드는 검증 계층이 없어 서버가 대신 거절했고, 그것도 schema로 판정한다 |
| `model:function` | 불러오지 않은 쓰기를 부름, 없는 함수 |
| `model:ungrounded` | 조회한 값(ID, 테이블·키 이름)이 질문이나 앞선 **성공** 결과 어디에도 없음(지어낸 값) |
| `model:described` | 서버가 거절한 규칙이 함수 설명·schema에 적혀 있었음 |
| `source:undocumented` | 서버가 거절한 규칙이 함수 설명·schema 어디에도 없음. 레거시 정의에 없고 변환도 보충하지 못한 정보 |
| `business` | 상태·업무 규칙의 거절이나 서버 오류(입력 문제가 아님) |
| `unclear` | 자동으로 정하지 못함. 목록에 남겨 사람이 읽는다 |

"설명에 규칙이 있다"는 규칙을 담을 수 있는 것만 센다: 필수, enum, pattern, 날짜·이메일 같은 format, 그리고 숫자나 "from / at most / only / such as" 같은 규칙 말이 있는 필드 설명이다. `minimum`·`uint32` 같은 값은 세지 않는다. 원본 파사드의 페이지 필드는 `minimum: 0`인데 서버는 1부터 받기 때문이다.

과업이 기대한 쓰기 입력(change set 항목의 `args`)과 모델이 실제로 보낸 입력도 비교한다.

## 3. 변환에서 정보가 빠지는가(정적 점검)

`examples/acommerce/conversion_fidelity.py`는 원본 입력 schema와, 모델이 ToolSession에서 실제로 받는 함수 정의를 필드 단위로 비교한다. 변환, vocabulary, 평탄화, 모델용 보기를 모두 거친 결과다.

| 카탈로그 | 함수 | 입력 필드 | 사라진 필드 | 필수 손실 | enum 변경 | 설명·예시·pattern·format·min/max·기본값 손실 | 설명 교체 |
|---|---|---|---|---|---|---|---|
| A-Commerce 도구 | 253 | 1,353 | 0 | 0 | 0 | 0 | 0 |
| 레거시 파사드 | 22 | 120 | 0 | 0 | 0(코드 → 단어 1:1) | 0 | 50(코드에서 읽은 규칙을 더함) |

교체된 설명의 예:
- `pageNo` "Page no." → "Page number, from 1."
- `ordNo` "Order no." → "Order key such as ord_20402 (order_id in order and claim rows)."
- `tgtMbrGrdCd` "Target member grade code." → "Member grade code: G00 is every shopper, then G01, G02… by tier rank (…)."
- `prmtStatCd` → "In a save row with row_action update: paused pauses it, ended ends it."

**변환이 원본의 정보를 잃지는 않는다.** 남는 위험은 **원본에도 없는 정보를 변환이 보충하지 못한 것**이다. 이것은 실행 기록에서 `source:undocumented`로 찾는다(4절).

## 4. 지난 실행의 리뷰

리뷰 페이지는 실행 묶음마다 `docs/traces/<묶음>/review.md`에 있다. 맨 아래에 실패한 호출과 기대와 다른 쓰기 입력이 모두 나열돼 있다.

### 4.1 첫 held_out 판정(10/31–11/01, [리뷰](traces/ours-heldout-1/review.md))

필요한 함수의 확보 → 호출 → 성공. 파사드는 대응 화면이 있는 것만 센다.

| 방식 | 통과 | API에 있는 필요한 함수 | 모델에게 줌 | 불렀음 | 성공 |
|---|---|---|---|---|---|
| 원본 파사드 전부 | 4/32 | 16/32 | 16/16 | 14/16 | 10/16 |
| A-Commerce 도구 전부 | 0/32 | 32/32 | 32/32 | 0/32 | 0/32 |
| a2api(A-Commerce, 검색) | 3/32 | 32/32 | 27/32 | 18/32 | 18/32 |
| a2api(파사드 변환, 검색) | 5/32 | 16/32 | 14/16 | 9/16 | 8/16 |

실패한 업무 호출의 원인:

| 방식 | 업무 호출 | 실패 | model:schema | model:ungrounded | source:undocumented | business | unclear |
|---|---|---|---|---|---|---|---|
| 원본 파사드 전부 | 270 | 189 | **157** | 0 | **28** | 3 | 1 |
| a2api(A-Commerce, 검색) | 119 | 2 | 0 | 0 | 0 | 1 | 1 |
| a2api(파사드 변환, 검색) | 131 | 21 | 1 | 0 | **4** | 16 | 0 |

- **원본 파사드의 실패 189건**
  - 157건은 문자열 필드에 숫자를 넣은 것이다(`getRfndPopInitData {"clmNo": 20402}`, `getMbrGrdList {"prgmNo": 1}`). 원본 schema에 `string`이라고 적혀 있으니 모델의 위반이다. 원본에는 이를 막을 검증 계층이 없다.
  - 28건은 원본 정의에 없는 규칙이다: 페이지가 1부터(`pageNo: 0` → "Invalid paging."), 날짜 형식(`2026-10-01 00:00:00` is not a date-time).
- **a2api 파사드 변환은 이 두 유형을 없앴다.** 숫자 ID는 ToolSession이 문자열로 보내고, 페이지·날짜 규칙은 변환 설명에 들어갔다. 남은 실패 21건 중 16건은 업무 규칙 거절이다.
- **변환이 보충하지 못한 정보 4건**: `get_rfnd_pop_init_data {"claim_id": 20366}` → "There is no claim 20366."
  - 환불 팝업은 클레임 키(`clm_20366`)를 받는데, 변환 설명은 원본 그대로 "Claim no."였다. 모델이 주문 번호를 넣었다.
  - 주문 키에는 "Order key such as ord_20402"를 보탰지만, **클레임 키에는 같은 보충을 하지 않았다.** 이 리뷰가 찾은 실제 변환 누락이다(5절에서 보충).
- A-Commerce 도구 전부는 32회 모두 첫 요청이 문맥 초과(D)였다.

### 4.2 이후 held_out 사후 확인(A-Commerce 도구, [3.8](traces/ours-heldout-index-posthoc-2/review.md) · [3.9](traces/ours-heldout-fix-posthoc-1/review.md) · [3.11](traces/ours-heldout-guard-posthoc-1/review.md))

| 묶음 | 방식 | 통과 | 함수 줌 | 불렀음 | 성공 | 실패한 업무 호출(원인) |
|---|---|---|---|---|---|---|
| 3.8 | 검색 | 5/32 | 26/32 | 18/32 | 18/32 | 10/133(business 7, model:function 2, model:described 1) |
| 3.8 | 이름 목차 | 7/32 | 28/32 | 25/32 | 25/32 | 0/140 |
| 3.9 | 검색 | 9/32 | 28/32 | 21/32 | 21/32 | 0/120 |
| 3.9 | 목차 + batch | 5/32 | 28/32 | 26/32 | 26/32 | 9/155(model:ungrounded 8, unclear 1) |
| 3.11 | 검색 | 8/32 | 25/32 | 21/32 | 21/32 | 0/126 |
| 3.11 | 목차 + batch | 7/32 | 25/32 | 23/32 | 23/32 | 16/142(model:ungrounded 16) |

(이 실행들은 단계별 함수 목록을 기록하기 전이다. "함수 줌"은 불러오기·검색 결과로 추정했고, 검색 방식의 사전 선택은 포함하지 못했다.)

처음 막힌 단계(3.11):

| 방식 | 통과 | A | B | C | D | E-write | E-format | E-content |
|---|---|---|---|---|---|---|---|---|
| 검색 | 8 | 7 | 2 | 0 | 11 | 2 | 0 | 2 |
| 목차 + batch | 7 | 7 | 0 | 0 | 9 | 2 | 1 | 6 |

- **입력 문제로 실패한 실행(C)은 0이다.** 필요한 함수를 부른 실행에서 그 호출은 모두 성공했다.
  - 실패한 업무 호출은 목차 + batch의 `describe_data`가 대부분이다. `{"table": "catalog.inventory"}`, `catalog.product_inventory`, `catalog.stock`처럼 앞선 결과에 없는 테이블 이름을 지어내 넣었다(`model:ungrounded`).
  - 이 실패는 "30일 넘게 품절" 과업에서 없는 데이터를 찾는 탐색의 일부였다.
- **A(필요한 함수를 받지 못함)는 네 과업에 몰려 있다.**
  - `mgr-undo-banner`(`search_change_sets`), `mk-winback`(`send_bulk`), `ops-cancel-delivered`(`get_order`), `md-out-of-stock-30-days`(`search_products`)
  - 목차 방식에서 이것은 검색 실패가 아니다. 모델이 목차를 보고 **다른 함수를 골랐거나**, 쓰기 과업의 마지막 단계(대량 발송)까지 **가지 못한** 것이다.
- **D(한도)가 가장 큰 단계다.** 필요한 함수를 받았지만 부르거나 답하기 전에 모델 호출 12회나 120초에 걸렸다.
- **E-write는 모두 `ops-photo-request`다.**
  - 과업은 `send_customer_message {"customer_id": "cus_riley", "kind": "photo_request"}`를 기대한다. 하지만 도구의 `kind` 값은 `ask_for_photos, decline, refund_done, custom`뿐이다. **기대값을 도구로 만들 수 없다**(과업 정의 문제).
  - 모델이 `customer_id`를 비우고 `order_id`만 넣은 것은 모델 쪽 선택이다.

**정리: a2api 경로에서 "API는 가져왔지만 입력이 틀려 실패"는 드물다.**
- 변환이 원본 정보를 잃은 경우는 정적 점검에서 0이다.
- 원본에 없던 정보를 변환이 보충하지 못한 경우는 1종(클레임 키)이었다.
- 실패의 대부분은 함수 선택(다른 함수), 탐색 종료(한도), 답 구성(사실 누락)이다.

## 5. 모델 카드 설정으로 다시 잰 결과

(측정 중: design·held_out, 검색 / 목차 + batch / 원본 파사드 전부 / a2api 파사드 변환 전부, 각 2회)
