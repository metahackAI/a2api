# mk-hero-free-next-weekend — ours-design-9

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> is the homepage hero open next weekend? want to run something for VIPs

- 필요한 도구: `list_display_slots`
- 허용 도구: `get_display_slot`, `list_banners`
- 답에 있어야 할 사실: next weekend is Sat Nov 14 – Sun Nov 15
- 답에 있어야 할 사실: the home hero shows Fall layers to everyone with no end date, and is free for VIP, Gold and Member audiences all of Nov 14–15
- 부르면 안 됨: schedule_banner

### a2api-acom-hybrid · 1회차 · ✗ 실패

토큰 22,150 · 26.574초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 4,933토큰

준비: 전략 `index`, 함수 253개, 목차 4,645자(system prompt)

**질문 1**
> is the homepage hero open next weekend? want to run something for VIPs

1. 모델 → **`a2api_load`** `` {"names":["list_tiers","list_display_slots"]} ``
   ← 결과 105B: `` {"already":["list_tiers","list_display_slots"],"note":"These functions are already callable; call them."} ``
2. 모델 → **`list_tiers`** `` {} ``
   ← 결과 305B: `` {"status":"succeeded","data":{"items":[{"id":"vip","name":"VIP","rank":3,"program_id":"prg_rewards","member_count":1284},{"id":"gold","name":"Gold","rank":2,"program_id":"prg_rewards","member_count":2900},{"id":"member","name":"Member","rank":1,"program_id":"prg_rewards","member_count":9816}],"total":3}} ``
3. 모델 → **`list_display_slots`** `` {"page":"main","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","audience":"vip","slot_type":"hero"} ``
   ← 결과 509B: `` {"status":"succeeded","data":{"items":[{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"]}],"availability":[{"audience":"vip","free_from":"2026-11-07T00:00:00-05:00","free_until":"2026-11-08T23:59:00-05:00"}]}],"total":1}} ``

**답변 1**
> Yes — the Home hero is free for VIPs next weekend.
>
> * Slot: **slot_home_hero** – Home hero on the main page
> * Period checked: Sat 2026-11-07 00:00 to Sun 2026-11-08 23:59 America/New_York
> * Audience: VIP  `vip` – 1,284 members
>
> Availability for VIP:
> * free_from: 2026-11-07T00:00:00-05:00
> * free_until: 2026-11-08T23:59:00-05:00
>
> Current booking on the slot:
> * dsp_fall_layers – “Fall layers”, audience = everyone, active from 2026-11-06T10:00:00-05:00, valid_through = null
>
> So the hero is booked for everyone but the VIP audience window is completely open for the whole weekend of Nov 7-8. You can schedule a VIP-targeted display for that period.

**채점**: ✗ 실패 — 빠진 것: fact "next weekend is Sat Nov 14 – Sun Nov 15" (14, 15 not shown); fact "the home hero shows Fall layers to everyone with no end date" (14, 15 not shown)
(도구 정밀도 0.50, 재현율 1.00)

### a2api-acom-hybrid · 2회차 · ✗ 실패

토큰 22,150 · 26.463초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 4,933토큰

준비: 전략 `index`, 함수 253개, 목차 4,645자(system prompt)

**질문 1**
> is the homepage hero open next weekend? want to run something for VIPs

1. 모델 → **`a2api_load`** `` {"names":["list_tiers","list_display_slots"]} ``
   ← 결과 105B: `` {"already":["list_tiers","list_display_slots"],"note":"These functions are already callable; call them."} ``
2. 모델 → **`list_tiers`** `` {} ``
   ← 결과 305B: `` {"status":"succeeded","data":{"items":[{"id":"vip","name":"VIP","rank":3,"program_id":"prg_rewards","member_count":1284},{"id":"gold","name":"Gold","rank":2,"program_id":"prg_rewards","member_count":2900},{"id":"member","name":"Member","rank":1,"program_id":"prg_rewards","member_count":9816}],"total":3}} ``
3. 모델 → **`list_display_slots`** `` {"page":"main","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","audience":"vip","slot_type":"hero"} ``
   ← 결과 509B: `` {"status":"succeeded","data":{"items":[{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"]}],"availability":[{"audience":"vip","free_from":"2026-11-07T00:00:00-05:00","free_until":"2026-11-08T23:59:00-05:00"}]}],"total":1}} ``

**답변 1**
> Yes — the Home hero is free for VIPs next weekend.
>
> * Slot: **slot_home_hero** – Home hero on the main page
> * Period checked: Sat 2026-11-07 00:00 to Sun 2026-11-08 23:59 America/New_York
> * Audience: VIP  `vip` – 1,284 members
>
> Availability for VIP:
> * free_from: 2026-11-07T00:00:00-05:00
> * free_until: 2026-11-08T23:59:00-05:00
>
> Current booking on the slot:
> * dsp_fall_layers – “Fall layers”, audience = everyone, active from 2026-11-06T10:00:00-05:00, valid_through = null
>
> So the hero is booked for everyone but the VIP audience window is completely open for the whole weekend of Nov 7-8. You can schedule a VIP-targeted display for that period.

**채점**: ✗ 실패 — 빠진 것: fact "next weekend is Sat Nov 14 – Sun Nov 15" (14, 15 not shown); fact "the home hero shows Fall layers to everyone with no end date" (14, 15 not shown)
(도구 정밀도 0.50, 재현율 1.00)
