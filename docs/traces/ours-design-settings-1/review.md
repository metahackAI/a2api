# 호출 단계 리뷰 — ours-design-settings-1

판정 기준 함수 정의: `ours-design-settings-1.functions.json`(실행 때 모델이 본 것)

단계: A0 API에 해당 기능 없음 · A 필요한 함수를 받지 못함 · B 받았지만 부르지 않음 · C 불렀지만 성공 못 함 · D-before 필요한 함수를 부르기 전 한도·오류로 중단 · D-after 필요한 함수는 모두 성공했는데 답하기 전 한도로 중단 · E-write 쓰기 입력·change set · E-format 숫자는 있으나 표기 · E-content 답 내용 누락

## 필요한 함수: 확보 → 호출 → 성공

| 방식 | 통과 | 필요한 함수(API에 있음/전체) | 모델에게 줌 | 불렀음 | 성공 | 확보 기록 |
|---|---|---|---|---|---|---|
| a2api-acom | 12/24 | 42/42 | 40/42 (95%) | 31/42 (74%) | 31/42 (74%) | 단계별 기록 |
| a2api-acom-names-batch | 15/24 | 42/42 | 35/42 (83%) | 35/42 (83%) | 35/42 (83%) | 단계별 기록 |
| facade-all | 2/24 | 28/42 | 28/28 (100%) | 22/28 (79%) | 20/28 (71%) | 단계별 기록 |
| a2api-facade-all | 4/24 | 28/42 | 28/28 (100%) | 24/28 (86%) | 24/28 (86%) | 단계별 기록 |

## 실패한 실행이 처음 막힌 단계

| 방식 | passed | A0 | A | B | C | D-before | D-after | E-write | E-format | E-content |
|---|---|---|---|---|---|---|---|---|---|---|
| a2api-acom | 12 | 0 | 2 | 1 | 0 | 4 | 1 | 0 | 2 | 2 |
| a2api-acom-names-batch | 15 | 0 | 4 | 0 | 0 | 0 | 1 | 0 | 1 | 3 |
| facade-all | 2 | 13 | 0 | 0 | 1 | 2 | 6 | 0 | 0 | 0 |
| a2api-facade-all | 4 | 13 | 0 | 0 | 0 | 2 | 5 | 0 | 0 | 0 |

## 실패한 업무 호출의 원인

| 방식 | 업무 호출 | 실패 | model:schema | model:function | model:ungrounded | model:described | source:undocumented | business | unclear |
|---|---|---|---|---|---|---|---|---|---|
| a2api-acom | 121 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| a2api-acom-names-batch | 152 | 6 | 0 | 0 | 0 | 0 | 0 | 3 | 3 |
| facade-all | 283 | 153 | 86 | 0 | 12 | 0 | 45 | 3 | 7 |
| a2api-facade-all | 207 | 11 | 0 | 0 | 4 | 1 | 6 | 0 | 0 |

## 쓰기 입력(과업이 기대한 change set 항목)

| 방식 | 기대 항목 | 불렀음 | 입력 일치 |
|---|---|---|---|
| a2api-acom | 12 | 4 | 4 |
| a2api-acom-names-batch | 12 | 6 | 6 |

## 실패한 호출 목록

