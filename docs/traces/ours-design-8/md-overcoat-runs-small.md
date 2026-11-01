# md-overcoat-runs-small — ours-design-8

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> people keep saying the wool overcoat runs small. is that actually true?

- 필요한 도구: `get_review_summary`
- 허용 도구: `search_products`, `list_reviews`, `get_product_measurements`
- 답에 있어야 할 사실: 41 reviews, average 4.6
- 답에 있어야 할 사실: 29 say true to size, 12 say a bit snug, none say it runs large
- 답에 있어야 할 사실: the most common phrase is 'size up for a hoodie' (9 mentions), so the snug votes come from layering

### a2api-acom-names · 1회차 · ✓ 통과

토큰 41,546 · 39.123초 · 모델 호출 8회 · 도구 호출 7회 · 첫 요청 프롬프트 1,630토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_product","get_product_measurements","list_reviews","get_review_summary"]} ``
   ← 결과 107B: `` {"loaded":["search_products","get_product","get_product_measurements","list_reviews","get_review_summary"]} ``
2. 모델 → **`search_products`** `` {"query":"wool overcoat"} ``
   ← 결과 1,847B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/garment/chore-charcoal.svg","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"availability":"in… (+900자) ``
3. 모델 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 1,101B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":null},"review_count":41,"rating_value":4.6,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":29},{"fit":"runs_small","label":"A bit snug","count":12},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[{"text":"size up for a hoodie","count":9}],"sample":[{"review_id":"rev_8812","review_rating":5,"size_bought":"L","height_cm":180,"excerpt":"Size up if you wear a hoodie underneath.","date_published":"2026-10-12"},{"review_id":"rev_8807","review_ra… (+501자) ``
4. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 532B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","unit":"cm","measurements":["chest","shoulder","sleeve","length"],"sizes":[{"size":"M","chest":56,"shoulder":46,"sleeve":64,"length":98},{"size":"L","chest":59,"shoulder":48,"sleeve":65.5,"length":100}],"how_measured":"Garment laid flat. Chest is armpit to armpit; length is from the highest point of the shoulder."},"next":"Functions that take IDs from this result: get_review_summary, approve_product, suggest_reorder, add_to_wishlist, compare_products (product_id)"} ``
5. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat","sizes":["S","M","L","XL"]} ``
   ← 실패 292B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) The size chart has no size S. Next: get_product."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
6. 모델 → **`list_reviews`** `` {"product_id":"prd_wool_overcoat","limit":20} ``
   ← 결과 4,294B: `` {"status":"succeeded","data":{"items":[{"id":"rev_8812","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_l_charcoal","review_rating":5,"author":{"@type":"Person","name":"Jordan P."},"review_body":"Size up if you wear a hoodie underneath. Warm, sharp, and the wool feels solid.","fit":"true_to_size","height_cm":180,"size_bought":"L","image":[],"mentions":["size up for a hoodie"],"status":"visible","helpful_count":0,"date_published":"2026-10-12"},{"id":"rev_8811","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_l_charcoal","review_… (+900자) ``
7. 모델 → **`get_product`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 1,244B: `` {"status":"succeeded","data":{"id":"prd_wool_overcoat","@type":"ProductGroup","name":"Wool overcoat","description":"A single-breasted overcoat in a 70% wool blend, cut to fit over a sweater.","brand_id":"brn_northwind","category_id":"cat_outerwear","keywords":[],"approval_status":"active","varies_by":["color","size"],"image":"/media/garment/chore-charcoal.svg","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","additional_property":[{"name":"material","value":"70% wool, 30% polyamide"}],"has_variant":[{"variant_id":"var_wool_ove… (+644자) ``

**답변 1**
> The Wool overcoat, prd_wool_overcoat, is not generally reported as running small.
>
> Review summary for the product, 41 visible reviews, rating 4.6:
> * Fit votes
>   * True to size: 29
>   * A bit snug / runs small: 12
>   * Runs large: 0
> * Repeated mention: “size up for a hoodie” – 9 mentions
>
> So ~71% of reviewers vote true to size and ~29% vote runs small / a bit snug. The snug reports are most often “a bit snug across the chest and shoulders, fine over a shirt” and the common advice in the samples is to size up if you want to wear a hoodie underneath.
>
> * rev_8812, L, 180 cm, 5★: “Size up if you wear a hoodie underneath. Warm, sharp, and the wool feels solid.”
> * rev_8807, L, 176 cm, 5★: “True to size over a shirt or a thin sweater; size up for a hoodie.”
> * rev_8803, L, 180 cm, 5★: “True to size over a shirt or a thin sweater; size up for a hoodie.”
>
> Product info
> * Price: $289.00 USD, in stock, total inventory 24
> * Variants: S, M, L, XL in Charcoal
> * Description: “A single-breasted overcoat in a 70% wool blend, cut to fit over a sweater.” Material: 70% wool, 30% polyamide
>
> Measurements on file, garment laid flat, chest armpit to armpit; length from highest point of shoulder:
> * M: chest 56 cm, shoulder 46 cm, sleeve 64 cm, length 98 cm
> * L: chest 59 cm, shoulder 48 cm, sleeve 65.5 cm, length 100 cm
>
> Size S and XL are not present in the measurement chart returned by the system.
>
> Bottom line: most buyers find it true to size for a shirt/thin sweater. The “runs small” perception comes from the ~29% who find it a bit snug, especially when layering. If you plan to wear a hoodie under it, sizing up is the common recommendation.

**채점**: ✓ 통과
(도구 정밀도 0.83, 재현율 1.00)

### a2api-acom-names · 2회차 · ✓ 통과

토큰 27,214 · 23.533초 · 모델 호출 6회 · 도구 호출 5회 · 첫 요청 프롬프트 1,630토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_product","get_product_measurements","list_reviews","get_review_summary"]} ``
   ← 결과 107B: `` {"loaded":["search_products","get_product","get_product_measurements","list_reviews","get_review_summary"]} ``
2. 모델 → **`search_products`** `` {"query":"wool overcoat"} ``
   ← 결과 1,847B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/garment/chore-charcoal.svg","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"availability":"in… (+900자) ``
3. 모델 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 1,101B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":null},"review_count":41,"rating_value":4.6,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":29},{"fit":"runs_small","label":"A bit snug","count":12},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[{"text":"size up for a hoodie","count":9}],"sample":[{"review_id":"rev_8812","review_rating":5,"size_bought":"L","height_cm":180,"excerpt":"Size up if you wear a hoodie underneath.","date_published":"2026-10-12"},{"review_id":"rev_8807","review_ra… (+501자) ``
4. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 532B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","unit":"cm","measurements":["chest","shoulder","sleeve","length"],"sizes":[{"size":"M","chest":56,"shoulder":46,"sleeve":64,"length":98},{"size":"L","chest":59,"shoulder":48,"sleeve":65.5,"length":100}],"how_measured":"Garment laid flat. Chest is armpit to armpit; length is from the highest point of the shoulder."},"next":"Functions that take IDs from this result: get_review_summary, approve_product, suggest_reorder, add_to_wishlist, compare_products (product_id)"} ``
5. 모델 → **`get_product`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 1,244B: `` {"status":"succeeded","data":{"id":"prd_wool_overcoat","@type":"ProductGroup","name":"Wool overcoat","description":"A single-breasted overcoat in a 70% wool blend, cut to fit over a sweater.","brand_id":"brn_northwind","category_id":"cat_outerwear","keywords":[],"approval_status":"active","varies_by":["color","size"],"image":"/media/garment/chore-charcoal.svg","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","additional_property":[{"name":"material","value":"70% wool, 30% polyamide"}],"has_variant":[{"variant_id":"var_wool_ove… (+644자) ``

**답변 1**
> The Wool overcoat (prd_wool_overcoat) – $289, in stock 24 units Charcoal S-XL – is not broadly “runs small”.
>
> Review summary from 41 visible reviews, rating 4.6/5:
>
> * Fit votes
>   * True to size: 29 votes
>   * A bit snug / runs small: 12 votes
>   * Runs large: 0 votes
>
> The recurring theme is layering, not a systematic small sizing. The top repeated mention is “size up for a hoodie” – 9 mentions.
>
> Sample evidence:
> * rev_8812 – 5★, size L, 180 cm: “Size up if you wear a hoodie underneath.” 2026-10-12
> * rev_8807 – 5★, size L, 176 cm: “True to size over a shirt or a thin sweater; size up for a hoodie.” 2026-08-27
> * rev_8803 – 5★, size L, 180 cm: “True to size over a shirt or a thin sweater; size up for a hoodie.” 2026-07-24
>
> Product description notes it is “cut to fit over a sweater.” Measurements are garment laid flat, chest armpit-to-armpit; length from highest point of shoulder:
>
> * M: chest 56 cm, shoulder 46 cm, sleeve 64 cm, length 98 cm
> * L: chest 59 cm, shoulder 48 cm, sleeve 65.5 cm, length 100 cm
>
> So most buyers find it true to size for a shirt/thin sweater, and the 12 “a bit snug” votes align with the common advice to size up if you plan to wear a hoodie underneath.

**채점**: ✓ 통과
(도구 정밀도 0.75, 재현율 1.00)

### a2api-acom-names-norelated · 1회차 · ✓ 통과

토큰 71,122 · 45.342초 · 모델 호출 10회 · 도구 호출 9회 · 첫 요청 프롬프트 1,630토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_product","get_product_measurements","list_reviews","get_review_summary"]} ``
   ← 결과 107B: `` {"loaded":["search_products","get_product","get_product_measurements","list_reviews","get_review_summary"]} ``
2. 모델 → **`search_products`** `` {"query":"wool overcoat"} ``
   ← 결과 5,925B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/garment/chore-charcoal.svg","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"availability":"in… (+900자) ``
3. 모델 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 940B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":null},"review_count":41,"rating_value":4.6,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":29},{"fit":"runs_small","label":"A bit snug","count":12},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[{"text":"size up for a hoodie","count":9}],"sample":[{"review_id":"rev_8812","review_rating":5,"size_bought":"L","height_cm":180,"excerpt":"Size up if you wear a hoodie underneath.","date_published":"2026-10-12"},{"review_id":"rev_8807","review_ra… (+340자) ``
4. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 380B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","unit":"cm","measurements":["chest","shoulder","sleeve","length"],"sizes":[{"size":"M","chest":56,"shoulder":46,"sleeve":64,"length":98},{"size":"L","chest":59,"shoulder":48,"sleeve":65.5,"length":100}],"how_measured":"Garment laid flat. Chest is armpit to armpit; length is from the highest point of the shoulder."}} ``
5. 모델 → **`list_reviews`** `` {"product_id":"prd_wool_overcoat","sort":"rating","limit":20} ``
   ← 결과 4,138B: `` {"status":"succeeded","data":{"items":[{"id":"rev_8812","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_l_charcoal","review_rating":5,"author":{"@type":"Person","name":"Jordan P."},"review_body":"Size up if you wear a hoodie underneath. Warm, sharp, and the wool feels solid.","fit":"true_to_size","height_cm":180,"size_bought":"L","image":[],"mentions":["size up for a hoodie"],"status":"visible","helpful_count":0,"date_published":"2026-10-12"},{"id":"rev_8810","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_m_charcoal","review_… (+900자) ``
6. 모델 → **`list_reviews`** `` {"product_id":"prd_wool_overcoat","limit":100,"sort":"newest"} ``
   ← 결과 4,122B: `` {"status":"succeeded","data":{"items":[{"id":"rev_8812","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_l_charcoal","review_rating":5,"author":{"@type":"Person","name":"Jordan P."},"review_body":"Size up if you wear a hoodie underneath. Warm, sharp, and the wool feels solid.","fit":"true_to_size","height_cm":180,"size_bought":"L","image":[],"mentions":["size up for a hoodie"],"status":"visible","helpful_count":0,"date_published":"2026-10-12"},{"id":"rev_8811","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_l_charcoal","review_… (+900자) ``
7. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat","sizes":["S","XL"]} ``
   ← 실패 292B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) The size chart has no size S. Next: get_product."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
8. 모델 → **`get_product`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 1,154B: `` {"status":"succeeded","data":{"id":"prd_wool_overcoat","@type":"ProductGroup","name":"Wool overcoat","description":"A single-breasted overcoat in a 70% wool blend, cut to fit over a sweater.","brand_id":"brn_northwind","category_id":"cat_outerwear","keywords":[],"approval_status":"active","varies_by":["color","size"],"image":"/media/garment/chore-charcoal.svg","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","additional_property":[{"name":"material","value":"70% wool, 30% polyamide"}],"has_variant":[{"variant_id":"var_wool_ove… (+554자) ``
9. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 488B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","unit":"cm","measurements":["chest","shoulder","sleeve","length"],"sizes":[{"size":"M","chest":56,"shoulder":46,"sleeve":64,"length":98},{"size":"L","chest":59,"shoulder":48,"sleeve":65.5,"length":100}],"how_measured":"Garment laid flat. Chest is armpit to armpit; length is from the highest point of the shoulder."},"note":"Same call and result as 1 earlier time(s); you already have this data. Use it, or answer the user."} ``

**답변 1**
> The Wool overcoat prd_wool_overcoat is not consistently reported as running small.
>
> Review summary for the product, 41 visible reviews:
> * Average rating: 4.6 / 5
> * Fit votes
>   * True to size: 29
>   * A bit snug / runs small: 12
>   * Runs large: 0
>
> So ~71% of reviewers vote true to size and ~29% vote runs small.
>
> The repeated mention is “size up for a hoodie”, mentioned 9 times. Examples:
>
> * rev_8812 – 5★, size L, 180 cm: “Size up if you wear a hoodie underneath. Warm, sharp, and the wool feels solid.” fit = true_to_size
> * rev_8807 – 5★, size L, 176 cm: “True to size over a shirt or a thin sweater; size up for a hoodie.” fit = true_to_size
> * rev_8803 – 5★, size L, 180 cm: “True to size over a shirt or a thin sweater; size up for a hoodie.” fit = true_to_size
>
> Runs-small reports are snug over the chest/shoulders, not a full size down:
>
> * rev_8811 – 4★, size L, 180 cm, fit runs_small: “A bit snug across the chest and shoulders, fine over a shirt.”
> * rev_8808 – 3★, size L, 179 cm, fit runs_small: “A bit snug across the chest and shoulders, fine over a shirt.”
> * rev_8805 – 4★, size L, 178 cm, fit runs_small: “A bit snug across the chest and shoulders, fine over a shirt.”
>
> Product description: “A single-breasted overcoat in a 70% wool blend, cut to fit over a sweater.”
>
> Measurements on file, garment laid flat, chest armpit to armpit; length from highest point of shoulder:
> * M: chest 56 cm, shoulder 46 cm, sleeve 64 cm, length 98 cm
> * L: chest 59 cm, shoulder 48 cm, sleeve 65.5 cm, length 100 cm
>
> Size chart data for S and XL is not available in the system.
>
> Takeaway: most buyers find it true to size for a shirt/thin sweater. The “runs small” perception comes from the snug fit when layering; reviewers commonly recommend sizing up if you plan to wear a hoodie underneath.

**채점**: ✓ 통과
(도구 정밀도 0.88, 재현율 1.00)

### a2api-acom-names-norelated · 2회차 · ✓ 통과

토큰 32,805 · 24.28초 · 모델 호출 6회 · 도구 호출 5회 · 첫 요청 프롬프트 1,630토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_product","get_product_measurements","list_reviews","get_review_summary"]} ``
   ← 결과 107B: `` {"loaded":["search_products","get_product","get_product_measurements","list_reviews","get_review_summary"]} ``
2. 모델 → **`search_products`** `` {"query":"wool overcoat"} ``
   ← 결과 5,925B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/garment/chore-charcoal.svg","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"availability":"in… (+900자) ``
3. 모델 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 940B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":null},"review_count":41,"rating_value":4.6,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":29},{"fit":"runs_small","label":"A bit snug","count":12},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[{"text":"size up for a hoodie","count":9}],"sample":[{"review_id":"rev_8812","review_rating":5,"size_bought":"L","height_cm":180,"excerpt":"Size up if you wear a hoodie underneath.","date_published":"2026-10-12"},{"review_id":"rev_8807","review_ra… (+340자) ``
4. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 380B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","unit":"cm","measurements":["chest","shoulder","sleeve","length"],"sizes":[{"size":"M","chest":56,"shoulder":46,"sleeve":64,"length":98},{"size":"L","chest":59,"shoulder":48,"sleeve":65.5,"length":100}],"how_measured":"Garment laid flat. Chest is armpit to armpit; length is from the highest point of the shoulder."}} ``
5. 모델 → **`list_reviews`** `` {"product_id":"prd_wool_overcoat","status":"visible","sort":"rating","limit":20} ``
   ← 결과 4,138B: `` {"status":"succeeded","data":{"items":[{"id":"rev_8812","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_l_charcoal","review_rating":5,"author":{"@type":"Person","name":"Jordan P."},"review_body":"Size up if you wear a hoodie underneath. Warm, sharp, and the wool feels solid.","fit":"true_to_size","height_cm":180,"size_bought":"L","image":[],"mentions":["size up for a hoodie"],"status":"visible","helpful_count":0,"date_published":"2026-10-12"},{"id":"rev_8810","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_m_charcoal","review_… (+900자) ``

**답변 1**
> The Wool overcoat, prd_wool_overcoat, is not showing a systematic “runs small” pattern in the visible reviews.
>
> * Review base: 41 visible reviews, average rating 4.6/5
> * Fit votes
>   * True to size: 29
>   * A bit snug / runs small: 12
>   * Runs large: 0
>
> The most repeated mention is “size up for a hoodie” – 9 mentions. Sample evidence:
>
> * rev_8812 – 5★, size L, 180 cm: “Size up if you wear a hoodie underneath. Warm, sharp, and the wool feels solid.” fit = true_to_size
> * rev_8807 – 5★, size L, 176 cm: “True to size over a shirt or a thin sweater; size up for a hoodie.” fit = true_to_size
> * rev_8803 – 5★, size L, 180 cm: “True to size over a shirt or a thin sweater; size up for a hoodie.” fit = true_to_size
>
> So the majority call it true to size, with a minority reporting it feels a bit snug. The snug reports are largely tied to layering – reviewers say it’s true to size over a shirt/thin sweater and recommend sizing up when wearing a hoodie underneath.
>
> Garment measurements returned for the product, laid flat:
>
> * M: chest 56 cm, shoulder 46 cm, sleeve 64 cm, length 98 cm
> * L: chest 59 cm, shoulder 48 cm, sleeve 65.5 cm, length 100 cm
>
> How measured: “Garment laid flat. Chest is armpit to armpit; length is from the highest point of the shoulder.”
>
> In short: it’s generally true to size, not a consistent run-small issue, but expect a snug fit if you plan to layer heavily.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)
