# a-commerce 자체 에이전트 + GPT-6-Luna(Codex CLI): 기존 API와 a2api

2026-11-05 · 같은 하네스·같은 조건의 Muse Glimmer 결과는 [42 문서](42-own-agent-latest.ko.md)

사용자 요청(2026-11-05): Codex CLI로 gpt6-luna를 써서 레거시와 a2api를 테스트한다. 하네스는 a-commerce의 것을 쓴다.

## 1. 무엇을 어떻게 쟀나

**하네스.** 42 문서와 같다. a-commerce main `4c6e415`의 자체 에이전트와 평가기(`cargo xtask eval`)를 그대로 썼다.
- 라우팅, 도구 검색, 계획, 값 연결, 답 생성, 채점은 바꾸지 않았다.
- 한도도 저장소 설정 그대로다: 턴당 모델 호출 12회, 도구 호출 20회, 60초, 모델 호출 하나당 30초.
- 바뀐 것은 모델뿐이다. 에이전트의 작업 모델 주소(`GLIMMER_BASE_URL`)와 모델 ID(`GLIMMER_MODEL=gpt-6-luna`)만 바꿨다. Spark가 설정되지 않아 계획 모델도 같은 곳으로 간다.

**모델.** `gpt-6-luna`(GPT-6-Luna). 추론 강도는 이 모델의 기본값 `medium`이다(Codex 모델 목록).
- Codex CLI `0.164.0-alpha.11.1`(Codex 데스크톱 앱에 들어 있는 것), ChatGPT 로그인이다.
- 모든 실행의 모델 호출은 실행 기록에 `gpt-6-luna`로 남았다.

**Codex CLI 연결.** `examples/acommerce/codex_model.py`가 OpenAI 호환 `/v1/chat/completions`를 받는다. 에이전트의 모델 호출 하나를 `codex exec` 한 번으로 돌린다.
- 요청의 system 메시지가 Codex의 기본 지시를 대신한다(`model_instructions_file`). 나머지 메시지가 프롬프트다.
- 출력 schema는 a-commerce의 `structured_output: prompt` 방식으로 요구한다. schema를 지시에 넣고, 답에서 JSON을 읽는다.
  - Codex의 `--output-schema`는 strict 모드로 보낸다. 에이전트의 schema(선택 필드, 자유 형식 `args`)는 strict에 맞지 않는다.
- Codex의 도구는 모두 끄고, 빈 폴더에서 읽기 전용·일회성으로, 사용자 설정 없이 돌린다(인증만 `~/.codex`).
- 지시 첫 줄에 "도구가 없으니 바로 답하라"를 넣는다.
  - Codex는 꺼도 code mode `exec` 도구를 목록에 남긴다. 이 줄이 없으면 모델이 가끔 그 도구를 먼저 부르고(실패), 다시 답해 그 호출의 입력 토큰이 두 배가 됐다.
  - 이 줄을 넣고는 같은 요청 6번 모두 한 번에 답했다.
- 남는 Codex 자체 프롬프트는 호출마다 고정 **4,680토큰**이다(빈 요청으로 측정). 아래 토큰은 Codex가 보고한 값과, 이 고정분을 뺀 값(순 토큰)을 함께 적는다.
- `temperature`·`max_tokens`는 넘기지 않는다(Codex가 정함). 스트리밍 요청에는 400을 돌려 에이전트가 한 번에 받는 방식을 쓰게 했다.

**조건.** 과업마다 3회, held_out 16개·design 12개.

| 조건 | 에이전트가 받는 도구 |
|---|---|
| 기존 API(원본 파사드) | 레거시 운영자 화면 22개 그대로 |
| a2api | 같은 22개를 a2api 게이트웨이로 변환(주문 번호 조회 포함, 게이트웨이 기본값) |
| A-Commerce 도구(참고) | 에이전트용으로 설계된 API 253개 |

**실행 상태.**
- 11/05 11:20–12:51, Codex 호출 827회 모두 성공했다(오류 0).
- 호출당 시간 중앙값 4.9초(p90 9.4초, 최대 17.3초)다.
- 한도에 걸린 턴은 0이다. 같은 하네스 한도 안에서 돌았다.

기록:
- held_out: [원본](traces/luna-heldout-raw/README.md) · [a2api](traces/luna-heldout-a2api/README.md) · [A-Commerce](traces/luna-heldout-acom/README.md) · [리뷰](traces/luna-review-heldout.md)
- design: [원본](traces/luna-design-raw/README.md) · [a2api](traces/luna-design-a2api/README.md) · [A-Commerce](traces/luna-design-acom/README.md) · [리뷰](traces/luna-review-design.md)
- [evidence](evidence/acommerce-own-gpt-6-luna.json)

## 2. 결과

