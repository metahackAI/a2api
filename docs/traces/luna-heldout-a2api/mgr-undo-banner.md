# mgr-undo-banner — luna-heldout-a2api

[← 실행 묶음](README.md)

**과업**

> actually put the old homepage banner back

- 답에 있어야 할 사실: the swap is cs_1039, live since 10:00; it can be undone until Nov 7 23:59
- 답에 있어야 할 사실: undo is a person's button on the change set; the agent points to it instead of booking a new banner

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 1회차 · ✗ 실패

토큰 15,019 · 모델 호출 2회 · 도구 호출 1회

**질문 1**
> actually put the old homepage banner back

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: save_display_banner_list, get_display_corner_list, get_promotion_grid_list, get_promotion_grid_list_count, get_member_grade_list
- 계획: `get_display_corner_list` `` {"ends_at":"2026-11-06T23:59","page_type":"main","starts_at":"2026-11-06T00:00"} ``
1. 에이전트 → **`get_display_corner_list`** `` {"ends_at":"2026-11-06T23:59:00-05:00","page_type":"main","starts_at":"2026-11-06T00:00:00-05:00"} ``
   ← 결과: `` {"list":[{"banners":[{"ends_at":"2026-11-06T09:59:00-05:00","headline":"The October edit","starts_at":"2026-10-01T00:00:00-04:00","booking_id":"dsp_october_edit","display_status":"ended","target_member_grade":"G00"},{"ends_at":null,"headline":"Fall layers","starts_at":"2026-11-06T10:00:00-05:00","booking_id":"dsp_fall_layers","display_status":"active","target_member_grade":"G00"}],"corner_id":"slot_home_hero","corner_name":"Home hero","corner_type":"hero"},{"banners":[],"corner_id":"slot_home_new_in","corner_name":"New in","corner_type":"product_grid"},{"banners":[],"corner_id":"slot_home_stor… (+157자) ``

**답변 1**
> The old homepage banner, “The October edit,” has ended, and “Fall layers” is currently active in the Home hero slot. Nothing was changed, so you’ll need to decide which banner should be displayed.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: fact "the swap is cs_1039, live since 10:00; it can be undone unti" (1039, 10, 0, 7, 23, 59 not shown)

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 2회차 · ✗ 실패

토큰 14,631 · 모델 호출 2회 · 도구 호출 1회

**질문 1**
> actually put the old homepage banner back

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: save_display_banner_list, get_display_corner_list, get_promotion_grid_list, get_promotion_grid_list_count, get_member_grade_list
- 계획: `get_display_corner_list` `` {"ends_at":"2030-12-31T23:59","page_type":"main","starts_at":"2020-01-01T00:00"} ``
1. 에이전트 → **`get_display_corner_list`** `` {"ends_at":"2030-12-31T23:59:00-05:00","page_type":"main","starts_at":"2020-01-01T00:00:00-05:00"} ``
   ← 결과: `` {"list":[{"banners":[{"ends_at":"2026-11-06T09:59:00-05:00","headline":"The October edit","starts_at":"2026-10-01T00:00:00-04:00","booking_id":"dsp_october_edit","display_status":"ended","target_member_grade":"G00"},{"ends_at":null,"headline":"Fall layers","starts_at":"2026-11-06T10:00:00-05:00","booking_id":"dsp_fall_layers","display_status":"active","target_member_grade":"G00"}],"corner_id":"slot_home_hero","corner_name":"Home hero","corner_type":"hero"},{"banners":[],"corner_id":"slot_home_new_in","corner_name":"New in","corner_type":"product_grid"},{"banners":[],"corner_id":"slot_home_stor… (+157자) ``

**답변 1**
> “Fall layers” is the active Home hero banner; the previous “The October edit” banner has ended. No change is drafted, so there’s nothing to approve yet.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: fact "the swap is cs_1039, live since 10:00; it can be undone unti" (1039, 10, 0, 7, 23, 59 not shown)

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 3회차 · ✗ 실패

토큰 13,711 · 모델 호출 2회 · 도구 호출 1회

**질문 1**
> actually put the old homepage banner back

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: save_display_banner_list, get_display_corner_list, get_promotion_grid_list, get_promotion_grid_list_count, get_member_grade_list
- 계획: `get_display_corner_list` `` {"ends_at":"2026-11-06T11:00","page_type":"main","starts_at":"2026-11-06T11:00"} ``
1. 에이전트 → **`get_display_corner_list`** `` {"ends_at":"2026-11-06T11:00:00-05:00","page_type":"main","starts_at":"2026-11-06T11:00:00-05:00"} ``
   ← 결과: `` {"list":[{"banners":[{"ends_at":null,"headline":"Fall layers","starts_at":"2026-11-06T10:00:00-05:00","booking_id":"dsp_fall_layers","display_status":"active","target_member_grade":"G00"}],"corner_id":"slot_home_hero","corner_name":"Home hero","corner_type":"hero"},{"banners":[],"corner_id":"slot_home_new_in","corner_name":"New in","corner_type":"product_grid"},{"banners":[],"corner_id":"slot_home_stories","corner_name":"Stories","corner_type":"banner_board"},{"banners":[],"corner_id":"slot_home_brands","corner_name":"Brands","corner_type":"brand_strip"}]} ``

**답변 1**
> The Home hero already has the “Fall layers” banner active, starting Fri Nov 6 at 10:00 AM, with no end date. Nothing needs to be changed.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: fact "the swap is cs_1039, live since 10:00; it can be undone unti" (1039, 7, 23, 59 not shown)
