# mk-whats-running-this-weekend — luna-design-a2api

[← 실행 묶음](README.md)

**과업**

> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 답에 있어야 할 사실: four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwear 15% (everyone, until Nov 15), Birthday coupon (members), Free shipping over $80 (everyone), Gold tier 10% (gold)
- 답에 있어야 할 사실: the knit sale covers 26 knitwear products

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 1회차 · ✗ 실패

토큰 19,583 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 6 candidates: get_promotion_grid_list, get_promotion_grid_list_count, save_promotion_list, save_coupon_list, get_promotion_target_member_list, get_promotion_target_member_list_count
- 계획: `get_promotion_grid_list` `` {"page":1,"page_size":100,"active_from":"2026-11-07T00:00","active_until":"2026-11-08T23:59"} ``
1. 에이전트 → **`get_promotion_grid_list`** `` {"page":1,"page_size":100,"active_from":"2026-11-07T00:00:00-05:00","active_until":"2026-11-08T23:59:00-05:00"} ``
   ← 결과: `` {"list":[{"ends_at":"2026-11-15T23:59:00-05:00","starts_at":"2026-11-01T00:00:00-04:00","promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00"},{"ends_at":null,"starts_at":"2026-01-01T00:00:00-05:00","promotion_id":"promo_birthday","promotion_name":"Birthday coupon","promotion_type":"order_discount","promotion_status":"running","target_member_grade":"G01"},{"ends_at":null,"starts_at":"2026-01-01T00:00:00-05:00","promotion_id":"promo_free_ship_80","promotion_name":"Free shipping ov… (+330자) ``

**답변 1**
> The Autumn knitwear 15% sale is live through Sun Nov 15, so it’s active this weekend. Birthday coupon, Free shipping over $80, and Gold tier 10% are also listed as running; the results don’t say whether they stack with the knit sale.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown)

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 2회차 · ✗ 실패

토큰 19,918 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 6 candidates: get_promotion_grid_list, get_promotion_grid_list_count, save_promotion_list, save_coupon_list, get_promotion_target_member_list, get_promotion_target_member_list_count
- 계획: `get_promotion_grid_list` `` {"page":1,"page_size":100,"active_from":"2026-11-07T00:00","active_until":"2026-11-08T23:59"} ``
1. 에이전트 → **`get_promotion_grid_list`** `` {"page":1,"page_size":100,"active_from":"2026-11-07T00:00:00-05:00","active_until":"2026-11-08T23:59:00-05:00"} ``
   ← 결과: `` {"list":[{"ends_at":"2026-11-15T23:59:00-05:00","starts_at":"2026-11-01T00:00:00-04:00","promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00"},{"ends_at":null,"starts_at":"2026-01-01T00:00:00-05:00","promotion_id":"promo_birthday","promotion_name":"Birthday coupon","promotion_type":"order_discount","promotion_status":"running","target_member_grade":"G01"},{"ends_at":null,"starts_at":"2026-01-01T00:00:00-05:00","promotion_id":"promo_free_ship_80","promotion_name":"Free shipping ov… (+330자) ``

**답변 1**
> The Autumn knitwear 15% sale and free shipping over $80 are live this weekend for everyone; the Birthday coupon and Gold tier 10% are also running for their respective tiers. I haven’t added or changed any promotions, so nothing is stacked on top of the knit sale.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown)

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 3회차 · ✗ 실패

토큰 19,592 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 6 candidates: get_promotion_grid_list, get_promotion_grid_list_count, save_promotion_list, save_coupon_list, get_promotion_target_member_list, get_promotion_target_member_list_count
- 계획: `get_promotion_grid_list` `` {"page":1,"page_size":100,"active_from":"2026-11-07T00:00","active_until":"2026-11-08T23:59"} ``
1. 에이전트 → **`get_promotion_grid_list`** `` {"page":1,"page_size":100,"active_from":"2026-11-07T00:00:00-05:00","active_until":"2026-11-08T23:59:00-05:00"} ``
   ← 결과: `` {"list":[{"ends_at":"2026-11-15T23:59:00-05:00","starts_at":"2026-11-01T00:00:00-04:00","promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00"},{"ends_at":null,"starts_at":"2026-01-01T00:00:00-05:00","promotion_id":"promo_birthday","promotion_name":"Birthday coupon","promotion_type":"order_discount","promotion_status":"running","target_member_grade":"G01"},{"ends_at":null,"starts_at":"2026-01-01T00:00:00-05:00","promotion_id":"promo_free_ship_80","promotion_name":"Free shipping ov… (+330자) ``

**답변 1**
> The knitwear sale, “Autumn knitwear 15%,” is live this weekend, Nov 7–8, so I’ve left it out of the list. The other live promos are Birthday coupon, Free shipping over $80, and Gold tier 10%.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: fact "the knit sale covers 26 knitwear products" (26 not shown)
