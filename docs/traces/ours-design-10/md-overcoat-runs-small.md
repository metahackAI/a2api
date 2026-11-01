# md-overcoat-runs-small — ours-design-10

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `c8c944e`

**과업**

> people keep saying the wool overcoat runs small. is that actually true?

- 필요한 도구: `get_review_summary`
- 허용 도구: `search_products`, `list_reviews`, `get_product_measurements`
- 답에 있어야 할 사실: 41 reviews, average 4.6
- 답에 있어야 할 사실: 29 say true to size, 12 say a bit snug, none say it runs large
- 답에 있어야 할 사실: the most common phrase is 'size up for a hoodie' (9 mentions), so the snug votes come from layering

### a2api-acom · 1회차 · ✓ 통과

토큰 9,740 · 12.295초 · 모델 호출 2회 · 도구 호출 1회 · 첫 요청 프롬프트 4,360토큰

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

### a2api-acom · 2회차 · ✓ 통과

토큰 9,664 · 10.841초 · 모델 호출 2회 · 도구 호출 1회 · 첫 요청 프롬프트 4,360토큰

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

### a2api-acom-names-norelated · 1회차 · E MODEL_CALL_LIMIT

토큰 87,513 · 49.393초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 1,984토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_product","get_product_measurements","list_reviews","get_review_summary"]} ``
   ← 결과 107B: `` {"loaded":["search_products","get_product","get_product_measurements","list_reviews","get_review_summary"]} ``
2. 모델 → **`search_products`** `` {"query":"wool overcoat","limit":20} ``
   ← 결과 5,925B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/garment/chore-charcoal.svg","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"availability":"in… (+900자) ``
