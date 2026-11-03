# 호출 단계 리뷰 — own-latest-heldout-raw, own-latest-heldout-a2api, own-latest-heldout-a2api-lookup, own-latest-heldout-acom

a-commerce 자체 에이전트. "모델에게 줌"은 에이전트의 도구 검색이 계획기에 준 후보다. 판정 기준 함수 정의: 원본 화면 / a2api 변환 화면(`--converted`) / A-Commerce 도구.

단계: A0 API에 해당 기능 없음 · A 필요한 함수를 받지 못함 · B 받았지만 부르지 않음 · C 불렀지만 성공 못 함 · D-before 필요한 함수를 부르기 전 한도·오류로 중단 · D-after 필요한 함수는 모두 성공했는데 답하기 전 한도로 중단 · E-write 쓰기 입력·change set · E-format 숫자는 있으나 표기 · E-content 답 내용 누락

## 필요한 함수: 확보 → 호출 → 성공

| 방식 | 통과 | 필요한 함수(API에 있음/전체) | 모델에게 줌 | 불렀음 | 성공 | 확보 기록 |
|---|---|---|---|---|---|---|
| own-facade-raw | 7/48 | 24/48 | 21/24 (88%) | 13/24 (54%) | 8/24 (33%) | 단계별 기록 |
| own-facade-a2api | 9/48 | 24/48 | 24/24 (100%) | 21/24 (88%) | 15/24 (62%) | 단계별 기록 |
| own-facade-a2api-lookup | 12/48 | 24/48 | 24/24 (100%) | 21/24 (88%) | 21/24 (88%) | 단계별 기록 |
| own-acom | 11/48 | 48/48 | 39/48 (81%) | 36/48 (75%) | 36/48 (75%) | 단계별 기록 |

## 실패한 실행이 처음 막힌 단계

| 방식 | passed | A0 | A | B | C | D-before | D-after | E-write | E-format | E-content |
|---|---|---|---|---|---|---|---|---|---|---|
| own-facade-raw | 7 | 18 | 3 | 8 | 5 | 0 | 0 | 0 | 0 | 7 |
| own-facade-a2api | 9 | 18 | 0 | 3 | 6 | 0 | 0 | 0 | 0 | 12 |
| own-facade-a2api-lookup | 12 | 18 | 0 | 3 | 0 | 0 | 0 | 0 | 3 | 12 |
| own-acom | 11 | 0 | 9 | 0 | 0 | 0 | 1 | 3 | 4 | 20 |

## 실패한 업무 호출의 원인

| 방식 | 업무 호출 | 실패 | model:schema | model:function | model:ungrounded | model:described | source:undocumented | business | unclear |
|---|---|---|---|---|---|---|---|---|---|
| own-facade-raw | 94 | 72 | 0 | 0 | 1 | 0 | 67 | 0 | 4 |
| own-facade-a2api | 67 | 21 | 0 | 0 | 2 | 6 | 4 | 3 | 6 |
| own-facade-a2api-lookup | 69 | 15 | 0 | 0 | 2 | 0 | 4 | 3 | 6 |
| own-acom | 177 | 18 | 0 | 0 | 10 | 5 | 0 | 0 | 3 |

## 쓰기 입력(과업이 기대한 change set 항목)

| 방식 | 기대 항목 | 불렀음 | 입력 일치 |
|---|---|---|---|
| own-acom | 6 | 6 | 0 |

## 실패한 호출 목록

