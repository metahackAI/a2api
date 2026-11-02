# 호출 단계 리뷰 — ours-heldout-1

판정 기준 함수 정의: `ours-heldout-1.functions.json`(실행 때 모델이 본 것)

단계: A0 API에 해당 기능 없음 · A 필요한 함수를 받지 못함 · B 받았지만 부르지 않음 · C 불렀지만 성공 못 함 · D-before 필요한 함수를 부르기 전 한도·오류로 중단 · D-after 필요한 함수는 모두 성공했는데 답하기 전 한도로 중단 · E-write 쓰기 입력·change set · E-format 숫자는 있으나 표기 · E-content 답 내용 누락

## 필요한 함수: 확보 → 호출 → 성공

| 방식 | 통과 | 필요한 함수(API에 있음/전체) | 모델에게 줌 | 불렀음 | 성공 | 확보 기록 |
|---|---|---|---|---|---|---|
| facade-all | 4/32 | 16/32 | 16/16 (100%) | 14/16 (88%) | 10/16 (62%) | 단계별 기록 |
| acom-all | 0/32 | 32/32 | 32/32 (100%) | 0/32 (0%) | 0/32 (0%) | 단계별 기록 |
| a2api-acom | 3/32 | 32/32 | 27/32 (84%) | 18/32 (56%) | 18/32 (56%) | 불러오기·검색 결과로 추정 |
| a2api-facade | 5/32 | 16/32 | 14/16 (88%) | 9/16 (56%) | 8/16 (50%) | 불러오기·검색 결과로 추정 |

## 실패한 실행이 처음 막힌 단계

| 방식 | passed | A0 | A | B | C | D-before | D-after | E-write | E-format | E-content |
|---|---|---|---|---|---|---|---|---|---|---|
| facade-all | 4 | 12 | 0 | 2 | 4 | 0 | 6 | 0 | 0 | 4 |
| acom-all | 0 | 0 | 0 | 0 | 0 | 30 | 2 | 0 | 0 | 0 |
| a2api-acom | 3 | 0 | 5 | 3 | 0 | 4 | 9 | 2 | 1 | 5 |
| a2api-facade | 5 | 11 | 2 | 3 | 1 | 2 | 6 | 0 | 0 | 2 |

## 실패한 업무 호출의 원인

| 방식 | 업무 호출 | 실패 | model:schema | model:function | model:ungrounded | model:described | source:undocumented | business | unclear |
|---|---|---|---|---|---|---|---|---|---|
| facade-all | 270 | 189 | 157 | 0 | 0 | 0 | 28 | 3 | 1 |
| acom-all | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| a2api-acom | 119 | 2 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| a2api-facade | 131 | 21 | 1 | 0 | 0 | 0 | 4 | 16 | 0 |

## 쓰기 입력(과업이 기대한 change set 항목)

| 방식 | 기대 항목 | 불렀음 | 입력 일치 |
|---|---|---|---|
| acom-all | 4 | 0 | 0 |
| a2api-acom | 4 | 4 | 2 |

## 실패한 호출 목록

