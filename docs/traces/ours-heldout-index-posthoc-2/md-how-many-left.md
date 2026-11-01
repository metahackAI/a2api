# md-how-many-left — ours-heldout-index-posthoc-2

[← 실행 묶음](README.md) · 세트 `held_out` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> How many Light rain parka remain in my inventory?

- 필요한 도구: `get_inventory`
- 허용 도구: `search_products`
- 답에 있어야 할 사실: 4 in total: S 2, M 0, L 0, XL 2 (all Stone)
- 답에 있어야 할 사실: S and XL are at their safety stock of 2, so the parka is effectively sold out for new sales planning

### a2api-acom · 1회차 · ✓ 통과

토큰 21,223 · 17.223초 · 모델 호출 4회 · 도구 호출 5회 · 첫 요청 프롬프트 2,055토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> How many Light rain parka remain in my inventory?

1. 모델 → **`a2api_search`** `` {"query":"inventory product stock remaining"} ``
   ← 결과 375B: `` {"selected":[{"name":"acom_get_inventory","id":"acom.get_inventory"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_get_product_group","id":"acom.get_product_group"},{"name":"acom_update_product","id":"acom.update_product"},{"name":"acom_get_product","id":"acom.get_product"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"product inventory count"} ``
   ← 결과 447B: `` {"selected":[{"name":"acom_get_inventory","id":"acom.get_inventory"},{"name":"acom_get_review_summary","id":"acom.get_review_summary"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_generate_image","id":"acom.generate_image"},{"name":"acom_get_customer_overview","id":"acom.get_customer_overview"}],"evicted":["acom_get_category","acom_get_tenant"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`a2api_search`** `` {"query":"Light rain parka product"} ``
   ← 결과 509B: `` {"selected":[{"name":"acom_compare_products","id":"acom.compare_products"},{"name":"acom_reject_product","id":"acom.reject_product"},{"name":"acom_discontinue_product","id":"acom.discontinue_product"}],"omitted":[{"id":"acom.create_product","reason":"SCHEMA_BUDGET"},{"id":"acom.search_product_groups","reason":"SCHEMA_BUDGET"}],"evicted":["acom_list_orgs","acom_get_campaign","acom_get_coupon","acom_get_promotion","acom_list_policies"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`acom_search_products`** `` {"query":"Light rain parka"} ``
   ← 결과 2,692B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/parka-stone.svg","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_stock"},{"variant… (+900자) ``
5. 모델 → **`acom_get_inventory`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 893B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","inventory_level":4,"availability":"in_stock","variants":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"acom:safety_stock":2,"acom:managed":true,"availability":"out_of_stock","on_order":0},{"variant_id":"var_rain_parka_l_stone","sku":"rp-stone-l","size":"L","color":"Stone","inventory_level":0… (+293자) ``

**답변 1**
> Light rain parka — **prd_rain_parka**
> * Total sellable stock: **4 units** — availability in_stock
>
> Variant breakdown:
> * var_rain_parka_s_stone — S / Stone — inventory_level 2 — in_stock — safety_stock 2
> * var_rain_parka_m_stone — M / Stone — inventory_level 0 — out_of_stock — safety_stock 2
> * var_rain_parka_l_stone — L / Stone — inventory_level 0 — out_of_stock — safety_stock 2
> * var_rain_parka_xl_stone — XL / Stone — inventory_level 2 — in_stock — safety_stock 2
>
> On order: 0 for all variants.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom · 2회차 · ✓ 통과

토큰 21,207 · 18.916초 · 모델 호출 4회 · 도구 호출 5회 · 첫 요청 프롬프트 2,055토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> How many Light rain parka remain in my inventory?

1. 모델 → **`a2api_search`** `` {"query":"inventory product stock"} ``
   ← 결과 375B: `` {"selected":[{"name":"acom_get_inventory","id":"acom.get_inventory"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_get_product_group","id":"acom.get_product_group"},{"name":"acom_update_product","id":"acom.update_product"},{"name":"acom_get_product","id":"acom.get_product"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"product inventory count"} ``
   ← 결과 447B: `` {"selected":[{"name":"acom_get_inventory","id":"acom.get_inventory"},{"name":"acom_get_review_summary","id":"acom.get_review_summary"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_generate_image","id":"acom.generate_image"},{"name":"acom_get_customer_overview","id":"acom.get_customer_overview"}],"evicted":["acom_get_category","acom_get_tenant"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`a2api_search`** `` {"query":"Light rain parka"} ``
   ← 결과 215B: `` {"selected":[{"name":"acom_compare_products","id":"acom.compare_products"}],"evicted":["acom_list_orgs","acom_get_campaign","acom_get_coupon"],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`acom_search_products`** `` {"query":"Light rain parka","limit":20} ``
   ← 결과 2,692B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/parka-stone.svg","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_stock"},{"variant… (+900자) ``
5. 모델 → **`acom_get_inventory`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 893B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","inventory_level":4,"availability":"in_stock","variants":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"acom:safety_stock":2,"acom:managed":true,"availability":"out_of_stock","on_order":0},{"variant_id":"var_rain_parka_l_stone","sku":"rp-stone-l","size":"L","color":"Stone","inventory_level":0… (+293자) ``

**답변 1**
> Light rain parka — **prd_rain_parka**
>
> Total sellable stock: **4 units**
>
> * var_rain_parka_s_stone — S / Stone: 2 in stock, availability in_stock
> * var_rain_parka_m_stone — M / Stone: 0 in stock, availability out_of_stock
> * var_rain_parka_l_stone — L / Stone: 0 in stock, availability out_of_stock
> * var_rain_parka_xl_stone — XL / Stone: 2 in stock, availability in_stock
>
> Product-level inventory_level = 4, availability in_stock. No units on order.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-index · 1회차 · ✓ 통과

토큰 35,507 · 16.142초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 6,985토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> How many Light rain parka remain in my inventory?

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_inventory","get_product"]} ``
   ← 결과 60B: `` {"loaded":["search_products","get_inventory","get_product"]} ``
2. 모델 → **`search_products`** `` {"query":"Light rain parka","limit":20} ``
   ← 결과 2,692B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/parka-stone.svg","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_stock"},{"variant… (+900자) ``
3. 모델 → **`get_inventory`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 893B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","inventory_level":4,"availability":"in_stock","variants":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"acom:safety_stock":2,"acom:managed":true,"availability":"out_of_stock","on_order":0},{"variant_id":"var_rain_parka_l_stone","sku":"rp-stone-l","size":"L","color":"Stone","inventory_level":0… (+293자) ``

**답변 1**
> The Light rain parka is **prd_rain_parka**.
>
> * Total sellable stock: **4 units**
> * Availability: in_stock
>
> Variant breakdown:
> * var_rain_parka_s_stone – S / Stone – 2 in stock, safety stock 2
> * var_rain_parka_m_stone – M / Stone – 0 in stock, out_of_stock, safety stock 2
> * var_rain_parka_l_stone – L / Stone – 0 in stock, out_of_stock, safety stock 2
> * var_rain_parka_xl_stone – XL / Stone – 2 in stock, safety stock 2
>
> So you have 2 × S and 2 × XL remaining; M and L are currently out of stock.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-index · 2회차 · ✓ 통과

토큰 35,508 · 15.281초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 6,985토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> How many Light rain parka remain in my inventory?

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_inventory","get_product"]} ``
   ← 결과 60B: `` {"loaded":["search_products","get_inventory","get_product"]} ``
2. 모델 → **`search_products`** `` {"query":"Light rain parka"} ``
   ← 결과 2,692B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/parka-stone.svg","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_stock"},{"variant… (+900자) ``
3. 모델 → **`get_inventory`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 893B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","inventory_level":4,"availability":"in_stock","variants":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"acom:safety_stock":2,"acom:managed":true,"availability":"out_of_stock","on_order":0},{"variant_id":"var_rain_parka_l_stone","sku":"rp-stone-l","size":"L","color":"Stone","inventory_level":0… (+293자) ``

**답변 1**
> The Light rain parka is **prd_rain_parka**.
>
> * Total sellable stock: **4 units**
> * Availability: in_stock
>
> Variant breakdown:
> * S / Stone – var_rain_parka_s_stone – 2 in stock, safety stock 2
> * M / Stone – var_rain_parka_m_stone – 0 in stock, out_of_stock, safety stock 2
> * L / Stone – var_rain_parka_l_stone – 0 in stock, out_of_stock, safety stock 2
> * XL / Stone – var_rain_parka_xl_stone – 2 in stock, safety stock 2
>
> So you have 2 × S and 2 × XL remaining; M and L are currently out of stock.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names · 1회차 · ✓ 통과

토큰 14,025 · 13.221초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 1,626토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> How many Light rain parka remain in my inventory?

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_inventory","get_product"]} ``
   ← 결과 60B: `` {"loaded":["search_products","get_inventory","get_product"]} ``
2. 모델 → **`search_products`** `` {"query":"Light rain parka"} ``
   ← 결과 2,865B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/parka-stone.svg","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_stock"},{"variant… (+900자) ``
3. 모델 → **`get_inventory`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 1,023B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","inventory_level":4,"availability":"in_stock","variants":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"acom:safety_stock":2,"acom:managed":true,"availability":"out_of_stock","on_order":0},{"variant_id":"var_rain_parka_l_stone","sku":"rp-stone-l","size":"L","color":"Stone","inventory_level":0… (+423자) ``

**답변 1**
> The Light rain parka **prd_rain_parka** has 4 units in stock in total.
>
> * var_rain_parka_s_stone – S / Stone: 2 in stock, availability in_stock
> * var_rain_parka_m_stone – M / Stone: 0 in stock, availability out_of_stock
> * var_rain_parka_l_stone – L / Stone: 0 in stock, availability out_of_stock
> * var_rain_parka_xl_stone – XL / Stone: 2 in stock, availability in_stock
>
> Product total inventory_level = 4, availability = in_stock.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names · 2회차 · ✓ 통과

토큰 14,025 · 12.893초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 1,626토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> How many Light rain parka remain in my inventory?

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_inventory","get_product"]} ``
   ← 결과 60B: `` {"loaded":["search_products","get_inventory","get_product"]} ``
2. 모델 → **`search_products`** `` {"query":"Light rain parka"} ``
   ← 결과 2,865B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/parka-stone.svg","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_stock"},{"variant… (+900자) ``
3. 모델 → **`get_inventory`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 1,023B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","inventory_level":4,"availability":"in_stock","variants":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"acom:safety_stock":2,"acom:managed":true,"availability":"out_of_stock","on_order":0},{"variant_id":"var_rain_parka_l_stone","sku":"rp-stone-l","size":"L","color":"Stone","inventory_level":0… (+423자) ``

**답변 1**
> The Light rain parka `prd_rain_parka` has 4 units in stock total.
>
> * S / Stone `var_rain_parka_s_stone` – 2 in stock, in_stock
> * M / Stone `var_rain_parka_m_stone` – 0 in stock, out_of_stock
> * L / Stone `var_rain_parka_l_stone` – 0 in stock, out_of_stock
> * XL / Stone `var_rain_parka_xl_stone` – 2 in stock, in_stock
>
> Product inventory_level: 4, availability: in_stock.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)
