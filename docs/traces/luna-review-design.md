# 호출 단계 리뷰 — luna-design-raw, luna-design-a2api, luna-design-acom

a-commerce 자체 에이전트. "모델에게 줌"은 에이전트의 도구 검색이 계획기에 준 후보다. 판정 기준 함수 정의: 원본 화면 / a2api 변환 화면(`--converted`) / A-Commerce 도구.

단계: A0 API에 해당 기능 없음 · A 필요한 함수를 받지 못함 · B 받았지만 부르지 않음 · C 불렀지만 성공 못 함 · D-before 필요한 함수를 부르기 전 한도·오류로 중단 · D-after 필요한 함수는 모두 성공했는데 답하기 전 한도로 중단 · E-write 쓰기 입력·change set · E-format 숫자는 있으나 표기 · E-content 답 내용 누락

## 필요한 함수: 확보 → 호출 → 성공

| 방식 | 통과 | 필요한 함수(API에 있음/전체) | 모델에게 줌 | 불렀음 | 성공 | 확보 기록 |
|---|---|---|---|---|---|---|
| own-facade-raw | 2/36 | 42/63 | 30/42 (71%) | 19/42 (45%) | 11/42 (26%) | 단계별 기록 |
| own-facade-a2api-lookup | 6/36 | 42/63 | 39/42 (93%) | 25/42 (60%) | 25/42 (60%) | 단계별 기록 |
| own-acom | 7/36 | 63/63 | 54/63 (86%) | 44/63 (70%) | 44/63 (70%) | 단계별 기록 |

## 실패한 실행이 처음 막힌 단계

| 방식 | passed | A0 | A | B | C | D-before | D-after | E-write | E-format | E-content |
|---|---|---|---|---|---|---|---|---|---|---|
| own-facade-raw | 2 | 21 | 8 | 0 | 2 | 0 | 0 | 0 | 0 | 3 |
| own-facade-a2api-lookup | 6 | 21 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 4 |
| own-acom | 7 | 0 | 6 | 5 | 0 | 0 | 0 | 0 | 0 | 18 |

## 실패한 업무 호출의 원인

| 방식 | 업무 호출 | 실패 | model:schema | model:function | model:ungrounded | model:described | source:undocumented | business | unclear |
|---|---|---|---|---|---|---|---|---|---|
| own-facade-raw | 105 | 67 | 0 | 0 | 3 | 0 | 57 | 0 | 7 |
| own-facade-a2api-lookup | 101 | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| own-acom | 275 | 6 | 0 | 0 | 0 | 3 | 0 | 0 | 3 |

## 쓰기 입력(과업이 기대한 change set 항목)

| 방식 | 기대 항목 | 불렀음 | 입력 일치 |
|---|---|---|---|
| own-acom | 18 | 2 | 2 |

## 실패한 호출 목록

