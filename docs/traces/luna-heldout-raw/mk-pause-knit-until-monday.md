# mk-pause-knit-until-monday — luna-heldout-raw

[← 실행 묶음](README.md)

**과업**

> pause the knit sale until monday, we're out of the good sizes

- 답에 있어야 할 사실: Autumn knitwear 15% (promo_autumn_knit, running until Nov 15) is paused
- 답에 있어야 할 사실: pausing has no end time: the agent says someone has to resume it on Mon Nov 9

### GPT-6-Luna · 원본 파사드 · 1회차 · ✗ 실패

토큰 31,161 · 모델 호출 4회 · 도구 호출 3회

**질문 1**
> pause the knit sale until monday, we're out of the good sizes

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 7 candidates: getPrmtGridList, getPrmtGridListCnt, savePrmtList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt, getPrdGridList, getPrdGridListCnt
- 계획: `getPrmtGridList` `` {"pageNo":0,"prmtNm":"knit","pageSize":100} ``
1. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"prmtNm":"knit","pageSize":100} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrmtGridList` `` {"pageNo":0,"prmtNm":"knit","pageSize":10} ``
2. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"prmtNm":"knit","pageSize":10} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrmtGridList` `` {"pageNo":0,"prmtNm":"knit","pageSize":10} ``; `savePrmtList` `` {"rows":[{"rowStat":"U","prmtStatCd":"90"}]} ``
3. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"prmtNm":"knit","pageSize":10} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``

**답변 1**
> getPrmtGridList failed (ERR_PARAM): Invalid paging. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "Autumn knitwear 15% (promo_autumn_knit, running until Nov 15" (15, 15 not shown); fact "pausing has no end time: the agent says someone has to resum" (9 not shown)

### GPT-6-Luna · 원본 파사드 · 2회차 · ✗ 실패

토큰 30,584 · 모델 호출 4회 · 도구 호출 3회

**질문 1**
> pause the knit sale until monday, we're out of the good sizes

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 7 candidates: getPrmtGridList, getPrmtGridListCnt, savePrmtList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt, getPrdGridList, getPrdGridListCnt
- 계획: `getPrmtGridList` `` {"pageNo":0,"prmtNm":"knit","pageSize":100} ``; `savePrmtList` `` {"rows":[{"endDtm":"2026-11-09 00:00","rowStat":"U","prmtStatCd":"30"}]} ``
1. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"prmtNm":"knit","pageSize":100} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrmtGridList` `` {"pageNo":0,"prmtNm":"knit","pageSize":20} ``; `savePrmtList` `` {"rows":[]} ``
2. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"prmtNm":"knit","pageSize":20} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrmtGridList` `` {"pageNo":0,"prmtNm":"knit","pageSize":20} ``; `savePrmtList` `` {"rows":[{"endDtm":"2026-11-09 00:00:00","rowStat":"U","prmtStatCd":"20"}]} ``
3. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"prmtNm":"knit","pageSize":20} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``

**답변 1**
> getPrmtGridList failed (ERR_PARAM): Invalid paging. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "Autumn knitwear 15% (promo_autumn_knit, running until Nov 15" (15, 15 not shown); fact "pausing has no end time: the agent says someone has to resum" (9 not shown)

### GPT-6-Luna · 원본 파사드 · 3회차 · ✗ 실패

토큰 29,872 · 모델 호출 4회 · 도구 호출 3회

**질문 1**
> pause the knit sale until monday, we're out of the good sizes

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 7 candidates: getPrmtGridList, getPrmtGridListCnt, savePrmtList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt, getPrdGridList, getPrdGridListCnt
- 계획: `getPrmtGridList` `` {"pageNo":0,"prmtNm":"knit","pageSize":50} ``; `savePrmtList` `` {"rows":[{"endDtm":"2026-11-09 00:00:00","rowStat":"U","prmtStatCd":"30"}]} ``
1. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"prmtNm":"knit","pageSize":50} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrmtGridList` `` {"pageNo":0,"prmtNm":"knit sale","pageSize":20} ``; `savePrmtList` `` {"rows":[{"endDtm":"2026-11-09 00:00:00","rowStat":"U","prmtStatCd":"20"}]} ``
2. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"prmtNm":"knit sale","pageSize":20} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrmtGridList` `` {"pageNo":0,"prmtNm":"knit","pageSize":20} ``; `savePrmtList` `` {"rows":[{"endDtm":"2026-11-09 00:00:00","rowStat":"U","prmtStatCd":"90"}]} ``
3. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"prmtNm":"knit","pageSize":20} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``

**답변 1**
> getPrmtGridList failed (ERR_PARAM): Invalid paging. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "Autumn knitwear 15% (promo_autumn_knit, running until Nov 15" (15, 15 not shown); fact "pausing has no end time: the agent says someone has to resum" (9 not shown)
