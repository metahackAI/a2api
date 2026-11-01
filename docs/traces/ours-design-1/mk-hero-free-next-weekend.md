# mk-hero-free-next-weekend — ours-design-1

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `a2c7201`

**과업**

> is the homepage hero open next weekend? want to run something for VIPs

- 필요한 도구: `list_display_slots`
- 허용 도구: `get_display_slot`, `list_banners`
- 답에 있어야 할 사실: next weekend is Sat Nov 14 – Sun Nov 15
- 답에 있어야 할 사실: the home hero shows Fall layers to everyone with no end date, and is free for VIP, Gold and Member audiences all of Nov 14–15
- 부르면 안 됨: schedule_banner

### facade-all · 1회차 · E MODEL_CALL_LIMIT

토큰 72,339 · 89.071초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 4,652토큰

준비: 전략 `None`, 함수 19개

**질문 1**
> is the homepage hero open next weekend? want to run something for VIPs

1. 모델 → **`getDispCornerList`** `` {"dispPageCd":"01","strtDtm":20261107000000,"endDtm":20261108235959,"cornerTpCd":"H"} ``
   ← 결과 164B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid parameter: invalid type: number, expected a string","next_tool":null}}} ``
2. 모델 → **`getDispCornerList`** `` {"dispPageCd":"01","strtDtm":"2026-11-07 00:00:00","endDtm":"2026-11-08 23:59:59","cornerTpCd":"H"} ``
   ← 결과 190B: `` {"status":422,"body":{"error":{"code":"invalid_input","class":"invalid_input","message":"'2026-11-07 00:00:00' is not a date-time (expected 2026-11-07T00:00 or RFC 3339)","next_tool":null}}} ``
3. 모델 → **`getDispCornerList`** `` {"dispPageCd":"01","strtDtm":"2026-11-07T00:00:00","endDtm":"2026-11-08T23:59:59","cornerTpCd":"H"} ``
   ← 결과 257B: `` {"status":200,"body":{"list":[{"cornerNo":"slot_home_hero","cornerNm":"Home hero","cornerTpCd":"H","bnrList":[{"dispNo":"dsp_fall_layers","tgtMbrGrdCd":"G00","bnrTitl":"Fall layers","strtDtm":"2026-11-06T10:00:00-05:00","endDtm":null,"dispStatCd":"20"}]}]}} ``
4. 모델 → **`getMbrGrdList`** `` {"prgmNo":""} ``
   ← 결과 131B: `` {"status":404,"body":{"error":{"code":"program_not_found","class":"not_found","message":"There is no program .","next_tool":null}}} ``
5. 모델 → **`getMbrGrdList`** `` {"prgmNo":1} ``
   ← 결과 164B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid parameter: invalid type: number, expected a string","next_tool":null}}} ``
6. 모델 → **`getMbrGrdList`** `` {"prgmNo":"P01"} ``
   ← 결과 134B: `` {"status":404,"body":{"error":{"code":"program_not_found","class":"not_found","message":"There is no program P01.","next_tool":null}}} ``
7. 모델 → **`getPrmtTgtMbrList`** `` {"mbrGrdCd":"VIP","pageNo":0,"pageSize":1} ``
   ← 결과 121B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null}}} ``
8. 모델 → **`getPrmtTgtMbrList`** `` {"mbrGrdCd":"VIP","pageNo":0,"pageSize":10} ``
   ← 결과 121B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null}}} ``
9. 모델 → **`getPrmtTgtMbrList`** `` {"mbrGrdCd":"VIP","pageNo":1,"pageSize":10} ``
   ← 결과 132B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid member grade code.","next_tool":null}}} ``
10. 모델 → **`getPrmtGridList`** `` {"pageNo":0,"pageSize":10} ``
   ← 결과 121B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null}}} ``
