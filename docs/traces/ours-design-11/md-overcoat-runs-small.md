# md-overcoat-runs-small — ours-design-11

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `d86a1ff` · a2api `140fda2`

**과업**

> people keep saying the wool overcoat runs small. is that actually true?

- 필요한 도구: `get_review_summary`
- 허용 도구: `search_products`, `list_reviews`, `get_product_measurements`
- 답에 있어야 할 사실: 41 reviews, average 4.6
- 답에 있어야 할 사실: 29 say true to size, 12 say a bit snug, none say it runs large
- 답에 있어야 할 사실: the most common phrase is 'size up for a hoodie' (9 mentions), so the snug votes come from layering

### a2api-acom-names-batch · 1회차 · ✓ 통과

토큰 72,759 · 54.466초 · 모델 호출 10회 · 도구 호출 9회 · 첫 요청 프롬프트 1,984토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_product","get_product_measurements","list_reviews","get_review_summary"]} ``
   ← 결과 107B: `` {"loaded":["search_products","get_product","get_product_measurements","list_reviews","get_review_summary"]} ``
2. 모델 → **`search_products`** `` {"query":"wool overcoat","limit":20} ``
   ← 결과 5,999B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_wool_overcoat-b50a91c0.webp","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"ava… (+900자) ``
3. 모델 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat","sample_limit":5} ``
   ← 결과 1,312B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":null},"review_count":41,"rating_value":4.6,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":29},{"fit":"runs_small","label":"A bit snug","count":12},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[{"text":"size up for a hoodie","count":9}],"sample":[{"review_id":"rev_8812","review_rating":5,"size_bought":"L","height_cm":180,"excerpt":"Size up if you wear a hoodie underneath.","date_published":"2026-10-12"},{"review_id":"rev_8807","review_ra… (+712자) ``
4. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 380B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","unit":"cm","measurements":["chest","shoulder","sleeve","length"],"sizes":[{"size":"M","chest":56,"shoulder":46,"sleeve":64,"length":98},{"size":"L","chest":59,"shoulder":48,"sleeve":65.5,"length":100}],"how_measured":"Garment laid flat. Chest is armpit to armpit; length is from the highest point of the shoulder."}} ``
5. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat","sizes":["S","XL"]} ``
   ← 실패 292B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) The size chart has no size S. Next: get_product."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
6. 모델 → **`get_product`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 1,400B: `` {"status":"succeeded","data":{"id":"prd_wool_overcoat","@type":"ProductGroup","name":"Wool overcoat","description":"A single-breasted overcoat in a 70% wool blend, cut to fit over a sweater.","brand_id":"brn_northwind","category_id":"cat_outerwear","keywords":[],"approval_status":"active","varies_by":["color","size"],"image":"/media/products/prd_wool_overcoat-b50a91c0.webp","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","additional_property":[{"name":"material","value":"70% wool, 30% polyamide"}],"has_variant":[{"variant_id"… (+800자) ``
7. 모델 → **`a2api_batch`** `` {"calls":[{"name":"get_review_summary","arguments":{"product_id":"prd_wool_overcoat","size":"M","sample_limit":3}},{"name":"get_review_summary","arguments":{"product_id":"prd_wool_overcoat","size":"L","sample_limit":3}},{"name":"get_review_summary","arguments":{"product_id":"prd_wool_overcoat","size":"S","sample_limit":3}}]} ``
   ← 결과 2,263B: `` {"batch":[{"name":"get_review_summary","result":{"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":"M"},"review_count":15,"rating_value":4.9,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":15},{"fit":"runs_small","label":"A bit snug","count":0},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[],"sample":[{"review_id":"rev_8810","review_rating":5,"size_bought":"M","height_cm":177,"excerpt":"True to size and the charcoal is a deep, even color.","date_published":"2026-09-22"},{"review_id":"rev… (+900자) ``
8. 모델 → **`list_reviews`** `` {"product_id":"prd_wool_overcoat","status":"visible","limit":100} ``
   ← 결과 4,122B: `` {"status":"succeeded","data":{"items":[{"id":"rev_8812","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_l_charcoal","review_rating":5,"author":{"@type":"Person","name":"Jordan P."},"review_body":"Size up if you wear a hoodie underneath. Warm, sharp, and the wool feels solid.","fit":"true_to_size","height_cm":180,"size_bought":"L","image":[],"mentions":["size up for a hoodie"],"status":"visible","helpful_count":0,"date_published":"2026-10-12"},{"id":"rev_8811","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_l_charcoal","review_… (+900자) ``
9. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat","sizes":["XL"]} ``
   ← 실패 293B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) The size chart has no size XL. Next: get_product."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``

**답변 1**
> The Wool overcoat `prd_wool_overcoat` is not generally “runs small” in the aggregate, but the fit feedback is size-dependent.
>
> **Overall fit votes from 41 visible reviews**
> * Rating: 4.6 / 5
> * Fit votes
>   * True to size: 29
>   * A bit snug / runs small: 12
>   * Runs large: 0
> * Repeated mention: “size up for a hoodie” – 9 mentions
>
> **By size**
>
> * Size M – 15 reviews, rating 4.9
>   * True to size: 15
>   * Runs small: 0
>   * Runs large: 0
>   * Sample: “True to size and the charcoal is a deep, even color.” – Mo N., 177 cm, 2026-09-22; “Fits true to size, sleeves the right length.” – Gus L., 182 cm, 2026-09-13
>
> * Size L – 26 reviews, rating 4.4
>   * True to size: 14
>   * Runs small: 12
>   * Runs large: 0
>   * Repeated theme: true to size over a shirt / thin sweater, size up for a hoodie.
>   * Sample: “Size up if you wear a hoodie underneath.” – Jordan P., 180 cm, 2026-10-12; “True to size over a shirt or a thin sweater; size up for a hoodie.” – Alex D., 176 cm, 2026-08-27
>   * Snug reports: “A bit snug across the chest and shoulders, fine over a shirt.” – Tim G., 180 cm, 2026-09-30; Andy F., 179 cm, 2026-09-05
>
> No visible reviews were found for size S in the review summary, and the size chart returned by `get_product_measurements` only contains M and L:
>
> * Garment laid flat, cm
>   * M: chest 56, shoulder 46, sleeve 64, length 98
>   * L: chest 59, shoulder 48, sleeve 65.5, length 100
>   * How measured: “Garment laid flat. Chest is armpit to armpit; length is from the highest point of the shoulder.”
>
> Measurements for S and XL are not present in the size chart, so they can’t be compared here.
>
> Takeaway: The coat is reported true to size for M buyers. For L buyers the coat is split ~54% true to size / 46% a bit snug, with the snugness most often noted when layering over a hoodie. That’s why you hear “runs small” – it’s really a layering / L-size effect, not a blanket small sizing.

**채점**: ✓ 통과
(도구 정밀도 0.90, 재현율 1.00)

### a2api-acom-names-batch · 2회차 · ✓ 통과

토큰 72,759 · 53.592초 · 모델 호출 10회 · 도구 호출 9회 · 첫 요청 프롬프트 1,984토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_product","get_product_measurements","list_reviews","get_review_summary"]} ``
   ← 결과 107B: `` {"loaded":["search_products","get_product","get_product_measurements","list_reviews","get_review_summary"]} ``
2. 모델 → **`search_products`** `` {"query":"wool overcoat","limit":20} ``
   ← 결과 5,999B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_wool_overcoat-b50a91c0.webp","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"ava… (+900자) ``
3. 모델 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat","sample_limit":5} ``
   ← 결과 1,312B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":null},"review_count":41,"rating_value":4.6,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":29},{"fit":"runs_small","label":"A bit snug","count":12},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[{"text":"size up for a hoodie","count":9}],"sample":[{"review_id":"rev_8812","review_rating":5,"size_bought":"L","height_cm":180,"excerpt":"Size up if you wear a hoodie underneath.","date_published":"2026-10-12"},{"review_id":"rev_8807","review_ra… (+712자) ``
4. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 380B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","unit":"cm","measurements":["chest","shoulder","sleeve","length"],"sizes":[{"size":"M","chest":56,"shoulder":46,"sleeve":64,"length":98},{"size":"L","chest":59,"shoulder":48,"sleeve":65.5,"length":100}],"how_measured":"Garment laid flat. Chest is armpit to armpit; length is from the highest point of the shoulder."}} ``
5. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat","sizes":["S","XL"]} ``
   ← 실패 292B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) The size chart has no size S. Next: get_product."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
6. 모델 → **`get_product`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 1,400B: `` {"status":"succeeded","data":{"id":"prd_wool_overcoat","@type":"ProductGroup","name":"Wool overcoat","description":"A single-breasted overcoat in a 70% wool blend, cut to fit over a sweater.","brand_id":"brn_northwind","category_id":"cat_outerwear","keywords":[],"approval_status":"active","varies_by":["color","size"],"image":"/media/products/prd_wool_overcoat-b50a91c0.webp","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","additional_property":[{"name":"material","value":"70% wool, 30% polyamide"}],"has_variant":[{"variant_id"… (+800자) ``
7. 모델 → **`a2api_batch`** `` {"calls":[{"name":"get_review_summary","arguments":{"product_id":"prd_wool_overcoat","size":"M","sample_limit":3}},{"name":"get_review_summary","arguments":{"product_id":"prd_wool_overcoat","size":"L","sample_limit":3}},{"name":"get_review_summary","arguments":{"product_id":"prd_wool_overcoat","size":"S","sample_limit":3}}]} ``
   ← 결과 2,263B: `` {"batch":[{"name":"get_review_summary","result":{"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":"M"},"review_count":15,"rating_value":4.9,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":15},{"fit":"runs_small","label":"A bit snug","count":0},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[],"sample":[{"review_id":"rev_8810","review_rating":5,"size_bought":"M","height_cm":177,"excerpt":"True to size and the charcoal is a deep, even color.","date_published":"2026-09-22"},{"review_id":"rev… (+900자) ``
8. 모델 → **`list_reviews`** `` {"product_id":"prd_wool_overcoat","status":"visible","limit":100} ``
   ← 결과 4,122B: `` {"status":"succeeded","data":{"items":[{"id":"rev_8812","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_l_charcoal","review_rating":5,"author":{"@type":"Person","name":"Jordan P."},"review_body":"Size up if you wear a hoodie underneath. Warm, sharp, and the wool feels solid.","fit":"true_to_size","height_cm":180,"size_bought":"L","image":[],"mentions":["size up for a hoodie"],"status":"visible","helpful_count":0,"date_published":"2026-10-12"},{"id":"rev_8811","@type":"Review","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_l_charcoal","review_… (+900자) ``
9. 모델 → **`get_product_measurements`** `` {"product_id":"prd_wool_overcoat","sizes":["XL"]} ``
   ← 실패 293B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) The size chart has no size XL. Next: get_product."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``

**답변 1**
> The Wool overcoat `prd_wool_overcoat` is not generally “runs small” in the aggregate, but the fit feedback is size-dependent.
>
> **Overall fit votes from 41 visible reviews**
> * Rating: 4.6 / 5
> * Fit votes
>   * True to size: 29
>   * A bit snug / runs small: 12
>   * Runs large: 0
> * Repeated mention: “size up for a hoodie” – 9 mentions
>
> **By size**
>
> * Size M – 15 reviews, rating 4.9
>   * True to size: 15
>   * Runs small: 0
>   * Runs large: 0
>   * Sample: “True to size and the charcoal is a deep, even color.” – Mo N., 177 cm, 2026-09-22; “Fits true to size, sleeves the right length.” – Gus L., 182 cm, 2026-09-13
>
> * Size L – 26 reviews, rating 4.4
>   * True to size: 14
>   * Runs small: 12
>   * Runs large: 0
>   * Repeated theme: true to size over a shirt / thin sweater, size up for a hoodie.
>   * Sample: “Size up if you wear a hoodie underneath.” – Jordan P., 180 cm, 2026-10-12; “True to size over a shirt or a thin sweater; size up for a hoodie.” – Alex D., 176 cm, 2026-08-27
>   * Snug reports: “A bit snug across the chest and shoulders, fine over a shirt.” – Tim G., 180 cm, 2026-09-30; Andy F., 179 cm, 2026-09-05
>
> No visible reviews were found for size S in the review summary, and the size chart returned by `get_product_measurements` only contains M and L:
>
> * Garment laid flat, cm
>   * M: chest 56, shoulder 46, sleeve 64, length 98
>   * L: chest 59, shoulder 48, sleeve 65.5, length 100
>   * How measured: “Garment laid flat. Chest is armpit to armpit; length is from the highest point of the shoulder.”
>
> Measurements for S and XL are not present in the size chart, so they can’t be compared here.
>
> Takeaway: The coat is reported true to size for M buyers. For L buyers the coat is split ~54% true to size / 46% a bit snug, with the snugness most often noted when layering over a hoodie. That’s why you hear “runs small” – it’s really a layering / L-size effect, not a blanket small sizing.

**채점**: ✓ 통과
(도구 정밀도 0.90, 재현율 1.00)
