# mgr-what-needs-me-today — ours-design-9

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> what needs my attention today?

- 필요한 도구: `list_tasks`
- 허용 도구: `get_task`, `search_change_sets`, `get_change_set`, `search_return_requests`
- 답에 있어야 할 사실: one task needs you: the Linen shirt reorder draft (task_linen_reorder, draft cs_1041: 3 sizes, 240 units)
- 답에 있어야 할 사실: two are still working: the over-$200 returns review (task_returns_1106) and the size chart check (task_size_charts)
- 답에 있어야 할 사실: two finished this morning: below-cost prices raised to the floor (cs_1040, undo until Nov 7 23:59) and the Fall layers banner (cs_1039, live since 10:00)

### a2api-acom-hybrid · 1회차 · ✗ 실패

토큰 13,818 · 16.502초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 3,794토큰

준비: 전략 `index`, 함수 253개, 목차 4,645자(system prompt)

**질문 1**
> what needs my attention today?

1. 모델 → **`list_tasks`** `` {"state":["needs_you"],"limit":100} ``
   ← 결과 406B: `` {"status":"succeeded","data":{"items":[{"id":"task_linen_reorder","title":"Linen shirt sells out in about 4 days","state":"needs_you","origin":"agent_noticed","at":"2026-11-06T08:40:00-05:00","summary":"Reorder draft: 3 sizes, 240 units","tag":"inventory","change_set_id":"cs_1041","watcher":"stock_out_forecast","conversation_id":"conv_linen_reorder","updated_at":"2026-11-06T08:40:00-05:00"}],"total":1}} ``
2. 모델 → **`get_change_set`** `` {"change_set_id":"cs_1041"} ``
   ← 결과 3,467B: `` {"status":"succeeded","data":{"id":"cs_1041","number":1041,"version":1,"state":"waiting_for_approval","title":"Reorder linen shirt: 3 sizes, 240 units","request":{"text":["Linen shirt sells out in about 4 days. Draft a reorder for the sizes that will run out."],"conversation_id":"conv_linen_reorder","requested_by":"sys_watcher"},"interpretation":[{"slot":"products","text":"Linen shirt, White, S M L","value":{"sizes":["S","M","L"],"product_id":"prd_linen_shirt"}},{"slot":"other","text":"240 units: S 70, M 90, L 80","value":{"quantities":{"L":80,"M":90,"S":70}}}],"items":[{"position":1,"preview_… (+900자) ``

**답변 1**
> Today you have 1 item needing your attention:
>
> **Linen shirt sells out in about 4 days** — task `task_linen_reorder`
> * Origin: agent_noticed at 2026-11-06 08:40 America/New_York
> * Change set: **cs_1041** — *Reorder linen shirt: 3 sizes, 240 units*
> * State: waiting_for_approval
>
> Draft reorder for `prd_linen_shirt` White:
> * var_linen_shirt_s_white — S — 70 units @ $26.00
> * var_linen_shirt_m_white — M — 90 units @ $26.00
> * var_linen_shirt_l_white — L — 80 units @ $26.00
>
> Total units: 240
> Total payment due: $6,240.00 USD
> Expected arrival until: 2026-11-13 23:59 -05:00
> Reason for approval: Reorder cost over $1,000.00
>
> Checks passed: reorder.max_units_per_line, reorder.variant_orderable
> Undo deadline: 2026-11-07 23:59:00 -05:00
>
> The change set is a preview waiting for your approval before it can be placed.

**채점**: ✗ 실패 — 빠진 것: fact "two are still working: the over-$200 returns review (task_re" (200, 1106 not shown); fact "two finished this morning: below-cost prices raised to the f" (1040, 1039, 10 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-hybrid · 2회차 · ✗ 실패

토큰 13,818 · 16.147초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 3,794토큰

준비: 전략 `index`, 함수 253개, 목차 4,645자(system prompt)

**질문 1**
> what needs my attention today?

1. 모델 → **`list_tasks`** `` {"state":["needs_you"],"limit":100} ``
   ← 결과 406B: `` {"status":"succeeded","data":{"items":[{"id":"task_linen_reorder","title":"Linen shirt sells out in about 4 days","state":"needs_you","origin":"agent_noticed","at":"2026-11-06T08:40:00-05:00","summary":"Reorder draft: 3 sizes, 240 units","tag":"inventory","change_set_id":"cs_1041","watcher":"stock_out_forecast","conversation_id":"conv_linen_reorder","updated_at":"2026-11-06T08:40:00-05:00"}],"total":1}} ``
2. 모델 → **`get_change_set`** `` {"change_set_id":"cs_1041"} ``
   ← 결과 3,467B: `` {"status":"succeeded","data":{"id":"cs_1041","number":1041,"version":1,"state":"waiting_for_approval","title":"Reorder linen shirt: 3 sizes, 240 units","request":{"text":["Linen shirt sells out in about 4 days. Draft a reorder for the sizes that will run out."],"conversation_id":"conv_linen_reorder","requested_by":"sys_watcher"},"interpretation":[{"slot":"products","text":"Linen shirt, White, S M L","value":{"sizes":["S","M","L"],"product_id":"prd_linen_shirt"}},{"slot":"other","text":"240 units: S 70, M 90, L 80","value":{"quantities":{"L":80,"M":90,"S":70}}}],"items":[{"position":1,"preview_… (+900자) ``

**답변 1**
> Today you have 1 item needing your attention:
>
> **Linen shirt sells out in about 4 days** — task `task_linen_reorder`
> * Origin: agent_noticed at 2026-11-06 08:40 America/New_York
> * Change set: **cs_1041** — *Reorder linen shirt: 3 sizes, 240 units*
> * State: waiting_for_approval
>
> Draft reorder for `prd_linen_shirt` White:
> * var_linen_shirt_s_white — S — 70 units @ $26.00
> * var_linen_shirt_m_white — M — 90 units @ $26.00
> * var_linen_shirt_l_white — L — 80 units @ $26.00
>
> Total units: 240
> Total payment due: $6,240.00 USD
> Expected arrival until: 2026-11-13 23:59 -05:00
> Reason for approval: Reorder cost over $1,000.00
>
> Checks passed: reorder.max_units_per_line, reorder.variant_orderable
> Undo deadline: 2026-11-07 23:59:00 -05:00
>
> The change set is a preview waiting for your approval before it can be placed.

**채점**: ✗ 실패 — 빠진 것: fact "two are still working: the over-$200 returns review (task_re" (200, 1106 not shown); fact "two finished this morning: below-cost prices raised to the f" (1040, 1039, 10 not shown)
(도구 정밀도 1.00, 재현율 1.00)
