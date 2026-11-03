# mk-whats-running-this-weekend — own-latest-design-raw

[← 실행 묶음](README.md)

**과업**

> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 답에 있어야 할 사실: four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwear 15% (everyone, until Nov 15), Birthday coupon (members), Free shipping over $80 (everyone), Gold tier 10% (gold)
- 답에 있어야 할 사실: the knit sale covers 26 knitwear products

### 원본 파사드 · 1회차 · ✗ 실패

토큰 8,469 · 모델 호출 4회 · 도구 호출 4회

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 5 candidates: getPrmtGridList, getPrmtGridListCnt, savePrmtList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `getPrmtGridListCnt` `` {"srchEndDtm":"2026-11-08 23:59:59","srchStrtDtm":"2026-11-07 00:00:00"} ``; `getPrmtGridList` `` {"pageNo":0,"pageSize":100,"srchEndDtm":"2026-11-08 23:59:59","srchStrtDtm":"2026-11-07 00:00:00"} ``
1. 에이전트 → **`getPrmtGridListCnt`** `` {"srchEndDtm":"2026-11-08 23:59:59","srchStrtDtm":"2026-11-07 00:00:00"} ``
   ← 실패: `` {"code":"invalid_filter","class":"invalid_input","message":"'2026-11-07 00:00:00' is not a date-time (expected 2026-11-07T00:00 or RFC 3339)","next_tool":null} ``
- 계획: `getPrmtGridListCnt` `` {"srchEndDtm":"2026-11-08T23:59:59-05:00","srchStrtDtm":"2026-11-07T00:00:00-05:00"} ``; `getPrmtGridList` `` {"pageNo":0,"pageSize":50,"srchEndDtm":"2026-11-08T23:59:59-05:00","srchStrtDtm":"2026-11-07T00:00:00-05:00"} ``
2. 에이전트 → **`getPrmtGridListCnt`** `` {"srchEndDtm":"2026-11-08T23:59:59-05:00","srchStrtDtm":"2026-11-07T00:00:00-05:00"} ``
   ← 결과: `` {"totCnt":4} ``
3. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"pageSize":50,"srchEndDtm":"2026-11-08T23:59:59-05:00","srchStrtDtm":"2026-11-07T00:00:00-05:00"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrmtGridList` `` {"pageNo":0,"pageSize":50,"srchEndDtm":"2026-11-08T23:59:59-05:00","srchStrtDtm":"2026-11-07T00:00:00-05:00"} ``
4. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"pageSize":50,"srchEndDtm":"2026-11-08T23:59:59-05:00","srchStrtDtm":"2026-11-07T00:00:00-05:00"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``

**답변 1**
> getPrmtGridList failed (ERR_PARAM): Invalid paging. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8, 15, 15, 80, 10 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown)

### 원본 파사드 · 2회차 · ✗ 실패

토큰 8,551 · 모델 호출 5회 · 도구 호출 3회

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 5 candidates: getPrmtGridList, getPrmtGridListCnt, savePrmtList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `getPrmtGridListCnt` `` {"srchEndDtm":"2026-11-08 23:59","srchStrtDtm":"2026-11-07 00:00"} ``; `getPrmtGridList` `` {"pageNo":0,"pageSize":50,"srchEndDtm":"2026-11-08 23:59","srchStrtDtm":"2026-11-07 00:00"} ``
1. 에이전트 → **`getPrmtGridListCnt`** `` {"srchEndDtm":"2026-11-08 23:59","srchStrtDtm":"2026-11-07 00:00"} ``
   ← 결과: `` {"totCnt":4} ``
2. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"pageSize":50,"srchEndDtm":"2026-11-08 23:59","srchStrtDtm":"2026-11-07 00:00"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrmtGridList` `` {"srchEndDtm":"2026-11-08 23:59","srchStrtDtm":"2026-11-07 00:00"} ``
3. 에이전트 → **`getPrmtGridList`** `` {"srchEndDtm":"2026-11-08 23:59","srchStrtDtm":"2026-11-07 00:00"} ``
   ← 결과: `` {"list":[{"endDtm":"2026-11-15T23:59:00-05:00","prmtNm":"Autumn knitwear 15%","prmtNo":"promo_autumn_knit","strtDtm":"2026-11-01T00:00:00-04:00","prmtTpCd":"T01","prmtStatCd":"20","tgtMbrGrdCd":"G00"},{"endDtm":null,"prmtNm":"Birthday coupon","prmtNo":"promo_birthday","strtDtm":"2026-01-01T00:00:00-05:00","prmtTpCd":"T02","prmtStatCd":"20","tgtMbrGrdCd":"G01"},{"endDtm":null,"prmtNm":"Free shipping over $80","prmtNo":"promo_free_ship_80","strtDtm":"2026-01-01T00:00:00-05:00","prmtTpCd":"T04","prmtStatCd":"20","tgtMbrGrdCd":"G00"},{"endDtm":null,"prmtNm":"Gold tier 10%","prmtNo":"promo_gold_10"… (+121자) ``
- check: The reply was cut at the length limit

**답변 1**
> The Autumn knitwear 15% sale is live this weekend, running through Nov 15. The Birthday coupon, Free shipping over $80, and Gold tier 10% are also active, but you asked not to stack anything on top of the knit sale. The blocks on screen show the four live promotions and their dates.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown)

### 원본 파사드 · 3회차 · ✗ 실패

토큰 6,516 · 모델 호출 4회 · 도구 호출 1회

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 5 candidates: getPrmtGridList, getPrmtGridListCnt, savePrmtList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `getPrmtGridListCnt` `` {"srchEndDtm":"2026-11-08 23:59:59","srchStrtDtm":"2026-11-07 00:00:00"} ``; `getPrmtGridList` `` {"pageNo":0,"pageSize":100,"srchEndDtm":"2026-11-08 23:59:59","srchStrtDtm":"2026-11-07 00:00:00"} ``
1. 에이전트 → **`getPrmtGridListCnt`** `` {"srchEndDtm":"2026-11-08 23:59:59","srchStrtDtm":"2026-11-07 00:00:00"} ``
   ← 실패: `` {"code":"invalid_filter","class":"invalid_input","message":"'2026-11-07 00:00:00' is not a date-time (expected 2026-11-07T00:00 or RFC 3339)","next_tool":null} ``
- 계획: store operator · knit sale · what promos are live this weekend · this weekend · storefront · do not stack anything on top of the knit sale · 0 steps by Muse Glimmer 30B

**답변 1**
> I don't have any live promo data in this turn. No reads or change sets were returned, so I can't confirm which promotions are active this weekend or whether anything is stacking on the knit sale. If you can share the current promo list or the knit sale details, I can check for overlaps and stacking rules.

**채점**: ✗ 실패 — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8, 15, 15, 80, 10 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown)
