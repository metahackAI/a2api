# md-low-stock-before-weekend — smoke-fix-2-batch

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `c8c944e`

**과업**

> what's about to sell out? anything I need to reorder before the weekend

- 필요한 도구: `search_products`
- 허용 도구: `get_inventory`, `list_tasks`, `get_task`
- 답에 있어야 할 사실: Light rain parka has 4 units left and Cotton chore coat has 7, the two lowest in the store
- 답에 있어야 할 사실: Linen shirt is the one with a reorder task: it sells out in about 4 days (task_linen_reorder, needs you)
- 부르면 안 됨: set_variant_stock

### a2api-acom-names-batch · 1회차 · ✓ 통과

토큰 55,062 · 93.062초 · 모델 호출 8회 · 도구 호출 7회 · 첫 요청 프롬프트 2,170토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> what's about to sell out? anything I need to reorder before the weekend

1. 모델 → **`a2api_load`** `` {"names":["get_inventory","suggest_reorder","get_sales_trend","get_sales_overview"]} ``
   ← 결과 85B: `` {"loaded":["get_inventory","suggest_reorder","get_sales_trend","get_sales_overview"]} ``
2. 모델 → **`a2api_load`** `` {"names":["search_products"]} ``
   ← 결과 30B: `` {"loaded":["search_products"]} ``
