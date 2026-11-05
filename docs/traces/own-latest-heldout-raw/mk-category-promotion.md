# mk-category-promotion — own-latest-heldout-raw

[← 실행 묶음](README.md)

**과업**

> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 답에 있어야 할 사실: 2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store time

### 원본 파사드 · 1회차 · ✗ 실패

토큰 10,098 · 모델 호출 5회 · 도구 호출 2회

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: getPrmtGridList, getPrmtGridListCnt, savePrmtList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `getPrmtGridList` `` {"pageNo":0,"pageSize":1,"prmtStatCd":"00"} ``
1. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"pageSize":1,"prmtStatCd":"00"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrmtGridList` `` {"pageNo":0,"pageSize":10} ``
2. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"pageSize":10} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: everyone · Outerwear · $50 off orders above $250 · 2 weeks from 2026-11-06 11:00 America/New_York · 0 steps by Muse Glimmer 30B

**답변 1**
> I could not find anything to show for that.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (2, 6, 19, 23, 59 not shown)

### 원본 파사드 · 2회차 · ✗ 실패

토큰 7,968 · 모델 호출 3회 · 도구 호출 3회

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: getPrmtGridList, getPrmtGridListCnt, savePrmtList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `savePrmtList` `` {"rows":[{"dcRt":0,"ctgNo":"","endDtm":"2026-11-20 23:59","prmtNm":"Outerwear $50 off orders above $250","rowStat":"I","strtDtm":"2026-11-06 11:00","prmtTpCd":"T01","aplyTgtCd":"C","prdNoList":[],"prmtStatCd":"10","tgtMbrGrdCd":""}]} ``
1. 에이전트 → **`savePrmtList`** `` {"rows":[{"dcRt":0,"ctgNo":"","endDtm":"2026-11-20 23:59","prmtNm":"Outerwear $50 off orders above $250","rowStat":"I","strtDtm":"2026-11-06 11:00","prmtTpCd":"T01","aplyTgtCd":"C","prdNoList":[],"prmtStatCd":"10","tgtMbrGrdCd":""}]} ``
   ← 실패: `` {"code":"invalid_input","class":"invalid_input","message":"Row 1: 'percent_off' must be above 0 and below 100, with at most two decimals; got 0.","next_tool":null} ``
- 계획: `savePrmtList` `` {"rows":[{"dcRt":0,"ctgNo":"","endDtm":"2026-11-20 11:00","prmtNm":"Outerwear $50 off orders above $250","rowStat":"I","strtDtm":"2026-11-06 11:00","prmtTpCd":"T01","aplyTgtCd":"C","prdNoList":[],"prmtStatCd":"10","tgtMbrGrdCd":""}]} ``
2. 에이전트 → **`savePrmtList`** `` {"rows":[{"dcRt":0,"ctgNo":"","endDtm":"2026-11-20 11:00","prmtNm":"Outerwear $50 off orders above $250","rowStat":"I","strtDtm":"2026-11-06 11:00","prmtTpCd":"T01","aplyTgtCd":"C","prdNoList":[],"prmtStatCd":"10","tgtMbrGrdCd":""}]} ``
   ← 실패: `` {"code":"invalid_input","class":"invalid_input","message":"Row 1: 'percent_off' must be above 0 and below 100, with at most two decimals; got 0.","next_tool":null} ``
- 계획: `savePrmtList` `` {"rows":[{"dcRt":0,"ctgNo":"","endDtm":"2026-11-20 11:00","prmtNm":"Outerwear $50 off orders above $250","rowStat":"I","strtDtm":"2026-11-06 11:00","prmtTpCd":"T01","aplyTgtCd":"C","prdNoList":[],"prmtStatCd":"10","tgtMbrGrdCd":""}]} ``
3. 에이전트 → **`savePrmtList`** `` {"rows":[{"dcRt":0,"ctgNo":"","endDtm":"2026-11-20 11:00","prmtNm":"Outerwear $50 off orders above $250","rowStat":"I","strtDtm":"2026-11-06 11:00","prmtTpCd":"T01","aplyTgtCd":"C","prdNoList":[],"prmtStatCd":"10","tgtMbrGrdCd":""}]} ``
   ← 실패: `` {"code":"invalid_input","class":"invalid_input","message":"Row 1: 'percent_off' must be above 0 and below 100, with at most two decimals; got 0.","next_tool":null} ``

**답변 1**
> savePrmtList failed (invalid_input): Row 1: `percent_off` must be above 0 and below 100, with at most two decimals; got 0. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (2, 6, 19, 23, 59 not shown)

### 원본 파사드 · 3회차 · ✗ 실패

토큰 8,611 · 모델 호출 4회 · 도구 호출 1회

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: getPrmtGridList, getPrmtGridListCnt, savePrmtList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `getPrmtGridList` `` {"pageNo":0,"pageSize":10,"prmtStatCd":"10"} ``
1. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"pageSize":10,"prmtStatCd":"10"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: everyone · Outerwear · $50 off orders above $250 · 2 weeks from 2026-11-06 11:00 America/New_York · 0 steps by Muse Glimmer 30B

**답변 1**
> The promotion for Outerwear with $50 off orders above $250 for 2 weeks from Fri Nov 6, 11:00 AM America/New_York is not created yet. No change set was produced in this turn, so there is nothing to approve or publish at the moment. If you want, I can draft the coupon and the banner for the Outerwear category and the everyone tier for the requested 2-week window.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (19, 23, 59 not shown)
