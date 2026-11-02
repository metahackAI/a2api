# 호출 단계 리뷰 — ours-held_out-facade2-1

판정 기준 함수 정의: `ours-held_out-facade2-1.functions.json`(실행 때 모델이 본 것)

단계: A0 API에 해당 기능 없음 · A 필요한 함수를 받지 못함 · B 받았지만 부르지 않음 · C 불렀지만 성공 못 함 · D 한도·오류로 중단 · E-write 쓰기 입력·change set · E-format 숫자는 있으나 표기 · E-content 답 내용 누락

## 필요한 함수: 확보 → 호출 → 성공

| 방식 | 통과 | 필요한 함수(API에 있음/전체) | 모델에게 줌 | 불렀음 | 성공 | 확보 기록 |
|---|---|---|---|---|---|---|
| a2api-facade-all | 12/32 | 16/32 | 16/16 (100%) | 16/16 (100%) | 16/16 (100%) | 단계별 기록 |

## 실패한 실행이 처음 막힌 단계

| 방식 | passed | A0 | A | B | C | D | E-write | E-format | E-content |
|---|---|---|---|---|---|---|---|---|---|
| a2api-facade-all | 12 | 9 | 0 | 0 | 0 | 5 | 0 | 0 | 6 |

## 실패한 업무 호출의 원인

| 방식 | 업무 호출 | 실패 | model:schema | model:function | model:ungrounded | model:described | source:undocumented | business | unclear |
|---|---|---|---|---|---|---|---|---|---|
| a2api-facade-all | 189 | 6 | 0 | 0 | 1 | 1 | 0 | 2 | 2 |

## 실패한 호출 목록

- `business` mk-category-promotion [a2api-facade-all] 1회차 · `facade_save_promotion_list` `{"rows": [{"row_action": "insert", "promotion_name": "Outerwear $50 Off Orders $250+", "promotion_type": "order_discount", "starts_at": "2026-11-06T00:00", "ends_at": "2026-11-20T23:59", "applies_to":` → UPSTREAM_CONFLICT: The backend reported that the current state does not allow this request. (HTTP 409) Row 1: Promotion type not available on this screen.
- `business` mk-winback [a2api-facade-all] 2회차 · `facade_save_promotion_list` `{"rows": [{"row_action": "insert", "promotion_name": "Win-back 15% off", "promotion_type": "order_discount", "target_member_grade": "G00", "starts_at": "2026-11-06T00:00:00-05:00", "ends_at": "2026-12` → UPSTREAM_CONFLICT: The backend reported that the current state does not allow this request. (HTTP 409) Row 1: Promotion type not available on this screen.
- `model:ungrounded` md-broken-sizes-outerwear [a2api-facade-all] 2회차 · `facade_get_product_grid_list_count` `{"category_id": "cat_winter_outerwear"}` → RESOURCE_NOT_FOUND: The backend reported that the target does not exist. (HTTP 404) There is no category cat_winter_outerwear.
- `unclear` md-best-sellers-this-month [a2api-facade-all] 2회차 · `facade_get_sale_analysis_grid_list` `{"from_date": "2026-11-01", "to_date": "2026-11-30", "compare_to": "previous_period"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) The period ends on 2026-11-30, after today (2026-11-06); sales after today are not known yet.
- `model:described` mgr-undo-banner [a2api-facade-all] 2회차 · `facade_save_display_banner_list` `{"rows": [{"row_action": "insert", "corner_id": "slot_home_hero", "target_member_grade": "G00", "starts_at": "2026-11-06T11:00", "ends_at": "2026-11-13T23:59", "headline": "The October edit"}]}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) Row 1: `button_label` is required.
- `unclear` mgr-how-is-business [a2api-facade-all] 2회차 · `facade_get_sale_analysis_grid_list` `{"from_date": "2026-10-30", "to_date": "2026-11-06", "compare_to": "same_weekday_last_4_weeks"}` → UPSTREAM_VALIDATION_FAILED: The backend rejected the request values. (HTTP 422) same_weekday_last_4_weeks compares periods of 7 days at most; this one has 8. Use previous_period or custom.