- `source:undocumented` mk-pause-knit-until-monday [facade-all] 1회차 · `getPrmtGridList` `{"prmtNm": "knit", "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-pause-knit-until-monday [facade-all] 1회차 · `savePrmtList` `{"rows": [{"rowStat": "U", "prmtNo": "promo_autumn_knit", "strtDtm": "2026-11-09T00:00:00-05:00"}]}` → UPSTREAM_VALIDATION_FAILED: Row 1: `prmtStatCd` is required.
- `business` mk-pause-knit-until-monday [facade-all] 1회차 · `savePrmtList` `{"rows": [{"rowStat": "U", "prmtNo": "promo_autumn_knit", "prmtStatCd": "10", "strtDtm": "2026-11-09T00:00:00-05:00"}]}` → UPSTREAM_CONFLICT: Row 1: Status change not available on this screen.
- `business` mk-pause-knit-until-monday [facade-all] 1회차 · `savePrmtList` `{"rows": [{"rowStat": "U", "prmtNo": "promo_autumn_knit", "prmtStatCd": "20", "strtDtm": "2026-11-09T00:00:00-05:00", "endDtm": "2026-11-15T23:59:00-05:00"}]}` → UPSTREAM_CONFLICT: Row 1: Status change not available on this screen.
- `business` mk-pause-knit-until-monday [facade-all] 1회차 · `savePrmtList` `{"rows": [{"rowStat": "U", "prmtNo": "promo_autumn_knit", "prmtStatCd": "20", "strtDtm": "2026-11-01T00:00:00-04:00", "endDtm": "2026-11-08T23:59:00-05:00"}]}` → UPSTREAM_CONFLICT: Row 1: Status change not available on this screen.
- `unclear` mk-category-promotion [a2api-acom] 1회차 · `acom_map_category` `{"standard_category_id": "cat_outerwear", "display_category_ids": ["cat_outerwear"]}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) cat_outerwear is a standard category; a standard category maps to display ones. Next: map_category.
- `source:undocumented` mk-category-promotion [facade-all] 1회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-category-promotion [facade-all] 1회차 · `getPrdGridList` `{"srchKwd": "Outerwear", "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `unclear` mk-category-promotion [facade-all] 1회차 · `savePrmtList` `{"rows": [{"rowStat": "I", "prmtNo": "promo_outerwear_50off_20261106", "prmtNm": "Outerwear $50 off $250+", "prmtTpCd": "T03", "prmtStatCd": "10", "tgtMbrGrdCd": "G00", "strtDtm": "2026-11-06T11:00:00` → UPSTREAM_VALIDATION_FAILED: Row 1: Invalid member grade code.
- `model:schema` mk-category-promotion [facade-all] 1회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-category-promotion [facade-all] 1회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-category-promotion [facade-all] 1회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `source:undocumented` mk-category-promotion [facade-all] 1회차 · `getPrmtTgtMbrList` `{"mbrGrdCd": "G00", "pageNo": 0, "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:schema` mk-winback [facade-all] 1회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-winback [facade-all] 1회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-winback [facade-all] 1회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-winback [facade-all] 1회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-winback [facade-all] 1회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-winback [facade-all] 1회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `source:undocumented` mk-winback [facade-all] 1회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:schema` mk-winback [facade-all] 1회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-winback [facade-all] 1회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-winback [facade-all] 1회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-winback [facade-all] 1회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-winback [facade-all] 1회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `source:undocumented` md-broken-sizes-outerwear [facade-all] 1회차 · `getPrdGridList` `{"srchKwd": "outerwear", "pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `business` md-broken-sizes-outerwear [a2api-facade] 1회차 · `facade_get_prd_dtl_info_v2` `{"product_id": "prd_summer_outerwear_02"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `business` md-broken-sizes-outerwear [a2api-facade] 1회차 · `facade_get_prd_dtl_info_v2` `{"product_id": "prd_utility_jacket"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `business` md-broken-sizes-outerwear [a2api-facade] 1회차 · `facade_get_prd_dtl_info_v2` `{"product_id": "prd_summer_outerwear_15"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `business` md-broken-sizes-outerwear [a2api-facade] 1회차 · `facade_get_prd_dtl_info_v2` `{"product_id": "prd_summer_outerwear_02"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `business` md-broken-sizes-outerwear [a2api-facade] 1회차 · `facade_get_prd_dtl_info_v2` `{"product_id": "prd_utility_jacket"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `business` md-broken-sizes-outerwear [a2api-facade] 1회차 · `facade_get_prd_dtl_info_v2` `{"product_id": "prd_summer_outerwear_15"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `business` md-broken-sizes-outerwear [a2api-facade] 1회차 · `facade_get_prd_dtl_info_v2` `{"product_id": "prd_field_jacket"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `business` md-broken-sizes-outerwear [a2api-facade] 1회차 · `facade_get_prd_dtl_info_v2` `{"product_id": "prd_chore_coat"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `business` md-broken-sizes-outerwear [a2api-facade] 1회차 · `facade_get_prd_dtl_info_v2` `{"product_id": "prd_summer_outerwear_02"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `business` md-broken-sizes-outerwear [a2api-facade] 1회차 · `facade_get_prd_dtl_info_v2` `{"product_id": "prd_utility_jacket"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `business` md-broken-sizes-outerwear [a2api-facade] 1회차 · `facade_get_prd_dtl_info_v2` `{"product_id": "prd_summer_outerwear_15"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `business` md-broken-sizes-outerwear [a2api-facade] 1회차 · `facade_get_prd_dtl_info_v2` `{"product_id": "prd_field_jacket"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `business` md-broken-sizes-outerwear [a2api-facade] 1회차 · `facade_get_prd_dtl_info_v2` `{"product_id": "prd_chore_coat"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `source:undocumented` md-how-many-left [facade-all] 1회차 · `getPrdGridList` `{"srchKwd": "Light rain parka", "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-below-cost [facade-all] 1회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 100}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-below-cost [facade-all] 1회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:schema` md-best-sellers-this-month [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-01", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-best-sellers-this-month [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261101, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` md-best-sellers-this-month [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261101, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` md-best-sellers-this-month [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261101, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` md-best-sellers-this-month [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261101, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` md-best-sellers-this-month [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261101, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` md-best-sellers-this-month [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-01", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-best-sellers-this-month [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261101, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` md-best-sellers-this-month [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-01", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-best-sellers-this-month [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-01", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-best-sellers-this-month [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261001, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` md-best-sellers-this-month [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261101, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `source:undocumented` md-out-of-stock-30-days [facade-all] 1회차 · `getPrdGridList` `{"stkQtyFrom": 0, "stkQtyTo": 0, "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:schema` md-out-of-stock-30-days [facade-all] 1회차 · `getPrdGridListCnt` `{"sellStatCd": 30}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-out-of-stock-30-days [facade-all] 1회차 · `getPrdGridListCnt` `{"sellStatCd": 30}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-out-of-stock-30-days [facade-all] 1회차 · `getPrdGridListCnt` `{"sellStatCd": 30}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-out-of-stock-30-days [facade-all] 1회차 · `getPrdGridList` `{"sellStatCd": 30, "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-out-of-stock-30-days [facade-all] 1회차 · `getPrdGridListCnt` `{"sellStatCd": 30, "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `source:undocumented` md-out-of-stock-30-days [facade-all] 1회차 · `getPrdGridList` `{"stkQtyFrom": 0, "stkQtyTo": 0, "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:schema` md-out-of-stock-30-days [facade-all] 1회차 · `getPrdGridList` `{"sellStatCd": 30, "pageNo": 1, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-out-of-stock-30-days [facade-all] 1회차 · `getPrdGridList` `{"sellStatCd": 30, "pageNo": 1, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `source:undocumented` ops-photo-request [a2api-facade] 1회차 · `facade_get_rfnd_pop_init_data` `{"claim_id": 20366}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no claim 20366.
- `model:schema` ops-photo-request [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 20366}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-photo-request [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 20366}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-photo-request [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 20366}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `source:undocumented` ops-photo-request [facade-all] 1회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:schema` ops-cancel-delivered [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-cancel-delivered [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-cancel-delivered [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-cancel-delivered [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-cancel-delivered [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-cancel-delivered [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-cancel-delivered [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-cancel-delivered [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-cancel-delivered [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-cancel-delivered [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-cancel-delivered [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-cancel-delivered [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-change-address-in-transit [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-change-address-in-transit [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-change-address-in-transit [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-change-address-in-transit [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-change-address-in-transit [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `source:undocumented` ops-change-address-in-transit [facade-all] 1회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:schema` ops-change-address-in-transit [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-change-address-in-transit [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-change-address-in-transit [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-change-address-in-transit [facade-all] 1회차 · `getRfndPopInitData` `{"clmNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `source:undocumented` mgr-undo-banner [facade-all] 1회차 · `getDispCornerList` `{"dispPageCd": "01", "strtDtm": "2026-10-01 00:00:00", "endDtm": "2026-11-06 23:59:59"}` → UPSTREAM_VALIDATION_FAILED: `2026-10-01 00:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `model:schema` mgr-weekly-summary [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-30", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-weekly-summary [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-30", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-weekly-summary [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-26", "srchEndDt": "2026-11-01", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-weekly-summary [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-30", "srchEndDt": "2026-11-05", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-weekly-summary [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261030, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mgr-weekly-summary [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261030, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mgr-weekly-summary [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-30", "srchEndDt": "2026-11-05", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-weekly-summary [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-30", "srchEndDt": "2026-11-05", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-weekly-summary [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261030, "srchEndDt": 20261105, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mgr-weekly-summary [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261030, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mgr-weekly-summary [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-30", "srchEndDt": "2026-11-05", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-weekly-summary [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261030, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mgr-how-is-business [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-30", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-how-is-business [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-30", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-how-is-business [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-30", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-how-is-business [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-30", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-how-is-business [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-30", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-how-is-business [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261030, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mgr-how-is-business [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261030, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mgr-how-is-business [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261030, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mgr-how-is-business [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261030, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mgr-how-is-business [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261030, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mgr-how-is-business [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261030, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mgr-how-is-business [facade-all] 1회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261030, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `source:undocumented` mk-pause-knit-until-monday [facade-all] 2회차 · `getPrmtGridList` `{"prmtNm": "knit", "pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-category-promotion [facade-all] 2회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-category-promotion [facade-all] 2회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` mk-category-promotion [facade-all] 2회차 · `getPrdGridList` `{"srchKwd": "Outerwear", "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:schema` mk-category-promotion [facade-all] 2회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-category-promotion [facade-all] 2회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-category-promotion [facade-all] 2회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `source:undocumented` mk-winback [facade-all] 2회차 · `getPrmtGridList` `{"pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:schema` mk-winback [facade-all] 2회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-winback [facade-all] 2회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-winback [facade-all] 2회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-winback [facade-all] 2회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-winback [facade-all] 2회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-winback [facade-all] 2회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-winback [facade-all] 2회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-winback [facade-all] 2회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-winback [facade-all] 2회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mk-winback [facade-all] 2회차 · `getMbrGrdList` `{"prgmNo": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `source:undocumented` md-broken-sizes-outerwear [facade-all] 2회차 · `getPrdGridList` `{"srchKwd": "outerwear", "pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-how-many-left [facade-all] 2회차 · `getPrdGridList` `{"srchKwd": "Light rain parka", "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` md-below-cost [facade-all] 2회차 · `getPrdGridList` `{"pageNo": 0, "pageSize": 20}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:schema` md-best-sellers-this-month [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-01", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-best-sellers-this-month [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261101, "srchEndDt": 20261130, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` md-best-sellers-this-month [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-01", "srchEndDt": "2026-11-30", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-best-sellers-this-month [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261101, "srchEndDt": 20261130, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` md-best-sellers-this-month [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-01", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-best-sellers-this-month [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-01", "srchEndDt": "2026-11-30", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-best-sellers-this-month [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-01", "srchEndDt": "2026-11-30", "cmprBaseCd": 2}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-best-sellers-this-month [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026/11/01", "srchEndDt": "2026/11/30", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-best-sellers-this-month [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-01", "srchEndDt": "2026-11-30", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-best-sellers-this-month [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-01", "srchEndDt": "2026-11-30", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-best-sellers-this-month [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-11-01", "srchEndDt": "2026-11-30", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `business` md-out-of-stock-30-days [a2api-acom] 2회차 · `acom_get_inventory` `{"product_id": "prd_wool_overcoat"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `business` md-out-of-stock-30-days [a2api-facade] 2회차 · `facade_get_prd_grid_list` `{"page": 1, "page_size": 20}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `business` md-out-of-stock-30-days [a2api-facade] 2회차 · `facade_get_prd_grid_list_cnt` `{"availability": "discontinued"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `source:undocumented` md-out-of-stock-30-days [facade-all] 2회차 · `getPrdGridList` `{"stkQtyFrom": 0, "stkQtyTo": 0, "pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:schema` md-out-of-stock-30-days [facade-all] 2회차 · `getPrdGridListCnt` `{"sellStatCd": 30, "pageNo": 1, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-out-of-stock-30-days [facade-all] 2회차 · `getPrdGridListCnt` `{"sellStatCd": 30}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-out-of-stock-30-days [facade-all] 2회차 · `getPrdGridListCnt` `{"sellStatCd": 30, "pageNo": 1, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-out-of-stock-30-days [facade-all] 2회차 · `getPrdGridList` `{"sellStatCd": 30, "pageNo": 1, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-out-of-stock-30-days [facade-all] 2회차 · `getPrdGridList` `{"sellStatCd": 30, "pageNo": 1, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-out-of-stock-30-days [facade-all] 2회차 · `getPrdGridList` `{"sellStatCd": 30}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` md-out-of-stock-30-days [facade-all] 2회차 · `getPrdGridList` `{"sellStatCd": 30, "pageNo": 1, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `source:undocumented` ops-unfulfilled-3-days [facade-all] 2회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `source:undocumented` ops-photo-request [a2api-facade] 2회차 · `facade_get_rfnd_pop_init_data` `{"claim_id": 20366}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no claim 20366.
- `model:schema` ops-photo-request [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 20366}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-photo-request [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 20366}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `source:undocumented` ops-photo-request [facade-all] 2회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:schema` ops-photo-request [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 20366}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-cancel-delivered [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-cancel-delivered [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `source:undocumented` ops-cancel-delivered [facade-all] 2회차 · `getClmGridList` `{"pageNo": 0, "pageSize": 10}` → UPSTREAM_VALIDATION_FAILED: Invalid paging.
- `model:schema` ops-cancel-delivered [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-cancel-delivered [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-cancel-delivered [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-cancel-delivered [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-cancel-delivered [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-cancel-delivered [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-cancel-delivered [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-cancel-delivered [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-cancel-delivered [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 20402}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `source:undocumented` ops-change-address-in-transit [a2api-facade] 2회차 · `facade_get_rfnd_pop_init_data` `{"claim_id": 27184}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no claim 27184.
- `source:undocumented` ops-change-address-in-transit [a2api-facade] 2회차 · `facade_get_prd_dtl_info` `{"product_id": 27184}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no product 27184 in this store.
- `model:schema` ops-change-address-in-transit [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-change-address-in-transit [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-change-address-in-transit [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-change-address-in-transit [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-change-address-in-transit [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-change-address-in-transit [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-change-address-in-transit [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-change-address-in-transit [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-change-address-in-transit [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-change-address-in-transit [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-change-address-in-transit [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` ops-change-address-in-transit [facade-all] 2회차 · `getRfndPopInitData` `{"clmNo": 27184}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mgr-undo-banner [a2api-facade] 2회차 · `facade_save_disp_bnr_list` `{"rows": [{"row_action": "delete", "corner_id": "slot_home_hero", "target_member_grade": "G00", "starts_at": "2026-11-06T10:00:00-05:00", "ends_at": null}]}` → INVALID_INPUT: Value does not conform to the declared schema. issues [{"path": "/rows/0/ends_at", "rule": "type", "expected": "string"}]
- `business` mgr-undo-banner [a2api-facade] 2회차 · `facade_save_disp_bnr_list` `{"rows": [{"row_action": "delete", "corner_id": "slot_home_hero", "target_member_grade": "G00", "starts_at": "2026-11-06T10:00:00-05:00", "ends_at": "2026-11-06T10:00:00-05:00"}]}` → UPSTREAM_CONFLICT: The backend reported that the current state does not allow this request. (HTTP 409) Row 1: Row status not available on this screen.
- `model:schema` mgr-undo-banner [facade-all] 2회차 · `getDispCornerList` `{"dispPageCd": "01", "strtDtm": 20261001000000, "endDtm": 20261106110000}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `source:undocumented` mgr-undo-banner [facade-all] 2회차 · `getDispCornerList` `{"dispPageCd": "01", "strtDtm": "2026-10-01 00:00:00", "endDtm": "2026-11-06 11:00:00"}` → UPSTREAM_VALIDATION_FAILED: `2026-10-01 00:00:00` is not a date-time (expected 2026-11-07T00:00 or RFC 3339)
- `model:schema` mgr-weekly-summary [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-30", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-weekly-summary [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-30", "srchEndDt": "2026-11-05", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-weekly-summary [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261030, "srchEndDt": 20261105, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mgr-weekly-summary [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": 20261030, "srchEndDt": 20261106, "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected a string
- `model:schema` mgr-weekly-summary [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026/10/30", "srchEndDt": "2026/11/06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-weekly-summary [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-30", "srchEndDt": "2026-11-06", "cmprBaseCd": 2}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-how-is-business [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-01", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-how-is-business [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-01", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-how-is-business [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-01", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-how-is-business [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-01", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-how-is-business [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-01", "srchEndDt": "2026-11-06", "cmprBaseCd": 2}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-how-is-business [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-01", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-how-is-business [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-30", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-how-is-business [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-01", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-how-is-business [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-01", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-how-is-business [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-01", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-how-is-business [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-01", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map
- `model:schema` mgr-how-is-business [facade-all] 2회차 · `getSaleAnlsGridList` `{"srchStrtDt": "2026-10-01", "srchEndDt": "2026-11-06", "cmprBaseCd": 1}` → UPSTREAM_VALIDATION_FAILED: Invalid parameter: invalid type: number, expected string or map

## 기대와 다른 쓰기 입력

- mk-pause-knit-until-monday [acom-all] 1회차 · `pause_promotion` 기대 {"promotion_id": "promo_autumn_knit"} · 부르지 않음
- ops-photo-request [a2api-acom] 1회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
- ops-photo-request [acom-all] 1회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 부르지 않음
- mk-pause-knit-until-monday [acom-all] 2회차 · `pause_promotion` 기대 {"promotion_id": "promo_autumn_knit"} · 부르지 않음
- ops-photo-request [acom-all] 2회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 부르지 않음
- ops-photo-request [a2api-acom] 2회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
