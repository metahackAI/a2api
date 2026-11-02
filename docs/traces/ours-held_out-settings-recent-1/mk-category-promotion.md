# mk-category-promotion — ours-held_out-settings-recent-1

[← 실행 묶음](README.md) · 세트 `held_out` · a-commerce `d86a1ff` · a2api `8112189`

**과업**

> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 필요한 도구: `create_promotion`
- 허용 도구: `list_categories`, `list_active_promotions`, `get_policy`
- 답에 있어야 할 사실: 2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store time

### a2api-acom · 1회차 · ✗ 실패

토큰 36,349 · 43.985초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 6,020토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 모델 판단(추론 필드): We need promotion for Outerwear, $50 off orders above $250, valid for 2 weeks. Promotion type: threshold with threshold_benefit amount_off? According to acom_create_promotion, promotion_type options: bogo, bundle, threshold, amount_off. threshold promotion: needs threshold, threshold_benefit, amount_off? Description: threshold: a benefit once subtotal reaches threshold; threshold_benefit: what promotion gives. amount_off: fixed amount off. discount_layer: item_price, order_discount, add_on. So we need threshold promotion with threshold $250, threshold_benefit amount_off, amount_off $50. Discount layer likely order_discount. Scope: Outerwear category. Need category_id. We need to find categor… (+309자)
1. 모델 → **`a2api_search`** `` {"query":"list categories"} ``
   ← 결과 367B: `` {"selected":[{"name":"acom_list_categories","id":"acom.list_categories"},{"name":"acom_get_contract","id":"acom.get_contract"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_list_faqs","id":"acom.list_faqs"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
- 모델 판단(추론 필드): We have acom_list_categories. Need to find Outerwear category id. Call acom_list_categories with term_set? Let's list categories.
2. 모델 → **`acom_list_categories`** `` {} ``
   ← 결과 3,713B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+2,400자) ``
- 모델 판단(추론 필드): We have cat_outerwear id. Now need promotion. Valid for 2 weeks. Store time is Friday, November 6, 2026, 11:00 America/New_York. Need valid_from and valid_through. Valid for 2 weeks. Start inclusive. Could start now? Probably start now? Or start today? Valid for 2 weeks. Could set valid_from = 2026-11-06T11:00? The format examples: "2026-11-20T00:00". It says without offset it is read in store time. Let's use 2026-11-06T11:00? Might be better to start at 2026-11-06T00:00? Or now? Probably start now. The promotion valid for 2 weeks. Let's compute valid_through = 2 weeks later. 2 weeks = 14 days. From Nov 6 to Nov 20 inclusive? If start Nov 6 11:00, end Nov 20 11:00? Or end of day Nov 20? Use … (+1,934자)
3. 모델 → **`acom_create_promotion`** `` {"name":"$50 off $250+ Outerwear","promotion_type":"threshold","discount_layer":"order_discount","amount_off":{"value":50,"currency":"USD"},"threshold":{"value":250,"currency":"USD"},"threshold_benefit":"amount_off","valid_from":"2026-11-06T00:00","valid_through":"2026-11-19T23:59","scope_mode":"categories","category_ids":["cat_outerwear"],"valid_for_member_tier":"everyone"} ``
   ← 결과 1,411B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6ed17qgqd1b5y5kvnwqxq6z","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"$50 off $250+ Outerwear","promotion_type":"threshold","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-06T00:00:00-05:00","valid_through":"2026-11-19T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_outerwear"],"product_count":62},"amount_off":{"value":50.0,"currency":"USD"},"threshold":{"value":250.0,"currency":"USD"},"threshold_benefit":"amount_off"}}],"checks":[{"ru… (+809자) ``
- 모델 판단(추론 필드): Promotion created as preview, needs approval. Checks: price_floor passed false: Seersucker overshirt would be $63.20 under floor $66.70. Hmm that's weird because this is threshold amount off, not price floor? Maybe price floor applies to combined discount? Could be issue. Promotion overlap passed false: Denim bundle, Birthday coupon, Gold tier 10% already give order discount on outerwear in this period. The system says needs approval. Should inform user about preview and checks failures. We should report promotion preview created, ID? preview_id pv_01m6ed17qgqd1b5y5kvnwqxq6z, change_set_id cs_1042. Price floor issue, overlap. Possibly need to adjust? User just asked create promotion. We crea… (+339자)

**답변 1**
> Promotion preview created and waiting for approval.
>
> * Name: **$50 off $250+ Outerwear**
> * Type: threshold – order_discount
> * Benefit: $50.00 USD off when subtotal before member benefits ≥ $250.00 USD
> * Scope: categories → cat_outerwear
>   * Applies to 62 products in Outerwear incl. sub-categories
> * Audience: everyone
> * Period: 2026-11-06T00:00:00-05:00 → 2026-11-19T23:59:00-05:00 (≈2 weeks)
> * Change set: cs_1042
> * Preview: pv_01m6ed17qgqd1b5y5kvnwqxq6z
>
> Checks:
> * max_discount: passed – at most 20% on a $250 order; limit 20%
> * price_floor: **failed** – Seersucker overshirt would be $63.20, under the floor $66.70
> * promotion_overlap: **failed** – Denim bundle (everyone), Birthday coupon (member) and Gold tier 10% (gold) already give an order discount on outerwear in this period
> * discount_layers.max_total_discount_rate: passed – combined discount stays under 50% (at most 20%)
> * cost_share.sum_must_equal: passed – Store 100%
>
> The change is a preview only; approval is required before it goes live.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (6, 19, 23 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom · 2회차 · ✗ 실패

토큰 38,167 · 52.967초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 6,020토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 모델 판단(추론 필드): We need promotion for Outerwear, $50 off orders above $250, valid for 2 weeks. We need to interpret. Promotion type? $50 off orders above $250. That's threshold benefit amount off. promotion_type = threshold, discount_layer = order_discount? threshold benefit amount_off. Scope: Outerwear category. So scope_mode categories? Could be categories. Need category_id for Outerwear. We need to find category id. Likely cat_outerwear or similar. Need search. We need valid for 2 weeks. Store time: Friday November 6, 2026, 11:00 America/New_York. 2 weeks valid from? Probably start now? Or start? Might need valid_from and valid_through. "valid for 2 weeks". Probably start today? Could be from 2026-11-06T… (+1,109자)
1. 모델 → **`a2api_search`** `` {"query":"category list"} ``
   ← 결과 367B: `` {"selected":[{"name":"acom_list_categories","id":"acom.list_categories"},{"name":"acom_get_contract","id":"acom.get_contract"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_list_faqs","id":"acom.list_faqs"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
- 모델 판단(추론 필드): We have acom_list_categories available now. Good. Now list categories to find Outerwear.
2. 모델 → **`acom_list_categories`** `` {} ``
   ← 결과 3,713B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+2,400자) ``
- 모델 판단(추론 필드): Outerwear category id is cat_outerwear. Now need promotion: $50 off orders above $250. Promotion_type threshold, discount_layer order_discount? For amount off order. threshold_benefit = amount_off. Need threshold value $250, amount_off $50. Scope_mode categories, category_ids = ["cat_outerwear"]. valid_for_member_tier? Not specified, so default everyone? Valid_for_member_tier parameter optional? In schema, it's optional. Might default everyone. valid_from and valid_through. Store time Friday Nov 6 2026 11:00. Valid for 2 weeks. Could start now? Probably start now inclusive. valid_from = 2026-11-06T11:00? Could be 2026-11-06T00:00? The requirement says valid for 2 weeks. Could interpret as st… (+2,286자)
3. 모델 → **`acom_create_promotion`** `` {"name":"$50 off Outerwear orders over $250","promotion_type":"threshold","discount_layer":"order_discount","amount_off":{"value":50,"currency":"USD"},"threshold":{"value":250,"currency":"USD"},"threshold_benefit":"amount_off","valid_from":"2026-11-06T11:00","valid_through":"2026-11-20T11:00","scope_mode":"categories","category_ids":["cat_outerwear"]} ``
   ← 결과 1,422B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6eevtyvq7d7ab90rs2kexyc","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"$50 off Outerwear orders over $250","promotion_type":"threshold","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-06T11:00:00-05:00","valid_through":"2026-11-20T11:00:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_outerwear"],"product_count":62},"amount_off":{"value":50.0,"currency":"USD"},"threshold":{"value":250.0,"currency":"USD"},"threshold_benefit":"amount_off"}}],"ch… (+820자) ``
