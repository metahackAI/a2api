# mgr-how-is-business — luna-heldout-raw

[← 실행 묶음](README.md)

**과업**

> How is my business doing?

- 답에 있어야 할 사실: yesterday (Thu Nov 5) was $18,240, 20% under the Thursday average; the agent leads with that and its causes

### GPT-6-Luna · 원본 파사드 · 1회차 · ✗ 실패

토큰 18,241 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> How is my business doing?

- 라우팅: Insights agent (chosen by the model)
- 도구 검색 후보: 4 candidates: getSaleAnlsGridList, getMbrGrdList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-06","cmprBaseCd":"1","srchStrtDt":"2026-11-01"} ``
1. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-06","cmprBaseCd":"1","srchStrtDt":"2026-11-01"} ``
   ← 결과: `` {"list":[{"diffRt":-0.2179,"ordCnt":1088,"diffAmt":-27736.5,"saleAmt":99530.0,"srchEndDt":"2026-11-06","cmprOrdCnt":1365.5,"srchStrtDt":"2026-11-01","cmprSaleAmt":127266.5}]} ``

**답변 1**
> Your business is down month to date: sales are $99,530 across 1,088 orders, compared with $127,266.50 and 1,365.5 orders for the comparison period. The results show the totals, but not what caused the decline.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "yesterday (Thu Nov 5) was $18,240, 20% under the Thursday av" (5, 18240, 20 not shown)

### GPT-6-Luna · 원본 파사드 · 2회차 · ✗ 실패

토큰 27,978 · 모델 호출 4회 · 도구 호출 3회

**질문 1**
> How is my business doing?

- 라우팅: Insights agent (chosen by the model)
- 도구 검색 후보: 4 candidates: getSaleAnlsGridList, getMbrGrdList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-06","cmprBaseCd":"1","srchStrtDt":"2026-10-01"} ``
1. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-06","cmprBaseCd":"1","srchStrtDt":"2026-10-01"} ``
   ← 실패: `` {"code":"invalid_period","class":"invalid_input","message":"same_weekday_last_4_weeks compares periods of 7 days at most; this one has 37. Use previous_period or custom.","next_tool":null} ``
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-06","cmprBaseCd":"1","srchStrtDt":"2026-10-01"} ``
2. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-06","cmprBaseCd":"1","srchStrtDt":"2026-10-01"} ``
   ← 실패: `` {"code":"invalid_period","class":"invalid_input","message":"same_weekday_last_4_weeks compares periods of 7 days at most; this one has 37. Use previous_period or custom.","next_tool":null} ``
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-06","cmprBaseCd":"1","srchStrtDt":"2026-10-01"} ``
3. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-06","cmprBaseCd":"1","srchStrtDt":"2026-10-01"} ``
   ← 실패: `` {"code":"invalid_period","class":"invalid_input","message":"same_weekday_last_4_weeks compares periods of 7 days at most; this one has 37. Use previous_period or custom.","next_tool":null} ``

**답변 1**
> getSaleAnlsGridList failed (invalid_period): same_weekday_last_4_weeks compares periods of 7 days at most; this one has 37. Use previous_period or custom. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "yesterday (Thu Nov 5) was $18,240, 20% under the Thursday av" (5, 18240, 20 not shown)

### GPT-6-Luna · 원본 파사드 · 3회차 · ✗ 실패

토큰 23,772 · 모델 호출 4회 · 도구 호출 1회

**질문 1**
> How is my business doing?

- 라우팅: Insights agent (chosen by the model)
- 도구 검색 후보: 4 candidates: getSaleAnlsGridList, getMbrGrdList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-06","cmprBaseCd":"1","srchStrtDt":"2026-11-01"} ``
1. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-06","cmprBaseCd":"1","srchStrtDt":"2026-11-01"} ``
   ← 결과: `` {"list":[{"diffRt":-0.2179,"ordCnt":1088,"diffAmt":-27736.5,"saleAmt":99530.0,"srchEndDt":"2026-11-06","cmprOrdCnt":1365.5,"srchStrtDt":"2026-11-01","cmprSaleAmt":127266.5}]} ``
- check: Numbers not in the results: 21.79

**답변 1**
> Month to date through Nov 6, sales are $99,530 across 1,088 orders, down $27,736.50 from the comparison period.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "yesterday (Thu Nov 5) was $18,240, 20% under the Thursday av" (5, 18240, 20 not shown)
