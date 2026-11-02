# 호출 단계 리뷰 — ours-design-12b

판정 기준 함수 정의: `ours-design-12b.functions.json`(실행 때 모델이 본 것)

단계: A0 API에 해당 기능 없음 · A 필요한 함수를 받지 못함 · B 받았지만 부르지 않음 · C 불렀지만 성공 못 함 · D 한도·오류로 중단 · E-write 쓰기 입력·change set · E-format 숫자는 있으나 표기 · E-content 답 내용 누락

## 필요한 함수: 확보 → 호출 → 성공

| 방식 | 통과 | 필요한 함수(API에 있음/전체) | 모델에게 줌 | 불렀음 | 성공 | 확보 기록 |
|---|---|---|---|---|---|---|
| a2api-acom | 5/24 | 42/42 | 36/42 (86%) | 28/42 (67%) | 28/42 (67%) | 불러오기·검색 결과로 추정 |
| a2api-acom-guard | 6/24 | 42/42 | 35/42 (83%) | 30/42 (71%) | 30/42 (71%) | 불러오기·검색 결과로 추정 |
| a2api-acom-names-batch | 13/24 | 42/42 | 34/42 (81%) | 34/42 (81%) | 34/42 (81%) | 불러오기·검색 결과로 추정 |
| a2api-acom-names-batch-guard | 12/24 | 42/42 | 34/42 (81%) | 31/42 (74%) | 31/42 (74%) | 불러오기·검색 결과로 추정 |

## 실패한 실행이 처음 막힌 단계

| 방식 | passed | A0 | A | B | C | D | E-write | E-format | E-content |
|---|---|---|---|---|---|---|---|---|---|
| a2api-acom | 5 | 0 | 4 | 3 | 0 | 4 | 0 | 3 | 5 |
| a2api-acom-guard | 6 | 0 | 5 | 1 | 0 | 5 | 0 | 2 | 5 |
| a2api-acom-names-batch | 13 | 0 | 4 | 0 | 0 | 3 | 0 | 2 | 2 |
| a2api-acom-names-batch-guard | 12 | 0 | 4 | 0 | 0 | 4 | 0 | 2 | 2 |

## 실패한 업무 호출의 원인

| 방식 | 업무 호출 | 실패 | model:schema | model:function | model:ungrounded | model:described | source:undocumented | business | unclear |
|---|---|---|---|---|---|---|---|---|---|
| a2api-acom | 112 | 10 | 1 | 1 | 4 | 0 | 0 | 0 | 4 |
| a2api-acom-guard | 120 | 10 | 2 | 0 | 4 | 0 | 0 | 0 | 4 |
| a2api-acom-names-batch | 139 | 11 | 0 | 0 | 2 | 0 | 0 | 3 | 6 |
| a2api-acom-names-batch-guard | 138 | 5 | 2 | 0 | 2 | 0 | 0 | 1 | 0 |

## 쓰기 입력(과업이 기대한 change set 항목)

| 방식 | 기대 항목 | 불렀음 | 입력 일치 |
|---|---|---|---|
| a2api-acom | 12 | 3 | 3 |
| a2api-acom-guard | 12 | 4 | 4 |
| a2api-acom-names-batch | 12 | 6 | 6 |
| a2api-acom-names-batch-guard | 12 | 3 | 3 |

## 실패한 호출 목록

