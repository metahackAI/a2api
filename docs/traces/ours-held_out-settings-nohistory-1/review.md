# 호출 단계 리뷰 — ours-held_out-settings-nohistory-1

판정 기준 함수 정의: `ours-held_out-settings-nohistory-1.functions.json`(실행 때 모델이 본 것)

단계: A0 API에 해당 기능 없음 · A 필요한 함수를 받지 못함 · B 받았지만 부르지 않음 · C 불렀지만 성공 못 함 · D 한도·오류로 중단 · E-write 쓰기 입력·change set · E-format 숫자는 있으나 표기 · E-content 답 내용 누락

## 필요한 함수: 확보 → 호출 → 성공

| 방식 | 통과 | 필요한 함수(API에 있음/전체) | 모델에게 줌 | 불렀음 | 성공 | 확보 기록 |
|---|---|---|---|---|---|---|
| a2api-acom | 5/32 | 32/32 | 27/32 (84%) | 20/32 (62%) | 20/32 (62%) | 단계별 기록 |
| a2api-acom-names-batch | 7/32 | 32/32 | 28/32 (88%) | 26/32 (81%) | 26/32 (81%) | 단계별 기록 |

## 실패한 실행이 처음 막힌 단계

| 방식 | passed | A0 | A | B | C | D | E-write | E-format | E-content |
|---|---|---|---|---|---|---|---|---|---|
| a2api-acom | 5 | 0 | 5 | 1 | 0 | 13 | 2 | 0 | 6 |
| a2api-acom-names-batch | 7 | 0 | 4 | 0 | 0 | 9 | 2 | 0 | 10 |

## 실패한 업무 호출의 원인

| 방식 | 업무 호출 | 실패 | model:schema | model:function | model:ungrounded | model:described | source:undocumented | business | unclear |
|---|---|---|---|---|---|---|---|---|---|
| a2api-acom | 136 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| a2api-acom-names-batch | 161 | 4 | 0 | 0 | 0 | 2 | 0 | 2 | 0 |

## 쓰기 입력(과업이 기대한 change set 항목)

| 방식 | 기대 항목 | 불렀음 | 입력 일치 |
|---|---|---|---|
| a2api-acom | 4 | 4 | 2 |
| a2api-acom-names-batch | 4 | 3 | 2 |

## 실패한 호출 목록

- `source:undocumented` md-broken-sizes-outerwear [a2api-acom] 1회차 · `acom_search_products` `{"category_id": "cat_outerwear", "limit": 100, "cursor": ""}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) `cursor` must be a `next_cursor` from an earlier page.
- `model:described` md-below-cost [a2api-acom-names-batch] 1회차 · `search_products` `{"query": "", "limit": 100, "fields": ["id", "name", "variants"]}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) `fields` names `variants` this result does not have. Its top-level fields are availability, brand_id, category_id, cost, has_variant, id, image, inventory_level, member
- `business` md-best-sellers-this-month [a2api-acom-names-batch] 1회차 · `get_category` `{"category_id": "cat_underwear", "fields": ["name"]}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `business` md-best-sellers-this-month [a2api-acom-names-batch] 1회차 · `get_category` `{"category_id": "cat_scarves", "fields": ["name"]}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `model:described` md-out-of-stock-30-days [a2api-acom-names-batch] 2회차 · `get_product` `{"product_id": "prd_wool_overcoat", "fields": ["id", "name", "inventory_level", "variants"]}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) `fields` names `variants` this result does not have. Its top-level fields are @type, additional_property, approval_status, availability, brand_id, category_id, cost, de

## 기대와 다른 쓰기 입력

- ops-photo-request [a2api-acom] 1회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
- ops-photo-request [a2api-acom-names-batch] 1회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 부르지 않음
- ops-photo-request [a2api-acom-names-batch] 2회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
- ops-photo-request [a2api-acom] 2회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": "cus_riley", "kind": "ask_for_photos"}]
