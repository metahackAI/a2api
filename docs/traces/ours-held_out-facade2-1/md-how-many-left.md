# md-how-many-left — ours-held_out-facade2-1

[← 실행 묶음](README.md) · 세트 `held_out` · a-commerce `d86a1ff` · a2api `3ddac9b`

**과업**

> How many Light rain parka remain in my inventory?

- 필요한 도구: `get_inventory`
- 허용 도구: `search_products`
- 답에 있어야 할 사실: 4 in total: S 2, M 0, L 0, XL 2 (all Stone)
- 답에 있어야 할 사실: S and XL are at their safety stock of 2, so the parka is effectively sold out for new sales planning

### a2api-facade-all · 1회차 · ✓ 통과

토큰 24,188 · 9.931초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 6,555토큰

준비: 전략 `all`, 함수 22개

**질문 1**
> How many Light rain parka remain in my inventory?

- 모델 판단(추론 필드): We need find product "Light rain parka". Search product grid list. keyword "Light rain parka". Could also be product name. Use facade_get_product_grid_list with keyword. We need count? How many remain in inventory. Could be stock quantity. Need product id. First search product grid list. Let's call facade_get_product_grid_list with keyword "Light rain parka".
1. 모델 → **`facade_get_product_grid_list`** `` {"keyword":"Light rain parka","page":1,"page_size":100} ``
   ← 결과 5,543B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_rain_parka","product_name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":118.0,"member_price":null,"stock":4,"availability":"in_stock","cost":50.0},{"product_id":"prd_outerwear_06","product_name":"Recycled nylon trench coat","category_id":"cat_outerwear","brand_id":"brn_northwind","price":259.0,"member_price":null,"stock":69,"availability":"in_stock","cost":115.38},{"product_id":"prd_outerwear_01","product_name":"Waxed cotton duffle coat","category_id":"cat_outerwear","brand_id":"brn_ridgeline… (+2,400자) ``
- 모델 판단(추론 필드): We found product_id prd_rain_parka, product_name Light rain parka, stock 4. But may have variants? The product detail v2 gives variants with color/size stock each. Might need total inventory across variants. The product grid list shows stock 4. Could be total. Better get product_detail_info_v2 to see variants.
2. 모델 → **`facade_get_product_detail_info_v2`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 1,055B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","product_name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":118.0,"member_price":null,"stock":4,"availability":"in_stock","cost":50.0,"approval_status":"active","variants":[{"variant_id":"var_rain_parka_s_stone","color":"Stone","size":"S","stock":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","color":"Stone","size":"M","stock":0,"availability":"out_of_stock"},{"variant_id":"var_rain_parka_l_stone","color":"Stone","size":"L","stock":0,"availability":"out_of_stock"},{"va… (+455자) ``
- 모델 판단(추론 필드): Stock total 4, variants: S Stone 2, XL Stone 2, M/L zero. Answer: 4 remain in inventory, 2 in size S stone, 2 in XL stone. Possibly user asks how many remain. Provide number. Might also give per variant. Answer succinctly.

**답변 1**
> Light rain parka – product_id **prd_rain_parka**
>
> * Total on-hand stock: **4 units**
> * Availability: in_stock
>
> Variants:
> * var_rain_parka_s_stone – Stone / S – 2 in stock, in_stock
> * var_rain_parka_m_stone – Stone / M – 0 in stock, out_of_stock
> * var_rain_parka_l_stone – Stone / L – 0 in stock, out_of_stock
> * var_rain_parka_xl_stone – Stone / XL – 2 in stock, in_stock
>
> Price $118.00, cost $50.00, category cat_summer_outerwear.

**채점**: ✓ 통과

### a2api-facade-all · 2회차 · ✓ 통과

토큰 23,550 · 10.006초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 6,555토큰

준비: 전략 `all`, 함수 22개

**질문 1**
> How many Light rain parka remain in my inventory?

- 모델 판단(추론 필드): We need count of inventory for Light rain parka. Likely product search. Need product_id. First search product grid list with keyword "Light rain parka". Then get product detail info for stock. Use facade_get_product_grid_list with keyword "Light rain parka". Could also use count. Probably need to find product, then get stock. Might be variant stock. Let's search.
1. 모델 → **`facade_get_product_grid_list`** `` {"keyword":"Light rain parka","page":1,"page_size":20} ``
   ← 결과 4,374B: `` {"status":"succeeded","data":{"list":[{"product_id":"prd_rain_parka","product_name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":118.0,"member_price":null,"stock":4,"availability":"in_stock","cost":50.0},{"product_id":"prd_outerwear_06","product_name":"Recycled nylon trench coat","category_id":"cat_outerwear","brand_id":"brn_northwind","price":259.0,"member_price":null,"stock":69,"availability":"in_stock","cost":115.38},{"product_id":"prd_outerwear_01","product_name":"Waxed cotton duffle coat","category_id":"cat_outerwear","brand_id":"brn_ridgeline… (+2,400자) ``
- 모델 판단(추론 필드): We found product_id prd_rain_parka, product_name Light rain parka, stock 4. But product may have variants. Need check variants stock each. Could be total stock 4 from product grid list. Might need more detailed info. Could call facade_get_product_detail_info_v2 to get variants stock each. Probably answer 4. Might want sum of variants. Let's get detail v2.
2. 모델 → **`facade_get_product_detail_info_v2`** `` {"product_id":"prd_rain_parka"} ``
   ← 결과 1,055B: `` {"status":"succeeded","data":{"product_id":"prd_rain_parka","product_name":"Light rain parka","category_id":"cat_summer_outerwear","brand_id":"brn_northwind","price":118.0,"member_price":null,"stock":4,"availability":"in_stock","cost":50.0,"approval_status":"active","variants":[{"variant_id":"var_rain_parka_s_stone","color":"Stone","size":"S","stock":2,"availability":"in_stock"},{"variant_id":"var_rain_parka_m_stone","color":"Stone","size":"M","stock":0,"availability":"out_of_stock"},{"variant_id":"var_rain_parka_l_stone","color":"Stone","size":"L","stock":0,"availability":"out_of_stock"},{"va… (+455자) ``
- 모델 판단(추론 필드): Stock is 4 total, with variants: S Stone 2, XL Stone 2, M 0, L 0. Sum 4. Answer: 4 remain in inventory, breakdown. Possibly ask how many remain in inventory? Answer 4 units. Provide details.

**답변 1**
> Light rain parka — product **prd_rain_parka**
>
> * Overall stock shown in the catalogue: **4 units**, availability `in_stock`
> * Variant breakdown
>   * var_rain_parka_s_stone – Stone / S – 2 in stock, in_stock
>   * var_rain_parka_m_stone – Stone / M – 0 in stock, out_of_stock
>   * var_rain_parka_l_stone – Stone / L – 0 in stock, out_of_stock
>   * var_rain_parka_xl_stone – Stone / XL – 2 in stock, in_stock
>
> Total remaining across the variants = 2 + 0 + 0 + 2 = **4 pieces**.

**채점**: ✓ 통과
