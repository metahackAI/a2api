# md-low-stock-before-weekend — ours-design-1

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `a2c7201`

**과업**

> what's about to sell out? anything I need to reorder before the weekend

- 필요한 도구: `search_products`
- 허용 도구: `get_inventory`, `list_tasks`, `get_task`
- 답에 있어야 할 사실: Light rain parka has 4 units left and Cotton chore coat has 7, the two lowest in the store
- 답에 있어야 할 사실: Linen shirt is the one with a reorder task: it sells out in about 4 days (task_linen_reorder, needs you)
- 부르면 안 됨: set_variant_stock

### facade-all · 1회차 · ✓ 통과

토큰 21,468 · 27.335초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 4,652토큰

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

토큰 0 · 0.294초 · 모델 호출 0회 · 도구 호출 0회

준비: 전략 `None`, 함수 253개

**질문 1**
> what's about to sell out? anything I need to reorder before the weekend


_(CONTEXT_OVERFLOW로 중단)_

**채점**: E CONTEXT_OVERFLOW — 빠진 것: tool search_products; fact "Light rain parka has 4 units left and Cotton chore coat has " (4, 7 not shown); fact "Linen shirt is the one with a reorder task: it sells out in " (4 not shown); HOST:CONTEXT_OVERFLOW
(도구 정밀도 —, 재현율 0.00)

### a2api-acom · 1회차 · ✗ 실패

토큰 20,737 · 33.933초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 3,736토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> what's about to sell out? anything I need to reorder before the weekend