- `source:undocumented` md-best-sellers-this-month [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-best-sellers-this-month [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-best-sellers-this-month [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-broken-sizes-outerwear [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "outerwear", "pageSize": 50}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-broken-sizes-outerwear [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "outerwear", "pageSize": 64}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-broken-sizes-outerwear [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "outerwear", "pageSize": 64}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-broken-sizes-outerwear [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "outerwear", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-broken-sizes-outerwear [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "outerwear", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-broken-sizes-outerwear [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "outerwear", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-broken-sizes-outerwear [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "outerwear", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-how-many-left [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "Light rain parka", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-how-many-left [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "Light rain parka", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-how-many-left [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "Light rain parka", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-how-many-left [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "Light rain parka", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-how-many-left [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "Light rain parka", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-how-many-left [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "Light rain parka", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-how-many-left [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "Light rain parka", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-how-many-left [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "Light rain parka", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-how-many-left [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "srchKwd": "Light rain parka", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-out-of-stock-30-days [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 100, "stkQtyTo": 0, "stkQtyFrom": 0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-out-of-stock-30-days [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 100, "stkQtyTo": 0, "stkQtyFrom": 0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-out-of-stock-30-days [own-facade-raw] 1회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 100, "stkQtyTo": 0, "stkQtyFrom": 0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-out-of-stock-30-days [own-facade-raw] 2회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 50, "stkQtyTo": 0, "stkQtyFrom": 0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-out-of-stock-30-days [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 50, "stkQtyTo": 0, "stkQtyFrom": 0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-out-of-stock-30-days [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 100, "stkQtyTo": 0, "stkQtyFrom": 0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-out-of-stock-30-days [own-facade-raw] 3회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 100, "stkQtyTo": 0, "stkQtyFrom": 0}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `unclear` mgr-how-is-business [own-facade-raw] 1회차 · `getSaleAnlsGridList` `{"srchEndDt": "2026-11-06", "cmprBaseCd": "1", "srchStrtDt": "2026-10-06"}` → UPSTREAM_VALIDATION_FAILED: same_weekday_last_4_weeks compares periods of 7 days at most; this one has 32. Use previous_period or custom.
- `unclear` mgr-how-is-business [own-facade-raw] 2회차 · `getSaleAnlsGridList` `{"srchEndDt": "2026-11-06", "cmprBaseCd": "1", "srchStrtDt": "2026-10-01"}` → UPSTREAM_VALIDATION_FAILED: same_weekday_last_4_weeks compares periods of 7 days at most; this one has 37. Use previous_period or custom.
- `unclear` mgr-how-is-business [own-facade-raw] 3회차 · `getSaleAnlsGridList` `{"srchEndDt": "2026-11-06", "cmprBaseCd": "1", "srchStrtDt": "2026-10-06"}` → UPSTREAM_VALIDATION_FAILED: same_weekday_last_4_weeks compares periods of 7 days at most; this one has 32. Use previous_period or custom.
- `model:ungrounded` mgr-weekly-summary [own-facade-raw] 1회차 · `getMbrGrdList` `{"prgmNo": "1"}` → RESOURCE_NOT_FOUND: There is no program 1.
- `source:undocumented` mk-category-promotion [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 1, "prmtStatCd": "00"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-category-promotion [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-category-promotion [own-facade-raw] 2회차 · `savePrmtList` `{"rows": [{"dcRt": 0, "ctgNo": "", "endDtm": "2026-11-20 23:59", "prmtNm": "Outerwear $50 off orders above $250", "rowStat": "I", "strtDtm": "2026-11-06 11:00", "prmtTpCd": "T01", "aplyTgtCd": "C", "p` → UPSTREAM_VALIDATION_FAILED: Row 1: `percent_off` must be above 0 and below 100, with at most two decimals; got 0.
- `source:undocumented` mk-category-promotion [own-facade-raw] 2회차 · `savePrmtList` `{"rows": [{"dcRt": 0, "ctgNo": "", "endDtm": "2026-11-20 11:00", "prmtNm": "Outerwear $50 off orders above $250", "rowStat": "I", "strtDtm": "2026-11-06 11:00", "prmtTpCd": "T01", "aplyTgtCd": "C", "p` → UPSTREAM_VALIDATION_FAILED: Row 1: `percent_off` must be above 0 and below 100, with at most two decimals; got 0.
- `source:undocumented` mk-category-promotion [own-facade-raw] 2회차 · `savePrmtList` `{"rows": [{"dcRt": 0, "ctgNo": "", "endDtm": "2026-11-20 11:00", "prmtNm": "Outerwear $50 off orders above $250", "rowStat": "I", "strtDtm": "2026-11-06 11:00", "prmtTpCd": "T01", "aplyTgtCd": "C", "p` → UPSTREAM_VALIDATION_FAILED: Row 1: `percent_off` must be above 0 and below 100, with at most two decimals; got 0.
- `source:undocumented` mk-category-promotion [own-facade-raw] 3회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 10, "prmtStatCd": "10"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "prmtNm": "knit", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "prmtNm": "knit sale", "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-raw] 1회차 · `getPrmtGridList` `{"pageNo": 0, "prmtNm": "knit sale", "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "prmtNm": "knit", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "prmtNm": "knit sale", "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-raw] 2회차 · `getPrmtGridList` `{"pageNo": 0, "prmtNm": "knit sale", "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-raw] 3회차 · `getPrmtGridList` `{"pageNo": 0, "prmtNm": "knit", "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-raw] 3회차 · `getPrmtGridList` `{"pageNo": 0, "prmtNm": "knit sale", "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-raw] 3회차 · `getPrmtGridList` `{"pageNo": 0, "prmtNm": "knit sale", "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-winback [own-facade-raw] 1회차 · `getPrmtTgtMbrList` `{"pageNo": 0, "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-winback [own-facade-raw] 1회차 · `getPrmtTgtMbrList` `{"pageNo": 0, "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-winback [own-facade-raw] 1회차 · `getPrmtTgtMbrList` `{"pageNo": 0, "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-winback [own-facade-raw] 2회차 · `getPrmtTgtMbrList` `{"pageNo": 0, "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-winback [own-facade-raw] 2회차 · `getPrmtTgtMbrList` `{"pageNo": 0, "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-winback [own-facade-raw] 2회차 · `getPrmtTgtMbrList` `{"pageNo": 0, "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-winback [own-facade-raw] 3회차 · `getPrmtTgtMbrList` `{"pageNo": 0, "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-winback [own-facade-raw] 3회차 · `getPrmtTgtMbrList` `{"pageNo": 0, "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-winback [own-facade-raw] 3회차 · `getPrmtTgtMbrList` `{"pageNo": 0, "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-cancel-delivered [own-facade-raw] 1회차 · `getOrdDtlPopInitData` `{"ordNo": "20402"}` → RESOURCE_NOT_FOUND: There is no order 20402.
- `source:undocumented` ops-cancel-delivered [own-facade-raw] 2회차 · `getOrdDtlPopInitData` `{"ordNo": "20402"}` → RESOURCE_NOT_FOUND: There is no order 20402.
- `source:undocumented` ops-cancel-delivered [own-facade-raw] 3회차 · `getOrdDtlPopInitData` `{"ordNo": "20402"}` → RESOURCE_NOT_FOUND: There is no order 20402.
- `source:undocumented` ops-change-address-in-transit [own-facade-raw] 2회차 · `getOrdGridList` `{"pageNo": 0, "srchKwd": "27184", "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-change-address-in-transit [own-facade-raw] 2회차 · `getOrdGridList` `{"pageNo": 0, "srchKwd": "27184", "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-change-address-in-transit [own-facade-raw] 2회차 · `getOrdGridList` `{"pageNo": 0, "srchKwd": "27184", "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-photo-request [own-facade-raw] 1회차 · `getOrdGridList` `{"pageNo": 0, "srchKwd": "20366", "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `unclear` ops-photo-request [own-facade-raw] 2회차 · `saveCustMsgSend` `{"mbrNo": "", "msgCntt": "Could you please share photos of the damage? This will help us assess the issue and assist you promptly.", "msgTpCd": "M01"}` → UPSTREAM_VALIDATION_FAILED: Say which order the message is about.
- `source:undocumented` ops-photo-request [own-facade-raw] 3회차 · `getOrdGridList` `{"pageNo": 0, "srchKwd": "20366", "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-unfulfilled-3-days [own-facade-raw] 1회차 · `getOrdGridList` `{"pageNo": 0, "ordDtmTo": "2026-11-06", "pageSize": 50, "ordStatCd": "20", "ordDtmFrom": "2026-10-31"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-unfulfilled-3-days [own-facade-raw] 1회차 · `getOrdGridList` `{"pageNo": 0, "ordDtmTo": "2026-11-06", "pageSize": 100, "ordStatCd": "20", "ordDtmFrom": "2026-10-31"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-unfulfilled-3-days [own-facade-raw] 1회차 · `getOrdGridList` `{"pageNo": 0, "ordDtmTo": "2026-11-06", "pageSize": 100, "ordStatCd": "20", "ordDtmFrom": "2026-10-31"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-unfulfilled-3-days [own-facade-raw] 2회차 · `getOrdGridList` `{"pageNo": 0, "ordDtmTo": "2026-11-06", "pageSize": 50, "ordStatCd": "20", "ordDtmFrom": "2026-11-02"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-unfulfilled-3-days [own-facade-raw] 2회차 · `getOrdGridList` `{"pageNo": 0, "ordDtmTo": "2026-11-06", "pageSize": 100, "ordStatCd": "20", "ordDtmFrom": "2026-11-02"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-unfulfilled-3-days [own-facade-raw] 2회차 · `getOrdGridList` `{"pageNo": 0, "ordDtmTo": "2026-11-06", "pageSize": 100, "ordStatCd": "20", "ordDtmFrom": "2026-11-02"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-unfulfilled-3-days [own-facade-raw] 3회차 · `getOrdGridList` `{"pageNo": 0, "ordDtmTo": "2026-11-06", "pageSize": 50, "ordStatCd": "20", "ordDtmFrom": "2026-11-03"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-unfulfilled-3-days [own-facade-raw] 3회차 · `getOrdGridList` `{"pageNo": 0, "ordDtmTo": "2026-11-06", "pageSize": 100, "ordStatCd": "20", "ordDtmFrom": "2026-11-03"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-unfulfilled-3-days [own-facade-raw] 3회차 · `getOrdGridList` `{"pageNo": 0, "ordDtmTo": "2026-11-06", "pageSize": 100, "ordStatCd": "20", "ordDtmFrom": "2026-11-03"}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `unclear` md-how-many-left [own-facade-a2api] 1회차 · `get_product_detail_info_v2` `{"product_id": ""}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no product in this store.
- `unclear` md-how-many-left [own-facade-a2api] 2회차 · `get_product_detail_info_v2` `{"product_id": ""}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no product in this store.
- `unclear` md-how-many-left [own-facade-a2api] 3회차 · `get_product_detail_info_v2` `{"product_id": ""}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no product in this store.
- `unclear` mgr-how-is-business [own-facade-a2api] 1회차 · `get_sale_analysis_grid_list` `{"to_date": "2026-11-06", "from_date": "2026-10-06", "compare_to": "same_weekday_last_4_weeks"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) same_weekday_last_4_weeks compares periods of 7 days at most; this one has 32. Use previous_period or custom.
- `unclear` mgr-how-is-business [own-facade-a2api] 2회차 · `get_sale_analysis_grid_list` `{"to_date": "2026-11-06", "from_date": "2026-10-06", "compare_to": "same_weekday_last_4_weeks"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) same_weekday_last_4_weeks compares periods of 7 days at most; this one has 32. Use previous_period or custom.
- `model:ungrounded` mgr-how-is-business [own-facade-a2api] 2회차 · `get_member_grade_list` `{"loyalty_program_id": "default"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no program default.
- `unclear` mgr-how-is-business [own-facade-a2api] 3회차 · `get_sale_analysis_grid_list` `{"to_date": "2026-11-06", "from_date": "2026-10-06", "compare_to": "same_weekday_last_4_weeks"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) same_weekday_last_4_weeks compares periods of 7 days at most; this one has 32. Use previous_period or custom.
- `model:ungrounded` mgr-how-is-business [own-facade-a2api] 3회차 · `get_member_grade_list` `{"loyalty_program_id": "default"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no program default.
- `business` mk-category-promotion [own-facade-a2api] 1회차 · `save_promotion_list` `{"rows": [{"ends_at": "2026-11-20T23:59:00-05:00", "starts_at": "2026-11-06T11:00:00-05:00", "applies_to": "category", "row_action": "insert", "category_id": "cat", "promotion_name": "Outerwear $50 of` → UPSTREAM_CONFLICT: The backend reported that the current state does not allow this request. (HTTP 409) Row 1: Promotion type not available on this screen.
- `business` mk-category-promotion [own-facade-a2api] 2회차 · `save_promotion_list` `{"rows": [{"ends_at": "2026-11-20T23:59:00-05:00", "starts_at": "2026-11-06T11:00:00-05:00", "applies_to": "category", "row_action": "insert", "category_id": "cat", "promotion_name": "Outerwear $50 of` → UPSTREAM_CONFLICT: The backend reported that the current state does not allow this request. (HTTP 409) Row 1: Promotion type not available on this screen.
- `business` mk-category-promotion [own-facade-a2api] 3회차 · `save_promotion_list` `{"rows": [{"ends_at": "2026-11-20T23:59:00-05:00", "starts_at": "2026-11-06T11:00:00-05:00", "applies_to": "category", "row_action": "insert", "category_id": "cat", "promotion_name": "Outerwear $50 of` → UPSTREAM_CONFLICT: The backend reported that the current state does not allow this request. (HTTP 409) Row 1: Promotion type not available on this screen.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-a2api] 1회차 · `save_promotion_list` `{"rows": [{"row_action": "update", "promotion_id": "", "promotion_status": "paused"}]}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Row 1: `promotion_id` must look like `promo_…`; got ``.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-a2api] 2회차 · `save_promotion_list` `{"rows": [{"row_action": "update", "promotion_id": "", "promotion_status": "paused"}]}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Row 1: `promotion_id` must look like `promo_…`; got ``.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-a2api] 3회차 · `save_promotion_list` `{"rows": [{"row_action": "update", "promotion_id": "", "promotion_status": "paused"}]}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Row 1: `promotion_id` must look like `promo_…`; got ``.
- `model:described` ops-cancel-delivered [own-facade-a2api] 1회차 · `get_order_detail_popup_init_data` `{"order_id": "20402"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no order 20402.
- `model:described` ops-cancel-delivered [own-facade-a2api] 2회차 · `get_order_detail_popup_init_data` `{"order_id": "20402"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no order 20402.
- `model:described` ops-cancel-delivered [own-facade-a2api] 3회차 · `get_order_detail_popup_init_data` `{"order_id": "20402"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no order 20402.
- `model:described` ops-change-address-in-transit [own-facade-a2api] 1회차 · `get_order_detail_popup_init_data` `{"order_id": "27184"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no order 27184.
- `model:described` ops-change-address-in-transit [own-facade-a2api] 2회차 · `get_order_detail_popup_init_data` `{"order_id": "27184"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no order 27184.
- `model:described` ops-change-address-in-transit [own-facade-a2api] 3회차 · `get_order_detail_popup_init_data` `{"order_id": "27184"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no order 27184.
- `source:undocumented` ops-photo-request [own-facade-a2api] 1회차 · `save_customer_message_send` `{"text": "", "channel": "email", "member_id": "", "message_type": "ask_for_photos"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) The message has no text.
- `unclear` md-how-many-left [own-facade-a2api-lookup] 1회차 · `get_product_detail_info_v2` `{"product_id": ""}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no product in this store.
- `unclear` md-how-many-left [own-facade-a2api-lookup] 2회차 · `get_product_detail_info_v2` `{"product_id": ""}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no product in this store.
- `unclear` md-how-many-left [own-facade-a2api-lookup] 3회차 · `get_product_detail_info_v2` `{"product_id": ""}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no product in this store.
- `unclear` mgr-how-is-business [own-facade-a2api-lookup] 1회차 · `get_sale_analysis_grid_list` `{"to_date": "2026-11-06", "from_date": "2026-10-06", "compare_to": "same_weekday_last_4_weeks"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) same_weekday_last_4_weeks compares periods of 7 days at most; this one has 32. Use previous_period or custom.
- `unclear` mgr-how-is-business [own-facade-a2api-lookup] 2회차 · `get_sale_analysis_grid_list` `{"to_date": "2026-11-06", "from_date": "2026-10-06", "compare_to": "same_weekday_last_4_weeks"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) same_weekday_last_4_weeks compares periods of 7 days at most; this one has 32. Use previous_period or custom.
- `model:ungrounded` mgr-how-is-business [own-facade-a2api-lookup] 2회차 · `get_member_grade_list` `{"loyalty_program_id": "default"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no program default.
- `unclear` mgr-how-is-business [own-facade-a2api-lookup] 3회차 · `get_sale_analysis_grid_list` `{"to_date": "2026-11-06", "from_date": "2026-10-06", "compare_to": "same_weekday_last_4_weeks"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) same_weekday_last_4_weeks compares periods of 7 days at most; this one has 32. Use previous_period or custom.
- `model:ungrounded` mgr-how-is-business [own-facade-a2api-lookup] 3회차 · `get_member_grade_list` `{"loyalty_program_id": "default"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no program default.
- `business` mk-category-promotion [own-facade-a2api-lookup] 1회차 · `save_promotion_list` `{"rows": [{"ends_at": "2026-11-20T23:59:00-05:00", "starts_at": "2026-11-06T11:00:00-05:00", "applies_to": "category", "row_action": "insert", "category_id": "cat", "promotion_name": "Outerwear $50 of` → UPSTREAM_CONFLICT: The backend reported that the current state does not allow this request. (HTTP 409) Row 1: Promotion type not available on this screen.
- `business` mk-category-promotion [own-facade-a2api-lookup] 2회차 · `save_promotion_list` `{"rows": [{"ends_at": "2026-11-20T23:59:00-05:00", "starts_at": "2026-11-06T11:00:00-05:00", "applies_to": "category", "row_action": "insert", "category_id": "cat", "promotion_name": "Outerwear $50 of` → UPSTREAM_CONFLICT: The backend reported that the current state does not allow this request. (HTTP 409) Row 1: Promotion type not available on this screen.
- `business` mk-category-promotion [own-facade-a2api-lookup] 3회차 · `save_promotion_list` `{"rows": [{"ends_at": "2026-11-20T23:59:00-05:00", "starts_at": "2026-11-06T11:00:00-05:00", "applies_to": "category", "row_action": "insert", "category_id": "cat", "promotion_name": "Outerwear $50 of` → UPSTREAM_CONFLICT: The backend reported that the current state does not allow this request. (HTTP 409) Row 1: Promotion type not available on this screen.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-a2api-lookup] 1회차 · `save_promotion_list` `{"rows": [{"row_action": "update", "promotion_id": "", "promotion_status": "paused"}]}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Row 1: `promotion_id` must look like `promo_…`; got ``.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-a2api-lookup] 2회차 · `save_promotion_list` `{"rows": [{"row_action": "update", "promotion_id": "", "promotion_status": "paused"}]}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Row 1: `promotion_id` must look like `promo_…`; got ``.
- `source:undocumented` mk-pause-knit-until-monday [own-facade-a2api-lookup] 3회차 · `save_promotion_list` `{"rows": [{"row_action": "update", "promotion_id": "", "promotion_status": "paused"}]}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Row 1: `promotion_id` must look like `promo_…`; got ``.
- `source:undocumented` ops-photo-request [own-facade-a2api-lookup] 1회차 · `save_customer_message_send` `{"text": "", "channel": "email", "member_id": "", "message_type": "ask_for_photos"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) The message has no text.
- `model:described` md-broken-sizes-outerwear [own-acom] 3회차 · `get_inventory` `{"fields": ["variant_id[]"], "product_id": "prd_rain_parka"}` → UPSTREAM_VALIDATION_FAILED: `fields` names `variant_id[]` this result does not have. Its top-level fields are availability, inventory_level, product_id, reorders, variants. Name some of those, or leave `fields` out to get all of them.
- `model:ungrounded` md-out-of-stock-30-days [own-acom] 1회차 · `get_product` `{"product_id": "prd_1"}` → RESOURCE_NOT_FOUND: There is no product prd_1 in this store.
- `model:ungrounded` md-out-of-stock-30-days [own-acom] 2회차 · `get_product` `{"product_id": "prd_1"}` → RESOURCE_NOT_FOUND: There is no product prd_1 in this store.
- `model:ungrounded` md-out-of-stock-30-days [own-acom] 2회차 · `get_product` `{"product_id": "prd_1"}` → RESOURCE_NOT_FOUND: There is no product prd_1 in this store.
- `model:ungrounded` md-out-of-stock-30-days [own-acom] 2회차 · `get_product` `{"product_id": "prd_1"}` → RESOURCE_NOT_FOUND: There is no product prd_1 in this store.
- `model:ungrounded` md-out-of-stock-30-days [own-acom] 3회차 · `get_product` `{"product_id": "prd_1"}` → RESOURCE_NOT_FOUND: There is no product prd_1 in this store.
- `model:ungrounded` md-out-of-stock-30-days [own-acom] 3회차 · `get_product` `{"product_id": "prd_1"}` → RESOURCE_NOT_FOUND: There is no product prd_1 in this store.
- `model:ungrounded` md-out-of-stock-30-days [own-acom] 3회차 · `get_product` `{"product_id": "prd_1"}` → RESOURCE_NOT_FOUND: There is no product prd_1 in this store.
- `model:ungrounded` ops-cancel-delivered [own-acom] 1회차 · `get_order` `{"fields": ["id", "order_number", "order_status", "order_date", "customer_id", "ordered_item", "delivery", "payment", "totals", "claims"], "order_id": "1"}` → RESOURCE_NOT_FOUND: No order has the number 1.
- `model:ungrounded` ops-cancel-delivered [own-acom] 2회차 · `get_order` `{"fields": ["id", "order_number", "order_status", "order_date", "customer_id", "ordered_item", "delivery", "payment", "totals", "claims"], "order_id": "1"}` → RESOURCE_NOT_FOUND: No order has the number 1.
- `model:described` ops-cancel-delivered [own-acom] 3회차 · `track_shipment` `{"mode": "delivery", "limit": 20}` → UPSTREAM_VALIDATION_FAILED: mode delivery needs delivery_id.
- `model:described` ops-change-address-in-transit [own-acom] 1회차 · `track_shipment` `{"mode": "delivery"}` → UPSTREAM_VALIDATION_FAILED: mode delivery needs delivery_id.
- `model:ungrounded` ops-change-address-in-transit [own-acom] 1회차 · `get_delivery_dates` `{"address_id": "adr_m005474", "product_id": "prd_outerwear_01", "variant_id": "var_outerwear_01_xl_stone", "address_mode": "saved"}` → RESOURCE_NOT_FOUND: There is no saved address adr_m005474.
- `model:described` ops-change-address-in-transit [own-acom] 2회차 · `track_shipment` `{"mode": "delivery"}` → UPSTREAM_VALIDATION_FAILED: mode delivery needs delivery_id.
- `model:described` ops-change-address-in-transit [own-acom] 3회차 · `track_shipment` `{"mode": "delivery"}` → UPSTREAM_VALIDATION_FAILED: mode delivery needs delivery_id.
- `unclear` ops-photo-request [own-acom] 1회차 · `search_claims` `{"claim_type": "return"}` → UNKNOWN: The arguments for search_claims are not usable: order_id needs a ord_ id; "ord_" names none..
- `unclear` ops-photo-request [own-acom] 2회차 · `search_claims` `{"claim_type": "return"}` → UNKNOWN: The arguments for search_claims are not usable: order_id needs a ord_ id; "ord_" names none..
- `unclear` ops-photo-request [own-acom] 3회차 · `search_claims` `{"claim_type": "return"}` → UNKNOWN: The arguments for search_claims are not usable: order_id needs a ord_ id; "ord_" names none..

## 기대와 다른 쓰기 입력

- mk-pause-knit-until-monday [own-acom] 1회차 · `pause_promotion` 기대 {"promotion_id": "promo_autumn_knit"} · 불일치: [{"promotion_id": null}]
- mk-pause-knit-until-monday [own-acom] 2회차 · `pause_promotion` 기대 {"promotion_id": "promo_autumn_knit"} · 불일치: [{"promotion_id": null}]
- mk-pause-knit-until-monday [own-acom] 3회차 · `pause_promotion` 기대 {"promotion_id": "promo_autumn_knit"} · 불일치: [{"promotion_id": null}]
- ops-photo-request [own-acom] 1회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": null}]
- ops-photo-request [own-acom] 2회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": null}]
- ops-photo-request [own-acom] 3회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": null}]
