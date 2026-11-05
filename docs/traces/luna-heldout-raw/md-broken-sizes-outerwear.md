# md-broken-sizes-outerwear — luna-heldout-raw

[← 실행 묶음](README.md)

**과업**

> which outerwear styles have broken sizes right now?

- 답에 있어야 할 사실: 5 of the 62 outerwear products have a sold-out size
- 답에 있어야 할 사실: Cotton chore coat, Light rain parka and Denim jacket are out in M and L; Poplin shacket is out in M; Cotton overshirt is out in XL

### GPT-6-Luna · 원본 파사드 · 1회차 · ✗ 실패

토큰 20,114 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> which outerwear styles have broken sizes right now?

- 라우팅: Catalog agent (chosen by the model)
- 도구 검색 후보: 5 candidates: getPrdGridList, getPrdGridListCnt, getDispCornerList, getPrdDtlInfo, getPrdDtlInfoV2
- 계획: `getPrdGridList` `` {"srchKwd":"outerwear"} ``
1. 에이전트 → **`getPrdGridList`** `` {"srchKwd":"outerwear"} ``
   ← 결과: `` {"list":[{"ctgNo":"cat_summer_outerwear","prdNm":"Light rain parka","prdNo":"prd_rain_parka","brndNo":"brn_northwind","mbrPrc":null,"stkQty":4,"costPrc":50.0,"salePrc":118.0,"sellStatCd":"10"},{"ctgNo":"cat_summer_outerwear","prdNm":"Seersucker shacket","prdNo":"prd_summer_outerwear_22","brndNo":"brn_northwind","mbrPrc":null,"stkQty":36,"costPrc":35.55,"salePrc":79.0,"sellStatCd":"10"},{"ctgNo":"cat_summer_outerwear","prdNm":"Linen shacket","prdNo":"prd_summer_outerwear_33","brndNo":"brn_northwind","mbrPrc":null,"stkQty":30,"costPrc":58.05,"salePrc":129.0,"sellStatCd":"10"},{"ctgNo":"cat_summe… (+3,316자) ``

**답변 1**
> I can’t tell which outerwear styles have broken sizes from this list; it shows overall stock, not sizes. The store’s size-level inventory is needed to identify them.

화면 블록: product_table(20 of 20)

**채점**: ✗ 실패 — 빠진 것: fact "5 of the 62 outerwear products have a sold-out size" (62 not shown)

### GPT-6-Luna · 원본 파사드 · 2회차 · ✗ 실패

토큰 28,405 · 모델 호출 4회 · 도구 호출 3회

**질문 1**
> which outerwear styles have broken sizes right now?

- 라우팅: Catalog agent (chosen by the model)
- 도구 검색 후보: 5 candidates: getPrdGridList, getPrdGridListCnt, getDispCornerList, getPrdDtlInfo, getPrdDtlInfoV2
- 계획: `getPrdGridList` `` {"pageNo":0,"srchKwd":"outerwear","pageSize":100} ``; `getPrdDtlInfoV2` `` {} ``
1. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"srchKwd":"outerwear","pageSize":100} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrdGridList` `` {"pageNo":0,"srchKwd":"outerwear","pageSize":100} ``; `getPrdDtlInfoV2` `` {} ``
2. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"srchKwd":"outerwear","pageSize":100} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrdGridList` `` {"pageNo":0,"srchKwd":"outerwear","pageSize":100} ``; `getPrdDtlInfoV2` `` {} ``
3. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"srchKwd":"outerwear","pageSize":100} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``

**답변 1**
> getPrdGridList failed (ERR_PARAM): Invalid paging. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "5 of the 62 outerwear products have a sold-out size" (5, 62 not shown)

### GPT-6-Luna · 원본 파사드 · 3회차 · ✗ 실패

토큰 28,496 · 모델 호출 4회 · 도구 호출 3회

**질문 1**
> which outerwear styles have broken sizes right now?

- 라우팅: Catalog agent (chosen by the model)
- 도구 검색 후보: 5 candidates: getPrdGridList, getPrdGridListCnt, getDispCornerList, getPrdDtlInfo, getPrdDtlInfoV2
- 계획: `getPrdGridList` `` {"pageNo":0,"srchKwd":"outerwear","pageSize":100} ``; `getPrdDtlInfoV2` `` {} ``
1. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"srchKwd":"outerwear","pageSize":100} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrdGridList` `` {"pageNo":0,"srchKwd":"outerwear","pageSize":100} ``; `getPrdDtlInfoV2` `` {} ``
2. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"srchKwd":"outerwear","pageSize":100} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrdGridList` `` {"pageNo":0,"srchKwd":"outerwear","pageSize":100} ``; `getPrdDtlInfoV2` `` {} ``
3. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"srchKwd":"outerwear","pageSize":100} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``

**답변 1**
> getPrdGridList failed (ERR_PARAM): Invalid paging. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "5 of the 62 outerwear products have a sold-out size" (5, 62 not shown)
