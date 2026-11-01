# ops-wismo-tracking-stuck — ours-design-9

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> customer on order 27184 says tracking hasn't moved since monday. what's going on and what do I tell them

- 필요한 도구: `get_order`, `track_shipment`
- 허용 도구: `get_delivery`, `get_member`, `list_message_templates`
- 답에 있어야 할 사실: UPS 1ZNW271840001, the last scan is picked_up on Mon Nov 2
- 답에 있어야 할 사실: the promised delivery date is today, Fri Nov 6
- 답에 있어야 할 사실: the agent drafts a reply for the operator; it does not send one
- 부르면 안 됨: send_customer_message

### a2api-acom-hybrid · 1회차 · ✓ 통과

토큰 39,304 · 27.789초 · 모델 호출 6회 · 도구 호출 5회 · 첫 요청 프롬프트 4,598토큰

준비: 전략 `index`, 함수 253개, 목차 4,645자(system prompt)

**질문 1**
> customer on order 27184 says tracking hasn't moved since monday. what's going on and what do I tell them

1. 모델 → **`a2api_load`** `` {"names":["get_order","search_orders","get_delivery","track_shipment","list_tasks"]} ``
   ← 결과 130B: `` {"loaded":["get_order","search_orders","get_delivery","track_shipment"],"already":["list_tasks"],"evicted":["list_subscriptions"]} ``
