# a-commerce 자체 에이전트로 기존 API와 a2api 평가(main `4c6e415`)

2026-11-03 · 앞선 자체 에이전트 측정은 [39 문서 3.10](39-improvement-results.ko.md) · 단계별 평가 방법은 [41 문서 2절](41-call-stage-review.ko.md)

사용자 요청(2026-11-03): 현재 a-commerce가 쓰는 에이전트 하네스로 기존 API와 a2api를 평가한다. 모델은 두 역할 모두 Muse Glimmer다.

## 1. 무엇을 어떻게 쟀나

**하네스.** a-commerce main `4c6e415`(11/03 08:49 병합)의 자체 에이전트와 평가기(`cargo xtask eval`)를 그대로 썼다.
- `d86a1ff`(3.10 측정) 이후 66커밋. 바뀐 것은 에이전트 런타임이다: 계획, 도구 검색, 이전 결과의 값 연결, 기록 블록, 응답 스트리밍, 대화 기록.
- 평가기, 과업(`eval/`), 파사드 화면(`crates/facade`)은 바뀌지 않았다. 데모 상점 데이터에는 상품 리뷰·위시리스트가 더해졌다.
- 한도는 저장소 설정 그대로다: 턴당 모델 호출 12회, 도구 호출 20회, 60초, 모델 호출 하나당 30초.

**모델.** 에이전트 정의는 작업 모델 `glimmer`, 계획 모델 `spark`를 쓴다. Spark가 설정되지 않으면 Glimmer로 간다(a-commerce `docs/backend/agent.md`).
- 이 측정의 모델 호출 1,198회 모두 `nvidia/Muse-Glimmer-30B-NVFP4`가 답했다(실행 기록의 `model_calls`).
- 시작 전과 세트마다 모델 서버 속도를 확인했다(3회 연속 출력 토큰당 30ms 미만, 실측 16–17ms).

**조건.** 같은 에이전트에 도구 표현만 바꿨다.

| 조건 | 에이전트가 받는 도구 |
|---|---|
| 원본 파사드 | 레거시 운영자 화면 22개 그대로(`--tool-set facade`) |
| a2api 변환 파사드 | 같은 22개를 a2api 게이트웨이로 변환(이름·단어·코드값·설명, 입력 검증). 주문 번호는 그대로 넘김(`a2api_gateway.py --no-lookup`) |
| a2api 변환 파사드 + 주문 번호 조회 | 위 + 사람이 보는 주문 번호를 같은 파사드의 주문 목록 화면으로 키로 바꿈(3.10) |
| A-Commerce 도구(참고) | 에이전트용으로 설계된 현대적 API 253개(`--tool-set acom`). 기존 API도 a2api도 아닌 기준선 |

- 과업: design 12개, held_out 16개. 과업마다 3회(a-commerce가 pass^3을 보고하므로).
- 게이트웨이 검수: 이 스택에서 원본과 게이트웨이에 같은 요청을 보낸 29개 사례가 모두 같은 결과였다(`verify_gateway.py`). 파사드 매니페스트는 변환에 쓴 22개와 같다.
- 단계별 리뷰: `examples/acommerce/own_review.py`가 자체 에이전트 실행 기록을 읽어 41 문서와 같은 규칙으로 판정한다.
  - "모델에게 줌"은 에이전트의 도구 검색이 계획기에 준 후보다.
  - 실패 호출은 에이전트가 본 정의(원본 화면, 변환 화면, A-Commerce 도구)를 기준으로 판정한다.

기록:
- held_out: [원본](traces/own-latest-heldout-raw/README.md) · [a2api](traces/own-latest-heldout-a2api/README.md) · [a2api + 조회](traces/own-latest-heldout-a2api-lookup/README.md) · [A-Commerce](traces/own-latest-heldout-acom/README.md) · [리뷰](traces/own-latest-review-heldout.md)
- design: [원본](traces/own-latest-design-raw/README.md) · [a2api](traces/own-latest-design-a2api/README.md) · [a2api + 조회](traces/own-latest-design-a2api-lookup/README.md) · [A-Commerce](traces/own-latest-design-acom/README.md) · [리뷰](traces/own-latest-review-design.md)
- [evidence](evidence/acommerce-own-latest.json)

