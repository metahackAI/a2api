# mk-hero-free-next-weekend — ours-design-7

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> is the homepage hero open next weekend? want to run something for VIPs

- 필요한 도구: `list_display_slots`
- 허용 도구: `get_display_slot`, `list_banners`
- 답에 있어야 할 사실: next weekend is Sat Nov 14 – Sun Nov 15
- 답에 있어야 할 사실: the home hero shows Fall layers to everyone with no end date, and is free for VIP, Gold and Member audiences all of Nov 14–15
- 부르면 안 됨: schedule_banner

### a2api-acom · 1회차 · ✓ 통과

토큰 13,826 · 23.354초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 3,959토큰

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
> * Slot: `slot_home_hero` — Home hero, hero
> * Audience: VIP `vip` — 1,284 members
> * Period checked: 2026-11-07 00:00 to 2026-11-08 23:59 America/New_York
>
> Availability for VIP:
> * free_from: 2026-11-07T00:00:00-05:00
> * free_until: 2026-11-08T23:59:00-05:00
>
> Current booking on the slot:
> * `dsp_fall_layers` — “Fall layers” for audience everyone, active from 2026-11-06T10:00:00-05:00, valid_through null, change_set_id cs_1039
>
> So the hero is booked for everyone but has free time for VIPs for the whole weekend of Nov 7-8. If you meant the weekend after that, say 14-15 Nov, I can check that period too.

**채점**: ✓ 통과
(도구 정밀도 0.50, 재현율 1.00)

### a2api-acom · 2회차 · ✓ 통과

토큰 13,826 · 23.261초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 3,959토큰

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
> * Slot: `slot_home_hero` — Home hero, hero
> * Audience: VIP `vip` — 1,284 members
> * Period checked: 2026-11-07 00:00 to 2026-11-08 23:59 America/New_York
>
> Availability for VIP:
> * free_from: 2026-11-07T00:00:00-05:00
> * free_until: 2026-11-08T23:59:00-05:00
>
> Current booking on the slot:
> * `dsp_fall_layers` — “Fall layers” for audience everyone, active from 2026-11-06T10:00:00-05:00, valid_through null, change_set_id cs_1039
>
> So the hero is booked for everyone but has free time for VIPs for the whole weekend of Nov 7-8. If you meant the weekend after that, say 14-15 Nov, I can check that period too.

**채점**: ✓ 통과
(도구 정밀도 0.50, 재현율 1.00)

### a2api-acom-index · 1회차 · ✓ 통과

토큰 46,443 · 47.789초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 6,989토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> is the homepage hero open next weekend? want to run something for VIPs

1. 모델 → **`a2api_load`** `` {"names":["list_display_slots","get_display_slot","list_banners","schedule_display"]} ``
   ← 결과 86B: `` {"loaded":["list_display_slots","get_display_slot","list_banners","schedule_display"]} ``
