# b1-vip-weekend-sale — ours-design-1

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `a2c7201`

**과업**

> Run a 20% weekend sale on summer outerwear for VIP members and put it on the main page.

> Drop the low-stock ones. Give the overshirt 15% instead.

- 필요한 도구: `search_products`, `list_tiers`, `set_sale_prices`, `create_coupon`, `schedule_banner`
- 허용 도구: `get_policy`, `list_active_promotions`, `list_display_slots`, `list_categories`
- 답에 있어야 할 사실: 40 of 42 summer outerwear products; chore coat (7) and rain parka (4) are left out for low stock
- 답에 있어야 할 사실: the overshirt is at 15% ($67.15) to stay above the price floor
- change set: `` {"state":"drafting","version":2,"items":[{"tool":"set_sale_prices","args":{"valid_for_member_tier":"vip","percent_off":20}},{"tool":"create_coupon"},{"tool":"schedule_banner","args":{"slot_id":"slot_home_hero"}}],"checks_passed":["max_discount","price_floor","promo_min_stock","promotion_overlap","member_benefits_per_order","slot_free"]} ``

### facade-all · 1회차 · E MODEL_CALL_LIMIT

토큰 80,983 · 78.704초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 4,659토큰

준비: 전략 `None`, 함수 19개

**질문 1**
> Run a 20% weekend sale on summer outerwear for VIP members and put it on the main page.

**질문 2**
> Drop the low-stock ones. Give the overshirt 15% instead.

_(이 실행은 호출이 어느 턴에 속하는지 기록하지 않았다. 호출을 순서대로 보인다.)_

1. 모델 → **`getPrdGridList`** `` {"srchKwd":"summer outerwear","pageNo":0,"pageSize":10} ``
   ← 결과 121B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null}}} ``
2. 모델 → **`getMbrGrdList`** `` {} ``
   ← 결과 222B: `` {"status":200,"body":{"list":[{"mbrGrdCd":"G03","mbrGrdNm":"VIP","mbrCnt":1284,"sortSeq":3},{"mbrGrdCd":"G02","mbrGrdNm":"Gold","mbrCnt":2900,"sortSeq":2},{"mbrGrdCd":"G01","mbrGrdNm":"Member","mbrCnt":9816,"sortSeq":1}]}} ``
