# md-low-stock-before-weekend — smoke-fix-1-headings

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `c8c944e`

**과업**

> what's about to sell out? anything I need to reorder before the weekend

- 필요한 도구: `search_products`
- 허용 도구: `get_inventory`, `list_tasks`, `get_task`
- 답에 있어야 할 사실: Light rain parka has 4 units left and Cotton chore coat has 7, the two lowest in the store
- 답에 있어야 할 사실: Linen shirt is the one with a reorder task: it sells out in about 4 days (task_linen_reorder, needs you)
- 부르면 안 됨: set_variant_stock

### a2api-acom-names-norelated · 1회차 · E MODEL_CALL_LIMIT

토큰 59,380 · 66.161초 · 모델 호출 12회 · 도구 호출 14회 · 첫 요청 프롬프트 1,934토큰

준비: 전략 `index`, 함수 253개, 목차 6,029자(system prompt)

**질문 1**
> what's about to sell out? anything I need to reorder before the weekend

1. 모델 → **`a2api_load`** `` {"names":["catalog.inventory.get_inventory","catalog.reorder.suggest_reorder","analytics.sales.get_sales_trend"]} ``
   ← 결과 329B: `` {"unknown":["catalog.inventory.get_inventory","catalog.reorder.suggest_reorder","analytics.sales.get_sales_trend"],"suggest":["get_product_group","get_inventory","search_product_groups","suggest_reorder","receive_reorder"],"note":"Unknown names are not in the function index; use names from the index, such as those in suggest."} ``
2. 모델 → **`a2api_load`** `` {"names":["get_inventory","suggest_reorder"]} ``
   ← 결과 46B: `` {"loaded":["get_inventory","suggest_reorder"]} ``
3. 모델 → **`a2api_load`** `` {"names":["analytics.sales.get_sales_overview"]} ``
   ← 결과 225B: `` {"unknown":["analytics.sales.get_sales_overview"],"suggest":["get_sales_overview","get_sales_trend","get_cs_overview"],"note":"Unknown names are not in the function index; use names from the index, such as those in suggest."} ``
4. 모델 → **`a2api_load`** `` {"names":["get_sales_overview"]} ``
   ← 결과 33B: `` {"loaded":["get_sales_overview"]} ``
5. 모델 → **`a2api_load`** `` {"names":["search_products"]} ``
   ← 결과 30B: `` {"loaded":["search_products"]} ``
6. 모델 → **`search_products`** `` {"query":"","sort":"inventory_level","limit":20} ``
   ← 결과 1,771B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/parka-stone.svg","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_stock"},{"variant… (+900자) ``
7. 모델 → **`search_products`** `` {"max_inventory_level":9,"sort":"inventory_level","limit":50} ``
   ← 결과 1,702B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/parka-stone.svg","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_stock"},{"variant… (+900자) ``
8. 모델 → **`suggest_reorder`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 1,094B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","name":"Light rain parka","sales_window":{"valid_from":"2026-10-30","valid_through":"2026-11-05","days":7},"lead_time_days":7,"cover_days":14,"variants":[{"variant_id":"var_rain_parka_s_stone","size":"S","color":"Stone","inventory_level":2,"acom:safety_stock":2,"on_order":0,"units_sold":0,"days_until_stockout":null,"order_quantity":0},{"variant_id":"var_rain_parka_m_stone","size":"M","color":"Stone","inventory_level":0,"acom:safety_stock":2,"on_order":0,"units_sold":0,"days_until_stockout":null,"order_quantity":2},{"variant_id":"var_r… (+494자) ``
9. 모델 → **`suggest_reorder`** `` {"product_id":"prd_chore_coat"} ``
   ← 결과 1,152B: `` {"status":"succeeded","data":{"product_id":"prd_chore_coat","name":"Cotton chore coat","sales_window":{"valid_from":"2026-10-30","valid_through":"2026-11-05","days":7},"lead_time_days":7,"cover_days":14,"variants":[{"variant_id":"var_chore_coat_s_olive","size":"S","color":"Olive","inventory_level":3,"acom:safety_stock":2,"on_order":0,"units_sold":1,"days_until_stockout":21,"order_quantity":2},{"variant_id":"var_chore_coat_m_olive","size":"M","color":"Olive","inventory_level":0,"acom:safety_stock":2,"on_order":0,"units_sold":0,"days_until_stockout":null,"order_quantity":2},{"variant_id":"var_ch… (+552자) ``
10. 모델 → **`get_sales_overview`** `` {"valid_from":"2026-11-02","valid_through":"2026-11-06","acom:metrics":["revenue","order_count","average_order_value"]} ``
   ← 결과 434B: `` {"status":"succeeded","data":{"items":[{"acom:metric":"revenue","value":{"value":74650.0,"currency":"USD"},"acom:dimension":null,"acom:change_rate":null},{"acom:metric":"order_count","value":818,"acom:dimension":null,"acom:change_rate":null},{"acom:metric":"average_order_value","value":{"value":91.26,"currency":"USD"},"acom:dimension":null,"acom:change_rate":null}],"total":3,"valid_from":"2026-11-02","valid_through":"2026-11-06"}} ``
11. 모델 → **`get_inventory`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 893B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","inventory_level":4,"availability":"in_stock","variants":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"acom:safety_stock":2,"acom:managed":true,"availability":"out_of_stock","on_order":0},{"variant_id":"var_rain_parka_l_stone","sku":"rp-stone-l","size":"L","color":"Stone","inventory_level":0… (+293자) ``
12. 모델 → **`get_inventory`** `` {"product_id":"prd_chore_coat"} ``
   ← 결과 893B: `` {"status":"succeeded","data":{"product_id":"prd_chore_coat","inventory_level":7,"availability":"in_stock","variants":[{"variant_id":"var_chore_coat_s_olive","sku":"cc-olive-s","size":"S","color":"Olive","inventory_level":3,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_chore_coat_m_olive","sku":"cc-olive-m","size":"M","color":"Olive","inventory_level":0,"acom:safety_stock":2,"acom:managed":true,"availability":"out_of_stock","on_order":0},{"variant_id":"var_chore_coat_l_olive","sku":"cc-olive-l","size":"L","color":"Olive","inventory_level":0… (+293자) ``
13. 모델 → **`search_products`** `` {"sort":"inventory_level","limit":50,"cursor":"o20"} ``
   ← 결과 1,261B: `` {"status":"succeeded","data":{"items":[{"id":"prd_sneakers_09","name":"Leather low-tops","category_id":"cat_sneakers","brand_id":"brn_northwind","image":"/media/garment/shoe-stone.svg","price":109.0,"price_currency":"USD","member_price":null,"cost":50.45,"inventory_level":14,"availability":"in_stock","has_variant":[{"variant_id":"var_sneakers_09_7_stone","sku":"sneakers-09-stone-7","size":"7","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_sneakers_09_8_stone","sku":"sneakers-09-stone-8","size":"8","color":"Stone","inventory_level":2,"availability":"in_stock"}… (+661자) ``
14. 모델 → **`search_products`** `` {"max_inventory_level":10,"sort":"inventory_level","limit":50} ``
   ← 결과 3,221B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/garment/parka-stone.svg","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_stock"},{"variant… (+900자) ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "Light rain parka has 4 units left and Cotton chore coat has " (4, 7 not shown); fact "Linen shirt is the one with a reorder task: it sells out in " (4 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.67, 재현율 1.00)
