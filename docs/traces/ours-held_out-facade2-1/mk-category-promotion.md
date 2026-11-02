# mk-category-promotion — ours-held_out-facade2-1

[← 실행 묶음](README.md) · 세트 `held_out` · a-commerce `d86a1ff` · a2api `3ddac9b`

**과업**

> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 필요한 도구: `create_promotion`
- 허용 도구: `list_categories`, `list_active_promotions`, `get_policy`
- 답에 있어야 할 사실: 2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store time

### a2api-facade-all · 1회차 · ✗ 실패

토큰 55,908 · 68.946초 · 모델 호출 5회 · 도구 호출 4회 · 첫 요청 프롬프트 6,564토큰

준비: 전략 `all`, 함수 22개

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 모델 판단(추론 필드): We need to create promotion. The tools: facade_save_promotion_list. It says: Save promotion rows at once: insert creates a percent-off sale price promotion for a category or products (types item_price_everyone or item_price_one_grade); update pauses or ends one; delete ends one. An insert row needs promotion_name, promotion_type, starts_at, ends_at, percent_off, applies_to and category_id (category) or product_ids (products), and target_member_grade for item_price_one_grade (not G00); ... The description says percent-off sale price promotion. But user wants $50 off orders above $250. That's order discount, not percent off items. However promotion_type options: item_price_everyone, order_disc… (+2,211자)
1. 모델 → **`facade_get_product_grid_list`** `` {"keyword":"Outerwear","page":1,"page_size":20} ``
   ← 결과 4,505B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_rain_parka","product_name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":118.0,"member_price":null,"stock":4,"availability":"in_stock","cost":50.0},{"product_id":"prd_summer_outerwear_22","product_name":"Seersucker shacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":79.0,"member_price":null,"stock":36,"availability":"in_stock","cost":35.55},{"product_id":"prd_summer_outerwear_33","product_name":"Linen shacket","category_id":"cat_summer_outerwear","brand_id":"brn_no… (+2,400자) ``
- 모델 판단(추론 필드): The keyword Outerwear returned category_id cat_summer_outerwear. Maybe Outerwear is broader. Might be category_id cat_outerwear? Let's try search products with category? Could try keyword "outerwear" lower case? Already got results. Could be category name is "Outerwear" but products have category_id cat_summer_outerwear. Might be multiple categories: cat_summer_outerwear, cat_winter_outerwear? Let's try search product grid list with keyword "jacket"? Not helpful. Alternative: maybe category_id for Outerwear is cat_outerwear. Let's try search product grid list with category_id cat_outerwear? Can't know. Could search product grid list with keyword "Outerwear" maybe matches product name contain… (+759자)
2. 모델 → **`facade_get_product_grid_list`** `` {"keyword":"winter","page":1,"page_size":20} ``
   ← 결과 4,242B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_outerwear_01","product_name":"Waxed cotton duffle coat","category_id":"cat_outerwear","brand_id":"brn_ridgeline","price":289.0,"member_price":null,"stock":24,"availability":"in_stock","cost":134.5},{"product_id":"prd_knitwear_02","product_name":"Merino fisherman sweater","category_id":"cat_knitwear","brand_id":"brn_northwind","price":229.0,"member_price":194.65,"stock":26,"availability":"in_stock","cost":103.03},{"product_id":"prd_scarves_02","product_name":"Cotton snood","category_id":"cat_scarves","brand_id":"brn_northwind","price":59.… (+2,400자) ``
