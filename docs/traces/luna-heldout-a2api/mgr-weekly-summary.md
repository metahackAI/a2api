# mgr-weekly-summary — luna-heldout-a2api

[← 실행 묶음](README.md)

**과업**

> Give me a weekly performance summary

- 답에 있어야 할 사실: the window is stated (Sat Oct 31 – Fri Nov 6 so far, or the last 7 full days) with the week before for comparison

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 1회차 · ✗ 실패

토큰 18,049 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> Give me a weekly performance summary

- 라우팅: Insights agent (chosen by the model)
- 도구 검색 후보: 4 candidates: get_sale_analysis_grid_list, get_member_grade_list, get_promotion_target_member_list, get_promotion_target_member_list_count
- 계획: `get_sale_analysis_grid_list` `` {"to_date":"2026-11-06","from_date":"2026-11-02","compare_to":"previous_period"} ``
1. 에이전트 → **`get_sale_analysis_grid_list`** `` {"to_date":"2026-11-06","from_date":"2026-11-02","compare_to":"previous_period"} ``
   ← 결과: `` {"list":[{"revenue":74650.0,"to_date":"2026-11-06","from_date":"2026-11-02","change_rate":-0.3596,"order_count":818,"revenue_change":-41920.0,"compare_revenue":116570.0,"compare_order_count":1266}]} ``

**답변 1**
> For Nov 2–6, revenue was $74,650 across 818 orders, down $41,920 (36%) from the comparison period. The results don’t explain what drove the decline.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "the window is stated (Sat Oct 31 – Fri Nov 6 so far, or the " (31, 7 not shown)

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 2회차 · ✗ 실패

토큰 23,854 · 모델 호출 4회 · 도구 호출 1회

**질문 1**
> Give me a weekly performance summary

- 라우팅: Insights agent (chosen by the model)
- 도구 검색 후보: 4 candidates: get_sale_analysis_grid_list, get_member_grade_list, get_promotion_target_member_list, get_promotion_target_member_list_count
- 계획: `get_sale_analysis_grid_list` `` {"to_date":"2026-11-06","from_date":"2026-11-02","compare_to":"previous_period"} ``
1. 에이전트 → **`get_sale_analysis_grid_list`** `` {"to_date":"2026-11-06","from_date":"2026-11-02","compare_to":"previous_period"} ``
   ← 결과: `` {"list":[{"revenue":74650.0,"to_date":"2026-11-06","from_date":"2026-11-02","change_rate":-0.3596,"order_count":818,"revenue_change":-41920.0,"compare_revenue":116570.0,"compare_order_count":1266}]} ``
- check: Numbers not in the results: 35.96

**답변 1**
> This week to date (Nov 2–6), revenue was $74,650 across 818 orders, down $41,920 from the previous period. The results don’t explain what drove the decline.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "the window is stated (Sat Oct 31 – Fri Nov 6 so far, or the " (31, 7 not shown)

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 3회차 · ✗ 실패

토큰 23,936 · 모델 호출 4회 · 도구 호출 1회

**질문 1**
> Give me a weekly performance summary

- 라우팅: Insights agent (chosen by the model)
- 도구 검색 후보: 4 candidates: get_sale_analysis_grid_list, get_member_grade_list, get_promotion_target_member_list, get_promotion_target_member_list_count
- 계획: `get_sale_analysis_grid_list` `` {"to_date":"2026-11-05","from_date":"2026-10-30","compare_to":"previous_period"} ``
1. 에이전트 → **`get_sale_analysis_grid_list`** `` {"to_date":"2026-11-05","from_date":"2026-10-30","compare_to":"previous_period"} ``
   ← 결과: `` {"list":[{"revenue":148870.0,"to_date":"2026-11-05","from_date":"2026-10-30","change_rate":-0.0177,"order_count":1621,"revenue_change":-2680.0,"compare_revenue":151550.0,"compare_order_count":1647}]} ``
- check: Numbers not in the results: 1.77, 26

**답변 1**
> From Oct 30–Nov 5, revenue was $148,870 across 1,621 orders, compared with $151,550 and 1,647 orders in the previous period. The summary does not explain what drove the differences.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "the window is stated (Sat Oct 31 – Fri Nov 6 so far, or the " (31, 6, 7 not shown)
