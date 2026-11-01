# md-overcoat-runs-small — ours-design-4

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `879cc92`

**과업**

> people keep saying the wool overcoat runs small. is that actually true?

- 필요한 도구: `get_review_summary`
- 허용 도구: `search_products`, `list_reviews`, `get_product_measurements`
- 답에 있어야 할 사실: 41 reviews, average 4.6
- 답에 있어야 할 사실: 29 say true to size, 12 say a bit snug, none say it runs large
- 답에 있어야 할 사실: the most common phrase is 'size up for a hoodie' (9 mentions), so the snug votes come from layering

### a2api-acom · 1회차 · ✓ 통과

토큰 9,664 · 10.894초 · 모델 호출 2회 · 도구 호출 1회 · 첫 요청 프롬프트 4,360토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

1. 모델 → **`acom_get_review_summary`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 940B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":null},"review_count":41,"rating_value":4.6,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":29},{"fit":"runs_small","label":"A bit snug","count":12},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[{"text":"size up for a hoodie","count":9}],"sample":[{"review_id":"rev_8812","review_rating":5,"size_bought":"L","height_cm":180,"excerpt":"Size up if you wear a hoodie underneath.","date_published":"2026-10-12"},{"review_id":"rev_8807","review_ra… (+340자) ``

**답변 1**
> The wool overcoat isn’t broadly “runs small” in the reviews.
>
> * 41 reviews, average rating 4.6
> * Fit votes:
>   * True to size: 29
>   * A bit snug / runs small: 12
>   * Runs large: 0
>
> The repeated theme is layering, not a general small sizing. The top mention is “size up for a hoodie” – 9 reviewers note it.
>
> Sample evidence:
> * rev_8812 – 5★, L, 180 cm: “Size up if you wear a hoodie underneath.”
> * rev_8807 – 5★, L, 176 cm: “True to size over a shirt or a thin sweater; size up for a hoodie.”
> * rev_8803 – 5★, L, 180 cm: “True to size over a shirt or a thin sweater; size up for a hoodie.”
>
> So it’s true to size for a shirt/thin sweater, and reviewers tend to size up when they want to wear a hoodie underneath.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-facade · 1회차 · ✗ 실패

토큰 18,684 · 26.049초 · 모델 호출 4회 · 도구 호출 5회 · 첫 요청 프롬프트 2,257토큰

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

**답변 1**
> The Wool overcoat in the system is:
>
> * **product_id:** prd_wool_overcoat
> * **product_name:** Wool overcoat
> * **price:** $289.00
> * **stock:** 24, availability in_stock
> * **Variants on file:** Charcoal only
>   * S – stock 5
>   * M – stock 7
>   * L – stock 8
>   * XL – stock 4
> * **Attributes on file:** material = 70% wool, 30% polyamide
>
> No fit / size-run note is stored for this SKU in the product detail record. The v2 detail returns only the material attribute and the size/color variants above; there is no official “runs small/large” flag or size chart in the data I can access.

**채점**: ✗ 실패 — 빠진 것: fact "41 reviews, average 4.6" (41, 4.6 not shown); fact "29 say true to size, 12 say a bit snug, none say it runs lar" (29, 12 not shown); fact "the most common phrase is 'size up for a hoodie' (9 mentions" (9 not shown)
