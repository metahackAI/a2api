# mk-category-promotion — ours-heldout-guard-posthoc-1

[← 실행 묶음](README.md) · 세트 `held_out` · a-commerce `d86a1ff` · a2api `e2b7fa2`

**과업**

> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 필요한 도구: `create_promotion`
- 허용 도구: `list_categories`, `list_active_promotions`, `get_policy`
- 답에 있어야 할 사실: 2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store time

### a2api-acom · 1회차 · ✓ 통과

토큰 34,665 · 28.974초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 6,020토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 모델 판단(추론 필드): We need to create promotion. Promotion type? $50 off orders above $250. That's threshold promotion: threshold $250, benefit amount_off $50. Discount layer? order_discount? Probably order_discount. Promotion type threshold. Need scope_mode? Outerwear category. Need category_id. Need to find category id for Outerwear. Use a2api_search? Could search for functions? Need list_categories? Not in tool list. Might need to search products? Could use a2api_search to find function list_categories. Let's search. We need category_id for Outerwear. Use a2api_search query "category".
1. 모델 → **`a2api_search`** `` {"query":"list categories"} ``
   ← 결과 367B: `` {"selected":[{"name":"acom_list_categories","id":"acom.list_categories"},{"name":"acom_get_contract","id":"acom.get_contract"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_list_faqs","id":"acom.list_faqs"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
- 모델 판단(추론 필드): We need promotion for Outerwear, $50 off orders above $250, valid for 2 weeks. We need category id for Outerwear. Use acom_list_categories. We need to find category id. Let's list categories.
2. 모델 → **`acom_list_categories`** `` {} ``
   ← 결과 3,713B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+2,400자) ``
- 모델 판단(추론 필드): We have category id cat_outerwear. Promotion type: threshold? $50 off orders above $250. That's threshold benefit amount_off. Promotion_type threshold, discount_layer order_discount? The description: threshold: a benefit once subtotal reaches threshold; threshold_benefit: amount_off or free_shipping. discount_layer? For threshold promotion, discount_layer is order_discount? Probably order_discount. Need name, promotion_type, discount_layer, amount_off, threshold, threshold_benefit, valid_from, valid_through, scope_mode, category_ids. Valid for 2 weeks. Store time: Friday, November 6, 2026, 11:00 America/New_York. Valid from? Probably start now? Could be 2026-11-06T11:00? Or start at 00:00? U… (+1,781자)
3. 모델 → **`acom_create_promotion`** `` {"name":"$50 off Outerwear $250+","promotion_type":"threshold","discount_layer":"order_discount","amount_off":{"value":50,"currency":"USD"},"threshold":{"value":250,"currency":"USD"},"threshold_benefit":"amount_off","valid_from":"2026-11-06T00:00","valid_through":"2026-11-19T23:59","scope_mode":"categories","category_ids":["cat_outerwear"]} ``
   ← 결과 1,411B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6cfgzfbqhj9v0rkjae0wjnn","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"$50 off Outerwear $250+","promotion_type":"threshold","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-06T00:00:00-05:00","valid_through":"2026-11-19T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_outerwear"],"product_count":62},"amount_off":{"value":50.0,"currency":"USD"},"threshold":{"value":250.0,"currency":"USD"},"threshold_benefit":"amount_off"}}],"checks":[{"ru… (+809자) ``

**답변 1**
> The promotion is created as a preview and needs approval.
>
> **$50 off Outerwear $250+**
> - Type: threshold → $50 off the order when subtotal ≥ $250
> - Scope: category cat_outerwear (Outerwear, includes subcategories; 62 products in scope)
> - Discount layer: order_discount
> - Valid: 2026-11-06 00:00 to 2026-11-19 23:59 America/New_York (2 weeks)
> - Member tier: everyone
>
> Preview ID: pv_01m6cfgzfbqhj9v0rkjae0wjnn
> Change set: cs_1042
>
> Checks:
> - max_discount: passed
> - price_floor: failed – Seersucker overshirt would be $63.20, under the floor $66.70
> - promotion_overlap: failed – Denim bundle (everyone), Birthday coupon (member) and Gold tier 10% (gold) already give an order discount on outerwear in this period
> - discount_layers.max_total_discount_rate: passed
> - cost_share.sum_must_equal: passed
>
> The change is waiting for a person’s approval before it goes live.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom · 2회차 · ✓ 통과

토큰 35,171 · 37.566초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 6,020토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 모델 판단(추론 필드): We need to create promotion. Outerwear category. $50 off orders above $250. That's threshold promotion: threshold $250, benefit amount_off $50. Promotion type threshold, discount_layer order_discount? threshold benefit amount_off. Scope mode? Outerwear category. So scope_mode categories? The promotion type threshold with scope_mode categories? Let's see parameters for acom_create_promotion. Parameters: name promotion_type: bogo, bundle, threshold, amount_off discount_layer: item_price, order_discount, add_on amount_off: object value currency threshold: object value currency threshold_benefit: amount_off or free_shipping buy_quantity etc valid_from valid_through valid_for_member_tier scope_mo… (+1,479자)
1. 모델 → **`a2api_search`** `` {"query":"list categories"} ``
   ← 결과 367B: `` {"selected":[{"name":"acom_list_categories","id":"acom.list_categories"},{"name":"acom_get_contract","id":"acom.get_contract"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_list_faqs","id":"acom.list_faqs"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
- 모델 판단(추론 필드): We need promotion for Outerwear, $50 off orders above $250, valid for 2 weeks. We need category id for Outerwear. Use acom_list_categories. We need to find category id. Let's list categories.
2. 모델 → **`acom_list_categories`** `` {} ``
   ← 결과 3,713B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+2,400자) ``
- 모델 판단(추론 필드): We have category id cat_outerwear. Promotion type: threshold? $50 off orders above $250. That's threshold benefit amount_off. Promotion_type threshold, discount_layer order_discount? The description: threshold: a benefit once subtotal reaches threshold; threshold_benefit: amount_off or free_shipping. discount_layer? For threshold promotion, discount_layer is order_discount? Probably order_discount. Need name, promotion_type, discount_layer, amount_off, threshold, threshold_benefit, valid_from, valid_through, scope_mode, category_ids. Valid for 2 weeks. Store time: Friday, November 6, 2026, 11:00 America/New_York. Valid from? Probably start now? Could be 2026-11-06T11:00? Or start at 00:00? U… (+1,781자)
3. 모델 → **`acom_create_promotion`** `` {"name":"$50 off Outerwear $250+","promotion_type":"threshold","discount_layer":"order_discount","amount_off":{"value":50,"currency":"USD"},"threshold":{"value":250,"currency":"USD"},"threshold_benefit":"amount_off","valid_from":"2026-11-06T00:00","valid_through":"2026-11-19T23:59","scope_mode":"categories","category_ids":["cat_outerwear"]} ``
   ← 결과 1,411B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6cm087bb1mppp4xv9agvw80","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"$50 off Outerwear $250+","promotion_type":"threshold","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-06T00:00:00-05:00","valid_through":"2026-11-19T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_outerwear"],"product_count":62},"amount_off":{"value":50.0,"currency":"USD"},"threshold":{"value":250.0,"currency":"USD"},"threshold_benefit":"amount_off"}}],"checks":[{"ru… (+809자) ``

**답변 1**
> The promotion is created as a preview and needs approval.
>
> Preview ID: pv_01m6cm087bb1mppp4xv9agvw80
> Change set: cs_1042
>
> $50 off Outerwear $250+
> - Type: threshold amount_off
> - Discount layer: order_discount
> - Scope: categories cat_outerwear (62 products, subcategories included)
> - Valid: 2026-11-06 00:00 to 2026-11-19 23:59 America/New_York (2 weeks)
> - Tier: everyone
> - Threshold: $250.00 USD, benefit: $50.00 USD off
>
> Checks:
> - max_discount: passed
> - price_floor: failed – Seersucker overshirt would be $63.20, under the floor $66.70
> - promotion_overlap: failed – Denim bundle (everyone), Birthday coupon (member) and Gold tier 10% (gold) already give an order discount on outerwear in this period
> - discount_layers.max_total_discount_rate: passed
> - cost_share.sum_must_equal: passed
>
> The change is waiting for a person's approval before it can be published.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-guard · 1회차 · ✓ 통과

토큰 34,632 · 28.696초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 6,020토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 모델 판단(추론 필드): We need to create promotion. Outerwear category? Need category id. Need to find category for Outerwear. Use a2api_search to find functions? We need category id. Possibly list_categories? Not in tool list. Could search products? Might need category id. Use a2api_search to find function to list categories. Let's search. We have tools: a2api_search to find functions by task keywords. Could search for list categories. Let's call a2api_search query "list categories".
1. 모델 → **`a2api_search`** `` {"query":"list categories"} ``
   ← 결과 367B: `` {"selected":[{"name":"acom_list_categories","id":"acom.list_categories"},{"name":"acom_get_contract","id":"acom.get_contract"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_list_faqs","id":"acom.list_faqs"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
- 모델 판단(추론 필드): We need promotion for Outerwear, $50 off orders above $250, valid for 2 weeks. We need category id for Outerwear. Use acom_list_categories. We need to find category id. Let's list categories.
2. 모델 → **`acom_list_categories`** `` {} ``
   ← 결과 3,713B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+2,400자) ``
- 모델 판단(추론 필드): We have category id cat_outerwear. Promotion type: threshold? $50 off orders above $250. That's threshold benefit amount_off. Promotion_type threshold, discount_layer order_discount? The description: threshold: a benefit once subtotal reaches threshold; threshold_benefit: amount_off or free_shipping. discount_layer? For threshold promotion, discount_layer is order_discount? Probably order_discount. Need name, promotion_type, discount_layer, amount_off, threshold, threshold_benefit, valid_from, valid_through, scope_mode, category_ids. Valid for 2 weeks. Store time: Friday, November 6, 2026, 11:00 America/New_York. Valid from? Probably start now? Could be 2026-11-06T11:00? Or start at 00:00? U… (+1,781자)
3. 모델 → **`acom_create_promotion`** `` {"name":"$50 off Outerwear $250+","promotion_type":"threshold","discount_layer":"order_discount","amount_off":{"value":50,"currency":"USD"},"threshold":{"value":250,"currency":"USD"},"threshold_benefit":"amount_off","valid_from":"2026-11-06T00:00","valid_through":"2026-11-19T23:59","scope_mode":"categories","category_ids":["cat_outerwear"]} ``
   ← 결과 1,411B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6cfc75zqmayd4w85wxzgckq","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"$50 off Outerwear $250+","promotion_type":"threshold","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-06T00:00:00-05:00","valid_through":"2026-11-19T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_outerwear"],"product_count":62},"amount_off":{"value":50.0,"currency":"USD"},"threshold":{"value":250.0,"currency":"USD"},"threshold_benefit":"amount_off"}}],"checks":[{"ru… (+809자) ``

**답변 1**
> Created a preview for “$50 off Outerwear $250+” (threshold promotion).
>
> * Scope: category cat_outerwear (62 products, subcategories included)
> * Benefit: $50 off the order when subtotal before member benefits ≥ $250
> * Period: 2026-11-06 00:00 to 2026-11-19 23:59 America/New_York (2 weeks)
> * Tier: everyone
> * Discount layer: order_discount
>
> Preview ID: pv_01m6cfc75zqmayd4w85wxzgckq
> Change set: cs_1042 — waiting for approval.
>
> Checks:
> * max_discount: passed (≤20% on a $250 order)
> * price_floor: failed — Seersucker overshirt would be $63.20, under floor $66.70
> * promotion_overlap: failed — Denim bundle (everyone), Birthday coupon (member) and Gold tier 10% (gold) already give an order discount on outerwear in this period
> * combined discount: passed
> * cost share: passed
>
> The promotion is not live until approved.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-guard · 2회차 · ✗ 실패

토큰 35,182 · 34.598초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 6,020토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 모델 판단(추론 필드): We need to create promotion. Promotion type? $50 off orders above $250. That's threshold promotion: threshold $250, benefit amount_off $50. Discount layer? order_discount? Probably order_discount. Promotion type threshold. Need scope_mode? Outerwear category. So scope_mode categories? The promotion is for Outerwear. Does it apply to orders containing Outerwear? Or whole order? The description: $50 off orders above $250. Probably for orders with Outerwear? Could be scope_mode categories with category_ids for Outerwear. Need category id. Need to find category id for Outerwear. Use a2api_search? Could search for functions? Need list_categories. Not in tool list. Might need to search for functio… (+1,683자)
1. 모델 → **`a2api_search`** `` {"query":"list categories"} ``
   ← 결과 367B: `` {"selected":[{"name":"acom_list_categories","id":"acom.list_categories"},{"name":"acom_get_contract","id":"acom.get_contract"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_list_faqs","id":"acom.list_faqs"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
- 모델 판단(추론 필드): We need promotion for Outerwear, $50 off orders above $250, valid for 2 weeks. We need category id for Outerwear. Use acom_list_categories. We need to find category id. Let's list categories.
2. 모델 → **`acom_list_categories`** `` {} ``
   ← 결과 3,713B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+2,400자) ``
- 모델 판단(추론 필드): We have category cat_outerwear. Need promotion: $50 off orders above $250. That's threshold promotion: threshold $250, benefit amount_off $50. Scope mode categories? Promotion type threshold, discount_layer order_discount? The threshold benefit amount_off off order. Scope_mode categories, category_ids [cat_outerwear]. Need valid_from and valid_through. Store time: Friday, November 6, 2026, 11:00 America/New_York. Valid for 2 weeks. So valid_from? Probably start now? Could be 2026-11-06T11:00? Or start at 00:00? Usually start inclusive. Let's assume start today 2026-11-06T00:00? Or 11:00? The store time is 11:00. Might want start now. Use valid_from 2026-11-06T11:00? The format examples: 2026… (+1,905자)
3. 모델 → **`acom_create_promotion`** `` {"name":"$50 off $250+ Outerwear","promotion_type":"threshold","discount_layer":"order_discount","amount_off":{"value":50,"currency":"USD"},"threshold":{"value":250,"currency":"USD"},"threshold_benefit":"amount_off","valid_from":"2026-11-06T00:00","valid_through":"2026-11-20T23:59","scope_mode":"categories","category_ids":["cat_outerwear"]} ``
   ← 결과 1,411B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6cm1mb227fa0wch0jyfmbpx","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"$50 off $250+ Outerwear","promotion_type":"threshold","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-06T00:00:00-05:00","valid_through":"2026-11-20T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_outerwear"],"product_count":62},"amount_off":{"value":50.0,"currency":"USD"},"threshold":{"value":250.0,"currency":"USD"},"threshold_benefit":"amount_off"}}],"checks":[{"ru… (+809자) ``

**답변 1**
> The promotion is created as a preview and is waiting for approval.
>
> **$50 off $250+ Outerwear**
> - Type: threshold → $50 off the order when subtotal ≥ $250
> - Scope: category cat_outerwear (Outerwear, includes subcategories; 62 products in scope)
> - Discount layer: order_discount
> - Valid for: everyone
> - Period: 2026-11-06 00:00 to 2026-11-20 23:59 America/New_York (2 weeks)
> - Preview ID: pv_01m6cm1mb227fa0wch0jyfmbpx
> - Change set: cs_1042
>
> Checks:
> - max_discount: passed (at most 20% on a $250 order; limit 20%)
> - price_floor: failed – Seersucker overshirt would be $63.20, under the floor $66.70
> - promotion_overlap: failed – Denim bundle (everyone), Birthday coupon (member) and Gold tier 10% (gold) already give an order discount on outerwear in this period
> - discount_layers.max_total_discount_rate: passed
> - cost_share.sum_must_equal: passed
>
> The change needs a person’s approval before it goes live.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (19 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-batch · 1회차 · ✗ 실패

토큰 24,586 · 44.637초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 1,989토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 모델 판단(추론 필드): We need to create a promotion. Use promotion › promotion: create_promotion, end_promotion, get_promotion, list_active_promotions, pause_promotion, search_promotions, update_promotion We need to know parameters for create_promotion. Need to load function.
1. 모델 → **`a2api_load`** `` {"names":["create_promotion"]} ``
   ← 결과 31B: `` {"loaded":["create_promotion"]} ``
- 모델 판단(추론 필드): We need promotion for Outerwear, $50 off orders above $250, valid for 2 weeks. We need category id for Outerwear. Need to find category. Use list_categories? Need to load function. Let's load merchandising category list_categories. Also need valid_from and valid_through. Store time: Friday, November 6, 2026, 11:00 America/New_York. Valid for 2 weeks. So valid_from? Probably start now? Could be 2026-11-06T11:00? Or start at 00:00? Probably start now. Valid through 2 weeks later: 2026-11-20? 2 weeks = 14 days. From Nov 6 to Nov 20 inclusive? Let's compute: Nov 6 +14 days = Nov 20. If valid_from is 2026-11-06T11:00, valid_through 2026-11-20T11:00? Or end of day? The spec says end inclusive minu… (+272자)
2. 모델 → **`a2api_load`** `` {"names":["list_categories"]} ``
   ← 결과 30B: `` {"loaded":["list_categories"]} ``
- 모델 판단(추론 필드): We need promotion for Outerwear, $50 off orders above $250, valid for 2 weeks. We need category id for Outerwear. Need to list categories. Use list_categories. Probably term_set? Could be standard or display. Outerwear likely category. We need scope_mode categories, category_ids. Need category id. Also promotion_type: threshold? $50 off orders above $250. That's threshold promotion with threshold benefit amount_off. promotion_type = threshold. discount_layer = order_discount? Probably order_discount. threshold value 250 currency USD. amount_off value 50 currency USD. threshold_benefit = amount_off. valid_from: store time Friday November 6 2026 11:00 America/New_York. Valid for 2 weeks. So va… (+892자)
3. 모델 → **`list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+2,400자) ``
- 모델 판단(추론 필드): We have category id cat_outerwear. Need promotion type threshold? $50 off orders above $250. That's threshold promotion with threshold benefit amount_off. Promotion type threshold, discount_layer order_discount? Probably order_discount. Scope_mode categories, category_ids [cat_outerwear]. Need valid_from and valid_through. Store time: Friday, November 6, 2026, 11:00 America/New_York. Valid for 2 weeks. So valid_from? Probably start now? Could be 2026-11-06T11:00? Or start at 00:00? Probably start now. Use valid_from = 2026-11-06T11:00? The example uses 2026-11-20T00:00. Might need inclusive. Let's use start today at 00:00? The request says valid for 2 weeks. Could start now. Safer to start a… (+1,686자)
4. 모델 → **`create_promotion`** `` {"name":"$50 off $250+ Outerwear","promotion_type":"threshold","discount_layer":"order_discount","amount_off":{"value":50,"currency":"USD"},"threshold":{"value":250,"currency":"USD"},"threshold_benefit":"amount_off","valid_from":"2026-11-06T00:00","valid_through":"2026-11-19T23:59","scope_mode":"categories","category_ids":["cat_outerwear"]} ``
   ← 결과 1,411B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6cfdt572qna9321yz48zsn5","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"$50 off $250+ Outerwear","promotion_type":"threshold","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-06T00:00:00-05:00","valid_through":"2026-11-19T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_outerwear"],"product_count":62},"amount_off":{"value":50.0,"currency":"USD"},"threshold":{"value":250.0,"currency":"USD"},"threshold_benefit":"amount_off"}}],"checks":[{"ru… (+809자) ``
- 모델 판단(추론 필드): Create promotion for Outerwear, $50 off orders above $250, valid for 2 weeks. We have created promotion preview. The tool output shows succeeded but checks: price_floor passed false: Seersucker overshirt would be $63.20, under floor $66.70. promotion_overlap passed false: Denim bundle etc already give order discount on outerwear in this period. Needs approval. Change set id cs_1042. We need to inform user. The promotion is created as preview waiting approval. Might need to note issues. The user asked create promotion. We have done. Should report key numbers: preview_id pv_01m6cfdt572qna9321yz48zsn5, change_set_id cs_1042, valid 2026-11-06 to 2026-11-19, applies to cat_outerwear with 62 produ… (+456자)

**답변 1**
> Promotion preview created and waiting for approval.
>
> * Preview ID: pv_01m6cfdt572qna9321yz48zsn5
> * Change set: cs_1042
> * Name: $50 off $250+ Outerwear
> * Type: threshold → $50 off order_discount when subtotal ≥ $250
> * Scope: categories → cat_outerwear
>   * Applies to 62 products in the category tree
> * Valid: 2026-11-06T00:00:00-05:00 to 2026-11-19T23:59:00-05:00  ≈ 2 weeks
> * Member tier: everyone
>
> Checks:
> * max_discount: passed
> * price_floor: **failed** – Seersucker overshirt would be $63.20, under floor $66.70
> * promotion_overlap: **failed** – Denim bundle (everyone), Birthday coupon (member) and Gold tier 10% (gold) already give an order discount on outerwear in this period
> * discount_layers.max_total_discount_rate: passed
> * cost_share.sum_must_equal: passed
>
> The change is in change set cs_1042 and needs a person's approval before it can be published.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (6, 19, 23 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-batch · 2회차 · ✗ 실패

토큰 20,844 · 43.32초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 1,989토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 모델 판단(추론 필드): We need to create a promotion. Use promotion › promotion: create_promotion. Need parameters. Let's load function. We need to know parameters for create_promotion. Likely need promotion name, description, discount type, amount, conditions, product group/category, validity dates. We have store time: Friday, November 6, 2026, 11:00 America/New_York. Valid for 2 weeks. So start date? Probably now? Valid for 2 weeks from now? Could be start today, end 2 weeks later. Need dates. We need Outerwear category. Might need product group or category ID. Need to find Outerwear category. Use merchandising › category: list_categories or get_category? Might need to search. We need to create promotion for Out… (+223자)
1. 모델 → **`a2api_load`** `` {"names":["promotion › promotion: create_promotion","merchandising › category: list_categories","merchandising › category: get_category"]} ``
   ← 결과 64B: `` {"loaded":["create_promotion","list_categories","get_category"]} ``
- 모델 판단(추론 필드): We need promotion for Outerwear, $50 off orders above $250, valid for 2 weeks. Promotion type: threshold? $50 off orders above $250. That's threshold promotion with threshold_benefit amount_off. discount_layer: order_discount? Probably order_discount. threshold benefit amount_off. scope_mode: categories. Need category_ids for Outerwear. We need to find category id for Outerwear. Use list_categories. Possibly standard or display. Let's list categories. We need to find Outerwear category id. Could be cat_outerwear. Let's list categories with term_set? Let's list all. We need to find category id. Use list_categories. Also need valid_from and valid_through. Store time: Friday, November 6, 2026, … (+1,290자)
2. 모델 → **`list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+2,400자) ``
- 모델 판단(추론 필드): We have cat_outerwear id cat_outerwear. Need promotion for Outerwear, $50 off orders above $250, valid for 2 weeks. Promotion type: threshold? $50 off orders above $250. That's threshold promotion with threshold_benefit amount_off. Promotion_type threshold, discount_layer order_discount? Probably order_discount. Need amount_off value 50 currency USD. threshold value 250 currency USD. threshold_benefit amount_off. Scope_mode categories, category_ids [cat_outerwear]. Valid_from? Store time Friday November 6 2026 11:00 America/New_York. Valid for 2 weeks. Valid_from inclusive? Probably start now? Could be 2026-11-06T11:00? Or start at 00:00? Use store time. Valid_from "2026-11-06T11:00"? Might … (+1,929자)
3. 모델 → **`create_promotion`** `` {"name":"$50 off $250+ Outerwear","promotion_type":"threshold","discount_layer":"order_discount","amount_off":{"value":50,"currency":"USD"},"threshold":{"value":250,"currency":"USD"},"threshold_benefit":"amount_off","valid_from":"2026-11-06T11:00","valid_through":"2026-11-20T11:00","scope_mode":"categories","category_ids":["cat_outerwear"]} ``
   ← 결과 1,411B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6ckwxtjf4j9y8n9qphyrdhr","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"$50 off $250+ Outerwear","promotion_type":"threshold","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-06T11:00:00-05:00","valid_through":"2026-11-20T11:00:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_outerwear"],"product_count":62},"amount_off":{"value":50.0,"currency":"USD"},"threshold":{"value":250.0,"currency":"USD"},"threshold_benefit":"amount_off"}}],"checks":[{"ru… (+809자) ``
- 모델 판단(추론 필드): Create promotion for Outerwear, $50 off orders above $250, valid for 2 weeks. We have created promotion preview. The tool output shows status succeeded, preview_id, changes, checks. Checks: price_floor passed false: Seersucker overshirt would be $63.20, under floor $66.70. promotion_overlap passed false: Denim bundle, Birthday coupon, Gold tier 10% already give order discount on outerwear in this period. needs_approval true. We need to inform user. The promotion is created as preview, waiting for approval. Also note checks failed. We should report key numbers: promotion name, valid from 2026-11-06 11:00 to 2026-11-20 11:00 (2 weeks). Scope categories cat_outerwear, product count 62. Amount o… (+388자)

**답변 1**
> Created a preview for the Outerwear threshold promotion.
>
> * Name: **$50 off $250+ Outerwear**
> * Type: threshold → $50 off order when subtotal ≥ $250
> * Discount layer: order_discount
> * Scope: categories `cat_outerwear` – 62 products in scope (subcategories included)
> * Valid: 2026-11-06 11:00 to 2026-11-20 11:00 America/New_York  – 2 weeks
> * Member tier: everyone
>
> Preview ID: pv_01m6ckwxtjf4j9y8n9qphyrdhr
> Change set: cs_1042 – waiting for approval.
>
> Checks:
> * max_discount: passed – at most 20% on a $250 order
> * price_floor: **failed** – Seersucker overshirt would be $63.20, under the floor $66.70
> * promotion_overlap: **failed** – Denim bundle (everyone), Birthday coupon (member) and Gold tier 10% (gold) already give an order discount on outerwear in this period
> * discount_layers.max_total_discount_rate: passed
> * cost_share.sum_must_equal: passed – Store 100%
>
> The promotion is not live yet; it needs a person’s approval in change set cs_1042.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (19, 23, 59 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-batch-guard · 1회차 · ✗ 실패

토큰 24,879 · 47.911초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 1,989토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 모델 판단(추론 필드): We need to create a promotion. Use promotion › promotion: create_promotion, end_promotion, get_promotion, list_active_promotions, pause_promotion, search_promotions, update_promotion We need to know parameters for create_promotion. Need to load function.
1. 모델 → **`a2api_load`** `` {"names":["create_promotion"]} ``
   ← 결과 31B: `` {"loaded":["create_promotion"]} ``
- 모델 판단(추론 필드): We need promotion for Outerwear, $50 off orders above $250, valid for 2 weeks. We need category id for Outerwear. Need to find category. Use list_categories? Need to load function. Let's load merchandising category list_categories. Also need valid_from and valid_through. Store time: Friday, November 6, 2026, 11:00 America/New_York. Valid for 2 weeks. So valid_from? Probably start now? Could be 2026-11-06T11:00? Or start at 00:00? Probably start now. Valid through 2 weeks later: 2026-11-20? 2 weeks = 14 days. From Nov 6 to Nov 20 inclusive? Let's compute: Nov 6 +14 days = Nov 20. If valid_from is 2026-11-06T11:00, valid_through 2026-11-20T11:00? Or end of day? The spec says valid_through incl… (+248자)
2. 모델 → **`a2api_load`** `` {"names":["list_categories"]} ``
   ← 결과 30B: `` {"loaded":["list_categories"]} ``
- 모델 판단(추론 필드): We need promotion for Outerwear, $50 off orders above $250, valid for 2 weeks. We need category id for Outerwear. Need to list categories. Use list_categories. Probably term_set? Could be standard or display. Outerwear likely category. We need scope_mode categories, category_ids. Need category id. Also promotion_type: threshold? $50 off orders above $250. That's threshold promotion with threshold benefit amount_off. promotion_type = threshold. discount_layer = order_discount? Probably order_discount. threshold value 250 currency USD. amount_off value 50 currency USD. threshold_benefit = amount_off. valid_from: store time Friday November 6 2026 11:00 America/New_York. Valid for 2 weeks. So va… (+1,053자)
3. 모델 → **`list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+2,400자) ``
- 모델 판단(추론 필드): We have category id cat_outerwear. Need promotion type threshold? $50 off orders above $250. That's threshold promotion with threshold benefit amount_off. Promotion type threshold, discount_layer order_discount? Probably order_discount. Scope_mode categories, category_ids [cat_outerwear]. Need valid_from and valid_through. Store time: Friday, November 6, 2026, 11:00 America/New_York. Valid for 2 weeks. So valid_from? Probably start now? Could be 2026-11-06T11:00? Or start at 00:00? Use store time. Valid_from inclusive. Let's set valid_from = 2026-11-06T11:00? Might be better to start at 2026-11-06T00:00? The request says valid for 2 weeks. Could start now. Use 2026-11-06T11:00 to 2026-11-20T… (+1,880자)
4. 모델 → **`create_promotion`** `` {"name":"$50 off $250+ Outerwear","promotion_type":"threshold","discount_layer":"order_discount","amount_off":{"value":50,"currency":"USD"},"threshold":{"value":250,"currency":"USD"},"threshold_benefit":"amount_off","valid_from":"2026-11-06T11:00","valid_through":"2026-11-20T11:00","scope_mode":"categories","category_ids":["cat_outerwear"]} ``
   ← 결과 1,411B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6cffgrwpj48v7g5xg1kae04","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"$50 off $250+ Outerwear","promotion_type":"threshold","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-06T11:00:00-05:00","valid_through":"2026-11-20T11:00:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_outerwear"],"product_count":62},"amount_off":{"value":50.0,"currency":"USD"},"threshold":{"value":250.0,"currency":"USD"},"threshold_benefit":"amount_off"}}],"checks":[{"ru… (+809자) ``
- 모델 판단(추론 필드): Create promotion for Outerwear, $50 off orders above $250, valid for 2 weeks. We have created promotion preview. The tool output shows succeeded but checks: price_floor passed false: Seersucker overshirt would be $63.20, under floor $66.70. promotion_overlap passed false: Denim bundle etc already give order discount on outerwear in this period. Needs approval: true, change_set_id cs_1042. We need to inform user. The promotion is created as preview waiting approval. Should mention issues: price floor violation and overlap. We should report key numbers: preview_id pv_01m6cffgrwpj48v7g5xg1kae04, change_set_id cs_1042, valid_from 2026-11-06T11:00:00-05:00 to 2026-11-20T11:00:00-05:00, applies to… (+1,275자)

**답변 1**
> Promotion preview created and waiting for approval.
>
> * Name: $50 off $250+ Outerwear
> * Type: threshold → $50 off when subtotal ≥ $250
> * Discount layer: order_discount
> * Scope: categories `cat_outerwear` – 62 products in scope, subcategories included
> * Valid: 2026-11-06 11:00-05:00 to 2026-11-20 11:00-05:00  (2 weeks)
> * Member tier: everyone
> * Preview ID: pv_01m6cffgrwpj48v7g5xg1kae04
> * Change set: cs_1042 – needs approval
>
> Checks:
> * max_discount: passed – at most 20% on a $250 order
> * price_floor: **failed** – Seersucker overshirt would be $63.20, under the floor $66.70
> * promotion_overlap: **failed** – Denim bundle (everyone), Birthday coupon (member) and Gold tier 10% (gold) already give an order discount on outerwear in this period
> * discount_layers.max_total_discount_rate: passed
> * cost_share.sum_must_equal: passed – Store 100%
>
> The change is in one change set for a person to approve; it is not live yet.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (19, 23, 59 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-batch-guard · 2회차 · ✗ 실패

토큰 24,557 · 43.999초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 1,989토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 모델 판단(추론 필드): We need to create a promotion. Use promotion › promotion: create_promotion, end_promotion, get_promotion, list_active_promotions, pause_promotion, search_promotions, update_promotion We need to know parameters for create_promotion. Need to load function.
1. 모델 → **`a2api_load`** `` {"names":["create_promotion"]} ``
   ← 결과 31B: `` {"loaded":["create_promotion"]} ``
- 모델 판단(추론 필드): We need promotion for Outerwear, $50 off orders above $250, valid for 2 weeks. We need category id for Outerwear. Need to find category. Use list_categories? Need to load merchandising category functions. We need category_ids. Let's load list_categories. Also need valid_from and valid_through. Store time: Friday, November 6, 2026, 11:00 America/New_York. Valid for 2 weeks. So valid_from? Probably start now? Could be 2026-11-06T11:00? Or start at 00:00? Probably start now. Valid through 2 weeks later: 2026-11-20? 2 weeks = 14 days. From Nov 6 to Nov 20 inclusive? Let's compute: Nov 6 +14 days = Nov 20. If valid_from is 2026-11-06T11:00, valid_through is 2026-11-20T11:00? Or end of day? The sp… (+249자)
2. 모델 → **`a2api_load`** `` {"names":["list_categories"]} ``
   ← 결과 30B: `` {"loaded":["list_categories"]} ``
- 모델 판단(추론 필드): We need promotion for Outerwear, $50 off orders above $250, valid for 2 weeks. We need category id for Outerwear. Need to list categories. Use list_categories. Probably term_set? Could be standard or display. Outerwear likely category. We need scope_mode categories, category_ids. Need category id. Also promotion_type: threshold? $50 off orders above $250. That's threshold promotion with threshold benefit amount_off. promotion_type = threshold. discount_layer = order_discount? Probably order_discount. threshold value 250 currency USD. amount_off value 50 currency USD. threshold_benefit = amount_off. valid_from: store time Friday November 6 2026 11:00 America/New_York. Valid for 2 weeks. So va… (+947자)
3. 모델 → **`list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+2,400자) ``
- 모델 판단(추론 필드): We have category id cat_outerwear. Need promotion type threshold? $50 off orders above $250. That's threshold promotion with threshold benefit amount_off. Promotion type threshold, discount_layer order_discount? Probably order_discount. Scope_mode categories, category_ids [cat_outerwear]. Need valid_from and valid_through. Store time: Friday, November 6, 2026, 11:00 America/New_York. Valid for 2 weeks. So valid_from? Probably start now? Could be 2026-11-06T11:00? Or start at 00:00? Probably start now. Use valid_from = 2026-11-06T11:00? Might be better to start at 2026-11-06T00:00? The request says valid for 2 weeks. Could assume start today. Use valid_from = 2026-11-06T11:00? The format exam… (+1,072자)
4. 모델 → **`create_promotion`** `` {"name":"$50 off $250+ Outerwear","promotion_type":"threshold","discount_layer":"order_discount","amount_off":{"value":50,"currency":"USD"},"threshold":{"value":250,"currency":"USD"},"threshold_benefit":"amount_off","valid_from":"2026-11-06T11:00","valid_through":"2026-11-20T23:59","scope_mode":"categories","category_ids":["cat_outerwear"]} ``
   ← 결과 1,411B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6ckyh4ar3y7tkjgaa1ahvzk","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"$50 off $250+ Outerwear","promotion_type":"threshold","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-06T11:00:00-05:00","valid_through":"2026-11-20T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_outerwear"],"product_count":62},"amount_off":{"value":50.0,"currency":"USD"},"threshold":{"value":250.0,"currency":"USD"},"threshold_benefit":"amount_off"}}],"checks":[{"ru… (+809자) ``
- 모델 판단(추론 필드): Create promotion for Outerwear, $50 off orders above $250, valid for 2 weeks. We have created promotion preview. The tool returned succeeded with preview_id pv_01m6ckyh4ar3y7tkjgaa1ahvzk, change_set_id cs_1042. Checks: price_floor passed false: Seersucker overshirt would be $63.20 under floor $66.70. promotion_overlap passed false: Denim bundle, Birthday coupon and Gold tier 10% already give order discount on outerwear in this period. Needs approval true. We should inform user about creation preview, and note checks failures. The user asked create promotion. We have created preview. Should we mention needs approval? Yes. We might need to adjust? The user didn't ask to fix. We can present res… (+775자)

**답변 1**
> Created a preview for the Outerwear threshold promotion.
>
> * Name: **$50 off $250+ Outerwear**
> * Type: threshold → $50 off the order when subtotal ≥ $250
> * Discount layer: order_discount
> * Scope: categories `cat_outerwear` – 62 products in scope
> * Member tier: everyone
> * Valid: 2026-11-06T11:00:00-05:00 to 2026-11-20T23:59:00-05:00  ≈ 2 weeks from store time
> * Currency: USD
>
> Preview ID: `pv_01m6ckyh4ar3y7tkjgaa1ahvzk`
> Change set: `cs_1042` – waiting for approval. Approval reason: *New order discount for everyone, Nov 6–20*
>
> Checks on the preview:
> * max_discount: passed – at most 20% on a $250 order; limit 20%
> * price_floor: **failed** – Seersucker overshirt would be $63.20, under the floor $66.70
> * promotion_overlap: **failed** – Denim bundle (everyone), Birthday coupon (member) and Gold tier 10% (gold) already give an order discount on outerwear in this period
> * discount_layers.max_total_discount_rate: passed – combined discount stays under 50% (at most 20%)
> * cost_share.sum_must_equal: passed – Store 100%
>
> The promotion is not live yet; it is in change set `cs_1042` for a person to approve.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (19, 23 not shown)
(도구 정밀도 1.00, 재현율 1.00)
