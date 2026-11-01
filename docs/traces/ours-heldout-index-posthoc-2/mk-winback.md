# mk-winback — ours-heldout-index-posthoc-2

[← 실행 묶음](README.md) · 세트 `held_out` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> set up a win-back for customers who haven't ordered in 90 days. 15% off, email

- 필요한 도구: `define_segment`, `send_bulk`
- 허용 도구: `preview_segment`, `search_members`, `create_coupon`, `list_message_templates`
- 답에 있어야 할 사실: the segment size is shown before anything is sent

### a2api-acom · 1회차 · E MODEL_CALL_LIMIT

토큰 85,381 · 94.843초 · 모델 호출 12회 · 도구 호출 16회 · 첫 요청 프롬프트 5,265토큰

준비: 전략 `search`, 함수 8개

**질문 1**
> set up a win-back for customers who haven't ordered in 90 days. 15% off, email

1. 모델 → **`a2api_search`** `` {"query":"set sale prices percent off tier"} ``
   ← 결과 540B: `` {"selected":[{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_list_active_promotions","id":"acom.list_active_promotions"},{"name":"acom_set_price","id":"acom.set_price"},{"name":"acom_get_promotion","id":"acom.get_promotion"}],"evicted":["acom_create_campaign","acom_send_password_reset","acom_get_return_history","acom_respond_inquiry","acom_dispatch_reward","acom_search_orders"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"percent off promotion"} ``
   ← 결과 396B: `` {"selected":[{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"}],"omitted":[{"id":"acom.end_promotion","reason":"SCHEMA_BUDGET"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`a2api_search`** `` {"query":"win back segment lapsed"} ``
   ← 결과 414B: `` {"selected":[{"name":"acom_list_segments","id":"acom.list_segments"},{"name":"acom_preview_segment","id":"acom.preview_segment"},{"name":"acom_define_segment","id":"acom.define_segment"}],"omitted":[{"id":"acom.issue_coupon","reason":"SCHEMA_BUDGET"},{"id":"acom.create_campaign","reason":"SCHEMA_BUDGET"}],"evicted":["acom_create_promotion"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`acom_list_segments`** `` {} ``
   ← 결과 467B: `` {"status":"succeeded","data":{"items":[{"id":"seg_lapsed_knit_buyers","name":"Lapsed knit buyers","version":1,"estimated_size":22,"estimated_at":"2026-11-06T09:00:00-05:00","condition_rules":{"exclude_segment_ids":["seg_recent_buyers"],"purchased_category_ids":["cat_knitwear"]}},{"id":"seg_recent_buyers","name":"Recent buyers","version":1,"estimated_size":5143,"estimated_at":"2026-11-06T09:00:00-05:00","condition_rules":{"last_order_within_days":30}}],"total":2}} ``
5. 모델 → **`a2api_search`** `` {"query":"email campaign send"} ``
   ← 결과 480B: `` {"selected":[{"name":"acom_search_campaigns","id":"acom.search_campaigns"},{"name":"acom_get_campaign","id":"acom.get_campaign"},{"name":"acom_create_campaign","id":"acom.create_campaign"},{"name":"acom_send_bulk","id":"acom.send_bulk"},{"name":"acom_send_password_reset","id":"acom.send_password_reset"}],"evicted":["acom_list_active_promotions","acom_set_price","acom_get_promotion","acom_set_sale_prices"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
6. 모델 → **`a2api_search`** `` {"query":"create campaign email"} ``
   ← 결과 455B: `` {"selected":[{"name":"acom_create_campaign","id":"acom.create_campaign"},{"name":"acom_explain_sales_change","id":"acom.explain_sales_change"},{"name":"acom_create_admin_user","id":"acom.create_admin_user"},{"name":"acom_search_campaigns","id":"acom.search_campaigns"},{"name":"acom_get_campaign","id":"acom.get_campaign"}],"evicted":["acom_pause_promotion","acom_search_promotions"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
7. 모델 → **`a2api_search`** `` {"query":"coupon issue"} ``
   ← 결과 437B: `` {"selected":[{"name":"acom_issue_coupon","id":"acom.issue_coupon"},{"name":"acom_get_coupon","id":"acom.get_coupon"},{"name":"acom_issue_api_key","id":"acom.issue_api_key"},{"name":"acom_issue_receipt","id":"acom.issue_receipt"},{"name":"acom_search_coupons","id":"acom.search_coupons"}],"evicted":["acom_preview_segment","acom_define_segment","acom_list_segments"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
8. 모델 → **`acom_search_coupons`** `` {"limit":100} ``
   ← 결과 539B: `` {"status":"succeeded","data":{"items":[{"id":"cpn_birthday","code":"BIRTHDAY10","name":"Birthday coupon","promotion_id":"promo_birthday","valid_for_member_tier":"member","application":"download","stacking":"no_other_coupons","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null},{"id":"cpn_gold_10","code":"GOLD10","name":"Gold tier 10%","promotion_id":"promo_gold_10","valid_for_member_tier":"gold","application":"download","stacking":"no_other_coupons","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null}],"total":2}} ``
9. 모델 → **`a2api_search`** `` {"query":"define segment"} ``
   ← 결과 531B: `` {"selected":[{"name":"acom_define_segment","id":"acom.define_segment"},{"name":"acom_list_segments","id":"acom.list_segments"},{"name":"acom_preview_segment","id":"acom.preview_segment"},{"name":"acom_set_menu","id":"acom.set_menu"},{"name":"acom_manage_shipping_zone","id":"acom.manage_shipping_zone"}],"evicted":["acom_send_bulk","acom_send_password_reset","acom_create_campaign","acom_explain_sales_change","acom_create_admin_user","acom_search_campaigns"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
10. 모델 → **`a2api_search`** `` {"query":"create campaign"} ``
   ← 결과 535B: `` {"selected":[{"name":"acom_create_campaign","id":"acom.create_campaign"},{"name":"acom_search_campaigns","id":"acom.search_campaigns"},{"name":"acom_get_campaign","id":"acom.get_campaign"},{"name":"acom_create_category","id":"acom.create_category"},{"name":"acom_create_product","id":"acom.create_product"}],"evicted":["acom_get_campaign","acom_issue_coupon","acom_get_coupon","acom_issue_api_key","acom_issue_receipt","acom_search_coupons","acom_define_segment"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
11. 모델 → **`a2api_search`** `` {"query":"define segment"} ``
   ← 결과 661B: `` {"selected":[{"name":"acom_define_segment","id":"acom.define_segment"},{"name":"acom_list_segments","id":"acom.list_segments"},{"name":"acom_preview_segment","id":"acom.preview_segment"},{"name":"acom_set_menu","id":"acom.set_menu"},{"name":"acom_manage_shipping_zone","id":"acom.manage_shipping_zone"}],"evicted":["acom_list_segments","acom_preview_segment","acom_set_menu","acom_manage_shipping_zone","acom_create_campaign"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":false,"note":"No new functions: every match was already offered in this conversation. If they cannot answer… (+61자) ``
12. 모델 → **`acom_define_segment`** `` {"name":"Active 90 days","condition_rules":{"last_order_within_days":90}} ``
   ← 결과 336B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6atxst17rshg78wbk6z5mfw","expires_at":null,"changes":[{"op":"create","entity":"segment","id":null,"to":{"name":"Active 90 days","condition_rules":{"last_order_within_days":90},"estimated_size":5960}}],"checks":[],"needs_approval":false,"approval_reason":null,"change_set_id":"cs_1042"}} ``
13. 모델 → **`acom_preview_segment`** `` {"condition_rules":{"last_order_within_days":90},"sample_size":5} ``
   ← 결과 182B: `` {"status":"succeeded","data":{"estimated_size":5960,"sample_customer_ids":["cus_4431","cus_alex","cus_dana","cus_elena","cus_grace"],"by_tier":{"gold":1645,"member":3396,"vip":919}}} ``
14. 모델 → **`acom_define_segment`** `` {"name":"Lapsed 90 days","condition_rules":{"last_order_within_days":90,"exclude_segment_ids":["seg_recent_buyers"]}} ``
   ← 결과 379B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6atxx56bch551krn2c2qj91","expires_at":null,"changes":[{"op":"create","entity":"segment","id":null,"to":{"name":"Lapsed 90 days","condition_rules":{"last_order_within_days":90,"exclude_segment_ids":["seg_recent_buyers"]},"estimated_size":817}}],"checks":[],"needs_approval":false,"approval_reason":null,"change_set_id":"cs_1042"}} ``
15. 모델 → **`acom_preview_segment`** `` {"condition_rules":{"last_order_within_days":90,"exclude_segment_ids":["seg_recent_buyers"]},"sample_size":5} ``
   ← 결과 188B: `` {"status":"succeeded","data":{"estimated_size":817,"sample_customer_ids":["cus_dana","cus_m000038","cus_m000075","cus_m000131","cus_m000147"],"by_tier":{"gold":213,"member":511,"vip":93}}} ``
16. 모델 → **`a2api_search`** `` {"query":"last_order_within_days segment"} ``
   ← 결과 468B: `` {"selected":[{"name":"acom_define_segment","id":"acom.define_segment"},{"name":"acom_get_seller_grade","id":"acom.get_seller_grade"},{"name":"acom_get_seller_overview","id":"acom.get_seller_overview"},{"name":"acom_suggest_reorder","id":"acom.suggest_reorder"},{"name":"acom_list_segments","id":"acom.list_segments"}],"evicted":["acom_search_campaigns","acom_get_campaign","acom_create_category"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: tool send_bulk; HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.67, 재현율 0.50)

### a2api-acom · 2회차 · E MODEL_CALL_LIMIT

토큰 80,151 · 79.235초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 5,265토큰

준비: 전략 `search`, 함수 8개

**질문 1**
> set up a win-back for customers who haven't ordered in 90 days. 15% off, email

1. 모델 → **`a2api_search`** `` {"query":"segment"} ``
   ← 결과 528B: `` {"selected":[{"name":"acom_list_segments","id":"acom.list_segments"},{"name":"acom_preview_segment","id":"acom.preview_segment"},{"name":"acom_define_segment","id":"acom.define_segment"},{"name":"acom_issue_coupon","id":"acom.issue_coupon"},{"name":"acom_create_campaign","id":"acom.create_campaign"}],"evicted":["acom_create_campaign","acom_send_password_reset","acom_get_return_history","acom_respond_inquiry","acom_dispatch_reward","acom_search_orders"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"sale price"} ``
   ← 결과 463B: `` {"selected":[{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_get_price_breakdown","id":"acom.get_price_breakdown"},{"name":"acom_set_price","id":"acom.set_price"},{"name":"acom_get_promotion","id":"acom.get_promotion"},{"name":"acom_calculate_benefits","id":"acom.calculate_benefits"}],"evicted":["acom_create_promotion","acom_list_segments","acom_preview_segment"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`a2api_search`** `` {"query":"coupon"} ``
   ← 결과 450B: `` {"selected":[{"name":"acom_search_coupons","id":"acom.search_coupons"},{"name":"acom_list_member_coupons","id":"acom.list_member_coupons"},{"name":"acom_revoke_coupon","id":"acom.revoke_coupon"},{"name":"acom_get_coupon","id":"acom.get_coupon"},{"name":"acom_create_coupon","id":"acom.create_coupon"}],"evicted":["acom_define_segment","acom_issue_coupon","acom_create_campaign"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`a2api_search`** `` {"query":"campaign"} ``
   ← 결과 459B: `` {"selected":[{"name":"acom_search_campaigns","id":"acom.search_campaigns"},{"name":"acom_get_campaign","id":"acom.get_campaign"},{"name":"acom_create_campaign","id":"acom.create_campaign"},{"name":"acom_send_bulk","id":"acom.send_bulk"},{"name":"acom_explain_sales_change","id":"acom.explain_sales_change"}],"evicted":["acom_set_sale_prices","acom_get_price_breakdown","acom_set_price"],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true} ``
5. 모델 → **`a2api_search`** `` {"query":"promotion"} ``
   ← 결과 512B: `` {"selected":[{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_end_promotion","id":"acom.end_promotion"},{"name":"acom_get_promotion","id":"acom.get_promotion"},{"name":"acom_update_promotion","id":"acom.update_promotion"}],"evicted":["acom_get_promotion","acom_calculate_benefits","acom_search_coupons","acom_list_member_coupons","acom_revoke_coupon"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
6. 모델 → **`acom_search_promotions`** `` {"query":"win-back","limit":20} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
7. 모델 → **`acom_search_promotions`** `` {"limit":20} ``
   ← 결과 1,315B: `` {"status":"succeeded","data":{"items":[{"id":"promo_denim_bundle","name":"Denim bundle","status":"scheduled","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-13T00:00:00-05:00","valid_through":"2026-11-20T23:59:00-05:00"},{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00"},{"id":"promo_linen_clearance","name":"Linen clearance","status":"ended","discount_layer":"item_price","valid_fo… (+715자) ``
8. 모델 → **`acom_search_campaigns`** `` {"channel":"email","limit":20} ``
   ← 결과 1,470B: `` {"status":"succeeded","data":{"items":[{"id":"cmp_vip_weekend","name":"VIP weekend reminder","channel":"email","template_id":"tpl_vip_weekend","status":"draft","scheduled_time":null,"date_sent":null,"recipient_count":null,"error_message":null},{"id":"cmp_weekly_1105","name":"Weekly email","channel":"email","template_id":"tpl_weekly_email","status":"failed","scheduled_time":"2026-11-05T08:00:00-05:00","date_sent":null,"recipient_count":null,"error_message":"List import failed"},{"id":"cmp_weekly_1029","name":"Weekly email","channel":"email","template_id":"tpl_weekly_email","status":"sent","sche… (+870자) ``
9. 모델 → **`a2api_search`** `` {"query":"list segments"} ``
   ← 결과 674B: `` {"selected":[{"name":"acom_list_segments","id":"acom.list_segments"},{"name":"acom_issue_coupon","id":"acom.issue_coupon"},{"name":"acom_create_campaign","id":"acom.create_campaign"},{"name":"acom_preview_segment","id":"acom.preview_segment"},{"name":"acom_define_segment","id":"acom.define_segment"}],"evicted":["acom_get_coupon","acom_create_coupon","acom_get_campaign","acom_send_bulk","acom_explain_sales_change","acom_pause_promotion"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match was already offered in this conversation. If they … (+74자) ``
10. 모델 → **`acom_list_segments`** `` {"limit":100} ``
   ← 결과 467B: `` {"status":"succeeded","data":{"items":[{"id":"seg_lapsed_knit_buyers","name":"Lapsed knit buyers","version":1,"estimated_size":22,"estimated_at":"2026-11-06T09:00:00-05:00","condition_rules":{"exclude_segment_ids":["seg_recent_buyers"],"purchased_category_ids":["cat_knitwear"]}},{"id":"seg_recent_buyers","name":"Recent buyers","version":1,"estimated_size":5143,"estimated_at":"2026-11-06T09:00:00-05:00","condition_rules":{"last_order_within_days":30}}],"total":2}} ``
11. 모델 → **`a2api_search`** `` {"query":"search coupons"} ``
   ← 결과 662B: `` {"selected":[{"name":"acom_search_coupons","id":"acom.search_coupons"},{"name":"acom_list_member_coupons","id":"acom.list_member_coupons"},{"name":"acom_revoke_coupon","id":"acom.revoke_coupon"},{"name":"acom_get_coupon","id":"acom.get_coupon"},{"name":"acom_create_coupon","id":"acom.create_coupon"}],"evicted":["acom_end_promotion","acom_get_promotion","acom_update_promotion","acom_search_promotions","acom_search_campaigns"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match was already offered in this conversation. If they cannot answe… (+62자) ``
12. 모델 → **`acom_search_coupons`** `` {"limit":100} ``
   ← 결과 539B: `` {"status":"succeeded","data":{"items":[{"id":"cpn_birthday","code":"BIRTHDAY10","name":"Birthday coupon","promotion_id":"promo_birthday","valid_for_member_tier":"member","application":"download","stacking":"no_other_coupons","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null},{"id":"cpn_gold_10","code":"GOLD10","name":"Gold tier 10%","promotion_id":"promo_gold_10","valid_for_member_tier":"gold","application":"download","stacking":"no_other_coupons","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null}],"total":2}} ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: tool define_segment; tool send_bulk; HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.00, 재현율 0.00)

### a2api-acom-index · 1회차 · E TURN_TIMEOUT

토큰 81,875 · 120.098초 · 모델 호출 7회 · 도구 호출 7회 · 첫 요청 프롬프트 6,995토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> set up a win-back for customers who haven't ordered in 90 days. 15% off, email

1. 모델 → **`a2api_load`** `` {"names":["define_segment","create_promotion","create_coupon","create_campaign","create_message_template","preview_segment","set_sale_prices","list_segments"]} ``
   ← 결과 240B: `` {"loaded":["define_segment","create_promotion","create_coupon","create_campaign","create_message_template","list_segments"],"omitted":[{"name":"preview_segment","reason":"SCHEMA_BUDGET"},{"name":"set_sale_prices","reason":"SCHEMA_BUDGET"}]} ``
2. 모델 → **`a2api_load`** `` {"names":["set_sale_prices"]} ``
   ← 결과 59B: `` {"loaded":["set_sale_prices"],"evicted":["define_segment"]} ``
3. 모델 → **`list_segments`** `` {"limit":20} ``
   ← 결과 467B: `` {"status":"succeeded","data":{"items":[{"id":"seg_lapsed_knit_buyers","name":"Lapsed knit buyers","version":1,"estimated_size":22,"estimated_at":"2026-11-06T09:00:00-05:00","condition_rules":{"exclude_segment_ids":["seg_recent_buyers"],"purchased_category_ids":["cat_knitwear"]}},{"id":"seg_recent_buyers","name":"Recent buyers","version":1,"estimated_size":5143,"estimated_at":"2026-11-06T09:00:00-05:00","condition_rules":{"last_order_within_days":30}}],"total":2}} ``
4. 모델 → **`a2api_load`** `` {"names":["define_segment"]} ``
   ← 결과 60B: `` {"loaded":["define_segment"],"evicted":["create_promotion"]} ``
5. 모델 → **`a2api_load`** `` {"names":["create_promotion"]} ``
   ← 결과 77B: `` {"loaded":["create_promotion"],"evicted":["create_coupon","create_campaign"]} ``
6. 모델 → **`a2api_load`** `` {"names":["create_coupon","create_campaign","create_message_template"]} ``
   ← 결과 128B: `` {"loaded":["create_coupon","create_campaign","create_message_template"],"evicted":["create_message_template","set_sale_prices"]} ``
7. 모델 → **`a2api_load`** `` {"names":["set_sale_prices"]} ``
   ← 결과 75B: `` {"loaded":["set_sale_prices"],"evicted":["list_segments","define_segment"]} ``

_(한 턴의 시간 한도(120초)에 걸려 중단)_

**채점**: E TURN_TIMEOUT — 빠진 것: tool define_segment; tool send_bulk; HOST:TURN_TIMEOUT
(도구 정밀도 0.00, 재현율 0.00)

### a2api-acom-index · 2회차 · E MODEL_OUTPUT_TRUNCATED

토큰 82,414 · 113.835초 · 모델 호출 7회 · 도구 호출 6회 · 첫 요청 프롬프트 6,995토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> set up a win-back for customers who haven't ordered in 90 days. 15% off, email

1. 모델 → **`a2api_load`** `` {"names":["define_segment","create_promotion","create_coupon","create_campaign","create_message_template","preview_segment","set_sale_prices","list_segments"]} ``
   ← 결과 240B: `` {"loaded":["define_segment","create_promotion","create_coupon","create_campaign","create_message_template","list_segments"],"omitted":[{"name":"preview_segment","reason":"SCHEMA_BUDGET"},{"name":"set_sale_prices","reason":"SCHEMA_BUDGET"}]} ``
2. 모델 → **`a2api_load`** `` {"names":["set_sale_prices"]} ``
   ← 결과 59B: `` {"loaded":["set_sale_prices"],"evicted":["define_segment"]} ``
3. 모델 → **`a2api_load`** `` {"names":["define_segment"]} ``
   ← 결과 60B: `` {"loaded":["define_segment"],"evicted":["create_promotion"]} ``
4. 모델 → **`list_segments`** `` {"limit":20} ``
   ← 결과 467B: `` {"status":"succeeded","data":{"items":[{"id":"seg_lapsed_knit_buyers","name":"Lapsed knit buyers","version":1,"estimated_size":22,"estimated_at":"2026-11-06T09:00:00-05:00","condition_rules":{"exclude_segment_ids":["seg_recent_buyers"],"purchased_category_ids":["cat_knitwear"]}},{"id":"seg_recent_buyers","name":"Recent buyers","version":1,"estimated_size":5143,"estimated_at":"2026-11-06T09:00:00-05:00","condition_rules":{"last_order_within_days":30}}],"total":2}} ``
5. 모델 → **`a2api_load`** `` {"names":["list_categories"]} ``
   ← 결과 30B: `` {"loaded":["list_categories"]} ``
6. 모델 → **`list_categories`** `` {"term_set":"standard","limit":100} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``

_(모델 출력이 출력 한도에 걸려 중단)_

**채점**: E MODEL_OUTPUT_TRUNCATED — 빠진 것: tool define_segment; tool send_bulk; HOST:MODEL_OUTPUT_TRUNCATED
(도구 정밀도 0.00, 재현율 0.00)

### a2api-acom-names · 1회차 · E TURN_TIMEOUT

토큰 53,130 · 120.201초 · 모델 호출 8회 · 도구 호출 8회 · 첫 요청 프롬프트 1,636토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> set up a win-back for customers who haven't ordered in 90 days. 15% off, email

1. 모델 → **`a2api_load`** `` {"names":["define_segment","create_promotion","create_coupon","create_campaign","send_bulk","preview_segment","list_segments"]} ``
   ← 결과 174B: `` {"loaded":["define_segment","create_promotion","create_coupon","create_campaign","send_bulk","preview_segment"],"omitted":[{"name":"list_segments","reason":"SCHEMA_BUDGET"}]} ``
2. 모델 → **`a2api_load`** `` {"names":["list_message_templates","set_sale_prices"]} ``
   ← 결과 103B: `` {"loaded":["list_message_templates","set_sale_prices"],"evicted":["define_segment","create_promotion"]} ``
3. 모델 → **`a2api_load`** `` {"names":["define_segment"]} ``
   ← 결과 29B: `` {"loaded":["define_segment"]} ``
4. 모델 → **`list_message_templates`** `` {"channel":"email","purpose":"marketing"} ``
   ← 결과 884B: `` {"status":"succeeded","data":{"items":[{"id":"tpl_weekly_email","name":"Weekly email","channel":"email","purpose":"marketing","status":"in_use","headline":"This week at Northwind: {{headline_item}}","text":"Hi {{customer_name}}, here is what is new this week. {{highlights}}","variables":["customer_name","headline_item","highlights"],"in_language":"en-US","created_at":"2026-11-01T01:53:37.237665-04:00"},{"id":"tpl_vip_weekend","name":"VIP weekend reminder","channel":"email","purpose":"marketing","status":"in_use","headline":"VIP weekend: {{headline_item}}","text":"Hi {{customer_name}}, as a VIP… (+284자) ``
5. 모델 → **`a2api_load`** `` {"names":["list_categories"]} ``
   ← 결과 30B: `` {"loaded":["list_categories"]} ``
6. 모델 → **`list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,399B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
7. 모델 → **`a2api_load`** `` {"names":["preview_segment"]} ``
   ← 결과 89B: `` {"already":["preview_segment"],"note":"These functions are already callable; call them."} ``
8. 모델 → **`preview_segment`** `` {"condition_rules":{"last_order_within_days":90},"sample_size":5} ``
   ← 결과 182B: `` {"status":"succeeded","data":{"estimated_size":5960,"sample_customer_ids":["cus_4431","cus_alex","cus_dana","cus_elena","cus_grace"],"by_tier":{"gold":1645,"member":3396,"vip":919}}} ``

_(한 턴의 시간 한도(120초)에 걸려 중단)_

**채점**: E TURN_TIMEOUT — 빠진 것: tool define_segment; tool send_bulk; HOST:TURN_TIMEOUT
(도구 정밀도 0.67, 재현율 0.00)

### a2api-acom-names · 2회차 · E MODEL_OUTPUT_TRUNCATED

토큰 24,289 · 88.871초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 1,636토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> set up a win-back for customers who haven't ordered in 90 days. 15% off, email

1. 모델 → **`a2api_load`** `` {"names":["define_segment","create_promotion","create_coupon","create_campaign","create_message_template"]} ``
   ← 결과 108B: `` {"loaded":["define_segment","create_promotion","create_coupon","create_campaign","create_message_template"]} ``
2. 모델 → **`a2api_load`** `` {"names":["set_sale_prices"]} ``
   ← 결과 59B: `` {"loaded":["set_sale_prices"],"evicted":["define_segment"]} ``
3. 모델 → **`a2api_load`** `` {"names":["define_segment"]} ``
   ← 결과 60B: `` {"loaded":["define_segment"],"evicted":["create_promotion"]} ``

_(모델 출력이 출력 한도에 걸려 중단)_

**채점**: E MODEL_OUTPUT_TRUNCATED — 빠진 것: tool define_segment; tool send_bulk; HOST:MODEL_OUTPUT_TRUNCATED
(도구 정밀도 —, 재현율 0.00)
