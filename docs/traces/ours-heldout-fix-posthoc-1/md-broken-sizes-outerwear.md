# md-broken-sizes-outerwear — ours-heldout-fix-posthoc-1

[← 실행 묶음](README.md) · 세트 `held_out` · a-commerce `d86a1ff` · a2api `bb2cb7a`

**과업**

> which outerwear styles have broken sizes right now?

- 필요한 도구: `search_products`
- 허용 도구: `get_inventory`, `list_categories`
- 답에 있어야 할 사실: 5 of the 62 outerwear products have a sold-out size
- 답에 있어야 할 사실: Cotton chore coat, Light rain parka and Denim jacket are out in M and L; Poplin shacket is out in M; Cotton overshirt is out in XL
- 부르면 안 됨: set_variant_stock

### a2api-acom · 1회차 · E MODEL_CALL_LIMIT

토큰 126,932 · 75.643초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 3,359토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> which outerwear styles have broken sizes right now?

1. 모델 → **`a2api_search`** `` {"query":"search products outerwear"} ``
   ← 결과 393B: `` {"selected":[{"name":"acom_search_product_groups","id":"acom.search_product_groups"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_autocomplete","id":"acom.autocomplete"},{"name":"acom_get_index_status","id":"acom.get_index_status"},{"name":"acom_create_curation","id":"acom.create_curation"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`acom_search_product_groups`** `` {"query":"outerwear","limit":100} ``
   ← 결과 3,243B: `` {"status":"succeeded","data":{"items":[{"id":"prd_outerwear_01","@type":"ProductGroup","name":"Waxed cotton duffle coat","brand_id":"brn_ridgeline","category_id":"cat_outerwear","approval_status":"active","varies_by":["color","size"],"image":"/media/products/prd_outerwear_01-56f79d3b.webp","price":289.0,"price_currency":"USD","inventory_level":24,"availability":"in_stock","variant_count":10,"release_date":"2026-08-25","cost":134.5},{"id":"prd_outerwear_05","@type":"ProductGroup","name":"Waxed cotton shell jacket","brand_id":"brn_northwind","category_id":"cat_outerwear","approval_status":"activ… (+900자) ``
3. 모델 → **`acom_search_products`** `` {"category_id":"cat_outerwear","limit":100} ``
   ← 결과 4,464B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_wool_overcoat-b50a91c0.webp","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"ava… (+900자) ``
4. 모델 → **`acom_search_products`** `` {"category_id":"cat_outerwear","limit":100,"cursor":"o20"} ``
   ← 결과 2,909B: `` {"status":"succeeded","data":{"items":[{"id":"prd_summer_outerwear_17","name":"Cotton coach jacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_summer_outerwear_17-691ce929.webp","price":89.0,"price_currency":"USD","member_price":null,"cost":40.05,"inventory_level":80,"availability":"in_stock","has_variant":[{"variant_id":"var_summer_outerwear_17_xs_slate","sku":"so-17-slate-xs","size":"XS","color":"Slate","inventory_level":11,"availability":"in_stock"},{"variant_id":"var_summer_outerwear_17_s_slate","sku":"so-17-slate-s","size":"S","color":"Sla… (+900자) ``
5. 모델 → **`acom_search_products`** `` {"category_id":"cat_outerwear","availability":["out_of_stock"],"limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
6. 모델 → **`acom_search_products`** `` {"category_id":"cat_outerwear","limit":100,"cursor":"o40"} ``
   ← 결과 3,615B: `` {"status":"succeeded","data":{"items":[{"id":"prd_summer_outerwear_26","name":"Twill shirt jacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_summer_outerwear_26-9fa9a1eb.webp","price":109.0,"price_currency":"USD","member_price":null,"cost":49.05,"inventory_level":55,"availability":"in_stock","has_variant":[{"variant_id":"var_summer_outerwear_26_xs_black","sku":"so-26-black-xs","size":"XS","color":"Black","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_summer_outerwear_26_s_black","sku":"so-26-black-s","size":"S","color":"Blac… (+900자) ``
7. 모델 → **`acom_search_products`** `` {"category_id":"cat_outerwear","limit":100,"cursor":"o60"} ``
   ← 결과 3,508B: `` {"status":"succeeded","data":{"items":[{"id":"prd_outerwear_15","name":"Down peacoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_outerwear_15-ab58f1c9.webp","price":109.0,"price_currency":"USD","member_price":null,"cost":53.14,"inventory_level":25,"availability":"in_stock","has_variant":[{"variant_id":"var_outerwear_15_xs_clay","sku":"outerwear-15-clay-xs","size":"XS","color":"Clay","inventory_level":4,"availability":"in_stock"},{"variant_id":"var_outerwear_15_s_clay","sku":"outerwear-15-clay-s","size":"S","color":"Clay","inventory_level":3,"availabil… (+900자) ``
8. 모델 → **`acom_search_product_groups`** `` {"category_id":"cat_outerwear","limit":100} ``
   ← 결과 2,915B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","@type":"ProductGroup","name":"Wool overcoat","brand_id":"brn_northwind","category_id":"cat_outerwear","approval_status":"active","varies_by":["color","size"],"image":"/media/products/prd_wool_overcoat-b50a91c0.webp","price":289.0,"price_currency":"USD","inventory_level":24,"availability":"in_stock","variant_count":4,"release_date":"2026-09-15","cost":120.0},{"id":"prd_outerwear_01","@type":"ProductGroup","name":"Waxed cotton duffle coat","brand_id":"brn_ridgeline","category_id":"cat_outerwear","approval_status":"active","varies_… (+900자) ``
9. 모델 → **`acom_search_products`** `` {"category_id":"cat_outerwear","availability":["out_of_stock","back_order","discontinued"],"limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
10. 모델 → **`acom_search_products`** `` {"category_id":"cat_outerwear","limit":100,"cursor":"o20"} ``
   ← 결과 3,017B: `` {"status":"succeeded","data":{"items":[{"id":"prd_summer_outerwear_17","name":"Cotton coach jacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_summer_outerwear_17-691ce929.webp","price":89.0,"price_currency":"USD","member_price":null,"cost":40.05,"inventory_level":80,"availability":"in_stock","has_variant":[{"variant_id":"var_summer_outerwear_17_xs_slate","sku":"so-17-slate-xs","size":"XS","color":"Slate","inventory_level":11,"availability":"in_stock"},{"variant_id":"var_summer_outerwear_17_s_slate","sku":"so-17-slate-s","size":"S","color":"Sla… (+900자) ``
11. 모델 → **`a2api_search`** `` {"query":"broken sizes inventory variant"} ``
   ← 결과 371B: `` {"selected":[{"name":"acom_set_variants","id":"acom.set_variants"},{"name":"acom_get_inventory","id":"acom.get_inventory"},{"name":"acom_create_product","id":"acom.create_product"},{"name":"acom_update_product","id":"acom.update_product"},{"name":"acom_suggest_reorder","id":"acom.suggest_reorder"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
12. 모델 → **`acom_get_inventory`** `` {"product_id":"prd_outerwear_01"} ``
   ← 결과 2,109B: `` {"status":"succeeded","data":{"product_id":"prd_outerwear_01","inventory_level":24,"availability":"in_stock","variants":[{"variant_id":"var_outerwear_01_xs_stone","sku":"outerwear-01-stone-xs","size":"XS","color":"Stone","inventory_level":4,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_outerwear_01_s_stone","sku":"outerwear-01-stone-s","size":"S","color":"Stone","inventory_level":1,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_outerwear_01_m_stone","sku":"outerwear-01-stone-m","size":"… (+900자) ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "5 of the 62 outerwear products have a sold-out size" (5, 62 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.80, 재현율 1.00)

### a2api-acom · 2회차 · E MODEL_CALL_LIMIT

토큰 126,932 · 75.64초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 3,359토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> which outerwear styles have broken sizes right now?

1. 모델 → **`a2api_search`** `` {"query":"search products outerwear"} ``
   ← 결과 393B: `` {"selected":[{"name":"acom_search_product_groups","id":"acom.search_product_groups"},{"name":"acom_search_products","id":"acom.search_products"},{"name":"acom_autocomplete","id":"acom.autocomplete"},{"name":"acom_get_index_status","id":"acom.get_index_status"},{"name":"acom_create_curation","id":"acom.create_curation"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
2. 모델 → **`acom_search_product_groups`** `` {"query":"outerwear","limit":100} ``
   ← 결과 3,243B: `` {"status":"succeeded","data":{"items":[{"id":"prd_outerwear_01","@type":"ProductGroup","name":"Waxed cotton duffle coat","brand_id":"brn_ridgeline","category_id":"cat_outerwear","approval_status":"active","varies_by":["color","size"],"image":"/media/products/prd_outerwear_01-56f79d3b.webp","price":289.0,"price_currency":"USD","inventory_level":24,"availability":"in_stock","variant_count":10,"release_date":"2026-08-25","cost":134.5},{"id":"prd_outerwear_05","@type":"ProductGroup","name":"Waxed cotton shell jacket","brand_id":"brn_northwind","category_id":"cat_outerwear","approval_status":"activ… (+900자) ``
3. 모델 → **`acom_search_products`** `` {"category_id":"cat_outerwear","limit":100} ``
   ← 결과 4,464B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_wool_overcoat-b50a91c0.webp","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"ava… (+900자) ``
4. 모델 → **`acom_search_products`** `` {"category_id":"cat_outerwear","limit":100,"cursor":"o20"} ``
   ← 결과 2,909B: `` {"status":"succeeded","data":{"items":[{"id":"prd_summer_outerwear_17","name":"Cotton coach jacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_summer_outerwear_17-691ce929.webp","price":89.0,"price_currency":"USD","member_price":null,"cost":40.05,"inventory_level":80,"availability":"in_stock","has_variant":[{"variant_id":"var_summer_outerwear_17_xs_slate","sku":"so-17-slate-xs","size":"XS","color":"Slate","inventory_level":11,"availability":"in_stock"},{"variant_id":"var_summer_outerwear_17_s_slate","sku":"so-17-slate-s","size":"S","color":"Sla… (+900자) ``
5. 모델 → **`acom_search_products`** `` {"category_id":"cat_outerwear","availability":["out_of_stock"],"limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
6. 모델 → **`acom_search_products`** `` {"category_id":"cat_outerwear","limit":100,"cursor":"o40"} ``
   ← 결과 3,615B: `` {"status":"succeeded","data":{"items":[{"id":"prd_summer_outerwear_26","name":"Twill shirt jacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_summer_outerwear_26-9fa9a1eb.webp","price":109.0,"price_currency":"USD","member_price":null,"cost":49.05,"inventory_level":55,"availability":"in_stock","has_variant":[{"variant_id":"var_summer_outerwear_26_xs_black","sku":"so-26-black-xs","size":"XS","color":"Black","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_summer_outerwear_26_s_black","sku":"so-26-black-s","size":"S","color":"Blac… (+900자) ``
7. 모델 → **`acom_search_products`** `` {"category_id":"cat_outerwear","limit":100,"cursor":"o60"} ``
   ← 결과 3,508B: `` {"status":"succeeded","data":{"items":[{"id":"prd_outerwear_15","name":"Down peacoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_outerwear_15-ab58f1c9.webp","price":109.0,"price_currency":"USD","member_price":null,"cost":53.14,"inventory_level":25,"availability":"in_stock","has_variant":[{"variant_id":"var_outerwear_15_xs_clay","sku":"outerwear-15-clay-xs","size":"XS","color":"Clay","inventory_level":4,"availability":"in_stock"},{"variant_id":"var_outerwear_15_s_clay","sku":"outerwear-15-clay-s","size":"S","color":"Clay","inventory_level":3,"availabil… (+900자) ``
8. 모델 → **`acom_search_product_groups`** `` {"category_id":"cat_outerwear","limit":100} ``
   ← 결과 2,915B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","@type":"ProductGroup","name":"Wool overcoat","brand_id":"brn_northwind","category_id":"cat_outerwear","approval_status":"active","varies_by":["color","size"],"image":"/media/products/prd_wool_overcoat-b50a91c0.webp","price":289.0,"price_currency":"USD","inventory_level":24,"availability":"in_stock","variant_count":4,"release_date":"2026-09-15","cost":120.0},{"id":"prd_outerwear_01","@type":"ProductGroup","name":"Waxed cotton duffle coat","brand_id":"brn_ridgeline","category_id":"cat_outerwear","approval_status":"active","varies_… (+900자) ``
9. 모델 → **`acom_search_products`** `` {"category_id":"cat_outerwear","availability":["out_of_stock","back_order","discontinued"],"limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
10. 모델 → **`acom_search_products`** `` {"category_id":"cat_outerwear","limit":100,"cursor":"o20"} ``
   ← 결과 3,017B: `` {"status":"succeeded","data":{"items":[{"id":"prd_summer_outerwear_17","name":"Cotton coach jacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_summer_outerwear_17-691ce929.webp","price":89.0,"price_currency":"USD","member_price":null,"cost":40.05,"inventory_level":80,"availability":"in_stock","has_variant":[{"variant_id":"var_summer_outerwear_17_xs_slate","sku":"so-17-slate-xs","size":"XS","color":"Slate","inventory_level":11,"availability":"in_stock"},{"variant_id":"var_summer_outerwear_17_s_slate","sku":"so-17-slate-s","size":"S","color":"Sla… (+900자) ``
11. 모델 → **`a2api_search`** `` {"query":"broken sizes inventory variant"} ``
   ← 결과 371B: `` {"selected":[{"name":"acom_set_variants","id":"acom.set_variants"},{"name":"acom_get_inventory","id":"acom.get_inventory"},{"name":"acom_create_product","id":"acom.create_product"},{"name":"acom_update_product","id":"acom.update_product"},{"name":"acom_suggest_reorder","id":"acom.suggest_reorder"}],"moreAvailable":true,"page":1,"pageLimitReached":false,"progress":true} ``
12. 모델 → **`acom_get_inventory`** `` {"product_id":"prd_outerwear_01"} ``
   ← 결과 2,109B: `` {"status":"succeeded","data":{"product_id":"prd_outerwear_01","inventory_level":24,"availability":"in_stock","variants":[{"variant_id":"var_outerwear_01_xs_stone","sku":"outerwear-01-stone-xs","size":"XS","color":"Stone","inventory_level":4,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_outerwear_01_s_stone","sku":"outerwear-01-stone-s","size":"S","color":"Stone","inventory_level":1,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_outerwear_01_m_stone","sku":"outerwear-01-stone-m","size":"… (+900자) ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "5 of the 62 outerwear products have a sold-out size" (5, 62 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.80, 재현율 1.00)

### a2api-acom-names-norelated · 1회차 · E MODEL_CALL_LIMIT

토큰 103,118 · 104.221초 · 모델 호출 12회 · 도구 호출 17회 · 첫 요청 프롬프트 1,979토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> which outerwear styles have broken sizes right now?

1. 모델 → **`a2api_load`** `` {"names":["list_categories","search_products","get_inventory"]} ``
   ← 결과 64B: `` {"loaded":["list_categories","search_products","get_inventory"]} ``
2. 모델 → **`list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
3. 모델 → **`list_categories`** `` {"parent_id":"cat_outerwear","term_set":"standard"} ``
   ← 결과 220B: `` {"status":"succeeded","data":{"items":[{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true}],"total":1}} ``
4. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","limit":100} ``
   ← 결과 4,464B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_wool_overcoat-b50a91c0.webp","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"ava… (+900자) ``
5. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","availability":["out_of_stock"],"limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
6. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","limit":100,"sort":"newest"} ``
   ← 결과 4,464B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_wool_overcoat-b50a91c0.webp","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"ava… (+900자) ``
7. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","limit":100,"fields":["id","name"]} ``
   ← 결과 3,602B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat"},{"id":"prd_outerwear_01","name":"Waxed cotton duffle coat"},{"id":"prd_outerwear_05","name":"Waxed cotton shell jacket"},{"id":"prd_summer_outerwear_13","name":"Poplin shacket"},{"id":"prd_summer_outerwear_22","name":"Seersucker shacket"},{"id":"prd_summer_outerwear_20","name":"Cotton anorak"},{"id":"prd_summer_outerwear_01","name":"Seersucker cagoule"},{"id":"prd_outerwear_04","name":"Melton parka"},{"id":"prd_summer_outerwear_06","name":"Poplin harrington"},{"id":"prd_summer_outerwear_10","name":"Nylon g… (+900자) ``
8. 모델 → **`get_inventory`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 937B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","inventory_level":24,"availability":"in_stock","variants":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_wool_overcoat_l_charcoal","sku":"wo-charcoal-l","size":"L","c… (+337자) ``
9. 모델 → **`get_inventory`** `` {"product_id":"prd_outerwear_01"} ``
   ← 결과 2,109B: `` {"status":"succeeded","data":{"product_id":"prd_outerwear_01","inventory_level":24,"availability":"in_stock","variants":[{"variant_id":"var_outerwear_01_xs_stone","sku":"outerwear-01-stone-xs","size":"XS","color":"Stone","inventory_level":4,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_outerwear_01_s_stone","sku":"outerwear-01-stone-s","size":"S","color":"Stone","inventory_level":1,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_outerwear_01_m_stone","sku":"outerwear-01-stone-m","size":"… (+900자) ``
10. 모델 → **`get_inventory`** `` {"product_id":"prd_outerwear_05"} ``
   ← 결과 2,139B: `` {"status":"succeeded","data":{"product_id":"prd_outerwear_05","inventory_level":25,"availability":"in_stock","variants":[{"variant_id":"var_outerwear_05_xs_black","sku":"outerwear-05-black-xs","size":"XS","color":"Black","inventory_level":1,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_outerwear_05_s_black","sku":"outerwear-05-black-s","size":"S","color":"Black","inventory_level":3,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_outerwear_05_m_black","sku":"outerwear-05-black-m","size":"… (+900자) ``
11. 모델 → **`get_inventory`** `` {"product_id":"prd_summer_outerwear_13"} ``
   ← 결과 3,121B: `` {"status":"succeeded","data":{"product_id":"prd_summer_outerwear_13","inventory_level":14,"availability":"in_stock","variants":[{"variant_id":"var_summer_outerwear_13_xs_olive","sku":"so-13-olive-xs","size":"XS","color":"Olive","inventory_level":1,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_summer_outerwear_13_s_olive","sku":"so-13-olive-s","size":"S","color":"Olive","inventory_level":1,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_summer_outerwear_13_m_olive","sku":"so-13-olive-m","… (+900자) ``
12. 모델 → **`get_inventory`** `` {"product_id":"prd_summer_outerwear_22"} ``
   ← 결과 3,102B: `` {"status":"succeeded","data":{"product_id":"prd_summer_outerwear_22","inventory_level":36,"availability":"in_stock","variants":[{"variant_id":"var_summer_outerwear_22_xs_rust","sku":"so-22-rust-xs","size":"XS","color":"Rust","inventory_level":2,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_summer_outerwear_22_s_rust","sku":"so-22-rust-s","size":"S","color":"Rust","inventory_level":3,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_summer_outerwear_22_m_rust","sku":"so-22-rust-m","size":"M… (+900자) ``
13. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","limit":20,"sort":"inventory_level"} ``
   ← 결과 1,798B: `` {"status":"succeeded","data":{"items":[{"id":"prd_rain_parka","name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_rain_parka-01f49e29.webp","price":118.0,"price_currency":"USD","member_price":null,"cost":50.0,"inventory_level":4,"availability":"in_stock","has_variant":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"availability":"out_of_sto… (+900자) ``
14. 모델 → **`get_inventory`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 893B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","inventory_level":4,"availability":"in_stock","variants":[{"variant_id":"var_rain_parka_s_stone","sku":"rp-stone-s","size":"S","color":"Stone","inventory_level":2,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_rain_parka_m_stone","sku":"rp-stone-m","size":"M","color":"Stone","inventory_level":0,"acom:safety_stock":2,"acom:managed":true,"availability":"out_of_stock","on_order":0},{"variant_id":"var_rain_parka_l_stone","sku":"rp-stone-l","size":"L","color":"Stone","inventory_level":0… (+293자) ``
15. 모델 → **`get_inventory`** `` {"product_id":"prd_chore_coat"} ``
   ← 결과 893B: `` {"status":"succeeded","data":{"product_id":"prd_chore_coat","inventory_level":7,"availability":"in_stock","variants":[{"variant_id":"var_chore_coat_s_olive","sku":"cc-olive-s","size":"S","color":"Olive","inventory_level":3,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_chore_coat_m_olive","sku":"cc-olive-m","size":"M","color":"Olive","inventory_level":0,"acom:safety_stock":2,"acom:managed":true,"availability":"out_of_stock","on_order":0},{"variant_id":"var_chore_coat_l_olive","sku":"cc-olive-l","size":"L","color":"Olive","inventory_level":0… (+293자) ``
16. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","limit":62,"fields":["id","name"]} ``
   ← 결과 3,602B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat"},{"id":"prd_outerwear_01","name":"Waxed cotton duffle coat"},{"id":"prd_outerwear_05","name":"Waxed cotton shell jacket"},{"id":"prd_summer_outerwear_13","name":"Poplin shacket"},{"id":"prd_summer_outerwear_22","name":"Seersucker shacket"},{"id":"prd_summer_outerwear_20","name":"Cotton anorak"},{"id":"prd_summer_outerwear_01","name":"Seersucker cagoule"},{"id":"prd_outerwear_04","name":"Melton parka"},{"id":"prd_summer_outerwear_06","name":"Poplin harrington"},{"id":"prd_summer_outerwear_10","name":"Nylon g… (+900자) ``
17. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","max_inventory_level":9,"limit":100} ``
   ← 결과 1,730B: `` {"status":"succeeded","data":{"items":[{"id":"prd_chore_coat","name":"Cotton chore coat","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_chore_coat-51cdcf8e.webp","price":142.0,"price_currency":"USD","member_price":null,"cost":60.0,"inventory_level":7,"availability":"in_stock","has_variant":[{"variant_id":"var_chore_coat_s_olive","sku":"cc-olive-s","size":"S","color":"Olive","inventory_level":3,"availability":"in_stock"},{"variant_id":"var_chore_coat_m_olive","sku":"cc-olive-m","size":"M","color":"Olive","inventory_level":0,"availability":"out_of_st… (+900자) ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "5 of the 62 outerwear products have a sold-out size" (5, 62 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-norelated · 2회차 · E MODEL_CALL_LIMIT

토큰 87,100 · 89.586초 · 모델 호출 12회 · 도구 호출 12회 · 첫 요청 프롬프트 1,979토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> which outerwear styles have broken sizes right now?

1. 모델 → **`a2api_load`** `` {"names":["merchandising.category.list_categories","merchandising.category.get_category","search.product.search_products","catalog.product.get_product","catalog.inventory.get_inventory"]} ``
   ← 결과 93B: `` {"loaded":["list_categories","get_category","search_products","get_product","get_inventory"]} ``
2. 모델 → **`list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
3. 모델 → **`list_categories`** `` {"parent_id":"cat_outerwear","term_set":"standard"} ``
   ← 결과 220B: `` {"status":"succeeded","data":{"items":[{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true}],"total":1}} ``
4. 모델 → **`list_categories`** `` {"parent_id":"cat_summer_outerwear","term_set":"standard"} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
5. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","limit":100} ``
   ← 결과 4,464B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_wool_overcoat-b50a91c0.webp","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"ava… (+900자) ``
6. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","availability":["out_of_stock"],"limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
7. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","limit":100} ``
   ← 결과 4,572B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_wool_overcoat-b50a91c0.webp","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"ava… (+900자) ``
8. 모델 → **`get_category`** `` {"category_id":"cat_outerwear","fields":["name","product_count"]} ``
   ← 결과 90B: `` {"status":"succeeded","data":{"id":"cat_outerwear","name":"Outerwear","product_count":62}} ``
9. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","limit":100,"sort":"newest"} ``
   ← 결과 4,464B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_wool_overcoat-b50a91c0.webp","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"ava… (+900자) ``
10. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","max_inventory_level":0,"limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
11. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","min_inventory_level":1,"limit":100} ``
   ← 결과 4,464B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_wool_overcoat-b50a91c0.webp","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"ava… (+900자) ``
12. 모델 → **`get_inventory`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 937B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","inventory_level":24,"availability":"in_stock","variants":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_wool_overcoat_l_charcoal","sku":"wo-charcoal-l","size":"L","c… (+337자) ``

_(한 턴의 모델 호출 한도(12회)에 걸려 중단)_

**채점**: E MODEL_CALL_LIMIT — 빠진 것: fact "5 of the 62 outerwear products have a sold-out size" (5, 62 not shown); HOST:MODEL_CALL_LIMIT
(도구 정밀도 0.91, 재현율 1.00)

### a2api-acom-names-batch · 1회차 · E TURN_TIMEOUT

토큰 79,983 · 120.101초 · 모델 호출 11회 · 도구 호출 11회 · 첫 요청 프롬프트 1,979토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> which outerwear styles have broken sizes right now?

1. 모델 → **`a2api_load`** `` {"names":["merchandising › category: list_categories","search › product: search_products","catalog › inventory: get_inventory"]} ``
   ← 결과 64B: `` {"loaded":["list_categories","search_products","get_inventory"]} ``
2. 모델 → **`list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
3. 모델 → **`list_categories`** `` {"parent_id":"cat_outerwear","term_set":"standard"} ``
   ← 결과 220B: `` {"status":"succeeded","data":{"items":[{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true}],"total":1}} ``
4. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","limit":100} ``
   ← 결과 4,464B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_wool_overcoat-b50a91c0.webp","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"ava… (+900자) ``
5. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","availability":["out_of_stock"],"limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
6. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","limit":100,"cursor":"o20"} ``
   ← 결과 2,909B: `` {"status":"succeeded","data":{"items":[{"id":"prd_summer_outerwear_17","name":"Cotton coach jacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_summer_outerwear_17-691ce929.webp","price":89.0,"price_currency":"USD","member_price":null,"cost":40.05,"inventory_level":80,"availability":"in_stock","has_variant":[{"variant_id":"var_summer_outerwear_17_xs_slate","sku":"so-17-slate-xs","size":"XS","color":"Slate","inventory_level":11,"availability":"in_stock"},{"variant_id":"var_summer_outerwear_17_s_slate","sku":"so-17-slate-s","size":"S","color":"Sla… (+900자) ``
7. 모델 → **`get_inventory`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 937B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","inventory_level":24,"availability":"in_stock","variants":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"acom:safety_stock":2,"acom:managed":true,"availability":"in_stock","on_order":0},{"variant_id":"var_wool_overcoat_l_charcoal","sku":"wo-charcoal-l","size":"L","c… (+337자) ``
8. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","limit":100,"sort":"newest"} ``
   ← 결과 4,464B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_wool_overcoat-b50a91c0.webp","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"ava… (+900자) ``
9. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","min_inventory_level":1,"limit":100} ``
   ← 결과 4,464B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_wool_overcoat-b50a91c0.webp","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"ava… (+900자) ``
10. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","limit":100,"cursor":"o40"} ``
   ← 결과 3,615B: `` {"status":"succeeded","data":{"items":[{"id":"prd_summer_outerwear_26","name":"Twill shirt jacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_summer_outerwear_26-9fa9a1eb.webp","price":109.0,"price_currency":"USD","member_price":null,"cost":49.05,"inventory_level":55,"availability":"in_stock","has_variant":[{"variant_id":"var_summer_outerwear_26_xs_black","sku":"so-26-black-xs","size":"XS","color":"Black","inventory_level":2,"availability":"in_stock"},{"variant_id":"var_summer_outerwear_26_s_black","sku":"so-26-black-s","size":"S","color":"Blac… (+900자) ``
11. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","limit":100,"fields":["id","name"]} ``
   ← 결과 3,602B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat"},{"id":"prd_outerwear_01","name":"Waxed cotton duffle coat"},{"id":"prd_outerwear_05","name":"Waxed cotton shell jacket"},{"id":"prd_summer_outerwear_13","name":"Poplin shacket"},{"id":"prd_summer_outerwear_22","name":"Seersucker shacket"},{"id":"prd_summer_outerwear_20","name":"Cotton anorak"},{"id":"prd_summer_outerwear_01","name":"Seersucker cagoule"},{"id":"prd_outerwear_04","name":"Melton parka"},{"id":"prd_summer_outerwear_06","name":"Poplin harrington"},{"id":"prd_summer_outerwear_10","name":"Nylon g… (+900자) ``

_(한 턴의 시간 한도(120초)에 걸려 중단)_

**채점**: E TURN_TIMEOUT — 빠진 것: fact "5 of the 62 outerwear products have a sold-out size" (5, 62 not shown); HOST:TURN_TIMEOUT
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-batch · 2회차 · E TURN_TIMEOUT

토큰 71,617 · 120.082초 · 모델 호출 10회 · 도구 호출 10회 · 첫 요청 프롬프트 1,979토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> which outerwear styles have broken sizes right now?

1. 모델 → **`a2api_load`** `` {"names":["merchandising.category.list_categories","merchandising.category.get_category","search.product.search_products","catalog.product.get_product","catalog.inventory.get_inventory"]} ``
   ← 결과 93B: `` {"loaded":["list_categories","get_category","search_products","get_product","get_inventory"]} ``
2. 모델 → **`list_categories`** `` {"term_set":"standard"} ``
   ← 결과 3,317B: `` {"status":"succeeded","data":{"items":[{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true},{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true},{"id":"cat_knitwear","name":"Knitwear","term_code":"knitwear","term_set":"standard","parent_id":null,"display_order":2,"active":true},{"id":"cat_shirts","name":"Shirts","term_code":"shirts","term_set":"standard","parent_id":null,"display_order":3,"active"… (+900자) ``
3. 모델 → **`list_categories`** `` {"parent_id":"cat_outerwear","term_set":"standard"} ``
   ← 결과 220B: `` {"status":"succeeded","data":{"items":[{"id":"cat_summer_outerwear","name":"Summer outerwear","term_code":"summer_outerwear","term_set":"standard","parent_id":"cat_outerwear","display_order":3,"active":true}],"total":1}} ``
4. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","limit":100} ``
   ← 결과 4,464B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","image":"/media/products/prd_wool_overcoat-b50a91c0.webp","price":289.0,"price_currency":"USD","member_price":null,"cost":120.0,"inventory_level":24,"availability":"in_stock","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"ava… (+900자) ``
5. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","availability":["out_of_stock"],"limit":100} ``
   ← 결과 52B: `` {"status":"succeeded","data":{"items":[],"total":0}} ``
6. 모델 → **`get_category`** `` {"category_id":"cat_outerwear"} ``
   ← 결과 236B: `` {"status":"succeeded","data":{"id":"cat_outerwear","name":"Outerwear","term_code":"outerwear","term_set":"standard","parent_id":null,"display_order":1,"active":true,"description":null,"ancestor_ids":[],"mappings":[],"product_count":62}} ``
7. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","limit":100,"fields":["id","name","has_variant"]} ``
   ← 결과 3,771B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat","has_variant":[{"variant_id":"var_wool_overcoat_s_charcoal","sku":"wo-charcoal-s","size":"S","color":"Charcoal","inventory_level":5,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_m_charcoal","sku":"wo-charcoal-m","size":"M","color":"Charcoal","inventory_level":7,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_l_charcoal","sku":"wo-charcoal-l","size":"L","color":"Charcoal","inventory_level":8,"availability":"in_stock"},{"variant_id":"var_wool_overcoat_xl_charcoal","sku":"wo-charcoal-… (+900자) ``
8. 모델 → **`search_products`** `` {"category_id":"cat_outerwear","limit":100,"fields":["id","name"]} ``
   ← 결과 3,602B: `` {"status":"succeeded","data":{"items":[{"id":"prd_wool_overcoat","name":"Wool overcoat"},{"id":"prd_outerwear_01","name":"Waxed cotton duffle coat"},{"id":"prd_outerwear_05","name":"Waxed cotton shell jacket"},{"id":"prd_summer_outerwear_13","name":"Poplin shacket"},{"id":"prd_summer_outerwear_22","name":"Seersucker shacket"},{"id":"prd_summer_outerwear_20","name":"Cotton anorak"},{"id":"prd_summer_outerwear_01","name":"Seersucker cagoule"},{"id":"prd_outerwear_04","name":"Melton parka"},{"id":"prd_summer_outerwear_06","name":"Poplin harrington"},{"id":"prd_summer_outerwear_10","name":"Nylon g… (+900자) ``
9. 모델 → **`a2api_batch`** `` {"calls":[{"name":"get_inventory","arguments":{"product_id":"prd_wool_overcoat"}},{"name":"get_inventory","arguments":{"product_id":"prd_outerwear_01"}},{"name":"get_inventory","arguments":{"product_id":"prd_outerwear_05"}},{"name":"get_inventory","arguments":{"product_id":"prd_summer_outerwear_13"}},{"name":"get_inventory","arguments":{"product_id":"prd_summer_outerwear_22"}},{"name":"get_inventory","arguments":{"product_id":"prd_summer_outerwear_20"}},{"name":"get_inventory","arguments":{"product_id":"prd_summer_outerwear_01"}},{"name":"get_inventory","arguments":{"product_id":"prd_outerwear_04"}},{"name":"get_inventory","arguments":{"product_id":"prd_summer_outerwear_06"}},{"name":"get_in… (+840자) ``
   ← 실패 49B: `` {"error":"tool call limit reached for this turn"} ``
10. 모델 → **`a2api_batch`** `` {"calls":[{"name":"get_inventory","arguments":{"product_id":"prd_wool_overcoat"}},{"name":"get_inventory","arguments":{"product_id":"prd_outerwear_01"}},{"name":"get_inventory","arguments":{"product_id":"prd_outerwear_05"}},{"name":"get_inventory","arguments":{"product_id":"prd_summer_outerwear_13"}},{"name":"get_inventory","arguments":{"product_id":"prd_summer_outerwear_22"}},{"name":"get_inventory","arguments":{"product_id":"prd_summer_outerwear_20"}},{"name":"get_inventory","arguments":{"product_id":"prd_summer_outerwear_01"}},{"name":"get_inventory","arguments":{"product_id":"prd_outerwear_04"}},{"name":"get_inventory","arguments":{"product_id":"prd_summer_outerwear_06"}},{"name":"get_in… (+840자) ``
   ← 실패 49B: `` {"error":"tool call limit reached for this turn"} ``

_(한 턴의 시간 한도(120초)에 걸려 중단)_

**채점**: E TURN_TIMEOUT — 빠진 것: fact "5 of the 62 outerwear products have a sold-out size" (5, 62 not shown); HOST:TURN_TIMEOUT
(도구 정밀도 0.86, 재현율 1.00)