- 모델 판단(추론 필드): Promotion created as preview, needs approval. Checks: price_floor passed false: Seersucker overshirt would be $63.20 under floor $66.70. That's a price floor check? Maybe because threshold discount applies to whole order, not per item. Hmm price floor maybe about item price? Might be unrelated. The rule passed false, needs person decision. Also promotion overlap passed false: Denim bundle, Birthday coupon, Gold tier 10% already give order discount on outerwear in this period. We need to inform user. The promotion is created as preview, waiting for approval. Provide details. We should summarize: promotion preview created, id? promotion id null? preview_id pv... change_set_id cs_1042. Needs ap… (+2,164자)

**답변 1**
> The promotion is created as a preview and is waiting for approval.
>
> * **Preview:** pv_01m6eevtyvq7d7ab90rs2kexyc  
> * **Change set:** cs_1042
> * **Name:** $50 off Outerwear orders over $250
> * **Type:** threshold – $50 off the order
> * **Discount layer:** order_discount
> * **Scope:** categories → cat_outerwear  
>   Applies to 62 products in scope
> * **Threshold:** $250.00 USD  
>   Benefit: amount_off $50.00 USD
> * **Member tier:** everyone
> * **Valid:** 2026-11-06T11:00:00-05:00 to 2026-11-20T11:00:00-05:00  ≈ 2 weeks from now
> * **Cost share:** store 100%
>
> Checks:
> * max_discount – passed – at most 20% on a $250 order; limit 20%
> * price_floor – **failed** – Seersucker overshirt would be $63.20, under the floor $66.70
> * promotion_overlap – **failed** – Denim bundle (everyone), Birthday coupon (member) and Gold tier 10% (gold) already give an order discount on outerwear in this period
> * discount_layers.max_total_discount_rate – passed – combined discount stays under 50% (at most 20%)
> * cost_share.sum_must_equal – passed – Store 100%
>
> The change is in preview only. A person must approve change set cs_1042 before the $50 off threshold for Outerwear goes live.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (6, 19, 23, 59 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-batch · 1회차 · ✗ 실패

토큰 55,286 · 66.33초 · 모델 호출 7회 · 도구 호출 6회 · 첫 요청 프롬프트 1,989토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 모델 판단(추론 필드): We need to create a promotion. Likely need to use promotion › promotion: create_promotion. Also maybe need to set sale prices? The promotion is $50 off orders above $250 for Outerwear. We need to know how to create promotion. Let's load functions. We need parameters for create_promotion. Let's load promotion promotion functions.
1. 모델 → **`a2api_load`** `` {"names":["create_promotion","list_active_promotions","get_promotion","search_promotions"]} ``
   ← 결과 92B: `` {"loaded":["create_promotion","list_active_promotions","get_promotion","search_promotions"]} ``
- 모델 판단(추론 필드): We have functions. Create promotion for Outerwear, $50 off orders above $250, valid for 2 weeks. We need product category? Outerwear. Need category_ids. Need to find category id for Outerwear. Possibly via catalog › category: list_categories. Could search. Need category id. We don't have category list function loaded. Might need to load catalog category functions. Let's load.
2. 모델 → **`a2api_load`** `` {"names":["list_categories","get_category","search_products"]} ``
   ← 결과 63B: `` {"loaded":["list_categories","get_category","search_products"]} ``
- 모델 판단(추론 필드): Now get Outerwear category.
3. 모델 → **`list_categories`** `` {} ``
   ← 결과 3,713B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+2,400자) ``
