# 호출 단계 리뷰 — ours-design-10

판정 기준 함수 정의: `ours-design-10.functions.json`(실행 때 모델이 본 것)

단계: A0 API에 해당 기능 없음 · A 필요한 함수를 받지 못함 · B 받았지만 부르지 않음 · C 불렀지만 성공 못 함 · D 한도·오류로 중단 · E-write 쓰기 입력·change set · E-format 숫자는 있으나 표기 · E-content 답 내용 누락

## 필요한 함수: 확보 → 호출 → 성공

| 방식 | 통과 | 필요한 함수(API에 있음/전체) | 모델에게 줌 | 불렀음 | 성공 | 확보 기록 |
|---|---|---|---|---|---|---|
| a2api-acom | 5/24 | 42/42 | 35/42 (83%) | 27/42 (64%) | 27/42 (64%) | 불러오기·검색 결과로 추정 |
| a2api-acom-names-norelated | 11/24 | 42/42 | 32/42 (76%) | 32/42 (76%) | 32/42 (76%) | 불러오기·검색 결과로 추정 |
| a2api-acom-names-batch | 14/24 | 42/42 | 36/42 (86%) | 35/42 (83%) | 35/42 (83%) | 불러오기·검색 결과로 추정 |

## 실패한 실행이 처음 막힌 단계

| 방식 | passed | A0 | A | B | C | D | E-write | E-format | E-content |
|---|---|---|---|---|---|---|---|---|---|
| a2api-acom | 5 | 0 | 5 | 2 | 0 | 5 | 0 | 3 | 4 |
| a2api-acom-names-norelated | 11 | 0 | 5 | 0 | 0 | 3 | 0 | 2 | 3 |
| a2api-acom-names-batch | 14 | 0 | 4 | 0 | 0 | 2 | 0 | 2 | 2 |

## 실패한 업무 호출의 원인

| 방식 | 업무 호출 | 실패 | model:schema | model:function | model:ungrounded | model:described | source:undocumented | business | unclear |
|---|---|---|---|---|---|---|---|---|---|
| a2api-acom | 106 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| a2api-acom-names-norelated | 139 | 6 | 0 | 0 | 2 | 0 | 0 | 2 | 2 |
| a2api-acom-names-batch | 126 | 4 | 0 | 0 | 2 | 0 | 0 | 1 | 1 |

## 쓰기 입력(과업이 기대한 change set 항목)

| 방식 | 기대 항목 | 불렀음 | 입력 일치 |
|---|---|---|---|
| a2api-acom | 12 | 2 | 2 |
| a2api-acom-names-norelated | 12 | 6 | 6 |
| a2api-acom-names-batch | 12 | 5 | 5 |

## 실패한 호출 목록

- `unclear` md-overcoat-runs-small [a2api-acom-names-norelated] 1회차 · `get_product_measurements` `{"product_id": "prd_wool_overcoat", "sizes": ["S", "M", "L", "XL"]}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) The size chart has no size S. Next: get_product.
- `business` md-overcoat-runs-small [a2api-acom-names-norelated] 1회차 · `get_review_summary` `{"product_id": "prd_wool_overcoat", "size": "S", "sample_limit": 3}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) No reviews match these conditions; widen the height range or size. Next: get_product_measurements.
- `business` md-overcoat-runs-small [a2api-acom-names-norelated] 1회차 · `get_review_summary` `{"product_id": "prd_wool_overcoat", "size": "XL", "sample_limit": 3}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) No reviews match these conditions; widen the height range or size. Next: get_product_measurements.
- `unclear` md-overcoat-runs-small [a2api-acom-names-batch] 1회차 · `get_product_measurements` `{"product_id": "prd_wool_overcoat", "sizes": ["S", "XL"]}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) The size chart has no size S. Next: get_product.
- `business` md-overcoat-runs-small [a2api-acom-names-batch] 1회차 · `get_review_summary` `{"product_id": "prd_wool_overcoat", "size": "S", "sample_limit": 3}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) No reviews match these conditions; widen the height range or size. Next: get_product_measurements.
- `model:ungrounded` mgr-what-needs-me-today [a2api-acom-names-norelated] 1회차 · `list_notifications` `{"customer_id": "me", "limit": 20}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no customer me. Next: search_members.
- `model:ungrounded` mgr-what-needs-me-today [a2api-acom-names-batch] 1회차 · `list_notifications` `{"customer_id": "me", "limit": 20}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no customer me. Next: search_members.
- `unclear` md-overcoat-runs-small [a2api-acom-names-norelated] 2회차 · `get_product_measurements` `{"product_id": "prd_wool_overcoat", "sizes": ["S", "XL"]}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) The size chart has no size S. Next: get_product.
- `model:ungrounded` mgr-what-needs-me-today [a2api-acom-names-norelated] 2회차 · `list_notifications` `{"customer_id": "me", "limit": 20}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no customer me. Next: search_members.
- `model:ungrounded` mgr-what-needs-me-today [a2api-acom-names-batch] 2회차 · `list_notifications` `{"customer_id": "me", "limit": 20}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no customer me. Next: search_members.

## 기대와 다른 쓰기 입력

- b1-vip-weekend-sale [a2api-acom] 1회차 · `set_sale_prices` 기대 {"valid_for_member_tier": "vip", "percent_off": 20} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom] 1회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom] 1회차 · `schedule_banner` 기대 {"slot_id": "slot_home_hero"} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-names-norelated] 1회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-names-batch] 1회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-names-batch] 1회차 · `schedule_banner` 기대 {"slot_id": "slot_home_hero"} · 부르지 않음
- b2-returns-over-200 [a2api-acom] 1회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom] 1회차 · `send_customer_message` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names-norelated] 1회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names-norelated] 1회차 · `send_customer_message` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names-batch] 1회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names-batch] 1회차 · `send_customer_message` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-names-norelated] 2회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-names-batch] 2회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom] 2회차 · `set_sale_prices` 기대 {"valid_for_member_tier": "vip", "percent_off": 20} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom] 2회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom] 2회차 · `schedule_banner` 기대 {"slot_id": "slot_home_hero"} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names-norelated] 2회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names-norelated] 2회차 · `send_customer_message` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names-batch] 2회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names-batch] 2회차 · `send_customer_message` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom] 2회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom] 2회차 · `send_customer_message` 기대 {} · 부르지 않음
