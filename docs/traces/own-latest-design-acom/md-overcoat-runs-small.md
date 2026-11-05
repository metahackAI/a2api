# md-overcoat-runs-small — own-latest-design-acom

[← 실행 묶음](README.md)

**과업**

> people keep saying the wool overcoat runs small. is that actually true?

- 답에 있어야 할 사실: 41 reviews, average 4.6
- 답에 있어야 할 사실: 29 say true to size, 12 say a bit snug, none say it runs large
- 답에 있어야 할 사실: the most common phrase is 'size up for a hoodie' (9 mentions), so the snug votes come from layering

### A-Commerce 도구(참고) · 1회차 · ✓ 통과

토큰 8,770 · 모델 호출 3회 · 도구 호출 2회

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

- 라우팅: Catalog agent (chosen by the model)
- 도구 검색 후보: 12 candidates: search_products, get_product, get_inventory, list_tasks, get_review_summary, schedule_banner, verify_change_set, list_display_slots, get_task, approve_product, schedule_display, suggest_reorder
- 계획: `search_products` `` {"query":"wool overcoat"} ``; `get_review_summary` `` {"product_id":"from find_overcoat","sample_limit":3} ``
1. 에이전트 → **`search_products`** `` {"query":"wool overcoat"} ``
   ← 결과: `` {"items":[{"id":"prd_wool_overcoat","cost":120.0,"name":"Wool overcoat","image":"/media/products/prd_wool_overcoat-b50a91c0.webp","price":289.0,"brand_id":"brn_northwind","category_id":"cat_outerwear","has_variant":[{"sku":"wo-charcoal-s","size":"S","color":"Charcoal","variant_id":"var_wool_overcoat_s_charcoal","availability":"in_stock","inventory_level":5},{"sku":"wo-charcoal-m","size":"M","color":"Charcoal","variant_id":"var_wool_overcoat_m_charcoal","availability":"in_stock","inventory_level":7},{"sku":"wo-charcoal-l","size":"L","color":"Charcoal","variant_id":"var_wool_overcoat_l_charcoal"… (+27,227자) ``
2. 에이전트 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat","sample_limit":3} ``
   ← 결과: `` {"filter":{"size":null,"height_max_cm":null,"height_min_cm":null},"sample":[{"excerpt":"Size up if you wear a hoodie underneath.","height_cm":180,"review_id":"rev_8812","size_bought":"L","review_rating":5,"date_published":"2026-10-12"},{"excerpt":"True to size over a shirt or a thin sweater; size up for a hoodie.","height_cm":176,"review_id":"rev_8807","size_bought":"L","review_rating":5,"date_published":"2026-08-27"},{"excerpt":"True to size over a shirt or a thin sweater; size up for a hoodie.","height_cm":180,"review_id":"rev_8803","size_bought":"L","review_rating":5,"date_published":"2026-… (+310자) ``

**답변 1**
> The Wool overcoat has 41 reviews with a 4.6 rating. Fit votes show 29 True to size, 12 A bit snug, and 0 Runs large. Mentions include size up for a hoodie, 9 times. Sample reviews say true to size over a shirt or thin sweater; size up for a hoodie.

화면 블록: product_table(20 of 39)

**채점**: ✓ 통과

### A-Commerce 도구(참고) · 2회차 · ✗ 실패

토큰 8,754 · 모델 호출 3회 · 도구 호출 2회

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

- 라우팅: Catalog agent (chosen by the model)
- 도구 검색 후보: 12 candidates: search_products, get_product, get_inventory, list_tasks, get_review_summary, schedule_banner, verify_change_set, list_display_slots, get_task, approve_product, schedule_display, suggest_reorder
- 계획: `search_products` `` {"query":"wool overcoat"} ``; `get_review_summary` `` {"product_id":"from find_overcoat","sample_limit":3} ``
1. 에이전트 → **`search_products`** `` {"query":"wool overcoat"} ``
   ← 결과: `` {"items":[{"id":"prd_wool_overcoat","cost":120.0,"name":"Wool overcoat","image":"/media/products/prd_wool_overcoat-b50a91c0.webp","price":289.0,"brand_id":"brn_northwind","category_id":"cat_outerwear","has_variant":[{"sku":"wo-charcoal-s","size":"S","color":"Charcoal","variant_id":"var_wool_overcoat_s_charcoal","availability":"in_stock","inventory_level":5},{"sku":"wo-charcoal-m","size":"M","color":"Charcoal","variant_id":"var_wool_overcoat_m_charcoal","availability":"in_stock","inventory_level":7},{"sku":"wo-charcoal-l","size":"L","color":"Charcoal","variant_id":"var_wool_overcoat_l_charcoal"… (+27,227자) ``
2. 에이전트 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat","sample_limit":3} ``
   ← 결과: `` {"filter":{"size":null,"height_max_cm":null,"height_min_cm":null},"sample":[{"excerpt":"Size up if you wear a hoodie underneath.","height_cm":180,"review_id":"rev_8812","size_bought":"L","review_rating":5,"date_published":"2026-10-12"},{"excerpt":"True to size over a shirt or a thin sweater; size up for a hoodie.","height_cm":176,"review_id":"rev_8807","size_bought":"L","review_rating":5,"date_published":"2026-08-27"},{"excerpt":"True to size over a shirt or a thin sweater; size up for a hoodie.","height_cm":180,"review_id":"rev_8803","size_bought":"L","review_rating":5,"date_published":"2026-… (+310자) ``

**답변 1**
> The Wool overcoat has 41 reviews with a 4.6 rating. Fit votes show 29 True to size, 12 A bit snug, and 0 Runs large. Mentions include size up for a hoodie, with sample reviews noting true to size over a shirt or thin sweater and size up for a hoodie.

화면 블록: product_table(20 of 39)

**채점**: ✗ 실패 — 빠진 것: fact "the most common phrase is 'size up for a hoodie' (9 mentions" (9 not shown)

### A-Commerce 도구(참고) · 3회차 · ✓ 통과

토큰 8,757 · 모델 호출 3회 · 도구 호출 2회

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

- 라우팅: Catalog agent (chosen by the model)
- 도구 검색 후보: 12 candidates: search_products, get_product, get_inventory, list_tasks, get_review_summary, schedule_banner, verify_change_set, list_display_slots, get_task, approve_product, schedule_display, suggest_reorder
- 계획: `search_products` `` {"query":"wool overcoat"} ``; `get_review_summary` `` {"product_id":"from find_overcoat","sample_limit":3} ``
1. 에이전트 → **`search_products`** `` {"query":"wool overcoat"} ``
   ← 결과: `` {"items":[{"id":"prd_wool_overcoat","cost":120.0,"name":"Wool overcoat","image":"/media/products/prd_wool_overcoat-b50a91c0.webp","price":289.0,"brand_id":"brn_northwind","category_id":"cat_outerwear","has_variant":[{"sku":"wo-charcoal-s","size":"S","color":"Charcoal","variant_id":"var_wool_overcoat_s_charcoal","availability":"in_stock","inventory_level":5},{"sku":"wo-charcoal-m","size":"M","color":"Charcoal","variant_id":"var_wool_overcoat_m_charcoal","availability":"in_stock","inventory_level":7},{"sku":"wo-charcoal-l","size":"L","color":"Charcoal","variant_id":"var_wool_overcoat_l_charcoal"… (+27,227자) ``
2. 에이전트 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat","sample_limit":3} ``
   ← 결과: `` {"filter":{"size":null,"height_max_cm":null,"height_min_cm":null},"sample":[{"excerpt":"Size up if you wear a hoodie underneath.","height_cm":180,"review_id":"rev_8812","size_bought":"L","review_rating":5,"date_published":"2026-10-12"},{"excerpt":"True to size over a shirt or a thin sweater; size up for a hoodie.","height_cm":176,"review_id":"rev_8807","size_bought":"L","review_rating":5,"date_published":"2026-08-27"},{"excerpt":"True to size over a shirt or a thin sweater; size up for a hoodie.","height_cm":180,"review_id":"rev_8803","size_bought":"L","review_rating":5,"date_published":"2026-… (+310자) ``

**답변 1**
> The Wool overcoat has 41 reviews with a 4.6 rating. Fit votes show 29 True to size, 12 A bit snug, and 0 Runs large. Mentions include size up for a hoodie, 9 times. Sample reviews say true to size over a shirt or thin sweater; size up for a hoodie.

화면 블록: product_table(20 of 39)

**채점**: ✓ 통과
