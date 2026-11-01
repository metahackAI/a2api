# md-end-of-season-markdown — ours-design-1

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `a2c7201`

**과업**

> start the end of season markdown on tees. 25% off for everyone through Nov 15, leave out anything that's almost gone

- 필요한 도구: `search_products`, `set_sale_prices`
- 허용 도구: `get_policy`, `list_categories`, `list_active_promotions`
- 답에 있어야 할 사실: 25% is over the 20% limit for everyone (the VIP limit of 30% does not apply), so the draft is blocked
- 답에 있어야 할 사실: the agent offers 20%, or a 25% sale limited to VIP
- change set: `` {"state":"drafting","items":[{"tool":"set_sale_prices","args":{"valid_for_member_tier":"everyone","scope_mode":"category","category_id":"cat_tees","exclude_low_stock":true}}],"checks_failed":["max_discount"]} ``

### facade-all · 1회차 · E MODEL_OUTPUT_TRUNCATED

토큰 71,581 · 117.784초 · 모델 호출 10회 · 도구 호출 9회 · 첫 요청 프롬프트 4,664토큰

준비: 전략 `None`, 함수 19개

**질문 1**
> start the end of season markdown on tees. 25% off for everyone through Nov 15, leave out anything that's almost gone

1. 모델 → **`getPrmtGridList`** `` {"pageNo":0,"pageSize":10} ``
   ← 결과 121B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null}}} ``
2. 모델 → **`getPrdGridList`** `` {"srchKwd":"tee","pageNo":0,"pageSize":10} ``
   ← 결과 121B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null}}} ``
