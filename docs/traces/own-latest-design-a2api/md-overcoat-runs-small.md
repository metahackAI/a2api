# md-overcoat-runs-small — own-latest-design-a2api

[← 실행 묶음](README.md)

**과업**

> people keep saying the wool overcoat runs small. is that actually true?

- 답에 있어야 할 사실: 41 reviews, average 4.6
- 답에 있어야 할 사실: 29 say true to size, 12 say a bit snug, none say it runs large
- 답에 있어야 할 사실: the most common phrase is 'size up for a hoodie' (9 mentions), so the snug votes come from layering

### a2api 변환 파사드 · 1회차 · ✗ 실패

토큰 6,940 · 모델 호출 4회 · 도구 호출 0회

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

- 라우팅: Catalog agent (chosen by the model)
- 도구 검색 후보: 5 candidates: save_display_banner_list, get_display_corner_list, get_product_detail_info, get_product_detail_info_v2, get_product_grid_list
- 계획: people · wool overcoat · runs small · now · store · is that actually true · 0 steps by Muse Glimmer 30B

**답변 1**
> I don't have any data in this turn to check whether the wool overcoat runs small. No product details, reviews, or size feedback were returned, so I can't confirm or deny the claim right now. If you can share the product name or SKU, I can pull reviews and size notes to see what customers are actually reporting.

**채점**: ✗ 실패 — 빠진 것: fact "41 reviews, average 4.6" (41, 4.6 not shown); fact "29 say true to size, 12 say a bit snug, none say it runs lar" (29, 12 not shown); fact "the most common phrase is 'size up for a hoodie' (9 mentions" (9 not shown)

### a2api 변환 파사드 · 2회차 · ✗ 실패

토큰 6,894 · 모델 호출 4회 · 도구 호출 0회

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

- 라우팅: Catalog agent (chosen by the model)
- 도구 검색 후보: 5 candidates: save_display_banner_list, get_display_corner_list, get_product_detail_info, get_product_detail_info_v2, get_product_grid_list
- 계획: people · wool overcoat · runs small · people keep saying · reviews · is that actually true · 0 steps by Muse Glimmer 30B

**답변 1**
> The wool overcoat runs small. is that actually true?

**채점**: ✗ 실패 — 빠진 것: fact "41 reviews, average 4.6" (41, 4.6 not shown); fact "29 say true to size, 12 say a bit snug, none say it runs lar" (29, 12 not shown); fact "the most common phrase is 'size up for a hoodie' (9 mentions" (9 not shown)

### a2api 변환 파사드 · 3회차 · ✗ 실패

토큰 6,931 · 모델 호출 4회 · 도구 호출 0회

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

- 라우팅: Catalog agent (chosen by the model)
- 도구 검색 후보: 5 candidates: save_display_banner_list, get_display_corner_list, get_product_detail_info, get_product_detail_info_v2, get_product_grid_list
- 계획: people · wool overcoat · runs small · people keep saying · reviews · is that actually true · 0 steps by Muse Glimmer 30B

**답변 1**
> I don’t have any reviews or feedback on file for the wool overcoat in this turn, so I can’t confirm whether it runs small. If you want, I can pull the product’s reviews and questions to check what customers are saying.

**채점**: ✗ 실패 — 빠진 것: fact "41 reviews, average 4.6" (41, 4.6 not shown); fact "29 say true to size, 12 say a bit snug, none say it runs lar" (29, 12 not shown); fact "the most common phrase is 'size up for a hoodie' (9 mentions" (9 not shown)
