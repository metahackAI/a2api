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
- **어디에 적용했나:** `examples/benchmark/evaluate.py`의 `chat()`·`run_task()`를 a-commerce·RealWorld 하네스가 함께 쓴다. 세 하네스 모두 `--temperature --top-p --top-k --reasoning-strength --reasoning-history --reasoning-keep --max-tokens`를 받는다. `--reasoning-history`는 `turn`(기본) · `recent`(턴의 마지막 N단계만, 5.4) · `all` · `none`이다. 기본값은 위 표의 "이후"이고, 실행 기록 머리(`sampling`, `reasoningHistory`, `maxTokens`)에 남긴다. 이전 실행은 `--temperature 0 --reasoning-history none`으로 재현한다.
- 단계마다 모델에게 준 함수 목록(`offered`)도 기록한다. 아래의 "API를 가져왔는가"를 정확히 재기 위해서다.

## 2. 평가 방법: 전체 정확도를 단계로 나누기

`examples/acommerce/call_review.py`는 실행마다 **처음 막힌 단계**를 정한다. 과업의 필요한 도구(`tools.required`)를 기준으로 한다.

| 단계 | 뜻 | 주로 누구의 문제 |
|---|---|---|
| A0 | API에 그 기능이 없음(파사드에 대응 화면이 없음) | API 자체 |
| A | 필요한 함수를 모델이 받지 못함. 검색 방식은 검색이 못 찾았거나, 목차 방식은 모델이 불러오지 않음 | a2api 검색 / 모델의 선택 |
| B | 받았지만 부르지 않음 | 모델(계획) |
| C | 불렀지만 성공하지 못함 | 아래 호출 원인으로 나눔 |
| D-before | 필요한 함수를 부르기 전에 한도(모델 호출 12회, 120초)나 provider 오류로 끝남 | 모델(탐색) + 하네스 한도 |
| D-after | 필요한 함수는 모두 성공했는데, 답하기 전에 한도로 끝남 | 모델(탐색 종료) |
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

11/02 10:08–14:20, a-commerce `d86a1ff`, 각 2회. 설정은 1절의 "이후" 기본값이다.
- 기록: [design](traces/ours-design-settings-1/README.md)·[리뷰](traces/ours-design-settings-1/review.md), [held_out](traces/ours-held_out-settings-1/README.md)·[리뷰](traces/ours-held_out-settings-1/review.md)
- evidence: [design](evidence/acommerce-settings-design.json), [held_out](evidence/acommerce-settings-heldout.json)

비교한 방식:
- **검색**, **목차 + batch**: A-Commerce 도구 253개
- **원본 파사드 전부**: 레거시 파사드 22개 화면을 원본 그대로 모두 준다
- **a2api 변환 파사드 전부**: 같은 22개를 a2api로 변환해 모두 준다. 검색 없이 변환의 이름·단어·설명 효과만 본다

held_out 실행은 클레임 키 설명(4.1)을 보탠 뒤 시작했고, design 실행은 그 전이다.

### 5.1 통과와 단계

| 세트 | 방식 | 통과 | 이전 설정(같은 커밋) | 작업당 토큰 중앙값 | 필요한 함수: 줌 / 불렀음 / 성공 |
|---|---|---|---|---|---|
| design | 검색 | **12/24** | 5/24 | 43,276 | 40 / 31 / 31 (42개 중) |
| design | 목차 + batch | **15/24** | 13/24 | 37,928 | 35 / 35 / 35 (42개 중) |
| design | 원본 파사드 전부 | 2/24 | — | 96,054 | 28 / 22 / 20 (API에 있는 28개 중) |
| design | a2api 변환 파사드 전부 | 4/24 | — | 94,474 | 28 / 24 / 24 (28개 중) |
| held_out | 검색 | 8/32 | 8/32 | 49,003 | 25 / 23 / 23 (32개 중) |
| held_out | 목차 + batch | 6/32 | 7/32 | 47,584 | 27 / 27 / 27 (32개 중) |
| held_out | 원본 파사드 전부 | 3/32 | — | 96,112 | 16 / 15 / 10 (16개 중) |
| held_out | a2api 변환 파사드 전부 | **12/32** | — | 45,552 | 16 / 16 / 16 (16개 중) |

