# mk-whats-running-this-weekend — ours-design-2-aborted-reset-bug

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `8c25f4a`

**과업**

> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 필요한 도구: `list_active_promotions`
- 허용 도구: `get_promotion`, `search_promotions`
- 답에 있어야 할 사실: four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwear 15% (everyone, until Nov 15), Birthday coupon (members), Free shipping over $80 (everyone), Gold tier 10% (gold)
- 답에 있어야 할 사실: the knit sale covers 26 knitwear products

### facade-all · 1회차 · E TURN_TIMEOUT

토큰 61,439 · 120.046초 · 모델 호출 10회 · 도구 호출 10회 · 첫 요청 프롬프트 4,657토큰

준비: 전략 `None`, 함수 19개

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`getPrmtGridList`** `` {"prmtNm":"knit","pageNo":0,"pageSize":10} ``
   ← 결과 121B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null}}} ``
2. 모델 → **`getPrmtGridList`** `` {"prmtNm":"knit","pageNo":1,"pageSize":10} ``
   ← 결과 249B: `` {"status":200,"body":{"list":[{"prmtNo":"promo_autumn_knit","prmtNm":"Autumn knitwear 15%","prmtTpCd":"T01","prmtStatCd":"20","tgtMbrGrdCd":"G00","strtDtm":"2026-11-01T00:00:00-04:00","endDtm":"2026-11-15T23:59:00-05:00"}],"pageNo":1,"pageSize":10}} ``
3. 모델 → **`getPrmtGridList`** `` {"prmtStatCd":20,"srchStrtDtm":"2026-11-07T00:00:00-05:00","srchEndDtm":"2026-11-08T23:59:59-05:00","pageNo":1,"pageSize":20} ``
   ← 결과 169B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid parameter: invalid type: number, expected string or map","next_tool":null}}} ``
4. 모델 → **`getPrmtGridList`** `` {"prmtStatCd":20,"srchStrtDtm":"2026-11-07T00:00:00-05:00","srchEndDtm":"2026-11-08T23:59:59-05:00","pageNo":1,"pageSize":20} ``
   ← 결과 169B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid parameter: invalid type: number, expected string or map","next_tool":null}}} ``
5. 모델 → **`getPrmtGridList`** `` {"prmtStatCd":20,"pageNo":1,"pageSize":20} ``
   ← 결과 169B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid parameter: invalid type: number, expected string or map","next_tool":null}}} ``
6. 모델 → **`getPrmtGridListCnt`** `` {"prmtStatCd":20} ``
   ← 결과 169B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid parameter: invalid type: number, expected string or map","next_tool":null}}} ``
7. 모델 → **`getPrmtGridList`** `` {"prmtStatCd":20} ``
   ← 결과 169B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid parameter: invalid type: number, expected string or map","next_tool":null}}} ``
