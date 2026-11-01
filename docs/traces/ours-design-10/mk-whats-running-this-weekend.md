# mk-whats-running-this-weekend — ours-design-10

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `c8c944e`

**과업**

> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 필요한 도구: `list_active_promotions`
- 허용 도구: `get_promotion`, `search_promotions`
- 답에 있어야 할 사실: four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwear 15% (everyone, until Nov 15), Birthday coupon (members), Free shipping over $80 (everyone), Gold tier 10% (gold)
- 답에 있어야 할 사실: the knit sale covers 26 knitwear products

### a2api-acom · 1회차 · E MODEL_CALL_LIMIT

토큰 81,953 · 66.843초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 3,773토큰

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
   ← 결과 363B: `` {"selected":[{"name":"acom_list_policies","id":"acom.list_policies"},{"name":"acom_get_return_policy","id":"acom.get_return_policy"},{"name":"acom_get_policy","id":"acom.get_policy"},{"name":"acom_get_action_log","id":"acom.get_action_log"},{"name":"acom_get_tenant","id":"acom.get_tenant"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8, 15, 15, 80, 10 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.56, 재현율 1.00)

### a2api-acom · 2회차 · E MODEL_CALL_LIMIT

토큰 81,953 · 64.983초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 3,773토큰

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
   ← 결과 363B: `` {"selected":[{"name":"acom_list_policies","id":"acom.list_policies"},{"name":"acom_get_return_policy","id":"acom.get_return_policy"},{"name":"acom_get_policy","id":"acom.get_policy"},{"name":"acom_get_action_log","id":"acom.get_action_log"},{"name":"acom_get_tenant","id":"acom.get_tenant"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8, 15, 15, 80, 10 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.56, 재현율 1.00)

### a2api-acom-names-norelated · 1회차 · ✓ 통과

토큰 15,973 · 40.439초 · 모델 호출 4회 · 도구 호출 7회 · 첫 요청 프롬프트 1,989토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`a2api_load`** `` {"names":["list_active_promotions","search_promotions","get_promotion"]} ``
   ← 결과 73B: `` {"loaded":["list_active_promotions","search_promotions","get_promotion"]} ``
2. 모델 → **`list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"} ``
   ← 결과 1,164B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"applies_to":{"scope":"order","category_ids":[],"prod… (+564자) ``
3. 모델 → **`search_promotions`** `` {"query":"knit"} ``
   ← 결과 276B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00"}],"total":1}} ``
4. 모델 → **`get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``
5. 모델 → **`get_promotion`** `` {"promotion_id":"promo_birthday"} ``
   ← 결과 522B: `` {"status":"succeeded","data":{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"$10.00 off one order in the member's birthday month.","percent_off":null,"amount_off":{"value":10.0,"currency":"USD"},"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_birthday"],"change_set_id":null,"version":1}} ``
6. 모델 → **`get_promotion`** `` {"promotion_id":"promo_free_ship_80"} ``
   ← 결과 521B: `` {"status":"succeeded","data":{"id":"promo_free_ship_80","name":"Free shipping over $80","status":"running","discount_layer":"add_on","valid_for_member_tier":"everyone","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Free standard shipping when the item subtotal before member benefits is $80.00 or more.","percent_off":null,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":[],"change_set_id":null,"version":1}} ``
7. 모델 → **`get_promotion`** `` {"promotion_id":"promo_gold_10"} ``
   ← 결과 483B: `` {"status":"succeeded","data":{"id":"promo_gold_10","name":"Gold tier 10%","status":"running","discount_layer":"order_discount","valid_for_member_tier":"gold","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Gold members get a 10% order coupon every month.","percent_off":10,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_gold_10"],"change_set_id":null,"version":1}} ``

**답변 1**
> This weekend in store time — Sat 2026-11-07 to Sun 2026-11-08 — 4 promotions overlap the period.
>
> **Running now and covering the weekend**
>
> * **promo_autumn_knit — Autumn knitwear 15%**
>   * status: running
>   * layer: item_price
>   * tier: everyone
>   * valid: 2026-11-01 00:00-04:00 → 2026-11-15 23:59-05:00
>   * applies to: categories cat_knitwear, 26 products, 260 price specifications
>   * 15% off all knitwear for everyone. This is the knit sale you referenced.
>
> * **promo_birthday — Birthday coupon**
>   * status: running
>   * layer: order_discount
>   * tier: member
>   * valid: 2026-01-01 → no end date
>   * $10.00 off one order in the member’s birthday month. Coupon cpn_birthday.
>   * Applies to order scope.
>
> * **promo_free_ship_80 — Free shipping over $80**
>   * status: running
>   * layer: add_on
>   * tier: everyone
>   * valid: 2026-01-01 → no end date
>   * Free standard shipping when item subtotal before member benefits is $80.00 or more.
>   * Applies to order scope.
>
> * **promo_gold_10 — Gold tier 10%**
>   * status: running
>   * layer: order_discount
>   * tier: gold
>   * valid: 2026-01-01 → no end date
>   * Gold members get a 10% order coupon every month. Coupon cpn_gold_10.
>   * Applies to order scope.
>
> Stacking note for your request:
> The knit sale is an `item_price` promotion on cat_knitwear. The other live weekend promos are on different layers:
> * `order_discount` — Birthday coupon and Gold tier 10%
> * `add_on` — Free shipping over $80
>
> Item-price vs order-discount / add-on are different discount layers, so they are the promotions that would normally be considered alongside the knit sale. If you want zero stacking on top of the knit sale, you would need to avoid adding any additional `item_price` promotions that target the same knitwear category/products during 2026-11-07–2026-11-08.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-norelated · 2회차 · ✓ 통과

토큰 20,248 · 54.726초 · 모델 호출 5회 · 도구 호출 7회 · 첫 요청 프롬프트 1,989토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`a2api_load`** `` {"names":["list_active_promotions","search_promotions","get_promotion"]} ``
   ← 결과 73B: `` {"loaded":["list_active_promotions","search_promotions","get_promotion"]} ``
2. 모델 → **`search_promotions`** `` {"query":"knit","limit":20} ``
   ← 결과 276B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00"}],"total":1}} ``
3. 모델 → **`list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"} ``
   ← 결과 1,164B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"applies_to":{"scope":"order","category_ids":[],"prod… (+564자) ``
4. 모델 → **`get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``
5. 모델 → **`get_promotion`** `` {"promotion_id":"promo_birthday"} ``
   ← 결과 522B: `` {"status":"succeeded","data":{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"$10.00 off one order in the member's birthday month.","percent_off":null,"amount_off":{"value":10.0,"currency":"USD"},"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_birthday"],"change_set_id":null,"version":1}} ``
6. 모델 → **`get_promotion`** `` {"promotion_id":"promo_free_ship_80"} ``
   ← 결과 521B: `` {"status":"succeeded","data":{"id":"promo_free_ship_80","name":"Free shipping over $80","status":"running","discount_layer":"add_on","valid_for_member_tier":"everyone","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Free standard shipping when the item subtotal before member benefits is $80.00 or more.","percent_off":null,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":[],"change_set_id":null,"version":1}} ``
7. 모델 → **`get_promotion`** `` {"promotion_id":"promo_gold_10"} ``
   ← 결과 483B: `` {"status":"succeeded","data":{"id":"promo_gold_10","name":"Gold tier 10%","status":"running","discount_layer":"order_discount","valid_for_member_tier":"gold","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Gold members get a 10% order coupon every month.","percent_off":10,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_gold_10"],"change_set_id":null,"version":1}} ``

**답변 1**
> This weekend in store time America/New_York is Sat 2026-11-07 to Sun 2026-11-08.
>
> Live promotions that overlap that period:
>
> * **promo_autumn_knit – Autumn knitwear 15%**
>   status: running
>   discount_layer: item_price
>   valid_for_member_tier: everyone
>   valid_from: 2026-11-01T00:00:00-04:00 → valid_through: 2026-11-15T23:59:00-05:00
>   applies_to: scope categories, category_ids [cat_knitwear], product_count 26
>   15% off all knitwear for everyone. price_specification_count 260
>
> * **promo_birthday – Birthday coupon**
>   status: running
>   discount_layer: order_discount
>   valid_for_member_tier: member
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   applies_to: scope order
>   $10.00 off one order in the member's birthday month. coupon_ids [cpn_birthday]
>
> * **promo_free_ship_80 – Free shipping over $80**
>   status: running
>   discount_layer: add_on
>   valid_for_member_tier: everyone
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   applies_to: scope order
>   Free standard shipping when the item subtotal before member benefits is $80.00 or more.
>
> * **promo_gold_10 – Gold tier 10%**
>   status: running
>   discount_layer: order_discount
>   valid_for_member_tier: gold
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   applies_to: scope order
>   Gold members get a 10% order coupon every month. coupon_ids [cpn_gold_10]
>
> The knit sale is an `item_price` promotion on cat_knitwear. The other three live promos are on different layers:
> * order_discount: promo_birthday, promo_gold_10
> * add_on: promo_free_ship_80
>
> If you want to avoid stacking anything on top of the knit sale, the item_price layer is only occupied by promo_autumn_knit this weekend.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-batch · 1회차 · ✓ 통과

토큰 16,792 · 43.272초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 2,175토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`a2api_load`** `` {"names":["search_promotions","list_active_promotions","get_promotion"]} ``
   ← 결과 73B: `` {"loaded":["search_promotions","list_active_promotions","get_promotion"]} ``
2. 모델 → **`a2api_batch`** `` {"calls":[{"name":"search_promotions","arguments":{"query":"knit","limit":20}},{"name":"list_active_promotions","arguments":{"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","limit":100}}]} ``
   ← 결과 1,534B: `` {"batch":[{"name":"search_promotions","result":{"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00"}],"total":1}}},{"name":"list_active_promotions","result":{"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through… (+900자) ``
3. 모델 → **`a2api_batch`** `` {"calls":[{"name":"get_promotion","arguments":{"promotion_id":"promo_autumn_knit"}},{"name":"get_promotion","arguments":{"promotion_id":"promo_birthday"}},{"name":"get_promotion","arguments":{"promotion_id":"promo_free_ship_80"}},{"name":"get_promotion","arguments":{"promotion_id":"promo_gold_10"}}]} ``
   ← 결과 2,185B: `` {"batch":[{"name":"get_promotion","result":{"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}}},{"name":"get_promotion","result":{"status":"suc… (+900자) ``

**답변 1**
> This weekend 2026-11-07 to 2026-11-08, store time, 4 promotions overlap the period and are reachable for shoppers.
>
> **Running now and covering the weekend**
>
> * **promo_autumn_knit – Autumn knitwear 15%**
>   * status: running
>   * discount_layer: item_price
>   * valid_for_member_tier: everyone
>   * period: 2026-11-01T00:00:00-04:00 → 2026-11-15T23:59:00-05:00
>   * applies_to: scope categories, category_ids [cat_knitwear], product_count 26
>   * 15% off all knitwear for everyone. price_specification_count 260. No coupon.
>
> * **promo_birthday – Birthday coupon**
>   * status: running
>   * discount_layer: order_discount
>   * valid_for_member_tier: member
>   * period: 2026-01-01T00:00:00-05:00 → null
>   * applies_to: scope order
>   * $10.00 off one order in the member’s birthday month. coupon_ids [cpn_birthday]
>
> * **promo_free_ship_80 – Free shipping over $80**
>   * status: running
>   * discount_layer: add_on
>   * valid_for_member_tier: everyone
>   * period: 2026-01-01T00:00:00-05:00 → null
>   * applies_to: scope order
>   * Free standard shipping when item subtotal before member benefits is $80.00 or more.
>
> * **promo_gold_10 – Gold tier 10%**
>   * status: running
>   * discount_layer: order_discount
>   * valid_for_member_tier: gold
>   * period: 2026-01-01T00:00:00-05:00 → null
>   * applies_to: scope order
>   * Gold members get a 10% order coupon every month. coupon_ids [cpn_gold_10]
>
> Stacking note for your request:
> The knit sale is `item_price`. The other three live promos are on different layers:
> * Birthday coupon and Gold tier 10% are `order_discount`
> * Free shipping over $80 is `add_on`
>
> Different layers can be applied together in the system. If you do not want anything to stack on top of the Autumn knitwear 15% item-price sale this weekend, the promotions that would stack with it are promo_birthday, promo_gold_10 and promo_free_ship_80.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-batch · 2회차 · ✓ 통과

토큰 21,888 · 51.609초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 2,175토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`a2api_load`** `` {"names":["list_active_promotions","search_promotions","get_promotion"]} ``
   ← 결과 73B: `` {"loaded":["list_active_promotions","search_promotions","get_promotion"]} ``
2. 모델 → **`a2api_batch`** `` {"calls":[{"name":"list_active_promotions","arguments":{"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"}},{"name":"search_promotions","arguments":{"query":"knit","limit":20}}]} ``
   ← 결과 1,534B: `` {"batch":[{"name":"list_active_promotions","result":{"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"… (+900자) ``
3. 모델 → **`a2api_batch`** `` {"calls":[{"name":"get_promotion","arguments":{"promotion_id":"promo_birthday"}},{"name":"get_promotion","arguments":{"promotion_id":"promo_free_ship_80"}},{"name":"get_promotion","arguments":{"promotion_id":"promo_gold_10"}}]} ``
   ← 결과 1,642B: `` {"batch":[{"name":"get_promotion","result":{"status":"succeeded","data":{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"$10.00 off one order in the member's birthday month.","percent_off":null,"amount_off":{"value":10.0,"currency":"USD"},"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_birthday"],"change_set_id":null,"version":1}}},{"name":"get_promotion","result":… (+900자) ``
4. 모델 → **`a2api_batch`** `` {"calls":[{"name":"get_promotion","arguments":{"promotion_id":"promo_autumn_knit"}}]} ``
   ← 결과 554B: `` {"batch":[{"name":"get_promotion","result":{"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}}}]} ``

**답변 1**
> This weekend in store time — Sat 2026-11-07 to Sun 2026-11-08 — 4 promotions overlap the period.
>
> **Live now**
>
> * **promo_autumn_knit — Autumn knitwear 15%**
>   status: running
>   discount_layer: item_price
>   valid_for_member_tier: everyone
>   valid_from: 2026-11-01T00:00:00-04:00 → valid_through: 2026-11-15T23:59:00-05:00
>   applies_to: scope categories, category_ids [cat_knitwear], product_count 26
>   15% off all knitwear for everyone. price_specification_count 260
>
> * **promo_birthday — Birthday coupon**
>   status: running
>   discount_layer: order_discount
>   valid_for_member_tier: member
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   applies_to: scope order
>   $10.00 off one order in the member's birthday month. amount_off 10.0 USD
>   coupon_ids: cpn_birthday
>
> * **promo_free_ship_80 — Free shipping over $80**
>   status: running
>   discount_layer: add_on
>   valid_for_member_tier: everyone
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   applies_to: scope order
>   Free standard shipping when the item subtotal before member benefits is $80.00 or more.
>
> * **promo_gold_10 — Gold tier 10%**
>   status: running
>   discount_layer: order_discount
>   valid_for_member_tier: gold
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   applies_to: scope order
>   Gold members get a 10% order coupon every month. percent_off 10
>   coupon_ids: cpn_gold_10
>
> The knit sale you mentioned is promo_autumn_knit, item_price layer on cat_knitwear 2026-11-01 to 2026-11-15.
>
> Stacking note: the three other live promos are on different layers:
> * Birthday coupon and Gold tier 10% are order_discount
> * Free shipping over $80 is add_on
>
> Those layers are distinct from the knit sale’s item_price layer, so in the current setup they would be able to apply together with the 15% knitwear price on an order. If you want no stacking on top of the knit sale, you would need to keep those order_discount / add_on promotions from applying to knitwear orders this weekend.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)