"이전 설정"은 temperature 0, 추론을 다시 보내지 않음, 출력 상한 없음이다(design-12b, held_out 3.11).

처음 막힌 단계:

| 세트 | 방식 | 통과 | A0 | A | B | C | D-before | D-after | E-write | E-format | E-content |
|---|---|---|---|---|---|---|---|---|---|---|---|
| design | 검색 | 12 | 0 | 2 | 1 | 0 | 4 | 1 | 0 | 2 | 2 |
| design | 목차 + batch | 15 | 0 | 4 | 0 | 0 | 0 | 1 | 0 | 1 | 3 |
| design | 원본 파사드 전부 | 2 | 13 | 0 | 0 | 1 | 2 | 6 | 0 | 0 | 0 |
| design | a2api 변환 파사드 전부 | 4 | 13 | 0 | 0 | 0 | 2 | 5 | 0 | 0 | 0 |
| held_out | 검색 | 8 | 0 | 7 | 0 | 0 | 2 | 6 | 2 | 2 | 5 |
| held_out | 목차 + batch | 6 | 0 | 5 | 0 | 0 | 0 | 7 | 2 | 3 | 9 |
| held_out | 원본 파사드 전부 | 3 | 13 | 0 | 0 | 5 | 1 | 9 | 0 | 0 | 1 |
| held_out | a2api 변환 파사드 전부 | 12 | 9 | 0 | 0 | 0 | 0 | 6 | 0 | 1 | 4 |

한도 실패는 대부분 D-after다(held_out 31건 중 28건, design 21건 중 13건). 필요한 함수를 모두 성공적으로 부른 뒤에도 모델이 호출을 이어 가다 한도에 걸렸다.

실패한 업무 호출의 원인:

| 세트 | 방식 | 업무 호출 | 실패 | model:schema | model:function | model:ungrounded | model:described | source:undocumented | business | unclear |
|---|---|---|---|---|---|---|---|---|---|---|
| design | 검색 | 121 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| design | 목차 + batch | 152 | 6 | 0 | 0 | 0 | 0 | 0 | 3 | 3 |
| design | 원본 파사드 전부 | 283 | **153** | 86 | 0 | 12 | 0 | 45 | 3 | 7 |
| design | a2api 변환 파사드 전부 | 207 | 11 | 0 | 0 | 4 | 1 | 6 | 0 | 0 |
| held_out | 검색 | 145 | 4 | 2 | 0 | 2 | 0 | 0 | 0 | 0 |
| held_out | 목차 + batch | 191 | 6 | 0 | 0 | 2 | 0 | 0 | 3 | 1 |
| held_out | 원본 파사드 전부 | 333 | **202** | 148 | 0 | 6 | 0 | 39 | 5 | 4 |
| held_out | a2api 변환 파사드 전부 | 192 | 15 | 0 | 1 | 0 | 0 | 4 | 8 | 2 |

**읽는 법**

- **설정 효과는 세트마다 달랐다.**
  - design에서 검색은 5 → 12/24, 목차 + batch는 13 → 15/24로 올랐다. 시간 초과(이전 설정 design에서 여러 건)는 거의 사라졌다.
  - held_out에서는 검색 8 → 8, 목차 + batch 7 → 6으로 변화가 없었다.
  - temperature 1.0은 실행마다 결과를 흔든다. 작업당 2회로는 이 차이를 판정할 수 없다. 샘플링과 추론 재전달 중 어느 쪽 효과인지는 5.2에서 나눈다.