8. 모델 → **`getPrmtGridList`** `` {"pageNo":1,"pageSize":10} ``
   ← 결과 1,345B: `` {"status":200,"body":{"list":[{"prmtNo":"promo_denim_bundle","prmtNm":"Denim bundle","prmtTpCd":"T02","prmtStatCd":"10","tgtMbrGrdCd":"G00","strtDtm":"2026-11-13T00:00:00-05:00","endDtm":"2026-11-20T23:59:00-05:00"},{"prmtNo":"promo_01m6984wcjt81jhqy24a9jd9n7","prmtNm":"Weekend Summer Outerwear VIP 20% Off","prmtTpCd":"T03","prmtStatCd":"10","tgtMbrGrdCd":"G03","strtDtm":"2026-11-07T00:00:00-05:00","endDtm":"2026-11-08T23:59:59-05:00"},{"prmtNo":"promo_autumn_knit","prmtNm":"Autumn knitwear 15%","prmtTpCd":"T01","prmtStatCd":"20","tgtMbrGrdCd":"G00","strtDtm":"2026-11-01T00:00:00-04:00","endDt… (+745자) ``
9. 모델 → **`getPrmtGridList`** `` {"pageNo":2,"pageSize":10} ``
   ← 결과 58B: `` {"status":200,"body":{"list":[],"pageNo":2,"pageSize":10}} ``
10. 모델 → **`getPrmtGridList`** `` {"prmtStatCd":20,"pageNo":1,"pageSize":10} ``
   ← 결과 169B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid parameter: invalid type: number, expected string or map","next_tool":null}}} ``

_(한 턴의 시간 한도(120초)에 걸려 중단)_

**채점**: E TURN_TIMEOUT — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8, 15, 15, 80, 10 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown); HOST:TURN_TIMEOUT

### acom-all · 1회차 · E CONTEXT_OVERFLOW

토큰 0 · 0.273초 · 모델 호출 0회 · 도구 호출 0회

준비: 전략 `None`, 함수 253개

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale


_(CONTEXT_OVERFLOW로 중단)_

**채점**: E CONTEXT_OVERFLOW — 빠진 것: tool list_active_promotions; fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8, 15, 15, 80, 10 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown); HOST:CONTEXT_OVERFLOW
(도구 정밀도 —, 재현율 0.00)

### a2api-acom · 1회차 · E MODEL_CALL_LIMIT

토큰 76,208 · 79.894초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 3,773토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`acom_list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"} ``
   ← 결과 1,511B: `` {"status":"succeeded","data":{"items":[{"id":"promo_01m6984wcjt81jhqy24a9jd9n7","name":"Weekend Summer Outerwear VIP 20% Off","status":"scheduled","discount_layer":"item_price","valid_for_member_tier":"vip","valid_from":"2026-11-07T00:00:00-05:00","valid_through":"2026-11-08T23:59:59-05:00","applies_to":{"scope":"products","category_ids":["cat_summer_outerwear"],"product_count":42}},{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:… (+900자) ``
2. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``
3. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_01m6984wcjt81jhqy24a9jd9n7"} ``
   ← 결과 537B: `` {"status":"succeeded","data":{"id":"promo_01m6984wcjt81jhqy24a9jd9n7","name":"Weekend Summer Outerwear VIP 20% Off","status":"scheduled","discount_layer":"item_price","valid_for_member_tier":"vip","valid_from":"2026-11-07T00:00:00-05:00","valid_through":"2026-11-08T23:59:59-05:00","description":"20% off 42 products for vip.","percent_off":20,"amount_off":null,"applies_to":{"scope":"products","category_ids":["cat_summer_outerwear"],"product_count":42},"price_specification_count":493,"coupon_ids":[],"change_set_id":null,"version":1}} ``
4. 모델 → **`a2api_search`** `` {"query":"promotion stacking"} ``
   ← 결과 377B: `` {"selected":[{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_end_promotion","id":"acom.end_promotion"},{"name":"acom_get_promotion","id":"acom.get_promotion"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
5. 모델 → **`a2api_search`** `` {"query":"promotion stacking policy"} ``
   ← 결과 432B: `` {"selected":[{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_list_policies","id":"acom.list_policies"},{"name":"acom_get_return_policy","id":"acom.get_return_policy"},{"name":"acom_get_policy","id":"acom.get_policy"},{"name":"acom_pause_promotion","id":"acom.pause_promotion"}],"evicted":["acom_explain_sales_change","acom_describe_data"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
6. 모델 → **`acom_get_policy`** `` {"key":"promotion.stacking","file":"promotion"} ``
   ← 실패 312B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) No policy key starts with 'promotion.stacking'. Next: list_policies."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
7. 모델 → **`acom_list_policies`** `` {"domain":"promotion"} ``
   ← 결과 224B: `` {"status":"succeeded","data":{"items":[{"file":"promotion","version":3,"domain":"promotion","summary":"Discount caps, minimum stock, overlap and coupon rules","overridden_keys":1}],"total":1,"policy_version":"918b3118ff2e"}} ``
8. 모델 → **`acom_get_policy`** `` {"key":"coupon","file":"promotion"} ``
   ← 결과 2,082B: `` {"status":"succeeded","data":{"items":[{"key":"coupon.applications","value":["automatic_at_checkout","code_entry","download"],"display":"automatic at checkout, code entry, download","file":"promotion","overridden_by_store":false},{"key":"coupon.stacking.default","value":"no_tier_coupons","display":"no tier coupons","file":"promotion","overridden_by_store":false},{"key":"coupon.stacking.allowed","value":["no_tier_coupons","with_tier_coupons","no_other_coupons"],"display":"no tier coupons, with tier coupons, no other coupons","file":"promotion","overridden_by_store":false},{"key":"coupon.records… (+900자) ``
9. 모델 → **`acom_get_policy`** `` {"key":"max_discount","file":"promotion"} ``
   ← 결과 518B: `` {"status":"succeeded","data":{"items":[{"key":"max_discount.everyone","value":0.2,"display":"20%","file":"promotion","overridden_by_store":false},{"key":"max_discount.by_tier.vip","value":0.3,"display":"30%","file":"promotion","overridden_by_store":true},{"key":"max_discount.on_unknown_tier","value":"use_everyone","display":"use everyone","file":"promotion","overridden_by_store":false},{"key":"max_discount.on_violation","value":"block","display":"block","file":"promotion","overridden_by_store":false}],"total":4}} ``
10. 모델 → **`acom_search_promotions`** `` {"query":"knit"} ``
   ← 결과 276B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00"}],"total":1}} ``
11. 모델 → **`acom_get_policy`** `` {"key":"overlap","file":"promotion"} ``
   ← 실패 301B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) No policy key starts with 'overlap'. Next: list_policies."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
12. 모델 → **`acom_get_policy`** `` {"key":"discount","file":"promotion"} ``
   ← 실패 302B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) No policy key starts with 'discount'. Next: list_policies."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8, 15, 15, 80, 10 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.40, 재현율 1.00)

### a2api-facade · 1회차 · E MODEL_CALL_LIMIT

토큰 63,553 · 115.741초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 2,850토큰

준비: 전략 `search`, 함수 8개

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`facade_get_prmt_grid_list`** `` {"promotion_status":"running","active_from":"2026-11-07","active_until":"2026-11-08","page":1,"page_size":100} ``
   ← 결과 960B: `` {"status":"succeeded","data":{"list":[{"promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00","starts_at":"2026-11-01T00:00:00-04:00","ends_at":"2026-11-15T23:59:00-05:00"},{"promotion_id":"promo_birthday","promotion_name":"Birthday coupon","promotion_type":"order_discount","promotion_status":"running","target_member_grade":"G01","starts_at":"2026-01-01T00:00:00-05:00","ends_at":null},{"promotion_id":"promo_free_ship_80","promotion_name":"Free shipping over $80","promotion_type":"… (+360자) ``
2. 모델 → **`a2api_search`** `` {"query":"stacking promotion"} ``
   ← 결과 572B: `` {"selected":[{"name":"facade_get_prmt_grid_list_cnt","id":"facade.get_prmt_grid_list_cnt"},{"name":"facade_get_prmt_grid_list","id":"facade.get_prmt_grid_list"},{"name":"facade_save_prmt_list","id":"facade.save_prmt_list"},{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"},{"name":"facade_get_prmt_tgt_mbr_list","id":"facade.get_prmt_tgt_mbr_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match is already callable. If they cannot answer, tell the user what is missing instead of searching again."} ``
3. 모델 → **`a2api_search`** `` {"query":"coupon"} ``
   ← 결과 287B: `` {"selected":[{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match is already callable. If they cannot answer, tell the user what is missing instead of searching again."} ``
4. 모델 → **`a2api_search`** `` {"query":"coupon list"} ``
   ← 결과 415B: `` {"selected":[{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"},{"name":"facade_get_mbr_grd_list","id":"facade.get_mbr_grd_list"},{"name":"facade_get_disp_corner_list","id":"facade.get_disp_corner_list"},{"name":"facade_save_prmt_list","id":"facade.save_prmt_list"},{"name":"facade_get_clm_grid_list","id":"facade.get_clm_grid_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
5. 모델 → **`facade_get_prmt_grid_list`** `` {"promotion_name":"Autumn knitwear","promotion_status":"running","page":1,"page_size":100} ``
   ← 결과 315B: `` {"status":"succeeded","data":{"list":[{"promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00","starts_at":"2026-11-01T00:00:00-04:00","ends_at":"2026-11-15T23:59:00-05:00"}],"page":1,"page_size":100}} ``
6. 모델 → **`a2api_search`** `` {"query":"coupon list get"} ``
   ← 결과 421B: `` {"selected":[{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"},{"name":"facade_get_mbr_grd_list","id":"facade.get_mbr_grd_list"},{"name":"facade_get_disp_corner_list","id":"facade.get_disp_corner_list"},{"name":"facade_get_clm_grid_list","id":"facade.get_clm_grid_list"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
7. 모델 → **`a2api_search`** `` {"query":"stacking"} ``
   ← 결과 74B: `` {"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":false} ``
8. 모델 → **`a2api_search`** `` {"query":"coupon get list"} ``
   ← 결과 562B: `` {"selected":[{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"},{"name":"facade_get_mbr_grd_list","id":"facade.get_mbr_grd_list"},{"name":"facade_get_disp_corner_list","id":"facade.get_disp_corner_list"},{"name":"facade_get_clm_grid_list","id":"facade.get_clm_grid_list"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match is already callable. If they cannot answer, tell the user what is missing instead of searching again."} ``
9. 모델 → **`facade_get_mbr_grd_list`** `` {} ``
   ← 결과 257B: `` {"status":"succeeded","data":{"list":[{"member_grade":"G03","grade_name":"VIP","member_count":1284,"rank":3},{"member_grade":"G02","grade_name":"Gold","member_count":2900,"rank":2},{"member_grade":"G01","grade_name":"Member","member_count":9816,"rank":1}]}} ``
10. 모델 → **`facade_get_prmt_grid_list_cnt`** `` {"promotion_status":"running","active_from":"2026-11-07","active_until":"2026-11-08"} ``
   ← 결과 41B: `` {"status":"succeeded","data":{"total":4}} ``
11. 모델 → **`a2api_search`** `` {"query":"coupon grid list"} ``
   ← 결과 427B: `` {"selected":[{"name":"facade_save_cpn_list","id":"facade.save_cpn_list"},{"name":"facade_get_clm_grid_list","id":"facade.get_clm_grid_list"},{"name":"facade_get_prd_grid_list","id":"facade.get_prd_grid_list"},{"name":"facade_get_prmt_grid_list","id":"facade.get_prmt_grid_list"},{"name":"facade_get_clm_grid_list_cnt","id":"facade.get_clm_grid_list_cnt"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
12. 모델 → **`a2api_search`** `` {"query":"coupon","more":true} ``
   ← 실패 101B: `` {"status":"failed","error":{"code":"SEARCH_EXHAUSTED","detail":"No more candidates for this query."}} ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8, 15, 15, 80, 10 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown); HOST:MODEL_CALL_LIMIT
