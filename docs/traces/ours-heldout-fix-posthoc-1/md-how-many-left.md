# md-how-many-left — ours-heldout-fix-posthoc-1

[← 실행 묶음](README.md) · 세트 `held_out` · a-commerce `d86a1ff` · a2api `bb2cb7a`

**과업**

> How many Light rain parka remain in my inventory?

- 필요한 도구: `get_inventory`
- 허용 도구: `search_products`
- 답에 있어야 할 사실: 4 in total: S 2, M 0, L 0, XL 2 (all Stone)
- 답에 있어야 할 사실: S and XL are at their safety stock of 2, so the parka is effectively sold out for new sales planning

### a2api-acom · 1회차 · ✓ 통과

토큰 29,922 · 18.973초 · 모델 호출 4회 · 도구 호출 5회 · 첫 요청 프롬프트 2,055토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> How many Light rain parka remain in my inventory?

1. 모델 → **`a2api_search`** `` {"query":"inventory product stock remaining"} ``
   ← 결과 375B: `` {"selected":[{"name":"acom_get_inventory","id":"acom.get_inventory"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_get_product_group","id":"acom.get_product_group"},{"name":"acom_update_product","id":"acom.update_product"},{"name":"acom_get_product","id":"acom.get_product"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"product inventory count"} ``
   ← 결과 397B: `` {"selected":[{"name":"acom_get_inventory","id":"acom.get_inventory"},{"name":"acom_get_review_summary","id":"acom.get_review_summary"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_generate_image","id":"acom.generate_image"},{"name":"acom_get_customer_overview","id":"acom.get_customer_overview"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`a2api_search`** `` {"query":"Light rain parka product"} ``
   ← 결과 403B: `` {"selected":[{"name":"acom_compare_products","id":"acom.compare_products"},{"name":"acom_reject_product","id":"acom.reject_product"},{"name":"acom_create_product","id":"acom.create_product"},{"name":"acom_discontinue_product","id":"acom.discontinue_product"},{"name":"acom_search_product_groups","id":"acom.search_product_groups"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`acom_search_products`** `` {"query":"Light rain parka","limit":20} ``
   ← 결과 2,722B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_rain_parka-01f49e29.webp","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_sto… (+900자) ``
5. 모델 → **`acom_get_inventory`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 893B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","inventory_level":4,"availability":"in_stock","variants":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"acom:safety_stock":2,"acom:managed":true,"availability":"out_of_stock","on_order":0},{"variant_id":"var_rain_parka_l_stone","sku":"rp-stone-l","size":"L","color":"Stone","inventory_level":0… (+293자) ``

**답변 1**
> Light rain parka — **prd_rain_parka**
>
> * Total sellable stock: **4 units** — availability in_stock
> * Variants
>   * var_rain_parka_s_stone — S / Stone — SKU rp-stone-s — 2 in stock
>   * var_rain_parka_m_stone — M / Stone — SKU rp-stone-m — 0 in stock, out_of_stock
>   * var_rain_parka_l_stone — L / Stone — SKU rp-stone-l — 0 in stock, out_of_stock
>   * var_rain_parka_xl_stone — XL / Stone — SKU rp-stone-xl — 2 in stock
>
> So 4 remain in inventory overall, 2 S and 2 XL.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom · 2회차 · ✓ 통과

토큰 23,697 · 17.306초 · 모델 호출 4회 · 도구 호출 5회 · 첫 요청 프롬프트 2,055토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> How many Light rain parka remain in my inventory?

1. 모델 → **`a2api_search`** `` {"query":"inventory product stock"} ``
   ← 결과 375B: `` {"selected":[{"name":"acom_get_inventory","id":"acom.get_inventory"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_get_product_group","id":"acom.get_product_group"},{"name":"acom_update_product","id":"acom.update_product"},{"name":"acom_get_product","id":"acom.get_product"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"product inventory count"} ``
   ← 결과 397B: `` {"selected":[{"name":"acom_get_inventory","id":"acom.get_inventory"},{"name":"acom_get_review_summary","id":"acom.get_review_summary"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_generate_image","id":"acom.generate_image"},{"name":"acom_get_customer_overview","id":"acom.get_customer_overview"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`a2api_search`** `` {"query":"Light rain parka"} ``
   ← 결과 148B: `` {"selected":[{"name":"acom_compare_products","id":"acom.compare_products"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`acom_search_products`** `` {"query":"Light rain parka"} ``
   ← 결과 2,722B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_rain_parka-01f49e29.webp","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_sto… (+900자) ``
5. 모델 → **`acom_get_inventory`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 893B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","inventory_level":4,"availability":"in_stock","variants":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"acom:safety_stock":2,"acom:managed":true,"availability":"out_of_stock","on_order":0},{"variant_id":"var_rain_parka_l_stone","sku":"rp-stone-l","size":"L","color":"Stone","inventory_level":0… (+293자) ``

**답변 1**
> Light rain parka — **prd_rain_parka**
>
> * Total sellable stock: **4 units** in stock
> * Variant breakdown
>   * var_rain_parka_s_stone – S / Stone: 2 in stock, availability in_stock
>   * var_rain_parka_m_stone – M / Stone: 0 in stock, availability out_of_stock
>   * var_rain_parka_l_stone – L / Stone: 0 in stock, availability out_of_stock
>   * var_rain_parka_xl_stone – XL / Stone: 2 in stock, availability in_stock
>
> So 2 × S and 2 × XL remain; M and L are currently out of stock.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-norelated · 1회차 · ✓ 통과

토큰 15,511 · 14.916초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 1,980토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> How many Light rain parka remain in my inventory?

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_inventory","get_product"]} ``
   ← 결과 60B: `` {"loaded":["search_products","get_inventory","get_product"]} ``
2. 모델 → **`search_products`** `` {"query":"Light rain parka"} ``
   ← 결과 2,722B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_rain_parka-01f49e29.webp","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_sto… (+900자) ``
3. 모델 → **`get_inventory`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 893B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","inventory_level":4,"availability":"in_stock","variants":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"acom:safety_stock":2,"acom:managed":true,"availability":"out_of_stock","on_order":0},{"variant_id":"var_rain_parka_l_stone","sku":"rp-stone-l","size":"L","color":"Stone","inventory_level":0… (+293자) ``

**답변 1**
> Light rain parka — `prd_rain_parka`
>
> * Total sellable stock: **4 units**
> * Availability: in_stock
>
> Variant breakdown:
> * var_rain_parka_s_stone — S / Stone — 2 in stock, safety stock 2
> * var_rain_parka_m_stone — M / Stone — 0 in stock, out_of_stock, safety stock 2
> * var_rain_parka_l_stone — L / Stone — 0 in stock, out_of_stock, safety stock 2
> * var_rain_parka_xl_stone — XL / Stone — 2 in stock, safety stock 2
>
> No units on order.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-norelated · 2회차 · ✓ 통과

토큰 14,498 · 13.251초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 1,980토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> How many Light rain parka remain in my inventory?

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_inventory"]} ``
   ← 결과 46B: `` {"loaded":["search_products","get_inventory"]} ``
2. 모델 → **`search_products`** `` {"query":"Light rain parka","limit":20} ``
   ← 결과 2,722B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_rain_parka-01f49e29.webp","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_sto… (+900자) ``
3. 모델 → **`get_inventory`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 893B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","inventory_level":4,"availability":"in_stock","variants":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"acom:safety_stock":2,"acom:managed":true,"availability":"out_of_stock","on_order":0},{"variant_id":"var_rain_parka_l_stone","sku":"rp-stone-l","size":"L","color":"Stone","inventory_level":0… (+293자) ``

**답변 1**
> The Light rain parka **prd_rain_parka** has 4 units in stock total.
>
> * S / Stone – var_rain_parka_s_stone, SKU rp-stone-s: 2 in stock
> * M / Stone – var_rain_parka_m_stone, SKU rp-stone-m: 0 in stock, out_of_stock
> * L / Stone – var_rain_parka_l_stone, SKU rp-stone-l: 0 in stock, out_of_stock
> * XL / Stone – var_rain_parka_xl_stone, SKU rp-stone-xl: 2 in stock
>
> Product inventory_level = 4, availability = in_stock.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-batch · 1회차 · ✓ 통과

토큰 15,070 · 14.189초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 1,980토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> How many Light rain parka remain in my inventory?

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_inventory"]} ``
   ← 결과 46B: `` {"loaded":["search_products","get_inventory"]} ``
2. 모델 → **`search_products`** `` {"query":"Light rain parka"} ``
   ← 결과 2,722B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_rain_parka-01f49e29.webp","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_sto… (+900자) ``
3. 모델 → **`get_inventory`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 893B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","inventory_level":4,"availability":"in_stock","variants":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"acom:safety_stock":2,"acom:managed":true,"availability":"out_of_stock","on_order":0},{"variant_id":"var_rain_parka_l_stone","sku":"rp-stone-l","size":"L","color":"Stone","inventory_level":0… (+293자) ``

**답변 1**
> Light rain parka — **prd_rain_parka**
>
> * Total sellable stock: **4 units**
> * Availability: in_stock
>
> Variant breakdown:
> * var_rain_parka_s_stone — S / Stone — 2 in stock, safety stock 2
> * var_rain_parka_m_stone — M / Stone — 0 in stock, out_of_stock, safety stock 2
> * var_rain_parka_l_stone — L / Stone — 0 in stock, out_of_stock, safety stock 2
> * var_rain_parka_xl_stone — XL / Stone — 2 in stock, safety stock 2
>
> On order: 0 for all variants.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-batch · 2회차 · ✓ 통과

토큰 15,939 · 12.905초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 1,980토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> How many Light rain parka remain in my inventory?

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_inventory","get_product"]} ``
   ← 결과 60B: `` {"loaded":["search_products","get_inventory","get_product"]} ``
2. 모델 → **`search_products`** `` {"query":"Light rain parka"} ``
   ← 결과 2,722B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_rain_parka-01f49e29.webp","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_sto… (+900자) ``
3. 모델 → **`get_inventory`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 893B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","inventory_level":4,"availability":"in_stock","variants":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"acom:safety_stock":2,"acom:managed":true,"availability":"out_of_stock","on_order":0},{"variant_id":"var_rain_parka_l_stone","sku":"rp-stone-l","size":"L","color":"Stone","inventory_level":0… (+293자) ``

**답변 1**
> Light rain parka — **prd_rain_parka**
>
> * Total sellable stock: **4 units**
> * Availability: in_stock
>
> Variant breakdown:
> * var_rain_parka_s_stone — S / Stone — 2 in stock
> * var_rain_parka_m_stone — M / Stone — 0 in stock, out_of_stock
> * var_rain_parka_l_stone — L / Stone — 0 in stock, out_of_stock
> * var_rain_parka_xl_stone — XL / Stone — 2 in stock
>
> Safety stock per variant is 2; no units on order.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)