3. 모델 → **`a2api_batch`** `` {"calls":[{"name":"search_products","arguments":{"max_inventory_level":10,"availability":["in_stock"],"limit":100,"fields":["id","name","inventory_level","price"]}}]} ``
   ← 결과 615B: `` {"batch":[{"name":"search_products","result":{"status":"succeeded","data":{"items":[{"id":"prd_chore_coat","name":"Cotton chore coat","price":142.0,"inventory_level":7},{"id":"prd_knitwear_19","name":"Cashmere blend knit vest","price":199.0,"inventory_level":10},{"id":"prd_rain_parka","name":"Light rain parka","price":118.0,"inventory_level":4},{"id":"prd_belts_01","name":"Canvas belt","price":69.0,"inventory_level":10},{"id":"prd_knitwear_24","name":"Ribbed cotton cardigan","price":139.0,"inventory_level":10},{"id":"prd_skirts_01","name":"Satin slip skirt","price":129.0,"inventory_level":10}]… (+15자) ``
4. 모델 → **`a2api_batch`** `` {"calls":[{"name":"suggest_reorder","arguments":{"product_id":"prd_chore_coat"}},{"name":"suggest_reorder","arguments":{"product_id":"prd_knitwear_19"}},{"name":"suggest_reorder","arguments":{"product_id":"prd_rain_parka"}},{"name":"suggest_reorder","arguments":{"product_id":"prd_belts_01"}},{"name":"suggest_reorder","arguments":{"product_id":"prd_knitwear_24"}},{"name":"suggest_reorder","arguments":{"product_id":"prd_skirts_01"}}]} ``
   ← 결과 5,538B: `` {"batch":[{"name":"suggest_reorder","result":{"status":"succeeded","data":{"product_id":"prd_chore_coat","name":"Cotton chore coat","sales_window":{"valid_from":"2026-10-30","valid_through":"2026-11-05","days":7},"lead_time_days":7,"cover_days":14,"variants":[{"variant_id":"var_chore_coat_s_olive","size":"S","color":"Olive","inventory_level":3,"acom:safety_stock":2,"on_order":0,"units_sold":1,"days_until_stockout":21,"order_quantity":2},{"variant_id":"var_chore_coat_m_olive","size":"M","color":"Olive","inventory_level":0,"acom:safety_stock":2,"on_order":0,"units_sold":0,"days_until_stockout":n… (+900자) ``
5. 모델 → **`a2api_batch`** `` {"calls":[{"name":"get_inventory","arguments":{"product_id":"prd_chore_coat"}},{"name":"get_inventory","arguments":{"product_id":"prd_rain_parka"}},{"name":"get_inventory","arguments":{"product_id":"prd_knitwear_19"}},{"name":"get_inventory","arguments":{"product_id":"prd_belts_01"}},{"name":"get_inventory","arguments":{"product_id":"prd_knitwear_24"}},{"name":"get_inventory","arguments":{"product_id":"prd_skirts_01"}}]} ``
   ← 결과 4,668B: `` {"batch":[{"name":"get_inventory","result":{"status":"succeeded","data":{"product_id":"prd_chore_coat","inventory_level":7,"availability":"in_stock","variants":[{"variant_id":"var_chore_coat_s_olive","sku":"cc-olive-s","size":"S","color":"Olive","inventory_level":3,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_chore_coat_m_olive","sku":"cc-olive-m","size":"M","color":"Olive","inventory_level":0,"acom:safety_stock":2,"acom:managed":true,"availability":"out_of_stock","on_order":0},{"variant_id":"var_chore_coat_l_olive","sku":"cc-olive-l","si… (+900자) ``
6. 모델 → **`get_sales_trend`** `` {"valid_from":"2026-10-30","valid_through":"2026-11-06","acom:granularity":"day","acom:metrics":["revenue","order_count"]} ``
   ← 결과 1,446B: `` {"status":"succeeded","data":{"items":[{"observation_date":"2026-10-30","acom:metric":"revenue","value":{"value":21930.0,"currency":"USD"}},{"observation_date":"2026-10-30","acom:metric":"order_count","value":238},{"observation_date":"2026-10-31","acom:metric":"revenue","value":{"value":27410.0,"currency":"USD"}},{"observation_date":"2026-10-31","acom:metric":"order_count","value":295},{"observation_date":"2026-11-01","acom:metric":"revenue","value":{"value":24880.0,"currency":"USD"}},{"observation_date":"2026-11-01","acom:metric":"order_count","value":270},{"observation_date":"2026-11-02","ac… (+846자) ``
7. 모델 → **`get_sales_overview`** `` {"valid_from":"2026-10-30","valid_through":"2026-11-06","acom:metrics":["revenue","order_count","average_order_value"]} ``
   ← 결과 436B: `` {"status":"succeeded","data":{"items":[{"acom:metric":"revenue","value":{"value":148870.0,"currency":"USD"},"acom:dimension":null,"acom:change_rate":null},{"acom:metric":"order_count","value":1621,"acom:dimension":null,"acom:change_rate":null},{"acom:metric":"average_order_value","value":{"value":91.84,"currency":"USD"},"acom:dimension":null,"acom:change_rate":null}],"total":3,"valid_from":"2026-10-30","valid_through":"2026-11-06"}} ``

**답변 1**
> Low-stock in-stock products right now, total on-hand ≤10 units:
>
> * **Cotton chore coat – prd_chore_coat** – $142.00 – total inventory 7
>   * var_chore_coat_s_olive S Olive: 3 on hand, safety stock 2, units sold last 7d 1 → days until stockout 21, suggested order 2
>   * var_chore_coat_m_olive M Olive: 0 on hand, safety stock 2, availability out_of_stock, suggested order 2
>   * var_chore_coat_l_olive L Olive: 0 on hand, safety stock 2, availability out_of_stock, suggested order 2
>   * var_chore_coat_xl_olive XL Olive: 4 on hand
>   Suggest reorder lines from the system: S Olive 2, M Olive 2, L Olive 2 → total 6 units. M and L are already out of stock.
>
> * **Light rain parka – prd_rain_parka** – $118.00 – total inventory 4
>   * var_rain_parka_s_stone S Stone: 2 on hand, safety stock 2
>   * var_rain_parka_m_stone M Stone: 0 on hand, safety stock 2, availability out_of_stock, suggested order 2
>   * var_rain_parka_l_stone L Stone: 0 on hand, safety stock 2, availability out_of_stock, suggested order 2
>   * var_rain_parka_xl_stone XL Stone: 2 on hand
>   Suggest reorder lines: M Stone 2, L Stone 2 → total 4 units. M and L are out of stock now.
>
> * **Cashmere blend knit vest – prd_knitwear_19** – $199.00 – total inventory 10
>   * var_knitwear_19_xs_navy XS Navy: 1 on hand, safety stock 2, units sold last 7d 0 → suggested order 1
>   * var_knitwear_19_s_navy S Navy: 1 on hand, safety stock 2, units sold last 7d 0 → suggested order 1
>   System suggests 1 unit per size across the range, total suggested 10 units. Inventory is below safety stock on the shown sizes.
>
> * **Canvas belt – prd_belts_01** – $69.00 – total inventory 10
>   * var_belts_01_m_rust M Rust: 1 on hand, safety stock 2, units sold last 7d 1 → days until stockout 7, suggested order 4
>   * var_belts_01_s_rust S Rust: 2 on hand
>   * var_belts_01_l_rust L Rust: 1 on hand
>   * var_belts_01_s_navy S Navy: 1 on hand
>   Suggest reorder lines include M Rust 4, L Rust 1, S Navy 1, M Navy 4 → total suggested 20 units. M Rust is the near-term ris… (+1,502자)

**채점**: ✓ 통과
(도구 정밀도 0.47, 재현율 1.00)
