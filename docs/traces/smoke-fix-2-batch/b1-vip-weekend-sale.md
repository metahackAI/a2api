# b1-vip-weekend-sale — smoke-fix-2-batch

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `c8c944e`

**과업**

> Run a 20% weekend sale on summer outerwear for VIP members and put it on the main page.

> Drop the low-stock ones. Give the overshirt 15% instead.

- 필요한 도구: `search_products`, `list_tiers`, `set_sale_prices`, `create_coupon`, `schedule_banner`
- 허용 도구: `get_policy`, `list_active_promotions`, `list_display_slots`, `list_categories`
- 답에 있어야 할 사실: 40 of 42 summer outerwear products; chore coat (7) and rain parka (4) are left out for low stock
- 답에 있어야 할 사실: the overshirt is at 15% ($67.15) to stay above the price floor
- change set: `` {"state":"drafting","version":2,"items":[{"tool":"set_sale_prices","args":{"valid_for_member_tier":"vip","percent_off":20}},{"tool":"create_coupon"},{"tool":"schedule_banner","args":{"slot_id":"slot_home_hero"}}],"checks_passed":["max_discount","price_floor","promo_min_stock","promotion_overlap","member_benefits_per_order","slot_free"]} ``

### a2api-acom-names-batch · 1회차 · E MODEL_HTTP_500

토큰 52,493 · 61.303초 · 모델 호출 6회 · 도구 호출 6회 · 첫 요청 프롬프트 2,177토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> Run a 20% weekend sale on summer outerwear for VIP members and put it on the main page.

**질문 2**
> Drop the low-stock ones. Give the overshirt 15% instead.

_(이 실행은 호출이 어느 턴에 속하는지 기록하지 않았다. 호출을 순서대로 보인다.)_

1. 모델 → **`a2api_load`** `` {"names":["merchandising › category: list_categories","promotion › segment: list_segments","customer › membership: list_tiers","promotion › promotion: create_promotion","merchandising › banner: schedule_banner","catalog › product: get_product"]} ``
   ← 결과 110B: `` {"loaded":["list_categories","list_segments","list_tiers","create_promotion","schedule_banner","get_product"]} ``
2. 모델 → **`a2api_load`** `` {"names":["promotion › offer: set_sale_prices","merchandising › display_slot: list_display_slots","search › product: search_products"]} ``
   ← 결과 69B: `` {"loaded":["set_sale_prices","list_display_slots","search_products"]} ``
3. 모델 → **`a2api_batch`** `` {"calls":[{"name":"list_tiers","arguments":{}},{"name":"list_categories","arguments":{"term_set":"standard","fields":["id","name"]}},{"name":"list_display_slots","arguments":{"page":"main","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"}}]} ``
   ← 결과 2,687B: `` {"batch":[{"name":"list_tiers","result":{"status":"succeeded","data":{"items":[{"id":"vip","name":"VIP","rank":3,"program_id":"prg_rewards","member_count":1284},{"id":"gold","name":"Gold","rank":2,"program_id":"prg_rewards","member_count":2900},{"id":"member","name":"Member","rank":1,"program_id":"prg_rewards","member_count":9816}],"total":3}}},{"name":"list_categories","result":{"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear"},{"id":"cat_summer_outerwear","name":"Summer outerwear"},{"id":"cat_knitwear","name":"Knitwear"},{"id":"cat_shirts","name":"Shirts"},{"id"… (+900자) ``
4. 모델 → **`a2api_batch`** `` {"calls":[{"name":"search_products","arguments":{"category_id":"cat_summer_outerwear","limit":5,"fields":["id","name"]}},{"name":"set_sale_prices","arguments":{"name":"VIP weekend summer outerwear","valid_for_member_tier":"vip","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","scope_mode":"category","category_id":"cat_summer_outerwear","percent_off":20}}]} ``
   ← 결과 2,653B: `` {"batch":[{"name":"search_products","result":{"status":"succeeded","data":{"items":[{"id":"prd_summer_outerwear_13","name":"Poplin shacket"},{"id":"prd_summer_outerwear_22","name":"Seersucker shacket"},{"id":"prd_summer_outerwear_20","name":"Cotton anorak"},{"id":"prd_summer_outerwear_01","name":"Seersucker cagoule"},{"id":"prd_summer_outerwear_06","name":"Poplin harrington"}],"total":42,"next_cursor":"o5"}}},{"name":"set_sale_prices","result":{"status":"succeeded","data":{"preview_id":"pv_01m6b3mdvyat60z38bk6b9yzw0","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"t… (+900자) ``
5. 모델 → **`a2api_batch`** `` {"calls":[{"name":"search_products","arguments":{"query":"Seersucker overshirt","category_id":"cat_summer_outerwear","fields":["id","name"]}},{"name":"search_products","arguments":{"query":"Cotton chore coat","category_id":"cat_summer_outerwear","fields":["id","name"]}},{"name":"search_products","arguments":{"query":"Light rain parka","category_id":"cat_summer_outerwear","fields":["id","name"]}}]} ``
   ← 결과 3,882B: `` {"batch":[{"name":"search_products","result":{"status":"succeeded","data":{"items":[{"id":"prd_seersucker_overshirt","name":"Seersucker overshirt"},{"id":"prd_summer_outerwear_22","name":"Seersucker shacket"},{"id":"prd_summer_outerwear_27","name":"Seersucker bomber"},{"id":"prd_summer_outerwear_01","name":"Seersucker cagoule"},{"id":"prd_summer_outerwear_30","name":"Seersucker gilet"},{"id":"prd_camp_overshirt","name":"Linen camp overshirt"},{"id":"prd_summer_outerwear_15","name":"Cotton overshirt"},{"id":"prd_summer_outerwear_08","name":"Twill overshirt"},{"id":"prd_rain_parka","name":"Light… (+900자) ``
6. 모델 → **`a2api_batch`** `` {"calls":[{"name":"get_product","arguments":{"product_id":"prd_seersucker_overshirt"}},{"name":"get_product","arguments":{"product_id":"prd_chore_coat"}},{"name":"get_product","arguments":{"product_id":"prd_rain_parka"}}]} ``
   ← 결과 4,523B: `` {"batch":[{"name":"get_product","result":{"status":"succeeded","data":{"id":"prd_seersucker_overshirt","@type":"ProductGroup","name":"Seersucker overshirt","description":"A cotton seersucker overshirt for warm evenings.","brand_id":"brn_northwind","category_id":"cat_summer_outerwear","keywords":[],"approval_status":"active","varies_by":["color","size"],"image":"/media/garment/shirt-clay.svg","price":79.0,"price_currency":"USD","member_price":null,"cost":58.0,"inventory_level":53,"availability":"in_stock","additional_property":[{"name":"material","value":"Cotton"},{"name":"weight","value":360,"… (+900자) ``

_(모델 서버 오류(500)로 중단)_

**채점**: E MODEL_HTTP_500 — 빠진 것: tool create_coupon; tool schedule_banner; change set item create_coupon {}; change set item schedule_banner {'slot_id': 'slot_home_hero'}; fact "40 of 42 summer outerwear products; chore coat (7) and rain " (40, 42, 7, 4 not shown); fact "the overshirt is at 15% ($67.15) to stay above the price flo" (15, 67.15 not shown); HOST:MODEL_HTTP_500
(도구 정밀도 0.73, 재현율 0.60)
