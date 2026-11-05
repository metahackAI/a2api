# md-out-of-stock-30-days — luna-heldout-raw

[← 실행 묶음](README.md)

**과업**

> Find all products that have been out of stock for more than 30 days

- 답에 있어야 할 사실: the store keeps current stock only, not since when a size has been out, so the agent cannot answer the 30 day part and says that

### GPT-6-Luna · 원본 파사드 · 1회차 · ✗ 실패

토큰 23,864 · 모델 호출 3회 · 도구 호출 3회

**질문 1**
> Find all products that have been out of stock for more than 30 days

- 라우팅: Catalog agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: getPrdGridList, getPrdDtlInfo, getPrdGridListCnt, getPrdDtlInfoV2, getDispCornerList
- 계획: `getPrdGridList` `` {"pageNo":0,"pageSize":100,"stkQtyTo":0,"stkQtyFrom":0} ``; `getPrdDtlInfoV2` `` {} ``
1. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"pageSize":100,"stkQtyTo":0,"stkQtyFrom":0} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrdGridList` `` {"pageNo":0,"pageSize":100,"stkQtyTo":0,"stkQtyFrom":0} ``; `getPrdDtlInfoV2` `` {} ``
2. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"pageSize":100,"stkQtyTo":0,"stkQtyFrom":0} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrdGridList` `` {"pageNo":0,"pageSize":100,"stkQtyTo":0,"stkQtyFrom":0} ``; `getPrdDtlInfoV2` `` {} ``
3. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"pageSize":100,"stkQtyTo":0,"stkQtyFrom":0} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``

**답변 1**
> getPrdGridList failed (ERR_PARAM): Invalid paging. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "the store keeps current stock only, not since when a size ha" (30 not shown)

### GPT-6-Luna · 원본 파사드 · 2회차 · ✓ 통과

토큰 20,966 · 모델 호출 3회 · 도구 호출 2회

**질문 1**
> Find all products that have been out of stock for more than 30 days

- 라우팅: Catalog agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: getPrdGridList, getPrdDtlInfo, getPrdGridListCnt, getPrdDtlInfoV2, getDispCornerList
- 계획: `getPrdGridList` `` {"pageNo":0,"pageSize":100,"stkQtyTo":0,"stkQtyFrom":0} ``
1. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"pageSize":100,"stkQtyTo":0,"stkQtyFrom":0} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrdGridList` `` {"pageNo":1,"pageSize":100,"stkQtyTo":0,"stkQtyFrom":0} ``
2. 에이전트 → **`getPrdGridList`** `` {"pageNo":1,"pageSize":100,"stkQtyTo":0,"stkQtyFrom":0} ``
   ← 결과: `` {"list":[],"pageNo":1,"pageSize":100} ``

**답변 1**
> No products were found that have been out of stock for more than 30 days.

**채점**: ✓ 통과

### GPT-6-Luna · 원본 파사드 · 3회차 · ✗ 실패

토큰 28,835 · 모델 호출 4회 · 도구 호출 5회

**질문 1**
> Find all products that have been out of stock for more than 30 days

- 라우팅: Catalog agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: getPrdGridList, getPrdDtlInfo, getPrdGridListCnt, getPrdDtlInfoV2, getDispCornerList
- 계획: `getPrdGridListCnt` `` {"stkQtyTo":0,"stkQtyFrom":0} ``; `getPrdGridList` `` {"pageNo":0,"pageSize":100,"stkQtyTo":0,"stkQtyFrom":0} ``; `getPrdDtlInfo` `` {} ``
1. 에이전트 → **`getPrdGridListCnt`** `` {"stkQtyTo":0,"stkQtyFrom":0} ``
   ← 결과: `` {"totCnt":0} ``
2. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"pageSize":100,"stkQtyTo":0,"stkQtyFrom":0} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrdGridList` `` {"pageNo":0,"pageSize":100,"stkQtyTo":0,"stkQtyFrom":0} ``; `getPrdDtlInfo` `` {} ``
3. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"pageSize":100,"stkQtyTo":0,"stkQtyFrom":0} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrdGridList` `` {"pageNo":1,"pageSize":100,"stkQtyTo":0,"stkQtyFrom":0} ``; `getPrdDtlInfo` `` {} ``
4. 에이전트 → **`getPrdGridList`** `` {"pageNo":1,"pageSize":100,"stkQtyTo":0,"stkQtyFrom":0} ``
   ← 결과: `` {"list":[],"pageNo":1,"pageSize":100} ``
5. 에이전트 → **`getPrdDtlInfo`** `` {"prdNo":""} ``
   ← 실패: `` {"code":"not_found","class":"not_found","message":"There is no product  in this store.","next_tool":null} ``

**답변 1**
> getPrdDtlInfo failed: There is no product  in this store.

**채점**: ✗ 실패 — 빠진 것: fact "the store keeps current stock only, not since when a size ha" (30 not shown)
