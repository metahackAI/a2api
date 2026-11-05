# 호출 단계 리뷰 — luna-heldout-raw, luna-heldout-a2api, luna-heldout-acom

a-commerce 자체 에이전트. "모델에게 줌"은 에이전트의 도구 검색이 계획기에 준 후보다. 판정 기준 함수 정의: 원본 화면 / a2api 변환 화면(`--converted`) / A-Commerce 도구.

단계: A0 API에 해당 기능 없음 · A 필요한 함수를 받지 못함 · B 받았지만 부르지 않음 · C 불렀지만 성공 못 함 · D-before 필요한 함수를 부르기 전 한도·오류로 중단 · D-after 필요한 함수는 모두 성공했는데 답하기 전 한도로 중단 · E-write 쓰기 입력·change set · E-format 숫자는 있으나 표기 · E-content 답 내용 누락

## 필요한 함수: 확보 → 호출 → 성공

| 방식 | 통과 | 필요한 함수(API에 있음/전체) | 모델에게 줌 | 불렀음 | 성공 | 확보 기록 |
|---|---|---|---|---|---|---|
| own-facade-raw | 10/48 | 24/48 | 21/24 (88%) | 17/24 (71%) | 9/24 (38%) | 단계별 기록 |
| own-facade-a2api-lookup | 11/48 | 24/48 | 24/24 (100%) | 24/24 (100%) | 23/24 (96%) | 단계별 기록 |
| own-acom | 9/48 | 48/48 | 39/48 (81%) | 33/48 (69%) | 33/48 (69%) | 단계별 기록 |

## 실패한 실행이 처음 막힌 단계

| 방식 | passed | A0 | A | B | C | D-before | D-after | E-write | E-format | E-content |
|---|---|---|---|---|---|---|---|---|---|---|
| own-facade-raw | 10 | 15 | 3 | 4 | 8 | 0 | 0 | 0 | 0 | 8 |
| own-facade-a2api-lookup | 11 | 15 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 21 |
| own-acom | 9 | 0 | 9 | 3 | 0 | 0 | 0 | 3 | 2 | 22 |

## 실패한 업무 호출의 원인

| 방식 | 업무 호출 | 실패 | model:schema | model:function | model:ungrounded | model:described | source:undocumented | business | unclear |
|---|---|---|---|---|---|---|---|---|---|
| own-facade-raw | 104 | 62 | 0 | 0 | 0 | 0 | 55 | 1 | 6 |
| own-facade-a2api-lookup | 137 | 5 | 0 | 0 | 0 | 3 | 0 | 0 | 2 |
| own-acom | 125 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |

## 쓰기 입력(과업이 기대한 change set 항목)

| 방식 | 기대 항목 | 불렀음 | 입력 일치 |
|---|---|---|---|
| own-acom | 6 | 5 | 0 |

## 실패한 호출 목록