- **레거시 파사드에서 변환 효과가 분명하다.**
  - 같은 22개 화면을 모두 주었을 때, 변환 전 실패 호출은 54–61%, 변환 후는 5–8%다.
  - held_out 통과는 3 → **12/32**로, 이번 측정의 모든 방식 중 가장 높다.
  - 필요한 함수를 성공적으로 부른 비율도 10/16 → 16/16이다.
- **원본 파사드 실패의 원인**
  - 대부분 모델의 schema 위반이다(문자열 필드에 숫자. a2api는 숫자 ID를 문자열로 보낸다).
  - 다음은 원본 정의에 없는 규칙이다: 페이지 1부터, 날짜 형식, 저장 행의 필수 항목.
- **a2api 변환 후에도 남은 "원본·변환에 없던 규칙"**
  - design 6: 날짜·시각 형식(`2026-11-07 00:00:00` → "expected 2026-11-07T00:00")
  - held_out 4: 배너 저장 행의 필수 항목(`button_label`, `link_url`, `image_product_id` 또는 `image_id`)
  - 둘 다 화면 코드에만 있는 규칙이고, 변환 설명에 보충했다(5.3에서 다시 잼).
- **A-Commerce 도구 경로에서는 입력 문제로 실패한 실행(C)이 0이다.**
  - 실패한 업무 호출 4–6건도 대부분 근거 없는 값이나 업무 규칙 거절이었다.
  - 실패 단계는 A(다른 함수 선택), D(한도), E(답)다.

### 5.2 설정 효과 나누기

샘플링만 카드 권장값으로 바꾸고 추론은 다시 보내지 않는 조건(`--reasoning-history none`)을 따로 쟀다.
- design: 11/02 14:22–15:08. [기록](traces/ours-design-settings-nohistory-1/README.md), [리뷰](traces/ours-design-settings-nohistory-1/review.md), [evidence](evidence/acommerce-settings-nohistory-design.json)

| design(작업당 2회) | 검색 | 목차 + batch | 작업당 토큰 중앙값(검색 / 목차) | 필요한 함수 성공(검색 / 목차, 42개 중) |
|---|---|---|---|---|
| temperature 0, 추론 버림(이전) | 5/24 | 13/24 | 37,532 / 35,457 | — |
| 샘플링 1.0·0.95·64, 추론 버림 | 8/24 | 11/24 | 34,320 / 31,377 | 27 / 32 |
| 샘플링 + 같은 턴 추론 재전달 | **12/24** | **15/24** | 43,276 / 37,928 | 31 / 35 |

- 추론 재전달은 두 방식 모두 +4건이었다. 함수를 받아 성공적으로 부른 수도 늘었다(27 → 31, 32 → 35).
  - 같은 턴의 앞 단계에서 왜 그 함수를 불렀는지가 남아, 탐색이 덜 반복된 것으로 보인다. 호출 한도·시간 초과(추론 버림 → 재전달)는 검색 5 → 5, 목차 3 → 1이었다.
  - 대신 토큰이 작업당 6.6–9.0k 늘었다.
- 샘플링만 바꾼 효과는 +3과 −2로 방향이 엇갈려 오차 범위다.

held_out도 같은 방식으로 나눴다(11/02 16:07–17:26. [기록](traces/ours-held_out-settings-nohistory-1/README.md), [리뷰](traces/ours-held_out-settings-nohistory-1/review.md), [evidence](evidence/acommerce-settings-nohistory-heldout.json)).

| held_out(작업당 2회) | 검색 | 목차 + batch | 한도 초과(검색 / 목차) | 작업당 토큰 중앙값(검색 / 목차) |
|---|---|---|---|---|
| temperature 0, 추론 버림(이전, 3.11) | 8/32 | 7/32 | 15 / 14 | 47,820 / 23,669 |
| 샘플링만, 추론 버림 | 5/32 | 7/32 | 15 / 11 | 76,176 / 21,210 |
| 샘플링 + 같은 턴 추론 재전달 | 8/32 | 6/32 | 7 / 10 | 49,003 / 47,584 |

