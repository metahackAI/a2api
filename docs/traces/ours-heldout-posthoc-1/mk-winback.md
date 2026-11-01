# mk-winback — ours-heldout-posthoc-1

[← 실행 묶음](README.md) · 세트 `held_out` · a-commerce `7e1557b` · a2api `d99f239`

**과업**

> set up a win-back for customers who haven't ordered in 90 days. 15% off, email

- 필요한 도구: `define_segment`, `send_bulk`
- 허용 도구: `preview_segment`, `search_members`, `create_coupon`, `list_message_templates`
- 답에 있어야 할 사실: the segment size is shown before anything is sent

### a2api-acom · 1회차 · E MODEL_CALL_LIMIT

토큰 74,717 · 69.796초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 5,265토큰

준비: 전략 `search`, 함수 8개

**질문 1**
> set up a win-back for customers who haven't ordered in 90 days. 15% off, email

1. 모델 → **`a2api_search`** `` {"query":"segment"} ``
   ← 결과 528B: `` {"selected":[{"name":"acom_list_segments","id":"acom.list_segments"},{"name":"acom_preview_segment","id":"acom.preview_segment"},{"name":"acom_define_segment","id":"acom.define_segment"},{"name":"acom_issue_coupon","id":"acom.issue_coupon"},{"name":"acom_create_campaign","id":"acom.create_campaign"}],"evicted":["acom_create_campaign","acom_send_password_reset","acom_get_return_history","acom_respond_inquiry","acom_dispatch_reward","acom_search_orders"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`acom_list_segments`** `` {} ``
   ← 결과 467B: `` {"status":"succeeded","data":{"items":[{"id":"seg_lapsed_knit_buyers","name":"Lapsed knit buyers","version":1,"estimated_size":22,"estimated_at":"2026-11-06T09:00:00-05:00","condition_rules":{"exclude_segment_ids":["seg_recent_buyers"],"purchased_category_ids":["cat_knitwear"]}},{"id":"seg_recent_buyers","name":"Recent buyers","version":1,"estimated_size":5143,"estimated_at":"2026-11-06T09:00:00-05:00","condition_rules":{"last_order_within_days":30}}],"total":2}} ``
3. 모델 → **`a2api_search`** `` {"query":"coupon"} ``
   ← 결과 409B: `` {"selected":[{"name":"acom_search_coupons","id":"acom.search_coupons"},{"name":"acom_list_member_coupons","id":"acom.list_member_coupons"},{"name":"acom_revoke_coupon","id":"acom.revoke_coupon"},{"name":"acom_get_coupon","id":"acom.get_coupon"},{"name":"acom_create_coupon","id":"acom.create_coupon"}],"evicted":["acom_create_promotion"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`a2api_search`** `` {"query":"promotion"} ``
   ← 결과 460B: `` {"selected":[{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_end_promotion","id":"acom.end_promotion"},{"name":"acom_get_promotion","id":"acom.get_promotion"},{"name":"acom_update_promotion","id":"acom.update_promotion"}],"evicted":["acom_preview_segment","acom_define_segment","acom_issue_coupon"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
5. 모델 → **`acom_search_promotions`** `` {"query":"win-back"} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
6. 모델 → **`acom_search_promotions`** `` {"status":["draft","scheduled","running","paused"],"discount_layer":["order_discount"]} ``
   ← 실패 333B: `` {"status":"failed","error":{"code":"INVALID_INPUT","detail":"Value does not conform to the declared schema.","issues":[{"path":"/discount_layer","rule":"type","expected":"string"},{"path":"/discount_layer","rule":"enum","expected":["item_price","order_discount","add_on"]}]},"hint":"Fix the arguments using issues, then call again."} ``
7. 모델 → **`acom_search_promotions`** `` {"status":["draft","scheduled","running","paused"],"discount_layer":"order_discount"} ``
   ← 결과 665B: `` {"status":"succeeded","data":{"items":[{"id":"promo_denim_bundle","name":"Denim bundle","status":"scheduled","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-13T00:00:00-05:00","valid_through":"2026-11-20T23:59:00-05:00"},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null},{"id":"promo_gold_10","name":"Gold tier 10%","status":"running","discount_layer":"order_discount","valid_for_member_tier":"gold","valid_fro… (+65자) ``
8. 모델 → **`a2api_search`** `` {"query":"define segment"} ``
   ← 결과 498B: `` {"selected":[{"name":"acom_define_segment","id":"acom.define_segment"},{"name":"acom_list_segments","id":"acom.list_segments"},{"name":"acom_preview_segment","id":"acom.preview_segment"},{"name":"acom_set_menu","id":"acom.set_menu"},{"name":"acom_manage_shipping_zone","id":"acom.manage_shipping_zone"}],"evicted":["acom_create_campaign","acom_search_coupons","acom_list_member_coupons","acom_revoke_coupon","acom_get_coupon"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
9. 모델 → **`a2api_search`** `` {"query":"create promotion"} ``
   ← 결과 596B: `` {"selected":[{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_get_promotion","id":"acom.get_promotion"},{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"}],"evicted":["acom_create_coupon","acom_pause_promotion","acom_end_promotion","acom_get_promotion","acom_update_promotion","acom_search_promotions","acom_define_segment","acom_list_segments","acom_preview_segment"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
10. 모델 → **`a2api_search`** `` {"query":"campaign"} ``
   ← 결과 460B: `` {"selected":[{"name":"acom_search_campaigns","id":"acom.search_campaigns"},{"name":"acom_get_campaign","id":"acom.get_campaign"},{"name":"acom_create_campaign","id":"acom.create_campaign"},{"name":"acom_send_bulk","id":"acom.send_bulk"},{"name":"acom_explain_sales_change","id":"acom.explain_sales_change"}],"evicted":["acom_set_menu","acom_manage_shipping_zone","acom_create_promotion"],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true} ``
11. 모델 → **`a2api_search`** `` {"query":"define segment","more":true} ``
   ← 결과 580B: `` {"selected":[{"name":"acom_issue_coupon","id":"acom.issue_coupon"},{"name":"acom_create_campaign","id":"acom.create_campaign"},{"name":"acom_define_tier_program","id":"acom.define_tier_program"}],"omitted":[{"id":"acom.create_role","reason":"SCHEMA_BUDGET"},{"id":"acom.run_tier_evaluation","reason":"SCHEMA_BUDGET"}],"evicted":["acom_create_coupon","acom_get_promotion","acom_pause_promotion","acom_search_promotions","acom_search_campaigns","acom_get_campaign","acom_send_bulk","acom_explain_sales_change"],"moreAvailable":true,"page":2,"pageLimitReached":false,"progress":true} ``
12. 모델 → **`acom_search_coupons`** `` {} ``
   ← 실패 198B: `` {"status":"failed","error":{"code":"NOT_SELECTED","detail":"Function is not active in this session; search again."},"hint":"Call only functions currently provided; search if a function is missing."} ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: tool define_segment; tool send_bulk; HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.00, 재현율 0.00)

### a2api-acom · 2회차 · E MODEL_CALL_LIMIT

토큰 81,303 · 104.543초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 5,265토큰

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
   ← 결과 512B: `` {"selected":[{"name":"acom_list_segments","id":"acom.list_segments"},{"name":"acom_issue_coupon","id":"acom.issue_coupon"},{"name":"acom_create_campaign","id":"acom.create_campaign"},{"name":"acom_preview_segment","id":"acom.preview_segment"},{"name":"acom_define_segment","id":"acom.define_segment"}],"evicted":["acom_get_coupon","acom_create_coupon","acom_get_campaign","acom_send_bulk","acom_explain_sales_change","acom_pause_promotion"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
10. 모델 → **`acom_list_segments`** `` {"limit":100} ``
   ← 결과 467B: `` {"status":"succeeded","data":{"items":[{"id":"seg_lapsed_knit_buyers","name":"Lapsed knit buyers","version":1,"estimated_size":22,"estimated_at":"2026-11-06T09:00:00-05:00","condition_rules":{"exclude_segment_ids":["seg_recent_buyers"],"purchased_category_ids":["cat_knitwear"]}},{"id":"seg_recent_buyers","name":"Recent buyers","version":1,"estimated_size":5143,"estimated_at":"2026-11-06T09:00:00-05:00","condition_rules":{"last_order_within_days":30}}],"total":2}} ``
11. 모델 → **`a2api_search`** `` {"query":"template"} ``
   ← 결과 515B: `` {"selected":[{"name":"acom_list_message_templates","id":"acom.list_message_templates"},{"name":"acom_create_message_template","id":"acom.create_message_template"},{"name":"acom_search_campaigns","id":"acom.search_campaigns"},{"name":"acom_get_campaign","id":"acom.get_campaign"},{"name":"acom_create_campaign","id":"acom.create_campaign"}],"evicted":["acom_end_promotion","acom_get_promotion","acom_update_promotion","acom_search_promotions"],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true} ``
12. 모델 → **`acom_list_message_templates`** `` {"channel":"email","purpose":"marketing","limit":100} ``
   ← 결과 803B: `` {"status":"succeeded","data":{"items":[{"id":"tpl_weekly_email","name":"Weekly email","channel":"email","purpose":"marketing","status":"in_use","headline":"This week at Northwind: {{headline_item}}","text":"Hi {{customer_name}}, here is what is new this week. {{highlights}}","variables":["customer_name","headline_item","highlights"],"in_language":"en-US","created_at":"2026-10-31T16:37:20.646646-04:00"},{"id":"tpl_vip_weekend","name":"VIP weekend reminder","channel":"email","purpose":"marketing","status":"in_use","headline":"VIP weekend: {{headline_item}}","text":"Hi {{customer_name}}, as a VIP… (+203자) ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: tool define_segment; tool send_bulk; HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.20, 재현율 0.00)

### a2api-facade · 1회차 · E TURN_TIMEOUT

토큰 37,440 · 120.085초 · 모델 호출 7회 · 도구 호출 11회 · 첫 요청 프롬프트 2,102토큰

준비: 전략 `search`, 함수 6개

**질문 1**
> set up a win-back for customers who haven't ordered in 90 days. 15% off, email

1. 모델 → **`a2api_search`** `` {"query":"win-back promotion dormant member last order"} ``
   ← 결과 439B: `` {"selected":[{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"},{"name":"facade_save_cust_msg_send","id":"facade.save_cust_msg_send"},{"name":"facade_get_prmt_grid_list_cnt","id":"facade.get_prmt_grid_list_cnt"},{"name":"facade_get_prmt_grid_list","id":"facade.get_prmt_grid_list"},{"name":"facade_get_prmt_tgt_mbr_list","id":"facade.get_prmt_tgt_mbr_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"member last order date filter"} ``
   ← 결과 457B: `` {"selected":[{"name":"facade_get_sale_anls_grid_list","id":"facade.get_sale_anls_grid_list"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_save_cust_msg_send","id":"facade.save_cust_msg_send"},{"name":"facade_get_rfnd_pop_init_data","id":"facade.get_rfnd_pop_init_data"},{"name":"facade_get_prmt_tgt_mbr_list","id":"facade.get_prmt_tgt_mbr_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`a2api_search`** `` {"query":"promotion target by inactivity"} ``
   ← 결과 572B: `` {"selected":[{"name":"facade_get_prmt_grid_list","id":"facade.get_prmt_grid_list"},{"name":"facade_get_prmt_grid_list_cnt","id":"facade.get_prmt_grid_list_cnt"},{"name":"facade_save_prmt_list","id":"facade.save_prmt_list"},{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"},{"name":"facade_get_prmt_tgt_mbr_list","id":"facade.get_prmt_tgt_mbr_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match is already callable. If they cannot answer, tell the user what is missing instead of searching again."} ``
4. 모델 → **`facade_get_prmt_tgt_mbr_list_cnt`** `` {"member_status":"dormant"} ``
   ← 결과 41B: `` {"status":"succeeded","data":{"total":0}} ``
5. 모델 → **`facade_get_prmt_grid_list_cnt`** `` {} ``
   ← 결과 41B: `` {"status":"succeeded","data":{"total":6}} ``
6. 모델 → **`facade_get_prmt_grid_list`** `` {"page_size":20,"page":1} ``
   ← 결과 1,448B: `` {"status":"succeeded","data":{"list":[{"promotion_id":"promo_denim_bundle","promotion_name":"Denim bundle","promotion_type":"order_discount","promotion_status":"scheduled","target_member_grade":"G00","starts_at":"2026-11-13T00:00:00-05:00","ends_at":"2026-11-20T23:59:00-05:00"},{"promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00","starts_at":"2026-11-01T00:00:00-04:00","ends_at":"2026-11-15T23:59:00-05:00"},{"promotion_id":"promo_linen_clearance","promotion_name":"Linen clearan… (+848자) ``
7. 모델 → **`facade_get_prmt_tgt_mbr_list`** `` {"member_status":"dormant","page":1,"page_size":20} ``
   ← 결과 65B: `` {"status":"succeeded","data":{"list":[],"page":1,"page_size":20}} ``
8. 모델 → **`facade_get_prmt_tgt_mbr_list_cnt`** `` {"member_status":"active"} ``
   ← 결과 45B: `` {"status":"succeeded","data":{"total":14000}} ``
9. 모델 → **`a2api_search`** `` {"query":"last order date member"} ``
   ← 결과 598B: `` {"selected":[{"name":"facade_get_sale_anls_grid_list","id":"facade.get_sale_anls_grid_list"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_save_cust_msg_send","id":"facade.save_cust_msg_send"},{"name":"facade_get_rfnd_pop_init_data","id":"facade.get_rfnd_pop_init_data"},{"name":"facade_get_prmt_tgt_mbr_list","id":"facade.get_prmt_tgt_mbr_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match is already callable. If they cannot answer, tell the user what is missing instead of searching again."} ``
10. 모델 → **`a2api_search`** `` {"query":"member inactivity"} ``
   ← 결과 437B: `` {"selected":[{"name":"facade_get_prmt_tgt_mbr_list","id":"facade.get_prmt_tgt_mbr_list"},{"name":"facade_get_prmt_tgt_mbr_list_cnt","id":"facade.get_prmt_tgt_mbr_list_cnt"},{"name":"facade_get_mbr_grd_list","id":"facade.get_mbr_grd_list"},{"name":"facade_get_prd_dtl_info","id":"facade.get_prd_dtl_info"},{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
11. 모델 → **`a2api_search`** `` {"query":"customer win back"} ``
   ← 결과 457B: `` {"selected":[{"name":"facade_save_cust_msg_send","id":"facade.save_cust_msg_send"},{"name":"facade_get_prmt_tgt_mbr_list","id":"facade.get_prmt_tgt_mbr_list"},{"name":"facade_get_prmt_tgt_mbr_list_cnt","id":"facade.get_prmt_tgt_mbr_list_cnt"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match is already callable. If they cannot answer, tell the user what is missing instead of searching again."} ``

_(한 턴의 시간 한도(120초)에 걸려 중단)_

**채점**: E TURN_TIMEOUT — 빠진 것: HOST:TURN_TIMEOUT

### a2api-facade · 2회차 · E TURN_TIMEOUT

토큰 37,440 · 120.097초 · 모델 호출 7회 · 도구 호출 11회 · 첫 요청 프롬프트 2,102토큰

준비: 전략 `search`, 함수 6개

**질문 1**
> set up a win-back for customers who haven't ordered in 90 days. 15% off, email

1. 모델 → **`a2api_search`** `` {"query":"win-back promotion dormant member last order"} ``
   ← 결과 439B: `` {"selected":[{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"},{"name":"facade_save_cust_msg_send","id":"facade.save_cust_msg_send"},{"name":"facade_get_prmt_grid_list_cnt","id":"facade.get_prmt_grid_list_cnt"},{"name":"facade_get_prmt_grid_list","id":"facade.get_prmt_grid_list"},{"name":"facade_get_prmt_tgt_mbr_list","id":"facade.get_prmt_tgt_mbr_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"member last order date filter"} ``
   ← 결과 457B: `` {"selected":[{"name":"facade_get_sale_anls_grid_list","id":"facade.get_sale_anls_grid_list"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_save_cust_msg_send","id":"facade.save_cust_msg_send"},{"name":"facade_get_rfnd_pop_init_data","id":"facade.get_rfnd_pop_init_data"},{"name":"facade_get_prmt_tgt_mbr_list","id":"facade.get_prmt_tgt_mbr_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`a2api_search`** `` {"query":"promotion target by inactivity"} ``
   ← 결과 572B: `` {"selected":[{"name":"facade_get_prmt_grid_list","id":"facade.get_prmt_grid_list"},{"name":"facade_get_prmt_grid_list_cnt","id":"facade.get_prmt_grid_list_cnt"},{"name":"facade_save_prmt_list","id":"facade.save_prmt_list"},{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"},{"name":"facade_get_prmt_tgt_mbr_list","id":"facade.get_prmt_tgt_mbr_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match is already callable. If they cannot answer, tell the user what is missing instead of searching again."} ``
4. 모델 → **`facade_get_prmt_tgt_mbr_list_cnt`** `` {"member_status":"dormant"} ``
   ← 결과 41B: `` {"status":"succeeded","data":{"total":0}} ``
5. 모델 → **`facade_get_prmt_grid_list_cnt`** `` {} ``
   ← 결과 41B: `` {"status":"succeeded","data":{"total":6}} ``
6. 모델 → **`facade_get_prmt_grid_list`** `` {"page_size":20,"page":1} ``
   ← 결과 1,448B: `` {"status":"succeeded","data":{"list":[{"promotion_id":"promo_denim_bundle","promotion_name":"Denim bundle","promotion_type":"order_discount","promotion_status":"scheduled","target_member_grade":"G00","starts_at":"2026-11-13T00:00:00-05:00","ends_at":"2026-11-20T23:59:00-05:00"},{"promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00","starts_at":"2026-11-01T00:00:00-04:00","ends_at":"2026-11-15T23:59:00-05:00"},{"promotion_id":"promo_linen_clearance","promotion_name":"Linen clearan… (+848자) ``
7. 모델 → **`facade_get_prmt_tgt_mbr_list`** `` {"member_status":"dormant","page":1,"page_size":20} ``
   ← 결과 65B: `` {"status":"succeeded","data":{"list":[],"page":1,"page_size":20}} ``
8. 모델 → **`facade_get_prmt_tgt_mbr_list_cnt`** `` {"member_status":"active"} ``
   ← 결과 45B: `` {"status":"succeeded","data":{"total":14000}} ``
9. 모델 → **`a2api_search`** `` {"query":"last order date member"} ``
   ← 결과 598B: `` {"selected":[{"name":"facade_get_sale_anls_grid_list","id":"facade.get_sale_anls_grid_list"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_save_cust_msg_send","id":"facade.save_cust_msg_send"},{"name":"facade_get_rfnd_pop_init_data","id":"facade.get_rfnd_pop_init_data"},{"name":"facade_get_prmt_tgt_mbr_list","id":"facade.get_prmt_tgt_mbr_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match is already callable. If they cannot answer, tell the user what is missing instead of searching again."} ``
10. 모델 → **`a2api_search`** `` {"query":"member inactivity"} ``
   ← 결과 437B: `` {"selected":[{"name":"facade_get_prmt_tgt_mbr_list","id":"facade.get_prmt_tgt_mbr_list"},{"name":"facade_get_prmt_tgt_mbr_list_cnt","id":"facade.get_prmt_tgt_mbr_list_cnt"},{"name":"facade_get_mbr_grd_list","id":"facade.get_mbr_grd_list"},{"name":"facade_get_prd_dtl_info","id":"facade.get_prd_dtl_info"},{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
11. 모델 → **`a2api_search`** `` {"query":"customer win back"} ``
   ← 결과 457B: `` {"selected":[{"name":"facade_save_cust_msg_send","id":"facade.save_cust_msg_send"},{"name":"facade_get_prmt_tgt_mbr_list","id":"facade.get_prmt_tgt_mbr_list"},{"name":"facade_get_prmt_tgt_mbr_list_cnt","id":"facade.get_prmt_tgt_mbr_list_cnt"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match is already callable. If they cannot answer, tell the user what is missing instead of searching again."} ``

_(한 턴의 시간 한도(120초)에 걸려 중단)_

**채점**: E TURN_TIMEOUT — 빠진 것: HOST:TURN_TIMEOUT
