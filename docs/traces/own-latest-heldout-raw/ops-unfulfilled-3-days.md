# ops-unfulfilled-3-days — own-latest-heldout-raw

[← 실행 묶음](README.md)

**과업**

> any orders sitting unfulfilled for more than 3 days?

- 답에 있어야 할 사실: none: 412 orders are processing and the oldest was placed Wed Nov 4 00:09

### 원본 파사드 · 1회차 · ✗ 실패

토큰 7,299 · 모델 호출 3회 · 도구 호출 4회

**질문 1**
> any orders sitting unfulfilled for more than 3 days?

- 라우팅: Orders agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: getOrdGridList, getOrdGridListCnt, getOrdDtlPopInitData, saveCustMsgSend, getClmGridList
- 계획: `getOrdGridListCnt` `` {"ordDtmTo":"2026-11-06","ordStatCd":"20","ordDtmFrom":"2026-10-31"} ``; `getOrdGridList` `` {"pageNo":0,"ordDtmTo":"2026-11-06","pageSize":50,"ordStatCd":"20","ordDtmFrom":"2026-10-31"} ``
1. 에이전트 → **`getOrdGridListCnt`** `` {"ordDtmTo":"2026-11-06","ordStatCd":"20","ordDtmFrom":"2026-10-31"} ``
   ← 결과: `` {"totCnt":412} ``
2. 에이전트 → **`getOrdGridList`** `` {"pageNo":0,"ordDtmTo":"2026-11-06","pageSize":50,"ordStatCd":"20","ordDtmFrom":"2026-10-31"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getOrdGridList` `` {"pageNo":0,"ordDtmTo":"2026-11-06","pageSize":100,"ordStatCd":"20","ordDtmFrom":"2026-10-31"} ``
3. 에이전트 → **`getOrdGridList`** `` {"pageNo":0,"ordDtmTo":"2026-11-06","pageSize":100,"ordStatCd":"20","ordDtmFrom":"2026-10-31"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getOrdGridList` `` {"pageNo":0,"ordDtmTo":"2026-11-06","pageSize":100,"ordStatCd":"20","ordDtmFrom":"2026-10-31"} ``
4. 에이전트 → **`getOrdGridList`** `` {"pageNo":0,"ordDtmTo":"2026-11-06","pageSize":100,"ordStatCd":"20","ordDtmFrom":"2026-10-31"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``

**답변 1**
> getOrdGridList failed (ERR_PARAM): Invalid paging. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "none: 412 orders are processing and the oldest was placed We" (412, 4, 0, 9 not shown)

### 원본 파사드 · 2회차 · ✗ 실패

토큰 7,298 · 모델 호출 3회 · 도구 호출 4회

**질문 1**
> any orders sitting unfulfilled for more than 3 days?

- 라우팅: Orders agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: getOrdGridList, getOrdGridListCnt, getOrdDtlPopInitData, saveCustMsgSend, getClmGridList
- 계획: `getOrdGridListCnt` `` {"ordDtmTo":"2026-11-06","ordStatCd":"20","ordDtmFrom":"2026-11-02"} ``; `getOrdGridList` `` {"pageNo":0,"ordDtmTo":"2026-11-06","pageSize":50,"ordStatCd":"20","ordDtmFrom":"2026-11-02"} ``
1. 에이전트 → **`getOrdGridListCnt`** `` {"ordDtmTo":"2026-11-06","ordStatCd":"20","ordDtmFrom":"2026-11-02"} ``
   ← 결과: `` {"totCnt":412} ``
2. 에이전트 → **`getOrdGridList`** `` {"pageNo":0,"ordDtmTo":"2026-11-06","pageSize":50,"ordStatCd":"20","ordDtmFrom":"2026-11-02"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getOrdGridList` `` {"pageNo":0,"ordDtmTo":"2026-11-06","pageSize":100,"ordStatCd":"20","ordDtmFrom":"2026-11-02"} ``
3. 에이전트 → **`getOrdGridList`** `` {"pageNo":0,"ordDtmTo":"2026-11-06","pageSize":100,"ordStatCd":"20","ordDtmFrom":"2026-11-02"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getOrdGridList` `` {"pageNo":0,"ordDtmTo":"2026-11-06","pageSize":100,"ordStatCd":"20","ordDtmFrom":"2026-11-02"} ``
4. 에이전트 → **`getOrdGridList`** `` {"pageNo":0,"ordDtmTo":"2026-11-06","pageSize":100,"ordStatCd":"20","ordDtmFrom":"2026-11-02"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``

**답변 1**
> getOrdGridList failed (ERR_PARAM): Invalid paging. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "none: 412 orders are processing and the oldest was placed We" (412, 4, 0, 9 not shown)

### 원본 파사드 · 3회차 · ✗ 실패

토큰 7,310 · 모델 호출 3회 · 도구 호출 4회

**질문 1**
> any orders sitting unfulfilled for more than 3 days?

- 라우팅: Orders agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: getOrdGridList, getOrdGridListCnt, getOrdDtlPopInitData, saveCustMsgSend, getClmGridList
- 계획: `getOrdGridListCnt` `` {"ordDtmTo":"2026-11-06","ordStatCd":"20","ordDtmFrom":"2026-11-03"} ``; `getOrdGridList` `` {"pageNo":0,"ordDtmTo":"2026-11-06","pageSize":50,"ordStatCd":"20","ordDtmFrom":"2026-11-03"} ``
1. 에이전트 → **`getOrdGridListCnt`** `` {"ordDtmTo":"2026-11-06","ordStatCd":"20","ordDtmFrom":"2026-11-03"} ``
   ← 결과: `` {"totCnt":412} ``
2. 에이전트 → **`getOrdGridList`** `` {"pageNo":0,"ordDtmTo":"2026-11-06","pageSize":50,"ordStatCd":"20","ordDtmFrom":"2026-11-03"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getOrdGridList` `` {"pageNo":0,"ordDtmTo":"2026-11-06","pageSize":100,"ordStatCd":"20","ordDtmFrom":"2026-11-03"} ``
3. 에이전트 → **`getOrdGridList`** `` {"pageNo":0,"ordDtmTo":"2026-11-06","pageSize":100,"ordStatCd":"20","ordDtmFrom":"2026-11-03"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getOrdGridList` `` {"pageNo":0,"ordDtmTo":"2026-11-06","pageSize":100,"ordStatCd":"20","ordDtmFrom":"2026-11-03"} ``
4. 에이전트 → **`getOrdGridList`** `` {"pageNo":0,"ordDtmTo":"2026-11-06","pageSize":100,"ordStatCd":"20","ordDtmFrom":"2026-11-03"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``

**답변 1**
> getOrdGridList failed (ERR_PARAM): Invalid paging. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "none: 412 orders are processing and the oldest was placed We" (412, 4, 0, 9 not shown)
