# md-overcoat-runs-small — smoke-index-1

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> people keep saying the wool overcoat runs small. is that actually true?

- 필요한 도구: `get_review_summary`
- 허용 도구: `search_products`, `list_reviews`, `get_product_measurements`
- 답에 있어야 할 사실: 41 reviews, average 4.6
- 답에 있어야 할 사실: 29 say true to size, 12 say a bit snug, none say it runs large
- 답에 있어야 할 사실: the most common phrase is 'size up for a hoodie' (9 mentions), so the snug votes come from layering

### a2api-acom-index · 1회차 · ✓ 통과

토큰 74,778 · 36.305초 · 모델 호출 7회 · 도구 호출 6회 · 첫 요청 프롬프트 6,989토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_review_summary","get_product_measurements","get_product"]} ``
   ← 결과 92B: `` {"loaded":["search_products","get_review_summary","get_product_measurements","get_product"]} ``
2. 모델 → **`search_products`** `` {"query":"wool overcoat","limit":20} ``
   ← 결과 5,925B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/garment/chore-charcoal.svg","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"availability":"in… (+900자) ``
3. 모델 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat","sample_limit":3} ``
   ← 결과 940B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":null},"review_count":41,"rating_value":4.6,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":29},{"fit":"runs_small","label":"A bit snug","count":12},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[{"text":"size up for a hoodie","count":9}],"sample":[{"review_id":"rev_8812","review_rating":5,"size_bought":"L","height_cm":180,"excerpt":"Size up if you wear a hoodie underneath.","date_published":"2026-10-12"},{"review_id":"rev_8807","review_ra… (+340자) ``
4. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 380B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","unit":"cm","measurements":["chest","shoulder","sleeve","length"],"sizes":[{"size":"M","chest":56,"shoulder":46,"sleeve":64,"length":98},{"size":"L","chest":59,"shoulder":48,"sleeve":65.5,"length":100}],"how_measured":"Garment laid flat. Chest is armpit to armpit; length is from the highest point of the shoulder."}} ``
5. 모델 → **`get_product`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 1,154B: `` {"status":"succeeded","data":{"id":"prd_wool_overcoat","@type":"ProductGroup","name":"Wool overcoat","description":"A single-breasted overcoat in a 70% wool blend, cut to fit over a sweater.","brand_id":"brn_northwind","category_id":"cat_outerwear","keywords":[],"approval_status":"active","varies_by":["color","size"],"image":"/media/garment/chore-charcoal.svg","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","additional_property":[{"name":"material","value":"70% wool, 30% polyamide"}],"has_variant":[{"variant_id":"var_wool_ove… (+554자) ``
6. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat","sizes":["S","XL"]} ``
   ← 실패 292B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) The size chart has no size S. Next: get_product."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``

**답변 1**
> The Wool overcoat `prd_wool_overcoat` is not generally reported as running small.
>
> Review summary for the product, 41 reviews counted:
> * Rating: 4.6 / 5
> * Fit votes
>   * True to size: 29
>   * A bit snug / runs small: 12
>   * Runs large: 0
>
> So ~71% of reviewers say true to size and ~29% say a bit snug. No runs-large votes.
>
> Repeated mention:
> * “size up for a hoodie” – 9 mentions
>
> Sample evidence:
> * rev_8812 – 5★, size L, 180 cm: “Size up if you wear a hoodie underneath.”
> * rev_8807 – 5★, size L, 176 cm: “True to size over a shirt or a thin sweater; size up for a hoodie.”
> * rev_8803 – 5★, size L, 180 cm: “True to size over a shirt or a thin sweater; size up for a hoodie.”
>
> Product description: “A single-breasted overcoat in a 70% wool blend, cut to fit over a sweater.”
>
> Measurements on file, garment laid flat. Chest is armpit to armpit; length is from the highest point of the shoulder.
>
> * M: chest 56 cm, shoulder 46 cm, sleeve 64 cm, length 98 cm
> * L: chest 59 cm, shoulder 48 cm, sleeve 65.5 cm, length 100 cm
>
> Size S and XL are sold – S, M, L, XL in Charcoal, in stock – but the size chart currently has no measurement entries for S and XL.
>
> In practice reviewers find it true to size for a shirt/thin sweater and recommend sizing up when layering over a hoodie, which is where the “runs small” impression comes from.

**채점**: ✓ 통과
(도구 정밀도 0.80, 재현율 1.00)

### a2api-acom-graph · 1회차 · ✓ 통과

토큰 57,422 · 21.269초 · 모델 호출 6회 · 도구 호출 5회 · 첫 요청 프롬프트 6,989토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_review_summary","get_product_measurements","get_product"]} ``
   ← 결과 92B: `` {"loaded":["search_products","get_review_summary","get_product_measurements","get_product"]} ``
2. 모델 → **`search_products`** `` {"query":"wool overcoat","limit":20} ``
   ← 결과 1,847B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/garment/chore-charcoal.svg","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"availability":"in… (+900자) ``
3. 모델 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 1,101B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":null},"review_count":41,"rating_value":4.6,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":29},{"fit":"runs_small","label":"A bit snug","count":12},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[{"text":"size up for a hoodie","count":9}],"sample":[{"review_id":"rev_8812","review_rating":5,"size_bought":"L","height_cm":180,"excerpt":"Size up if you wear a hoodie underneath.","date_published":"2026-10-12"},{"review_id":"rev_8807","review_ra… (+501자) ``
4. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 532B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","unit":"cm","measurements":["chest","shoulder","sleeve","length"],"sizes":[{"size":"M","chest":56,"shoulder":46,"sleeve":64,"length":98},{"size":"L","chest":59,"shoulder":48,"sleeve":65.5,"length":100}],"how_measured":"Garment laid flat. Chest is armpit to armpit; length is from the highest point of the shoulder."},"next":"Functions that take IDs from this result: get_review_summary, approve_product, suggest_reorder, add_to_wishlist, compare_products (product_id)"} ``
5. 모델 → **`get_product`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 1,244B: `` {"status":"succeeded","data":{"id":"prd_wool_overcoat","@type":"ProductGroup","name":"Wool overcoat","description":"A single-breasted overcoat in a 70% wool blend, cut to fit over a sweater.","brand_id":"brn_northwind","category_id":"cat_outerwear","keywords":[],"approval_status":"active","varies_by":["color","size"],"image":"/media/garment/chore-charcoal.svg","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","additional_property":[{"name":"material","value":"70% wool, 30% polyamide"}],"has_variant":[{"variant_id":"var_wool_ove… (+644자) ``

**답변 1**
> The Wool overcoat, prd_wool_overcoat, is not generally reported as running small.
>
> Review summary for 41 reviews:
> * Average rating: 4.6 / 5
> * Fit votes
>   * True to size: 29 votes
>   * A bit snug / runs small: 12 votes
>   * Runs large: 0 votes
>
> So ~71% of reviewers say true to size and ~29% say it runs a bit snug. No reviewers voted runs large.
>
> The repeated phrase is “size up for a hoodie” – mentioned 9 times. Sample evidence:
>
> * “Size up if you wear a hoodie underneath.” – 5★, size L, 180 cm, 2026-10-12
> * “True to size over a shirt or a thin sweater; size up for a hoodie.” – 5★, size L, 176 cm, 2026-08-27
> * “True to size over a shirt or a thin sweater; size up for a hoodie.” – 5★, size L, 180 cm, 2026-07-24
>
> Measurements, garment laid flat:
> * M: chest 56 cm, shoulder 46 cm, sleeve 64 cm, length 98 cm
> * L: chest 59 cm, shoulder 48 cm, sleeve 65.5 cm, length 100 cm
> How measured: chest is armpit to armpit; length is from the highest point of the shoulder.
>
> In practice it fits true to size for shirts / thin sweaters, and reviewers recommend sizing up if you plan to layer a hoodie underneath.

**채점**: ✓ 통과
(도구 정밀도 0.75, 재현율 1.00)

### a2api-acom-names · 1회차 · ✓ 통과

토큰 28,547 · 31.531초 · 모델 호출 6회 · 도구 호출 5회 · 첫 요청 프롬프트 1,630토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_product","get_review_summary","list_reviews","get_product_measurements"]} ``
   ← 결과 107B: `` {"loaded":["search_products","get_product","get_review_summary","list_reviews","get_product_measurements"]} ``
2. 모델 → **`search_products`** `` {"query":"wool overcoat"} ``
   ← 결과 1,847B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/garment/chore-charcoal.svg","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"availability":"in… (+900자) ``
3. 모델 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 1,101B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":null},"review_count":41,"rating_value":4.6,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":29},{"fit":"runs_small","label":"A bit snug","count":12},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[{"text":"size up for a hoodie","count":9}],"sample":[{"review_id":"rev_8812","review_rating":5,"size_bought":"L","height_cm":180,"excerpt":"Size up if you wear a hoodie underneath.","date_published":"2026-10-12"},{"review_id":"rev_8807","review_ra… (+501자) ``
4. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 532B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","unit":"cm","measurements":["chest","shoulder","sleeve","length"],"sizes":[{"size":"M","chest":56,"shoulder":46,"sleeve":64,"length":98},{"size":"L","chest":59,"shoulder":48,"sleeve":65.5,"length":100}],"how_measured":"Garment laid flat. Chest is armpit to armpit; length is from the highest point of the shoulder."},"next":"Functions that take IDs from this result: get_review_summary, approve_product, suggest_reorder, add_to_wishlist, compare_products (product_id)"} ``
5. 모델 → **`list_reviews`** `` {"product_id":"prd_wool_overcoat","limit":20,"sort":"newest"} ``
   ← 결과 4,294B: `` {"status":"succeeded","data":{"items":[{"id":"rev_8812","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_l_charcoal","review_rating":5,"author":{"@type":"Person","name":"Jordan P."},"review_body":"Size up if you wear a hoodie underneath. Warm, sharp, and the wool feels solid.","fit":"true_to_size","height_cm":180,"size_bought":"L","image":[],"mentions":["size up for a hoodie"],"status":"visible","helpful_count":0,"date_published":"2026-10-12"},{"id":"rev_8811","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_l_charcoal","review_… (+900자) ``

**답변 1**
> The Wool overcoat `prd_wool_overcoat` is not generally reported as running small.
>
> Review summary for the product, 41 visible reviews, 4.6★ average:
>
> * Fit votes
>   * True to size: 29 votes
>   * A bit snug / runs small: 12 votes
>   * Runs large: 0 votes
>
> So ~71% of reviewers vote true to size and ~29% vote runs small. The repeated theme is layering:
>
> * “size up for a hoodie” mentioned 9 times
> * Sample reviewer notes:
>   * Jordan P., L, 180 cm, 5★, 2026-10-12: “Size up if you wear a hoodie underneath. Warm, sharp, and the wool feels solid.” fit = true_to_size
>   * Alex D., L, 176 cm, 5★, 2026-08-27: “True to size over a shirt or a thin sweater; size up for a hoodie.” fit = true_to_size
>   * Tim G., L, 180 cm, 4★, 2026-09-30: “A bit snug across the chest and shoulders, fine over a shirt.” fit = runs_small
>
> In practice reviewers say it’s true to size over a shirt/thin sweater and feels snug when you want to wear a hoodie underneath. That’s why you hear “runs small” – it’s layering sensitive rather than a systematic sizing issue.
>
> Garment measurements, laid flat, cm:
>
> * M: chest 56, shoulder 46, sleeve 64, length 98
> * L: chest 59, shoulder 48, sleeve 65.5, length 100
>
> How measured: Chest is armpit to armpit; length is from the highest point of the shoulder.
>
> Current stock: 24 total in Charcoal, S 5 / M 7 / L 8 / XL 4, list $289.00 USD, in stock.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)
