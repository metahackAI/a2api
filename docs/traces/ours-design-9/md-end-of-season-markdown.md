# md-end-of-season-markdown — ours-design-9

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> start the end of season markdown on tees. 25% off for everyone through Nov 15, leave out anything that's almost gone

- 필요한 도구: `search_products`, `set_sale_prices`
- 허용 도구: `get_policy`, `list_categories`, `list_active_promotions`
- 답에 있어야 할 사실: 25% is over the 20% limit for everyone (the VIP limit of 30% does not apply), so the draft is blocked
- 답에 있어야 할 사실: the agent offers 20%, or a 25% sale limited to VIP
- change set: `` {"state":"drafting","items":[{"tool":"set_sale_prices","args":{"valid_for_member_tier":"everyone","scope_mode":"category","category_id":"cat_tees","exclude_low_stock":true}}],"checks_failed":["max_discount"]} ``

### a2api-acom-hybrid · 1회차 · ✗ 실패

토큰 30,435 · 51.991초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 6,019토큰

준비: 전략 `index`, 함수 253개, 목차 4,645자(system prompt)

**질문 1**
> start the end of season markdown on tees. 25% off for everyone through Nov 15, leave out anything that's almost gone

1. 모델 → **`a2api_load`** `` {"names":["list_categories","set_sale_prices"]} ``
   ← 결과 91B: `` {"loaded":["list_categories"],"already":["set_sale_prices"],"evicted":["update_promotion"]} ``
2. 모델 → **`list_categories`** `` {} ``
   ← 결과 3,713B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
3. 모델 → **`set_sale_prices`** `` {"name":"End of season tees markdown","valid_for_member_tier":"everyone","valid_from":"2026-11-06T11:00","valid_through":"2026-11-15T23:59","scope_mode":"category","category_id":"cat_tees","percent_off":25,"exclude_low_stock":true} ``
   ← 결과 4,077B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6arkm9af1pk3pkht3cj9eb2","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"End of season tees markdown","valid_for_member_tier":"everyone","discount_layer":"item_price","valid_from":"2026-11-06T11:00:00-05:00","valid_through":"2026-11-15T23:59:00-05:00","products":24}},{"op":"update","entity":"unit_price_specification","id":null,"from":{"product_id":"prd_breton_tee","price":23.0,"price_currency":"USD","price_type":"list_price"},"to":{"product_id":"prd_breton_tee","price":17.25,"price_currency":"USD","price… (+900자) ``

**답변 1**
> Preview created for the end-of-season tees markdown, waiting for a person to approve.
>
> * Change set: cs_1042
> * Preview: pv_01m6arkm9af1pk3pkht3cj9eb2
> * Promotion: “End of season tees markdown”
> * Who: everyone
> * When: 2026-11-06T11:00:00-05:00 → 2026-11-15T23:59:00-05:00
> * Scope: category cat_tees – Tees
> * Discount: 25% item price
> * Low stock handling: exclude_low_stock = true
>
> Scope result from the preview:
> * 24 products in scope
> * Example price updates in the preview:
>   * prd_breton_tee $23.00 list → $17.25 sale, 25%
>   * prd_tees_01 $49.00 → $36.75 sale, 25%
>   * prd_tees_02 $39.00 → $29.25 sale, 25%
>   * prd_tees_03 $39.00 → $29.25 sale, 25%
>   * prd_tees_04 $39.00 → $29.25 sale, 25%
>   * prd_tees_05 $19.00 → $14.25 sale, 25%
>   * prd_tees_06 $49.00 → $36.75 sale, 25%
>   * prd_tees_07 $29.00 → $21.75 sale, 25%
>   * prd_tees_08 $49.00 → $36.75 sale, 25%
>   * prd_tees_09 $59.00 → $44.25 sale, 25%
>   * prd_tees_10 $49.00 → $36.75 sale, 25%
>   * … 13 more updates omitted in the preview
>
> Checks:
> * max_discount: FAILED – 25% is over the 20% limit for everyone; vip allows up to 30%
> * price_floor: FAILED – Breton tee at 25% would be $17.25, under the floor $23.00 (cost $20.00 + 15%)
> * promo_min_stock: PASSED – Every product has at least 10 units
> * promotion_overlap: PASSED – Checked 4 running and 1 scheduled promotions; none gives an item price on tees
>
> The change set is not live. It needs approval because it changes 24 prices and fails the max discount and price floor rules. If you want it to go through, the discount for the “everyone” tier would need to be ≤20% or the Breton tee would need to be excluded/overridden to respect the $23.00 floor.

**채점**: ✗ 실패 — 빠진 것: tool search_products
(도구 정밀도 1.00, 재현율 0.50)

### a2api-acom-hybrid · 2회차 · ✗ 실패

토큰 29,818 · 41.776초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 6,019토큰

준비: 전략 `index`, 함수 253개, 목차 4,645자(system prompt)

**질문 1**
> start the end of season markdown on tees. 25% off for everyone through Nov 15, leave out anything that's almost gone

1. 모델 → **`a2api_load`** `` {"names":["list_categories","set_sale_prices"]} ``
   ← 결과 91B: `` {"loaded":["list_categories"],"already":["set_sale_prices"],"evicted":["update_promotion"]} ``
2. 모델 → **`list_categories`** `` {} ``
   ← 결과 3,713B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
3. 모델 → **`set_sale_prices`** `` {"name":"End of season tees markdown","valid_for_member_tier":"everyone","valid_from":"2026-11-06T11:00","valid_through":"2026-11-15T23:59","scope_mode":"category","category_id":"cat_tees","percent_off":25,"exclude_low_stock":true} ``
   ← 결과 4,077B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6as5zt3rtttbwctjp7p2c0q","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"End of season tees markdown","valid_for_member_tier":"everyone","discount_layer":"item_price","valid_from":"2026-11-06T11:00:00-05:00","valid_through":"2026-11-15T23:59:00-05:00","products":24}},{"op":"update","entity":"unit_price_specification","id":null,"from":{"product_id":"prd_breton_tee","price":23.0,"price_currency":"USD","price_type":"list_price"},"to":{"product_id":"prd_breton_tee","price":17.25,"price_currency":"USD","price… (+900자) ``

**답변 1**
> Preview created for the end-of-season tees markdown.
>
> * Promotion: **End of season tees markdown**
> * Scope: category `cat_tees` → 24 products in scope
> * Who: everyone
> * When: 2026-11-06T11:00:00-05:00 to 2026-11-15T23:59:00-05:00
> * Discount: 25% item price
> * Low stock: `exclude_low_stock = true` – items under minimum stock are left out
>
> Preview id: `pv_01m6as5zt3rtttbwctjp7p2c0q`
> Change set: `cs_1042` – needs a person’s approval. Changes 24 prices.
>
> Checks:
> * max_discount – **failed**: 25% is over the 20% limit for everyone; vip allows up to 30%
> * price_floor – **failed**: `prd_breton_tee` at 25% would be $17.25, under the floor $23.00 (cost $20.00 + 15%)
> * promo_min_stock – passed: every product has at least 10 units
> * promotion_overlap – passed: no existing item-price promotion on tees
>
> The change is waiting for approval and cannot be published as-is because of the discount-limit and price-floor rules. Want me to adjust to 20% for everyone, exclude the Breton tee, or make it VIP-only?

**채점**: ✗ 실패 — 빠진 것: tool search_products
(도구 정밀도 1.00, 재현율 0.50)
