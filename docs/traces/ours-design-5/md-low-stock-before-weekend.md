# md-low-stock-before-weekend — ours-design-5

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `d4c6603`

**과업**

> what's about to sell out? anything I need to reorder before the weekend

- 필요한 도구: `search_products`
- 허용 도구: `get_inventory`, `list_tasks`, `get_task`
- 답에 있어야 할 사실: Light rain parka has 4 units left and Cotton chore coat has 7, the two lowest in the store
- 답에 있어야 할 사실: Linen shirt is the one with a reorder task: it sells out in about 4 days (task_linen_reorder, needs you)
- 부르면 안 됨: set_variant_stock

### a2api-acom · 1회차 · E MODEL_CALL_LIMIT

토큰 93,806 · 47.369초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 3,736토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> what's about to sell out? anything I need to reorder before the weekend

1. 모델 → **`acom_list_tasks`** `` {"state":["needs_you","working"]} ``
   ← 결과 1,075B: `` {"status":"succeeded","data":{"items":[{"id":"task_linen_reorder","title":"Linen shirt sells out in about 4 days","state":"needs_you","origin":"agent_noticed","at":"2026-11-06T08:40:00-05:00","summary":"Reorder draft: 3 sizes, 240 units","tag":"inventory","change_set_id":"cs_1041","watcher":"stock_out_forecast","conversation_id":"conv_linen_reorder","updated_at":"2026-11-06T08:40:00-05:00"},{"id":"task_returns_1106","title":"12 return requests over $200 are waiting","state":"working","origin":"agent_noticed","at":"2026-11-06T10:40:00-05:00","summary":"Operations agent is sorting the requests b… (+475자) ``
2. 모델 → **`acom_get_change_set`** `` {"change_set_id":"cs_1041"} ``
   ← 결과 3,467B: `` {"status":"succeeded","data":{"id":"cs_1041","number":1041,"version":1,"state":"waiting_for_approval","title":"Reorder linen shirt: 3 sizes, 240 units","request":{"text":["Linen shirt sells out in about 4 days. Draft a reorder for the sizes that will run out."],"conversation_id":"conv_linen_reorder","requested_by":"sys_watcher"},"interpretation":[{"slot":"products","text":"Linen shirt, White, S M L","value":{"sizes":["S","M","L"],"product_id":"prd_linen_shirt"}},{"slot":"other","text":"240 units: S 70, M 90, L 80","value":{"quantities":{"L":80,"M":90,"S":70}}}],"items":[{"position":1,"preview_… (+900자) ``
3. 모델 → **`a2api_search`** `` {"query":"sell out forecast inventory"} ``
   ← 결과 387B: `` {"selected":[{"name":"acom_set_variant_stock","id":"acom.set_variant_stock"},{"name":"acom_get_inventory","id":"acom.get_inventory"},{"name":"acom_receive_reorder","id":"acom.receive_reorder"},{"name":"acom_cancel_order_lines","id":"acom.cancel_order_lines"},{"name":"acom_update_seller","id":"acom.update_seller"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`a2api_search`** `` {"query":"stock out forecast","more":true} ``
   ← 실패 110B: `` {"status":"failed","error":{"code":"SEARCH_NOT_STARTED","detail":"Search this query before requesting more."}} ``
5. 모델 → **`a2api_search`** `` {"query":"inventory forecast"} ``
   ← 결과 351B: `` {"selected":[{"name":"acom_get_inventory","id":"acom.get_inventory"},{"name":"acom_set_variant_stock","id":"acom.set_variant_stock"},{"name":"acom_search_products","id":"acom.search_products"}],"evicted":["acom_suggest_reorder","acom_list_display_slots","acom_schedule_display"],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true} ``
6. 모델 → **`acom_search_products`** `` {"query":"linen shirt","limit":20} ``
   ← 결과 2,674B: `` {"status":"succeeded","data":{"items":[{"id":"prd_linen_shirt","name":"Linen shirt","category_id":"cat_shirts","brand_id":"brn_northwind","image":"/media/garment/shirt-white.svg","price":68.0,"price_currency":"USD","member_price":null,"cost":26.0,"inventory_level":38,"availability":"in_stock","has_variant":[{"variant_id":"var_linen_shirt_xs_white","sku":"ls-white-xs","size":"XS","color":"White","inventory_level":4,"availability":"in_stock"},{"variant_id":"var_linen_shirt_s_white","sku":"ls-white-s","size":"S","color":"White","inventory_level":9,"availability":"in_stock"},{"variant_id":"var_lin… (+900자) ``
7. 모델 → **`acom_get_inventory`** `` {"product_id":"prd_linen_shirt"} ``
   ← 결과 1,083B: `` {"status":"succeeded","data":{"product_id":"prd_linen_shirt","inventory_level":38,"availability":"in_stock","variants":[{"variant_id":"var_linen_shirt_xs_white","sku":"ls-white-xs","size":"XS","color":"White","inventory_level":4,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_linen_shirt_s_white","sku":"ls-white-s","size":"S","color":"White","inventory_level":9,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_linen_shirt_m_white","sku":"ls-white-m","size":"M","color":"White","inventory_leve… (+483자) ``
8. 모델 → **`acom_search_products`** `` {"max_inventory_level":20,"limit":50} ``
   ← 결과 4,823B: `` {"status":"succeeded","data":{"items":[{"id":"prd_shirts_11","name":"Corduroy band-collar shirt","category_id":"cat_shirts","brand_id":"brn_northwind","image":"/media/garment/shirt-sky.svg","price":79.0,"price_currency":"USD","member_price":null,"cost":35.64,"inventory_level":19,"availability":"in_stock","has_variant":[{"variant_id":"var_shirts_11_xs_slate","sku":"shirts-11-slate-xs","size":"XS","color":"Slate","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_shirts_11_s_slate","sku":"shirts-11-slate-s","size":"S","color":"Slate","inventory_level":3,"availability":"in_stock"},… (+900자) ``
9. 모델 → **`acom_search_products`** `` {"max_inventory_level":10,"limit":100} ``
   ← 결과 3,592B: `` {"status":"succeeded","data":{"items":[{"id":"prd_chore_coat","name":"Cotton chore coat","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/chore-olive.svg","price":142.0,"price_currency":"USD","member_price":null,"cost":60.0,"inventory_level":7,"availability":"in_stock","has_variant":[{"variant_id":"var_chore_coat_s_olive","sku":"cc-olive-s","size":"S","color":"Olive","inventory_level":3,"availability":"in_stock"},{"variant_id":"var_chore_coat_m_olive","sku":"cc-olive-m","size":"M","color":"Olive","inventory_level":0,"availability":"out_of_stock"},{"varian… (+900자) ``
10. 모델 → **`acom_search_products`** `` {"max_inventory_level":5,"limit":100} ``
   ← 결과 876B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/parka-stone.svg","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_stock"},{"variant… (+276자) ``
11. 모델 → **`acom_get_inventory`** `` {"product_id":"prd_chore_coat"} ``
   ← 결과 893B: `` {"status":"succeeded","data":{"product_id":"prd_chore_coat","inventory_level":7,"availability":"in_stock","variants":[{"variant_id":"var_chore_coat_s_olive","sku":"cc-olive-s","size":"S","color":"Olive","inventory_level":3,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_chore_coat_m_olive","sku":"cc-olive-m","size":"M","color":"Olive","inventory_level":0,"acom:safety_stock":2,"acom:managed":true,"availability":"out_of_stock","on_order":0},{"variant_id":"var_chore_coat_l_olive","sku":"cc-olive-l","size":"L","color":"Olive","inventory_level":0… (+293자) ``
12. 모델 → **`acom_get_inventory`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 893B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","inventory_level":4,"availability":"in_stock","variants":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"acom:safety_stock":2,"acom:managed":true,"availability":"out_of_stock","on_order":0},{"variant_id":"var_rain_parka_l_stone","sku":"rp-stone-l","size":"L","color":"Stone","inventory_level":0… (+293자) ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "Light rain parka has 4 units left and Cotton chore coat has " (4, 7 not shown); fact "Linen shirt is the one with a reorder task: it sells out in " (4 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.89, 재현율 1.00)

### a2api-facade · 1회차 · ✓ 통과

토큰 37,471 · 35.006초 · 모델 호출 10회 · 도구 호출 9회 · 첫 요청 프롬프트 992토큰

준비: 전략 `search`, 함수 3개

**질문 1**
> what's about to sell out? anything I need to reorder before the weekend

1. 모델 → **`a2api_search`** `` {"query":"sell out stock inventory low reorder"} ``
   ← 결과 368B: `` {"selected":[{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_get_prd_dtl_info","id":"facade.get_prd_dtl_info"},{"name":"facade_get_prd_dtl_info_v2","id":"facade.get_prd_dtl_info_v2"},{"name":"facade_get_prd_grid_list_cnt","id":"facade.get_prd_grid_list_cnt"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`facade_get_prd_grid_list_cnt`** `` {"availability":"in_stock","max_stock":10} ``
   ← 결과 41B: `` {"status":"succeeded","data":{"total":6}} ``
3. 모델 → **`facade_get_prd_grid_list`** `` {"availability":"in_stock","max_stock":10,"page":1,"page_size":100} ``
   ← 결과 1,320B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_chore_coat","product_name":"Cotton chore coat","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":142.0,"member_price":null,"stock":7,"availability":"in_stock","cost":60.0},{"product_id":"prd_knitwear_19","product_name":"Cashmere blend knit vest","category_id":"cat_knitwear","brand_id":"brn_northwind","price":199.0,"member_price":169.15,"stock":10,"availability":"in_stock","cost":83.04},{"product_id":"prd_rain_parka","product_name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","pr… (+720자) ``
4. 모델 → **`facade_get_prd_dtl_info_v2`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 1,055B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","product_name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":118.0,"member_price":null,"stock":4,"availability":"in_stock","cost":50.0,"approval_status":"active","variants":[{"variant_id":"var_rain_parka_s_stone","color":"Stone","size":"S","stock":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","color":"Stone","size":"M","stock":0,"availability":"out_of_stock"},{"variant_id":"var_rain_parka_l_stone","color":"Stone","size":"L","stock":0,"availability":"out_of_stock"},{"va… (+455자) ``
5. 모델 → **`facade_get_prd_dtl_info_v2`** `` {"product_id":"prd_chore_coat"} ``
   ← 결과 1,029B: `` {"status":"succeeded","data":{"product_id":"prd_chore_coat","product_name":"Cotton chore coat","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":142.0,"member_price":null,"stock":7,"availability":"in_stock","cost":60.0,"approval_status":"active","variants":[{"variant_id":"var_chore_coat_s_olive","color":"Olive","size":"S","stock":3,"availability":"in_stock"},{"variant_id":"var_chore_coat_m_olive","color":"Olive","size":"M","stock":0,"availability":"out_of_stock"},{"variant_id":"var_chore_coat_l_olive","color":"Olive","size":"L","stock":0,"availability":"out_of_stock"},{"v… (+429자) ``
6. 모델 → **`facade_get_prd_dtl_info_v2`** `` {"product_id":"prd_knitwear_19"} ``
   ← 결과 2,162B: `` {"status":"succeeded","data":{"product_id":"prd_knitwear_19","product_name":"Cashmere blend knit vest","category_id":"cat_knitwear","brand_id":"brn_northwind","price":199.0,"member_price":169.15,"stock":10,"availability":"in_stock","cost":83.04,"approval_status":"active","variants":[{"variant_id":"var_knitwear_19_xs_navy","color":"Navy","size":"XS","stock":1,"availability":"in_stock"},{"variant_id":"var_knitwear_19_s_navy","color":"Navy","size":"S","stock":1,"availability":"in_stock"},{"variant_id":"var_knitwear_19_m_navy","color":"Navy","size":"M","stock":1,"availability":"in_stock"},{"varian… (+900자) ``
7. 모델 → **`facade_get_prd_dtl_info_v2`** `` {"product_id":"prd_belts_01"} ``
   ← 결과 1,811B: `` {"status":"succeeded","data":{"product_id":"prd_belts_01","product_name":"Canvas belt","category_id":"cat_belts","brand_id":"brn_northwind","price":69.0,"member_price":null,"stock":10,"availability":"in_stock","cost":24.38,"approval_status":"active","variants":[{"variant_id":"var_belts_01_s_rust","color":"Rust","size":"S","stock":2,"availability":"in_stock"},{"variant_id":"var_belts_01_m_rust","color":"Rust","size":"M","stock":1,"availability":"in_stock"},{"variant_id":"var_belts_01_l_rust","color":"Rust","size":"L","stock":1,"availability":"in_stock"},{"variant_id":"var_belts_01_s_navy","colo… (+900자) ``
8. 모델 → **`facade_get_prd_dtl_info_v2`** `` {"product_id":"prd_knitwear_24"} ``
   ← 결과 2,222B: `` {"status":"succeeded","data":{"product_id":"prd_knitwear_24","product_name":"Ribbed cotton cardigan","category_id":"cat_knitwear","brand_id":"brn_northwind","price":139.0,"member_price":118.15,"stock":10,"availability":"in_stock","cost":66.21,"approval_status":"active","variants":[{"variant_id":"var_knitwear_24_xs_black","color":"Black","size":"XS","stock":1,"availability":"in_stock"},{"variant_id":"var_knitwear_24_s_black","color":"Black","size":"S","stock":1,"availability":"in_stock"},{"variant_id":"var_knitwear_24_m_black","color":"Black","size":"M","stock":1,"availability":"in_stock"},{"va… (+900자) ``
9. 모델 → **`facade_get_prd_dtl_info_v2`** `` {"product_id":"prd_skirts_01"} ``
   ← 결과 1,991B: `` {"status":"succeeded","data":{"product_id":"prd_skirts_01","product_name":"Satin slip skirt","category_id":"cat_skirts","brand_id":"brn_northwind","price":129.0,"member_price":null,"stock":10,"availability":"in_stock","cost":59.71,"approval_status":"active","variants":[{"variant_id":"var_skirts_01_xs_rust","color":"Rust","size":"XS","stock":1,"availability":"in_stock"},{"variant_id":"var_skirts_01_s_rust","color":"Rust","size":"S","stock":1,"availability":"in_stock"},{"variant_id":"var_skirts_01_m_rust","color":"Rust","size":"M","stock":1,"availability":"in_stock"},{"variant_id":"var_skirts_01… (+900자) ``

**답변 1**
> Here are the in-stock SKUs with ≤10 units on hand as of now — 6 products total. The ones most at risk before the weekend are the two outerwear styles with low total stock and zero-stock variants:
>
> **About to sell out / reorder candidates**
>
> * **Light rain parka – prd_rain_parka**
>   * Total stock: 4 / Price $118.00 / Cost $50.00
>   * Variants:
>     * Stone S – 2 in stock
>     * Stone M – 0 in stock, out_of_stock
>     * Stone L – 0 in stock, out_of_stock
>     * Stone XL – 2 in stock
>   * Material: Nylon with a waterproof coating, light warmth, rolls_into_hood
>
> * **Cotton chore coat – prd_chore_coat**
>   * Total stock: 7 / Price $142.00 / Cost $60.00
>   * Variants:
>     * Olive S – 3 in stock
>     * Olive M – 0 in stock, out_of_stock
>     * Olive L – 0 in stock, out_of_stock
>     * Olive XL – 4 in stock
>   * Material: Cotton canvas, medium warmth
>
> **Other low-stock items, 10 units total but 1 unit per variant**
>
> * **Cashmere blend knit vest – prd_knitwear_19**
>   * Total stock: 10 / Price $199.00, member $169.15 / Cost $83.04
>   * 10 variants, each 1 unit: Navy XS/S/M/L/XL and Rust XS/S/M/L/XL
>
> * **Canvas belt – prd_belts_01**
>   * Total stock: 10 / Price $69.00 / Cost $24.38
>   * 9 variants, stock 1-2 units each: Rust S 2, Rust M 1, Rust L 1, Navy S 1, Navy M 1, Navy L 1, Olive S 1, Olive M 1, Olive L 1
>
> * **Ribbed cotton cardigan – prd_knitwear_24**
>   * Total stock: 10 / Price $139.00, member $118.15 / Cost $66.21
>   * 10 variants, each 1 unit: Black XS/S/M/L/XL and Slate XS/S/M/L/XL
>
> * **Satin slip skirt – prd_skirts_01**
>   * Total stock: 10 / Price $129.00 / Cost $59.71
>   * 10 variants, each 1 unit: Rust XS/S/M/L/XL and White XS/S/M/L/XL
>
> If you need to prioritize for the weekend, the Light rain parka and Cotton chore coat are the immediate risks — total stock 4 and 7 respectively with the core M/L sizes already at zero. The knit vest, belt, cardigan and skirt are at 1 unit per variant, so any weekend demand will wipe those sizes out quickly.

**채점**: ✓ 통과
