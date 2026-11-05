# b3-why-sales-dropped — own-latest-design-acom

[← 실행 묶음](README.md)

**과업**

> Why did sales drop yesterday?

- 답에 있어야 할 사실: Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$4,660, -20%); 201 orders against 247
- 답에 있어야 할 사실: M and L sold out on the three best sellers (chore coat, rain parka, denim jacket): about -$2,700
- 답에 있어야 할 사실: the weekly email did not go out (Thu 08:00 list import failed): about -$1,300; -$660 is not explained

### A-Commerce 도구(참고) · 1회차 · ✓ 통과

토큰 7,433 · 모델 호출 2회 · 도구 호출 2회

**질문 1**
> Why did sales drop yesterday?

- 라우팅: Insights agent (the request names this agent's work)
- 도구 검색 후보: 13 candidates: explain_sales_change, get_sales_trend, get_sales_overview, get_customer_overview, search_members, preview_tier_evaluation, get_tier, get_member_tier, get_member, list_tier_history, get_consent, get_preferences, get_return_history
- 계획: `explain_sales_change` `` {"max_causes":5,"valid_from":"2026-11-05","acom:metric":"revenue","compare_mode":"same_weekday_last_4_weeks","valid_through":"2026-11-05"} ``; `get_sales_trend` `` {"valid_from":"2026-10-23","acom:metrics":["revenue"],"valid_through":"2026-11-05","acom:granularity":"day"} ``
1. 에이전트 → **`explain_sales_change`** `` {"max_causes":5,"valid_from":"2026-11-05","acom:metric":"revenue","compare_mode":"same_weekday_last_4_weeks","valid_through":"2026-11-05"} ``
   ← 결과: `` {"gap":{"value":-4660.0,"currency":"USD"},"items":[{"cause":"out_of_stock","since":"2026-11-04T15:00:00-05:00","actual":{"value":0.0,"currency":"USD"},"amount":{"value":-2700.0,"currency":"USD"},"detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"products":[{"name":"Cotton chore coat","sizes":["M","L"],"actual":{"value":0.0,"currency":"USD"},"expected":{"value":1313.5,"currency":"USD"},"product_id":"prd_chore_coat","sold_out_at":"2026-11-04T15:00:00-05:00","is_bestseller":t… (+1,537자) ``
2. 에이전트 → **`get_sales_trend`** `` {"valid_from":"2026-10-23","acom:metrics":["revenue"],"valid_through":"2026-11-05","acom:granularity":"day"} ``
   ← 결과: `` {"items":[{"value":{"value":21480.0,"currency":"USD"},"acom:metric":"revenue","observation_date":"2026-10-23"},{"value":{"value":26950.0,"currency":"USD"},"acom:metric":"revenue","observation_date":"2026-10-24"},{"value":{"value":24310.0,"currency":"USD"},"acom:metric":"revenue","observation_date":"2026-10-25"},{"value":{"value":17840.0,"currency":"USD"},"acom:metric":"revenue","observation_date":"2026-10-26"},{"value":{"value":18620.0,"currency":"USD"},"acom:metric":"revenue","observation_date":"2026-10-27"},{"value":{"value":19750.0,"currency":"USD"},"acom:metric":"revenue","observation_date… (+836자) ``

**답변 1**
> Sales on Thu Nov 5 were $18,240, down 20% from the Thursday average of $22,900, a $4,660 gap. The biggest drivers are three bestsellers out of stock in M and L since Wed Nov 4 15:00 — Cotton chore coat, Denim jacket and Light rain parka — costing about $2,700, and the Weekly email not sent due to a list import failure on Thu 08:00, costing about $1,300. About $660 of the drop remains unexplained.

화면 블록: sales_explainer(Sales on Thu Nov 5)

**채점**: ✓ 통과

### A-Commerce 도구(참고) · 2회차 · ✗ 실패

토큰 8,166 · 모델 호출 2회 · 도구 호출 2회

**질문 1**
> Why did sales drop yesterday?

- 라우팅: Insights agent (the request names this agent's work)
- 도구 검색 후보: 13 candidates: explain_sales_change, get_sales_trend, get_sales_overview, get_customer_overview, search_members, preview_tier_evaluation, get_tier, get_member_tier, get_member, list_tier_history, get_consent, get_preferences, get_return_history
- 계획: `explain_sales_change` `` {"max_causes":5,"valid_from":"2026-11-05","acom:metric":"revenue","compare_mode":"same_weekday_last_4_weeks","valid_through":"2026-11-05"} ``; `get_sales_trend` `` {"valid_from":"2026-10-23","acom:metrics":["revenue","order_count","average_order_value"],"valid_through":"2026-11-05","acom:granularity":"day"} ``
1. 에이전트 → **`explain_sales_change`** `` {"max_causes":5,"valid_from":"2026-11-05","acom:metric":"revenue","compare_mode":"same_weekday_last_4_weeks","valid_through":"2026-11-05"} ``
   ← 결과: `` {"gap":{"value":-4660.0,"currency":"USD"},"items":[{"cause":"out_of_stock","since":"2026-11-04T15:00:00-05:00","actual":{"value":0.0,"currency":"USD"},"amount":{"value":-2700.0,"currency":"USD"},"detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"products":[{"name":"Cotton chore coat","sizes":["M","L"],"actual":{"value":0.0,"currency":"USD"},"expected":{"value":1313.5,"currency":"USD"},"product_id":"prd_chore_coat","sold_out_at":"2026-11-04T15:00:00-05:00","is_bestseller":t… (+1,537자) ``
2. 에이전트 → **`get_sales_trend`** `` {"valid_from":"2026-10-23","acom:metrics":["revenue","order_count","average_order_value"],"valid_through":"2026-11-05","acom:granularity":"day"} ``
   ← 결과: `` {"items":[{"value":{"value":21480.0,"currency":"USD"},"acom:metric":"revenue","observation_date":"2026-10-23"},{"value":232,"acom:metric":"order_count","observation_date":"2026-10-23"},{"value":{"value":92.59,"currency":"USD"},"acom:metric":"average_order_value","observation_date":"2026-10-23"},{"value":{"value":26950.0,"currency":"USD"},"acom:metric":"revenue","observation_date":"2026-10-24"},{"value":289,"acom:metric":"order_count","observation_date":"2026-10-24"},{"value":{"value":93.25,"currency":"USD"},"acom:metric":"average_order_value","observation_date":"2026-10-24"},{"value":{"value":… (+3,424자) ``

**답변 1**
> Sales on Thu Nov 5 were $18,240, down $4,660 from the Thursday average of $22,900, a 20.4% drop. The biggest causes are three bestsellers out of stock in M and L since Wed Nov 4 15:00 — Cotton chore coat, Denim jacket and Light rain parka — accounting for about $2,700 in lost revenue, and the Weekly email not sent due to a list import failure on Thu 08:00, accounting for about $1,300. About $660 remains unexplained.

화면 블록: sales_explainer(Sales on Thu Nov 5)

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown)

### A-Commerce 도구(참고) · 3회차 · ✗ 실패

토큰 8,165 · 모델 호출 2회 · 도구 호출 2회

**질문 1**
> Why did sales drop yesterday?

- 라우팅: Insights agent (the request names this agent's work)
- 도구 검색 후보: 13 candidates: explain_sales_change, get_sales_trend, get_sales_overview, get_customer_overview, search_members, preview_tier_evaluation, get_tier, get_member_tier, get_member, list_tier_history, get_consent, get_preferences, get_return_history
- 계획: `explain_sales_change` `` {"max_causes":5,"valid_from":"2026-11-05","acom:metric":"revenue","compare_mode":"same_weekday_last_4_weeks","valid_through":"2026-11-05"} ``; `get_sales_trend` `` {"valid_from":"2026-10-23","acom:metrics":["revenue","order_count","average_order_value"],"valid_through":"2026-11-05","acom:granularity":"day"} ``
1. 에이전트 → **`explain_sales_change`** `` {"max_causes":5,"valid_from":"2026-11-05","acom:metric":"revenue","compare_mode":"same_weekday_last_4_weeks","valid_through":"2026-11-05"} ``
   ← 결과: `` {"gap":{"value":-4660.0,"currency":"USD"},"items":[{"cause":"out_of_stock","since":"2026-11-04T15:00:00-05:00","actual":{"value":0.0,"currency":"USD"},"amount":{"value":-2700.0,"currency":"USD"},"detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"products":[{"name":"Cotton chore coat","sizes":["M","L"],"actual":{"value":0.0,"currency":"USD"},"expected":{"value":1313.5,"currency":"USD"},"product_id":"prd_chore_coat","sold_out_at":"2026-11-04T15:00:00-05:00","is_bestseller":t… (+1,537자) ``
2. 에이전트 → **`get_sales_trend`** `` {"valid_from":"2026-10-23","acom:metrics":["revenue","order_count","average_order_value"],"valid_through":"2026-11-05","acom:granularity":"day"} ``
   ← 결과: `` {"items":[{"value":{"value":21480.0,"currency":"USD"},"acom:metric":"revenue","observation_date":"2026-10-23"},{"value":232,"acom:metric":"order_count","observation_date":"2026-10-23"},{"value":{"value":92.59,"currency":"USD"},"acom:metric":"average_order_value","observation_date":"2026-10-23"},{"value":{"value":26950.0,"currency":"USD"},"acom:metric":"revenue","observation_date":"2026-10-24"},{"value":289,"acom:metric":"order_count","observation_date":"2026-10-24"},{"value":{"value":93.25,"currency":"USD"},"acom:metric":"average_order_value","observation_date":"2026-10-24"},{"value":{"value":… (+3,424자) ``

**답변 1**
> Sales on Thu Nov 5 were $18,240, down $4,660 from the Thursday average of $22,900, a 20.4% drop. The biggest causes are three bestsellers out of stock in M and L since Wed Nov 4 15:00 — Cotton chore coat, Denim jacket and Light rain parka — accounting for about $2,700 in lost revenue, and the Weekly email not sent on Thu 08:00 due to list import failed, accounting for about $1,300. About $660 remains unexplained.

화면 블록: sales_explainer(Sales on Thu Nov 5)

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown)
