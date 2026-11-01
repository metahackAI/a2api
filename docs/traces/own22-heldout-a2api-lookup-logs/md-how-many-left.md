# md-how-many-left — own22-heldout-a2api-lookup-logs

[← 실행 묶음](README.md)

**과업**

> How many Light rain parka remain in my inventory?

- 답에 있어야 할 사실: 4 in total: S 2, M 0, L 0, XL 2 (all Stone)
- 답에 있어야 할 사실: S and XL are at their safety stock of 2, so the parka is effectively sold out for new sales planning

### a2api 변환 파사드 + 주문 번호 조회 · 1회차 · ✗ 실패

토큰 7,010 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> How many Light rain parka remain in my inventory?

- 라우팅: Catalog agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: get_display_corner_list, get_product_detail_info, get_product_detail_info_v2, get_product_grid_list, get_product_grid_list_count
- 계획: `get_product_grid_list` `` {"page":1,"keyword":"Light rain parka","page_size":100} ``
1. 에이전트 → **`get_product_grid_list`** `` {"page":1,"keyword":"Light rain parka","page_size":100} ``
   ← 결과: `` {"list":[{"cost":50.0,"price":118.0,"stock":4,"brand_id":"brn_northwind","product_id":"prd_rain_parka","category_id":"cat_summer_outerwear","availability":"in_stock","member_price":null,"product_name":"Light rain parka"},{"cost":115.38,"price":259.0,"stock":69,"brand_id":"brn_northwind","product_id":"prd_outerwear_06","category_id":"cat_outerwear","availability":"in_stock","member_price":null,"product_name":"Recycled nylon trench coat"},{"cost":134.5,"price":289.0,"stock":24,"brand_id":"brn_ridgeline","product_id":"prd_outerwear_01","category_id":"cat_outerwear","availability":"in_stock","memb… (+20,835자) ``

**답변 1**
> The Light rain parka shows 4 units in stock and is in stock.

화면 블록: product_table(100 of 100)

**채점**: ✗ 실패 — 빠진 것: fact "4 in total: S 2, M 0, L 0, XL 2 (all Stone)" (0, 0 not shown)

### a2api 변환 파사드 + 주문 번호 조회 · 2회차 · ✗ 실패

토큰 4,760 · 모델 호출 2회 · 도구 호출 2회

**질문 1**
> How many Light rain parka remain in my inventory?

- 라우팅: Catalog agent (the request names this agent's work)
- 도구 검색 후보: 5 candidates: get_display_corner_list, get_product_detail_info, get_product_detail_info_v2, get_product_grid_list, get_product_grid_list_count
- 계획: `get_product_grid_list_count` `` {"keyword":"Light rain parka"} ``; `get_product_grid_list` `` {"page":1,"keyword":"Light rain parka","page_size":100} ``
1. 에이전트 → **`get_product_grid_list_count`** `` {"keyword":"Light rain parka"} ``
   ← 결과: `` {"total":120} ``
2. 에이전트 → **`get_product_grid_list`** `` {"page":1,"keyword":"Light rain parka","page_size":100} ``
   ← 결과: `` {"list":[{"cost":50.0,"price":118.0,"stock":4,"brand_id":"brn_northwind","product_id":"prd_rain_parka","category_id":"cat_summer_outerwear","availability":"in_stock","member_price":null,"product_name":"Light rain parka"},{"cost":115.38,"price":259.0,"stock":69,"brand_id":"brn_northwind","product_id":"prd_outerwear_06","category_id":"cat_outerwear","availability":"in_stock","member_price":null,"product_name":"Recycled nylon trench coat"},{"cost":134.5,"price":289.0,"stock":24,"brand_id":"brn_ridgeline","product_id":"prd_outerwear_01","category_id":"cat_outerwear","availability":"in_stock","memb… (+20,835자) ``

**답변 1**
> You have 4 Light rain parka in stock. The product is in stock and listed at $118.00.

화면 블록: product_table(100 of 100)

**채점**: ✗ 실패 — 빠진 것: fact "4 in total: S 2, M 0, L 0, XL 2 (all Stone)" (0, 0 not shown)
