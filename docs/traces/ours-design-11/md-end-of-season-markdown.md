# md-end-of-season-markdown — ours-design-11

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `d86a1ff` · a2api `140fda2`

**과업**

> start the end of season markdown on tees. 25% off for everyone through Nov 15, leave out anything that's almost gone

- 필요한 도구: `search_products`, `set_sale_prices`
- 허용 도구: `get_policy`, `list_categories`, `list_active_promotions`
- 답에 있어야 할 사실: 25% is over the 20% limit for everyone (the VIP limit of 30% does not apply), so the draft is blocked
- 답에 있어야 할 사실: the agent offers 20%, or a 25% sale limited to VIP
- change set: `` {"state":"drafting","items":[{"tool":"set_sale_prices","args":{"valid_for_member_tier":"everyone","scope_mode":"category","category_id":"cat_tees","exclude_low_stock":true}}],"checks_failed":["max_discount"]} ``

### a2api-acom-names-batch · 1회차 · ✗ 실패

토큰 35,276 · 77.757초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 1,996토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> start the end of season markdown on tees. 25% off for everyone through Nov 15, leave out anything that's almost gone

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_inventory","create_promotion","list_categories"]} ``
   ← 결과 83B: `` {"loaded":["search_products","get_inventory","create_promotion","list_categories"]} ``
2. 모델 → **`list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
3. 모델 → **`a2api_load`** `` {"names":["set_sale_prices"]} ``
   ← 결과 30B: `` {"loaded":["set_sale_prices"]} ``
4. 모델 → **`set_sale_prices`** `` {"name":"End of season tees markdown","valid_for_member_tier":"everyone","valid_from":"2026-11-06T11:00","valid_through":"2026-11-15T23:59","scope_mode":"category","category_id":"cat_tees","percent_off":25.0,"exclude_low_stock":true} ``
   ← 결과 4,077B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6bdjprzkp1zk3e7cda0h1n6","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"End of season tees markdown","valid_for_member_tier":"everyone","discount_layer":"item_price","valid_from":"2026-11-06T11:00:00-05:00","valid_through":"2026-11-15T23:59:00-05:00","products":24}},{"op":"update","entity":"unit_price_specification","id":null,"from":{"product_id":"prd_breton_tee","price":23.0,"price_currency":"USD","price_type":"list_price"},"to":{"product_id":"prd_breton_tee","price":17.25,"price_currency":"USD","price… (+900자) ``

**답변 1**
> End-of-season tees markdown is staged as a preview.
>
> * Promotion: **End of season tees markdown**
> * Tier: everyone
> * Scope: category `cat_tees`
> * Period: 2026-11-06T11:00:00-05:00 → 2026-11-15T23:59:00-05:00
> * Discount: 25% off list price, item-price layer
> * Low-stock handling: `exclude_low_stock = true`
>
> Preview
> * preview_id: `pv_01m6bdjprzkp1zk3e7cda0h1n6`
> * change_set_id: `cs_1042`
> * Products in scope: 24
> * Price updates staged: 24 products, e.g.
>   * prd_breton_tee  $23.00 → $17.25  25%
>   * prd_tees_01     $49.00 → $36.75  25%
>   * prd_tees_02     $39.00 → $29.25  25%
>   * prd_tees_03     $39.00 → $29.25  25%
>   * prd_tees_04     $39.00 → $29.25  25%
>   * prd_tees_05     $19.00 → $14.25  25%
>   * prd_tees_06     $49.00 → $36.75  25%
>   * prd_tees_07     $29.00 → $21.75  25%
>   * prd_tees_08     $49.00 → $36.75  25%
>   * prd_tees_09     $59.00 → $44.25  25%
>   * prd_tees_10     $49.00 → $36.75  25%
>   * … 13 more updates omitted in the preview
>
> Checks
> * max_discount: **failed** – 25% is over the 20% limit for `everyone`; vip allows up to 30%
> * price_floor: **failed** – prd_breton_tee at 25% would be $17.25, under the floor $23.00 (cost $20.00 + 15%)
> * promo_min_stock: passed – Every product has at least 10 units
> * promotion_overlap: passed – No existing item-price promotion on tees
>
> The change set is waiting for a person’s approval. It will not publish until approved, and the two failed checks will need to be resolved – e.g., reduce the discount to ≤20% for everyone, move the offer to a VIP tier, or override/exclude prd_breton_tee for the price-floor violation.

**채점**: ✗ 실패 — 빠진 것: tool search_products
(도구 정밀도 1.00, 재현율 0.50)

### a2api-acom-names-batch · 2회차 · ✓ 통과

토큰 45,722 · 89.521초 · 모델 호출 6회 · 도구 호출 5회 · 첫 요청 프롬프트 1,996토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> start the end of season markdown on tees. 25% off for everyone through Nov 15, leave out anything that's almost gone

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_inventory","create_promotion","list_categories"]} ``
   ← 결과 83B: `` {"loaded":["search_products","get_inventory","create_promotion","list_categories"]} ``
2. 모델 → **`list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
3. 모델 → **`a2api_load`** `` {"names":["set_sale_prices"]} ``
   ← 결과 30B: `` {"loaded":["set_sale_prices"]} ``
