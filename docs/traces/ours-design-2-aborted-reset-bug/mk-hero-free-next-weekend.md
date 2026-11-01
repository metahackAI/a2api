# mk-hero-free-next-weekend — ours-design-2-aborted-reset-bug

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `8c25f4a`

**과업**

> is the homepage hero open next weekend? want to run something for VIPs

- 필요한 도구: `list_display_slots`
- 허용 도구: `get_display_slot`, `list_banners`
- 답에 있어야 할 사실: next weekend is Sat Nov 14 – Sun Nov 15
- 답에 있어야 할 사실: the home hero shows Fall layers to everyone with no end date, and is free for VIP, Gold and Member audiences all of Nov 14–15
- 부르면 안 됨: schedule_banner

### a2api-acom · 1회차 · ✓ 통과

토큰 19,356 · 34.986초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 3,959토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> is the homepage hero open next weekend? want to run something for VIPs

1. 모델 → **`acom_list_tiers`** `` {} ``
   ← 결과 305B: `` {"status":"succeeded","data":{"items":[{"id":"vip","name":"VIP","rank":3,"program_id":"prg_rewards","member_count":1284},{"id":"gold","name":"Gold","rank":2,"program_id":"prg_rewards","member_count":2900},{"id":"member","name":"Member","rank":1,"program_id":"prg_rewards","member_count":9816}],"total":3}} ``
2. 모델 → **`acom_list_display_slots`** `` {"page":"main","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","audience":"vip","slot_type":"hero"} ``
   ← 결과 736B: `` {"status":"succeeded","data":{"items":[{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"]},{"display_booking_id":"dsp_01m6984zzpmwz07mfv3qxdq13m","audience":"vip","headline":"20% Off Summer Outerwear","valid_from":"2026-11-07T00:00:00-05:00","valid_through":"2026-11-08T23:59:59-05:00","status":"scheduled","promo… (+136자) ``
3. 모델 → **`acom_list_display_slots`** `` {"page":"main","valid_from":"2026-11-14T00:00","valid_through":"2026-11-15T23:59","audience":"vip","slot_type":"hero"} ``
   ← 결과 509B: `` {"status":"succeeded","data":{"items":[{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"]}],"availability":[{"audience":"vip","free_from":"2026-11-14T00:00:00-05:00","free_until":"2026-11-15T23:59:00-05:00"}]}],"total":1}} ``

**답변 1**
> Yes — the Home hero is free for VIPs next weekend.
>
> * **Sat–Sun 14–15 Nov 2026**
>   * `slot_home_hero` on the main page
>   * VIP audience availability: `2026-11-14T00:00:00-05:00` → `2026-11-15T23:59:00-05:00`
>   * The “everyone” booking *Fall layers* `dsp_fall_layers` is active through, but there is no VIP-specific booking in that window, so the VIP layer is open.
>
> For reference, this coming weekend is already taken for VIPs:
> * **Sat–Sun 7–8 Nov 2026**
>   * VIP booking `dsp_01m6984zzpmwz07mfv3qxdq13m` – “20% Off Summer Outerwear”
>   * `valid_from 2026-11-07T00:00:00-05:00` to `valid_through 2026-11-08T23:59:59-05:00`, status scheduled
>
> Tier used: `vip` – VIP, rank 3, 1,284 members in `prg_rewards`.
>
> Want me to check other hero slots or hold the 14–15 Nov VIP window for you?

**채점**: ✓ 통과
(도구 정밀도 0.67, 재현율 1.00)
