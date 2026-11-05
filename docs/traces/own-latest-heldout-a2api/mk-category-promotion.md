# mk-category-promotion — own-latest-heldout-a2api

[← 실행 묶음](README.md)

**과업**

> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 답에 있어야 할 사실: 2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store time

### a2api 변환 파사드 · 1회차 · ✗ 실패

토큰 3,330 · 모델 호출 1회 · 도구 호출 2회

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 6 candidates: save_promotion_list, save_coupon_list, get_promotion_grid_list_count, get_promotion_grid_list, get_promotion_target_member_list, get_promotion_target_member_list_count
- 계획: `get_promotion_grid_list` `` {"page":1,"page_size":20,"promotion_name":"Outerwear"} ``; `save_promotion_list` `` {"rows":[{"ends_at":"2026-11-20T23:59","starts_at":"2026-11-06T11:00","applies_to":"category","row_action":"insert","category_id":"cat","promotion_name":"Outerwear $50 off orders above $250","promotion_type":"order_discount"}]} ``
1. 에이전트 → **`get_promotion_grid_list`** `` {"page":1,"page_size":20,"promotion_name":"Outerwear"} ``
   ← 결과: `` {"list":[],"page":1,"page_size":20} ``
2. 에이전트 → **`save_promotion_list`** `` {"rows":[{"ends_at":"2026-11-20T23:59:00-05:00","starts_at":"2026-11-06T11:00:00-05:00","applies_to":"category","row_action":"insert","category_id":"cat","promotion_name":"Outerwear $50 off orders above $250","promotion_type":"order_discount"}]} ``
   ← 실패: `` {"code":"upstream_conflict","class":"invalid_state","message":"The backend reported that the current state does not allow this request. (HTTP 409) Row 1: Promotion type not available on this screen.","next_tool":null} ``

**답변 1**
> save_promotion_list failed: The backend reported that the current state does not allow this request. (HTTP 409) Row 1: Promotion type not available on this screen.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (2, 6, 19, 23, 59 not shown)

### a2api 변환 파사드 · 2회차 · ✗ 실패

토큰 3,335 · 모델 호출 1회 · 도구 호출 2회

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 6 candidates: save_promotion_list, save_coupon_list, get_promotion_grid_list_count, get_promotion_grid_list, get_promotion_target_member_list, get_promotion_target_member_list_count
- 계획: `get_promotion_grid_list` `` {"page":1,"page_size":20,"promotion_name":"Outerwear"} ``; `save_promotion_list` `` {"rows":[{"ends_at":"2026-11-20T23:59","starts_at":"2026-11-06T11:00","applies_to":"category","row_action":"insert","category_id":"cat","promotion_name":"Outerwear $50 off orders above $250","promotion_type":"order_discount"}]} ``
1. 에이전트 → **`get_promotion_grid_list`** `` {"page":1,"page_size":20,"promotion_name":"Outerwear"} ``
   ← 결과: `` {"list":[],"page":1,"page_size":20} ``
2. 에이전트 → **`save_promotion_list`** `` {"rows":[{"ends_at":"2026-11-20T23:59:00-05:00","starts_at":"2026-11-06T11:00:00-05:00","applies_to":"category","row_action":"insert","category_id":"cat","promotion_name":"Outerwear $50 off orders above $250","promotion_type":"order_discount"}]} ``
   ← 실패: `` {"code":"upstream_conflict","class":"invalid_state","message":"The backend reported that the current state does not allow this request. (HTTP 409) Row 1: Promotion type not available on this screen.","next_tool":null} ``

**답변 1**
> save_promotion_list failed: The backend reported that the current state does not allow this request. (HTTP 409) Row 1: Promotion type not available on this screen.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (2, 6, 19, 23, 59 not shown)

### a2api 변환 파사드 · 3회차 · ✗ 실패

토큰 3,335 · 모델 호출 1회 · 도구 호출 2회

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 라우팅: Promotion agent (the request names this agent's work)
- 도구 검색 후보: 6 candidates: save_promotion_list, save_coupon_list, get_promotion_grid_list_count, get_promotion_grid_list, get_promotion_target_member_list, get_promotion_target_member_list_count
- 계획: `get_promotion_grid_list` `` {"page":1,"page_size":20,"promotion_name":"Outerwear"} ``; `save_promotion_list` `` {"rows":[{"ends_at":"2026-11-20T23:59","starts_at":"2026-11-06T11:00","applies_to":"category","row_action":"insert","category_id":"cat","promotion_name":"Outerwear $50 off orders above $250","promotion_type":"order_discount"}]} ``
1. 에이전트 → **`get_promotion_grid_list`** `` {"page":1,"page_size":20,"promotion_name":"Outerwear"} ``
   ← 결과: `` {"list":[],"page":1,"page_size":20} ``
2. 에이전트 → **`save_promotion_list`** `` {"rows":[{"ends_at":"2026-11-20T23:59:00-05:00","starts_at":"2026-11-06T11:00:00-05:00","applies_to":"category","row_action":"insert","category_id":"cat","promotion_name":"Outerwear $50 off orders above $250","promotion_type":"order_discount"}]} ``
   ← 실패: `` {"code":"upstream_conflict","class":"invalid_state","message":"The backend reported that the current state does not allow this request. (HTTP 409) Row 1: Promotion type not available on this screen.","next_tool":null} ``

**답변 1**
> save_promotion_list failed: The backend reported that the current state does not allow this request. (HTTP 409) Row 1: Promotion type not available on this screen.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (2, 6, 19, 23, 59 not shown)
