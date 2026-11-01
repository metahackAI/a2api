# md-end-of-season-markdown — smoke-fix-1-headings

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `c8c944e`

**과업**

> start the end of season markdown on tees. 25% off for everyone through Nov 15, leave out anything that's almost gone

- 필요한 도구: `search_products`, `set_sale_prices`
- 허용 도구: `get_policy`, `list_categories`, `list_active_promotions`
- 답에 있어야 할 사실: 25% is over the 20% limit for everyone (the VIP limit of 30% does not apply), so the draft is blocked
- 답에 있어야 할 사실: the agent offers 20%, or a 25% sale limited to VIP
- change set: `` {"state":"drafting","items":[{"tool":"set_sale_prices","args":{"valid_for_member_tier":"everyone","scope_mode":"category","category_id":"cat_tees","exclude_low_stock":true}}],"checks_failed":["max_discount"]} ``

### a2api-acom-names-norelated · 1회차 · ✓ 통과

토큰 42,044 · 80.913초 · 모델 호출 6회 · 도구 호출 5회 · 첫 요청 프롬프트 1,946토큰

준비: 전략 `index`, 함수 253개, 목차 6,029자(system prompt)

**질문 1**
> start the end of season markdown on tees. 25% off for everyone through Nov 15, leave out anything that's almost gone

1. 모델 → **`a2api_load`** `` {"names":["search_products","get_inventory","set_sale_prices","get_facets","list_categories"]} ``
   ← 결과 95B: `` {"loaded":["search_products","get_inventory","set_sale_prices","get_facets","list_categories"]} ``
2. 모델 → **`list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
3. 모델 → **`search_products`** `` {"category_id":"cat_tees","limit":100} ``
   ← 결과 3,621B: `` {"status":"succeeded","data":{"items":[{"id":"prd_tees_04","name":"Jersey long-sleeve tee","category_id":"cat_tees","brand_id":"brn_northwind","image":"/media/garment/tee-white.svg","price":39.0,"price_currency":"USD","member_price":null,"cost":16.8,"inventory_level":77,"availability":"in_stock","has_variant":[{"variant_id":"var_tees_04_xs_white","sku":"tees-04-white-xs","size":"XS","color":"White","inventory_level":13,"availability":"in_stock"},{"variant_id":"var_tees_04_s_white","sku":"tees-04-white-s","size":"S","color":"White","inventory_level":14,"availability":"in_stock"},{"variant_id":"… (+900자) ``
4. 모델 → **`search_products`** `` {"category_id":"cat_tees","limit":100} ``
   ← 결과 3,729B: `` {"status":"succeeded","data":{"items":[{"id":"prd_tees_04","name":"Jersey long-sleeve tee","category_id":"cat_tees","brand_id":"brn_northwind","image":"/media/garment/tee-white.svg","price":39.0,"price_currency":"USD","member_price":null,"cost":16.8,"inventory_level":77,"availability":"in_stock","has_variant":[{"variant_id":"var_tees_04_xs_white","sku":"tees-04-white-xs","size":"XS","color":"White","inventory_level":13,"availability":"in_stock"},{"variant_id":"var_tees_04_s_white","sku":"tees-04-white-s","size":"S","color":"White","inventory_level":14,"availability":"in_stock"},{"variant_id":"… (+900자) ``
5. 모델 → **`set_sale_prices`** `` {"name":"End of season markdown on tees","valid_for_member_tier":"everyone","valid_from":"2026-11-06T11:00","valid_through":"2026-11-15T23:59","scope_mode":"category","category_id":"cat_tees","percent_off":25,"exclude_low_stock":true} ``
   ← 결과 4,080B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6b366tdtfvdf18ze0jpm92h","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"End of season markdown on tees","valid_for_member_tier":"everyone","discount_layer":"item_price","valid_from":"2026-11-06T11:00:00-05:00","valid_through":"2026-11-15T23:59:00-05:00","products":24}},{"op":"update","entity":"unit_price_specification","id":null,"from":{"product_id":"prd_breton_tee","price":23.0,"price_currency":"USD","price_type":"list_price"},"to":{"product_id":"prd_breton_tee","price":17.25,"price_currency":"USD","pr… (+900자) ``

**답변 1**
> The end-of-season markdown preview is built for the Tees category `cat_tees`.
>
> * Scope: 24 tee products
> * Tier: everyone
> * Window: 2026-11-06T11:00-05:00 → 2026-11-15T23:59-05:00
> * Discount: 25% off list price
> * Low-stock handling: `exclude_low_stock = true`
>
> Preview created
> * change set: `cs_1042`
> * preview: `pv_01m6b366tdtfvdf18ze0jpm92h`
> * Needs approval – 24 price changes are waiting for a person to approve.
>
> Checks on the preview:
>
> * max_discount: **failed** – 25% is over the 20% limit for `everyone`; VIP allows up to 30%.
> * price_floor: **failed** – `prd_breton_tee` at 25% would be $17.25, under the floor $23.00 (cost $20.00 + 15%).
> * promo_min_stock: passed – every product has at least 10 units.
> * promotion_overlap: passed – no running/scheduled item-price promotion on tees.
>
> Example price moves in the preview:
> * `prd_tees_04` Jersey long-sleeve tee $39.00 → $29.25 sale
> * `prd_tees_09` Waffle crew tee $59.00 → $44.25 sale
> * `prd_tees_01` $49.00 → $36.75 sale
> * `prd_breton_tee` $23.00 → $17.25 sale – floor violation
>
> No products were excluded for low stock under the current `promo_min_stock` rule.
>
> You can’t publish this as-is because the 25% everyone discount exceeds the allowed 20% discount limit and the Breton tee would breach its price floor. Options:
> * reduce to 20% for everyone, or
> * keep 25% for VIP only, or
> * keep 25% for everyone with an override/exclusion for `prd_breton_tee` and accept the discount-limit exception for approval.
>
> Tell me which adjustment you want and I’ll rebuild the preview.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)
