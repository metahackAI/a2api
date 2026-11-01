# b1-vip-weekend-sale — smoke-fix-1-headings

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `c8c944e`

**과업**

> Run a 20% weekend sale on summer outerwear for VIP members and put it on the main page.

> Drop the low-stock ones. Give the overshirt 15% instead.

- 필요한 도구: `search_products`, `list_tiers`, `set_sale_prices`, `create_coupon`, `schedule_banner`
- 허용 도구: `get_policy`, `list_active_promotions`, `list_display_slots`, `list_categories`
- 답에 있어야 할 사실: 40 of 42 summer outerwear products; chore coat (7) and rain parka (4) are left out for low stock
- 답에 있어야 할 사실: the overshirt is at 15% ($67.15) to stay above the price floor
- change set: `` {"state":"drafting","version":2,"items":[{"tool":"set_sale_prices","args":{"valid_for_member_tier":"vip","percent_off":20}},{"tool":"create_coupon"},{"tool":"schedule_banner","args":{"slot_id":"slot_home_hero"}}],"checks_passed":["max_discount","price_floor","promo_min_stock","promotion_overlap","member_benefits_per_order","slot_free"]} ``

### a2api-acom-names-norelated · 1회차 · E MODEL_CALL_LIMIT

토큰 135,464 · 93.881초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 1,941토큰

준비: 전략 `index`, 함수 253개, 목차 6,029자(system prompt)

**질문 1**
> Run a 20% weekend sale on summer outerwear for VIP members and put it on the main page.

**질문 2**
> Drop the low-stock ones. Give the overshirt 15% instead.

_(이 실행은 호출이 어느 턴에 속하는지 기록하지 않았다. 호출을 순서대로 보인다.)_

1. 모델 → **`a2api_load`** `` {"names":["search_products","list_categories","list_segments","create_promotion","search_product_groups","list_banners","schedule_banner"]} ``
   ← 결과 140B: `` {"loaded":["search_products","list_categories","list_segments","create_promotion","search_product_groups","list_banners","schedule_banner"]} ``