- `source:undocumented` md-below-cost [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "aplyDtm": "2026-11-06 11:00:00", "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-below-cost [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "aplyDtm": "2026-11-06 11:00", "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-below-cost [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-best-sellers-this-month [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-best-sellers-this-month [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-best-sellers-this-month [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-broken-sizes-outerwear [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "outerwear", "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-broken-sizes-outerwear [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "outerwear", "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-broken-sizes-outerwear [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "outerwear", "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-broken-sizes-outerwear [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "outerwear", "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-broken-sizes-outerwear [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "outerwear", "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-broken-sizes-outerwear [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "outerwear", "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-out-of-stock-30-days [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 100, "stkQtyTo": 0, "stkQtyFrom": 0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-out-of-stock-30-days [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 100, "stkQtyTo": 0, "stkQtyFrom": 0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-out-of-stock-30-days [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 100, "stkQtyTo": 0, "stkQtyFrom": 0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-out-of-stock-30-days [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 100, "stkQtyTo": 0, "stkQtyFrom": 0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-out-of-stock-30-days [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 100, "stkQtyTo": 0, "stkQtyFrom": 0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-out-of-stock-30-days [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 100, "stkQtyTo": 0, "stkQtyFrom": 0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `unclear` md-out-of-stock-30-days [own-facade-raw] 3회차 · `getPrdDtlInfo` `{"prdNo": ""}` → RESOURCE_NOT_FOUND: There is no product  in this store.
- `unclear` mgr-how-is-business [own-facade-raw] 2회차 · `getSaleAnlsGridList` `{"srchEndDt": "2026-11-06", "cmprBaseCd": "1", "srchStrtDt": "2026-10-01"}` → UPSTREAM_VALIDATION_FAILED: same_weekday_last_4_weeks compares periods of 7 days at most; this one has 37. Use previous_period or custom.
- `unclear` mgr-how-is-business [own-facade-raw] 2회차 · `getSaleAnlsGridList` `{"srchEndDt": "2026-11-06", "cmprBaseCd": "1", "srchStrtDt": "2026-10-01"}` → UPSTREAM_VALIDATION_FAILED: same_weekday_last_4_weeks compares periods of 7 days at most; this one has 37. Use previous_period or custom.
- `unclear` mgr-how-is-business [own-facade-raw] 2회차 · `getSaleAnlsGridList` `{"srchEndDt": "2026-11-06", "cmprBaseCd": "1", "srchStrtDt": "2026-10-01"}` → UPSTREAM_VALIDATION_FAILED: same_weekday_last_4_weeks compares periods of 7 days at most; this one has 37. Use previous_period or custom.
- `source:undocumented` mgr-undo-banner [own-facade-raw] 1회차 · `getDispCornerList` `{"endDtm": "2026-11-06 11:00:00", "strtDtm": "2026-01-01 00:00:00", "dispPageCd": "01"}` → UPSTREAM_VALIDATION_FAILED: `2026-01-01 00:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `source:undocumented` mgr-undo-banner [own-facade-raw] 1회차 · `saveDispBnrList` `{"rows": []}` → UPSTREAM_VALIDATION_FAILED: No rows.
- `source:undocumented` mgr-undo-banner [own-facade-raw] 1회차 · `saveDispBnrList` `{"rows": [{"bnrTitl": "The October edit", "rowStat": "I", "strtDtm": "2026-11-06T11:00:00-05:00", "cornerNo": "slot_home_hero", "tgtMbrGrdCd": "G00"}]}` → UPSTREAM_VALIDATION_FAILED: Row 1: `btnNm` is required.
- `source:undocumented` mgr-undo-banner [own-facade-raw] 2회차 · `getDispCornerList` `{"endDtm": "2099-12-31 23:59:59", "strtDtm": "2000-01-01 00:00:00", "dispPageCd": "01"}` → UPSTREAM_VALIDATION_FAILED: `2000-01-01 00:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `source:undocumented` mgr-undo-banner [own-facade-raw] 3회차 · `getDispCornerList` `{"endDtm": "2026-11-06 11:00:00", "strtDtm": "2000-01-01 00:00:00", "dispPageCd": "01"}` → UPSTREAM_VALIDATION_FAILED: `2000-01-01 00:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `source:undocumented` mk-category-promotion [own-facade-raw] 1회차 · `savePrmtList` `{"rows": [{"dcRt": 0.2, "endDtm": "2026-11-20 10:59", "prmtNm": "Outerwear $50 Off $250+", "rowStat": "I", "strtDtm": "2026-11-06 11:00", "prmtTpCd": "T01", "aplyTgtCd": "C", "prmtStatCd": "00"}]}` → UPSTREAM_VALIDATION_FAILED: Row 1: `ctgNo` is required.
- `source:undocumented` mk-category-promotion [own-facade-raw] 1회차 · `savePrmtList` `{"rows": [{"ctgNo": "Outerwear", "endDtm": "2026-11-20 23:59", "prmtNm": "Outerwear: $50 off orders above $250", "rowStat": "I", "strtDtm": "2026-11-06 11:00", "aplyTgtCd": "C"}]}` → UPSTREAM_VALIDATION_FAILED: Row 1: `prmtTpCd` is required.
- `source:undocumented` mk-category-promotion [own-facade-raw] 1회차 · `savePrmtList` `{"rows": [{"ctgNo": "Outerwear", "endDtm": "2026-11-20 23:59", "prmtNm": "Outerwear $50 Off $250+", "rowStat": "I", "strtDtm": "2026-11-06 11:00", "prmtTpCd": "T01", "aplyTgtCd": "C"}]}` → UPSTREAM_VALIDATION_FAILED: Row 1: `dcRt` is required.
- `source:undocumented` mk-category-promotion [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "prmtNm": "Outerwear", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-category-promotion [own-facade-raw] 3회차 · `savePrmtList` `{"rows": [{"endDtm": "2026-11-20 10:59", "prmtNm": "Outerwear $50 Off Orders Above $250", "rowStat": "I", "strtDtm": "2026-11-06 11:00", "prmtTpCd": "T01", "aplyTgtCd": "C", "prmtStatCd": "00"}]}` → UPSTREAM_VALIDATION_FAILED: Row 1: `dcRt` is required.
- `source:undocumented` mk-category-promotion [own-facade-raw] 3회차 · `savePrmtList` `{"rows": [{"dcRt": 50, "endDtm": "2026-11-20 10:59", "prmtNm": "Outerwear $50 Off $250+", "rowStat": "I", "strtDtm": "2026-11-06 11:00", "prmtTpCd": "T01", "aplyTgtCd": "C", "prmtStatCd": "00"}]}` → UPSTREAM_VALIDATION_FAILED: Row 1: `ctgNo` is required.
- `business` mk-category-promotion [own-facade-raw] 3회차 · `savePrmtList` `{"rows": [{"ctgNo": "Outerwear", "endDtm": "2026-11-20 23:59", "prmtNm": "Outerwear $50 Off $250+", "rowStat": "I", "strtDtm": "2026-11-06 11:00", "prmtTpCd": "T02", "aplyTgtCd": "C", "prmtStatCd": "1` → UPSTREAM_CONFLICT: Row 1: Promotion type not available on this screen.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "prmtNm": "knit", "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "prmtNm": "knit", "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "prmtNm": "knit", "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "prmtNm": "knit", "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "prmtNm": "knit", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "prmtNm": "knit", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-raw] 3회차 · `getPrmtGridList` `{"pageNo": 0, "prmtNm": "knit", "pageSize": 50}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-raw] 3회차 · `getPrmtGridList` `{"pageNo": 0, "prmtNm": "knit sale", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-raw] 3회차 · `getPrmtGridList` `{"pageNo": 0, "prmtNm": "knit", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-viewed-not-purchased [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-viewed-not-purchased [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-viewed-not-purchased [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-winback [own-facade-raw] 2회차 · `getPrmtTgtMbrList` `{"pageNo": 0, "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-winback [own-facade-raw] 3회차 · `getPrmtTgtMbrList` `{"pageNo": 0, "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-cancel-delivered [own-facade-raw] 1회차 · `getOrdDtlPopInitData` `{"ordNo": "20402"}` → RESOURCE_NOT_FOUND: There is no order 20402.
- `source:undocumented` ops-cancel-delivered [own-facade-raw] 2회차 · `getOrdDtlPopInitData` `{"ordNo": "20402"}` → RESOURCE_NOT_FOUND: There is no order 20402.
- `source:undocumented` ops-cancel-delivered [own-facade-raw] 3회차 · `getOrdDtlPopInitData` `{"ordNo": "20402"}` → RESOURCE_NOT_FOUND: There is no order 20402.
- `unclear` ops-photo-request [own-facade-raw] 1회차 · `saveCustMsgSend` `{"mbrNo": "cus_riley", "msgCntt": "Could you please send us photos of the damage? Thank you.", "msgTpCd": "M02"}` → UPSTREAM_VALIDATION_FAILED: Say which order the message is about.
- `unclear` ops-photo-request [own-facade-raw] 2회차 · `saveCustMsgSend` `{"mbrNo": "cus_riley", "msgCntt": "Could you please send us photos of the damage? Thank you.", "msgTpCd": "M02"}` → UPSTREAM_VALIDATION_FAILED: Say which order the message is about.
- `source:undocumented` ops-photo-request [own-facade-raw] 3회차 · `getOrdGridList` `{"pageNo": 0, "srchKwd": "20366", "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-photo-request [own-facade-raw] 3회차 · `getOrdGridList` `{"pageNo": 0, "srchKwd": "20366", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-photo-request [own-facade-raw] 3회차 · `getOrdGridList` `{"pageNo": 0, "srchKwd": "20366", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-unfulfilled-3-days [own-facade-raw] 2회차 · `getOrdGridList` `{"pageNo": 0, "ordDtmTo": "2026-11-03 11:00", "pageSize": 100, "ordStatCd": "10"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-unfulfilled-3-days [own-facade-raw] 2회차 · `getOrdGridList` `{"pageNo": 0, "ordDtmTo": "2026-11-03 11:00", "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-unfulfilled-3-days [own-facade-raw] 2회차 · `getOrdGridList` `{"pageNo": 0, "pageSize": 50}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-unfulfilled-3-days [own-facade-raw] 3회차 · `getOrdGridList` `{"pageNo": 0, "ordDtmTo": "2026-11-03 11:00", "pageSize": 100, "ordStatCd": "20"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-unfulfilled-3-days [own-facade-raw] 3회차 · `getOrdGridList` `{"pageNo": 0, "pageSize": 50}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-unfulfilled-3-days [own-facade-raw] 3회차 · `getOrdGridList` `{"pageNo": 0, "pageSize": 50, "ordStatCd": "20"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:described` mk-pause-knit-until-monday [own-facade-a2api-lookup] 1회차 · `save_promotion_list` `{"rows": [{"row_action": "update", "promotion_status": "paused"}]}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Row 1: `promotion_id` is required.
- `model:described` mk-pause-knit-until-monday [own-facade-a2api-lookup] 2회차 · `save_promotion_list` `{"rows": [{"row_action": "update", "promotion_status": "paused"}]}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Row 1: `promotion_id` is required.
- `model:described` mk-pause-knit-until-monday [own-facade-a2api-lookup] 3회차 · `save_promotion_list` `{"rows": [{"row_action": "update", "promotion_status": "paused"}]}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Row 1: `promotion_id` is required.
- `unclear` ops-photo-request [own-facade-a2api-lookup] 1회차 · `save_customer_message_send` `{"text": "Could you please send us photos showing the damage? Thank you.", "member_id": "cus_riley", "message_type": "ask_for_photos"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Say which order the message is about.
- `unclear` ops-photo-request [own-facade-a2api-lookup] 2회차 · `save_customer_message_send` `{"text": "Could you please send us photos showing the damage? Thank you.", "member_id": "cus_riley", "message_type": "ask_for_photos"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Say which order the message is about.
- `unclear` mgr-weekly-summary [own-acom] 2회차 · `get_sales_overview` `{"valid_from": "2026-11-02", "valid_through": "2026-11-08"}` → UPSTREAM_VALIDATION_FAILED: The period ends on 2026-11-08, after today (2026-11-06); sales after today are not known yet.
- `unclear` mgr-weekly-summary [own-acom] 3회차 · `get_sales_overview` `{"valid_from": "2026-11-02", "valid_through": "2026-11-08"}` → UPSTREAM_VALIDATION_FAILED: The period ends on 2026-11-08, after today (2026-11-06); sales after today are not known yet.
- `unclear` ops-photo-request [own-acom] 2회차 · `send_customer_message` `{"kind": "ask_for_photos", "text": "Could you please send us photos showing the damage? This will help us review your request."}` → UPSTREAM_VALIDATION_FAILED: Say which order the message is about (it goes to the order's customer), or which customer it goes to.

## 기대와 다른 쓰기 입력

- mk-pause-knit-until-monday [own-acom] 1회차 · `pause_promotion` 기대 {"promotion_id": "promo_autumn_knit"} · 부르지 않음
- mk-pause-knit-until-monday [own-acom] 2회차 · `pause_promotion` 기대 {"promotion_id": "promo_autumn_knit"} · 불일치: [{"promotion_id": null}]
- mk-pause-knit-until-monday [own-acom] 3회차 · `pause_promotion` 기대 {"promotion_id": "promo_autumn_knit"} · 불일치: [{"promotion_id": null}]
- ops-photo-request [own-acom] 1회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": null}]
- ops-photo-request [own-acom] 2회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}, {"customer_id": null, "kind": null}]
- ops-photo-request [own-acom] 3회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": null}]
