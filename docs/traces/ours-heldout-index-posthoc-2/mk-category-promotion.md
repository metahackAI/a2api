# mk-category-promotion — ours-heldout-index-posthoc-2

[← 실행 묶음](README.md) · 세트 `held_out` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 필요한 도구: `create_promotion`
- 허용 도구: `list_categories`, `list_active_promotions`, `get_policy`
- 답에 있어야 할 사실: 2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store time

### a2api-acom · 1회차 · E MODEL_CALL_LIMIT

토큰 76,895 · 96.413초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 5,114토큰

준비: 전략 `search`, 함수 8개

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

1. 모델 → **`a2api_search`** `` {"query":"list categories"} ``
   ← 결과 447B: `` {"selected":[{"name":"acom_list_categories","id":"acom.list_categories"},{"name":"acom_get_contract","id":"acom.get_contract"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_list_faqs","id":"acom.list_faqs"}],"evicted":["acom_create_promotion","acom_create_coupon","acom_get_sales_trend"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"create promotion"} ``
   ← 결과 568B: `` {"selected":[{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_get_promotion","id":"acom.get_promotion"},{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"}],"evicted":["acom_create_conditional_gift","acom_list_display_slots","acom_get_price_breakdown","acom_set_installment","acom_list_categories","acom_get_contract","acom_search_products"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`acom_search_promotions`** `` {"query":"outerwear","limit":20} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
4. 모델 → **`a2api_search`** `` {"query":"list categories"} ``
   ← 결과 606B: `` {"selected":[{"name":"acom_list_categories","id":"acom.list_categories"},{"name":"acom_get_contract","id":"acom.get_contract"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_list_faqs","id":"acom.list_faqs"}],"evicted":["acom_set_sale_prices","acom_list_faqs","acom_create_promotion"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":false,"note":"No new functions: every match was already offered in this conversation. If they cannot answer, tell the user what is missing instead of searching ag… (+6자) ``
5. 모델 → **`a2api_search`** `` {"query":"create order discount promotion"} ``
   ← 결과 557B: `` {"selected":[{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_update_promotion","id":"acom.update_promotion"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"}],"evicted":["acom_create_coupon","acom_get_promotion","acom_pause_promotion","acom_search_promotions","acom_list_categories","acom_get_contract","acom_search_products"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
6. 모델 → **`a2api_search`** `` {"query":"list categories","more":true} ``
   ← 결과 416B: `` {"selected":[{"name":"acom_list_notices","id":"acom.list_notices"},{"name":"acom_list_wishlist","id":"acom.list_wishlist"},{"name":"acom_create_category","id":"acom.create_category"},{"name":"acom_get_category","id":"acom.get_category"},{"name":"acom_map_category","id":"acom.map_category"}],"evicted":["acom_list_faqs","acom_create_promotion"],"moreAvailable":true,"page":2,"pageLimitReached":false,"progress":true} ``
7. 모델 → **`a2api_search`** `` {"query":"list categories"} ``
   ← 결과 526B: `` {"selected":[{"name":"acom_list_notices","id":"acom.list_notices"},{"name":"acom_list_wishlist","id":"acom.list_wishlist"},{"name":"acom_create_category","id":"acom.create_category"},{"name":"acom_get_category","id":"acom.get_category"},{"name":"acom_map_category","id":"acom.map_category"}],"moreAvailable":true,"page":2,"pageLimitReached":false,"progress":false,"note":"No new functions: every match was already offered in this conversation. If they cannot answer, tell the user what is missing instead of searching again."} ``
8. 모델 → **`a2api_search`** `` {"query":"create promotion order discount"} ``
   ← 결과 740B: `` {"selected":[{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_update_promotion","id":"acom.update_promotion"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"}],"evicted":["acom_create_coupon","acom_search_promotions","acom_update_promotion","acom_set_sale_prices","acom_list_notices","acom_list_wishlist","acom_create_category","acom_get_category"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functio… (+140자) ``
9. 모델 → **`a2api_search`** `` {"query":"search products"} ``
   ← 결과 495B: `` {"selected":[{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_search_product_groups","id":"acom.search_product_groups"},{"name":"acom_autocomplete","id":"acom.autocomplete"},{"name":"acom_get_index_status","id":"acom.get_index_status"},{"name":"acom_create_curation","id":"acom.create_curation"}],"evicted":["acom_map_category","acom_create_promotion","acom_create_coupon","acom_search_promotions"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
10. 모델 → **`acom_search_products`** `` {"query":"Outerwear","limit":20} ``
   ← 결과 3,373B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/parka-stone.svg","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_stock"},{"variant… (+900자) ``
11. 모델 → **`a2api_search`** `` {"query":"create promotion"} ``
   ← 결과 701B: `` {"selected":[{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_get_promotion","id":"acom.get_promotion"},{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"}],"evicted":["acom_update_promotion","acom_set_sale_prices","acom_search_product_groups","acom_autocomplete","acom_get_index_status","acom_create_curation"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":false,"note":"No new functions: every match was already offered in … (+101자) ``
12. 모델 → **`acom_search_products`** `` {"query":"outerwear","limit":100} ``
   ← 결과 3,353B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/parka-stone.svg","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_stock"},{"variant… (+900자) ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: tool create_promotion; fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (2, 6, 19, 23, 59 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.00, 재현율 0.00)

### a2api-acom · 2회차 · E MODEL_CALL_LIMIT

토큰 72,926 · 58.738초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 5,114토큰

준비: 전략 `search`, 함수 8개

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

1. 모델 → **`a2api_search`** `` {"query":"category"} ``
   ← 결과 409B: `` {"selected":[{"name":"acom_create_category","id":"acom.create_category"},{"name":"acom_get_category","id":"acom.get_category"},{"name":"acom_list_categories","id":"acom.list_categories"},{"name":"acom_map_category","id":"acom.map_category"},{"name":"acom_update_category","id":"acom.update_category"}],"evicted":["acom_create_promotion"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"promotion","more":true} ``
   ← 실패 110B: `` {"status":"failed","error":{"code":"SEARCH_NOT_STARTED","detail":"Search this query before requesting more."}} ``
3. 모델 → **`a2api_search`** `` {"query":"promotion"} ``
   ← 결과 470B: `` {"selected":[{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_end_promotion","id":"acom.end_promotion"},{"name":"acom_get_promotion","id":"acom.get_promotion"},{"name":"acom_update_promotion","id":"acom.update_promotion"}],"evicted":["acom_create_coupon","acom_get_sales_trend","acom_create_conditional_gift"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`a2api_search`** `` {"query":"create promotion"} ``
   ← 결과 699B: `` {"selected":[{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_get_promotion","id":"acom.get_promotion"},{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"}],"evicted":["acom_list_display_slots","acom_get_price_breakdown","acom_set_installment","acom_create_category","acom_get_category","acom_list_categories"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match was already offered in th… (+99자) ``
5. 모델 → **`a2api_search`** `` {"query":"list categories"} ``
   ← 결과 491B: `` {"selected":[{"name":"acom_list_categories","id":"acom.list_categories"},{"name":"acom_get_contract","id":"acom.get_contract"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_list_faqs","id":"acom.list_faqs"}],"evicted":["acom_map_category","acom_update_category","acom_end_promotion","acom_update_promotion","acom_create_promotion"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
6. 모델 → **`a2api_search`** `` {"query":"order discount promotion"} ``
   ← 결과 719B: `` {"selected":[{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_update_promotion","id":"acom.update_promotion"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"}],"evicted":["acom_create_coupon","acom_get_promotion","acom_pause_promotion","acom_search_promotions","acom_list_categories","acom_get_contract","acom_search_products"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match was a… (+119자) ``
7. 모델 → **`acom_list_categories`** `` {} ``
   ← 실패 198B: `` {"status":"failed","error":{"code":"NOT_SELECTED","detail":"Function is not active in this session; search again."},"hint":"Call only functions currently provided; search if a function is missing."} ``
8. 모델 → **`a2api_search`** `` {"query":"list categories"} ``
   ← 결과 583B: `` {"selected":[{"name":"acom_list_categories","id":"acom.list_categories"},{"name":"acom_get_contract","id":"acom.get_contract"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_list_faqs","id":"acom.list_faqs"}],"evicted":["acom_list_faqs","acom_create_promotion"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":false,"note":"No new functions: every match was already offered in this conversation. If they cannot answer, tell the user what is missing instead of searching again."} ``
9. 모델 → **`a2api_search`** `` {"query":"create promotion"} ``
   ← 결과 694B: `` {"selected":[{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_get_promotion","id":"acom.get_promotion"},{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"}],"evicted":["acom_create_coupon","acom_search_promotions","acom_update_promotion","acom_list_categories","acom_get_contract","acom_search_products"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":false,"note":"No new functions: every match was already offered in this co… (+94자) ``
10. 모델 → **`acom_list_categories`** `` {} ``
   ← 실패 269B: `` {"status":"failed","error":{"code":"NOT_SELECTED","detail":"Function is not active in this session; search again."},"hint":"This exact call already failed 1 time(s); repeating it will fail again. Change the arguments as the error says, or tell the user what is wrong."} ``
11. 모델 → **`a2api_search`** `` {"query":"category list"} ``
   ← 결과 605B: `` {"selected":[{"name":"acom_list_categories","id":"acom.list_categories"},{"name":"acom_get_contract","id":"acom.get_contract"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_list_faqs","id":"acom.list_faqs"}],"evicted":["acom_set_sale_prices","acom_list_faqs","acom_create_promotion"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match was already offered in this conversation. If they cannot answer, tell the user what is missing instead of searching aga… (+5자) ``
12. 모델 → **`acom_search_products`** `` {"query":"Outerwear","limit":1} ``
   ← 결과 896B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/parka-stone.svg","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_stock"},{"variant… (+296자) ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: tool create_promotion; fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (2, 6, 19, 23, 59 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.00, 재현율 0.00)

### a2api-acom-index · 1회차 · ✗ 실패

토큰 40,251 · 42.854초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 6,994토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

1. 모델 → **`a2api_load`** `` {"names":["create_promotion","list_categories","get_category"]} ``
   ← 결과 64B: `` {"loaded":["create_promotion","list_categories","get_category"]} ``
2. 모델 → **`list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
3. 모델 → **`create_promotion`** `` {"name":"$50 off Outerwear orders $250+","promotion_type":"threshold","discount_layer":"order_discount","amount_off":{"value":50,"currency":"USD"},"threshold":{"value":250,"currency":"USD"},"threshold_benefit":"amount_off","valid_from":"2026-11-06T11:00","valid_through":"2026-11-20T23:59","scope_mode":"categories","category_ids":["cat_outerwear"]} ``
   ← 결과 1,418B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6atjc0g67bzatc1gwwp4mj5","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"$50 off Outerwear orders $250+","promotion_type":"threshold","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-06T11:00:00-05:00","valid_through":"2026-11-20T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_outerwear"],"product_count":62},"amount_off":{"value":50.0,"currency":"USD"},"threshold":{"value":250.0,"currency":"USD"},"threshold_benefit":"amount_off"}}],"checks… (+816자) ``

**답변 1**
> The promotion is drafted as a preview waiting for approval.
>
> * **Name:** $50 off Outerwear orders $250+
> * **Type:** threshold → $50 off the order
> * **Discount layer:** order_discount
> * **Scope:** categories `cat_outerwear` – Outerwear
>   * Applies to 62 products in the category (sub-categories included)
> * **Threshold:** $250.00 USD subtotal before member benefits
> * **Benefit:** $50.00 USD off
> * **Member tier:** everyone
> * **Valid:** 2026-11-06T11:00:00-05:00 → 2026-11-20T23:59:00-05:00  (2 weeks from store time)
> * **Change set:** cs_1042, preview pv_01m6atjc0g67bzatc1gwwp4mj5
>
> Checks on the preview:
> * max_discount: passed – at most 20% on a $250 order; limit 20%
> * price_floor: **failed** – Seersucker overshirt would be $63.20, under the floor $66.70
> * promotion_overlap: **failed** – Denim bundle (everyone), Birthday coupon (member) and Gold tier 10% (gold) already give an order discount on outerwear in this period
> * discount_layers.max_total_discount_rate: passed – combined discount stays under 50% (at most 20%)
> * cost_share.sum_must_equal: passed – Store 100%
>
> The change is not live yet; it needs operator approval before it can be published.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (6, 19, 23 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-index · 2회차 · ✗ 실패

토큰 39,878 · 38.295초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 6,994토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

1. 모델 → **`a2api_load`** `` {"names":["list_categories","create_promotion","get_category"]} ``
   ← 결과 64B: `` {"loaded":["list_categories","create_promotion","get_category"]} ``
2. 모델 → **`list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
3. 모델 → **`create_promotion`** `` {"name":"$50 off Outerwear orders $250+","promotion_type":"threshold","discount_layer":"order_discount","amount_off":{"value":50,"currency":"USD"},"threshold":{"value":250,"currency":"USD"},"threshold_benefit":"amount_off","valid_from":"2026-11-06T00:00","valid_through":"2026-11-19T23:59","scope_mode":"categories","category_ids":["cat_outerwear"]} ``
   ← 결과 1,418B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6ayed28damweekga1f7317j","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"$50 off Outerwear orders $250+","promotion_type":"threshold","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-06T00:00:00-05:00","valid_through":"2026-11-19T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_outerwear"],"product_count":62},"amount_off":{"value":50.0,"currency":"USD"},"threshold":{"value":250.0,"currency":"USD"},"threshold_benefit":"amount_off"}}],"checks… (+816자) ``

**답변 1**
> Created a preview for the Outerwear threshold promotion — it’s waiting for approval in change set **cs_1042** (preview pv_01m6ayed28damweekga1f7317j).
>
> * Name: $50 off Outerwear orders $250+
> * Type: threshold, discount_layer = order_discount
> * Benefit: $50.00 USD off when subtotal before member benefits ≥ $250.00 USD
> * Scope: categories → cat_outerwear
>   * Applies to 62 products in cat_outerwear (subcategories included, e.g. cat_summer_outerwear)
> * Audience: everyone
> * Period in store time America/New_York:
>   * valid_from: 2026-11-06T00:00:00-05:00
>   * valid_through: 2026-11-19T23:59:00-05:00  → 2 weeks from today
>
> Checks on the preview:
> * max_discount: passed
> * price_floor: **failed** – Seersucker overshirt would be $63.20, under the floor $66.70
> * promotion_overlap: **failed** – Denim bundle (everyone), Birthday coupon (member) and Gold tier 10% (gold) already give an order discount on outerwear in this period
> * discount_layers.max_total_discount_rate: passed
> * cost_share.sum_must_equal: passed
>
> The change is a preview only. It needs an operator’s approval before it can be published.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (6, 19, 23 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names · 1회차 · ✓ 통과

토큰 19,707 · 31.591초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 1,635토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

1. 모델 → **`a2api_load`** `` {"names":["create_promotion","search_product_groups","list_categories"]} ``
   ← 결과 73B: `` {"loaded":["create_promotion","search_product_groups","list_categories"]} ``
2. 모델 → **`list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,450B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
3. 모델 → **`create_promotion`** `` {"name":"$50 off Outerwear orders $250+","promotion_type":"threshold","discount_layer":"order_discount","amount_off":{"value":50,"currency":"USD"},"threshold":{"value":250,"currency":"USD"},"threshold_benefit":"amount_off","valid_from":"2026-11-06T00:00","valid_through":"2026-11-19T23:59","scope_mode":"categories","category_ids":["cat_outerwear"]} ``
   ← 결과 1,565B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6atkwaegrbg2qvjg21kjzsm","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"$50 off Outerwear orders $250+","promotion_type":"threshold","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-06T00:00:00-05:00","valid_through":"2026-11-19T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_outerwear"],"product_count":62},"amount_off":{"value":50.0,"currency":"USD"},"threshold":{"value":250.0,"currency":"USD"},"threshold_benefit":"amount_off"}}],"checks… (+900자) ``

**답변 1**
> Created a preview for the Outerwear threshold promotion.
>
> * Name: $50 off Outerwear orders $250+
> * Type: threshold, order_discount, $50 off when subtotal ≥ $250
> * Scope: categories cat_outerwear (62 products, subcategories included)
> * Valid: 2026-11-06 00:00 to 2026-11-19 23:59 America/New_York (2 weeks)
> * Preview ID: pv_01m6atkwaegrbg2qvjg21kjzsm
> * Change set: cs_1042 — waiting for approval
>
> Checks:
> * max_discount: passed
> * price_floor: failed — Seersucker overshirt would be $63.20, under the floor $66.70
> * promotion_overlap: failed — Denim bundle (everyone), Birthday coupon (member) and Gold tier 10% (gold) already give an order discount on outerwear in this period
> * discount_layers.max_total_discount_rate: passed
> * cost_share.sum_must_equal: passed
>
> The promotion is not live yet; it needs approval and the price-floor / overlap issues should be addressed before publishing.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names · 2회차 · ✓ 통과

토큰 27,913 · 58.58초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 1,635토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

1. 모델 → **`a2api_load`** `` {"names":["create_promotion","get_category","list_categories","search_products"]} ``
   ← 결과 82B: `` {"loaded":["create_promotion","get_category","list_categories","search_products"]} ``
2. 모델 → **`list_categories`** `` {"term_set":"standard","fields":["id","name","parent_id"],"limit":100} ``
   ← 결과 1,611B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","parent_id":null},{"id":"cat_summer_outerwear","name":"Summer outerwear","parent_id":"cat_outerwear"},{"id":"cat_knitwear","name":"Knitwear","parent_id":null},{"id":"cat_shirts","name":"Shirts","parent_id":null},{"id":"cat_tees","name":"Tees","parent_id":null},{"id":"cat_sweatshirts","name":"Sweatshirts","parent_id":null},{"id":"cat_pants","name":"Pants","parent_id":null},{"id":"cat_denim","name":"Denim","parent_id":null},{"id":"cat_shorts","name":"Shorts","parent_id":null},{"id":"cat_dresses","name":"Dresses","par… (+900자) ``
3. 모델 → **`get_category`** `` {"category_id":"cat_outerwear","fields":["name","product_count"]} ``
   ← 결과 90B: `` {"status":"succeeded","data":{"id":"cat_outerwear","name":"Outerwear","product_count":62}} ``
4. 모델 → **`create_promotion`** `` {"name":"$50 off $250+","promotion_type":"threshold","discount_layer":"order_discount","amount_off":{"value":50,"currency":"USD"},"threshold":{"value":250,"currency":"USD"},"threshold_benefit":"amount_off","valid_from":"2026-11-06T00:00","valid_through":"2026-11-19T23:59","scope_mode":"categories","category_ids":["cat_outerwear"]} ``
   ← 결과 1,548B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6ayb15t65varrd2tkh7ysm2","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"$50 off $250+","promotion_type":"threshold","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-06T00:00:00-05:00","valid_through":"2026-11-19T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_outerwear"],"product_count":62},"amount_off":{"value":50.0,"currency":"USD"},"threshold":{"value":250.0,"currency":"USD"},"threshold_benefit":"amount_off"}}],"checks":[{"rule":"max_d… (+900자) ``

**답변 1**
> Created a preview for the Outerwear promotion.
>
> * Name: $50 off $250+
> * Type: threshold – $50 off the order when subtotal ≥ $250
> * Scope: category cat_outerwear (Outerwear, 62 products, includes subcategories)
> * Discount layer: order_discount
> * Valid: 2026-11-06 00:00 to 2026-11-19 23:59 America/New_York (2 weeks)
> * Member tier: everyone
>
> Preview ID: pv_01m6ayb15t65varrd2tkh7ysm2
> Change set: cs_1042 – waiting for approval.
>
> Checks:
> * max_discount: passed
> * price_floor: failed – Seersucker overshirt would be $63.20, under the floor $66.70
> * promotion_overlap: failed – Denim bundle (everyone), Birthday coupon (member) and Gold tier 10% (gold) already give an order discount on outerwear in this period
> * discount_layers.max_total_discount_rate: passed
> * cost_share.sum_must_equal: passed
>
> The change is a preview only and needs approval before it goes live.

**채점**: ✓ 통과
(도구 정밀도 0.67, 재현율 1.00)