- 모델 판단(추론 필드): Outerwear cat_outerwear. Should we include subcategories? Scope mode categories includes subcategories included per description. So cat_outerwear includes summer_outerwear. Likely fine. Promotion: $50 off orders above $250. That's threshold promotion with threshold benefit amount_off. Promotion type: threshold. discount_layer: order_discount? Could be order_discount. threshold benefit amount_off. Parameters needed: name, promotion_type, discount_layer, amount_off, threshold, threshold_benefit, valid_from, valid_through, scope_mode, category_ids. valid_from: start now? Store time Friday, November 6, 2026, 11:00 America/New_York. Valid for 2 weeks. So valid_from = 2026-11-06T11:00? The API exp… (+1,914자)
4. 모델 → **`list_active_promotions`** `` {"valid_from":"2026-11-06T00:00","valid_through":"2026-11-19T23:59"} ``
   ← 결과 1,489B: `` {"status":"succeeded","data":{"items":[{"id":"promo_denim_bundle","name":"Denim bundle","status":"scheduled","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-13T00:00:00-05:00","valid_through":"2026-11-20T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_denim","cat_outerwear"],"product_count":78}},{"id":"promo_autumn_knit","name":"Autumn knitwear 15%","status":"running","discount_layer":"item_price","valid_for_member_tier":"everyone","valid_from":"2026-11-01T00:00:00-04:00","valid_through":"2026-11-15T23:59:00-05:00","applies_to"… (+889자) ``
- 모델 판단(추론 필드): We have promo_denim_bundle scheduled from Nov 13 to Nov 20 covering categories cat_denim and cat_outerwear, discount_layer order_discount. Overlap with our promotion Nov 6-19 for outerwear. That could be overlap. The promotion overlap check will consider combined discount. Might be okay? Could be conflict. The create_promotion checks discount limit, price floor, overlaps, combined discount and cost share. It always needs a person's approval. So we can still create; it will go to change set. We might want to ensure scope doesn't conflict too much. Might be okay. Also there is no active threshold for outerwear currently. The user requested promotion for Outerwear, $50 off orders above $250, va… (+178자)
5. 모델 → **`create_promotion`** `` {"name":"$50 off $250+ Outerwear","promotion_type":"threshold","discount_layer":"order_discount","amount_off":{"value":50,"currency":"USD"},"threshold":{"value":250,"currency":"USD"},"threshold_benefit":"amount_off","valid_from":"2026-11-06T00:00","valid_through":"2026-11-19T23:59","scope_mode":"categories","category_ids":["cat_outerwear"]} ``
   ← 결과 1,411B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6ecz4qh7t1sp022wk5xjbzm","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"$50 off $250+ Outerwear","promotion_type":"threshold","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-06T00:00:00-05:00","valid_through":"2026-11-19T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_outerwear"],"product_count":62},"amount_off":{"value":50.0,"currency":"USD"},"threshold":{"value":250.0,"currency":"USD"},"threshold_benefit":"amount_off"}}],"checks":[{"ru… (+809자) ``
- 모델 판단(추론 필드): The promotion creation succeeded as preview, but checks failed: price_floor passed false because Seersucker overshirt would be $63.20 under floor $66.70. Also promotion_overlap passed false. The system says needs approval, change_set_id cs_1042. We need to inform user that promotion is created as preview awaiting approval, and note issues: price floor violation and overlap. Possibly we need to address price floor. Could exclude that product? Or adjust? The user asked to create promotion. The system flagged price floor issue. We could suggest adjustments, maybe exclude product? Or increase threshold? The price floor rule relates to item_price discounts? Wait discount_layer is order_discount, … (+1,244자)
6. 모델 → **`search_products`** `` {"query":"Seersucker overshirt"} ``
   ← 결과 5,000B: `` {"status":"succeeded","data":{"items":[{"id":"prd_seersucker_overshirt","name":"Seersucker overshirt","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_seersucker_overshirt-cc4cafc0.webp","price":79.0,"price_currency":"USD","member_price":null,"cost":58.0,"inventory_level":53,"availability":"in_stock","has_variant":[{"variant_id":"var_seersucker_overshirt_xs_white","sku":"so-white-xs","size":"XS","color":"White","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_seersucker_overshirt_s_white","sku":"so-white-s","size":"S","color":"White"… (+2,400자) ``
- 모델 판단(추론 필드): Product id prd_seersucker_overshirt. The price floor issue might be because combined with existing promotion denim bundle which gives order discount? Hmm. The promotion_overlap check failed due to denim bundle (everyone), birthday coupon (member), gold tier 10% (gold) already give order discount on outerwear. Maybe we need to adjust scope to avoid overlap? Could exclude categories? Actually denim bundle applies to cat_denim and cat_outerwear. So overlap. Perhaps we can keep promotion but need approval. The system allowed creation with warnings. The user might just want creation. We should report preview created, change set cs_1042 awaiting approval, notes about price floor and overlap. Poten… (+1,057자)

**답변 1**
> The promotion is staged for approval — it isn’t live yet.
>
> * Preview: pv_01m6ecz4qh7t1sp022wk5xjbzm
> * Change set: cs_1042
> * Name: $50 off $250+ Outerwear
> * Type: threshold – $50 off order_discount when subtotal ≥ $250.00 USD
> * Scope: categories → cat_outerwear
>   * Products covered in scope: 62
> * Period (store time): 2026-11-06T00:00:00-05:00 → 2026-11-19T23:59:00-05:00
> * Audience: everyone
>
> Checks on the preview:
>
> * max_discount: passed – at most 20% on a $250.00 order; limit 20%
> * price_floor: **failed** – “Seersucker overshirt would be $63.20, under the floor $66.70”
> * promotion_overlap: **failed** – Denim bundle (everyone), Birthday coupon (member) and Gold tier 10% (gold) already give an order discount on outerwear in this period
> * discount_layers.max_total_discount_rate: passed – combined discount stays under 50% (at most 20%)
> * cost_share.sum_must_equal: passed – Store 100%
>
> The change set is waiting for a person’s approval before it can be published. Do you want me to re-create it with the Seersucker overshirt excluded – e.g. `exclude_product_ids: ["prd_seersucker_overshirt"]` – or narrow the dates to avoid the Denim bundle overlap (Nov 13-20 on cat_denim + cat_outerwear)?

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (2, 6, 19, 23 not shown)
(도구 정밀도 0.75, 재현율 1.00)

### a2api-acom-names-batch · 2회차 · ✗ 실패

토큰 25,381 · 35.155초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 1,989토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 모델 판단(추론 필드): We need to create a promotion. Use promotion › promotion: create_promotion, ... Also need maybe product group? Outerwear is a category? Need to identify outerwear products. Possibly need to define promotion with conditions. The create_promotion function likely needs parameters. We need to load function to see schema. Let's load create_promotion. a2api_load names: ["promotion.create_promotion"] Also maybe need to find product group for Outerwear? Promotion may require target product group or category. Might need to search product groups. Let's load promotion.create_promotion and also catalog.product_group.search_product_groups? Might need to get product group id for Outerwear. First load crea… (+13자)
1. 모델 → **`a2api_load`** `` {"names":["promotion.create_promotion"]} ``
   ← 결과 31B: `` {"loaded":["create_promotion"]} ``
- 모델 판단(추론 필드): We have create_promotion loaded. Parameters required: name, promotion_type, discount_layer, valid_from, valid_through, scope_mode promotion_type options: bogo, bundle, threshold, amount_off $50 off orders above $250. That's threshold: threshold benefit amount_off $50. promotion_type threshold, discount_layer order_discount? threshold_benefit amount_off. Need threshold value 250 USD, amount_off value 50 USD. scope_mode: need to target Outerwear. Possibly categories? We need category_ids for Outerwear. Let's find category. Could be categories: list_categories. Let's load catalog › category: list_categories.
2. 모델 → **`a2api_load`** `` {"names":["catalog.list_categories"]} ``
   ← 결과 30B: `` {"loaded":["list_categories"]} ``
- 모델 판단(추론 필드): We need to find category id for Outerwear. Probably standard classification. Call list_categories with maybe term_set standard? We'll search for name containing outerwear. list_categories doesn't have search term? Might need to list all and find. Could filter fields name. We could try list_categories with parent_id? Unknown. Let's try list_categories term_set standard, limit 100.
3. 모델 → **`list_categories`** `` {"term_set":"standard","limit":100} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+2,400자) ``
- 모델 판단(추론 필드): Category Outerwear id cat_outerwear. Now need valid_from and valid_through for 2 weeks. Store time: Friday, November 6, 2026, 11:00 America/New_York. 2 weeks valid for. Probably start today? Probably valid from now? Could start 2026-11-06T11:00? Or start at 00:00? Might be 2 weeks inclusive. Let's assume valid_from 2026-11-06T11:00 (store time). Valid_through 2 weeks later: 2026-11-20? Actually 2 weeks = 14 days. From Nov 6 11:00 to Nov 20 11:00. End inclusive minute precision. The function expects valid_through inclusive minute. Maybe use 2026-11-20T10:59? Or 2026-11-20T23:59. Simpler: valid_from 2026-11-06T00:00, valid_through 2026-11-19T23:59 (that's 14 days). Hmm. The user said valid for… (+1,347자)
4. 모델 → **`create_promotion`** `` {"name":"$50 off Outerwear orders $250+","promotion_type":"threshold","discount_layer":"order_discount","threshold":{"value":250,"currency":"USD"},"threshold_benefit":"amount_off","amount_off":{"value":50,"currency":"USD"},"valid_from":"2026-11-06T11:00","valid_through":"2026-11-20T11:00","scope_mode":"categories","category_ids":["cat_outerwear"]} ``
   ← 결과 1,418B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6eexerkd4ry7xard67px4ep","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"$50 off Outerwear orders $250+","promotion_type":"threshold","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-06T11:00:00-05:00","valid_through":"2026-11-20T11:00:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_outerwear"],"product_count":62},"amount_off":{"value":50.0,"currency":"USD"},"threshold":{"value":250.0,"currency":"USD"},"threshold_benefit":"amount_off"}}],"checks… (+816자) ``
- 모델 판단(추론 필드): The promotion creation succeeded as preview, needs approval. Checks: price_floor passed false, promotion_overlap passed false. But it still created preview. We need to inform user. Should note issues: price floor violation for Seersucker overshirt would be $63.20 under floor $66.70. Also overlap with Denim bundle, Birthday coupon, Gold tier 10%. The user asked create promotion. We did. It's pending approval. We should report status, preview_id, change_set_id, and warnings. Perhaps we should suggest fixing price floor? Could adjust amount_off? Or exclude product? Might be okay to inform. The instruction: A change you make is only a preview that goes into one change set for a person to approve… (+289자)

**답변 1**
> Created a preview for the Outerwear threshold promotion.
>
> * Name: $50 off Outerwear orders $250+
> * Type: threshold → $50 amount_off when subtotal ≥ $250
> * Discount layer: order_discount
> * Scope: categories `cat_outerwear` – Outerwear
>   * Applies to 62 products (sub-categories included, e.g. Summer outerwear)
> * Valid: 2026-11-06T11:00:00-05:00 to 2026-11-20T11:00:00-05:00  (2 weeks from store time)
> * Member tier: everyone
>
> Preview
> * preview_id: pv_01m6eexerkd4ry7xard67px4ep
> * change_set_id: cs_1042
> * Needs approval: yes – “New order discount for everyone, Nov 6–20”
>
> Checks from the preview
> * max_discount: passed – at most 20% on a $250 order, within limit
> * price_floor: failed – Seersucker overshirt would be $63.20, under the floor $66.70
> * promotion_overlap: failed – Denim bundle (everyone), Birthday coupon (member) and Gold tier 10% (gold) already give an order discount on outerwear in this period
> * discount_layers.max_total_discount_rate: passed
> * cost_share.sum_must_equal: passed – store 100%
>
> The change is in change set cs_1042 and is waiting for an approver before it can be published.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (19, 23, 59 not shown)
(도구 정밀도 1.00, 재현율 1.00)
