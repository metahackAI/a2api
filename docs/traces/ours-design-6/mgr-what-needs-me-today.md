# mgr-what-needs-me-today — ours-design-6

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `20f2d63`

**과업**

> what needs my attention today?

- 필요한 도구: `list_tasks`
- 허용 도구: `get_task`, `search_change_sets`, `get_change_set`, `search_return_requests`
- 답에 있어야 할 사실: one task needs you: the Linen shirt reorder draft (task_linen_reorder, draft cs_1041: 3 sizes, 240 units)
- 답에 있어야 할 사실: two are still working: the over-$200 returns review (task_returns_1106) and the size chart check (task_size_charts)
- 답에 있어야 할 사실: two finished this morning: below-cost prices raised to the floor (cs_1040, undo until Nov 7 23:59) and the Fall layers banner (cs_1039, live since 10:00)

### a2api-acom · 1회차 · ✗ 실패

토큰 10,944 · 16.059초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 2,817토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> what needs my attention today?

1. 모델 → **`acom_list_tasks`** `` {"state":["needs_you"],"since":"2026-11-06T00:00","limit":100} ``
   ← 결과 406B: `` {"status":"succeeded","data":{"items":[{"id":"task_linen_reorder","title":"Linen shirt sells out in about 4 days","state":"needs_you","origin":"agent_noticed","at":"2026-11-06T08:40:00-05:00","summary":"Reorder draft: 3 sizes, 240 units","tag":"inventory","change_set_id":"cs_1041","watcher":"stock_out_forecast","conversation_id":"conv_linen_reorder","updated_at":"2026-11-06T08:40:00-05:00"}],"total":1}} ``