| 세트 | 조건 | 통과 | pass^3 | pass@3 | 토큰 중앙값(순) | 시간 중앙값 | 모델 호출/실행 | 도구 호출/실행 | 실패한 도구 호출 |
|---|---|---|---|---|---|---|---|---|---|
| held_out | 기존 API | 10/48 | 3/16 | 4/16 | 23,694 (8,615) | 22.5초 | 3.29 | 2.17 | 62/104 (60%) |
| held_out | a2api | 11/48 | 3/16 | 4/16 | 21,780 (5,717) | 15.3초 | 2.85 | 2.85 | **5/137 (4%)** |
| held_out | A-Commerce(참고) | 9/48 | 2/16 | 4/16 | 19,504 (8,772) | 16.2초 | 2.65 | 2.60 | 3/125 (2%) |
| design | 기존 API | 2/36 | 0/12 | 2/12 | 26,676 (9,408) | 22.4초 | 4.22 | 2.92 | 67/105 (64%) |
| design | a2api | 6/36 | 1/12 | 3/12 | 22,598 (7,816) | 14.5초 | 3.69 | 2.81 | **2/101 (2%)** |
| design | A-Commerce(참고) | 7/36 | 2/12 | 3/12 | 23,845 (10,440) | 15.9초 | 3.33 | 7.64 | 6/275 (2%) |

**Muse Glimmer(42 문서, 같은 하네스·같은 과업·각 3회)와 비교**

| 조건 | Glimmer 통과 | GPT-6-Luna 통과 | Glimmer 실패한 도구 호출 | GPT-6-Luna 실패한 도구 호출 |
|---|---|---|---|---|
| 기존 API | 7/84 | 12/84 | 144/179 (80%) | 129/209 (62%) |
| a2api | 15/84 | 17/84 | 21/145 (14%) | **7/238 (3%)** |
| A-Commerce(참고) | 26/84 | 16/84 | 28/467 (6%) | 9/400 (2%) |

(Glimmer의 a2api는 42 문서의 "a2api 변환 + 조회"다. 이번 a2api와 같은 게이트웨이 설정이다.)

**읽는 법**
- **도구 호출은 a2api에서 거의 실패하지 않는다.** GPT-6-Luna는 실패한 호출 62% → 3%다(129/209 대 7/238, p ≈ 1e-12). 같은 a2api에서 Glimmer(14%)보다도 적다.
- **통과는 a2api가 많지만 판정할 만한 차이는 아니다.**
  - GPT-6-Luna 12 → 17/84(p = 0.41)
  - Glimmer 7 → 15/84(p = 0.11)
- **비용**: a2api는 기존 API보다 순 토큰 −17–34%, 시간 −32–35%, 모델 호출 −13%다.
- **모델 차이는 판정할 수 없다.**
  - GPT-6-Luna가 기존 API(12 대 7)와 a2api(17 대 15)에서 조금 많고, A-Commerce 도구에서는 적다(16 대 26, design 7 대 15, p = 0.07).
  - 셋 다 통계적으로 구별되지 않는다.

**채점 주의: 답 문장과 화면 블록.** a-commerce 채점은 사실의 숫자가 사람이 보는 것(답 문장 + 화면 블록)에 있으면 통과로 센다. 통과한 실행을 답 문장만으로 다시 보면:

| 조건 | Glimmer 통과(문장만으로도) | GPT-6-Luna 통과(문장만으로도) |
|---|---|---|
| 기존 API | 7 (7) | 12 (8) |
| a2api | 15 (14) | 17 (9) |
| A-Commerce(참고) | 26 (20) | 16 (8) |

- GPT-6-Luna 통과의 약 절반은 사실의 숫자가 답 문장에는 없고 화면 블록(표·미리보기)에만 있다.
  - 블록이 그 사실을 실제로 보여 주는 경우는 정당하다. 예: md-low-stock-before-weekend의 재고 표에 4와 7이 있다.
  - 우연인 경우도 있다(4절 md-best-sellers-this-month).
- 답 문장만으로 세면 a2api 효과가 Glimmer는 7 → 14, GPT-6-Luna는 8 → 9다. GPT-6-Luna는 답 문장에 세부를 덜 쓰고 블록에 맡기는 경향이 있다.

## 3. 단계별 리뷰

필요한 함수(과업의 필수 A-Commerce 도구, 파사드는 대응 화면):

| 세트 | 조건 | 필요 함수 | 도구 검색이 줌 | 불렀음 | 성공 |
|---|---|---|---|---|---|
| held_out | 기존 API | 24 | 21 (88%) | 17 (71%) | 9 (38%) |
| held_out | a2api | 24 | 24 (100%) | 24 (100%) | **23 (96%)** |
| held_out | A-Commerce(참고) | 48 | 39 (81%) | 33 (69%) | 33 (69%) |
| design | 기존 API | 42 | 30 (71%) | 19 (45%) | 11 (26%) |
| design | a2api | 42 | 39 (93%) | 25 (60%) | **25 (60%)** |
| design | A-Commerce(참고) | 63 | 54 (86%) | 44 (70%) | 44 (70%) |

