# 호출 단계 리뷰 — ours-design-7

판정 기준 함수 정의: `ours-design-7.functions.json`(실행 때 모델이 본 것)

단계: A0 API에 해당 기능 없음 · A 필요한 함수를 받지 못함 · B 받았지만 부르지 않음 · C 불렀지만 성공 못 함 · D-before 필요한 함수를 부르기 전 한도·오류로 중단 · D-after 필요한 함수는 모두 성공했는데 답하기 전 한도로 중단 · E-write 쓰기 입력·change set · E-format 숫자는 있으나 표기 · E-content 답 내용 누락

## 필요한 함수: 확보 → 호출 → 성공

| 방식 | 통과 | 필요한 함수(API에 있음/전체) | 모델에게 줌 | 불렀음 | 성공 | 확보 기록 |
|---|---|---|---|---|---|---|
| a2api-acom | 6/24 | 42/42 | 34/42 (81%) | 28/42 (67%) | 28/42 (67%) | 불러오기·검색 결과로 추정 |
| a2api-acom-index | 12/24 | 42/42 | 35/42 (83%) | 33/42 (79%) | 32/42 (76%) | 불러오기·검색 결과로 추정 |
| a2api-acom-graph | 10/24 | 42/42 | 34/42 (81%) | 32/42 (76%) | 32/42 (76%) | 불러오기·검색 결과로 추정 |
| a2api-acom-names | 10/24 | 42/42 | 33/42 (79%) | 31/42 (74%) | 31/42 (74%) | 불러오기·검색 결과로 추정 |

## 실패한 실행이 처음 막힌 단계

| 방식 | passed | A0 | A | B | C | D-before | D-after | E-write | E-format | E-content |
|---|---|---|---|---|---|---|---|---|---|---|
| a2api-acom | 6 | 0 | 6 | 0 | 0 | 0 | 6 | 0 | 4 | 2 |
| a2api-acom-index | 12 | 0 | 5 | 0 | 0 | 0 | 3 | 0 | 2 | 2 |
| a2api-acom-graph | 10 | 0 | 5 | 0 | 0 | 1 | 3 | 0 | 2 | 3 |
| a2api-acom-names | 10 | 0 | 5 | 0 | 0 | 1 | 4 | 0 | 2 | 2 |

## 실패한 업무 호출의 원인

| 방식 | 업무 호출 | 실패 | model:schema | model:function | model:ungrounded | model:described | source:undocumented | business | unclear |
|---|---|---|---|---|---|---|---|---|---|
| a2api-acom | 119 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| a2api-acom-index | 126 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| a2api-acom-graph | 130 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| a2api-acom-names | 136 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |

## 쓰기 입력(과업이 기대한 change set 항목)

| 방식 | 기대 항목 | 불렀음 | 입력 일치 |
|---|---|---|---|
| a2api-acom | 12 | 2 | 2 |
| a2api-acom-index | 12 | 4 | 4 |
| a2api-acom-graph | 12 | 4 | 4 |
| a2api-acom-names | 12 | 5 | 5 |

## 실패한 호출 목록

- `unclear` b1-vip-weekend-sale [a2api-acom-index] 1회차 · `schedule_banner` `{"slot_id": "slot_home_hero", "audience": "vip", "valid_from": "2026-11-07T00:00", "valid_through": "2026-11-08T23:59", "content": {"eyebrow": "VIP WEEKEND", "headline": "20% off summer outerwear", "c` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no image bnr_vip_weekend_summer. Next: search_products.
- `model:schema` mgr-what-needs-me-today [a2api-acom-names] 1회차 · `search_inquiries` `{"status": ["received", "in_progress"], "created_from": "2026-11-06", "limit": 100}` → INVALID_INPUT: Value does not conform to the declared schema. issues [{"path": "/status", "rule": "type", "expected": "string"}, {"path": "/status", "rule": "enum", "expected": ["received", "in_progress", "resolved"]}]
- `unclear` md-overcoat-runs-small [a2api-acom-index] 2회차 · `get_product_measurements` `{"product_id": "prd_wool_overcoat", "sizes": ["S", "XL"]}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) The size chart has no size S. Next: get_product.

## 기대와 다른 쓰기 입력

- b1-vip-weekend-sale [a2api-acom] 1회차 · `set_sale_prices` 기대 {"valid_for_member_tier": "vip", "percent_off": 20} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom] 1회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom] 1회차 · `schedule_banner` 기대 {"slot_id": "slot_home_hero"} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-index] 1회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-graph] 1회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-graph] 1회차 · `schedule_banner` 기대 {"slot_id": "slot_home_hero"} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-names] 1회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-names] 1회차 · `schedule_banner` 기대 {"slot_id": "slot_home_hero"} · 부르지 않음
- b2-returns-over-200 [a2api-acom-graph] 1회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-graph] 1회차 · `send_customer_message` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names] 1회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names] 1회차 · `send_customer_message` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom] 1회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom] 1회차 · `send_customer_message` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-index] 1회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-index] 1회차 · `send_customer_message` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-index] 2회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-index] 2회차 · `schedule_banner` 기대 {"slot_id": "slot_home_hero"} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-graph] 2회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom-names] 2회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom] 2회차 · `set_sale_prices` 기대 {"valid_for_member_tier": "vip", "percent_off": 20} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom] 2회차 · `create_coupon` 기대 {} · 부르지 않음
- b1-vip-weekend-sale [a2api-acom] 2회차 · `schedule_banner` 기대 {"slot_id": "slot_home_hero"} · 부르지 않음
- md-end-of-season-markdown [a2api-acom-graph] 2회차 · `set_sale_prices` 기대 {"valid_for_member_tier": "everyone", "scope_mode": "category", "category_id": "cat_tees", "exclude_low_stock": true} · 부르지 않음
- md-end-of-season-markdown [a2api-acom-index] 2회차 · `set_sale_prices` 기대 {"valid_for_member_tier": "everyone", "scope_mode": "category", "category_id": "cat_tees", "exclude_low_stock": true} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names] 2회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-names] 2회차 · `send_customer_message` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom] 2회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom] 2회차 · `send_customer_message` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-index] 2회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-index] 2회차 · `send_customer_message` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-graph] 2회차 · `refund_return` 기대 {} · 부르지 않음
- b2-returns-over-200 [a2api-acom-graph] 2회차 · `send_customer_message` 기대 {} · 부르지 않음
