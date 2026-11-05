# md-how-many-left — luna-heldout-raw

[← 실행 묶음](README.md)

**과업**

> How many Light rain parka remain in my inventory?

- 답에 있어야 할 사실: 4 in total: S 2, M 0, L 0, XL 2 (all Stone)
- 답에 있어야 할 사실: S and XL are at their safety stock of 2, so the parka is effectively sold out for new sales planning

### GPT-6-Luna · 원본 파사드 · 1회차 · ✗ 실패

토큰 21,549 · 모델 호출 3회 · 도구 호출 2회

**질문 1**
> How many Light rain parka remain in my inventory?

- 라우팅: Catalog agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: getDispCornerList, getPrdDtlInfo, getPrdDtlInfoV2, getPrdGridList, getPrdGridListCnt
- 계획: `getPrdGridList` `` {"srchKwd":"Light rain parka"} ``; `getPrdDtlInfoV2` `` {} ``
1. 에이전트 → **`getPrdGridList`** `` {"srchKwd":"Light rain parka"} ``
   ← 결과: `` {"list":[{"ctgNo":"cat_summer_outerwear","prdNm":"Light rain parka","prdNo":"prd_rain_parka","brndNo":"brn_northwind","mbrPrc":null,"stkQty":4,"costPrc":50.0,"salePrc":118.0,"sellStatCd":"10"},{"ctgNo":"cat_outerwear","prdNm":"Recycled nylon trench coat","prdNo":"prd_outerwear_06","brndNo":"brn_northwind","mbrPrc":null,"stkQty":69,"costPrc":115.38,"salePrc":259.0,"sellStatCd":"10"},{"ctgNo":"cat_outerwear","prdNm":"Waxed cotton duffle coat","prdNo":"prd_outerwear_01","brndNo":"brn_ridgeline","mbrPrc":null,"stkQty":24,"costPrc":134.5,"salePrc":289.0,"sellStatCd":"10"},{"ctgNo":"cat_outerwear","… (+3,185자) ``
2. 에이전트 → **`getPrdDtlInfoV2`** `` {"prdNo":"prd_rain_parka"} ``
   ← 결과: `` {"ctgNo":"cat_summer_outerwear","prdNm":"Light rain parka","prdNo":"prd_rain_parka","brndNo":"brn_northwind","mbrPrc":null,"stkQty":4,"costPrc":50.0,"optList":[{"optNo":"var_rain_parka_s_stone","stkQty":2,"optVal1":"Stone","optVal2":"S","sellStatCd":"10"},{"optNo":"var_rain_parka_m_stone","stkQty":0,"optVal1":"Stone","optVal2":"M","sellStatCd":"20"},{"optNo":"var_rain_parka_l_stone","stkQty":0,"optVal1":"Stone","optVal2":"L","sellStatCd":"20"},{"optNo":"var_rain_parka_xl_stone","stkQty":2,"optVal1":"Stone","optVal2":"XL","sellStatCd":"10"}],"salePrc":118.0,"attrList":[{"attrNm":"material","uni… (+358자) ``

**답변 1**
> There are 4 Light rain parkas in inventory: 2 in size S and 2 in size XL. Sizes M and L are out of stock.

화면 블록: product_table(20 of 20)

**채점**: ✗ 실패 — 빠진 것: fact "4 in total: S 2, M 0, L 0, XL 2 (all Stone)" (0, 0 not shown)

### GPT-6-Luna · 원본 파사드 · 2회차 · ✗ 실패

토큰 21,625 · 모델 호출 3회 · 도구 호출 2회

**질문 1**
> How many Light rain parka remain in my inventory?

- 라우팅: Catalog agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: getDispCornerList, getPrdDtlInfo, getPrdDtlInfoV2, getPrdGridList, getPrdGridListCnt
- 계획: `getPrdGridList` `` {"srchKwd":"Light rain parka"} ``; `getPrdDtlInfoV2` `` {} ``
1. 에이전트 → **`getPrdGridList`** `` {"srchKwd":"Light rain parka"} ``
   ← 결과: `` {"list":[{"ctgNo":"cat_summer_outerwear","prdNm":"Light rain parka","prdNo":"prd_rain_parka","brndNo":"brn_northwind","mbrPrc":null,"stkQty":4,"costPrc":50.0,"salePrc":118.0,"sellStatCd":"10"},{"ctgNo":"cat_outerwear","prdNm":"Recycled nylon trench coat","prdNo":"prd_outerwear_06","brndNo":"brn_northwind","mbrPrc":null,"stkQty":69,"costPrc":115.38,"salePrc":259.0,"sellStatCd":"10"},{"ctgNo":"cat_outerwear","prdNm":"Waxed cotton duffle coat","prdNo":"prd_outerwear_01","brndNo":"brn_ridgeline","mbrPrc":null,"stkQty":24,"costPrc":134.5,"salePrc":289.0,"sellStatCd":"10"},{"ctgNo":"cat_outerwear","… (+3,185자) ``
2. 에이전트 → **`getPrdDtlInfoV2`** `` {"prdNo":"prd_rain_parka"} ``
   ← 결과: `` {"ctgNo":"cat_summer_outerwear","prdNm":"Light rain parka","prdNo":"prd_rain_parka","brndNo":"brn_northwind","mbrPrc":null,"stkQty":4,"costPrc":50.0,"optList":[{"optNo":"var_rain_parka_s_stone","stkQty":2,"optVal1":"Stone","optVal2":"S","sellStatCd":"10"},{"optNo":"var_rain_parka_m_stone","stkQty":0,"optVal1":"Stone","optVal2":"M","sellStatCd":"20"},{"optNo":"var_rain_parka_l_stone","stkQty":0,"optVal1":"Stone","optVal2":"L","sellStatCd":"20"},{"optNo":"var_rain_parka_xl_stone","stkQty":2,"optVal1":"Stone","optVal2":"XL","sellStatCd":"10"}],"salePrc":118.0,"attrList":[{"attrNm":"material","uni… (+358자) ``

**답변 1**
> The Light rain parka has 4 units in stock: 2 in Stone S and 2 in Stone XL. Stone M and L are out of stock.

화면 블록: product_table(20 of 20)

**채점**: ✗ 실패 — 빠진 것: fact "4 in total: S 2, M 0, L 0, XL 2 (all Stone)" (0, 0 not shown)

### GPT-6-Luna · 원본 파사드 · 3회차 · ✗ 실패

토큰 21,349 · 모델 호출 3회 · 도구 호출 2회

**질문 1**
> How many Light rain parka remain in my inventory?

- 라우팅: Catalog agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: getDispCornerList, getPrdDtlInfo, getPrdDtlInfoV2, getPrdGridList, getPrdGridListCnt
- 계획: `getPrdGridList` `` {"srchKwd":"Light rain parka"} ``; `getPrdDtlInfo` `` {} ``
1. 에이전트 → **`getPrdGridList`** `` {"srchKwd":"Light rain parka"} ``
   ← 결과: `` {"list":[{"ctgNo":"cat_summer_outerwear","prdNm":"Light rain parka","prdNo":"prd_rain_parka","brndNo":"brn_northwind","mbrPrc":null,"stkQty":4,"costPrc":50.0,"salePrc":118.0,"sellStatCd":"10"},{"ctgNo":"cat_outerwear","prdNm":"Recycled nylon trench coat","prdNo":"prd_outerwear_06","brndNo":"brn_northwind","mbrPrc":null,"stkQty":69,"costPrc":115.38,"salePrc":259.0,"sellStatCd":"10"},{"ctgNo":"cat_outerwear","prdNm":"Waxed cotton duffle coat","prdNo":"prd_outerwear_01","brndNo":"brn_ridgeline","mbrPrc":null,"stkQty":24,"costPrc":134.5,"salePrc":289.0,"sellStatCd":"10"},{"ctgNo":"cat_outerwear","… (+3,185자) ``
2. 에이전트 → **`getPrdDtlInfo`** `` {"prdNo":"prd_rain_parka"} ``
   ← 결과: `` {"ctgNo":"cat_summer_outerwear","prdNm":"Light rain parka","prdNo":"prd_rain_parka","brndNo":"brn_northwind","mbrPrc":null,"stkQty":4,"costPrc":50.0,"salePrc":118.0,"prdStatCd":"active","sellStatCd":"10"} ``

**답변 1**
> There are 4 Light rain parkas in your inventory.

화면 블록: product_table(20 of 20)

**채점**: ✗ 실패 — 빠진 것: fact "4 in total: S 2, M 0, L 0, XL 2 (all Stone)" (2, 0, 0, 2 not shown); fact "S and XL are at their safety stock of 2, so the parka is eff" (2 not shown)