처음 막힌 단계:

| 세트 | 조건 | 통과 | A0 | A | B | C | D | E-write | E-format | E-content |
|---|---|---|---|---|---|---|---|---|---|---|
| held_out | 기존 API | 10 | 15 | 3 | 4 | 8 | 0 | 0 | 0 | 8 |
| held_out | a2api | 11 | 15 | 0 | 0 | 1 | 0 | 0 | 0 | **21** |
| held_out | A-Commerce(참고) | 9 | — | 9 | 3 | 0 | 0 | 3 | 2 | 22 |
| design | 기존 API | 2 | 21 | 8 | 0 | 2 | 0 | 0 | 0 | 3 |
| design | a2api | 6 | 21 | 3 | 2 | 0 | 0 | 0 | 0 | 4 |
| design | A-Commerce(참고) | 7 | — | 6 | 5 | 0 | 0 | 0 | 0 | 18 |

- **기존 API의 실패는 모델이 바뀌어도 같다.**
  - 실패한 호출 129건 중 96건(74%)이 `Invalid paging.`이다. Glimmer는 144건 중 125건이었다.
  - GPT-6-Luna도 원본 schema(`minimum: 0`, 설명 "Page no.")대로 `pageNo: 0`을 보냈다.
  - 원본 정의에 없는 규칙은 더 강한 모델로도 풀리지 않는다. a2api 변환 설명("from 1")이 막았다.
- **a2api에서는 필요한 데이터를 거의 다 받는다(held_out 96%).** 남은 실패는 답(E-content)이다.
  - a2api의 E-content 25건 중 16건은 답에 숫자 하나만 빠졌다(Glimmer는 17건 중 8건).
  - 예: ops-change-address-in-transit. 주문 상세를 받고 "Order 27184 is already in transit with UPS"라고 바르게 답했지만, 채점이 요구하는 "since Nov 2"의 2가 없다. 3회 모두 같다. Glimmer는 이 과업을 a2api에서 3/3 통과했다.
- **A-Commerce 도구(참고)에서도 같다.**
  - E-content가 실패의 대부분이다(design 29건 중 18, held_out 39건 중 22). 그중 18건은 숫자 하나만 빠졌다.
  - 예: md-overcoat-runs-small에서 리뷰 요약을 받고 "4.6"을 쓰지 않았다. ops-wismo-tracking-stuck에서는 운송장 번호를 쓰지 않았다.
  - 이 하네스의 답 생성 지시와 숫자 채점에서는 GPT-6-Luna의 답이 Glimmer보다 세부를 덜 쓴다.

### a2api에서 실패한 호출 7건

| 과업 | 호출 | 원인 | 누구의 문제 |
|---|---|---|---|
| mk-pause-knit-until-monday(3회) | `save_promotion_list` 행에 `promotion_id`를 넣지 않음 → 422 | 앞 단계 결과의 ID를 잇지 못함(아래) | 정의에 없는 관계 |
| md-end-of-season-markdown(1회) | `category_id: ""` → 422 | 같음 | 정의에 없는 관계 |
| ops-photo-request(2회) | `save_customer_message_send`에 `order_id` 없이 `ask_for_photos` → "Say which order the message is about." | 변환 설명이 "optionally about an order"라고 함. 코드는 `custom` 외의 모든 메시지에 주문을 요구한다(`send_customer_message.rs`) | **변환 설명의 누락** |
| mk-hero-free-next-weekend(1회) | `target_member_grade: "VIP"` → "Invalid member grade code." | 설명은 등급 코드 G00, G01…을 적고 있음 | 모델 |

- **정의에 없는 관계**(42 문서 3절): 파사드 매니페스트의 `consumes`/`produces`가 비어 있다. 런타임이 앞 결과의 ID를 다음 호출에 채우지 못한다. Glimmer는 `""`를 보냈고, GPT-6-Luna는 필드를 뺐다.
- **변환 설명의 누락**: 이번에 새로 찾은 것이다. 레거시 정의에도 없고, 변환이 보탠 설명이 오히려 "선택"이라고 했다. 41 문서 5.3처럼 코드의 규칙을 설명에 보태면 막을 수 있다. 이번 측정에는 넣지 않았다.

## 4. 과업별(held_out, 3회)

