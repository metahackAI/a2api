# mk-whats-running-this-weekend — luna-design-raw

[← 실행 묶음](README.md)

**과업**

> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 답에 있어야 할 사실: four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwear 15% (everyone, until Nov 15), Birthday coupon (members), Free shipping over $80 (everyone), Gold tier 10% (gold)
- 답에 있어야 할 사실: the knit sale covers 26 knitwear products

### GPT-6-Luna · 원본 파사드 · 1회차 · ✗ 실패

토큰 28,973 · 모델 호출 4회 · 도구 호출 3회

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 5 candidates: getPrmtGridList, getPrmtGridListCnt, savePrmtList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `getPrmtGridList` `` {"pageNo":0,"pageSize":100,"srchEndDtm":"2026-11-08 23:59:00","srchStrtDtm":"2026-11-07 00:00:00"} ``
1. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"pageSize":100,"srchEndDtm":"2026-11-08 23:59:00","srchStrtDtm":"2026-11-07 00:00:00"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrmtGridList` `` {"pageNo":0,"pageSize":100,"srchEndDtm":"2026-11-08 23:59:00","srchStrtDtm":"2026-11-06 00:00:00"} ``
2. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"pageSize":100,"srchEndDtm":"2026-11-08 23:59:00","srchStrtDtm":"2026-11-06 00:00:00"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrmtGridList` `` {"pageNo":0,"pageSize":50,"srchEndDtm":"2026-11-08 23:59","srchStrtDtm":"2026-11-07 00:00"} ``
3. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"pageSize":50,"srchEndDtm":"2026-11-08 23:59","srchStrtDtm":"2026-11-07 00:00"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``

**답변 1**
> getPrmtGridList failed (ERR_PARAM): Invalid paging. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8, 15, 15, 80, 10 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown)

### GPT-6-Luna · 원본 파사드 · 2회차 · ✗ 실패

토큰 29,014 · 모델 호출 4회 · 도구 호출 3회

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 5 candidates: getPrmtGridList, getPrmtGridListCnt, savePrmtList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `getPrmtGridList` `` {"pageNo":0,"pageSize":100,"srchEndDtm":"2026-11-08 23:59","srchStrtDtm":"2026-11-07 00:00"} ``
1. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"pageSize":100,"srchEndDtm":"2026-11-08 23:59","srchStrtDtm":"2026-11-07 00:00"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrmtGridList` `` {"pageNo":0,"pageSize":20,"srchEndDtm":"2026-11-08 23:59","srchStrtDtm":"2026-11-06 00:00"} ``
2. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"pageSize":20,"srchEndDtm":"2026-11-08 23:59","srchStrtDtm":"2026-11-06 00:00"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrmtGridList` `` {"pageNo":0,"pageSize":20,"srchEndDtm":"2026-11-08 23:59","srchStrtDtm":"2026-11-07 00:00"} ``
3. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"pageSize":20,"srchEndDtm":"2026-11-08 23:59","srchStrtDtm":"2026-11-07 00:00"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``

**답변 1**
> getPrmtGridList failed (ERR_PARAM): Invalid paging. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8, 15, 15, 80, 10 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown)

### GPT-6-Luna · 원본 파사드 · 3회차 · ✗ 실패

토큰 26,993 · 모델 호출 4회 · 도구 호출 2회

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 5 candidates: getPrmtGridList, getPrmtGridListCnt, savePrmtList, getPrmtTgtMbrList, getPrmtTgtMbrListCnt
- 계획: `getPrmtGridList` `` {"pageNo":0,"pageSize":100,"srchEndDtm":"2026-11-08 23:59","srchStrtDtm":"2026-11-07 00:00"} ``
1. 에이전트 → **`getPrmtGridList`** `` {"pageNo":0,"pageSize":100,"srchEndDtm":"2026-11-08 23:59","srchStrtDtm":"2026-11-07 00:00"} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrmtGridList` `` {"pageNo":1,"pageSize":20,"srchEndDtm":"2026-11-08 23:59","srchStrtDtm":"2026-11-06 00:00"} ``
2. 에이전트 → **`getPrmtGridList`** `` {"pageNo":1,"pageSize":20,"srchEndDtm":"2026-11-08 23:59","srchStrtDtm":"2026-11-06 00:00"} ``
   ← 결과: `` {"list":[{"endDtm":"2026-11-15T23:59:00-05:00","prmtNm":"Autumn knitwear 15%","prmtNo":"promo_autumn_knit","strtDtm":"2026-11-01T00:00:00-04:00","prmtTpCd":"T01","prmtStatCd":"20","tgtMbrGrdCd":"G00"},{"endDtm":null,"prmtNm":"Birthday coupon","prmtNo":"promo_birthday","strtDtm":"2026-01-01T00:00:00-05:00","prmtTpCd":"T02","prmtStatCd":"20","tgtMbrGrdCd":"G01"},{"endDtm":null,"prmtNm":"Free shipping over $80","prmtNo":"promo_free_ship_80","strtDtm":"2026-01-01T00:00:00-05:00","prmtTpCd":"T04","prmtStatCd":"20","tgtMbrGrdCd":"G00"},{"endDtm":null,"prmtNm":"Gold tier 10%","prmtNo":"promo_gold_10"… (+121자) ``

**답변 1**
> The Autumn knitwear 15% sale is live this weekend, along with the Birthday coupon, free shipping over $80, and Gold tier 10%. The birthday and Gold offers are tier-specific; there’s no indication here whether they can be combined with the knit sale.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown)
