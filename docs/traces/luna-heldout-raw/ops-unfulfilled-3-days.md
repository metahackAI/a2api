# ops-unfulfilled-3-days — luna-heldout-raw

[← 실행 묶음](README.md)

**과업**

> any orders sitting unfulfilled for more than 3 days?

- 답에 있어야 할 사실: none: 412 orders are processing and the oldest was placed Wed Nov 4 00:09

### GPT-6-Luna · 원본 파사드 · 1회차 · ✗ 실패

토큰 13,307 · 모델 호출 2회 · 도구 호출 1회

**질문 1**
> any orders sitting unfulfilled for more than 3 days?

- 라우팅: Orders agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: getOrdGridList, getOrdGridListCnt, getOrdDtlPopInitData, saveCustMsgSend, getClmGridList
- 계획: `getOrdGridList` `` {"ordStatCd":"10"} ``
1. 에이전트 → **`getOrdGridList`** `` {"ordStatCd":"10"} ``
   ← 결과: `` {"list":[{"mbrNo":"cus_owen","ordNo":"ord_29002","ordAmt":89.0,"ordDtm":"2026-11-06T09:05:00-05:00","ordStatCd":"10"},{"mbrNo":"cus_priya","ordNo":"ord_29001","ordAmt":128.0,"ordDtm":"2026-11-05T16:20:00-05:00","ordStatCd":"10"}],"pageNo":1,"pageSize":20} ``

**답변 1**
> There are no orders shown as unfulfilled for more than 3 days. The two listed orders were placed on Nov 5 and Nov 6, so neither is more than 3 days old.

화면 블록: product_table(2 of 2)

**채점**: ✗ 실패 — 빠진 것: fact "none: 412 orders are processing and the oldest was placed We" (412, 4 not shown)

### GPT-6-Luna · 원본 파사드 · 2회차 · ✗ 실패

토큰 23,754 · 모델 호출 3회 · 도구 호출 3회

**질문 1**
> any orders sitting unfulfilled for more than 3 days?

- 라우팅: Orders agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: getOrdGridList, getOrdGridListCnt, getOrdDtlPopInitData, saveCustMsgSend, getClmGridList
- 계획: `getOrdGridList` `` {"pageNo":0,"ordDtmTo":"2026-11-03 11:00","pageSize":100,"ordStatCd":"10"} ``
1. 에이전트 → **`getOrdGridList`** `` {"pageNo":0,"ordDtmTo":"2026-11-03 11:00","pageSize":100,"ordStatCd":"10"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getOrdGridList` `` {"pageNo":0,"ordDtmTo":"2026-11-03 11:00","pageSize":100} ``
2. 에이전트 → **`getOrdGridList`** `` {"pageNo":0,"ordDtmTo":"2026-11-03 11:00","pageSize":100} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getOrdGridList` `` {"pageNo":0,"pageSize":50} ``
3. 에이전트 → **`getOrdGridList`** `` {"pageNo":0,"pageSize":50} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``

**답변 1**
> getOrdGridList failed (ERR_PARAM): Invalid paging. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "none: 412 orders are processing and the oldest was placed We" (412, 4, 0, 9 not shown)

### GPT-6-Luna · 원본 파사드 · 3회차 · ✗ 실패

토큰 22,887 · 모델 호출 3회 · 도구 호출 3회

**질문 1**
> any orders sitting unfulfilled for more than 3 days?

- 라우팅: Orders agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: getOrdGridList, getOrdGridListCnt, getOrdDtlPopInitData, saveCustMsgSend, getClmGridList
- 계획: `getOrdGridList` `` {"pageNo":0,"ordDtmTo":"2026-11-03 11:00","pageSize":100,"ordStatCd":"20"} ``
1. 에이전트 → **`getOrdGridList`** `` {"pageNo":0,"ordDtmTo":"2026-11-03 11:00","pageSize":100,"ordStatCd":"20"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getOrdGridList` `` {"pageNo":0,"pageSize":50} ``
2. 에이전트 → **`getOrdGridList`** `` {"pageNo":0,"pageSize":50} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getOrdGridList` `` {"pageNo":0,"pageSize":50,"ordStatCd":"20"} ``
3. 에이전트 → **`getOrdGridList`** `` {"pageNo":0,"pageSize":50,"ordStatCd":"20"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``

**답변 1**
> getOrdGridList failed (ERR_PARAM): Invalid paging. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "none: 412 orders are processing and the oldest was placed We" (412, 4, 0, 9 not shown)
