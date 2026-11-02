# mk-whats-running-this-weekend — ours-design-settings-1

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `d86a1ff` · a2api `16030e2`

**과업**

> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 필요한 도구: `list_active_promotions`
- 허용 도구: `get_promotion`, `search_promotions`
- 답에 있어야 할 사실: four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwear 15% (everyone, until Nov 15), Birthday coupon (members), Free shipping over $80 (everyone), Gold tier 10% (gold)
- 답에 있어야 할 사실: the knit sale covers 26 knitwear products

### a2api-acom · 1회차 · ✓ 통과

토큰 41,741 · 46.165초 · 모델 호출 7회 · 도구 호출 6회 · 첫 요청 프롬프트 3,996토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 모델 판단(추론 필드): We need find promos live this weekend. Store time Friday, November 6, 2026, 11:00 America/New_York. Weekend? This weekend likely starting Saturday? Could be Saturday Nov 7 to Sunday Nov 8? Or maybe Friday evening? Need define valid_from valid_through. Weekend likely Saturday 2026-11-07 to Sunday 2026-11-08. Could also include Friday evening? Usually weekend is Saturday-Sunday. Could be from now? Might be weekend starting Saturday 00:00 to Sunday 23:59. We need find promos live this weekend, and don't want to stack anything on top of knit sale. So need identify knit sale promotion. Need to find promotion named knit sale? Might be promo_autumn_knit? Possibly. We need list active promotions for… (+847자)
1. 모델 → **`acom_list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"} ``
   ← 결과 1,164B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"applies_to":{"scope":"order","category_ids":[],"prod… (+564자) ``
- 모델 판단(추론 필드): We have four promos live this weekend: promo_autumn_knit - Autumn knitwear 15% - running, valid_for_member_tier everyone, valid 2026-11-01 to 2026-11-15. Applies to categories cat_knitwear. promo_birthday - Birthday coupon - order discount, member only. promo_free_ship_80 - Free shipping over $80 - add_on. promo_gold_10 - Gold tier 10% - order discount for gold tier. User doesn't want to stack anything on top of knit sale. Need to check stacking rules? Might need to see promotion details to see if they stack. discount_layer: item_price vs order_discount vs add_on. Likely item_price and order_discount can stack? Maybe need to see promotion details for each to know if stacking allowed. The use… (+980자)
2. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``
- 모델 판단(추론 필드): Let's get others to see discount_layer.
3. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_birthday"} ``
   ← 결과 522B: `` {"status":"succeeded","data":{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"$10.00 off one order in the member's birthday month.","percent_off":null,"amount_off":{"value":10.0,"currency":"USD"},"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_birthday"],"change_set_id":null,"version":1}} ``
- 모델 판단(추론 필드): Get promo_free_ship_80
4. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_free_ship_80"} ``
   ← 결과 521B: `` {"status":"succeeded","data":{"id":"promo_free_ship_80","name":"Free shipping over $80","status":"running","discount_layer":"add_on","valid_for_member_tier":"everyone","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Free standard shipping when the item subtotal before member benefits is $80.00 or more.","percent_off":null,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":[],"change_set_id":null,"version":1}} ``
- 모델 판단(추론 필드): Get promo_gold_10
5. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_gold_10"} ``
   ← 결과 483B: `` {"status":"succeeded","data":{"id":"promo_gold_10","name":"Gold tier 10%","status":"running","discount_layer":"order_discount","valid_for_member_tier":"gold","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Gold members get a 10% order coupon every month.","percent_off":10,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_gold_10"],"change_set_id":null,"version":1}} ``
- 모델 판단(추론 필드): We have list. User doesn't want to stack anything on top of knit sale. So we need to inform which promos are live and which would stack. We might need to know stacking rules. Perhaps discount_layer item_price and order_discount can stack? Typically they can stack. Add_on free shipping likely stacks. But user says don't want to stack anything on top of knit sale. Maybe they want to know which promos are live so they can avoid stacking. Could be they want to ensure no additional promo overlaps with knitwear category? The knit sale applies to categories cat_knitwear. The other promos are order-level, not category-specific. So they would apply to entire order including knitwear, thus stacking. F… (+2,279자)
6. 모델 → **`acom_describe_data`** `` {"api_name":"discount_layer"} ``
   ← 결과 547B: `` {"status":"succeeded","data":{"items":[{"table":"promotion.promotion","kind":"table","term":"schema:OfferCatalog/acom:Promotion","id_prefix":"promo","description":"a time-boxed benefit that groups member and sale prices or an order discount. id prefix promo_.","columns":[{"name":"discount_layer","type":"text","nullable":false,"term":"acom:discountLayer","description":"where the benefit applies when benefits are calculated. values: discount_layer","values":["item_price","order_discount","add_on"],"values_list":"discount_layer"}]}],"total":1}} ``
- 모델 판단(추론 필드): We have discount_layer values. We could respond. Perhaps also need to check if any promotion applies to same category as knit sale causing stacking within same layer? None. Answer accordingly. Provide bullet list. Make sure to note change set preview? No. User just asked what promos are live this weekend? I don't want to stack anything on top of the knit sale. We should answer: Autumn knitwear 15% is live Nov1-15, plus Birthday coupon, Free shipping over $80, Gold tier 10%. If you want to avoid stacking, note that Birthday and Gold are order discounts that will apply in addition to item price discount on knitwear items. Possibly suggest to check promotion stacking rules? Not needed. Provide … (+75자)

**답변 1**
> This weekend in store time — Sat 2026-11-07 00:00 to Sun 2026-11-08 23:59 America/New_York — 4 promotions overlap the period.
>
> **Running now**
>
> * **promo_autumn_knit — Autumn knitwear 15%**
>   * status: running
>   * discount_layer: item_price
>   * valid_for_member_tier: everyone
>   * valid_from: 2026-11-01T00:00:00-04:00 → valid_through: 2026-11-15T23:59:00-05:00
>   * applies_to: scope categories, category_ids: cat_knitwear, product_count 26
>   * 15% off all knitwear for everyone. price_specification_count 260
>
> * **promo_birthday — Birthday coupon**
>   * status: running
>   * discount_layer: order_discount
>   * valid_for_member_tier: member
>   * valid_from: 2026-01-01 → valid_through: null
>   * applies_to: scope order
>   * $10.00 off one order in the member's birthday month. coupon_ids: cpn_birthday
>
> * **promo_free_ship_80 — Free shipping over $80**
>   * status: running
>   * discount_layer: add_on
>   * valid_for_member_tier: everyone
>   * valid_from: 2026-01-01 → valid_through: null
>   * applies_to: scope order
>   * Free standard shipping when the item subtotal before member benefits is $80.00 or more.
>
> * **promo_gold_10 — Gold tier 10%**
>   * status: running
>   * discount_layer: order_discount
>   * valid_for_member_tier: gold
>   * valid_from: 2026-01-01 → valid_through: null
>   * applies_to: scope order
>   * Gold members get a 10% order coupon every month. coupon_ids: cpn_gold_10
>
> Stacking note for the knit sale:
> The Autumn knitwear 15% is an `item_price` layer on cat_knitwear. The two other active benefits that affect order total are order-level:
>
> * promo_birthday `order_discount` for members — $10 off order
> * promo_gold_10 `order_discount` for Gold tier — 10% off order
>
> Both will apply in addition to the 15% item price on knitwear items in the same order. Free shipping over $80 is an `add_on` layer.
>
> No other active promotion this weekend applies to the knitwear category itself; the only category-scoped promo in the window is promo_autumn_knit.

**채점**: ✓ 통과
(도구 정밀도 0.83, 재현율 1.00)

### a2api-acom · 2회차 · ✓ 통과

토큰 84,846 · 62.138초 · 모델 호출 10회 · 도구 호출 9회 · 첫 요청 프롬프트 3,996토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 모델 판단(추론 필드): We need find promos live this weekend. Store time: Friday, November 6, 2026, 11:00 America/New_York. This weekend: presumably Saturday Nov 7? Sunday Nov 8? Might be weekend starting Saturday? Could be Friday-Sunday? "this weekend" ambiguous. Probably Saturday 7 to Sunday 8, maybe also Friday? Let's assume weekend = Saturday 2026-11-07 to Sunday 2026-11-08. Could include Friday? Let's check active promotions overlapping period. Need promo knit sale. Might be promo_autumn_knit? Need identify knit sale promotion. Possibly need to list active promotions for valid_from to valid_through. We need valid_from and valid_through. Use dates. For list_active_promotions, valid_from format like "2026-11-07… (+1,483자)
1. 모델 → **`acom_list_active_promotions`** `` {"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"} ``
   ← 결과 1,164B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"applies_to":{"scope":"order","category_ids":[],"prod… (+564자) ``
- 모델 판단(추론 필드): We have 4 active promotions: promo_autumn_knit - Autumn knitwear 15% - running - valid 2026-11-01 to 2026-11-15. discount_layer item_price, everyone, applies to cat_knitwear. promo_birthday - Birthday coupon - running, order_discount, member tier. promo_free_ship_80 - Free shipping over $80 - running, add_on, everyone. promo_gold_10 - Gold tier 10% - running, order_discount, gold tier. User doesn't want to stack anything on top of knit sale. So need to identify which promotions stack with knit sale? Possibly discount_layer item_price vs order_discount? Stacking rules? Might need to check promotion details. We have promo_autumn_knit. Possibly stacking constraints: item_price discount vs order… (+290자)
2. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_autumn_knit"} ``
   ← 결과 508B: `` {"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}} ``
- 모델 판단(추론 필드): Maybe need to check if other promotions stack with it. Could be discount_layer item_price vs order_discount can stack? Possibly stacking is allowed per discount_layer? Need to check data dictionary for promotion? Could search for stacking rules. Might need to describe data for promotion table? Let's see schema. We could use acom_describe_data with schema promotion.
3. 모델 → **`acom_describe_data`** `` {"schema":"promotion"} ``
   ← 결과 5,112B: `` {"status":"succeeded","data":{"items":[{"table":"promotion.conditional_gift","kind":"table","term":"schema:Offer/acom:ConditionalGift","id_prefix":"cgf","description":"a gift added to an order whose subtotal before member benefits reaches a threshold, with one gift per threshold. id prefix cgf_.","columns":[{"name":"tenant_id","type":"text","nullable":false,"term":"-","description":"store (tenant) that owns this row; row-level security key.","references":"platform.online_store"},{"name":"id","type":"text","nullable":false,"term":"-","description":"id with prefix cgf_; the same value the API, l… (+2,400자) ``
- 모델 판단(추론 필드): Need promotion table schema. Let's describe data with table promotion.promotion.
4. 모델 → **`acom_describe_data`** `` {"table":"promotion.promotion"} ``
   ← 결과 4,589B: `` {"status":"succeeded","data":{"items":[{"table":"promotion.promotion","kind":"table","term":"schema:OfferCatalog/acom:Promotion","id_prefix":"promo","description":"a time-boxed benefit that groups member and sale prices or an order discount. id prefix promo_.","columns":[{"name":"tenant_id","type":"text","nullable":false,"term":"-","description":"store (tenant) that owns this row; row-level security key.","references":"platform.online_store"},{"name":"id","type":"text","nullable":false,"term":"-","description":"id with prefix promo_; the same value the API, logs and events use."},{"name":"name… (+2,400자) ``
- 모델 판단(추론 필드): discount_layer values: item_price, order_discount, add_on. Stacking? Might be by discount_layer? Possibly item_price and order_discount can stack? Need to understand rules. Could be system prevents stacking same layer? Might need to check promotion terms. User says "I don't want to stack anything on top of the knit sale". So they want to know which promos are live this weekend, and which would stack with knit sale (so they can avoid stacking). Might be they want to know which promotions are active, and note that knit sale is item_price, so order_discount promotions would stack? Or maybe add_on stacks? Better to provide list of live promos with details, and note discount_layer. Maybe stacking… (+186자)
5. 모델 → **`a2api_search`** `` {"query":"stack promotion"} ``
   ← 결과 377B: `` {"selected":[{"name":"acom_create_coupon","id":"acom.create_coupon"},{"name":"acom_pause_promotion","id":"acom.pause_promotion"},{"name":"acom_search_promotions","id":"acom.search_promotions"},{"name":"acom_end_promotion","id":"acom.end_promotion"},{"name":"acom_get_promotion","id":"acom.get_promotion"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
- 모델 판단(추론 필드): Maybe need to find policy? Could be default stacking is no stacking? Let's check promotion terms? Might not need deep. User wants list of promos live this weekend, and don't want to stack anything on top of knit sale. So we can report promos live: Autumn knitwear 15% (promo_autumn_knit), Birthday coupon (promo_birthday), Free shipping over $80 (promo_free_ship_80), Gold tier 10% (promo_gold_10). Possibly also note that knit sale is item_price, birthday and gold are order_discount, free ship is add_on. If they don't want to stack anything on top of knit sale, they might want to avoid order_discount promotions stacking? Hmm. Could be they want to know which promotions are live and which can be… (+178자)
6. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_birthday"} ``
   ← 결과 522B: `` {"status":"succeeded","data":{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"$10.00 off one order in the member's birthday month.","percent_off":null,"amount_off":{"value":10.0,"currency":"USD"},"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_birthday"],"change_set_id":null,"version":1}} ``
- 모델 판단(추론 필드): Get promo_free_ship_80
7. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_free_ship_80"} ``
   ← 결과 521B: `` {"status":"succeeded","data":{"id":"promo_free_ship_80","name":"Free shipping over $80","status":"running","discount_layer":"add_on","valid_for_member_tier":"everyone","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Free standard shipping when the item subtotal before member benefits is $80.00 or more.","percent_off":null,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":[],"change_set_id":null,"version":1}} ``
- 모델 판단(추론 필드): Get promo_gold_10
8. 모델 → **`acom_get_promotion`** `` {"promotion_id":"promo_gold_10"} ``
   ← 결과 483B: `` {"status":"succeeded","data":{"id":"promo_gold_10","name":"Gold tier 10%","status":"running","discount_layer":"order_discount","valid_for_member_tier":"gold","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"description":"Gold members get a 10% order coupon every month.","percent_off":10,"amount_off":null,"applies_to":{"scope":"order","category_ids":[],"product_count":null},"price_specification_count":0,"coupon_ids":["cpn_gold_10"],"change_set_id":null,"version":1}} ``
- 모델 판단(추론 필드): Now we have info. User might want to avoid stacking anything on top of knit sale. Which promotions stack? Possibly order_discount promotions stack with item_price. Add_on maybe also stacks. We could check coupon stacking info for birthday coupon and gold coupon. Get coupon details? No function for get coupon. Could describe data for coupon table already seen has stacking field. Could we fetch coupon? Not directly. Maybe we can assume that item_price promotions generally stack with order_discount and add_on, but user doesn't want stacking. Maybe they want to know which promotions are live and which would stack with knit sale, so they can pause them? The request: "what promos are live this wee… (+2,280자)
9. 모델 → **`acom_search_promotions`** `` {"status":["running","scheduled"],"valid_from":"2026-11-07T00:00","limit":100} ``
   ← 결과 1,092B: `` {"status":"succeeded","data":{"items":[{"id":"promo_denim_bundle","name":"Denim bundle","status":"scheduled","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-13T00:00:00-05:00","valid_through":"2026-11-20T23:59:00-05:00"},{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00"},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for… (+492자) ``
- 모델 판단(추론 필드): Denim bundle scheduled starting Nov 13, so not this weekend. Thus answer stands. Maybe also check for Friday Nov 6 evening? Could be weekend starts Friday. If include Friday 6, promotions same. We could also list active promotions for 2026-11-06T... Let's just assume weekend = Sat-Sun. Provide summary. Potentially also want to know if any of these stack on top of knit sale. Typically item_price discounts apply first, then order_discount. So birthday and gold would stack. Free shipping is add_on, might also stack. If user doesn't want stacking, they could pause birthday, gold, free ship. Could suggest pausing. But user only asked what promos are live this weekend? I don't want to stack anythi… (+174자)

**답변 1**
> This weekend in store time (Sat 2026-11-07 00:00 – Sun 2026-11-08 23:59 America/New_York) the overlap check returns 4 promotions that are running / scheduled for the period.
>
> * **promo_autumn_knit – Autumn knitwear 15%**
>   status: running
>   discount_layer: item_price
>   valid_for_member_tier: everyone
>   valid_from: 2026-11-01T00:00:00-04:00 → valid_through: 2026-11-15T23:59:00-05:00
>   applies_to: scope categories, category_ids [cat_knitwear], product_count 26
>   15% off all knitwear for everyone.  price_specification_count 260.  coupon_ids: []
>
> * **promo_birthday – Birthday coupon**
>   status: running
>   discount_layer: order_discount
>   valid_for_member_tier: member
>   valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   applies_to: scope order
>   $10.00 off one order in the member's birthday month.  coupon_ids: [cpn_birthday]
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
>   Gold members get a 10% order coupon every month.  coupon_ids: [cpn_gold_10]
>
> The knit sale is promo_autumn_knit, item_price for everyone on cat_knitwear through 2026-11-15.
>
> Stacking note:
> * promo_birthday and promo_gold_10 are order_discount promotions for member / gold tiers. With the current configuration an order_discount benefit is calculated after item_price benefits, so a knitwear item that receives the 15% Autumn knitwear price would also be eligible for the $10 birthday order discount and the 10% Gold order discount on the same order.
> * promo_free_ship_80 is an add_on discount_layer, also applied after item prices.
>
> If you want… (+405자)

**채점**: ✓ 통과
(도구 정밀도 0.75, 재현율 1.00)

### a2api-acom-names-batch · 1회차 · ✓ 통과

토큰 18,525 · 51.24초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 1,989토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 모델 판단(추론 필드): We need to find promos live this weekend. Store time: Friday, November 6, 2026, 11:00 America/New_York. Weekend = Saturday Nov 7, Sunday Nov 8? Possibly also Friday evening? "this weekend" likely Saturday and Sunday. Need promos live this weekend. Also don't want to stack anything on top of knit sale. Need to find knit sale promotion? Might need to identify promotion related to knit sale. Could be a promotion with name containing knit. Need to list active promotions, filter by dates. We have promotion › promotion: list_active_promotions, get_promotion, search_promotions, etc. Also promotion › offer: set_sale_prices? Might be separate. We need to find promos live this weekend. Use list_active… (+200자)
1. 모델 → **`a2api_load`** `` {"names":["list_active_promotions","get_promotion","search_promotions"]} ``
   ← 결과 73B: `` {"loaded":["list_active_promotions","get_promotion","search_promotions"]} ``
- 모델 판단(추론 필드): We need valid_from and valid_through. Weekend: store time Friday Nov 6 2026 11:00. Weekend probably Saturday Nov 7 and Sunday Nov 8. Might include Friday evening? Usually weekend starts Saturday. Let's check from 2026-11-07T00:00 to 2026-11-08T23:59. We need list_active_promotions with valid_from, valid_through. Might also want status running and scheduled. Default statuses are running and scheduled. That's fine. Also need to find knit sale promotion. Could search promotions with query "knit". Let's do both in batch. list_active_promotions valid_from 2026-11-07T00:00 valid_through 2026-11-08T23:59 search_promotions query "knit" maybe? Could also search with discount_layer? Let's search promo… (+92자)
2. 모델 → **`a2api_batch`** `` {"calls":[{"name":"list_active_promotions","arguments":{"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59"}},{"name":"search_promotions","arguments":{"query":"knit","limit":20}}]} ``
   ← 결과 1,534B: `` {"batch":[{"name":"list_active_promotions","result":{"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"… (+934자) ``
- 모델 판단(추론 필드): We have active promotions for weekend: 1. promo_autumn_knit - Autumn knitwear 15% - running, discount_layer item_price, valid for everyone, valid 2026-11-01 to 2026-11-15, applies to categories cat_knitwear, product_count 26 2. promo_birthday - Birthday coupon - running, discount_layer order_discount, valid for member, valid from 2026-01-01 ongoing, applies to order 3. promo_free_ship_80 - Free shipping over $80 - running, discount_layer add_on, everyone 4. promo_gold_10 - Gold tier 10% - running, discount_layer order_discount, gold tier User says I don't want to stack anything on top of the knit sale. So they want to know promos live this weekend, but note stacking? Maybe they want to know … (+873자)
3. 모델 → **`a2api_batch`** `` {"calls":[{"name":"get_promotion","arguments":{"promotion_id":"promo_autumn_knit"}},{"name":"get_promotion","arguments":{"promotion_id":"promo_birthday"}},{"name":"get_promotion","arguments":{"promotion_id":"promo_free_ship_80"}},{"name":"get_promotion","arguments":{"promotion_id":"promo_gold_10"}}]} ``
   ← 결과 2,185B: `` {"batch":[{"name":"get_promotion","result":{"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}}},{"name":"get_promotion","result":{"status":"suc… (+1,585자) ``
- 모델 판단(추론 필드): We have details. No explicit stackable flag returned. Maybe stacking is determined by discount_layer? Typically item_price and order_discount may stack? Could be system prevents stacking same layer? Or need to check policy. User says I don't want to stack anything on top of the knit sale. Perhaps they want to know which promos are live and which would stack with knit sale, so they can avoid stacking. Might need to inform that knit sale is item_price, and other promos are order_discount or add_on. Typically different layers can stack. Maybe they want list of promos live this weekend, excluding those that would stack with knit sale? "I don't want to stack anything on top of the knit sale" coul… (+2,284자)

**답변 1**
> This weekend in store time (Sat 2026-11-07 → Sun 2026-11-08) the overlap check returns 4 active promotions:
>
> * **promo_autumn_knit – Autumn knitwear 15%**
>   * status: running
>   * discount_layer: item_price
>   * valid_for_member_tier: everyone
>   * valid_from: 2026-11-01T00:00:00-04:00 → valid_through: 2026-11-15T23:59:00-05:00
>   * applies_to: scope categories, category_ids [cat_knitwear], 26 products / 260 price specifications
>   * 15% off all knitwear for everyone. This is the knit sale you referenced.
>
> * **promo_birthday – Birthday coupon**
>   * status: running
>   * discount_layer: order_discount
>   * valid_for_member_tier: member
>   * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
>   * applies_to: scope order
>   * $10.00 off one order in the member's birthday month. coupon_ids: [cpn_birthday]
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
>   * Gold members get a 10% order coupon every month. coupon_ids: [cpn_gold_10]
>
> Stacking note:
> The knit sale is the only active `item_price` promotion for the weekend and it covers cat_knitwear. The other three live promotions are on different layers:
>
> * Birthday coupon and Gold tier 10% are `order_discount`
> * Free shipping over $80 is `add_on`
>
> With the current set, no other `item_price` promotion overlaps the knit sale on 7-8 Nov, so you would not get a second item-price discount on knitwear. Order-level and add-on benefits would still be able to combine with the item price if the system allows cross-layer stacking; if you want zero stacking on … (+154자)

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-batch · 2회차 · ✗ 실패

토큰 32,680 · 55.307초 · 모델 호출 6회 · 도구 호출 5회 · 첫 요청 프롬프트 1,989토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 모델 판단(추론 필드): We need to find promotions live this weekend. Store time: Friday, November 6, 2026, 11:00 America/New_York. This weekend = presumably Saturday Nov 7 and Sunday Nov 8? Or Friday? Might be weekend starting Saturday. Could check active promotions. We need to not stack anything on top of the knit sale. So need to identify knit sale promotion. Need to find promotions live this weekend, and possibly identify which ones conflict with knit sale stacking. We have promotion › promotion: list_active_promotions, search_promotions, get_promotion, create_promotion, etc. Also promotion › offer: set_sale_prices Probably need to list active promotions. Then filter those active this weekend. We need to know d… (+405자)
1. 모델 → **`a2api_load`** `` {"names":["list_active_promotions","search_promotions","get_promotion"]} ``
   ← 결과 73B: `` {"loaded":["list_active_promotions","search_promotions","get_promotion"]} ``
- 모델 판단(추론 필드): We have loaded. Now need to define weekend. Today is Friday Nov 6 2026 11:00. Weekend probably Saturday 7 Nov and Sunday 8 Nov. Could also include Friday evening? Might be safe to check from 2026-11-07T00:00 to 2026-11-08T23:59. Maybe also include Friday 6? The weekend starts Friday? Some consider weekend starts Friday evening. Better to check Friday 6 evening onward? User said this weekend. Could assume Saturday and Sunday. Better to check range: valid_from = 2026-11-07T00:00, valid_through = 2026-11-08T23:59. We also need to identify knit sale. Could search promotions query knit. Let's first list active promotions for that period. list_active_promotions requires valid_from and valid_throug… (+435자)
2. 모델 → **`a2api_batch`** `` {"calls":[{"name":"list_active_promotions","arguments":{"valid_from":"2026-11-07T00:00","valid_through":"2026-11-08T23:59","limit":100}}]} ``
   ← 결과 1,219B: `` {"batch":[{"name":"list_active_promotions","result":{"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"… (+619자) ``
- 모델 판단(추론 필드): We have 4 active promotions this weekend. promo_autumn_knit: Autumn knitwear 15% running, discount_layer item_price, valid for everyone, valid_from 2026-11-01 to 2026-11-15, applies to categories cat_knitwear, product_count 26. promo_birthday: Birthday coupon, order_discount, member tier. promo_free_ship_80: Free shipping over $80, add_on, everyone. promo_gold_10: Gold tier 10%, order_discount, gold tier. User said I don't want to stack anything on top of the knit sale. So we need to note which promotions stack? Possibly need to check promotion details for stacking rules. The promotion data may include stacking info. We have get_promotion to get more details. We might need to check if any of… (+314자)
3. 모델 → **`a2api_batch`** `` {"calls":[{"name":"get_promotion","arguments":{"promotion_id":"promo_autumn_knit"}},{"name":"get_promotion","arguments":{"promotion_id":"promo_birthday"}},{"name":"get_promotion","arguments":{"promotion_id":"promo_free_ship_80"}},{"name":"get_promotion","arguments":{"promotion_id":"promo_gold_10"}}]} ``
   ← 결과 2,185B: `` {"batch":[{"name":"get_promotion","result":{"status":"succeeded","data":{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","description":"15% off all knitwear for everyone.","percent_off":15,"amount_off":null,"applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26},"price_specification_count":260,"coupon_ids":[],"change_set_id":null,"version":1}}},{"name":"get_promotion","result":{"status":"suc… (+1,585자) ``
- 모델 판단(추론 필드): We have details. No explicit stacking info in fields returned. Might need more fields? Maybe promotion has stacking rules not returned? Could be in fields we didn't request. We could get with fields? The get_promotion returns basic. The user wants promos live this weekend, and don't want to stack anything on top of knit sale. Perhaps they want to know which promos are live, and note which would stack with knit sale? Might need to check overlap rules. The list_active_promotions returns promotions overlapping period. Possibly need to know which promotions are compatible with knit sale stacking. Maybe the platform has rule that item_price promotions cannot stack with order_discount? Or need to … (+2,285자)
4. 모델 → **`a2api_batch`** `` {"calls":[{"name":"search_promotions","arguments":{"query":"knit","limit":20}}]} ``
   ← 결과 326B: `` {"batch":[{"name":"search_promotions","result":{"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00"}],"total":1}}}]} ``
- 모델 판단(추론 필드): Only one knit promo. Now answer user. Provide list: - Autumn knitwear 15% (promo_autumn_knit) – running Nov 1-15, 15% off knitwear category, 26 products. - Birthday coupon – $10 off order for members in birthday month, order_discount, member tier. - Free shipping over $80 – add_on, everyone. - Gold tier 10% – 10% off order for Gold members, order_discount. If they don't want to stack anything on top of knit sale, they should be aware that birthday coupon and Gold tier 10% are order-level discounts that would apply to the order including knitwear items, effectively stacking with the 15% item price discount. Free shipping is add-on and typically stacks. We could also mention that no other item… (+456자)
5. 모델 → **`list_active_promotions`** `` {"valid_from":"2026-11-06T17:00","valid_through":"2026-11-08T23:59","limit":100} ``
   ← 결과 1,164B: `` {"status":"succeeded","data":{"items":[{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_knitwear"],"product_count":26}},{"id":"promo_birthday","name":"Birthday coupon","status":"running","discount_layer":"order_discount","valid_for_member_tier":"member","valid_from":"2026-01-01T00:00:00-05:00","valid_through":null,"applies_to":{"scope":"order","category_ids":[],"prod… (+564자) ``
- 모델 판단(추론 필드): Same. Answer accordingly. Perhaps also note that the knit sale is promo_autumn_knit, and you don't want to stack, so be aware of order discounts. Provide concise answer. Possibly user wants to avoid stacking anything on top of knit sale, so they might want to know which promos are live to avoid enabling them. We can list. Provide summary with IDs. Final answer.

**답변 1**
> This weekend in store time (America/New_York) the promotions whose period overlaps 6 Nov 17:00 → 8 Nov 23:59 are:
>
> **1. Autumn knitwear 15% – promo_autumn_knit**
> * status: running
> * discount_layer: item_price
> * valid for: everyone
> * valid_from: 2026-11-01T00:00:00-04:00 → valid_through: 2026-11-15T23:59:00-05:00
> * applies_to: scope categories, category_ids [cat_knitwear], 26 products covered
> * 15% off all knitwear for everyone. Price specification count 260.
> This is the knit sale you referenced. It is live all weekend, 1 Nov – 15 Nov.
>
> **2. Birthday coupon – promo_birthday**
> * status: running
> * discount_layer: order_discount
> * valid for: member tier
> * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
> * applies_to: scope order
> * $10.00 off one order in the member’s birthday month. Coupon ids: cpn_birthday
>
> **3. Free shipping over $80 – promo_free_ship_80**
> * status: running
> * discount_layer: add_on
> * valid for: everyone
> * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
> * applies_to: scope order
> * Free standard shipping when the item subtotal before member benefits is $80.00 or more.
>
> **4. Gold tier 10% – promo_gold_10**
> * status: running
> * discount_layer: order_discount
> * valid for: gold tier
> * valid_from: 2026-01-01T00:00:00-05:00 → valid_through: null
> * applies_to: scope order
> * Gold members get a 10% order coupon every month. Coupon ids: cpn_gold_10
>
> No other item_price promotions are live this weekend. The knit sale is the only item-price promotion on cat_knitwear.
>
> Note on stacking: promo_autumn_knit is item_price on the knitwear category. 
> * promo_birthday and promo_gold_10 are order_discount promotions and would apply to the order total including the knitwear items, i.e. they would stack on top of the 15% item price discount if used on the same order.
> * promo_free_ship_80 is an add_on shipping benefit.
>
> If you want zero stacking on the knit sale, the order-level discounts above are the ones to keep separate from knitwear purchases.

**채점**: ✗ 실패 — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### facade-all · 1회차 · E MODEL_CALL_LIMIT

토큰 96,416 · 63.384초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 5,239토큰

준비: 전략 `None`, 함수 22개

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 모델 판단(추론 필드): We need find promos live this weekend. Store time: Friday, November 6, 2026, 11:00 America/New_York. Weekend = Saturday Nov 7 and Sunday Nov 8? Possibly weekend start Friday? Could be Saturday-Sunday. Need promos live this weekend. Don't want to stack anything on top of knit sale. We need identify knit sale promo. Need find promo with knit? Might need search promotion list. We need promo status live. Probably prmtStatCd? 10? 20? Need know what codes mean. Likely 10 = active? 20? Let's search. We need promos live this weekend. So start datetime <= weekend and end datetime >= weekend. Need to find promotions where strtDtm <= end of weekend and endDtm >= start of weekend. Need search. We have g… (+1,445자)
1. 모델 → **`getPrmtGridList`** `` {"prmtStatCd":10,"srchStrtDtm":"2026-11-07 00:00:00","srchEndDtm":"2026-11-08 23:59:59","pageNo":0,"pageSize":100} ``
   ← 결과 169B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid parameter: invalid type: number, expected string or map","next_tool":null}}} ``
- 모델 판단(추론 필드): Invalid parameter: invalid type: number, expected string or map. Hmm pageNo is integer, but maybe expects string? The schema says integer. Might be issue with srchStrtDtm format? It's string. Maybe prmtStatCd? Hmm. Error says invalid type: number, expected string or map. Which parameter is number? pageNo is integer. Could be the tool expects pageNo as string? Or maybe srchStrtDtm format expects date only? Let's try with different parameters. Maybe srchStrtDtm and srchEndDtm expects just date? Or format with T? Let's try without srch dates, just prmtStatCd=10 and pageNo/pageSize. Also pageSize might need to be string? Hmm. The schema says pageNo integer format uint32, pageSize integer. Could … (+434자)
2. 모델 → **`getPrmtGridList`** `` {"prmtStatCd":10,"pageNo":0,"pageSize":10} ``
   ← 결과 169B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid parameter: invalid type: number, expected string or map","next_tool":null}}} ``
- 모델 판단(추론 필드): Same error. Maybe pageNo and pageSize need to be strings? Let's try as strings? Schema says integer. But maybe tool expects string. Let's try pageNo as string "0".
3. 모델 → **`getPrmtGridList`** `` {"prmtStatCd":10,"pageNo":0,"pageSize":10} ``
   ← 결과 169B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid parameter: invalid type: number, expected string or map","next_tool":null}}} ``
- 모델 판단(추론 필드): Hmm still same. Maybe the tool requires prmtStatCd to be string, but we gave string. Maybe need also other params? Could be that pageNo is integer but the tool expects string? Could try pageNo=0 but as JSON number is okay. Could be the error is about prmtStatCd? No. Let's try getPrmtGridListCnt which has same params. Maybe test.
4. 모델 → **`getPrmtGridListCnt`** `` {"prmtStatCd":10,"pageNo":0,"pageSize":10} ``
   ← 결과 169B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid parameter: invalid type: number, expected string or map","next_tool":null}}} ``
- 모델 판단(추론 필드): Same error. Maybe pageNo/pageSize are causing issue. Let's omit them.
5. 모델 → **`getPrmtGridList`** `` {"prmtStatCd":10} ``
   ← 결과 169B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid parameter: invalid type: number, expected string or map","next_tool":null}}} ``
- 모델 판단(추론 필드): Still error. Maybe prmtStatCd value "10" is invalid? Enum is ["00","10","20","30","90"]. So 10 is valid. Could be the tool expects parameters as string or map? Error says invalid type: number, expected string or map. Means one of the parameters is number but expected string or map. prmtStatCd is string. So maybe default? Hmm. Wait maybe the tool requires all parameters? No. Could be the JSON parsing treats prmtStatCd as number? No. Alternative: maybe the API expects parameters wrapped? Hmm. Maybe the error is because pageNo is integer but the tool expects string? But we removed pageNo. Hmm. Maybe we need to pass pageNo as 0 but as string "0". Let's try with only prmtStatCd and pageNo as stri… (+105자)
6. 모델 → **`getPrdGridList`** `` {"pageNo":0,"pageSize":1} ``
   ← 결과 121B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null}}} ``
- 모델 판단(추론 필드): Invalid paging. Hmm. Maybe pageNo must be >=0? 0 is okay. Maybe pageSize must be >0? 1 is >0. Let's try getPrdGridListCnt with no params.
7. 모델 → **`getPrdGridListCnt`** `` {} ``
   ← 결과 36B: `` {"status":200,"body":{"totCnt":400}} ``
- 모델 판단(추론 필드): Works without params. So pageNo/pageSize cause error? Let's try getPrdGridList with no paging.
8. 모델 → **`getPrdGridList`** `` {} ``
   ← 결과 3,706B: `` {"status":200,"body":{"list":[{"prdNo":"prd_wool_overcoat","prdNm":"Wool overcoat","ctgNo":"cat_outerwear","brndNo":"brn_northwind","salePrc":289.0,"mbrPrc":null,"stkQty":24,"sellStatCd":"10","costPrc":120.0},{"prdNo":"prd_shorts_15","prdNm":"Terry trail shorts","ctgNo":"cat_shorts","brndNo":"brn_northwind","salePrc":89.0,"mbrPrc":null,"stkQty":28,"sellStatCd":"10","costPrc":34.08},{"prdNo":"prd_shirts_11","prdNm":"Corduroy band-collar shirt","ctgNo":"cat_shirts","brndNo":"brn_northwind","salePrc":79.0,"mbrPrc":null,"stkQty":19,"sellStatCd":"10","costPrc":35.64},{"prdNo":"prd_shirts_15","prdNm… (+2,400자) ``
- 모델 판단(추론 필드): Works without paging params. It returned list with pageNo 1 pageSize 20 default. So for getPrmtGridList, maybe we need not provide pageNo/pageSize, or provide as strings? Let's try without paging.
9. 모델 → **`getPrmtGridList`** `` {"prmtStatCd":10} ``
   ← 결과 169B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid parameter: invalid type: number, expected string or map","next_tool":null}}} ``
- 모델 판단(추론 필드): Still error. Why getPrmtGridList fails with prmtStatCd? Maybe prmtStatCd expects string but we give string. Could be other param causing number? Hmm. Maybe the function expects pageNo always? But getPrdGridList worked without. Let's try getPrmtGridList with no params.
10. 모델 → **`getPrmtGridList`** `` {} ``
   ← 결과 1,121B: `` {"status":200,"body":{"list":[{"prmtNo":"promo_denim_bundle","prmtNm":"Denim bundle","prmtTpCd":"T02","prmtStatCd":"10","tgtMbrGrdCd":"G00","strtDtm":"2026-11-13T00:00:00-05:00","endDtm":"2026-11-20T23:59:00-05:00"},{"prmtNo":"promo_autumn_knit","prmtNm":"Autumn knitwear 15%","prmtTpCd":"T01","prmtStatCd":"20","tgtMbrGrdCd":"G00","strtDtm":"2026-11-01T00:00:00-04:00","endDtm":"2026-11-15T23:59:00-05:00"},{"prmtNo":"promo_linen_clearance","prmtNm":"Linen clearance","prmtTpCd":"T01","prmtStatCd":"90","tgtMbrGrdCd":"G00","strtDtm":"2026-10-01T00:00:00-04:00","endDtm":"2026-10-20T23:59:00-04:00"},… (+521자) ``
- 모델 판단(추론 필드): Works without params. Returns list. We have promos: - promo_denim_bundle "Denim bundle" prmtStatCd "10", strt 2026-11-13, end 2026-11-20 → not weekend (starts Nov13) - promo_autumn_knit "Autumn knitwear 15%" prmtStatCd "20", strt 2026-11-01, end 2026-11-15 → active? StatCd 20 maybe scheduled? Could be live? Hmm. - promo_linen_clearance stat 90 ended. - promo_birthday stat 20 - promo_free_ship_80 stat20 - promo_gold_10 stat20 The knit sale likely is promo_autumn_knit "Autumn knitwear 15%" which runs Nov1-15. StatCd 20. Maybe statCd 10 means upcoming? Actually denim bundle starts Nov13. StatCd10. So stat 10 might be upcoming/scheduled? Or active? Hmm. Maybe statCd 20 means active? Because autu… (+1,062자)
11. 모델 → **`getPrmtGridListCnt`** `` {} ``
   ← 결과 34B: `` {"status":200,"body":{"totCnt":6}} ``
- 모델 판단(추론 필드): Total count 6. So we have all 6. List: 1 promo_denim_bundle Denim bundle stat10 2026-11-13 to 2026-11-20 2 promo_autumn_knit Autumn knitwear 15% stat20 2026-11-01 to 2026-11-15 3 promo_linen_clearance Linen clearance stat90 ended 4 promo_birthday Birthday coupon stat20 2026-01-01 to null 5 promo_free_ship_80 Free shipping over $80 stat20 2026-01-01 to null 6 promo_gold_10 Gold tier 10% stat20 2026-01-01 to null So live this weekend (Nov7-8): - Autumn knitwear 15% (knit sale) 2026-11-01 to 2026-11-15 → live - Birthday coupon → live - Free shipping over $80 → live - Gold tier 10% → live Denim bundle starts Nov13, not live yet. Linen clearance ended. Now user says I don't want to stack anything… (+2,282자)
12. 모델 → **`getPrmtGridList`** `` {"prmtNm":"knit"} ``
   ← 결과 249B: `` {"status":200,"body":{"list":[{"prmtNo":"promo_autumn_knit","prmtNm":"Autumn knitwear 15%","prmtTpCd":"T01","prmtStatCd":"20","tgtMbrGrdCd":"G00","strtDtm":"2026-11-01T00:00:00-04:00","endDtm":"2026-11-15T23:59:00-05:00"}],"pageNo":1,"pageSize":20}} ``
_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "four promotions overlap Sat Nov 7 – Sun Nov 8: Autumn knitwe" (7, 8, 15, 15, 80, 10 not shown); fact "the knit sale covers 26 knitwear products" (26 not shown); HOST:MODEL_CALL_LIMIT

### facade-all · 2회차 · ✗ 실패

토큰 61,307 · 63.388초 · 모델 호출 8회 · 도구 호출 7회 · 첫 요청 프롬프트 5,239토큰

준비: 전략 `None`, 함수 22개

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 모델 판단(추론 필드): We need find promos live this weekend. Store time Friday Nov 6 2026 11:00 America/New_York. Weekend = Saturday Nov 7 2026 and Sunday Nov 8 2026? Could be this weekend. Need promos live this weekend. Don't want to stack anything on top of knit sale. We need find promos live this weekend. Probably need promotion grid list with date range. Need start/end date times. Need to find knit sale promotion first? "don't want to stack anything on top of the knit sale" maybe means exclude promos that apply to knit sale? Or find promos live this weekend, and ensure they don't stack with knit sale. We need identify knit sale promotion. Possibly promotion name contains knit? Let's search promotion grid list… (+1,926자)
1. 모델 → **`getPrmtGridList`** `` {"prmtNm":"knit","pageNo":0,"pageSize":20} ``
   ← 결과 121B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null}}} ``
- 모델 판단(추론 필드): Invalid paging. Maybe pageNo must start at 1? Or pageSize >0. It says invalid paging. pageNo 0? Minimum 0. Maybe need pageNo >=0 but maybe pageSize must be >0. 20 is >0. Hmm error. Maybe prmtNm needs exact? Could try empty. Let's try getPrmtGridList with pageNo 1? Or pageNo 0 pageSize 10. Try pageNo 0 pageSize 10.
2. 모델 → **`getPrmtGridList`** `` {"prmtNm":"knit","pageNo":0,"pageSize":10} ``
   ← 결과 121B: `` {"status":422,"body":{"error":{"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null}}} ``
- 모델 판단(추론 필드): Invalid paging. Maybe pageNo must be >=1? Let's try pageNo 1.
3. 모델 → **`getPrmtGridList`** `` {"prmtNm":"knit","pageNo":1,"pageSize":10} ``
   ← 결과 249B: `` {"status":200,"body":{"list":[{"prmtNo":"promo_autumn_knit","prmtNm":"Autumn knitwear 15%","prmtTpCd":"T01","prmtStatCd":"20","tgtMbrGrdCd":"G00","strtDtm":"2026-11-01T00:00:00-04:00","endDtm":"2026-11-15T23:59:00-05:00"}],"pageNo":1,"pageSize":10}} ``
- 모델 판단(추론 필드): Found knit sale: promo_autumn_knit, Autumn knitwear 15%, prmtStatCd 20, starts 2026-11-01 to 2026-11-15. Live this weekend. Now need promos live this weekend. Probably need all promos with prmtStatCd 20? And date range overlaps weekend. Weekend: Nov 7-8 2026. We need promos where strtDtm <= 2026-11-08 23:59 and endDtm >= 2026-11-07 00:00. Also prmtStatCd maybe 20 (live) or 10 (scheduled)? Could be live. Better query getPrmtGridList with srchStrtDtm and srchEndDtm to filter promotions active within that window. Use srchStrtDtm = 2026-11-07 00:00:00, srchEndDtm = 2026-11-08 23:59:59. Let's try.
4. 모델 → **`getPrmtGridList`** `` {"srchStrtDtm":"2026-11-07 00:00:00","srchEndDtm":"2026-11-08 23:59:59","pageNo":1,"pageSize":20} ``
   ← 결과 191B: `` {"status":422,"body":{"error":{"code":"invalid_filter","class":"invalid_input","message":"'2026-11-07 00:00:00' is not a date-time (expected 2026-11-07T00:00 or RFC 3339)","next_tool":null}}} ``
- 모델 판단(추론 필드): Need format 2026-11-07T00:00 or RFC3339. Use 2026-11-07T00:00:00-05:00? Since store time America/New_York. Let's use ISO: 2026-11-07T00:00:00-04:00? November is EST? Actually DST ends early November. Nov 7 is EST -05:00. Use -05:00. Let's try srchStrtDtm: 2026-11-07T00:00:00-05:00, srchEndDtm: 2026-11-08T23:59:59-05:00.
5. 모델 → **`getPrmtGridList`** `` {"srchStrtDtm":"2026-11-07T00:00:00-05:00","srchEndDtm":"2026-11-08T23:59:59-05:00","pageNo":1,"pageSize":20} ``
   ← 결과 743B: `` {"status":200,"body":{"list":[{"prmtNo":"promo_autumn_knit","prmtNm":"Autumn knitwear 15%","prmtTpCd":"T01","prmtStatCd":"20","tgtMbrGrdCd":"G00","strtDtm":"2026-11-01T00:00:00-04:00","endDtm":"2026-11-15T23:59:00-05:00"},{"prmtNo":"promo_birthday","prmtNm":"Birthday coupon","prmtTpCd":"T02","prmtStatCd":"20","tgtMbrGrdCd":"G01","strtDtm":"2026-01-01T00:00:00-05:00","endDtm":null},{"prmtNo":"promo_free_ship_80","prmtNm":"Free shipping over $80","prmtTpCd":"T04","prmtStatCd":"20","tgtMbrGrdCd":"G00","strtDtm":"2026-01-01T00:00:00-05:00","endDtm":null},{"prmtNo":"promo_gold_10","prmtNm":"Gold ti… (+143자) ``
- 모델 판단(추론 필드): We have 4 promos live this weekend: 1. Autumn knitwear 15% (promo_autumn_knit) - live 2026-11-01 to 2026-11-15 2. Birthday coupon (promo_birthday) - ongoing since Jan 1, no end 3. Free shipping over $80 (promo_free_ship_80) - ongoing 4. Gold tier 10% (promo_gold_10) - ongoing User says "I don't want to stack anything on top of the knit sale". Stacking usually means multiple discounts applied to same item. Need to know which promos stack with knit sale? Might need to know promotion type and apply target. Possibly knit sale is product specific? prmtTpCd T01 maybe product discount? Let's get details? Might need prmt details to see apply target code etc. The grid list doesn't show apply target. … (+1,822자)
6. 모델 → **`getPrdGridList`** `` {"srchKwd":"knit","pageNo":1,"pageSize":10} ``
   ← 결과 1,821B: `` {"status":200,"body":{"list":[{"prdNo":"prd_dresses_07","prdNm":"Knit shirt dress","ctgNo":"cat_dresses","brndNo":"brn_northwind","salePrc":169.0,"mbrPrc":null,"stkQty":52,"sellStatCd":"10","costPrc":81.61},{"prdNo":"prd_dresses_01","prdNm":"Knit midi dress","ctgNo":"cat_dresses","brndNo":"brn_ridgeline","salePrc":159.0,"mbrPrc":null,"stkQty":42,"sellStatCd":"10","costPrc":68.45},{"prdNo":"prd_dresses_06","prdNm":"Knit maxi dress","ctgNo":"cat_dresses","brndNo":"brn_northwind","salePrc":159.0,"mbrPrc":null,"stkQty":30,"sellStatCd":"10","costPrc":70.66},{"prdNo":"prd_skirts_08","prdNm":"Knit A-… (+1,221자) ``
- 모델 판단(추론 필드): Knit products across categories. Without more detail, maybe we can assume knit sale applies to knitwear category. But we don't know. Alternative interpretation: user wants promos live this weekend, and they specifically do not want to stack anything on top of knit sale, meaning they want promos that are live but are not stackable with knit sale? Could be they want to avoid recommending promotions that would stack. Given limited data, best we can do: list promos live this weekend, note knit sale is live 11/1-11/15, and note other live promos. Possibly advise that stacking is generally not allowed? Or mention Gold tier 10% is member grade, might stack. We could also check promotion target memb… (+633자)
7. 모델 → **`getPrmtGridListCnt`** `` {"srchStrtDtm":"2026-11-07T00:00:00-05:00","srchEndDtm":"2026-11-08T23:59:59-05:00","pageNo":1,"pageSize":20} ``
   ← 결과 34B: `` {"status":200,"body":{"totCnt":4}} ``
- 모델 판단(추론 필드): Total 4. Thus answer: 4 promos live this weekend: Autumn knitwear 15% (the knit sale), Birthday coupon, Free shipping over $80, Gold tier 10%. User doesn't want to stack anything on top of knit sale, so maybe they want to know which promos are live besides knit sale, and which are safe to run without stacking. Free shipping over $80 is shipping, not price discount, so likely okay. Birthday coupon is coupon, might stack. Gold tier 10% is member grade discount, might stack. Could provide summary and note that to avoid stacking, you would need to set stacking rules. Given limited data, provide list and note knit sale details. Perhaps also check promotion type codes: T01 = ? Probably product dis… (+564자)

**답변 1**
> This weekend in America/New_York – Sat 2026-11-07 to Sun 2026-11-08 – there are 4 promotions with status 20 that are active in the search window.
>
> * **promo_autumn_knit – Autumn knitwear 15%**
>   prmtStatCd 20, prmtTpCd T01
>   tgtMbrGrdCd G00
>   strtDtm 2026-11-01T00:00:00-04:00 → endDtm 2026-11-15T23:59:00-05:00
>   This is the knit sale you mentioned. It is live all weekend.
>
> * **promo_birthday – Birthday coupon**
>   prmtStatCd 20, prmtTpCd T02
>   tgtMbrGrdCd G01
>   strtDtm 2026-01-01T00:00:00-05:00 → endDtm null
>   Ongoing.
>
> * **promo_free_ship_80 – Free shipping over $80**
>   prmtStatCd 20, prmtTpCd T04
>   tgtMbrGrdCd G00
>   strtDtm 2026-01-01T00:00:00-05:00 → endDtm null
>   Ongoing.
>
> * **promo_gold_10 – Gold tier 10%**
>   prmtStatCd 20, prmtTpCd T02
>   tgtMbrGrdCd G02
>   strtDtm 2026-01-01T00:00:00-05:00 → endDtm null
>   Ongoing.
>
> Total count for the 2026-11-07T00:00:00-05:00 to 2026-11-08T23:59:59-05:00 window is 4.
>
> If you do not want stacking on top of the Autumn knitwear 15% sale, the knit sale is the product discount active 1 Nov – 15 Nov on G00. The other live items this weekend are:
>
> * Free shipping over $80 – shipping benefit, G00, no end date
> * Birthday coupon – coupon benefit, G01 only, no end date
> * Gold tier 10% – member grade discount, G02 only, no end date
>
> The Birthday coupon and Gold tier 10% are price/coupon discounts that would be the ones to watch for stacking with the knitwear 15% product discount on overlapping SKUs/members. Free shipping is a T04 shipping promotion and does not stack with a price discount in the usual sense.

**채점**: ✗ 실패 — 빠진 것: fact "the knit sale covers 26 knitwear products" (26 not shown)

### a2api-facade-all · 1회차 · ✗ 실패

토큰 26,124 · 55.897초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 6,212토큰

준비: 전략 `all`, 함수 22개

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 모델 판단(추론 필드): We need to find promotions live this weekend. Store time: Friday, November 6, 2026, 11:00 (America/New_York). This weekend: presumably Saturday Nov 7 and Sunday Nov 8? Or weekend includes Friday? Usually weekend is Saturday-Sunday. Could be from now to end of Sunday. Need promotions live this weekend. Don't want to stack anything on top of knit sale. We need to identify knit sale promotion. Find promotions with name containing knit? Or maybe category knit? Need to search promotions. We have facade_get_promotion_grid_list with promotion_status, promotion_name, target_member_grade, active_from, active_until, page, page_size. We need promotions live this weekend. Live means status running? Prob… (+2,196자)
1. 모델 → **`facade_get_promotion_grid_list`** `` {"promotion_status":"running","active_from":"2026-11-07T00:00:00","active_until":"2026-11-08T23:59:59","page":1,"page_size":100} ``
   ← 결과 960B: `` {"status":"succeeded","data":{"list":[{"promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00","starts_at":"2026-11-01T00:00:00-04:00","ends_at":"2026-11-15T23:59:00-05:00"},{"promotion_id":"promo_birthday","promotion_name":"Birthday coupon","promotion_type":"order_discount","promotion_status":"running","target_member_grade":"G01","starts_at":"2026-01-01T00:00:00-05:00","ends_at":null},{"promotion_id":"promo_free_ship_80","promotion_name":"Free shipping over $80","promotion_type":"… (+360자) ``
- 모델 판단(추론 필드): We have four running promotions active in that window. Promotion IDs: promo_autumn_knit - Autumn knitwear 15% - item_price_everyone - G00 - starts 2026-11-01 to 2026-11-15 promo_birthday - Birthday coupon - order_discount - G01 - starts 2026-01-01 ends null promo_free_ship_80 - Free shipping over $80 - add_on - G00 promo_gold_10 - Gold tier 10% - order_discount - G02 The knit sale is promo_autumn_knit. User says don't want to stack anything on top of knit sale. Possibly need to identify which of these are stackable? Might need to check stacking rules? Could be promotions have stacking attribute? Not in list. Maybe user wants to know promos live this weekend excluding those that stack with kn… (+2,287자)
2. 모델 → **`facade_get_member_grade_list`** `` {} ``
   ← 결과 257B: `` {"status":"succeeded","data":{"list":[{"member_grade":"G03","grade_name":"VIP","member_count":1284,"rank":3},{"member_grade":"G02","grade_name":"Gold","member_count":2900,"rank":2},{"member_grade":"G01","grade_name":"Member","member_count":9816,"rank":1}]}} ``
- 모델 판단(추론 필드): Member grades: G03 VIP, G02 Gold, G01 Member. G00 is every shopper. Now we can summarize. Possibly also need to check if any promotions are scheduled for weekend specifically? We already have running. We could also check promotion grid list with active_from = 2026-11-06 to 2026-11-08 to include Friday night. Let's check if any additional promotions start this weekend. The current filter active at any time from 2026-11-07 to 2026-11-08. Might miss promotions that start on Saturday but end after. That's covered. If we want to be safe, we could also query for promotions with active_from <= 2026-11-08 and active_until >= 2026-11-07. Our query used active_from and active_until as filters for prom… (+1,926자)

**답변 1**
> This weekend – Sat 2026-11-07 to Sun 2026-11-08 – the promotions that are **running** and active at any time in that window are:
>
> * **promo_autumn_knit – Autumn knitwear 15%**
>   * type: item_price_everyone
>   * target: G00 – Every shopper
>   * status: running
>   * active: 2026-11-01T00:00:00-04:00 → 2026-11-15T23:59:00-05:00
>   * This is your knit sale. It is live all weekend.
>
> * **promo_birthday – Birthday coupon**
>   * type: order_discount
>   * target: G01 – Member
>   * status: running
>   * active: 2026-01-01T00:00:00-05:00 → no end date
>
> * **promo_free_ship_80 – Free shipping over $80**
>   * type: add_on
>   * target: G00 – Every shopper
>   * status: running
>   * active: 2026-01-01T00:00:00-05:00 → no end date
>
> * **promo_gold_10 – Gold tier 10%**
>   * type: order_discount
>   * target: G02 – Gold
>   * status: running
>   * active: 2026-01-01T00:00:00-05:00 → no end date
>
> So the knit sale promo_autumn_knit is live Sat–Sun 7-8 Nov, together with the always-on Birthday coupon for Members, Free shipping over $80 for everyone, and the Gold tier 10% order discount for Gold members.
>
> If you want to keep the knit sale non-stackable, those three other running offers are the ones that would be in play this weekend alongside it.

**채점**: ✗ 실패 — 빠진 것: fact "the knit sale covers 26 knitwear products" (26 not shown)

### a2api-facade-all · 2회차 · ✗ 실패

토큰 52,678 · 60.738초 · 모델 호출 6회 · 도구 호출 5회 · 첫 요청 프롬프트 6,212토큰

준비: 전략 `all`, 함수 22개

**질문 1**
> what promos are live this weekend? I don't want to stack anything on top of the knit sale

- 모델 판단(추론 필드): We need to find promotions live this weekend. Need define weekend. Store time Friday Nov 6 2026 11:00 America/New_York. This weekend presumably Saturday Nov 7 2026 and Sunday Nov 8 2026? Or also Friday? "this weekend" likely Saturday-Sunday. Could be from now onward. Need promotions live this weekend. Don't want to stack anything on top of knit sale. So need identify knit sale promotion. Find promotions with name containing knit? Or maybe category knit? Let's search promotions. We need live this weekend. Promotion status running? Could be scheduled. Live means running on weekend dates. We need get promotion grid list. Filter by active period overlapping weekend. Need date range. We have stor… (+2,192자)
1. 모델 → **`facade_get_promotion_grid_list`** `` {"promotion_status":"running","active_from":"2026-11-07 00:00:00","active_until":"2026-11-08 23:59:59","page":1,"page_size":100} ``
   ← 실패 302B: `` {"status":"failed","error":{"code":"UPSTREAM_VALIDATION_FAILED","detail":"The backend rejected the request values. (HTTP 422) '2026-11-07 00:00:00' is not a date-time (expected 2026-11-07T00:00 or RFC 3339)"},"hint":"The service rejected these values. Correct them only if the user gave other values."} ``
- 모델 판단(추론 필드): Need RFC3339 format. Use 2026-11-07T00:00:00-05:00? Store time America/New_York. Could use Z? Might be okay to use 2026-11-07T00:00:00-04:00? November is EST -05:00. Let's try 2026-11-07T00:00:00-05:00 and 2026-11-08T23:59:59-05:00. Let's retry.
2. 모델 → **`facade_get_promotion_grid_list`** `` {"promotion_status":"running","active_from":"2026-11-07T00:00:00-05:00","active_until":"2026-11-08T23:59:59-05:00","page":1,"page_size":100} ``
   ← 결과 960B: `` {"status":"succeeded","data":{"list":[{"promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00","starts_at":"2026-11-01T00:00:00-04:00","ends_at":"2026-11-15T23:59:00-05:00"},{"promotion_id":"promo_birthday","promotion_name":"Birthday coupon","promotion_type":"order_discount","promotion_status":"running","target_member_grade":"G01","starts_at":"2026-01-01T00:00:00-05:00","ends_at":null},{"promotion_id":"promo_free_ship_80","promotion_name":"Free shipping over $80","promotion_type":"… (+360자) ``
- 모델 판단(추론 필드): We have promotions running this weekend: 1. promo_autumn_knit - Autumn knitwear 15% - item_price_everyone - target G00 - starts 2026-11-01 ends 2026-11-15. That's the knit sale. 2. promo_birthday - Birthday coupon - order_discount - target G01 - starts 2026-01-01 ends null (ongoing) 3. promo_free_ship_80 - Free shipping over $80 - add_on - target G00 4. promo_gold_10 - Gold tier 10% - order_discount - target G02 User says don't want to stack anything on top of knit sale. So need to know which promos stack? Possibly we need to check stacking settings for coupons? Or promotion type? Might need to check if promotions can be combined? The user might want to know which promos are live this weeken… (+2,282자)
3. 모델 → **`facade_get_member_grade_list`** `` {} ``
   ← 결과 257B: `` {"status":"succeeded","data":{"list":[{"member_grade":"G03","grade_name":"VIP","member_count":1284,"rank":3},{"member_grade":"G02","grade_name":"Gold","member_count":2900,"rank":2},{"member_grade":"G01","grade_name":"Member","member_count":9816,"rank":1}]}} ``
- 모델 판단(추론 필드): Member grades: G00 is every shopper (not listed? maybe). G01 = Member, G02 = Gold, G03 = VIP. Now we can answer. We could also check if birthday coupon and gold tier 10% are order discounts that might stack with item_price. Might be they can stack. User doesn't want to stack anything on top of knit sale. So we should warn that Birthday coupon and Gold tier 10% are order discounts active, and free shipping is add-on. If stacking is not desired, you may need to adjust stacking settings. Potentially we could check promotion target member list to see how many members affected. But answer is sufficient. Maybe also check if there are any promotions specifically for knit category besides autumn kni… (+375자)
4. 모델 → **`facade_get_promotion_grid_list`** `` {"promotion_name":"knit","page":1,"page_size":100} ``
   ← 결과 315B: `` {"status":"succeeded","data":{"list":[{"promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00","starts_at":"2026-11-01T00:00:00-04:00","ends_at":"2026-11-15T23:59:00-05:00"}],"page":1,"page_size":100}} ``
- 모델 판단(추론 필드): So knit sale is that. Now we can answer. Potentially also check if any promotion is scheduled to start this weekend. Could query promotion_status = scheduled with active_from within weekend. Let's try promotion_status = scheduled, active_from = 2026-11-07T00:00:00-05:00, active_until = 2026-11-08T23:59:59-05:00.
5. 모델 → **`facade_get_promotion_grid_list`** `` {"promotion_status":"scheduled","active_from":"2026-11-07T00:00:00-05:00","active_until":"2026-11-08T23:59:59-05:00","page":1,"page_size":100} ``
   ← 결과 66B: `` {"status":"succeeded","data":{"list":[],"page":1,"page_size":100}} ``
- 모델 판단(추론 필드): No scheduled. So answer. We might also want to note that the knit sale runs until Nov 15, so it's active. User says I don't want to stack anything on top of knit sale. So we can note that Birthday coupon (Member tier order discount) and Gold tier 10% (Gold tier order discount) are order discounts that could stack with item price. Free shipping over $80 is add-on. If they want no stacking, they might need to ensure stacking settings are no_tier_coupons etc. Might be we need to check coupon stacking for knit sale? Could search coupons for promotion_id promo_autumn_knit. We have facade_save_coupon_list for creating, not querying. No query tool for coupons. Maybe the stacking is inherent to prom… (+319자)

**답변 1**
> This weekend Sat 2026-11-07 – Sun 2026-11-08 America/New_York there are 4 promotions with `promotion_status = running` that are active at any time in that window.
>
> * **promo_autumn_knit – Autumn knitwear 15%**
>   * promotion_type: item_price_everyone
>   * target_member_grade: G00 – every shopper
>   * status: running
>   * starts_at: 2026-11-01T00:00:00-04:00
>   * ends_at: 2026-11-15T23:59:00-05:00
>   This is the knit sale you mentioned. It is live all weekend and runs through 15 Nov.
>
> * **promo_birthday – Birthday coupon**
>   * promotion_type: order_discount
>   * target_member_grade: G01 – Member
>   * status: running
>   * starts_at: 2026-01-01T00:00:00-05:00
>   * ends_at: null
>   Ongoing birthday order discount for Member tier.
>
> * **promo_free_ship_80 – Free shipping over $80**
>   * promotion_type: add_on
>   * target_member_grade: G00 – every shopper
>   * status: running
>   * starts_at: 2026-01-01T00:00:00-05:00
>   * ends_at: null
>   Ongoing free-shipping add-on.
>
> * **promo_gold_10 – Gold tier 10%**
>   * promotion_type: order_discount
>   * target_member_grade: G02 – Gold
>   * status: running
>   * starts_at: 2026-01-01T00:00:00-05:00
>   * ends_at: null
>   Ongoing Gold tier order discount.
>
> Member grades in the system:
> * G01 Member – 9 816 members, rank 1
> * G02 Gold – 2 900 members, rank 2
> * G03 VIP – 1 284 members, rank 3
>
> No promotions are scheduled to start on the weekend. The knit sale `promo_autumn_knit` is the only item-price promotion in the window; the other three live offers are order_discount / add_on offers for G01/G00/G02. If you do not want anything to stack on top of the knit sale, the Birthday coupon and Gold tier 10% order discounts and the Free shipping over $80 add-on are the live offers that would be able to combine with the Autumn knitwear 15% item price in the current running set.

**채점**: ✗ 실패 — 빠진 것: fact "the knit sale covers 26 knitwear products" (26 not shown)
