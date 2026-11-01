# mk-whats-running-this-weekend — ours-design-5

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `d4c6603`

**과업**

> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 필요한 도구: `list_active_promotions`
- 허용 도구: `get_promotion`, `search_promotions`
- 답에 있어야 할 사실: four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwear 15% (everyone, until Nov 15), Birthday coupon (members), Free shipping over $80 (everyone), Gold tier 10% (gold)
- 답에 있어야 할 사실: the knit sale covers 26 knitwear products

### a2api-acom · 1회차 · E MODEL_CALL_LIMIT

토큰 88,641 · 56.312초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 3,773토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`acom_list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"} ``
   ← 결과 1,164B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"applies_to":{"scope":"order","category_ids":[],"prod… (+564자) ``
2. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``
3. 모델 → **`a2api_search`** `` {"query":"stack promotion"} ``
   ← 결과 377B: `` {"selected":[{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_end_promotion","id":"acom.end_promotion"},{"name":"acom_get_promotion","id":"acom.get_promotion"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`a2api_search`** `` {"query":"promotion stacking"} ``
   ← 결과 518B: `` {"selected":[{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_end_promotion","id":"acom.end_promotion"},{"name":"acom_get_promotion","id":"acom.get_promotion"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match is already callable. If they cannot answer, tell the user what is missing instead of searching again."} ``
5. 모델 → **`acom_describe_data`** `` {"schema":"promotion"} ``
   ← 결과 5,112B: `` {"status":"succeeded","data":{"items":[{"table":"promotion.conditional_gift","kind":"table","term":"schema:Offer/acom:ConditionalGift","id_prefix":"cgf","description":"a gift added to an order whose subtotal before member benefits reaches a threshold, with one gift per threshold. id prefix cgf_.","columns":[{"name":"tenant_id","type":"text","nullable":false,"term":"-","description":"store (tenant) that owns this row; row-level security key.","references":"platform.online_store"},{"name":"id","type":"text","nullable":false,"term":"-","description":"id with prefix cgf_; the same value the API, l… (+900자) ``
6. 모델 → **`acom_describe_data`** `` {"schema":"promotion","table":"promotion.promotion"} ``
   ← 결과 4,589B: `` {"status":"succeeded","data":{"items":[{"table":"promotion.promotion","kind":"table","term":"schema:OfferCatalog/acom:Promotion","id_prefix":"promo","description":"a time-boxed benefit that groups member and sale prices or an order discount. id prefix promo_.","columns":[{"name":"tenant_id","type":"text","nullable":false,"term":"-","description":"store (tenant) that owns this row; row-level security key.","references":"platform.online_store"},{"name":"id","type":"text","nullable":false,"term":"-","description":"id with prefix promo_; the same value the API, logs and events use."},{"name":"name… (+900자) ``
7. 모델 → **`acom_describe_data`** `` {"term":"acom:stacking"} ``
   ← 결과 568B: `` {"status":"succeeded","data":{"items":[{"table":"promotion.coupon","kind":"table","term":"schema:Offer/acom:Coupon","id_prefix":"cpn","description":"a coupon tied to a promotion; it records the promotion's benefit on the order and never adds a second discount. id prefix cpn_.","columns":[{"name":"stacking","type":"text","nullable":false,"term":"acom:stacking","description":"which other coupons may be used in the same order. values: coupon_stacking","values":["no_tier_coupons","with_tier_coupons","no_other_coupons"],"values_list":"coupon_stacking"}]}],"total":1}} ``
8. 모델 → **`acom_describe_data`** `` {"term":"acom:discountLayer"} ``
   ← 결과 547B: `` {"status":"succeeded","data":{"items":[{"table":"promotion.promotion","kind":"table","term":"schema:OfferCatalog/acom:Promotion","id_prefix":"promo","description":"a time-boxed benefit that groups member and sale prices or an order discount. id prefix promo_.","columns":[{"name":"discount_layer","type":"text","nullable":false,"term":"acom:discountLayer","description":"where the benefit applies when benefits are calculated. values: discount_layer","values":["item_price","order_discount","add_on"],"values_list":"discount_layer"}]}],"total":1}} ``
9. 모델 → **`a2api_search`** `` {"query":"stacking policy"} ``
   ← 결과 427B: `` {"selected":[{"name":"acom_list_policies","id":"acom.list_policies"},{"name":"acom_get_return_policy","id":"acom.get_return_policy"},{"name":"acom_get_policy","id":"acom.get_policy"},{"name":"acom_get_action_log","id":"acom.get_action_log"},{"name":"acom_get_tenant","id":"acom.get_tenant"}],"evicted":["acom_explain_sales_change","acom_schedule_display"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
10. 모델 → **`acom_list_policies`** `` {"domain":"promotion"} ``
   ← 결과 224B: `` {"status":"succeeded","data":{"items":[{"file":"promotion","version":3,"domain":"promotion","summary":"Discount caps, minimum stock, overlap and coupon rules","overridden_keys":1}],"total":1,"policy_version":"918b3118ff2e"}} ``
11. 모델 → **`acom_get_policy`** `` {"key":"stacking","file":"promotion"} ``
   ← 실패 302B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) No policy key starts with 'stacking'. Next: list_policies."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
12. 모델 → **`acom_get_policy`** `` {"key":"coupon","file":"promotion"} ``
   ← 결과 2,082B: `` {"status":"succeeded","data":{"items":[{"key":"coupon.applications","value":["automatic_at_checkout","code_entry","download"],"display":"automatic at checkout, code entry, download","file":"promotion","overridden_by_store":false},{"key":"coupon.stacking.default","value":"no_tier_coupons","display":"no tier coupons","file":"promotion","overridden_by_store":false},{"key":"coupon.stacking.allowed","value":["no_tier_coupons","with_tier_coupons","no_other_coupons"],"display":"no tier coupons, with tier coupons, no other coupons","file":"promotion","overridden_by_store":false},{"key":"coupon.records… (+900자) ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8, 15, 15, 80, 10 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.22, 재현율 1.00)

### a2api-facade · 1회차 · ✗ 실패

토큰 41,412 · 119.576초 · 모델 호출 8회 · 도구 호출 7회 · 첫 요청 프롬프트 2,850토큰

준비: 전략 `search`, 함수 8개

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`facade_get_prmt_grid_list`** `` {"promotion_status":"running","active_from":"2026-11-07T00:00:00","active_until":"2026-11-08T23:59:59","page":1,"page_size":100} ``
   ← 결과 960B: `` {"status":"succeeded","data":{"list":[{"promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00","starts_at":"2026-11-01T00:00:00-04:00","ends_at":"2026-11-15T23:59:00-05:00"},{"promotion_id":"promo_birthday","promotion_name":"Birthday coupon","promotion_type":"order_discount","promotion_status":"running","target_member_grade":"G01","starts_at":"2026-01-01T00:00:00-05:00","ends_at":null},{"promotion_id":"promo_free_ship_80","promotion_name":"Free shipping over $80","promotion_type":"… (+360자) ``
2. 모델 → **`a2api_search`** `` {"query":"coupon"} ``
   ← 결과 287B: `` {"selected":[{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match is already callable. If they cannot answer, tell the user what is missing instead of searching again."} ``
3. 모델 → **`a2api_search`** `` {"query":"coupon list"} ``
   ← 결과 415B: `` {"selected":[{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"},{"name":"facade_get_mbr_grd_list","id":"facade.get_mbr_grd_list"},{"name":"facade_get_disp_corner_list","id":"facade.get_disp_corner_list"},{"name":"facade_save_prmt_list","id":"facade.save_prmt_list"},{"name":"facade_get_clm_grid_list","id":"facade.get_clm_grid_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`a2api_search`** `` {"query":"get coupon"} ``
   ← 결과 419B: `` {"selected":[{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"},{"name":"facade_get_clm_grid_list","id":"facade.get_clm_grid_list"},{"name":"facade_get_disp_corner_list","id":"facade.get_disp_corner_list"},{"name":"facade_get_mbr_grd_list","id":"facade.get_mbr_grd_list"},{"name":"facade_get_prd_dtl_info","id":"facade.get_prd_dtl_info"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
5. 모델 → **`a2api_search`** `` {"query":"coupon grid"} ``
   ← 결과 427B: `` {"selected":[{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"},{"name":"facade_get_clm_grid_list","id":"facade.get_clm_grid_list"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_get_prmt_grid_list","id":"facade.get_prmt_grid_list"},{"name":"facade_get_clm_grid_list_cnt","id":"facade.get_clm_grid_list_cnt"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
6. 모델 → **`facade_get_mbr_grd_list`** `` {} ``
   ← 결과 257B: `` {"status":"succeeded","data":{"list":[{"member_grade":"G03","grade_name":"VIP","member_count":1284,"rank":3},{"member_grade":"G02","grade_name":"Gold","member_count":2900,"rank":2},{"member_grade":"G01","grade_name":"Member","member_count":9816,"rank":1}]}} ``
7. 모델 → **`facade_get_prmt_grid_list_cnt`** `` {"promotion_status":"running","active_from":"2026-11-07T00:00:00","active_until":"2026-11-08T23:59:59"} ``
   ← 결과 41B: `` {"status":"succeeded","data":{"total":4}} ``

**답변 1**
> This weekend 2026-11-07 to 2026-11-08, 4 promotions are running:
>
> * **promo_autumn_knit – Autumn knitwear 15%**
>   promotion_type: item_price_everyone
>   target_member_grade: G00 – every shopper
>   status: running
>   starts_at: 2026-11-01T00:00:00-04:00
>   ends_at: 2026-11-15T23:59:00-05:00
>   This is the knit sale you referenced.
>
> * **promo_birthday – Birthday coupon**
>   promotion_type: order_discount
>   target_member_grade: G01 – Member
>   status: running
>   starts_at: 2026-01-01T00:00:00-05:00
>   ends_at: null
>
> * **promo_free_ship_80 – Free shipping over $80**
>   promotion_type: add_on
>   target_member_grade: G00 – every shopper
>   status: running
>   starts_at: 2026-01-01T00:00:00-05:00
>   ends_at: null
>
> * **promo_gold_10 – Gold tier 10%**
>   promotion_type: order_discount
>   target_member_grade: G02 – Gold
>   status: running
>   starts_at: 2026-01-01T00:00:00-05:00
>   ends_at: null
>
> Member grades in store:
> G01 Member, G02 Gold, G03 VIP. G00 = every shopper.
>
> The knit sale promo_autumn_knit is live all weekend 7-8 Nov. The other three running promos – Birthday coupon for G01 Members, Free shipping over $80 for everyone, and Gold tier 10% order discount for G02 – are also live this weekend and would be in scope for stacking with the knit sale if stacking is allowed. Let me know if you want me to pause/ end any of them.

**채점**: ✗ 실패 — 빠진 것: fact "the knit sale covers 26 knitwear products" (26 not shown)
