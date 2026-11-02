# 호출 단계 리뷰 — ours-heldout-guard-posthoc-1

판정 기준 함수 정의: `ours-heldout-guard-posthoc-1.functions.json`(실행 때 모델이 본 것)

단계: A0 API에 해당 기능 없음 · A 필요한 함수를 받지 못함 · B 받았지만 부르지 않음 · C 불렀지만 성공 못 함 · D 한도·오류로 중단 · E-write 쓰기 입력·change set · E-format 숫자는 있으나 표기 · E-content 답 내용 누락

## 필요한 함수: 확보 → 호출 → 성공

| 방식 | 통과 | 필요한 함수(API에 있음/전체) | 모델에게 줌 | 불렀음 | 성공 | 확보 기록 |
|---|---|---|---|---|---|---|
| a2api-acom | 8/32 | 32/32 | 25/32 (78%) | 21/32 (66%) | 21/32 (66%) | 불러오기·검색 결과로 추정 |
| a2api-acom-guard | 7/32 | 32/32 | 26/32 (81%) | 19/32 (59%) | 19/32 (59%) | 불러오기·검색 결과로 추정 |
| a2api-acom-names-batch | 7/32 | 32/32 | 25/32 (78%) | 23/32 (72%) | 23/32 (72%) | 불러오기·검색 결과로 추정 |
| a2api-acom-names-batch-guard | 7/32 | 32/32 | 28/32 (88%) | 26/32 (81%) | 26/32 (81%) | 불러오기·검색 결과로 추정 |

## 실패한 실행이 처음 막힌 단계

| 방식 | passed | A0 | A | B | C | D | E-write | E-format | E-content |
|---|---|---|---|---|---|---|---|---|---|
| a2api-acom | 8 | 0 | 7 | 2 | 0 | 11 | 2 | 0 | 2 |
| a2api-acom-guard | 7 | 0 | 6 | 4 | 0 | 7 | 2 | 0 | 6 |
| a2api-acom-names-batch | 7 | 0 | 7 | 0 | 0 | 9 | 2 | 1 | 6 |
| a2api-acom-names-batch-guard | 7 | 0 | 4 | 0 | 0 | 10 | 2 | 0 | 9 |

## 실패한 업무 호출의 원인

| 방식 | 업무 호출 | 실패 | model:schema | model:function | model:ungrounded | model:described | source:undocumented | business | unclear |
|---|---|---|---|---|---|---|---|---|---|
| a2api-acom | 126 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| a2api-acom-guard | 102 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| a2api-acom-names-batch | 142 | 16 | 0 | 0 | 16 | 0 | 0 | 0 | 0 |
| a2api-acom-names-batch-guard | 141 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## 쓰기 입력(과업이 기대한 change set 항목)

| 방식 | 기대 항목 | 불렀음 | 입력 일치 |
|---|---|---|---|
| a2api-acom | 4 | 3 | 1 |
| a2api-acom-guard | 4 | 4 | 2 |
| a2api-acom-names-batch | 4 | 4 | 2 |
| a2api-acom-names-batch-guard | 4 | 4 | 2 |

## 실패한 호출 목록

- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 1회차 · `describe_data` `{"schema": "catalog", "table": "catalog.inventory"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches `catalog.inventory`. Next: describe_data.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 1회차 · `describe_data` `{"schema": "catalog", "table": "catalog.product_inventory"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches `catalog.product_inventory`. Next: describe_data.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 1회차 · `describe_data` `{"api_name": "variant_id"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches ``. Next: describe_data.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 1회차 · `describe_data` `{"schema": "catalog", "api_name": "stock"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches ``. Next: describe_data.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 1회차 · `describe_data` `{"api_name": "out_of_stock_since"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches ``. Next: describe_data.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 1회차 · `describe_data` `{"schema": "catalog", "table": "catalog.variant_stock"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches `catalog.variant_stock`. Next: describe_data.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 1회차 · `describe_data` `{"schema": "catalog", "table": "catalog.stock"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches `catalog.stock`. Next: describe_data.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 1회차 · `describe_data` `{"schema": "catalog", "table": "catalog.inventory"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches `catalog.inventory`. Next: describe_data.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 2회차 · `describe_data` `{"schema": "catalog", "table": "catalog.inventory"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches `catalog.inventory`. Next: describe_data.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 2회차 · `describe_data` `{"schema": "catalog", "table": "catalog.product_inventory"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches `catalog.product_inventory`. Next: describe_data.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 2회차 · `describe_data` `{"api_name": "variant_id"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches ``. Next: describe_data.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 2회차 · `describe_data` `{"schema": "catalog", "api_name": "stock"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches ``. Next: describe_data.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 2회차 · `describe_data` `{"api_name": "out_of_stock_since"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches ``. Next: describe_data.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 2회차 · `describe_data` `{"schema": "catalog", "table": "catalog.variant_stock"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches `catalog.variant_stock`. Next: describe_data.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 2회차 · `describe_data` `{"schema": "catalog", "table": "catalog.stock"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches `catalog.stock`. Next: describe_data.
- `model:ungrounded` md-out-of-stock-30-days [a2api-acom-names-batch] 2회차 · `describe_data` `{"schema": "catalog", "table": "catalog.inventory"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) Nothing in the data dictionary matches `catalog.inventory`. Next: describe_data.

## 기대와 다른 쓰기 입력

- mk-pause-knit-until-monday [a2api-acom] 1회차 · `pause_promotion` 기대 {"promotion_id": "promo_autumn_knit"} · 부르지 않음
- ops-photo-request [a2api-acom-names-batch] 1회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": "cus_riley", "kind": "ask_for_photos"}]
- ops-photo-request [a2api-acom-names-batch-guard] 1회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
- ops-photo-request [a2api-acom] 1회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
- ops-photo-request [a2api-acom-guard] 1회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
- ops-photo-request [a2api-acom-names-batch-guard] 2회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
- ops-photo-request [a2api-acom] 2회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
- ops-photo-request [a2api-acom-guard] 2회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
- ops-photo-request [a2api-acom-names-batch] 2회차 · `send_customer_message` 기대 {"customer_id": "cus_riley", "kind": "photo_request"} · 불일치: [{"customer_id": null, "kind": "ask_for_photos"}]
