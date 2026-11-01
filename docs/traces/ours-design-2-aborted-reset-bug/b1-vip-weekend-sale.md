# b1-vip-weekend-sale — ours-design-2-aborted-reset-bug

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `8c25f4a`

**과업**

> Run a 20% weekend sale on summer outerwear for VIP members and put it on the main page.

> Drop the low-stock ones. Give the overshirt 15% instead.

- 필요한 도구: `search_products`, `list_tiers`, `set_sale_prices`, `create_coupon`, `schedule_banner`
- 허용 도구: `get_policy`, `list_active_promotions`, `list_display_slots`, `list_categories`
- 답에 있어야 할 사실: 40 of 42 summer outerwear products; chore coat (7) and rain parka (4) are left out for low stock
- 답에 있어야 할 사실: the overshirt is at 15% ($67.15) to stay above the price floor
- change set: `` {"state":"drafting","version":2,"items":[{"tool":"set_sale_prices","args":{"valid_for_member_tier":"vip","percent_off":20}},{"tool":"create_coupon"},{"tool":"schedule_banner","args":{"slot_id":"slot_home_hero"}}],"checks_passed":["max_discount","price_floor","promo_min_stock","promotion_overlap","member_benefits_per_order","slot_free"]} ``

### facade-all · 1회차 · E TURN_TIMEOUT

토큰 153,495 · 186.734초 · 모델 호출 18회 · 도구 호출 17회 · 첫 요청 프롬프트 4,659토큰

준비: 전략 `None`, 함수 19개

**질문 1**
> Run a 20% weekend sale on summer outerwear for VIP members and put it on the main page.

**질문 2**
> Drop the low-stock ones. Give the overshirt 15% instead.

_(이 실행은 호출이 어느 턴에 속하는지 기록하지 않았다. 호출을 순서대로 보인다.)_

1. 모델 → **`getMbrGrdList`** `` {} ``
   ← 결과 222B: `` {"status":200,"body":{"list":[{"mbrGrdCd":"G03","mbrGrdNm":"VIP","mbrCnt":1284,"sortSeq":3},{"mbrGrdCd":"G02","mbrGrdNm":"Gold","mbrCnt":2900,"sortSeq":2},{"mbrGrdCd":"G01","mbrGrdNm":"Member","mbrCnt":9816,"sortSeq":1}]}} ``
2. 모델 → **`getPrdGridList`** `` {"srchKwd":"summer outerwear","pageNo":0,"pageSize":10} ``
   ← 결과 121B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null}}} ``