3. 모델 → **`getPrdGridList`** `` {"srchKwd":"tee","pageNo":1,"pageSize":10} ``
   ← 결과 1,780B: `` {"status":200,"body":{"list":[{"prdNo":"prd_tees_14","prdNm":"Waffle tee","ctgNo":"cat_tees","brndNo":"brn_northwind","salePrc":19.0,"mbrPrc":null,"stkQty":84,"sellStatCd":"10","costPrc":7.0},{"prdNo":"prd_merino_tee","prdNm":"Merino trail tee","ctgNo":"cat_shirts","brndNo":"brn_ridgeline","salePrc":58.0,"mbrPrc":null,"stkQty":45,"sellStatCd":"10","costPrc":22.0},{"prdNo":"prd_tees_04","prdNm":"Jersey long-sleeve tee","ctgNo":"cat_tees","brndNo":"brn_northwind","salePrc":39.0,"mbrPrc":null,"stkQty":77,"sellStatCd":"10","costPrc":16.8},{"prdNo":"prd_tees_09","prdNm":"Waffle crew tee","ctgNo":"c… (+900자) ``
4. 모델 → **`getPrmtGridList`** `` {"pageNo":1,"pageSize":10} ``
   ← 결과 1,121B: `` {"status":200,"body":{"list":[{"prmtNo":"promo_denim_bundle","prmtNm":"Denim bundle","prmtTpCd":"T02","prmtStatCd":"10","tgtMbrGrdCd":"G00","strtDtm":"2026-11-13T00:00:00-05:00","endDtm":"2026-11-20T23:59:00-05:00"},{"prmtNo":"promo_autumn_knit","prmtNm":"Autumn knitwear 15%","prmtTpCd":"T01","prmtStatCd":"20","tgtMbrGrdCd":"G00","strtDtm":"2026-11-01T00:00:00-04:00","endDtm":"2026-11-15T23:59:00-05:00"},{"prmtNo":"promo_linen_clearance","prmtNm":"Linen clearance","prmtTpCd":"T01","prmtStatCd":"90","tgtMbrGrdCd":"G00","strtDtm":"2026-10-01T00:00:00-04:00","endDtm":"2026-10-20T23:59:00-04:00"},… (+521자) ``
5. 모델 → **`getPrdGridListCnt`** `` {"srchKwd":"tee","pageNo":1,"pageSize":10} ``
   ← 결과 35B: `` {"status":200,"body":{"totCnt":61}} ``
6. 모델 → **`getPrdGridList`** `` {"ctgNo":"cat_tees","pageNo":1,"pageSize":10} ``
   ← 결과 1,777B: `` {"status":200,"body":{"list":[{"prdNo":"prd_tees_04","prdNm":"Jersey long-sleeve tee","ctgNo":"cat_tees","brndNo":"brn_northwind","salePrc":39.0,"mbrPrc":null,"stkQty":77,"sellStatCd":"10","costPrc":16.8},{"prdNo":"prd_tees_09","prdNm":"Waffle crew tee","ctgNo":"cat_tees","brndNo":"brn_northwind","salePrc":59.0,"mbrPrc":null,"stkQty":134,"sellStatCd":"10","costPrc":21.22},{"prdNo":"prd_tees_22","prdNm":"Organic cotton boxy tee","ctgNo":"cat_tees","brndNo":"brn_ridgeline","salePrc":39.0,"mbrPrc":null,"stkQty":75,"sellStatCd":"10","costPrc":15.14},{"prdNo":"prd_tees_02","prdNm":"Cotton V-neck te… (+900자) ``
7. 모델 → **`getPrdGridListCnt`** `` {"ctgNo":"cat_tees","pageNo":1,"pageSize":10} ``
   ← 결과 35B: `` {"status":200,"body":{"totCnt":24}} ``
8. 모델 → **`getPrdGridList`** `` {"ctgNo":"cat_tees","pageNo":2,"pageSize":10} ``
   ← 결과 1,811B: `` {"status":200,"body":{"list":[{"prdNo":"prd_tees_19","prdNm":"Linen blend pocket tee","ctgNo":"cat_tees","brndNo":"brn_northwind","salePrc":19.0,"mbrPrc":null,"stkQty":30,"sellStatCd":"10","costPrc":8.17},{"prdNo":"prd_tees_21","prdNm":"Heavyweight cotton henley","ctgNo":"cat_tees","brndNo":"brn_northwind","salePrc":29.0,"mbrPrc":null,"stkQty":94,"sellStatCd":"10","costPrc":10.78},{"prdNo":"prd_tees_13","prdNm":"Linen blend boxy tee","ctgNo":"cat_tees","brndNo":"brn_northwind","salePrc":39.0,"mbrPrc":null,"stkQty":73,"sellStatCd":"10","costPrc":14.59},{"prdNo":"prd_tees_03","prdNm":"Heavyweigh… (+900자) ``
9. 모델 → **`getPrdGridList`** `` {"ctgNo":"cat_tees","pageNo":3,"pageSize":10} ``
   ← 결과 758B: `` {"status":200,"body":{"list":[{"prdNo":"prd_tees_10","prdNm":"Cotton raglan tee","ctgNo":"cat_tees","brndNo":"brn_ridgeline","salePrc":49.0,"mbrPrc":null,"stkQty":67,"sellStatCd":"10","costPrc":17.4},{"prdNo":"prd_tees_17","prdNm":"Organic cotton crew tee","ctgNo":"cat_tees","brndNo":"brn_northwind","salePrc":19.0,"mbrPrc":null,"stkQty":76,"sellStatCd":"10","costPrc":8.53},{"prdNo":"prd_tees_12","prdNm":"Slub cotton V-neck tee","ctgNo":"cat_tees","brndNo":"brn_northwind","salePrc":49.0,"mbrPrc":null,"stkQty":34,"sellStatCd":"10","costPrc":20.85},{"prdNo":"prd_tees_01","prdNm":"Organic cotton p… (+158자) ``

_(모델 출력이 출력 한도에 걸려 중단)_

**채점**: E MODEL_OUTPUT_TRUNCATED — 빠진 것: fact "25% is over the 20% limit for everyone (the VIP limit of 30%" (25, 20, 30 not shown); fact "the agent offers 20%, or a 25% sale limited to VIP" (20, 25 not shown); HOST:MODEL_OUTPUT_TRUNCATED

### acom-all · 1회차 · E CONTEXT_OVERFLOW

토큰 0 · 0.382초 · 모델 호출 0회 · 도구 호출 0회

준비: 전략 `None`, 함수 253개

**질문 1**
> start the end of season markdown on tees. 25% off for everyone through Nov 15, leave out anything that's almost gone


_(CONTEXT_OVERFLOW로 중단)_

**채점**: E CONTEXT_OVERFLOW — 빠진 것: tool search_products; tool set_sale_prices; change set; fact "25% is over the 20% limit for everyone (the VIP limit of 30%" (25, 20, 30 not shown); fact "the agent offers 20%, or a 25% sale limited to VIP" (20, 25 not shown); HOST:CONTEXT_OVERFLOW
(도구 정밀도 —, 재현율 0.00)

### a2api-acom · 1회차 · ✓ 통과

토큰 67,748 · 106.78초 · 모델 호출 8회 · 도구 호출 7회 · 첫 요청 프롬프트 5,033토큰

준비: 전략 `search`, 함수 7개

**질문 1**
> start the end of season markdown on tees. 25% off for everyone through Nov 15, leave out anything that's almost gone

1. 모델 → **`a2api_search`** `` {"query":"list categories"} ``
   ← 결과 473B: `` {"selected":[{"name":"acom_list_categories","id":"acom.list_categories"},{"name":"acom_get_contract","id":"acom.get_contract"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_list_faqs","id":"acom.list_faqs"}],"evicted":["acom_update_promotion","acom_set_member_tier","acom_suggest_reorder","acom_create_promotion"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`acom_list_categories`** `` {} ``
   ← 결과 3,713B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
3. 모델 → **`acom_set_sale_prices`** `` {"name":"End of season tees markdown","valid_for_member_tier":"everyone","valid_from":"2026-11-06T11:00","valid_through":"2026-11-15T23:59","scope_mode":"category","category_id":"cat_tees","percent_off":25,"exclude_low_stock":true} ``
   ← 결과 6,014B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6968w50szztdb6kcdt6tv99","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"End of season tees markdown","valid_for_member_tier":"everyone","discount_layer":"item_price","valid_from":"2026-11-06T11:00:00-05:00","valid_through":"2026-11-15T23:59:00-05:00","products":24}},{"op":"update","entity":"unit_price_specification","id":null,"from":{"product_id":"prd_breton_tee","price":23.0,"price_currency":"USD","price_type":"list_price"},"to":{"product_id":"prd_breton_tee","price":17.25,"price_currency":"USD","price… (+900자) ``
4. 모델 → **`acom_search_products`** `` {"category_id":"cat_tees","limit":100} ``
   ← 결과 6,014B: `` {"status":"succeeded","data":{"items":[{"id":"prd_tees_04","name":"Jersey long-sleeve tee","category_id":"cat_tees","brand_id":"brn_northwind","image":"/media/garment/tee-white.svg","price":39.0,"price_currency":"USD","member_price":null,"cost":16.8,"inventory_level":77,"availability":"in_stock","has_variant":[{"variant_id":"var_tees_04_xs_white","sku":"tees-04-white-xs","size":"XS","color":"White","inventory_level":13,"availability":"in_stock"},{"variant_id":"var_tees_04_s_white","sku":"tees-04-white-s","size":"S","color":"White","inventory_level":14,"availability":"in_stock"},{"variant_id":"… (+900자) ``
5. 모델 → **`acom_search_products`** `` {"category_id":"cat_tees","limit":100,"fields":["id","name","inventory_level","price"]} ``
   ← 결과 2,102B: `` {"status":"succeeded","data":{"items":[{"id":"prd_tees_04","name":"Jersey long-sleeve tee","price":39.0,"inventory_level":77},{"id":"prd_tees_09","name":"Waffle crew tee","price":59.0,"inventory_level":134},{"id":"prd_tees_22","name":"Organic cotton boxy tee","price":39.0,"inventory_level":75},{"id":"prd_tees_02","name":"Cotton V-neck tee","price":39.0,"inventory_level":63},{"id":"prd_tees_11","name":"Pima cotton henley","price":19.0,"inventory_level":34},{"id":"prd_tees_16","name":"Jersey raglan tee","price":29.0,"inventory_level":98},{"id":"prd_tees_14","name":"Waffle tee","price":19.0,"inve… (+900자) ``
6. 모델 → **`a2api_search`** `` {"query":"promo min stock"} ``
   ← 결과 387B: `` {"selected":[{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_set_variant_stock","id":"acom.set_variant_stock"},{"name":"acom_set_safety_stock","id":"acom.set_safety_stock"},{"name":"acom_get_inventory","id":"acom.get_inventory"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
7. 모델 → **`a2api_search`** `` {"query":"promo_min_stock"} ``
   ← 결과 387B: `` {"selected":[{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_set_variant_stock","id":"acom.set_variant_stock"},{"name":"acom_set_safety_stock","id":"acom.set_safety_stock"},{"name":"acom_get_inventory","id":"acom.get_inventory"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``

**답변 1**
> End-of-season markdown for Tees is staged as a preview waiting for approval.
>
> **Promotion preview**
> * preview_id: `pv_01m6968w50szztdb6kcdt6tv99`
> * name: End of season tees markdown
> * valid_for_member_tier: everyone
> * valid_from: 2026-11-06T11:00:00-05:00
> * valid_through: 2026-11-15T23:59:00-05:00
> * scope: category `cat_tees` – Tees
> * discount: 25% off list price
> * exclude_low_stock: true
>
> The preview creates a promotion for the Tees category and applies a 25% sale price to the products in scope. The system reports 24 products in scope.
>
> Products included in the preview with list → sale price and total inventory:
>
> * prd_breton_tee – Breton tee – $23.00 → $17.25 – inventory 60
> * prd_tees_01 – Organic cotton pocket tee – $49.00 → $36.75 – inventory 32
> * prd_tees_02 – Cotton V-neck tee – $39.00 → $29.25 – inventory 63
> * prd_tees_03 – Heavyweight cotton raglan tee – $39.00 → $29.25 – inventory 91
> * prd_tees_04 – Jersey long-sleeve tee – $39.00 → $29.25 – inventory 77
> * prd_tees_05 – Linen blend V-neck tee – $19.00 → $14.25 – inventory 63
> * prd_tees_06 – Jersey boxy tee – $49.00 → $36.75 – inventory 32
> * prd_tees_07 – Cotton henley – $29.00 → $21.75 – inventory 145
> * prd_tees_08 – Heavyweight cotton V-neck tee – $49.00 → $36.75 – inventory 121
> * prd_tees_09 – Waffle crew tee – $59.00 → $44.25 – inventory 134
> * prd_tees_10 – Cotton raglan tee – $49.00 → $36.75 – inventory 67
> * prd_tees_11 – Pima cotton henley – $19.00 → $14.25 – inventory 34
> * prd_tees_12 – Slub cotton V-neck tee – $49.00 → $36.75 – inventory 34
> * prd_tees_13 – Linen blend boxy tee – $39.00 → $29.25 – inventory 73
> * prd_tees_14 – Waffle tee – $19.00 → $14.25 – inventory 84
> * prd_tees_15 – Slub cotton long-sleeve tee – $29.00 → $21.75 – inventory 115
> * prd_tees_16 – Jersey raglan tee – $29.00 → $21.75 – inventory 98
> * prd_tees_17 – Organic cotton crew tee – $19.00 → $14.25 – inventory 76
> * prd_tees_18 – Organic cotton raglan tee – $39.00 → $29.25 – inventory 24
> * prd_tees_19 – Linen blend pocket tee – $19.… (+725자)

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-facade · 1회차 · E MODEL_CONNECTION_FAILED

토큰 50,661 · 120.183초 · 모델 호출 11회 · 도구 호출 19회 · 첫 요청 프롬프트 1,368토큰

준비: 전략 `search`, 함수 3개

**질문 1**
> start the end of season markdown on tees. 25% off for everyone through Nov 15, leave out anything that's almost gone

1. 모델 → **`a2api_search`** `` {"query":"category list"} ``
   ← 결과 431B: `` {"selected":[{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_save_prmt_list","id":"facade.save_prmt_list"},{"name":"facade_get_prd_grid_list_cnt","id":"facade.get_prd_grid_list_cnt"},{"name":"facade_get_mbr_grd_list","id":"facade.get_mbr_grd_list"},{"name":"facade_get_disp_corner_list","id":"facade.get_disp_corner_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"product list"} ``
   ← 결과 429B: `` {"selected":[{"name":"facade_get_prd_grid_list_cnt","id":"facade.get_prd_grid_list_cnt"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_save_prmt_list","id":"facade.save_prmt_list"},{"name":"facade_get_prd_dtl_info","id":"facade.get_prd_dtl_info"},{"name":"facade_get_prd_dtl_info_v2","id":"facade.get_prd_dtl_info_v2"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`a2api_search`** `` {"query":"stock inventory"} ``
   ← 결과 368B: `` {"selected":[{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_get_prd_dtl_info","id":"facade.get_prd_dtl_info"},{"name":"facade_get_prd_dtl_info_v2","id":"facade.get_prd_dtl_info_v2"},{"name":"facade_get_prd_grid_list_cnt","id":"facade.get_prd_grid_list_cnt"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`a2api_search`** `` {"query":"tee shirt category"} ``
   ← 결과 292B: `` {"selected":[{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_save_prmt_list","id":"facade.save_prmt_list"},{"name":"facade_get_prd_grid_list_cnt","id":"facade.get_prd_grid_list_cnt"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true} ``
5. 모델 → **`facade_get_mbr_grd_list`** `` {} ``
   ← 결과 257B: `` {"status":"succeeded","data":{"list":[{"member_grade":"G03","grade_name":"VIP","member_count":1284,"rank":3},{"member_grade":"G02","grade_name":"Gold","member_count":2900,"rank":2},{"member_grade":"G01","grade_name":"Member","member_count":9816,"rank":1}]}} ``
6. 모델 → **`facade_get_prd_grid_list`** `` {"keyword":"tee","availability":"in_stock","page":0,"page_size":20} ``
   ← 실패 237B: `` {"status":"failed","error":{"code":"UPSTREAM_VALIDATION_FAILED","detail":"The backend rejected the request values. (HTTP 422) Invalid paging."},"hint":"The service rejected these values. Correct them only if the user gave other values."} ``
7. 모델 → **`facade_get_prd_grid_list`** `` {"keyword":"tee","availability":"in_stock","page":0,"page_size":10} ``
   ← 실패 237B: `` {"status":"failed","error":{"code":"UPSTREAM_VALIDATION_FAILED","detail":"The backend rejected the request values. (HTTP 422) Invalid paging."},"hint":"The service rejected these values. Correct them only if the user gave other values."} ``
8. 모델 → **`facade_get_prd_grid_list_cnt`** `` {"keyword":"tee","availability":"in_stock"} ``
   ← 결과 42B: `` {"status":"succeeded","data":{"total":61}} ``
9. 모델 → **`facade_get_prd_grid_list`** `` {"keyword":"tee","availability":"in_stock","page":1,"page_size":10} ``
   ← 결과 2,067B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_tees_14","product_name":"Waffle tee","category_id":"cat_tees","brand_id":"brn_northwind","price":19.0,"member_price":null,"stock":84,"availability":"in_stock","cost":7.0},{"product_id":"prd_merino_tee","product_name":"Merino trail tee","category_id":"cat_shirts","brand_id":"brn_ridgeline","price":58.0,"member_price":null,"stock":45,"availability":"in_stock","cost":22.0},{"product_id":"prd_tees_04","product_name":"Jersey long-sleeve tee","category_id":"cat_tees","brand_id":"brn_northwind","price":39.0,"member_price":null,"stock":77,"avail… (+900자) ``
10. 모델 → **`facade_get_prd_grid_list_cnt`** `` {"category_id":"cat_tees","availability":"in_stock"} ``
   ← 결과 42B: `` {"status":"succeeded","data":{"total":24}} ``
11. 모델 → **`facade_get_prd_grid_list`** `` {"category_id":"cat_tees","availability":"in_stock","page":1,"page_size":10} ``
   ← 결과 2,064B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_tees_04","product_name":"Jersey long-sleeve tee","category_id":"cat_tees","brand_id":"brn_northwind","price":39.0,"member_price":null,"stock":77,"availability":"in_stock","cost":16.8},{"product_id":"prd_tees_09","product_name":"Waffle crew tee","category_id":"cat_tees","brand_id":"brn_northwind","price":59.0,"member_price":null,"stock":134,"availability":"in_stock","cost":21.22},{"product_id":"prd_tees_22","product_name":"Organic cotton boxy tee","category_id":"cat_tees","brand_id":"brn_ridgeline","price":39.0,"member_price":null,"stock"… (+900자) ``
12. 모델 → **`facade_get_prd_grid_list`** `` {"category_id":"cat_tees","availability":"in_stock","page":2,"page_size":10} ``
   ← 결과 2,098B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_tees_19","product_name":"Linen blend pocket tee","category_id":"cat_tees","brand_id":"brn_northwind","price":19.0,"member_price":null,"stock":30,"availability":"in_stock","cost":8.17},{"product_id":"prd_tees_21","product_name":"Heavyweight cotton henley","category_id":"cat_tees","brand_id":"brn_northwind","price":29.0,"member_price":null,"stock":94,"availability":"in_stock","cost":10.78},{"product_id":"prd_tees_13","product_name":"Linen blend boxy tee","category_id":"cat_tees","brand_id":"brn_northwind","price":39.0,"member_price":null,"… (+900자) ``
13. 모델 → **`facade_get_prd_grid_list`** `` {"category_id":"cat_tees","availability":"in_stock","page":3,"page_size":10} ``
   ← 결과 877B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_tees_10","product_name":"Cotton raglan tee","category_id":"cat_tees","brand_id":"brn_ridgeline","price":49.0,"member_price":null,"stock":67,"availability":"in_stock","cost":17.4},{"product_id":"prd_tees_17","product_name":"Organic cotton crew tee","category_id":"cat_tees","brand_id":"brn_northwind","price":19.0,"member_price":null,"stock":76,"availability":"in_stock","cost":8.53},{"product_id":"prd_tees_12","product_name":"Slub cotton V-neck tee","category_id":"cat_tees","brand_id":"brn_northwind","price":49.0,"member_price":null,"stock"… (+277자) ``
14. 모델 → **`facade_get_prd_dtl_info_v2`** `` {"product_id":"prd_tees_18"} ``
   ← 결과 2,141B: `` {"status":"succeeded","data":{"product_id":"prd_tees_18","product_name":"Organic cotton raglan tee","category_id":"cat_tees","brand_id":"brn_ridgeline","price":39.0,"member_price":null,"stock":24,"availability":"in_stock","cost":14.54,"approval_status":"active","variants":[{"variant_id":"var_tees_18_xs_black","color":"Black","size":"XS","stock":3,"availability":"in_stock"},{"variant_id":"var_tees_18_s_black","color":"Black","size":"S","stock":3,"availability":"in_stock"},{"variant_id":"var_tees_18_m_black","color":"Black","size":"M","stock":1,"availability":"in_stock"},{"variant_id":"var_tees_… (+900자) ``
15. 모델 → **`facade_get_prd_dtl_info_v2`** `` {"product_id":"prd_tees_19"} ``
   ← 결과 2,163B: `` {"status":"succeeded","data":{"product_id":"prd_tees_19","product_name":"Linen blend pocket tee","category_id":"cat_tees","brand_id":"brn_northwind","price":19.0,"member_price":null,"stock":30,"availability":"in_stock","cost":8.17,"approval_status":"active","variants":[{"variant_id":"var_tees_19_xs_clay","color":"Clay","size":"XS","stock":4,"availability":"in_stock"},{"variant_id":"var_tees_19_s_clay","color":"Clay","size":"S","stock":2,"availability":"in_stock"},{"variant_id":"var_tees_19_m_clay","color":"Clay","size":"M","stock":3,"availability":"in_stock"},{"variant_id":"var_tees_19_l_clay"… (+900자) ``
16. 모델 → **`facade_get_prd_dtl_info_v2`** `` {"product_id":"prd_tees_06"} ``
   ← 결과 2,604B: `` {"status":"succeeded","data":{"product_id":"prd_tees_06","product_name":"Jersey boxy tee","category_id":"cat_tees","brand_id":"brn_northwind","price":49.0,"member_price":null,"stock":32,"availability":"in_stock","cost":17.65,"approval_status":"active","variants":[{"variant_id":"var_tees_06_xs_white","color":"White","size":"XS","stock":4,"availability":"in_stock"},{"variant_id":"var_tees_06_s_white","color":"White","size":"S","stock":1,"availability":"in_stock"},{"variant_id":"var_tees_06_m_white","color":"White","size":"M","stock":2,"availability":"in_stock"},{"variant_id":"var_tees_06_l_white… (+900자) ``
17. 모델 → **`facade_get_prd_dtl_info_v2`** `` {"product_id":"prd_tees_01"} ``
   ← 결과 2,148B: `` {"status":"succeeded","data":{"product_id":"prd_tees_01","product_name":"Organic cotton pocket tee","category_id":"cat_tees","brand_id":"brn_northwind","price":49.0,"member_price":null,"stock":32,"availability":"in_stock","cost":20.21,"approval_status":"active","variants":[{"variant_id":"var_tees_01_xs_white","color":"White","size":"XS","stock":5,"availability":"in_stock"},{"variant_id":"var_tees_01_s_white","color":"White","size":"S","stock":5,"availability":"in_stock"},{"variant_id":"var_tees_01_m_white","color":"White","size":"M","stock":2,"availability":"in_stock"},{"variant_id":"var_tees_… (+900자) ``
18. 모델 → **`facade_get_prd_dtl_info_v2`** `` {"product_id":"prd_tees_11"} ``
   ← 결과 2,101B: `` {"status":"succeeded","data":{"product_id":"prd_tees_11","product_name":"Pima cotton henley","category_id":"cat_tees","brand_id":"brn_ridgeline","price":19.0,"member_price":null,"stock":34,"availability":"in_stock","cost":7.25,"approval_status":"active","variants":[{"variant_id":"var_tees_11_xs_sky","color":"Sky","size":"XS","stock":3,"availability":"in_stock"},{"variant_id":"var_tees_11_s_sky","color":"Sky","size":"S","stock":1,"availability":"in_stock"},{"variant_id":"var_tees_11_m_sky","color":"Sky","size":"M","stock":8,"availability":"in_stock"},{"variant_id":"var_tees_11_l_sky","color":"S… (+900자) ``
19. 모델 → **`facade_get_prd_dtl_info_v2`** `` {"product_id":"prd_tees_12"} ``
   ← 결과 2,551B: `` {"status":"succeeded","data":{"product_id":"prd_tees_12","product_name":"Slub cotton V-neck tee","category_id":"cat_tees","brand_id":"brn_northwind","price":49.0,"member_price":null,"stock":34,"availability":"in_stock","cost":20.85,"approval_status":"active","variants":[{"variant_id":"var_tees_12_xs_stone","color":"Stone","size":"XS","stock":1,"availability":"in_stock"},{"variant_id":"var_tees_12_s_stone","color":"Stone","size":"S","stock":1,"availability":"in_stock"},{"variant_id":"var_tees_12_m_stone","color":"Stone","size":"M","stock":7,"availability":"in_stock"},{"variant_id":"var_tees_12_… (+900자) ``

_(MODEL_CONNECTION_FAILED로 중단)_

**채점**: E MODEL_CONNECTION_FAILED — 빠진 것: fact "25% is over the 20% limit for everyone (the VIP limit of 30%" (25, 20, 30 not shown); fact "the agent offers 20%, or a 25% sale limited to VIP" (20, 25 not shown); HOST:MODEL_CONNECTION_FAILED
