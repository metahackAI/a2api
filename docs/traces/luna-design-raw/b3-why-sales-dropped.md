# b3-why-sales-dropped — luna-design-raw

[← 실행 묶음](README.md)

**과업**

> Why did sales drop yesterday?

- 답에 있어야 할 사실: Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$4,660, -20%); 201 orders against 247
- 답에 있어야 할 사실: M and L sold out on the three best sellers (chore coat, rain parka, denim jacket): about -$2,700
- 답에 있어야 할 사실: the weekly email did not go out (Thu 08:00 list import failed): about -$1,300; -$660 is not explained

### GPT-6-Luna · 원본 파사드 · 1회차 · ✗ 실패

토큰 18,684 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> Why did sales drop yesterday?

- 라우팅: Insights agent (the request names this agent's work)
- 도구 검색 후보: 4 candidates: getSaleAnlsGridList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt, getMbrGrdList
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-05","cmprBaseCd":"2","srchStrtDt":"2026-11-05"} ``
1. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-05","cmprBaseCd":"2","srchStrtDt":"2026-11-05"} ``
   ← 결과: `` {"list":[{"diffRt":-0.0559,"ordCnt":201,"diffAmt":-1080.0,"saleAmt":18240.0,"srchEndDt":"2026-11-05","cmprOrdCnt":211,"srchStrtDt":"2026-11-05","cmprSaleAmt":19320.0}]} ``
- check: Numbers not in the results: 5.59

**답변 1**
> Yesterday’s sales were $18,240, down $1,080 from the comparison period, with 201 orders versus 211. The figures don’t explain what caused the drop.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (22900, 4660, 20, 247 not shown); fact "M and L sold out on the three best sellers (chore coat, rain" (2700 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8, 0, 1300, 660 not shown)

### GPT-6-Luna · 원본 파사드 · 2회차 · ✗ 실패

토큰 34,596 · 모델 호출 5회 · 도구 호출 4회

**질문 1**
> Why did sales drop yesterday?

- 라우팅: Insights agent (the request names this agent's work)
- 도구 검색 후보: 4 candidates: getSaleAnlsGridList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt, getMbrGrdList
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-11-05"} ``; `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-10-23"} ``
1. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-11-05"} ``
   ← 결과: `` {"list":[{"diffRt":-0.2035,"ordCnt":201,"diffAmt":-4660.0,"saleAmt":18240.0,"srchEndDt":"2026-11-05","cmprOrdCnt":247,"srchStrtDt":"2026-11-05","cmprSaleAmt":22900.0}]} ``
2. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-10-23"} ``
   ← 실패: `` {"code":"invalid_period","class":"invalid_input","message":"same_weekday_last_4_weeks compares periods of 7 days at most; this one has 14. Use previous_period or custom.","next_tool":null} ``
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-10-23"} ``
3. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-10-23"} ``
   ← 실패: `` {"code":"invalid_period","class":"invalid_input","message":"same_weekday_last_4_weeks compares periods of 7 days at most; this one has 14. Use previous_period or custom.","next_tool":null} ``
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-05","cmprBaseCd":"2","srchStrtDt":"2026-11-05"} ``
4. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-05","cmprBaseCd":"2","srchStrtDt":"2026-11-05"} ``
   ← 결과: `` {"list":[{"diffRt":-0.0559,"ordCnt":201,"diffAmt":-1080.0,"saleAmt":18240.0,"srchEndDt":"2026-11-05","cmprOrdCnt":211,"srchStrtDt":"2026-11-05","cmprSaleAmt":19320.0}]} ``
- check: Numbers not in the results: 20.35, 5.59

**답변 1**
> Yesterday, Thu Nov 5, sales were $18,240 across 201 orders, down $4,660 from the first comparison and $1,080 from the second. The figures show the drop, but not what caused it.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (22900, 20, 247 not shown); fact "M and L sold out on the three best sellers (chore coat, rain" (2700 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8, 0, 1300, 660 not shown)

### GPT-6-Luna · 원본 파사드 · 3회차 · ✗ 실패

토큰 26,376 · 모델 호출 4회 · 도구 호출 3회

**질문 1**
> Why did sales drop yesterday?

- 라우팅: Insights agent (the request names this agent's work)
- 도구 검색 후보: 4 candidates: getSaleAnlsGridList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt, getMbrGrdList
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-11-05"} ``; `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-10-23"} ``
1. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-11-05"} ``
   ← 결과: `` {"list":[{"diffRt":-0.2035,"ordCnt":201,"diffAmt":-4660.0,"saleAmt":18240.0,"srchEndDt":"2026-11-05","cmprOrdCnt":247,"srchStrtDt":"2026-11-05","cmprSaleAmt":22900.0}]} ``
2. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-10-23"} ``
   ← 실패: `` {"code":"invalid_period","class":"invalid_input","message":"same_weekday_last_4_weeks compares periods of 7 days at most; this one has 14. Use previous_period or custom.","next_tool":null} ``
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-05","cmprBaseCd":"2","srchStrtDt":"2026-11-05"} ``
3. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-05","cmprBaseCd":"2","srchStrtDt":"2026-11-05"} ``
   ← 결과: `` {"list":[{"diffRt":-0.0559,"ordCnt":201,"diffAmt":-1080.0,"saleAmt":18240.0,"srchEndDt":"2026-11-05","cmprOrdCnt":211,"srchStrtDt":"2026-11-05","cmprSaleAmt":19320.0}]} ``
- check: Numbers not in the results: 20.35, 5.59

**답변 1**
> Sales were $18,240 yesterday, down $4,660 from the first comparison and $1,080 from the second. There were 201 orders, compared with 247 and 211; the results don’t explain what caused the drop.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (22900, 20 not shown); fact "M and L sold out on the three best sellers (chore coat, rain" (2700 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8, 0, 1300, 660 not shown)
