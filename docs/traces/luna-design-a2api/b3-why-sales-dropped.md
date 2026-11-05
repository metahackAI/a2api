# b3-why-sales-dropped — luna-design-a2api

[← 실행 묶음](README.md)

**과업**

> Why did sales drop yesterday?

- 답에 있어야 할 사실: Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$4,660, -20%); 201 orders against 247
- 답에 있어야 할 사실: M and L sold out on the three best sellers (chore coat, rain parka, denim jacket): about -$2,700
- 답에 있어야 할 사실: the weekly email did not go out (Thu 08:00 list import failed): about -$1,300; -$660 is not explained

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 1회차 · ✗ 실패

토큰 18,600 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> Why did sales drop yesterday?

- 라우팅: Insights agent (the request names this agent's work)
- 도구 검색 후보: 4 candidates: get_sale_analysis_grid_list, get_promotion_target_member_list, get_promotion_target_member_list_count, get_member_grade_list
- 계획: `get_sale_analysis_grid_list` `` {"to_date":"2026-11-05","from_date":"2026-11-05","compare_to":"same_weekday_last_4_weeks"} ``
1. 에이전트 → **`get_sale_analysis_grid_list`** `` {"to_date":"2026-11-05","from_date":"2026-11-05","compare_to":"same_weekday_last_4_weeks"} ``
   ← 결과: `` {"list":[{"revenue":18240.0,"to_date":"2026-11-05","from_date":"2026-11-05","change_rate":-0.2035,"order_count":201,"revenue_change":-4660.0,"compare_revenue":22900.0,"compare_order_count":247}]} ``
- check: Numbers not in the results: 20.35

**답변 1**
> Sales yesterday were down $4,660, with 201 orders versus 247 in the comparison period. The results show the drop but don’t explain its causes.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown); fact "M and L sold out on the three best sellers (chore coat, rain" (2700 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8, 0, 1300, 660 not shown)

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 2회차 · ✗ 실패

토큰 18,483 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> Why did sales drop yesterday?

- 라우팅: Insights agent (the request names this agent's work)
- 도구 검색 후보: 4 candidates: get_sale_analysis_grid_list, get_promotion_target_member_list, get_promotion_target_member_list_count, get_member_grade_list
- 계획: `get_sale_analysis_grid_list` `` {"to_date":"2026-11-05","from_date":"2026-11-05","compare_to":"same_weekday_last_4_weeks"} ``
1. 에이전트 → **`get_sale_analysis_grid_list`** `` {"to_date":"2026-11-05","from_date":"2026-11-05","compare_to":"same_weekday_last_4_weeks"} ``
   ← 결과: `` {"list":[{"revenue":18240.0,"to_date":"2026-11-05","from_date":"2026-11-05","change_rate":-0.2035,"order_count":201,"revenue_change":-4660.0,"compare_revenue":22900.0,"compare_order_count":247}]} ``
- check: Numbers not in the results: 20.35

**답변 1**
> Sales yesterday, Nov 5, were $18,240 across 201 orders, down $4,660 from the comparison period. The results don’t explain what caused the drop.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown); fact "M and L sold out on the three best sellers (chore coat, rain" (2700 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8, 0, 1300, 660 not shown)

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 3회차 · ✗ 실패

토큰 18,525 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> Why did sales drop yesterday?

- 라우팅: Insights agent (the request names this agent's work)
- 도구 검색 후보: 4 candidates: get_sale_analysis_grid_list, get_promotion_target_member_list, get_promotion_target_member_list_count, get_member_grade_list
- 계획: `get_sale_analysis_grid_list` `` {"to_date":"2026-11-05","from_date":"2026-11-05","compare_to":"same_weekday_last_4_weeks"} ``
1. 에이전트 → **`get_sale_analysis_grid_list`** `` {"to_date":"2026-11-05","from_date":"2026-11-05","compare_to":"same_weekday_last_4_weeks"} ``
   ← 결과: `` {"list":[{"revenue":18240.0,"to_date":"2026-11-05","from_date":"2026-11-05","change_rate":-0.2035,"order_count":201,"revenue_change":-4660.0,"compare_revenue":22900.0,"compare_order_count":247}]} ``
- check: Numbers not in the results: 20.35

**답변 1**
> Sales on Thu Nov 5 were $18,240 across 201 orders, down $4,660 from the same-weekday comparison. The results show lower revenue and fewer orders, but don’t explain why.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown); fact "M and L sold out on the three best sellers (chore coat, rain" (2700 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8, 0, 1300, 660 not shown)
