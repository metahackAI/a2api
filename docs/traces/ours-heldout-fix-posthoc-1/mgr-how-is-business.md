# mgr-how-is-business — ours-heldout-fix-posthoc-1

[← 실행 묶음](README.md) · 세트 `held_out` · a-commerce `d86a1ff` · a2api `bb2cb7a`

**과업**

> How is my business doing?

- 필요한 도구: `get_sales_overview`
- 허용 도구: `get_sales_trend`, `explain_sales_change`, `get_customer_overview`, `list_tasks`
- 답에 있어야 할 사실: yesterday (Thu Nov 5) was $18,240, 20% under the Thursday average; the agent leads with that and its causes

### a2api-acom · 1회차 · ✗ 실패

토큰 14,037 · 12.917초 · 모델 호출 2회 · 도구 호출 3회 · 첫 요청 프롬프트 3,838토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> How is my business doing?

1. 모델 → **`a2api_search`** `` {"query":"business performance metrics"} ``
   ← 결과 379B: `` {"selected":[{"name":"acom_verify_business","id":"acom.verify_business"},{"name":"acom_get_seller_grade","id":"acom.get_seller_grade"},{"name":"acom_update_seller","id":"acom.update_seller"},{"name":"acom_issue_receipt","id":"acom.issue_receipt"},{"name":"acom_verify_identity","id":"acom.verify_identity"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"seller performance"} ``
   ← 결과 369B: `` {"selected":[{"name":"acom_update_seller","id":"acom.update_seller"},{"name":"acom_set_seller_grade","id":"acom.set_seller_grade"},{"name":"acom_get_seller","id":"acom.get_seller"},{"name":"acom_search_sellers","id":"acom.search_sellers"},{"name":"acom_onboard_seller","id":"acom.onboard_seller"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`a2api_search`** `` {"query":"business sales"} ``
   ← 결과 401B: `` {"selected":[{"name":"acom_verify_business","id":"acom.verify_business"},{"name":"acom_get_sales_trend","id":"acom.get_sales_trend"},{"name":"acom_get_sales_overview","id":"acom.get_sales_overview"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_explain_sales_change","id":"acom.explain_sales_change"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``

**답변 1**
> To check how your business is doing I need to identify it first.
>
> Could you provide your business legal name, tax ID, or seller ID? Once I have that I can pull your seller grade, sales overview/trend and recent performance metrics.

**채점**: ✗ 실패 — 빠진 것: tool get_sales_overview; fact "yesterday (Thu Nov 5) was $18,240, 20% under the Thursday av" (5, 18240, 20 not shown)
(도구 정밀도 —, 재현율 0.00)

### a2api-acom · 2회차 · ✗ 실패

토큰 14,111 · 14.03초 · 모델 호출 2회 · 도구 호출 3회 · 첫 요청 프롬프트 3,838토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> How is my business doing?

1. 모델 → **`a2api_search`** `` {"query":"business performance sales revenue"} ``
   ← 결과 401B: `` {"selected":[{"name":"acom_get_sales_trend","id":"acom.get_sales_trend"},{"name":"acom_get_sales_overview","id":"acom.get_sales_overview"},{"name":"acom_verify_business","id":"acom.verify_business"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_explain_sales_change","id":"acom.explain_sales_change"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`a2api_search`** `` {"query":"seller performance"} ``
   ← 결과 369B: `` {"selected":[{"name":"acom_update_seller","id":"acom.update_seller"},{"name":"acom_set_seller_grade","id":"acom.set_seller_grade"},{"name":"acom_get_seller","id":"acom.get_seller"},{"name":"acom_search_sellers","id":"acom.search_sellers"},{"name":"acom_onboard_seller","id":"acom.onboard_seller"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`a2api_search`** `` {"query":"business metrics"} ``
   ← 결과 379B: `` {"selected":[{"name":"acom_verify_business","id":"acom.verify_business"},{"name":"acom_get_seller_grade","id":"acom.get_seller_grade"},{"name":"acom_update_seller","id":"acom.update_seller"},{"name":"acom_issue_receipt","id":"acom.issue_receipt"},{"name":"acom_verify_identity","id":"acom.verify_identity"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``

**답변 1**
> To check how your business is doing I need to identify it first.
>
> Could you provide your business legal name, tax ID, or seller ID? Once I have that I can pull your recent sales, revenue, order count, and seller grade/performance metrics.

**채점**: ✗ 실패 — 빠진 것: tool get_sales_overview; fact "yesterday (Thu Nov 5) was $18,240, 20% under the Thursday av" (5, 18240, 20 not shown)
(도구 정밀도 —, 재현율 0.00)

### a2api-acom-names-norelated · 1회차 · ✗ 실패

토큰 13,097 · 45.352초 · 모델 호출 3회 · 도구 호출 4회 · 첫 요청 프롬프트 1,975토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> How is my business doing?

1. 모델 → **`a2api_load`** `` {"names":["get_customer_overview","get_sales_overview","get_cs_overview"]} ``
   ← 결과 75B: `` {"loaded":["get_customer_overview","get_sales_overview","get_cs_overview"]} ``
2. 모델 → **`get_sales_overview`** `` {"valid_from":"2026-11-01","valid_through":"2026-11-06","acom:metrics":["revenue","order_count","average_order_value","cancellation_rate","return_rate"],"acom:dimensions":["member_tier"],"compare_from":"2026-10-01","compare_through":"2026-10-31"} ``
   ← 결과 1,924B: `` {"status":"succeeded","data":{"items":[{"acom:metric":"revenue","value":{"value":29646.05,"currency":"USD"},"acom:dimension":{"member_tier":"gold"},"acom:change_rate":-0.8477},{"acom:metric":"order_count","value":331,"acom:dimension":{"member_tier":"gold"},"acom:change_rate":-0.8422},{"acom:metric":"average_order_value","value":{"value":89.57,"currency":"USD"},"acom:dimension":{"member_tier":"gold"},"acom:change_rate":-0.0346},{"acom:metric":"cancellation_rate","value":0,"acom:dimension":{"member_tier":"gold"},"acom:change_rate":null},{"acom:metric":"return_rate","value":0,"acom:dimension":{"m… (+900자) ``
3. 모델 → **`get_customer_overview`** `` {"valid_from":"2026-11-01","valid_through":"2026-11-06","acom:metrics":["new_members","active_members","tier_distribution","repurchase_rate"],"acom:dimensions":["member_tier"]} ``
   ← 결과 513B: `` {"status":"succeeded","data":{"items":[{"acom:metric":"active_members","value":1045,"acom:dimension":null},{"acom:metric":"tier_distribution","value":2900,"acom:dimension":{"member_tier":"gold"}},{"acom:metric":"tier_distribution","value":9816,"acom:dimension":{"member_tier":"member"}},{"acom:metric":"tier_distribution","value":1284,"acom:dimension":{"member_tier":"vip"}},{"acom:metric":"repurchase_rate","value":0.0402,"acom:dimension":null}],"total":5,"valid_from":"2026-11-01","valid_through":"2026-11-06"}} ``
4. 모델 → **`get_cs_overview`** `` {"valid_from":"2026-11-01","valid_through":"2026-11-06","acom:metrics":["inquiry_count","unresolved_count","average_response_time","resolution_rate"],"acom:dimensions":["inquiry_type"]} ``
   ← 결과 867B: `` {"status":"succeeded","data":{"items":[{"acom:metric":"inquiry_count","value":1,"acom:dimension":{"inquiry_type":"callback"}},{"acom:metric":"inquiry_count","value":1,"acom:dimension":{"inquiry_type":"return"}},{"acom:metric":"unresolved_count","value":1,"acom:dimension":{"inquiry_type":"callback"}},{"acom:metric":"unresolved_count","value":1,"acom:dimension":{"inquiry_type":"return"}},{"acom:metric":"average_response_time","value":35,"acom:dimension":{"inquiry_type":"callback"}},{"acom:metric":"average_response_time","value":null,"acom:dimension":{"inquiry_type":"return"}},{"acom:metric":"res… (+267자) ``

**답변 1**
> For the store period 2026-11-01 to 2026-11-06, 11:00 America/New_York:
>
> **Sales – by member tier, vs 2026-10-01 to 2026-10-31**
>
> * Gold
>   * Revenue: $29,646.05  change_rate -0.8477
>   * Orders: 331  change_rate -0.8422
>   * AOV: $89.57  change_rate -0.0346
>   * Cancellation rate: 0
>   * Return rate: 0  change_rate -1
>
> * Member
>   * Revenue: $49,654.45  change_rate -0.8542
>   * Orders: 543  change_rate -0.8516
>   * AOV: $91.44  change_rate -0.0175
>   * Cancellation rate: 0
>   * Return rate: 0  change_rate -1
>
> * VIP
>   * Revenue: $20,229.50  change_rate -0.8473
>   * Orders: 214  change_rate -0.8493
>   * AOV: $94.53  change_rate 0.0135
>   * Cancellation rate: 0
>   * Return rate: 0
>
> Combined for the 6-day window:
> * Revenue ≈ $99,530.00
> * Orders = 1,088
> * Implied AOV ≈ $91.60
> * Cancellation rate = 0 across tiers
> * Return rate = 0 across tiers
>
> All three tiers are down ~84-85% in revenue and order count vs the full October comparison period. AOV is essentially flat, VIP AOV up +1.35%.
>
> **Customers**
>
> * Active members 2026-11-01 to 2026-11-06: 1,045
> * Repurchase rate in period: 0.0402  ≈ 4.02%
> * Current tier distribution:
>   * gold: 2,900
>   * member: 9,816
>   * vip: 1,284
>   * Total tiered members = 14,000
>
> New members for the period was requested but not returned in the data.
>
> **Customer service 2026-11-01 to 2026-11-06**
>
> * Inquiries in: 2
>   * callback: 1
>   * return: 1
> * Unresolved: 2
>   * callback: 1
>   * return: 1
> * Average response time:
>   * callback: 35 minutes
>   * return: null
> * Resolution rate:
>   * callback: 0
>   * return: 0
>
> So sales volume is sharply lower than October on a period basis, with no cancellations or returns recorded in the window, a low 4% repurchase rate among active members, and two open service inquiries.

**채점**: ✗ 실패 — 빠진 것: fact "yesterday (Thu Nov 5) was $18,240, 20% under the Thursday av" (5, 18240, 20 not shown)
(도구 정밀도 0.67, 재현율 1.00)

### a2api-acom-names-norelated · 2회차 · ✗ 실패

토큰 28,706 · 68.697초 · 모델 호출 5회 · 도구 호출 6회 · 첫 요청 프롬프트 1,975토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> How is my business doing?

1. 모델 → **`a2api_load`** `` {"names":["get_sales_overview","get_sales_trend","explain_sales_change","get_customer_overview","get_cs_overview"]} ``
   ← 결과 116B: `` {"loaded":["get_sales_overview","get_sales_trend","explain_sales_change","get_customer_overview","get_cs_overview"]} ``
2. 모델 → **`get_sales_overview`** `` {"valid_from":"2026-10-31","valid_through":"2026-11-06","compare_from":"2026-10-24","compare_through":"2026-10-30"} ``
   ← 결과 621B: `` {"status":"succeeded","data":{"items":[{"acom:metric":"revenue","value":{"value":126940.0,"currency":"USD"},"acom:dimension":null,"acom:change_rate":-0.1649},{"acom:metric":"order_count","value":1383,"acom:dimension":null,"acom:change_rate":-0.1633},{"acom:metric":"average_order_value","value":{"value":91.79,"currency":"USD"},"acom:dimension":null,"acom:change_rate":-0.0018},{"acom:metric":"cancellation_rate","value":0,"acom:dimension":null,"acom:change_rate":null},{"acom:metric":"return_rate","value":0,"acom:dimension":null,"acom:change_rate":-1}],"total":5,"valid_from":"2026-10-31","valid_th… (+21자) ``
3. 모델 → **`get_customer_overview`** `` {"valid_from":"2026-10-31","valid_through":"2026-11-06"} ``
   ← 결과 575B: `` {"status":"succeeded","data":{"items":[{"acom:metric":"new_members","value":7,"acom:dimension":null},{"acom:metric":"active_members","value":1317,"acom:dimension":null},{"acom:metric":"tier_distribution","value":2900,"acom:dimension":{"member_tier":"gold"}},{"acom:metric":"tier_distribution","value":9816,"acom:dimension":{"member_tier":"member"}},{"acom:metric":"tier_distribution","value":1284,"acom:dimension":{"member_tier":"vip"}},{"acom:metric":"repurchase_rate","value":0.0486,"acom:dimension":null}],"total":6,"valid_from":"2026-10-31","valid_through":"2026-11-06"}} ``
4. 모델 → **`get_cs_overview`** `` {"valid_from":"2026-10-31","valid_through":"2026-11-06"} ``
   ← 결과 419B: `` {"status":"succeeded","data":{"items":[{"acom:metric":"inquiry_count","value":2,"acom:dimension":null},{"acom:metric":"unresolved_count","value":2,"acom:dimension":null},{"acom:metric":"average_response_time","value":35,"acom:dimension":null},{"acom:metric":"resolution_rate","value":0,"acom:dimension":null}],"total":4,"valid_from":"2026-10-31","valid_through":"2026-11-06","unit":{"average_response_time":"minutes"}}} ``
5. 모델 → **`get_sales_trend`** `` {"valid_from":"2026-10-31","valid_through":"2026-11-06","acom:granularity":"day","acom:metrics":["revenue","order_count"]} ``
   ← 결과 1,271B: `` {"status":"succeeded","data":{"items":[{"observation_date":"2026-10-31","acom:metric":"revenue","value":{"value":27410.0,"currency":"USD"}},{"observation_date":"2026-10-31","acom:metric":"order_count","value":295},{"observation_date":"2026-11-01","acom:metric":"revenue","value":{"value":24880.0,"currency":"USD"}},{"observation_date":"2026-11-01","acom:metric":"order_count","value":270},{"observation_date":"2026-11-02","acom:metric":"revenue","value":{"value":18150.0,"currency":"USD"}},{"observation_date":"2026-11-02","acom:metric":"order_count","value":199},{"observation_date":"2026-11-03","ac… (+671자) ``
6. 모델 → **`explain_sales_change`** `` {"valid_from":"2026-10-31","valid_through":"2026-11-05","compare_mode":"previous_period","acom:metric":"revenue","max_causes":5} ``
   ← 결과 2,131B: `` {"status":"succeeded","data":{"items":[{"cause":"campaign_not_sent","detail":"Weekly email not sent: list import failed Thu 08:00","amount":{"value":-1370.0,"currency":"USD"},"evidence":["cmp_weekly_1105"],"expected":{"value":1370.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"campaign":{"campaign_id":"cmp_weekly_1105","name":"Weekly email","channel":"email","campaign_status":"failed","scheduled_time":"2026-11-05T08:00:00-05:00","error_message":"List import failed","compared_with":["cmp_weekly_1029"]}},{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4… (+900자) ``

**답변 1**
> Last 7 store days 2026-10-31 → 2026-11-06, store time Fri 2026-11-06 11:00 America/New_York. 2026-11-06 is still open, so $0 / 0 orders so far today.
>
> **Sales – 2026-10-31 to 2026-11-06**
> * Revenue: $126,940
> * Orders: 1,383
> * Average order value: $91.79
> * vs 2026-10-24 to 2026-10-30
>   * revenue change_rate: -0.1649  ≈ -16.5%
>   * order_count change_rate: -0.1633  ≈ -16.3%
>   * average_order_value change_rate: -0.0018  ≈ -0.2%
> * cancellation_rate: 0
> * return_rate: 0
>
> Daily trend in the period:
> * 2026-10-31: $27,410 revenue, 295 orders
> * 2026-11-01: $24,880 revenue, 270 orders
> * 2026-11-02: $18,150 revenue, 199 orders
> * 2026-11-03: $18,940 revenue, 207 orders
> * 2026-11-04: $19,320 revenue, 211 orders
> * 2026-11-05: $18,240 revenue, 201 orders
> * 2026-11-06: $0.0 revenue, 0 orders
>
> **Customers – 2026-10-31 to 2026-11-06**
> * new_members: 7
> * active_members: 1,317
> * repurchase_rate: 0.0486  ≈ 4.9%
> * tier distribution now
>   * gold: 2,900
>   * member: 9,816
>   * vip: 1,284
>
> **Customer service – 2026-10-31 to 2026-11-06**
> * inquiry_count: 2
> * unresolved_count: 2
> * average_response_time: 35 minutes
> * resolution_rate: 0
>
> **Why sales moved in the last 6 full days**
> Period 2026-10-31 to 2026-11-05 vs previous 6 days 2026-10-25 to 2026-10-30:
> * Period revenue: $126,940, order_count 1,383
> * Compare revenue: $125,050, order_count 1,364
> * change_rate: +0.0151  ≈ +1.5%
> * gap: $1,890
>
> Explained causes for revenue:
> * campaign_not_sent: Weekly email not sent: list import failed Thu 08:00
>   amount: -$1,370.0 USD. Campaign cmp_weekly_1105 “Weekly email”, status failed, scheduled 2026-11-05T08:00:00-05:00, error “List import failed”. Expected $1,370.0, actual $0.0
> * out_of_stock: 3 bestsellers out of M and L since Wed Nov 4 15:00
>   amount: -$2,718.0 USD
>   * prd_chore_coat Cotton chore coat sizes M,L sold out at 2026-11-04T15:00:00-05:00, availability starts 2026-11-12T00:00:00-05:00, expected $1,420.0, actual $0.0
>   * prd_denim_jacket Denim jacket sizes M,L sold out at 2026-11-04T15:00:00-05:00… (+706자)

**채점**: ✗ 실패 — 빠진 것: fact "yesterday (Thu Nov 5) was $18,240, 20% under the Thursday av" (20 not shown)
(도구 정밀도 0.80, 재현율 1.00)

### a2api-acom-names-batch · 1회차 · ✗ 실패

토큰 12,371 · 33.365초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 1,975토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> How is my business doing?

1. 모델 → **`a2api_load`** `` {"names":["get_customer_overview","get_sales_overview","get_cs_overview"]} ``
   ← 결과 75B: `` {"loaded":["get_customer_overview","get_sales_overview","get_cs_overview"]} ``
2. 모델 → **`a2api_batch`** `` {"calls":[{"name":"get_sales_overview","arguments":{"valid_from":"2026-10-07","valid_through":"2026-11-06","acom:metrics":["revenue","order_count","average_order_value","cancellation_rate","return_rate"],"compare_from":"2026-09-08","compare_through":"2026-10-06"}},{"name":"get_customer_overview","arguments":{"valid_from":"2026-10-07","valid_through":"2026-11-06","acom:metrics":["new_members","active_members","tier_distribution","repurchase_rate"],"acom:dimensions":["member_tier"]}},{"name":"get_cs_overview","arguments":{"valid_from":"2026-10-07","valid_through":"2026-11-06","acom:metrics":["inquiry_count","unresolved_count","average_response_time","resolution_rate"],"acom:dimensions":["inqui… (+13자) ``
   ← 결과 2,763B: `` {"batch":[{"name":"get_sales_overview","result":{"status":"succeeded","data":{"items":[{"acom:metric":"revenue","value":{"value":638357.0,"currency":"USD"},"acom:dimension":null,"acom:change_rate":3.9429},{"acom:metric":"order_count","value":6879,"acom:dimension":null,"acom:change_rate":3.9561},{"acom:metric":"average_order_value","value":{"value":92.8,"currency":"USD"},"acom:dimension":null,"acom:change_rate":-0.0026},{"acom:metric":"cancellation_rate","value":0,"acom:dimension":null,"acom:change_rate":null},{"acom:metric":"return_rate","value":0.0016,"acom:dimension":null,"acom:change_rate":… (+900자) ``

**답변 1**
> For the last 31 store days 2026-10-07 to 2026-11-06 vs 2026-09-08 to 2026-10-06:
>
> **Sales**
> * Revenue: $638,357 USD, +394.3% vs prior period
> * Orders: 6,879 paid, not cancelled, +395.6% vs prior period
> * Average order value: $92.8 USD, -0.3% vs prior period
> * Cancellation rate: 0
> * Return rate: 0.16%, -44.5% vs prior period
>
> **Customers**
> * New members in period: 235
>   * gold: 39
>   * member: 172
>   * vip: 24
> * Active members in period: 5,189
> * Current tier distribution
>   * gold: 2,900
>   * member: 9,816
>   * vip: 1,284
> * Repurchase rate: 25.77% of active members ordered twice or more
>
> **Customer service**
> * Inquiries received: 3
>   * callback: 1
>   * order_status: 1
>   * return: 1
> * Unresolved: 2
>   * callback: 1 unresolved
>   * return: 1 unresolved
>   * order_status: 0 unresolved
> * Average first response time
>   * callback: 35 minutes
>   * order_status: 21 minutes
>   * return: no answered inquiries in period
> * Resolution rate
>   * callback: 0
>   * order_status: 1.00
>   * return: 0
>
> Revenue and order volume are up sharply ~4x year-over-year, AOV is essentially flat, returns are down and cancellations are at zero. Member base is ~14k with ~5.2k active in the period and a 25.8% repurchase rate. Service volume is very low with 2 of 3 inquiries still open.

**채점**: ✗ 실패 — 빠진 것: fact "yesterday (Thu Nov 5) was $18,240, 20% under the Thursday av" (5, 18240, 20 not shown)
(도구 정밀도 0.67, 재현율 1.00)

### a2api-acom-names-batch · 2회차 · E MODEL_HTTP_500

토큰 8,087 · 25.822초 · 모델 호출 2회 · 도구 호출 2회 · 첫 요청 프롬프트 1,975토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> How is my business doing?

1. 모델 → **`a2api_load`** `` {"names":["get_sales_overview","get_sales_trend","explain_sales_change","get_customer_overview","get_cs_overview"]} ``
   ← 결과 116B: `` {"loaded":["get_sales_overview","get_sales_trend","explain_sales_change","get_customer_overview","get_cs_overview"]} ``
2. 모델 → **`a2api_batch`** `` {"calls":[{"name":"get_sales_overview","arguments":{"valid_from":"2026-10-31","valid_through":"2026-11-06","acom:metrics":["revenue","order_count","average_order_value","cancellation_rate","return_rate"],"acom:dimensions":["member_tier"],"compare_from":"2026-10-24","compare_through":"2026-10-30"}},{"name":"get_sales_trend","arguments":{"valid_from":"2026-10-31","valid_through":"2026-11-06","acom:granularity":"day","acom:metrics":["revenue","order_count","average_order_value"]}},{"name":"get_customer_overview","arguments":{"valid_from":"2026-10-31","valid_through":"2026-11-06","acom:metrics":["new_members","active_members","tier_distribution","repurchase_rate"],"acom:dimensions":["member_tier… (+231자) ``
   ← 결과 3,695B: `` {"batch":[{"name":"get_sales_overview","result":{"status":"succeeded","data":{"items":[{"acom:metric":"revenue","value":{"value":38685.05,"currency":"USD"},"acom:dimension":{"member_tier":"gold"},"acom:change_rate":-0.1496},{"acom:metric":"order_count","value":433,"acom:dimension":{"member_tier":"gold"},"acom:change_rate":-0.1375},{"acom:metric":"average_order_value","value":{"value":89.34,"currency":"USD"},"acom:dimension":{"member_tier":"gold"},"acom:change_rate":-0.014},{"acom:metric":"cancellation_rate","value":0,"acom:dimension":{"member_tier":"gold"},"acom:change_rate":null},{"acom:metri… (+900자) ``

_(모델 서버 오류(500)로 중단)_

**채점**: E MODEL_HTTP_500 — 빠진 것: fact "yesterday (Thu Nov 5) was $18,240, 20% under the Thursday av" (5, 18240, 20 not shown); HOST:MODEL_HTTP_500
(도구 정밀도 0.75, 재현율 1.00)
