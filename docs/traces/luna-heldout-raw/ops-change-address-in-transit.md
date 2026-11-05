# ops-change-address-in-transit — luna-heldout-raw

[← 실행 묶음](README.md)

**과업**

> customer on 27184 moved, can you change the shipping address?

- 답에 있어야 할 사실: no: the order is already with UPS (in transit since Nov 2); an address can only change before it ships

### GPT-6-Luna · 원본 파사드 · 1회차 · ✗ 실패

토큰 13,389 · 모델 호출 2회 · 도구 호출 1회

**질문 1**
> customer on 27184 moved, can you change the shipping address?

- 라우팅: Orders agent (the request names this agent's work)
- 도구 검색 후보: 6 candidates: saveCustMsgSend, getOrdGridList, getPrmtTgtMbrList, getOrdGridListCnt, getPrmtTgtMbrListCnt, getMbrGrdList
- 계획: `getOrdGridList` `` {"srchKwd":"27184"} ``
1. 에이전트 → **`getOrdGridList`** `` {"srchKwd":"27184"} ``
   ← 결과: `` {"list":[{"mbrNo":"cus_m005474","ordNo":"ord_27184","ordAmt":289.0,"ordDtm":"2026-11-01T00:18:00-04:00","ordStatCd":"30"}],"pageNo":1,"pageSize":20} ``

**답변 1**
> I found order #27184, but its customer, parcel, and payment details haven’t been checked yet. Nothing has been changed; I need to review the order before I can check whether its shipping address can be updated.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "no: the order is already with UPS (in transit since Nov 2); " (2 not shown)

### GPT-6-Luna · 원본 파사드 · 2회차 · ✗ 실패

토큰 13,383 · 모델 호출 2회 · 도구 호출 1회

**질문 1**
> customer on 27184 moved, can you change the shipping address?

- 라우팅: Orders agent (the request names this agent's work)
- 도구 검색 후보: 6 candidates: saveCustMsgSend, getOrdGridList, getPrmtTgtMbrList, getOrdGridListCnt, getPrmtTgtMbrListCnt, getMbrGrdList
- 계획: `getOrdGridList` `` {"srchKwd":"27184"} ``
1. 에이전트 → **`getOrdGridList`** `` {"srchKwd":"27184"} ``
   ← 결과: `` {"list":[{"mbrNo":"cus_m005474","ordNo":"ord_27184","ordAmt":289.0,"ordDtm":"2026-11-01T00:18:00-04:00","ordStatCd":"30"}],"pageNo":1,"pageSize":20} ``

**답변 1**
> I found order #27184, but the order details weren’t retrieved, so I can’t confirm its shipping address or change it yet. Please open the order details first.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "no: the order is already with UPS (in transit since Nov 2); " (2 not shown)

### GPT-6-Luna · 원본 파사드 · 3회차 · ✗ 실패

토큰 13,379 · 모델 호출 2회 · 도구 호출 1회

**질문 1**
> customer on 27184 moved, can you change the shipping address?

- 라우팅: Orders agent (the request names this agent's work)
- 도구 검색 후보: 6 candidates: saveCustMsgSend, getOrdGridList, getPrmtTgtMbrList, getOrdGridListCnt, getPrmtTgtMbrListCnt, getMbrGrdList
- 계획: `getOrdGridList` `` {"srchKwd":"27184"} ``
1. 에이전트 → **`getOrdGridList`** `` {"srchKwd":"27184"} ``
   ← 결과: `` {"list":[{"mbrNo":"cus_m005474","ordNo":"ord_27184","ordAmt":289.0,"ordDtm":"2026-11-01T00:18:00-04:00","ordStatCd":"30"}],"pageNo":1,"pageSize":20} ``

**답변 1**
> I found order #27184, but its shipping address hasn’t been changed. I still need the customer’s new shipping address before it can be updated.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "no: the order is already with UPS (in transit since Nov 2); " (2 not shown)
