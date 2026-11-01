# ops-wismo-tracking-stuck — smoke-index-1

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> customer on order 27184 says tracking hasn't moved since monday. what's going on and what do I tell them

- 필요한 도구: `get_order`, `track_shipment`
- 허용 도구: `get_delivery`, `get_member`, `list_message_templates`
- 답에 있어야 할 사실: UPS 1ZNW271840001, the last scan is picked_up on Mon Nov 2
- 답에 있어야 할 사실: the promised delivery date is today, Fri Nov 6
- 답에 있어야 할 사실: the agent drafts a reply for the operator; it does not send one
- 부르면 안 됨: send_customer_message

### a2api-acom-index · 1회차 · ✓ 통과

토큰 41,571 · 17.961초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 6,996토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> customer on order 27184 says tracking hasn't moved since monday. what's going on and what do I tell them

1. 모델 → **`a2api_load`** `` {"names":["get_order","get_delivery","track_shipment"]} ``
   ← 결과 56B: `` {"loaded":["get_order","get_delivery","track_shipment"]} ``
2. 모델 → **`get_order`** `` {"order_id":27184} ``
   ← 결과 1,095B: `` {"status":"succeeded","data":{"id":"ord_27184","order_number":"27184","order_status":"in_transit","order_date":"2026-11-01T00:18:00-04:00","customer_id":"cus_m005474","ordered_item":[{"id":"oln_27184_1","product_id":"prd_outerwear_01","variant_id":"var_outerwear_01_xl_stone","name":"Waxed cotton duffle coat","size":"XL","color":"Stone","order_quantity":1,"price":{"value":289.0,"currency":"USD"},"discount":{"value":0.0,"currency":"USD"},"order_item_status":"in_transit"}],"delivery":{"id":"dlv_27184","delivery_address":{"name":"Jordan Walsh","postal_code":"02840","address_region":"RI","street_ad… (+495자) ``
3. 모델 → **`get_delivery`** `` {"delivery_id":"dlv_27184"} ``
   ← 결과 400B: `` {"status":"succeeded","data":{"id":"dlv_27184","order_id":"ord_27184","delivery_address":"140 River Rd","tracking_number":"1ZNW271840001","tracking_url":"https://track.example/1ZNW271840001","carrier":"UPS","has_delivery_method":"standard","delivery_state":"in_transit","expected_arrival_until":"2026-11-06","events":[{"at":"2026-11-02T12:43:00-05:00","delivery_state":"picked_up","location":null}]}} ``
4. 모델 → **`track_shipment`** `` {"mode":"delivery","delivery_id":"dlv_27184"} ``
   ← 결과 207B: `` {"status":"succeeded","data":{"items":[{"at":"2026-11-02T12:43:00-05:00","delivery_state":"picked_up","location":null}],"total":1,"delivery_id":"dlv_27184","carrier":"UPS","tracking_number":"1ZNW271840001"}} ``

**답변 1**
> Order 27184 – Waxed cotton duffle coat XL Stone
>
> * Order status: **in_transit**
> * Order date: 2026-11-01
> * Delivery: dlv_27184
> * Carrier: UPS
> * Tracking number: **1ZNW271840001**
> * Tracking URL: https://track.example/1ZNW271840001
> * Delivery address: Jordan Walsh, 140 River Rd, Newport, RI 02840, US
> * Expected arrival until: 2026-11-06
>
> Tracking events on file:
>
> * 2026-11-02 12:43:00 -05:00 – picked_up
>
> That is the only scan we have. The carrier has not posted a new event since Monday 2 Nov. The parcel is still showing as in_transit in our system and the carrier’s expected arrival window is today, 2026-11-06.
>
> What to tell the customer:
> The last confirmed scan is pick-up on Monday 2 Nov at 12:43. No further updates have been posted by UPS since then. The shipment is still marked in transit and is due by end of day 6 Nov. I can share the tracking number 1ZNW271840001 and the tracking link above so they can monitor directly with UPS. If there is still no movement by the expected arrival date, we can open a carrier inquiry on their behalf.
>
> Do you want me to create a service note / inquiry for the customer on this order?

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-graph · 1회차 · ✓ 통과

토큰 42,232 · 26.728초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 6,996토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> customer on order 27184 says tracking hasn't moved since monday. what's going on and what do I tell them

1. 모델 → **`a2api_load`** `` {"names":["get_order","get_delivery","track_shipment"]} ``
   ← 결과 56B: `` {"loaded":["get_order","get_delivery","track_shipment"]} ``
2. 모델 → **`get_order`** `` {"order_id":27184} ``
   ← 결과 1,292B: `` {"status":"succeeded","data":{"id":"ord_27184","order_number":"27184","order_status":"in_transit","order_date":"2026-11-01T00:18:00-04:00","customer_id":"cus_m005474","ordered_item":[{"id":"oln_27184_1","product_id":"prd_outerwear_01","variant_id":"var_outerwear_01_xl_stone","name":"Waxed cotton duffle coat","size":"XL","color":"Stone","order_quantity":1,"price":{"value":289.0,"currency":"USD"},"discount":{"value":0.0,"currency":"USD"},"order_item_status":"in_transit"}],"delivery":{"id":"dlv_27184","delivery_address":{"name":"Jordan Walsh","postal_code":"02840","address_region":"RI","street_ad… (+692자) ``
3. 모델 → **`track_shipment`** `` {"mode":"delivery","delivery_id":"dlv_27184"} ``
   ← 결과 289B: `` {"status":"succeeded","data":{"items":[{"at":"2026-11-02T12:43:00-05:00","delivery_state":"picked_up","location":null}],"total":1,"delivery_id":"dlv_27184","carrier":"UPS","tracking_number":"1ZNW271840001"},"next":"Functions that take IDs from this result: confirm_shipment (delivery_id)"} ``
4. 모델 → **`get_delivery`** `` {"delivery_id":"dlv_27184"} ``
   ← 결과 569B: `` {"status":"succeeded","data":{"id":"dlv_27184","order_id":"ord_27184","delivery_address":"140 River Rd","tracking_number":"1ZNW271840001","tracking_url":"https://track.example/1ZNW271840001","carrier":"UPS","has_delivery_method":"standard","delivery_state":"in_transit","expected_arrival_until":"2026-11-06","events":[{"at":"2026-11-02T12:43:00-05:00","delivery_state":"picked_up","location":null}]},"next":"Functions that take IDs from this result: schedule_shipment, confirm_virtual_account_deposit, cancel_order_lines, send_customer_message, get_payment (order_id)"} ``

**답변 1**
> Order 27184 – ord_27184
>
> * Order status: **in_transit** placed 2026-11-01 00:18 -04:00
> * Delivery dlv_27184 to Jordan Walsh, 140 River Rd, Newport RI 02840
> * Carrier: UPS, tracking 1ZNW271840001
>   tracking URL: https://track.example/1ZNW271840001
> * Delivery state: in_transit
> * Expected arrival until: 2026-11-06 20:00 -05:00 – i.e. today by 8pm ET
>
> Carrier events on file:
> * 2026-11-02 12:43 -05:00 – picked_up
>
> That is the only scan in the system. Monday 2 Nov is the last movement, so the customer’s observation is correct – no further scans since pick-up.
>
> What to tell them:
> The parcel was picked up by UPS on Monday 2 Nov at 12:43 and is still showing in-transit. The current delivery estimate is today, 6 Nov, by 20:00 ET. UPS often has a gap between pick-up and the next facility scan, especially over the weekend. Ask them to monitor the tracking link above until the end of the day; if there is no delivery or a new scan by this evening, have them contact UPS directly with 1ZNW271840001 and we can open a carrier inquiry on their behalf.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names · 1회차 · ✓ 통과

토큰 15,369 · 24.336초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 1,637토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> customer on order 27184 says tracking hasn't moved since monday. what's going on and what do I tell them

1. 모델 → **`a2api_load`** `` {"names":["get_order","get_delivery","track_shipment"]} ``
   ← 결과 56B: `` {"loaded":["get_order","get_delivery","track_shipment"]} ``
2. 모델 → **`get_order`** `` {"order_id":27184} ``
   ← 결과 1,292B: `` {"status":"succeeded","data":{"id":"ord_27184","order_number":"27184","order_status":"in_transit","order_date":"2026-11-01T00:18:00-04:00","customer_id":"cus_m005474","ordered_item":[{"id":"oln_27184_1","product_id":"prd_outerwear_01","variant_id":"var_outerwear_01_xl_stone","name":"Waxed cotton duffle coat","size":"XL","color":"Stone","order_quantity":1,"price":{"value":289.0,"currency":"USD"},"discount":{"value":0.0,"currency":"USD"},"order_item_status":"in_transit"}],"delivery":{"id":"dlv_27184","delivery_address":{"name":"Jordan Walsh","postal_code":"02840","address_region":"RI","street_ad… (+692자) ``
3. 모델 → **`get_delivery`** `` {"delivery_id":"dlv_27184"} ``
   ← 결과 569B: `` {"status":"succeeded","data":{"id":"dlv_27184","order_id":"ord_27184","delivery_address":"140 River Rd","tracking_number":"1ZNW271840001","tracking_url":"https://track.example/1ZNW271840001","carrier":"UPS","has_delivery_method":"standard","delivery_state":"in_transit","expected_arrival_until":"2026-11-06","events":[{"at":"2026-11-02T12:43:00-05:00","delivery_state":"picked_up","location":null}]},"next":"Functions that take IDs from this result: schedule_shipment, confirm_virtual_account_deposit, cancel_order_lines, send_customer_message, get_payment (order_id)"} ``
4. 모델 → **`track_shipment`** `` {"mode":"delivery","delivery_id":"dlv_27184"} ``
   ← 결과 289B: `` {"status":"succeeded","data":{"items":[{"at":"2026-11-02T12:43:00-05:00","delivery_state":"picked_up","location":null}],"total":1,"delivery_id":"dlv_27184","carrier":"UPS","tracking_number":"1ZNW271840001"},"next":"Functions that take IDs from this result: confirm_shipment (delivery_id)"} ``

**답변 1**
> Order 27184 — ord_27184
>
> * Customer: cus_m005474
> * Order status: in_transit
> * Order date: 2026-11-01 00:18 -04:00
> * Line: Waxed cotton duffle coat, XL Stone, prd_outerwear_01 / var_outerwear_01_xl_stone, qty 1, $289.00
> * Payment: credit_card ending 6149, payment_complete
> * Delivery: dlv_27184
>   * Carrier: UPS
>   * Tracking number: 1ZNW271840001
>   * Tracking URL: https://track.example/1ZNW271840001
>   * Delivery address: Jordan Walsh, 140 River Rd, Newport, RI 02840, US
>   * Delivery state: in_transit
>   * Expected arrival until: 2026-11-06 20:00:00 -05:00
>
> Tracking events on file:
>
> * 2026-11-02T12:43:00-05:00 — picked_up
>
> That is the only scan we have. No further carrier events have been recorded since the Monday 2 Nov pick-up. The parcel is still showing in_transit in our system and the carrier ETA remains today, 6 Nov, by 20:00 EST.
>
> What to tell the customer:
> The last confirmed scan is pick-up on Monday 2 Nov at 12:43 EST. UPS has not posted a new scan since then. The order is still marked in transit with an expected arrival window of today, 6 Nov until 8pm EST.
>
> Ask them to keep monitoring the tracking link above. If there is no movement by the end of the expected arrival window today, advise them to contact UPS directly with tracking number 1ZNW271840001 for a live status check, and let us know what UPS reports so we can follow up on the shipment.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)