- `source:undocumented` b1-vip-weekend-sale [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "aplyDtm": "2026-11-07 00:00:00", "srchKwd": "summer outerwear", "pageSize": 100, "aplyMbrGrdCd": "vip"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `unclear` b1-vip-weekend-sale [own-facade-raw] 1회차 · `getPrmtTgtMbrList` `{"pageNo": 1, "mbrGrdCd": "VIP", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid member grade code.
- `source:undocumented` b1-vip-weekend-sale [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "summer outerwear", "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:ungrounded` b1-vip-weekend-sale [own-facade-raw] 2회차 · `getPrdGridList` `{"ctgNo": "summer_outerwear", "pageNo": 1, "pageSize": 20}` → RESOURCE_NOT_FOUND: There is no category summer_outerwear.
- `source:undocumented` b1-vip-weekend-sale [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "summer outerwear", "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b1-vip-weekend-sale [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "summer outerwear", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b1-vip-weekend-sale [own-facade-raw] 3회차 · `getPrdGridList` `{"ctgNo": "summer_outerwear", "pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b1-vip-weekend-sale [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "summer outerwear", "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b1-vip-weekend-sale [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "summer outerwear", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b1-vip-weekend-sale [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 1회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 100, "clmAmtFrom": 200}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 1회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 12, "clmAmtFrom": 200}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 1회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 12, "clmAmtFrom": 200}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 1회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 1회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 1회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `unclear` b2-returns-over-200 [own-facade-raw] 1회차 · `saveCustMsgSend` `{"mbrNo": "cus_grace", "msgCntt": "We’re sorry, but we’re unable to approve your return request. Thank you for understanding.", "msgTpCd": "M03"}` → UPSTREAM_VALIDATION_FAILED: Say which order the message is about.
- `model:ungrounded` b2-returns-over-200 [own-facade-raw] 1회차 · `saveCustMsgSend` `{"mbrNo": "cus_dana", "ordNo": "ord_20290", "msgCntt": "We’re sorry, but we’re unable to approve the return for your cashmere sweater. We understand this may be disappointing, and appreciate your unde` → RESOURCE_NOT_FOUND: No refund has gone out for this order, so the notice is not sent.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 2회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 100, "clmAmtFrom": 200}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `unclear` b2-returns-over-200 [own-facade-raw] 2회차 · `saveCustMsgSend` `{"mbrNo": "cus_4431", "msgCntt": "We’re sorry, but we’re unable to approve your return request. Thank you for understanding.", "msgTpCd": "M03"}` → UPSTREAM_VALIDATION_FAILED: Say which order the message is about.
- `model:ungrounded` b2-returns-over-200 [own-facade-raw] 2회차 · `saveCustMsgSend` `{"mbrNo": "cus_dana", "ordNo": "ord_20290", "msgCntt": "Thank you for reaching out about your cashmere sweater return. We’re sorry, but we’re unable to approve the return. We appreciate your understan` → RESOURCE_NOT_FOUND: No refund has gone out for this order, so the notice is not sent.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 3회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 100, "clmAmtFrom": 200}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 3회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 100, "clmAmtFrom": 200}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 3회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 100, "clmAmtFrom": 200}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 3회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 100, "clmAmtFrom": 200}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 3회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 3회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 3회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 50, "clmAmtFrom": 200}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `unclear` b3-why-sales-dropped [own-facade-raw] 2회차 · `getSaleAnlsGridList` `{"srchEndDt": "2026-11-05", "cmprBaseCd": "1", "srchStrtDt": "2026-10-23"}` → UPSTREAM_VALIDATION_FAILED: same_weekday_last_4_weeks compares periods of 7 days at most; this one has 14. Use previous_period or custom.
- `unclear` b3-why-sales-dropped [own-facade-raw] 2회차 · `getSaleAnlsGridList` `{"srchEndDt": "2026-11-05", "cmprBaseCd": "1", "srchStrtDt": "2026-10-23"}` → UPSTREAM_VALIDATION_FAILED: same_weekday_last_4_weeks compares periods of 7 days at most; this one has 14. Use previous_period or custom.
- `unclear` b3-why-sales-dropped [own-facade-raw] 3회차 · `getSaleAnlsGridList` `{"srchEndDt": "2026-11-05", "cmprBaseCd": "1", "srchStrtDt": "2026-10-23"}` → UPSTREAM_VALIDATION_FAILED: same_weekday_last_4_weeks compares periods of 7 days at most; this one has 14. Use previous_period or custom.
- `source:undocumented` md-end-of-season-markdown [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "prmtNm": "End of season", "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-end-of-season-markdown [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "prmtNm": "End of season markdown", "pageSize": 50}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-end-of-season-markdown [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-end-of-season-markdown [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-end-of-season-markdown [own-facade-raw] 3회차 · `getPrmtGridList` `{"pageNo": 0, "prmtNm": "End of season markdown", "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-low-stock-before-weekend [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-low-stock-before-weekend [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-low-stock-before-weekend [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-low-stock-before-weekend [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-low-stock-before-weekend [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-low-stock-before-weekend [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-low-stock-before-weekend [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 50}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-overcoat-runs-small [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "wool overcoat", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-overcoat-runs-small [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "wool overcoat", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mgr-what-changed-this-morning [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 100, "srchEndDtm": "2026-11-06 11:00", "srchStrtDtm": "2026-11-06 00:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mgr-what-changed-this-morning [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 10, "srchEndDtm": "2026-11-06 11:00:00", "srchStrtDtm": "2026-11-06 00:00:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mgr-what-changed-this-morning [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 20, "srchEndDtm": "2026-11-06 11:00", "srchStrtDtm": "2026-11-06 00:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mgr-what-needs-me-today [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 100, "srchEndDtm": "2026-11-06 23:59", "srchStrtDtm": "2026-11-06 00:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mgr-what-needs-me-today [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mgr-what-needs-me-today [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-hero-free-next-weekend [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 100, "srchEndDtm": "2026-11-15 23:59", "srchStrtDtm": "2026-11-14 00:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-hero-free-next-weekend [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 20, "srchEndDtm": "2026-11-08 23:59:00", "srchStrtDtm": "2026-11-07 00:00:00", "tgtMbrGrdCd": "G03"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-hero-free-next-weekend [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 50}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `unclear` mk-hero-free-next-weekend [own-facade-raw] 3회차 · `getPrmtGridList` `{"srchEndDtm": "2026-11-15 23:59:00", "srchStrtDtm": "2026-11-13 00:00:00", "tgtMbrGrdCd": "VIP"}` → UPSTREAM_VALIDATION_FAILED: Invalid member grade code.
- `source:undocumented` mk-whats-running-this-weekend [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 100, "srchEndDtm": "2026-11-08 23:59:00", "srchStrtDtm": "2026-11-07 00:00:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-whats-running-this-weekend [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 100, "srchEndDtm": "2026-11-08 23:59:00", "srchStrtDtm": "2026-11-06 00:00:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-whats-running-this-weekend [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 50, "srchEndDtm": "2026-11-08 23:59", "srchStrtDtm": "2026-11-07 00:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-whats-running-this-weekend [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 100, "srchEndDtm": "2026-11-08 23:59", "srchStrtDtm": "2026-11-07 00:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-whats-running-this-weekend [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 20, "srchEndDtm": "2026-11-08 23:59", "srchStrtDtm": "2026-11-06 00:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-whats-running-this-weekend [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 20, "srchEndDtm": "2026-11-08 23:59", "srchStrtDtm": "2026-11-07 00:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-whats-running-this-weekend [own-facade-raw] 3회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 100, "srchEndDtm": "2026-11-08 23:59", "srchStrtDtm": "2026-11-07 00:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-frequent-returner [own-facade-raw] 2회차 · `getOrdGridList` `{"pageNo": 0, "srchKwd": "20431", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-frequent-returner [own-facade-raw] 2회차 · `getOrdGridList` `{"pageNo": 0, "srchKwd": "20431", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-wismo-tracking-stuck [own-facade-raw] 1회차 · `getOrdDtlPopInitData` `{"ordNo": "27184"}` → RESOURCE_NOT_FOUND: There is no order 27184.
- `source:undocumented` ops-wismo-tracking-stuck [own-facade-raw] 2회차 · `getOrdDtlPopInitData` `{"ordNo": "27184"}` → RESOURCE_NOT_FOUND: There is no order 27184.
- `source:undocumented` ops-wismo-tracking-stuck [own-facade-raw] 3회차 · `getOrdDtlPopInitData` `{"ordNo": "27184"}` → RESOURCE_NOT_FOUND: There is no order 27184.
- `source:undocumented` md-end-of-season-markdown [own-facade-a2api-lookup] 1회차 · `save_promotion_list` `{"rows": [{"ends_at": "2026-11-15T23:59:00-05:00", "starts_at": "2026-11-06T11:00:00-05:00", "applies_to": "category", "row_action": "insert", "category_id": "", "percent_off": 25, "promotion_name": "` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Row 1: `category_id` must look like `cat_…`; got ``.
- `unclear` mk-hero-free-next-weekend [own-facade-a2api-lookup] 2회차 · `get_promotion_grid_list` `{"active_from": "2026-11-07T00:00:00-05:00", "active_until": "2026-11-08T23:59:00-05:00", "target_member_grade": "VIP"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Invalid member grade code.
- `unclear` b2-returns-over-200 [own-acom] 1회차 · `reject_claim` `{"reason": "outside_return_window"}` → UNKNOWN: The arguments for reject_claim are not usable: missing claim_id.
- `unclear` b2-returns-over-200 [own-acom] 1회차 · `reject_claim` `{"reason": "outside_return_window"}` → UNKNOWN: The arguments for reject_claim are not usable: missing claim_id.
- `unclear` b2-returns-over-200 [own-acom] 1회차 · `reject_claim` `{"reason": "outside_return_window"}` → UNKNOWN: The arguments for reject_claim are not usable: missing claim_id.
- `model:described` ops-wismo-tracking-stuck [own-acom] 1회차 · `track_shipment` `{"mode": "delivery"}` → UPSTREAM_VALIDATION_FAILED: mode delivery needs delivery_id.
- `model:described` ops-wismo-tracking-stuck [own-acom] 2회차 · `track_shipment` `{"mode": "delivery"}` → UPSTREAM_VALIDATION_FAILED: mode delivery needs delivery_id.
- `model:described` ops-wismo-tracking-stuck [own-acom] 3회차 · `track_shipment` `{"mode": "delivery"}` → UPSTREAM_VALIDATION_FAILED: mode delivery needs delivery_id.

## 기대와 다른 쓰기 입력

- b1-vip-weekend-sale [own-acom] 1회차 · `set_sale_prices` 기대 {"valid_for_member_tier": "vip", "percent_off": 20} · 부르지 않음
- b1-vip-weekend-sale [own-acom] 1회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [own-acom] 1회차 · `schedule_banner` 기대 {"slot_id": "slot_home_hero"} · 부르지 않음
- b1-vip-weekend-sale [own-acom] 2회차 · `set_sale_prices` 기대 {"valid_for_member_tier": "vip", "percent_off": 20} · 부르지 않음
- b1-vip-weekend-sale [own-acom] 2회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [own-acom] 2회차 · `schedule_banner` 기대 {"slot_id": "slot_home_hero"} · 부르지 않음
- b1-vip-weekend-sale [own-acom] 3회차 · `set_sale_prices` 기대 {"valid_for_member_tier": "vip", "percent_off": 20} · 부르지 않음
- b1-vip-weekend-sale [own-acom] 3회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [own-acom] 3회차 · `schedule_banner` 기대 {"slot_id": "slot_home_hero"} · 부르지 않음
- b2-returns-over-200 [own-acom] 1회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [own-acom] 1회차 · `send_customer_message` 기대 {} · 부르지 않음
- b2-returns-over-200 [own-acom] 2회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [own-acom] 3회차 · `refund_return` 기대 {} · 부르지 않음
- md-end-of-season-markdown [own-acom] 1회차 · `set_sale_prices` 기대 {"valid_for_member_tier": "everyone", "scope_mode": "category", "category_id": "cat_tees", "exclude_low_stock": true} · 부르지 않음
- md-end-of-season-markdown [own-acom] 2회차 · `set_sale_prices` 기대 {"valid_for_member_tier": "everyone", "scope_mode": "category", "category_id": "cat_tees", "exclude_low_stock": true} · 부르지 않음
- md-end-of-season-markdown [own-acom] 3회차 · `set_sale_prices` 기대 {"valid_for_member_tier": "everyone", "scope_mode": "category", "category_id": "cat_tees", "exclude_low_stock": true} · 부르지 않음
