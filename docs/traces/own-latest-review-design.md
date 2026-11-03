# 호출 단계 리뷰 — own-latest-design-raw, own-latest-design-a2api, own-latest-design-a2api-lookup, own-latest-design-acom

a-commerce 자체 에이전트. "모델에게 줌"은 에이전트의 도구 검색이 계획기에 준 후보다. 판정 기준 함수 정의: 원본 화면 / a2api 변환 화면(`--converted`) / A-Commerce 도구.

단계: A0 API에 해당 기능 없음 · A 필요한 함수를 받지 못함 · B 받았지만 부르지 않음 · C 불렀지만 성공 못 함 · D-before 필요한 함수를 부르기 전 한도·오류로 중단 · D-after 필요한 함수는 모두 성공했는데 답하기 전 한도로 중단 · E-write 쓰기 입력·change set · E-format 숫자는 있으나 표기 · E-content 답 내용 누락

## 필요한 함수: 확보 → 호출 → 성공

| 방식 | 통과 | 필요한 함수(API에 있음/전체) | 모델에게 줌 | 불렀음 | 성공 | 확보 기록 |
|---|---|---|---|---|---|---|
| own-facade-raw | 0/36 | 42/63 | 30/42 (71%) | 15/42 (36%) | 9/42 (21%) | 단계별 기록 |
| own-facade-a2api | 3/36 | 42/63 | 39/42 (93%) | 25/42 (60%) | 19/42 (45%) | 단계별 기록 |
| own-facade-a2api-lookup | 3/36 | 42/63 | 39/42 (93%) | 26/42 (62%) | 22/42 (52%) | 단계별 기록 |
| own-acom | 15/36 | 63/63 | 55/63 (87%) | 46/63 (73%) | 44/63 (70%) | 단계별 기록 |

## 실패한 실행이 처음 막힌 단계

| 방식 | passed | A0 | A | B | C | D-before | D-after | E-write | E-format | E-content |
|---|---|---|---|---|---|---|---|---|---|---|
| own-facade-raw | 0 | 21 | 9 | 0 | 1 | 0 | 0 | 0 | 0 | 5 |
| own-facade-a2api | 3 | 21 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 6 |
| own-facade-a2api-lookup | 3 | 21 | 3 | 2 | 2 | 0 | 0 | 0 | 0 | 5 |
| own-acom | 15 | 0 | 6 | 3 | 0 | 0 | 0 | 0 | 2 | 10 |

## 실패한 업무 호출의 원인

| 방식 | 업무 호출 | 실패 | model:schema | model:function | model:ungrounded | model:described | source:undocumented | business | unclear |
|---|---|---|---|---|---|---|---|---|---|
| own-facade-raw | 85 | 72 | 0 | 0 | 0 | 0 | 69 | 0 | 3 |
| own-facade-a2api | 77 | 15 | 0 | 0 | 3 | 7 | 0 | 0 | 5 |
| own-facade-a2api-lookup | 76 | 6 | 0 | 0 | 3 | 2 | 0 | 0 | 1 |
| own-acom | 290 | 10 | 0 | 0 | 2 | 4 | 1 | 0 | 3 |

## 쓰기 입력(과업이 기대한 change set 항목)

| 방식 | 기대 항목 | 불렀음 | 입력 일치 |
|---|---|---|---|
| own-acom | 18 | 2 | 2 |

## 실패한 호출 목록

