# mk-hero-free-next-weekend — luna-design-a2api

[← 실행 묶음](README.md)

**과업**

> is the homepage hero open next weekend? want to run something for VIPs

- 답에 있어야 할 사실: next weekend is Sat Nov 14 – Sun Nov 15
- 답에 있어야 할 사실: the home hero shows Fall layers to everyone with no end date, and is free for VIP, Gold and Member audiences all of Nov 14–15

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 1회차 · ✓ 통과

토큰 29,945 · 모델 호출 4회 · 도구 호출 2회

**질문 1**
> is the homepage hero open next weekend? want to run something for VIPs

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 9 candidates: get_member_grade_list, get_promotion_target_member_list_count, save_coupon_list, get_promotion_grid_list_count, get_promotion_grid_list, get_promotion_target_member_list, get_product_grid_list_count, get_product_grid_list, save_display_banner_list
- 계획: `get_member_grade_list` `` {} ``; `get_promotion_grid_list` `` {"page":1,"page_size":100,"active_from":"2026-11-14T00:00","active_until":"2026-11-15T23:59"} ``
1. 에이전트 → **`get_member_grade_list`** `` {} ``
   ← 결과: `` {"list":[{"rank":3,"grade_name":"VIP","member_count":1284,"member_grade":"G03"},{"rank":2,"grade_name":"Gold","member_count":2900,"member_grade":"G02"},{"rank":1,"grade_name":"Member","member_count":9816,"member_grade":"G01"}]} ``
2. 에이전트 → **`get_promotion_grid_list`** `` {"page":1,"page_size":100,"active_from":"2026-11-14T00:00:00-05:00","active_until":"2026-11-15T23:59:00-05:00"} ``
   ← 결과: `` {"list":[{"ends_at":"2026-11-20T23:59:00-05:00","starts_at":"2026-11-13T00:00:00-05:00","promotion_id":"promo_denim_bundle","promotion_name":"Denim bundle","promotion_type":"order_discount","promotion_status":"scheduled","target_member_grade":"G00"},{"ends_at":"2026-11-15T23:59:00-05:00","starts_at":"2026-11-01T00:00:00-04:00","promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00"},{"ends_at":null,"starts_at":"2026-01-01T00:00:00-05:00","promotion_id":"promo_birthday","promotion_n… (+571자) ``

**답변 1**
> The homepage hero’s availability isn’t shown in these results, so I can’t tell whether it’s open next weekend (Sat Nov 14–Sun Nov 15). There’s no VIP promotion specified yet; tell me what you’d like to run, and the VIP tier is available.

화면 블록: product_table(5 of 5)

**채점**: ✓ 통과

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 2회차 · ✗ 실패

토큰 38,713 · 모델 호출 5회 · 도구 호출 3회

**질문 1**
> is the homepage hero open next weekend? want to run something for VIPs

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 9 candidates: get_member_grade_list, get_promotion_target_member_list_count, save_coupon_list, get_promotion_grid_list_count, get_promotion_grid_list, get_promotion_target_member_list, get_product_grid_list_count, get_product_grid_list, save_display_banner_list
- 계획: `get_promotion_grid_list` `` {"active_from":"2026-11-07T00:00","active_until":"2026-11-08T23:59","target_member_grade":"VIP"} ``
1. 에이전트 → **`get_promotion_grid_list`** `` {"active_from":"2026-11-07T00:00:00-05:00","active_until":"2026-11-08T23:59:00-05:00","target_member_grade":"VIP"} ``
   ← 실패: `` {"code":"upstream_validation_failed","class":"invalid_input","message":"The backend rejected the request values. (HTTP 422) Invalid member grade code.","next_tool":null} ``
- 계획: `get_member_grade_list` `` {} ``; `get_promotion_grid_list` `` {"active_from":"2026-11-07T00:00","active_until":"2026-11-08T23:59"} ``
2. 에이전트 → **`get_member_grade_list`** `` {} ``
   ← 결과: `` {"list":[{"rank":3,"grade_name":"VIP","member_count":1284,"member_grade":"G03"},{"rank":2,"grade_name":"Gold","member_count":2900,"member_grade":"G02"},{"rank":1,"grade_name":"Member","member_count":9816,"member_grade":"G01"}]} ``
3. 에이전트 → **`get_promotion_grid_list`** `` {"active_from":"2026-11-07T00:00:00-05:00","active_until":"2026-11-08T23:59:00-05:00"} ``
   ← 결과: `` {"list":[{"ends_at":"2026-11-15T23:59:00-05:00","starts_at":"2026-11-01T00:00:00-04:00","promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00"},{"ends_at":null,"starts_at":"2026-01-01T00:00:00-05:00","promotion_id":"promo_birthday","promotion_name":"Birthday coupon","promotion_type":"order_discount","promotion_status":"running","target_member_grade":"G01"},{"ends_at":null,"starts_at":"2026-01-01T00:00:00-05:00","promotion_id":"promo_free_ship_80","promotion_name":"Free shipping ov… (+329자) ``

**답변 1**
> The homepage hero’s availability next weekend, Sat Nov 7 through Sun Nov 8, isn’t shown in these results. They also don’t show a VIP promotion for that weekend, so there’s nothing here to confirm or plan yet.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: fact "next weekend is Sat Nov 14 – Sun Nov 15" (14 not shown); fact "the home hero shows Fall layers to everyone with no end date" (14 not shown)

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 3회차 · ✗ 실패

토큰 29,475 · 모델 호출 4회 · 도구 호출 1회

**질문 1**
> is the homepage hero open next weekend? want to run something for VIPs

- 라우팅: Promotion agent (chosen by the model)
- 도구 검색 후보: 9 candidates: get_member_grade_list, get_promotion_target_member_list_count, save_coupon_list, get_promotion_grid_list_count, get_promotion_grid_list, get_promotion_target_member_list, get_product_grid_list_count, get_product_grid_list, save_display_banner_list
- 계획: `get_promotion_grid_list` `` {"page":1,"page_size":100,"active_from":"2026-11-07T00:00","active_until":"2026-11-08T23:59"} ``
1. 에이전트 → **`get_promotion_grid_list`** `` {"page":1,"page_size":100,"active_from":"2026-11-07T00:00:00-05:00","active_until":"2026-11-08T23:59:00-05:00"} ``
   ← 결과: `` {"list":[{"ends_at":"2026-11-15T23:59:00-05:00","starts_at":"2026-11-01T00:00:00-04:00","promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00"},{"ends_at":null,"starts_at":"2026-01-01T00:00:00-05:00","promotion_id":"promo_birthday","promotion_name":"Birthday coupon","promotion_type":"order_discount","promotion_status":"running","target_member_grade":"G01"},{"ends_at":null,"starts_at":"2026-01-01T00:00:00-05:00","promotion_id":"promo_free_ship_80","promotion_name":"Free shipping ov… (+330자) ``

**답변 1**
> The homepage hero’s availability for Nov 7–8 hasn’t been checked, so I can’t tell whether it’s open. Nothing has been planned for VIPs yet.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: fact "next weekend is Sat Nov 14 – Sun Nov 15" (14 not shown); fact "the home hero shows Fall layers to everyone with no end date" (14 not shown)