- `model:function` b1-vip-weekend-sale [a2api-acom] 1회차 · `acom_search_products` `{"category_id": "cat_summer_outerwear", "limit": 10}` → NOT_SELECTED: Function is not active in this session; search again.
- `model:schema` b1-vip-weekend-sale [a2api-acom-names-batch-guard] 1회차 · `list_categories` `{"term_set": ["standard"]}` → INVALID_INPUT: Value does not conform to the declared schema. issues [{"path": "/term_set", "rule": "type", "expected": "string"}, {"path": "/term_set", "rule": "enum", "expected": ["standard", "display"]}]
- `model:ungrounded` mk-whats-running-this-weekend [a2api-acom-guard] 1회차 · `acom_get_policy` `{"key": "stacking", "file": "promotion"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) No policy key starts with `stacking`. Next: list_policies.
- `model:ungrounded` mk-whats-running-this-weekend [a2api-acom-guard] 1회차 · `acom_get_policy` `{"key": "discount", "file": "promotion"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) No policy key starts with `discount`. Next: list_policies.
- `unclear` mk-whats-running-this-weekend [a2api-acom-guard] 1회차 · `acom_get_policy` `{"key": "overlap", "file": "promotion"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) No policy key starts with `overlap`. Next: list_policies.
- `unclear` mk-whats-running-this-weekend [a2api-acom-guard] 1회차 · `acom_get_policy` `{"key": "promotion", "file": "promotion"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) No policy key starts with `promotion`. Next: list_policies.
- `model:ungrounded` mk-whats-running-this-weekend [a2api-acom] 1회차 · `acom_get_policy` `{"key": "stacking", "file": "promotion"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) No policy key starts with `stacking`. Next: list_policies.
- `model:ungrounded` mk-whats-running-this-weekend [a2api-acom] 1회차 · `acom_get_policy` `{"key": "discount", "file": "promotion"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) No policy key starts with `discount`. Next: list_policies.
- `unclear` mk-whats-running-this-weekend [a2api-acom] 1회차 · `acom_get_policy` `{"key": "overlap", "file": "promotion"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) No policy key starts with `overlap`. Next: list_policies.
- `unclear` mk-whats-running-this-weekend [a2api-acom] 1회차 · `acom_get_policy` `{"key": "promotion", "file": "promotion"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) No policy key starts with `promotion`. Next: list_policies.
- `business` md-low-stock-before-weekend [a2api-acom-names-batch-guard] 1회차 · `get_inventory` `{"product_id": "prd_knitwear_24"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `business` md-low-stock-before-weekend [a2api-acom-names-batch] 1회차 · `get_inventory` `{"product_id": "prd_rain_parka"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `business` md-low-stock-before-weekend [a2api-acom-names-batch] 1회차 · `get_inventory` `{"product_id": "prd_rain_parka"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `unclear` md-overcoat-runs-small [a2api-acom-names-batch] 1회차 · `get_product_measurements` `{"product_id": "prd_wool_overcoat", "sizes": ["S", "XL"]}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) The size chart has no size S. Next: get_product.
- `unclear` md-overcoat-runs-small [a2api-acom-names-batch] 1회차 · `get_product_measurements` `{"product_id": "prd_wool_overcoat", "sizes": ["S", "XL"]}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) The size chart has no size S. Next: get_product.
- `unclear` md-overcoat-runs-small [a2api-acom-names-batch] 1회차 · `get_product_measurements` `{"product_id": "prd_wool_overcoat", "sizes": ["XL"]}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) The size chart has no size XL. Next: get_product.
- `model:schema` md-end-of-season-markdown [a2api-acom-guard] 1회차 · `acom_set_sale_prices` `{"name": "End of season tees markdown", "valid_for_member_tier": "everyone", "valid_from": "2026-11-06T11:00", "valid_through": "2026-11-15T23:59", "scope_mode": "category", "category_id": "cat_tees",` → INVALID_INPUT: Value does not conform to the declared schema. issues [{"path": "/overrides/0/percent_off", "rule": "minimum", "expected": 0.01}]
- `model:ungrounded` mgr-what-needs-me-today [a2api-acom-names-batch] 1회차 · `list_notifications` `{"customer_id": "me", "sent_from": "2026-11-06T00:00:00", "limit": 100}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no customer me. Next: search_members.
- `model:ungrounded` mgr-what-needs-me-today [a2api-acom-names-batch-guard] 1회차 · `list_notifications` `{"customer_id": "me", "read": false, "sent_from": "2026-11-06T00:00:00", "limit": 100}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no customer me. Next: search_members.
- `model:schema` b1-vip-weekend-sale [a2api-acom-names-batch-guard] 2회차 · `list_categories` `{"term_set": ["standard"]}` → INVALID_INPUT: Value does not conform to the declared schema. issues [{"path": "/term_set", "rule": "type", "expected": "string"}, {"path": "/term_set", "rule": "enum", "expected": ["standard", "display"]}]
- `model:ungrounded` mk-whats-running-this-weekend [a2api-acom] 2회차 · `acom_get_policy` `{"key": "stacking", "file": "promotion"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) No policy key starts with `stacking`. Next: list_policies.
- `model:ungrounded` mk-whats-running-this-weekend [a2api-acom] 2회차 · `acom_get_policy` `{"key": "discount", "file": "promotion"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) No policy key starts with `discount`. Next: list_policies.
- `unclear` mk-whats-running-this-weekend [a2api-acom] 2회차 · `acom_get_policy` `{"key": "overlap", "file": "promotion"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) No policy key starts with `overlap`. Next: list_policies.
- `unclear` mk-whats-running-this-weekend [a2api-acom] 2회차 · `acom_get_policy` `{"key": "promotion", "file": "promotion"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) No policy key starts with `promotion`. Next: list_policies.
- `model:ungrounded` mk-whats-running-this-weekend [a2api-acom-guard] 2회차 · `acom_get_policy` `{"key": "stacking", "file": "promotion"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) No policy key starts with `stacking`. Next: list_policies.
- `model:ungrounded` mk-whats-running-this-weekend [a2api-acom-guard] 2회차 · `acom_get_policy` `{"key": "discount", "file": "promotion"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) No policy key starts with `discount`. Next: list_policies.
- `unclear` mk-whats-running-this-weekend [a2api-acom-guard] 2회차 · `acom_get_policy` `{"key": "overlap", "file": "promotion"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) No policy key starts with `overlap`. Next: list_policies.
- `unclear` mk-whats-running-this-weekend [a2api-acom-guard] 2회차 · `acom_get_policy` `{"key": "promotion", "file": "promotion"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) No policy key starts with `promotion`. Next: list_policies.
- `business` md-low-stock-before-weekend [a2api-acom-names-batch] 2회차 · `get_inventory` `{"product_id": "prd_knitwear_24"}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `unclear` md-overcoat-runs-small [a2api-acom-names-batch] 2회차 · `get_product_measurements` `{"product_id": "prd_wool_overcoat", "sizes": ["S", "XL"]}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) The size chart has no size S. Next: get_product.
- `unclear` md-overcoat-runs-small [a2api-acom-names-batch] 2회차 · `get_product_measurements` `{"product_id": "prd_wool_overcoat", "sizes": ["S", "XL"]}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) The size chart has no size S. Next: get_product.
- `unclear` md-overcoat-runs-small [a2api-acom-names-batch] 2회차 · `get_product_measurements` `{"product_id": "prd_wool_overcoat", "sizes": ["XL"]}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) The size chart has no size XL. Next: get_product.
- `model:schema` md-end-of-season-markdown [a2api-acom] 2회차 · `acom_set_sale_prices` `{"name": "End of season tees markdown", "valid_for_member_tier": "everyone", "valid_from": "2026-11-06T11:00", "valid_through": "2026-11-15T23:59", "scope_mode": "category", "category_id": "cat_tees",` → INVALID_INPUT: Value does not conform to the declared schema. issues [{"path": "/overrides/0/percent_off", "rule": "minimum", "expected": 0.01}]
- `model:schema` md-end-of-season-markdown [a2api-acom-guard] 2회차 · `acom_set_sale_prices` `{"name": "End of season tees markdown", "valid_for_member_tier": "everyone", "valid_from": "2026-11-06T11:00", "valid_through": "2026-11-15T23:59", "scope_mode": "category", "category_id": "cat_tees",` → INVALID_INPUT: Value does not conform to the declared schema. issues [{"path": "/overrides/0/percent_off", "rule": "minimum", "expected": 0.01}]
- `model:ungrounded` mgr-what-needs-me-today [a2api-acom-names-batch] 2회차 · `list_notifications` `{"customer_id": "me", "sent_from": "2026-11-06T00:00:00", "limit": 100}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no customer me. Next: search_members.
- `model:ungrounded` mgr-what-needs-me-today [a2api-acom-names-batch-guard] 2회차 · `list_notifications` `{"customer_id": "me", "sent_from": "2026-11-06T00:00:00", "limit": 100}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no customer me. Next: search_members.