## 2. 결과

| 세트 | 조건 | 통과 | pass^3 | pass@3 | 실행당 토큰 중앙값 | 시간 중앙값 | 모델 호출/실행 | 도구 호출/실행 | 실패한 도구 호출 |
|---|---|---|---|---|---|---|---|---|---|
| held_out | 원본 파사드 | 7/48 | 2/16 | 3/16 | 7,512 | 10.0초 | 3.73 | 1.96 | 72/94 (77%) |
| held_out | a2api 변환 | 9/48 | 3/16 | 3/16 | 5,522 | 6.2초 | 2.85 | 1.40 | 21/67 (31%) |
| held_out | a2api 변환 + 조회 | **12/48** | **4/16** | 4/16 | 5,472 | 6.0초 | 2.90 | 1.44 | 15/69 (22%) |
| held_out | A-Commerce(참고) | 11/48 | 3/16 | 4/16 | 12,941 | 11.6초 | 3.50 | 3.69 | 18/177 (10%) |
| design | 원본 파사드 | 0/36 | 0/12 | 0/12 | 8,046 | 12.1초 | 4.81 | 2.36 | 72/85 (85%) |
| design | a2api 변환 | 3/36 | 1/12 | 1/12 | 6,446 | 7.2초 | 3.69 | 2.14 | 15/77 (19%) |
| design | a2api 변환 + 조회 | 3/36 | 1/12 | 1/12 | 5,917 | 7.8초 | 3.56 | 2.11 | 6/76 (8%) |
| design | A-Commerce(참고) | 15/36 | 4/12 | 6/12 | 15,812 | 9.3초 | 3.92 | 8.06 | 10/290 (3%) |

pass^3은 세 번 모두 통과한 과업, pass@3은 한 번이라도 통과한 과업이다.

**읽는 법**
- **통과는 a2api가 원본보다 많지만 판정할 만한 차이는 아니다.**
  - held_out 7 → 9 → 12/48, design 0 → 3/36.
  - 두 세트 합 7/84 대 15/84, Fisher p = 0.11.
- **도구 호출 성공은 분명히 다르다.**
  - 실패한 도구 호출이 77–85%에서 8–31%로 줄었다(합 144/179 대 21/145, p ≈ 1e-12).
  - 필요한 화면을 성공적으로 부른 비율(3절)은 held_out 33% → 88%, design 21% → 52%다.
- **비용도 줄었다.** 원본 대비 a2api + 조회는 실행당 토큰 −27%, 시간 −36–40%, 모델 호출 −22–26%다. 실패한 호출을 고쳐 다시 계획하는 일이 줄었기 때문이다.
- **A-Commerce 도구(참고)와 비교**
  - held_out에서 a2api + 조회(12/48)는 A-Commerce 도구(11/48)와 비슷하다.
  - design에서는 A-Commerce 도구가 15/36으로 훨씬 높다. 파사드에 없는 기능을 요구하는 과업이 많기 때문이다(A0, 3절).
- **provider 오류.** 12실행에서 답 생성 단계의 모델 호출이 500(또는 1초 시간 초과)을 받았다(원본 3, a2api 4, a2api + 조회 4, A-Commerce 1).
  - 이 12실행은 어느 조건에서도 통과하지 못한 과업이다. 빼고 세어도 모든 조건의 통과 수가 같다.
  - held_out md-best-sellers-this-month에서는 같은 1,035토큰 답 생성 프롬프트(도구 결과 없음)가 a2api 쪽에서 6번 중 4번, 원본에서 3번 중 0번 500을 받았다. 프롬프트가 같으므로 표현 탓이 아니라 서버 쪽 무작위 오류로 본다.

