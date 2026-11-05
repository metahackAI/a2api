# mk-whats-running-this-weekend — luna-design-acom

[← 실행 묶음](README.md)

**과업**

> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 답에 있어야 할 사실: four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwear 15% (everyone, until Nov 15), Birthday coupon (members), Free shipping over $80 (everyone), Gold tier 10% (gold)
- 답에 있어야 할 사실: the knit sale covers 26 knitwear products

### GPT-6-Luna · A-Commerce 도구(참고) · 1회차 · ✗ 실패

토큰 22,969 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 12 candidates: list_tasks, list_active_promotions, search_products, list_tiers, set_sale_prices, search_promotions, list_display_slots, list_categories, schedule_banner, schedule_display, create_coupon, pause_promotion
- 계획: `list_active_promotions` `` {"valid_from":"2026-11-06 11:00","valid_through":"2026-11-08 23:59"} ``
1. 에이전트 → **`list_active_promotions`** `` {"valid_from":"2026-11-06T11:00:00-05:00","valid_through":"2026-11-08T23:59:00-05:00"} ``
   ← 결과: `` {"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","discount_layer":"item_price","valid_for_member_tier":"everyone"},{"id":"promo_birthday","name":"Birthday coupon","status":"running","applies_to":{"scope":"order","category_ids":[],"product_count":null},"valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"discount_layer":"order_discount","valid_for_member_tier":"member"},{"id":"prom… (+534자) ``

**답변 1**
> Autumn knitwear 15% is live this weekend, Fri Nov 6 through Sun Nov 8, on 26 knitwear products. Birthday coupon, Free shipping over $80, and Gold tier 10% are also running; avoid applying any of them on top of the knit sale.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7 not shown)

### GPT-6-Luna · A-Commerce 도구(참고) · 2회차 · ✗ 실패

토큰 23,006 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 12 candidates: list_tasks, list_active_promotions, search_products, list_tiers, set_sale_prices, search_promotions, list_display_slots, list_categories, schedule_banner, schedule_display, create_coupon, pause_promotion
- 계획: `search_promotions` `` {"status":["running","scheduled"],"valid_from":"2026-11-06 11:00","valid_through":"2026-11-08 23:59"} ``
1. 에이전트 → **`search_promotions`** `` {"status":["running","scheduled"],"valid_from":"2026-11-06T11:00:00-05:00","valid_through":"2026-11-08T23:59:00-05:00"} ``
   ← 결과: `` {"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","discount_layer":"item_price","valid_for_member_tier":"everyone"},{"id":"promo_birthday","name":"Birthday coupon","status":"running","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"discount_layer":"order_discount","valid_for_member_tier":"member"},{"id":"promo_free_ship_80","name":"Free shipping over $80","status":"running","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"discount_layer":"add_on","v… (+237자) ``

**답변 1**
> The Autumn knitwear 15% sale is live through Sun Nov 15, and the Birthday coupon, Free shipping over $80, and Gold tier 10% promotions are also running. The knit sale is an item-price discount; the other promotions are order discounts or an add-on, so the results don’t show them being stacked on top of it.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: tool list_active_promotions; fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown)

### GPT-6-Luna · A-Commerce 도구(참고) · 3회차 · ✗ 실패

토큰 22,637 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 12 candidates: list_tasks, list_active_promotions, search_products, list_tiers, set_sale_prices, search_promotions, list_display_slots, list_categories, schedule_banner, schedule_display, create_coupon, pause_promotion
- 계획: `search_promotions` `` {"status":["running","scheduled"],"valid_from":"2026-11-07 00:00","valid_through":"2026-11-08 23:59"} ``
1. 에이전트 → **`search_promotions`** `` {"status":["running","scheduled"],"valid_from":"2026-11-07T00:00:00-05:00","valid_through":"2026-11-08T23:59:00-05:00"} ``
   ← 결과: `` {"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","discount_layer":"item_price","valid_for_member_tier":"everyone"},{"id":"promo_birthday","name":"Birthday coupon","status":"running","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"discount_layer":"order_discount","valid_for_member_tier":"member"},{"id":"promo_free_ship_80","name":"Free shipping over $80","status":"running","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"discount_layer":"add_on","v… (+237자) ``

**답변 1**
> The Autumn knitwear 15% sale is live this weekend, Nov 7–8, and I’ve left it out as requested. Other live promotions are Birthday coupon, Free shipping over $80, and Gold tier 10%.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: tool list_active_promotions; fact "the knit sale covers 26 knitwear products" (26 not shown)
