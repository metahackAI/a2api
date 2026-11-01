# b1-vip-weekend-sale — ours-design-9

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> Run a 20% weekend sale on summer outerwear for VIP members and put it on the main page.

> Drop the low-stock ones. Give the overshirt 15% instead.

- 필요한 도구: `search_products`, `list_tiers`, `set_sale_prices`, `create_coupon`, `schedule_banner`
- 허용 도구: `get_policy`, `list_active_promotions`, `list_display_slots`, `list_categories`
- 답에 있어야 할 사실: 40 of 42 summer outerwear products; chore coat (7) and rain parka (4) are left out for low stock
- 답에 있어야 할 사실: the overshirt is at 15% ($67.15) to stay above the price floor
- change set: `` {"state":"drafting","version":2,"items":[{"tool":"set_sale_prices","args":{"valid_for_member_tier":"vip","percent_off":20}},{"tool":"create_coupon"},{"tool":"schedule_banner","args":{"slot_id":"slot_home_hero"}}],"checks_passed":["max_discount","price_floor","promo_min_stock","promotion_overlap","member_benefits_per_order","slot_free"]} ``

### a2api-acom-hybrid · 1회차 · E MODEL_CALL_LIMIT

토큰 97,562 · 69.053초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 4,607토큰

준비: 전략 `index`, 함수 253개, 목차 4,645자(system prompt)

**질문 1**
> Run a 20% weekend sale on summer outerwear for VIP members and put it on the main page.

**질문 2**
> Drop the low-stock ones. Give the overshirt 15% instead.

_(이 실행은 호출이 어느 턴에 속하는지 기록하지 않았다. 호출을 순서대로 보인다.)_

1. 모델 → **`a2api_load`** `` {"names":["list_tiers","search_product_groups","create_promotion","list_display_slots","schedule_banner"]} ``
   ← 결과 256B: `` {"loaded":["search_product_groups","create_promotion","list_display_slots","schedule_banner"],"already":["list_tiers"],"evicted":["list_display_slots","invalidate_display_cache","get_promotion","get_price_breakdown","get_sales_trend","get_sales_overview"]} ``
2. 모델 → **`list_tiers`** `` {} ``
   ← 결과 305B: `` {"status":"succeeded","data":{"items":[{"id":"vip","name":"VIP","rank":3,"program_id":"prg_rewards","member_count":1284},{"id":"gold","name":"Gold","rank":2,"program_id":"prg_rewards","member_count":2900},{"id":"member","name":"Member","rank":1,"program_id":"prg_rewards","member_count":9816}],"total":3}} ``
