# ops-unfulfilled-3-days — ours-heldout-fix-posthoc-1

[← 실행 묶음](README.md) · 세트 `held_out` · a-commerce `d86a1ff` · a2api `bb2cb7a`

**과업**

> any orders sitting unfulfilled for more than 3 days?

- 필요한 도구: `search_orders`
- 허용 도구: `get_order`
- 답에 있어야 할 사실: none: 412 orders are processing and the oldest was placed Wed Nov 4 00:09

### a2api-acom · 1회차 · ✓ 통과

토큰 100,434 · 58.265초 · 모델 호출 9회 · 도구 호출 10회 · 첫 요청 프롬프트 3,469토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> any orders sitting unfulfilled for more than 3 days?

1. 모델 → **`a2api_search`** `` {"query":"unfulfilled orders pending fulfillment"} ``
   ← 결과 387B: `` {"selected":[{"name":"acom_get_seller_grade","id":"acom.get_seller_grade"},{"name":"acom_sync_claim_status","id":"acom.sync_claim_status"},{"name":"acom_search_orders","id":"acom.search_orders"},{"name":"acom_get_order","id":"acom.get_order"},{"name":"acom_lookup_external_order","id":"acom.lookup_external_order"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"orders unfulfilled"} ``
   ← 결과 391B: `` {"selected":[{"name":"acom_search_orders","id":"acom.search_orders"},{"name":"acom_get_order","id":"acom.get_order"},{"name":"acom_lookup_external_order","id":"acom.lookup_external_order"},{"name":"acom_sync_order_status","id":"acom.sync_order_status"},{"name":"acom_cancel_order_lines","id":"acom.cancel_order_lines"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`a2api_search`** `` {"query":"list orders"} ``
   ← 결과 460B: `` {"selected":[{"name":"acom_list_enums","id":"acom.list_enums"},{"name":"acom_create_event","id":"acom.create_event"},{"name":"acom_list_conditional_gifts","id":"acom.list_conditional_gifts"},{"name":"acom_list_subscriptions","id":"acom.list_subscriptions"},{"name":"acom_list_display_slots","id":"acom.list_display_slots"}],"evicted":["acom_pause_subscription","acom_cancel_subscription"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`acom_list_enums`** `` {"names":["order_status"]} ``
   ← 결과 610B: `` {"status":"succeeded","data":{"items":[{"name":"order_status","applies_to":["analytics.order_summary","catalog.reorder","sales.order_event","sales.order_item","sales.sales_order"],"values":[{"value":"payment_due","label":"Payment due","order":1},{"value":"processing","label":"Processing","order":2},{"value":"in_transit","label":"In transit","order":3},{"value":"delivered","label":"Delivered","order":4},{"value":"returned","label":"Returned","order":5,"terminal":true},{"value":"cancelled","label":"Cancelled","order":6,"terminal":true},{"value":"problem","label":"Needs attention","order":7}]}],"… (+10자) ``
5. 모델 → **`acom_search_orders`** `` {"order_status":["processing"],"order_date_to":"2026-11-02","sort":"order_date","limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
6. 모델 → **`acom_search_orders`** `` {"order_status":["processing"],"order_date_to":"2026-11-03","sort":"order_date","limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
7. 모델 → **`acom_search_orders`** `` {"order_status":["processing"],"limit":100,"sort":"order_date"} ``
   ← 결과 4,606B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27860","order_number":"27860","order_status":"processing","customer_id":"cus_m008451","order_date":"2026-11-04T00:09:00-05:00","total":{"value":92.0,"currency":"USD"}},{"id":"ord_27861","order_number":"27861","order_status":"processing","customer_id":"cus_m000912","order_date":"2026-11-04T00:11:00-05:00","total":{"value":89.0,"currency":"USD"}},{"id":"ord_27862","order_number":"27862","order_status":"processing","customer_id":"cus_m013479","order_date":"2026-11-04T00:29:00-05:00","total":{"value":84.0,"currency":"USD"}},{"id":"ord_27863","order… (+900자) ``
8. 모델 → **`acom_search_orders`** `` {"order_status":["payment_due"],"order_date_to":"2026-11-02","sort":"order_date","limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
9. 모델 → **`acom_search_orders`** `` {"order_status":["payment_due"],"limit":100,"sort":"order_date"} ``
   ← 결과 407B: `` {"status":"succeeded","data":{"items":[{"id":"ord_29001","order_number":"29001","order_status":"payment_due","customer_id":"cus_priya","order_date":"2026-11-05T16:20:00-05:00","total":{"value":128.0,"currency":"USD"}},{"id":"ord_29002","order_number":"29002","order_status":"payment_due","customer_id":"cus_owen","order_date":"2026-11-06T09:05:00-05:00","total":{"value":89.0,"currency":"USD"}}],"total":2}} ``
10. 모델 → **`acom_search_orders`** `` {"order_status":["problem"],"limit":100,"sort":"order_date"} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``

**답변 1**
> No. There are no unfulfilled orders that have been sitting >3 days as of Fri 2026-11-06 11:00 America/New_York.
>
> Unfulfilled statuses checked:
> * **processing** – 412 orders total
>   * Oldest in the set: ord_27860 #27860 placed 2026-11-04T00:09-05:00, $92.00
>   * Next: ord_27861 #27861 2026-11-04T00:11-05:00, $89.00
>   * … all 412 are from 2026-11-04 onward
>   * Search for processing with order_date_to ≤ 2026-11-02 and ≤ 2026-11-03 returns 0 items
>   * The oldest processing order is ~2.5 days old, i.e. <3 days
>
> * **payment_due** – 2 orders total
>   * ord_29001 #29001 2026-11-05T16:20-05:00, $128.00
>   * ord_29002 #29002 2026-11-06T09:05-05:00, $89.00
>   * No payment_due orders older than 3 days
>
> * **problem / Needs attention** – 0 orders
>
> So the current unfulfilled backlog is limited to the 412 processing orders placed on 2026-11-04 and the two payment_due orders from 2026-11-05/06. Nothing is >3 days old.

**채점**: ✓ 통과
(도구 정밀도 0.86, 재현율 1.00)

### a2api-acom · 2회차 · ✓ 통과

토큰 100,434 · 57.452초 · 모델 호출 9회 · 도구 호출 10회 · 첫 요청 프롬프트 3,469토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> any orders sitting unfulfilled for more than 3 days?

1. 모델 → **`a2api_search`** `` {"query":"unfulfilled orders pending fulfillment"} ``
   ← 결과 387B: `` {"selected":[{"name":"acom_get_seller_grade","id":"acom.get_seller_grade"},{"name":"acom_sync_claim_status","id":"acom.sync_claim_status"},{"name":"acom_search_orders","id":"acom.search_orders"},{"name":"acom_get_order","id":"acom.get_order"},{"name":"acom_lookup_external_order","id":"acom.lookup_external_order"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"orders unfulfilled"} ``
   ← 결과 391B: `` {"selected":[{"name":"acom_search_orders","id":"acom.search_orders"},{"name":"acom_get_order","id":"acom.get_order"},{"name":"acom_lookup_external_order","id":"acom.lookup_external_order"},{"name":"acom_sync_order_status","id":"acom.sync_order_status"},{"name":"acom_cancel_order_lines","id":"acom.cancel_order_lines"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`a2api_search`** `` {"query":"list orders"} ``
   ← 결과 460B: `` {"selected":[{"name":"acom_list_enums","id":"acom.list_enums"},{"name":"acom_create_event","id":"acom.create_event"},{"name":"acom_list_conditional_gifts","id":"acom.list_conditional_gifts"},{"name":"acom_list_subscriptions","id":"acom.list_subscriptions"},{"name":"acom_list_display_slots","id":"acom.list_display_slots"}],"evicted":["acom_pause_subscription","acom_cancel_subscription"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`acom_list_enums`** `` {"names":["order_status"]} ``
   ← 결과 610B: `` {"status":"succeeded","data":{"items":[{"name":"order_status","applies_to":["analytics.order_summary","catalog.reorder","sales.order_event","sales.order_item","sales.sales_order"],"values":[{"value":"payment_due","label":"Payment due","order":1},{"value":"processing","label":"Processing","order":2},{"value":"in_transit","label":"In transit","order":3},{"value":"delivered","label":"Delivered","order":4},{"value":"returned","label":"Returned","order":5,"terminal":true},{"value":"cancelled","label":"Cancelled","order":6,"terminal":true},{"value":"problem","label":"Needs attention","order":7}]}],"… (+10자) ``
5. 모델 → **`acom_search_orders`** `` {"order_status":["processing"],"order_date_to":"2026-11-02","sort":"order_date","limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
6. 모델 → **`acom_search_orders`** `` {"order_status":["processing"],"order_date_to":"2026-11-03","sort":"order_date","limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
7. 모델 → **`acom_search_orders`** `` {"order_status":["processing"],"limit":100,"sort":"order_date"} ``
   ← 결과 4,606B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27860","order_number":"27860","order_status":"processing","customer_id":"cus_m008451","order_date":"2026-11-04T00:09:00-05:00","total":{"value":92.0,"currency":"USD"}},{"id":"ord_27861","order_number":"27861","order_status":"processing","customer_id":"cus_m000912","order_date":"2026-11-04T00:11:00-05:00","total":{"value":89.0,"currency":"USD"}},{"id":"ord_27862","order_number":"27862","order_status":"processing","customer_id":"cus_m013479","order_date":"2026-11-04T00:29:00-05:00","total":{"value":84.0,"currency":"USD"}},{"id":"ord_27863","order… (+900자) ``
8. 모델 → **`acom_search_orders`** `` {"order_status":["payment_due"],"order_date_to":"2026-11-02","sort":"order_date","limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
9. 모델 → **`acom_search_orders`** `` {"order_status":["payment_due"],"limit":100,"sort":"order_date"} ``
   ← 결과 407B: `` {"status":"succeeded","data":{"items":[{"id":"ord_29001","order_number":"29001","order_status":"payment_due","customer_id":"cus_priya","order_date":"2026-11-05T16:20:00-05:00","total":{"value":128.0,"currency":"USD"}},{"id":"ord_29002","order_number":"29002","order_status":"payment_due","customer_id":"cus_owen","order_date":"2026-11-06T09:05:00-05:00","total":{"value":89.0,"currency":"USD"}}],"total":2}} ``
10. 모델 → **`acom_search_orders`** `` {"order_status":["problem"],"limit":100,"sort":"order_date"} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``

**답변 1**
> No. There are no unfulfilled orders that have been sitting >3 days as of Fri 2026-11-06 11:00 America/New_York.
>
> Unfulfilled statuses checked:
> * **processing** – 412 orders total
>   * Oldest in the set: ord_27860 #27860 placed 2026-11-04T00:09-05:00, $92.00
>   * Next: ord_27861 #27861 2026-11-04T00:11-05:00, $89.00
>   * … all 412 are from 2026-11-04 onward
>   * Search for processing with order_date_to ≤ 2026-11-02 and ≤ 2026-11-03 returns 0 items
>   * The oldest processing order is ~2.5 days old, i.e. <3 days
>
> * **payment_due** – 2 orders total
>   * ord_29001 #29001 2026-11-05T16:20-05:00, $128.00
>   * ord_29002 #29002 2026-11-06T09:05-05:00, $89.00
>   * No payment_due orders older than 3 days
>
> * **problem / Needs attention** – 0 orders
>
> So the current unfulfilled backlog is limited to the 412 processing orders placed on 2026-11-04 and the two payment_due orders from 2026-11-05/06. Nothing is >3 days old.

**채점**: ✓ 통과
(도구 정밀도 0.86, 재현율 1.00)

### a2api-acom-names-norelated · 1회차 · E MODEL_CALL_LIMIT

토큰 97,256 · 101.507초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 1,982토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> any orders sitting unfulfilled for more than 3 days?

1. 모델 → **`a2api_load`** `` {"names":["search_orders","get_order"]} ``
   ← 결과 40B: `` {"loaded":["search_orders","get_order"]} ``
2. 모델 → **`search_orders`** `` {"order_status":["payment_due","processing","in_transit","problem"],"order_date_to":"2026-11-02","sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 4,608B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27184","order_number":"27184","order_status":"in_transit","customer_id":"cus_m005474","order_date":"2026-11-01T00:18:00-04:00","total":{"value":289.0,"currency":"USD"}},{"id":"ord_27185","order_number":"27185","order_status":"in_transit","customer_id":"cus_m004091","order_date":"2026-11-01T00:24:00-04:00","total":{"value":118.0,"currency":"USD"}},{"id":"ord_27186","order_number":"27186","order_status":"in_transit","customer_id":"cus_m006436","order_date":"2026-11-01T00:29:00-04:00","total":{"value":188.0,"currency":"USD"}},{"id":"ord_27187","or… (+900자) ``
3. 모델 → **`search_orders`** `` {"order_status":["payment_due","processing","problem"],"order_date_to":"2026-11-03","sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
4. 모델 → **`search_orders`** `` {"order_status":["payment_due","processing","problem"],"order_date_to":"2026-11-04","sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 4,606B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27860","order_number":"27860","order_status":"processing","customer_id":"cus_m008451","order_date":"2026-11-04T00:09:00-05:00","total":{"value":92.0,"currency":"USD"}},{"id":"ord_27861","order_number":"27861","order_status":"processing","customer_id":"cus_m000912","order_date":"2026-11-04T00:11:00-05:00","total":{"value":89.0,"currency":"USD"}},{"id":"ord_27862","order_number":"27862","order_status":"processing","customer_id":"cus_m013479","order_date":"2026-11-04T00:29:00-05:00","total":{"value":84.0,"currency":"USD"}},{"id":"ord_27863","order… (+900자) ``
5. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_to":"2026-11-02","sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
6. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_to":"2026-11-03","sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
7. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_to":"2026-11-04","sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 4,606B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27860","order_number":"27860","order_status":"processing","customer_id":"cus_m008451","order_date":"2026-11-04T00:09:00-05:00","total":{"value":92.0,"currency":"USD"}},{"id":"ord_27861","order_number":"27861","order_status":"processing","customer_id":"cus_m000912","order_date":"2026-11-04T00:11:00-05:00","total":{"value":89.0,"currency":"USD"}},{"id":"ord_27862","order_number":"27862","order_status":"processing","customer_id":"cus_m013479","order_date":"2026-11-04T00:29:00-05:00","total":{"value":84.0,"currency":"USD"}},{"id":"ord_27863","order… (+900자) ``
8. 모델 → **`search_orders`** `` {"order_status":["in_transit"],"order_date_to":"2026-11-03","sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 4,608B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27184","order_number":"27184","order_status":"in_transit","customer_id":"cus_m005474","order_date":"2026-11-01T00:18:00-04:00","total":{"value":289.0,"currency":"USD"}},{"id":"ord_27185","order_number":"27185","order_status":"in_transit","customer_id":"cus_m004091","order_date":"2026-11-01T00:24:00-04:00","total":{"value":118.0,"currency":"USD"}},{"id":"ord_27186","order_number":"27186","order_status":"in_transit","customer_id":"cus_m006436","order_date":"2026-11-01T00:29:00-04:00","total":{"value":188.0,"currency":"USD"}},{"id":"ord_27187","or… (+900자) ``
9. 모델 → **`search_orders`** `` {"order_status":["problem"],"order_date_to":"2026-11-03","sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
10. 모델 → **`search_orders`** `` {"order_status":["in_transit"],"order_date_to":"2026-11-02","sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 4,608B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27184","order_number":"27184","order_status":"in_transit","customer_id":"cus_m005474","order_date":"2026-11-01T00:18:00-04:00","total":{"value":289.0,"currency":"USD"}},{"id":"ord_27185","order_number":"27185","order_status":"in_transit","customer_id":"cus_m004091","order_date":"2026-11-01T00:24:00-04:00","total":{"value":118.0,"currency":"USD"}},{"id":"ord_27186","order_number":"27186","order_status":"in_transit","customer_id":"cus_m006436","order_date":"2026-11-01T00:29:00-04:00","total":{"value":188.0,"currency":"USD"}},{"id":"ord_27187","or… (+900자) ``
11. 모델 → **`search_orders`** `` {"order_status":["in_transit"],"order_date_to":"2026-10-31","sort":"order_date","limit":10,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
12. 모델 → **`search_orders`** `` {"order_status":["in_transit"],"order_date_to":"2026-11-01","sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","customer_id","total"]} ``
   ← 결과 4,608B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27184","order_number":"27184","order_status":"in_transit","customer_id":"cus_m005474","order_date":"2026-11-01T00:18:00-04:00","total":{"value":289.0,"currency":"USD"}},{"id":"ord_27185","order_number":"27185","order_status":"in_transit","customer_id":"cus_m004091","order_date":"2026-11-01T00:24:00-04:00","total":{"value":118.0,"currency":"USD"}},{"id":"ord_27186","order_number":"27186","order_status":"in_transit","customer_id":"cus_m006436","order_date":"2026-11-01T00:29:00-04:00","total":{"value":188.0,"currency":"USD"}},{"id":"ord_27187","or… (+900자) ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "none: 412 orders are processing and the oldest was placed We" (412, 4, 0, 9 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-norelated · 2회차 · E MODEL_CALL_LIMIT

토큰 70,595 · 105.986초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 1,982토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> any orders sitting unfulfilled for more than 3 days?

1. 모델 → **`a2api_load`** `` {"names":["sales › order: search_orders","sales › order: get_order"]} ``
   ← 결과 40B: `` {"loaded":["search_orders","get_order"]} ``
2. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_to":"2026-11-03","sort":"order_date","limit":100,"fields":["id","order_number","order_status","customer_id","order_date","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
3. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_to":"2026-11-02","sort":"order_date","limit":100,"fields":["id","order_number","order_status","customer_id","order_date","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
4. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_to":"2026-11-01","sort":"order_date","limit":100,"fields":["id","order_number","order_status","customer_id","order_date","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
5. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_to":"2026-10-31","sort":"order_date","limit":100,"fields":["id","order_number","order_status","customer_id","order_date","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
6. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"sort":"order_date","limit":100,"fields":["id","order_number","order_status","customer_id","order_date","total"]} ``
   ← 결과 4,606B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27860","order_number":"27860","order_status":"processing","customer_id":"cus_m008451","order_date":"2026-11-04T00:09:00-05:00","total":{"value":92.0,"currency":"USD"}},{"id":"ord_27861","order_number":"27861","order_status":"processing","customer_id":"cus_m000912","order_date":"2026-11-04T00:11:00-05:00","total":{"value":89.0,"currency":"USD"}},{"id":"ord_27862","order_number":"27862","order_status":"processing","customer_id":"cus_m013479","order_date":"2026-11-04T00:29:00-05:00","total":{"value":84.0,"currency":"USD"}},{"id":"ord_27863","order… (+900자) ``
7. 모델 → **`search_orders`** `` {"order_status":["in_transit"],"order_date_to":"2026-11-02","sort":"order_date","limit":100,"fields":["id","order_number","order_status","customer_id","order_date","total"]} ``
   ← 결과 4,608B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27184","order_number":"27184","order_status":"in_transit","customer_id":"cus_m005474","order_date":"2026-11-01T00:18:00-04:00","total":{"value":289.0,"currency":"USD"}},{"id":"ord_27185","order_number":"27185","order_status":"in_transit","customer_id":"cus_m004091","order_date":"2026-11-01T00:24:00-04:00","total":{"value":118.0,"currency":"USD"}},{"id":"ord_27186","order_number":"27186","order_status":"in_transit","customer_id":"cus_m006436","order_date":"2026-11-01T00:29:00-04:00","total":{"value":188.0,"currency":"USD"}},{"id":"ord_27187","or… (+900자) ``
8. 모델 → **`search_orders`** `` {"order_status":["problem"],"sort":"order_date","limit":100,"fields":["id","order_number","order_status","customer_id","order_date","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
9. 모델 → **`search_orders`** `` {"order_status":["payment_due"],"sort":"order_date","limit":100,"fields":["id","order_number","order_status","customer_id","order_date","total"]} ``
   ← 결과 407B: `` {"status":"succeeded","data":{"items":[{"id":"ord_29001","order_number":"29001","order_status":"payment_due","customer_id":"cus_priya","order_date":"2026-11-05T16:20:00-05:00","total":{"value":128.0,"currency":"USD"}},{"id":"ord_29002","order_number":"29002","order_status":"payment_due","customer_id":"cus_owen","order_date":"2026-11-06T09:05:00-05:00","total":{"value":89.0,"currency":"USD"}}],"total":2}} ``
10. 모델 → **`get_order`** `` {"order_id":"ord_27184","fields":["id","order_number","order_status","order_date","delivery","totals"]} ``
   ← 결과 614B: `` {"status":"succeeded","data":{"id":"ord_27184","order_number":"27184","order_status":"in_transit","order_date":"2026-11-01T00:18:00-04:00","delivery":{"id":"dlv_27184","delivery_address":{"name":"Jordan Walsh","postal_code":"02840","address_region":"RI","street_address":"140 River Rd","address_country":"US","address_locality":"Newport"},"expected_arrival_until":"2026-11-06T20:00:00-05:00","delivery_state":"in_transit","delivered_at":null},"totals":{"subtotal":{"value":289.0,"currency":"USD"},"discounts":[],"shipping":{"value":0.0,"currency":"USD"},"gift_wrap":null,"total":{"value":289.0,"curre… (+14자) ``
11. 모델 → **`get_order`** `` {"order_id":"ord_27185","fields":["id","order_number","order_status","order_date","delivery","totals"]} ``
   ← 결과 616B: `` {"status":"succeeded","data":{"id":"ord_27185","order_number":"27185","order_status":"in_transit","order_date":"2026-11-01T00:24:00-04:00","delivery":{"id":"dlv_27185","delivery_address":{"name":"Kendall Silva","postal_code":"17602","address_region":"PA","street_address":"577 High St","address_country":"US","address_locality":"Lancaster"},"expected_arrival_until":"2026-11-06T20:00:00-05:00","delivery_state":"in_transit","delivered_at":null},"totals":{"subtotal":{"value":118.0,"currency":"USD"},"discounts":[],"shipping":{"value":0.0,"currency":"USD"},"gift_wrap":null,"total":{"value":118.0,"cur… (+16자) ``
12. 모델 → **`get_order`** `` {"order_id":"ord_27186","fields":["id","order_number","order_status","order_date","delivery","totals"]} ``
   ← 결과 612B: `` {"status":"succeeded","data":{"id":"ord_27186","order_number":"27186","order_status":"in_transit","order_date":"2026-11-01T00:29:00-04:00","delivery":{"id":"dlv_27186","delivery_address":{"name":"Logan Khan","postal_code":"07102","address_region":"NJ","street_address":"269 Spring St","address_country":"US","address_locality":"Newark"},"expected_arrival_until":"2026-11-06T20:00:00-05:00","delivery_state":"in_transit","delivered_at":null},"totals":{"subtotal":{"value":188.0,"currency":"USD"},"discounts":[],"shipping":{"value":0.0,"currency":"USD"},"gift_wrap":null,"total":{"value":188.0,"currenc… (+12자) ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "none: 412 orders are processing and the oldest was placed We" (412, 4, 0, 9 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-batch · 1회차 · E TURN_TIMEOUT

토큰 65,281 · 120.097초 · 모델 호출 10회 · 도구 호출 10회 · 첫 요청 프롬프트 1,982토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> any orders sitting unfulfilled for more than 3 days?

1. 모델 → **`a2api_load`** `` {"names":["search_orders","get_order"]} ``
   ← 결과 40B: `` {"loaded":["search_orders","get_order"]} ``
2. 모델 → **`search_orders`** `` {"order_status":["payment_due","processing","problem"],"order_date_to":"2026-11-03","sort":"order_date","limit":100,"fields":["id","order_number","order_status","customer_id","order_date","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
3. 모델 → **`search_orders`** `` {"order_status":["payment_due","processing","in_transit","problem"],"order_date_to":"2026-11-02","sort":"order_date","limit":100,"fields":["id","order_number","order_status","customer_id","order_date","total"]} ``
   ← 결과 4,608B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27184","order_number":"27184","order_status":"in_transit","customer_id":"cus_m005474","order_date":"2026-11-01T00:18:00-04:00","total":{"value":289.0,"currency":"USD"}},{"id":"ord_27185","order_number":"27185","order_status":"in_transit","customer_id":"cus_m004091","order_date":"2026-11-01T00:24:00-04:00","total":{"value":118.0,"currency":"USD"}},{"id":"ord_27186","order_number":"27186","order_status":"in_transit","customer_id":"cus_m006436","order_date":"2026-11-01T00:29:00-04:00","total":{"value":188.0,"currency":"USD"}},{"id":"ord_27187","or… (+900자) ``
4. 모델 → **`search_orders`** `` {"order_status":["payment_due","processing","in_transit","problem"],"order_date_to":"2026-11-03","sort":"order_date","limit":100,"fields":["id","order_number","order_status","customer_id","order_date","total"]} ``
   ← 결과 4,608B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27184","order_number":"27184","order_status":"in_transit","customer_id":"cus_m005474","order_date":"2026-11-01T00:18:00-04:00","total":{"value":289.0,"currency":"USD"}},{"id":"ord_27185","order_number":"27185","order_status":"in_transit","customer_id":"cus_m004091","order_date":"2026-11-01T00:24:00-04:00","total":{"value":118.0,"currency":"USD"}},{"id":"ord_27186","order_number":"27186","order_status":"in_transit","customer_id":"cus_m006436","order_date":"2026-11-01T00:29:00-04:00","total":{"value":188.0,"currency":"USD"}},{"id":"ord_27187","or… (+900자) ``
5. 모델 → **`search_orders`** `` {"order_status":["processing"],"order_date_to":"2026-11-03","sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
6. 모델 → **`search_orders`** `` {"order_status":["payment_due","processing","problem"],"order_date_to":"2026-11-03","sort":"order_date","limit":100,"fields":["id","order_number","order_status","customer_id","order_date","total"]} ``
   ← 결과 160B: `` {"status":"succeeded","data":{"items":[],"total":0},"note":"Same call and result as 1 earlier time(s); you already have this data. Use it, or answer the user."} ``
7. 모델 → **`get_order`** `` {"order_id":"ord_27184","fields":["id","order_number","order_status","order_date","customer_id","totals"]} ``
   ← 결과 338B: `` {"status":"succeeded","data":{"id":"ord_27184","order_number":"27184","order_status":"in_transit","order_date":"2026-11-01T00:18:00-04:00","customer_id":"cus_m005474","totals":{"subtotal":{"value":289.0,"currency":"USD"},"discounts":[],"shipping":{"value":0.0,"currency":"USD"},"gift_wrap":null,"total":{"value":289.0,"currency":"USD"}}}} ``
8. 모델 → **`search_orders`** `` {"order_status":["problem"],"order_date_to":"2026-11-03","sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
9. 모델 → **`search_orders`** `` {"order_status":["payment_due"],"order_date_to":"2026-11-03","sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","total"]} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
10. 모델 → **`search_orders`** `` {"order_status":["in_transit"],"order_date_from":"2026-11-02","order_date_to":"2026-11-02","sort":"order_date","limit":100,"fields":["id","order_number","order_status","order_date","total"]} ``
   ← 결과 3,908B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27454","order_number":"27454","order_status":"in_transit","order_date":"2026-11-02T00:04:00-05:00","total":{"value":84.0,"currency":"USD"}},{"id":"ord_27455","order_number":"27455","order_status":"in_transit","order_date":"2026-11-02T00:20:00-05:00","total":{"value":189.0,"currency":"USD"}},{"id":"ord_27456","order_number":"27456","order_status":"in_transit","order_date":"2026-11-02T00:46:00-05:00","total":{"value":72.0,"currency":"USD"}},{"id":"ord_27457","order_number":"27457","order_status":"in_transit","order_date":"2026-11-02T00:50:00-05:0… (+900자) ``

_(한 턴의 시간 한도(120초)에 걸려 중단)_

**채점**: E TURN_TIMEOUT — 빠진 것: fact "none: 412 orders are processing and the oldest was placed We" (412, 4, 0, 9 not shown); HOST:TURN_TIMEOUT
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-batch · 2회차 · E MODEL_CALL_LIMIT

토큰 79,362 · 99.463초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 1,982토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> any orders sitting unfulfilled for more than 3 days?

1. 모델 → **`a2api_load`** `` {"names":["search_orders","get_order"]} ``
   ← 결과 40B: `` {"loaded":["search_orders","get_order"]} ``
2. 모델 → **`search_orders`** `` {"order_status":["payment_due","processing"],"order_date_to":"2026-11-03","sort":"-order_date","limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
3. 모델 → **`search_orders`** `` {"order_status":["payment_due","processing","in_transit"],"order_date_to":"2026-11-02","sort":"-order_date","limit":100} ``
   ← 결과 4,600B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27652","order_number":"27652","order_status":"in_transit","customer_id":"cus_m003766","order_date":"2026-11-02T23:57:00-05:00","total":{"value":30.0,"currency":"USD"}},{"id":"ord_27651","order_number":"27651","order_status":"in_transit","customer_id":"cus_m012620","order_date":"2026-11-02T23:47:00-05:00","total":{"value":30.0,"currency":"USD"}},{"id":"ord_27650","order_number":"27650","order_status":"in_transit","customer_id":"cus_m007655","order_date":"2026-11-02T23:45:00-05:00","total":{"value":32.0,"currency":"USD"}},{"id":"ord_27649","order… (+900자) ``
4. 모델 → **`search_orders`** `` {"order_status":["processing"],"order_date_to":"2026-11-03","sort":"-order_date","limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
5. 모델 → **`search_orders`** `` {"order_status":["payment_due"],"order_date_to":"2026-11-03","sort":"-order_date","limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
6. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due"],"order_date_from":"2026-10-30","order_date_to":"2026-11-03","sort":"order_date","limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
7. 모델 → **`search_orders`** `` {"order_status":["in_transit"],"order_date_to":"2026-11-03","sort":"order_date","limit":100} ``
   ← 결과 4,608B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27184","order_number":"27184","order_status":"in_transit","customer_id":"cus_m005474","order_date":"2026-11-01T00:18:00-04:00","total":{"value":289.0,"currency":"USD"}},{"id":"ord_27185","order_number":"27185","order_status":"in_transit","customer_id":"cus_m004091","order_date":"2026-11-01T00:24:00-04:00","total":{"value":118.0,"currency":"USD"}},{"id":"ord_27186","order_number":"27186","order_status":"in_transit","customer_id":"cus_m006436","order_date":"2026-11-01T00:29:00-04:00","total":{"value":188.0,"currency":"USD"}},{"id":"ord_27187","or… (+900자) ``
8. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_to":"2026-11-03","sort":"order_date","limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
9. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"sort":"order_date","limit":100} ``
   ← 결과 4,606B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27860","order_number":"27860","order_status":"processing","customer_id":"cus_m008451","order_date":"2026-11-04T00:09:00-05:00","total":{"value":92.0,"currency":"USD"}},{"id":"ord_27861","order_number":"27861","order_status":"processing","customer_id":"cus_m000912","order_date":"2026-11-04T00:11:00-05:00","total":{"value":89.0,"currency":"USD"}},{"id":"ord_27862","order_number":"27862","order_status":"processing","customer_id":"cus_m013479","order_date":"2026-11-04T00:29:00-05:00","total":{"value":84.0,"currency":"USD"}},{"id":"ord_27863","order… (+900자) ``
10. 모델 → **`get_order`** `` {"order_id":"ord_27184","fields":["id","order_number","order_status","order_date","customer_id","totals"]} ``
   ← 결과 338B: `` {"status":"succeeded","data":{"id":"ord_27184","order_number":"27184","order_status":"in_transit","order_date":"2026-11-01T00:18:00-04:00","customer_id":"cus_m005474","totals":{"subtotal":{"value":289.0,"currency":"USD"},"discounts":[],"shipping":{"value":0.0,"currency":"USD"},"gift_wrap":null,"total":{"value":289.0,"currency":"USD"}}}} ``
11. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_to":"2026-11-02","sort":"order_date","limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
12. 모델 → **`search_orders`** `` {"order_status":["processing","payment_due","problem"],"order_date_from":"2026-10-28","order_date_to":"2026-11-06","sort":"order_date","limit":100} ``
   ← 결과 4,606B: `` {"status":"succeeded","data":{"items":[{"id":"ord_27860","order_number":"27860","order_status":"processing","customer_id":"cus_m008451","order_date":"2026-11-04T00:09:00-05:00","total":{"value":92.0,"currency":"USD"}},{"id":"ord_27861","order_number":"27861","order_status":"processing","customer_id":"cus_m000912","order_date":"2026-11-04T00:11:00-05:00","total":{"value":89.0,"currency":"USD"}},{"id":"ord_27862","order_number":"27862","order_status":"processing","customer_id":"cus_m013479","order_date":"2026-11-04T00:29:00-05:00","total":{"value":84.0,"currency":"USD"}},{"id":"ord_27863","order… (+900자) ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "none: 412 orders are processing and the oldest was placed We" (412, 4, 0, 9 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 1.00, 재현율 1.00)