2. 모델 → **`list_display_slots`** `` {"page":"main","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","slot_type":"hero"} ``
   ← 결과 713B: `` {"status":"succeeded","data":{"items":[{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"]}],"availability":[{"audience":"vip","free_from":"2026-11-07T00:00:00-05:00","free_until":"2026-11-08T23:59:00-05:00"},{"audience":"gold","free_from":"2026-11-07T00:00:00-05:00","free_until":"2026-11-08T23:59:00-05:00"},{"au… (+113자) ``
3. 모델 → **`list_display_slots`** `` {"page":"main","valid_from":"2026-11-14T00:00","valid_through":"2026-11-15T23:59","slot_type":"hero","audience":"vip"} ``
   ← 결과 509B: `` {"status":"succeeded","data":{"items":[{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"]}],"availability":[{"audience":"vip","free_from":"2026-11-14T00:00:00-05:00","free_until":"2026-11-15T23:59:00-05:00"}]}],"total":1}} ``
4. 모델 → **`get_display_slot`** `` {"slot_id":"slot_home_hero","as_of":"2026-11-14T12:00"} ``
   ← 결과 1,044B: `` {"status":"succeeded","data":{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","position":1,"item_list_element":[],"bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"],"banner":{"id":"bnr_fall_layers","eyebrow":"NEW SEASON","headline":"Fall layers","alternative_headline":"Coats, knits and fleece for cold starts","cta_label":"Shop fall layers","url":"/c/fall-layer… (+444자) ``

**답변 1**
> Yes — the Home hero is free for VIPs next weekend.
>
> * Slot: `slot_home_hero` – Home hero, page `main`, slot_type `hero`
> * Current booking in place: `dsp_fall_layers` “Fall layers” for `everyone`
>   * valid_from 2026-11-06T10:00:00-05:00, valid_through null, status active
>   * channels web / mobile_web / app
>   * As of 2026-11-14T12:00 the slot is live and VIPs are currently falling back to the everyone booking.
>
> VIP availability:
>
> * 2026-11-07 00:00 – 2026-11-08 23:59 America/New_York: free for VIP
> * 2026-11-14 00:00 – 2026-11-15 23:59 America/New_York: free for VIP
>
> So you can book a VIP-only hero for Sat–Sun 14-15 Nov 2026. The slot’s items would need to be arranged first with `arrange_display_slot`, then `schedule_display` for audience `vip` with `valid_from` 2026-11-14T00:00 and `valid_through` 2026-11-15T23:59. That change would need approval before it reaches shoppers.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-index · 2회차 · ✓ 통과

토큰 33,621 · 26.89초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 6,989토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> is the homepage hero open next weekend? want to run something for VIPs

1. 모델 → **`a2api_load`** `` {"names":["list_display_slots","get_display_slot","list_tiers"]} ``
   ← 결과 65B: `` {"loaded":["list_display_slots","get_display_slot","list_tiers"]} ``
2. 모델 → **`list_tiers`** `` {} ``
   ← 결과 305B: `` {"status":"succeeded","data":{"items":[{"id":"vip","name":"VIP","rank":3,"program_id":"prg_rewards","member_count":1284},{"id":"gold","name":"Gold","rank":2,"program_id":"prg_rewards","member_count":2900},{"id":"member","name":"Member","rank":1,"program_id":"prg_rewards","member_count":9816}],"total":3}} ``
3. 모델 → **`list_display_slots`** `` {"page":"main","valid_from":"2026-11-14T00:00","valid_through":"2026-11-15T23:59","audience":"vip","slot_type":"hero"} ``
   ← 결과 509B: `` {"status":"succeeded","data":{"items":[{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"]}],"availability":[{"audience":"vip","free_from":"2026-11-14T00:00:00-05:00","free_until":"2026-11-15T23:59:00-05:00"}]}],"total":1}} ``

**답변 1**
> Yes — the Home hero is free for VIPs next weekend.
>
> * Slot: **slot_home_hero** – Home hero, page `main`, type `hero`
> * Period checked: 2026-11-14 00:00 → 2026-11-15 23:59 America/New_York
> * Audience: `vip`  – tier id `vip` (VIP, rank 3, 1,284 members)
>
> Availability for VIP:
> * free_from: 2026-11-14T00:00:00-05:00
> * free_until: 2026-11-15T23:59:00-05:00
>
> Current booking on the slot:
> * `dsp_fall_layers` – “Fall layers”, audience `everyone`, valid_from 2026-11-06T10:00:00-05:00, valid_through null, status active
> The everyone booking does not occupy the VIP audience, so the whole weekend 14-15 Nov is open for a VIP-only hero booking.

**채점**: ✓ 통과
(도구 정밀도 0.50, 재현율 1.00)

### a2api-acom-graph · 1회차 · ✓ 통과

토큰 47,025 · 44.379초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 6,989토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> is the homepage hero open next weekend? want to run something for VIPs

1. 모델 → **`a2api_load`** `` {"names":["list_display_slots","get_display_slot","schedule_display","arrange_display_slot"]} ``
   ← 결과 94B: `` {"loaded":["list_display_slots","get_display_slot","schedule_display","arrange_display_slot"]} ``
2. 모델 → **`list_display_slots`** `` {"page":"main","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","slot_type":"hero"} ``
   ← 결과 850B: `` {"status":"succeeded","data":{"items":[{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"]}],"availability":[{"audience":"vip","free_from":"2026-11-07T00:00:00-05:00","free_until":"2026-11-08T23:59:00-05:00"},{"audience":"gold","free_from":"2026-11-07T00:00:00-05:00","free_until":"2026-11-08T23:59:00-05:00"},{"au… (+250자) ``
3. 모델 → **`list_display_slots`** `` {"page":"main","valid_from":"2026-11-14T00:00","valid_through":"2026-11-15T23:59","slot_type":"hero","audience":"vip"} ``
   ← 결과 646B: `` {"status":"succeeded","data":{"items":[{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"]}],"availability":[{"audience":"vip","free_from":"2026-11-14T00:00:00-05:00","free_until":"2026-11-15T23:59:00-05:00"}]}],"total":1},"next":"Functions that take IDs from this result: invalidate_display_cache (slot_id); get_c… (+46자) ``
4. 모델 → **`get_display_slot`** `` {"slot_id":"slot_home_hero"} ``
   ← 결과 1,145B: `` {"status":"succeeded","data":{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","position":1,"item_list_element":[],"bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"],"banner":{"id":"bnr_fall_layers","eyebrow":"NEW SEASON","headline":"Fall layers","alternative_headline":"Coats, knits and fleece for cold starts","cta_label":"Shop fall layers","url":"/c/fall-layer… (+545자) ``

**답변 1**
> Yes — the Home hero is free for VIPs next weekend.
>
> * Slot: **slot_home_hero** – Home hero, page main, slot_type hero
> * VIP availability for the period you asked:
>   * free_from: 2026-11-14T00:00:00-05:00
>   * free_until: 2026-11-15T23:59:00-05:00
>
> Current booking on the slot:
> * display_booking_id dsp_fall_layers, audience everyone, headline “Fall layers”
>   * valid_from 2026-11-06T10:00:00-05:00, valid_through null, status active
>   * channels web, mobile_web, app
>   * change_set_id cs_1039
>
> Right now VIP, gold, member and everyone are all showing that same booking. No VIP-specific booking exists for 2026-11-14/15, so the whole weekend is open for a VIP-only booking.
>
> If you want to run something for VIPs you’ll need to `arrange_display_slot` for slot_home_hero first, then `schedule_display` for audience vip for 2026-11-14T00:00 → 2026-11-15T23:59. That schedule step requires approval before it reaches shoppers.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-graph · 2회차 · ✗ 실패

토큰 35,207 · 41.522초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 6,989토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> is the homepage hero open next weekend? want to run something for VIPs

1. 모델 → **`a2api_load`** `` {"names":["list_display_slots","get_display_slot","list_banners"]} ``
   ← 결과 67B: `` {"loaded":["list_display_slots","get_display_slot","list_banners"]} ``
2. 모델 → **`list_display_slots`** `` {"page":"main","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","slot_type":"hero","limit":20} ``
   ← 결과 850B: `` {"status":"succeeded","data":{"items":[{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"]}],"availability":[{"audience":"vip","free_from":"2026-11-07T00:00:00-05:00","free_until":"2026-11-08T23:59:00-05:00"},{"audience":"gold","free_from":"2026-11-07T00:00:00-05:00","free_until":"2026-11-08T23:59:00-05:00"},{"au… (+250자) ``
3. 모델 → **`get_display_slot`** `` {"slot_id":"slot_home_hero","as_of":"2026-11-07T12:00"} ``
   ← 결과 1,145B: `` {"status":"succeeded","data":{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","position":1,"item_list_element":[],"bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"],"banner":{"id":"bnr_fall_layers","eyebrow":"NEW SEASON","headline":"Fall layers","alternative_headline":"Coats, knits and fleece for cold starts","cta_label":"Shop fall layers","url":"/c/fall-layer… (+545자) ``

**답변 1**
> Yes — the Home hero is free for a VIP-only booking next weekend.
>
> * Slot: `slot_home_hero` – Home hero, page `main`, slot_type `hero`
> * Current booking in place
>   * `dsp_fall_layers` – audience `everyone`, headline “Fall layers”
>   * valid_from `2026-11-06T10:00:00-05:00`, valid_through `null`, status `active`
>   * Channels: web, mobile_web, app
>   * As of 2026-11-07T12:00-05:00 the slot is live and the showing audience mapping is:
>     * everyone → `dsp_fall_layers`
>     * vip → `dsp_fall_layers`
>     * gold → `dsp_fall_layers`
>     * member → `dsp_fall_layers`
>
> * Free time for VIP
>   * audience `vip` free_from `2026-11-07T00:00:00-05:00` free_until `2026-11-08T23:59:00-05:00`
>   * Same free window is shown for gold and member.
>
> So for Saturday 2026-11-07 and Sunday 2026-11-08 the hero is unbooked for a VIP-specific audience. VIPs are currently falling back to the everyone “Fall layers” booking, so you can schedule a VIP-exclusive banner/display for the weekend without conflict.

**채점**: ✗ 실패 — 빠진 것: fact "next weekend is Sat Nov 14 – Sun Nov 15" (14, 15 not shown); fact "the home hero shows Fall layers to everyone with no end date" (14, 15 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names · 1회차 · ✓ 통과

토큰 14,614 · 36.917초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 1,630토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> is the homepage hero open next weekend? want to run something for VIPs

1. 모델 → **`a2api_load`** `` {"names":["list_display_slots","get_display_slot","list_banners","schedule_display"]} ``
   ← 결과 86B: `` {"loaded":["list_display_slots","get_display_slot","list_banners","schedule_display"]} ``
2. 모델 → **`list_display_slots`** `` {"page":"main","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","audience":"vip","slot_type":"hero"} ``
   ← 결과 646B: `` {"status":"succeeded","data":{"items":[{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"]}],"availability":[{"audience":"vip","free_from":"2026-11-07T00:00:00-05:00","free_until":"2026-11-08T23:59:00-05:00"}]}],"total":1},"next":"Functions that take IDs from this result: invalidate_display_cache (slot_id); get_c… (+46자) ``
3. 모델 → **`list_display_slots`** `` {"page":"main","valid_from":"2026-11-14T00:00","valid_through":"2026-11-15T23:59","audience":"vip","slot_type":"hero"} ``
   ← 결과 646B: `` {"status":"succeeded","data":{"items":[{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"]}],"availability":[{"audience":"vip","free_from":"2026-11-14T00:00:00-05:00","free_until":"2026-11-15T23:59:00-05:00"}]}],"total":1},"next":"Functions that take IDs from this result: invalidate_display_cache (slot_id); get_c… (+46자) ``

**답변 1**
> Yes — the homepage hero is free for VIPs next weekend.
>
> * Slot: **slot_home_hero** – Home hero, page `main`, slot_type `hero`
> * Audience: `vip`
>
> Availability for VIP:
> * **2026-11-14 00:00 – 2026-11-15 23:59 America/New_York** → free_from `2026-11-14T00:00:00-05:00` to `free_until 2026-11-15T23:59:00-05:00`
>
> Current booking on the slot:
> * `dsp_fall_layers` “Fall layers” for `everyone`, valid_from `2026-11-06T10:00:00-05:00`, valid_through `null`, status `active`, change_set `cs_1039`. That booking does not block VIP, so VIP inventory is open.
>
> The slot is also free for VIP this weekend 2026-11-07 to 2026-11-08.
>
> If you want to book it, the items need to be arranged on `slot_home_hero` first with `arrange_display_slot`, then `schedule_display` for audience `vip` for 2026-11-14 → 2026-11-15. That change will need approval.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names · 2회차 · ✓ 통과

토큰 14,614 · 36.664초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 1,630토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> is the homepage hero open next weekend? want to run something for VIPs

1. 모델 → **`a2api_load`** `` {"names":["list_display_slots","get_display_slot","list_banners","schedule_display"]} ``
   ← 결과 86B: `` {"loaded":["list_display_slots","get_display_slot","list_banners","schedule_display"]} ``
2. 모델 → **`list_display_slots`** `` {"page":"main","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","audience":"vip","slot_type":"hero"} ``
   ← 결과 646B: `` {"status":"succeeded","data":{"items":[{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"]}],"availability":[{"audience":"vip","free_from":"2026-11-07T00:00:00-05:00","free_until":"2026-11-08T23:59:00-05:00"}]}],"total":1},"next":"Functions that take IDs from this result: invalidate_display_cache (slot_id); get_c… (+46자) ``
3. 모델 → **`list_display_slots`** `` {"page":"main","valid_from":"2026-11-14T00:00","valid_through":"2026-11-15T23:59","audience":"vip","slot_type":"hero"} ``
   ← 결과 646B: `` {"status":"succeeded","data":{"items":[{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"]}],"availability":[{"audience":"vip","free_from":"2026-11-14T00:00:00-05:00","free_until":"2026-11-15T23:59:00-05:00"}]}],"total":1},"next":"Functions that take IDs from this result: invalidate_display_cache (slot_id); get_c… (+46자) ``

**답변 1**
> Yes — the homepage hero is free for VIPs next weekend.
>
> * Slot: **slot_home_hero** – Home hero, page `main`, slot_type `hero`
> * Audience: `vip`
>
> Availability for VIP:
> * **2026-11-14 00:00 – 2026-11-15 23:59 America/New_York** → free_from `2026-11-14T00:00:00-05:00` to `free_until 2026-11-15T23:59:00-05:00`
>
> Current booking on the slot:
> * `dsp_fall_layers` “Fall layers” for `everyone`, valid_from `2026-11-06T10:00:00-05:00`, valid_through `null`, status `active`, change_set `cs_1039`. That booking does not block VIP, so VIP inventory is open.
>
> The slot is also free for VIP this weekend 2026-11-07 to 2026-11-08.
>
> If you want to book it, the items need to be arranged on `slot_home_hero` first with `arrange_display_slot`, then `schedule_display` for audience `vip` for 2026-11-14 → 2026-11-15. That change will need approval.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)
