# b1-vip-weekend-sale — smoke-fix-3-b1

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `c8c944e`

**과업**

> Run a 20% weekend sale on summer outerwear for VIP members and put it on the main page.

> Drop the low-stock ones. Give the overshirt 15% instead.

- 필요한 도구: `search_products`, `list_tiers`, `set_sale_prices`, `create_coupon`, `schedule_banner`
- 허용 도구: `get_policy`, `list_active_promotions`, `list_display_slots`, `list_categories`
- 답에 있어야 할 사실: 40 of 42 summer outerwear products; chore coat (7) and rain parka (4) are left out for low stock
- 답에 있어야 할 사실: the overshirt is at 15% ($67.15) to stay above the price floor
- change set: `` {"state":"drafting","version":2,"items":[{"tool":"set_sale_prices","args":{"valid_for_member_tier":"vip","percent_off":20}},{"tool":"create_coupon"},{"tool":"schedule_banner","args":{"slot_id":"slot_home_hero"}}],"checks_passed":["max_discount","price_floor","promo_min_stock","promotion_overlap","member_benefits_per_order","slot_free"]} ``

### a2api-acom-names-batch · 1회차 · ✗ 실패

토큰 170,163 · 100.646초 · 모델 호출 13회 · 도구 호출 11회 · 첫 요청 프롬프트 2,177토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> Run a 20% weekend sale on summer outerwear for VIP members and put it on the main page.

**질문 2**
> Drop the low-stock ones. Give the overshirt 15% instead.

_(이 실행은 호출이 어느 턴에 속하는지 기록하지 않았다. 호출을 순서대로 보인다.)_

1. 모델 → **`a2api_load`** `` {"names":["merchandising › category: list_categories","catalog › product_group: search_product_groups","search › product: search_products","promotion › promotion: create_promotion","promotion › segment: list_segments","merchandising › banner: list_banners","merchandising › display_slot: list_display_slots"]} ``
   ← 결과 143B: `` {"loaded":["list_categories","search_product_groups","search_products","create_promotion","list_segments","list_banners","list_display_slots"]} ``
2. 모델 → **`a2api_load`** `` {"names":["promotion › offer: set_sale_prices","customer › membership: list_tiers","merchandising › banner: schedule_banner","merchandising › display_slot: schedule_display"]} ``
   ← 결과 80B: `` {"loaded":["set_sale_prices","list_tiers","schedule_banner","schedule_display"]} ``