| 과업 | 파사드에 기능 | Glimmer 기존 | Glimmer a2api | GPT-6-Luna 기존 | GPT-6-Luna a2api |
|---|---|---|---|---|---|
| md-best-sellers-this-month | 없음 | ✗✗✗ | ✗✗✗ | **✓✓✓** | **✓✓✓** |
| md-out-of-stock-30-days | 있음 | ✗✓✗ | ✓✓✓ | ✗✓✗ | ✓✗✓ |
| mk-viewed-not-purchased | 있음 | ✓✓✓ | ✓✓✓ | ✓✓✓ | ✓✓✓ |
| mk-winback | 일부 | ✓✓✓ | ✓✓✓ | ✓✓✓ | ✓✓✓ |
| ops-change-address-in-transit | 있음 | ✗✗✗ | **✓✓✓** | ✗✗✗ | ✗✗✗ |
| 나머지 11과업 | — | ✗ | ✗ | ✗ | ✗ |

- md-best-sellers-this-month의 GPT-6-Luna 통과 6회는 **채점의 우연**이다.
  - 필요한 도구(`get_sales_overview`)에 대응하는 화면이 없다. 과업이 기대하는 사실은 "이번 달은 11/1–11/6이라고 말한다"다.
  - GPT-6-Luna는 상품 목록을 불러 표로 보여 주고 "이번 달 판매 데이터가 없다"고 답했다. 답 문장에 기간은 없다.
  - 그런데 보여 준 상품 표의 재고 숫자에 1과 6이 있어 채점이 통과로 셌다.
  - Glimmer는 목록을 부르지 않았다(a2api, 0단계 계획). 원본에서는 페이지 오류로 목록을 받지 못했다.
  - 이 6회를 빼면 held_out은 GPT-6-Luna 기존 7/48, a2api 8/48이다.
- design에서 a2api가 통과한 과업: md-end-of-season-markdown ✓✓✓(기존 ✗✗✗), md-low-stock-before-weekend ✓✓✗(기존 ✗✗✓), mk-hero-free-next-weekend ✓✗✗(기존 ✓✗✗).

## 5. 결론

**1. GPT-6-Luna로 바꾸면 기존 API와 a2api의 차이가 달라지나?**
- 방향은 같다.
  - 기존 API의 실패 원인(페이지 0 등 정의에 없는 규칙)은 모델이 바뀌어도 그대로다.
  - a2api는 그 실패를 거의 없앴다(GPT-6-Luna 62% → 3%, Glimmer 80% → 14%).
- 통과율 차이는 두 모델 모두 판정할 만큼 크지 않다(GPT-6-Luna 12 → 17/84, Glimmer 7 → 15/84).
- 답 문장만으로 세면 a2api 효과는 Glimmer 7 → 14, GPT-6-Luna 8 → 9다(2절 채점 주의).

**2. 무엇이 다른가?**
- GPT-6-Luna는 a2api 함수를 더 정확히 부른다(실패한 호출 3% 대 14%, held_out 필요 함수 성공 96% 대 88%).
- 대신 답 문장에서 세부(숫자 하나)를 더 자주 빠뜨린다(a2api E-content 25건 중 16건 대 Glimmer 17건 중 8건).
- 통과한 경우도 절반은 숫자가 화면 블록에만 있다. 그중에는 우연히 맞은 것(md-best-sellers-this-month 6회)도 있다.
- 통과 수가 비슷한 것은 호출 정확도와 답 구성의 차이가 서로 상쇄되기 때문이다. a-commerce의 라이브 데모는 모든 모델 호출을 Glimmer로 보낸다(a-commerce `docs/backend/agent.md`). 답 생성 지시가 다른 모델에 맞는지는 이 측정이 따로 보지 않았다.

**3. a2api 쪽에서 더 고칠 것은?**
- 변환 설명 보충: 메시지 발송의 "주문이 필요한 경우"(이번에 찾음), 매출 비교 기간 규칙(42 문서).
- 화면 간 관계: 게이트웨이가 변환된 필드 이름으로 `consumes`/`produces`를 채우면, 앞 결과의 ID를 다음 호출로 이을 수 있다.
- 나머지 실패는 파사드에 없는 기능(A0)과 답 구성(E)이다. 변환으로 풀 수 없다.

**재현**

```bash
# Codex CLI 모델 어댑터(Codex 데스크톱 앱의 codex, ChatGPT 로그인)
python examples/acommerce/codex_model.py --port 7020 --model gpt-6-luna --effort medium --overhead --log calls.jsonl
# a-commerce 스택: 에이전트의 모델만 어댑터로
A2API_MODEL_BASE_URL=http://127.0.0.1:7020/v1 A2API_MODEL=gpt-6-luna python examples/acommerce/stack.py up
# 평가와 리뷰는 42 문서와 같음
xtask eval --base http://127.0.0.1:7000 --set held_out --tool-set facade --repeat 3 --reset --logs RUN-logs --out RUN.md
python examples/acommerce/own_review.py RAW.md A2API.md ACOM.md --mode own-facade-raw --mode own-facade-a2api-lookup \
    --mode own-acom --converted facade-converted.json --out review.md
```
