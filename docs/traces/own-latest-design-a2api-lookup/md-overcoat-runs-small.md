# md-overcoat-runs-small — own-latest-design-a2api-lookup

[← 실행 묶음](README.md)

**과업**

> people keep saying the wool overcoat runs small. is that actually true?

- 답에 있어야 할 사실: 41 reviews, average 4.6
- 답에 있어야 할 사실: 29 say true to size, 12 say a bit snug, none say it runs large
- 답에 있어야 할 사실: the most common phrase is 'size up for a hoodie' (9 mentions), so the snug votes come from layering

### a2api 변환 파사드 + 주문 번호 조회 · 1회차 · ✗ 실패

토큰 5,431 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

- 라우팅: Catalog agent (chosen by the model)
- 도구 검색 후보: 5 candidates: save_display_banner_list, get_display_corner_list, get_product_detail_info, get_product_detail_info_v2, get_product_grid_list
- 계획: `get_product_grid_list` `` {"page":1,"keyword":"wool overcoat","page_size":20} ``
1. 에이전트 → **`get_product_grid_list`** `` {"page":1,"keyword":"wool overcoat","page_size":20} ``
   ← 결과: `` {"list":[{"cost":120.0,"price":289.0,"stock":24,"brand_id":"brn_northwind","product_id":"prd_wool_overcoat","category_id":"cat_outerwear","availability":"in_stock","member_price":null,"product_name":"Wool overcoat"},{"cost":24.46,"price":59.0,"stock":23,"brand_id":"brn_ridgeline","product_id":"prd_scarves_04","category_id":"cat_scarves","availability":"in_stock","member_price":null,"product_name":"Wool stole"},{"cost":74.16,"price":149.0,"stock":89,"brand_id":"brn_northwind","product_id":"prd_pants_22","category_id":"cat_pants","availability":"in_stock","member_price":null,"product_name":"Wool… (+3,560자) ``

**답변 1**
> The Wool overcoat is in stock with 24 units on hand. The product grid list shows the Wool overcoat at $289, but it does not include sizing feedback or fit notes, so there is no evidence here that it runs small or not.

화면 블록: product_table(20 of 20)

**채점**: ✗ 실패 — 빠진 것: fact "41 reviews, average 4.6" (41, 4.6 not shown); fact "the most common phrase is 'size up for a hoodie' (9 mentions" (9 not shown)

### a2api 변환 파사드 + 주문 번호 조회 · 2회차 · ✗ 실패

토큰 8,091 · 모델 호출 4회 · 도구 호출 1회

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

- 라우팅: Catalog agent (chosen by the model)
- 도구 검색 후보: 5 candidates: save_display_banner_list, get_display_corner_list, get_product_detail_info, get_product_detail_info_v2, get_product_grid_list
- 계획: `get_product_grid_list` `` {"page":1,"keyword":"wool overcoat","page_size":20} ``
1. 에이전트 → **`get_product_grid_list`** `` {"page":1,"keyword":"wool overcoat","page_size":20} ``
   ← 결과: `` {"list":[{"cost":120.0,"price":289.0,"stock":24,"brand_id":"brn_northwind","product_id":"prd_wool_overcoat","category_id":"cat_outerwear","availability":"in_stock","member_price":null,"product_name":"Wool overcoat"},{"cost":24.46,"price":59.0,"stock":23,"brand_id":"brn_ridgeline","product_id":"prd_scarves_04","category_id":"cat_scarves","availability":"in_stock","member_price":null,"product_name":"Wool stole"},{"cost":74.16,"price":149.0,"stock":89,"brand_id":"brn_northwind","product_id":"prd_pants_22","category_id":"cat_pants","availability":"in_stock","member_price":null,"product_name":"Wool… (+3,560자) ``

**답변 1**
> The results show the Wool overcoat product in the catalog, but they don’t include sizing or fit feedback. There’s no data here about whether the overcoat runs small or not.

화면 블록: product_table(20 of 20)

**채점**: ✗ 실패 — 빠진 것: fact "41 reviews, average 4.6" (41, 4.6 not shown); fact "the most common phrase is 'size up for a hoodie' (9 mentions" (9 not shown)

### a2api 변환 파사드 + 주문 번호 조회 · 3회차 · ✗ 실패

토큰 8,091 · 모델 호출 4회 · 도구 호출 1회

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

- 라우팅: Catalog agent (chosen by the model)
- 도구 검색 후보: 5 candidates: save_display_banner_list, get_display_corner_list, get_product_detail_info, get_product_detail_info_v2, get_product_grid_list
- 계획: `get_product_grid_list` `` {"page":1,"keyword":"wool overcoat","page_size":20} ``
1. 에이전트 → **`get_product_grid_list`** `` {"page":1,"keyword":"wool overcoat","page_size":20} ``
   ← 결과: `` {"list":[{"cost":120.0,"price":289.0,"stock":24,"brand_id":"brn_northwind","product_id":"prd_wool_overcoat","category_id":"cat_outerwear","availability":"in_stock","member_price":null,"product_name":"Wool overcoat"},{"cost":24.46,"price":59.0,"stock":23,"brand_id":"brn_ridgeline","product_id":"prd_scarves_04","category_id":"cat_scarves","availability":"in_stock","member_price":null,"product_name":"Wool stole"},{"cost":74.16,"price":149.0,"stock":89,"brand_id":"brn_northwind","product_id":"prd_pants_22","category_id":"cat_pants","availability":"in_stock","member_price":null,"product_name":"Wool… (+3,560자) ``

**답변 1**
> The results show the Wool overcoat product in the catalog, but they don’t include sizing or fit feedback. There’s no data here about whether the overcoat runs small or not.

화면 블록: product_table(20 of 20)

**채점**: ✗ 실패 — 빠진 것: fact "41 reviews, average 4.6" (41, 4.6 not shown); fact "the most common phrase is 'size up for a hoodie' (9 mentions" (9 not shown)
