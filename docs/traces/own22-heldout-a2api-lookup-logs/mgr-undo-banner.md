# mgr-undo-banner — own22-heldout-a2api-lookup-logs

[← 실행 묶음](README.md)

**과업**

> actually put the old homepage banner back

- 답에 있어야 할 사실: the swap is cs_1039, live since 10:00; it can be undone until Nov 7 23:59
- 답에 있어야 할 사실: undo is a person's button on the change set; the agent points to it instead of booking a new banner

### a2api 변환 파사드 + 주문 번호 조회 · 1회차 · ✗ 실패

토큰 5,852 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> actually put the old homepage banner back

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: save_display_banner_list, get_display_corner_list, get_promotion_grid_list, get_promotion_grid_list_count, get_member_grade_list
- 계획: `get_display_corner_list` `` {"ends_at":"2026-11-30T23:59:59-05:00","page_type":"main","starts_at":"2026-11-01T00:00:00-05:00"} ``
1. 에이전트 → **`get_display_corner_list`** `` {"ends_at":"2026-11-30T23:59:59-05:00","page_type":"main","starts_at":"2026-11-01T01:00:00-04:00"} ``
   ← 결과: `` {"list":[{"banners":[{"ends_at":"2026-11-06T09:59:00-05:00","headline":"The October edit","starts_at":"2026-10-01T00:00:00-04:00","booking_id":"dsp_october_edit","display_status":"ended","target_member_grade":"G00"},{"ends_at":null,"headline":"Fall layers","starts_at":"2026-11-06T10:00:00-05:00","booking_id":"dsp_fall_layers","display_status":"active","target_member_grade":"G00"}],"corner_id":"slot_home_hero","corner_name":"Home hero","corner_type":"hero"},{"banners":[],"corner_id":"slot_home_new_in","corner_name":"New in","corner_type":"product_grid"},{"banners":[],"corner_id":"slot_home_stor… (+157자) ``

**답변 1**
> The homepage hero slot currently shows the active banner 'Fall layers' (dsp_fall_layers) that started Fri Nov 6, 10:00 AM. The previous banner 'The October edit' (dsp_october_edit) ended Fri Nov 6, 9:59 AM. I don't have a way to reactivate an ended booking from the current display data, so I can't put the old banner back right now. If you want the October edit to run again, I can schedule a new booking for the Home hero slot with the same headline and timing you want.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: fact "the swap is cs_1039, live since 10:00; it can be undone unti" (1039, 7, 23 not shown)

### a2api 변환 파사드 + 주문 번호 조회 · 2회차 · ✗ 실패

토큰 5,846 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> actually put the old homepage banner back

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: save_display_banner_list, get_display_corner_list, get_promotion_grid_list, get_promotion_grid_list_count, get_member_grade_list
- 계획: `get_display_corner_list` `` {"ends_at":"2026-11-30T23:59:59-05:00","page_type":"main","starts_at":"2026-11-01T00:00:00-05:00"} ``
1. 에이전트 → **`get_display_corner_list`** `` {"ends_at":"2026-11-30T23:59:59-05:00","page_type":"main","starts_at":"2026-11-01T01:00:00-04:00"} ``
   ← 결과: `` {"list":[{"banners":[{"ends_at":"2026-11-06T09:59:00-05:00","headline":"The October edit","starts_at":"2026-10-01T00:00:00-04:00","booking_id":"dsp_october_edit","display_status":"ended","target_member_grade":"G00"},{"ends_at":null,"headline":"Fall layers","starts_at":"2026-11-06T10:00:00-05:00","booking_id":"dsp_fall_layers","display_status":"active","target_member_grade":"G00"}],"corner_id":"slot_home_hero","corner_name":"Home hero","corner_type":"hero"},{"banners":[],"corner_id":"slot_home_new_in","corner_name":"New in","corner_type":"product_grid"},{"banners":[],"corner_id":"slot_home_stor… (+157자) ``

**답변 1**
> The homepage hero slot currently shows the active banner “Fall layers” (dsp_fall_layers) that started Fri Nov 6, 10:00 AM. The previous banner “The October edit” (dsp_october_edit) ended Fri Nov 6, 9:59 AM. I don’t have a way to reactivate an ended booking from the data shown, and no other homepage banners are listed. If you want a different banner back, tell me which headline or booking to use and I’ll schedule it for the Home hero slot.

화면 블록: product_table(4 of 4)

**채점**: ✗ 실패 — 빠진 것: fact "the swap is cs_1039, live since 10:00; it can be undone unti" (1039, 7, 23 not shown)
