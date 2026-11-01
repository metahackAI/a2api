# md-how-many-left — ours-heldout-1

[← 실행 묶음](README.md) · 세트 `held_out` · a-commerce `7e1557b` · a2api `38d156e`

**과업**

> How many Light rain parka remain in my inventory?

- 필요한 도구: `get_inventory`
- 허용 도구: `search_products`
- 답에 있어야 할 사실: 4 in total: S 2, M 0, L 0, XL 2 (all Stone)
- 답에 있어야 할 사실: S and XL are at their safety stock of 2, so the parka is effectively sold out for new sales planning

### facade-all · 1회차 · ✓ 통과

토큰 27,714 · 26.949초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 4,648토큰

준비: 전략 `None`, 함수 19개

**질문 1**
> How many Light rain parka remain in my inventory?

1. 모델 → **`getPrdGridListCnt`** `` {"srchKwd":"Light rain parka","pageNo":0,"pageSize":10} ``
   ← 결과 36B: `` {"status":200,"body":{"totCnt":120}} ``
2. 모델 → **`getPrdGridList`** `` {"srchKwd":"Light rain parka","pageNo":0,"pageSize":10} ``
   ← 결과 121B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null}}} ``
3. 모델 → **`getPrdGridList`** `` {"srchKwd":"Light rain parka","pageNo":1,"pageSize":10} ``
   ← 결과 1,937B: `` {"status":200,"body":{"list":[{"prdNo":"prd_rain_parka","prdNm":"Light rain parka","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":118.0,"mbrPrc":null,"stkQty":4,"sellStatCd":"10","costPrc":50.0},{"prdNo":"prd_outerwear_06","prdNm":"Recycled nylon trench coat","ctgNo":"cat_outerwear","brndNo":"brn_northwind","salePrc":259.0,"mbrPrc":null,"stkQty":69,"sellStatCd":"10","costPrc":115.38},{"prdNo":"prd_outerwear_01","prdNm":"Waxed cotton duffle coat","ctgNo":"cat_outerwear","brndNo":"brn_ridgeline","salePrc":289.0,"mbrPrc":null,"stkQty":24,"sellStatCd":"10","costPrc":134.5},{"prd… (+900자) ``
4. 모델 → **`getPrdDtlInfoV2`** `` {"prdNo":"prd_rain_parka"} ``
   ← 결과 980B: `` {"status":200,"body":{"prdNo":"prd_rain_parka","prdNm":"Light rain parka","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":118.0,"mbrPrc":null,"stkQty":4,"sellStatCd":"10","costPrc":50.0,"prdStatCd":"active","optList":[{"optNo":"var_rain_parka_s_stone","optVal1":"Stone","optVal2":"S","stkQty":2,"sellStatCd":"10"},{"optNo":"var_rain_parka_m_stone","optVal1":"Stone","optVal2":"M","stkQty":0,"sellStatCd":"20"},{"optNo":"var_rain_parka_l_stone","optVal1":"Stone","optVal2":"L","stkQty":0,"sellStatCd":"20"},{"optNo":"var_rain_parka_xl_stone","optVal1":"Stone","optVal2":"XL","stkQty"… (+380자) ``

**답변 1**
> The Light rain parka (prd_rain_parka) is active with a total on-hand stock of **4 units**.
>
> Breakdown by option:
> * var_rain_parka_s_stone – Stone / S – stkQty 2 – sellStatCd 10
> * var_rain_parka_m_stone – Stone / M – stkQty 0 – sellStatCd 20
> * var_rain_parka_l_stone – Stone / L – stkQty 0 – sellStatCd 20
> * var_rain_parka_xl_stone – Stone / XL – stkQty 2 – sellStatCd 10
>
> Sale price $118.00, cost $50.00, sell status 10.

**채점**: ✓ 통과

### facade-all · 2회차 · ✓ 통과

토큰 22,073 · 18.145초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 4,648토큰

준비: 전략 `None`, 함수 19개

**질문 1**
> How many Light rain parka remain in my inventory?

1. 모델 → **`getPrdGridList`** `` {"srchKwd":"Light rain parka","pageNo":0,"pageSize":10} ``
   ← 결과 121B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null}}} ``
2. 모델 → **`getPrdGridList`** `` {"srchKwd":"Light rain parka","pageNo":1,"pageSize":10} ``
   ← 결과 1,937B: `` {"status":200,"body":{"list":[{"prdNo":"prd_rain_parka","prdNm":"Light rain parka","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":118.0,"mbrPrc":null,"stkQty":4,"sellStatCd":"10","costPrc":50.0},{"prdNo":"prd_outerwear_06","prdNm":"Recycled nylon trench coat","ctgNo":"cat_outerwear","brndNo":"brn_northwind","salePrc":259.0,"mbrPrc":null,"stkQty":69,"sellStatCd":"10","costPrc":115.38},{"prdNo":"prd_outerwear_01","prdNm":"Waxed cotton duffle coat","ctgNo":"cat_outerwear","brndNo":"brn_ridgeline","salePrc":289.0,"mbrPrc":null,"stkQty":24,"sellStatCd":"10","costPrc":134.5},{"prd… (+900자) ``
3. 모델 → **`getPrdDtlInfoV2`** `` {"prdNo":"prd_rain_parka"} ``
   ← 결과 980B: `` {"status":200,"body":{"prdNo":"prd_rain_parka","prdNm":"Light rain parka","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":118.0,"mbrPrc":null,"stkQty":4,"sellStatCd":"10","costPrc":50.0,"prdStatCd":"active","optList":[{"optNo":"var_rain_parka_s_stone","optVal1":"Stone","optVal2":"S","stkQty":2,"sellStatCd":"10"},{"optNo":"var_rain_parka_m_stone","optVal1":"Stone","optVal2":"M","stkQty":0,"sellStatCd":"20"},{"optNo":"var_rain_parka_l_stone","optVal1":"Stone","optVal2":"L","stkQty":0,"sellStatCd":"20"},{"optNo":"var_rain_parka_xl_stone","optVal1":"Stone","optVal2":"XL","stkQty"… (+380자) ``

**답변 1**
> Light rain parka – prd_rain_parka
>
> * Total on-hand stock: **4 units**
> * Sell status: 10 – on sale, $118.00
>
> Variant breakdown:
> * var_rain_parka_s_stone – Stone / S – stkQty 2 – sellStatCd 10
> * var_rain_parka_m_stone – Stone / M – stkQty 0 – sellStatCd 20
> * var_rain_parka_l_stone – Stone / L – stkQty 0 – sellStatCd 20
> * var_rain_parka_xl_stone – Stone / XL – stkQty 2 – sellStatCd 10
>
> So you have 2 × S Stone and 2 × XL Stone in inventory; M and L Stone are out of stock.

**채점**: ✓ 통과

### acom-all · 1회차 · E CONTEXT_OVERFLOW

토큰 0 · 0.468초 · 모델 호출 0회 · 도구 호출 0회

준비: 전략 `None`, 함수 253개

**질문 1**
> How many Light rain parka remain in my inventory?


_(CONTEXT_OVERFLOW로 중단)_

**채점**: E CONTEXT_OVERFLOW — 빠진 것: tool get_inventory; fact "4 in total: S 2, M 0, L 0, XL 2 (all Stone)" (4, 2, 0, 0, 2 not shown); fact "S and XL are at their safety stock of 2, so the parka is eff" (2 not shown); HOST:CONTEXT_OVERFLOW
(도구 정밀도 —, 재현율 0.00)

### acom-all · 2회차 · E CONTEXT_OVERFLOW

토큰 0 · 0.459초 · 모델 호출 0회 · 도구 호출 0회

준비: 전략 `None`, 함수 253개

**질문 1**
> How many Light rain parka remain in my inventory?


_(CONTEXT_OVERFLOW로 중단)_

**채점**: E CONTEXT_OVERFLOW — 빠진 것: tool get_inventory; fact "4 in total: S 2, M 0, L 0, XL 2 (all Stone)" (4, 2, 0, 0, 2 not shown); fact "S and XL are at their safety stock of 2, so the parka is eff" (2 not shown); HOST:CONTEXT_OVERFLOW
(도구 정밀도 —, 재현율 0.00)

### a2api-acom · 1회차 · ✗ 실패

토큰 14,341 · 12.519초 · 모델 호출 3회 · 도구 호출 4회 · 첫 요청 프롬프트 2,055토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> How many Light rain parka remain in my inventory?

1. 모델 → **`a2api_search`** `` {"query":"inventory product stock remaining"} ``
   ← 결과 375B: `` {"selected":[{"name":"acom_get_inventory","id":"acom.get_inventory"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_get_product_group","id":"acom.get_product_group"},{"name":"acom_update_product","id":"acom.update_product"},{"name":"acom_get_product","id":"acom.get_product"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"product inventory count"} ``
   ← 결과 447B: `` {"selected":[{"name":"acom_get_inventory","id":"acom.get_inventory"},{"name":"acom_get_review_summary","id":"acom.get_review_summary"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_generate_image","id":"acom.generate_image"},{"name":"acom_get_customer_overview","id":"acom.get_customer_overview"}],"evicted":["acom_get_category","acom_get_tenant"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`a2api_search`** `` {"query":"Light rain parka product"} ``
   ← 결과 649B: `` {"selected":[{"name":"acom_compare_products","id":"acom.compare_products"},{"name":"acom_reject_product","id":"acom.reject_product"},{"name":"acom_create_product","id":"acom.create_product"},{"name":"acom_discontinue_product","id":"acom.discontinue_product"},{"name":"acom_search_product_groups","id":"acom.search_product_groups"}],"evicted":["acom_list_orgs","acom_get_campaign","acom_get_coupon","acom_get_promotion","acom_list_policies","acom_get_index_status","acom_get_product_group","acom_update_product","acom_get_product","acom_get_inventory","acom_get_review_summary"],"moreAvailable":true,"… (+49자) ``
4. 모델 → **`acom_search_products`** `` {"query":"Light rain parka"} ``
   ← 결과 2,692B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/parka-stone.svg","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_stock"},{"variant… (+900자) ``

**답변 1**
> The Light rain parka — `prd_rain_parka` — has 4 units in stock total.
>
> * var_rain_parka_s_stone  SKU rp-stone-s  Size S / Stone: 2 in stock
> * var_rain_parka_m_stone  SKU rp-stone-m  Size M / Stone: 0 — out of stock
> * var_rain_parka_l_stone  SKU rp-stone-l  Size L / Stone: 0 — out of stock
> * var_rain_parka_xl_stone SKU rp-stone-xl Size XL / Stone: 2 in stock
>
> Product-level inventory_level = 4, availability in_stock.

**채점**: ✗ 실패 — 빠진 것: tool get_inventory
(도구 정밀도 1.00, 재현율 0.00)

### a2api-acom · 2회차 · ✓ 통과

토큰 20,340 · 16.882초 · 모델 호출 4회 · 도구 호출 5회 · 첫 요청 프롬프트 2,055토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> How many Light rain parka remain in my inventory?

1. 모델 → **`a2api_search`** `` {"query":"inventory product stock count"} ``
   ← 결과 375B: `` {"selected":[{"name":"acom_get_inventory","id":"acom.get_inventory"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_get_product_group","id":"acom.get_product_group"},{"name":"acom_update_product","id":"acom.update_product"},{"name":"acom_get_product","id":"acom.get_product"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"product inventory remaining"} ``
   ← 결과 452B: `` {"selected":[{"name":"acom_get_inventory","id":"acom.get_inventory"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_reject_product","id":"acom.reject_product"},{"name":"acom_create_product","id":"acom.create_product"},{"name":"acom_discontinue_product","id":"acom.discontinue_product"}],"evicted":["acom_get_category","acom_get_tenant","acom_list_orgs"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`a2api_search`** `` {"query":"Light rain parka product"} ``
   ← 결과 566B: `` {"selected":[{"name":"acom_compare_products","id":"acom.compare_products"},{"name":"acom_reject_product","id":"acom.reject_product"},{"name":"acom_create_product","id":"acom.create_product"},{"name":"acom_discontinue_product","id":"acom.discontinue_product"},{"name":"acom_search_product_groups","id":"acom.search_product_groups"}],"evicted":["acom_get_campaign","acom_get_coupon","acom_get_promotion","acom_list_policies","acom_get_index_status","acom_get_product_group","acom_update_product"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`acom_search_products`** `` {"query":"Light rain parka"} ``
   ← 결과 2,692B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/parka-stone.svg","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_stock"},{"variant… (+900자) ``
5. 모델 → **`acom_get_inventory`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 893B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","inventory_level":4,"availability":"in_stock","variants":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"acom:safety_stock":2,"acom:managed":true,"availability":"out_of_stock","on_order":0},{"variant_id":"var_rain_parka_l_stone","sku":"rp-stone-l","size":"L","color":"Stone","inventory_level":0… (+293자) ``

**답변 1**
> Light rain parka — **prd_rain_parka**
>
> * Total sellable stock: **4 units**
> * Availability: in_stock
>
> Variant breakdown:
> * var_rain_parka_s_stone — S / Stone — 2 in stock, safety stock 2
> * var_rain_parka_m_stone — M / Stone — 0 in stock, out_of_stock
> * var_rain_parka_l_stone — L / Stone — 0 in stock, out_of_stock
> * var_rain_parka_xl_stone — XL / Stone — 2 in stock, safety stock 2
>
> So 2 × S and 2 × XL remain; M and L are currently out of stock.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-facade · 1회차 · ✗ 실패

토큰 23,902 · 48.234초 · 모델 호출 6회 · 도구 호출 5회 · 첫 요청 프롬프트 1,366토큰

준비: 전략 `search`, 함수 3개

**질문 1**
> How many Light rain parka remain in my inventory?

1. 모델 → **`facade_get_prd_grid_list_cnt`** `` {"keyword":"Light rain parka"} ``
   ← 결과 43B: `` {"status":"succeeded","data":{"total":120}} ``
2. 모델 → **`facade_get_prd_grid_list`** `` {"keyword":"Light rain parka","page":1,"page_size":100} ``
   ← 결과 5,543B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_rain_parka","product_name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":118.0,"member_price":null,"stock":4,"availability":"in_stock","cost":50.0},{"product_id":"prd_outerwear_06","product_name":"Recycled nylon trench coat","category_id":"cat_outerwear","brand_id":"brn_northwind","price":259.0,"member_price":null,"stock":69,"availability":"in_stock","cost":115.38},{"product_id":"prd_outerwear_01","product_name":"Waxed cotton duffle coat","category_id":"cat_outerwear","brand_id":"brn_ridgeline… (+900자) ``
3. 모델 → **`facade_get_prd_grid_list`** `` {"keyword":"Light rain parka","page":2,"page_size":100} ``
   ← 결과 4,189B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_shoes_06","product_name":"Canvas derby shoes","category_id":"cat_shoes","brand_id":"brn_northwind","price":219.0,"member_price":null,"stock":57,"availability":"in_stock","cost":88.15},{"product_id":"prd_dresses_02","product_name":"Silk blend tiered dress","category_id":"cat_dresses","brand_id":"brn_northwind","price":139.0,"member_price":null,"stock":17,"availability":"in_stock","cost":56.91},{"product_id":"prd_skirts_09","product_name":"Satin mini skirt","category_id":"cat_skirts","brand_id":"brn_northwind","price":119.0,"member_price":… (+900자) ``
4. 모델 → **`facade_get_prd_grid_list_cnt`** `` {"keyword":"prd_rain_parka"} ``
   ← 결과 42B: `` {"status":"succeeded","data":{"total":90}} ``
5. 모델 → **`facade_get_prd_grid_list`** `` {"keyword":"prd_rain_parka","page":1,"page_size":100} ``
   ← 결과 4,851B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_rain_parka","product_name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":118.0,"member_price":null,"stock":4,"availability":"in_stock","cost":50.0},{"product_id":"prd_outerwear_06","product_name":"Recycled nylon trench coat","category_id":"cat_outerwear","brand_id":"brn_northwind","price":259.0,"member_price":null,"stock":69,"availability":"in_stock","cost":115.38},{"product_id":"prd_outerwear_01","product_name":"Waxed cotton duffle coat","category_id":"cat_outerwear","brand_id":"brn_ridgeline… (+900자) ``

**답변 1**
> The Light rain parka in your inventory is:
>
> * **Product ID:** prd_rain_parka
> * **Product name:** Light rain parka
> * **Category:** cat_summer_outerwear
> * **Availability:** in_stock
> * **Stock on hand:** **4 units**
> * Price: $118.00
>
> That is the current stock for prd_rain_parka.

**채점**: ✗ 실패 — 빠진 것: fact "4 in total: S 2, M 0, L 0, XL 2 (all Stone)" (2, 0, 0, 2 not shown); fact "S and XL are at their safety stock of 2, so the parka is eff" (2 not shown)

### a2api-facade · 2회차 · ✓ 통과

토큰 15,722 · 37.56초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 1,366토큰

준비: 전략 `search`, 함수 3개

**질문 1**
> How many Light rain parka remain in my inventory?

1. 모델 → **`facade_get_prd_grid_list_cnt`** `` {"keyword":"Light rain parka"} ``
   ← 결과 43B: `` {"status":"succeeded","data":{"total":120}} ``
2. 모델 → **`facade_get_prd_grid_list`** `` {"keyword":"Light rain parka","page":1,"page_size":20} ``
   ← 결과 4,374B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_rain_parka","product_name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":118.0,"member_price":null,"stock":4,"availability":"in_stock","cost":50.0},{"product_id":"prd_outerwear_06","product_name":"Recycled nylon trench coat","category_id":"cat_outerwear","brand_id":"brn_northwind","price":259.0,"member_price":null,"stock":69,"availability":"in_stock","cost":115.38},{"product_id":"prd_outerwear_01","product_name":"Waxed cotton duffle coat","category_id":"cat_outerwear","brand_id":"brn_ridgeline… (+900자) ``
3. 모델 → **`a2api_search`** `` {"query":"product stock inventory"} ``
   ← 결과 430B: `` {"selected":[{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_get_prd_dtl_info","id":"facade.get_prd_dtl_info"},{"name":"facade_get_prd_dtl_info_v2","id":"facade.get_prd_dtl_info_v2"},{"name":"facade_get_prd_grid_list_cnt","id":"facade.get_prd_grid_list_cnt"},{"name":"facade_save_prmt_list","id":"facade.save_prmt_list"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`facade_get_prd_dtl_info_v2`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 1,055B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","product_name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":118.0,"member_price":null,"stock":4,"availability":"in_stock","cost":50.0,"approval_status":"active","variants":[{"variant_id":"var_rain_parka_s_stone","color":"Stone","size":"S","stock":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","color":"Stone","size":"M","stock":0,"availability":"out_of_stock"},{"variant_id":"var_rain_parka_l_stone","color":"Stone","size":"L","stock":0,"availability":"out_of_stock"},{"va… (+455자) ``

**답변 1**
> The product **Light rain parka – prd_rain_parka** is active and in stock.
>
> * Total on-hand stock: **4 units**
> * Availability by variant:
>   * Stone / S – var_rain_parka_s_stone: 2 in stock, in_stock
>   * Stone / M – var_rain_parka_m_stone: 0 in stock, out_of_stock
>   * Stone / L – var_rain_parka_l_stone: 0 in stock, out_of_stock
>   * Stone / XL – var_rain_parka_xl_stone: 2 in stock, in_stock
>
> Price $118.00, cost $50.00, availability in_stock.

**채점**: ✓ 통과
