# mk-hero-free-next-weekend — luna-design-raw

[← 실행 묶음](README.md)

**과업**

> is the homepage hero open next weekend? want to run something for VIPs

- 답에 있어야 할 사실: next weekend is Sat Nov 14 – Sun Nov 15
- 답에 있어야 할 사실: the home hero shows Fall layers to everyone with no end date, and is free for VIP, Gold and Member audiences all of Nov 14–15

### GPT-6-Luna · 원본 파사드 · 1회차 · ✓ 통과

토큰 19,776 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> is the homepage hero open next weekend? want to run something for VIPs

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 7 candidates: getPrmtTgtMbrList, getPrmtTgtMbrListCnt, getMbrGrdList, getPrmtGridList, getPrmtGridListCnt, getPrdGridList, getPrdGridListCnt
- 계획: `getPrmtGridList` `` {"srchEndDtm":"2026-11-15 23:59","srchStrtDtm":"2026-11-14 00:00"} ``
1. 에이전트 → **`getPrmtGridList`** `` {"srchEndDtm":"2026-11-15 23:59","srchStrtDtm":"2026-11-14 00:00"} ``
   ← 결과: `` {"list":[{"endDtm":"2026-11-20T23:59:00-05:00","prmtNm":"Denim bundle","prmtNo":"promo_denim_bundle","strtDtm":"2026-11-13T00:00:00-05:00","prmtTpCd":"T02","prmtStatCd":"10","tgtMbrGrdCd":"G00"},{"endDtm":"2026-11-15T23:59:00-05:00","prmtNm":"Autumn knitwear 15%","prmtNo":"promo_autumn_knit","strtDtm":"2026-11-01T00:00:00-04:00","prmtTpCd":"T01","prmtStatCd":"20","tgtMbrGrdCd":"G00"},{"endDtm":null,"prmtNm":"Birthday coupon","prmtNo":"promo_birthday","strtDtm":"2026-01-01T00:00:00-05:00","prmtTpCd":"T02","prmtStatCd":"20","tgtMbrGrdCd":"G01"},{"endDtm":null,"prmtNm":"Free shipping over $80","p… (+307자) ``

**답변 1**
> The homepage hero’s availability isn’t shown here, so I can’t tell whether it’s open November 14–15. The promotion list doesn’t show a VIP promotion for that weekend; check the hero schedule before planning one.

화면 블록: product_table(5 of 5)

**채점**: ✓ 통과

### GPT-6-Luna · 원본 파사드 · 2회차 · ✗ 실패

토큰 44,241 · 모델 호출 6회 · 도구 호출 4회

**질문 1**
> is the homepage hero open next weekend? want to run something for VIPs

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 7 candidates: getPrmtTgtMbrList, getPrmtTgtMbrListCnt, getMbrGrdList, getPrmtGridList, getPrmtGridListCnt, getPrdGridList, getPrdGridListCnt
- 계획: `getMbrGrdList` `` {} ``; `getPrmtGridList` `` {"pageNo":0,"pageSize":100,"srchEndDtm":"2026-11-15 23:59","srchStrtDtm":"2026-11-14 00:00"} ``
1. 에이전트 → **`getMbrGrdList`** `` {} ``
   ← 결과: `` {"list":[{"mbrCnt":1284,"sortSeq":3,"mbrGrdCd":"G03","mbrGrdNm":"VIP"},{"mbrCnt":2900,"sortSeq":2,"mbrGrdCd":"G02","mbrGrdNm":"Gold"},{"mbrCnt":9816,"sortSeq":1,"mbrGrdCd":"G01","mbrGrdNm":"Member"}]} ``
2. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"pageSize":100,"srchEndDtm":"2026-11-15 23:59","srchStrtDtm":"2026-11-14 00:00"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrmtGridList` `` {"pageNo":0,"pageSize":20,"srchEndDtm":"2026-11-08 23:59:00","srchStrtDtm":"2026-11-07 00:00:00","tgtMbrGrdCd":"G03"} ``
3. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"pageSize":20,"srchEndDtm":"2026-11-08 23:59:00","srchStrtDtm":"2026-11-07 00:00:00","tgtMbrGrdCd":"G03"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrmtGridList` `` {"pageNo":0,"pageSize":50} ``
4. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"pageSize":50} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``

**답변 1**
> I couldn’t check whether the homepage hero is open for Nov 7–8 because the promotion schedule lookup failed due to invalid paging. Please try again so I can check availability before planning anything for VIPs.

화면 블록: product_table(3 of 3)

**채점**: ✗ 실패 — 빠진 것: fact "next weekend is Sat Nov 14 – Sun Nov 15" (14, 15 not shown); fact "the home hero shows Fall layers to everyone with no end date" (14, 15 not shown)

### GPT-6-Luna · 원본 파사드 · 3회차 · ✗ 실패

토큰 36,238 · 모델 호출 5회 · 도구 호출 3회

**질문 1**
> is the homepage hero open next weekend? want to run something for VIPs

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 7 candidates: getPrmtTgtMbrList, getPrmtTgtMbrListCnt, getMbrGrdList, getPrmtGridList, getPrmtGridListCnt, getPrdGridList, getPrdGridListCnt
- 계획: `getPrmtGridList` `` {"srchEndDtm":"2026-11-15 23:59:00","srchStrtDtm":"2026-11-13 00:00:00","tgtMbrGrdCd":"VIP"} ``
1. 에이전트 → **`getPrmtGridList`** `` {"srchEndDtm":"2026-11-15 23:59:00","srchStrtDtm":"2026-11-13 00:00:00","tgtMbrGrdCd":"VIP"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid member grade code.","next_tool":null} ``
- 계획: `getMbrGrdList` `` {} ``; `getPrmtGridList` `` {"srchEndDtm":"2026-11-15 23:59","srchStrtDtm":"2026-11-14 00:00"} ``
2. 에이전트 → **`getMbrGrdList`** `` {} ``
   ← 결과: `` {"list":[{"mbrCnt":1284,"sortSeq":3,"mbrGrdCd":"G03","mbrGrdNm":"VIP"},{"mbrCnt":2900,"sortSeq":2,"mbrGrdCd":"G02","mbrGrdNm":"Gold"},{"mbrCnt":9816,"sortSeq":1,"mbrGrdCd":"G01","mbrGrdNm":"Member"}]} ``
3. 에이전트 → **`getPrmtGridList`** `` {"srchEndDtm":"2026-11-15 23:59","srchStrtDtm":"2026-11-14 00:00"} ``
   ← 결과: `` {"list":[{"endDtm":"2026-11-20T23:59:00-05:00","prmtNm":"Denim bundle","prmtNo":"promo_denim_bundle","strtDtm":"2026-11-13T00:00:00-05:00","prmtTpCd":"T02","prmtStatCd":"10","tgtMbrGrdCd":"G00"},{"endDtm":"2026-11-15T23:59:00-05:00","prmtNm":"Autumn knitwear 15%","prmtNo":"promo_autumn_knit","strtDtm":"2026-11-01T00:00:00-04:00","prmtTpCd":"T01","prmtStatCd":"20","tgtMbrGrdCd":"G00"},{"endDtm":null,"prmtNm":"Birthday coupon","prmtNo":"promo_birthday","strtDtm":"2026-01-01T00:00:00-05:00","prmtTpCd":"T02","prmtStatCd":"20","tgtMbrGrdCd":"G01"},{"endDtm":null,"prmtNm":"Free shipping over $80","p… (+307자) ``

**답변 1**
> VIP is a membership tier, and the Denim bundle promotion runs through Nov 20, but that doesn’t show whether the homepage hero is available next weekend. Nothing has been drafted; you’ll need to confirm the hero slot is open and what VIP offer you want to run.

화면 블록: product_table(5 of 5)

**채점**: ✗ 실패 — 빠진 것: fact "next weekend is Sat Nov 14 – Sun Nov 15" (14 not shown); fact "the home hero shows Fall layers to everyone with no end date" (14 not shown)
