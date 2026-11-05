# md-overcoat-runs-small — luna-design-a2api

[← 실행 묶음](README.md)

**과업**

> people keep saying the wool overcoat runs small. is that actually true?

- 답에 있어야 할 사실: 41 reviews, average 4.6
- 답에 있어야 할 사실: 29 say true to size, 12 say a bit snug, none say it runs large
- 답에 있어야 할 사실: the most common phrase is 'size up for a hoodie' (9 mentions), so the snug votes come from layering

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 1회차 · ✗ 실패

토큰 26,536 · 모델 호출 4회 · 도구 호출 2회

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

- 라우팅: Catalog agent (chosen by the model)
- 도구 검색 후보: 5 candidates: save_display_banner_list, get_display_corner_list, get_product_detail_info, get_product_detail_info_v2, get_product_grid_list
- 계획: `get_product_grid_list` `` {"page":1,"keyword":"wool overcoat","page_size":20} ``; `get_product_detail_info_v2` `` {} ``
1. 에이전트 → **`get_product_grid_list`** `` {"page":1,"keyword":"wool overcoat","page_size":20} ``
   ← 결과: `` {"list":[{"cost":120.0,"price":289.0,"stock":24,"brand_id":"brn_northwind","product_id":"prd_wool_overcoat","category_id":"cat_outerwear","availability":"in_stock","member_price":null,"product_name":"Wool overcoat"},{"cost":24.46,"price":59.0,"stock":23,"brand_id":"brn_ridgeline","product_id":"prd_scarves_04","category_id":"cat_scarves","availability":"in_stock","member_price":null,"product_name":"Wool stole"},{"cost":74.16,"price":149.0,"stock":89,"brand_id":"brn_northwind","product_id":"prd_pants_22","category_id":"cat_pants","availability":"in_stock","member_price":null,"product_name":"Wool… (+3,560자) ``
2. 에이전트 → **`get_product_detail_info_v2`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과: `` {"cost":120.0,"price":289.0,"stock":24,"brand_id":"brn_northwind","variants":[{"size":"S","color":"Charcoal","stock":5,"variant_id":"var_wool_overcoat_s_charcoal","availability":"in_stock"},{"size":"M","color":"Charcoal","stock":7,"variant_id":"var_wool_overcoat_m_charcoal","availability":"in_stock"},{"size":"L","color":"Charcoal","stock":8,"variant_id":"var_wool_overcoat_l_charcoal","availability":"in_stock"},{"size":"XL","color":"Charcoal","stock":4,"variant_id":"var_wool_overcoat_xl_charcoal","availability":"in_stock"}],"attributes":[{"unit":null,"value":"70% wool, 30% polyamide","attribute… (+182자) ``

**답변 1**
> The results show the Wool overcoat’s sizes and stock, but no customer feedback, so they don’t confirm whether it runs small. There’s nothing to conclude about fit from these results.

화면 블록: product_table(20 of 20)

**채점**: ✗ 실패 — 빠진 것: fact "41 reviews, average 4.6" (41, 4.6 not shown); fact "the most common phrase is 'size up for a hoodie' (9 mentions" (9 not shown)

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 2회차 · ✗ 실패

토큰 26,641 · 모델 호출 4회 · 도구 호출 2회

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

- 라우팅: Catalog agent (chosen by the model)
- 도구 검색 후보: 5 candidates: save_display_banner_list, get_display_corner_list, get_product_detail_info, get_product_detail_info_v2, get_product_grid_list
- 계획: `get_product_grid_list` `` {"page":1,"keyword":"wool overcoat"} ``; `get_product_detail_info_v2` `` {} ``
1. 에이전트 → **`get_product_grid_list`** `` {"page":1,"keyword":"wool overcoat"} ``
   ← 결과: `` {"list":[{"cost":120.0,"price":289.0,"stock":24,"brand_id":"brn_northwind","product_id":"prd_wool_overcoat","category_id":"cat_outerwear","availability":"in_stock","member_price":null,"product_name":"Wool overcoat"},{"cost":24.46,"price":59.0,"stock":23,"brand_id":"brn_ridgeline","product_id":"prd_scarves_04","category_id":"cat_scarves","availability":"in_stock","member_price":null,"product_name":"Wool stole"},{"cost":74.16,"price":149.0,"stock":89,"brand_id":"brn_northwind","product_id":"prd_pants_22","category_id":"cat_pants","availability":"in_stock","member_price":null,"product_name":"Wool… (+3,560자) ``
2. 에이전트 → **`get_product_detail_info_v2`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과: `` {"cost":120.0,"price":289.0,"stock":24,"brand_id":"brn_northwind","variants":[{"size":"S","color":"Charcoal","stock":5,"variant_id":"var_wool_overcoat_s_charcoal","availability":"in_stock"},{"size":"M","color":"Charcoal","stock":7,"variant_id":"var_wool_overcoat_m_charcoal","availability":"in_stock"},{"size":"L","color":"Charcoal","stock":8,"variant_id":"var_wool_overcoat_l_charcoal","availability":"in_stock"},{"size":"XL","color":"Charcoal","stock":4,"variant_id":"var_wool_overcoat_xl_charcoal","availability":"in_stock"}],"attributes":[{"unit":null,"value":"70% wool, 30% polyamide","attribute… (+182자) ``

**답변 1**
> The results show the Wool overcoat’s sizes and stock, but no fit feedback or sizing guidance. They don’t confirm whether it runs small.

화면 블록: product_table(20 of 20)

**채점**: ✗ 실패 — 빠진 것: fact "41 reviews, average 4.6" (41, 4.6 not shown); fact "the most common phrase is 'size up for a hoodie' (9 mentions" (9 not shown)

### GPT-6-Luna · a2api 변환 파사드 + 주문 번호 조회 · 3회차 · ✗ 실패

토큰 26,537 · 모델 호출 4회 · 도구 호출 2회

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

- 라우팅: Catalog agent (chosen by the model)
- 도구 검색 후보: 5 candidates: save_display_banner_list, get_display_corner_list, get_product_detail_info, get_product_detail_info_v2, get_product_grid_list
- 계획: `get_product_grid_list` `` {"keyword":"wool overcoat"} ``; `get_product_detail_info_v2` `` {} ``
1. 에이전트 → **`get_product_grid_list`** `` {"keyword":"wool overcoat"} ``
   ← 결과: `` {"list":[{"cost":120.0,"price":289.0,"stock":24,"brand_id":"brn_northwind","product_id":"prd_wool_overcoat","category_id":"cat_outerwear","availability":"in_stock","member_price":null,"product_name":"Wool overcoat"},{"cost":24.46,"price":59.0,"stock":23,"brand_id":"brn_ridgeline","product_id":"prd_scarves_04","category_id":"cat_scarves","availability":"in_stock","member_price":null,"product_name":"Wool stole"},{"cost":74.16,"price":149.0,"stock":89,"brand_id":"brn_northwind","product_id":"prd_pants_22","category_id":"cat_pants","availability":"in_stock","member_price":null,"product_name":"Wool… (+3,560자) ``
2. 에이전트 → **`get_product_detail_info_v2`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과: `` {"cost":120.0,"price":289.0,"stock":24,"brand_id":"brn_northwind","variants":[{"size":"S","color":"Charcoal","stock":5,"variant_id":"var_wool_overcoat_s_charcoal","availability":"in_stock"},{"size":"M","color":"Charcoal","stock":7,"variant_id":"var_wool_overcoat_m_charcoal","availability":"in_stock"},{"size":"L","color":"Charcoal","stock":8,"variant_id":"var_wool_overcoat_l_charcoal","availability":"in_stock"},{"size":"XL","color":"Charcoal","stock":4,"variant_id":"var_wool_overcoat_xl_charcoal","availability":"in_stock"}],"attributes":[{"unit":null,"value":"70% wool, 30% polyamide","attribute… (+182자) ``

**답변 1**
> The results show the Wool overcoat’s sizes and stock, but no customer feedback about fit. I can’t confirm whether it runs small from this information.

화면 블록: product_table(20 of 20)

**채점**: ✗ 실패 — 빠진 것: fact "41 reviews, average 4.6" (41, 4.6 not shown); fact "the most common phrase is 'size up for a hoodie' (9 mentions" (9 not shown)
