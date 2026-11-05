# mgr-undo-banner — own-latest-heldout-a2api

[← 실행 묶음](README.md)

**과업**

> actually put the old homepage banner back

- 답에 있어야 할 사실: the swap is cs_1039, live since 10:00; it can be undone until Nov 7 23:59
- 답에 있어야 할 사실: undo is a person's button on the change set; the agent points to it instead of booking a new banner

### a2api 변환 파사드 · 1회차 · ✗ 실패

토큰 6,729 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> actually put the old homepage banner back

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: save_display_banner_list, get_display_corner_list, get_promotion_grid_list, get_promotion_grid_list_count, get_member_grade_list
- 계획: `get_display_corner_list` `` {"ends_at":"2026-11-06T23:59","page_type":"main","starts_at":"2026-11-06T00:00"} ``
1. 에이전트 → **`get_display_corner_list`** `` {"ends_at":"2026-11-06T23:59:00-05:00","page_type":"main","starts_at":"2026-11-06T00:00:00-05:00"} ``
   ← 결과: `` {"list":[{"banners":[{"ends_at":"2026-11-06T09:59:00-05:00","headline":"The October edit","starts_at":"2026-10-01T00:00:00-04:00","booking_id":"dsp_october_edit","display_status":"ended","target_member_grade":"G00"},{"ends_at":null,"headline":"Fall layers","starts_at":"2026-11-06T10:00:00-05:00","booking_id":"dsp_fall_layers","display_status":"active","target_member_grade":"G00"}],"corner_id":"slot_home_hero","corner_name":"Home hero","corner_type":"hero"},{"banners":[],"corner_id":"slot_home_new_in","corner_name":"New in","corner_type":"product_grid"},{"banners":[],"corner_id":"slot_home_stor… (+157자) ``

**답변 1**
> The Home hero slot currently shows the active banner “Fall layers” (dsp_fall_layers) that started Fri Nov 6, 10:00 AM. The previous banner “The October edit” (dsp_october_edit) ended Fri Nov 6, 9:59 AM. I don’t have a booking to reactivate the old banner, and there’s no change set to put it back. If you want the October edit shown again, tell me the new start/end time and which member grade it should target, and I’ll schedule it.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: fact "the swap is cs_1039, live since 10:00; it can be undone unti" (1039, 7, 23 not shown)

### a2api 변환 파사드 · 2회차 · ✗ 실패

토큰 6,748 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> actually put the old homepage banner back

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: save_display_banner_list, get_display_corner_list, get_promotion_grid_list, get_promotion_grid_list_count, get_member_grade_list
- 계획: `get_display_corner_list` `` {"ends_at":"2026-11-06T23:59","page_type":"main","starts_at":"2026-11-06T00:00"} ``
1. 에이전트 → **`get_display_corner_list`** `` {"ends_at":"2026-11-06T23:59:00-05:00","page_type":"main","starts_at":"2026-11-06T00:00:00-05:00"} ``
   ← 결과: `` {"list":[{"banners":[{"ends_at":"2026-11-06T09:59:00-05:00","headline":"The October edit","starts_at":"2026-10-01T00:00:00-04:00","booking_id":"dsp_october_edit","display_status":"ended","target_member_grade":"G00"},{"ends_at":null,"headline":"Fall layers","starts_at":"2026-11-06T10:00:00-05:00","booking_id":"dsp_fall_layers","display_status":"active","target_member_grade":"G00"}],"corner_id":"slot_home_hero","corner_name":"Home hero","corner_type":"hero"},{"banners":[],"corner_id":"slot_home_new_in","corner_name":"New in","corner_type":"product_grid"},{"banners":[],"corner_id":"slot_home_stor… (+157자) ``

**답변 1**
> The Home hero slot currently shows the active banner 'Fall layers' (dsp_fall_layers) that started Fri Nov 6, 10:00 AM. The previous banner 'The October edit' (dsp_october_edit) ended Fri Nov 6, 9:59 AM. I don't have a booking to reactivate the old banner, and no change set was created this turn. To put the old homepage banner back, a new booking for 'The October edit' in slot_home_hero would need to be scheduled with a start time now and an end time, or the existing 'Fall layers' booking would need to be ended and replaced.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: fact "the swap is cs_1039, live since 10:00; it can be undone unti" (1039, 7, 23 not shown)

### a2api 변환 파사드 · 3회차 · ✗ 실패

토큰 6,748 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> actually put the old homepage banner back

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: save_display_banner_list, get_display_corner_list, get_promotion_grid_list, get_promotion_grid_list_count, get_member_grade_list
- 계획: `get_display_corner_list` `` {"ends_at":"2026-11-06T23:59","page_type":"main","starts_at":"2026-11-06T00:00"} ``
1. 에이전트 → **`get_display_corner_list`** `` {"ends_at":"2026-11-06T23:59:00-05:00","page_type":"main","starts_at":"2026-11-06T00:00:00-05:00"} ``
   ← 결과: `` {"list":[{"banners":[{"ends_at":"2026-11-06T09:59:00-05:00","headline":"The October edit","starts_at":"2026-10-01T00:00:00-04:00","booking_id":"dsp_october_edit","display_status":"ended","target_member_grade":"G00"},{"ends_at":null,"headline":"Fall layers","starts_at":"2026-11-06T10:00:00-05:00","booking_id":"dsp_fall_layers","display_status":"active","target_member_grade":"G00"}],"corner_id":"slot_home_hero","corner_name":"Home hero","corner_type":"hero"},{"banners":[],"corner_id":"slot_home_new_in","corner_name":"New in","corner_type":"product_grid"},{"banners":[],"corner_id":"slot_home_stor… (+157자) ``

**답변 1**
> The Home hero slot currently shows the active banner 'Fall layers' (dsp_fall_layers) that started Fri Nov 6, 10:00 AM. The previous banner 'The October edit' (dsp_october_edit) ended Fri Nov 6, 9:59 AM. I don't have a booking to reactivate the old banner, and no change set was created this turn. To put the old homepage banner back, a new booking for 'The October edit' in slot_home_hero would need to be scheduled with a start time now and an end time, or the existing 'Fall layers' booking would need to be ended and replaced.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: fact "the swap is cs_1039, live since 10:00; it can be undone unti" (1039, 7, 23 not shown)
