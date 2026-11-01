# b3-why-sales-dropped — ours-design-9

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> Why did sales drop yesterday?

- 필요한 도구: `explain_sales_change`
- 허용 도구: `get_sales_trend`, `get_sales_overview`, `search_products`, `get_inventory`
- 답에 있어야 할 사실: Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$4,660, -20%); 201 orders against 247
- 답에 있어야 할 사실: M and L sold out on the three best sellers (chore coat, rain parka, denim jacket): about -$2,700
- 답에 있어야 할 사실: the weekly email did not go out (Thu 08:00 list import failed): about -$1,300; -$660 is not explained

### a2api-acom-hybrid · 1회차 · ✗ 실패

토큰 13,907 · 21.624초 · 모델 호출 2회 · 도구 호출 1회 · 첫 요청 프롬프트 5,918토큰

준비: 전략 `index`, 함수 253개, 목차 4,645자(system prompt)

**질문 1**
> Why did sales drop yesterday?

1. 모델 → **`explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue","max_causes":5} ``
   ← 결과 2,167B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+900자) ``

**답변 1**
> Yesterday (Thu 2026-11-05, store time) revenue was $18,240 on 201 orders vs the same weekday last 4 weeks average $22,900 on 247 orders.
>
> Gap: -$4,660 revenue, -20.35% vs basis.
>
> Explained causes from the data:
>
> * **Out of stock – 3 bestsellers M/L since Wed Nov 4 15:00** – -$2,700
>   * prd_chore_coat – Cotton chore coat, sizes M, L. Sold out 2026-11-04T15:00:00-05:00, availability starts 2026-11-12T00:00:00-05:00. Expected $1,313.50, actual $0
>   * prd_denim_jacket – Denim jacket, sizes M, L. Sold out 2026-11-04T15:00:00-05:00, availability starts 2026-11-12T00:00:00-05:00. Expected $796.50, actual $0
>   * prd_rain_parka – Light rain parka, sizes M, L. Sold out 2026-11-04T15:00:00-05:00, availability starts null. Expected $590.00, actual $0
>
> * **Campaign not sent** – -$1,300
>   * cmp_weekly_1105 – Weekly email, channel email, scheduled 2026-11-05T08:00:00-05:00
>   * Status: failed – error_message: List import failed
>   * Expected lift $1,300 vs the four prior weekly emails cmp_weekly_1008, cmp_weekly_1015, cmp_weekly_1022, cmp_weekly_1029; actual $0
>
> Unexplained remainder: -$660
>
> So ~ $4,000 of the $4,660 drop is accounted for by the stock-outs of the three bestsellers and the failed weekly email send.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-hybrid · 2회차 · ✗ 실패

토큰 13,907 · 21.422초 · 모델 호출 2회 · 도구 호출 1회 · 첫 요청 프롬프트 5,918토큰

준비: 전략 `index`, 함수 253개, 목차 4,645자(system prompt)

**질문 1**
> Why did sales drop yesterday?

1. 모델 → **`explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue","max_causes":5} ``
   ← 결과 2,167B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+900자) ``

**답변 1**
> Yesterday (Thu 2026-11-05, store time) revenue was $18,240 on 201 orders vs the same weekday last 4 weeks average $22,900 on 247 orders.
>
> Gap: -$4,660 revenue, -20.35% vs basis.
>
> Explained causes from the data:
>
> * **Out of stock – 3 bestsellers M/L since Wed Nov 4 15:00** – -$2,700
>   * prd_chore_coat – Cotton chore coat, sizes M, L. Sold out 2026-11-04T15:00:00-05:00, availability starts 2026-11-12T00:00:00-05:00. Expected $1,313.50, actual $0
>   * prd_denim_jacket – Denim jacket, sizes M, L. Sold out 2026-11-04T15:00:00-05:00, availability starts 2026-11-12T00:00:00-05:00. Expected $796.50, actual $0
>   * prd_rain_parka – Light rain parka, sizes M, L. Sold out 2026-11-04T15:00:00-05:00, availability starts null. Expected $590.00, actual $0
>
> * **Campaign not sent** – -$1,300
>   * cmp_weekly_1105 – Weekly email, channel email, scheduled 2026-11-05T08:00:00-05:00
>   * Status: failed – error_message: List import failed
>   * Expected lift $1,300 vs the four prior weekly emails cmp_weekly_1008, cmp_weekly_1015, cmp_weekly_1022, cmp_weekly_1029; actual $0
>
> Unexplained remainder: -$660
>
> So ~ $4,000 of the $4,660 drop is accounted for by the stock-outs of the three bestsellers and the failed weekly email send.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8 not shown)
(도구 정밀도 1.00, 재현율 1.00)