## 기대와 다른 쓰기 입력

- b1-vip-weekend-sale [a2api-acom] 1회차 · `set_sale_prices` 기대 {"valid_for_member_tier": "vip", "percent_off": 20} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom] 1회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom] 1회차 · `schedule_banner` 기대 {"slot_id": "slot_home_hero"} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-guard] 1회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-guard] 1회차 · `schedule_banner` 기대 {"slot_id": "slot_home_hero"} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-names-batch] 1회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-names-batch-guard] 1회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-names-batch-guard] 1회차 · `schedule_banner` 기대 {"slot_id": "slot_home_hero"} · 부르지 않음
- md-end-of-season-markdown [a2api-acom-names-batch-guard] 1회차 · `set_sale_prices` 기대 {"valid_for_member_tier": "everyone", "scope_mode": "category", "category_id": "cat_tees", "exclude_low_stock": true} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names-batch] 1회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names-batch] 1회차 · `send_customer_message` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names-batch-guard] 1회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names-batch-guard] 1회차 · `send_customer_message` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom] 1회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom] 1회차 · `send_customer_message` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-guard] 1회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-guard] 1회차 · `send_customer_message` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-guard] 2회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-guard] 2회차 · `schedule_banner` 기대 {"slot_id": "slot_home_hero"} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-names-batch] 2회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-names-batch-guard] 2회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-names-batch-guard] 2회차 · `schedule_banner` 기대 {"slot_id": "slot_home_hero"} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom] 2회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom] 2회차 · `schedule_banner` 기대 {"slot_id": "slot_home_hero"} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names-batch-guard] 2회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names-batch-guard] 2회차 · `send_customer_message` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom] 2회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom] 2회차 · `send_customer_message` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-guard] 2회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-guard] 2회차 · `send_customer_message` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names-batch] 2회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names-batch] 2회차 · `send_customer_message` 기대 {} · 부르지 않음
