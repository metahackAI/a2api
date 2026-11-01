# ops-unfulfilled-3-days — ours-heldout-index-posthoc-2

[← 실행 묶음](README.md) · 세트 `held_out` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> any orders sitting unfulfilled for more than 3 days?

- 필요한 도구: `search_orders`
- 허용 도구: `get_order`
- 답에 있어야 할 사실: none: 412 orders are processing and the oldest was placed Wed Nov 4 00:09

### a2api-acom · 1회차 · E MODEL_CALL_LIMIT

토큰 95,561 · 75.38초 · 모델 호출 12회 · 도구 호출 14회 · 첫 요청 프롬프트 3,469토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> any orders sitting unfulfilled for more than 3 days?

1. 모델 → **`a2api_search`** `` {"query":"unfulfilled orders pending fulfillment"} ``
   ← 결과 474B: `` {"selected":[{"name":"acom_get_seller_grade","id":"acom.get_seller_grade"},{"name":"acom_sync_claim_status","id":"acom.sync_claim_status"},{"name":"acom_search_orders","id":"acom.search_orders"},{"name":"acom_get_order","id":"acom.get_order"},{"name":"acom_lookup_external_order","id":"acom.lookup_external_order"}],"evicted":["acom_pause_subscription","acom_cancel_subscription","acom_create_reorder"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"orders unfulfilled"} ``
   ← 결과 448B: `` {"selected":[{"name":"acom_search_orders","id":"acom.search_orders"},{"name":"acom_get_order","id":"acom.get_order"},{"name":"acom_lookup_external_order","id":"acom.lookup_external_order"},{"name":"acom_sync_order_status","id":"acom.sync_order_status"},{"name":"acom_cancel_order_lines","id":"acom.cancel_order_lines"}],"evicted":["acom_get_sales_trend","acom_restore_coupon"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`a2api_search`** `` {"query":"list orders"} ``
   ← 결과 498B: `` {"selected":[{"name":"acom_list_enums","id":"acom.list_enums"},{"name":"acom_list_conditional_gifts","id":"acom.list_conditional_gifts"},{"name":"acom_list_subscriptions","id":"acom.list_subscriptions"},{"name":"acom_list_display_slots","id":"acom.list_display_slots"}],"omitted":[{"id":"acom.create_event","reason":"SCHEMA_BUDGET"}],"evicted":["acom_search_return_requests","acom_get_seller_overview","acom_get_seller_grade"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`acom_list_enums`** `` {"names":["order_status"]} ``
   ← 결과 610B: `` {"status":"succeeded","data":{"items":[{"name":"order_status","applies_to":["analytics.order_summary","catalog.reorder","sales.order_event","sales.order_item","sales.sales_order"],"values":[{"value":"payment_due","label":"Payment due","order":1},{"value":"processing","label":"Processing","order":2},{"value":"in_transit","label":"In transit","order":3},{"value":"delivered","label":"Delivered","order":4},{"value":"returned","label":"Returned","order":5,"terminal":true},{"value":"cancelled","label":"Cancelled","order":6,"terminal":true},{"value":"problem","label":"Needs attention","order":7}]}],"… (+10자) ``
5. 모델 → **`acom_search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_to":"2026-11-03","sort":"-order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
6. 모델 → **`acom_search_orders`** `` {"order_status":["processing"],"order_date_to":"2026-11-06","sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 4,606B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27860","order_number":"27860","order_status":"processing","customer_id":"cus_m008451","order_date":"2026-11-04T00:09:00-05:00","total":{"value":92.0,"currency":"USD"}},{"id":"ord_27861","order_number":"27861","order_status":"processing","customer_id":"cus_m000912","order_date":"2026-11-04T00:11:00-05:00","total":{"value":89.0,"currency":"USD"}},{"id":"ord_27862","order_number":"27862","order_status":"processing","customer_id":"cus_m013479","order_date":"2026-11-04T00:29:00-05:00","total":{"value":84.0,"currency":"USD"}},{"id":"ord_27863","order… (+900자) ``
7. 모델 → **`acom_search_orders`** `` {"order_status":["processing"],"order_date_to":"2026-11-03","sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
8. 모델 → **`acom_search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_from":"2026-10-31","order_date_to":"2026-11-03","sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
9. 모델 → **`acom_search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_from":"2026-10-01","order_date_to":"2026-11-03","sort":"-order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
10. 모델 → **`acom_search_orders`** `` {"order_status":["processing"],"order_date_from":"2026-10-01","order_date_to":"2026-11-06","sort":"-order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 4,600B: `` {"status":"succeeded","data":{"items":[{"id":"ord_28271","order_number":"28271","order_status":"processing","customer_id":"cus_m008008","order_date":"2026-11-05T23:40:00-05:00","total":{"value":55.0,"currency":"USD"}},{"id":"ord_28270","order_number":"28270","order_status":"processing","customer_id":"cus_m002731","order_date":"2026-11-05T22:34:00-05:00","total":{"value":49.0,"currency":"USD"}},{"id":"ord_28269","order_number":"28269","order_status":"processing","customer_id":"cus_m007104","order_date":"2026-11-05T22:20:00-05:00","total":{"value":55.0,"currency":"USD"}},{"id":"ord_28268","order… (+900자) ``
11. 모델 → **`acom_search_orders`** `` {"order_status":["processing"],"sort":"order_date","limit":1,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 251B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27860","order_number":"27860","order_status":"processing","customer_id":"cus_m008451","order_date":"2026-11-04T00:09:00-05:00","total":{"value":92.0,"currency":"USD"}}],"total":412,"next_cursor":"o1"}} ``
12. 모델 → **`acom_search_orders`** `` {"order_status":["payment_due"],"sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 407B: `` {"status":"succeeded","data":{"items":[{"id":"ord_29001","order_number":"29001","order_status":"payment_due","customer_id":"cus_priya","order_date":"2026-11-05T16:20:00-05:00","total":{"value":128.0,"currency":"USD"}},{"id":"ord_29002","order_number":"29002","order_status":"payment_due","customer_id":"cus_owen","order_date":"2026-11-06T09:05:00-05:00","total":{"value":89.0,"currency":"USD"}}],"total":2}} ``
13. 모델 → **`acom_search_orders`** `` {"order_status":["problem"],"sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
14. 모델 → **`acom_search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_to":"2026-11-02","sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "none: 412 orders are processing and the oldest was placed We" (412, 4, 0, 9 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.91, 재현율 1.00)

### a2api-acom · 2회차 · E MODEL_CALL_LIMIT

토큰 95,561 · 74.438초 · 모델 호출 12회 · 도구 호출 14회 · 첫 요청 프롬프트 3,469토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> any orders sitting unfulfilled for more than 3 days?

1. 모델 → **`a2api_search`** `` {"query":"unfulfilled orders pending fulfillment"} ``
   ← 결과 474B: `` {"selected":[{"name":"acom_get_seller_grade","id":"acom.get_seller_grade"},{"name":"acom_sync_claim_status","id":"acom.sync_claim_status"},{"name":"acom_search_orders","id":"acom.search_orders"},{"name":"acom_get_order","id":"acom.get_order"},{"name":"acom_lookup_external_order","id":"acom.lookup_external_order"}],"evicted":["acom_pause_subscription","acom_cancel_subscription","acom_create_reorder"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"orders unfulfilled"} ``
   ← 결과 448B: `` {"selected":[{"name":"acom_search_orders","id":"acom.search_orders"},{"name":"acom_get_order","id":"acom.get_order"},{"name":"acom_lookup_external_order","id":"acom.lookup_external_order"},{"name":"acom_sync_order_status","id":"acom.sync_order_status"},{"name":"acom_cancel_order_lines","id":"acom.cancel_order_lines"}],"evicted":["acom_get_sales_trend","acom_restore_coupon"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`a2api_search`** `` {"query":"list orders"} ``
   ← 결과 498B: `` {"selected":[{"name":"acom_list_enums","id":"acom.list_enums"},{"name":"acom_list_conditional_gifts","id":"acom.list_conditional_gifts"},{"name":"acom_list_subscriptions","id":"acom.list_subscriptions"},{"name":"acom_list_display_slots","id":"acom.list_display_slots"}],"omitted":[{"id":"acom.create_event","reason":"SCHEMA_BUDGET"}],"evicted":["acom_search_return_requests","acom_get_seller_overview","acom_get_seller_grade"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`acom_list_enums`** `` {"names":["order_status"]} ``
   ← 결과 610B: `` {"status":"succeeded","data":{"items":[{"name":"order_status","applies_to":["analytics.order_summary","catalog.reorder","sales.order_event","sales.order_item","sales.sales_order"],"values":[{"value":"payment_due","label":"Payment due","order":1},{"value":"processing","label":"Processing","order":2},{"value":"in_transit","label":"In transit","order":3},{"value":"delivered","label":"Delivered","order":4},{"value":"returned","label":"Returned","order":5,"terminal":true},{"value":"cancelled","label":"Cancelled","order":6,"terminal":true},{"value":"problem","label":"Needs attention","order":7}]}],"… (+10자) ``
5. 모델 → **`acom_search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_to":"2026-11-03","sort":"-order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
6. 모델 → **`acom_search_orders`** `` {"order_status":["processing"],"order_date_to":"2026-11-06","sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 4,606B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27860","order_number":"27860","order_status":"processing","customer_id":"cus_m008451","order_date":"2026-11-04T00:09:00-05:00","total":{"value":92.0,"currency":"USD"}},{"id":"ord_27861","order_number":"27861","order_status":"processing","customer_id":"cus_m000912","order_date":"2026-11-04T00:11:00-05:00","total":{"value":89.0,"currency":"USD"}},{"id":"ord_27862","order_number":"27862","order_status":"processing","customer_id":"cus_m013479","order_date":"2026-11-04T00:29:00-05:00","total":{"value":84.0,"currency":"USD"}},{"id":"ord_27863","order… (+900자) ``
7. 모델 → **`acom_search_orders`** `` {"order_status":["processing"],"order_date_to":"2026-11-03","sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
8. 모델 → **`acom_search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_from":"2026-10-31","order_date_to":"2026-11-03","sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
9. 모델 → **`acom_search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_from":"2026-10-01","order_date_to":"2026-11-03","sort":"-order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
10. 모델 → **`acom_search_orders`** `` {"order_status":["processing"],"order_date_from":"2026-10-01","order_date_to":"2026-11-06","sort":"-order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 4,600B: `` {"status":"succeeded","data":{"items":[{"id":"ord_28271","order_number":"28271","order_status":"processing","customer_id":"cus_m008008","order_date":"2026-11-05T23:40:00-05:00","total":{"value":55.0,"currency":"USD"}},{"id":"ord_28270","order_number":"28270","order_status":"processing","customer_id":"cus_m002731","order_date":"2026-11-05T22:34:00-05:00","total":{"value":49.0,"currency":"USD"}},{"id":"ord_28269","order_number":"28269","order_status":"processing","customer_id":"cus_m007104","order_date":"2026-11-05T22:20:00-05:00","total":{"value":55.0,"currency":"USD"}},{"id":"ord_28268","order… (+900자) ``
11. 모델 → **`acom_search_orders`** `` {"order_status":["processing"],"sort":"order_date","limit":1,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 251B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27860","order_number":"27860","order_status":"processing","customer_id":"cus_m008451","order_date":"2026-11-04T00:09:00-05:00","total":{"value":92.0,"currency":"USD"}}],"total":412,"next_cursor":"o1"}} ``
12. 모델 → **`acom_search_orders`** `` {"order_status":["payment_due"],"sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 407B: `` {"status":"succeeded","data":{"items":[{"id":"ord_29001","order_number":"29001","order_status":"payment_due","customer_id":"cus_priya","order_date":"2026-11-05T16:20:00-05:00","total":{"value":128.0,"currency":"USD"}},{"id":"ord_29002","order_number":"29002","order_status":"payment_due","customer_id":"cus_owen","order_date":"2026-11-06T09:05:00-05:00","total":{"value":89.0,"currency":"USD"}}],"total":2}} ``
13. 모델 → **`acom_search_orders`** `` {"order_status":["problem"],"sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
14. 모델 → **`acom_search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_to":"2026-11-02","sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "none: 412 orders are processing and the oldest was placed We" (412, 4, 0, 9 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.91, 재현율 1.00)

### a2api-acom-index · 1회차 · ✗ 실패

토큰 119,220 · 94.494초 · 모델 호출 11회 · 도구 호출 10회 · 첫 요청 프롬프트 6,987토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> any orders sitting unfulfilled for more than 3 days?

1. 모델 → **`a2api_load`** `` {"names":["search_orders","get_order","list_enums"]} ``
   ← 결과 53B: `` {"loaded":["search_orders","get_order","list_enums"]} ``
2. 모델 → **`list_enums`** `` {"names":["order_status"]} ``
   ← 결과 610B: `` {"status":"succeeded","data":{"items":[{"name":"order_status","applies_to":["analytics.order_summary","catalog.reorder","sales.order_event","sales.order_item","sales.sales_order"],"values":[{"value":"payment_due","label":"Payment due","order":1},{"value":"processing","label":"Processing","order":2},{"value":"in_transit","label":"In transit","order":3},{"value":"delivered","label":"Delivered","order":4},{"value":"returned","label":"Returned","order":5,"terminal":true},{"value":"cancelled","label":"Cancelled","order":6,"terminal":true},{"value":"problem","label":"Needs attention","order":7}]}],"… (+10자) ``
3. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_to":"2026-11-03","sort":"-order_date","limit":100,"fields":["id","order_number","order_status","customer_id","order_date","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
4. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_to":"2026-11-02","sort":"-order_date","limit":100,"fields":["id","order_number","order_status","customer_id","order_date","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
5. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"sort":"-order_date","limit":100,"fields":["id","order_number","order_status","customer_id","order_date","total"]} ``
   ← 결과 4,598B: `` {"status":"succeeded","data":{"items":[{"id":"ord_29002","order_number":"29002","order_status":"payment_due","customer_id":"cus_owen","order_date":"2026-11-06T09:05:00-05:00","total":{"value":89.0,"currency":"USD"}},{"id":"ord_28271","order_number":"28271","order_status":"processing","customer_id":"cus_m008008","order_date":"2026-11-05T23:40:00-05:00","total":{"value":55.0,"currency":"USD"}},{"id":"ord_28270","order_number":"28270","order_status":"processing","customer_id":"cus_m002731","order_date":"2026-11-05T22:34:00-05:00","total":{"value":49.0,"currency":"USD"}},{"id":"ord_28269","order_n… (+900자) ``
6. 모델 → **`search_orders`** `` {"order_status":["problem"],"order_date_to":"2026-11-03","limit":100,"fields":["id","order_number","order_status","order_date"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
7. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_from":"2026-10-30","order_date_to":"2026-11-03","limit":100,"fields":["id","order_number","order_status","order_date"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
8. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date"]} ``
   ← 결과 5,673B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27860","order_number":"27860","order_status":"processing","order_date":"2026-11-04T00:09:00-05:00"},{"id":"ord_27861","order_number":"27861","order_status":"processing","order_date":"2026-11-04T00:11:00-05:00"},{"id":"ord_27862","order_number":"27862","order_status":"processing","order_date":"2026-11-04T00:29:00-05:00"},{"id":"ord_27863","order_number":"27863","order_status":"processing","order_date":"2026-11-04T00:41:00-05:00"},{"id":"ord_27864","order_number":"27864","order_status":"processing","order_date":"2026-11-04T00:43:00-05:00"},{"id":… (+900자) ``
9. 모델 → **`search_orders`** `` {"order_status":["payment_due"],"sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date"]} ``
   ← 결과 275B: `` {"status":"succeeded","data":{"items":[{"id":"ord_29001","order_number":"29001","order_status":"payment_due","order_date":"2026-11-05T16:20:00-05:00"},{"id":"ord_29002","order_number":"29002","order_status":"payment_due","order_date":"2026-11-06T09:05:00-05:00"}],"total":2}} ``
10. 모델 → **`search_orders`** `` {"order_status":["problem"],"limit":100,"fields":["id","order_number","order_status","order_date"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``

**답변 1**
> No. There are no unfulfilled orders that are >3 days old as of Fri 2026-11-06 11:00 America/New_York.
>
> Unfulfilled statuses checked: `processing`, `payment_due`, `problem`.
>
> * `processing` – 414 orders in the set. The oldest ones are from 2026-11-04:
>   * ord_27860 / 27860 – processing – 2026-11-04T00:09:00-05:00
>   * ord_27861 / 27861 – processing – 2026-11-04T00:11:00-05:00
>   * ord_27862 / 27862 – processing – 2026-11-04T00:29:00-05:00
>   * ord_27863 / 27863 – processing – 2026-11-04T00:41:00-05:00
>   * … the first 100 results are all 2026-11-04 onward. No processing orders dated ≤2026-11-03 11:00 are returned.
>
> * `payment_due` – 2 orders total:
>   * ord_29001 / 29001 – payment_due – 2026-11-05T16:20:00-05:00
>   * ord_29002 / 29002 – payment_due – 2026-11-06T09:05:00-05:00
>
> * `problem` – 0 orders.
>
> A search for `order_status` in [processing, payment_due, problem] with `order_date_to` = 2026-11-03 returns 0 items, and with `order_date_to` = 2026-11-02 returns 0 items. The oldest unfulfilled orders are ~2 days old, placed on 2026-11-04, so nothing is sitting unfulfilled for more than 3 days right now.

**채점**: ✗ 실패 — 빠진 것: fact "none: 412 orders are processing and the oldest was placed We" (412 not shown)
(도구 정밀도 0.89, 재현율 1.00)

### a2api-acom-index · 2회차 · E MODEL_CALL_LIMIT

토큰 119,263 · 62.103초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 6,987토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> any orders sitting unfulfilled for more than 3 days?

1. 모델 → **`a2api_load`** `` {"names":["search_orders","list_enums"]} ``
   ← 결과 41B: `` {"loaded":["search_orders","list_enums"]} ``
2. 모델 → **`list_enums`** `` {"names":["order_status"]} ``
   ← 결과 610B: `` {"status":"succeeded","data":{"items":[{"name":"order_status","applies_to":["analytics.order_summary","catalog.reorder","sales.order_event","sales.order_item","sales.sales_order"],"values":[{"value":"payment_due","label":"Payment due","order":1},{"value":"processing","label":"Processing","order":2},{"value":"in_transit","label":"In transit","order":3},{"value":"delivered","label":"Delivered","order":4},{"value":"returned","label":"Returned","order":5,"terminal":true},{"value":"cancelled","label":"Cancelled","order":6,"terminal":true},{"value":"problem","label":"Needs attention","order":7}]}],"… (+10자) ``
3. 모델 → **`search_orders`** `` {"order_status":["payment_due","processing","problem"],"order_date_to":"2026-11-03","sort":"order_date","limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
4. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"sort":"order_date","limit":100} ``
   ← 결과 4,606B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27860","order_number":"27860","order_status":"processing","customer_id":"cus_m008451","order_date":"2026-11-04T00:09:00-05:00","total":{"value":92.0,"currency":"USD"}},{"id":"ord_27861","order_number":"27861","order_status":"processing","customer_id":"cus_m000912","order_date":"2026-11-04T00:11:00-05:00","total":{"value":89.0,"currency":"USD"}},{"id":"ord_27862","order_number":"27862","order_status":"processing","customer_id":"cus_m013479","order_date":"2026-11-04T00:29:00-05:00","total":{"value":84.0,"currency":"USD"}},{"id":"ord_27863","order… (+900자) ``
5. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_to":"2026-11-02","sort":"order_date","limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
6. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_to":"2026-11-03","order_date_from":"2026-11-01","sort":"order_date","limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
7. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_from":"2026-10-31","order_date_to":"2026-11-03","sort":"order_date","limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
8. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_from":"2026-10-30","order_date_to":"2026-11-03","sort":"order_date","limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
9. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_from":"2026-10-29","order_date_to":"2026-11-03","sort":"order_date","limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
10. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_from":"2026-10-28","order_date_to":"2026-11-03","sort":"order_date","limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
11. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_from":"2026-10-27","order_date_to":"2026-11-03","sort":"order_date","limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
12. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_from":"2026-10-26","order_date_to":"2026-11-03","sort":"order_date","limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "none: 412 orders are processing and the oldest was placed We" (412, 4, 0, 9 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.91, 재현율 1.00)

### a2api-acom-names · 1회차 · ✗ 실패

토큰 24,883 · 72.637초 · 모델 호출 6회 · 도구 호출 5회 · 첫 요청 프롬프트 1,628토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> any orders sitting unfulfilled for more than 3 days?

1. 모델 → **`a2api_load`** `` {"names":["search_orders"]} ``
   ← 결과 28B: `` {"loaded":["search_orders"]} ``
2. 모델 → **`search_orders`** `` {"order_status":["payment_due","processing","problem"],"order_date_to":"2026-11-03","sort":"order_date","limit":100,"fields":["id","order_number","order_status","customer_id","order_date","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
3. 모델 → **`search_orders`** `` {"order_status":["payment_due","processing","problem","in_transit"],"order_date_to":"2026-11-02","sort":"order_date","limit":100,"fields":["id","order_number","order_status","customer_id","order_date","total"]} ``
   ← 결과 4,765B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27184","order_number":"27184","order_status":"in_transit","customer_id":"cus_m005474","order_date":"2026-11-01T00:18:00-04:00","total":{"value":289.0,"currency":"USD"}},{"id":"ord_27185","order_number":"27185","order_status":"in_transit","customer_id":"cus_m004091","order_date":"2026-11-01T00:24:00-04:00","total":{"value":118.0,"currency":"USD"}},{"id":"ord_27186","order_number":"27186","order_status":"in_transit","customer_id":"cus_m006436","order_date":"2026-11-01T00:29:00-04:00","total":{"value":188.0,"currency":"USD"}},{"id":"ord_27187","or… (+900자) ``
4. 모델 → **`search_orders`** `` {"order_status":["in_transit"],"order_date_to":"2026-10-31","sort":"order_date","limit":20,"fields":["id","order_number","order_status","customer_id","order_date","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
5. 모델 → **`search_orders`** `` {"order_status":["payment_due","processing","problem"],"order_date_to":"2026-10-31","sort":"order_date","limit":100,"fields":["id","order_number","order_status","customer_id","order_date","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``

**답변 1**
> No payment_due / processing / problem orders are sitting >3 days old as of Fri 2026-11-06 11:00 America/New_York.
>
> * payment_due, processing, problem with order_date ≤ 2026-11-03: 0 orders found.
>
> If you count **in_transit** as still unfulfilled, there are older shipments:
>
> * in_transit with order_date ≤ 2026-11-02: 469 orders total
> * Oldest in the first page are placed 2026-11-01, e.g.:
>
>   * 27184 – ord_27184 – in_transit – cus_m005474 – 2026-11-01T00:18:00-04:00 – $289.00
>   * 27185 – ord_27185 – in_transit – cus_m004091 – 2026-11-01T00:24:00-04:00 – $118.00
>   * 27186 – ord_27186 – in_transit – cus_m006436 – 2026-11-01T00:29:00-04:00 – $188.00
>   * 27187 – ord_27187 – in_transit – cus_m002124 – 2026-11-01T00:38:00-04:00 – $85.00
>   * 27188 – ord_27188 – in_transit – cus_m005545 – 2026-11-01T00:49:00-04:00 – $119.00
>   * … up to 27208 – ord_27208 – in_transit – cus_m006060 – 2026-11-01T07:02:00-05:00 – $109.00
>
> Those Nov 1 in_transit orders are ~5 days old. No in_transit orders exist with order_date ≤ 2026-10-31.
>
> Want me to pull the full list of the 469 in_transit orders or filter to a specific customer/status?

**채점**: ✗ 실패 — 빠진 것: fact "none: 412 orders are processing and the oldest was placed We" (412, 9 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names · 2회차 · E MODEL_OUTPUT_TRUNCATED

토큰 20,661 · 80.655초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 1,628토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> any orders sitting unfulfilled for more than 3 days?

1. 모델 → **`a2api_load`** `` {"names":["search_orders"]} ``
   ← 결과 28B: `` {"loaded":["search_orders"]} ``
2. 모델 → **`search_orders`** `` {"order_status":["payment_due","processing","problem"],"order_date_to":"2026-11-03","sort":"order_date","limit":100,"fields":["id","order_number","order_status","customer_id","order_date","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
3. 모델 → **`search_orders`** `` {"order_status":["payment_due","processing","problem","in_transit"],"order_date_to":"2026-11-02","sort":"order_date","limit":100,"fields":["id","order_number","order_status","customer_id","order_date","total"]} ``
   ← 결과 4,765B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27184","order_number":"27184","order_status":"in_transit","customer_id":"cus_m005474","order_date":"2026-11-01T00:18:00-04:00","total":{"value":289.0,"currency":"USD"}},{"id":"ord_27185","order_number":"27185","order_status":"in_transit","customer_id":"cus_m004091","order_date":"2026-11-01T00:24:00-04:00","total":{"value":118.0,"currency":"USD"}},{"id":"ord_27186","order_number":"27186","order_status":"in_transit","customer_id":"cus_m006436","order_date":"2026-11-01T00:29:00-04:00","total":{"value":188.0,"currency":"USD"}},{"id":"ord_27187","or… (+900자) ``
4. 모델 → **`search_orders`** `` {"order_status":["payment_due","processing","problem"],"order_date_to":"2026-11-02","sort":"order_date","limit":100,"fields":["id","order_number","order_status","customer_id","order_date","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``

_(모델 출력이 출력 한도에 걸려 중단)_

**채점**: E MODEL_OUTPUT_TRUNCATED — 빠진 것: fact "none: 412 orders are processing and the oldest was placed We" (412, 4, 0, 9 not shown); HOST:MODEL_OUTPUT_TRUNCATED
(도구 정밀도 1.00, 재현율 1.00)