- held_out에서는 세 설정의 통과가 5–8로 구별되지 않는다.
- 추론 재전달은 한도 초과를 줄였다(검색 15 → 7). 하지만 그 실행들은 답 단계(E)에서 실패했다.
- 토큰은 방식마다 반대로 움직였다.
  - 검색: 반복이 줄어 재전달 쪽이 오히려 적다(76k → 49k).
  - 목차 + batch: 이전 추론이 쌓여 두 배 넘게 늘었다(21k → 48k).
- design과 held_out을 합치면(각 56실행):
  - 검색: 13(이전) · 13(샘플링만) · **20**(재전달)
  - 목차 + batch: 20 · 18 · **21**

**설정 판단.** 기본값은 모델 카드대로 둔다: 샘플링 1.0·0.95·64, 추론 강도 high, 같은 턴의 추론 재전달, 요청당 8,192토큰.
- 근거 1: 모델이 의도한 사용법(템플릿)이다.
- 근거 2: 한도 초과를 줄였다.
- 근거 3: design에서 두 방식 모두 올랐다.

다만 held_out 통과율은 바뀌지 않았고, 목차 방식은 토큰이 늘었다. 다시 보내는 추론을 줄이는 방법은 5.4에서 쟀다.

### 5.3 변환 보충 뒤 다시 잼

리뷰가 찾은 세 가지를 파사드 변환 설명에 보탰다. 모두 화면 코드에서 읽을 수 있는 규칙이다.
- 클레임 키 형식: `clmNo` "Claim key such as clm_20402"
- 화면의 날짜·시각 형식: `strtDtm`·`endDtm`·`srchStrtDtm`·`srchEndDtm`·`aplyDtm` "such as 2026-11-07T00:00"
- 저장 화면의 행별 필수 항목: `saveDispBnrList`, `savePrmtList`, `saveCpnList`. 원본 schema는 `rowStat`만 필수로 표시한다.

다시 잰 시각과 기록:
- design 11/02 15:09–15:35([기록](traces/ours-design-facade2-1/README.md), [리뷰](traces/ours-design-facade2-1/review.md))
- held_out 15:37–16:05([기록](traces/ours-held_out-facade2-1/README.md), [리뷰](traces/ours-held_out-facade2-1/review.md))

| 세트 | a2api 변환 파사드 전부 | 통과 | 실패한 업무 호출 | source:undocumented | model:ungrounded | model:described | business | unclear |
|---|---|---|---|---|---|---|---|---|
| design | 보충 전(5.1) | 4/24 | 11/207 | 6 | 4 | 1 | 0 | 0 |
| design | 보충 후 | 4/24 | 7/220 | **0** | 6 | 0 | 0 | 1 |
| held_out | 보충 전(5.1, 클레임 키만 보충) | 12/32 | 15/192 | 4 | 0 | 0 | 8 | 2 |
| held_out | 보충 후 | 12/32 | 6/189 | **0** | 1 | 1 | 2 | 2 |

**결과**
- 보충한 규칙 때문에 나던 실패는 사라졌다(source:undocumented 6 → 0, 4 → 0). 실패한 업무 호출도 절반 이하로 줄었다.
- 남은 것은 모델 쪽이다.
  - 슬롯이 없는 페이지 유형을 조회했다(`page_type: "search"` → "The search page has no display slots", model:ungrounded).
  - 설명에 적힌 필수 항목(`button_label`)을 빠뜨렸다(model:described).
- 통과 수는 그대로다. 필요한 함수는 이미 모두 성공적으로 부르고 있었고(held_out 16/16), 실패 단계가 다음과 같기 때문이다.
  - A0: 파사드에 그 기능이 없음(design 14, held_out 9)
  - D: 한도
  - E: 답
- **변환 정보를 더해 고칠 수 있는 실패는 이것으로 거의 남지 않았다.**

### 5.4 추론 재전달 줄이기(`recent`)

사용자 요청(11/02): 추론을 다시 보내는 토큰을 줄인다.

