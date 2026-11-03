# b3-why-sales-dropped — own-latest-design-a2api-lookup

[← 실행 묶음](README.md)

**과업**

> Why did sales drop yesterday?

- 답에 있어야 할 사실: Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$4,660, -20%); 201 orders against 247
- 답에 있어야 할 사실: M and L sold out on the three best sellers (chore coat, rain parka, denim jacket): about -$2,700
- 답에 있어야 할 사실: the weekly email did not go out (Thu 08:00 list import failed): about -$1,300; -$660 is not explained

### a2api 변환 파사드 + 주문 번호 조회 · 1회차 · ✗ 실패

토큰 6,395 · 모델 호출 4회 · 도구 호출 3회

**질문 1**
> Why did sales drop yesterday?

- 라우팅: Insights agent (the request names this agent's work)
- 도구 검색 후보: 4 candidates: get_sale_analysis_grid_list, get_promotion_target_member_list, get_promotion_target_member_list_count, get_member_grade_list
- 계획: `get_sale_analysis_grid_list` `` {"to_date":"2026-11-05","from_date":"2026-11-05","compare_to":"same_weekday_last_4_weeks"} ``; `get_sale_analysis_grid_list` `` {"to_date":"2026-11-05","from_date":"2026-10-23","compare_to":"same_weekday_last_4_weeks"} ``
1. 에이전트 → **`get_sale_analysis_grid_list`** `` {"to_date":"2026-11-05","from_date":"2026-11-05","compare_to":"same_weekday_last_4_weeks"} ``
   ← 결과: `` {"list":[{"revenue":18240.0,"to_date":"2026-11-05","from_date":"2026-11-05","change_rate":-0.2035,"order_count":201,"revenue_change":-4660.0,"compare_revenue":22900.0,"compare_order_count":247}]} ``
2. 에이전트 → **`get_sale_analysis_grid_list`** `` {"to_date":"2026-11-05","from_date":"2026-10-23","compare_to":"same_weekday_last_4_weeks"} ``
   ← 실패: `` {"code":"upstream_validation_failed","class":"invalid_input","message":"The backend rejected the request values. (HTTP 422) same_weekday_last_4_weeks compares periods of 7 days at most; this one has 14. Use previous_period or custom.","next_tool":null} ``
- 계획: `get_sale_analysis_grid_list` `` {"to_date":"2026-11-05","from_date":"2026-11-05","compare_to":"previous_period"} ``
3. 에이전트 → **`get_sale_analysis_grid_list`** `` {"to_date":"2026-11-05","from_date":"2026-11-05","compare_to":"previous_period"} ``
   ← 결과: `` {"list":[{"revenue":18240.0,"to_date":"2026-11-05","from_date":"2026-11-05","change_rate":-0.0559,"order_count":201,"revenue_change":-1080.0,"compare_revenue":19320.0,"compare_order_count":211}]} ``
- check: Numbers not in the results: 46, 10

**답변 1**
> The blocks show yesterday's sales (Thu Nov 5) at $18,240 from 201 orders, down $4,660 versus the same weekday four weeks ago. The same day versus the same weekday last week is also down $1,080. The blocks do not list the specific causes for the drop.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (22900, 20, 247 not shown); fact "M and L sold out on the three best sellers (chore coat, rain" (2700 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8, 0, 1300, 660 not shown)

### a2api 변환 파사드 + 주문 번호 조회 · 2회차 · ✗ 실패

토큰 3,884 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> Why did sales drop yesterday?

- 라우팅: Insights agent (the request names this agent's work)
- 도구 검색 후보: 4 candidates: get_sale_analysis_grid_list, get_promotion_target_member_list, get_promotion_target_member_list_count, get_member_grade_list
- 계획: `get_sale_analysis_grid_list` `` {"to_date":"2026-11-05","from_date":"2026-11-05","compare_to":"same_weekday_last_4_weeks"} ``
1. 에이전트 → **`get_sale_analysis_grid_list`** `` {"to_date":"2026-11-05","from_date":"2026-11-05","compare_to":"same_weekday_last_4_weeks"} ``
   ← 결과: `` {"list":[{"revenue":18240.0,"to_date":"2026-11-05","from_date":"2026-11-05","change_rate":-0.2035,"order_count":201,"revenue_change":-4660.0,"compare_revenue":22900.0,"compare_order_count":247}]} ``
- check: Numbers not in the results: 20.35

**답변 1**
> The blocks show yesterday's sales fell to $18,240 from $22,900, with orders down to 201 from 247. The results do not include a breakdown of the causes, so what drove the drop is not shown here.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (4660, 20 not shown); fact "M and L sold out on the three best sellers (chore coat, rain" (2700 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8, 0, 1300, 660 not shown)

### a2api 변환 파사드 + 주문 번호 조회 · 3회차 · ✗ 실패

토큰 3,881 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> Why did sales drop yesterday?

- 라우팅: Insights agent (the request names this agent's work)
- 도구 검색 후보: 4 candidates: get_sale_analysis_grid_list, get_promotion_target_member_list, get_promotion_target_member_list_count, get_member_grade_list
- 계획: `get_sale_analysis_grid_list` `` {"to_date":"2026-11-05","from_date":"2026-11-05","compare_to":"same_weekday_last_4_weeks"} ``
1. 에이전트 → **`get_sale_analysis_grid_list`** `` {"to_date":"2026-11-05","from_date":"2026-11-05","compare_to":"same_weekday_last_4_weeks"} ``
   ← 결과: `` {"list":[{"revenue":18240.0,"to_date":"2026-11-05","from_date":"2026-11-05","change_rate":-0.2035,"order_count":201,"revenue_change":-4660.0,"compare_revenue":22900.0,"compare_order_count":247}]} ``
- check: Numbers not in the results: 20.35

**답변 1**
> The blocks show yesterday's sales fell to $18,240 from $22,900, with orders down to 201 from 247. The results do not include a breakdown of causes, so what drove the drop is not shown here.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (4660, 20 not shown); fact "M and L sold out on the three best sellers (chore coat, rain" (2700 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8, 0, 1300, 660 not shown)
