# 호출 단계 리뷰 — ours-design-facade2-1

판정 기준 함수 정의: `ours-design-facade2-1.functions.json`(실행 때 모델이 본 것)

단계: A0 API에 해당 기능 없음 · A 필요한 함수를 받지 못함 · B 받았지만 부르지 않음 · C 불렀지만 성공 못 함 · D-before 필요한 함수를 부르기 전 한도·오류로 중단 · D-after 필요한 함수는 모두 성공했는데 답하기 전 한도로 중단 · E-write 쓰기 입력·change set · E-format 숫자는 있으나 표기 · E-content 답 내용 누락

## 필요한 함수: 확보 → 호출 → 성공

| 방식 | 통과 | 필요한 함수(API에 있음/전체) | 모델에게 줌 | 불렀음 | 성공 | 확보 기록 |
|---|---|---|---|---|---|---|
| a2api-facade-all | 4/24 | 28/42 | 28/28 (100%) | 24/28 (86%) | 24/28 (86%) | 단계별 기록 |

## 실패한 실행이 처음 막힌 단계

| 방식 | passed | A0 | A | B | C | D-before | D-after | E-write | E-format | E-content |
|---|---|---|---|---|---|---|---|---|---|---|
| a2api-facade-all | 4 | 14 | 0 | 0 | 0 | 2 | 4 | 0 | 0 | 0 |

## 실패한 업무 호출의 원인

| 방식 | 업무 호출 | 실패 | model:schema | model:function | model:ungrounded | model:described | source:undocumented | business | unclear |
|---|---|---|---|---|---|---|---|---|---|
| a2api-facade-all | 220 | 7 | 0 | 0 | 6 | 0 | 0 | 0 | 1 |

## 실패한 호출 목록

- `unclear` md-low-stock-before-weekend [a2api-facade-all] 1회차 · `facade_get_sale_analysis_grid_list` `{"from_date": "2026-10-30", "to_date": "2026-11-06", "compare_to": "same_weekday_last_4_weeks"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) same_weekday_last_4_weeks compares periods of 7 days at most; this one has 8. Use previous_period or custom.
- `model:ungrounded` mgr-what-changed-this-morning [a2api-facade-all] 1회차 · `facade_get_display_corner_list` `{"page_type": "category", "starts_at": "2026-11-06T00:00", "ends_at": "2026-11-06T23:59"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) The category page has no display slots.
- `model:ungrounded` mgr-what-changed-this-morning [a2api-facade-all] 1회차 · `facade_get_display_corner_list` `{"page_type": "product", "starts_at": "2026-11-06T00:00", "ends_at": "2026-11-06T23:59"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) The product page has no display slots.
- `model:ungrounded` mgr-what-changed-this-morning [a2api-facade-all] 1회차 · `facade_get_display_corner_list` `{"page_type": "search", "starts_at": "2026-11-06T00:00", "ends_at": "2026-11-06T23:59"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) The search page has no display slots.
- `model:ungrounded` mgr-what-changed-this-morning [a2api-facade-all] 2회차 · `facade_get_display_corner_list` `{"page_type": "category", "starts_at": "2026-11-06T00:00", "ends_at": "2026-11-06T23:59"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) The category page has no display slots.
- `model:ungrounded` mgr-what-changed-this-morning [a2api-facade-all] 2회차 · `facade_get_display_corner_list` `{"page_type": "product", "starts_at": "2026-11-06T00:00", "ends_at": "2026-11-06T23:59"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) The product page has no display slots.
- `model:ungrounded` mgr-what-changed-this-morning [a2api-facade-all] 2회차 · `facade_get_display_corner_list` `{"page_type": "search", "starts_at": "2026-11-06T00:00", "ends_at": "2026-11-06T23:59"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) The search page has no display slots.