3. 모델 → **`list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
4. 모델 → **`list_tiers`** `` {} ``
   ← 결과 305B: `` {"status":"succeeded","data":{"items":[{"id":"vip","name":"VIP","rank":3,"program_id":"prg_rewards","member_count":1284},{"id":"gold","name":"Gold","rank":2,"program_id":"prg_rewards","member_count":2900},{"id":"member","name":"Member","rank":1,"program_id":"prg_rewards","member_count":9816}],"total":3}} ``
5. 모델 → **`list_display_slots`** `` {"page":"main","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","audience":"vip"} ``
   ← 결과 1,152B: `` {"status":"succeeded","data":{"items":[{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"]}],"availability":[{"audience":"vip","free_from":"2026-11-07T00:00:00-05:00","free_until":"2026-11-08T23:59:00-05:00"}]},{"id":"slot_home_new_in","page":"main","name":"New in","slot_type":"product_grid","bookings":[],"availa… (+552자) ``
6. 모델 → **`search_products`** `` {"category_id":"cat_summer_outerwear","limit":5} ``
   ← 결과 4,992B: `` {"status":"succeeded","data":{"items":[{"id":"prd_summer_outerwear_13","name":"Poplin shacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/field-olive.svg","price":99.0,"price_currency":"USD","member_price":null,"cost":44.55,"inventory_level":14,"availability":"in_stock","has_variant":[{"variant_id":"var_summer_outerwear_13_xs_olive","sku":"so-13-olive-xs","size":"XS","color":"Olive","inventory_level":1,"availability":"in_stock"},{"variant_id":"var_summer_outerwear_13_s_olive","sku":"so-13-olive-s","size":"S","color":"Olive","inventory_level":1,"avai… (+900자) ``
7. 모델 → **`set_sale_prices`** `` {"name":"VIP weekend summer outerwear","valid_for_member_tier":"vip","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","scope_mode":"category","category_id":"cat_summer_outerwear","percent_off":20.0} ``
   ← 결과 3,692B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6b4124tzq7q3345ffe1e8aq","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"VIP weekend summer outerwear","valid_for_member_tier":"vip","discount_layer":"item_price","valid_from":"2026-11-07T00:00:00-05:00","valid_through":"2026-11-08T23:59:00-05:00","products":42}},{"op":"update","entity":"unit_price_specification","id":null,"from":{"product_id":"prd_camp_overshirt","price":88.0,"price_currency":"USD","price_type":"list_price"},"to":{"product_id":"prd_camp_overshirt","price":70.4,"price_currency":"USD","pr… (+900자) ``
8. 모델 → **`search_products`** `` {"query":"chore coat","category_id":"cat_summer_outerwear","limit":10} ``
   ← 결과 1,770B: `` {"status":"succeeded","data":{"items":[{"id":"prd_chore_coat","name":"Cotton chore coat","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/chore-olive.svg","price":142.0,"price_currency":"USD","member_price":null,"cost":60.0,"inventory_level":7,"availability":"in_stock","has_variant":[{"variant_id":"var_chore_coat_s_olive","sku":"cc-olive-s","size":"S","color":"Olive","inventory_level":3,"availability":"in_stock"},{"variant_id":"var_chore_coat_m_olive","sku":"cc-olive-m","size":"M","color":"Olive","inventory_level":0,"availability":"out_of_stock"},{"varian… (+900자) ``
9. 모델 → **`search_products`** `` {"query":"seersucker overshirt","category_id":"cat_summer_outerwear","limit":10} ``
   ← 결과 4,950B: `` {"status":"succeeded","data":{"items":[{"id":"prd_seersucker_overshirt","name":"Seersucker overshirt","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/shirt-clay.svg","price":79.0,"price_currency":"USD","member_price":null,"cost":58.0,"inventory_level":53,"availability":"in_stock","has_variant":[{"variant_id":"var_seersucker_overshirt_xs_white","sku":"so-white-xs","size":"XS","color":"White","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_seersucker_overshirt_s_white","sku":"so-white-s","size":"S","color":"White","inventory_level":4,"ava… (+900자) ``
10. 모델 → **`set_sale_prices`** `` {"name":"VIP weekend summer outerwear","valid_for_member_tier":"vip","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","scope_mode":"category","category_id":"cat_summer_outerwear","percent_off":20.0,"exclude_low_stock":true,"overrides":[{"product_id":"prd_seersucker_overshirt","percent_off":15.0}]} ``
   ← 결과 3,700B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6b41phct0e4119kvtysztfs","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"VIP weekend summer outerwear","valid_for_member_tier":"vip","discount_layer":"item_price","valid_from":"2026-11-07T00:00:00-05:00","valid_through":"2026-11-08T23:59:00-05:00","products":40}},{"op":"update","entity":"unit_price_specification","id":null,"from":{"product_id":"prd_camp_overshirt","price":88.0,"price_currency":"USD","price_type":"list_price"},"to":{"product_id":"prd_camp_overshirt","price":70.4,"price_currency":"USD","pr… (+900자) ``
11. 모델 → **`schedule_banner`** `` {"slot_id":"slot_home_hero","audience":"vip","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","content":{"eyebrow":"VIP WEEKEND","headline":"20% off summer outerwear","cta_label":"Shop the sale","url":"/category/summer-outerwear","image_source":"product","image_product_id":"prd_summer_outerwear_13"}} ``
   ← 결과 742B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6b41t8b6dp1fwq9t5wkjx84","expires_at":null,"changes":[{"op":"schedule","entity":"display_booking","id":null,"to":{"slot_id":"slot_home_hero","audience":"vip","valid_from":"2026-11-07T00:00:00-05:00","valid_through":"2026-11-08T23:59:00-05:00","content":{"eyebrow":"VIP WEEKEND","headline":"20% off summer outerwear","cta_label":"Shop the sale","url":"/category/summer-outerwear","image_source":"product","image_product_id":"prd_summer_outerwear_13"},"promotion_id":null}}],"checks":[{"rule":"slot_free","passed":true,"detail":"Hero slot open Nov 7–8 … (+140자) ``

**답변 1**
> The 20% VIP weekend sale on summer outerwear is staged for Nov 7–8, 2026 (store time).
>
> * Sale price preview: change set cs_1042, preview pv_01m6b41phct0e4119kvtysztfs
>   * 40 of 42 products in cat_summer_outerwear get 20% off for tier vip
>   * Excluded low-stock: Cotton chore coat (7 units) and Light rain parka (4 units)
>   * Price-floor override: Seersucker overshirt prd_seersucker_overshirt at 15% → $67.15 (floor $66.70)
>   * Checks passed: max_discount, price_floor, promo_min_stock, promotion_overlap
>   * Needs approval: changes 40 prices
>
> * Main-page banner for VIP: change set cs_1042, preview pv_01m6b41t8b6dp1fwq9t5wkjx84
>   * Slot slot_home_hero, audience vip, 2026-11-07 00:00 to 2026-11-08 23:59
>   * Eyebrow “VIP WEEKEND”, headline “20% off summer outerwear”, CTA “Shop the sale” → /category/summer-outerwear
>   * Image from prd_summer_outerwear_13 (Poplin shacket)
>   * Slot free for VIP on the weekend; needs approval to show to 1,284 VIP members
>
> Both changes are in the same change set cs_1042 and await approval before they go live.

**답변 2**
> Done.
>
> * Low-stock items are out of the sale
>   * Cotton chore coat prd_chore_coat – 7 units total → excluded
>   * Light rain parka prd_rain_parka – 4 units total → excluded
>   * Promo_min_stock check now passes; 40 of 42 summer-outerwear products remain in scope
>
> * Seersucker overshirt price-floor override
>   * prd_seersucker_overshirt: 15% off → $67.15 sale price
>   * Keeps price above cost +15% floor $66.70 (cost $58.00)
>
> Current staged change set cs_1042:
> * Sale price preview pv_01m6b41phct0e4119kvtysztfs
>   * VIP weekend summer outerwear, tier vip, 2026-11-07 00:00 to 2026-11-08 23:59
>   * 40 products priced, 2 excluded for low stock, 1 override at 15%
>   * Checks: max_discount passed, price_floor passed, promo_min_stock passed, promotion_overlap passed
>   * Needs approval: changes 40 prices
>
> * Main-page banner preview pv_01m6b41t8b6dp1fwq9t5wkjx84
>   * slot_home_hero for VIP 2026-11-07 to 2026-11-08
>   * “VIP WEEKEND / 20% off summer outerwear” → /category/summer-outerwear
>   * Needs approval to show to 1,284 VIP members
>
> Both items are in change set cs_1042 awaiting approval.

**채점**: ✗ 실패 — 빠진 것: tool create_coupon; change set item create_coupon {}
(도구 정밀도 1.00, 재현율 0.80)
