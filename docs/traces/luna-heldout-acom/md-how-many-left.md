# md-how-many-left — luna-heldout-acom

[← 실행 묶음](README.md)

**과업**

> How many Light rain parka remain in my inventory?

- 답에 있어야 할 사실: 4 in total: S 2, M 0, L 0, XL 2 (all Stone)
- 답에 있어야 할 사실: S and XL are at their safety stock of 2, so the parka is effectively sold out for new sales planning

### GPT-6-Luna · A-Commerce 도구(참고) · 1회차 · ✗ 실패

토큰 17,245 · 모델 호출 2회 · 도구 호출 1회

**질문 1**
> How many Light rain parka remain in my inventory?

- 라우팅: Catalog agent (the request names this agent's work)
- 도구 검색 후보: 13 candidates: search_products, get_product, get_inventory, list_tasks, compare_products, get_category, list_categories, set_variant_stock, suggest_reorder, create_reorder, receive_reorder, generate_image, get_review_summary
- 계획: `search_products` `` {"limit":10,"query":"Light rain parka"} ``
1. 에이전트 → **`search_products`** `` {"limit":10,"query":"Light rain parka"} ``
   ← 결과: `` {"items":[{"id":"prd_rain_parka","cost":50.0,"name":"Light rain parka","image":"/media/products/prd_rain_parka-01f49e29.webp","price":118.0,"brand_id":"brn_northwind","category_id":"cat_summer_outerwear","has_variant":[{"sku":"rp-stone-s","size":"S","color":"Stone","variant_id":"var_rain_parka_s_stone","availability":"in_stock","inventory_level":2},{"sku":"rp-stone-m","size":"M","color":"Stone","variant_id":"var_rain_parka_m_stone","availability":"out_of_stock","inventory_level":0},{"sku":"rp-stone-l","size":"L","color":"Stone","variant_id":"var_rain_parka_l_stone","availability":"out_of_stock… (+18,570자) ``

**답변 1**
> There are 4 Light rain parkas in inventory: 2 size S and 2 size XL. Sizes M and L are out of stock.

화면 블록: product_table(10 of 120)

**채점**: ✗ 실패 — 빠진 것: tool get_inventory; fact "4 in total: S 2, M 0, L 0, XL 2 (all Stone)" (0, 0 not shown)

### GPT-6-Luna · A-Commerce 도구(참고) · 2회차 · ✗ 실패

토큰 17,241 · 모델 호출 2회 · 도구 호출 1회

**질문 1**
> How many Light rain parka remain in my inventory?

- 라우팅: Catalog agent (the request names this agent's work)
- 도구 검색 후보: 13 candidates: search_products, get_product, get_inventory, list_tasks, compare_products, get_category, list_categories, set_variant_stock, suggest_reorder, create_reorder, receive_reorder, generate_image, get_review_summary
- 계획: `search_products` `` {"limit":10,"query":"Light rain parka"} ``
1. 에이전트 → **`search_products`** `` {"limit":10,"query":"Light rain parka"} ``
   ← 결과: `` {"items":[{"id":"prd_rain_parka","cost":50.0,"name":"Light rain parka","image":"/media/products/prd_rain_parka-01f49e29.webp","price":118.0,"brand_id":"brn_northwind","category_id":"cat_summer_outerwear","has_variant":[{"sku":"rp-stone-s","size":"S","color":"Stone","variant_id":"var_rain_parka_s_stone","availability":"in_stock","inventory_level":2},{"sku":"rp-stone-m","size":"M","color":"Stone","variant_id":"var_rain_parka_m_stone","availability":"out_of_stock","inventory_level":0},{"sku":"rp-stone-l","size":"L","color":"Stone","variant_id":"var_rain_parka_l_stone","availability":"out_of_stock… (+18,570자) ``

**답변 1**
> There are 4 Light rain parkas in inventory: 2 size S and 2 size XL. Sizes M and L are out of stock.

화면 블록: product_table(10 of 120)

**채점**: ✗ 실패 — 빠진 것: tool get_inventory; fact "4 in total: S 2, M 0, L 0, XL 2 (all Stone)" (0, 0 not shown)

### GPT-6-Luna · A-Commerce 도구(참고) · 3회차 · ✗ 실패

토큰 27,190 · 모델 호출 2회 · 도구 호출 2회

**질문 1**
> How many Light rain parka remain in my inventory?

- 라우팅: Catalog agent (the request names this agent's work)
- 도구 검색 후보: 13 candidates: search_products, get_product, get_inventory, list_tasks, compare_products, get_category, list_categories, set_variant_stock, suggest_reorder, create_reorder, receive_reorder, generate_image, get_review_summary
- 계획: `search_products` `` {"limit":100,"query":"Light rain parka"} ``; `get_inventory` `` {} ``
1. 에이전트 → **`search_products`** `` {"limit":100,"query":"Light rain parka"} ``
   ← 결과: `` {"items":[{"id":"prd_rain_parka","cost":50.0,"name":"Light rain parka","image":"/media/products/prd_rain_parka-01f49e29.webp","price":118.0,"brand_id":"brn_northwind","category_id":"cat_summer_outerwear","has_variant":[{"sku":"rp-stone-s","size":"S","color":"Stone","variant_id":"var_rain_parka_s_stone","availability":"in_stock","inventory_level":2},{"sku":"rp-stone-m","size":"M","color":"Stone","variant_id":"var_rain_parka_m_stone","availability":"out_of_stock","inventory_level":0},{"sku":"rp-stone-l","size":"L","color":"Stone","variant_id":"var_rain_parka_l_stone","availability":"out_of_stock… (+175,671자) ``
2. 에이전트 → **`get_inventory`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과: `` {"reorders":[],"variants":[{"sku":"rp-stone-s","size":"S","color":"Stone","on_order":0,"variant_id":"var_rain_parka_s_stone","acom:managed":true,"availability":"in_stock","inventory_level":2,"acom:safety_stock":2},{"sku":"rp-stone-m","size":"M","color":"Stone","on_order":0,"variant_id":"var_rain_parka_m_stone","acom:managed":true,"availability":"out_of_stock","inventory_level":0,"acom:safety_stock":2},{"sku":"rp-stone-l","size":"L","color":"Stone","on_order":0,"variant_id":"var_rain_parka_l_stone","acom:managed":true,"availability":"out_of_stock","inventory_level":0,"acom:safety_stock":2},{"sk… (+263자) ``

**답변 1**
> There are 4 Light rain parkas in inventory: 2 size S and 2 size XL. Sizes M and L are out of stock.

화면 블록: product_table(100 of 120)

**채점**: ✗ 실패 — 빠진 것: fact "4 in total: S 2, M 0, L 0, XL 2 (all Stone)" (0, 0 not shown)