- 모델 판단(추론 필드): We found category_id cat_outerwear. Good. Now we need to create promotion. $50 off orders above $250. Promotion_type options: item_price_everyone, order_discount, item_price_one_grade, add_on, other. Order discount might be correct. But does facade_save_promotion_list support $50 off threshold? The tool definition does not include threshold or discount amount, only percent_off. Hmm. Maybe the tool actually supports $50 off via percent_off? Could be they want $50 off as a flat discount, but the tool only supports percent off. Could be a mismatch. Alternative interpretation: Maybe the promotion is $50 off orders above $250, meaning order discount of $50 flat when order total >= $250, and appli… (+2,284자)
3. 모델 → **`facade_save_promotion_list`** `` {"rows":[{"row_action":"insert","promotion_name":"Outerwear $50 Off Orders $250+","promotion_type":"order_discount","starts_at":"2026-11-06T00:00","ends_at":"2026-11-20T23:59","applies_to":"category","category_id":"cat_outerwear"}]} ``
   ← 실패 296B: `` {"status":"failed","error":{"code":"UPSTREAM_CONFLICT","detail":"The backend reported that the current state does not allow this request. (HTTP 409) Row 1: Promotion type not available on this screen."},"hint":"The current state does not allow this change. Report the state instead of retrying."} ``
