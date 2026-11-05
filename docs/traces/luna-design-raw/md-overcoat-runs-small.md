# md-overcoat-runs-small — luna-design-raw

[← 실행 묶음](README.md)

**과업**

> people keep saying the wool overcoat runs small. is that actually true?

- 답에 있어야 할 사실: 41 reviews, average 4.6
- 답에 있어야 할 사실: 29 say true to size, 12 say a bit snug, none say it runs large
- 답에 있어야 할 사실: the most common phrase is 'size up for a hoodie' (9 mentions), so the snug votes come from layering

### GPT-6-Luna · 원본 파사드 · 1회차 · ✗ 실패

토큰 41,952 · 모델 호출 6회 · 도구 호출 4회

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

- 라우팅: Catalog agent (chosen by the model)
- 도구 검색 후보: 5 candidates: getDispCornerList, getPrdDtlInfo, getPrdDtlInfoV2, getPrdGridList, getPrdGridListCnt
- 계획: `getPrdGridList` `` {"pageNo":0,"srchKwd":"wool overcoat","pageSize":20} ``; `getPrdDtlInfoV2` `` {} ``
1. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"srchKwd":"wool overcoat","pageSize":20} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrdGridList` `` {"pageNo":0,"srchKwd":"wool overcoat","pageSize":20} ``; `getPrdDtlInfoV2` `` {} ``
2. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"srchKwd":"wool overcoat","pageSize":20} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getPrdGridList` `` {"pageNo":1,"srchKwd":"wool overcoat","pageSize":20} ``; `getPrdDtlInfoV2` `` {} ``
3. 에이전트 → **`getPrdGridList`** `` {"pageNo":1,"srchKwd":"wool overcoat","pageSize":20} ``
   ← 결과: `` {"list":[{"ctgNo":"cat_outerwear","prdNm":"Wool overcoat","prdNo":"prd_wool_overcoat","brndNo":"brn_northwind","mbrPrc":null,"stkQty":24,"costPrc":120.0,"salePrc":289.0,"sellStatCd":"10"},{"ctgNo":"cat_scarves","prdNm":"Wool stole","prdNo":"prd_scarves_04","brndNo":"brn_ridgeline","mbrPrc":null,"stkQty":23,"costPrc":24.46,"salePrc":59.0,"sellStatCd":"10"},{"ctgNo":"cat_pants","prdNm":"Wool drawstring pants","prdNo":"prd_pants_22","brndNo":"brn_northwind","mbrPrc":null,"stkQty":89,"costPrc":74.16,"salePrc":149.0,"sellStatCd":"10"},{"ctgNo":"cat_outerwear","prdNm":"Wool liner jacket","prdNo":"pr… (+3,001자) ``
4. 에이전트 → **`getPrdDtlInfoV2`** `` {"prdNo":"prd_wool_overcoat"} ``
   ← 결과: `` {"ctgNo":"cat_outerwear","prdNm":"Wool overcoat","prdNo":"prd_wool_overcoat","brndNo":"brn_northwind","mbrPrc":null,"stkQty":24,"costPrc":120.0,"optList":[{"optNo":"var_wool_overcoat_s_charcoal","stkQty":5,"optVal1":"Charcoal","optVal2":"S","sellStatCd":"10"},{"optNo":"var_wool_overcoat_m_charcoal","stkQty":7,"optVal1":"Charcoal","optVal2":"M","sellStatCd":"10"},{"optNo":"var_wool_overcoat_l_charcoal","stkQty":8,"optVal1":"Charcoal","optVal2":"L","sellStatCd":"10"},{"optNo":"var_wool_overcoat_xl_charcoal","stkQty":4,"optVal1":"Charcoal","optVal2":"XL","sellStatCd":"10"}],"salePrc":289.0,"attrL… (+118자) ``

**답변 1**
> I can’t tell from the results shown: they include the wool overcoat’s sizes and stock, but no customer reviews or sizing feedback. There’s nothing here to confirm whether it runs small.

화면 블록: product_table(20 of 20)

**채점**: ✗ 실패 — 빠진 것: fact "41 reviews, average 4.6" (41, 4.6 not shown); fact "the most common phrase is 'size up for a hoodie' (9 mentions" (9 not shown)

### GPT-6-Luna · 원본 파사드 · 2회차 · ✗ 실패

토큰 26,704 · 모델 호출 4회 · 도구 호출 2회

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

- 라우팅: Catalog agent (chosen by the model)
- 도구 검색 후보: 5 candidates: getDispCornerList, getPrdDtlInfo, getPrdDtlInfoV2, getPrdGridList, getPrdGridListCnt
- 계획: `getPrdGridList` `` {"srchKwd":"wool overcoat"} ``; `getPrdDtlInfoV2` `` {} ``
1. 에이전트 → **`getPrdGridList`** `` {"srchKwd":"wool overcoat"} ``
   ← 결과: `` {"list":[{"ctgNo":"cat_outerwear","prdNm":"Wool overcoat","prdNo":"prd_wool_overcoat","brndNo":"brn_northwind","mbrPrc":null,"stkQty":24,"costPrc":120.0,"salePrc":289.0,"sellStatCd":"10"},{"ctgNo":"cat_scarves","prdNm":"Wool stole","prdNo":"prd_scarves_04","brndNo":"brn_ridgeline","mbrPrc":null,"stkQty":23,"costPrc":24.46,"salePrc":59.0,"sellStatCd":"10"},{"ctgNo":"cat_pants","prdNm":"Wool drawstring pants","prdNo":"prd_pants_22","brndNo":"brn_northwind","mbrPrc":null,"stkQty":89,"costPrc":74.16,"salePrc":149.0,"sellStatCd":"10"},{"ctgNo":"cat_outerwear","prdNm":"Wool liner jacket","prdNo":"pr… (+3,001자) ``
2. 에이전트 → **`getPrdDtlInfoV2`** `` {"prdNo":"prd_wool_overcoat"} ``
   ← 결과: `` {"ctgNo":"cat_outerwear","prdNm":"Wool overcoat","prdNo":"prd_wool_overcoat","brndNo":"brn_northwind","mbrPrc":null,"stkQty":24,"costPrc":120.0,"optList":[{"optNo":"var_wool_overcoat_s_charcoal","stkQty":5,"optVal1":"Charcoal","optVal2":"S","sellStatCd":"10"},{"optNo":"var_wool_overcoat_m_charcoal","stkQty":7,"optVal1":"Charcoal","optVal2":"M","sellStatCd":"10"},{"optNo":"var_wool_overcoat_l_charcoal","stkQty":8,"optVal1":"Charcoal","optVal2":"L","sellStatCd":"10"},{"optNo":"var_wool_overcoat_xl_charcoal","stkQty":4,"optVal1":"Charcoal","optVal2":"XL","sellStatCd":"10"}],"salePrc":289.0,"attrL… (+118자) ``

**답변 1**
> The Wool overcoat has 24 units in stock across sizes S through XL. These results don’t include customer reviews or fit feedback, so they don’t show whether it runs small.

화면 블록: product_table(20 of 20)

**채점**: ✗ 실패 — 빠진 것: fact "41 reviews, average 4.6" (41, 4.6 not shown); fact "the most common phrase is 'size up for a hoodie' (9 mentions" (9 not shown)

### GPT-6-Luna · 원본 파사드 · 3회차 · ✗ 실패

토큰 26,648 · 모델 호출 4회 · 도구 호출 2회

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

- 라우팅: Catalog agent (chosen by the model)
- 도구 검색 후보: 5 candidates: getDispCornerList, getPrdDtlInfo, getPrdDtlInfoV2, getPrdGridList, getPrdGridListCnt
- 계획: `getPrdGridList` `` {"srchKwd":"wool overcoat"} ``; `getPrdDtlInfoV2` `` {} ``
1. 에이전트 → **`getPrdGridList`** `` {"srchKwd":"wool overcoat"} ``
   ← 결과: `` {"list":[{"ctgNo":"cat_outerwear","prdNm":"Wool overcoat","prdNo":"prd_wool_overcoat","brndNo":"brn_northwind","mbrPrc":null,"stkQty":24,"costPrc":120.0,"salePrc":289.0,"sellStatCd":"10"},{"ctgNo":"cat_scarves","prdNm":"Wool stole","prdNo":"prd_scarves_04","brndNo":"brn_ridgeline","mbrPrc":null,"stkQty":23,"costPrc":24.46,"salePrc":59.0,"sellStatCd":"10"},{"ctgNo":"cat_pants","prdNm":"Wool drawstring pants","prdNo":"prd_pants_22","brndNo":"brn_northwind","mbrPrc":null,"stkQty":89,"costPrc":74.16,"salePrc":149.0,"sellStatCd":"10"},{"ctgNo":"cat_outerwear","prdNm":"Wool liner jacket","prdNo":"pr… (+3,001자) ``
2. 에이전트 → **`getPrdDtlInfoV2`** `` {"prdNo":"prd_wool_overcoat"} ``
   ← 결과: `` {"ctgNo":"cat_outerwear","prdNm":"Wool overcoat","prdNo":"prd_wool_overcoat","brndNo":"brn_northwind","mbrPrc":null,"stkQty":24,"costPrc":120.0,"optList":[{"optNo":"var_wool_overcoat_s_charcoal","stkQty":5,"optVal1":"Charcoal","optVal2":"S","sellStatCd":"10"},{"optNo":"var_wool_overcoat_m_charcoal","stkQty":7,"optVal1":"Charcoal","optVal2":"M","sellStatCd":"10"},{"optNo":"var_wool_overcoat_l_charcoal","stkQty":8,"optVal1":"Charcoal","optVal2":"L","sellStatCd":"10"},{"optNo":"var_wool_overcoat_xl_charcoal","stkQty":4,"optVal1":"Charcoal","optVal2":"XL","sellStatCd":"10"}],"salePrc":289.0,"attrL… (+118자) ``

**답변 1**
> There’s no customer feedback in the results to confirm whether the Wool overcoat runs small. The product details show stock by size, but not what customers say about fit.

화면 블록: product_table(20 of 20)

**채점**: ✗ 실패 — 빠진 것: fact "41 reviews, average 4.6" (41, 4.6 not shown); fact "the most common phrase is 'size up for a hoodie' (9 mentions" (9 not shown)
