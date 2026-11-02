# mk-whats-running-this-weekend — ours-design-12b

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `d86a1ff` · a2api `6adfc3b`

**과업**

> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 필요한 도구: `list_active_promotions`
- 허용 도구: `get_promotion`, `search_promotions`
- 답에 있어야 할 사실: four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwear 15% (everyone, until Nov 15), Birthday coupon (members), Free shipping over $80 (everyone), Gold tier 10% (gold)
- 답에 있어야 할 사실: the knit sale covers 26 knitwear products

### a2api-acom · 1회차 · E MODEL_CALL_LIMIT

토큰 108,599 · 50.221초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 3,996토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 모델 판단(추론 필드): We need to find promos live this weekend. Store time: Friday, November 6, 2026, 11:00 America/New_York. This weekend? Likely Saturday Nov 7 and Sunday Nov 8? Or weekend starting Friday? Probably Saturday-Sunday. Could be Friday evening onward? "this weekend" ambiguous. Could be from now through Sunday. Let's assume valid_from = 2026-11-07T00:00? Or Friday? Store time Friday Nov 6 11:00. Weekend maybe Saturday 7 and Sunday 8. Could also include Friday evening? Might be safe to check from 2026-11-07 to 2026-11-08 23:59. Also maybe include Friday? Let's check both? Could ask clarification but better to provide. We need promos live this weekend, and don't want to stack anything on top of knit sa… (+1,105자)
1. 모델 → **`acom_list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"} ``
   ← 결과 1,164B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"applies_to":{"scope":"order","category_ids":[],"prod… (+564자) ``
- 모델 판단(추론 필드): We need to answer what promos are live this weekend. We have list active promotions for 2026-11-07 to 2026-11-08. Items: promo_autumn_knit (Autumn knitwear 15%), promo_birthday, promo_free_ship_80, promo_gold_10. User says don't want to stack anything on top of knit sale. Possibly need to check stacking? Might need to see promotion details to see if they stack? The list shows discount_layer: item_price for knit, order_discount for birthday and gold, add_on for free ship. We could provide summary. Possibly also need to check if any scheduled promotions? The list includes running and scheduled? Default statuses running and scheduled. It returned 4. Maybe need to explain stacking rules? Could g… (+1,081자)
2. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``
- 모델 판단(추론 필드): We have list active promotions for 2026-11-07 to 2026-11-08. Items: promo_autumn_knit - Autumn knitwear 15% - running - discount_layer item_price - everyone - valid 2026-11-01 to 2026-11-15 promo_birthday - Birthday coupon - running - discount_layer order_discount - member - valid from 2026-01-01 onward promo_free_ship_80 - Free shipping over $80 - running - discount_layer add_on - everyone promo_gold_10 - Gold tier 10% - running - discount_layer order_discount - gold User doesn't want to stack anything on top of knit sale. Need to explain which promos are live this weekend, and note stacking? Possibly need to check if any stack with knit sale. Discount layer item_price vs order_discount vs … (+781자)
3. 모델 → **`a2api_search`** `` {"query":"promotion stacking discount layer"} ``
   ← 결과 395B: `` {"selected":[{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_update_promotion","id":"acom.update_promotion"},{"name":"acom_calculate_benefits","id":"acom.calculate_benefits"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`a2api_search`** `` {"query":"stacking policy"} ``
   ← 결과 363B: `` {"selected":[{"name":"acom_list_policies","id":"acom.list_policies"},{"name":"acom_get_return_policy","id":"acom.get_return_policy"},{"name":"acom_get_policy","id":"acom.get_policy"},{"name":"acom_get_action_log","id":"acom.get_action_log"},{"name":"acom_get_tenant","id":"acom.get_tenant"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
5. 모델 → **`acom_get_policy`** `` {"key":"stacking","file":"promotion"} ``
   ← 실패 302B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) No policy key starts with 'stacking'. Next: list_policies."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
6. 모델 → **`acom_list_policies`** `` {"domain":"promotion"} ``
   ← 결과 224B: `` {"status":"succeeded","data":{"items":[{"file":"promotion","version":3,"domain":"promotion","summary":"Discount caps, minimum stock, overlap and coupon rules","overridden_keys":1}],"total":1,"policy_version":"918b3118ff2e"}} ``
7. 모델 → **`acom_get_policy`** `` {"key":"coupon","file":"promotion"} ``
   ← 결과 2,082B: `` {"status":"succeeded","data":{"items":[{"key":"coupon.applications","value":["automatic_at_checkout","code_entry","download"],"display":"automatic at checkout, code entry, download","file":"promotion","overridden_by_store":false},{"key":"coupon.stacking.default","value":"no_tier_coupons","display":"no tier coupons","file":"promotion","overridden_by_store":false},{"key":"coupon.stacking.allowed","value":["no_tier_coupons","with_tier_coupons","no_other_coupons"],"display":"no tier coupons, with tier coupons, no other coupons","file":"promotion","overridden_by_store":false},{"key":"coupon.records… (+1,482자) ``
- 모델 판단(추론 필드): We have list active promotions for weekend 2026-11-07 to 2026-11-08. Items: promo_autumn_knit - Autumn knitwear 15% - running - discount_layer item_price - everyone - valid 2026-11-01 to 2026-11-15 - applies to categories cat_knitwear product_count 26 promo_birthday - Birthday coupon - running - discount_layer order_discount - valid_for_member_tier member - valid_from 2026-01-01 ... valid_through null - applies to order promo_free_ship_80 - Free shipping over $80 - running - discount_layer add_on - everyone promo_gold_10 - Gold tier 10% - running - discount_layer order_discount - valid_for_member_tier gold User doesn't want to stack anything on top of knit sale. Need to explain stacking rule… (+606자)
8. 모델 → **`acom_get_policy`** `` {"key":"discount","file":"promotion"} ``
   ← 실패 302B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) No policy key starts with 'discount'. Next: list_policies."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
9. 모델 → **`acom_get_policy`** `` {"key":"max_discount","file":"promotion"} ``
   ← 결과 518B: `` {"status":"succeeded","data":{"items":[{"key":"max_discount.everyone","value":0.2,"display":"20%","file":"promotion","overridden_by_store":false},{"key":"max_discount.by_tier.vip","value":0.3,"display":"30%","file":"promotion","overridden_by_store":true},{"key":"max_discount.on_unknown_tier","value":"use_everyone","display":"use everyone","file":"promotion","overridden_by_store":false},{"key":"max_discount.on_violation","value":"block","display":"block","file":"promotion","overridden_by_store":false}],"total":4}} ``
- 모델 판단(추론 필드): We have list active promotions for weekend 2026-11-07 to 2026-11-08. Items: promo_autumn_knit - Autumn knitwear 15% - running - discount_layer item_price - everyone - valid 2026-11-01 to 2026-11-15 - applies to categories cat_knitwear product_count 26 promo_birthday - Birthday coupon - running - discount_layer order_discount - valid_for_member_tier member - valid from 2026-01-01 onward - applies to order promo_free_ship_80 - Free shipping over $80 - running - discount_layer add_on - everyone promo_gold_10 - Gold tier 10% - running - discount_layer order_discount - valid_for_member_tier gold User doesn't want to stack anything on top of knit sale. Need to explain stacking rules. We have polic… (+491자)
10. 모델 → **`acom_get_policy`** `` {"key":"overlap","file":"promotion"} ``
   ← 실패 301B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) No policy key starts with 'overlap'. Next: list_policies."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
11. 모델 → **`acom_get_policy`** `` {"key":"promotion","file":"promotion"} ``
   ← 실패 303B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) No policy key starts with 'promotion'. Next: list_policies."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
12. 모델 → **`a2api_search`** `` {"query":"promotion overlap"} ``
   ← 결과 403B: `` {"selected":[{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_update_promotion","id":"acom.update_promotion"},{"name":"acom_list_active_promotions","id":"acom.list_active_promotions"},{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_end_promotion","id":"acom.end_promotion"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8, 15, 15, 80, 10 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.22, 재현율 1.00)

### a2api-acom · 2회차 · E MODEL_CALL_LIMIT

토큰 89,151 · 48.008초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 3,996토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 모델 판단(추론 필드): We need to find promos live this weekend. Store time: Friday, November 6, 2026, 11:00 America/New_York. This weekend? Likely Saturday Nov 7 and Sunday Nov 8? Or weekend starting Friday? Probably Saturday-Sunday. Could be Friday evening onward? "this weekend" ambiguous. Could be from now onward to Sunday end. Let's assume valid_from = 2026-11-07T00:00? Or Friday? Store time Friday Nov 6 11:00. Weekend could be Saturday 7 and Sunday 8. Might also include Friday night? Safer to check from 2026-11-07T00:00 to 2026-11-08T23:59. Also maybe include Friday? Could ask clarification but better provide. We need promos live this weekend, and don't want to stack anything on top of knit sale. So need to i… (+1,045자)
1. 모델 → **`acom_list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"} ``
   ← 결과 1,164B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"applies_to":{"scope":"order","category_ids":[],"prod… (+564자) ``
- 모델 판단(추론 필드): We need to answer what promos are live this weekend. We have list active promotions for 2026-11-07 to 2026-11-08. Items: promo_autumn_knit - Autumn knitwear 15% - running - discount_layer item_price - valid_for_member_tier everyone - valid_from 2026-11-01 to 2026-11-15 promo_birthday - Birthday coupon - running - discount_layer order_discount - valid_for_member_tier member promo_free_ship_80 - Free shipping over $80 - running - discount_layer add_on - everyone promo_gold_10 - Gold tier 10% - running - discount_layer order_discount - gold User doesn't want to stack anything on top of knit sale. Need to explain stacking? Possibly need to check promotion details to see if they stack. The discou… (+1,426자)
2. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``
- 모델 판단(추론 필드): We have list active promotions for weekend 2026-11-07 to 2026-11-08. Items: promo_autumn_knit - Autumn knitwear 15% - running - discount_layer item_price - everyone - valid 2026-11-01 to 2026-11-15 - applies to categories cat_knitwear promo_birthday - Birthday coupon - running - discount_layer order_discount - member - valid from 2026-01-01 onward - applies to order promo_free_ship_80 - Free shipping over $80 - running - discount_layer add_on - everyone promo_gold_10 - Gold tier 10% - running - discount_layer order_discount - gold User doesn't want to stack anything on top of knit sale. Need to explain which promos are live this weekend, and note stacking? Possibly need to check if any stack… (+1,087자)
3. 모델 → **`a2api_search`** `` {"query":"promotion stacking"} ``
   ← 결과 377B: `` {"selected":[{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_end_promotion","id":"acom.end_promotion"},{"name":"acom_get_promotion","id":"acom.get_promotion"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`a2api_search`** `` {"query":"stacking policy"} ``
   ← 결과 363B: `` {"selected":[{"name":"acom_list_policies","id":"acom.list_policies"},{"name":"acom_get_return_policy","id":"acom.get_return_policy"},{"name":"acom_get_policy","id":"acom.get_policy"},{"name":"acom_get_action_log","id":"acom.get_action_log"},{"name":"acom_get_tenant","id":"acom.get_tenant"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
5. 모델 → **`acom_get_policy`** `` {"key":"stacking","file":"promotion"} ``
   ← 실패 302B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) No policy key starts with 'stacking'. Next: list_policies."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
6. 모델 → **`acom_list_policies`** `` {"domain":"promotion"} ``
   ← 결과 224B: `` {"status":"succeeded","data":{"items":[{"file":"promotion","version":3,"domain":"promotion","summary":"Discount caps, minimum stock, overlap and coupon rules","overridden_keys":1}],"total":1,"policy_version":"918b3118ff2e"}} ``
7. 모델 → **`acom_get_policy`** `` {"key":"coupon","file":"promotion"} ``
   ← 결과 2,082B: `` {"status":"succeeded","data":{"items":[{"key":"coupon.applications","value":["automatic_at_checkout","code_entry","download"],"display":"automatic at checkout, code entry, download","file":"promotion","overridden_by_store":false},{"key":"coupon.stacking.default","value":"no_tier_coupons","display":"no tier coupons","file":"promotion","overridden_by_store":false},{"key":"coupon.stacking.allowed","value":["no_tier_coupons","with_tier_coupons","no_other_coupons"],"display":"no tier coupons, with tier coupons, no other coupons","file":"promotion","overridden_by_store":false},{"key":"coupon.records… (+1,482자) ``
- 모델 판단(추론 필드): We have list active promotions for weekend 2026-11-07 to 2026-11-08. Items: promo_autumn_knit - Autumn knitwear 15% - running - discount_layer item_price - everyone - valid 2026-11-01 to 2026-11-15 promo_birthday - Birthday coupon - running - order_discount - member - valid from 2026-01-01 onward promo_free_ship_80 - Free shipping over $80 - running - add_on - everyone promo_gold_10 - Gold tier 10% - running - order_discount - gold User doesn't want to stack anything on top of knit sale. Need to explain stacking rules. We have policy coupon.stacking.default = no_tier_coupons. Need to understand stacking between item_price and order_discount? Possibly need to check policy for promotion stacki… (+259자)
8. 모델 → **`acom_get_policy`** `` {"key":"discount","file":"promotion"} ``
   ← 실패 302B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) No policy key starts with 'discount'. Next: list_policies."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
9. 모델 → **`acom_get_policy`** `` {"key":"max_discount","file":"promotion"} ``
   ← 결과 518B: `` {"status":"succeeded","data":{"items":[{"key":"max_discount.everyone","value":0.2,"display":"20%","file":"promotion","overridden_by_store":false},{"key":"max_discount.by_tier.vip","value":0.3,"display":"30%","file":"promotion","overridden_by_store":true},{"key":"max_discount.on_unknown_tier","value":"use_everyone","display":"use everyone","file":"promotion","overridden_by_store":false},{"key":"max_discount.on_violation","value":"block","display":"block","file":"promotion","overridden_by_store":false}],"total":4}} ``
10. 모델 → **`acom_get_policy`** `` {"key":"overlap","file":"promotion"} ``
   ← 실패 301B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) No policy key starts with 'overlap'. Next: list_policies."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
11. 모델 → **`a2api_search`** `` {"query":"promotion overlap"} ``
   ← 결과 403B: `` {"selected":[{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_update_promotion","id":"acom.update_promotion"},{"name":"acom_list_active_promotions","id":"acom.list_active_promotions"},{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_end_promotion","id":"acom.end_promotion"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
12. 모델 → **`acom_get_policy`** `` {"key":"promotion","file":"promotion"} ``
   ← 실패 303B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) No policy key starts with 'promotion'. Next: list_policies."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8, 15, 15, 80, 10 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.22, 재현율 1.00)

### a2api-acom-guard · 1회차 · E MODEL_CALL_LIMIT

토큰 89,151 · 48.15초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 3,996토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 모델 판단(추론 필드): We need to find promos live this weekend. Store time: Friday, November 6, 2026, 11:00 America/New_York. This weekend? Likely Saturday Nov 7 and Sunday Nov 8? Or weekend starting Friday? Probably Saturday-Sunday. Could be Friday evening onward? "this weekend" ambiguous. Could be from now onward to Sunday end. Let's assume valid_from = 2026-11-07T00:00? Or Friday? Store time Friday Nov 6 11:00. Weekend could be Saturday 7 and Sunday 8. Might also include Friday night? Safer to check from 2026-11-07T00:00 to 2026-11-08T23:59. Also maybe include Friday? Could ask clarification but better provide. We need promos live this weekend, and don't want to stack anything on top of knit sale. So need to i… (+1,045자)
1. 모델 → **`acom_list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"} ``
   ← 결과 1,164B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"applies_to":{"scope":"order","category_ids":[],"prod… (+564자) ``
- 모델 판단(추론 필드): We need to answer what promos are live this weekend. We have list active promotions for 2026-11-07 to 2026-11-08. Items: promo_autumn_knit - Autumn knitwear 15% - running - discount_layer item_price - valid_for_member_tier everyone - valid_from 2026-11-01 to 2026-11-15 promo_birthday - Birthday coupon - running - discount_layer order_discount - valid_for_member_tier member promo_free_ship_80 - Free shipping over $80 - running - discount_layer add_on - everyone promo_gold_10 - Gold tier 10% - running - discount_layer order_discount - gold User doesn't want to stack anything on top of knit sale. Need to explain stacking? Possibly need to check promotion details to see if they stack. The discou… (+1,426자)
2. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``
- 모델 판단(추론 필드): We have list active promotions for weekend 2026-11-07 to 2026-11-08. Items: promo_autumn_knit - Autumn knitwear 15% - running - discount_layer item_price - everyone - valid 2026-11-01 to 2026-11-15 - applies to categories cat_knitwear promo_birthday - Birthday coupon - running - discount_layer order_discount - member - valid from 2026-01-01 onward - applies to order promo_free_ship_80 - Free shipping over $80 - running - discount_layer add_on - everyone promo_gold_10 - Gold tier 10% - running - discount_layer order_discount - gold User doesn't want to stack anything on top of knit sale. Need to explain which promos are live this weekend, and note stacking? Possibly need to check if any stack… (+1,087자)
3. 모델 → **`a2api_search`** `` {"query":"promotion stacking"} ``
   ← 결과 377B: `` {"selected":[{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_end_promotion","id":"acom.end_promotion"},{"name":"acom_get_promotion","id":"acom.get_promotion"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`a2api_search`** `` {"query":"stacking policy"} ``
   ← 결과 363B: `` {"selected":[{"name":"acom_list_policies","id":"acom.list_policies"},{"name":"acom_get_return_policy","id":"acom.get_return_policy"},{"name":"acom_get_policy","id":"acom.get_policy"},{"name":"acom_get_action_log","id":"acom.get_action_log"},{"name":"acom_get_tenant","id":"acom.get_tenant"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
5. 모델 → **`acom_get_policy`** `` {"key":"stacking","file":"promotion"} ``
   ← 실패 302B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) No policy key starts with 'stacking'. Next: list_policies."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
6. 모델 → **`acom_list_policies`** `` {"domain":"promotion"} ``
   ← 결과 224B: `` {"status":"succeeded","data":{"items":[{"file":"promotion","version":3,"domain":"promotion","summary":"Discount caps, minimum stock, overlap and coupon rules","overridden_keys":1}],"total":1,"policy_version":"918b3118ff2e"}} ``
7. 모델 → **`acom_get_policy`** `` {"key":"coupon","file":"promotion"} ``
   ← 결과 2,082B: `` {"status":"succeeded","data":{"items":[{"key":"coupon.applications","value":["automatic_at_checkout","code_entry","download"],"display":"automatic at checkout, code entry, download","file":"promotion","overridden_by_store":false},{"key":"coupon.stacking.default","value":"no_tier_coupons","display":"no tier coupons","file":"promotion","overridden_by_store":false},{"key":"coupon.stacking.allowed","value":["no_tier_coupons","with_tier_coupons","no_other_coupons"],"display":"no tier coupons, with tier coupons, no other coupons","file":"promotion","overridden_by_store":false},{"key":"coupon.records… (+1,482자) ``
- 모델 판단(추론 필드): We have list active promotions for weekend 2026-11-07 to 2026-11-08. Items: promo_autumn_knit - Autumn knitwear 15% - running - discount_layer item_price - everyone - valid 2026-11-01 to 2026-11-15 promo_birthday - Birthday coupon - running - order_discount - member - valid from 2026-01-01 onward promo_free_ship_80 - Free shipping over $80 - running - add_on - everyone promo_gold_10 - Gold tier 10% - running - order_discount - gold User doesn't want to stack anything on top of knit sale. Need to explain stacking rules. We have policy coupon.stacking.default = no_tier_coupons. Need to understand stacking between item_price and order_discount? Possibly need to check policy for promotion stacki… (+259자)
8. 모델 → **`acom_get_policy`** `` {"key":"discount","file":"promotion"} ``
   ← 실패 302B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) No policy key starts with 'discount'. Next: list_policies."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
9. 모델 → **`acom_get_policy`** `` {"key":"max_discount","file":"promotion"} ``
   ← 결과 518B: `` {"status":"succeeded","data":{"items":[{"key":"max_discount.everyone","value":0.2,"display":"20%","file":"promotion","overridden_by_store":false},{"key":"max_discount.by_tier.vip","value":0.3,"display":"30%","file":"promotion","overridden_by_store":true},{"key":"max_discount.on_unknown_tier","value":"use_everyone","display":"use everyone","file":"promotion","overridden_by_store":false},{"key":"max_discount.on_violation","value":"block","display":"block","file":"promotion","overridden_by_store":false}],"total":4}} ``
10. 모델 → **`acom_get_policy`** `` {"key":"overlap","file":"promotion"} ``
   ← 실패 301B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) No policy key starts with 'overlap'. Next: list_policies."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
11. 모델 → **`a2api_search`** `` {"query":"promotion overlap"} ``
   ← 결과 403B: `` {"selected":[{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_update_promotion","id":"acom.update_promotion"},{"name":"acom_list_active_promotions","id":"acom.list_active_promotions"},{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_end_promotion","id":"acom.end_promotion"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
12. 모델 → **`acom_get_policy`** `` {"key":"promotion","file":"promotion"} ``
   ← 실패 303B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) No policy key starts with 'promotion'. Next: list_policies."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8, 15, 15, 80, 10 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.22, 재현율 1.00)

### a2api-acom-guard · 2회차 · E MODEL_CALL_LIMIT

토큰 108,599 · 50.156초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 3,996토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 모델 판단(추론 필드): We need to find promos live this weekend. Store time: Friday, November 6, 2026, 11:00 America/New_York. This weekend? Likely Saturday Nov 7 and Sunday Nov 8? Or weekend starting Friday? Probably Saturday-Sunday. Could be Friday evening onward? "this weekend" ambiguous. Could be from now through Sunday. Let's assume valid_from = 2026-11-07T00:00? Or Friday? Store time Friday Nov 6 11:00. Weekend maybe Saturday 7 and Sunday 8. Could also include Friday evening? Might be safe to check from 2026-11-07 to 2026-11-08 23:59. Also maybe include Friday? Let's check both? Could ask clarification but better to provide. We need promos live this weekend, and don't want to stack anything on top of knit sa… (+1,105자)
1. 모델 → **`acom_list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"} ``
   ← 결과 1,164B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"applies_to":{"scope":"order","category_ids":[],"prod… (+564자) ``
- 모델 판단(추론 필드): We need to answer what promos are live this weekend. We have list active promotions for 2026-11-07 to 2026-11-08. Items: promo_autumn_knit (Autumn knitwear 15%), promo_birthday, promo_free_ship_80, promo_gold_10. User says don't want to stack anything on top of knit sale. Possibly need to check stacking? Might need to see promotion details to see if they stack? The list shows discount_layer: item_price for knit, order_discount for birthday and gold, add_on for free ship. We could provide summary. Possibly also need to check if any scheduled promotions? The list includes running and scheduled? Default statuses running and scheduled. It returned 4. Maybe need to explain stacking rules? Could g… (+1,081자)
2. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``
- 모델 판단(추론 필드): We have list active promotions for 2026-11-07 to 2026-11-08. Items: promo_autumn_knit - Autumn knitwear 15% - running - discount_layer item_price - everyone - valid 2026-11-01 to 2026-11-15 promo_birthday - Birthday coupon - running - discount_layer order_discount - member - valid from 2026-01-01 onward promo_free_ship_80 - Free shipping over $80 - running - discount_layer add_on - everyone promo_gold_10 - Gold tier 10% - running - discount_layer order_discount - gold User doesn't want to stack anything on top of knit sale. Need to explain which promos are live this weekend, and note stacking? Possibly need to check if any stack with knit sale. Discount layer item_price vs order_discount vs … (+781자)
3. 모델 → **`a2api_search`** `` {"query":"promotion stacking discount layer"} ``
   ← 결과 395B: `` {"selected":[{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_update_promotion","id":"acom.update_promotion"},{"name":"acom_calculate_benefits","id":"acom.calculate_benefits"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
4. 모델 → **`a2api_search`** `` {"query":"stacking policy"} ``
   ← 결과 363B: `` {"selected":[{"name":"acom_list_policies","id":"acom.list_policies"},{"name":"acom_get_return_policy","id":"acom.get_return_policy"},{"name":"acom_get_policy","id":"acom.get_policy"},{"name":"acom_get_action_log","id":"acom.get_action_log"},{"name":"acom_get_tenant","id":"acom.get_tenant"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
5. 모델 → **`acom_get_policy`** `` {"key":"stacking","file":"promotion"} ``
   ← 실패 302B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) No policy key starts with 'stacking'. Next: list_policies."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
6. 모델 → **`acom_list_policies`** `` {"domain":"promotion"} ``
   ← 결과 224B: `` {"status":"succeeded","data":{"items":[{"file":"promotion","version":3,"domain":"promotion","summary":"Discount caps, minimum stock, overlap and coupon rules","overridden_keys":1}],"total":1,"policy_version":"918b3118ff2e"}} ``
7. 모델 → **`acom_get_policy`** `` {"key":"coupon","file":"promotion"} ``
   ← 결과 2,082B: `` {"status":"succeeded","data":{"items":[{"key":"coupon.applications","value":["automatic_at_checkout","code_entry","download"],"display":"automatic at checkout, code entry, download","file":"promotion","overridden_by_store":false},{"key":"coupon.stacking.default","value":"no_tier_coupons","display":"no tier coupons","file":"promotion","overridden_by_store":false},{"key":"coupon.stacking.allowed","value":["no_tier_coupons","with_tier_coupons","no_other_coupons"],"display":"no tier coupons, with tier coupons, no other coupons","file":"promotion","overridden_by_store":false},{"key":"coupon.records… (+1,482자) ``
- 모델 판단(추론 필드): We have list active promotions for weekend 2026-11-07 to 2026-11-08. Items: promo_autumn_knit - Autumn knitwear 15% - running - discount_layer item_price - everyone - valid 2026-11-01 to 2026-11-15 - applies to categories cat_knitwear product_count 26 promo_birthday - Birthday coupon - running - discount_layer order_discount - valid_for_member_tier member - valid_from 2026-01-01 ... valid_through null - applies to order promo_free_ship_80 - Free shipping over $80 - running - discount_layer add_on - everyone promo_gold_10 - Gold tier 10% - running - discount_layer order_discount - valid_for_member_tier gold User doesn't want to stack anything on top of knit sale. Need to explain stacking rule… (+606자)
8. 모델 → **`acom_get_policy`** `` {"key":"discount","file":"promotion"} ``
   ← 실패 302B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) No policy key starts with 'discount'. Next: list_policies."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
9. 모델 → **`acom_get_policy`** `` {"key":"max_discount","file":"promotion"} ``
   ← 결과 518B: `` {"status":"succeeded","data":{"items":[{"key":"max_discount.everyone","value":0.2,"display":"20%","file":"promotion","overridden_by_store":false},{"key":"max_discount.by_tier.vip","value":0.3,"display":"30%","file":"promotion","overridden_by_store":true},{"key":"max_discount.on_unknown_tier","value":"use_everyone","display":"use everyone","file":"promotion","overridden_by_store":false},{"key":"max_discount.on_violation","value":"block","display":"block","file":"promotion","overridden_by_store":false}],"total":4}} ``
- 모델 판단(추론 필드): We have list active promotions for weekend 2026-11-07 to 2026-11-08. Items: promo_autumn_knit - Autumn knitwear 15% - running - discount_layer item_price - everyone - valid 2026-11-01 to 2026-11-15 - applies to categories cat_knitwear product_count 26 promo_birthday - Birthday coupon - running - discount_layer order_discount - valid_for_member_tier member - valid from 2026-01-01 onward - applies to order promo_free_ship_80 - Free shipping over $80 - running - discount_layer add_on - everyone promo_gold_10 - Gold tier 10% - running - discount_layer order_discount - valid_for_member_tier gold User doesn't want to stack anything on top of knit sale. Need to explain stacking rules. We have polic… (+491자)
10. 모델 → **`acom_get_policy`** `` {"key":"overlap","file":"promotion"} ``
   ← 실패 301B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) No policy key starts with 'overlap'. Next: list_policies."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
11. 모델 → **`acom_get_policy`** `` {"key":"promotion","file":"promotion"} ``
   ← 실패 303B: `` {"status":"failed","error":{"code":"RESOURCE_NOT_FOUND","detail":"The backend reported that the target does not exist. (HTTP 404) No policy key starts with 'promotion'. Next: list_policies."},"hint":"The target was not found. Check the ID against earlier results; other functions will not change this."} ``
12. 모델 → **`a2api_search`** `` {"query":"promotion overlap"} ``
   ← 결과 403B: `` {"selected":[{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_update_promotion","id":"acom.update_promotion"},{"name":"acom_list_active_promotions","id":"acom.list_active_promotions"},{"name":"acom_create_promotion","id":"acom.create_promotion"},{"name":"acom_end_promotion","id":"acom.end_promotion"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8, 15, 15, 80, 10 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.22, 재현율 1.00)

### a2api-acom-names-batch · 1회차 · ✓ 통과

토큰 21,710 · 52.137초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 1,989토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 모델 판단(추론 필드): We need to find promotions live this weekend. Store time: Friday, November 6, 2026, 11:00 America/New_York. This weekend = Saturday Nov 7 and Sunday Nov 8? Possibly also Friday? "this weekend" likely Saturday-Sunday. Need promos live this weekend. Don't want to stack anything on top of knit sale. So need to identify knit sale promotion, and other promos live, and note stacking rules. We need to use tools. Likely promotion › promotion: list_active_promotions, search_promotions, get_promotion. Also need to know dates. We need to find promotions active on weekend. list_active_promotions probably returns active now. But need this weekend. Might need to search promotions with start/end dates. We … (+779자)
1. 모델 → **`a2api_load`** `` {"names":["list_active_promotions","search_promotions","get_promotion"]} ``
   ← 결과 73B: `` {"loaded":["list_active_promotions","search_promotions","get_promotion"]} ``
- 모델 판단(추론 필드): We need promos live this weekend. Store time: Friday, November 6, 2026, 11:00 America/New_York. Weekend = Saturday Nov 7 and Sunday Nov 8? Possibly also Friday? "this weekend" likely Saturday 7 and Sunday 8. Could include Friday evening? Probably Saturday-Sunday. We need list active promotions for period. Need valid_from and valid_through. Use list_active_promotions with valid_from = 2026-11-07T00:00, valid_through = 2026-11-08T23:59. Also maybe include Friday? Let's assume weekend starts Saturday. Could also include Friday night? Might be safe to check Saturday and Sunday. Also user says don't want to stack anything on top of the knit sale. So need to identify knit sale promotion. Probably … (+808자)
2. 모델 → **`a2api_batch`** `` {"calls":[{"name":"search_promotions","arguments":{"query":"knit","limit":20}},{"name":"list_active_promotions","arguments":{"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","limit":100}}]} ``
   ← 결과 1,534B: `` {"batch":[{"name":"search_promotions","result":{"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00"}],"total":1}}},{"name":"list_active_promotions","result":{"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through… (+934자) ``
- 모델 판단(추론 필드): We have search promotions for knit: promo_autumn_knit running 2026-11-01 to 2026-11-15. That's the knit sale. List active promotions for weekend 2026-11-07 to 2026-11-08: items: promo_autumn_knit - item_price, everyone, categories cat_knitwear, product_count 26 promo_birthday - order_discount, member, order scope promo_free_ship_80 - add_on, everyone, order scope promo_gold_10 - order_discount, gold tier User doesn't want to stack anything on top of knit sale. So we need to list promos live this weekend, and note stacking? Possibly need to check if any overlap? The user says I don't want to stack anything on top of the knit sale. Maybe they want to know which promos are live, and which would… (+1,733자)
3. 모델 → **`a2api_batch`** `` {"calls":[{"name":"get_promotion","arguments":{"promotion_id":"promo_birthday"}},{"name":"get_promotion","arguments":{"promotion_id":"promo_free_ship_80"}},{"name":"get_promotion","arguments":{"promotion_id":"promo_gold_10"}}]} ``
   ← 결과 1,642B: `` {"batch":[{"name":"get_promotion","result":{"status":"succeeded","data":{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"$10.00 off one order in the member's birthday month.","percent_off":null,"amount_off":{"value":10.0,"currency":"USD"},"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_birthday"],"change_set_id":null,"version":1}}},{"name":"get_promotion","result":… (+1,042자) ``
- 모델 판단(추론 필드): We have list_active_promotions for weekend 2026-11-07 to 2026-11-08. Items: promo_autumn_knit - Autumn knitwear 15% - status running - discount_layer item_price - valid_for_member_tier everyone - valid_from 2026-11-01 to 2026-11-15 - applies to categories cat_knitwear product_count 26 promo_birthday - Birthday coupon - order_discount - member - $10 off one order in member's birthday month promo_free_ship_80 - Free shipping over $80 - add_on - everyone promo_gold_10 - Gold tier 10% - order_discount - gold User doesn't want to stack anything on top of knit sale. Need to explain stacking? The knit sale is item_price layer. Birthday coupon and Gold tier 10% are order_discount layer. Free shippin… (+417자)
4. 모델 → **`get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``
- 모델 판단(추론 필드): We have weekend: store time Friday Nov 6 2026 11:00 America/New_York. Weekend is Saturday Nov 7 and Sunday Nov 8 2026. We have list_active_promotions for 2026-11-07 to 2026-11-08. Items: promo_autumn_knit - Autumn knitwear 15% - running - discount_layer item_price - everyone - valid 2026-11-01 to 2026-11-15 - applies to categories cat_knitwear product_count 26 promo_birthday - Birthday coupon - running - order_discount - member - valid from 2026-01-01 no end - $10 off one order in member's birthday month. coupon_ids cpn_birthday promo_free_ship_80 - Free shipping over $80 - running - add_on - everyone - free standard shipping when item subtotal before member benefits >= $80 promo_gold_10 - G… (+1,724자)

**답변 1**
> This weekend in store time — Sat 2026-11-07 to Sun 2026-11-08 — 4 promotions overlap the period.
>
> **Running on the knit sale**
>
> * **promo_autumn_knit – Autumn knitwear 15%**
>   status: running
>   discount_layer: item_price
>   valid_for_member_tier: everyone
>   valid_from: 2026-11-01T00:00:00-04:00 → valid_through: 2026-11-15T23:59:00-05:00
>   applies_to: scope categories, category_ids [cat_knitwear], product_count 26
>   15% off all knitwear for everyone. 260 price specifications.
>
> **Other promotions live the same weekend**
>
> * **promo_birthday – Birthday coupon**
>   status: running
>   discount_layer: order_discount
>   valid_for_member_tier: member
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   $10.00 off one order in the member's birthday month.
>   applies_to: scope order
>   coupon_ids: [cpn_birthday]
>
> * **promo_free_ship_80 – Free shipping over $80**
>   status: running
>   discount_layer: add_on
>   valid_for_member_tier: everyone
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   Free standard shipping when the item subtotal before member benefits is $80.00 or more.
>   applies_to: scope order
>
> * **promo_gold_10 – Gold tier 10%**
>   status: running
>   discount_layer: order_discount
>   valid_for_member_tier: gold
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   Gold members get a 10% order coupon every month.
>   applies_to: scope order
>   coupon_ids: [cpn_gold_10]
>
> The knit sale is an `item_price` promotion on cat_knitwear. The Birthday coupon and Gold tier 10% are `order_discount` promotions, and Free shipping over $80 is an `add_on` promotion. If you do not want anything to stack on top of the knit sale, avoid adding additional `item_price` promotions that target the same knitwear category/products for 2026-11-07 to 2026-11-08.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-batch · 2회차 · ✓ 통과

토큰 21,710 · 52.143초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 1,989토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 모델 판단(추론 필드): We need to find promotions live this weekend. Store time: Friday, November 6, 2026, 11:00 America/New_York. This weekend = Saturday Nov 7 and Sunday Nov 8? Possibly also Friday? "this weekend" likely Saturday-Sunday. Need promos live this weekend. Don't want to stack anything on top of knit sale. So need to identify knit sale promotion, and other promos live, and note stacking rules. We need to use tools. Likely promotion › promotion: list_active_promotions, search_promotions, get_promotion. Also need to know dates. We need to find promotions active on weekend. list_active_promotions probably returns active now. But need this weekend. Might need to search promotions with start/end dates. We … (+779자)
1. 모델 → **`a2api_load`** `` {"names":["list_active_promotions","search_promotions","get_promotion"]} ``
   ← 결과 73B: `` {"loaded":["list_active_promotions","search_promotions","get_promotion"]} ``
- 모델 판단(추론 필드): We need promos live this weekend. Store time: Friday, November 6, 2026, 11:00 America/New_York. Weekend = Saturday Nov 7 and Sunday Nov 8? Possibly also Friday? "this weekend" likely Saturday 7 and Sunday 8. Could include Friday evening? Probably Saturday-Sunday. We need list active promotions for period. Need valid_from and valid_through. Use list_active_promotions with valid_from = 2026-11-07T00:00, valid_through = 2026-11-08T23:59. Also maybe include Friday? Let's assume weekend starts Saturday. Could also include Friday night? Might be safe to check Saturday and Sunday. Also user says don't want to stack anything on top of the knit sale. So need to identify knit sale promotion. Probably … (+808자)
2. 모델 → **`a2api_batch`** `` {"calls":[{"name":"search_promotions","arguments":{"query":"knit","limit":20}},{"name":"list_active_promotions","arguments":{"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","limit":100}}]} ``
   ← 결과 1,534B: `` {"batch":[{"name":"search_promotions","result":{"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00"}],"total":1}}},{"name":"list_active_promotions","result":{"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through… (+934자) ``
- 모델 판단(추론 필드): We have search promotions for knit: promo_autumn_knit running 2026-11-01 to 2026-11-15. That's the knit sale. List active promotions for weekend 2026-11-07 to 2026-11-08: items: promo_autumn_knit - item_price, everyone, categories cat_knitwear, product_count 26 promo_birthday - order_discount, member, order scope promo_free_ship_80 - add_on, everyone, order scope promo_gold_10 - order_discount, gold tier User doesn't want to stack anything on top of knit sale. So we need to list promos live this weekend, and note stacking? Possibly need to check if any overlap? The user says I don't want to stack anything on top of the knit sale. Maybe they want to know which promos are live, and which would… (+1,733자)
3. 모델 → **`a2api_batch`** `` {"calls":[{"name":"get_promotion","arguments":{"promotion_id":"promo_birthday"}},{"name":"get_promotion","arguments":{"promotion_id":"promo_free_ship_80"}},{"name":"get_promotion","arguments":{"promotion_id":"promo_gold_10"}}]} ``
   ← 결과 1,642B: `` {"batch":[{"name":"get_promotion","result":{"status":"succeeded","data":{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"$10.00 off one order in the member's birthday month.","percent_off":null,"amount_off":{"value":10.0,"currency":"USD"},"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_birthday"],"change_set_id":null,"version":1}}},{"name":"get_promotion","result":… (+1,042자) ``
- 모델 판단(추론 필드): We have list_active_promotions for weekend 2026-11-07 to 2026-11-08. Items: promo_autumn_knit - Autumn knitwear 15% - status running - discount_layer item_price - valid_for_member_tier everyone - valid_from 2026-11-01 to 2026-11-15 - applies to categories cat_knitwear product_count 26 promo_birthday - Birthday coupon - order_discount - member - $10 off one order in member's birthday month promo_free_ship_80 - Free shipping over $80 - add_on - everyone promo_gold_10 - Gold tier 10% - order_discount - gold User doesn't want to stack anything on top of knit sale. Need to explain stacking? The knit sale is item_price layer. Birthday coupon and Gold tier 10% are order_discount layer. Free shippin… (+417자)
4. 모델 → **`get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``
- 모델 판단(추론 필드): We have weekend: store time Friday Nov 6 2026 11:00 America/New_York. Weekend is Saturday Nov 7 and Sunday Nov 8 2026. We have list_active_promotions for 2026-11-07 to 2026-11-08. Items: promo_autumn_knit - Autumn knitwear 15% - running - discount_layer item_price - everyone - valid 2026-11-01 to 2026-11-15 - applies to categories cat_knitwear product_count 26 promo_birthday - Birthday coupon - running - order_discount - member - valid from 2026-01-01 no end - $10 off one order in member's birthday month. coupon_ids cpn_birthday promo_free_ship_80 - Free shipping over $80 - running - add_on - everyone - free standard shipping when item subtotal before member benefits >= $80 promo_gold_10 - G… (+1,724자)

**답변 1**
> This weekend in store time — Sat 2026-11-07 to Sun 2026-11-08 — 4 promotions overlap the period.
>
> **Running on the knit sale**
>
> * **promo_autumn_knit – Autumn knitwear 15%**
>   status: running
>   discount_layer: item_price
>   valid_for_member_tier: everyone
>   valid_from: 2026-11-01T00:00:00-04:00 → valid_through: 2026-11-15T23:59:00-05:00
>   applies_to: scope categories, category_ids [cat_knitwear], product_count 26
>   15% off all knitwear for everyone. 260 price specifications.
>
> **Other promotions live the same weekend**
>
> * **promo_birthday – Birthday coupon**
>   status: running
>   discount_layer: order_discount
>   valid_for_member_tier: member
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   $10.00 off one order in the member's birthday month.
>   applies_to: scope order
>   coupon_ids: [cpn_birthday]
>
> * **promo_free_ship_80 – Free shipping over $80**
>   status: running
>   discount_layer: add_on
>   valid_for_member_tier: everyone
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   Free standard shipping when the item subtotal before member benefits is $80.00 or more.
>   applies_to: scope order
>
> * **promo_gold_10 – Gold tier 10%**
>   status: running
>   discount_layer: order_discount
>   valid_for_member_tier: gold
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   Gold members get a 10% order coupon every month.
>   applies_to: scope order
>   coupon_ids: [cpn_gold_10]
>
> The knit sale is an `item_price` promotion on cat_knitwear. The Birthday coupon and Gold tier 10% are `order_discount` promotions, and Free shipping over $80 is an `add_on` promotion. If you do not want anything to stack on top of the knit sale, avoid adding additional `item_price` promotions that target the same knitwear category/products for 2026-11-07 to 2026-11-08.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-batch-guard · 1회차 · ✓ 통과

토큰 17,153 · 51.604초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 1,989토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 모델 판단(추론 필드): We need to find promotions live this weekend. Store time: Friday, November 6, 2026, 11:00 America/New_York. This weekend = Saturday Nov 7 and Sunday Nov 8? Possibly also Friday? "this weekend" likely Saturday-Sunday. Need promos live this weekend. Don't want to stack anything on top of knit sale. So need to identify knit sale promotion, and other promos live, and note stacking rules. We need to use tools. Likely promotion › promotion: list_active_promotions, search_promotions, get_promotion. Also need to know dates. We need to find promotions active on weekend. list_active_promotions probably returns active now. But need this weekend. Might need to search promotions with start/end dates. We … (+367자)
1. 모델 → **`a2api_load`** `` {"names":["search_promotions","list_active_promotions","get_promotion"]} ``
   ← 결과 73B: `` {"loaded":["search_promotions","list_active_promotions","get_promotion"]} ``
- 모델 판단(추론 필드): We need promos live this weekend. Store time: Friday, November 6, 2026, 11:00 America/New_York. Weekend = Saturday Nov 7 and Sunday Nov 8? Possibly also Friday evening? "this weekend" likely Saturday 7 and Sunday 8. Could include Friday? Let's assume weekend starts Saturday 00:00 to Sunday 23:59. Could also include Friday night? Safer to check from 2026-11-07T00:00 to 2026-11-08T23:59. We need promos live. Also don't want to stack anything on top of knit sale. So need to identify knit sale promotion. Probably promotion name contains knit. Need to find knit sale promo. First find promotions with query "knit" or "knit sale". Use search_promotions with query "knit". Then list active promotions … (+825자)
2. 모델 → **`a2api_batch`** `` {"calls":[{"name":"search_promotions","arguments":{"query":"knit","limit":20}},{"name":"list_active_promotions","arguments":{"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","limit":100}}]} ``
   ← 결과 1,534B: `` {"batch":[{"name":"search_promotions","result":{"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00"}],"total":1}}},{"name":"list_active_promotions","result":{"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through… (+934자) ``
- 모델 판단(추론 필드): We have search_promotions for knit: promo_autumn_knit running 2026-11-01 to 2026-11-15. list_active_promotions for weekend 2026-11-07 to 2026-11-08: items: promo_autumn_knit - item_price, everyone, categories cat_knitwear, product_count 26 promo_birthday - order_discount, member, order scope promo_free_ship_80 - add_on, everyone promo_gold_10 - order_discount, gold User doesn't want to stack anything on top of knit sale. So we need to note which promos are live this weekend, and note stacking constraints? Possibly need to check if any overlap? The user says I don't want to stack anything on top of the knit sale. Maybe they want to know which promos are live, and which would stack? The knit s… (+1,683자)
3. 모델 → **`a2api_batch`** `` {"calls":[{"name":"get_promotion","arguments":{"promotion_id":"promo_autumn_knit"}},{"name":"get_promotion","arguments":{"promotion_id":"promo_birthday"}},{"name":"get_promotion","arguments":{"promotion_id":"promo_free_ship_80"}},{"name":"get_promotion","arguments":{"promotion_id":"promo_gold_10"}}]} ``
   ← 결과 2,185B: `` {"batch":[{"name":"get_promotion","result":{"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}}},{"name":"get_promotion","result":{"status":"suc… (+1,585자) ``
- 모델 판단(추론 필드): We have weekend: store time Friday Nov 6 2026 11:00 America/New_York. Weekend is Saturday Nov 7 and Sunday Nov 8 2026. We have list_active_promotions for 2026-11-07 to 2026-11-08. Items: promo_autumn_knit - Autumn knitwear 15% - running - discount_layer item_price - valid_for_member_tier everyone - valid_from 2026-11-01 to 2026-11-15 - applies to categories cat_knitwear product_count 26 promo_birthday - Birthday coupon - running - discount_layer order_discount - valid_for_member_tier member - valid_from 2026-01-01 onward - applies to order promo_free_ship_80 - Free shipping over $80 - running - discount_layer add_on - everyone promo_gold_10 - Gold tier 10% - running - discount_layer order_di… (+2,199자)

**답변 1**
> This weekend in store time — Sat 2026-11-07 to Sun 2026-11-08 — 4 promotions overlap the period and are running/scheduled.
>
> **Live for everyone**
>
> * **promo_autumn_knit – Autumn knitwear 15%**
>   status: running
>   discount_layer: item_price
>   valid_for_member_tier: everyone
>   valid_from: 2026-11-01T00:00:00-04:00 → valid_through: 2026-11-15T23:59:00-05:00
>   applies_to: scope categories, category_ids [cat_knitwear], product_count 26
>   15% off all knitwear. price_specification_count 260. No coupon.
>
> * **promo_free_ship_80 – Free shipping over $80**
>   status: running
>   discount_layer: add_on
>   valid_for_member_tier: everyone
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   applies_to: scope order
>   Free standard shipping when item subtotal before member benefits is $80.00 or more.
>
> **Live for members / tiers**
>
> * **promo_birthday – Birthday coupon**
>   status: running
>   discount_layer: order_discount
>   valid_for_member_tier: member
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   applies_to: scope order
>   $10.00 off one order in the member’s birthday month. coupon_ids: cpn_birthday
>
> * **promo_gold_10 – Gold tier 10%**
>   status: running
>   discount_layer: order_discount
>   valid_for_member_tier: gold
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   applies_to: scope order
>   10% order coupon every month for Gold members. coupon_ids: cpn_gold_10
>
> The knit sale is an `item_price` promotion on cat_knitwear. The other three live promos are on different layers:
> * order_discount: Birthday coupon, Gold tier 10%
> * add_on: Free shipping over $80
>
> Those layers are the ones that would normally stack on top of an item_price sale. If you want zero stacking on the knit sale this weekend, those order_discount / add_on promotions would need to be paused or restricted for the knitwear category.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-batch-guard · 2회차 · ✓ 통과

토큰 17,153 · 51.925초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 1,989토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 모델 판단(추론 필드): We need to find promotions live this weekend. Store time: Friday, November 6, 2026, 11:00 America/New_York. This weekend = Saturday Nov 7 and Sunday Nov 8? Possibly also Friday? "this weekend" likely Saturday-Sunday. Need promos live this weekend. Don't want to stack anything on top of knit sale. So need to identify knit sale promotion, and other promos live, and note stacking rules. We need to use tools. Likely promotion › promotion: list_active_promotions, search_promotions, get_promotion. Also need to know dates. We need to find promotions active on weekend. list_active_promotions probably returns active now. But need this weekend. Might need to search promotions with start/end dates. We … (+367자)
1. 모델 → **`a2api_load`** `` {"names":["search_promotions","list_active_promotions","get_promotion"]} ``
   ← 결과 73B: `` {"loaded":["search_promotions","list_active_promotions","get_promotion"]} ``
- 모델 판단(추론 필드): We need promos live this weekend. Store time: Friday, November 6, 2026, 11:00 America/New_York. Weekend = Saturday Nov 7 and Sunday Nov 8? Possibly also Friday evening? "this weekend" likely Saturday 7 and Sunday 8. Could include Friday? Let's assume weekend starts Saturday 00:00 to Sunday 23:59. Could also include Friday night? Safer to check from 2026-11-07T00:00 to 2026-11-08T23:59. We need promos live. Also don't want to stack anything on top of knit sale. So need to identify knit sale promotion. Probably promotion name contains knit. Need to find knit sale promo. First find promotions with query "knit" or "knit sale". Use search_promotions with query "knit". Then list active promotions … (+825자)
2. 모델 → **`a2api_batch`** `` {"calls":[{"name":"search_promotions","arguments":{"query":"knit","limit":20}},{"name":"list_active_promotions","arguments":{"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","limit":100}}]} ``
   ← 결과 1,534B: `` {"batch":[{"name":"search_promotions","result":{"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00"}],"total":1}}},{"name":"list_active_promotions","result":{"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through… (+934자) ``
- 모델 판단(추론 필드): We have search_promotions for knit: promo_autumn_knit running 2026-11-01 to 2026-11-15. list_active_promotions for weekend 2026-11-07 to 2026-11-08: items: promo_autumn_knit - item_price, everyone, categories cat_knitwear, product_count 26 promo_birthday - order_discount, member, order scope promo_free_ship_80 - add_on, everyone promo_gold_10 - order_discount, gold User doesn't want to stack anything on top of knit sale. So we need to note which promos are live this weekend, and note stacking constraints? Possibly need to check if any overlap? The user says I don't want to stack anything on top of the knit sale. Maybe they want to know which promos are live, and which would stack? The knit s… (+1,683자)
3. 모델 → **`a2api_batch`** `` {"calls":[{"name":"get_promotion","arguments":{"promotion_id":"promo_autumn_knit"}},{"name":"get_promotion","arguments":{"promotion_id":"promo_birthday"}},{"name":"get_promotion","arguments":{"promotion_id":"promo_free_ship_80"}},{"name":"get_promotion","arguments":{"promotion_id":"promo_gold_10"}}]} ``
   ← 결과 2,185B: `` {"batch":[{"name":"get_promotion","result":{"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}}},{"name":"get_promotion","result":{"status":"suc… (+1,585자) ``
- 모델 판단(추론 필드): We have weekend: store time Friday Nov 6 2026 11:00 America/New_York. Weekend is Saturday Nov 7 and Sunday Nov 8 2026. We have list_active_promotions for 2026-11-07 to 2026-11-08. Items: promo_autumn_knit - Autumn knitwear 15% - running - discount_layer item_price - valid_for_member_tier everyone - valid_from 2026-11-01 to 2026-11-15 - applies to categories cat_knitwear product_count 26 promo_birthday - Birthday coupon - running - discount_layer order_discount - valid_for_member_tier member - valid_from 2026-01-01 onward - applies to order promo_free_ship_80 - Free shipping over $80 - running - discount_layer add_on - everyone promo_gold_10 - Gold tier 10% - running - discount_layer order_di… (+2,199자)

**답변 1**
> This weekend in store time — Sat 2026-11-07 to Sun 2026-11-08 — 4 promotions overlap the period and are running/scheduled.
>
> **Live for everyone**
>
> * **promo_autumn_knit – Autumn knitwear 15%**
>   status: running
>   discount_layer: item_price
>   valid_for_member_tier: everyone
>   valid_from: 2026-11-01T00:00:00-04:00 → valid_through: 2026-11-15T23:59:00-05:00
>   applies_to: scope categories, category_ids [cat_knitwear], product_count 26
>   15% off all knitwear. price_specification_count 260. No coupon.
>
> * **promo_free_ship_80 – Free shipping over $80**
>   status: running
>   discount_layer: add_on
>   valid_for_member_tier: everyone
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   applies_to: scope order
>   Free standard shipping when item subtotal before member benefits is $80.00 or more.
>
> **Live for members / tiers**
>
> * **promo_birthday – Birthday coupon**
>   status: running
>   discount_layer: order_discount
>   valid_for_member_tier: member
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   applies_to: scope order
>   $10.00 off one order in the member’s birthday month. coupon_ids: cpn_birthday
>
> * **promo_gold_10 – Gold tier 10%**
>   status: running
>   discount_layer: order_discount
>   valid_for_member_tier: gold
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   applies_to: scope order
>   10% order coupon every month for Gold members. coupon_ids: cpn_gold_10
>
> The knit sale is an `item_price` promotion on cat_knitwear. The other three live promos are on different layers:
> * order_discount: Birthday coupon, Gold tier 10%
> * add_on: Free shipping over $80
>
> Those layers are the ones that would normally stack on top of an item_price sale. If you want zero stacking on the knit sale this weekend, those order_discount / add_on promotions would need to be paused or restricted for the knitwear category.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)
