# mk-whats-running-this-weekend — ours-design-9

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 필요한 도구: `list_active_promotions`
- 허용 도구: `get_promotion`, `search_promotions`
- 답에 있어야 할 사실: four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwear 15% (everyone, until Nov 15), Birthday coupon (members), Free shipping over $80 (everyone), Gold tier 10% (gold)
- 답에 있어야 할 사실: the knit sale covers 26 knitwear products

### a2api-acom-hybrid · 1회차 · E MODEL_CALL_LIMIT

토큰 92,756 · 76.209초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 4,747토큰

준비: 전략 `index`, 함수 253개, 목차 4,645자(system prompt)

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`a2api_load`** `` {"names":["list_active_promotions","get_promotion"]} ``
   ← 결과 112B: `` {"already":["list_active_promotions","get_promotion"],"note":"These functions are already callable; call them."} ``
2. 모델 → **`list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"} ``
   ← 결과 1,164B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"applies_to":{"scope":"order","category_ids":[],"prod… (+564자) ``
3. 모델 → **`describe_data`** `` {"schema":"promotion"} ``
   ← 결과 5,112B: `` {"status":"succeeded","data":{"items":[{"table":"promotion.conditional_gift","kind":"table","term":"schema:Offer/acom:ConditionalGift","id_prefix":"cgf","description":"a gift added to an order whose subtotal before member benefits reaches a threshold, with one gift per threshold. id prefix cgf_.","columns":[{"name":"tenant_id","type":"text","nullable":false,"term":"-","description":"store (tenant) that owns this row; row-level security key.","references":"platform.online_store"},{"name":"id","type":"text","nullable":false,"term":"-","description":"id with prefix cgf_; the same value the API, l… (+900자) ``
4. 모델 → **`get_promotion`** `` {"promotion_id":"promo_autumn_knit","fields":["status","applies_to","discount_layer","valid_for_member_tier","valid_from","valid_through"]} ``
   ← 결과 312B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}}} ``
5. 모델 → **`describe_data`** `` {"schema":"promotion","table":"promotion.promotion"} ``
   ← 결과 4,589B: `` {"status":"succeeded","data":{"items":[{"table":"promotion.promotion","kind":"table","term":"schema:OfferCatalog/acom:Promotion","id_prefix":"promo","description":"a time-boxed benefit that groups member and sale prices or an order discount. id prefix promo_.","columns":[{"name":"tenant_id","type":"text","nullable":false,"term":"-","description":"store (tenant) that owns this row; row-level security key.","references":"platform.online_store"},{"name":"id","type":"text","nullable":false,"term":"-","description":"id with prefix promo_; the same value the API, logs and events use."},{"name":"name… (+900자) ``
6. 모델 → **`get_promotion`** `` {"promotion_id":"promo_birthday","fields":["status","discount_layer","valid_for_member_tier","valid_from","valid_through","applies_to","percent_off","amount_off_value"]} ``
   ← 실패 566B: `` {"status":"failed","error":{"code":"UPSTREAM_VALIDATION_FAILED","detail":"The backend rejected the request values. (HTTP 422) 'fields' names 'amount_off_value' this result does not have. Its top-level fields are amount_off, applies_to, change_set_id, coupon_ids, description, discount_layer, id, name, percent_off, price_specification_count, status, valid_for_member_tier, valid_from, valid_through, version. Name some of those, or leave 'fields' out to get all of them."},"hint":"The service rejected these values. Correct them only if the user gave other values."} ``
7. 모델 → **`get_promotion`** `` {"promotion_id":"promo_birthday","fields":["status","discount_layer","valid_for_member_tier","valid_from","valid_through","applies_to","percent_off"]} ``
   ← 결과 290B: `` {"status":"succeeded","data":{"id":"promo_birthday","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"percent_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null}}} ``
8. 모델 → **`get_promotion`** `` {"promotion_id":"promo_free_ship_80","fields":["status","discount_layer","valid_for_member_tier","valid_from","valid_through","applies_to","eligible_transaction_volume_value","eligible_transaction_volume_currency"]} ``
   ← 실패 623B: `` {"status":"failed","error":{"code":"UPSTREAM_VALIDATION_FAILED","detail":"The backend rejected the request values. (HTTP 422) 'fields' names 'eligible_transaction_volume_value', 'eligible_transaction_volume_currency' this result does not have. Its top-level fields are amount_off, applies_to, change_set_id, coupon_ids, description, discount_layer, id, name, percent_off, price_specification_count, status, valid_for_member_tier, valid_from, valid_through, version. Name some of those, or leave 'fields' out to get all of them."},"hint":"The service rejected these values. Correct them only if the us… (+23자) ``
9. 모델 → **`get_promotion`** `` {"promotion_id":"promo_free_ship_80","fields":["status","discount_layer","valid_for_member_tier","valid_from","valid_through","applies_to","percent_off","amount_off"]} ``
   ← 결과 306B: `` {"status":"succeeded","data":{"id":"promo_free_ship_80","status":"running","discount_layer":"add_on","valid_for_member_tier":"everyone","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"percent_off":null,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null}}} ``
10. 모델 → **`get_promotion`** `` {"promotion_id":"promo_gold_10","fields":["status","discount_layer","valid_for_member_tier","valid_from","valid_through","applies_to","percent_off"]} ``
   ← 결과 285B: `` {"status":"succeeded","data":{"id":"promo_gold_10","status":"running","discount_layer":"order_discount","valid_for_member_tier":"gold","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"percent_off":10,"applies_to":{"scope":"order","category_ids":[],"product_count":null}}} ``
11. 모델 → **`get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``
12. 모델 → **`get_promotion`** `` {"promotion_id":"promo_birthday"} ``
   ← 결과 522B: `` {"status":"succeeded","data":{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"$10.00 off one order in the member's birthday month.","percent_off":null,"amount_off":{"value":10.0,"currency":"USD"},"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_birthday"],"change_set_id":null,"version":1}} ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8, 15, 15, 80, 10 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.82, 재현율 1.00)

