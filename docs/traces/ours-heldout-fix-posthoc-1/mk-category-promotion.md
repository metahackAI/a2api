# mk-category-promotion — ours-heldout-fix-posthoc-1

[← 실행 묶음](README.md) · 세트 `held_out` · a-commerce `d86a1ff` · a2api `bb2cb7a`

**과업**

> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 필요한 도구: `create_promotion`
- 허용 도구: `list_categories`, `list_active_promotions`, `get_policy`
- 답에 있어야 할 사실: 2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store time

### a2api-acom · 1회차 · ✓ 통과

토큰 34,924 · 38.803초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 6,020토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

1. 모델 → **`a2api_search`** `` {"query":"list categories"} ``
   ← 결과 367B: `` {"selected":[{"name":"acom_list_categories","id":"acom.list_categories"},{"name":"acom_get_contract","id":"acom.get_contract"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_list_faqs","id":"acom.list_faqs"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`acom_list_categories`** `` {} ``
   ← 결과 3,713B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
3. 모델 → **`acom_create_promotion`** `` {"name":"$50 off Outerwear orders $250+","promotion_type":"threshold","discount_layer":"order_discount","amount_off":{"value":50,"currency":"USD"},"threshold":{"value":250,"currency":"USD"},"threshold_benefit":"amount_off","valid_from":"2026-11-06T00:00","valid_through":"2026-11-19T23:59","scope_mode":"categories","category_ids":["cat_outerwear"]} ``
   ← 결과 1,418B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6bezy088bm9gj81bn6k1wpd","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"$50 off Outerwear orders $250+","promotion_type":"threshold","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-06T00:00:00-05:00","valid_through":"2026-11-19T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_outerwear"],"product_count":62},"amount_off":{"value":50.0,"currency":"USD"},"threshold":{"value":250.0,"currency":"USD"},"threshold_benefit":"amount_off"}}],"checks… (+816자) ``

**답변 1**
> Created a preview for the Outerwear threshold promotion.
>
> * Name: $50 off Outerwear orders $250+
> * Type: threshold → $50 off when subtotal ≥ $250
> * Scope: category cat_outerwear (62 products, subcategories included)
> * Discount layer: order_discount
> * Valid: 2026-11-06 00:00 to 2026-11-19 23:59 America/New_York (2 weeks)
> * Member tier: everyone
>
> Preview ID: pv_01m6bezy088bm9gj81bn6k1wpd
> Change set: cs_1042 — waiting for approval.
>
> Checks:
> * max_discount: passed (≤20% on a $250 order)
> * price_floor: failed — Seersucker overshirt would be $63.20, under floor $66.70
> * promotion_overlap: failed — Denim bundle (everyone), Birthday coupon (member) and Gold tier 10% (gold) already give an order discount on outerwear in this period
> * discount_layers.max_total_discount_rate: passed
> * cost_share.sum_must_equal: passed
>
> The promotion is not live until approved.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom · 2회차 · ✓ 통과

토큰 34,667 · 29.48초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 6,020토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