## 3. 단계별 리뷰: API를 잘 가져왔나, 입력이 맞았나

필요한 함수(과업의 필수 A-Commerce 도구, 파사드는 a-commerce 문서의 대응 화면):

| 세트 | 조건 | 파사드에 있는 필요 함수 | 도구 검색이 줌 | 불렀음 | 성공 |
|---|---|---|---|---|---|
| held_out | 원본 | 24 | 21 (88%) | 13 (54%) | 8 (33%) |
| held_out | a2api | 24 | 24 (100%) | 21 (88%) | 15 (63%) |
| held_out | a2api + 조회 | 24 | 24 (100%) | 21 (88%) | **21 (88%)** |
| held_out | A-Commerce(참고) | 48 | 39 (81%) | 36 (75%) | 36 (75%) |
| design | 원본 | 42 | 30 (71%) | 15 (36%) | 9 (21%) |
| design | a2api | 42 | 39 (93%) | 25 (60%) | 19 (45%) |
| design | a2api + 조회 | 42 | 39 (93%) | 26 (62%) | **22 (52%)** |
| design | A-Commerce(참고) | 63 | 55 (87%) | 46 (73%) | 44 (70%) |

- **찾기:** 에이전트의 도구 검색은 같다. 그런데 변환 이름(`get_promotion_grid_list`)과 요약으로 필요한 화면을 더 많이 찾았다(71–88% → 93–100%). 검색이 도구 이름에 가중치를 주기 때문이다(3.10).
- **부르기·성공:** 원본은 화면을 찾고도 첫 호출에서 실패해 다시 계획하다 끝나는 경우가 많았다(아래 실패 원인).

처음 막힌 단계:

| 세트 | 조건 | 통과 | A0 | A | B | C | D | E-write | E-format | E-content |
|---|---|---|---|---|---|---|---|---|---|---|
| held_out | 원본 | 7 | 18 | 3 | 8 | 5 | 0 | 0 | 0 | 7 |
| held_out | a2api | 9 | 18 | 0 | 3 | 6 | 0 | 0 | 0 | 12 |
| held_out | a2api + 조회 | 12 | 18 | 0 | 3 | 0 | 0 | 0 | 3 | 12 |
| held_out | A-Commerce(참고) | 11 | — | 9 | 0 | 0 | 1 | 3 | 4 | 20 |
| design | 원본 | 0 | 21 | 9 | 0 | 1 | 0 | 0 | 0 | 5 |
| design | a2api | 3 | 21 | 3 | 3 | 0 | 0 | 0 | 0 | 6 |
| design | a2api + 조회 | 3 | 21 | 3 | 2 | 2 | 0 | 0 | 0 | 5 |
| design | A-Commerce(참고) | 15 | — | 6 | 3 | 0 | 0 | 0 | 2 | 10 |

(D는 D-before + D-after. 한도에 걸린 실행은 A-Commerce 조건의 3건뿐이고, 그중 2건은 그 전에 A로 판정됐다.)

- **A0이 파사드 조건 실패의 44–64%다.** 파사드에 그 기능이 없다.
  - 필요한 함수 중 파사드에 없는 것이 있는 과업은 held_out 16개 중 7개, design 12개 중 7개다. held_out의 mk-winback은 그래도 통과했다.
  - 변환으로 풀 수 없는 실패다.
- **원본의 A·B·C가 a2api에서 대부분 사라졌다.** 남은 실패는 E-content(답에서 사실 누락)다.

### 실패한 호출의 원인

**원본 파사드:** 실패 144건 중 125건이 `Invalid paging.`이다(held_out 61/72, design 64/72).
- 에이전트는 `pageNo: 0`을 보낸다. 원본 schema는 `minimum: 0`이고 설명은 "Page no."뿐이라 0도 맞는 값이다. 화면은 1부터만 받는다.
- **원본 정의에 없는 규칙**(source:undocumented)이다. a2api 변환 설명("from 1")이 이 실패를 없앴다.
- 나머지는 주문 번호 404(키만 받음), 매출 비교 기간 규칙, 할인율 범위, 날짜 형식이다.