### a2api-acom-hybrid · 2회차 · E MODEL_CALL_LIMIT

토큰 92,756 · 75.244초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 4,747토큰

준비: 전략 `index`, 함수 253개, 목차 4,645자(system prompt)

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`a2api_load`** `` {"names":["list_active_promotions","get_promotion"]} ``
   ← 결과 112B: `` {"already":["list_active_promotions","get_promotion"],"note":"These functions are already callable; call them."} ``
2. 모델 → **`list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"} ``
   ← 결과 1,164B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"applies_to":{"scope":"order","category_ids":[],"prod… (+564자) ``
3. 모델 → **`describe_data`** `` {"schema":"promotion"} ``
   ← 결과 5,112B: `` {"status":"succeeded","data":{"items":[{"table":"promotion.conditional_gift","kind":"table","term":"schema:Offer/acom:ConditionalGift","id_prefix":"cgf","description":"a gift added to an order whose subtotal before member benefits reaches a threshold, with one gift per threshold. id prefix cgf_.","columns":[{"name":"tenant_id","type":"text","nullable":false,"term":"-","description":"store (tenant) that owns this row; row-level security key.","references":"platform.online_store"},{"name":"id","type":"text","nullable":false,"term":"-","description":"id with prefix cgf_; the same value the API, l… (+900자) ``
4. 모델 → **`get_promotion`** `` {"promotion_id":"promo_autumn_knit","fields":["status","applies_to","discount_layer","valid_for_member_tier","valid_from","valid_through"]} ``
   ← 결과 312B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}}} ``
5. 모델 → **`describe_data`** `` {"schema":"promotion","table":"promotion.promotion"} ``
   ← 결과 4,589B: `` {"status":"succeeded","data":{"items":[{"table":"promotion.promotion","kind":"table","term":"schema:OfferCatalog/acom:Promotion","id_prefix":"promo","description":"a time-boxed benefit that groups member and sale prices or an order discount. id prefix promo_.","columns":[{"name":"tenant_id","type":"text","nullable":false,"term":"-","description":"store (tenant) that owns this row; row-level security key.","references":"platform.online_store"},{"name":"id","type":"text","nullable":false,"term":"-","description":"id with prefix promo_; the same value the API, logs and events use."},{"name":"name… (+900자) ``
6. 모델 → **`get_promotion`** `` {"promotion_id":"promo_birthday","fields":["status","discount_layer","valid_for_member_tier","valid_from","valid_through","applies_to","percent_off","amount_off_value"]} ``
   ← 실패 566B: `` {"status":"failed","error":{"code":"UPSTREAM_VALIDATION_FAILED","detail":"The backend rejected the request values. (HTTP 422) 'fields' names 'amount_off_value' this result does not have. Its top-level fields are amount_off, applies_to, change_set_id, coupon_ids, description, discount_layer, id, name, percent_off, price_specification_count, status, valid_for_member_tier, valid_from, valid_through, version. Name some of those, or leave 'fields' out to get all of them."},"hint":"The service rejected these values. Correct them only if the user gave other values."} ``
7. 모델 → **`get_promotion`** `` {"promotion_id":"promo_birthday","fields":["status","discount_layer","valid_for_member_tier","valid_from","valid_through","applies_to","percent_off"]} ``
   ← 결과 290B: `` {"status":"succeeded","data":{"id":"promo_birthday","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"percent_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null}}} ``
8. 모델 → **`get_promotion`** `` {"promotion_id":"promo_free_ship_80","fields":["status","discount_layer","valid_for_member_tier","valid_from","valid_through","applies_to","eligible_transaction_volume_value","eligible_transaction_volume_currency"]} ``
   ← 실패 623B: `` {"status":"failed","error":{"code":"UPSTREAM_VALIDATION_FAILED","detail":"The backend rejected the request values. (HTTP 422) 'fields' names 'eligible_transaction_volume_value', 'eligible_transaction_volume_currency' this result does not have. Its top-level fields are amount_off, applies_to, change_set_id, coupon_ids, description, discount_layer, id, name, percent_off, price_specification_count, status, valid_for_member_tier, valid_from, valid_through, version. Name some of those, or leave 'fields' out to get all of them."},"hint":"The service rejected these values. Correct them only if the us… (+23자) ``
9. 모델 → **`get_promotion`** `` {"promotion_id":"promo_free_ship_80","fields":["status","discount_layer","valid_for_member_tier","valid_from","valid_through","applies_to","percent_off","amount_off"]} ``
   ← 결과 306B: `` {"status":"succeeded","data":{"id":"promo_free_ship_80","status":"running","discount_layer":"add_on","valid_for_member_tier":"everyone","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"percent_off":null,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null}}} ``
10. 모델 → **`get_promotion`** `` {"promotion_id":"promo_gold_10","fields":["status","discount_layer","valid_for_member_tier","valid_from","valid_through","applies_to","percent_off"]} ``
   ← 결과 285B: `` {"status":"succeeded","data":{"id":"promo_gold_10","status":"running","discount_layer":"order_discount","valid_for_member_tier":"gold","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"percent_off":10,"applies_to":{"scope":"order","category_ids":[],"product_count":null}}} ``
11. 모델 → **`get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``
12. 모델 → **`get_promotion`** `` {"promotion_id":"promo_birthday"} ``
   ← 결과 522B: `` {"status":"succeeded","data":{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"$10.00 off one order in the member's birthday month.","percent_off":null,"amount_off":{"value":10.0,"currency":"USD"},"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_birthday"],"change_set_id":null,"version":1}} ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8, 15, 15, 80, 10 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.82, 재현율 1.00)
