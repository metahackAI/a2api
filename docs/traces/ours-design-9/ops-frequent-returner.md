# ops-frequent-returner — ours-design-9

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> the customer on 20431 is flagged for returns. how bad is it, should I still refund the overcoat?

- 필요한 도구: `get_return_history`
- 허용 도구: `get_order`, `get_claim`, `get_member`, `search_return_requests`, `get_return_policy`, `evaluate_return_request`
- 답에 있어야 할 사실: customer cus_4431 has 4 returns in the last 90 days: clm_20431 waiting, and 20311, 20324, 20298 already completed
- 답에 있어야 할 사실: the overcoat return itself is inside the window and meets the policy; the history is a reason for a person to decide, not a rule that blocks it
- 부르면 안 됨: refund_return, reject_claim

### a2api-acom-hybrid · 1회차 · ✓ 통과

토큰 24,367 · 24.366초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 3,846토큰

준비: 전략 `index`, 함수 253개, 목차 4,645자(system prompt)

**질문 1**
> the customer on 20431 is flagged for returns. how bad is it, should I still refund the overcoat?

1. 모델 → **`a2api_load`** `` {"names":["get_order","get_return_history","evaluate_return_request"]} ``
   ← 결과 83B: `` {"loaded":["get_order"],"already":["get_return_history","evaluate_return_request"]} ``
2. 모델 → **`get_order`** `` {"order_id":20431,"fields":["id","order_number","customer_id","ordered_item","claims"]} ``
   ← 결과 553B: `` {"status":"succeeded","data":{"id":"ord_20431","order_number":"20431","customer_id":"cus_4431","ordered_item":[{"id":"oln_20431_1","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_m_charcoal","name":"Wool overcoat","size":"M","color":"Charcoal","order_quantity":1,"price":{"value":289.0,"currency":"USD"},"discount":{"value":0.0,"currency":"USD"},"order_item_status":"delivered"}],"claims":[{"id":"clm_20431","claim_type":"return","claim_status":"requested","order_item_ids":["oln_20431_1"],"requested_at":"2026-11-05T16:40:00-05:00"}]}} ``