- 모델 판단(추론 필드): Promotion type not available on this screen. So order_discount not allowed? Or promotion type not available? Maybe we need to use item_price_everyone. The hint says report the state instead of retrying. Maybe we need to use item_price_everyone which creates percent-off sale price promotion. But user wants $50 off orders above $250. Could interpret as $50 off meaning 50% off? No. Maybe the tool only allows item_price_everyone or item_price_one_grade for insert. So promotion type order_discount not available. Alternative: Create a percent off promotion for Outerwear category. Could approximate $50 off as percent off? Maybe we can create 20% off? Because $50 off $250 is 20%. Could be acceptable… (+2,283자)
4. 모델 → **`facade_get_promotion_grid_list`** `` {"page":1,"page_size":20} ``
   ← 결과 1,448B: `` {"status":"succeeded","data":{"list":[{"promotion_id":"promo_denim_bundle","promotion_name":"Denim bundle","promotion_type":"order_discount","promotion_status":"scheduled","target_member_grade":"G00","starts_at":"2026-11-13T00:00:00-05:00","ends_at":"2026-11-20T23:59:00-05:00"},{"promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00","starts_at":"2026-11-01T00:00:00-04:00","ends_at":"2026-11-15T23:59:00-05:00"},{"promotion_id":"promo_linen_clearance","promotion_name":"Linen clearan… (+848자) ``
- 모델 판단(추론 필드): Existing promotions include order_discount type. So promotion_type order_discount exists. But insert creation via save_promotion_list maybe not allowed for order_discount? Error says Promotion type not available on this screen. Could be the UI screen restricts to item_price types. The error says Promotion type not available on this screen. So we cannot create order_discount via this tool in current state. Alternative: Maybe we need to use promotion_type item_price_everyone with percent_off = ? Could approximate $50 off as 50%? Hmm. The user asked for $50 off orders above $250. Maybe we can create an order_discount promotion via a different method? The save_promotion_list seems to only suppor… (+1,354자)

**답변 1**
> The promotion creation screen you’re on only allows percent-off sale-price promotions for a category or a set of products ( `item_price_everyone` / `item_price_one_grade` ). It does not allow creating a fixed $50 off an order with a $250 minimum, and `order_discount` type inserts are blocked on this screen:
>
> * “Promotion type not available on this screen.”
>
> I can create a percent-off sale price promotion for the Outerwear category `cat_outerwear` that runs for 2 weeks, e.g.:
>
> * starts_at: 2026-11-06T00:00
> * ends_at:   2026-11-20T23:59
>
> If you want a $50 off $250+ order discount / threshold rule, that type of promotion can’t be saved with `facade_save_promotion_list` from the current UI – it would need to be built via the order-discount workflow that isn’t available here. Let me know if you’d like a percent-off alternative for `cat_outerwear` instead, and what % you want.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (6, 19, 23 not shown)

### a2api-facade-all · 2회차 · ✗ 실패

토큰 148,204 · 101.129초 · 모델 호출 11회 · 도구 호출 10회 · 첫 요청 프롬프트 6,564토큰

준비: 전략 `all`, 함수 22개

**질문 1**
> Create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks

- 모델 판단(추론 필드): We need to create a promotion for Outerwear, $50 off orders above $250, valid for 2 weeks. We need to understand promotion types available. facade_save_promotion_list: save promotion rows at once: insert creates a percent-off sale price promotion for a category or products (types item_price_everyone or item_price_one_grade); update pauses or ends one; delete ends one. An insert row needs promotion_name, promotion_type, starts_at, ends_at, percent_off, applies_to and category_id (category) or product_ids (products), and target_member_grade for item_price_one_grade (not G00); an update row needs promotion_id and promotion_status paused or ended; a delete row needs promotion_id. The description… (+2,204자)
1. 모델 → **`facade_get_product_grid_list`** `` {"keyword":"Outerwear","page":1,"page_size":20} ``
   ← 결과 4,505B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_rain_parka","product_name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":118.0,"member_price":null,"stock":4,"availability":"in_stock","cost":50.0},{"product_id":"prd_summer_outerwear_22","product_name":"Seersucker shacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":79.0,"member_price":null,"stock":36,"availability":"in_stock","cost":35.55},{"product_id":"prd_summer_outerwear_33","product_name":"Linen shacket","category_id":"cat_summer_outerwear","brand_id":"brn_no… (+2,400자) ``
- 모델 판단(추론 필드): The keyword Outerwear returns category_id cat_summer_outerwear. Maybe Outerwear is broader. Could be cat_outerwear. Let's try search product grid with category? Maybe need to find category list. Could search keyword "outerwear" maybe case sensitive? It returned summer outerwear. Could be multiple categories: cat_outerwear? Let's try get product grid with keyword "outer".
2. 모델 → **`facade_get_product_grid_list`** `` {"keyword":"outerwear","page":1,"page_size":20} ``
   ← 결과 4,505B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_rain_parka","product_name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":118.0,"member_price":null,"stock":4,"availability":"in_stock","cost":50.0},{"product_id":"prd_summer_outerwear_22","product_name":"Seersucker shacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":79.0,"member_price":null,"stock":36,"availability":"in_stock","cost":35.55},{"product_id":"prd_summer_outerwear_33","product_name":"Linen shacket","category_id":"cat_summer_outerwear","brand_id":"brn_no… (+2,400자) ``
- 모델 판단(추론 필드): Same. Maybe Outerwear is cat_summer_outerwear? Could also be winter outerwear. Let's try search for "jacket".
3. 모델 → **`facade_get_product_grid_list`** `` {"keyword":"jacket","page":1,"page_size":5} ``
   ← 결과 1,193B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_summer_outerwear_31","product_name":"Chambray coach jacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":89.0,"member_price":null,"stock":104,"availability":"in_stock","cost":40.05},{"product_id":"prd_summer_outerwear_03","product_name":"Cotton shirt jacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":69.0,"member_price":null,"stock":23,"availability":"in_stock","cost":31.05},{"product_id":"prd_summer_outerwear_07","product_name":"Poplin shirt jacket","category_id":"cat_summer_outerw… (+593자) ``
- 모델 판단(추론 필드): Possibly Outerwear category is cat_summer_outerwear. Could also be cat_winter_outerwear. Let's search product grid with keyword "parka".
4. 모델 → **`facade_get_product_grid_list`** `` {"keyword":"parka","page":1,"page_size":20} ``
   ← 결과 4,491B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_rain_parka","product_name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":118.0,"member_price":null,"stock":4,"availability":"in_stock","cost":50.0},{"product_id":"prd_outerwear_04","product_name":"Melton parka","category_id":"cat_outerwear","brand_id":"brn_northwind","price":229.0,"member_price":null,"stock":45,"availability":"in_stock","cost":110.36},{"product_id":"prd_summer_outerwear_22","product_name":"Seersucker shacket","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","pri… (+2,400자) ``
- 모델 판단(추론 필드): We see category_id cat_outerwear for prd_outerwear_04 Melton parka. So there is cat_outerwear. Let's search products with category_id cat_outerwear to confirm.
5. 모델 → **`facade_get_product_grid_list`** `` {"category_id":"cat_outerwear","page":1,"page_size":20} ``
   ← 결과 4,465B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_wool_overcoat","product_name":"Wool overcoat","category_id":"cat_outerwear","brand_id":"brn_northwind","price":289.0,"member_price":null,"stock":24,"availability":"in_stock","cost":120.0},{"product_id":"prd_outerwear_01","product_name":"Waxed cotton duffle coat","category_id":"cat_outerwear","brand_id":"brn_ridgeline","price":289.0,"member_price":null,"stock":24,"availability":"in_stock","cost":134.5},{"product_id":"prd_outerwear_05","product_name":"Waxed cotton shell jacket","category_id":"cat_outerwear","brand_id":"brn_northwind","pric… (+2,400자) ``
- 모델 판단(추론 필드): It returns mixed categories? The query category_id cat_outerwear but results include cat_summer_outerwear. Maybe the API returns also subcategories? Or the filter not strict? Could be that category_id filter returns products in that category and subcategories? Or maybe data issue. Let's try count.
6. 모델 → **`facade_get_product_grid_list_count`** `` {"category_id":"cat_outerwear"} ``
   ← 결과 42B: `` {"status":"succeeded","data":{"total":62}} ``
- 모델 판단(추론 필드): Total 62 products. So cat_outerwear exists. Now we need to create promotion for Outerwear, $50 off orders above $250, valid for 2 weeks. The tool facade_save_promotion_list requires promotion_type, promotion_name, starts_at, ends_at, percent_off, applies_to, category_id or product_ids. Also promotion_type options include order_discount. Percent_off required? Schema shows percent_off is property but not required? Required fields: row_action. Additional properties optional? The insert row needs promotion_name, promotion_type, starts_at, ends_at, percent_off, applies_to and category_id (category) or product_ids (products), and target_member_grade for item_price_one_grade (not G00). So percent_o… (+1,396자)
7. 모델 → **`facade_get_promotion_grid_list`** `` {"page":1,"page_size":20} ``
   ← 결과 1,448B: `` {"status":"succeeded","data":{"list":[{"promotion_id":"promo_denim_bundle","promotion_name":"Denim bundle","promotion_type":"order_discount","promotion_status":"scheduled","target_member_grade":"G00","starts_at":"2026-11-13T00:00:00-05:00","ends_at":"2026-11-20T23:59:00-05:00"},{"promotion_id":"promo_autumn_knit","promotion_name":"Autumn knitwear 15%","promotion_type":"item_price_everyone","promotion_status":"running","target_member_grade":"G00","starts_at":"2026-11-01T00:00:00-04:00","ends_at":"2026-11-15T23:59:00-05:00"},{"promotion_id":"promo_linen_clearance","promotion_name":"Linen clearan… (+848자) ``
- 모델 판단(추론 필드): We see promotions with order_discount type but no percent_off shown? The list output doesn't show percent_off, applies_to, etc. Maybe the grid list returns limited fields. We need to understand how to create $50 off orders above $250. Maybe the promotion_type order_discount supports a fixed amount off? But schema for save promotion includes percent_off only. Hmm. Maybe the $50 off is actually $50 off orders above $250, which could be a promotion for Outerwear category with item_price_everyone and percent_off? Could be they want $50 off, but the tool only allows percent off. Could be a mismatch. Alternative interpretation: The promotion is for Outerwear category, $50 off orders above $250. Co… (+2,287자)
8. 모델 → **`facade_get_promotion_grid_list`** `` {"promotion_name":50,"page":1,"page_size":20} ``
   ← 결과 65B: `` {"status":"succeeded","data":{"list":[],"page":1,"page_size":20}} ``
- 모델 판단(추론 필드): No results. Maybe we need to get more details of a promotion to see fields. Could use promotion_id to get details? No tool for detail. Alternative: maybe the promotion for Outerwear $50 off orders above $250 can be created as promotion_type "order_discount" with percent_off = 0 and applies_to category? Might still be accepted. The instruction says: "If something does not exist or a rule forbids it, say so plainly instead of guessing." The tool may not support $50 off orders above $250 because it only supports percent-off sale price promotion for category or products. So we cannot create $50 off order threshold promotion with current tools. But the promotion_type order_discount exists. Maybe … (+2,283자)
9. 모델 → **`facade_get_promotion_grid_list_count`** `` {"promotion_status":"running","page":1,"page_size":100} ``
   ← 결과 41B: `` {"status":"succeeded","data":{"total":4}} ``
- 모델 판단(추론 필드): We saw promotions. Could try get promotion grid list with promotion_name "Free shipping over $80" which is add_on type. Might be that order_discount promotions are created elsewhere. Given ambiguity, maybe we can create a promotion with promotion_type "item_price_everyone", promotion_name "Outerwear $50 off orders $250+", applies_to category cat_outerwear, percent_off = 0? That would be weird. Alternative: Could be the promotion is for Outerwear category with a $50 discount per item, but only if order total > $250. The tool doesn't support minimum order amount. I think the most honest answer is to state limitation. However, the instruction says "A change you make is only a preview that goes … (+1,943자)
10. 모델 → **`facade_get_member_grade_list`** `` {} ``
   ← 결과 257B: `` {"status":"succeeded","data":{"list":[{"member_grade":"G03","grade_name":"VIP","member_count":1284,"rank":3},{"member_grade":"G02","grade_name":"Gold","member_count":2900,"rank":2},{"member_grade":"G01","grade_name":"Member","member_count":9816,"rank":1}]}} ``
- 모델 판단(추론 필드): No G00? Maybe G00 is everyone. Given time constraints, I'll respond that the current promotion tools only support percent-off item price promotions, not fixed dollar order discounts with minimum spend. Therefore cannot create exactly as requested. Offer alternative. Alternatively, could create promotion with promotion_type "order_discount", promotion_name "Outerwear $50 off $250+", starts_at 2026-11-06T11:00-05:00, ends_at 2026-11-20T23:59-05:00, applies_to category cat_outerwear, percent_off maybe 50? Could try. Given instruction to not guess, better to be transparent. I'll answer: Category cat_outerwear identified, 62 products. Tool only supports percent-off sale price promotions for item_… (+149자)

**답변 1**
> I can’t create that exact promotion with the current tools.
>
> * Outerwear category found: **cat_outerwear** – 62 products in the catalogue.
> * Current store time: 2026-11-06 11:00 America/New_York.
>
> `facade_save_promotion_list` insert only creates a percent-off sale-price promotion for
> `item_price_everyone` or `item_price_one_grade` – it needs `promotion_name, promotion_type, starts_at, ends_at, percent_off, applies_to` and a `category_id`/`product_ids`. There is no field for a fixed $ amount off, no minimum order amount/$250 threshold, and `order_discount` inserts are not a percent-off sale-price promotion per the tool description.
>
> So a $50 off orders above $250 for the Outerwear category cannot be built as specified. If you want, I can create a percent-off item-price promotion for cat_outerwear for the 2-week window, e.g.:
>
> * starts_at 2026-11-06T11:00-05:00
> * ends_at   2026-11-20T23:59-05:00
> * applies_to = category, category_id = cat_outerwear
> * promotion_type = item_price_everyone
>
> Tell me the percent you want and whether it should be for all shoppers G00 or a specific grade, and I’ll put the promotion in a change set for approval.

**채점**: ✗ 실패 — 빠진 것: fact "2 weeks from today is Fri Nov 6 – Thu Nov 19 23:59 store tim" (19, 23 not shown)
