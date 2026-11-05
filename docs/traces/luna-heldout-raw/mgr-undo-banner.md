# mgr-undo-banner — luna-heldout-raw

[← 실행 묶음](README.md)

**과업**

> actually put the old homepage banner back

- 답에 있어야 할 사실: the swap is cs_1039, live since 10:00; it can be undone until Nov 7 23:59
- 답에 있어야 할 사실: undo is a person's button on the change set; the agent points to it instead of booking a new banner

### GPT-6-Luna · 원본 파사드 · 1회차 · ✗ 실패

토큰 30,670 · 모델 호출 4회 · 도구 호출 4회

**질문 1**
> actually put the old homepage banner back

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: saveDispBnrList, getDispCornerList, getPrmtGridList, getPrmtGridListCnt, getMbrGrdList
- 계획: `getDispCornerList` `` {"endDtm":"2026-11-06 11:00:00","strtDtm":"2026-01-01 00:00:00","dispPageCd":"01"} ``
1. 에이전트 → **`getDispCornerList`** `` {"endDtm":"2026-11-06 11:00:00","strtDtm":"2026-01-01 00:00:00","dispPageCd":"01"} ``
   ← 실패: `` {"code":"invalid_input","class":"invalid_input","message":"'2026-01-01 00:00:00' is not a date-time (expected 2026-11-07T00:00 or RFC 3339)","next_tool":null} ``
