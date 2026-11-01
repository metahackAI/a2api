# mk-hero-free-next-weekend — ours-design-4

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `879cc92`

**과업**

> is the homepage hero open next weekend? want to run something for VIPs

- 필요한 도구: `list_display_slots`
- 허용 도구: `get_display_slot`, `list_banners`
- 답에 있어야 할 사실: next weekend is Sat Nov 14 – Sun Nov 15
- 답에 있어야 할 사실: the home hero shows Fall layers to everyone with no end date, and is free for VIP, Gold and Member audiences all of Nov 14–15
- 부르면 안 됨: schedule_banner

### a2api-acom · 1회차 · ✗ 실패

토큰 13,770 · 22.345초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 3,959토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> is the homepage hero open next weekend? want to run something for VIPs

1. 모델 → **`acom_list_tiers`** `` {} ``
   ← 결과 305B: `` {"status":"succeeded","data":{"items":[{"id":"vip","name":"VIP","rank":3,"program_id":"prg_rewards","member_count":1284},{"id":"gold","name":"Gold","rank":2,"program_id":"prg_rewards","member_count":2900},{"id":"member","name":"Member","rank":1,"program_id":"prg_rewards","member_count":9816}],"total":3}} ``
2. 모델 → **`acom_list_display_slots`** `` {"page":"main","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","audience":"vip","slot_type":"hero"} ``
   ← 결과 509B: `` {"status":"succeeded","data":{"items":[{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"]}],"availability":[{"audience":"vip","free_from":"2026-11-07T00:00:00-05:00","free_until":"2026-11-08T23:59:00-05:00"}]}],"total":1}} ``

**답변 1**
> Yes — the Home hero on the main page is free for VIPs next weekend.
>
> * Slot: `slot_home_hero` – Home hero, `hero` on `main`
> * Period checked: Sat 2026-11-07 00:00 to Sun 2026-11-08 23:59 America/New_York
> * VIP availability: free_from 2026-11-07T00:00:00-05:00 → free_until 2026-11-08T23:59:00-05:00
>
> Note: the slot is currently booked for `everyone` with `dsp_fall_layers` “Fall layers” from 2026-11-06T10:00:00-05:00 onward, active. The VIP audience window is still open for a VIP-targeted booking on 7-8 Nov.

**채점**: ✗ 실패 — 빠진 것: fact "next weekend is Sat Nov 14 – Sun Nov 15" (14, 15 not shown); fact "the home hero shows Fall layers to everyone with no end date" (14, 15 not shown)
(도구 정밀도 0.50, 재현율 1.00)

### a2api-facade · 1회차 · ✓ 통과

토큰 25,473 · 54.077초 · 모델 호출 6회 · 도구 호출 5회 · 첫 요청 프롬프트 2,465토큰

준비: 전략 `search`, 함수 7개

**질문 1**
> is the homepage hero open next weekend? want to run something for VIPs

1. 모델 → **`facade_get_disp_corner_list`** `` {"page_type":"main","starts_at":"2026-11-07T00:00:00","ends_at":"2026-11-08T23:59:59","corner_type":"hero"} ``
   ← 결과 297B: `` {"status":"succeeded","data":{"list":[{"corner_id":"slot_home_hero","corner_name":"Home hero","corner_type":"hero","banners":[{"booking_id":"dsp_fall_layers","target_member_grade":"G00","headline":"Fall layers","starts_at":"2026-11-06T10:00:00-05:00","ends_at":null,"display_status":"active"}]}]}} ``
2. 모델 → **`a2api_search`** `` {"query":"member grade"} ``
   ← 결과 425B: `` {"selected":[{"name":"facade_get_mbr_grd_list","id":"facade.get_mbr_grd_list"},{"name":"facade_get_prmt_tgt_mbr_list","id":"facade.get_prmt_tgt_mbr_list"},{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_get_prmt_grid_list","id":"facade.get_prmt_grid_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
3. 모델 → **`facade_get_mbr_grd_list`** `` {} ``
   ← 결과 257B: `` {"status":"succeeded","data":{"list":[{"member_grade":"G03","grade_name":"VIP","member_count":1284,"rank":3},{"member_grade":"G02","grade_name":"Gold","member_count":2900,"rank":2},{"member_grade":"G01","grade_name":"Member","member_count":9816,"rank":1}]}} ``
4. 모델 → **`facade_get_disp_corner_list`** `` {"page_type":"main","starts_at":"2026-11-14T00:00:00","ends_at":"2026-11-15T23:59:59","corner_type":"hero"} ``
   ← 결과 297B: `` {"status":"succeeded","data":{"list":[{"corner_id":"slot_home_hero","corner_name":"Home hero","corner_type":"hero","banners":[{"booking_id":"dsp_fall_layers","target_member_grade":"G00","headline":"Fall layers","starts_at":"2026-11-06T10:00:00-05:00","ends_at":null,"display_status":"active"}]}]}} ``
5. 모델 → **`facade_get_disp_corner_list`** `` {"page_type":"main","starts_at":"2026-11-07T00:00:00","ends_at":"2026-11-08T23:59:59","corner_type":"hero"} ``
   ← 결과 405B: `` {"status":"succeeded","data":{"list":[{"corner_id":"slot_home_hero","corner_name":"Home hero","corner_type":"hero","banners":[{"booking_id":"dsp_fall_layers","target_member_grade":"G00","headline":"Fall layers","starts_at":"2026-11-06T10:00:00-05:00","ends_at":null,"display_status":"active"}]}]},"note":"Same call and result as 1 earlier time(s); you already have this data. Use it, or answer the user."} ``

**답변 1**
> The Home hero slot is not free next weekend.
>
> * **Slot:** `slot_home_hero` – Home hero, `corner_type` hero, `page_type` main
> * **Current booking:** `dsp_fall_layers`
>   * `target_member_grade`: G00 – every shopper
>   * `headline`: Fall layers
>   * `starts_at`: 2026-11-06T10:00:00-05:00
>   * `ends_at`: null
>   * `display_status`: active
>
> The booking is active with no end date, so it covers the period you asked about:
>
> * This weekend 2026-11-07 to 2026-11-08: occupied by the active G00 banner
> * Next weekend 2026-11-14 to 2026-11-15: occupied by the same active G00 banner
>
> Member grade for VIPs in the system is:
> * `G03` – VIP, member_count 1,284, rank 3
>
> If you want a VIP-only hero for that weekend you would be scheduling an additional banner targeting `G03` on top of the existing G00 “Fall layers” booking. Want me to draft an insert for `slot_home_hero` with `target_member_grade` G03 for 2026-11-14/15?

**채점**: ✓ 통과