3. 모델 → **`search_product_groups`** `` {"query":"summer outerwear","limit":20} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
4. 모델 → **`search_product_groups`** `` {"query":"outerwear","limit":20} ``
   ← 결과 3,111B: `` {"status":"succeeded","data":{"items":[{"id":"prd_outerwear_01","@type":"ProductGroup","name":"Waxed cotton duffle coat","brand_id":"brn_ridgeline","category_id":"cat_outerwear","approval_status":"active","varies_by":["color","size"],"image":"/media/garment/chore-sky.svg","price":289.0,"price_currency":"USD","inventory_level":24,"availability":"in_stock","variant_count":10,"release_date":"2026-08-25","cost":134.5},{"id":"prd_outerwear_05","@type":"ProductGroup","name":"Waxed cotton shell jacket","brand_id":"brn_northwind","category_id":"cat_outerwear","approval_status":"active","varies_by":["c… (+900자) ``
5. 모델 → **`search_product_groups`** `` {"query":"summer","limit":20} ``
   ← 결과 3,799B: `` {"status":"succeeded","data":{"items":[{"id":"prd_sandals_01","@type":"ProductGroup","name":"Webbing trail sandals","brand_id":"brn_northwind","category_id":"cat_sandals","approval_status":"active","varies_by":["color","size"],"image":"/media/garment/shoe-sand.svg","price":49.0,"price_currency":"USD","inventory_level":42,"availability":"in_stock","variant_count":12,"release_date":"2026-08-19","cost":18.78},{"id":"prd_shoes_08","@type":"ProductGroup","name":"Leather boat shoes","brand_id":"brn_northwind","category_id":"cat_shoes","approval_status":"active","varies_by":["color","size"],"image":"… (+900자) ``
6. 모델 → **`a2api_load`** `` {"names":["list_categories","get_category"]} ``
   ← 결과 91B: `` {"loaded":["list_categories","get_category"],"evicted":["get_curation","create_promotion"]} ``
7. 모델 → **`list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
8. 모델 → **`get_category`** `` {"category_id":"cat_summer_outerwear"} ``
   ← 결과 283B: `` {"status":"succeeded","data":{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true,"description":null,"ancestor_ids":["cat_outerwear"],"mappings":[],"product_count":42}} ``
9. 모델 → **`a2api_load`** `` {"names":["search_product_groups","create_promotion"]} ``
   ← 결과 100B: `` {"loaded":["create_promotion"],"already":["search_product_groups"],"evicted":["list_display_slots"]} ``
10. 모델 → **`search_product_groups`** `` {"category_id":"cat_summer_outerwear","limit":100} ``
   ← 결과 3,950B: `` {"status":"succeeded","data":{"items":[{"id":"prd_summer_outerwear_13","@type":"ProductGroup","name":"Poplin shacket","brand_id":"brn_northwind","category_id":"cat_summer_outerwear","approval_status":"active","varies_by":["color","size"],"image":"/media/garment/field-olive.svg","price":99.0,"price_currency":"USD","inventory_level":14,"availability":"in_stock","variant_count":15,"release_date":"2026-06-28","cost":44.55},{"id":"prd_summer_outerwear_22","@type":"ProductGroup","name":"Seersucker shacket","brand_id":"brn_northwind","category_id":"cat_summer_outerwear","approval_status":"active","va… (+900자) ``
11. 모델 → **`a2api_load`** `` {"names":["set_sale_prices","list_display_slots"]} ``
   ← 결과 94B: `` {"loaded":["set_sale_prices","list_display_slots"],"evicted":["schedule_banner","list_tiers"]} ``
12. 모델 → **`list_display_slots`** `` {"page":"main","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","audience":"vip"} ``
   ← 결과 1,152B: `` {"status":"succeeded","data":{"items":[{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"]}],"availability":[{"audience":"vip","free_from":"2026-11-07T00:00:00-05:00","free_until":"2026-11-08T23:59:00-05:00"}]},{"id":"slot_home_new_in","page":"main","name":"New in","slot_type":"product_grid","bookings":[],"availa… (+552자) ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: tool search_products; tool set_sale_prices; tool create_coupon; tool schedule_banner; change set; fact "40 of 42 summer outerwear products; chore coat (7) and rain " (40, 42, 7, 4 not shown); fact "the overshirt is at 15% ($67.15) to stay above the price flo" (15, 67.15 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.38, 재현율 0.20)

### a2api-acom-hybrid · 2회차 · E MODEL_CALL_LIMIT

토큰 97,672 · 69.707초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 4,607토큰

준비: 전략 `index`, 함수 253개, 목차 4,645자(system prompt)

**질문 1**
> Run a 20% weekend sale on summer outerwear for VIP members and put it on the main page.

**질문 2**
> Drop the low-stock ones. Give the overshirt 15% instead.

_(이 실행은 호출이 어느 턴에 속하는지 기록하지 않았다. 호출을 순서대로 보인다.)_

1. 모델 → **`a2api_load`** `` {"names":["list_tiers","search_product_groups","create_promotion","list_display_slots","schedule_banner"]} ``
   ← 결과 256B: `` {"loaded":["search_product_groups","create_promotion","list_display_slots","schedule_banner"],"already":["list_tiers"],"evicted":["list_display_slots","invalidate_display_cache","get_promotion","get_price_breakdown","get_sales_trend","get_sales_overview"]} ``
2. 모델 → **`list_tiers`** `` {} ``
   ← 결과 305B: `` {"status":"succeeded","data":{"items":[{"id":"vip","name":"VIP","rank":3,"program_id":"prg_rewards","member_count":1284},{"id":"gold","name":"Gold","rank":2,"program_id":"prg_rewards","member_count":2900},{"id":"member","name":"Member","rank":1,"program_id":"prg_rewards","member_count":9816}],"total":3}} ``
3. 모델 → **`search_product_groups`** `` {"query":"summer outerwear","limit":20} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
4. 모델 → **`search_product_groups`** `` {"query":"outerwear","limit":20} ``
   ← 결과 3,111B: `` {"status":"succeeded","data":{"items":[{"id":"prd_outerwear_01","@type":"ProductGroup","name":"Waxed cotton duffle coat","brand_id":"brn_ridgeline","category_id":"cat_outerwear","approval_status":"active","varies_by":["color","size"],"image":"/media/garment/chore-sky.svg","price":289.0,"price_currency":"USD","inventory_level":24,"availability":"in_stock","variant_count":10,"release_date":"2026-08-25","cost":134.5},{"id":"prd_outerwear_05","@type":"ProductGroup","name":"Waxed cotton shell jacket","brand_id":"brn_northwind","category_id":"cat_outerwear","approval_status":"active","varies_by":["c… (+900자) ``
5. 모델 → **`search_product_groups`** `` {"query":"summer","limit":20} ``
   ← 결과 3,799B: `` {"status":"succeeded","data":{"items":[{"id":"prd_sandals_01","@type":"ProductGroup","name":"Webbing trail sandals","brand_id":"brn_northwind","category_id":"cat_sandals","approval_status":"active","varies_by":["color","size"],"image":"/media/garment/shoe-sand.svg","price":49.0,"price_currency":"USD","inventory_level":42,"availability":"in_stock","variant_count":12,"release_date":"2026-08-19","cost":18.78},{"id":"prd_shoes_08","@type":"ProductGroup","name":"Leather boat shoes","brand_id":"brn_northwind","category_id":"cat_shoes","approval_status":"active","varies_by":["color","size"],"image":"… (+900자) ``
6. 모델 → **`a2api_load`** `` {"names":["list_categories","get_category"]} ``
   ← 결과 91B: `` {"loaded":["list_categories","get_category"],"evicted":["get_curation","create_promotion"]} ``
7. 모델 → **`list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
8. 모델 → **`get_category`** `` {"category_id":"cat_summer_outerwear"} ``
   ← 결과 283B: `` {"status":"succeeded","data":{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true,"description":null,"ancestor_ids":["cat_outerwear"],"mappings":[],"product_count":42}} ``
9. 모델 → **`a2api_load`** `` {"names":["search_product_groups","create_promotion"]} ``
   ← 결과 100B: `` {"loaded":["create_promotion"],"already":["search_product_groups"],"evicted":["list_display_slots"]} ``
10. 모델 → **`search_product_groups`** `` {"category_id":"cat_summer_outerwear","limit":100} ``
   ← 결과 3,950B: `` {"status":"succeeded","data":{"items":[{"id":"prd_summer_outerwear_13","@type":"ProductGroup","name":"Poplin shacket","brand_id":"brn_northwind","category_id":"cat_summer_outerwear","approval_status":"active","varies_by":["color","size"],"image":"/media/garment/field-olive.svg","price":99.0,"price_currency":"USD","inventory_level":14,"availability":"in_stock","variant_count":15,"release_date":"2026-06-28","cost":44.55},{"id":"prd_summer_outerwear_22","@type":"ProductGroup","name":"Seersucker shacket","brand_id":"brn_northwind","category_id":"cat_summer_outerwear","approval_status":"active","va… (+900자) ``
11. 모델 → **`a2api_load`** `` {"names":["set_sale_prices","list_display_slots"]} ``
   ← 결과 94B: `` {"loaded":["set_sale_prices","list_display_slots"],"evicted":["schedule_banner","list_tiers"]} ``
12. 모델 → **`list_display_slots`** `` {"page":"main","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","audience":"vip"} ``
   ← 결과 1,152B: `` {"status":"succeeded","data":{"items":[{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"]}],"availability":[{"audience":"vip","free_from":"2026-11-07T00:00:00-05:00","free_until":"2026-11-08T23:59:00-05:00"}]},{"id":"slot_home_new_in","page":"main","name":"New in","slot_type":"product_grid","bookings":[],"availa… (+552자) ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: tool search_products; tool set_sale_prices; tool create_coupon; tool schedule_banner; change set; fact "40 of 42 summer outerwear products; chore coat (7) and rain " (40, 42, 7, 4 not shown); fact "the overshirt is at 15% ($67.15) to stay above the price flo" (15, 67.15 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.38, 재현율 0.20)