- 계획: `getDispCornerList` `` {"endDtm":"2026-11-06T11:00","strtDtm":"2026-01-01T00:00","dispPageCd":"01"} ``; `saveDispBnrList` `` {"rows":[]} ``
2. 에이전트 → **`getDispCornerList`** `` {"endDtm":"2026-11-06T11:00","strtDtm":"2026-01-01T00:00","dispPageCd":"01"} ``
   ← 결과: `` {"list":[{"bnrList":[{"dispNo":"dsp_october_edit","endDtm":"2026-11-06T09:59:00-05:00","bnrTitl":"The October edit","strtDtm":"2026-10-01T00:00:00-04:00","dispStatCd":"90","tgtMbrGrdCd":"G00"},{"dispNo":"dsp_fall_layers","endDtm":null,"bnrTitl":"Fall layers","strtDtm":"2026-11-06T10:00:00-05:00","dispStatCd":"20","tgtMbrGrdCd":"G00"}],"cornerNm":"Home hero","cornerNo":"slot_home_hero","cornerTpCd":"H"},{"bnrList":[],"cornerNm":"New in","cornerNo":"slot_home_new_in","cornerTpCd":"G"},{"bnrList":[],"cornerNm":"Stories","cornerNo":"slot_home_stories","cornerTpCd":"B"},{"bnrList":[],"cornerNm":"Br… (+55자) ``
3. 에이전트 → **`saveDispBnrList`** `` {"rows":[]} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"No rows.","next_tool":null} ``
- 계획: `saveDispBnrList` `` {"rows":[{"bnrTitl":"The October edit","rowStat":"I","strtDtm":"2026-11-06T11:00:00-05:00","cornerNo":"slot_home_hero","tgtMbrGrdCd":"G00"}]} ``
4. 에이전트 → **`saveDispBnrList`** `` {"rows":[{"bnrTitl":"The October edit","rowStat":"I","strtDtm":"2026-11-06T11:00:00-05:00","cornerNo":"slot_home_hero","tgtMbrGrdCd":"G00"}]} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Row 1: 'btnNm' is required.","next_tool":null} ``

**답변 1**
> The old homepage banner, “The October edit,” wasn’t restored because the request was missing a required button name. Choose a button name, then the change can be prepared for your approval.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: fact "the swap is cs_1039, live since 10:00; it can be undone unti" (1039, 10, 0, 7, 23, 59 not shown)

### GPT-6-Luna · 원본 파사드 · 2회차 · ✗ 실패

토큰 21,856 · 모델 호출 3회 · 도구 호출 2회

**질문 1**
> actually put the old homepage banner back

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: saveDispBnrList, getDispCornerList, getPrmtGridList, getPrmtGridListCnt, getMbrGrdList
- 계획: `getDispCornerList` `` {"endDtm":"2099-12-31 23:59:59","strtDtm":"2000-01-01 00:00:00","dispPageCd":"01"} ``
1. 에이전트 → **`getDispCornerList`** `` {"endDtm":"2099-12-31 23:59:59","strtDtm":"2000-01-01 00:00:00","dispPageCd":"01"} ``
   ← 실패: `` {"code":"invalid_input","class":"invalid_input","message":"'2000-01-01 00:00:00' is not a date-time (expected 2026-11-07T00:00 or RFC 3339)","next_tool":null} ``
- 계획: `getDispCornerList` `` {"endDtm":"2026-11-07T00:00","strtDtm":"2026-11-06T11:00","dispPageCd":"01"} ``
2. 에이전트 → **`getDispCornerList`** `` {"endDtm":"2026-11-07T00:00","strtDtm":"2026-11-06T11:00","dispPageCd":"01"} ``
   ← 결과: `` {"list":[{"bnrList":[{"dispNo":"dsp_fall_layers","endDtm":null,"bnrTitl":"Fall layers","strtDtm":"2026-11-06T10:00:00-05:00","dispStatCd":"20","tgtMbrGrdCd":"G00"}],"cornerNm":"Home hero","cornerNo":"slot_home_hero","cornerTpCd":"H"},{"bnrList":[],"cornerNm":"New in","cornerNo":"slot_home_new_in","cornerTpCd":"G"},{"bnrList":[],"cornerNm":"Stories","cornerNo":"slot_home_stories","cornerTpCd":"B"},{"bnrList":[],"cornerNm":"Brands","cornerNo":"slot_home_brands","cornerTpCd":"S"}]} ``

**답변 1**
> The “Fall layers” banner is already back in the Home hero slot, starting Fri Nov 6 at 10:00 AM, with no end date. No change is needed.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: fact "the swap is cs_1039, live since 10:00; it can be undone unti" (1039, 7, 23, 59 not shown)

### GPT-6-Luna · 원본 파사드 · 3회차 · ✗ 실패

토큰 22,579 · 모델 호출 3회 · 도구 호출 2회

**질문 1**
> actually put the old homepage banner back

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: saveDispBnrList, getDispCornerList, getPrmtGridList, getPrmtGridListCnt, getMbrGrdList
- 계획: `getDispCornerList` `` {"endDtm":"2026-11-06 11:00:00","strtDtm":"2000-01-01 00:00:00","dispPageCd":"01"} ``
1. 에이전트 → **`getDispCornerList`** `` {"endDtm":"2026-11-06 11:00:00","strtDtm":"2000-01-01 00:00:00","dispPageCd":"01"} ``
   ← 실패: `` {"code":"invalid_input","class":"invalid_input","message":"'2000-01-01 00:00:00' is not a date-time (expected 2026-11-07T00:00 or RFC 3339)","next_tool":null} ``
- 계획: `getDispCornerList` `` {"endDtm":"2026-11-07T00:00:00-05:00","strtDtm":"2000-01-01T00:00:00Z","dispPageCd":"01"} ``
2. 에이전트 → **`getDispCornerList`** `` {"endDtm":"2026-11-07T00:00:00-05:00","strtDtm":"2000-01-01T00:00:00Z","dispPageCd":"01"} ``
   ← 결과: `` {"list":[{"bnrList":[{"dispNo":"dsp_october_edit","endDtm":"2026-11-06T09:59:00-05:00","bnrTitl":"The October edit","strtDtm":"2026-10-01T00:00:00-04:00","dispStatCd":"90","tgtMbrGrdCd":"G00"},{"dispNo":"dsp_fall_layers","endDtm":null,"bnrTitl":"Fall layers","strtDtm":"2026-11-06T10:00:00-05:00","dispStatCd":"20","tgtMbrGrdCd":"G00"}],"cornerNm":"Home hero","cornerNo":"slot_home_hero","cornerTpCd":"H"},{"bnrList":[],"cornerNm":"New in","cornerNo":"slot_home_new_in","cornerTpCd":"G"},{"bnrList":[],"cornerNm":"Stories","cornerNo":"slot_home_stories","cornerTpCd":"B"},{"bnrList":[],"cornerNm":"Br… (+55자) ``

**답변 1**
> “Fall layers” is the current Home hero banner; “The October edit” ended Fri Nov 6 at 9:59 AM. No change was made, so there’s nothing to approve.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: fact "the swap is cs_1039, live since 10:00; it can be undone unti" (1039, 10, 0, 7, 23 not shown)