**a2api 변환 파사드 + 조회:** 실패 21건을 사람이 다시 읽고 나눴다.

| 원인 | held_out | design | 누구의 문제 |
|---|---|---|---|
| 이전 단계의 ID를 빈 값(`""`)으로 보냄 | 7 | 0 | 에이전트의 값 연결 + 정의에 없는 관계(아래) |
| 매출 비교 기간 규칙(`same_weekday_last_4_weeks`는 7일까지) | 3 | 1 | 원본·변환 설명에 없음(변환 보충 후보) |
| 업무 상태 거절(409) | 3 | 0 | 업무 |
| 질문·결과에 없는 값을 지어냄 | 2 | 3 | 모델 |
| 설명에 적힌 필수 항목 누락(배너 이미지) | 0 | 2 | 모델 |

- 조회 없는 a2api에서는 위에 더해 주문 번호를 키 자리에 넣은 404가 held_out 6, design 3건 있다. 변환 설명은 "Key such as ord_20402"라고 적고 있다(model:described). 조회가 이를 없앴다.
- **변환에서 정보를 잃어 난 실패는 없다.** 남은 정보 부족 두 가지(기간 규칙, 관계)는 원본 정의에도 없던 것이다.

### 빈 ID: 원본 정의에 없는 관계

held_out 세 과업에서 a2api 쪽 에이전트가 필요한 데이터를 찾은 뒤, 다음 단계에 ID를 빈 값으로 보냈다(조건마다 각 과업 3회 중 일부 또는 전부).

| 과업 | 앞 단계 결과 | 다음 호출 |
|---|---|---|
| mk-pause-knit-until-monday | `get_promotion_grid_list` → `promotion_id: promo_autumn_knit` | `save_promotion_list` `{"promotion_id": ""}` → 422 |
| md-how-many-left | `get_product_grid_list` → `product_id: prd_rain_parka` | `get_product_detail_info_v2` `{"product_id": ""}` → 404 |
| ops-photo-request | `get_order_grid_list` → `member_id: cus_riley` | `save_customer_message_send` `{"member_id": "", "text": ""}` → 422 |

- 계획은 `{"promotion_id": ""}`에 `"uses": ["find_knit_sale"]`를 붙여 "앞 단계에서 채운다"고 쓴다.
- a-commerce 런타임은 이 값을 매니페스트의 `consumes`/`produces` 슬롯으로만 채운다(`crates/agent/src/executor.rs` `bind`).
- **파사드 22개 화면은 원본·변환 모두 `consumes: []`, `produces: []`다.** 그래서 파사드에서는 앞 결과의 ID가 다음 호출로 이어지지 않는다.
- 원본에서도 같은 일이 있다(`ctgNo: ""`, `mbrNo: ""`). 다만 대부분은 그 전에 페이지 오류로 멈췄다.
- 이것은 레거시 정의에 없는 정보다. 변환이 정규화한 필드 이름(`promotion_id`, `product_id`, `member_id`)으로 채울 수 있다. 이 측정에서는 게이트웨이가 원본 값을 그대로 넘겼다.

## 4. 과업별

held_out(✓ 통과, ✗ 실패, 3회):

| 과업 | 파사드에 기능 | 원본 | a2api | a2api + 조회 | A-Commerce |
|---|---|---|---|---|---|
| md-out-of-stock-30-days | 있음 | ✗✓✗ | ✓✓✓ | ✓✓✓ | ✓✓✓ |
| mk-viewed-not-purchased | 있음 | ✓✓✓ | ✓✓✓ | ✓✓✓ | ✓✓✓ |
| mk-winback | 일부 | ✓✓✓ | ✓✓✓ | ✓✓✓ | ✗✗✗ |
| ops-change-address-in-transit | 있음 | ✗✗✗ | ✗✗✗ | **✓✓✓** | ✗✗✗ |
| ops-unfulfilled-3-days | 있음 | ✗✗✗ | ✗✗✗ | ✗✗✗ | ✗✓✓ |
| md-how-many-left | 없음 | ✗✗✗ | ✗✗✗ | ✗✗✗ | ✓✓✓ |
| 나머지 10과업 | — | ✗ | ✗ | ✗ | ✗ |