2. 모델 → **`list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
3. 모델 → **`list_segments`** `` {} ``
   ← 결과 467B: `` {"status":"succeeded","data":{"items":[{"id":"seg_lapsed_knit_buyers","name":"Lapsed knit buyers","version":1,"estimated_size":22,"estimated_at":"2026-11-06T09:00:00-05:00","condition_rules":{"exclude_segment_ids":["seg_recent_buyers"],"purchased_category_ids":["cat_knitwear"]}},{"id":"seg_recent_buyers","name":"Recent buyers","version":1,"estimated_size":5143,"estimated_at":"2026-11-06T09:00:00-05:00","condition_rules":{"last_order_within_days":30}}],"total":2}} ``
4. 모델 → **`a2api_load`** `` {"names":["set_sale_prices","list_tiers","list_display_slots"]} ``
   ← 결과 64B: `` {"loaded":["set_sale_prices","list_tiers","list_display_slots"]} ``
5. 모델 → **`list_tiers`** `` {} ``
   ← 결과 305B: `` {"status":"succeeded","data":{"items":[{"id":"vip","name":"VIP","rank":3,"program_id":"prg_rewards","member_count":1284},{"id":"gold","name":"Gold","rank":2,"program_id":"prg_rewards","member_count":2900},{"id":"member","name":"Member","rank":1,"program_id":"prg_rewards","member_count":9816}],"total":3}} ``
6. 모델 → **`list_display_slots`** `` {"page":"main","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","audience":"vip"} ``
   ← 결과 1,152B: `` {"status":"succeeded","data":{"items":[{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"]}],"availability":[{"audience":"vip","free_from":"2026-11-07T00:00:00-05:00","free_until":"2026-11-08T23:59:00-05:00"}]},{"id":"slot_home_new_in","page":"main","name":"New in","slot_type":"product_grid","bookings":[],"availa… (+552자) ``
7. 모델 → **`search_products`** `` {"category_id":"cat_summer_outerwear","limit":5} ``
   ← 결과 4,992B: `` {"status":"succeeded","data":{"items":[{"id":"prd_summer_outerwear_13","name":"Poplin shacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/field-olive.svg","price":99.0,"price_currency":"USD","member_price":null,"cost":44.55,"inventory_level":14,"availability":"in_stock","has_variant":[{"variant_id":"var_summer_outerwear_13_xs_olive","sku":"so-13-olive-xs","size":"XS","color":"Olive","inventory_level":1,"availability":"in_stock"},{"variant_id":"var_summer_outerwear_13_s_olive","sku":"so-13-olive-s","size":"S","color":"Olive","inventory_level":1,"avai… (+900자) ``
8. 모델 → **`set_sale_prices`** `` {"name":"VIP weekend summer outerwear","valid_for_member_tier":"vip","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","scope_mode":"category","category_id":"cat_summer_outerwear","percent_off":20} ``
   ← 결과 3,692B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6b3174xvmya2sdj9kp0tk87","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"VIP weekend summer outerwear","valid_for_member_tier":"vip","discount_layer":"item_price","valid_from":"2026-11-07T00:00:00-05:00","valid_through":"2026-11-08T23:59:00-05:00","products":42}},{"op":"update","entity":"unit_price_specification","id":null,"from":{"product_id":"prd_camp_overshirt","price":88.0,"price_currency":"USD","price_type":"list_price"},"to":{"product_id":"prd_camp_overshirt","price":70.4,"price_currency":"USD","pr… (+900자) ``
9. 모델 → **`search_products`** `` {"query":"chore coat","category_id":"cat_summer_outerwear","limit":10} ``
   ← 결과 1,770B: `` {"status":"succeeded","data":{"items":[{"id":"prd_chore_coat","name":"Cotton chore coat","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/chore-olive.svg","price":142.0,"price_currency":"USD","member_price":null,"cost":60.0,"inventory_level":7,"availability":"in_stock","has_variant":[{"variant_id":"var_chore_coat_s_olive","sku":"cc-olive-s","size":"S","color":"Olive","inventory_level":3,"availability":"in_stock"},{"variant_id":"var_chore_coat_m_olive","sku":"cc-olive-m","size":"M","color":"Olive","inventory_level":0,"availability":"out_of_stock"},{"varian… (+900자) ``
10. 모델 → **`search_products`** `` {"query":"seersucker overshirt","category_id":"cat_summer_outerwear","limit":10} ``
   ← 결과 4,950B: `` {"status":"succeeded","data":{"items":[{"id":"prd_seersucker_overshirt","name":"Seersucker overshirt","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/shirt-clay.svg","price":79.0,"price_currency":"USD","member_price":null,"cost":58.0,"inventory_level":53,"availability":"in_stock","has_variant":[{"variant_id":"var_seersucker_overshirt_xs_white","sku":"so-white-xs","size":"XS","color":"White","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_seersucker_overshirt_s_white","sku":"so-white-s","size":"S","color":"White","inventory_level":4,"ava… (+900자) ``
11. 모델 → **`set_sale_prices`** `` {"name":"VIP weekend summer outerwear","valid_for_member_tier":"vip","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","scope_mode":"category","category_id":"cat_summer_outerwear","percent_off":20,"overrides":[{"product_id":"prd_seersucker_overshirt","percent_off":15.0}],"exclude_low_stock":true} ``
   ← 결과 3,700B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6b31vv3zmz5nre4yeg2z1qk","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"VIP weekend summer outerwear","valid_for_member_tier":"vip","discount_layer":"item_price","valid_from":"2026-11-07T00:00:00-05:00","valid_through":"2026-11-08T23:59:00-05:00","products":40}},{"op":"update","entity":"unit_price_specification","id":null,"from":{"product_id":"prd_camp_overshirt","price":88.0,"price_currency":"USD","price_type":"list_price"},"to":{"product_id":"prd_camp_overshirt","price":70.4,"price_currency":"USD","pr… (+900자) ``
12. 모델 → **`schedule_banner`** `` {"slot_id":"slot_home_hero","audience":"vip","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","content":{"eyebrow":"VIP WEEKEND","headline":"20% off summer outerwear","cta_label":"Shop the sale","url":"/category/summer-outerwear","image_source":"product","image_product_id":"prd_summer_outerwear_13"}} ``
   ← 결과 742B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6b31zdpqs573qwsq5djgt95","expires_at":null,"changes":[{"op":"schedule","entity":"display_booking","id":null,"to":{"slot_id":"slot_home_hero","audience":"vip","valid_from":"2026-11-07T00:00:00-05:00","valid_through":"2026-11-08T23:59:00-05:00","content":{"eyebrow":"VIP WEEKEND","headline":"20% off summer outerwear","cta_label":"Shop the sale","url":"/category/summer-outerwear","image_source":"product","image_product_id":"prd_summer_outerwear_13"},"promotion_id":null}}],"checks":[{"rule":"slot_free","passed":true,"detail":"Hero slot open Nov 7–8 … (+140자) ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: tool create_coupon; change set item create_coupon {}; fact "40 of 42 summer outerwear products; chore coat (7) and rain " (40, 42, 7, 4 not shown); fact "the overshirt is at 15% ($67.15) to stay above the price flo" (15, 67.15 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.90, 재현율 0.80)
