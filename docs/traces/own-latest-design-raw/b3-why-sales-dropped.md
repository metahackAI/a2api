# b3-why-sales-dropped — own-latest-design-raw

[← 실행 묶음](README.md)

**과업**

> Why did sales drop yesterday?

- 답에 있어야 할 사실: Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$4,660, -20%); 201 orders against 247
- 답에 있어야 할 사실: M and L sold out on the three best sellers (chore coat, rain parka, denim jacket): about -$2,700
- 답에 있어야 할 사실: the weekly email did not go out (Thu 08:00 list import failed): about -$1,300; -$660 is not explained

### 원본 파사드 · 1회차 · ✗ 실패

토큰 4,949 · 모델 호출 3회 · 도구 호출 2회

**질문 1**
> Why did sales drop yesterday?

- 라우팅: Insights agent (the request names this agent's work)
- 도구 검색 후보: 4 candidates: getSaleAnlsGridList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt, getMbrGrdList
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-05","cmprBaseCd":"2","srchStrtDt":"2026-11-05"} ``; `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-10-23"} ``
1. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-05","cmprBaseCd":"2","srchStrtDt":"2026-11-05"} ``
   ← 결과: `` {"list":[{"diffRt":-0.0559,"ordCnt":201,"diffAmt":-1080.0,"saleAmt":18240.0,"srchEndDt":"2026-11-05","cmprOrdCnt":211,"srchStrtDt":"2026-11-05","cmprSaleAmt":19320.0}]} ``
2. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-10-23"} ``
   ← 실패: `` {"code":"invalid_period","class":"invalid_input","message":"same_weekday_last_4_weeks compares periods of 7 days at most; this one has 14. Use previous_period or custom.","next_tool":null} ``
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-05","cmprBaseCd":"2","srchStrtDt":"2026-11-05"} ``

**답변 1**
> The store operator asked why sales dropped yesterday. The results show sales fell from $19,320 to $18,240, a $1,080 drop, with orders down from 211 to 201. The blocks shown are a product_table, but no explain_sales_change or get_sales_trend data was returned to identify causes. There is nothing to do yet because the results do not include the breakdown needed to explain the drop.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (22900, 4660, 20, 247 not shown); fact "M and L sold out on the three best sellers (chore coat, rain" (2700 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8, 0, 1300, 660 not shown)

### 원본 파사드 · 2회차 · ✗ 실패

토큰 6,496 · 모델 호출 4회 · 도구 호출 2회

**질문 1**
> Why did sales drop yesterday?

- 라우팅: Insights agent (the request names this agent's work)
- 도구 검색 후보: 4 candidates: getSaleAnlsGridList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt, getMbrGrdList
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-05","cmprBaseCd":"2","srchStrtDt":"2026-11-05"} ``; `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-10-23"} ``
1. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-05","cmprBaseCd":"2","srchStrtDt":"2026-11-05"} ``
   ← 결과: `` {"list":[{"diffRt":-0.0559,"ordCnt":201,"diffAmt":-1080.0,"saleAmt":18240.0,"srchEndDt":"2026-11-05","cmprOrdCnt":211,"srchStrtDt":"2026-11-05","cmprSaleAmt":19320.0}]} ``
2. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-10-23"} ``
   ← 실패: `` {"code":"invalid_period","class":"invalid_input","message":"same_weekday_last_4_weeks compares periods of 7 days at most; this one has 14. Use previous_period or custom.","next_tool":null} ``
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-05","cmprBaseCd":"2","srchStrtDt":"2026-11-05"} ``
- check: The reply was cut at the length limit

**답변 1**
> The blocks on screen show yesterday’s sales at $18,240 with 201 orders, down from $19,320 with 211 orders, a $1,080 drop. The change set is null and the reads only return the grid list with sale amount and order count. There is no explainer data in the results to show why the drop happened.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (22900, 4660, 20, 247 not shown); fact "M and L sold out on the three best sellers (chore coat, rain" (2700 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8, 0, 1300, 660 not shown)

### 원본 파사드 · 3회차 · ✗ 실패

토큰 7,505 · 모델 호출 5회 · 도구 호출 2회

**질문 1**
> Why did sales drop yesterday?

- 라우팅: Insights agent (the request names this agent's work)
- 도구 검색 후보: 4 candidates: getSaleAnlsGridList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt, getMbrGrdList
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-05","cmprBaseCd":"2","srchStrtDt":"2026-11-05"} ``; `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-10-23"} ``
1. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-05","cmprBaseCd":"2","srchStrtDt":"2026-11-05"} ``
   ← 결과: `` {"list":[{"diffRt":-0.0559,"ordCnt":201,"diffAmt":-1080.0,"saleAmt":18240.0,"srchEndDt":"2026-11-05","cmprOrdCnt":211,"srchStrtDt":"2026-11-05","cmprSaleAmt":19320.0}]} ``
2. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-10-23"} ``
   ← 실패: `` {"code":"invalid_period","class":"invalid_input","message":"same_weekday_last_4_weeks compares periods of 7 days at most; this one has 14. Use previous_period or custom.","next_tool":null} ``
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-05","cmprBaseCd":"2","srchStrtDt":"2026-11-05"} ``
- check: The reply was cut at the length limit
- check: Numbers not in the results: 10, 4.7

**답변 1**
> The blocks on screen show yesterday’s sales at $18,240 from 201 orders, down $1,080 from the comparison day. The change is a 5.6% drop in revenue. The results do not show the causes of the drop.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (22900, 4660, 20, 247 not shown); fact "M and L sold out on the three best sellers (chore coat, rain" (2700 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8, 0, 1300, 660 not shown)
