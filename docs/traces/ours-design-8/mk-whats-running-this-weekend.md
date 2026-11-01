# mk-whats-running-this-weekend — ours-design-8

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 필요한 도구: `list_active_promotions`
- 허용 도구: `get_promotion`, `search_promotions`
- 답에 있어야 할 사실: four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwear 15% (everyone, until Nov 15), Birthday coupon (members), Free shipping over $80 (everyone), Gold tier 10% (gold)
- 답에 있어야 할 사실: the knit sale covers 26 knitwear products

### a2api-acom-names · 1회차 · ✓ 통과

토큰 26,275 · 53.233초 · 모델 호출 7회 · 도구 호출 6회 · 첫 요청 프롬프트 1,635토큰

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

**답변 1**
> This weekend (Sat 2026-11-07 00:00 – Sun 2026-11-08 23:59 America/New_York) the overlap check returns 4 promotions that are running / scheduled for the period.
>
> * **promo_autumn_knit – Autumn knitwear 15%**
>   * status: running
>   * discount_layer: item_price
>   * valid_for_member_tier: everyone
>   * valid_from: 2026-11-01T00:00:00-04:00
>   * valid_through: 2026-11-15T23:59:00-05:00
>   * applies_to: scope categories, category_ids [cat_knitwear], product_count 26
>   * description: 15% off all knitwear for everyone.
>   * percent_off: 15
>   * price_specification_count: 260
>
> * **promo_birthday – Birthday coupon**
>   * status: running
>   * discount_layer: order_discount
>   * valid_for_member_tier: member
>   * valid_from: 2026-01-01T00:00:00-05:00
>   * valid_through: null
>   * applies_to: scope order
>   * description: $10.00 off one order in the member's birthday month.
>   * amount_off: {value: 10.0, currency: USD}
>   * coupon_ids: [cpn_birthday]
>
> * **promo_free_ship_80 – Free shipping over $80**
>   * status: running
>   * discount_layer: add_on
>   * valid_for_member_tier: everyone
>   * valid_from: 2026-01-01T00:00:00-05:00
>   * valid_through: null
>   * applies_to: scope order
>   * description: Free standard shipping when the item subtotal before member benefits is $80.00 or more.
>
> * **promo_gold_10 – Gold tier 10%**
>   * status: running
>   * discount_layer: order_discount
>   * valid_for_member_tier: gold
>   * valid_from: 2026-01-01T00:00:00-05:00
>   * valid_through: null
>   * applies_to: scope order
>   * description: Gold members get a 10% order coupon every month.
>   * percent_off: 10
>   * coupon_ids: [cpn_gold_10]
>
> Stacking note for your request:
> The knit sale is the only active item_price promotion for the weekend. The other three live promos are on different layers:
> * order_discount: promo_birthday, promo_gold_10
> * add_on: promo_free_ship_80
>
> If you want nothing stacked on top of the Autumn knitwear 15% item_price sale, avoid applying the birthday coupon, Gold tier 10% order discount and the free-ship… (+44자)

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names · 2회차 · ✓ 통과

토큰 30,338 · 53.994초 · 모델 호출 8회 · 도구 호출 7회 · 첫 요청 프롬프트 1,635토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`a2api_load`** `` {"names":["list_active_promotions","get_promotion","search_promotions"]} ``
   ← 결과 73B: `` {"loaded":["list_active_promotions","get_promotion","search_promotions"]} ``
2. 모델 → **`search_promotions`** `` {"query":"knit","limit":20} ``
   ← 결과 371B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00"}],"total":1},"next":"Functions that take IDs from this result: get_promotion, create_coupon (promotion_id)"} ``