3. 모델 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat","sample_limit":5} ``
   ← 결과 1,312B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":null},"review_count":41,"rating_value":4.6,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":29},{"fit":"runs_small","label":"A bit snug","count":12},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[{"text":"size up for a hoodie","count":9}],"sample":[{"review_id":"rev_8812","review_rating":5,"size_bought":"L","height_cm":180,"excerpt":"Size up if you wear a hoodie underneath.","date_published":"2026-10-12"},{"review_id":"rev_8807","review_ra… (+712자) ``
4. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 380B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","unit":"cm","measurements":["chest","shoulder","sleeve","length"],"sizes":[{"size":"M","chest":56,"shoulder":46,"sleeve":64,"length":98},{"size":"L","chest":59,"shoulder":48,"sleeve":65.5,"length":100}],"how_measured":"Garment laid flat. Chest is armpit to armpit; length is from the highest point of the shoulder."}} ``
5. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat","sizes":["S","M","L","XL"]} ``
   ← 실패 292B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) The size chart has no size S. Next: get_product."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
6. 모델 → **`get_product`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 1,154B: `` {"status":"succeeded","data":{"id":"prd_wool_overcoat","@type":"ProductGroup","name":"Wool overcoat","description":"A single-breasted overcoat in a 70% wool blend, cut to fit over a sweater.","brand_id":"brn_northwind","category_id":"cat_outerwear","keywords":[],"approval_status":"active","varies_by":["color","size"],"image":"/media/garment/chore-charcoal.svg","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","additional_property":[{"name":"material","value":"70% wool, 30% polyamide"}],"has_variant":[{"variant_id":"var_wool_ove… (+554자) ``
7. 모델 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat","size":"M","sample_limit":3} ``
   ← 결과 873B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":"M"},"review_count":15,"rating_value":4.9,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":15},{"fit":"runs_small","label":"A bit snug","count":0},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[],"sample":[{"review_id":"rev_8810","review_rating":5,"size_bought":"M","height_cm":177,"excerpt":"True to size and the charcoal is a deep, even color.","date_published":"2026-09-22"},{"review_id":"rev_8809","review_rating":5,"size_bought":"M","heig… (+273자) ``
8. 모델 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat","size":"L","sample_limit":3} ``
   ← 결과 939B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":"L"},"review_count":26,"rating_value":4.4,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":14},{"fit":"runs_small","label":"A bit snug","count":12},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[{"text":"size up for a hoodie","count":9}],"sample":[{"review_id":"rev_8812","review_rating":5,"size_bought":"L","height_cm":180,"excerpt":"Size up if you wear a hoodie underneath.","date_published":"2026-10-12"},{"review_id":"rev_8807","review_rat… (+339자) ``
9. 모델 → **`list_reviews`** `` {"product_id":"prd_wool_overcoat","status":"visible","sort":"newest","limit":20} ``
   ← 결과 4,142B: `` {"status":"succeeded","data":{"items":[{"id":"rev_8812","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_l_charcoal","review_rating":5,"author":{"@type":"Person","name":"Jordan P."},"review_body":"Size up if you wear a hoodie underneath. Warm, sharp, and the wool feels solid.","fit":"true_to_size","height_cm":180,"size_bought":"L","image":[],"mentions":["size up for a hoodie"],"status":"visible","helpful_count":0,"date_published":"2026-10-12"},{"id":"rev_8811","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_l_charcoal","review_… (+900자) ``
10. 모델 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat","size":"S","sample_limit":3} ``
   ← 실패 320B: `` {"status":"failed","error":{"code":"UPSTREAM_VALIDATION_FAILED","detail":"The backend rejected the request values. (HTTP 422) No reviews match these conditions; widen the height range or size. Next: get_product_measurements."},"hint":"The service rejected these values. Correct them only if the user gave other values."} ``
11. 모델 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat","size":"XL","sample_limit":3} ``
   ← 실패 320B: `` {"status":"failed","error":{"code":"UPSTREAM_VALIDATION_FAILED","detail":"The backend rejected the request values. (HTTP 422) No reviews match these conditions; widen the height range or size. Next: get_product_measurements."},"hint":"The service rejected these values. Correct them only if the user gave other values."} ``
12. 모델 → **`list_reviews`** `` {"product_id":"prd_wool_overcoat","status":"visible","limit":100} ``
   ← 결과 4,122B: `` {"status":"succeeded","data":{"items":[{"id":"rev_8812","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_l_charcoal","review_rating":5,"author":{"@type":"Person","name":"Jordan P."},"review_body":"Size up if you wear a hoodie underneath. Warm, sharp, and the wool feels solid.","fit":"true_to_size","height_cm":180,"size_bought":"L","image":[],"mentions":["size up for a hoodie"],"status":"visible","helpful_count":0,"date_published":"2026-10-12"},{"id":"rev_8811","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_l_charcoal","review_… (+900자) ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "41 reviews, average 4.6" (41, 4.6 not shown); fact "29 say true to size, 12 say a bit snug, none say it runs lar" (29, 12 not shown); fact "the most common phrase is 'size up for a hoodie' (9 mentions" (9 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.91, 재현율 1.00)

### a2api-acom-names-norelated · 2회차 · ✓ 통과

토큰 52,239 · 33.027초 · 모델 호출 8회 · 도구 호출 7회 · 첫 요청 프롬프트 1,984토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_product","get_product_measurements","get_review_summary","list_reviews"]} ``
   ← 결과 107B: `` {"loaded":["search_products","get_product","get_product_measurements","get_review_summary","list_reviews"]} ``
2. 모델 → **`search_products`** `` {"query":"wool overcoat","limit":20} ``
   ← 결과 5,925B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/garment/chore-charcoal.svg","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"availability":"in… (+900자) ``
3. 모델 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat","sample_limit":3} ``
   ← 결과 940B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":null},"review_count":41,"rating_value":4.6,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":29},{"fit":"runs_small","label":"A bit snug","count":12},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[{"text":"size up for a hoodie","count":9}],"sample":[{"review_id":"rev_8812","review_rating":5,"size_bought":"L","height_cm":180,"excerpt":"Size up if you wear a hoodie underneath.","date_published":"2026-10-12"},{"review_id":"rev_8807","review_ra… (+340자) ``
4. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 380B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","unit":"cm","measurements":["chest","shoulder","sleeve","length"],"sizes":[{"size":"M","chest":56,"shoulder":46,"sleeve":64,"length":98},{"size":"L","chest":59,"shoulder":48,"sleeve":65.5,"length":100}],"how_measured":"Garment laid flat. Chest is armpit to armpit; length is from the highest point of the shoulder."}} ``
5. 모델 → **`list_reviews`** `` {"product_id":"prd_wool_overcoat","status":"visible","sort":"rating","limit":20} ``
   ← 결과 4,138B: `` {"status":"succeeded","data":{"items":[{"id":"rev_8812","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_l_charcoal","review_rating":5,"author":{"@type":"Person","name":"Jordan P."},"review_body":"Size up if you wear a hoodie underneath. Warm, sharp, and the wool feels solid.","fit":"true_to_size","height_cm":180,"size_bought":"L","image":[],"mentions":["size up for a hoodie"],"status":"visible","helpful_count":0,"date_published":"2026-10-12"},{"id":"rev_8810","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_m_charcoal","review_… (+900자) ``
6. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat","sizes":["S","XL"]} ``
   ← 실패 292B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) The size chart has no size S. Next: get_product."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
7. 모델 → **`get_product`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 1,154B: `` {"status":"succeeded","data":{"id":"prd_wool_overcoat","@type":"ProductGroup","name":"Wool overcoat","description":"A single-breasted overcoat in a 70% wool blend, cut to fit over a sweater.","brand_id":"brn_northwind","category_id":"cat_outerwear","keywords":[],"approval_status":"active","varies_by":["color","size"],"image":"/media/garment/chore-charcoal.svg","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","additional_property":[{"name":"material","value":"70% wool, 30% polyamide"}],"has_variant":[{"variant_id":"var_wool_ove… (+554자) ``

**답변 1**
> The Wool overcoat `prd_wool_overcoat` is not showing a systematic “runs small” pattern in the review data.
>
> Review summary for the product, 41 visible reviews:
> * Rating: 4.6 / 5
> * Fit votes
>   * True to size: 29
>   * A bit snug / runs small: 12
>   * Runs large: 0
> * Repeated mention: “size up for a hoodie” – 9 mentions
>
> Sample visible reviews:
> * rev_8812 – 5★, size L, 180 cm – “Size up if you wear a hoodie underneath. Warm, sharp, and the wool feels solid.” fit: true_to_size
> * rev_8807 – 5★, size L, 176 cm – “True to size over a shirt or a thin sweater; size up for a hoodie.” fit: true_to_size
> * rev_8803 – 5★, size L, 180 cm – “True to size over a shirt or a thin sweater; size up for a hoodie.” fit: true_to_size
>
> So ~71% of reviewers vote true to size and 29% vote a bit snug, with no runs-large votes. The recurring advice is to size up when layering over a hoodie, otherwise it is reported as true to size over a shirt or thin sweater.
>
> Garment measurements on file, laid flat, cm:
> * How measured: Garment laid flat. Chest is armpit to armpit; length is from the highest point of the shoulder.
> * M: chest 56, shoulder 46, sleeve 64, length 98
> * L: chest 59, shoulder 48, sleeve 65.5, length 100
>
> Measurements for sizes S and XL are not present in the size chart in the system; the product is sold in S, M, L, XL Charcoal with current total stock 24 units.
>
> If you want, I can pull the full set of “runs small” reviews for a specific size/height range.

**채점**: ✓ 통과
(도구 정밀도 0.83, 재현율 1.00)

### a2api-acom-names-batch · 1회차 · ✓ 통과

토큰 63,126 · 53.525초 · 모델 호출 9회 · 도구 호출 8회 · 첫 요청 프롬프트 2,170토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_product","get_product_measurements","list_reviews","get_review_summary"]} ``
   ← 결과 107B: `` {"loaded":["search_products","get_product","get_product_measurements","list_reviews","get_review_summary"]} ``
2. 모델 → **`search_products`** `` {"query":"wool overcoat","limit":20} ``
   ← 결과 5,925B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/garment/chore-charcoal.svg","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"availability":"in… (+900자) ``
3. 모델 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat","sample_limit":5} ``
   ← 결과 1,312B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":null},"review_count":41,"rating_value":4.6,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":29},{"fit":"runs_small","label":"A bit snug","count":12},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[{"text":"size up for a hoodie","count":9}],"sample":[{"review_id":"rev_8812","review_rating":5,"size_bought":"L","height_cm":180,"excerpt":"Size up if you wear a hoodie underneath.","date_published":"2026-10-12"},{"review_id":"rev_8807","review_ra… (+712자) ``
4. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 380B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","unit":"cm","measurements":["chest","shoulder","sleeve","length"],"sizes":[{"size":"M","chest":56,"shoulder":46,"sleeve":64,"length":98},{"size":"L","chest":59,"shoulder":48,"sleeve":65.5,"length":100}],"how_measured":"Garment laid flat. Chest is armpit to armpit; length is from the highest point of the shoulder."}} ``
5. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat","sizes":["S","XL"]} ``
   ← 실패 292B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) The size chart has no size S. Next: get_product."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
6. 모델 → **`get_product`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 1,154B: `` {"status":"succeeded","data":{"id":"prd_wool_overcoat","@type":"ProductGroup","name":"Wool overcoat","description":"A single-breasted overcoat in a 70% wool blend, cut to fit over a sweater.","brand_id":"brn_northwind","category_id":"cat_outerwear","keywords":[],"approval_status":"active","varies_by":["color","size"],"image":"/media/garment/chore-charcoal.svg","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","additional_property":[{"name":"material","value":"70% wool, 30% polyamide"}],"has_variant":[{"variant_id":"var_wool_ove… (+554자) ``
7. 모델 → **`list_reviews`** `` {"product_id":"prd_wool_overcoat","limit":100,"sort":"newest"} ``
   ← 결과 4,122B: `` {"status":"succeeded","data":{"items":[{"id":"rev_8812","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_l_charcoal","review_rating":5,"author":{"@type":"Person","name":"Jordan P."},"review_body":"Size up if you wear a hoodie underneath. Warm, sharp, and the wool feels solid.","fit":"true_to_size","height_cm":180,"size_bought":"L","image":[],"mentions":["size up for a hoodie"],"status":"visible","helpful_count":0,"date_published":"2026-10-12"},{"id":"rev_8811","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_l_charcoal","review_… (+900자) ``
8. 모델 → **`a2api_batch`** `` {"calls":[{"name":"get_review_summary","arguments":{"product_id":"prd_wool_overcoat","size":"S","sample_limit":3}},{"name":"get_review_summary","arguments":{"product_id":"prd_wool_overcoat","size":"M","sample_limit":3}},{"name":"get_review_summary","arguments":{"product_id":"prd_wool_overcoat","size":"L","sample_limit":3}},{"name":"get_review_summary","arguments":{"product_id":"prd_wool_overcoat","size":"XL","sample_limit":3}}]} ``
   ← 결과 2,623B: `` {"batch":[{"name":"get_review_summary","result":{"status":"failed","error":{"code":"UPSTREAM_VALIDATION_FAILED","detail":"The backend rejected the request values. (HTTP 422) No reviews match these conditions; widen the height range or size. Next: get_product_measurements."},"hint":"The service rejected these values. Correct them only if the user gave other values."}},{"name":"get_review_summary","result":{"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":"M"},"review_count":15,"rating_value":4.9,"fit_votes":[{"fit":"true_to… (+900자) ``

**답변 1**
> The Wool overcoat `prd_wool_overcoat` is not generally reported as running small.
>
> * Overall visible reviews: 41 reviews, 4.6★ average
>   * Fit votes: True to size 29, A bit snug / runs small 12, Runs large 0
>   * Repeated mention: “size up for a hoodie” – 9 mentions
>
> Size breakdown from the review summary:
>
> * Size M – 15 reviews, 4.9★
>   * Fit votes: True to size 15, Runs small 0, Runs large 0
>   * Sample: “True to size and the charcoal is a deep, even color.” rev_8810; “Fits true to size, sleeves the right length.” rev_8809
>
> * Size L – 26 reviews, 4.4★
>   * Fit votes: True to size 14, Runs small 12, Runs large 0
>   * Repeated mention: “size up for a hoodie” – 9 mentions
>   * Sample: “Size up if you wear a hoodie underneath.” rev_8812, 180 cm, L; “True to size over a shirt or a thin sweater; size up for a hoodie.” rev_8807, 176 cm, L
>
> No visible reviews were found for sizes S and XL in the review summary, so there is no fit signal for those sizes.
>
> Measurements on file, garment laid flat:
> * M: chest 56 cm, shoulder 46 cm, sleeve 64 cm, length 98 cm
> * L: chest 59 cm, shoulder 48 cm, sleeve 65.5 cm, length 100 cm
> How measured: “Garment laid flat. Chest is armpit to armpit; length is from the highest point of the shoulder.”
>
> So the “runs small” chatter is concentrated in size L and is mostly about layering: reviewers call it true to size over a shirt/thin sweater and recommend sizing up when a hoodie is worn underneath. The majority of reviews overall, and all M reviews, report true to size with no runs-large reports.

**채점**: ✓ 통과
(도구 정밀도 0.90, 재현율 1.00)

### a2api-acom-names-batch · 2회차 · ✓ 통과

토큰 36,902 · 30.05초 · 모델 호출 6회 · 도구 호출 5회 · 첫 요청 프롬프트 2,170토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

1. 모델 → **`a2api_load`** `` {"names":["search › product: search_products","catalog › product: get_product","catalog › product: get_product_measurements","catalog › review: get_review_summary","catalog › review: list_reviews"]} ``
   ← 결과 107B: `` {"loaded":["search_products","get_product","get_product_measurements","get_review_summary","list_reviews"]} ``
2. 모델 → **`search_products`** `` {"query":"wool overcoat","limit":20} ``
   ← 결과 5,925B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/garment/chore-charcoal.svg","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"availability":"in… (+900자) ``
3. 모델 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat","sample_limit":5} ``
   ← 결과 1,312B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":null},"review_count":41,"rating_value":4.6,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":29},{"fit":"runs_small","label":"A bit snug","count":12},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[{"text":"size up for a hoodie","count":9}],"sample":[{"review_id":"rev_8812","review_rating":5,"size_bought":"L","height_cm":180,"excerpt":"Size up if you wear a hoodie underneath.","date_published":"2026-10-12"},{"review_id":"rev_8807","review_ra… (+712자) ``
4. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 380B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","unit":"cm","measurements":["chest","shoulder","sleeve","length"],"sizes":[{"size":"M","chest":56,"shoulder":46,"sleeve":64,"length":98},{"size":"L","chest":59,"shoulder":48,"sleeve":65.5,"length":100}],"how_measured":"Garment laid flat. Chest is armpit to armpit; length is from the highest point of the shoulder."}} ``
5. 모델 → **`list_reviews`** `` {"product_id":"prd_wool_overcoat","status":"visible","sort":"newest","limit":20} ``
   ← 결과 4,142B: `` {"status":"succeeded","data":{"items":[{"id":"rev_8812","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_l_charcoal","review_rating":5,"author":{"@type":"Person","name":"Jordan P."},"review_body":"Size up if you wear a hoodie underneath. Warm, sharp, and the wool feels solid.","fit":"true_to_size","height_cm":180,"size_bought":"L","image":[],"mentions":["size up for a hoodie"],"status":"visible","helpful_count":0,"date_published":"2026-10-12"},{"id":"rev_8811","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_l_charcoal","review_… (+900자) ``

**답변 1**
> The Wool overcoat `prd_wool_overcoat` is not showing a systematic “runs small” pattern in the visible reviews.
>
> * Reviews: 41 visible
> * Average rating: 4.6 / 5
>
> Fit votes from those reviews:
> * True to size: 29 votes
> * A bit snug / runs small: 12 votes
> * Runs large: 0 votes
>
> The most repeated mention is “size up for a hoodie” – 9 mentions. Sample reviewer language:
>
> * “Size up if you wear a hoodie underneath. Warm, sharp, and the wool feels solid.” – Jordan P., L, 180 cm, 5★, 2026-10-12
> * “True to size over a shirt or a thin sweater; size up for a hoodie.” – Alex D., L, 176 cm, 5★, 2026-08-27
> * “A bit snug across the chest and shoulders, fine over a shirt.” – Tim G., L, 180 cm, 4★, 2026-09-30
>
> So ~71% of reviewers call it true to size and 29% call it a bit snug. No reviewer voted runs large. The snug reports cluster around wearing it over thicker layers; reviewers who wear it over a shirt/thin sweater tend to say true to size.
>
> Measurements on file, garment laid flat:
> * M: chest 56 cm, shoulder 46 cm, sleeve 64 cm, length 98 cm
> * L: chest 59 cm, shoulder 48 cm, sleeve 65.5 cm, length 100 cm
> How measured: Chest is armpit to armpit; length is from the highest point of the shoulder.
>
> If you plan to layer with a hoodie, the review consensus is to size up; for a shirt or thin sweater the current size is generally reported as true to size.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)
