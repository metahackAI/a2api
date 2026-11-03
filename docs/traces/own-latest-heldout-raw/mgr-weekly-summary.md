# mgr-weekly-summary — own-latest-heldout-raw

[← 실행 묶음](README.md)

**과업**

> Give me a weekly performance summary

- 답에 있어야 할 사실: the window is stated (Sat Oct 31 – Fri Nov 6 so far, or the last 7 full days) with the week before for comparison

### 원본 파사드 · 1회차 · ✗ 실패

토큰 4,268 · 모델 호출 4회 · 도구 호출 2회

**질문 1**
> Give me a weekly performance summary

- 라우팅: Insights agent (chosen by the model)
- 도구 검색 후보: 4 candidates: getSaleAnlsGridList, getMbrGrdList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-10-30"} ``; `getMbrGrdList` `` {"prgmNo":"1"} ``
1. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-10-30"} ``
   ← 결과: `` {"list":[{"diffRt":0,"ordCnt":1621,"diffAmt":-0.5,"saleAmt":148870.0,"srchEndDt":"2026-11-05","cmprOrdCnt":1599.75,"srchStrtDt":"2026-10-30","cmprSaleAmt":148870.5}]} ``
2. 에이전트 → **`getMbrGrdList`** `` {"prgmNo":"1"} ``
   ← 실패: `` {"code":"program_not_found","class":"not_found","message":"There is no program 1.","next_tool":null} ``
- check: Numbers not in the results: 21

**답변 1**
> The weekly performance summary for Oct 30 to Nov 5 shows sales of $148,870.00 across 1,621 orders. Compared with the prior week, sales are $148,870.50 and orders are 1,599.75, with a difference of -$0.50 and a difference rate of 0. The member grid could not be loaded because program 1 does not exist.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "the window is stated (Sat Oct 31 – Fri Nov 6 so far, or the " (31, 6, 7 not shown)

### 원본 파사드 · 2회차 · ✗ 실패

토큰 6,177 · 모델 호출 5회 · 도구 호출 1회

**질문 1**
> Give me a weekly performance summary

- 라우팅: Insights agent (chosen by the model)
- 도구 검색 후보: 4 candidates: getSaleAnlsGridList, getMbrGrdList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-10-30"} ``
1. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-10-30"} ``
   ← 결과: `` {"list":[{"diffRt":0,"ordCnt":1621,"diffAmt":-0.5,"saleAmt":148870.0,"srchEndDt":"2026-11-05","cmprOrdCnt":1599.75,"srchStrtDt":"2026-10-30","cmprSaleAmt":148870.5}]} ``
- check: Numbers not in the results: 21.25

**답변 1**
> The weekly performance summary for Oct 30 to Nov 5 shows sales of $148,870.00 across 1,621 orders. Compared with the prior week, sales are essentially flat at -$0.50 and orders are 1,599.75. The data does not show what drove the small change.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "the window is stated (Sat Oct 31 – Fri Nov 6 so far, or the " (31, 6, 7 not shown)

### 원본 파사드 · 3회차 · ✗ 실패

토큰 6,138 · 모델 호출 5회 · 도구 호출 1회

**질문 1**
> Give me a weekly performance summary

- 라우팅: Insights agent (chosen by the model)
- 도구 검색 후보: 4 candidates: getSaleAnlsGridList, getMbrGrdList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `getSaleAnlsGridList` `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-10-30"} ``
1. 에이전트 → **`getSaleAnlsGridList`** `` {"srchEndDt":"2026-11-05","cmprBaseCd":"1","srchStrtDt":"2026-10-30"} ``
   ← 결과: `` {"list":[{"diffRt":0,"ordCnt":1621,"diffAmt":-0.5,"saleAmt":148870.0,"srchEndDt":"2026-11-05","cmprOrdCnt":1599.75,"srchStrtDt":"2026-10-30","cmprSaleAmt":148870.5}]} ``
- check: Numbers not in the results: 21.25

**답변 1**
> The weekly performance summary for Oct 30 to Nov 5 shows sales of $148,870.00 across 1,621 orders. Compared with the prior week, sales are $148,870.50 and orders are 1,599.75, with a difference of -$0.50 and a difference rate of 0. The data does not show what drove the change.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "the window is stated (Sat Oct 31 – Fri Nov 6 so far, or the " (31, 6, 7 not shown)
