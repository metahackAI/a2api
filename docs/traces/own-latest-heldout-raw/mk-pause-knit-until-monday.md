# mk-pause-knit-until-monday — own-latest-heldout-raw

[← 실행 묶음](README.md)

**과업**

> pause the knit sale until monday, we're out of the good sizes

- 답에 있어야 할 사실: Autumn knitwear 15% (promo_autumn_knit, running until Nov 15) is paused
- 답에 있어야 할 사실: pausing has no end time: the agent says someone has to resume it on Mon Nov 9

### 원본 파사드 · 1회차 · ✗ 실패

토큰 9,443 · 모델 호출 4회 · 도구 호출 3회

**질문 1**
> pause the knit sale until monday, we're out of the good sizes

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 7 candidates: getPrmtGridList, getPrmtGridListCnt, savePrmtList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt, getPrdGridList, getPrdGridListCnt
- 계획: `getPrmtGridList` `` {"pageNo":0,"prmtNm":"knit","pageSize":20} ``; `savePrmtList` `` {"rows":[{"endDtm":"2026-11-09 23:59:59","prmtNo":"","rowStat":"U","strtDtm":"","prmtStatCd":"30"}]} ``
1. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"prmtNm":"knit","pageSize":20} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrmtGridList` `` {"pageNo":0,"prmtNm":"knit sale","pageSize":10} ``; `savePrmtList` `` {"rows":[]} ``
2. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"prmtNm":"knit sale","pageSize":10} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrmtGridList` `` {"pageNo":0,"prmtNm":"knit sale","pageSize":10} ``; `savePrmtList` `` {"rows":[]} ``
3. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"prmtNm":"knit sale","pageSize":10} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``

**답변 1**
> getPrmtGridList failed (ERR_PARAM): Invalid paging. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "Autumn knitwear 15% (promo_autumn_knit, running until Nov 15" (15, 15 not shown); fact "pausing has no end time: the agent says someone has to resum" (9 not shown)

### 원본 파사드 · 2회차 · ✗ 실패

토큰 9,437 · 모델 호출 4회 · 도구 호출 3회

**질문 1**
> pause the knit sale until monday, we're out of the good sizes

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 7 candidates: getPrmtGridList, getPrmtGridListCnt, savePrmtList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt, getPrdGridList, getPrdGridListCnt
- 계획: `getPrmtGridList` `` {"pageNo":0,"prmtNm":"knit","pageSize":20} ``; `savePrmtList` `` {"rows":[{"endDtm":"2026-11-09 23:59:59","prmtNo":"","rowStat":"U","prmtStatCd":"30"}]} ``
1. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"prmtNm":"knit","pageSize":20} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrmtGridList` `` {"pageNo":0,"prmtNm":"knit sale","pageSize":10} ``; `savePrmtList` `` {"rows":[]} ``
2. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"prmtNm":"knit sale","pageSize":10} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrmtGridList` `` {"pageNo":0,"prmtNm":"knit sale","pageSize":10} ``; `savePrmtList` `` {"rows":[]} ``
3. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"prmtNm":"knit sale","pageSize":10} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``

**답변 1**
> getPrmtGridList failed (ERR_PARAM): Invalid paging. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "Autumn knitwear 15% (promo_autumn_knit, running until Nov 15" (15, 15 not shown); fact "pausing has no end time: the agent says someone has to resum" (9 not shown)

### 원본 파사드 · 3회차 · ✗ 실패

토큰 9,434 · 모델 호출 4회 · 도구 호출 3회

**질문 1**
> pause the knit sale until monday, we're out of the good sizes

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 7 candidates: getPrmtGridList, getPrmtGridListCnt, savePrmtList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt, getPrdGridList, getPrdGridListCnt
- 계획: `getPrmtGridList` `` {"pageNo":0,"prmtNm":"knit","pageSize":20} ``; `savePrmtList` `` {"rows":[{"endDtm":"2026-11-09 23:59:59","prmtNo":"","rowStat":"U","prmtStatCd":"30"}]} ``
1. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"prmtNm":"knit","pageSize":20} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrmtGridList` `` {"pageNo":0,"prmtNm":"knit sale","pageSize":10} ``; `savePrmtList` `` {"rows":[]} ``
2. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"prmtNm":"knit sale","pageSize":10} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrmtGridList` `` {"pageNo":0,"prmtNm":"knit sale","pageSize":10} ``; `savePrmtList` `` {"rows":[]} ``
3. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"prmtNm":"knit sale","pageSize":10} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``

**답변 1**
> getPrmtGridList failed (ERR_PARAM): Invalid paging. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "Autumn knitwear 15% (promo_autumn_knit, running until Nov 15" (15, 15 not shown); fact "pausing has no end time: the agent says someone has to resum" (9 not shown)