2. 모델 → **`get_order`** `` {"order_id":27184} ``
   ← 결과 1,095B: `` {"status":"succeeded","data":{"id":"ord_27184","order_number":"27184","order_status":"in_transit","order_date":"2026-11-01T00:18:00-04:00","customer_id":"cus_m005474","ordered_item":[{"id":"oln_27184_1","product_id":"prd_outerwear_01","variant_id":"var_outerwear_01_xl_stone","name":"Waxed cotton duffle coat","size":"XL","color":"Stone","order_quantity":1,"price":{"value":289.0,"currency":"USD"},"discount":{"value":0.0,"currency":"USD"},"order_item_status":"in_transit"}],"delivery":{"id":"dlv_27184","delivery_address":{"name":"Jordan Walsh","postal_code":"02840","address_region":"RI","street_ad… (+495자) ``
3. 모델 → **`get_delivery`** `` {"delivery_id":"dlv_27184"} ``
   ← 결과 400B: `` {"status":"succeeded","data":{"id":"dlv_27184","order_id":"ord_27184","delivery_address":"140 River Rd","tracking_number":"1ZNW271840001","tracking_url":"https://track.example/1ZNW271840001","carrier":"UPS","has_delivery_method":"standard","delivery_state":"in_transit","expected_arrival_until":"2026-11-06","events":[{"at":"2026-11-02T12:43:00-05:00","delivery_state":"picked_up","location":null}]}} ``
4. 모델 → **`track_shipment`** `` {"mode":"delivery","delivery_id":"dlv_27184"} ``
   ← 결과 207B: `` {"status":"succeeded","data":{"items":[{"at":"2026-11-02T12:43:00-05:00","delivery_state":"picked_up","location":null}],"total":1,"delivery_id":"dlv_27184","carrier":"UPS","tracking_number":"1ZNW271840001"}} ``
5. 모델 → **`list_tasks`** `` {"state":["needs_you","working"]} ``
   ← 결과 1,075B: `` {"status":"succeeded","data":{"items":[{"id":"task_linen_reorder","title":"Linen shirt sells out in about 4 days","state":"needs_you","origin":"agent_noticed","at":"2026-11-06T08:40:00-05:00","summary":"Reorder draft: 3 sizes, 240 units","tag":"inventory","change_set_id":"cs_1041","watcher":"stock_out_forecast","conversation_id":"conv_linen_reorder","updated_at":"2026-11-06T08:40:00-05:00"},{"id":"task_returns_1106","title":"12 return requests over $200 are waiting","state":"working","origin":"agent_noticed","at":"2026-11-06T10:40:00-05:00","summary":"Operations agent is sorting the requests b… (+475자) ``

**답변 1**
> Order 27184 – ord_27184 – is **in_transit**.
>
> * Customer: cus_m005474 – Jordan Walsh, 140 River Rd, Newport RI 02840
> * Item: Waxed cotton duffle coat XL Stone, oln_27184_1 – $289.00 USD
> * Delivery: dlv_27184
>   * Carrier: UPS
>   * Tracking: 1ZNW271840001 – https://track.example/1ZNW271840001
>   * Delivery state: in_transit
>   * Expected arrival until: 2026-11-06 20:00 -05:00
>
> Carrier events on file:
> * 2026-11-02T12:43:00-05:00 – picked_up
>
> That is the only scan. No further UPS events have been reported since the Monday 2 Nov pickup. The parcel is still showing in-transit in our system and the carrier ETA is today, 6 Nov by 8pm ET.
>
> What to tell the customer:
> The tracking currently shows pickup on Monday 2 Nov at 12:43 ET and no subsequent scans. The shipment is still marked in-transit with UPS and is due to arrive today by 8pm ET. Tracking updates can lag 24-48h. Ask them to keep monitoring the tracking link above and to contact UPS directly if there is no movement or delivery by the expected arrival time tonight. We’ll continue to monitor the delivery and will update you if the status changes.

**채점**: ✓ 통과
(도구 정밀도 0.75, 재현율 1.00)

### a2api-acom-hybrid · 2회차 · ✓ 통과

토큰 39,304 · 27.409초 · 모델 호출 6회 · 도구 호출 5회 · 첫 요청 프롬프트 4,598토큰

준비: 전략 `index`, 함수 253개, 목차 4,645자(system prompt)

**질문 1**
> customer on order 27184 says tracking hasn't moved since monday. what's going on and what do I tell them

1. 모델 → **`a2api_load`** `` {"names":["get_order","search_orders","get_delivery","track_shipment","list_tasks"]} ``
   ← 결과 130B: `` {"loaded":["get_order","search_orders","get_delivery","track_shipment"],"already":["list_tasks"],"evicted":["list_subscriptions"]} ``
2. 모델 → **`get_order`** `` {"order_id":27184} ``
   ← 결과 1,095B: `` {"status":"succeeded","data":{"id":"ord_27184","order_number":"27184","order_status":"in_transit","order_date":"2026-11-01T00:18:00-04:00","customer_id":"cus_m005474","ordered_item":[{"id":"oln_27184_1","product_id":"prd_outerwear_01","variant_id":"var_outerwear_01_xl_stone","name":"Waxed cotton duffle coat","size":"XL","color":"Stone","order_quantity":1,"price":{"value":289.0,"currency":"USD"},"discount":{"value":0.0,"currency":"USD"},"order_item_status":"in_transit"}],"delivery":{"id":"dlv_27184","delivery_address":{"name":"Jordan Walsh","postal_code":"02840","address_region":"RI","street_ad… (+495자) ``
3. 모델 → **`get_delivery`** `` {"delivery_id":"dlv_27184"} ``
   ← 결과 400B: `` {"status":"succeeded","data":{"id":"dlv_27184","order_id":"ord_27184","delivery_address":"140 River Rd","tracking_number":"1ZNW271840001","tracking_url":"https://track.example/1ZNW271840001","carrier":"UPS","has_delivery_method":"standard","delivery_state":"in_transit","expected_arrival_until":"2026-11-06","events":[{"at":"2026-11-02T12:43:00-05:00","delivery_state":"picked_up","location":null}]}} ``
4. 모델 → **`track_shipment`** `` {"mode":"delivery","delivery_id":"dlv_27184"} ``
   ← 결과 207B: `` {"status":"succeeded","data":{"items":[{"at":"2026-11-02T12:43:00-05:00","delivery_state":"picked_up","location":null}],"total":1,"delivery_id":"dlv_27184","carrier":"UPS","tracking_number":"1ZNW271840001"}} ``
5. 모델 → **`list_tasks`** `` {"state":["needs_you","working"]} ``
   ← 결과 1,075B: `` {"status":"succeeded","data":{"items":[{"id":"task_linen_reorder","title":"Linen shirt sells out in about 4 days","state":"needs_you","origin":"agent_noticed","at":"2026-11-06T08:40:00-05:00","summary":"Reorder draft: 3 sizes, 240 units","tag":"inventory","change_set_id":"cs_1041","watcher":"stock_out_forecast","conversation_id":"conv_linen_reorder","updated_at":"2026-11-06T08:40:00-05:00"},{"id":"task_returns_1106","title":"12 return requests over $200 are waiting","state":"working","origin":"agent_noticed","at":"2026-11-06T10:40:00-05:00","summary":"Operations agent is sorting the requests b… (+475자) ``

**답변 1**
> Order 27184 – ord_27184 – is **in_transit**.
>
> * Customer: cus_m005474 – Jordan Walsh, 140 River Rd, Newport RI 02840
> * Item: Waxed cotton duffle coat XL Stone, oln_27184_1 – $289.00 USD
> * Delivery: dlv_27184
>   * Carrier: UPS
>   * Tracking: 1ZNW271840001 – https://track.example/1ZNW271840001
>   * Delivery state: in_transit
>   * Expected arrival until: 2026-11-06 20:00 -05:00
>
> Carrier events on file:
> * 2026-11-02T12:43:00-05:00 – picked_up
>
> That is the only scan. No further UPS events have been reported since the Monday 2 Nov pickup. The parcel is still showing in-transit in our system and the carrier ETA is today, 6 Nov by 8pm ET.
>
> What to tell the customer:
> The tracking currently shows pickup on Monday 2 Nov at 12:43 ET and no subsequent scans. The shipment is still marked in-transit with UPS and is due to arrive today by 8pm ET. Tracking updates can lag 24-48h. Ask them to keep monitoring the tracking link above and to contact UPS directly if there is no movement or delivery by the expected arrival time tonight. We’ll continue to monitor the delivery and will update you if the status changes.

**채점**: ✓ 통과
(도구 정밀도 0.75, 재현율 1.00)
