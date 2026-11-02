# mk-category-promotion — own22-heldout-raw-logs

[← 실행 묶음](README.md)

**과업**

> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 답에 있어야 할 사실: 2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store time

### 원본 파사드 · 1회차 · ✗ 실패

토큰 7,311 · 모델 호출 3회 · 도구 호출 3회

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: getPrmtGridList, getPrmtGridListCnt, savePrmtList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `savePrmtList` `` {"rows":[{"dcRt":50,"ctgNo":"Outerwear","endDtm":"2026-11-20T23:59:00-05:00","prmtNm":"Outerwear $50 off orders above $250","rowStat":"I","strtDtm":"2026-11-06T11:00:00-05:00","prmtTpCd":"T01","aplyTgtCd":"C","prmtStatCd":"10","tgtMbrGrdCd":"everyone"}]} ``
1. 에이전트 → **`savePrmtList`** `` {"rows":[{"dcRt":50,"ctgNo":"Outerwear","endDtm":"2026-11-20T23:59:00-05:00","prmtNm":"Outerwear $50 off orders above $250","rowStat":"I","strtDtm":"2026-11-06T11:00:00-05:00","prmtTpCd":"T01","aplyTgtCd":"C","prmtStatCd":"10","tgtMbrGrdCd":"everyone"}]} ``
   ← 실패: `` {"code":"invalid_input","class":"invalid_input","message":"Row 1: 'category_id' must look like 'cat_…'; got 'Outerwear'.","next_tool":null} ``
- 계획: `savePrmtList` `` {"rows":[{"dcRt":50,"ctgNo":"Outerwear","endDtm":"2026-11-20 11:00","prmtNm":"Outerwear $50 off orders above $250","rowStat":"I","strtDtm":"2026-11-06 11:00","prmtTpCd":"T01","aplyTgtCd":"C","prmtStatCd":"10","tgtMbrGrdCd":""}]} ``
2. 에이전트 → **`savePrmtList`** `` {"rows":[{"dcRt":50,"ctgNo":"Outerwear","endDtm":"2026-11-20 11:00","prmtNm":"Outerwear $50 off orders above $250","rowStat":"I","strtDtm":"2026-11-06 11:00","prmtTpCd":"T01","aplyTgtCd":"C","prmtStatCd":"10","tgtMbrGrdCd":""}]} ``
   ← 실패: `` {"code":"invalid_input","class":"invalid_input","message":"Row 1: 'category_id' must look like 'cat_…'; got 'Outerwear'.","next_tool":null} ``
- 계획: `savePrmtList` `` {"rows":[{"dcRt":50,"ctgNo":"Outerwear","endDtm":"2026-11-20 23:59","prmtNm":"Outerwear $50 off orders above $250","rowStat":"I","strtDtm":"2026-11-06 11:00","prmtTpCd":"T01","aplyTgtCd":"C","prmtStatCd":"10","tgtMbrGrdCd":""}]} ``
3. 에이전트 → **`savePrmtList`** `` {"rows":[{"dcRt":50,"ctgNo":"Outerwear","endDtm":"2026-11-20 23:59","prmtNm":"Outerwear $50 off orders above $250","rowStat":"I","strtDtm":"2026-11-06 11:00","prmtTpCd":"T01","aplyTgtCd":"C","prmtStatCd":"10","tgtMbrGrdCd":""}]} ``
   ← 실패: `` {"code":"invalid_input","class":"invalid_input","message":"Row 1: 'category_id' must look like 'cat_…'; got 'Outerwear'.","next_tool":null} ``

**답변 1**
> savePrmtList failed (invalid_input): Row 1: `category_id` must look like `cat_…`; got `Outerwear`. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (2, 6, 19, 23, 59 not shown)

### 원본 파사드 · 2회차 · ✗ 실패

토큰 7,299 · 모델 호출 3회 · 도구 호출 3회

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: getPrmtGridList, getPrmtGridListCnt, savePrmtList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `savePrmtList` `` {"rows":[{"dcRt":50,"ctgNo":"Outerwear","endDtm":"2026-11-20 23:59","prmtNm":"Outerwear $50 off orders above $250","rowStat":"I","strtDtm":"2026-11-06 11:00","prmtTpCd":"T01","aplyTgtCd":"C","prmtStatCd":"10","tgtMbrGrdCd":"everyone"}]} ``
1. 에이전트 → **`savePrmtList`** `` {"rows":[{"dcRt":50,"ctgNo":"Outerwear","endDtm":"2026-11-20 23:59","prmtNm":"Outerwear $50 off orders above $250","rowStat":"I","strtDtm":"2026-11-06 11:00","prmtTpCd":"T01","aplyTgtCd":"C","prmtStatCd":"10","tgtMbrGrdCd":"everyone"}]} ``
   ← 실패: `` {"code":"invalid_input","class":"invalid_input","message":"Row 1: 'category_id' must look like 'cat_…'; got 'Outerwear'.","next_tool":null} ``
- 계획: `savePrmtList` `` {"rows":[{"dcRt":50,"ctgNo":"Outerwear","endDtm":"2026-11-20 23:59","prmtNm":"Outerwear $50 off orders above $250","rowStat":"I","strtDtm":"2026-11-06 11:00","prmtTpCd":"T01","aplyTgtCd":"C","prmtStatCd":"10","tgtMbrGrdCd":""}]} ``
2. 에이전트 → **`savePrmtList`** `` {"rows":[{"dcRt":50,"ctgNo":"Outerwear","endDtm":"2026-11-20 23:59","prmtNm":"Outerwear $50 off orders above $250","rowStat":"I","strtDtm":"2026-11-06 11:00","prmtTpCd":"T01","aplyTgtCd":"C","prmtStatCd":"10","tgtMbrGrdCd":""}]} ``
   ← 실패: `` {"code":"invalid_input","class":"invalid_input","message":"Row 1: 'category_id' must look like 'cat_…'; got 'Outerwear'.","next_tool":null} ``
- 계획: `savePrmtList` `` {"rows":[{"dcRt":50,"ctgNo":"Outerwear","endDtm":"2026-11-20 23:59","prmtNm":"Outerwear $50 off orders above $250","rowStat":"I","strtDtm":"2026-11-06 11:00","prmtTpCd":"T01","aplyTgtCd":"C","prmtStatCd":"10","tgtMbrGrdCd":""}]} ``
3. 에이전트 → **`savePrmtList`** `` {"rows":[{"dcRt":50,"ctgNo":"Outerwear","endDtm":"2026-11-20 23:59","prmtNm":"Outerwear $50 off orders above $250","rowStat":"I","strtDtm":"2026-11-06 11:00","prmtTpCd":"T01","aplyTgtCd":"C","prmtStatCd":"10","tgtMbrGrdCd":""}]} ``
   ← 실패: `` {"code":"invalid_input","class":"invalid_input","message":"Row 1: 'category_id' must look like 'cat_…'; got 'Outerwear'.","next_tool":null} ``

**답변 1**
> savePrmtList failed (invalid_input): Row 1: `category_id` must look like `cat_…`; got `Outerwear`. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (2, 6, 19, 23, 59 not shown)
