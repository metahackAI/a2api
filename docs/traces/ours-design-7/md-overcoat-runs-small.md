# md-overcoat-runs-small — ours-design-7

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> people keep saying the wool overcoat runs small. is that actually true?

- 필요한 도구: `get_review_summary`
- 허용 도구: `search_products`, `list_reviews`, `get_product_measurements`
- 답에 있어야 할 사실: 41 reviews, average 4.6
- 답에 있어야 할 사실: 29 say true to size, 12 say a bit snug, none say it runs large
- 답에 있어야 할 사실: the most common phrase is 'size up for a hoodie' (9 mentions), so the snug votes come from layering

### a2api-acom · 1회차 · ✓ 통과

토큰 9,667 · 11.093초 · 모델 호출 2회 · 도구 호출 1회 · 첫 요청 프롬프트 4,360토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

1. 모델 → **`acom_get_review_summary`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 940B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":null},"review_count":41,"rating_value":4.6,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":29},{"fit":"runs_small","label":"A bit snug","count":12},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[{"text":"size up for a hoodie","count":9}],"sample":[{"review_id":"rev_8812","review_rating":5,"size_bought":"L","height_cm":180,"excerpt":"Size up if you wear a hoodie underneath.","date_published":"2026-10-12"},{"review_id":"rev_8807","review_ra… (+340자) ``

**답변 1**
> The wool overcoat isn’t broadly “runs small” in the reviews.
>
> * 41 reviews total, average rating 4.6
> * Fit votes:
>   * True to size: 29
>   * A bit snug / runs small: 12
>   * Runs large: 0
>
> The repeated theme is layering, not a general small sizing. The top mention is “size up for a hoodie” – 9 reviewers repeat it.
>
> Sample evidence:
> * rev_8812 – 5★, L, 180 cm: “Size up if you wear a hoodie underneath.”
> * rev_8807 – 5★, L, 176 cm: “True to size over a shirt or a thin sweater; size up for a hoodie.”
> * rev_8803 – 5★, L, 180 cm: “True to size over a shirt or a thin sweater; size up for a hoodie.”
>
> So most shoppers find it true to size for a shirt/thin sweater, with ~29% reporting it runs a bit snug and commonly recommending sizing up when layering.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom · 2회차 · ✓ 통과

토큰 9,740 · 12.19초 · 모델 호출 2회 · 도구 호출 1회 · 첫 요청 프롬프트 4,360토큰

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

### a2api-acom-index · 1회차 · ✓ 통과

토큰 38,163 · 17.478초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 6,989토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_review_summary","get_product"]} ``
   ← 결과 65B: `` {"loaded":["search_products","get_review_summary","get_product"]} ``
2. 모델 → **`search_products`** `` {"query":"wool overcoat","limit":20} ``
   ← 결과 5,925B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/garment/chore-charcoal.svg","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"availability":"in… (+900자) ``
3. 모델 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat","sample_limit":3} ``
   ← 결과 940B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":null},"review_count":41,"rating_value":4.6,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":29},{"fit":"runs_small","label":"A bit snug","count":12},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[{"text":"size up for a hoodie","count":9}],"sample":[{"review_id":"rev_8812","review_rating":5,"size_bought":"L","height_cm":180,"excerpt":"Size up if you wear a hoodie underneath.","date_published":"2026-10-12"},{"review_id":"rev_8807","review_ra… (+340자) ``

**답변 1**
> The Wool overcoat **prd_wool_overcoat** is not consistently reported as running small.
>
> From 41 reviews in the system:
> * **Fit votes**
>   * True to size: 29
>   * A bit snug / runs small: 12
>   * Runs large: 0
> * Overall rating: 4.6 / 5
>
> The recurring theme is layering, not a general small sizing. The top mention is “size up for a hoodie” – 9 times. Sample reviews:
>
> * “Size up if you wear a hoodie underneath.” – 5★, size L, 180 cm, 2026-10-12
> * “True to size over a shirt or a thin sweater; size up for a hoodie.” – 5★, size L, 176 cm, 2026-08-27
>
> So most shoppers find it true to size for a shirt/thin sweater, and the 12 “runs small” votes are largely about it feeling snug when layered. No reviewers voted runs large.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-index · 2회차 · ✓ 통과

토큰 74,494 · 30.871초 · 모델 호출 7회 · 도구 호출 6회 · 첫 요청 프롬프트 6,989토큰

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
> The Wool overcoat (prd_wool_overcoat) is not generally reported as running small.
>
> Review summary for the product, 41 reviews, 4.6 ★:
>
> * Fit votes
>   * True to size: 29 votes
>   * A bit snug / runs small: 12 votes
>   * Runs large: 0 votes
>
> So ~71% of reviewers say true to size and ~29% say it runs a bit snug. No “runs large” votes.
>
> The repeated theme is layering, not a systematic small sizing:
> * Mentions: “size up for a hoodie” – 9 times
> * Sample reviews:
>   * rev_8812 – 5★, size L, 180 cm: “Size up if you wear a hoodie underneath.”
>   * rev_8807 – 5★, size L, 176 cm: “True to size over a shirt or a thin sweater; size up for a hoodie.”
>   * rev_8803 – 5★, size L, 180 cm: “True to size over a shirt or a thin sweater; size up for a hoodie.”
>
> Product description: “A single-breasted overcoat in a 70% wool blend, cut to fit over a sweater.”
>
> Measurements on file, garment laid flat, chest armpit-to-armpit; length from highest point of shoulder:
> * M: chest 56 cm, shoulder 46 cm, sleeve 64 cm, length 98 cm
> * L: chest 59 cm, shoulder 48 cm, sleeve 65.5 cm, length 100 cm
>
> S and XL are not in the size chart returned by the system.
>
> In practice reviewers find it true to size for a shirt/thin sweater and recommend sizing up only when you want to wear a hoodie underneath.

**채점**: ✓ 통과
(도구 정밀도 0.80, 재현율 1.00)

### a2api-acom-graph · 1회차 · ✓ 통과

토큰 46,639 · 17.88초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 6,989토큰

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

**답변 1**
> Yes — there’s a real pattern, but it’s not “runs small” for everyone.
>
> **Wool overcoat — prd_wool_overcoat**
> * 41 reviews, average rating 4.6/5
> * Fit votes
>   * True to size: 29 votes
>   * A bit snug / runs small: 12 votes
>   * Runs large: 0 votes
>
> The repeated theme is layering. The top mention is “size up for a hoodie” — 9 reviewers note it.
>
> Sample evidence:
> * “Size up if you wear a hoodie underneath.” — 5★, size L, 180 cm, 2026-10-12
> * “True to size over a shirt or a thin sweater; size up for a hoodie.” — 5★, size L, 176 cm, 2026-08-27
> * “True to size over a shirt or a thin sweater; size up for a hoodie.” — 5★, size L, 180 cm, 2026-07-24
>
> So the coat is generally true to size for a shirt/thin sweater, and ~29% of reviewers find it a bit snug. Most of the “runs small” feedback is about wanting extra room for heavier layers.
>
> Measurements, garment laid flat:
> * M: chest 56 cm, shoulder 46 cm, sleeve 64 cm, length 98 cm
> * L: chest 59 cm, shoulder 48 cm, sleeve 65.5 cm, length 100 cm
> How measured: chest is armpit to armpit; length is from the highest point of the shoulder.
>
> If you plan to wear it over a hoodie or thick knit, sizing up is the common recommendation.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-graph · 2회차 · ✓ 통과

토큰 35,800 · 16.398초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 6,989토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_review_summary","get_product"]} ``
   ← 결과 65B: `` {"loaded":["search_products","get_review_summary","get_product"]} ``
2. 모델 → **`search_products`** `` {"query":"wool overcoat","limit":20} ``
   ← 결과 1,847B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/garment/chore-charcoal.svg","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"availability":"in… (+900자) ``
3. 모델 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat","sample_limit":3} ``
   ← 결과 1,101B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":null},"review_count":41,"rating_value":4.6,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":29},{"fit":"runs_small","label":"A bit snug","count":12},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[{"text":"size up for a hoodie","count":9}],"sample":[{"review_id":"rev_8812","review_rating":5,"size_bought":"L","height_cm":180,"excerpt":"Size up if you wear a hoodie underneath.","date_published":"2026-10-12"},{"review_id":"rev_8807","review_ra… (+501자) ``

**답변 1**
> The Wool overcoat **prd_wool_overcoat** is not generally reported as running small.
>
> Review summary from 41 reviews:
> * Rating: 4.6 / 5
> * Fit votes
>   * True to size: 29
>   * A bit snug / runs small: 12
>   * Runs large: 0
>
> So ~71% of reviewers say true to size and ~29% say it runs a bit snug. No reviewers voted runs large.
>
> The repeated mention is “size up for a hoodie” – 9 mentions – with sample reviews noting:
> * “Size up if you wear a hoodie underneath.” – L, 180 cm, 5★, 2026-10-12
> * “True to size over a shirt or a thin sweater; size up for a hoodie.” – L, 176 cm, 5★, 2026-08-27
>
> In practice it’s true to size for light layering, and reviewers recommend sizing up when you plan to wear a hoodie underneath.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names · 1회차 · ✓ 통과

토큰 28,547 · 31.055초 · 모델 호출 6회 · 도구 호출 5회 · 첫 요청 프롬프트 1,630토큰

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

### a2api-acom-names · 2회차 · ✓ 통과

토큰 27,716 · 32.433초 · 모델 호출 6회 · 도구 호출 5회 · 첫 요청 프롬프트 1,630토큰

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
5. 모델 → **`get_product`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 1,244B: `` {"status":"succeeded","data":{"id":"prd_wool_overcoat","@type":"ProductGroup","name":"Wool overcoat","description":"A single-breasted overcoat in a 70% wool blend, cut to fit over a sweater.","brand_id":"brn_northwind","category_id":"cat_outerwear","keywords":[],"approval_status":"active","varies_by":["color","size"],"image":"/media/garment/chore-charcoal.svg","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","additional_property":[{"name":"material","value":"70% wool, 30% polyamide"}],"has_variant":[{"variant_id":"var_wool_ove… (+644자) ``

**답변 1**
> The Wool overcoat `prd_wool_overcoat` is not generally reported as running small.
>
> Review summary for the product, 41 reviews total, rating 4.6/5:
>
> * Fit votes
>   * True to size: 29
>   * A bit snug / runs small: 12
>   * Runs large: 0
>
> The most repeated mention is “size up for a hoodie” – 9 mentions.
>
> Sample evidence:
> * rev_8812 – 5★, size L, 180 cm – “Size up if you wear a hoodie underneath.”
> * rev_8807 – 5★, size L, 176 cm – “True to size over a shirt or a thin sweater; size up for a hoodie.”
> * rev_8803 – 5★, size L, 180 cm – “True to size over a shirt or a thin sweater; size up for a hoodie.”
>
> So the majority find it true to size, with ~29% of reviewers finding it a bit snug. The snug reports are most common when layering over a hoodie/sweater. The product description notes it is “cut to fit over a sweater”.
>
> Current stock: 24 units in stock, Charcoal S 5, M 7, L 8, XL 4. List price $289.00 USD.
>
> Measurements on file, garment laid flat:
> * M: chest 56 cm, shoulder 46 cm, sleeve 64 cm, length 98 cm
> * L: chest 59 cm, shoulder 48 cm, sleeve 65.5 cm, length 100 cm
> How measured: Chest is armpit to armpit; length is from the highest point of the shoulder.

**채점**: ✓ 통과
(도구 정밀도 0.75, 재현율 1.00)
