# mgr-how-is-business — ours-heldout-posthoc-1

[← 실행 묶음](README.md) · 세트 `held_out` · a-commerce `7e1557b` · a2api `d99f239`

**과업**

> How is my business doing?

- 필요한 도구: `get_sales_overview`
- 허용 도구: `get_sales_trend`, `explain_sales_change`, `get_customer_overview`, `list_tasks`
- 답에 있어야 할 사실: yesterday (Thu Nov 5) was $18,240, 20% under the Thursday average; the agent leads with that and its causes

### a2api-acom · 1회차 · ✗ 실패

토큰 9,825 · 13.382초 · 모델 호출 2회 · 도구 호출 3회 · 첫 요청 프롬프트 3,838토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> How is my business doing?

1. 모델 → **`a2api_search`** `` {"query":"business performance metrics"} ``
   ← 결과 379B: `` {"selected":[{"name":"acom_verify_business","id":"acom.verify_business"},{"name":"acom_get_seller_grade","id":"acom.get_seller_grade"},{"name":"acom_update_seller","id":"acom.update_seller"},{"name":"acom_issue_receipt","id":"acom.issue_receipt"},{"name":"acom_verify_identity","id":"acom.verify_identity"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"seller performance"} ``
   ← 결과 492B: `` {"selected":[{"name":"acom_update_seller","id":"acom.update_seller"},{"name":"acom_set_seller_grade","id":"acom.set_seller_grade"},{"name":"acom_get_seller","id":"acom.get_seller"},{"name":"acom_search_sellers","id":"acom.search_sellers"},{"name":"acom_onboard_seller","id":"acom.onboard_seller"}],"evicted":["acom_set_favorite","acom_register_member","acom_get_category","acom_get_import_status","acom_verify_business"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`a2api_search`** `` {"query":"business sales"} ``
   ← 결과 475B: `` {"selected":[{"name":"acom_verify_business","id":"acom.verify_business"},{"name":"acom_get_sales_trend","id":"acom.get_sales_trend"},{"name":"acom_get_sales_overview","id":"acom.get_sales_overview"}],"omitted":[{"id":"acom.set_sale_prices","reason":"SCHEMA_BUDGET"},{"id":"acom.explain_sales_change","reason":"SCHEMA_BUDGET"}],"evicted":["acom_issue_receipt","acom_verify_identity","acom_update_seller"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``

**답변 1**
> To check how your business is doing I need to identify it in the marketplace.
>
> Could you provide your business legal name or tax ID (or your seller ID if you have it)? Once I have that I can pull your seller grade, sales performance and recent trends.

**채점**: ✗ 실패 — 빠진 것: tool get_sales_overview; fact "yesterday (Thu Nov 5) was $18,240, 20% under the Thursday av" (5, 18240, 20 not shown)
(도구 정밀도 —, 재현율 0.00)

### a2api-acom · 2회차 · ✗ 실패

토큰 9,825 · 13.373초 · 모델 호출 2회 · 도구 호출 3회 · 첫 요청 프롬프트 3,838토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> How is my business doing?

1. 모델 → **`a2api_search`** `` {"query":"business performance metrics"} ``
   ← 결과 379B: `` {"selected":[{"name":"acom_verify_business","id":"acom.verify_business"},{"name":"acom_get_seller_grade","id":"acom.get_seller_grade"},{"name":"acom_update_seller","id":"acom.update_seller"},{"name":"acom_issue_receipt","id":"acom.issue_receipt"},{"name":"acom_verify_identity","id":"acom.verify_identity"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"seller performance"} ``
   ← 결과 492B: `` {"selected":[{"name":"acom_update_seller","id":"acom.update_seller"},{"name":"acom_set_seller_grade","id":"acom.set_seller_grade"},{"name":"acom_get_seller","id":"acom.get_seller"},{"name":"acom_search_sellers","id":"acom.search_sellers"},{"name":"acom_onboard_seller","id":"acom.onboard_seller"}],"evicted":["acom_set_favorite","acom_register_member","acom_get_category","acom_get_import_status","acom_verify_business"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`a2api_search`** `` {"query":"business sales"} ``
   ← 결과 475B: `` {"selected":[{"name":"acom_verify_business","id":"acom.verify_business"},{"name":"acom_get_sales_trend","id":"acom.get_sales_trend"},{"name":"acom_get_sales_overview","id":"acom.get_sales_overview"}],"omitted":[{"id":"acom.set_sale_prices","reason":"SCHEMA_BUDGET"},{"id":"acom.explain_sales_change","reason":"SCHEMA_BUDGET"}],"evicted":["acom_issue_receipt","acom_verify_identity","acom_update_seller"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``

**답변 1**
> To check how your business is doing I need to identify it in the marketplace.
>
> Could you provide your business legal name or tax ID (or your seller ID if you have it)? Once I have that I can pull your seller grade, sales performance and recent trends.

**채점**: ✗ 실패 — 빠진 것: tool get_sales_overview; fact "yesterday (Thu Nov 5) was $18,240, 20% under the Thursday av" (5, 18240, 20 not shown)
(도구 정밀도 —, 재현율 0.00)

### a2api-facade · 1회차 · ✗ 실패

토큰 6,898 · 15.302초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 988토큰

준비: 전략 `search`, 함수 2개

**질문 1**
> How is my business doing?

1. 모델 → **`a2api_search`** `` {"query":"business performance sales revenue orders"} ``
   ← 결과 368B: `` {"selected":[{"name":"facade_get_sale_anls_grid_list","id":"facade.get_sale_anls_grid_list"},{"name":"facade_save_cust_msg_send","id":"facade.save_cust_msg_send"},{"name":"facade_get_prmt_grid_list","id":"facade.get_prmt_grid_list"},{"name":"facade_save_prmt_list","id":"facade.save_prmt_list"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`facade_get_sale_anls_grid_list`** `` {"from_date":"2026-10-30","to_date":"2026-11-06","compare_to":"previous_period"} ``
   ← 결과 230B: `` {"status":"succeeded","data":{"list":[{"from_date":"2026-10-30","to_date":"2026-11-06","revenue":148870.0,"order_count":1621,"compare_revenue":174450.0,"compare_order_count":1892,"revenue_change":-25580.0,"change_rate":-0.1466}]}} ``

**답변 1**
> For the last 7 days, 30 Oct – 6 Nov 2026:
>
> * Revenue: $148,870
> * Orders: 1,621
>
> vs the previous period:
>
> * Revenue: $174,450 → - $25,580 / -14.7%
> * Orders: 1,892 → -271 / -14.3%
>
> Revenue and order count are down ~14-15% week-over-week for the period ending today.

**채점**: ✗ 실패 — 빠진 것: fact "yesterday (Thu Nov 5) was $18,240, 20% under the Thursday av" (5, 18240, 20 not shown)

### a2api-facade · 2회차 · ✗ 실패

토큰 6,898 · 14.919초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 988토큰

준비: 전략 `search`, 함수 2개

**질문 1**
> How is my business doing?

1. 모델 → **`a2api_search`** `` {"query":"business performance sales revenue orders"} ``
   ← 결과 368B: `` {"selected":[{"name":"facade_get_sale_anls_grid_list","id":"facade.get_sale_anls_grid_list"},{"name":"facade_save_cust_msg_send","id":"facade.save_cust_msg_send"},{"name":"facade_get_prmt_grid_list","id":"facade.get_prmt_grid_list"},{"name":"facade_save_prmt_list","id":"facade.save_prmt_list"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`facade_get_sale_anls_grid_list`** `` {"from_date":"2026-10-30","to_date":"2026-11-06","compare_to":"previous_period"} ``
   ← 결과 230B: `` {"status":"succeeded","data":{"list":[{"from_date":"2026-10-30","to_date":"2026-11-06","revenue":148870.0,"order_count":1621,"compare_revenue":174450.0,"compare_order_count":1892,"revenue_change":-25580.0,"change_rate":-0.1466}]}} ``

**답변 1**
> For the last 7 days, 30 Oct – 6 Nov 2026:
>
> * Revenue: $148,870
> * Orders: 1,621
>
> vs the previous period:
>
> * Revenue: $174,450 → - $25,580 / -14.7%
> * Orders: 1,892 → -271 / -14.3%
>
> Revenue and order count are down ~14-15% week-over-week for the period ending today.

**채점**: ✗ 실패 — 빠진 것: fact "yesterday (Thu Nov 5) was $18,240, 20% under the Thursday av" (5, 18240, 20 not shown)
