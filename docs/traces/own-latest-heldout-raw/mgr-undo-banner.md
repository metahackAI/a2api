# mgr-undo-banner — own-latest-heldout-raw

[← 실행 묶음](README.md)

**과업**

> actually put the old homepage banner back

- 답에 있어야 할 사실: the swap is cs_1039, live since 10:00; it can be undone until Nov 7 23:59
- 답에 있어야 할 사실: undo is a person's button on the change set; the agent points to it instead of booking a new banner

### 원본 파사드 · 1회차 · ✗ 실패

토큰 5,963 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> actually put the old homepage banner back

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: saveDispBnrList, getDispCornerList, getPrmtGridList, getPrmtGridListCnt, getMbrGrdList
- 계획: `getDispCornerList` `` {"endDtm":"2026-11-06 23:59","strtDtm":"2026-11-06 00:00","cornerTpCd":"H","dispPageCd":"01"} ``
1. 에이전트 → **`getDispCornerList`** `` {"endDtm":"2026-11-06 23:59","strtDtm":"2026-11-06 00:00","cornerTpCd":"H","dispPageCd":"01"} ``
   ← 결과: `` {"list":[{"bnrList":[{"dispNo":"dsp_october_edit","endDtm":"2026-11-06T09:59:00-05:00","bnrTitl":"The October edit","strtDtm":"2026-10-01T00:00:00-04:00","dispStatCd":"90","tgtMbrGrdCd":"G00"},{"dispNo":"dsp_fall_layers","endDtm":null,"bnrTitl":"Fall layers","strtDtm":"2026-11-06T10:00:00-05:00","dispStatCd":"20","tgtMbrGrdCd":"G00"}],"cornerNm":"Home hero","cornerNo":"slot_home_hero","cornerTpCd":"H"}]} ``

**답변 1**
> The old homepage banner is already scheduled to return. The Home hero slot shows 'The October edit' running until Fri Nov 6, 9:59 AM, and 'Fall layers' is set to start at 10:00 AM on Fri Nov 6 with status 20. No change set was created this turn, so nothing was written.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "the swap is cs_1039, live since 10:00; it can be undone unti" (1039, 7, 23 not shown)

### 원본 파사드 · 2회차 · ✗ 실패

토큰 5,992 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> actually put the old homepage banner back

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: saveDispBnrList, getDispCornerList, getPrmtGridList, getPrmtGridListCnt, getMbrGrdList
- 계획: `getDispCornerList` `` {"endDtm":"2026-11-06 11:00","strtDtm":"2026-11-01 00:00","cornerTpCd":"H","dispPageCd":"01"} ``
1. 에이전트 → **`getDispCornerList`** `` {"endDtm":"2026-11-06 11:00","strtDtm":"2026-11-01 00:00","cornerTpCd":"H","dispPageCd":"01"} ``
   ← 결과: `` {"list":[{"bnrList":[{"dispNo":"dsp_october_edit","endDtm":"2026-11-06T09:59:00-05:00","bnrTitl":"The October edit","strtDtm":"2026-10-01T00:00:00-04:00","dispStatCd":"90","tgtMbrGrdCd":"G00"},{"dispNo":"dsp_fall_layers","endDtm":null,"bnrTitl":"Fall layers","strtDtm":"2026-11-06T10:00:00-05:00","dispStatCd":"20","tgtMbrGrdCd":"G00"}],"cornerNm":"Home hero","cornerNo":"slot_home_hero","cornerTpCd":"H"}]} ``

**답변 1**
> The homepage hero slot currently shows 'The October edit' until Fri Nov 6, 9:59 AM, then 'Fall layers' starts at 10:00 AM. I don't have a change set to restore a previous banner yet. If you tell me which banner you want back and when it should run, I can schedule it for the Home hero slot.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "the swap is cs_1039, live since 10:00; it can be undone unti" (1039, 7, 23 not shown)

### 원본 파사드 · 3회차 · ✗ 실패

토큰 5,956 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> actually put the old homepage banner back

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: saveDispBnrList, getDispCornerList, getPrmtGridList, getPrmtGridListCnt, getMbrGrdList
- 계획: `getDispCornerList` `` {"endDtm":"2026-11-06 23:59","strtDtm":"2026-11-06 00:00","cornerTpCd":"H","dispPageCd":"01"} ``
1. 에이전트 → **`getDispCornerList`** `` {"endDtm":"2026-11-06 23:59","strtDtm":"2026-11-06 00:00","cornerTpCd":"H","dispPageCd":"01"} ``
   ← 결과: `` {"list":[{"bnrList":[{"dispNo":"dsp_october_edit","endDtm":"2026-11-06T09:59:00-05:00","bnrTitl":"The October edit","strtDtm":"2026-10-01T00:00:00-04:00","dispStatCd":"90","tgtMbrGrdCd":"G00"},{"dispNo":"dsp_fall_layers","endDtm":null,"bnrTitl":"Fall layers","strtDtm":"2026-11-06T10:00:00-05:00","dispStatCd":"20","tgtMbrGrdCd":"G00"}],"cornerNm":"Home hero","cornerNo":"slot_home_hero","cornerTpCd":"H"}]} ``

**답변 1**
> The homepage hero slot currently shows 'The October edit' until Fri Nov 6, 9:59 AM, then 'Fall layers' starts at 10:00 AM. I can’t restore the old banner yet because no change set was created this turn. Tell me which banner you want back and I’ll schedule it for the Home hero slot.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "the swap is cs_1039, live since 10:00; it can be undone unti" (1039, 7, 23 not shown)
