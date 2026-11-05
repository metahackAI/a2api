# mgr-weekly-summary — luna-heldout-raw

[← 실행 묶음](README.md)

**과업**

> Give me a weekly performance summary

- 답에 있어야 할 사실: the window is stated (Sat Oct 31 – Fri Nov 6 so far, or the last 7 full days) with the week before for comparison

### GPT-6-Luna · 원본 파사드 · 1회차 · ✗ 실패

토큰 23,633 · 모델 호출 4회 · 도구 호출 1회

**질문 1**
> Give me a weekly performance summary

- 라우팅: Insights agent (chosen by the model)
- 도구 검색 후보: 4 candidates: getSaleAnlsGridList, getMbrGrdList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-10-30"} ``
1. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-10-30"} ``
   ← 결과: `` {"list":[{"diffRt":0,"ordCnt":1621,"diffAmt":-0.5,"saleAmt":148870.0,"srchEndDt":"2026-11-05","cmprOrdCnt":1599.75,"srchStrtDt":"2026-10-30","cmprSaleAmt":148870.5}]} ``
- check: Numbers not in the results: 21

**답변 1**
> Sales for Oct 30–Nov 5 were $148,870 across 1,621 orders, essentially flat compared with $148,870.50 in sales and 1,599.75 orders in the preceding seven days.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "the window is stated (Sat Oct 31 – Fri Nov 6 so far, or the " (31, 6, 7 not shown)

### GPT-6-Luna · 원본 파사드 · 2회차 · ✗ 실패

토큰 24,259 · 모델 호출 4회 · 도구 호출 1회

**질문 1**
> Give me a weekly performance summary

- 라우팅: Insights agent (chosen by the model)
- 도구 검색 후보: 4 candidates: getSaleAnlsGridList, getMbrGrdList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-01","cmprBaseCd":"1","srchStrtDt":"2026-10-26"} ``
1. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-01","cmprBaseCd":"1","srchStrtDt":"2026-10-26"} ``
   ← 결과: `` {"list":[{"diffRt":0.1348,"ordCnt":1666,"diffAmt":18179.75,"saleAmt":153030.0,"srchEndDt":"2026-11-01","cmprOrdCnt":1445,"srchStrtDt":"2026-10-26","cmprSaleAmt":134850.25}]} ``
- check: Numbers not in the results: 13.48, 221

**답변 1**
> For Oct 26–Nov 1, sales were $153,030.00 across 1,666 orders, compared with $134,850.25 and 1,445 orders in the comparison period. Sales were up $18,179.75.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "the window is stated (Sat Oct 31 – Fri Nov 6 so far, or the " (31, 6, 7 not shown)

### GPT-6-Luna · 원본 파사드 · 3회차 · ✗ 실패

토큰 23,775 · 모델 호출 4회 · 도구 호출 1회

**질문 1**
> Give me a weekly performance summary

- 라우팅: Insights agent (chosen by the model)
- 도구 검색 후보: 4 candidates: getSaleAnlsGridList, getMbrGrdList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-06","cmprBaseCd":"1","srchStrtDt":"2026-11-02"} ``
1. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-06","cmprBaseCd":"1","srchStrtDt":"2026-11-02"} ``
   ← 결과: `` {"list":[{"diffRt":-0.2947,"ordCnt":818,"diffAmt":-31186.25,"saleAmt":74650.0,"srchEndDt":"2026-11-06","cmprOrdCnt":1134.75,"srchStrtDt":"2026-11-02","cmprSaleAmt":105836.25}]} ``
- check: Numbers not in the results: 29.47

**답변 1**
> This week to date, Nov 2–6, sales were $74,650 across 818 orders, down $31,186.25 compared with the comparison period. The results show the decline but don’t explain what caused it.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "the window is stated (Sat Oct 31 – Fri Nov 6 so far, or the " (31, 7 not shown)
