# b3-why-sales-dropped — ours-design-4

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `879cc92`

**과업**

> Why did sales drop yesterday?

- 필요한 도구: `explain_sales_change`
- 허용 도구: `get_sales_trend`, `get_sales_overview`, `search_products`, `get_inventory`
- 답에 있어야 할 사실: Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$4,660, -20%); 201 orders against 247
- 답에 있어야 할 사실: M and L sold out on the three best sellers (chore coat, rain parka, denim jacket): about -$2,700
- 답에 있어야 할 사실: the weekly email did not go out (Thu 08:00 list import failed): about -$1,300; -$660 is not explained

### a2api-acom · 1회차 · ✗ 실패

토큰 11,684 · 16.892초 · 모델 호출 2회 · 도구 호출 1회 · 첫 요청 프롬프트 4,941토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> Why did sales drop yesterday?

1. 모델 → **`acom_explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue","max_causes":5} ``
   ← 결과 2,167B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+900자) ``

**답변 1**
> Yesterday 2026-11-05 revenue was $18,240 on 201 orders vs the same weekday average over the last 4 weeks $22,900 on 247 orders.
>
> Change: -$4,660 revenue, -20.4% vs same-weekday last 4 weeks.
>
> Explained causes:
>
> * **Out of stock – $2,700 lost**
>   3 bestsellers sold out in M/L since Wed Nov 4 15:00 ET:
>   - prd_chore_coat Cotton chore coat M/L – expected $1,313.5, actual $0. Availability starts 2026-11-12
>   - prd_denim_jacket Denim jacket M/L – expected $796.5, actual $0. Availability starts 2026-11-12
>   - prd_rain_parka Light rain parka M/L – expected $590.0, actual $0. Availability starts unknown
>
> * **Campaign not sent – $1,300 lost**
>   cmp_weekly_1105 Weekly email scheduled 2026-11-05 08:00 ET failed: List import failed. Expected lift $1,300 vs the four prior weekly sends cmp_weekly_1008/1015/1022/1029.
>
> Unexplained remainder: -$660.
>
> Total explained gap = -$4,000 of the -$4,660 drop.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-facade · 1회차 · E MODEL_CALL_LIMIT

토큰 48,172 · 89.632초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 1,645토큰

준비: 전략 `search`, 함수 4개

**질문 1**
> Why did sales drop yesterday?

1. 모델 → **`facade_get_sale_anls_grid_list`** `` {"from_date":"2026-11-05","to_date":"2026-11-05","compare_to":"same_weekday_last_4_weeks"} ``
   ← 결과 225B: `` {"status":"succeeded","data":{"list":[{"from_date":"2026-11-05","to_date":"2026-11-05","revenue":18240.0,"order_count":201,"compare_revenue":22900.0,"compare_order_count":247,"revenue_change":-4660.0,"change_rate":-0.2035}]}} ``
2. 모델 → **`facade_get_prmt_grid_list`** `` {"active_from":"2026-11-01","active_until":"2026-11-06","page":1,"page_size":100} ``
   ← 결과 960B: `` {"status":"succeeded","data":{"list":[{"promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00","starts_at":"2026-11-01T00:00:00-04:00","ends_at":"2026-11-15T23:59:00-05:00"},{"promotion_id":"promo_birthday","promotion_name":"Birthday coupon","promotion_type":"order_discount","promotion_status":"running","target_member_grade":"G01","starts_at":"2026-01-01T00:00:00-05:00","ends_at":null},{"promotion_id":"promo_free_ship_80","promotion_name":"Free shipping over $80","promotion_type":"… (+360자) ``
3. 모델 → **`facade_get_prmt_grid_list`** `` {"active_from":"2026-11-04T00:00:00-04:00","active_until":"2026-11-04T23:59:59-04:00","page":1,"page_size":100} ``
   ← 결과 960B: `` {"status":"succeeded","data":{"list":[{"promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00","starts_at":"2026-11-01T00:00:00-04:00","ends_at":"2026-11-15T23:59:00-05:00"},{"promotion_id":"promo_birthday","promotion_name":"Birthday coupon","promotion_type":"order_discount","promotion_status":"running","target_member_grade":"G01","starts_at":"2026-01-01T00:00:00-05:00","ends_at":null},{"promotion_id":"promo_free_ship_80","promotion_name":"Free shipping over $80","promotion_type":"… (+360자) ``
4. 모델 → **`a2api_search`** `` {"query":"sales by category"} ``
   ← 결과 442B: `` {"selected":[{"name":"facade_save_prmt_list","id":"facade.save_prmt_list"},{"name":"facade_get_sale_anls_grid_list","id":"facade.get_sale_anls_grid_list"},{"name":"facade_get_prmt_grid_list","id":"facade.get_prmt_grid_list"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_get_prd_grid_list_cnt","id":"facade.get_prd_grid_list_cnt"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true} ``
5. 모델 → **`a2api_search`** `` {"query":"sales analysis category"} ``
   ← 결과 583B: `` {"selected":[{"name":"facade_save_prmt_list","id":"facade.save_prmt_list"},{"name":"facade_get_sale_anls_grid_list","id":"facade.get_sale_anls_grid_list"},{"name":"facade_get_prmt_grid_list","id":"facade.get_prmt_grid_list"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_get_prd_grid_list_cnt","id":"facade.get_prd_grid_list_cnt"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match is already callable. If they cannot answer, tell the user what is missing instead of searching again."} ``
6. 모델 → **`facade_get_sale_anls_grid_list`** `` {"from_date":"2026-11-05","to_date":"2026-11-05","compare_to":"previous_period"} ``
   ← 결과 225B: `` {"status":"succeeded","data":{"list":[{"from_date":"2026-11-05","to_date":"2026-11-05","revenue":18240.0,"order_count":201,"compare_revenue":19320.0,"compare_order_count":211,"revenue_change":-1080.0,"change_rate":-0.0559}]}} ``
7. 모델 → **`facade_get_prd_grid_list_cnt`** `` {"availability":"out_of_stock"} ``
   ← 결과 41B: `` {"status":"succeeded","data":{"total":0}} ``
8. 모델 → **`a2api_search`** `` {"query":"category sales revenue"} ``
   ← 결과 583B: `` {"selected":[{"name":"facade_get_sale_anls_grid_list","id":"facade.get_sale_anls_grid_list"},{"name":"facade_save_prmt_list","id":"facade.save_prmt_list"},{"name":"facade_get_prmt_grid_list","id":"facade.get_prmt_grid_list"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_get_prd_grid_list_cnt","id":"facade.get_prd_grid_list_cnt"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match is already callable. If they cannot answer, tell the user what is missing instead of searching again."} ``
9. 모델 → **`a2api_search`** `` {"query":"sales analysis"} ``
   ← 결과 439B: `` {"selected":[{"name":"facade_get_sale_anls_grid_list","id":"facade.get_sale_anls_grid_list"},{"name":"facade_get_prmt_grid_list","id":"facade.get_prmt_grid_list"},{"name":"facade_save_prmt_list","id":"facade.save_prmt_list"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match is already callable. If they cannot answer, tell the user what is missing instead of searching again."} ``
10. 모델 → **`facade_get_sale_anls_grid_list`** `` {"from_date":"2026-11-04","to_date":"2026-11-04","compare_to":"same_weekday_last_4_weeks"} ``
   ← 결과 226B: `` {"status":"succeeded","data":{"list":[{"from_date":"2026-11-04","to_date":"2026-11-04","revenue":19320.0,"order_count":211,"compare_revenue":20532.0,"compare_order_count":220.5,"revenue_change":-1212.0,"change_rate":-0.059}]}} ``
11. 모델 → **`facade_get_prd_grid_list_cnt`** `` {"availability":"discontinued"} ``
   ← 결과 41B: `` {"status":"succeeded","data":{"total":0}} ``
12. 모델 → **`facade_get_prmt_grid_list`** `` {"promotion_status":"ended","active_until":"2026-11-05","page":1,"page_size":100} ``
   ← 결과 313B: `` {"status":"succeeded","data":{"list":[{"promotion_id":"promo_linen_clearance","promotion_name":"Linen clearance","promotion_type":"item_price_everyone","promotion_status":"ended","target_member_grade":"G00","starts_at":"2026-10-01T00:00:00-04:00","ends_at":"2026-10-20T23:59:00-04:00"}],"page":1,"page_size":100}} ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (5, 18240, 22900, 4660, 20, 201, 247 not shown); fact "M and L sold out on the three best sellers (chore coat, rain" (2700 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8, 0, 1300, 660 not shown); HOST:MODEL_CALL_LIMIT