3. 모델 → **`list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","limit":100} ``
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
> This weekend 2026-11-07 to 2026-11-08 store time the promotions that overlap the period are:
>
> **1. promo_autumn_knit – Autumn knitwear 15%**
> * status: running
> * discount_layer: item_price
> * valid_for_member_tier: everyone
> * valid_from: 2026-11-01T00:00:00-04:00 → valid_through: 2026-11-15T23:59:00-05:00
> * applies_to: scope categories, category_ids [cat_knitwear], product_count 26
> * 15% off all knitwear for everyone. price_specification_count 260
>
> **2. promo_birthday – Birthday coupon**
> * status: running
> * discount_layer: order_discount
> * valid_for_member_tier: member
> * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
> * applies_to: scope order
> * $10.00 off one order in the member's birthday month. coupon_ids [cpn_birthday]
>
> **3. promo_free_ship_80 – Free shipping over $80**
> * status: running
> * discount_layer: add_on
> * valid_for_member_tier: everyone
> * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
> * applies_to: scope order
> * Free standard shipping when the item subtotal before member benefits is $80.00 or more.
>
> **4. promo_gold_10 – Gold tier 10%**
> * status: running
> * discount_layer: order_discount
> * valid_for_member_tier: gold
> * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
> * applies_to: scope order
> * Gold members get a 10% order coupon every month. percent_off 10. coupon_ids [cpn_gold_10]
>
> Stacking note for your request:
> * The knit sale is an `item_price` promotion on cat_knitwear.
> * promo_birthday and promo_gold_10 are `order_discount` layer promotions. They apply to the order total and would stack on top of the item-price knit discount if used together.
> * promo_free_ship_80 is an `add_on` layer promotion for shipping. It is a different layer from the knit `item_price` sale.
>
> If you want no stacking on top of the knit sale, avoid using the order-discount coupons Birthday coupon and Gold tier 10% on knitwear orders this weekend. Free shipping over $80 is the only live promotion this weekend that is a different layer from the kn… (+19자)

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-norelated · 1회차 · ✓ 통과

토큰 30,395 · 58.348초 · 모델 호출 8회 · 도구 호출 7회 · 첫 요청 프롬프트 1,635토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`a2api_load`** `` {"names":["list_active_promotions","get_promotion","search_promotions"]} ``
   ← 결과 73B: `` {"loaded":["list_active_promotions","get_promotion","search_promotions"]} ``
2. 모델 → **`search_promotions`** `` {"query":"knit","limit":20} ``
   ← 결과 276B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00"}],"total":1}} ``
3. 모델 → **`list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","limit":100} ``
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
> This weekend in store time is Sat 2026-11-07 to Sun 2026-11-08. The promotions that overlap that period are:
>
> **1. promo_autumn_knit – Autumn knitwear 15%**
> * status: running
> * discount_layer: item_price
> * valid_for_member_tier: everyone
> * valid_from: 2026-11-01T00:00:00-04:00 → valid_through: 2026-11-15T23:59:00-05:00
> * applies_to: scope categories, category_ids [cat_knitwear], product_count 26
> * 15% off all knitwear for everyone. price_specification_count 260. No coupons.
>
> This is the knit sale you referenced. It is live all weekend and runs through 15 Nov.
>
> **2. promo_birthday – Birthday coupon**
> * status: running
> * discount_layer: order_discount
> * valid_for_member_tier: member
> * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
> * applies_to: scope order
> * $10.00 off one order in the member's birthday month. coupon_ids: cpn_birthday
>
> **3. promo_free_ship_80 – Free shipping over $80**
> * status: running
> * discount_layer: add_on
> * valid_for_member_tier: everyone
> * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
> * applies_to: scope order
> * Free standard shipping when the item subtotal before member benefits is $80.00 or more.
>
> **4. promo_gold_10 – Gold tier 10%**
> * status: running
> * discount_layer: order_discount
> * valid_for_member_tier: gold
> * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
> * applies_to: scope order
> * Gold members get a 10% order coupon every month. coupon_ids: cpn_gold_10
>
> Stacking note:
> * The knit sale is an `item_price` promotion on cat_knitwear.
> * Birthday coupon and Gold tier 10% are `order_discount` promotions.
> * Free shipping over $80 is an `add_on` promotion.
>
> So the only other item_price promotion live this weekend is the knit sale itself. The three other live promos are on different discount layers – order_discount and add_on – which is how the system distinguishes stacking eligibility from another item_price offer. If you want no stacking on top of the knit sale, avoid applying the order_discount coupons … (+64자)

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-norelated · 2회차 · ✓ 통과

토큰 30,853 · 59.657초 · 모델 호출 8회 · 도구 호출 7회 · 첫 요청 프롬프트 1,635토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

1. 모델 → **`a2api_load`** `` {"names":["list_active_promotions","get_promotion","search_promotions"]} ``
   ← 결과 73B: `` {"loaded":["list_active_promotions","get_promotion","search_promotions"]} ``
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
7. 모델 → **`search_promotions`** `` {"query":"knit","discount_layer":"item_price"} ``
   ← 결과 276B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00"}],"total":1}} ``

**답변 1**
> This weekend in store time Fri 2026-11-07 to Sun 2026-11-08 the active promotions that overlap the period are:
>
> * **promo_autumn_knit – Autumn knitwear 15%**
>   * status: running
>   * discount_layer: item_price
>   * valid_for_member_tier: everyone
>   * valid_from: 2026-11-01T00:00:00-04:00 → valid_through: 2026-11-15T23:59:00-05:00
>   * applies_to: scope categories, category_ids [cat_knitwear], product_count 26
>   * 15% off all knitwear for everyone. price_specification_count 260
>
> * **promo_birthday – Birthday coupon**
>   * status: running
>   * discount_layer: order_discount
>   * valid_for_member_tier: member
>   * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   * applies_to: scope order
>   * $10.00 off one order in the member's birthday month. coupon_ids [cpn_birthday]
>
> * **promo_free_ship_80 – Free shipping over $80**
>   * status: running
>   * discount_layer: add_on
>   * valid_for_member_tier: everyone
>   * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   * applies_to: scope order
>   * Free standard shipping when the item subtotal before member benefits is $80.00 or more.
>
> * **promo_gold_10 – Gold tier 10%**
>   * status: running
>   * discount_layer: order_discount
>   * valid_for_member_tier: gold
>   * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   * applies_to: scope order
>   * Gold members get a 10% order coupon every month. coupon_ids [cpn_gold_10]
>
> Stacking note for the knit sale:
> The Autumn knitwear 15% is an `item_price` promotion on cat_knitwear. The only other `item_price` promotion found for “knit” is promo_autumn_knit itself.
>
> The other live promos this weekend are on different layers:
> * order_discount: promo_birthday, promo_gold_10
> * add_on: promo_free_ship_80
>
> If you want no stacking on top of the knit sale, avoid adding another `item_price` promotion that touches cat_knitwear. The order_discount and add_on promos are separate layers from the item_price knit sale.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)
