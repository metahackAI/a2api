# 호출 단계 리뷰 — ours-held_out-settings-recent-1-merged

판정 기준 함수 정의: `ours-held_out-settings-recent-1-merged.functions.json`(실행 때 모델이 본 것)

단계: A0 API에 해당 기능 없음 · A 필요한 함수를 받지 못함 · B 받았지만 부르지 않음 · C 불렀지만 성공 못 함 · D-before 필요한 함수를 부르기 전 한도·오류로 중단 · D-after 필요한 함수는 모두 성공했는데 답하기 전 한도로 중단 · E-write 쓰기 입력·change set · E-format 숫자는 있으나 표기 · E-content 답 내용 누락

## 필요한 함수: 확보 → 호출 → 성공

| 방식 | 통과 | 필요한 함수(API에 있음/전체) | 모델에게 줌 | 불렀음 | 성공 | 확보 기록 |
|---|---|---|---|---|---|---|
| a2api-acom | 8/32 | 32/32 | 22/32 (69%) | 20/32 (62%) | 20/32 (62%) | 단계별 기록 |
| a2api-acom-names-batch | 8/32 | 32/32 | 29/32 (91%) | 28/32 (88%) | 28/32 (88%) | 단계별 기록 |

## 실패한 실행이 처음 막힌 단계

| 방식 | passed | A0 | A | B | C | D-before | D-after | E-write | E-format | E-content |
|---|---|---|---|---|---|---|---|---|---|---|
| a2api-acom | 8 | 0 | 10 | 1 | 0 | 0 | 6 | 2 | 1 | 4 |
| a2api-acom-names-batch | 8 | 0 | 3 | 0 | 0 | 1 | 9 | 1 | 1 | 9 |

## 실패한 업무 호출의 원인

| 방식 | 업무 호출 | 실패 | model:schema | model:function | model:ungrounded | model:described | source:undocumented | business | unclear |
|---|---|---|---|---|---|---|---|---|---|
| a2api-acom | 143 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| a2api-acom-names-batch | 174 | 3 | 0 | 0 | 1 | 0 | 0 | 1 | 1 |

## 쓰기 입력(과업이 기대한 change set 항목)

| 방식 | 기대 항목 | 불렀음 | 입력 일치 |
|---|---|---|---|
| a2api-acom | 4 | 4 | 2 |
| a2api-acom-names-batch | 4 | 3 | 2 |

## 실패한 호출 목록

- `business` md-broken-sizes-outerwear [a2api-acom-names-batch] 1회차 · `get_inventory` `{"product_id": "prd_outerwear_05", "fields": ["product_id", "variants"]}` → TOOL_CALL_LIMIT: {"error":"tool call limit reached for this turn"}
- `model:ungrounded` ops-photo-request [a2api-acom-names-batch] 1회차 · `get_inquiry` `{"inquiry_id": "inq_20366"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no inquiry inq_20366. Next: search_inquiries.
- `unclear` mgr-undo-banner [a2api-acom] 2회차 · `acom_schedule_display` `{"slot_id": "slot_home_hero", "audience": "everyone", "valid_from": "2026-11-06T11:00", "valid_through": "2026-11-06T23:59"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Home hero holds no items to show; arrange it first. Next: arrange_display_slot.
- `unclear` mgr-undo-banner [a2api-acom] 2회차 · `acom_schedule_display` `{"slot_id": "slot_home_hero", "audience": "everyone", "valid_from": "2026-11-06T11:00", "valid_through": "2026-11-06T23:59", "channels": ["web", "mobile_web", "app"]}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Home hero holds no items to show; arrange it first. Next: arrange_display_slot.
- `unclear` mgr-weekly-summary [a2api-acom-names-batch] 2회차 · `get_sales_overview` `{"valid_from": "2026-10-31", "valid_through": "2026-11-06", "acom:metrics": ["revenue", "order_count", "average_order_value", "cancellation_rate", "return_rate"], "acom:dimensions": ["category", "memb` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) cancellation_rate cannot be split by category_id: it counts whole orders. Split it by member_tier, or leave it out. Next: get_sales_overview.

## 기대와 다른 쓰기 입력

- ops-photo-request [a2api-acom] 1회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
- ops-photo-request [a2api-acom-names-batch] 1회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 부르지 않음
- ops-photo-request [a2api-acom-names-batch] 2회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
- ops-photo-request [a2api-acom] 2회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