4. 모델 → **`set_sale_prices`** `` {"name":"End of season tees markdown","valid_for_member_tier":"everyone","valid_from":"2026-11-06T11:00","valid_through":"2026-11-15T23:59","scope_mode":"category","category_id":"cat_tees","percent_off":25.0,"exclude_low_stock":true} ``
   ← 결과 4,077B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6beb8fxpwxkjsvz0fgjewts","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"End of season tees markdown","valid_for_member_tier":"everyone","discount_layer":"item_price","valid_from":"2026-11-06T11:00:00-05:00","valid_through":"2026-11-15T23:59:00-05:00","products":24}},{"op":"update","entity":"unit_price_specification","id":null,"from":{"product_id":"prd_breton_tee","price":23.0,"price_currency":"USD","price_type":"list_price"},"to":{"product_id":"prd_breton_tee","price":17.25,"price_currency":"USD","price… (+900자) ``
5. 모델 → **`search_products`** `` {"category_id":"cat_tees","limit":100,"fields":["id","name","price","inventory_level"]} ``
   ← 결과 2,102B: `` {"status":"succeeded","data":{"items":[{"id":"prd_tees_04","name":"Jersey long-sleeve tee","price":39.0,"inventory_level":77},{"id":"prd_tees_09","name":"Waffle crew tee","price":59.0,"inventory_level":134},{"id":"prd_tees_22","name":"Organic cotton boxy tee","price":39.0,"inventory_level":75},{"id":"prd_tees_02","name":"Cotton V-neck tee","price":39.0,"inventory_level":63},{"id":"prd_tees_11","name":"Pima cotton henley","price":19.0,"inventory_level":34},{"id":"prd_tees_16","name":"Jersey raglan tee","price":29.0,"inventory_level":98},{"id":"prd_tees_14","name":"Waffle tee","price":19.0,"inve… (+900자) ``

**답변 1**
> The end-of-season tee markdown is staged as a preview, not live yet.
>
> **Preview**
> * Promotion name: End of season tees markdown
> * Tier: everyone
> * Period: 2026-11-06 11:00 – 2026-11-15 23:59 America/New_York
> * Scope: category cat_tees – 24 products
> * Discount: 25% off list price on item price
> * Low-stock handling: exclude_low_stock = true
>
> Preview id: pv_01m6beb8fxpwxkjsvz0fgjewts
> Change set: cs_1042 – needs a person’s approval. Changes 24 prices.
>
> Products in scope from search_products:
> prd_tees_04 Jersey long-sleeve tee $39.00 inv 77
> prd_tees_09 Waffle crew tee $59.00 inv 134
> prd_tees_22 Organic cotton boxy tee $39.00 inv 75
> prd_tees_02 Cotton V-neck tee $39.00 inv 63
> prd_tees_11 Pima cotton henley $19.00 inv 34
> prd_tees_16 Jersey raglan tee $29.00 inv 98
> prd_tees_14 Waffle tee $19.00 inv 84
> prd_tees_23 Slub cotton tee $49.00 inv 118
> prd_tees_18 Organic cotton raglan tee $39.00 inv 24
> prd_tees_20 Slub cotton crew tee $39.00 inv 117
> prd_tees_19 Linen blend pocket tee $19.00 inv 30
> prd_tees_21 Heavyweight cotton henley $29.00 inv 94
> prd_tees_13 Linen blend boxy tee $39.00 inv 73
> prd_tees_03 Heavyweight cotton raglan tee $39.00 inv 91
> prd_tees_06 Jersey boxy tee $49.00 inv 32
> prd_breton_tee Breton tee $23.00 inv 60
> prd_tees_05 Linen blend V-neck tee $19.00 inv 63
> prd_tees_07 Cotton henley $29.00 inv 145
> prd_tees_08 Heavyweight cotton V-neck tee $49.00 inv 121
> prd_tees_15 Slub cotton long-sleeve tee $29.00 inv 115
> prd_tees_10 Cotton raglan tee $49.00 inv 67
> prd_tees_17 Organic cotton crew tee $19.00 inv 76
> prd_tees_12 Slub cotton V-neck tee $49.00 inv 34
> prd_tees_01 Organic cotton pocket tee $49.00 inv 32
>
> All 24 have ≥10 units, so with exclude_low_stock true no products were dropped for low stock.
>
> Checks from the preview:
> * max_discount: FAILED – 25% is over the 20% limit for everyone; vip allows up to 30%
> * price_floor: FAILED – Breton tee at 25% would be $17.25, under the floor $23.00 (cost $20.00 + 15%)
> * promo_min_stock: PASSED – Every product has at least 10 un… (+412자)

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)
