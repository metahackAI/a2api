# md-overcoat-runs-small — ours-design-3

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `92408c7`

**과업**

> people keep saying the wool overcoat runs small. is that actually true?

- 필요한 도구: `get_review_summary`
- 허용 도구: `search_products`, `list_reviews`, `get_product_measurements`
- 답에 있어야 할 사실: 41 reviews, average 4.6
- 답에 있어야 할 사실: 29 say true to size, 12 say a bit snug, none say it runs large
- 답에 있어야 할 사실: the most common phrase is 'size up for a hoodie' (9 mentions), so the snug votes come from layering

### facade-all · 1회차 · ✗ 실패

토큰 72,976 · 83.803초 · 모델 호출 10회 · 도구 호출 9회 · 첫 요청 프롬프트 4,652토큰

준비: 전략 `None`, 함수 19개

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

1. 모델 → **`getPrdGridList`** `` {"srchKwd":"wool overcoat","pageNo":0,"pageSize":10} ``
   ← 결과 121B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null}}} ``
2. 모델 → **`getPrdGridList`** `` {"srchKwd":"wool overcoat","pageNo":1,"pageSize":10} ``
   ← 결과 1,834B: `` {"status":200,"body":{"list":[{"prdNo":"prd_wool_overcoat","prdNm":"Wool overcoat","ctgNo":"cat_outerwear","brndNo":"brn_northwind","salePrc":289.0,"mbrPrc":null,"stkQty":24,"sellStatCd":"10","costPrc":120.0},{"prdNo":"prd_scarves_04","prdNm":"Wool stole","ctgNo":"cat_scarves","brndNo":"brn_ridgeline","salePrc":59.0,"mbrPrc":null,"stkQty":23,"sellStatCd":"10","costPrc":24.46},{"prdNo":"prd_pants_22","prdNm":"Wool drawstring pants","ctgNo":"cat_pants","brndNo":"brn_northwind","salePrc":149.0,"mbrPrc":null,"stkQty":89,"sellStatCd":"10","costPrc":74.16},{"prdNo":"prd_outerwear_12","prdNm":"Wool l… (+900자) ``
3. 모델 → **`getPrdDtlInfoV2`** `` {"prdNo":"prd_wool_overcoat"} ``
   ← 결과 740B: `` {"status":200,"body":{"prdNo":"prd_wool_overcoat","prdNm":"Wool overcoat","ctgNo":"cat_outerwear","brndNo":"brn_northwind","salePrc":289.0,"mbrPrc":null,"stkQty":24,"sellStatCd":"10","costPrc":120.0,"prdStatCd":"active","optList":[{"optNo":"var_wool_overcoat_s_charcoal","optVal1":"Charcoal","optVal2":"S","stkQty":5,"sellStatCd":"10"},{"optNo":"var_wool_overcoat_m_charcoal","optVal1":"Charcoal","optVal2":"M","stkQty":7,"sellStatCd":"10"},{"optNo":"var_wool_overcoat_l_charcoal","optVal1":"Charcoal","optVal2":"L","stkQty":8,"sellStatCd":"10"},{"optNo":"var_wool_overcoat_xl_charcoal","optVal1":"Ch… (+140자) ``
4. 모델 → **`getClmGridList`** `` {"pageNo":1,"pageSize":10} ``
   ← 결과 2,895B: `` {"status":200,"body":{"list":[{"clmNo":"clm_20333","ordNo":"ord_20333","mbrNo":"cus_priya","prdNm":"Wool overcoat","clmQty":1,"clmAmt":289.0,"clmRsnCd":"11","clmRsnCntt":"Too big in the shoulders.","atchFileCnt":0,"dlvCmplDt":"2026-10-12","clmReqDtm":"2026-11-04T09:12:00-05:00","clmStatCd":"R10"},{"clmNo":"clm_20341","ordNo":"ord_20341","mbrNo":"cus_marcus","prdNm":"Leather chelsea boots","clmQty":1,"clmAmt":312.0,"clmRsnCd":"01","clmRsnCntt":"Stitching came loose on the left boot.","atchFileCnt":1,"dlvCmplDt":"2026-10-14","clmReqDtm":"2026-11-04T13:40:00-05:00","clmStatCd":"R10"},{"clmNo":"cl… (+900자) ``
5. 모델 → **`getClmGridList`** `` {"pageNo":2,"pageSize":10} ``
   ← 결과 652B: `` {"status":200,"body":{"list":[{"clmNo":"clm_20409","ordNo":"ord_20409","mbrNo":"cus_grace","prdNm":"Wool overcoat","clmQty":1,"clmAmt":289.0,"clmRsnCd":"02","clmRsnCntt":"The box was crushed and the coat has a tear.","atchFileCnt":0,"dlvCmplDt":"2026-10-31","clmReqDtm":"2026-11-06T07:30:00-05:00","clmStatCd":"R10"},{"clmNo":"clm_20402","ordNo":"ord_20402","mbrNo":"cus_alex","prdNm":"Leather chelsea boots","clmQty":1,"clmAmt":312.0,"clmRsnCd":"01","clmRsnCntt":"The sole on my chelsea boots is coming apart after a week.","atchFileCnt":2,"dlvCmplDt":"2026-10-31","clmReqDtm":"2026-11-06T09:52:00-0… (+52자) ``
6. 모델 → **`getClmGridList`** `` {"pageNo":3,"pageSize":10} ``
   ← 결과 58B: `` {"status":200,"body":{"list":[],"pageNo":3,"pageSize":10}} ``
7. 모델 → **`getClmGridList`** `` {"clmRsnCd":11,"pageNo":1,"pageSize":10} ``
   ← 결과 169B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid parameter: invalid type: number, expected string or map","next_tool":null}}} ``
8. 모델 → **`getClmGridList`** `` {"clmRsnCd":11,"pageNo":1,"pageSize":10} ``
   ← 결과 169B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid parameter: invalid type: number, expected string or map","next_tool":null}}} ``
9. 모델 → **`getClmGridListCnt`** `` {"pageNo":1,"pageSize":10} ``
   ← 결과 35B: `` {"status":200,"body":{"totCnt":12}} ``

**답변 1**
> Based on the current claim records for the Wool overcoat `prd_wool_overcoat` – $289, Charcoal S/M/L/XL, 70% wool / 30% polyamide – there is no support for “runs small”.
>
> Claims in the system, total 12 open claims:
>
> * `clm_20333` – Wool overcoat – clmRsnCd 11 – “Too big in the shoulders.” – $289
> * `clm_20431` – Wool overcoat – clmRsnCd 03 – “The color is much darker than the photos.” – $289
> * `clm_20409` – Wool overcoat – clmRsnCd 02 – “The box was crushed and the coat has a tear.” – $289
>
> That is 3 of the 12 claims for the SKU, and none of them cite a small fit. The size-related claim for the overcoat is the opposite of the rumor: too big in the shoulders.
>
> The other size/fit claims in the current set are for other SKUs:
> * `clm_20352` Linen blend field jacket – “Both jackets are tight in the chest.” – clmRsnCd 11
> * `clm_20418` Linen blend field jacket – “Both are too small in the shoulders.” – clmRsnCd 11
>
> No claim for the Wool overcoat reports it running small.

**채점**: ✗ 실패 — 빠진 것: fact "41 reviews, average 4.6" (41, 4.6 not shown); fact "29 say true to size, 12 say a bit snug, none say it runs lar" (29 not shown); fact "the most common phrase is 'size up for a hoodie' (9 mentions" (9 not shown)

### acom-all · 1회차 · E CONTEXT_OVERFLOW

토큰 0 · 0.317초 · 모델 호출 0회 · 도구 호출 0회

준비: 전략 `None`, 함수 253개

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?


_(CONTEXT_OVERFLOW로 중단)_

**채점**: E CONTEXT_OVERFLOW — 빠진 것: tool get_review_summary; fact "41 reviews, average 4.6" (41, 4.6 not shown); fact "29 say true to size, 12 say a bit snug, none say it runs lar" (29, 12 not shown); fact "the most common phrase is 'size up for a hoodie' (9 mentions" (9 not shown); HOST:CONTEXT_OVERFLOW
(도구 정밀도 —, 재현율 0.00)

### a2api-acom · 1회차 · ✓ 통과

토큰 9,740 · 12.308초 · 모델 호출 2회 · 도구 호출 1회 · 첫 요청 프롬프트 4,360토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

1. 모델 → **`acom_get_review_summary`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 940B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":null},"review_count":41,"rating_value":4.6,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":29},{"fit":"runs_small","label":"A bit snug","count":12},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[{"text":"size up for a hoodie","count":9}],"sample":[{"review_id":"rev_8812","review_rating":5,"size_bought":"L","height_cm":180,"excerpt":"Size up if you wear a hoodie underneath.","date_published":"2026-10-12"},{"review_id":"rev_8807","review_ra… (+340자) ``

**답변 1**
> The Wool Overcoat isn’t really “runs small” overall.
>
> * 41 reviews, average rating 4.6/5
> * Fit votes:
>   * True to size: 29
>   * A bit snug / runs small: 12
>   * Runs large: 0
>
> The repeated theme is layering, not a systematic small sizing. The top mention is “size up for a hoodie” – 9 reviewers note it.
>
> Sample evidence:
> * rev_8812 – 5★, L, 180 cm: “Size up if you wear a hoodie underneath.”
> * rev_8807 – 5★, L, 176 cm: “True to size over a shirt or a thin sweater; size up for a hoodie.”
> * rev_8803 – 5★, L, 180 cm: “True to size over a shirt or a thin sweater; size up for a hoodie.”
>
> So most shoppers find it true to size for a shirt/thin sweater, and the “runs small” comments are mostly about wanting extra room for heavier layers.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-facade · 1회차 · ✗ 실패

토큰 24,358 · 24.22초 · 모델 호출 5회 · 도구 호출 6회 · 첫 요청 프롬프트 2,257토큰

준비: 전략 `search`, 함수 6개

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

1. 모델 → **`a2api_search`** `` {"query":"wool overcoat product"} ``
   ← 결과 430B: `` {"selected":[{"name":"facade_get_prd_dtl_info","id":"facade.get_prd_dtl_info"},{"name":"facade_get_prd_grid_list_cnt","id":"facade.get_prd_grid_list_cnt"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_get_prd_dtl_info_v2","id":"facade.get_prd_dtl_info_v2"},{"name":"facade_save_prmt_list","id":"facade.save_prmt_list"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"product size fit"} ``
   ← 결과 570B: `` {"selected":[{"name":"facade_get_prd_dtl_info_v2","id":"facade.get_prd_dtl_info_v2"},{"name":"facade_get_prd_grid_list_cnt","id":"facade.get_prd_grid_list_cnt"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_get_prd_dtl_info","id":"facade.get_prd_dtl_info"},{"name":"facade_save_prmt_list","id":"facade.save_prmt_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match is already callable. If they cannot answer, tell the user what is missing instead of searching again."} ``
3. 모델 → **`a2api_search`** `` {"query":"product details"} ``
   ← 결과 445B: `` {"selected":[{"name":"facade_get_prd_dtl_info","id":"facade.get_prd_dtl_info"},{"name":"facade_get_prd_dtl_info_v2","id":"facade.get_prd_dtl_info_v2"},{"name":"facade_get_rfnd_pop_init_data","id":"facade.get_rfnd_pop_init_data"},{"name":"facade_get_prd_grid_list_cnt","id":"facade.get_prd_grid_list_cnt"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`facade_get_prd_grid_list`** `` {"keyword":"wool overcoat","page":1,"page_size":20} ``
   ← 결과 4,190B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_wool_overcoat","product_name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","price":289.0,"member_price":null,"stock":24,"availability":"in_stock","cost":120.0},{"product_id":"prd_scarves_04","product_name":"Wool stole","category_id":"cat_scarves","brand_id":"brn_ridgeline","price":59.0,"member_price":null,"stock":23,"availability":"in_stock","cost":24.46},{"product_id":"prd_pants_22","product_name":"Wool drawstring pants","category_id":"cat_pants","brand_id":"brn_northwind","price":149.0,"member_price":null,"s… (+900자) ``
5. 모델 → **`facade_get_prd_dtl_info_v2`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 812B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","product_name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","price":289.0,"member_price":null,"stock":24,"availability":"in_stock","cost":120.0,"approval_status":"active","variants":[{"variant_id":"var_wool_overcoat_s_charcoal","color":"Charcoal","size":"S","stock":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","color":"Charcoal","size":"M","stock":7,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_l_charcoal","color":"Charcoal","size":"L","stock":8,"availability":"i… (+212자) ``
6. 모델 → **`facade_get_prd_dtl_info`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 263B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","product_name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","price":289.0,"member_price":null,"stock":24,"availability":"in_stock","cost":120.0,"approval_status":"active"}} ``

**답변 1**
> The Wool overcoat in the catalog is:
>
> * **product_id:** prd_wool_overcoat
> * **product_name:** Wool overcoat
> * **category_id:** cat_outerwear
> * **price:** $289.00
> * **stock:** 24, availability in_stock
> * **approval_status:** active
> * **material:** 70% wool, 30% polyamide
>
> Variants on file:
> * var_wool_overcoat_s_charcoal – Charcoal / S – stock 5
> * var_wool_overcoat_m_charcoal – Charcoal / M – stock 7
> * var_wool_overcoat_l_charcoal – Charcoal / L – stock 8
> * var_wool_overcoat_xl_charcoal – Charcoal / XL – stock 4
>
> The product detail records I can access do not include a size chart, fit notes or a “runs small/large” flag. There is no fit/run-size information stored for prd_wool_overcoat, so I can’t confirm from system data that it runs small.

**채점**: ✗ 실패 — 빠진 것: fact "41 reviews, average 4.6" (41, 4.6 not shown); fact "29 say true to size, 12 say a bit snug, none say it runs lar" (29, 12 not shown); fact "the most common phrase is 'size up for a hoodie' (9 mentions" (9 not shown)