3. 모델 → **`getPrdGridList`** `` {"srchKwd":"summer outerwear","pageNo":1,"pageSize":10} ``
   ← 결과 1,993B: `` {"status":200,"body":{"list":[{"prdNo":"prd_summer_outerwear_22","prdNm":"Seersucker shacket","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":79.0,"mbrPrc":null,"stkQty":36,"sellStatCd":"10","costPrc":35.55},{"prdNo":"prd_summer_outerwear_33","prdNm":"Linen shacket","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":129.0,"mbrPrc":null,"stkQty":30,"sellStatCd":"10","costPrc":58.05},{"prdNo":"prd_rain_parka","prdNm":"Light rain parka","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":118.0,"mbrPrc":null,"stkQty":4,"sellStatCd":"10","costPrc":50.0… (+900자) ``
4. 모델 → **`getPrdGridListCnt`** `` {"srchKwd":"summer outerwear","pageNo":1,"pageSize":10} ``
   ← 결과 36B: `` {"status":200,"body":{"totCnt":124}} ``
5. 모델 → **`getDispCornerList`** `` {"dispPageCd":"01","strtDtm":"2026-11-07 00:00:00","endDtm":"2026-11-08 23:59:59"} ``
   ← 결과 190B: `` {"status":422,"body":{"error":{"code":"invalid_input","class":"invalid_input","message":"'2026-11-07 00:00:00' is not a date-time (expected 2026-11-07T00:00 or RFC 3339)","next_tool":null}}} ``
6. 모델 → **`getDispCornerList`** `` {"dispPageCd":"01","strtDtm":"2026-11-07T00:00:00","endDtm":"2026-11-08T23:59:59"} ``
   ← 결과 505B: `` {"status":200,"body":{"list":[{"cornerNo":"slot_home_hero","cornerNm":"Home hero","cornerTpCd":"H","bnrList":[{"dispNo":"dsp_fall_layers","tgtMbrGrdCd":"G00","bnrTitl":"Fall layers","strtDtm":"2026-11-06T10:00:00-05:00","endDtm":null,"dispStatCd":"20"}]},{"cornerNo":"slot_home_new_in","cornerNm":"New in","cornerTpCd":"G","bnrList":[]},{"cornerNo":"slot_home_stories","cornerNm":"Stories","cornerTpCd":"B","bnrList":[]},{"cornerNo":"slot_home_brands","cornerNm":"Brands","cornerTpCd":"S","bnrList":[]}]}} ``
7. 모델 → **`getPrmtGridList`** `` {"pageNo":0,"pageSize":10} ``
   ← 결과 121B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null}}} ``
8. 모델 → **`getPrmtGridList`** `` {"pageNo":1,"pageSize":10} ``
   ← 결과 1,121B: `` {"status":200,"body":{"list":[{"prmtNo":"promo_denim_bundle","prmtNm":"Denim bundle","prmtTpCd":"T02","prmtStatCd":"10","tgtMbrGrdCd":"G00","strtDtm":"2026-11-13T00:00:00-05:00","endDtm":"2026-11-20T23:59:00-05:00"},{"prmtNo":"promo_autumn_knit","prmtNm":"Autumn knitwear 15%","prmtTpCd":"T01","prmtStatCd":"20","tgtMbrGrdCd":"G00","strtDtm":"2026-11-01T00:00:00-04:00","endDtm":"2026-11-15T23:59:00-05:00"},{"prmtNo":"promo_linen_clearance","prmtNm":"Linen clearance","prmtTpCd":"T01","prmtStatCd":"90","tgtMbrGrdCd":"G00","strtDtm":"2026-10-01T00:00:00-04:00","endDtm":"2026-10-20T23:59:00-04:00"},… (+521자) ``
9. 모델 → **`savePrmtList`** `` {"rows":[{"rowStat":"I","prmtNo":"promo_summer_outerwear_vip_weekend_20261107","prmtNm":"Weekend Summer Outerwear 20% VIP","prmtTpCd":"T01","prmtStatCd":"10","tgtMbrGrdCd":"G03","strtDtm":"2026-11-07T00:00:00-05:00","endDtm":"2026-11-08T23:59:59-05:00","aplyTgtCd":"C","ctgNo":"cat_summer_outerwear","prdNoList":[],"dcRt":20}]} ``
   ← 결과 153B: `` {"status":200,"body":{"resultCd":"0000","resultMsg":"Saved.","procCnt":1,"list":[{"rowNo":1,"rowStat":"I","prmtNo":"promo_01m695a2n5x79bmqm6keg5shsk"}]}} ``
10. 모델 → **`saveDispBnrList`** `` {"rows":[{"rowStat":"I","cornerNo":"slot_home_hero","tgtMbrGrdCd":"G03","strtDtm":"2026-11-07T00:00:00-05:00","endDtm":"2026-11-08T23:59:59-05:00","bnrTitl":"Weekend Summer Outerwear 20% Off VIP","bnrSubTitl":"VIP weekend sale on summer outerwear","btnNm":"Shop Now","lnkUrl":"/category/cat_summer_outerwear","prmtNo":"promo_01m695a2n5x79bmqm6keg5shsk"}]} ``
   ← 결과 147B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Row 1: 'imgPrdNo' or 'imgNo' is required.","next_tool":null}}} ``
11. 모델 → **`getPrdDtlInfoV2`** `` {"prdNo":"prd_summer_outerwear_22"} ``
   ← 결과 2,914B: `` {"status":200,"body":{"prdNo":"prd_summer_outerwear_22","prdNm":"Seersucker shacket","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":79.0,"mbrPrc":null,"stkQty":36,"sellStatCd":"10","costPrc":35.55,"prdStatCd":"active","optList":[{"optNo":"var_summer_outerwear_22_xs_rust","optVal1":"Rust","optVal2":"XS","stkQty":2,"sellStatCd":"10"},{"optNo":"var_summer_outerwear_22_s_rust","optVal1":"Rust","optVal2":"S","stkQty":3,"sellStatCd":"10"},{"optNo":"var_summer_outerwear_22_m_rust","optVal1":"Rust","optVal2":"M","stkQty":1,"sellStatCd":"10"},{"optNo":"var_summer_outerwear_22_l_rust"… (+900자) ``
12. 모델 → **`saveDispBnrList`** `` {"rows":[{"rowStat":"I","cornerNo":"slot_home_hero","tgtMbrGrdCd":"G03","strtDtm":"2026-11-07T00:00:00-05:00","endDtm":"2026-11-08T23:59:59-05:00","bnrTitl":"Weekend Summer Outerwear 20% Off VIP","bnrSubTitl":"VIP weekend sale on summer outerwear","btnNm":"Shop Now","lnkUrl":"/category/cat_summer_outerwear","imgPrdNo":"prd_summer_outerwear_22","prmtNo":"promo_01m695a2n5x79bmqm6keg5shsk"}]} ``
   ← 결과 160B: `` {"status":422,"body":{"error":{"code":"invalid_input","class":"invalid_input","message":"Row 1: 'content.eyebrow' is at most 24 characters.","next_tool":null}}} ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "40 of 42 summer outerwear products; chore coat (7) and rain " (40, 42, 7, 4 not shown); fact "the overshirt is at 15% ($67.15) to stay above the price flo" (15, 67.15 not shown); HOST:MODEL_CALL_LIMIT

### acom-all · 1회차 · E CONTEXT_OVERFLOW

토큰 0 · 0.348초 · 모델 호출 0회 · 도구 호출 0회

준비: 전략 `None`, 함수 253개

**질문 1**
> Run a 20% weekend sale on summer outerwear for VIP members and put it on the main page.

**질문 2**
> Drop the low-stock ones. Give the overshirt 15% instead.

_(이 실행은 호출이 어느 턴에 속하는지 기록하지 않았다. 호출을 순서대로 보인다.)_


_(CONTEXT_OVERFLOW로 중단)_

**채점**: E CONTEXT_OVERFLOW — 빠진 것: tool search_products; tool list_tiers; tool set_sale_prices; tool create_coupon; tool schedule_banner; change set; fact "40 of 42 summer outerwear products; chore coat (7) and rain " (40, 42, 7, 4 not shown); fact "the overshirt is at 15% ($67.15) to stay above the price flo" (15, 67.15 not shown); HOST:CONTEXT_OVERFLOW
(도구 정밀도 —, 재현율 0.00)

### a2api-acom · 1회차 · E MODEL_CONNECTION_FAILED

토큰 72,491 · 120.17초 · 모델 호출 9회 · 도구 호출 16회 · 첫 요청 프롬프트 3,630토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> Run a 20% weekend sale on summer outerwear for VIP members and put it on the main page.

**질문 2**
> Drop the low-stock ones. Give the overshirt 15% instead.

_(이 실행은 호출이 어느 턴에 속하는지 기록하지 않았다. 호출을 순서대로 보인다.)_

1. 모델 → **`a2api_search`** `` {"query":"create promotion"} ``
   ← 결과 503B: `` {"selected":[{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_get_promotion","id":"acom.get_promotion"},{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"}],"evicted":["acom_list_display_slots","acom_invalidate_display_cache","acom_get_price_breakdown","acom_get_sales_trend"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"schedule banner"} ``
   ← 결과 493B: `` {"selected":[{"name":"acom_schedule_banner","id":"acom.schedule_banner"},{"name":"acom_set_banner","id":"acom.set_banner"},{"name":"acom_schedule_display","id":"acom.schedule_display"},{"name":"acom_arrange_display_slot","id":"acom.arrange_display_slot"},{"name":"acom_list_display_slots","id":"acom.list_display_slots"}],"evicted":["acom_get_sales_overview","acom_list_tiers","acom_get_curation","acom_create_promotion"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`a2api_search`** `` {"query":"summer outerwear category"} ``
   ← 결과 475B: `` {"selected":[{"name":"acom_create_category","id":"acom.create_category"},{"name":"acom_get_category","id":"acom.get_category"},{"name":"acom_list_categories","id":"acom.list_categories"},{"name":"acom_map_category","id":"acom.map_category"},{"name":"acom_update_category","id":"acom.update_category"}],"evicted":["acom_create_coupon","acom_get_promotion","acom_pause_promotion","acom_search_promotions"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`a2api_search`** `` {"query":"VIP member tier"} ``
   ← 결과 438B: `` {"selected":[{"name":"acom_list_tiers","id":"acom.list_tiers"},{"name":"acom_get_member_tier","id":"acom.get_member_tier"},{"name":"acom_set_member_tier","id":"acom.set_member_tier"},{"name":"acom_list_display_slots","id":"acom.list_display_slots"},{"name":"acom_list_tier_history","id":"acom.list_tier_history"}],"evicted":["acom_schedule_banner","acom_set_banner"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
5. 모델 → **`acom_list_tiers`** `` {} ``
   ← 결과 305B: `` {"status":"succeeded","data":{"items":[{"id":"vip","name":"VIP","rank":3,"program_id":"prg_rewards","member_count":1284},{"id":"gold","name":"Gold","rank":2,"program_id":"prg_rewards","member_count":2900},{"id":"member","name":"Member","rank":1,"program_id":"prg_rewards","member_count":9816}],"total":3}} ``
6. 모델 → **`acom_list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
7. 모델 → **`acom_list_display_slots`** `` {"page":"main","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","audience":"vip"} ``
   ← 결과 1,152B: `` {"status":"succeeded","data":{"items":[{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"]}],"availability":[{"audience":"vip","free_from":"2026-11-07T00:00:00-05:00","free_until":"2026-11-08T23:59:00-05:00"}]},{"id":"slot_home_new_in","page":"main","name":"New in","slot_type":"product_grid","bookings":[],"availa… (+552자) ``
8. 모델 → **`a2api_search`** `` {"query":"create banner"} ``
   ← 결과 565B: `` {"selected":[{"name":"acom_create_curation","id":"acom.create_curation"},{"name":"acom_list_banners","id":"acom.list_banners"},{"name":"acom_set_banner","id":"acom.set_banner"},{"name":"acom_schedule_banner","id":"acom.schedule_banner"},{"name":"acom_create_category","id":"acom.create_category"}],"evicted":["acom_schedule_display","acom_arrange_display_slot","acom_create_category","acom_get_category","acom_map_category","acom_update_category","acom_get_member_tier","acom_set_member_tier"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
9. 모델 → **`a2api_search`** `` {"query":"create promotion"} ``
   ← 결과 549B: `` {"selected":[{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_get_promotion","id":"acom.get_promotion"},{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"}],"evicted":["acom_list_tier_history","acom_list_tiers","acom_list_categories","acom_list_display_slots","acom_create_curation","acom_list_banners","acom_set_banner"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":false} ``
10. 모델 → **`a2api_search`** `` {"query":"set sale prices"} ``
   ← 결과 463B: `` {"selected":[{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_set_price","id":"acom.set_price"},{"name":"acom_get_promotion","id":"acom.get_promotion"},{"name":"acom_update_product","id":"acom.update_product"},{"name":"acom_list_active_promotions","id":"acom.list_active_promotions"}],"evicted":["acom_schedule_banner","acom_create_category","acom_create_promotion"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
11. 모델 → **`a2api_search`** `` {"query":"percent off promotion"} ``
   ← 결과 506B: `` {"selected":[{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_end_promotion","id":"acom.end_promotion"}],"evicted":["acom_create_coupon","acom_pause_promotion","acom_search_promotions","acom_set_price","acom_get_promotion"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
12. 모델 → **`a2api_search`** `` {"query":"schedule banner parameters"} ``
   ← 결과 481B: `` {"selected":[{"name":"acom_set_banner","id":"acom.set_banner"},{"name":"acom_schedule_banner","id":"acom.schedule_banner"},{"name":"acom_schedule_display","id":"acom.schedule_display"},{"name":"acom_arrange_display_slot","id":"acom.arrange_display_slot"},{"name":"acom_list_display_slots","id":"acom.list_display_slots"}],"evicted":["acom_update_product","acom_list_active_promotions","acom_create_promotion"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
13. 모델 → **`a2api_search`** `` {"query":"search products"} ``
   ← 결과 538B: `` {"selected":[{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_search_product_groups","id":"acom.search_product_groups"},{"name":"acom_autocomplete","id":"acom.autocomplete"},{"name":"acom_get_index_status","id":"acom.get_index_status"},{"name":"acom_create_curation","id":"acom.create_curation"}],"evicted":["acom_set_sale_prices","acom_pause_promotion","acom_search_promotions","acom_end_promotion","acom_set_banner","acom_schedule_banner"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
14. 모델 → **`acom_search_products`** `` {"category_id":"cat_summer_outerwear","limit":20} ``
   ← 결과 6,014B: `` {"status":"succeeded","data":{"items":[{"id":"prd_summer_outerwear_13","name":"Poplin shacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/field-olive.svg","price":99.0,"price_currency":"USD","member_price":null,"cost":44.55,"inventory_level":14,"availability":"in_stock","has_variant":[{"variant_id":"var_summer_outerwear_13_xs_olive","sku":"so-13-olive-xs","size":"XS","color":"Olive","inventory_level":1,"availability":"in_stock"},{"variant_id":"var_summer_outerwear_13_s_olive","sku":"so-13-olive-s","size":"S","color":"Olive","inventory_level":1,"avai… (+900자) ``
15. 모델 → **`a2api_search`** `` {"query":"promotion discount percent off"} ``
   ← 결과 598B: `` {"selected":[{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_update_promotion","id":"acom.update_promotion"},{"name":"acom_create_coupon","id":"acom.create_coupon"}],"evicted":["acom_schedule_display","acom_arrange_display_slot","acom_list_display_slots","acom_search_product_groups","acom_autocomplete","acom_get_index_status","acom_create_curation","acom_search_products"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
16. 모델 → **`a2api_search`** `` {"query":"set sale prices parameters"} ``
   ← 결과 417B: `` {"selected":[{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_set_price","id":"acom.set_price"},{"name":"acom_get_promotion","id":"acom.get_promotion"},{"name":"acom_update_product","id":"acom.update_product"},{"name":"acom_list_active_promotions","id":"acom.list_active_promotions"}],"evicted":["acom_create_promotion"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``

_(MODEL_CONNECTION_FAILED로 중단)_

**채점**: E MODEL_CONNECTION_FAILED — 빠진 것: tool set_sale_prices; tool create_coupon; tool schedule_banner; change set; fact "40 of 42 summer outerwear products; chore coat (7) and rain " (40, 42, 7, 4 not shown); fact "the overshirt is at 15% ($67.15) to stay above the price flo" (15, 67.15 not shown); HOST:MODEL_CONNECTION_FAILED
(도구 정밀도 1.00, 재현율 0.40)

### a2api-facade · 1회차 · E MODEL_CALL_LIMIT

토큰 62,188 · 100.143초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 3,203토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> Run a 20% weekend sale on summer outerwear for VIP members and put it on the main page.

**질문 2**
> Drop the low-stock ones. Give the overshirt 15% instead.

_(이 실행은 호출이 어느 턴에 속하는지 기록하지 않았다. 호출을 순서대로 보인다.)_

1. 모델 → **`facade_get_prd_grid_list`** `` {"keyword":"summer outerwear","page":0,"page_size":10} ``
   ← 실패 237B: `` {"status":"failed","error":{"code":"UPSTREAM_VALIDATION_FAILED","detail":"The backend rejected the request values. (HTTP 422) Invalid paging."},"hint":"The service rejected these values. Correct them only if the user gave other values."} ``
2. 모델 → **`facade_get_prd_grid_list`** `` {"keyword":"outerwear","page":0,"page_size":20} ``
   ← 실패 237B: `` {"status":"failed","error":{"code":"UPSTREAM_VALIDATION_FAILED","detail":"The backend rejected the request values. (HTTP 422) Invalid paging."},"hint":"The service rejected these values. Correct them only if the user gave other values."} ``
3. 모델 → **`facade_get_prd_grid_list`** `` {"keyword":"summer","page":1,"page_size":10} ``
   ← 결과 2,192B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_summer_outerwear_22","product_name":"Seersucker shacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":79.0,"member_price":null,"stock":36,"availability":"in_stock","cost":35.55},{"product_id":"prd_summer_outerwear_14","product_name":"Linen harrington","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":149.0,"member_price":null,"stock":105,"availability":"in_stock","cost":67.05},{"product_id":"prd_summer_outerwear_33","product_name":"Linen shacket","category_id":"cat_summer_outerwear","brand… (+900자) ``
4. 모델 → **`a2api_search`** `` {"query":"member grade list"} ``
   ← 결과 425B: `` {"selected":[{"name":"facade_get_mbr_grd_list","id":"facade.get_mbr_grd_list"},{"name":"facade_get_prmt_tgt_mbr_list","id":"facade.get_prmt_tgt_mbr_list"},{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_get_prmt_grid_list","id":"facade.get_prmt_grid_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
5. 모델 → **`facade_get_mbr_grd_list`** `` {} ``
   ← 결과 257B: `` {"status":"succeeded","data":{"list":[{"member_grade":"G03","grade_name":"VIP","member_count":1284,"rank":3},{"member_grade":"G02","grade_name":"Gold","member_count":2900,"rank":2},{"member_grade":"G01","grade_name":"Member","member_count":9816,"rank":1}]}} ``
6. 모델 → **`facade_get_prmt_grid_list`** `` {"promotion_name":"summer outerwear","page":0,"page_size":10} ``
   ← 실패 237B: `` {"status":"failed","error":{"code":"UPSTREAM_VALIDATION_FAILED","detail":"The backend rejected the request values. (HTTP 422) Invalid paging."},"hint":"The service rejected these values. Correct them only if the user gave other values."} ``
7. 모델 → **`facade_get_prmt_grid_list`** `` {"promotion_name":"summer outerwear","page":1,"page_size":10} ``
   ← 결과 65B: `` {"status":"succeeded","data":{"list":[],"page":1,"page_size":10}} ``
8. 모델 → **`facade_get_prmt_grid_list_cnt`** `` {"promotion_name":"summer outerwear","page":0,"page_size":10} ``
   ← 결과 41B: `` {"status":"succeeded","data":{"total":0}} ``
9. 모델 → **`a2api_search`** `` {"query":"main page promotion"} ``
   ← 결과 431B: `` {"selected":[{"name":"facade_get_prmt_grid_list","id":"facade.get_prmt_grid_list"},{"name":"facade_get_prmt_grid_list_cnt","id":"facade.get_prmt_grid_list_cnt"},{"name":"facade_get_prmt_tgt_mbr_list","id":"facade.get_prmt_tgt_mbr_list"},{"name":"facade_save_prmt_list","id":"facade.save_prmt_list"},{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
10. 모델 → **`a2api_search`** `` {"query":"main page"} ``
   ← 결과 441B: `` {"selected":[{"name":"facade_get_prmt_tgt_mbr_list","id":"facade.get_prmt_tgt_mbr_list"},{"name":"facade_get_disp_corner_list","id":"facade.get_disp_corner_list"},{"name":"facade_get_clm_grid_list","id":"facade.get_clm_grid_list"},{"name":"facade_get_prmt_grid_list","id":"facade.get_prmt_grid_list"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
11. 모델 → **`facade_get_disp_corner_list`** `` {"page_type":"main","starts_at":"2026-11-07T00:00:00-04:00","ends_at":"2026-11-09T23:59:59-04:00"} ``
   ← 결과 592B: `` {"status":"succeeded","data":{"list":[{"corner_id":"slot_home_hero","corner_name":"Home hero","corner_type":"hero","banners":[{"booking_id":"dsp_fall_layers","target_member_grade":"G00","headline":"Fall layers","starts_at":"2026-11-06T10:00:00-05:00","ends_at":null,"display_status":"active"}]},{"corner_id":"slot_home_new_in","corner_name":"New in","corner_type":"product_grid","banners":[]},{"corner_id":"slot_home_stories","corner_name":"Stories","corner_type":"banner_board","banners":[]},{"corner_id":"slot_home_brands","corner_name":"Brands","corner_type":"brand_strip","banners":[]}]}} ``
12. 모델 → **`a2api_search`** `` {"query":"display corner save"} ``
   ← 결과 413B: `` {"selected":[{"name":"facade_save_disp_bnr_list","id":"facade.save_disp_bnr_list"},{"name":"facade_get_disp_corner_list","id":"facade.get_disp_corner_list"},{"name":"facade_save_prmt_list","id":"facade.save_prmt_list"},{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"},{"name":"facade_save_rfnd_proc","id":"facade.save_rfnd_proc"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "40 of 42 summer outerwear products; chore coat (7) and rain " (40, 42, 7, 4 not shown); fact "the overshirt is at 15% ($67.15) to stay above the price flo" (15, 67.15 not shown); HOST:MODEL_CALL_LIMIT