**방식.** `--reasoning-history recent --reasoning-keep 2`는 같은 사용자 턴 안에서도 마지막 두 단계의 추론만 다시 보낸다.
- 단계마다 추론이 질문과 앞 단계의 판단을 되풀이하므로, 턴 전체를 보내면 뒤 요청일수록 길어진다.
- 도구 호출과 결과는 그대로 모두 보낸다.
- 처음 세 요청은 다시 보낼 추론이 두 단계 이하라 `turn`과 프롬프트가 같다.

**측정.** 11/02 22:46 – 11/03 07:38, 작업당 2회, a-commerce `d86a1ff`.
- design: 29실행 뒤 모델 서버 중단(23:46)으로 멈췄다. 남은 실행은 11/03 06:52에 이어 했다. 서버 중단으로 모델 응답이 0회였던 1실행도 다시 했다.
  - 이때 서버가 출력 토큰당 약 47ms(평소 18ms)였다. 턴 시간 한도를 같은 비율로 120 → 320초로 늘렸고, 호출 한도(모델 12회, 도구 20회)는 그대로다.
- held_out: provider 502로 모델 응답이 0회였던 2실행을 07:33에 다시 했다.
- 기록:
  - design [1](traces/ours-design-settings-recent-1/README.md) · [1b](traces/ours-design-settings-recent-1b/README.md) · [리뷰](traces/ours-design-settings-recent-1/review.md)
  - held_out [1](traces/ours-held_out-settings-recent-1/README.md) · [1b](traces/ours-held_out-settings-recent-1b/README.md) · [리뷰](traces/ours-held_out-settings-recent-1/review.md)
  - evidence [design](evidence/acommerce-settings-recent-design.json) · [held_out](evidence/acommerce-settings-recent-heldout.json)
  - 리뷰와 evidence는 1과 1b를 합친 것이다.

| 세트 | 방식 | 추론 재전달 | 통과 | D-before / D-after | 작업당 토큰 중앙값 | 토큰 합 | 다시 보낸 추론(입력 중) |
|---|---|---|---|---|---|---|---|
| design | 검색 | 없음 | 8/24 | 4 / 1 | 34,320 | 1.04M | 0 |
| design | 검색 | 턴 전체 | 12/24 | 4 / 1 | 43,276 | 1.27M | ≈83k (7%) |
| design | 검색 | 최근 2단계 | 9/24 | 4 / 0 | 33,816 | 1.13M | ≈32k (3%) |
| design | 목차 + batch | 없음 | 11/24 | 1 / 2 | 31,377 | 1.10M | 0 |
| design | 목차 + batch | 턴 전체 | 15/24 | 0 / 1 | 37,928 | 1.35M | ≈157k (12%) |
| design | 목차 + batch | 최근 2단계 | 11/24 | 0 / 3 | 34,384 | 1.30M | ≈72k (6%) |
| held_out | 검색 | 없음 | 5/32 | 4 / 9 | 76,176 | 2.52M | 0 |
| held_out | 검색 | 턴 전체 | 8/32 | 2 / 6 | 49,003 | 2.33M | ≈244k (11%) |
| held_out | 검색 | 최근 2단계 | 8/32 | 0 / 6 | 51,844 | 2.34M | ≈78k (3%) |
| held_out | 목차 + batch | 없음 | 7/32 | 0 / 9 | 21,210 | 1.17M | 0 |
| held_out | 목차 + batch | 턴 전체 | 6/32 | 0 / 7 | 47,584 | 1.81M | ≈286k (17%) |
| held_out | 목차 + batch | 최근 2단계 | 8/32 | 1 / 9 | 41,001 | 1.55M | ≈95k (7%) |

다시 보낸 추론은 기록된 추론 글자 수 ÷ 4로 어림했다.

