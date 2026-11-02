# md-how-many-left — own22-heldout-raw-logs

[← 실행 묶음](README.md)

**과업**

> How many Light rain parka remain in my inventory?

- 답에 있어야 할 사실: 4 in total: S 2, M 0, L 0, XL 2 (all Stone)
- 답에 있어야 할 사실: S and XL are at their safety stock of 2, so the parka is effectively sold out for new sales planning

### 원본 파사드 · 1회차 · ✗ 실패

토큰 6,596 · 모델 호출 3회 · 도구 호출 3회

**질문 1**
> How many Light rain parka remain in my inventory?

- 라우팅: Catalog agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: getDispCornerList, getPrdDtlInfo, getPrdDtlInfoV2, getPrdGridList, getPrdGridListCnt
- 계획: `getPrdGridList` `` {"pageNo":0,"srchKwd":"Light rain parka","pageSize":20} ``; `getPrdGridListCnt` `` {"pageNo":0,"srchKwd":"Light rain parka","pageSize":20} ``
1. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"srchKwd":"Light rain parka","pageSize":20} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrdGridList` `` {"pageNo":0,"srchKwd":"Light rain parka","pageSize":20} ``; `getPrdGridListCnt` `` {"pageNo":0,"srchKwd":"Light rain parka","pageSize":20} ``
2. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"srchKwd":"Light rain parka","pageSize":20} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrdGridList` `` {"pageNo":0,"srchKwd":"Light rain parka","pageSize":20} ``; `getPrdGridListCnt` `` {"pageNo":0,"srchKwd":"Light rain parka","pageSize":20} ``
3. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"srchKwd":"Light rain parka","pageSize":20} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``

**답변 1**
> getPrdGridList failed (ERR_PARAM): Invalid paging. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "4 in total: S 2, M 0, L 0, XL 2 (all Stone)" (4, 2, 0, 0, 2 not shown); fact "S and XL are at their safety stock of 2, so the parka is eff" (2 not shown)

### 원본 파사드 · 2회차 · ✗ 실패

토큰 6,627 · 모델 호출 3회 · 도구 호출 3회

**질문 1**
> How many Light rain parka remain in my inventory?

- 라우팅: Catalog agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: getDispCornerList, getPrdDtlInfo, getPrdDtlInfoV2, getPrdGridList, getPrdGridListCnt
- 계획: `getPrdGridList` `` {"pageNo":0,"srchKwd":"Light rain parka","pageSize":20} ``; `getPrdGridListCnt` `` {"srchKwd":"Light rain parka"} ``
1. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"srchKwd":"Light rain parka","pageSize":20} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrdGridList` `` {"pageNo":0,"srchKwd":"Light rain parka","pageSize":20} ``; `getPrdGridListCnt` `` {"pageNo":0,"srchKwd":"Light rain parka","pageSize":20} ``
2. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"srchKwd":"Light rain parka","pageSize":20} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrdGridList` `` {"pageNo":0,"srchKwd":"Light rain parka","pageSize":20} ``; `getPrdGridListCnt` `` {"pageNo":0,"srchKwd":"Light rain parka","pageSize":20} ``
3. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"srchKwd":"Light rain parka","pageSize":20} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``

**답변 1**
> getPrdGridList failed (ERR_PARAM): Invalid paging. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "4 in total: S 2, M 0, L 0, XL 2 (all Stone)" (4, 2, 0, 0, 2 not shown); fact "S and XL are at their safety stock of 2, so the parka is eff" (2 not shown)
