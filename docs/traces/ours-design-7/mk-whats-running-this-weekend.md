# mk-whats-running-this-weekend — ours-design-7

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 필요한 도구: `list_active_promotions`
- 허용 도구: `get_promotion`, `search_promotions`
- 답에 있어야 할 사실: four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwear 15% (everyone, until Nov 15), Birthday coupon (members), Free shipping over $80 (everyone), Gold tier 10% (gold)
- 답에 있어야 할 사실: the knit sale covers 26 knitwear products

### a2api-acom · 1회차 · E MODEL_CALL_LIMIT

토큰 81,953 · 66.018초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 3,773토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`acom_list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"} ``
   ← 결과 1,164B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"applies_to":{"scope":"order","category_ids":[],"prod… (+564자) ``
2. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``
3. 모델 → **`acom_describe_data`** `` {"term":"discount_layer"} ``
   ← 결과 547B: `` {"status":"succeeded","data":{"items":[{"table":"promotion.promotion","kind":"table","term":"schema:OfferCatalog/acom:Promotion","id_prefix":"promo","description":"a time-boxed benefit that groups member and sale prices or an order discount. id prefix promo_.","columns":[{"name":"discount_layer","type":"text","nullable":false,"term":"acom:discountLayer","description":"where the benefit applies when benefits are calculated. values: discount_layer","values":["item_price","order_discount","add_on"],"values_list":"discount_layer"}]}],"total":1}} ``
4. 모델 → **`a2api_search`** `` {"query":"promotion stacking"} ``
   ← 결과 377B: `` {"selected":[{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_end_promotion","id":"acom.end_promotion"},{"name":"acom_get_promotion","id":"acom.get_promotion"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
5. 모델 → **`acom_describe_data`** `` {"schema":"promotion","table":"promotion.promotion"} ``
   ← 결과 4,589B: `` {"status":"succeeded","data":{"items":[{"table":"promotion.promotion","kind":"table","term":"schema:OfferCatalog/acom:Promotion","id_prefix":"promo","description":"a time-boxed benefit that groups member and sale prices or an order discount. id prefix promo_.","columns":[{"name":"tenant_id","type":"text","nullable":false,"term":"-","description":"store (tenant) that owns this row; row-level security key.","references":"platform.online_store"},{"name":"id","type":"text","nullable":false,"term":"-","description":"id with prefix promo_; the same value the API, logs and events use."},{"name":"name… (+900자) ``
6. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_birthday"} ``
   ← 결과 522B: `` {"status":"succeeded","data":{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"$10.00 off one order in the member's birthday month.","percent_off":null,"amount_off":{"value":10.0,"currency":"USD"},"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_birthday"],"change_set_id":null,"version":1}} ``
7. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_free_ship_80"} ``
   ← 결과 521B: `` {"status":"succeeded","data":{"id":"promo_free_ship_80","name":"Free shipping over $80","status":"running","discount_layer":"add_on","valid_for_member_tier":"everyone","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Free standard shipping when the item subtotal before member benefits is $80.00 or more.","percent_off":null,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":[],"change_set_id":null,"version":1}} ``
8. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_gold_10"} ``
   ← 결과 483B: `` {"status":"succeeded","data":{"id":"promo_gold_10","name":"Gold tier 10%","status":"running","discount_layer":"order_discount","valid_for_member_tier":"gold","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Gold members get a 10% order coupon every month.","percent_off":10,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_gold_10"],"change_set_id":null,"version":1}} ``
9. 모델 → **`a2api_search`** `` {"query":"stacking"} ``
   ← 결과 304B: `` {"selected":[{"name":"acom_create_coupon","id":"acom.create_coupon"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match was already offered in this conversation. If they cannot answer, tell the user what is missing instead of searching again."} ``
10. 모델 → **`acom_describe_data`** `` {"api_name":"stacking"} ``
   ← 결과 568B: `` {"status":"succeeded","data":{"items":[{"table":"promotion.coupon","kind":"table","term":"schema:Offer/acom:Coupon","id_prefix":"cpn","description":"a coupon tied to a promotion; it records the promotion's benefit on the order and never adds a second discount. id prefix cpn_.","columns":[{"name":"stacking","type":"text","nullable":false,"term":"acom:stacking","description":"which other coupons may be used in the same order. values: coupon_stacking","values":["no_tier_coupons","with_tier_coupons","no_other_coupons"],"values_list":"coupon_stacking"}]}],"total":1}} ``
11. 모델 → **`acom_describe_data`** `` {"term":"acom:stacking"} ``
   ← 결과 568B: `` {"status":"succeeded","data":{"items":[{"table":"promotion.coupon","kind":"table","term":"schema:Offer/acom:Coupon","id_prefix":"cpn","description":"a coupon tied to a promotion; it records the promotion's benefit on the order and never adds a second discount. id prefix cpn_.","columns":[{"name":"stacking","type":"text","nullable":false,"term":"acom:stacking","description":"which other coupons may be used in the same order. values: coupon_stacking","values":["no_tier_coupons","with_tier_coupons","no_other_coupons"],"values_list":"coupon_stacking"}]}],"total":1}} ``
12. 모델 → **`a2api_search`** `` {"query":"stacking policy"} ``
   ← 결과 427B: `` {"selected":[{"name":"acom_list_policies","id":"acom.list_policies"},{"name":"acom_get_return_policy","id":"acom.get_return_policy"},{"name":"acom_get_policy","id":"acom.get_policy"},{"name":"acom_get_action_log","id":"acom.get_action_log"},{"name":"acom_get_tenant","id":"acom.get_tenant"}],"evicted":["acom_explain_sales_change","acom_schedule_display"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8, 15, 15, 80, 10 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.56, 재현율 1.00)

### a2api-acom · 2회차 · E MODEL_CALL_LIMIT

토큰 81,953 · 64.903초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 3,773토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`acom_list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"} ``
   ← 결과 1,164B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"applies_to":{"scope":"order","category_ids":[],"prod… (+564자) ``
2. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``
3. 모델 → **`acom_describe_data`** `` {"term":"discount_layer"} ``
   ← 결과 547B: `` {"status":"succeeded","data":{"items":[{"table":"promotion.promotion","kind":"table","term":"schema:OfferCatalog/acom:Promotion","id_prefix":"promo","description":"a time-boxed benefit that groups member and sale prices or an order discount. id prefix promo_.","columns":[{"name":"discount_layer","type":"text","nullable":false,"term":"acom:discountLayer","description":"where the benefit applies when benefits are calculated. values: discount_layer","values":["item_price","order_discount","add_on"],"values_list":"discount_layer"}]}],"total":1}} ``
4. 모델 → **`a2api_search`** `` {"query":"promotion stacking"} ``
   ← 결과 377B: `` {"selected":[{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_end_promotion","id":"acom.end_promotion"},{"name":"acom_get_promotion","id":"acom.get_promotion"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
5. 모델 → **`acom_describe_data`** `` {"schema":"promotion","table":"promotion.promotion"} ``
   ← 결과 4,589B: `` {"status":"succeeded","data":{"items":[{"table":"promotion.promotion","kind":"table","term":"schema:OfferCatalog/acom:Promotion","id_prefix":"promo","description":"a time-boxed benefit that groups member and sale prices or an order discount. id prefix promo_.","columns":[{"name":"tenant_id","type":"text","nullable":false,"term":"-","description":"store (tenant) that owns this row; row-level security key.","references":"platform.online_store"},{"name":"id","type":"text","nullable":false,"term":"-","description":"id with prefix promo_; the same value the API, logs and events use."},{"name":"name… (+900자) ``
6. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_birthday"} ``
   ← 결과 522B: `` {"status":"succeeded","data":{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"$10.00 off one order in the member's birthday month.","percent_off":null,"amount_off":{"value":10.0,"currency":"USD"},"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_birthday"],"change_set_id":null,"version":1}} ``
7. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_free_ship_80"} ``
   ← 결과 521B: `` {"status":"succeeded","data":{"id":"promo_free_ship_80","name":"Free shipping over $80","status":"running","discount_layer":"add_on","valid_for_member_tier":"everyone","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Free standard shipping when the item subtotal before member benefits is $80.00 or more.","percent_off":null,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":[],"change_set_id":null,"version":1}} ``
8. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_gold_10"} ``
   ← 결과 483B: `` {"status":"succeeded","data":{"id":"promo_gold_10","name":"Gold tier 10%","status":"running","discount_layer":"order_discount","valid_for_member_tier":"gold","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Gold members get a 10% order coupon every month.","percent_off":10,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_gold_10"],"change_set_id":null,"version":1}} ``
9. 모델 → **`a2api_search`** `` {"query":"stacking"} ``
   ← 결과 304B: `` {"selected":[{"name":"acom_create_coupon","id":"acom.create_coupon"}],"moreAvailable":false,"page":1,"pageLimitReached":false,"progress":true,"note":"No new functions: every match was already offered in this conversation. If they cannot answer, tell the user what is missing instead of searching again."} ``
10. 모델 → **`acom_describe_data`** `` {"api_name":"stacking"} ``
   ← 결과 568B: `` {"status":"succeeded","data":{"items":[{"table":"promotion.coupon","kind":"table","term":"schema:Offer/acom:Coupon","id_prefix":"cpn","description":"a coupon tied to a promotion; it records the promotion's benefit on the order and never adds a second discount. id prefix cpn_.","columns":[{"name":"stacking","type":"text","nullable":false,"term":"acom:stacking","description":"which other coupons may be used in the same order. values: coupon_stacking","values":["no_tier_coupons","with_tier_coupons","no_other_coupons"],"values_list":"coupon_stacking"}]}],"total":1}} ``
11. 모델 → **`acom_describe_data`** `` {"term":"acom:stacking"} ``
   ← 결과 568B: `` {"status":"succeeded","data":{"items":[{"table":"promotion.coupon","kind":"table","term":"schema:Offer/acom:Coupon","id_prefix":"cpn","description":"a coupon tied to a promotion; it records the promotion's benefit on the order and never adds a second discount. id prefix cpn_.","columns":[{"name":"stacking","type":"text","nullable":false,"term":"acom:stacking","description":"which other coupons may be used in the same order. values: coupon_stacking","values":["no_tier_coupons","with_tier_coupons","no_other_coupons"],"values_list":"coupon_stacking"}]}],"total":1}} ``
12. 모델 → **`a2api_search`** `` {"query":"stacking policy"} ``
   ← 결과 427B: `` {"selected":[{"name":"acom_list_policies","id":"acom.list_policies"},{"name":"acom_get_return_policy","id":"acom.get_return_policy"},{"name":"acom_get_policy","id":"acom.get_policy"},{"name":"acom_get_action_log","id":"acom.get_action_log"},{"name":"acom_get_tenant","id":"acom.get_tenant"}],"evicted":["acom_explain_sales_change","acom_schedule_display"],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8, 15, 15, 80, 10 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.56, 재현율 1.00)

### a2api-acom-index · 1회차 · ✓ 통과

토큰 63,667 · 55.264초 · 모델 호출 7회 · 도구 호출 6회 · 첫 요청 프롬프트 6,994토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`a2api_load`** `` {"names":["list_active_promotions","search_promotions","get_promotion"]} ``
   ← 결과 73B: `` {"loaded":["list_active_promotions","search_promotions","get_promotion"]} ``
2. 모델 → **`list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"} ``
   ← 결과 1,164B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"applies_to":{"scope":"order","category_ids":[],"prod… (+564자) ``
3. 모델 → **`get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``
4. 모델 → **`get_promotion`** `` {"promotion_id":"promo_birthday"} ``
   ← 결과 522B: `` {"status":"succeeded","data":{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"$10.00 off one order in the member's birthday month.","percent_off":null,"amount_off":{"value":10.0,"currency":"USD"},"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_birthday"],"change_set_id":null,"version":1}} ``
5. 모델 → **`get_promotion`** `` {"promotion_id":"promo_free_ship_80"} ``
   ← 결과 521B: `` {"status":"succeeded","data":{"id":"promo_free_ship_80","name":"Free shipping over $80","status":"running","discount_layer":"add_on","valid_for_member_tier":"everyone","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Free standard shipping when the item subtotal before member benefits is $80.00 or more.","percent_off":null,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":[],"change_set_id":null,"version":1}} ``
6. 모델 → **`get_promotion`** `` {"promotion_id":"promo_gold_10"} ``
   ← 결과 483B: `` {"status":"succeeded","data":{"id":"promo_gold_10","name":"Gold tier 10%","status":"running","discount_layer":"order_discount","valid_for_member_tier":"gold","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Gold members get a 10% order coupon every month.","percent_off":10,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_gold_10"],"change_set_id":null,"version":1}} ``

**답변 1**
> This weekend, Fri 7 Nov 2026 – Sat 8 Nov 2026, the store has 4 promotions whose period overlaps the weekend.
>
> **Item-price – the knit sale you mentioned**
> * **promo_autumn_knit – Autumn knitwear 15%**
>   * status: running
>   * discount_layer: item_price
>   * valid_for_member_tier: everyone
>   * valid_from: 2026-11-01T00:00:00-04:00 → valid_through: 2026-11-15T23:59:00-05:00
>   * applies_to: scope categories, category_ids [cat_knitwear], product_count 26
>   * 15% off all knitwear for everyone. price_specification_count 260
>   * description: “15% off all knitwear for everyone.”
>
> No other item_price promotions are active for the weekend, so there is nothing else that would change the knitwear list price on top of the 15% sale.
>
> **Order-level / add-on promotions that are also live this weekend**
>
> * **promo_birthday – Birthday coupon**
>   * status: running
>   * discount_layer: order_discount
>   * valid_for_member_tier: member
>   * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   * applies_to: scope order
>   * $10.00 off one order in the member’s birthday month. coupon_ids [cpn_birthday]
>   * This is an order discount, i.e. it would apply after the item-price knit sale.
>
> * **promo_gold_10 – Gold tier 10%**
>   * status: running
>   * discount_layer: order_discount
>   * valid_for_member_tier: gold
>   * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   * applies_to: scope order
>   * Gold members get a 10% order coupon every month. coupon_ids [cpn_gold_10]
>   * Order discount, so it would stack on top of the knitwear 15% item price if used.
>
> * **promo_free_ship_80 – Free shipping over $80**
>   * status: running
>   * discount_layer: add_on
>   * valid_for_member_tier: everyone
>   * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   * applies_to: scope order
>   * Free standard shipping when the item subtotal before member benefits is $80.00 or more.
>
> If you do not want anything to stack on top of the Autumn knitwear 15% item-price sale, avoid applying the Birthday $10… (+157자)

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-index · 2회차 · ✓ 통과

토큰 63,667 · 54.814초 · 모델 호출 7회 · 도구 호출 6회 · 첫 요청 프롬프트 6,994토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`a2api_load`** `` {"names":["list_active_promotions","search_promotions","get_promotion"]} ``
   ← 결과 73B: `` {"loaded":["list_active_promotions","search_promotions","get_promotion"]} ``
2. 모델 → **`list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"} ``
   ← 결과 1,164B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"applies_to":{"scope":"order","category_ids":[],"prod… (+564자) ``
3. 모델 → **`get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``
4. 모델 → **`get_promotion`** `` {"promotion_id":"promo_birthday"} ``
   ← 결과 522B: `` {"status":"succeeded","data":{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"$10.00 off one order in the member's birthday month.","percent_off":null,"amount_off":{"value":10.0,"currency":"USD"},"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_birthday"],"change_set_id":null,"version":1}} ``
5. 모델 → **`get_promotion`** `` {"promotion_id":"promo_free_ship_80"} ``
   ← 결과 521B: `` {"status":"succeeded","data":{"id":"promo_free_ship_80","name":"Free shipping over $80","status":"running","discount_layer":"add_on","valid_for_member_tier":"everyone","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Free standard shipping when the item subtotal before member benefits is $80.00 or more.","percent_off":null,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":[],"change_set_id":null,"version":1}} ``
6. 모델 → **`get_promotion`** `` {"promotion_id":"promo_gold_10"} ``
   ← 결과 483B: `` {"status":"succeeded","data":{"id":"promo_gold_10","name":"Gold tier 10%","status":"running","discount_layer":"order_discount","valid_for_member_tier":"gold","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Gold members get a 10% order coupon every month.","percent_off":10,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_gold_10"],"change_set_id":null,"version":1}} ``

**답변 1**
> This weekend, Fri 7 Nov 2026 – Sat 8 Nov 2026, the store has 4 promotions whose period overlaps the weekend.
>
> **Item-price – the knit sale you mentioned**
> * **promo_autumn_knit – Autumn knitwear 15%**
>   * status: running
>   * discount_layer: item_price
>   * valid_for_member_tier: everyone
>   * valid_from: 2026-11-01T00:00:00-04:00 → valid_through: 2026-11-15T23:59:00-05:00
>   * applies_to: scope categories, category_ids [cat_knitwear], product_count 26
>   * 15% off all knitwear for everyone. price_specification_count 260
>   * description: “15% off all knitwear for everyone.”
>
> No other item_price promotions are active for the weekend, so there is nothing else that would change the knitwear list price on top of the 15% sale.
>
> **Order-level / add-on promotions that are also live this weekend**
>
> * **promo_birthday – Birthday coupon**
>   * status: running
>   * discount_layer: order_discount
>   * valid_for_member_tier: member
>   * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   * applies_to: scope order
>   * $10.00 off one order in the member’s birthday month. coupon_ids [cpn_birthday]
>   * This is an order discount, i.e. it would apply after the item-price knit sale.
>
> * **promo_gold_10 – Gold tier 10%**
>   * status: running
>   * discount_layer: order_discount
>   * valid_for_member_tier: gold
>   * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   * applies_to: scope order
>   * Gold members get a 10% order coupon every month. coupon_ids [cpn_gold_10]
>   * Order discount, so it would stack on top of the knitwear 15% item price if used.
>
> * **promo_free_ship_80 – Free shipping over $80**
>   * status: running
>   * discount_layer: add_on
>   * valid_for_member_tier: everyone
>   * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   * applies_to: scope order
>   * Free standard shipping when the item subtotal before member benefits is $80.00 or more.
>
> If you do not want anything to stack on top of the Autumn knitwear 15% item-price sale, avoid applying the Birthday $10… (+157자)

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-graph · 1회차 · ✓ 통과

토큰 63,922 · 55.731초 · 모델 호출 7회 · 도구 호출 6회 · 첫 요청 프롬프트 6,994토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`a2api_load`** `` {"names":["list_active_promotions","search_promotions","get_promotion"]} ``
   ← 결과 73B: `` {"loaded":["list_active_promotions","search_promotions","get_promotion"]} ``
2. 모델 → **`list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"} ``
   ← 결과 1,259B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"applies_to":{"scope":"order","category_ids":[],"prod… (+659자) ``
3. 모델 → **`get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``
4. 모델 → **`get_promotion`** `` {"promotion_id":"promo_birthday"} ``
   ← 결과 522B: `` {"status":"succeeded","data":{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"$10.00 off one order in the member's birthday month.","percent_off":null,"amount_off":{"value":10.0,"currency":"USD"},"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_birthday"],"change_set_id":null,"version":1}} ``
5. 모델 → **`get_promotion`** `` {"promotion_id":"promo_free_ship_80"} ``
   ← 결과 521B: `` {"status":"succeeded","data":{"id":"promo_free_ship_80","name":"Free shipping over $80","status":"running","discount_layer":"add_on","valid_for_member_tier":"everyone","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Free standard shipping when the item subtotal before member benefits is $80.00 or more.","percent_off":null,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":[],"change_set_id":null,"version":1}} ``
6. 모델 → **`get_promotion`** `` {"promotion_id":"promo_gold_10"} ``
   ← 결과 483B: `` {"status":"succeeded","data":{"id":"promo_gold_10","name":"Gold tier 10%","status":"running","discount_layer":"order_discount","valid_for_member_tier":"gold","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Gold members get a 10% order coupon every month.","percent_off":10,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_gold_10"],"change_set_id":null,"version":1}} ``

**답변 1**
> This weekend 7-8 Nov 2026, store time America/New_York, 4 promotions overlap the period:
>
> * **promo_autumn_knit – Autumn knitwear 15%**
>   status: running
>   discount_layer: item_price
>   valid_for_member_tier: everyone
>   valid_from: 2026-11-01T00:00:00-04:00 → valid_through: 2026-11-15T23:59:00-05:00
>   applies_to: scope categories, category_ids [cat_knitwear], product_count 26
>   15% off all knitwear for everyone. price_specification_count 260. No coupons.
>
> * **promo_birthday – Birthday coupon**
>   status: running
>   discount_layer: order_discount
>   valid_for_member_tier: member
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   $10.00 off one order in the member's birthday month. coupon_ids [cpn_birthday]
>
> * **promo_free_ship_80 – Free shipping over $80**
>   status: running
>   discount_layer: add_on
>   valid_for_member_tier: everyone
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   Free standard shipping when the item subtotal before member benefits is $80.00 or more.
>
> * **promo_gold_10 – Gold tier 10%**
>   status: running
>   discount_layer: order_discount
>   valid_for_member_tier: gold
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   Gold members get a 10% order coupon every month. coupon_ids [cpn_gold_10]
>
> The knit sale is an item_price promotion on cat_knitwear. The other three live promos are order-level / add-on:
>
> * Birthday coupon and Gold tier 10% are order_discount layer, so they would apply on top of the item-price knitwear discount if used on the same order.
> * Free shipping over $80 is add_on layer, also stacks with the item-price knitwear discount.
>
> If you want no stacking on top of the Autumn knitwear 15% sale, avoid applying the Birthday coupon / Gold tier 10% order coupons to knitwear orders this weekend; free shipping over $80 will still apply based on subtotal.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-graph · 2회차 · ✓ 통과

토큰 85,422 · 88.618초 · 모델 호출 9회 · 도구 호출 8회 · 첫 요청 프롬프트 6,994토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`a2api_load`** `` {"names":["list_active_promotions","search_promotions","get_promotion"]} ``
   ← 결과 73B: `` {"loaded":["list_active_promotions","search_promotions","get_promotion"]} ``
2. 모델 → **`list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"} ``
   ← 결과 1,259B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"applies_to":{"scope":"order","category_ids":[],"prod… (+659자) ``
3. 모델 → **`get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``
4. 모델 → **`get_promotion`** `` {"promotion_id":"promo_birthday"} ``
   ← 결과 522B: `` {"status":"succeeded","data":{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"$10.00 off one order in the member's birthday month.","percent_off":null,"amount_off":{"value":10.0,"currency":"USD"},"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_birthday"],"change_set_id":null,"version":1}} ``
5. 모델 → **`get_promotion`** `` {"promotion_id":"promo_free_ship_80"} ``
   ← 결과 521B: `` {"status":"succeeded","data":{"id":"promo_free_ship_80","name":"Free shipping over $80","status":"running","discount_layer":"add_on","valid_for_member_tier":"everyone","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Free standard shipping when the item subtotal before member benefits is $80.00 or more.","percent_off":null,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":[],"change_set_id":null,"version":1}} ``
6. 모델 → **`get_promotion`** `` {"promotion_id":"promo_gold_10"} ``
   ← 결과 483B: `` {"status":"succeeded","data":{"id":"promo_gold_10","name":"Gold tier 10%","status":"running","discount_layer":"order_discount","valid_for_member_tier":"gold","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Gold members get a 10% order coupon every month.","percent_off":10,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_gold_10"],"change_set_id":null,"version":1}} ``
7. 모델 → **`search_promotions`** `` {"query":"knit","limit":20} ``
   ← 결과 371B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00"}],"total":1},"next":"Functions that take IDs from this result: get_promotion, create_coupon (promotion_id)"} ``
8. 모델 → **`search_promotions`** `` {"discount_layer":"item_price","status":["running","scheduled"],"limit":100} ``
   ← 결과 371B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00"}],"total":1},"next":"Functions that take IDs from this result: get_promotion, create_coupon (promotion_id)"} ``

**답변 1**
> This weekend 7-8 Nov 2026 the store has 4 promotions overlapping the period:
>
> * **promo_autumn_knit – Autumn knitwear 15%**
>   status: running
>   discount_layer: item_price
>   valid_for_member_tier: everyone
>   valid_from: 2026-11-01T00:00:00-04:00 → valid_through: 2026-11-15T23:59:00-05:00
>   applies_to: scope categories, category_ids [cat_knitwear], product_count 26
>   price_specification_count: 260
>   description: 15% off all knitwear for everyone.
>
> * **promo_birthday – Birthday coupon**
>   status: running
>   discount_layer: order_discount
>   valid_for_member_tier: member
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   applies_to: scope order
>   amount_off: $10.00 USD
>   description: $10.00 off one order in the member's birthday month.
>   coupon_ids: [cpn_birthday]
>
> * **promo_free_ship_80 – Free shipping over $80**
>   status: running
>   discount_layer: add_on
>   valid_for_member_tier: everyone
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   applies_to: scope order
>   description: Free standard shipping when the item subtotal before member benefits is $80.00 or more.
>
> * **promo_gold_10 – Gold tier 10%**
>   status: running
>   discount_layer: order_discount
>   valid_for_member_tier: gold
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   applies_to: scope order
>   percent_off: 10
>   description: Gold members get a 10% order coupon every month.
>   coupon_ids: [cpn_gold_10]
>
> Item-price promotions active for the weekend:
> Only promo_autumn_knit is an item_price promotion. Search for item_price running/scheduled promotions returns just promo_autumn_knit, so there is no other item-price sale to stack on top of the knit sale.
>
> The other live promos are order_discount / add_on:
> * Birthday coupon and Gold tier 10% are order_discounts – they would apply to the order total and would stack on top of the 15% knit item price if used on an order containing knitwear.
> * Free shipping over $80 is an add_on shipping benefit.
>
> If you want to keep the knit sale un-… (+178자)

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names · 1회차 · ✓ 통과

토큰 22,772 · 56.222초 · 모델 호출 6회 · 도구 호출 7회 · 첫 요청 프롬프트 1,635토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`a2api_load`** `` {"names":["list_active_promotions","get_promotion","search_promotions"]} ``
   ← 결과 73B: `` {"loaded":["list_active_promotions","get_promotion","search_promotions"]} ``
2. 모델 → **`search_promotions`** `` {"query":"knit","limit":20} ``
   ← 결과 371B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00"}],"total":1},"next":"Functions that take IDs from this result: get_promotion, create_coupon (promotion_id)"} ``
3. 모델 → **`list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"} ``
   ← 결과 1,259B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"applies_to":{"scope":"order","category_ids":[],"prod… (+659자) ``
4. 모델 → **`get_promotion`** `` {"promotion_id":"promo_birthday"} ``
   ← 결과 522B: `` {"status":"succeeded","data":{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"$10.00 off one order in the member's birthday month.","percent_off":null,"amount_off":{"value":10.0,"currency":"USD"},"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_birthday"],"change_set_id":null,"version":1}} ``
5. 모델 → **`get_promotion`** `` {"promotion_id":"promo_free_ship_80"} ``
   ← 결과 521B: `` {"status":"succeeded","data":{"id":"promo_free_ship_80","name":"Free shipping over $80","status":"running","discount_layer":"add_on","valid_for_member_tier":"everyone","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Free standard shipping when the item subtotal before member benefits is $80.00 or more.","percent_off":null,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":[],"change_set_id":null,"version":1}} ``
6. 모델 → **`get_promotion`** `` {"promotion_id":"promo_gold_10"} ``
   ← 결과 483B: `` {"status":"succeeded","data":{"id":"promo_gold_10","name":"Gold tier 10%","status":"running","discount_layer":"order_discount","valid_for_member_tier":"gold","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Gold members get a 10% order coupon every month.","percent_off":10,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_gold_10"],"change_set_id":null,"version":1}} ``
7. 모델 → **`get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``

**답변 1**
> This weekend in store time — Sat 2026-11-07 to Sun 2026-11-08 — the following promotions overlap the period and are active for shoppers:
>
> **1. promo_autumn_knit — Autumn knitwear 15%**
> * status: running
> * discount_layer: item_price
> * valid_for_member_tier: everyone
> * valid_from: 2026-11-01T00:00:00-04:00 → valid_through: 2026-11-15T23:59:00-05:00
> * applies_to: scope categories, category_ids [cat_knitwear], product_count 26
> * 15% off all knitwear for everyone. price_specification_count 260
>
> **2. promo_birthday — Birthday coupon**
> * status: running
> * discount_layer: order_discount
> * valid_for_member_tier: member
> * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
> * applies_to: scope order
> * $10.00 off one order in the member's birthday month. coupon_ids: cpn_birthday
>
> **3. promo_free_ship_80 — Free shipping over $80**
> * status: running
> * discount_layer: add_on
> * valid_for_member_tier: everyone
> * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
> * applies_to: scope order
> * Free standard shipping when the item subtotal before member benefits is $80.00 or more.
>
> **4. promo_gold_10 — Gold tier 10%**
> * status: running
> * discount_layer: order_discount
> * valid_for_member_tier: gold
> * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
> * applies_to: scope order
> * Gold members get a 10% order coupon every month. coupon_ids: cpn_gold_10
>
> Stacking note for your knit sale:
> * Autumn knitwear 15% is an **item_price** promotion on cat_knitwear.
> * Birthday coupon and Gold tier 10% are **order_discount** promotions.
> * Free shipping over $80 is an **add_on** promotion.
>
> If you do not want anything stacked on top of the knit sale, the order_discount promotions — Birthday coupon for members and Gold tier 10% for gold members — are the ones that would add an additional discount on the order level. Free shipping over $80 is an add-on layer and the knit sale itself is the only active item_price promotion for the weekend.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names · 2회차 · ✓ 통과

토큰 31,296 · 65.071초 · 모델 호출 8회 · 도구 호출 7회 · 첫 요청 프롬프트 1,635토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`a2api_load`** `` {"names":["list_active_promotions","get_promotion","search_promotions"]} ``
   ← 결과 73B: `` {"loaded":["list_active_promotions","get_promotion","search_promotions"]} ``
2. 모델 → **`list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"} ``
   ← 결과 1,259B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"applies_to":{"scope":"order","category_ids":[],"prod… (+659자) ``
3. 모델 → **`get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``
4. 모델 → **`get_promotion`** `` {"promotion_id":"promo_birthday"} ``
   ← 결과 522B: `` {"status":"succeeded","data":{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"$10.00 off one order in the member's birthday month.","percent_off":null,"amount_off":{"value":10.0,"currency":"USD"},"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_birthday"],"change_set_id":null,"version":1}} ``
5. 모델 → **`get_promotion`** `` {"promotion_id":"promo_free_ship_80"} ``
   ← 결과 521B: `` {"status":"succeeded","data":{"id":"promo_free_ship_80","name":"Free shipping over $80","status":"running","discount_layer":"add_on","valid_for_member_tier":"everyone","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Free standard shipping when the item subtotal before member benefits is $80.00 or more.","percent_off":null,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":[],"change_set_id":null,"version":1}} ``
6. 모델 → **`get_promotion`** `` {"promotion_id":"promo_gold_10"} ``
   ← 결과 483B: `` {"status":"succeeded","data":{"id":"promo_gold_10","name":"Gold tier 10%","status":"running","discount_layer":"order_discount","valid_for_member_tier":"gold","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Gold members get a 10% order coupon every month.","percent_off":10,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_gold_10"],"change_set_id":null,"version":1}} ``
7. 모델 → **`search_promotions`** `` {"query":"knit","limit":20} ``
   ← 결과 371B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00"}],"total":1},"next":"Functions that take IDs from this result: get_promotion, create_coupon (promotion_id)"} ``

**답변 1**
> This weekend in store time — Sat 2026-11-07 to Sun 2026-11-08 — 4 promotions are active / scheduled to be active:
>
> **1. promo_autumn_knit — Autumn knitwear 15%**
> * status: running
> * discount_layer: item_price
> * valid_for_member_tier: everyone
> * valid_from: 2026-11-01T00:00:00-04:00 → valid_through: 2026-11-15T23:59:00-05:00
> * applies_to: scope categories, category_ids [cat_knitwear], product_count 26
> * 15% off all knitwear for everyone. price_specification_count 260. No coupons.
>
> This is the knit sale you referenced.
>
> **2. promo_birthday — Birthday coupon**
> * status: running
> * discount_layer: order_discount
> * valid_for_member_tier: member
> * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
> * applies_to: scope order
> * $10.00 off one order in the member's birthday month. coupon_ids: cpn_birthday
>
> **3. promo_free_ship_80 — Free shipping over $80**
> * status: running
> * discount_layer: add_on
> * valid_for_member_tier: everyone
> * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
> * applies_to: scope order
> * Free standard shipping when the item subtotal before member benefits is $80.00 or more.
>
> **4. promo_gold_10 — Gold tier 10%**
> * status: running
> * discount_layer: order_discount
> * valid_for_member_tier: gold
> * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
> * applies_to: scope order
> * Gold members get a 10% order coupon every month. coupon_ids: cpn_gold_10
>
> Stacking note for your request:
> The knit sale is an `item_price` promotion on cat_knitwear. The other three live this weekend are on different layers:
> * Birthday coupon and Gold tier 10% are `order_discount`
> * Free shipping over $80 is `add_on`
>
> If you want to avoid any stacking on top of the knit sale, you would need to keep the item_price layer exclusive for knitwear items for the weekend. The order_discount and add_on promotions above are the only other live promotions that would be in scope for the 7-8 Nov period.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)