design에서 파사드 조건이 통과한 것은 md-low-stock-before-weekend뿐이다(원본 ✗✗✗, a2api ✓✓✓, a2api + 조회 ✓✓✓, A-Commerce ✓✓✓). 원본은 같은 화면에서 페이지 오류로 실패했다.

## 5. 이전 측정(`d86a1ff`, 3.10)과 비교

| 세트 | 조건 | `d86a1ff`(각 2회) | `4c6e415`(각 3회) |
|---|---|---|---|
| held_out | 원본 파사드 | 5/32 (16%) | 7/48 (15%) |
| held_out | a2api 변환 | 6/32 (19%) | 9/48 (19%) |
| held_out | a2api 변환 + 조회 | 8/32 (25%) | 12/48 (25%) |
| design | 세 조건 | 0/24 | 0 · 3 · 3/36 |

- 에이전트 런타임이 바뀌었지만 파사드 조건의 held_out 통과율은 같다. 실패한 화면 호출 비율도 비슷하다(원본 73% → 77%, a2api + 조회 13% → 22%).
- design에서 a2api 쪽이 처음으로 통과했다(md-low-stock-before-weekend, 3/3).

## 6. 결론

**1. 같은 에이전트·같은 모델에서 a2api는 기존 API(레거시 파사드)보다 나은가?**
- 도구 호출에서는 분명히 낫다.
  - 실패한 호출 77–85% → 8–22%
  - 필요한 화면 성공 21–33% → 52–88%
  - 토큰 −27%, 시간 −36–40%
- 과업 통과는 높지만(7 → 15/84) 통계적으로 판정할 차이는 아니다(p = 0.11).

**2. 통과를 막는 것은?**
- 파사드에 없는 기능(A0): 파사드 조건 실패의 44–64%. 변환으로 풀 수 없다.
- 답 구성(E-content): 데이터를 다 받은 뒤 답에서 사실을 빠뜨린다. a2api 변환 + 조회의 held_out 실패 36건 중 15건이 E다.
- 빈 ID: 원본 정의에 없는 관계 때문에 에이전트가 앞 결과의 ID를 다음 호출로 잇지 못했다(held_out 3과업).

**3. 변환에서 정보가 빠졌나?** 아니다.
- 변환 때문에 난 실패는 없다.
- 남은 정보 부족 두 가지는 원본 정의에도 없던 것이다: 매출 비교 기간 규칙, 화면 간 ID 관계.
- 둘 다 화면 코드에서 읽어 보충할 수 있다(41 문서 5.3과 같은 방식). 이번 측정에는 넣지 않았다.

**재현**

```bash
# a-commerce main 스택 + 평가기(각 조건, 세트마다)
xtask eval --base http://127.0.0.1:7000 --set held_out --tool-set facade --repeat 3 --reset --logs RUN-logs --out RUN.md
# a2api 조건: 에이전트만 게이트웨이를 보게 함(ACOM_COMMERCE_URL), 조회 없이는 --no-lookup
python examples/acommerce/a2api_gateway.py --port 7011 --commerce http://127.0.0.1:7001 [--no-lookup]
# 단계별 리뷰
python examples/acommerce/a2api_gateway.py --dump facade-converted.json --manifest facade-manifest.json
python examples/acommerce/own_review.py RAW.md A2API.md LOOKUP.md ACOM.md --mode own-facade-raw --mode own-facade-a2api \
    --mode own-facade-a2api-lookup --mode own-acom --converted facade-converted.json --out review.md
```