- `source:undocumented` b1-vip-weekend-sale [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "summer outerwear", "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b1-vip-weekend-sale [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "summer outerwear", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b1-vip-weekend-sale [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "summer outerwear", "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b1-vip-weekend-sale [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "summer outerwear", "pageSize": 50}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b1-vip-weekend-sale [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "summer outerwear", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b1-vip-weekend-sale [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "summer outerwear", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b1-vip-weekend-sale [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "summer outerwear", "pageSize": 50}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 1회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 50, "clmAmtFrom": 200.0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 1회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 100, "clmAmtFrom": 200.0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 1회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 20, "clmAmtFrom": 200.0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 1회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 1회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 20, "clmAmtFrom": 200}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 1회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 20, "clmAmtFrom": 200}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 1회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 20, "clmAmtFrom": 200}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 2회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 20, "clmAmtFrom": 200}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 2회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 20, "clmAmtFrom": 200}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 2회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 20, "clmAmtFrom": 200}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 2회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 20, "clmAmtFrom": 200}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 3회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 50, "clmAmtFrom": 200.0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 3회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 100, "clmAmtFrom": 200.0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 3회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 100, "clmAmtFrom": 200.0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 3회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 20, "clmAmtFrom": 200}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [own-facade-raw] 3회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 20, "clmStatCd": "R10", "clmAmtFrom": 200.0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `unclear` b3-why-sales-dropped [own-facade-raw] 1회차 · `getSaleAnlsGridList` `{"srchEndDt": "2026-11-05", "cmprBaseCd": "1", "srchStrtDt": "2026-10-23"}` → UPSTREAM_VALIDATION_FAILED: same_weekday_last_4_weeks compares periods of 7 days at most; this one has 14. Use previous_period or custom.
- `unclear` b3-why-sales-dropped [own-facade-raw] 2회차 · `getSaleAnlsGridList` `{"srchEndDt": "2026-11-05", "cmprBaseCd": "1", "srchStrtDt": "2026-10-23"}` → UPSTREAM_VALIDATION_FAILED: same_weekday_last_4_weeks compares periods of 7 days at most; this one has 14. Use previous_period or custom.
- `unclear` b3-why-sales-dropped [own-facade-raw] 3회차 · `getSaleAnlsGridList` `{"srchEndDt": "2026-11-05", "cmprBaseCd": "1", "srchStrtDt": "2026-10-23"}` → UPSTREAM_VALIDATION_FAILED: same_weekday_last_4_weeks compares periods of 7 days at most; this one has 14. Use previous_period or custom.
- `source:undocumented` md-end-of-season-markdown [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 1, "prmtStatCd": "00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-end-of-season-markdown [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 1, "prmtStatCd": "00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-end-of-season-markdown [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-end-of-season-markdown [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-end-of-season-markdown [own-facade-raw] 3회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 1, "prmtStatCd": "00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-low-stock-before-weekend [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 20, "stkQtyTo": 5, "stkQtyFrom": 0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-low-stock-before-weekend [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-low-stock-before-weekend [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-low-stock-before-weekend [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 20, "stkQtyTo": 5, "stkQtyFrom": 0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-low-stock-before-weekend [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 20, "stkQtyTo": 5, "stkQtyFrom": 0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-low-stock-before-weekend [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-low-stock-before-weekend [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-overcoat-runs-small [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "wool overcoat", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-overcoat-runs-small [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "wool overcoat", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-overcoat-runs-small [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "wool overcoat", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mgr-what-changed-this-morning [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 100, "prmtStatCd": "00", "srchEndDtm": "2026-11-06 11:00", "srchStrtDtm": "2026-11-06 00:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mgr-what-changed-this-morning [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 100, "srchEndDtm": "2026-11-06 11:00", "srchStrtDtm": "2026-11-06 00:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mgr-what-changed-this-morning [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 100, "prmtStatCd": "00", "srchEndDtm": "2026-11-06 11:00:00", "srchStrtDtm": "2026-11-06 00:00:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mgr-what-changed-this-morning [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 0, "srchEndDtm": "2026-11-06 11:00", "srchStrtDtm": "2026-11-06 00:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mgr-what-changed-this-morning [own-facade-raw] 3회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 100, "prmtStatCd": "00", "srchEndDtm": "2026-11-06 11:00", "srchStrtDtm": "2026-11-06 00:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mgr-what-needs-me-today [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 100, "prmtStatCd": "00", "srchEndDtm": "2026-11-06 23:59", "srchStrtDtm": "2026-11-06 00:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mgr-what-needs-me-today [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 10, "prmtStatCd": "00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mgr-what-needs-me-today [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 20, "prmtStatCd": "00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mgr-what-needs-me-today [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 100, "prmtStatCd": "00", "srchEndDtm": "2026-11-06 23:59", "srchStrtDtm": "2026-11-06 00:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mgr-what-needs-me-today [own-facade-raw] 3회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 50, "prmtStatCd": "10", "srchEndDtm": "2026-11-06 23:59:59", "srchStrtDtm": "2026-11-06 00:00:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mgr-what-needs-me-today [own-facade-raw] 3회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mgr-what-needs-me-today [own-facade-raw] 3회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-hero-free-next-weekend [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 20, "prmtStatCd": "10", "srchEndDtm": "2026-11-15 23:59:59", "srchStrtDtm": "2026-11-14 00:00:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-hero-free-next-weekend [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-hero-free-next-weekend [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-whats-running-this-weekend [own-facade-raw] 1회차 · `getPrmtGridListCnt` `{"srchEndDtm": "2026-11-08 23:59:59", "srchStrtDtm": "2026-11-07 00:00:00"}` → UPSTREAM_VALIDATION_FAILED: `2026-11-07 00:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `source:undocumented` mk-whats-running-this-weekend [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 50, "srchEndDtm": "2026-11-08T23:59:59-05:00", "srchStrtDtm": "2026-11-07T00:00:00-05:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-whats-running-this-weekend [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 50, "srchEndDtm": "2026-11-08T23:59:59-05:00", "srchStrtDtm": "2026-11-07T00:00:00-05:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-whats-running-this-weekend [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 50, "srchEndDtm": "2026-11-08 23:59", "srchStrtDtm": "2026-11-07 00:00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-whats-running-this-weekend [own-facade-raw] 3회차 · `getPrmtGridListCnt` `{"srchEndDtm": "2026-11-08 23:59:59", "srchStrtDtm": "2026-11-07 00:00:00"}` → UPSTREAM_VALIDATION_FAILED: `2026-11-07 00:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `source:undocumented` ops-frequent-returner [own-facade-raw] 1회차 · `getOrdGridList` `{"pageNo": 0, "srchKwd": "20431", "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-frequent-returner [own-facade-raw] 1회차 · `getOrdGridList` `{"pageNo": 0, "srchKwd": "20431", "ordDtmTo": "2026-11-06", "pageSize": 10, "ordStatCd": "10", "ordDtmFrom": "2026-11-01"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-frequent-returner [own-facade-raw] 1회차 · `getOrdGridList` `{"pageNo": 0, "srchKwd": "20431", "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-frequent-returner [own-facade-raw] 2회차 · `getOrdGridList` `{"pageNo": 0, "srchKwd": "20431", "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-frequent-returner [own-facade-raw] 2회차 · `getOrdGridList` `{"pageNo": 0, "srchKwd": "20431", "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-frequent-returner [own-facade-raw] 3회차 · `getOrdGridList` `{"pageNo": 0, "srchKwd": "20431", "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-frequent-returner [own-facade-raw] 3회차 · `getOrdGridList` `{"pageNo": 0, "srchKwd": "20431", "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-frequent-returner [own-facade-raw] 3회차 · `getOrdGridList` `{"pageNo": 0, "srchKwd": "20431", "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-wismo-tracking-stuck [own-facade-raw] 1회차 · `getOrdDtlPopInitData` `{"ordNo": "27184"}` → RESOURCE_NOT_FOUND: There is no order 27184.
- `source:undocumented` ops-wismo-tracking-stuck [own-facade-raw] 2회차 · `getOrdDtlPopInitData` `{"ordNo": "27184"}` → RESOURCE_NOT_FOUND: There is no order 27184.
- `source:undocumented` ops-wismo-tracking-stuck [own-facade-raw] 3회차 · `getOrdDtlPopInitData` `{"ordNo": "27184"}` → RESOURCE_NOT_FOUND: There is no order 27184.
- `model:described` b1-vip-weekend-sale [own-facade-a2api] 1회차 · `save_promotion_list` `{"rows": [{"ends_at": "2026-11-08T23:59:00-05:00", "starts_at": "2026-11-07T00:00:00-05:00", "applies_to": "category", "row_action": "insert", "percent_off": 20, "promotion_name": "Weekend VIP Summer ` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Row 1: `category_id` is required.
- `model:ungrounded` b1-vip-weekend-sale [own-facade-a2api] 1회차 · `get_product_detail_info_v2` `{"product_id": "{{product_id}}"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no product {{product_id}} in this store.
- `unclear` b1-vip-weekend-sale [own-facade-a2api] 2회차 · `get_promotion_target_member_list` `{"page_size": 1, "member_grade": "VIP"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Invalid member grade code.
- `unclear` b1-vip-weekend-sale [own-facade-a2api] 3회차 · `get_promotion_target_member_list` `{"page_size": 1, "member_grade": "VIP"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Invalid member grade code.
- `model:ungrounded` b2-returns-over-200 [own-facade-a2api] 1회차 · `save_customer_message_send` `{"text": "text", "channel": "email", "subject": "subject", "order_id": "order_id", "member_id": "member_id", "message_type": "decline"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no order order_id.
- `model:ungrounded` b2-returns-over-200 [own-facade-a2api] 3회차 · `save_customer_message_send` `{"text": "text", "channel": "email", "subject": "subject", "order_id": "order_id", "member_id": "member_id", "message_type": "decline"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no order order_id.
- `unclear` b3-why-sales-dropped [own-facade-a2api] 1회차 · `get_sale_analysis_grid_list` `{"to_date": "2026-11-05", "from_date": "2026-10-23", "compare_to": "same_weekday_last_4_weeks"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) same_weekday_last_4_weeks compares periods of 7 days at most; this one has 14. Use previous_period or custom.
- `unclear` b3-why-sales-dropped [own-facade-a2api] 2회차 · `get_sale_analysis_grid_list` `{"to_date": "2026-11-05", "from_date": "2026-10-23", "compare_to": "same_weekday_last_4_weeks"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) same_weekday_last_4_weeks compares periods of 7 days at most; this one has 14. Use previous_period or custom.
- `unclear` b3-why-sales-dropped [own-facade-a2api] 3회차 · `get_sale_analysis_grid_list` `{"to_date": "2026-11-05", "from_date": "2026-10-23", "compare_to": "same_weekday_last_4_weeks"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) same_weekday_last_4_weeks compares periods of 7 days at most; this one has 14. Use previous_period or custom.
- `model:described` md-end-of-season-markdown [own-facade-a2api] 1회차 · `save_promotion_list` `{"rows": [{"ends_at": "2026-11-15T23:59:00-05:00", "starts_at": "2026-11-06T11:00:00-05:00", "applies_to": "category", "row_action": "insert", "percent_off": 25, "promotion_name": "End of Season Markd` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Row 1: `category_id` is required.
- `model:described` md-end-of-season-markdown [own-facade-a2api] 2회차 · `save_promotion_list` `{"rows": [{"ends_at": "2026-11-15T23:59:00-05:00", "starts_at": "2026-11-06T11:00:00-05:00", "applies_to": "category", "row_action": "insert", "percent_off": 25, "promotion_name": "End of Season Markd` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Row 1: `category_id` is required.
- `model:described` md-end-of-season-markdown [own-facade-a2api] 3회차 · `save_promotion_list` `{"rows": [{"ends_at": "2026-11-15T23:59:00-05:00", "starts_at": "2026-11-06T11:00:00-05:00", "applies_to": "category", "row_action": "insert", "percent_off": 25, "promotion_name": "End of Season Markd` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Row 1: `category_id` is required.
- `model:described` ops-wismo-tracking-stuck [own-facade-a2api] 1회차 · `get_order_detail_popup_init_data` `{"order_id": "27184"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no order 27184.
- `model:described` ops-wismo-tracking-stuck [own-facade-a2api] 2회차 · `get_order_detail_popup_init_data` `{"order_id": "27184"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no order 27184.
- `model:described` ops-wismo-tracking-stuck [own-facade-a2api] 3회차 · `get_order_detail_popup_init_data` `{"order_id": "27184"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no order 27184.
- `model:ungrounded` b1-vip-weekend-sale [own-facade-a2api-lookup] 2회차 · `get_product_grid_list` `{"page": 1, "page_size": 100, "category_id": "summer_outerwear", "availability": "in_stock"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no category summer_outerwear.
- `model:ungrounded` b2-returns-over-200 [own-facade-a2api-lookup] 1회차 · `save_customer_message_send` `{"text": "text", "channel": "email", "subject": "subject", "order_id": "order_id", "member_id": "member_id", "message_type": "decline"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no order order_id.
- `model:ungrounded` b2-returns-over-200 [own-facade-a2api-lookup] 2회차 · `save_customer_message_send` `{"text": "text", "channel": "email", "subject": "subject", "order_id": "order_id", "member_id": "member_id", "message_type": "decline"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no order order_id.
- `unclear` b3-why-sales-dropped [own-facade-a2api-lookup] 1회차 · `get_sale_analysis_grid_list` `{"to_date": "2026-11-05", "from_date": "2026-10-23", "compare_to": "same_weekday_last_4_weeks"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) same_weekday_last_4_weeks compares periods of 7 days at most; this one has 14. Use previous_period or custom.
- `model:described` mk-hero-free-next-weekend [own-facade-a2api-lookup] 2회차 · `save_display_banner_list` `{"rows": [{"ends_at": "2026-11-15T23:59:00-05:00", "headline": "VIP Weekend", "link_url": "/vip-weekend", "corner_id": "hero", "starts_at": "2026-11-14T00:00:00-05:00", "row_action": "insert", "button` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Row 1: `image_product_id` or `image_id` is required.
- `model:described` mk-hero-free-next-weekend [own-facade-a2api-lookup] 3회차 · `save_display_banner_list` `{"rows": [{"ends_at": "2026-11-15T23:59:00-05:00", "headline": "VIP Weekend", "link_url": "/vip", "corner_id": "homepage_hero", "starts_at": "2026-11-14T00:00:00-05:00", "row_action": "insert", "butto` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Row 1: `image_product_id` or `image_id` is required.
- `unclear` b1-vip-weekend-sale [own-acom] 1회차 · `schedule_banner` `{"slot_id": "slot_main_hero", "audience": "vip", "valid_from": "2026-11-07T00:00:00-05:00", "valid_through": "2026-11-08T23:59:00-05:00"}` → UNKNOWN: The arguments for schedule_banner are not usable: missing content.
- `model:ungrounded` b1-vip-weekend-sale [own-acom] 1회차 · `schedule_banner` `{"content": {"url": "/c/cat_summer_outerwear", "eyebrow": "VIP Weekend", "headline": "20% off Summer Outerwear", "cta_label": "Shop Now", "image_source": "product", "image_product_id": "prd_summer_out` → RESOURCE_NOT_FOUND: There is no promotion promo_summer_outerwear_vip_weekend.
- `model:ungrounded` b1-vip-weekend-sale [own-acom] 1회차 · `schedule_banner` `{"content": {"url": "/c/cat_summer_outerwear", "headline": "VIP Summer Outerwear Weekend Sale", "cta_label": "Shop Now", "image_source": "product", "image_product_id": "prd_summer_outerwear_22"}, "slo` → RESOURCE_NOT_FOUND: There is no promotion promo_summer_outerwear_vip_weekend.
- `source:undocumented` b1-vip-weekend-sale [own-acom] 1회차 · `set_sale_prices` `{"name": "VIP Summer Outerwear Weekend Sale", "overrides": [{"product_id": "prd_overshirt_01", "percent_off": 15}], "scope_mode": "category", "valid_from": "2026-11-07T00:00:00-05:00", "category_id": ` → UPSTREAM_VALIDATION_FAILED: prd_overshirt_01 in `overrides` is not in the sale's scope.
- `unclear` md-end-of-season-markdown [own-acom] 1회차 · `create_promotion` `{"name": "End of Season Markdown Tees", "scope_mode": "categories", "valid_from": "2026-11-06T00:00:00-05:00", "percent_off": 25, "product_ids": ["prd_summer_outerwear_03", "prd_summer_outerwear_07", ` → percent_off_for_tier: A percent off for a tier or a period is a sale price; make it with set_sale_prices.
- `model:described` md-end-of-season-markdown [own-acom] 3회차 · `create_promotion` `{"name": "End of Season Markdown Tees", "scope_mode": "categories", "valid_from": "2026-11-06T00:00:00-05:00", "product_ids": ["prd_tees_14", "prd_tees_04", "prd_tees_09", "prd_tees_22", "prd_tees_02"` → UPSTREAM_VALIDATION_FAILED: `amount_off` needs `amount_off`.
- `model:described` ops-wismo-tracking-stuck [own-acom] 1회차 · `track_shipment` `{"mode": "delivery"}` → UPSTREAM_VALIDATION_FAILED: mode delivery needs delivery_id.
- `unclear` ops-wismo-tracking-stuck [own-acom] 2회차 · `get_order` `{"order_id": "1"}` → RESOURCE_NOT_FOUND: No order has the number 1.
- `model:described` ops-wismo-tracking-stuck [own-acom] 2회차 · `track_shipment` `{"mode": "delivery"}` → UPSTREAM_VALIDATION_FAILED: mode delivery needs delivery_id.
- `model:described` ops-wismo-tracking-stuck [own-acom] 3회차 · `track_shipment` `{"mode": "delivery"}` → UPSTREAM_VALIDATION_FAILED: mode delivery needs delivery_id.

## 기대와 다른 쓰기 입력

- b1-vip-weekend-sale [own-acom] 1회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [own-acom] 2회차 · `set_sale_prices` 기대 {"valid_for_member_tier": "vip", "percent_off": 20} · 부르지 않음
- b1-vip-weekend-sale [own-acom] 2회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [own-acom] 2회차 · `schedule_banner` 기대 {"slot_id": "slot_home_hero"} · 부르지 않음
- b1-vip-weekend-sale [own-acom] 3회차 · `set_sale_prices` 기대 {"valid_for_member_tier": "vip", "percent_off": 20} · 부르지 않음
- b1-vip-weekend-sale [own-acom] 3회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [own-acom] 3회차 · `schedule_banner` 기대 {"slot_id": "slot_home_hero"} · 부르지 않음
- b2-returns-over-200 [own-acom] 1회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [own-acom] 1회차 · `send_customer_message` 기대 {} · 부르지 않음
- b2-returns-over-200 [own-acom] 2회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [own-acom] 2회차 · `send_customer_message` 기대 {} · 부르지 않음
- b2-returns-over-200 [own-acom] 3회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [own-acom] 3회차 · `send_customer_message` 기대 {} · 부르지 않음
- md-end-of-season-markdown [own-acom] 1회차 · `set_sale_prices` 기대 {"valid_for_member_tier": "everyone", "scope_mode": "category", "category_id": "cat_tees", "exclude_low_stock": true} · 부르지 않음
- md-end-of-season-markdown [own-acom] 2회차 · `set_sale_prices` 기대 {"valid_for_member_tier": "everyone", "scope_mode": "category", "category_id": "cat_tees", "exclude_low_stock": true} · 부르지 않음
- md-end-of-season-markdown [own-acom] 3회차 · `set_sale_prices` 기대 {"valid_for_member_tier": "everyone", "scope_mode": "category", "category_id": "cat_tees", "exclude_low_stock": true} · 부르지 않음
