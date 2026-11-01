# md-low-stock-before-weekend — ours-design-9

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> what's about to sell out? anything I need to reorder before the weekend

- 필요한 도구: `search_products`
- 허용 도구: `get_inventory`, `list_tasks`, `get_task`
- 답에 있어야 할 사실: Light rain parka has 4 units left and Cotton chore coat has 7, the two lowest in the store
- 답에 있어야 할 사실: Linen shirt is the one with a reorder task: it sells out in about 4 days (task_linen_reorder, needs you)
- 부르면 안 됨: set_variant_stock

### a2api-acom-hybrid · 1회차 · ✗ 실패

토큰 29,925 · 35.003초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 4,713토큰

준비: 전략 `index`, 함수 253개, 목차 4,645자(system prompt)

**질문 1**
> what's about to sell out? anything I need to reorder before the weekend

1. 모델 → **`a2api_load`** `` {"names":["list_tasks","suggest_reorder"]} ``
   ← 결과 102B: `` {"already":["list_tasks","suggest_reorder"],"note":"These functions are already callable; call them."} ``
2. 모델 → **`list_tasks`** `` {"state":["needs_you","working"],"limit":100} ``
   ← 결과 1,075B: `` {"status":"succeeded","data":{"items":[{"id":"task_linen_reorder","title":"Linen shirt sells out in about 4 days","state":"needs_you","origin":"agent_noticed","at":"2026-11-06T08:40:00-05:00","summary":"Reorder draft: 3 sizes, 240 units","tag":"inventory","change_set_id":"cs_1041","watcher":"stock_out_forecast","conversation_id":"conv_linen_reorder","updated_at":"2026-11-06T08:40:00-05:00"},{"id":"task_returns_1106","title":"12 return requests over $200 are waiting","state":"working","origin":"agent_noticed","at":"2026-11-06T10:40:00-05:00","summary":"Operations agent is sorting the requests b… (+475자) ``
3. 모델 → **`get_change_set`** `` {"change_set_id":"cs_1041"} ``
   ← 결과 3,467B: `` {"status":"succeeded","data":{"id":"cs_1041","number":1041,"version":1,"state":"waiting_for_approval","title":"Reorder linen shirt: 3 sizes, 240 units","request":{"text":["Linen shirt sells out in about 4 days. Draft a reorder for the sizes that will run out."],"conversation_id":"conv_linen_reorder","requested_by":"sys_watcher"},"interpretation":[{"slot":"products","text":"Linen shirt, White, S M L","value":{"sizes":["S","M","L"],"product_id":"prd_linen_shirt"}},{"slot":"other","text":"240 units: S 70, M 90, L 80","value":{"quantities":{"L":80,"M":90,"S":70}}}],"items":[{"position":1,"preview_… (+900자) ``
4. 모델 → **`suggest_reorder`** `` {"product_id":"prd_linen_shirt"} ``
   ← 결과 1,473B: `` {"status":"succeeded","data":{"product_id":"prd_linen_shirt","name":"Linen shirt","sales_window":{"valid_from":"2026-10-30","valid_through":"2026-11-05","days":7},"lead_time_days":7,"cover_days":14,"variants":[{"variant_id":"var_linen_shirt_xs_white","size":"XS","color":"White","inventory_level":4,"acom:safety_stock":2,"on_order":0,"units_sold":6,"days_until_stockout":4.7,"order_quantity":16},{"variant_id":"var_linen_shirt_s_white","size":"S","color":"White","inventory_level":9,"acom:safety_stock":2,"on_order":0,"units_sold":16,"days_until_stockout":3.9,"order_quantity":41},{"variant_id":"var_… (+873자) ``

**답변 1**
> The only imminent stock-out the system is flagging right now is the White Linen shirt.
>
> * Task `task_linen_reorder` – “Linen shirt sells out in about 4 days”
>   * Forecast from the watcher: S, M and L run out first, ~4 days at current rate.
>   * Draft reorder in change set **cs_1041** is waiting for your approval:
>     * prd_linen_shirt – White
>     * S 70 units, M 90 units, L 80 units = 240 units total
>     * Total payment due $6,240.00 USD
>     * Expected arrival until 2026-11-13 23:59 -05:00
>     * Approval needed because reorder cost > $1,000. Undo deadline 2026-11-07 23:59 -05:00
>
> Current suggest_reorder snapshot for prd_linen_shirt, sales window 2026-10-30 → 2026-11-05, lead time 7 days, cover 14 days:
>
> * var_linen_shirt_s_white – S White: inventory 9, safety 2, sold 16/7d, days until stockout 3.9, suggested order 41
> * var_linen_shirt_m_white – M White: inventory 10, safety 2, sold 19/7d, days until stockout 3.7, suggested order 49
> * var_linen_shirt_l_white – L White: inventory 9, safety 2, sold 14/7d, days until stockout 4.5, suggested order 35
> * var_linen_shirt_xs_white – XS White: inventory 4, days until stockout 4.7, suggested order 16
> * var_linen_shirt_xl_white – XL White: inventory 6, days until stockout 7.0, suggested order 14
>
> Total suggested now: 155 units across XS-XL.
>
> That puts S/M/L at risk of selling out around Tue 2026-11-10, i.e. before the reorder would arrive ~Nov 13. The 240-unit draft in cs_1041 is the pending action to cover the weekend and the lead time. No other “about to sell out” tasks are in needs_you/working right now.

**채점**: ✗ 실패 — 빠진 것: tool search_products
(도구 정밀도 0.33, 재현율 0.00)

### a2api-acom-hybrid · 2회차 · ✗ 실패

토큰 29,925 · 34.634초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 4,713토큰

준비: 전략 `index`, 함수 253개, 목차 4,645자(system prompt)

**질문 1**
> what's about to sell out? anything I need to reorder before the weekend

1. 모델 → **`a2api_load`** `` {"names":["list_tasks","suggest_reorder"]} ``
   ← 결과 102B: `` {"already":["list_tasks","suggest_reorder"],"note":"These functions are already callable; call them."} ``
2. 모델 → **`list_tasks`** `` {"state":["needs_you","working"],"limit":100} ``
   ← 결과 1,075B: `` {"status":"succeeded","data":{"items":[{"id":"task_linen_reorder","title":"Linen shirt sells out in about 4 days","state":"needs_you","origin":"agent_noticed","at":"2026-11-06T08:40:00-05:00","summary":"Reorder draft: 3 sizes, 240 units","tag":"inventory","change_set_id":"cs_1041","watcher":"stock_out_forecast","conversation_id":"conv_linen_reorder","updated_at":"2026-11-06T08:40:00-05:00"},{"id":"task_returns_1106","title":"12 return requests over $200 are waiting","state":"working","origin":"agent_noticed","at":"2026-11-06T10:40:00-05:00","summary":"Operations agent is sorting the requests b… (+475자) ``
3. 모델 → **`get_change_set`** `` {"change_set_id":"cs_1041"} ``
   ← 결과 3,467B: `` {"status":"succeeded","data":{"id":"cs_1041","number":1041,"version":1,"state":"waiting_for_approval","title":"Reorder linen shirt: 3 sizes, 240 units","request":{"text":["Linen shirt sells out in about 4 days. Draft a reorder for the sizes that will run out."],"conversation_id":"conv_linen_reorder","requested_by":"sys_watcher"},"interpretation":[{"slot":"products","text":"Linen shirt, White, S M L","value":{"sizes":["S","M","L"],"product_id":"prd_linen_shirt"}},{"slot":"other","text":"240 units: S 70, M 90, L 80","value":{"quantities":{"L":80,"M":90,"S":70}}}],"items":[{"position":1,"preview_… (+900자) ``
4. 모델 → **`suggest_reorder`** `` {"product_id":"prd_linen_shirt"} ``
   ← 결과 1,473B: `` {"status":"succeeded","data":{"product_id":"prd_linen_shirt","name":"Linen shirt","sales_window":{"valid_from":"2026-10-30","valid_through":"2026-11-05","days":7},"lead_time_days":7,"cover_days":14,"variants":[{"variant_id":"var_linen_shirt_xs_white","size":"XS","color":"White","inventory_level":4,"acom:safety_stock":2,"on_order":0,"units_sold":6,"days_until_stockout":4.7,"order_quantity":16},{"variant_id":"var_linen_shirt_s_white","size":"S","color":"White","inventory_level":9,"acom:safety_stock":2,"on_order":0,"units_sold":16,"days_until_stockout":3.9,"order_quantity":41},{"variant_id":"var_… (+873자) ``

**답변 1**
> The only imminent stock-out the system is flagging right now is the White Linen shirt.
>
> * Task `task_linen_reorder` – “Linen shirt sells out in about 4 days”
>   * Forecast from the watcher: S, M and L run out first, ~4 days at current rate.
>   * Draft reorder in change set **cs_1041** is waiting for your approval:
>     * prd_linen_shirt – White
>     * S 70 units, M 90 units, L 80 units = 240 units total
>     * Total payment due $6,240.00 USD
>     * Expected arrival until 2026-11-13 23:59 -05:00
>     * Approval needed because reorder cost > $1,000. Undo deadline 2026-11-07 23:59 -05:00
>
> Current suggest_reorder snapshot for prd_linen_shirt, sales window 2026-10-30 → 2026-11-05, lead time 7 days, cover 14 days:
>
> * var_linen_shirt_s_white – S White: inventory 9, safety 2, sold 16/7d, days until stockout 3.9, suggested order 41
> * var_linen_shirt_m_white – M White: inventory 10, safety 2, sold 19/7d, days until stockout 3.7, suggested order 49
> * var_linen_shirt_l_white – L White: inventory 9, safety 2, sold 14/7d, days until stockout 4.5, suggested order 35
> * var_linen_shirt_xs_white – XS White: inventory 4, days until stockout 4.7, suggested order 16
> * var_linen_shirt_xl_white – XL White: inventory 6, days until stockout 7.0, suggested order 14
>
> Total suggested now: 155 units across XS-XL.
>
> That puts S/M/L at risk of selling out around Tue 2026-11-10, i.e. before the reorder would arrive ~Nov 13. The 240-unit draft in cs_1041 is the pending action to cover the weekend and the lead time. No other “about to sell out” tasks are in needs_you/working right now.

**채점**: ✗ 실패 — 빠진 것: tool search_products
(도구 정밀도 0.33, 재현율 0.00)
