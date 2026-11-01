# md-overcoat-runs-small — ours-design-9

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> people keep saying the wool overcoat runs small. is that actually true?

- 필요한 도구: `get_review_summary`
- 허용 도구: `search_products`, `list_reviews`, `get_product_measurements`
- 답에 있어야 할 사실: 41 reviews, average 4.6
- 답에 있어야 할 사실: 29 say true to size, 12 say a bit snug, none say it runs large
- 답에 있어야 할 사실: the most common phrase is 'size up for a hoodie' (9 mentions), so the snug votes come from layering

### a2api-acom-hybrid · 1회차 · ✓ 통과

토큰 11,657 · 11.747초 · 모델 호출 2회 · 도구 호출 1회 · 첫 요청 프롬프트 5,334토큰

준비: 전략 `index`, 함수 253개, 목차 4,645자(system prompt)

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

1. 모델 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 940B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":null},"review_count":41,"rating_value":4.6,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":29},{"fit":"runs_small","label":"A bit snug","count":12},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[{"text":"size up for a hoodie","count":9}],"sample":[{"review_id":"rev_8812","review_rating":5,"size_bought":"L","height_cm":180,"excerpt":"Size up if you wear a hoodie underneath.","date_published":"2026-10-12"},{"review_id":"rev_8807","review_ra… (+340자) ``

**답변 1**
> The wool overcoat is not consistently reported as running small.
>
> From 41 reviews:
> * **Fit votes**
>   * True to size: 29
>   * A bit snug / runs small: 12
>   * Runs large: 0
> * Overall rating: 4.6 / 5
>
> The repeated theme is layering. The top mention is “size up for a hoodie” – 9 times.
>
> Sample evidence:
> * rev_8812 – 5★, size L, 180 cm: “Size up if you wear a hoodie underneath.”
> * rev_8807 – 5★, size L, 176 cm: “True to size over a shirt or a thin sweater; size up for a hoodie.”
> * rev_8803 – 5★, size L, 180 cm: “True to size over a shirt or a thin sweater; size up for a hoodie.”
>
> So most reviewers find it true to size for a shirt/thin sweater, with ~29% saying it runs a bit snug and recommending sizing up when layering.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-hybrid · 2회차 · ✓ 통과

토큰 11,657 · 11.694초 · 모델 호출 2회 · 도구 호출 1회 · 첫 요청 프롬프트 5,334토큰

준비: 전략 `index`, 함수 253개, 목차 4,645자(system prompt)

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

1. 모델 → **`get_review_summary`** `` {"product_id":"prd_wool_overcoat"} ``
   ← 결과 940B: `` {"status":"succeeded","data":{"product_id":"prd_wool_overcoat","filter":{"height_min_cm":null,"height_max_cm":null,"size":null},"review_count":41,"rating_value":4.6,"fit_votes":[{"fit":"true_to_size","label":"True to size","count":29},{"fit":"runs_small","label":"A bit snug","count":12},{"fit":"runs_large","label":"Runs large","count":0}],"mentions":[{"text":"size up for a hoodie","count":9}],"sample":[{"review_id":"rev_8812","review_rating":5,"size_bought":"L","height_cm":180,"excerpt":"Size up if you wear a hoodie underneath.","date_published":"2026-10-12"},{"review_id":"rev_8807","review_ra… (+340자) ``

**답변 1**
> The wool overcoat is not consistently reported as running small.
>
> From 41 reviews:
> * **Fit votes**
>   * True to size: 29
>   * A bit snug / runs small: 12
>   * Runs large: 0
> * Overall rating: 4.6 / 5
>
> The repeated theme is layering. The top mention is “size up for a hoodie” – 9 times.
>
> Sample evidence:
> * rev_8812 – 5★, size L, 180 cm: “Size up if you wear a hoodie underneath.”
> * rev_8807 – 5★, size L, 176 cm: “True to size over a shirt or a thin sweater; size up for a hoodie.”
> * rev_8803 – 5★, size L, 180 cm: “True to size over a shirt or a thin sweater; size up for a hoodie.”
>
> So most reviewers find it true to size for a shirt/thin sweater, with ~29% saying it runs a bit snug and recommending sizing up when layering.

**채점**: ✓ 통과
(도구 정밀도 1.00, 재현율 1.00)
