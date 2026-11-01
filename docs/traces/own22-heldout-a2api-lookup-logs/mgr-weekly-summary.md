# mgr-weekly-summary — own22-heldout-a2api-lookup-logs

[← 실행 묶음](README.md)

**과업**

> Give me a weekly performance summary

- 답에 있어야 할 사실: the window is stated (Sat Oct 31 – Fri Nov 6 so far, or the last 7 full days) with the week before for comparison

### a2api 변환 파사드 + 주문 번호 조회 · 1회차 · ✗ 실패

토큰 4,907 · 모델 호출 5회 · 도구 호출 1회

**질문 1**
> Give me a weekly performance summary

- 라우팅: Insights agent (chosen by the model)
- 도구 검색 후보: 1 candidates: get_sale_analysis_grid_list
- 계획: `get_sale_analysis_grid_list` `` {"to_date":"2026-11-05","from_date":"2026-10-30","compare_to":"previous_period"} ``
1. 에이전트 → **`get_sale_analysis_grid_list`** `` {"to_date":"2026-11-05","from_date":"2026-10-30","compare_to":"previous_period"} ``
   ← 결과: `` {"list":[{"revenue":148870.0,"to_date":"2026-11-05","from_date":"2026-10-30","change_rate":-0.0177,"order_count":1621,"revenue_change":-2680.0,"compare_revenue":151550.0,"compare_order_count":1647}]} ``
- check: Numbers not in the results: 26

**답변 1**
> The weekly performance summary for Oct 30 to Nov 5 shows revenue of $148,870 from 1,621 orders, down $2,680 versus the comparison week with revenue of $151,550 from 1,647 orders. The product table shows the figures for the period and the comparison basis.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "the window is stated (Sat Oct 31 – Fri Nov 6 so far, or the " (31, 6, 7 not shown)

### a2api 변환 파사드 + 주문 번호 조회 · 2회차 · ✗ 실패

토큰 3,598 · 모델 호출 4회 · 도구 호출 1회

**질문 1**
> Give me a weekly performance summary

- 라우팅: Insights agent (chosen by the model)
- 도구 검색 후보: 1 candidates: get_sale_analysis_grid_list
- 계획: `get_sale_analysis_grid_list` `` {"to_date":"2026-11-05","from_date":"2026-10-30","compare_to":"same_weekday_last_4_weeks"} ``
1. 에이전트 → **`get_sale_analysis_grid_list`** `` {"to_date":"2026-11-05","from_date":"2026-10-30","compare_to":"same_weekday_last_4_weeks"} ``
   ← 결과: `` {"list":[{"revenue":148870.0,"to_date":"2026-11-05","from_date":"2026-10-30","change_rate":0,"order_count":1621,"revenue_change":-0.5,"compare_revenue":148870.5,"compare_order_count":1599.75}]} ``
- check: Numbers not in the results: 21.25

**답변 1**
> The weekly performance summary for 2026-10-30 to 2026-11-05 shows revenue of $148,870.0 from 1,621 orders. Compared with the comparison basis, revenue is $148,870.5 and order count is 1,599.75, with a revenue change of -0.5 and a change rate of 0%. The results do not show the specific causes for the change.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "the window is stated (Sat Oct 31 – Fri Nov 6 so far, or the " (31, 6, 7 not shown)