2. 모델 → **`acom_get_change_set`** `` {"change_set_id":"cs_1041"} ``
   ← 결과 3,467B: `` {"status":"succeeded","data":{"id":"cs_1041","number":1041,"version":1,"state":"waiting_for_approval","title":"Reorder linen shirt: 3 sizes, 240 units","request":{"text":["Linen shirt sells out in about 4 days. Draft a reorder for the sizes that will run out."],"conversation_id":"conv_linen_reorder","requested_by":"sys_watcher"},"interpretation":[{"slot":"products","text":"Linen shirt, White, S M L","value":{"sizes":["S","M","L"],"product_id":"prd_linen_shirt"}},{"slot":"other","text":"240 units: S 70, M 90, L 80","value":{"quantities":{"L":80,"M":90,"S":70}}}],"items":[{"position":1,"preview_… (+900자) ``

**답변 1**
> You have 1 item needing your attention today:
>
> **Linen shirt sells out in about 4 days** — task_linen_reorder
> * Origin: agent_noticed at 2026-11-06 08:40 America/New_York
> * Change set 1041 — waiting_for_approval
>
> Draft reorder for prd_linen_shirt, White:
> * S 70 units, M 90 units, L 80 units = 240 units total
> * Total payment due: $6,240.00 USD
> * Expected arrival until: 2026-11-13 23:59 -05:00
> * Approval needed: Reorder cost over $1,000.00
>
> Change set cs_1041 is a preview only. It can be undone until 2026-11-07 23:59 -05:00.

**채점**: ✗ 실패 — 빠진 것: fact "one task needs you: the Linen shirt reorder draft (task_line" (3 not shown); fact "two are still working: the over-$200 returns review (task_re" (200, 1106 not shown); fact "two finished this morning: below-cost prices raised to the f" (1040, 1039, 10 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-facade · 1회차 · ✗ 실패

토큰 8,953 · 37.566초 · 모델 호출 4회 · 도구 호출 9회 · 첫 요청 프롬프트 630토큰

준비: 전략 `search`, 함수 1개

**질문 1**
> what needs my attention today?

1. 모델 → **`a2api_search`** `` {"query":"pending tasks attention today"} ``
   ← 결과 74B: `` {"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":false} ``
2. 모델 → **`a2api_search`** `` {"query":"orders needing attention"} ``
   ← 결과 236B: `` {"selected":[{"name":"facade_get_sale_anls_grid_list","id":"facade.get_sale_anls_grid_list"},{"name":"facade_save_cust_msg_send","id":"facade.save_cust_msg_send"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`a2api_search`** `` {"query":"change set pending approval"} ``
   ← 결과 232B: `` {"selected":[{"name":"facade_get_prd_dtl_info","id":"facade.get_prd_dtl_info"},{"name":"facade_get_sale_anls_grid_list","id":"facade.get_sale_anls_grid_list"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`a2api_search`** `` {"query":"today tasks due"} ``
   ← 결과 74B: `` {"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":false} ``
5. 모델 → **`a2api_search`** `` {"query":"pending approval change set"} ``
   ← 실패 233B: `` {"status":"failed","error":{"code":"SEARCH_LIMIT","detail":"4 searches in a row found no function to call for this request."},"hint":"Searching again will not find more. Use the functions you have, or tell the user what is missing."} ``
6. 모델 → **`a2api_search`** `` {"query":"alerts notifications today"} ``
   ← 실패 233B: `` {"status":"failed","error":{"code":"SEARCH_LIMIT","detail":"4 searches in a row found no function to call for this request."},"hint":"Searching again will not find more. Use the functions you have, or tell the user what is missing."} ``
7. 모델 → **`a2api_search`** `` {"query":"tasks due today"} ``
   ← 실패 233B: `` {"status":"failed","error":{"code":"SEARCH_LIMIT","detail":"4 searches in a row found no function to call for this request."},"hint":"Searching again will not find more. Use the functions you have, or tell the user what is missing."} ``
8. 모델 → **`a2api_search`** `` {"query":"customer messages pending"} ``
   ← 실패 233B: `` {"status":"failed","error":{"code":"SEARCH_LIMIT","detail":"4 searches in a row found no function to call for this request."},"hint":"Searching again will not find more. Use the functions you have, or tell the user what is missing."} ``
9. 모델 → **`facade_get_sale_anls_grid_list`** `` {"from_date":"2026-11-06","to_date":"2026-11-06","compare_to":"same_weekday_last_4_weeks"} ``
   ← 결과 220B: `` {"status":"succeeded","data":{"list":[{"from_date":"2026-11-06","to_date":"2026-11-06","revenue":0.0,"order_count":0,"compare_revenue":21879.75,"compare_order_count":233.75,"revenue_change":-21879.75,"change_rate":-1}]}} ``

**답변 1**
> Based on the tools I can access right now, here’s what’s visible for today **Fri 2026-11-06 11:00 America/New_York**:
>
> **Sales snapshot for today**
> * Revenue today: $0.00
> * Order count today: 0
> * Comparison basis: same weekday last 4 weeks
>   * Compare revenue: $21,879.75
>   * Compare order count: 233.75
>   * Revenue change: -$21,879.75  /  change rate: -100%
>
> That is a complete drop-off vs the recent weekday average. At 11:00am it’s still early in the day, but zero revenue/orders so far is the only anomaly I can surface with the available functions.
>
> I don’t have access to a task / change-set / order-pending queue or alerts dashboard in the current tool set. Available functions are:
> * `facade_get_sale_anls_grid_list` – sales/revenue analysis
> * `facade_get_prd_dtl_info` – product price/stock/availability
> * `facade_save_cust_msg_send` – send a customer message
>
> If you want me to check a specific product, order, or member, or run sales for a different date range, tell me the IDs and I’ll pull it.

**채점**: ✗ 실패 — 빠진 것: fact "one task needs you: the Linen shirt reorder draft (task_line" (1041, 3, 240 not shown); fact "two are still working: the over-$200 returns review (task_re" (200, 1106 not shown); fact "two finished this morning: below-cost prices raised to the f" (1040, 7, 23, 59, 1039, 10 not shown)
