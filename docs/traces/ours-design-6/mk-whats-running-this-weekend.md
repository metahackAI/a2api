# mk-whats-running-this-weekend — ours-design-6

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `20f2d63`

**과업**

> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 필요한 도구: `list_active_promotions`
- 허용 도구: `get_promotion`, `search_promotions`
- 답에 있어야 할 사실: four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwear 15% (everyone, until Nov 15), Birthday coupon (members), Free shipping over $80 (everyone), Gold tier 10% (gold)
- 답에 있어야 할 사실: the knit sale covers 26 knitwear products

### a2api-acom · 1회차 · E MODEL_CALL_LIMIT

토큰 77,597 · 75.569초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 3,773토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`acom_list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"} ``
   ← 결과 1,164B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"applies_to":{"scope":"order","category_ids":[],"prod… (+564자) ``
2. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``
3. 모델 → **`a2api_search`** `` {"query":"stack promotion discount layer"} ``
   ← 결과 517B: `` {"selected":[{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_update_promotion","id":"acom.update_promotion"},{"name":"acom_calculate_benefits","id":"acom.calculate_benefits"}],"evicted":["acom_explain_sales_change","acom_describe_data","acom_schedule_display","acom_set_price","acom_get_curation"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_birthday"} ``
   ← 결과 522B: `` {"status":"succeeded","data":{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"$10.00 off one order in the member's birthday month.","percent_off":null,"amount_off":{"value":10.0,"currency":"USD"},"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_birthday"],"change_set_id":null,"version":1}} ``
5. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_free_ship_80"} ``
   ← 결과 521B: `` {"status":"succeeded","data":{"id":"promo_free_ship_80","name":"Free shipping over $80","status":"running","discount_layer":"add_on","valid_for_member_tier":"everyone","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Free standard shipping when the item subtotal before member benefits is $80.00 or more.","percent_off":null,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":[],"change_set_id":null,"version":1}} ``
6. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_gold_10"} ``
   ← 결과 483B: `` {"status":"succeeded","data":{"id":"promo_gold_10","name":"Gold tier 10%","status":"running","discount_layer":"order_discount","valid_for_member_tier":"gold","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Gold members get a 10% order coupon every month.","percent_off":10,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_gold_10"],"change_set_id":null,"version":1}} ``
7. 모델 → **`a2api_search`** `` {"query":"stacking"} ``
   ← 결과 304B: `` {"selected":[{"name":"acom_create_coupon","id":"acom.create_coupon"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match was already offered in this conversation. If they cannot answer, tell the user what is missing instead of searching again."} ``
8. 모델 → **`a2api_search`** `` {"query":"coupon"} ``
   ← 결과 464B: `` {"selected":[{"name":"acom_search_coupons","id":"acom.search_coupons"},{"name":"acom_list_member_coupons","id":"acom.list_member_coupons"},{"name":"acom_revoke_coupon","id":"acom.revoke_coupon"},{"name":"acom_get_coupon","id":"acom.get_coupon"},{"name":"acom_create_coupon","id":"acom.create_coupon"}],"evicted":["acom_get_display_slot","acom_list_active_promotions","acom_search_promotions"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
9. 모델 → **`acom_search_coupons`** `` {"promotion_id":"promo_birthday"} ``
   ← 결과 300B: `` {"status":"succeeded","data":{"items":[{"id":"cpn_birthday","code":"BIRTHDAY10","name":"Birthday coupon","promotion_id":"promo_birthday","valid_for_member_tier":"member","application":"download","stacking":"no_other_coupons","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null}],"total":1}} ``
10. 모델 → **`acom_search_coupons`** `` {"promotion_id":"promo_gold_10"} ``
   ← 결과 290B: `` {"status":"succeeded","data":{"items":[{"id":"cpn_gold_10","code":"GOLD10","name":"Gold tier 10%","promotion_id":"promo_gold_10","valid_for_member_tier":"gold","application":"download","stacking":"no_other_coupons","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null}],"total":1}} ``
11. 모델 → **`a2api_search`** `` {"query":"stacking policy"} ``
   ← 결과 399B: `` {"selected":[{"name":"acom_list_policies","id":"acom.list_policies"},{"name":"acom_get_return_policy","id":"acom.get_return_policy"},{"name":"acom_get_policy","id":"acom.get_policy"},{"name":"acom_get_action_log","id":"acom.get_action_log"},{"name":"acom_get_tenant","id":"acom.get_tenant"}],"evicted":["acom_create_promotion"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
12. 모델 → **`acom_list_policies`** `` {"domain":"promotion"} ``
   ← 결과 224B: `` {"status":"succeeded","data":{"items":[{"file":"promotion","version":3,"domain":"promotion","summary":"Discount caps, minimum stock, overlap and coupon rules","overridden_keys":1}],"total":1,"policy_version":"918b3118ff2e"}} ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8, 15, 15, 80, 10 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.62, 재현율 1.00)

### a2api-facade · 1회차 · ✗ 실패

토큰 52,571 · 113.608초 · 모델 호출 10회 · 도구 호출 9회 · 첫 요청 프롬프트 2,850토큰

준비: 전략 `search`, 함수 8개

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`facade_get_prmt_grid_list`** `` {"promotion_status":"running","active_from":"2026-11-07","active_until":"2026-11-08","page":1,"page_size":100} ``
   ← 결과 960B: `` {"status":"succeeded","data":{"list":[{"promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00","starts_at":"2026-11-01T00:00:00-04:00","ends_at":"2026-11-15T23:59:00-05:00"},{"promotion_id":"promo_birthday","promotion_name":"Birthday coupon","promotion_type":"order_discount","promotion_status":"running","target_member_grade":"G01","starts_at":"2026-01-01T00:00:00-05:00","ends_at":null},{"promotion_id":"promo_free_ship_80","promotion_name":"Free shipping over $80","promotion_type":"… (+360자) ``
2. 모델 → **`facade_get_prmt_grid_list_cnt`** `` {"promotion_status":"running","active_from":"2026-11-07","active_until":"2026-11-08"} ``
   ← 결과 41B: `` {"status":"succeeded","data":{"total":4}} ``
3. 모델 → **`a2api_search`** `` {"query":"stacking promotion coupon"} ``
   ← 결과 593B: `` {"selected":[{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"},{"name":"facade_get_prmt_grid_list_cnt","id":"facade.get_prmt_grid_list_cnt"},{"name":"facade_get_prmt_grid_list","id":"facade.get_prmt_grid_list"},{"name":"facade_save_prmt_list","id":"facade.save_prmt_list"},{"name":"facade_get_prmt_tgt_mbr_list","id":"facade.get_prmt_tgt_mbr_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match was already offered in this conversation. If they cannot answer, tell the user what is missing instead of searching again."} ``
4. 모델 → **`a2api_search`** `` {"query":"coupon list get"} ``
   ← 결과 421B: `` {"selected":[{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"},{"name":"facade_get_mbr_grd_list","id":"facade.get_mbr_grd_list"},{"name":"facade_get_disp_corner_list","id":"facade.get_disp_corner_list"},{"name":"facade_get_clm_grid_list","id":"facade.get_clm_grid_list"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
5. 모델 → **`a2api_search`** `` {"query":"promotion stacking"} ``
   ← 결과 593B: `` {"selected":[{"name":"facade_get_prmt_grid_list_cnt","id":"facade.get_prmt_grid_list_cnt"},{"name":"facade_get_prmt_grid_list","id":"facade.get_prmt_grid_list"},{"name":"facade_save_prmt_list","id":"facade.save_prmt_list"},{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"},{"name":"facade_get_prmt_tgt_mbr_list","id":"facade.get_prmt_tgt_mbr_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match was already offered in this conversation. If they cannot answer, tell the user what is missing instead of searching again."} ``
6. 모델 → **`a2api_search`** `` {"query":"get coupon"} ``
   ← 결과 419B: `` {"selected":[{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"},{"name":"facade_get_clm_grid_list","id":"facade.get_clm_grid_list"},{"name":"facade_get_disp_corner_list","id":"facade.get_disp_corner_list"},{"name":"facade_get_mbr_grd_list","id":"facade.get_mbr_grd_list"},{"name":"facade_get_prd_dtl_info","id":"facade.get_prd_dtl_info"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
7. 모델 → **`a2api_search`** `` {"query":"coupon list","more":true} ``
   ← 실패 233B: `` {"status":"failed","error":{"code":"SEARCH_LIMIT","detail":"4 searches in a row found no function to call for this request."},"hint":"Searching again will not find more. Use the functions you have, or tell the user what is missing."} ``
8. 모델 → **`facade_get_mbr_grd_list`** `` {} ``
   ← 결과 257B: `` {"status":"succeeded","data":{"list":[{"member_grade":"G03","grade_name":"VIP","member_count":1284,"rank":3},{"member_grade":"G02","grade_name":"Gold","member_count":2900,"rank":2},{"member_grade":"G01","grade_name":"Member","member_count":9816,"rank":1}]}} ``
9. 모델 → **`a2api_search`** `` {"query":"promotion details"} ``
   ← 결과 449B: `` {"selected":[{"name":"facade_get_prd_dtl_info","id":"facade.get_prd_dtl_info"},{"name":"facade_get_rfnd_pop_init_data","id":"facade.get_rfnd_pop_init_data"},{"name":"facade_get_prd_dtl_info_v2","id":"facade.get_prd_dtl_info_v2"},{"name":"facade_get_prmt_grid_list_cnt","id":"facade.get_prmt_grid_list_cnt"},{"name":"facade_get_prmt_grid_list","id":"facade.get_prmt_grid_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``

**답변 1**
> This weekend Sat 2026-11-07 – Sun 2026-11-08 the promotion search for `promotion_status = running` and active in that window returns 4 running promotions, total = 4.
>
> Live promotions:
>
> * **promo_autumn_knit – Autumn knitwear 15%**
>   * type: item_price_everyone
>   * target: G00 – every shopper
>   * status: running
>   * starts_at: 2026-11-01T00:00:00-04:00
>   * ends_at: 2026-11-15T23:59:00-05:00
>   * This is the knit sale you referenced.
>
> * **promo_birthday – Birthday coupon**
>   * type: order_discount
>   * target: G01 – Member
>   * status: running
>   * starts_at: 2026-01-01T00:00:00-05:00
>   * ends_at: null
>
> * **promo_free_ship_80 – Free shipping over $80**
>   * type: add_on
>   * target: G00 – every shopper
>   * status: running
>   * starts_at: 2026-01-01T00:00:00-05:00
>   * ends_at: null
>
> * **promo_gold_10 – Gold tier 10%**
>   * type: order_discount
>   * target: G02 – Gold
>   * status: running
>   * starts_at: 2026-01-01T00:00:00-05:00
>   * ends_at: null
>
> Member grades in the system:
> * G01 Member – 9,816 members, rank 1
> * G02 Gold – 2,900 members, rank 2
> * G03 VIP – 1,284 members, rank 3
> G00 is the “every shopper” grade used for the knit sale and free shipping.
>
> Stacking configuration for these promotions / their coupons is not retrievable with the functions currently available to me, so I can’t confirm which of the three other live promos would stack on top of promo_autumn_knit. If you want me to check a specific promotion’s coupon stacking rules, let me know the promotion_id and I can try to pull the related coupon data.

**채점**: ✗ 실패 — 빠진 것: fact "the knit sale covers 26 knitwear products" (26 not shown)
