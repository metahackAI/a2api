# md-low-stock-before-weekend — ours-design-3

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `92408c7`

**과업**

> what's about to sell out? anything I need to reorder before the weekend

- 필요한 도구: `search_products`
- 허용 도구: `get_inventory`, `list_tasks`, `get_task`
- 답에 있어야 할 사실: Light rain parka has 4 units left and Cotton chore coat has 7, the two lowest in the store
- 답에 있어야 할 사실: Linen shirt is the one with a reorder task: it sells out in about 4 days (task_linen_reorder, needs you)
- 부르면 안 됨: set_variant_stock

### facade-all · 1회차 · ✓ 통과

토큰 21,468 · 27.615초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 4,652토큰

준비: 전략 `None`, 함수 19개

**질문 1**
> what's about to sell out? anything I need to reorder before the weekend

1. 모델 → **`getPrdGridListCnt`** `` {"stkQtyFrom":0,"stkQtyTo":10,"pageNo":0,"pageSize":20} ``
   ← 결과 34B: `` {"status":200,"body":{"totCnt":6}} ``
2. 모델 → **`getPrdGridList`** `` {"stkQtyFrom":0,"stkQtyTo":10,"pageNo":0,"pageSize":20} ``
   ← 결과 121B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null}}} ``
3. 모델 → **`getPrdGridList`** `` {"stkQtyFrom":0,"stkQtyTo":10,"pageNo":1,"pageSize":20} ``
   ← 결과 1,144B: `` {"status":200,"body":{"list":[{"prdNo":"prd_chore_coat","prdNm":"Cotton chore coat","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":142.0,"mbrPrc":null,"stkQty":7,"sellStatCd":"10","costPrc":60.0},{"prdNo":"prd_knitwear_19","prdNm":"Cashmere blend knit vest","ctgNo":"cat_knitwear","brndNo":"brn_northwind","salePrc":199.0,"mbrPrc":169.15,"stkQty":10,"sellStatCd":"10","costPrc":83.04},{"prdNo":"prd_rain_parka","prdNm":"Light rain parka","ctgNo":"cat_summer_outerwear","brndNo":"brn_northwind","salePrc":118.0,"mbrPrc":null,"stkQty":4,"sellStatCd":"10","costPrc":50.0},{"prdNo":"pr… (+544자) ``

**답변 1**
> There are 6 SKUs currently at low stock (0-10 units). From the current grid:
>
> * **prd_rain_parka – Light rain parka** – cat_summer_outerwear – Stock: 4 – Sale $118.00
> * **prd_chore_coat – Cotton chore coat** – cat_summer_outerwear – Stock: 7 – Sale $142.00
> * **prd_knitwear_19 – Cashmere blend knit vest** – cat_knitwear – Stock: 10 – Sale $199.00 / Mbr $169.15
> * **prd_belts_01 – Canvas belt** – cat_belts – Stock: 10 – Sale $69.00
> * **prd_knitwear_24 – Ribbed cotton cardigan** – cat_knitwear – Stock: 10 – Sale $139.00 / Mbr $118.15
> * **prd_skirts_01 – Satin slip skirt** – cat_skirts – Stock: 10 – Sale $129.00
>
> Lowest risk before the weekend is the Light rain parka at 4 units, followed by Cotton chore coat at 7 units. The other 4 items are sitting at the 10-unit threshold.
>
> Want me to pull recent sales velocity for these SKUs to estimate days-to-stockout?

**채점**: ✓ 통과

### acom-all · 1회차 · E CONTEXT_OVERFLOW

토큰 0 · 0.299초 · 모델 호출 0회 · 도구 호출 0회

준비: 전략 `None`, 함수 253개

**질문 1**
> what's about to sell out? anything I need to reorder before the weekend


_(CONTEXT_OVERFLOW로 중단)_

**채점**: E CONTEXT_OVERFLOW — 빠진 것: tool search_products; fact "Light rain parka has 4 units left and Cotton chore coat has " (4, 7 not shown); fact "Linen shirt is the one with a reorder task: it sells out in " (4 not shown); HOST:CONTEXT_OVERFLOW
(도구 정밀도 —, 재현율 0.00)

### a2api-acom · 1회차 · ✓ 통과

토큰 76,098 · 54.361초 · 모델 호출 9회 · 도구 호출 9회 · 첫 요청 프롬프트 3,736토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> what's about to sell out? anything I need to reorder before the weekend

1. 모델 → **`acom_list_tasks`** `` {"state":["needs_you","working"],"limit":100} ``
   ← 결과 1,075B: `` {"status":"succeeded","data":{"items":[{"id":"task_linen_reorder","title":"Linen shirt sells out in about 4 days","state":"needs_you","origin":"agent_noticed","at":"2026-11-06T08:40:00-05:00","summary":"Reorder draft: 3 sizes, 240 units","tag":"inventory","change_set_id":"cs_1041","watcher":"stock_out_forecast","conversation_id":"conv_linen_reorder","updated_at":"2026-11-06T08:40:00-05:00"},{"id":"task_returns_1106","title":"12 return requests over $200 are waiting","state":"working","origin":"agent_noticed","at":"2026-11-06T10:40:00-05:00","summary":"Operations agent is sorting the requests b… (+475자) ``
2. 모델 → **`acom_get_change_set`** `` {"change_set_id":"cs_1041"} ``
   ← 결과 3,467B: `` {"status":"succeeded","data":{"id":"cs_1041","number":1041,"version":1,"state":"waiting_for_approval","title":"Reorder linen shirt: 3 sizes, 240 units","request":{"text":["Linen shirt sells out in about 4 days. Draft a reorder for the sizes that will run out."],"conversation_id":"conv_linen_reorder","requested_by":"sys_watcher"},"interpretation":[{"slot":"products","text":"Linen shirt, White, S M L","value":{"sizes":["S","M","L"],"product_id":"prd_linen_shirt"}},{"slot":"other","text":"240 units: S 70, M 90, L 80","value":{"quantities":{"L":80,"M":90,"S":70}}}],"items":[{"position":1,"preview_… (+900자) ``
3. 모델 → **`a2api_search`** `` {"query":"inventory stock out forecast"} ``
   ← 결과 426B: `` {"selected":[{"name":"acom_set_variant_stock","id":"acom.set_variant_stock"},{"name":"acom_get_inventory","id":"acom.get_inventory"},{"name":"acom_receive_reorder","id":"acom.receive_reorder"},{"name":"acom_cancel_order_lines","id":"acom.cancel_order_lines"},{"name":"acom_search_products","id":"acom.search_products"}],"evicted":["acom_suggest_reorder"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`acom_search_products`** `` {"query":"linen shirt","limit":20} ``
   ← 결과 6,014B: `` {"status":"succeeded","data":{"items":[{"id":"prd_linen_shirt","name":"Linen shirt","category_id":"cat_shirts","brand_id":"brn_northwind","image":"/media/garment/shirt-white.svg","price":68.0,"price_currency":"USD","member_price":null,"cost":26.0,"inventory_level":38,"availability":"in_stock","has_variant":[{"variant_id":"var_linen_shirt_xs_white","sku":"ls-white-xs","size":"XS","color":"White","inventory_level":4,"availability":"in_stock"},{"variant_id":"var_linen_shirt_s_white","sku":"ls-white-s","size":"S","color":"White","inventory_level":9,"availability":"in_stock"},{"variant_id":"var_lin… (+900자) ``
5. 모델 → **`acom_get_inventory`** `` {"product_id":"prd_linen_shirt"} ``
   ← 결과 1,083B: `` {"status":"succeeded","data":{"product_id":"prd_linen_shirt","inventory_level":38,"availability":"in_stock","variants":[{"variant_id":"var_linen_shirt_xs_white","sku":"ls-white-xs","size":"XS","color":"White","inventory_level":4,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_linen_shirt_s_white","sku":"ls-white-s","size":"S","color":"White","inventory_level":9,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_linen_shirt_m_white","sku":"ls-white-m","size":"M","color":"White","inventory_leve… (+483자) ``
6. 모델 → **`acom_search_products`** `` {"max_inventory_level":20,"limit":100,"sort":"inventory_level"} ``
   ← 결과 6,014B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/parka-stone.svg","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_stock"},{"variant… (+900자) ``
7. 모델 → **`acom_get_inventory`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 893B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","inventory_level":4,"availability":"in_stock","variants":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"acom:safety_stock":2,"acom:managed":true,"availability":"out_of_stock","on_order":0},{"variant_id":"var_rain_parka_l_stone","sku":"rp-stone-l","size":"L","color":"Stone","inventory_level":0… (+293자) ``
8. 모델 → **`acom_get_inventory`** `` {"product_id":"prd_chore_coat"} ``
   ← 결과 893B: `` {"status":"succeeded","data":{"product_id":"prd_chore_coat","inventory_level":7,"availability":"in_stock","variants":[{"variant_id":"var_chore_coat_s_olive","sku":"cc-olive-s","size":"S","color":"Olive","inventory_level":3,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_chore_coat_m_olive","sku":"cc-olive-m","size":"M","color":"Olive","inventory_level":0,"acom:safety_stock":2,"acom:managed":true,"availability":"out_of_stock","on_order":0},{"variant_id":"var_chore_coat_l_olive","sku":"cc-olive-l","size":"L","color":"Olive","inventory_level":0… (+293자) ``
9. 모델 → **`acom_search_products`** `` {"max_inventory_level":15,"min_inventory_level":0,"limit":100,"sort":"inventory_level"} ``
   ← 결과 6,014B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/parka-stone.svg","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_stock"},{"variant… (+900자) ``

**답변 1**
> Here’s what’s flagged right now for the weekend:
>
> **Active stock-out watch**
> * **Linen shirt – White, prd_linen_shirt**
>   * Current sellable stock: 38 total
>     * XS White var_linen_shirt_xs_white: 4
>     * S White var_linen_shirt_s_white: 9
>     * M White var_linen_shirt_m_white: 10
>     * L White var_linen_shirt_l_white: 9
>     * XL White var_linen_shirt_xl_white: 6
>   * Safety stock per variant: 2, managed = true
>   * Task `task_linen_reorder` – “Linen shirt sells out in about 4 days”
>   * Draft reorder waiting for approval:
>     * Change set cs_1041 #1041 – “Reorder linen shirt: 3 sizes, 240 units”
>     * State: waiting_for_approval, undo until 2026-11-07T23:59:00-05:00
>     * Lines:
>       * var_linen_shirt_s_white S White – order 70 units
>       * var_linen_shirt_m_white M White – order 90 units
>       * var_linen_shirt_l_white L White – order 80 units
>     * Total units 240, total payment due $6,240.00 USD
>     * Expected arrival until 2026-11-13T23:59:00-05:00
>     * Approval reason: Reorder cost over $1000.00
>   * This is the only stock-out forecast currently in your “needs you” task list.
>
> **Low stock / out-of-stock variants you’ll likely feel before the weekend**
>
> * **Light rain parka, prd_rain_parka – total 4**
>   * var_rain_parka_s_stone S Stone: 2 in stock, safety 2
>   * var_rain_parka_m_stone M Stone: 0 out_of_stock, safety 2
>   * var_rain_parka_l_stone L Stone: 0 out_of_stock, safety 2
>   * var_rain_parka_xl_stone XL Stone: 2 in stock, safety 2
>   * No reorders on order.
>
> * **Cotton chore coat, prd_chore_coat – total 7**
>   * var_chore_coat_s_olive S Olive: 3 in stock, safety 2
>   * var_chore_coat_m_olive M Olive: 0 out_of_stock, safety 2
>   * var_chore_coat_l_olive L Olive: 0 out_of_stock, safety 2
>   * var_chore_coat_xl_olive XL Olive: 4 in stock, safety 2
>   * No reorders on order.
>
> * Other very low totals from the low-stock scan:
>   * Canvas belt prd_belts_01 – total 10, each variant 1-2 units
>   * Cashmere blend knit vest prd_knitwear_19 – total 10, each of 10 variants = 1 … (+324자)

**채점**: ✓ 통과
(도구 정밀도 0.88, 재현율 1.00)

### a2api-facade · 1회차 · ✓ 통과

토큰 37,540 · 61.08초 · 모델 호출 9회 · 도구 호출 14회 · 첫 요청 프롬프트 992토큰

준비: 전략 `search`, 함수 3개

**질문 1**
> what's about to sell out? anything I need to reorder before the weekend

1. 모델 → **`a2api_search`** `` {"query":"sell out low stock inventory reorder"} ``
   ← 결과 368B: `` {"selected":[{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_get_prd_dtl_info","id":"facade.get_prd_dtl_info"},{"name":"facade_get_prd_dtl_info_v2","id":"facade.get_prd_dtl_info_v2"},{"name":"facade_get_prd_grid_list_cnt","id":"facade.get_prd_grid_list_cnt"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"products about to sell out stock level"} ``
   ← 결과 578B: `` {"selected":[{"name":"facade_get_prd_dtl_info","id":"facade.get_prd_dtl_info"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_get_prd_dtl_info_v2","id":"facade.get_prd_dtl_info_v2"},{"name":"facade_get_prd_grid_list_cnt","id":"facade.get_prd_grid_list_cnt"},{"name":"facade_save_cust_msg_send","id":"facade.save_cust_msg_send"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match is already callable. If they cannot answer, tell the user what is missing instead of searching again."} ``
3. 모델 → **`a2api_search`** `` {"query":"inventory low stock alert"} ``
   ← 결과 509B: `` {"selected":[{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_get_prd_dtl_info","id":"facade.get_prd_dtl_info"},{"name":"facade_get_prd_dtl_info_v2","id":"facade.get_prd_dtl_info_v2"},{"name":"facade_get_prd_grid_list_cnt","id":"facade.get_prd_grid_list_cnt"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match is already callable. If they cannot answer, tell the user what is missing instead of searching again."} ``
4. 모델 → **`facade_get_prd_grid_list_cnt`** `` {"availability":"in_stock","min_stock":0,"max_stock":5} ``
   ← 결과 41B: `` {"status":"succeeded","data":{"total":1}} ``
5. 모델 → **`facade_get_prd_grid_list`** `` {"availability":"in_stock","min_stock":0,"max_stock":5,"page":1,"page_size":100} ``
   ← 결과 277B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_rain_parka","product_name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":118.0,"member_price":null,"stock":4,"availability":"in_stock","cost":50.0}],"page":1,"page_size":100}} ``
6. 모델 → **`facade_get_prd_dtl_info_v2`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 1,055B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","product_name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":118.0,"member_price":null,"stock":4,"availability":"in_stock","cost":50.0,"approval_status":"active","variants":[{"variant_id":"var_rain_parka_s_stone","color":"Stone","size":"S","stock":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","color":"Stone","size":"M","stock":0,"availability":"out_of_stock"},{"variant_id":"var_rain_parka_l_stone","color":"Stone","size":"L","stock":0,"availability":"out_of_stock"},{"va… (+455자) ``
7. 모델 → **`facade_get_prd_grid_list_cnt`** `` {"availability":"in_stock","min_stock":0,"max_stock":10} ``
   ← 결과 41B: `` {"status":"succeeded","data":{"total":6}} ``
8. 모델 → **`facade_get_prd_grid_list`** `` {"availability":"in_stock","min_stock":0,"max_stock":10,"page":1,"page_size":100} ``
   ← 결과 1,320B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_chore_coat","product_name":"Cotton chore coat","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":142.0,"member_price":null,"stock":7,"availability":"in_stock","cost":60.0},{"product_id":"prd_knitwear_19","product_name":"Cashmere blend knit vest","category_id":"cat_knitwear","brand_id":"brn_northwind","price":199.0,"member_price":169.15,"stock":10,"availability":"in_stock","cost":83.04},{"product_id":"prd_rain_parka","product_name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","pr… (+720자) ``
9. 모델 → **`facade_get_prd_dtl_info_v2`** `` {"product_id":"prd_chore_coat"} ``
   ← 결과 1,029B: `` {"status":"succeeded","data":{"product_id":"prd_chore_coat","product_name":"Cotton chore coat","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":142.0,"member_price":null,"stock":7,"availability":"in_stock","cost":60.0,"approval_status":"active","variants":[{"variant_id":"var_chore_coat_s_olive","color":"Olive","size":"S","stock":3,"availability":"in_stock"},{"variant_id":"var_chore_coat_m_olive","color":"Olive","size":"M","stock":0,"availability":"out_of_stock"},{"variant_id":"var_chore_coat_l_olive","color":"Olive","size":"L","stock":0,"availability":"out_of_stock"},{"v… (+429자) ``
10. 모델 → **`facade_get_prd_dtl_info_v2`** `` {"product_id":"prd_knitwear_19"} ``
   ← 결과 2,162B: `` {"status":"succeeded","data":{"product_id":"prd_knitwear_19","product_name":"Cashmere blend knit vest","category_id":"cat_knitwear","brand_id":"brn_northwind","price":199.0,"member_price":169.15,"stock":10,"availability":"in_stock","cost":83.04,"approval_status":"active","variants":[{"variant_id":"var_knitwear_19_xs_navy","color":"Navy","size":"XS","stock":1,"availability":"in_stock"},{"variant_id":"var_knitwear_19_s_navy","color":"Navy","size":"S","stock":1,"availability":"in_stock"},{"variant_id":"var_knitwear_19_m_navy","color":"Navy","size":"M","stock":1,"availability":"in_stock"},{"varian… (+900자) ``
11. 모델 → **`facade_get_prd_dtl_info_v2`** `` {"product_id":"prd_belts_01"} ``
   ← 결과 1,811B: `` {"status":"succeeded","data":{"product_id":"prd_belts_01","product_name":"Canvas belt","category_id":"cat_belts","brand_id":"brn_northwind","price":69.0,"member_price":null,"stock":10,"availability":"in_stock","cost":24.38,"approval_status":"active","variants":[{"variant_id":"var_belts_01_s_rust","color":"Rust","size":"S","stock":2,"availability":"in_stock"},{"variant_id":"var_belts_01_m_rust","color":"Rust","size":"M","stock":1,"availability":"in_stock"},{"variant_id":"var_belts_01_l_rust","color":"Rust","size":"L","stock":1,"availability":"in_stock"},{"variant_id":"var_belts_01_s_navy","colo… (+900자) ``
12. 모델 → **`facade_get_prd_dtl_info_v2`** `` {"product_id":"prd_knitwear_24"} ``
   ← 결과 2,222B: `` {"status":"succeeded","data":{"product_id":"prd_knitwear_24","product_name":"Ribbed cotton cardigan","category_id":"cat_knitwear","brand_id":"brn_northwind","price":139.0,"member_price":118.15,"stock":10,"availability":"in_stock","cost":66.21,"approval_status":"active","variants":[{"variant_id":"var_knitwear_24_xs_black","color":"Black","size":"XS","stock":1,"availability":"in_stock"},{"variant_id":"var_knitwear_24_s_black","color":"Black","size":"S","stock":1,"availability":"in_stock"},{"variant_id":"var_knitwear_24_m_black","color":"Black","size":"M","stock":1,"availability":"in_stock"},{"va… (+900자) ``
13. 모델 → **`facade_get_prd_dtl_info_v2`** `` {"product_id":"prd_skirts_01"} ``
   ← 결과 1,991B: `` {"status":"succeeded","data":{"product_id":"prd_skirts_01","product_name":"Satin slip skirt","category_id":"cat_skirts","brand_id":"brn_northwind","price":129.0,"member_price":null,"stock":10,"availability":"in_stock","cost":59.71,"approval_status":"active","variants":[{"variant_id":"var_skirts_01_xs_rust","color":"Rust","size":"XS","stock":1,"availability":"in_stock"},{"variant_id":"var_skirts_01_s_rust","color":"Rust","size":"S","stock":1,"availability":"in_stock"},{"variant_id":"var_skirts_01_m_rust","color":"Rust","size":"M","stock":1,"availability":"in_stock"},{"variant_id":"var_skirts_01… (+900자) ``
14. 모델 → **`facade_get_prd_grid_list_cnt`** `` {"availability":"out_of_stock"} ``
   ← 결과 41B: `` {"status":"succeeded","data":{"total":0}} ``

**답변 1**
> Here’s what’s tight right now, based on current in-stock totals:
>
> **Critical / about to sell out**
>
> * **Light rain parka – prd_rain_parka**
>   * Total stock: 4
>   * Price: $118.00 | Cost: $50.00
>   * Variants:
>     * Stone S – var_rain_parka_s_stone: 2 in stock
>     * Stone XL – var_rain_parka_xl_stone: 2 in stock
>     * Stone M – var_rain_parka_m_stone: 0 – out_of_stock
>     * Stone L – var_rain_parka_l_stone: 0 – out_of_stock
>   * This is the only product with total stock ≤5. M and L are already gone.
>
> **Low stock 6-10 units – watch before the weekend**
>
> * **Cotton chore coat – prd_chore_coat**
>   * Total stock: 7
>   * Price: $142.00 | Cost: $60.00
>   * Variants:
>     * Olive S – var_chore_coat_s_olive: 3
>     * Olive XL – var_chore_coat_xl_olive: 4
>     * Olive M – var_chore_coat_m_olive: 0 – out_of_stock
>     * Olive L – var_chore_coat_l_olive: 0 – out_of_stock
>
> * **Cashmere blend knit vest – prd_knitwear_19**
>   * Total stock: 10
>   * Price: $199.00 | Member price: $169.15 | Cost: $83.04
>   * All 10 variants are at 1 each:
>     * Navy XS/S/M/L/XL – 1 each
>     * Rust XS/S/M/L/XL – 1 each
>
> * **Canvas belt – prd_belts_01**
>   * Total stock: 10
>   * Price: $69.00 | Cost: $24.38
>   * Low points:
>     * Rust S – var_belts_01_s_rust: 2
>     * Rust M – var_belts_01_m_rust: 1
>     * Rust L – var_belts_01_l_rust: 1
>     * Navy S/M/L – 1 each
>     * Olive S/M/L – 1 each
>
> * **Ribbed cotton cardigan – prd_knitwear_24**
>   * Total stock: 10
>   * Price: $139.00 | Member price: $118.15 | Cost: $66.21
>   * All 10 variants at 1 each:
>     * Black XS/S/M/L/XL – 1 each
>     * Slate XS/S/M/L/XL – 1 each
>
> * **Satin slip skirt – prd_skirts_01**
>   * Total stock: 10
>   * Price: $129.00 | Cost: $59.71
>   * All 10 variants at 1 each:
>     * Rust XS/S/M/L/XL – 1 each
>     * White XS/S/M/L/XL – 1 each
>
> Product-level out-of-stock count is 0. The rain parka is the immediate reorder risk with only 4 units left and two sizes already out. The chore coat is next at 7 units with M/L gone, and the four items at 10 units are effectiv… (+137자)

**채점**: ✓ 통과
