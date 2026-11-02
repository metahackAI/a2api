# 호출 단계 리뷰 — ours-heldout-index-posthoc-2

판정 기준 함수 정의: `ours-heldout-index-posthoc-2.functions.json`(실행 때 모델이 본 것)

단계: A0 API에 해당 기능 없음 · A 필요한 함수를 받지 못함 · B 받았지만 부르지 않음 · C 불렀지만 성공 못 함 · D 한도·오류로 중단 · E-write 쓰기 입력·change set · E-format 숫자는 있으나 표기 · E-content 답 내용 누락

## 필요한 함수: 확보 → 호출 → 성공

| 방식 | 통과 | 필요한 함수(API에 있음/전체) | 모델에게 줌 | 불렀음 | 성공 | 확보 기록 |
|---|---|---|---|---|---|---|
| a2api-acom | 5/32 | 32/32 | 26/32 (81%) | 18/32 (56%) | 18/32 (56%) | 불러오기·검색 결과로 추정 |
| a2api-acom-index | 7/32 | 32/32 | 24/32 (75%) | 22/32 (69%) | 22/32 (69%) | 불러오기·검색 결과로 추정 |
| a2api-acom-names | 7/32 | 32/32 | 28/32 (88%) | 25/32 (78%) | 25/32 (78%) | 불러오기·검색 결과로 추정 |

## 실패한 실행이 처음 막힌 단계

| 방식 | passed | A0 | A | B | C | D | E-write | E-format | E-content |
|---|---|---|---|---|---|---|---|---|---|
| a2api-acom | 5 | 0 | 6 | 1 | 0 | 15 | 2 | 0 | 3 |
| a2api-acom-index | 7 | 0 | 8 | 0 | 0 | 4 | 2 | 3 | 8 |
| a2api-acom-names | 7 | 0 | 4 | 0 | 0 | 8 | 2 | 1 | 10 |

## 실패한 업무 호출의 원인

| 방식 | 업무 호출 | 실패 | model:schema | model:function | model:ungrounded | model:described | source:undocumented | business | unclear |
|---|---|---|---|---|---|---|---|---|---|
| a2api-acom | 133 | 10 | 0 | 2 | 0 | 1 | 0 | 7 | 0 |
| a2api-acom-index | 154 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| a2api-acom-names | 140 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## 쓰기 입력(과업이 기대한 change set 항목)

| 방식 | 기대 항목 | 불렀음 | 입력 일치 |
|---|---|---|---|
| a2api-acom | 4 | 3 | 1 |
| a2api-acom-index | 4 | 4 | 2 |
| a2api-acom-names | 4 | 4 | 2 |

## 실패한 호출 목록

- `business` md-below-cost [a2api-acom] 1회차 · `acom_search_products` `{"max_price": {"value": 50, "currency": "USD"}, "limit": 100}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `business` md-below-cost [a2api-acom] 1회차 · `acom_search_products` `{"limit": 100, "cursor": "o220"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `unclear` mgr-how-is-business [a2api-acom-index] 1회차 · `get_sales_overview` `{"valid_from": "2026-11-01", "valid_through": "2026-11-06", "acom:metrics": ["revenue", "order_count", "average_order_value", "cancellation_rate", "return_rate"], "acom:dimensions": ["category", "memb` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) cancellation_rate cannot be split by category_id: it counts whole orders. Split it by member_tier, or leave it out. Next: get_sales_overview.
- `model:function` mk-category-promotion [a2api-acom] 2회차 · `acom_list_categories` `{}` → NOT_SELECTED: Function is not active in this session; search again.
- `model:function` mk-category-promotion [a2api-acom] 2회차 · `acom_list_categories` `{}` → NOT_SELECTED: Function is not active in this session; search again.
- `business` md-broken-sizes-outerwear [a2api-acom] 2회차 · `acom_get_product_measurements` `{"product_id": "prd_chore_coat"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `business` md-broken-sizes-outerwear [a2api-acom] 2회차 · `acom_get_product_measurements` `{"product_id": "prd_rain_parka"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `business` md-broken-sizes-outerwear [a2api-acom] 2회차 · `acom_get_product_measurements` `{"product_id": "prd_denim_jacket"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `business` md-broken-sizes-outerwear [a2api-acom] 2회차 · `acom_search_product_groups` `{"query": "broken", "category_id": "cat_outerwear", "limit": 100}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `business` md-below-cost [a2api-acom] 2회차 · `acom_get_price_breakdown` `{"variant_id": "var_wool_overcoat_s_charcoal"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `model:described` ops-change-address-in-transit [a2api-acom] 2회차 · `acom_get_receipt` `{"order_id": 27184}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Order ord_27184 has no receipt yet. Next: issue_receipt.

## 기대와 다른 쓰기 입력

- mk-pause-knit-until-monday [a2api-acom] 1회차 · `pause_promotion` 기대 {"promotion_id": "promo_autumn_knit"} · 부르지 않음
- ops-photo-request [a2api-acom-index] 1회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
- ops-photo-request [a2api-acom-names] 1회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
- ops-photo-request [a2api-acom] 1회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
- ops-photo-request [a2api-acom-names] 2회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
- ops-photo-request [a2api-acom] 2회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
- ops-photo-request [a2api-acom-index] 2회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