- `source:undocumented` b1-vip-weekend-sale [facade-all] 1회차 · `getPrdGridList` `{"srchKwd": "summer outerwear", "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b1-vip-weekend-sale [facade-all] 1회차 · `getDispCornerList` `{"dispPageCd": "01", "strtDtm": "2026-11-07 00:00:00", "endDtm": "2026-11-08 23:59:59"}` → UPSTREAM_VALIDATION_FAILED: `2026-11-07 00:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `source:undocumented` b1-vip-weekend-sale [facade-all] 1회차 · `savePrmtList` `{"rows": [{"rowStat": "U", "prmtNo": "promo_01m6cx0x549vf1y3ah27kz9tew", "aplyTgtCd": "P", "prdNoList": ["prd_summer_outerwear_22", "prd_summer_outerwear_33", "prd_summer_outerwear_32", "prd_summer_ou` → UPSTREAM_VALIDATION_FAILED: Row 1: `prmtStatCd` is required.
- `business` b1-vip-weekend-sale [facade-all] 1회차 · `savePrmtList` `{"rows": [{"rowStat": "U", "prmtNo": "promo_01m6cx0x549vf1y3ah27kz9tew", "prmtStatCd": "10", "aplyTgtCd": "P", "prdNoList": ["prd_summer_outerwear_22", "prd_summer_outerwear_33", "prd_summer_outerwear` → UPSTREAM_CONFLICT: Row 1: Status change not available on this screen.
- `source:undocumented` b1-vip-weekend-sale [facade-all] 1회차 · `savePrmtList` `{"rows": [{"rowStat": "U", "prmtNo": "promo_01m6cx0x549vf1y3ah27kz9tew", "aplyTgtCd": "P", "prdNoList": ["prd_summer_outerwear_22", "prd_summer_outerwear_33", "prd_summer_outerwear_32", "prd_summer_ou` → UPSTREAM_VALIDATION_FAILED: Row 1: `prmtStatCd` is required.
- `business` b1-vip-weekend-sale [facade-all] 1회차 · `saveDispBnrList` `{"rows": [{"rowStat": "U", "cornerNo": "slot_home_hero", "tgtMbrGrdCd": "G03", "strtDtm": "2026-11-07T00:00:00-05:00", "endDtm": "2026-11-08T23:59:59-05:00", "bnrSubTitl": "VIP Weekend Exclusive", "bn` → UPSTREAM_CONFLICT: Row 1: Row status not available on this screen.
- `business` b1-vip-weekend-sale [facade-all] 1회차 · `saveDispBnrList` `{"rows": [{"rowStat": "D", "cornerNo": "slot_home_hero", "tgtMbrGrdCd": "G03", "strtDtm": "2026-11-07T00:00:00-05:00", "endDtm": "2026-11-08T23:59:59-05:00", "bnrTitl": "20% Off Summer Outerwear"}]}` → UPSTREAM_CONFLICT: Row 1: Row status not available on this screen.
- `unclear` b1-vip-weekend-sale [facade-all] 1회차 · `saveDispBnrList` `{"rows": [{"rowStat": "I", "cornerNo": "slot_home_hero", "tgtMbrGrdCd": "G03", "strtDtm": "2026-11-07T00:00:00-05:00", "endDtm": "2026-11-08T23:59:59-05:00", "bnrSubTitl": "VIP Weekend Exclusive", "bn` → UPSTREAM_VALIDATION_FAILED: Row 1: dsp_01m6cx1752tk3km2tmpmp78me0 now holds the slot for vip.
- `source:undocumented` b1-vip-weekend-sale [a2api-facade-all] 1회차 · `facade_get_display_corner_list` `{"page_type": "main", "starts_at": "2026-11-07 00:00:00", "ends_at": "2026-11-08 23:59:59"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) `2026-11-07 00:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `model:schema` mk-whats-running-this-weekend [facade-all] 1회차 · `getPrmtGridList` `{"prmtStatCd": 10, "srchStrtDtm": "2026-11-07 00:00:00", "srchEndDtm": "2026-11-08 23:59:59", "pageNo": 0, "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mk-whats-running-this-weekend [facade-all] 1회차 · `getPrmtGridList` `{"prmtStatCd": 10, "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mk-whats-running-this-weekend [facade-all] 1회차 · `getPrmtGridList` `{"prmtStatCd": 10, "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mk-whats-running-this-weekend [facade-all] 1회차 · `getPrmtGridListCnt` `{"prmtStatCd": 10, "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mk-whats-running-this-weekend [facade-all] 1회차 · `getPrmtGridList` `{"prmtStatCd": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `source:undocumented` mk-whats-running-this-weekend [facade-all] 1회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:schema` mk-whats-running-this-weekend [facade-all] 1회차 · `getPrmtGridList` `{"prmtStatCd": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `source:undocumented` mk-hero-free-next-weekend [facade-all] 1회차 · `getDispCornerList` `{"dispPageCd": "01", "strtDtm": "2026-11-07 00:00:00", "endDtm": "2026-11-08 23:59:59", "cornerTpCd": "H"}` → UPSTREAM_VALIDATION_FAILED: `2026-11-07 00:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `model:schema` mk-hero-free-next-weekend [facade-all] 1회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-hero-free-next-weekend [facade-all] 1회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:ungrounded` mk-hero-free-next-weekend [facade-all] 1회차 · `getMbrGrdList` `{"prgmNo": "DEFAULT"}` → RESOURCE_NOT_FOUND: There is no program DEFAULT.
- `source:undocumented` mk-hero-free-next-weekend [facade-all] 1회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-hero-free-next-weekend [facade-all] 1회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 5}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-hero-free-next-weekend [facade-all] 1회차 · `getPrmtTgtMbrList` `{"mbrGrdCd": "G01", "pageNo": 0, "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `business` md-low-stock-before-weekend [a2api-acom-names-batch] 1회차 · `get_inventory` `{"product_id": "prd_accessories_08"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `source:undocumented` md-low-stock-before-weekend [facade-all] 1회차 · `getPrdGridList` `{"stkQtyFrom": 0, "stkQtyTo": 5, "pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:schema` md-low-stock-before-weekend [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-30", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-low-stock-before-weekend [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261030, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `business` md-overcoat-runs-small [a2api-acom-names-batch] 1회차 · `get_review_summary` `{"product_id": "prd_wool_overcoat", "size": "S", "sample_limit": 3}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) No reviews match these conditions; widen the height range or size. Next: get_product_measurements.
- `business` md-overcoat-runs-small [a2api-acom-names-batch] 1회차 · `get_review_summary` `{"product_id": "prd_wool_overcoat", "size": "XL", "sample_limit": 3}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) No reviews match these conditions; widen the height range or size. Next: get_product_measurements.
- `source:undocumented` md-overcoat-runs-small [facade-all] 1회차 · `getPrdGridList` `{"srchKwd": "wool overcoat", "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-overcoat-runs-small [facade-all] 1회차 · `getPrdGridList` `{"srchKwd": "overcoat", "pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:schema` md-overcoat-runs-small [facade-all] 1회차 · `getClmGridList` `{"clmRsnCd": 11, "pageNo": 1, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-overcoat-runs-small [facade-all] 1회차 · `getClmGridList` `{"clmRsnCd": 11, "pageNo": 1, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `source:undocumented` md-end-of-season-markdown [facade-all] 1회차 · `getPrdGridList` `{"srchKwd": "tee", "pageNo": 0, "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-end-of-season-markdown [facade-all] 1회차 · `savePrmtList` `{"rows": [{"rowStat": "I", "prmtNm": "End of Season Tees Markdown", "prmtTpCd": "T01", "prmtStatCd": "10", "tgtMbrGrdCd": "", "strtDtm": "20261106110000", "endDtm": "20261115235959", "aplyTgtCd": "P",` → UPSTREAM_VALIDATION_FAILED: Row 1: `20261106110000` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `source:undocumented` md-end-of-season-markdown [a2api-facade-all] 1회차 · `facade_save_promotion_list` `{"rows": [{"row_action": "insert", "promotion_name": "End of Season Tees Markdown", "promotion_type": "item_price_everyone", "promotion_status": "running", "starts_at": "2026-11-06 11:00:00", "ends_at` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Row 1: `2026-11-06 11:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `source:undocumented` b2-returns-over-200 [facade-all] 1회차 · `getClmGridList` `{"clmAmtFrom": 200.0, "pageNo": 0, "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:described` ops-wismo-tracking-stuck [a2api-facade-all] 1회차 · `facade_get_order_detail_popup_init_data` `{"order_id": 27184}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no order 27184.
- `model:schema` ops-wismo-tracking-stuck [facade-all] 1회차 · `getOrdDtlPopInitData` `{"ordNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-wismo-tracking-stuck [facade-all] 1회차 · `getOrdDtlPopInitData` `{"ordNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-wismo-tracking-stuck [facade-all] 1회차 · `getOrdGridList` `{"srchKwd": 27184, "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-wismo-tracking-stuck [facade-all] 1회차 · `getOrdGridList` `{"srchKwd": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:ungrounded` ops-wismo-tracking-stuck [facade-all] 1회차 · `getOrdDtlPopInitData` `{"ordNo": "ORD27184"}` → RESOURCE_NOT_FOUND: There is no order ORD27184.
- `model:schema` ops-wismo-tracking-stuck [facade-all] 1회차 · `getOrdGridListCnt` `{"srchKwd": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `source:undocumented` ops-wismo-tracking-stuck [facade-all] 1회차 · `getOrdGridList` `{"srchKwd": "order 27184", "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:schema` ops-wismo-tracking-stuck [facade-all] 1회차 · `getOrdGridList` `{"srchKwd": 27184, "pageNo": 1, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-frequent-returner [facade-all] 1회차 · `getOrdGridList` `{"mbrNo": 20431, "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-frequent-returner [facade-all] 1회차 · `getOrdGridList` `{"mbrNo": 20431}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-frequent-returner [facade-all] 1회차 · `getOrdGridList` `{"srchKwd": 20431, "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-frequent-returner [facade-all] 1회차 · `getOrdGridList` `{"srchKwd": 20431}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-frequent-returner [facade-all] 1회차 · `getOrdDtlPopInitData` `{"ordNo": 20431}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-frequent-returner [facade-all] 1회차 · `getPrmtTgtMbrList` `{"srchKwd": 20431, "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-frequent-returner [facade-all] 1회차 · `getOrdGridList` `{"mbrNo": 20431, "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-frequent-returner [facade-all] 1회차 · `getOrdGridList` `{"mbrNo": 20431, "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-frequent-returner [facade-all] 1회차 · `getOrdGridList` `{"mbrNo": 20431, "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:ungrounded` ops-frequent-returner [facade-all] 1회차 · `getOrdDtlPopInitData` `{"ordNo": "020431"}` → RESOURCE_NOT_FOUND: There is no order 020431.
- `model:schema` ops-frequent-returner [facade-all] 1회차 · `getOrdDtlPopInitData` `{"ordNo": 20431}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:ungrounded` ops-frequent-returner [facade-all] 1회차 · `getOrdDtlPopInitData` `{"ordNo": "20431a"}` → RESOURCE_NOT_FOUND: There is no order 20431a.
- `model:schema` mgr-what-needs-me-today [facade-all] 1회차 · `getOrdGridListCnt` `{"ordStatCd": 10, "ordDtmFrom": "2026-11-06", "ordDtmTo": "2026-11-06", "pageNo": 0, "pageSize": 0}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-what-needs-me-today [facade-all] 1회차 · `getOrdGridListCnt` `{"ordStatCd": 10, "ordDtmFrom": "2026-11-06", "ordDtmTo": "2026-11-06"}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-what-needs-me-today [facade-all] 1회차 · `getOrdGridListCnt` `{"ordStatCd": 10, "ordDtmFrom": "2026-11-06 00:00:00", "ordDtmTo": "2026-11-06 23:59:59"}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-what-needs-me-today [facade-all] 1회차 · `getOrdGridList` `{"ordStatCd": 10, "ordDtmFrom": "2026-11-06 00:00:00", "ordDtmTo": "2026-11-06 23:59:59", "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `source:undocumented` mgr-what-needs-me-today [facade-all] 1회차 · `getOrdGridList` `{"ordDtmFrom": "2026-11-06 00:00:00", "ordDtmTo": "2026-11-06 23:59:59", "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mgr-what-needs-me-today [facade-all] 1회차 · `getOrdGridList` `{"ordDtmFrom": "2026-11-06 00:00:00", "ordDtmTo": "2026-11-06 23:59:59", "pageNo": 1, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: `2026-11-06 00:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `model:schema` mgr-what-needs-me-today [facade-all] 1회차 · `getOrdGridList` `{"ordStatCd": 30, "ordDtmFrom": "2026-11-06T00:00:00", "ordDtmTo": "2026-11-06T23:59:59", "pageNo": 1, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-what-needs-me-today [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-06", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-what-needs-me-today [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261106, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `source:undocumented` mgr-what-changed-this-morning [facade-all] 1회차 · `getPrmtGridList` `{"srchStrtDtm": "2026-11-06 00:00:00", "srchEndDtm": "2026-11-06 11:00:00", "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mgr-what-changed-this-morning [facade-all] 1회차 · `getPrmtGridList` `{"srchStrtDtm": "2026-11-06 00:00:00", "srchEndDtm": "2026-11-06 11:00:00", "pageNo": 1, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: `2026-11-06 00:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `source:undocumented` mgr-what-changed-this-morning [facade-all] 1회차 · `getPrmtGridList` `{"srchStrtDtm": "2026-11-06T00:00:00-05:00", "srchEndDtm": "2026-11-06T11:00:00-05:00", "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:ungrounded` mgr-what-changed-this-morning [facade-all] 1회차 · `getDispCornerList` `{"dispPageCd": "02", "strtDtm": "2026-11-06T00:00:00-05:00", "endDtm": "2026-11-06T11:00:00-05:00"}` → RESOURCE_NOT_FOUND: The category page has no display slots.
- `model:ungrounded` mgr-what-changed-this-morning [facade-all] 1회차 · `getDispCornerList` `{"dispPageCd": "03", "strtDtm": "2026-11-06T00:00:00-05:00", "endDtm": "2026-11-06T11:00:00-05:00"}` → RESOURCE_NOT_FOUND: The product page has no display slots.
- `model:ungrounded` mgr-what-changed-this-morning [facade-all] 1회차 · `getDispCornerList` `{"dispPageCd": "04", "strtDtm": "2026-11-06T00:00:00-05:00", "endDtm": "2026-11-06T11:00:00-05:00"}` → RESOURCE_NOT_FOUND: The search page has no display slots.
- `model:schema` mgr-what-changed-this-morning [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-06", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:ungrounded` mgr-what-changed-this-morning [a2api-facade-all] 1회차 · `facade_get_display_corner_list` `{"page_type": "category", "starts_at": "2026-11-06T00:00:00-04:00", "ends_at": "2026-11-06T23:59:59-04:00"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) The category page has no display slots.
- `model:schema` b3-why-sales-dropped [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-05", "srchEndDt": "2026-11-05", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` b3-why-sales-dropped [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261105, "srchEndDt": 20261105, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `source:undocumented` b3-why-sales-dropped [facade-all] 1회차 · `getOrdGridListCnt` `{"ordDtmFrom": "2026-11-05 00:00:00", "ordDtmTo": "2026-11-05 23:59:59", "pageNo": 0, "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: `2026-11-05 00:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `model:schema` b3-why-sales-dropped [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-05", "srchEndDt": "2026-11-05", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` b3-why-sales-dropped [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261105, "srchEndDt": 20261105, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` b3-why-sales-dropped [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-05", "srchEndDt": "2026-11-05", "cmprBaseCd": 2}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` b3-why-sales-dropped [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-05T00:00:00", "srchEndDt": "2026-11-05T23:59:59", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `source:undocumented` b3-why-sales-dropped [facade-all] 1회차 · `getPrmtGridList` `{"srchStrtDtm": "2026-11-04T00:00:00", "srchEndDtm": "2026-11-04T23:59:59", "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b3-why-sales-dropped [facade-all] 1회차 · `getPrmtGridList` `{"srchStrtDtm": "2026-11-04T00:00", "srchEndDtm": "2026-11-04T23:59", "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b1-vip-weekend-sale [facade-all] 2회차 · `getPrdGridList` `{"srchKwd": "summer outerwear", "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `unclear` b1-vip-weekend-sale [facade-all] 2회차 · `getMbrGrdList` `{"prgmNo": ""}` → RESOURCE_NOT_FOUND: There is no program .
- `model:schema` b1-vip-weekend-sale [facade-all] 2회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` b1-vip-weekend-sale [facade-all] 2회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `unclear` b1-vip-weekend-sale [facade-all] 2회차 · `getPrmtTgtMbrList` `{"mbrGrdCd": "04", "pageNo": 1, "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid member grade code.
- `unclear` b1-vip-weekend-sale [facade-all] 2회차 · `getPrmtTgtMbrList` `{"mbrGrdCd": "G04", "pageNo": 1, "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid member grade code.
- `source:undocumented` b1-vip-weekend-sale [a2api-facade-all] 2회차 · `facade_get_display_corner_list` `{"page_type": "main", "starts_at": "2026-11-07 00:00:00", "ends_at": "2026-11-08 23:59:59"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) `2026-11-07 00:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `source:undocumented` mk-whats-running-this-weekend [facade-all] 2회차 · `getPrmtGridList` `{"prmtNm": "knit", "pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-whats-running-this-weekend [facade-all] 2회차 · `getPrmtGridList` `{"prmtNm": "knit", "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-whats-running-this-weekend [facade-all] 2회차 · `getPrmtGridList` `{"srchStrtDtm": "2026-11-07 00:00:00", "srchEndDtm": "2026-11-08 23:59:59", "pageNo": 1, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: `2026-11-07 00:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `source:undocumented` mk-whats-running-this-weekend [a2api-facade-all] 2회차 · `facade_get_promotion_grid_list` `{"promotion_status": "running", "active_from": "2026-11-07 00:00:00", "active_until": "2026-11-08 23:59:59", "page": 1, "page_size": 100}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) `2026-11-07 00:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `source:undocumented` mk-hero-free-next-weekend [a2api-facade-all] 2회차 · `facade_get_display_corner_list` `{"page_type": "main", "starts_at": "2026-11-14 00:00:00", "ends_at": "2026-11-15 23:59:59", "corner_type": "hero"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) `2026-11-14 00:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `model:schema` mk-hero-free-next-weekend [facade-all] 2회차 · `getDispCornerList` `{"dispPageCd": "01", "strtDtm": 20261114000000, "endDtm": 20261115235959, "cornerTpCd": "H"}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `source:undocumented` mk-hero-free-next-weekend [facade-all] 2회차 · `getDispCornerList` `{"dispPageCd": "01", "strtDtm": "2026-11-14 00:00:00", "endDtm": "2026-11-15 23:59:59", "cornerTpCd": "H"}` → UPSTREAM_VALIDATION_FAILED: `2026-11-14 00:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `unclear` mk-hero-free-next-weekend [facade-all] 2회차 · `getMbrGrdList` `{"prgmNo": ""}` → RESOURCE_NOT_FOUND: There is no program .
- `source:undocumented` mk-hero-free-next-weekend [facade-all] 2회차 · `getPrmtGridList` `{"prmtNm": "VIP", "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:ungrounded` mk-hero-free-next-weekend [facade-all] 2회차 · `getMbrGrdList` `{"prgmNo": "01"}` → RESOURCE_NOT_FOUND: There is no program 01.
- `source:undocumented` mk-hero-free-next-weekend [facade-all] 2회차 · `getPrmtTgtMbrList` `{"mbrGrdCd": "G01", "pageNo": 0, "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `unclear` mk-hero-free-next-weekend [facade-all] 2회차 · `getPrmtTgtMbrList` `{"mbrGrdCd": "G04", "pageNo": 1, "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid member grade code.
- `model:schema` md-low-stock-before-weekend [facade-all] 2회차 · `getPrdGridListCnt` `{"stkQtyFrom": 0, "stkQtyTo": 5, "sellStatCd": 10, "pageNo": 0, "pageSize": 0}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-low-stock-before-weekend [facade-all] 2회차 · `getPrdGridListCnt` `{"stkQtyFrom": 0, "stkQtyTo": 5, "sellStatCd": 10, "pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-low-stock-before-weekend [facade-all] 2회차 · `getPrdGridList` `{"sellStatCd": 10, "pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-low-stock-before-weekend [facade-all] 2회차 · `getPrdGridList` `{"sellStatCd": 10, "pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-low-stock-before-weekend [facade-all] 2회차 · `getPrdGridList` `{"sellStatCd": 10, "pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-low-stock-before-weekend [facade-all] 2회차 · `getPrdGridList` `{"sellStatCd": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-low-stock-before-weekend [facade-all] 2회차 · `getPrdGridList` `{"sellStatCd": 10, "pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-low-stock-before-weekend [facade-all] 2회차 · `getPrdGridList` `{"sellStatCd": 10, "srchKwd": ""}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-low-stock-before-weekend [facade-all] 2회차 · `getPrdGridListCnt` `{"sellStatCd": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:ungrounded` md-low-stock-before-weekend [facade-all] 2회차 · `getPrdDtlInfo` `{"prdNo": "P000001"}` → RESOURCE_NOT_FOUND: There is no product P000001 in this store.
- `unclear` md-overcoat-runs-small [a2api-acom-names-batch] 2회차 · `get_product_measurements` `{"product_id": "prd_wool_overcoat", "sizes": ["S", "M", "L", "XL"]}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) The size chart has no size S. Next: get_product.
- `unclear` md-overcoat-runs-small [a2api-acom-names-batch] 2회차 · `get_product_measurements` `{"product_id": "prd_wool_overcoat", "sizes": ["XL"]}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) The size chart has no size XL. Next: get_product.
- `source:undocumented` md-overcoat-runs-small [facade-all] 2회차 · `getPrdGridList` `{"srchKwd": "wool overcoat", "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:schema` md-overcoat-runs-small [facade-all] 2회차 · `getClmGridList` `{"clmRsnCd": 11, "pageNo": 1, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-overcoat-runs-small [facade-all] 2회차 · `getClmGridList` `{"clmRsnCd": 11, "pageNo": 1, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-overcoat-runs-small [facade-all] 2회차 · `getClmGridListCnt` `{"clmRsnCd": 11, "pageNo": 1, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-overcoat-runs-small [facade-all] 2회차 · `getClmGridList` `{"clmStatCd": "R10", "clmRsnCd": 11, "pageNo": 1, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `source:undocumented` md-end-of-season-markdown [facade-all] 2회차 · `getPrdGridList` `{"srchKwd": "tee", "pageNo": 0, "pageSize": 61}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-end-of-season-markdown [facade-all] 2회차 · `getPrdGridList` `{"srchKwd": "tee", "pageNo": 0, "pageSize": 50}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-end-of-season-markdown [facade-all] 2회차 · `getPrdGridList` `{"srchKwd": "tee", "pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `unclear` md-end-of-season-markdown [facade-all] 2회차 · `getMbrGrdList` `{"prgmNo": ""}` → RESOURCE_NOT_FOUND: There is no program .
- `source:undocumented` md-end-of-season-markdown [facade-all] 2회차 · `savePrmtList` `{"rows": [{"rowStat": "I", "prmtNm": "End of Season Tees Markdown", "prmtTpCd": "T01", "prmtStatCd": "10", "tgtMbrGrdCd": "", "strtDtm": "2026-11-06 11:00:00", "endDtm": "2026-11-15 23:59:59", "aplyTg` → UPSTREAM_VALIDATION_FAILED: Row 1: `2026-11-06 11:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `source:undocumented` b2-returns-over-200 [facade-all] 2회차 · `getClmGridList` `{"clmAmtFrom": 200.0, "pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b2-returns-over-200 [facade-all] 2회차 · `getClmGridList` `{"clmAmtFrom": 200.0, "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:schema` ops-wismo-tracking-stuck [facade-all] 2회차 · `getOrdDtlPopInitData` `{"ordNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-wismo-tracking-stuck [facade-all] 2회차 · `getOrdGridList` `{"srchKwd": 27184, "pageNo": 0, "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-wismo-tracking-stuck [facade-all] 2회차 · `getOrdGridList` `{"srchKwd": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-wismo-tracking-stuck [facade-all] 2회차 · `getOrdGridList` `{"srchKwd": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-frequent-returner [facade-all] 2회차 · `getOrdDtlPopInitData` `{"ordNo": 20431}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-frequent-returner [facade-all] 2회차 · `getOrdDtlPopInitData` `{"ordNo": 20431}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-frequent-returner [facade-all] 2회차 · `getOrdGridList` `{"srchKwd": 20431, "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-frequent-returner [facade-all] 2회차 · `getOrdGridList` `{"mbrNo": 20431, "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-frequent-returner [facade-all] 2회차 · `getOrdGridListCnt` `{"mbrNo": 20431, "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-frequent-returner [facade-all] 2회차 · `getOrdGridList` `{"ordStatCd": 10, "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `source:undocumented` ops-frequent-returner [facade-all] 2회차 · `getOrdGridList` `{"pageNo": 0, "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:schema` ops-frequent-returner [facade-all] 2회차 · `getOrdGridList` `{"srchKwd": 20431, "pageNo": 1, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mgr-what-needs-me-today [facade-all] 2회차 · `getOrdGridListCnt` `{"ordDtmFrom": 20261106, "ordDtmTo": 20261106, "pageNo": 0, "pageSize": 0}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mgr-what-needs-me-today [facade-all] 2회차 · `getOrdGridListCnt` `{"ordDtmFrom": 20261106, "ordDtmTo": 20261106, "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mgr-what-needs-me-today [facade-all] 2회차 · `getOrdGridListCnt` `{"ordDtmFrom": 20261106, "ordDtmTo": 20261106}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `source:undocumented` mgr-what-needs-me-today [facade-all] 2회차 · `getOrdGridList` `{"ordDtmFrom": "2026-11-06", "ordDtmTo": "2026-11-06", "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:schema` mgr-what-needs-me-today [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-06", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-what-needs-me-today [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261106, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mgr-what-needs-me-today [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-06", "srchEndDt": "2026-11-06", "cmprBaseCd": 2}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `source:undocumented` mgr-what-changed-this-morning [a2api-facade-all] 2회차 · `facade_get_display_corner_list` `{"page_type": "main", "starts_at": "2026-11-06 00:00:00", "ends_at": "2026-11-06 12:00:00"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) `2026-11-06 00:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `model:ungrounded` mgr-what-changed-this-morning [a2api-facade-all] 2회차 · `facade_get_display_corner_list` `{"page_type": "category", "starts_at": "2026-11-06T00:00:00-05:00", "ends_at": "2026-11-06T12:00:00-05:00"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) The category page has no display slots.
- `model:ungrounded` mgr-what-changed-this-morning [a2api-facade-all] 2회차 · `facade_get_display_corner_list` `{"page_type": "product", "starts_at": "2026-11-06T00:00:00-05:00", "ends_at": "2026-11-06T12:00:00-05:00"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) The product page has no display slots.
- `model:ungrounded` mgr-what-changed-this-morning [a2api-facade-all] 2회차 · `facade_get_display_corner_list` `{"page_type": "search", "starts_at": "2026-11-06T00:00:00-05:00", "ends_at": "2026-11-06T12:00:00-05:00"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) The search page has no display slots.
- `source:undocumented` mgr-what-changed-this-morning [facade-all] 2회차 · `getPrmtGridList` `{"srchStrtDtm": "2026-11-06 00:00:00", "srchEndDtm": "2026-11-06 23:59:59", "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mgr-what-changed-this-morning [facade-all] 2회차 · `getPrmtGridList` `{"srchStrtDtm": "2026-11-06 00:00:00", "srchEndDtm": "2026-11-06 23:59:59", "pageNo": 1, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: `2026-11-06 00:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `model:ungrounded` mgr-what-changed-this-morning [facade-all] 2회차 · `getDispCornerList` `{"dispPageCd": "02", "strtDtm": "2026-11-06T00:00:00", "endDtm": "2026-11-06T23:59:59"}` → RESOURCE_NOT_FOUND: The category page has no display slots.
- `model:ungrounded` mgr-what-changed-this-morning [facade-all] 2회차 · `getDispCornerList` `{"dispPageCd": "03", "strtDtm": "2026-11-06T00:00:00", "endDtm": "2026-11-06T23:59:59"}` → RESOURCE_NOT_FOUND: The product page has no display slots.
- `model:ungrounded` mgr-what-changed-this-morning [facade-all] 2회차 · `getDispCornerList` `{"dispPageCd": "04", "strtDtm": "2026-11-06T00:00:00", "endDtm": "2026-11-06T23:59:59"}` → RESOURCE_NOT_FOUND: The search page has no display slots.
- `source:undocumented` mgr-what-changed-this-morning [facade-all] 2회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:schema` mgr-what-changed-this-morning [facade-all] 2회차 · `getPrmtGridList` `{"prmtStatCd": 20, "srchStrtDtm": "2026-11-06T00:00:00", "srchEndDtm": "2026-11-06T23:59:59", "pageNo": 1, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `unclear` b3-why-sales-dropped [a2api-acom-names-batch] 2회차 · `get_sales_overview` `{"valid_from": "2026-11-03", "valid_through": "2026-11-09", "acom:metrics": ["revenue", "order_count"], "compare_from": "2026-10-28", "compare_through": "2026-11-02"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) The period ends on 2026-11-09, after today (2026-11-06); sales after today are not known yet. Next: get_sales_overview.
- `model:schema` b3-why-sales-dropped [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-05", "srchEndDt": "2026-11-05", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` b3-why-sales-dropped [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261105, "srchEndDt": 20261105, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` b3-why-sales-dropped [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-05", "srchEndDt": "2026-11-05", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` b3-why-sales-dropped [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261105, "srchEndDt": 20261105, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` b3-why-sales-dropped [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-05", "srchEndDt": "2026-11-05", "cmprBaseCd": 2}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` b3-why-sales-dropped [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-05 00:00:00", "srchEndDt": "2026-11-05 23:59:59", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` b3-why-sales-dropped [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-05", "srchEndDt": "2026-11-05", "cmprBaseCd": "01"}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: unknown variant `01`, expected `1` or `2`
- `model:schema` b3-why-sales-dropped [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261105, "srchEndDt": 20261105, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` b3-why-sales-dropped [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-05", "srchEndDt": "2026-11-05", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` b3-why-sales-dropped [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-05", "srchEndDt": "2026-11-05", "cmprBaseCd": 2}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `source:undocumented` b3-why-sales-dropped [facade-all] 2회차 · `getOrdGridList` `{"ordDtmFrom": "2026-11-05 00:00:00", "ordDtmTo": "2026-11-05 23:59:59", "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` b3-why-sales-dropped [facade-all] 2회차 · `getOrdGridList` `{"ordDtmFrom": "2026-11-05 00:00:00", "ordDtmTo": "2026-11-05 23:59:59", "pageNo": 1, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: `2026-11-05 00:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)

## 기대와 다른 쓰기 입력

- b1-vip-weekend-sale [a2api-acom] 1회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom] 1회차 · `schedule_banner` 기대 {"slot_id": "slot_home_hero"} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-names-batch] 1회차 · `create_coupon` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom] 1회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom] 1회차 · `send_customer_message` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names-batch] 1회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names-batch] 1회차 · `send_customer_message` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-names-batch] 2회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom] 2회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom] 2회차 · `schedule_banner` 기대 {"slot_id": "slot_home_hero"} · 부르지 않음
- b2-returns-over-200 [a2api-acom] 2회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom] 2회차 · `send_customer_message` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names-batch] 2회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names-batch] 2회차 · `send_customer_message` 기대 {} · 부르지 않음