**결과**
- **다시 보낸 추론은 약 2/3 줄었다**(두 세트 합, 검색 ≈327k → 109k, 목차 + batch ≈442k → 167k토큰).
- **전체 토큰은 검색 3%, 목차 + batch 10%만 줄었다.**
  - 다시 보낸 추론은 원래 입력의 7–17%뿐이었다.
  - 입력의 대부분은 요청마다 다시 가는 도구 결과, 함수 정의, 목차다.
- **통과는 판정할 만큼 다르지 않다.**
  - 두 세트 합(방식마다 56실행): 검색 20 → 17, 목차 + batch 21 → 19. held_out은 같거나 +2, design은 −3, −4다.
  - Fisher 정확 검정 p = 0.39(design 목차), 0.57(전체 41/112 대 36/112).
  - 같은 설정의 두 회차끼리도 결과가 다른 과업이 6–25%다.
  - `turn`과 `recent`의 결과가 갈린 15쌍 중 14쌍은 프롬프트가 같은 처음 세 요청 안에서 이미 다른 호출을 했다. 그래서 차이의 대부분은 샘플링(temperature 1.0)으로 보인다. 다만 이것만으로 `recent`의 영향이 없다고 할 수는 없다.
- design의 1b 20실행은 느린 서버에서 늘린 시간 한도로 돌렸다. 비율은 맞췄지만 완전히 같은 조건은 아니다.

**판단.** 기본값은 턴 전체 재전달(`turn`)로 둔다. `recent`는 옵션으로 남긴다.
- 전체 토큰 절감(3–10%)이 작다.
- design에서 통과가 떨어졌을 가능성을 배제할 수 없다.
- 토큰을 크게 줄일 곳은 추론이 아니라 요청마다 다시 가는 도구 결과와 함수 정의다.

**필요한 함수를 다 찾은 뒤의 실패.** 필요한 함수를 모두 성공적으로 부른 뒤에 실패한 실행(D-after, E-write, E-format, E-content)을 셌다(검색 + 목차 + batch).

| 세트 | 추론 재전달 | 실패 | 다 찾은 뒤 실패 | D-after | E-write | E-format | E-content | 함수를 못 받음(A) |
|---|---|---|---|---|---|---|---|---|
| design | 없음 | 29 | 12 (41%) | 3 | 0 | 4 | 5 | 9 |
| design | 턴 전체 | 21 | 10 (48%) | 2 | 0 | 3 | 5 | 6 |
| design | 최근 2단계 | 28 | 13 (46%) | 3 | 0 | 4 | 6 | 9 |
| held_out | 없음 | 52 | 38 (73%) | 18 | 4 | 0 | 16 | 9 |
| held_out | 턴 전체 | 50 | 36 (72%) | 13 | 4 | 5 | 14 | 12 |
| held_out | 최근 2단계 | 48 | 33 (69%) | 15 | 3 | 2 | 13 | 13 |

- held_out 실패의 약 70%는 a2api가 필요한 함수를 주고 모델이 그 함수를 성공적으로 부른 **뒤**에 났다.
  - 계속 확인 호출을 하다 한도에 걸렸거나(D-after), 답에서 사실을 빠뜨리거나 다른 형태로 썼다(E).
  - 모델 자체의 탐색 종료와 답 구성 문제다.
- 서버의 최대 문맥(65,536)이나 요청당 출력 상한(8,192)에 걸린 요청은 없다. 위 여섯 묶음에서 요청의 입력은 최대 24,234토큰, 출력은 최대 4,300토큰이었고, 출력 한도로 잘린 요청(`finish: length`)은 0이다.
  - 한도 실패는 모두 하네스의 호출 수(모델 12회)·시간(턴당 120초) 한도다. 그 밖에는 provider 500·502가 몇 건 있다.

## 6. 결론: 질문별 답

**1. 모델 호출 설정은 맞게 되어 있었나?**

아니었다. 세 가지가 달랐다.
- temperature 0 고정(카드 권장 1.0·0.95·64)
- 템플릿이 다시 넣도록 된 이전 추론을 매 단계 버림
- 출력 상한 2,048: 숨은 추론까지 세어 답을 잘랐다