1. 모델 → **`a2api_search`** `` {"query":"list categories"} ``
   ← 결과 367B: `` {"selected":[{"name":"acom_list_categories","id":"acom.list_categories"},{"name":"acom_get_contract","id":"acom.get_contract"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_set_sale_prices","id":"acom.set_sale_prices"},{"name":"acom_list_faqs","id":"acom.list_faqs"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`acom_list_categories`** `` {} ``
   ← 결과 3,713B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
3. 모델 → **`acom_create_promotion`** `` {"name":"$50 off Outerwear $250+","promotion_type":"threshold","discount_layer":"order_discount","amount_off":{"value":50,"currency":"USD"},"threshold":{"value":250,"currency":"USD"},"threshold_benefit":"amount_off","valid_from":"2026-11-06T00:00","valid_through":"2026-11-19T23:59","scope_mode":"categories","category_ids":["cat_outerwear"]} ``
   ← 결과 1,411B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6bjbsx5s8tzrrfkpmnn9b8k","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"$50 off Outerwear $250+","promotion_type":"threshold","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-06T00:00:00-05:00","valid_through":"2026-11-19T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_outerwear"],"product_count":62},"amount_off":{"value":50.0,"currency":"USD"},"threshold":{"value":250.0,"currency":"USD"},"threshold_benefit":"amount_off"}}],"checks":[{"ru… (+809자) ``

**답변 1**
> Created a preview for the Outerwear threshold promotion.
>
> Name: $50 off Outerwear $250+
> Type: threshold → $50 off when subtotal ≥ $250
> Scope: categories cat_outerwear (62 products, subcategories included)
> Period: 2026-11-06 00:00 to 2026-11-19 23:59 America/New_York (2 weeks)
> Member tier: everyone
> Discount layer: order_discount
>
> Preview ID: pv_01m6bjbsx5s8tzrrfkpmnn9b8k
> Change set: cs_1042 — needs a person's approval before it goes live.
>
> Checks:
> • max_discount: passed (at most 20% on a $250 order; limit 20%)
> • price_floor: failed — Seersucker overshirt would be $63.20, under the floor $66.70
> • promotion_overlap: failed — Denim bundle (everyone), Birthday coupon (member) and Gold tier 10% (gold) already give an order discount on outerwear in this period
> • discount_layers.max_total_discount_rate: passed (combined discount stays under 50%, at most 20%)
> • cost_share.sum_must_equal: passed (store 100%)
>
> The promotion is staged and waiting for approval.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-norelated · 1회차 · ✗ 실패

토큰 23,837 · 44.539초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 1,989토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

1. 모델 → **`a2api_load`** `` {"names":["create_promotion"]} ``
   ← 결과 31B: `` {"loaded":["create_promotion"]} ``
2. 모델 → **`a2api_load`** `` {"names":["list_categories"]} ``
   ← 결과 30B: `` {"loaded":["list_categories"]} ``
3. 모델 → **`list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
4. 모델 → **`create_promotion`** `` {"name":"$50 off Outerwear orders $250+","promotion_type":"threshold","discount_layer":"order_discount","threshold":{"value":250,"currency":"USD"},"threshold_benefit":"amount_off","amount_off":{"value":50,"currency":"USD"},"valid_from":"2026-11-06T00:00","valid_through":"2026-11-19T23:59","scope_mode":"categories","category_ids":["cat_outerwear"]} ``
   ← 결과 1,418B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6bewcq1kcrc2f1jzj1r6snq","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"$50 off Outerwear orders $250+","promotion_type":"threshold","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-06T00:00:00-05:00","valid_through":"2026-11-19T23:59:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_outerwear"],"product_count":62},"amount_off":{"value":50.0,"currency":"USD"},"threshold":{"value":250.0,"currency":"USD"},"threshold_benefit":"amount_off"}}],"checks… (+816자) ``

**답변 1**
> Created a preview for the Outerwear threshold promotion.
>
> * Name: **$50 off Outerwear orders $250+**
> * Type: threshold → amount_off
> * Discount layer: order_discount
> * Scope: categories `cat_outerwear` – Outerwear
>   * Applies to 62 products in the category tree
> * Threshold: $250.00 USD
> * Benefit: $50.00 USD off the order
> * Valid: 2026-11-06T00:00:00-05:00 to 2026-11-19T23:59:00-05:00  – 2 weeks from store time
> * Member tier: everyone
>
> Preview ID: `pv_01m6bewcq1kcrc2f1jzj1r6snq`
> Change set: `cs_1042` – waiting for approval. Approval reason: *New order discount for everyone, Nov 6–19*
>
> Checks from the preview:
> * max_discount: passed – at most 20% on a $250 order; limit 20%
> * price_floor: **failed** – Seersucker overshirt would be $63.20, under the floor $66.70
> * promotion_overlap: **failed** – Denim bundle (everyone), Birthday coupon (member) and Gold tier 10% (gold) already give an order discount on outerwear in this period
> * discount_layers.max_total_discount_rate: passed – combined discount stays under 50% (at most 20%)
> * cost_share.sum_must_equal: passed – Store 100%
>
> The promotion is not live yet; it is in a change set that needs a person’s approval before it can be published.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (23 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-norelated · 2회차 · ✗ 실패

토큰 23,420 · 34.936초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 1,989토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

1. 모델 → **`a2api_load`** `` {"names":["create_promotion"]} ``
   ← 결과 31B: `` {"loaded":["create_promotion"]} ``
2. 모델 → **`a2api_load`** `` {"names":["list_categories"]} ``
   ← 결과 30B: `` {"loaded":["list_categories"]} ``
3. 모델 → **`list_categories`** `` {} ``
   ← 결과 3,713B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
4. 모델 → **`create_promotion`** `` {"name":"$50 off $250+ Outerwear","promotion_type":"threshold","discount_layer":"order_discount","amount_off":{"value":50,"currency":"USD"},"threshold":{"value":250,"currency":"USD"},"threshold_benefit":"amount_off","valid_from":"2026-11-06T11:00","valid_through":"2026-11-20T11:00","scope_mode":"categories","category_ids":["cat_outerwear"]} ``
   ← 결과 1,411B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6bjd3ear5zskfyp2tksgxmn","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"$50 off $250+ Outerwear","promotion_type":"threshold","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-06T11:00:00-05:00","valid_through":"2026-11-20T11:00:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_outerwear"],"product_count":62},"amount_off":{"value":50.0,"currency":"USD"},"threshold":{"value":250.0,"currency":"USD"},"threshold_benefit":"amount_off"}}],"checks":[{"ru… (+809자) ``

**답변 1**
> Created a preview for the Outerwear threshold promotion.
>
> * Name: **$50 off $250+ Outerwear**
> * Type: threshold → $50 off when subtotal ≥ $250
> * Discount layer: order_discount
> * Scope: categories `cat_outerwear` – applies to 62 products
> * Valid: 2026-11-06 11:00 to 2026-11-20 11:00 America/New_York  (2 weeks)
> * Member tier: everyone
>
> Preview ID: pv_01m6bjd3ear5zskfyp2tksgxmn
> Change set: cs_1042 – **needs approval** before it goes live.
>
> Checks:
> * max_discount: passed – at most 20% on a $250 order
> * price_floor: **failed** – Seersucker overshirt would be $63.20, under floor $66.70
> * promotion_overlap: **failed** – Denim bundle (everyone), Birthday coupon (member) and Gold tier 10% (gold) already give an order discount on outerwear in this period
> * discount_layers.max_total_discount_rate: passed
> * cost_share.sum_must_equal: passed – Store 100%
>
> The promotion is staged and waiting for a person to approve.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (19, 23, 59 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-batch · 1회차 · ✗ 실패

토큰 24,501 · 50.093초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 1,989토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

1. 모델 → **`a2api_load`** `` {"names":["create_promotion"]} ``
   ← 결과 31B: `` {"loaded":["create_promotion"]} ``
2. 모델 → **`a2api_load`** `` {"names":["list_categories"]} ``
   ← 결과 30B: `` {"loaded":["list_categories"]} ``
3. 모델 → **`list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
4. 모델 → **`create_promotion`** `` {"name":"$50 off $250+ Outerwear","promotion_type":"threshold","discount_layer":"order_discount","amount_off":{"value":50,"currency":"USD"},"threshold":{"value":250,"currency":"USD"},"threshold_benefit":"amount_off","valid_from":"2026-11-06T11:00","valid_through":"2026-11-20T11:00","scope_mode":"categories","category_ids":["cat_outerwear"]} ``
   ← 결과 1,411B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6bey80cve4ppjfzvmh19eas","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"$50 off $250+ Outerwear","promotion_type":"threshold","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-06T11:00:00-05:00","valid_through":"2026-11-20T11:00:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_outerwear"],"product_count":62},"amount_off":{"value":50.0,"currency":"USD"},"threshold":{"value":250.0,"currency":"USD"},"threshold_benefit":"amount_off"}}],"checks":[{"ru… (+809자) ``

**답변 1**
> Created a preview for the Outerwear threshold promotion.
>
> * Name: **$50 off $250+ Outerwear**
> * Type: threshold → $50 off when subtotal ≥ $250
> * Discount layer: order_discount
> * Scope: categories `cat_outerwear` – 62 products in scope
> * Valid: 2026-11-06T11:00:00-05:00 → 2026-11-20T11:00:00-05:00  (2 weeks from store time)
> * Member tier: everyone
> * Preview ID: `pv_01m6bey80cve4ppjfzvmh19eas`
> * Change set: `cs_1042` – waiting for approval
>
> Checks:
> * max_discount: passed – at most 20% on a $250 order
> * price_floor: **failed** – Seersucker overshirt would be $63.20, under the floor $66.70
> * promotion_overlap: **failed** – Denim bundle (everyone), Birthday coupon (member) and Gold tier 10% (gold) already give an order discount on outerwear in this period
> * discount_layers.max_total_discount_rate: passed
> * cost_share.sum_must_equal: passed – Store 100%
>
> The change is a preview only and needs a person's approval before it can be published.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (6, 19, 23, 59 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-batch · 2회차 · ✗ 실패

토큰 21,160 · 48.059초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 1,989토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

1. 모델 → **`a2api_load`** `` {"names":["promotion › promotion: create_promotion","merchandising › category: list_categories","merchandising › category: get_category"]} ``
   ← 결과 64B: `` {"loaded":["create_promotion","list_categories","get_category"]} ``
2. 모델 → **`list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
3. 모델 → **`create_promotion`** `` {"name":"$50 off $250+ Outerwear","promotion_type":"threshold","discount_layer":"order_discount","amount_off":{"value":50,"currency":"USD"},"threshold":{"value":250,"currency":"USD"},"threshold_benefit":"amount_off","valid_from":"2026-11-06T11:00","valid_through":"2026-11-20T11:00","scope_mode":"categories","category_ids":["cat_outerwear"]} ``
   ← 결과 1,411B: `` {"status":"succeeded","data":{"preview_id":"pv_01m6bja9vedh7mp5vn258z51x8","expires_at":null,"changes":[{"op":"create","entity":"promotion","id":null,"to":{"name":"$50 off $250+ Outerwear","promotion_type":"threshold","discount_layer":"order_discount","valid_for_member_tier":"everyone","valid_from":"2026-11-06T11:00:00-05:00","valid_through":"2026-11-20T11:00:00-05:00","applies_to":{"scope":"categories","category_ids":["cat_outerwear"],"product_count":62},"amount_off":{"value":50.0,"currency":"USD"},"threshold":{"value":250.0,"currency":"USD"},"threshold_benefit":"amount_off"}}],"checks":[{"ru… (+809자) ``

**답변 1**
> Promotion preview created and waiting for approval.
>
> * Change set: **cs_1042** – preview **pv_01m6bja9vedh7mp5vn258z51x8**
> * Name: $50 off $250+ Outerwear
> * Type: threshold – $50 off order, discount_layer order_discount
> * Scope: categories `cat_outerwear` – Outerwear
>   * Applies to 62 products in the category tree
> * Valid: 2026-11-06T11:00:00-05:00 → 2026-11-20T11:00:00-05:00  ≈ 2 weeks from store time
> * Member tier: everyone
> * Threshold: $250.00 USD, benefit: amount_off $50.00 USD
>
> Checks on the preview:
> * max_discount: passed – at most 20% on a $250 order; limit 20%
> * price_floor: **failed** – Seersucker overshirt would be $63.20, under the floor $66.70
> * promotion_overlap: **failed** – Denim bundle (everyone), Birthday coupon (member) and Gold tier 10% (gold) already give an order discount on outerwear in this period
> * discount_layers.max_total_discount_rate: passed – combined discount stays under 50% (at most 20%)
> * cost_share.sum_must_equal: passed – Store 100%
>
> The promotion is not live yet; it needs a person’s approval in change set cs_1042.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (6, 19, 23, 59 not shown)
(도구 정밀도 1.00, 재현율 1.00)
