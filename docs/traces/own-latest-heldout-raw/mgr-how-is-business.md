# mgr-how-is-business — own-latest-heldout-raw

[← 실행 묶음](README.md)

**과업**

> How is my business doing?

- 답에 있어야 할 사실: yesterday (Thu Nov 5) was $18,240, 20% under the Thursday average; the agent leads with that and its causes

### 원본 파사드 · 1회차 · ✗ 실패

토큰 6,834 · 모델 호출 6회 · 도구 호출 2회

**질문 1**
> How is my business doing?

- 라우팅: Insights agent (chosen by the model)
- 도구 검색 후보: 4 candidates: getSaleAnlsGridList, getMbrGrdList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-06","cmprBaseCd":"1","srchStrtDt":"2026-10-06"} ``
1. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-06","cmprBaseCd":"1","srchStrtDt":"2026-10-06"} ``
   ← 실패: `` {"code":"invalid_period","class":"invalid_input","message":"same_weekday_last_4_weeks compares periods of 7 days at most; this one has 32. Use previous_period or custom.","next_tool":null} ``
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-06","cmprBaseCd":"2","srchStrtDt":"2026-11-06"} ``
2. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-06","cmprBaseCd":"2","srchStrtDt":"2026-11-06"} ``
   ← 결과: `` {"list":[{"diffRt":-1,"ordCnt":0,"diffAmt":-18240.0,"saleAmt":0.0,"srchEndDt":"2026-11-06","cmprOrdCnt":201,"srchStrtDt":"2026-11-06","cmprSaleAmt":18240.0}]} ``

**답변 1**
> The business had no sales on Fri Nov 6, 2026, with 0 orders and $0 revenue. That is a $18,240 drop from the same day last period, which had 201 orders. The data does not show why sales fell to zero.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "yesterday (Thu Nov 5) was $18,240, 20% under the Thursday av" (5, 20 not shown)

### 원본 파사드 · 2회차 · ✗ 실패

토큰 6,812 · 모델 호출 5회 · 도구 호출 2회

**질문 1**
> How is my business doing?

- 라우팅: Insights agent (chosen by the model)
- 도구 검색 후보: 4 candidates: getSaleAnlsGridList, getMbrGrdList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-06","cmprBaseCd":"1","srchStrtDt":"2026-10-01"} ``
1. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-06","cmprBaseCd":"1","srchStrtDt":"2026-10-01"} ``
   ← 실패: `` {"code":"invalid_period","class":"invalid_input","message":"same_weekday_last_4_weeks compares periods of 7 days at most; this one has 37. Use previous_period or custom.","next_tool":null} ``
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-06","cmprBaseCd":"1","srchStrtDt":"2026-11-06"} ``
2. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-06","cmprBaseCd":"1","srchStrtDt":"2026-11-06"} ``
   ← 결과: `` {"list":[{"diffRt":-1,"ordCnt":0,"diffAmt":-21879.75,"saleAmt":0.0,"srchEndDt":"2026-11-06","cmprOrdCnt":233.75,"srchStrtDt":"2026-11-06","cmprSaleAmt":21879.75}]} ``

**답변 1**
> The business had no sales on Fri Nov 6, 2026. That is $0.00 from 0 orders versus $21,879.75 from 233.75 orders on the same weekday in the prior four weeks, a drop of $21,879.75. The data shown does not explain why sales fell to zero.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "yesterday (Thu Nov 5) was $18,240, 20% under the Thursday av" (5, 18240, 20 not shown)

### 원본 파사드 · 3회차 · ✗ 실패

토큰 7,819 · 모델 호출 6회 · 도구 호출 2회

**질문 1**
> How is my business doing?

- 라우팅: Insights agent (chosen by the model)
- 도구 검색 후보: 4 candidates: getSaleAnlsGridList, getMbrGrdList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-06","cmprBaseCd":"1","srchStrtDt":"2026-10-06"} ``
1. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-06","cmprBaseCd":"1","srchStrtDt":"2026-10-06"} ``
   ← 실패: `` {"code":"invalid_period","class":"invalid_input","message":"same_weekday_last_4_weeks compares periods of 7 days at most; this one has 32. Use previous_period or custom.","next_tool":null} ``
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-06","cmprBaseCd":"1","srchStrtDt":"2026-11-06"} ``
2. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-06","cmprBaseCd":"1","srchStrtDt":"2026-11-06"} ``
   ← 결과: `` {"list":[{"diffRt":-1,"ordCnt":0,"diffAmt":-21879.75,"saleAmt":0.0,"srchEndDt":"2026-11-06","cmprOrdCnt":233.75,"srchStrtDt":"2026-11-06","cmprSaleAmt":21879.75}]} ``
- check: Numbers not in the results: 100

**답변 1**
> The business had no sales on Fri Nov 6, 2026, with 0 orders and $0 revenue. That is a $21,879.75 drop from the same day in the prior four-week average, which is a -1 change. The data does not show why the drop occurred.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "yesterday (Thu Nov 5) was $18,240, 20% under the Thursday av" (5, 18240, 20 not shown)