세 가지를 바로잡았고, 요청당 최대 토큰은 실측 분포로 8,192로 정했다. 추론 재전달을 최근 2단계로 줄이는 옵션(`recent`)은 전체 토큰을 3–10%만 줄여 기본값으로 하지 않았다(5.4). 효과는 design에서 컸다(검색 5 → 12, 목차 + batch 13 → 15/24). held_out에서는 통과율이 바뀌지 않았다.

**2. a2api가 필요한 API를 잘 가져왔나?**

- **목차 방식:** 필요한 함수(A-Commerce 도구)의 79–88%를 모델에게 주었다(모델 카드 설정 실행 4묶음 기준. 이전 실행은 75–88%).
  - 못 준 경우는 모델이 목차에서 **다른 함수를 고르거나**, 여러 단계 쓰기의 마지막 함수까지 **가지 못한** 것이다(`send_bulk` 등).
  - 같은 몇 과업에 몰려 있다.
- **검색 방식:** 78–95%였다(같은 4묶음).
- **레거시 파사드:** 화면을 모두 주므로 100%다. 다만 과업이 요구하는 기능의 절반 정도는 파사드에 없다(A0).

**3. API는 가져왔지만 입력이 틀린 경우는 누구의 문제였나?**

- **A-Commerce 도구(현대적 정의):**
  - 입력 문제로 과업이 실패한 실행(C)은 리뷰한 11개 실행 묶음, 30개 방식 조합 모두에서 0이다.
  - 실패한 업무 호출은 0–11%(모델 카드 설정 실행은 0–8%)다. 대부분 모델이 근거 없는 값을 지어낸 경우(존재하지 않는 테이블·키 이름)와 업무 규칙 거절이다.
  - 변환에서 빠진 정보는 정적 점검에서 0이다.
- **레거시 파사드:**
  - 원본을 그대로 주면 업무 호출의 54–61%가 실패한다.
  - 대부분은 모델이 schema를 어긴 것이다(문자열 필드에 숫자. 원본에는 이를 막는 계층이 없다).
  - 다음은 **원본 정의에 없는 규칙**이다(페이지 1부터, 날짜 형식, 저장 행의 필수 항목).
  - a2api 변환은 앞의 것을 숫자 → 문자열 변환과 검증으로, 뒤의 것을 코드에서 읽은 설명으로 막는다. 실패는 5–8%로 줄었다.
- **변환 누락:**
  - 리뷰가 찾은 실제 누락은 세 가지였다(클레임 키 형식, 날짜·시각 형식, 저장 행의 필수 항목). 보충한 뒤 그 원인의 실패는 0이 됐다(5.3).
  - 남은 입력 실패는 모델이 설명에 적힌 규칙을 지키지 않았거나 근거 없는 값을 넣은 경우다.

**4. 그러면 무엇이 통과를 막나?**

입력이 아니라 다음 단계들이다(5.1의 단계표).
- D: 한도
- E-content: 답에서 사실 누락
- E-format: 채점이 읽는 표기
- A0: API에 없는 기능

그리고 과업 정의가 도구와 맞지 않는 경우가 하나 있다: `ops-photo-request`의 `kind: photo_request`. 이것은 모델 행동(탐색 종료, 답 구성)과 채점 방식의 영역이다. 도구 표현이나 변환으로 더 줄이기 어렵다.

**재현**

```bash
# 측정(모델 카드 설정이 기본값)
python examples/acommerce/evaluate.py --set held_out --repeat 2 \
    --modes a2api-acom,a2api-acom-names-batch,facade-all,a2api-facade-all --output runs.jsonl
# 단계별 리뷰(실행 때 함수 정의 runs.functions.json 기준)
python examples/acommerce/call_review.py runs.jsonl --out review.md
# 변환 정보 손실 점검
python examples/acommerce/conversion_fidelity.py --acom manifest-acom.json --facade facade-manifest.json
```
