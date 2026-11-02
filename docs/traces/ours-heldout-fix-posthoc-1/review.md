# 호출 단계 리뷰 — ours-heldout-fix-posthoc-1

판정 기준 함수 정의: `ours-heldout-fix-posthoc-1.functions.json`(실행 때 모델이 본 것)

단계: A0 API에 해당 기능 없음 · A 필요한 함수를 받지 못함 · B 받았지만 부르지 않음 · C 불렀지만 성공 못 함 · D-before 필요한 함수를 부르기 전 한도·오류로 중단 · D-after 필요한 함수는 모두 성공했는데 답하기 전 한도로 중단 · E-write 쓰기 입력·change set · E-format 숫자는 있으나 표기 · E-content 답 내용 누락

## 필요한 함수: 확보 → 호출 → 성공

| 방식 | 통과 | 필요한 함수(API에 있음/전체) | 모델에게 줌 | 불렀음 | 성공 | 확보 기록 |
|---|---|---|---|---|---|---|
| a2api-acom | 9/32 | 32/32 | 28/32 (88%) | 21/32 (66%) | 21/32 (66%) | 불러오기·검색 결과로 추정 |
| a2api-acom-names-norelated | 5/32 | 32/32 | 28/32 (88%) | 27/32 (84%) | 27/32 (84%) | 불러오기·검색 결과로 추정 |
| a2api-acom-names-batch | 5/32 | 32/32 | 28/32 (88%) | 26/32 (81%) | 26/32 (81%) | 불러오기·검색 결과로 추정 |

## 실패한 실행이 처음 막힌 단계

| 방식 | passed | A0 | A | B | C | D-before | D-after | E-write | E-format | E-content |
|---|---|---|---|---|---|---|---|---|---|---|
| a2api-acom | 9 | 0 | 4 | 2 | 0 | 4 | 6 | 2 | 0 | 5 |
| a2api-acom-names-norelated | 5 | 0 | 4 | 0 | 0 | 0 | 9 | 2 | 2 | 10 |
| a2api-acom-names-batch | 5 | 0 | 4 | 0 | 0 | 1 | 10 | 2 | 0 | 10 |

## 실패한 업무 호출의 원인

| 방식 | 업무 호출 | 실패 | model:schema | model:function | model:ungrounded | model:described | source:undocumented | business | unclear |
|---|---|---|---|---|---|---|---|---|---|
| a2api-acom | 120 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| a2api-acom-names-norelated | 165 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| a2api-acom-names-batch | 155 | 9 | 0 | 0 | 8 | 0 | 0 | 0 | 1 |

## 쓰기 입력(과업이 기대한 change set 항목)

| 방식 | 기대 항목 | 불렀음 | 입력 일치 |
|---|---|---|---|
| a2api-acom | 4 | 4 | 2 |
| a2api-acom-names-norelated | 4 | 4 | 2 |
| a2api-acom-names-batch | 4 | 4 | 2 |

## 실패한 호출 목록

- `unclear` mk-winback [a2api-acom-names-batch] 1회차 · `preview_segment` `{"condition_rules": {"last_order_within_days": 90, "exclude_segment_ids": ["seg_recent_90_buyers"]}, "sample_size": 5}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no segment seg_recent_90_buyers. Next: list_segments.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 1회차 · `describe_data` `{"schema": "catalog", "table": "catalog.inventory"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches `catalog.inventory`. Next: describe_data.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 1회차 · `describe_data` `{"schema": "catalog", "table": "catalog.product_inventory"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches `catalog.product_inventory`. Next: describe_data.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 1회차 · `describe_data` `{"api_name": "variant_id"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches ``. Next: describe_data.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 1회차 · `describe_data` `{"schema": "catalog", "api_name": "stock"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches ``. Next: describe_data.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 1회차 · `describe_data` `{"api_name": "out_of_stock_since"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches ``. Next: describe_data.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 1회차 · `describe_data` `{"schema": "catalog", "table": "catalog.variant_stock"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches `catalog.variant_stock`. Next: describe_data.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 1회차 · `describe_data` `{"schema": "catalog", "table": "catalog.stock"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches `catalog.stock`. Next: describe_data.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 1회차 · `describe_data` `{"schema": "catalog", "table": "catalog.inventory"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches `catalog.inventory`. Next: describe_data.

## 기대와 다른 쓰기 입력

- ops-photo-request [a2api-acom-names-norelated] 1회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
- ops-photo-request [a2api-acom-names-batch] 1회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
- ops-photo-request [a2api-acom] 1회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
- ops-photo-request [a2api-acom-names-batch] 2회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": "cus_riley", "kind": "ask_for_photos"}]
- ops-photo-request [a2api-acom] 2회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
- ops-photo-request [a2api-acom-names-norelated] 2회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
