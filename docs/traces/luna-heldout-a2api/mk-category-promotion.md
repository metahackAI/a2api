# mk-category-promotion — luna-heldout-a2api

[← 실행 묶음](README.md)

**과업**

> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 답에 있어야 할 사실: 2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store time

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 1회차 · ✗ 실패

토큰 23,061 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 6 candidates: save_promotion_list, save_coupon_list, get_promotion_grid_list_count, get_promotion_grid_list, get_promotion_target_member_list, get_promotion_target_member_list_count
- 계획: `get_promotion_grid_list` `` {"page":1,"page_size":20} ``
1. 에이전트 → **`get_promotion_grid_list`** `` {"page":1,"page_size":20} ``
   ← 결과: `` {"list":[{"ends_at":"2026-11-20T23:59:00-05:00","starts_at":"2026-11-13T00:00:00-05:00","promotion_id":"promo_denim_bundle","promotion_name":"Denim bundle","promotion_type":"order_discount","promotion_status":"scheduled","target_member_grade":"G00"},{"ends_at":"2026-11-15T23:59:00-05:00","starts_at":"2026-11-01T00:00:00-04:00","promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00"},{"ends_at":"2026-10-20T23:59:00-04:00","starts_at":"2026-10-01T00:00:00-04:00","promotion_id":"promo… (+818자) ``

**답변 1**
> There’s no Outerwear promotion in the results, and no promotion was created. Nothing has been set up for the $50-off-$250 offer; it still needs to be created with a two-week validity period.

화면 블록: product_table(6 of 6)

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (19, 23, 59 not shown)

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 2회차 · ✗ 실패

토큰 23,048 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 6 candidates: save_promotion_list, save_coupon_list, get_promotion_grid_list_count, get_promotion_grid_list, get_promotion_target_member_list, get_promotion_target_member_list_count
- 계획: `get_promotion_grid_list` `` {} ``
1. 에이전트 → **`get_promotion_grid_list`** `` {} ``
   ← 결과: `` {"list":[{"ends_at":"2026-11-20T23:59:00-05:00","starts_at":"2026-11-13T00:00:00-05:00","promotion_id":"promo_denim_bundle","promotion_name":"Denim bundle","promotion_type":"order_discount","promotion_status":"scheduled","target_member_grade":"G00"},{"ends_at":"2026-11-15T23:59:00-05:00","starts_at":"2026-11-01T00:00:00-04:00","promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00"},{"ends_at":"2026-10-20T23:59:00-04:00","starts_at":"2026-10-01T00:00:00-04:00","promotion_id":"promo… (+818자) ``

**답변 1**
> There’s no promotion draft yet; the results only show existing promotions. Nothing has been set up for Outerwear, so there’s nothing to approve.

화면 블록: product_table(6 of 6)

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (19, 23, 59 not shown)

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 3회차 · ✗ 실패

토큰 23,062 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 6 candidates: save_promotion_list, save_coupon_list, get_promotion_grid_list_count, get_promotion_grid_list, get_promotion_target_member_list, get_promotion_target_member_list_count
- 계획: `get_promotion_grid_list` `` {"page":1,"page_size":20} ``
1. 에이전트 → **`get_promotion_grid_list`** `` {"page":1,"page_size":20} ``
   ← 결과: `` {"list":[{"ends_at":"2026-11-20T23:59:00-05:00","starts_at":"2026-11-13T00:00:00-05:00","promotion_id":"promo_denim_bundle","promotion_name":"Denim bundle","promotion_type":"order_discount","promotion_status":"scheduled","target_member_grade":"G00"},{"ends_at":"2026-11-15T23:59:00-05:00","starts_at":"2026-11-01T00:00:00-04:00","promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00"},{"ends_at":"2026-10-20T23:59:00-04:00","starts_at":"2026-10-01T00:00:00-04:00","promotion_id":"promo… (+818자) ``

**답변 1**
> There are no Outerwear products or promotion details in the results, so nothing has been drafted yet. Share the Outerwear category or its products to set up the $50 discount on orders above $250 for two weeks.

화면 블록: product_table(6 of 6)

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (19, 23, 59 not shown)