3. 모델 → **`getPrdGridList`** `` {"srchKwd":"summer outerwear","pageNo":1,"pageSize":10} ``
   ← 결과 1,993B: `` {"status":200,"body":{"list":[{"prdNo":"prd_summer_outerwear_22","prdNm":"Seersucker shacket","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":79.0,"mbrPrc":null,"stkQty":36,"sellStatCd":"10","costPrc":35.55},{"prdNo":"prd_summer_outerwear_33","prdNm":"Linen shacket","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":129.0,"mbrPrc":null,"stkQty":30,"sellStatCd":"10","costPrc":58.05},{"prdNo":"prd_rain_parka","prdNm":"Light rain parka","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":118.0,"mbrPrc":null,"stkQty":4,"sellStatCd":"10","costPrc":50.0… (+900자) ``
4. 모델 → **`getPrdGridListCnt`** `` {"srchKwd":"summer outerwear"} ``
   ← 결과 36B: `` {"status":200,"body":{"totCnt":124}} ``
5. 모델 → **`getPrmtGridList`** `` {"pageNo":0,"pageSize":5} ``
   ← 결과 121B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null}}} ``
6. 모델 → **`getPrmtGridList`** `` {"pageNo":1,"pageSize":5} ``
   ← 결과 961B: `` {"status":200,"body":{"list":[{"prmtNo":"promo_denim_bundle","prmtNm":"Denim bundle","prmtTpCd":"T02","prmtStatCd":"10","tgtMbrGrdCd":"G00","strtDtm":"2026-11-13T00:00:00-05:00","endDtm":"2026-11-20T23:59:00-05:00"},{"prmtNo":"promo_autumn_knit","prmtNm":"Autumn knitwear 15%","prmtTpCd":"T01","prmtStatCd":"20","tgtMbrGrdCd":"G00","strtDtm":"2026-11-01T00:00:00-04:00","endDtm":"2026-11-15T23:59:00-05:00"},{"prmtNo":"promo_linen_clearance","prmtNm":"Linen clearance","prmtTpCd":"T01","prmtStatCd":"90","tgtMbrGrdCd":"G00","strtDtm":"2026-10-01T00:00:00-04:00","endDtm":"2026-10-20T23:59:00-04:00"},… (+361자) ``
7. 모델 → **`getDispCornerList`** `` {"dispPageCd":"01","strtDtm":"2026-11-06T00:00:00-05:00","endDtm":"2026-11-08T23:59:00-05:00"} ``
   ← 결과 677B: `` {"status":200,"body":{"list":[{"cornerNo":"slot_home_hero","cornerNm":"Home hero","cornerTpCd":"H","bnrList":[{"dispNo":"dsp_october_edit","tgtMbrGrdCd":"G00","bnrTitl":"The October edit","strtDtm":"2026-10-01T00:00:00-04:00","endDtm":"2026-11-06T09:59:00-05:00","dispStatCd":"90"},{"dispNo":"dsp_fall_layers","tgtMbrGrdCd":"G00","bnrTitl":"Fall layers","strtDtm":"2026-11-06T10:00:00-05:00","endDtm":null,"dispStatCd":"20"}]},{"cornerNo":"slot_home_new_in","cornerNm":"New in","cornerTpCd":"G","bnrList":[]},{"cornerNo":"slot_home_stories","cornerNm":"Stories","cornerTpCd":"B","bnrList":[]},{"corne… (+77자) ``
8. 모델 → **`savePrmtList`** `` {"rows":[{"rowStat":"I","prmtNo":"promo_summer_outerwear_vip_weekend_20261107","prmtNm":"Weekend Summer Outerwear 20% VIP","prmtTpCd":"T01","prmtStatCd":"10","tgtMbrGrdCd":"G03","strtDtm":"2026-11-07T00:00:00-05:00","endDtm":"2026-11-08T23:59:00-05:00","aplyTgtCd":"C","ctgNo":"cat_summer_outerwear","prdNoList":[],"dcRt":20}]} ``
   ← 결과 153B: `` {"status":200,"body":{"resultCd":"0000","resultMsg":"Saved.","procCnt":1,"list":[{"rowNo":1,"rowStat":"I","prmtNo":"promo_01m697tvfa8yx0ajw15y387ryn"}]}} ``
9. 모델 → **`saveDispBnrList`** `` {"rows":[{"rowStat":"I","cornerNo":"slot_home_hero","tgtMbrGrdCd":"G03","strtDtm":"2026-11-07T00:00:00-05:00","endDtm":"2026-11-08T23:59:00-05:00","bnrTitl":"Weekend Summer Outerwear 20% Off","bnrSubTitl":"VIP exclusive","btnNm":"Shop now","lnkUrl":"/category/cat_summer_outerwear","prmtNo":"promo_01m697tvfa8yx0ajw15y387ryn"}]} ``
   ← 결과 147B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Row 1: 'imgPrdNo' or 'imgNo' is required.","next_tool":null}}} ``
10. 모델 → **`getPrdDtlInfoV2`** `` {"prdNo":"prd_summer_outerwear_22"} ``
   ← 결과 2,914B: `` {"status":200,"body":{"prdNo":"prd_summer_outerwear_22","prdNm":"Seersucker shacket","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":79.0,"mbrPrc":null,"stkQty":36,"sellStatCd":"10","costPrc":35.55,"prdStatCd":"active","optList":[{"optNo":"var_summer_outerwear_22_xs_rust","optVal1":"Rust","optVal2":"XS","stkQty":2,"sellStatCd":"10"},{"optNo":"var_summer_outerwear_22_s_rust","optVal1":"Rust","optVal2":"S","stkQty":3,"sellStatCd":"10"},{"optNo":"var_summer_outerwear_22_m_rust","optVal1":"Rust","optVal2":"M","stkQty":1,"sellStatCd":"10"},{"optNo":"var_summer_outerwear_22_l_rust"… (+900자) ``
11. 모델 → **`saveDispBnrList`** `` {"rows":[{"rowStat":"I","cornerNo":"slot_home_hero","tgtMbrGrdCd":"G03","strtDtm":"2026-11-07T00:00:00-05:00","endDtm":"2026-11-08T23:59:00-05:00","bnrTitl":"Weekend Summer Outerwear 20% Off","bnrSubTitl":"VIP exclusive","btnNm":"Shop now","lnkUrl":"/category/cat_summer_outerwear","imgPrdNo":"prd_summer_outerwear_22","prmtNo":"promo_01m697tvfa8yx0ajw15y387ryn"}]} ``
   ← 결과 151B: `` {"status":200,"body":{"resultCd":"0000","resultMsg":"Saved.","procCnt":1,"list":[{"rowNo":1,"rowStat":"I","dispNo":"dsp_01m697v42m1zr3t2rmyqznmh5f"}]}} ``
12. 모델 → **`getPrdGridList`** `` {"srchKwd":"summer outerwear","pageNo":1,"pageSize":10} ``
   ← 결과 1,993B: `` {"status":200,"body":{"list":[{"prdNo":"prd_summer_outerwear_22","prdNm":"Seersucker shacket","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":79.0,"mbrPrc":null,"stkQty":36,"sellStatCd":"10","costPrc":35.55},{"prdNo":"prd_summer_outerwear_33","prdNm":"Linen shacket","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":129.0,"mbrPrc":null,"stkQty":30,"sellStatCd":"10","costPrc":58.05},{"prdNo":"prd_rain_parka","prdNm":"Light rain parka","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":118.0,"mbrPrc":null,"stkQty":4,"sellStatCd":"10","costPrc":50.0… (+900자) ``
13. 모델 → **`getPrdGridList`** `` {"srchKwd":"summer outerwear","stkQtyTo":19,"pageNo":1,"pageSize":10} ``
   ← 결과 1,916B: `` {"status":200,"body":{"list":[{"prdNo":"prd_rain_parka","prdNm":"Light rain parka","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":118.0,"mbrPrc":null,"stkQty":4,"sellStatCd":"10","costPrc":50.0},{"prdNo":"prd_summer_outerwear_13","prdNm":"Poplin shacket","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":99.0,"mbrPrc":null,"stkQty":14,"sellStatCd":"10","costPrc":44.55},{"prdNo":"prd_summer_outerwear_15","prdNm":"Cotton overshirt","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":119.0,"mbrPrc":null,"stkQty":14,"sellStatCd":"10","costPrc":53.55}… (+900자) ``
14. 모델 → **`getPrdGridListCnt`** `` {"srchKwd":"summer outerwear","stkQtyFrom":20} ``
   ← 결과 36B: `` {"status":200,"body":{"totCnt":110}} ``
15. 모델 → **`getPrdGridList`** `` {"srchKwd":"summer outerwear","stkQtyFrom":20,"pageNo":1,"pageSize":10} ``
   ← 결과 2,012B: `` {"status":200,"body":{"list":[{"prdNo":"prd_summer_outerwear_22","prdNm":"Seersucker shacket","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":79.0,"mbrPrc":null,"stkQty":36,"sellStatCd":"10","costPrc":35.55},{"prdNo":"prd_summer_outerwear_33","prdNm":"Linen shacket","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":129.0,"mbrPrc":null,"stkQty":30,"sellStatCd":"10","costPrc":58.05},{"prdNo":"prd_summer_outerwear_32","prdNm":"Chambray shacket","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":59.0,"mbrPrc":null,"stkQty":114,"sellStatCd":"10","cos… (+900자) ``
16. 모델 → **`getPrdGridList`** `` {"srchKwd":"summer outerwear","stkQtyFrom":20,"pageNo":2,"pageSize":10} ``
   ← 결과 2,010B: `` {"status":200,"body":{"list":[{"prdNo":"prd_summer_outerwear_02","prdNm":"Ripstop field jacket","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":129.0,"mbrPrc":null,"stkQty":37,"sellStatCd":"10","costPrc":58.05},{"prdNo":"prd_utility_jacket","prdNm":"Cotton utility jacket","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":118.0,"mbrPrc":null,"stkQty":31,"sellStatCd":"10","costPrc":50.0},{"prdNo":"prd_field_jacket","prdNm":"Linen blend field jacket","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":128.0,"mbrPrc":null,"stkQty":86,"sellStatCd":"10… (+900자) ``
17. 모델 → **`getPrdGridList`** `` {"srchKwd":"summer outerwear","stkQtyFrom":20,"pageNo":1,"pageSize":100} ``
   ← 결과 6,014B: `` {"status":200,"body":{"list":[{"prdNo":"prd_summer_outerwear_22","prdNm":"Seersucker shacket","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":79.0,"mbrPrc":null,"stkQty":36,"sellStatCd":"10","costPrc":35.55},{"prdNo":"prd_summer_outerwear_33","prdNm":"Linen shacket","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":129.0,"mbrPrc":null,"stkQty":30,"sellStatCd":"10","costPrc":58.05},{"prdNo":"prd_summer_outerwear_32","prdNm":"Chambray shacket","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":59.0,"mbrPrc":null,"stkQty":114,"sellStatCd":"10","cos… (+900자) ``

**답변 1**
> Created a VIP-only 20% weekend promotion for summer outerwear.
>
> * Promotion: promo_01m697tvfa8yx0ajw15y387ryn
>   Name: Weekend Summer Outerwear 20% VIP
>   Target member grade: G03 VIP
>   Type: T01, status: 10
>   Apply target: Category cat_summer_outerwear
>   Discount: 20%
>   Period: 2026-11-07 00:00:00-05:00 to 2026-11-08 23:59:00-05:00
>
> * Main page placement
>   Corner: slot_home_hero (Home hero)
>   Banner: dsp_01m697v42m1zr3t2rmyqznmh5f
>   Target: G03 VIP
>   Same period as promotion
>   Title: Weekend Summer Outerwear 20% Off
>   Sub-title: VIP exclusive
>   Button: Shop now
>   Link: /category/cat_summer_outerwear
>   Image product: prd_summer_outerwear_22 Seersucker shacket
>   Linked promotion: promo_01m697tvfa8yx0ajw15y387ryn
>
> Both the promotion and the banner are saved as a preview change set awaiting approval.

_(한 턴의 시간 한도(120초)에 걸려 중단)_

**채점**: E TURN_TIMEOUT — 빠진 것: fact "40 of 42 summer outerwear products; chore coat (7) and rain " (40, 42, 4 not shown); fact "the overshirt is at 15% ($67.15) to stay above the price flo" (15, 67.15 not shown); HOST:TURN_TIMEOUT

### acom-all · 1회차 · E CONTEXT_OVERFLOW

토큰 0 · 0.338초 · 모델 호출 0회 · 도구 호출 0회

준비: 전략 `None`, 함수 253개

**질문 1**
> Run a 20% weekend sale on summer outerwear for VIP members and put it on the main page.

**질문 2**
> Drop the low-stock ones. Give the overshirt 15% instead.

_(이 실행은 호출이 어느 턴에 속하는지 기록하지 않았다. 호출을 순서대로 보인다.)_


_(CONTEXT_OVERFLOW로 중단)_

**채점**: E CONTEXT_OVERFLOW — 빠진 것: tool search_products; tool list_tiers; tool set_sale_prices; tool create_coupon; tool schedule_banner; change set; fact "40 of 42 summer outerwear products; chore coat (7) and rain " (40, 42, 7, 4 not shown); fact "the overshirt is at 15% ($67.15) to stay above the price flo" (15, 67.15 not shown); HOST:CONTEXT_OVERFLOW
(도구 정밀도 —, 재현율 0.00)

### a2api-acom · 1회차 · E MODEL_CALL_LIMIT

토큰 86,294 · 70.853초 · 모델 호출 12회 · 도구 호출 16회 · 첫 요청 프롬프트 3,630토큰

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
3. 모델 → **`a2api_search`** `` {"query":"display slot book"} ``
   ← 결과 456B: `` {"selected":[{"name":"acom_schedule_display","id":"acom.schedule_display"},{"name":"acom_arrange_display_slot","id":"acom.arrange_display_slot"},{"name":"acom_get_display_slot","id":"acom.get_display_slot"},{"name":"acom_list_display_slots","id":"acom.list_display_slots"},{"name":"acom_invalidate_display_cache","id":"acom.invalidate_display_cache"}],"evicted":["acom_create_coupon"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`a2api_search`** `` {"query":"summer outerwear category"} ``
   ← 결과 477B: `` {"selected":[{"name":"acom_create_category","id":"acom.create_category"},{"name":"acom_get_category","id":"acom.get_category"},{"name":"acom_list_categories","id":"acom.list_categories"},{"name":"acom_map_category","id":"acom.map_category"},{"name":"acom_update_category","id":"acom.update_category"}],"evicted":["acom_get_promotion","acom_pause_promotion","acom_search_promotions","acom_schedule_banner"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
5. 모델 → **`acom_list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
6. 모델 → **`a2api_search`** `` {"query":"create promotion parameters"} ``
   ← 결과 547B: `` {"selected":[{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_get_promotion","id":"acom.get_promotion"},{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"}],"evicted":["acom_set_banner","acom_schedule_display","acom_arrange_display_slot","acom_get_display_slot","acom_list_display_slots","acom_invalidate_display_cache"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
7. 모델 → **`a2api_search`** `` {"query":"set sale prices"} ``
   ← 결과 526B: `` {"selected":[{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_set_price","id":"acom.set_price"},{"name":"acom_get_promotion","id":"acom.get_promotion"},{"name":"acom_update_product","id":"acom.update_product"},{"name":"acom_list_active_promotions","id":"acom.list_active_promotions"}],"evicted":["acom_create_category","acom_get_category","acom_map_category","acom_update_category","acom_list_categories","acom_create_promotion"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
8. 모델 → **`a2api_search`** `` {"query":"percent off promotion"} ``
   ← 결과 506B: `` {"selected":[{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_end_promotion","id":"acom.end_promotion"}],"evicted":["acom_create_coupon","acom_pause_promotion","acom_search_promotions","acom_set_price","acom_get_promotion"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
9. 모델 → **`a2api_search`** `` {"query":"list tiers"} ``
   ← 결과 484B: `` {"selected":[{"name":"acom_list_tiers","id":"acom.list_tiers"},{"name":"acom_list_tier_history","id":"acom.list_tier_history"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_issue_coupon","id":"acom.issue_coupon"},{"name":"acom_create_campaign","id":"acom.create_campaign"}],"evicted":["acom_update_product","acom_list_active_promotions","acom_create_promotion","acom_set_sale_prices"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
10. 모델 → **`acom_list_tiers`** `` {} ``
   ← 결과 305B: `` {"status":"succeeded","data":{"items":[{"id":"vip","name":"VIP","rank":3,"program_id":"prg_rewards","member_count":1284},{"id":"gold","name":"Gold","rank":2,"program_id":"prg_rewards","member_count":2900},{"id":"member","name":"Member","rank":1,"program_id":"prg_rewards","member_count":9816}],"total":3}} ``
11. 모델 → **`acom_search_promotions`** `` {"valid_for_member_tier":"vip","discount_layer":"item_price","query":"summer","limit":20} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
12. 모델 → **`a2api_search`** `` {"query":"create promotion"} ``
   ← 결과 508B: `` {"selected":[{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_get_promotion","id":"acom.get_promotion"},{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"}],"evicted":["acom_pause_promotion","acom_end_promotion","acom_list_tier_history","acom_search_products","acom_issue_coupon"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":false} ``
13. 모델 → **`a2api_search`** `` {"query":"set sale prices parameters"} ``
   ← 결과 458B: `` {"selected":[{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_set_price","id":"acom.set_price"},{"name":"acom_get_promotion","id":"acom.get_promotion"},{"name":"acom_update_product","id":"acom.update_product"},{"name":"acom_list_active_promotions","id":"acom.list_active_promotions"}],"evicted":["acom_create_campaign","acom_list_tiers","acom_create_promotion"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
14. 모델 → **`acom_list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","valid_for_member_tier":"vip"} ``
   ← 결과 635B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_free_ship_80","name":"Free shipping over $80","status":"running","discount_layer":"add_on","valid_for_member_tier":"everyone","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"applies_to":{"scope":"order","category_ids":[],… (+35자) ``
15. 모델 → **`acom_list_display_slots`** `` {} ``
   ← 실패 198B: `` {"status":"failed","error":{"code":"NOT_SELECTED","detail":"Function is not active in this session; search again."},"hint":"Call only functions currently provided; search if a function is missing."} ``
16. 모델 → **`a2api_search`** `` {"query":"list display slots"} ``
   ← 결과 527B: `` {"selected":[{"name":"acom_list_display_slots","id":"acom.list_display_slots"},{"name":"acom_arrange_display_slot","id":"acom.arrange_display_slot"},{"name":"acom_get_display_slot","id":"acom.get_display_slot"},{"name":"acom_invalidate_display_cache","id":"acom.invalidate_display_cache"},{"name":"acom_schedule_display","id":"acom.schedule_display"}],"evicted":["acom_create_coupon","acom_pause_promotion","acom_search_promotions","acom_set_sale_prices"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: tool search_products; tool set_sale_prices; tool create_coupon; tool schedule_banner; change set; fact "40 of 42 summer outerwear products; chore coat (7) and rain " (40, 42, 7, 4 not shown); fact "the overshirt is at 15% ($67.15) to stay above the price flo" (15, 67.15 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.75, 재현율 0.20)

### a2api-facade · 1회차 · E TURN_TIMEOUT

토큰 139,590 · 219.428초 · 모델 호출 16회 · 도구 호출 15회 · 첫 요청 프롬프트 3,288토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> Run a 20% weekend sale on summer outerwear for VIP members and put it on the main page.

**질문 2**
> Drop the low-stock ones. Give the overshirt 15% instead.

_(이 실행은 호출이 어느 턴에 속하는지 기록하지 않았다. 호출을 순서대로 보인다.)_

1. 모델 → **`facade_get_prd_grid_list`** `` {"keyword":"summer outerwear","page_size":20,"page":1} ``
   ← 결과 4,505B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_summer_outerwear_22","product_name":"Seersucker shacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":79.0,"member_price":null,"stock":36,"availability":"in_stock","cost":35.55},{"product_id":"prd_summer_outerwear_33","product_name":"Linen shacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":129.0,"member_price":null,"stock":30,"availability":"in_stock","cost":58.05},{"product_id":"prd_rain_parka","product_name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_… (+900자) ``
2. 모델 → **`a2api_search`** `` {"query":"member grade"} ``
   ← 결과 425B: `` {"selected":[{"name":"facade_get_mbr_grd_list","id":"facade.get_mbr_grd_list"},{"name":"facade_get_prmt_tgt_mbr_list","id":"facade.get_prmt_tgt_mbr_list"},{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_get_prmt_grid_list","id":"facade.get_prmt_grid_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`facade_get_mbr_grd_list`** `` {} ``
   ← 결과 257B: `` {"status":"succeeded","data":{"list":[{"member_grade":"G03","grade_name":"VIP","member_count":1284,"rank":3},{"member_grade":"G02","grade_name":"Gold","member_count":2900,"rank":2},{"member_grade":"G01","grade_name":"Member","member_count":9816,"rank":1}]}} ``
4. 모델 → **`a2api_search`** `` {"query":"main page"} ``
   ← 결과 441B: `` {"selected":[{"name":"facade_get_prmt_tgt_mbr_list","id":"facade.get_prmt_tgt_mbr_list"},{"name":"facade_get_disp_corner_list","id":"facade.get_disp_corner_list"},{"name":"facade_get_clm_grid_list","id":"facade.get_clm_grid_list"},{"name":"facade_get_prmt_grid_list","id":"facade.get_prmt_grid_list"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
5. 모델 → **`facade_get_disp_corner_list`** `` {"page_type":"main","starts_at":"2026-11-07T00:00:00-04:00","ends_at":"2026-11-09T23:59:59-04:00"} ``
   ← 결과 592B: `` {"status":"succeeded","data":{"list":[{"corner_id":"slot_home_hero","corner_name":"Home hero","corner_type":"hero","banners":[{"booking_id":"dsp_fall_layers","target_member_grade":"G00","headline":"Fall layers","starts_at":"2026-11-06T10:00:00-05:00","ends_at":null,"display_status":"active"}]},{"corner_id":"slot_home_new_in","corner_name":"New in","corner_type":"product_grid","banners":[]},{"corner_id":"slot_home_stories","corner_name":"Stories","corner_type":"banner_board","banners":[]},{"corner_id":"slot_home_brands","corner_name":"Brands","corner_type":"brand_strip","banners":[]}]}} ``
6. 모델 → **`a2api_search`** `` {"query":"display corner banner"} ``
   ← 결과 230B: `` {"selected":[{"name":"facade_get_disp_corner_list","id":"facade.get_disp_corner_list"},{"name":"facade_save_disp_bnr_list","id":"facade.save_disp_bnr_list"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true} ``
7. 모델 → **`facade_get_prmt_grid_list`** `` {"promotion_name":"summer","page_size":20,"page":1} ``
   ← 결과 65B: `` {"status":"succeeded","data":{"list":[],"page":1,"page_size":20}} ``
8. 모델 → **`facade_save_prmt_list`** `` {"rows":[{"row_action":"insert","promotion_id":"promo_summer_vip_weekend_20261107","promotion_name":"Weekend Summer Outerwear VIP 20% Off","promotion_type":"item_price_one_grade","promotion_status":"scheduled","target_member_grade":"G03","starts_at":"2026-11-07T00:00:00-05:00","ends_at":"2026-11-08T23:59:59-05:00","applies_to":"category","category_id":"cat_summer_outerwear","percent_off":20}]} ``
   ← 결과 184B: `` {"status":"succeeded","data":{"result_code":"0000","result_message":"Saved.","saved_rows":1,"list":[{"row":1,"row_action":"insert","promotion_id":"promo_01m6984wcjt81jhqy24a9jd9n7"}]}} ``
9. 모델 → **`facade_save_disp_bnr_list`** `` {"rows":[{"row_action":"insert","corner_id":"slot_home_hero","target_member_grade":"G03","starts_at":"2026-11-07T00:00:00-05:00","ends_at":"2026-11-08T23:59:59-05:00","eyebrow":"VIP Weekend","headline":"20% Off Summer Outerwear","button_label":"Shop Now","link_url":"/category/cat_summer_outerwear","image_product_id":"prd_summer_outerwear_22","promotion_id":"promo_01m6984wcjt81jhqy24a9jd9n7"}]} ``
   ← 결과 180B: `` {"status":"succeeded","data":{"result_code":"0000","result_message":"Saved.","saved_rows":1,"list":[{"row":1,"row_action":"insert","booking_id":"dsp_01m6984zzpmwz07mfv3qxdq13m"}]}} ``
10. 모델 → **`facade_get_prd_grid_list`** `` {"category_id":"cat_summer_outerwear","page_size":100,"page":1} ``
   ← 결과 6,014B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_summer_outerwear_13","product_name":"Poplin shacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":99.0,"member_price":null,"stock":14,"availability":"in_stock","cost":44.55},{"product_id":"prd_summer_outerwear_22","product_name":"Seersucker shacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":79.0,"member_price":null,"stock":36,"availability":"in_stock","cost":35.55},{"product_id":"prd_summer_outerwear_20","product_name":"Cotton anorak","category_id":"cat_summer_outerwear","brand_id"… (+900자) ``
11. 모델 → **`facade_get_prd_grid_list`** `` {"category_id":"cat_summer_outerwear","page_size":100,"page":2} ``
   ← 결과 66B: `` {"status":"succeeded","data":{"list":[],"page":2,"page_size":100}} ``
12. 모델 → **`facade_get_prd_grid_list`** `` {"keyword":"overshirt","page_size":100,"page":1} ``
   ← 결과 6,014B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_camp_overshirt","product_name":"Linen camp overshirt","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":88.0,"member_price":null,"stock":40,"availability":"in_stock","cost":36.0},{"product_id":"prd_seersucker_overshirt","product_name":"Seersucker overshirt","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":79.0,"member_price":null,"stock":53,"availability":"in_stock","cost":58.0},{"product_id":"prd_summer_outerwear_15","product_name":"Cotton overshirt","category_id":"cat_summer_outerwear","bran… (+900자) ``
13. 모델 → **`facade_get_prd_grid_list`** `` {"category_id":"cat_summer_outerwear","page_size":50,"page":1} ``
   ← 결과 6,014B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_summer_outerwear_13","product_name":"Poplin shacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":99.0,"member_price":null,"stock":14,"availability":"in_stock","cost":44.55},{"product_id":"prd_summer_outerwear_22","product_name":"Seersucker shacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":79.0,"member_price":null,"stock":36,"availability":"in_stock","cost":35.55},{"product_id":"prd_summer_outerwear_20","product_name":"Cotton anorak","category_id":"cat_summer_outerwear","brand_id"… (+900자) ``
14. 모델 → **`facade_get_prd_grid_list`** `` {"category_id":"cat_summer_outerwear","page_size":20,"page":1} ``
   ← 결과 4,514B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_summer_outerwear_13","product_name":"Poplin shacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":99.0,"member_price":null,"stock":14,"availability":"in_stock","cost":44.55},{"product_id":"prd_summer_outerwear_22","product_name":"Seersucker shacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":79.0,"member_price":null,"stock":36,"availability":"in_stock","cost":35.55},{"product_id":"prd_summer_outerwear_20","product_name":"Cotton anorak","category_id":"cat_summer_outerwear","brand_id"… (+900자) ``
15. 모델 → **`facade_get_prd_grid_list`** `` {"category_id":"cat_summer_outerwear","page_size":50,"page":1} ``
   ← 결과 6,014B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_summer_outerwear_13","product_name":"Poplin shacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":99.0,"member_price":null,"stock":14,"availability":"in_stock","cost":44.55},{"product_id":"prd_summer_outerwear_22","product_name":"Seersucker shacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":79.0,"member_price":null,"stock":36,"availability":"in_stock","cost":35.55},{"product_id":"prd_summer_outerwear_20","product_name":"Cotton anorak","category_id":"cat_summer_outerwear","brand_id"… (+900자) ``

**답변 1**
> Created promotion promo_01m6984wcjt81jhqy24a9jd9n7 “Weekend Summer Outerwear VIP 20% Off” for member grade G03 (VIP) on category cat_summer_outerwear, scheduled 2026-11-07 00:00 to 2026-11-08 23:59 America/New_York, 20% off.
>
> Scheduled main-page hero banner booking dsp_01m6984zzpmwz07mfv3qxdq13m in slot_home_hero for VIPs for the same weekend, linking to /category/cat_summer_outerwear with product prd_summer_outerwear_22 image.
>
> The promotion and banner are saved and pending approval; they will go live for the weekend once approved.

_(한 턴의 시간 한도(120초)에 걸려 중단)_

**채점**: E TURN_TIMEOUT — 빠진 것: fact "40 of 42 summer outerwear products; chore coat (7) and rain " (40, 42, 4 not shown); fact "the overshirt is at 15% ($67.15) to stay above the price flo" (15, 67.15 not shown); HOST:TURN_TIMEOUT