3. 모델 → **`get_return_history`** `` {"customer_id":"cus_4431","days":90} ``
   ← 결과 1,078B: `` {"status":"succeeded","data":{"items":[{"id":"clm_20431","claim_type":"return","order_id":"ord_20431","order_number":"20431","item":"Wool overcoat","amount":{"value":289.0,"currency":"USD"},"reason":"not_as_described","status":"requested","requested_at":"2026-11-05T16:40:00-05:00"},{"id":"clm_20311","claim_type":"return","order_id":"ord_20311","order_number":"20311","item":"Cashmere sweater","amount":{"value":248.0,"currency":"USD"},"reason":"changed_mind","status":"completed","requested_at":"2026-10-19T12:05:00-04:00"},{"id":"clm_20324","claim_type":"return","order_id":"ord_20324","order_numb… (+478자) ``
4. 모델 → **`evaluate_return_request`** `` {"claim_id":"clm_20431"} ``
   ← 결과 432B: `` {"status":"succeeded","data":{"items":[{"claim_id":"clm_20431","order_number":"20431","suggested":"refund","rule":"defect_refund","rule_text":"Defects are refunded in full, return shipping free","liability":"store_fault","refund_amount":{"value":289.0,"currency":"USD"},"return_fees":"free_return","needs_person":true,"flags":[{"rule":"return_suggestions.flag_return_history","detail":"4 returns in the last 90 days"}]}],"total":1}} ``

**답변 1**
> Order 20431 – cus_4431
> * Claim clm_20431: Wool overcoat M Charcoal, $289.00, status requested, reason not_as_described, requested 2026-11-05T16:40:00-05:00
>
> Return history last 90 days for cus_4431
> * total returns: 4, threshold: 4 → flagged: true
>   * clm_20431 – ord 20431 – Wool overcoat – $289.00 – not_as_described – requested
>   * clm_20311 – ord 20311 – Cashmere sweater – $248.00 – changed_mind – completed 2026-10-19
>   * clm_20324 – ord 20324 – Merino trail tee – $58.00 – wrong_size – completed 2026-10-14
>   * clm_20298 – ord 20298 – Fleece half-zip – $84.00 – wrong_size – completed 2026-10-05
>
> Policy evaluation for clm_20431
> * suggested: refund
> * rule: defect_refund – “Defects are refunded in full, return shipping free”
> * liability: store_fault
> * refund_amount: $289.00 USD
> * return_fees: free_return
> * needs_person: true
> * flags: return_suggestions.flag_return_history – “4 returns in the last 90 days”
>
> The flag is because the customer is at the 4-in-90-days threshold. The current request is a defect / not_as_described case with store fault, so policy still calls for a full refund with free return. The flag is a warning only; it does not block the refund. A person approval is required before the refund can be issued.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-hybrid · 2회차 · ✓ 통과

토큰 24,367 · 24.033초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 3,846토큰

준비: 전략 `index`, 함수 253개, 목차 4,645자(system prompt)

**질문 1**
> the customer on 20431 is flagged for returns. how bad is it, should I still refund the overcoat?

1. 모델 → **`a2api_load`** `` {"names":["get_order","get_return_history","evaluate_return_request"]} ``
   ← 결과 83B: `` {"loaded":["get_order"],"already":["get_return_history","evaluate_return_request"]} ``
2. 모델 → **`get_order`** `` {"order_id":20431,"fields":["id","order_number","customer_id","ordered_item","claims"]} ``
   ← 결과 553B: `` {"status":"succeeded","data":{"id":"ord_20431","order_number":"20431","customer_id":"cus_4431","ordered_item":[{"id":"oln_20431_1","product_id":"prd_wool_overcoat","variant_id":"var_wool_overcoat_m_charcoal","name":"Wool overcoat","size":"M","color":"Charcoal","order_quantity":1,"price":{"value":289.0,"currency":"USD"},"discount":{"value":0.0,"currency":"USD"},"order_item_status":"delivered"}],"claims":[{"id":"clm_20431","claim_type":"return","claim_status":"requested","order_item_ids":["oln_20431_1"],"requested_at":"2026-11-05T16:40:00-05:00"}]}} ``
3. 모델 → **`get_return_history`** `` {"customer_id":"cus_4431","days":90} ``
   ← 결과 1,078B: `` {"status":"succeeded","data":{"items":[{"id":"clm_20431","claim_type":"return","order_id":"ord_20431","order_number":"20431","item":"Wool overcoat","amount":{"value":289.0,"currency":"USD"},"reason":"not_as_described","status":"requested","requested_at":"2026-11-05T16:40:00-05:00"},{"id":"clm_20311","claim_type":"return","order_id":"ord_20311","order_number":"20311","item":"Cashmere sweater","amount":{"value":248.0,"currency":"USD"},"reason":"changed_mind","status":"completed","requested_at":"2026-10-19T12:05:00-04:00"},{"id":"clm_20324","claim_type":"return","order_id":"ord_20324","order_numb… (+478자) ``
4. 모델 → **`evaluate_return_request`** `` {"claim_id":"clm_20431"} ``
   ← 결과 432B: `` {"status":"succeeded","data":{"items":[{"claim_id":"clm_20431","order_number":"20431","suggested":"refund","rule":"defect_refund","rule_text":"Defects are refunded in full, return shipping free","liability":"store_fault","refund_amount":{"value":289.0,"currency":"USD"},"return_fees":"free_return","needs_person":true,"flags":[{"rule":"return_suggestions.flag_return_history","detail":"4 returns in the last 90 days"}]}],"total":1}} ``

**답변 1**
> Order 20431 – cus_4431
> * Claim clm_20431: Wool overcoat M Charcoal, $289.00, status requested, reason not_as_described, requested 2026-11-05T16:40:00-05:00
>
> Return history last 90 days for cus_4431
> * total returns: 4, threshold: 4 → flagged: true
>   * clm_20431 – ord 20431 – Wool overcoat – $289.00 – not_as_described – requested
>   * clm_20311 – ord 20311 – Cashmere sweater – $248.00 – changed_mind – completed 2026-10-19
>   * clm_20324 – ord 20324 – Merino trail tee – $58.00 – wrong_size – completed 2026-10-14
>   * clm_20298 – ord 20298 – Fleece half-zip – $84.00 – wrong_size – completed 2026-10-05
>
> Policy evaluation for clm_20431
> * suggested: refund
> * rule: defect_refund – “Defects are refunded in full, return shipping free”
> * liability: store_fault
> * refund_amount: $289.00 USD
> * return_fees: free_return
> * needs_person: true
> * flags: return_suggestions.flag_return_history – “4 returns in the last 90 days”
>
> The flag is because the customer is at the 4-in-90-days threshold. The current request is a defect / not_as_described case with store fault, so policy still calls for a full refund with free return. The flag is a warning only; it does not block the refund. A person approval is required before the refund can be issued.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)
