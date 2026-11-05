# mgr-undo-banner — luna-heldout-acom

[← 실행 묶음](README.md)

**과업**

> actually put the old homepage banner back

- 답에 있어야 할 사실: the swap is cs_1039, live since 10:00; it can be undone until Nov 7 23:59
- 답에 있어야 할 사실: undo is a person's button on the change set; the agent points to it instead of booking a new banner

### GPT-6-Luna · A-Commerce 도구(참고) · 1회차 · ✗ 실패

토큰 17,348 · 모델 호출 2회 · 도구 호출 1회

**질문 1**
> actually put the old homepage banner back

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 14 candidates: list_tasks, list_active_promotions, search_products, list_tiers, get_curation, set_banner, list_banners, restore_coupon, get_coupon, get_promotion, list_curations, get_display_slot, schedule_banner, create_curation
- 계획: `list_banners` `` {"page":"main"} ``
1. 에이전트 → **`list_banners`** `` {"page":"main"} ``
   ← 결과: `` {"items":[{"id":"bnr_fall_layers","url":"/c/fall-layers","name":"Fall layers","eyebrow":"NEW SEASON","bookings":[{"status":"active","slot_id":"slot_home_hero","audience":"everyone","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"display_booking_id":"dsp_fall_layers"}],"channels":["web","mobile_web","app"],"headline":"Fall layers","priority":null,"cta_label":"Shop fall layers","content_url":"/media/products/prd_wool_overcoat-b50a91c0.webp","image_color":"Charcoal","image_product_id":"prd_wool_overcoat","alternative_headline":"Coats, knits and fleece for cold starts"},{"id":"bnr_o… (+578자) ``

**답변 1**
> The old homepage banner, “October edit,” has ended, and no change has been drafted to restore it. Nothing has been put back yet.

화면 블록: product_table(2 of 2)

**채점**: ✗ 실패 — 빠진 것: tool search_change_sets; fact "the swap is cs_1039, live since 10:00; it can be undone unti" (1039, 10, 0, 7, 23, 59 not shown)

### GPT-6-Luna · A-Commerce 도구(참고) · 2회차 · ✗ 실패

토큰 17,285 · 모델 호출 2회 · 도구 호출 1회

**질문 1**
> actually put the old homepage banner back

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 14 candidates: list_tasks, list_active_promotions, search_products, list_tiers, get_curation, set_banner, list_banners, restore_coupon, get_coupon, get_promotion, list_curations, get_display_slot, schedule_banner, create_curation
- 계획: `list_banners` `` {"page":"main"} ``
1. 에이전트 → **`list_banners`** `` {"page":"main"} ``
   ← 결과: `` {"items":[{"id":"bnr_fall_layers","url":"/c/fall-layers","name":"Fall layers","eyebrow":"NEW SEASON","bookings":[{"status":"active","slot_id":"slot_home_hero","audience":"everyone","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"display_booking_id":"dsp_fall_layers"}],"channels":["web","mobile_web","app"],"headline":"Fall layers","priority":null,"cta_label":"Shop fall layers","content_url":"/media/products/prd_wool_overcoat-b50a91c0.webp","image_color":"Charcoal","image_product_id":"prd_wool_overcoat","alternative_headline":"Coats, knits and fleece for cold starts"},{"id":"bnr_o… (+578자) ``

**답변 1**
> The old homepage banner, “October edit,” has ended, and “Fall layers” is currently active in the homepage hero slot. Nothing has been changed yet; there’s no draft to approve.

화면 블록: product_table(2 of 2)

**채점**: ✗ 실패 — 빠진 것: tool search_change_sets; fact "the swap is cs_1039, live since 10:00; it can be undone unti" (1039, 10, 0, 7, 23, 59 not shown)

### GPT-6-Luna · A-Commerce 도구(참고) · 3회차 · ✗ 실패

토큰 16,978 · 모델 호출 2회 · 도구 호출 1회

**질문 1**
> actually put the old homepage banner back

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 14 candidates: list_tasks, list_active_promotions, search_products, list_tiers, get_curation, set_banner, list_banners, restore_coupon, get_coupon, get_promotion, list_curations, get_display_slot, schedule_banner, create_curation
- 계획: `list_banners` `` {"page":"main"} ``
1. 에이전트 → **`list_banners`** `` {"page":"main"} ``
   ← 결과: `` {"items":[{"id":"bnr_fall_layers","url":"/c/fall-layers","name":"Fall layers","eyebrow":"NEW SEASON","bookings":[{"status":"active","slot_id":"slot_home_hero","audience":"everyone","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"display_booking_id":"dsp_fall_layers"}],"channels":["web","mobile_web","app"],"headline":"Fall layers","priority":null,"cta_label":"Shop fall layers","content_url":"/media/products/prd_wool_overcoat-b50a91c0.webp","image_color":"Charcoal","image_product_id":"prd_wool_overcoat","alternative_headline":"Coats, knits and fleece for cold starts"},{"id":"bnr_o… (+578자) ``

**답변 1**
> The old homepage banner, “October edit,” is no longer active; “Fall layers” is currently active. Nothing has been changed, so there’s nothing to approve yet.

화면 블록: product_table(2 of 2)

**채점**: ✗ 실패 — 빠진 것: tool search_change_sets; fact "the swap is cs_1039, live since 10:00; it can be undone unti" (1039, 10, 0, 7, 23, 59 not shown)