11. 모델 → **`getPrmtGridList`** `` {"pageNo":1,"pageSize":10} ``
   ← 결과 1,121B: `` {"status":200,"body":{"list":[{"prmtNo":"promo_denim_bundle","prmtNm":"Denim bundle","prmtTpCd":"T02","prmtStatCd":"10","tgtMbrGrdCd":"G00","strtDtm":"2026-11-13T00:00:00-05:00","endDtm":"2026-11-20T23:59:00-05:00"},{"prmtNo":"promo_autumn_knit","prmtNm":"Autumn knitwear 15%","prmtTpCd":"T01","prmtStatCd":"20","tgtMbrGrdCd":"G00","strtDtm":"2026-11-01T00:00:00-04:00","endDtm":"2026-11-15T23:59:00-05:00"},{"prmtNo":"promo_linen_clearance","prmtNm":"Linen clearance","prmtTpCd":"T01","prmtStatCd":"90","tgtMbrGrdCd":"G00","strtDtm":"2026-10-01T00:00:00-04:00","endDtm":"2026-10-20T23:59:00-04:00"},… (+521자) ``
12. 모델 → **`getPrmtTgtMbrListCnt`** `` {"mbrGrdCd":"G02","pageNo":1,"pageSize":1} ``
   ← 결과 37B: `` {"status":200,"body":{"totCnt":2900}} ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "next weekend is Sat Nov 14 – Sun Nov 15" (14, 15 not shown); fact "the home hero shows Fall layers to everyone with no end date" (14, 15 not shown); HOST:MODEL_CALL_LIMIT

### acom-all · 1회차 · E CONTEXT_OVERFLOW

토큰 0 · 0.289초 · 모델 호출 0회 · 도구 호출 0회

준비: 전략 `None`, 함수 253개

**질문 1**
> is the homepage hero open next weekend? want to run something for VIPs


_(CONTEXT_OVERFLOW로 중단)_

**채점**: E CONTEXT_OVERFLOW — 빠진 것: tool list_display_slots; fact "next weekend is Sat Nov 14 – Sun Nov 15" (14, 15 not shown); fact "the home hero shows Fall layers to everyone with no end date" (14, 15 not shown); HOST:CONTEXT_OVERFLOW
(도구 정밀도 —, 재현율 0.00)

### a2api-acom · 1회차 · ✓ 통과

토큰 19,389 · 38.234초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 3,959토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> is the homepage hero open next weekend? want to run something for VIPs

1. 모델 → **`acom_list_tiers`** `` {} ``
   ← 결과 305B: `` {"status":"succeeded","data":{"items":[{"id":"vip","name":"VIP","rank":3,"program_id":"prg_rewards","member_count":1284},{"id":"gold","name":"Gold","rank":2,"program_id":"prg_rewards","member_count":2900},{"id":"member","name":"Member","rank":1,"program_id":"prg_rewards","member_count":9816}],"total":3}} ``
2. 모델 → **`acom_list_display_slots`** `` {"page":"main","valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","audience":"vip","slot_type":"hero"} ``
   ← 결과 509B: `` {"status":"succeeded","data":{"items":[{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"]}],"availability":[{"audience":"vip","free_from":"2026-11-07T00:00:00-05:00","free_until":"2026-11-08T23:59:00-05:00"}]}],"total":1}} ``
3. 모델 → **`acom_list_display_slots`** `` {"page":"main","valid_from":"2026-11-14T00:00","valid_through":"2026-11-15T23:59","audience":"vip","slot_type":"hero"} ``
   ← 결과 509B: `` {"status":"succeeded","data":{"items":[{"id":"slot_home_hero","page":"main","name":"Home hero","slot_type":"hero","bookings":[{"display_booking_id":"dsp_fall_layers","audience":"everyone","headline":"Fall layers","valid_from":"2026-11-06T10:00:00-05:00","valid_through":null,"status":"active","promotion_id":null,"change_set_id":"cs_1039","channels":["web","mobile_web","app"]}],"availability":[{"audience":"vip","free_from":"2026-11-14T00:00:00-05:00","free_until":"2026-11-15T23:59:00-05:00"}]}],"total":1}} ``

**답변 1**
> Yes — the Home hero is free for VIPs next weekend.
>
> * Slot: `slot_home_hero` – Home hero, page `main`, slot_type `hero`
> * VIP availability
>   * 2026-11-14 00:00 – 2026-11-15 23:59 America/New_York: free_from 2026-11-14T00:00:00-05:00 → free_until 2026-11-15T23:59:00-05:00
>   * This coming weekend is also free for VIPs: 2026-11-07 00:00 – 2026-11-08 23:59 free for VIP
>
> Current booking on the slot:
> * `dsp_fall_layers` – “Fall layers”, audience `everyone`, valid_from 2026-11-06T10:00:00-05:00, valid_through null, status active, change_set_id `cs_1039`
>
> So the hero is occupied for everyone but the VIP audience window is unbooked for both 7-8 Nov and 14-15 Nov, so you can run a VIP-only promotion there next weekend.

**채점**: ✓ 통과
(도구 정밀도 0.67, 재현율 1.00)

### a2api-facade · 1회차 · ✓ 통과

토큰 20,092 · 46.003초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 2,465토큰

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

**답변 1**
> The Home hero is not free next weekend.
>
> * **Corner:** `slot_home_hero` – Home hero, hero
> * **Current booking:** `dsp_fall_layers`
>   * Headline: Fall layers
>   * Target member grade: G00 – every shopper
>   * Starts at: 2026-11-06T10:00:00-05:00
>   * Ends at: null
>   * Display status: active
>
> That booking is active with no end date, so it is still scheduled for the periods you asked about:
>
> * 2026-11-07 to 2026-11-08
> * 2026-11-14 to 2026-11-15
>
> The slot is therefore occupied by an all-shopper banner for the coming weekend and the following weekend.
>
> VIP tier in the system is:
> * G03 – VIP, member_count 1,284, rank 3
>
> You can schedule a VIP-targeted banner for the same corner – target_member_grade G03 – to run alongside the existing G00 booking. The existing Fall layers banner will continue to show to non-VIP shoppers unless it is ended/paused.

**채점**: ✓ 통과
