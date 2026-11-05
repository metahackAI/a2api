# mgr-how-is-business — luna-heldout-a2api

[← 실행 묶음](README.md)

**과업**

> How is my business doing?

- 답에 있어야 할 사실: yesterday (Thu Nov 5) was $18,240, 20% under the Thursday average; the agent leads with that and its causes

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 1회차 · ✗ 실패

토큰 23,802 · 모델 호출 4회 · 도구 호출 1회

**질문 1**
> How is my business doing?

- 라우팅: Insights agent (chosen by the model)
- 도구 검색 후보: 4 candidates: get_sale_analysis_grid_list, get_member_grade_list, get_promotion_target_member_list, get_promotion_target_member_list_count
- 계획: `get_sale_analysis_grid_list` `` {"to_date":"2026-11-06","from_date":"2026-11-01","compare_to":"previous_period"} ``
1. 에이전트 → **`get_sale_analysis_grid_list`** `` {"to_date":"2026-11-06","from_date":"2026-11-01","compare_to":"previous_period"} ``
   ← 결과: `` {"list":[{"revenue":99530.0,"to_date":"2026-11-06","from_date":"2026-11-01","change_rate":-0.2233,"order_count":1088,"revenue_change":-28620.0,"compare_revenue":128150.0,"compare_order_count":1396}]} ``
- check: Numbers not in the results: 22.33

**답변 1**
> From Nov 1–6, revenue was $99,530 across 1,088 orders, down $28,620 from the comparison period. The results don’t explain what caused the decline.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "yesterday (Thu Nov 5) was $18,240, 20% under the Thursday av" (5, 18240, 20 not shown)

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 2회차 · ✗ 실패

토큰 23,566 · 모델 호출 4회 · 도구 호출 1회

**질문 1**
> How is my business doing?

- 라우팅: Insights agent (chosen by the model)
- 도구 검색 후보: 4 candidates: get_sale_analysis_grid_list, get_member_grade_list, get_promotion_target_member_list, get_promotion_target_member_list_count
- 계획: `get_sale_analysis_grid_list` `` {"to_date":"2026-11-06","from_date":"2026-10-01","compare_to":"previous_period"} ``
1. 에이전트 → **`get_sale_analysis_grid_list`** `` {"to_date":"2026-11-06","from_date":"2026-10-01","compare_to":"previous_period"} ``
   ← 결과: `` {"list":[{"revenue":767081.0,"to_date":"2026-11-06","from_date":"2026-10-01","change_rate":1821.0451,"order_count":8264,"revenue_change":766660.0,"compare_revenue":421.0,"compare_order_count":3}]} ``
- check: Numbers not in the results: 8261

**답변 1**
> From Oct 1 through Nov 6, revenue was $767,081 across 8,264 orders. The comparison period had $421 in revenue and 3 orders.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "yesterday (Thu Nov 5) was $18,240, 20% under the Thursday av" (5, 18240, 20 not shown)

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 3회차 · ✗ 실패

토큰 17,871 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> How is my business doing?

- 라우팅: Insights agent (chosen by the model)
- 도구 검색 후보: 4 candidates: get_sale_analysis_grid_list, get_member_grade_list, get_promotion_target_member_list, get_promotion_target_member_list_count
- 계획: `get_sale_analysis_grid_list` `` {"to_date":"2026-11-06","from_date":"2026-10-01","compare_to":"previous_period"} ``
1. 에이전트 → **`get_sale_analysis_grid_list`** `` {"to_date":"2026-11-06","from_date":"2026-10-01","compare_to":"previous_period"} ``
   ← 결과: `` {"list":[{"revenue":767081.0,"to_date":"2026-11-06","from_date":"2026-10-01","change_rate":1821.0451,"order_count":8264,"revenue_change":766660.0,"compare_revenue":421.0,"compare_order_count":3}]} ``

**답변 1**
> From Oct 1 through Nov 6, revenue was $767,081 across 8,264 orders. Compared with $421 and 3 orders in the comparison period, revenue increased by $766,660; the results don’t identify what drove the difference.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "yesterday (Thu Nov 5) was $18,240, 20% under the Thursday av" (5, 18240, 20 not shown)
