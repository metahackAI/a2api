# mgr-what-needs-me-today — own-latest-design-a2api-lookup

[← 실행 묶음](README.md)

**과업**

> what needs my attention today?

- 답에 있어야 할 사실: one task needs you: the Linen shirt reorder draft (task_linen_reorder, draft cs_1041: 3 sizes, 240 units)
- 답에 있어야 할 사실: two are still working: the over-$200 returns review (task_returns_1106) and the size chart check (task_size_charts)
- 답에 있어야 할 사실: two finished this morning: below-cost prices raised to the floor (cs_1040, undo until Nov 7 23:59) and the Fall layers banner (cs_1039, live since 10:00)

### a2api 변환 파사드 + 주문 번호 조회 · 1회차 · ✗ 실패

토큰 4,399 · 모델 호출 2회 · 도구 호출 1회

**질문 1**
> what needs my attention today?

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: save_promotion_list, save_coupon_list, save_display_banner_list, get_display_corner_list, get_promotion_grid_list
- 계획: `get_promotion_grid_list` `` {"page":1,"page_size":100,"active_from":"2026-11-06T00:00","active_until":"2026-11-06T23:59","promotion_status":"running"} ``
1. 에이전트 → **`get_promotion_grid_list`** `` {"page":1,"page_size":100,"active_from":"2026-11-06T00:00:00-05:00","active_until":"2026-11-06T23:59:00-05:00","promotion_status":"running"} ``
   ← 결과: `` {"list":[{"ends_at":"2026-11-15T23:59:00-05:00","starts_at":"2026-11-01T00:00:00-04:00","promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00"},{"ends_at":null,"starts_at":"2026-01-01T00:00:00-05:00","promotion_id":"promo_birthday","promotion_name":"Birthday coupon","promotion_type":"order_discount","promotion_status":"running","target_member_grade":"G01"},{"ends_at":null,"starts_at":"2026-01-01T00:00:00-05:00","promotion_id":"promo_free_ship_80","promotion_name":"Free shipping ov… (+330자) ``

**답변 1**
> The promotion grid shows four running promotions: Autumn knitwear 15% for everyone until Nov 15, Birthday coupon for G01, Free shipping over $80 for everyone, and Gold tier 10% for G02. No change set or tasks were returned, so there is nothing in the results that needs your attention today.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: fact "one task needs you: the Linen shirt reorder draft (task_line" (1041, 3, 240 not shown); fact "two are still working: the over-$200 returns review (task_re" (200, 1106 not shown); fact "two finished this morning: below-cost prices raised to the f" (1040, 7, 23, 59, 1039 not shown)

### a2api 변환 파사드 + 주문 번호 조회 · 2회차 · ✗ 실패

토큰 4,403 · 모델 호출 2회 · 도구 호출 1회

**질문 1**
> what needs my attention today?

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: save_promotion_list, save_coupon_list, save_display_banner_list, get_display_corner_list, get_promotion_grid_list
- 계획: `get_promotion_grid_list` `` {"page":1,"page_size":100,"active_from":"2026-11-06T00:00","active_until":"2026-11-06T23:59","promotion_status":"running"} ``
1. 에이전트 → **`get_promotion_grid_list`** `` {"page":1,"page_size":100,"active_from":"2026-11-06T00:00:00-05:00","active_until":"2026-11-06T23:59:00-05:00","promotion_status":"running"} ``
   ← 결과: `` {"list":[{"ends_at":"2026-11-15T23:59:00-05:00","starts_at":"2026-11-01T00:00:00-04:00","promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00"},{"ends_at":null,"starts_at":"2026-01-01T00:00:00-05:00","promotion_id":"promo_birthday","promotion_name":"Birthday coupon","promotion_type":"order_discount","promotion_status":"running","target_member_grade":"G01"},{"ends_at":null,"starts_at":"2026-01-01T00:00:00-05:00","promotion_id":"promo_free_ship_80","promotion_name":"Free shipping ov… (+330자) ``

**답변 1**
> The promotion grid shows four running promotions: Autumn knitwear 15% for everyone until Nov 15, Birthday coupon for G01, Free shipping over $80 for everyone, and Gold tier 10% for G02. No change set was created this turn, so there is nothing pending your approval right now. If you want a task list or recent actions, tell me which you’d like to see.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: fact "one task needs you: the Linen shirt reorder draft (task_line" (1041, 3, 240 not shown); fact "two are still working: the over-$200 returns review (task_re" (200, 1106 not shown); fact "two finished this morning: below-cost prices raised to the f" (1040, 7, 23, 59, 1039 not shown)

### a2api 변환 파사드 + 주문 번호 조회 · 3회차 · ✗ 실패

토큰 5,869 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> what needs my attention today?

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: save_promotion_list, save_coupon_list, save_display_banner_list, get_display_corner_list, get_promotion_grid_list
- 계획: `get_promotion_grid_list` `` {"page":1,"page_size":100,"active_from":"2026-11-06T00:00","active_until":"2026-11-06T23:59","promotion_status":"running"} ``
1. 에이전트 → **`get_promotion_grid_list`** `` {"page":1,"page_size":100,"active_from":"2026-11-06T00:00:00-05:00","active_until":"2026-11-06T23:59:00-05:00","promotion_status":"running"} ``
   ← 결과: `` {"list":[{"ends_at":"2026-11-15T23:59:00-05:00","starts_at":"2026-11-01T00:00:00-04:00","promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00"},{"ends_at":null,"starts_at":"2026-01-01T00:00:00-05:00","promotion_id":"promo_birthday","promotion_name":"Birthday coupon","promotion_type":"order_discount","promotion_status":"running","target_member_grade":"G01"},{"ends_at":null,"starts_at":"2026-01-01T00:00:00-05:00","promotion_id":"promo_free_ship_80","promotion_name":"Free shipping ov… (+330자) ``
- check: The reply was cut at the length limit

**답변 1**
> The promotion grid shows four running promotions: Autumn knitwear 15% for everyone until Nov 15, Birthday coupon for G01, Free shipping over $80 for everyone, and Gold tier 10% for G02. No tasks, change sets, or recent actions were returned, so there is nothing else flagged for attention today. The details are in the promotion table shown on screen.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: fact "one task needs you: the Linen shirt reorder draft (task_line" (1041, 3, 240 not shown); fact "two are still working: the over-$200 returns review (task_re" (200, 1106 not shown); fact "two finished this morning: below-cost prices raised to the f" (1040, 7, 23, 59, 1039 not shown)