1. 모델 → **`acom_list_tasks`** `` {"state":["needs_you","working"],"limit":100} ``
   ← 결과 1,075B: `` {"status":"succeeded","data":{"items":[{"id":"task_linen_reorder","title":"Linen shirt sells out in about 4 days","state":"needs_you","origin":"agent_noticed","at":"2026-11-06T08:40:00-05:00","summary":"Reorder draft: 3 sizes, 240 units","tag":"inventory","change_set_id":"cs_1041","watcher":"stock_out_forecast","conversation_id":"conv_linen_reorder","updated_at":"2026-11-06T08:40:00-05:00"},{"id":"task_returns_1106","title":"12 return requests over $200 are waiting","state":"working","origin":"agent_noticed","at":"2026-11-06T10:40:00-05:00","summary":"Operations agent is sorting the requests b… (+475자) ``
2. 모델 → **`acom_get_change_set`** `` {"change_set_id":"cs_1041"} ``
   ← 결과 3,467B: `` {"status":"succeeded","data":{"id":"cs_1041","number":1041,"version":1,"state":"waiting_for_approval","title":"Reorder linen shirt: 3 sizes, 240 units","request":{"text":["Linen shirt sells out in about 4 days. Draft a reorder for the sizes that will run out."],"conversation_id":"conv_linen_reorder","requested_by":"sys_watcher"},"interpretation":[{"slot":"products","text":"Linen shirt, White, S M L","value":{"sizes":["S","M","L"],"product_id":"prd_linen_shirt"}},{"slot":"other","text":"240 units: S 70, M 90, L 80","value":{"quantities":{"L":80,"M":90,"S":70}}}],"items":[{"position":1,"preview_… (+900자) ``
3. 모델 → **`acom_suggest_reorder`** `` {"product_id":"prd_linen_shirt"} ``
   ← 결과 1,473B: `` {"status":"succeeded","data":{"product_id":"prd_linen_shirt","name":"Linen shirt","sales_window":{"valid_from":"2026-10-30","valid_through":"2026-11-05","days":7},"lead_time_days":7,"cover_days":14,"variants":[{"variant_id":"var_linen_shirt_xs_white","size":"XS","color":"White","inventory_level":4,"acom:safety_stock":2,"on_order":0,"units_sold":6,"days_until_stockout":4.7,"order_quantity":16},{"variant_id":"var_linen_shirt_s_white","size":"S","color":"White","inventory_level":9,"acom:safety_stock":2,"on_order":0,"units_sold":16,"days_until_stockout":3.9,"order_quantity":41},{"variant_id":"var_… (+873자) ``

**답변 1**
> The only imminent stock-out on your task list is the Linen shirt, White.
>
> **Forecast**
> * Sales window 2026-10-30 → 2026-11-05, lead time 7 days, cover 14 days
> * Days until stockout at current rate:
>   * XS White var_linen_shirt_xs_white: 4.7 days, inventory 4, suggest order 16
>   * S White var_linen_shirt_s_white: 3.9 days, inventory 9, suggest order 41
>   * M White var_linen_shirt_m_white: 3.7 days, inventory 10, suggest order 49
>   * L White var_linen_shirt_l_white: 4.5 days, inventory 9, suggest order 35
>   * XL White var_linen_shirt_xl_white: 7.0 days, inventory 6, suggest order 14
> * Suggest reorder total: 155 units
>
> **Draft waiting for your approval**
> Task task_linen_reorder → change set cs_1041 #1041, waiting_for_approval
> * Title: Reorder linen shirt: 3 sizes, 240 units
> * Product: prd_linen_shirt Linen shirt, White S M L
> * Lines in draft:
>   * var_linen_shirt_s_white S 70 units
>   * var_linen_shirt_m_white M 90 units
>   * var_linen_shirt_l_white L 80 units
> * Total units 240, total payment due $6,240.00 USD
> * Expected arrival until 2026-11-13T23:59:00-05:00
> * Approval needed because reorder cost > $1,000.00
> * Undo until 2026-11-07T23:59:00-05:00
>
> The draft covers S/M/L only and is larger than the current suggest_reorder quantities. S and M are the closest to stock-out at ~3.7-3.9 days, so they would be gone before the weekend if sales continue.
>
> Want me to adjust the draft to the suggest quantities or approve the 240-unit draft as-is?

**채점**: ✗ 실패 — 빠진 것: tool search_products
(도구 정밀도 0.33, 재현율 0.00)

### a2api-facade · 1회차 · E MODEL_CALL_LIMIT

토큰 42,077 · 38.947초 · 모델 호출 12회 · 도구 호출 14회 · 첫 요청 프롬프트 992토큰

준비: 전략 `search`, 함수 3개

**질문 1**
> what's about to sell out? anything I need to reorder before the weekend

1. 모델 → **`a2api_search`** `` {"query":"sell out low stock inventory reorder"} ``
   ← 결과 368B: `` {"selected":[{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_get_prd_dtl_info","id":"facade.get_prd_dtl_info"},{"name":"facade_get_prd_dtl_info_v2","id":"facade.get_prd_dtl_info_v2"},{"name":"facade_get_prd_grid_list_cnt","id":"facade.get_prd_grid_list_cnt"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"products about to sell out stock level"} ``
   ← 결과 437B: `` {"selected":[{"name":"facade_get_prd_dtl_info","id":"facade.get_prd_dtl_info"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_get_prd_dtl_info_v2","id":"facade.get_prd_dtl_info_v2"},{"name":"facade_get_prd_grid_list_cnt","id":"facade.get_prd_grid_list_cnt"},{"name":"facade_save_cust_msg_send","id":"facade.save_cust_msg_send"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`a2api_search`** `` {"query":"inventory low stock alert"} ``
   ← 결과 368B: `` {"selected":[{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_get_prd_dtl_info","id":"facade.get_prd_dtl_info"},{"name":"facade_get_prd_dtl_info_v2","id":"facade.get_prd_dtl_info_v2"},{"name":"facade_get_prd_grid_list_cnt","id":"facade.get_prd_grid_list_cnt"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`facade_get_prd_grid_list_cnt`** `` {"availability":"in_stock","min_stock":0,"max_stock":5} ``
   ← 결과 41B: `` {"status":"succeeded","data":{"total":1}} ``
5. 모델 → **`facade_get_prd_grid_list`** `` {"availability":"in_stock","min_stock":0,"max_stock":5,"page":0,"page_size":20} ``
   ← 실패 237B: `` {"status":"failed","error":{"code":"UPSTREAM_VALIDATION_FAILED","detail":"The backend rejected the request values. (HTTP 422) Invalid paging."},"hint":"The service rejected these values. Correct them only if the user gave other values."} ``
6. 모델 → **`facade_get_prd_grid_list`** `` {"availability":"in_stock","min_stock":0,"max_stock":5,"page":1,"page_size":20} ``
   ← 결과 276B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_rain_parka","product_name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":118.0,"member_price":null,"stock":4,"availability":"in_stock","cost":50.0}],"page":1,"page_size":20}} ``
7. 모델 → **`facade_get_prd_grid_list_cnt`** `` {"availability":"in_stock","min_stock":6,"max_stock":10} ``
   ← 결과 41B: `` {"status":"succeeded","data":{"total":5}} ``
8. 모델 → **`facade_get_prd_grid_list`** `` {"availability":"in_stock","min_stock":6,"max_stock":10,"page":1,"page_size":20} ``
   ← 결과 1,107B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_chore_coat","product_name":"Cotton chore coat","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":142.0,"member_price":null,"stock":7,"availability":"in_stock","cost":60.0},{"product_id":"prd_knitwear_19","product_name":"Cashmere blend knit vest","category_id":"cat_knitwear","brand_id":"brn_northwind","price":199.0,"member_price":169.15,"stock":10,"availability":"in_stock","cost":83.04},{"product_id":"prd_belts_01","product_name":"Canvas belt","category_id":"cat_belts","brand_id":"brn_northwind","price":69.0,"member_… (+507자) ``
9. 모델 → **`facade_get_prd_dtl_info_v2`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 1,055B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","product_name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":118.0,"member_price":null,"stock":4,"availability":"in_stock","cost":50.0,"approval_status":"active","variants":[{"variant_id":"var_rain_parka_s_stone","color":"Stone","size":"S","stock":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","color":"Stone","size":"M","stock":0,"availability":"out_of_stock"},{"variant_id":"var_rain_parka_l_stone","color":"Stone","size":"L","stock":0,"availability":"out_of_stock"},{"va… (+455자) ``
10. 모델 → **`facade_get_prd_grid_list_cnt`** `` {"availability":"in_stock","min_stock":11,"max_stock":15} ``
   ← 결과 42B: `` {"status":"succeeded","data":{"total":22}} ``
11. 모델 → **`facade_get_prd_grid_list_cnt`** `` {"availability":"out_of_stock"} ``
   ← 결과 41B: `` {"status":"succeeded","data":{"total":0}} ``
12. 모델 → **`facade_get_prd_grid_list_cnt`** `` {"availability":"back_order"} ``
   ← 결과 41B: `` {"status":"succeeded","data":{"total":0}} ``
13. 모델 → **`facade_get_prd_grid_list_cnt`** `` {"availability":"pre_order"} ``
   ← 결과 41B: `` {"status":"succeeded","data":{"total":0}} ``
14. 모델 → **`facade_get_prd_grid_list_cnt`** `` {"availability":"discontinued"} ``
   ← 결과 41B: `` {"status":"succeeded","data":{"total":0}} ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "Light rain parka has 4 units left and Cotton chore coat has " (4, 7 not shown); fact "Linen shirt is the one with a reorder task: it sells out in " (4 not shown); HOST:MODEL_CALL_LIMIT
