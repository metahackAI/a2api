# b3-why-sales-dropped — ours-design-11

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `d86a1ff` · a2api `140fda2`

**과업**

> Why did sales drop yesterday?

- 필요한 도구: `explain_sales_change`
- 허용 도구: `get_sales_trend`, `get_sales_overview`, `search_products`, `get_inventory`
- 답에 있어야 할 사실: Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$4,660, -20%); 201 orders against 247
- 답에 있어야 할 사실: M and L sold out on the three best sellers (chore coat, rain parka, denim jacket): about -$2,700
- 답에 있어야 할 사실: the weekly email did not go out (Thu 08:00 list import failed): about -$1,300; -$660 is not explained

### a2api-acom-names-batch · 1회차 · ✗ 실패

토큰 12,009 · 21.466초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 1,975토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> Why did sales drop yesterday?

1. 모델 → **`a2api_load`** `` {"names":["get_sales_overview","get_sales_trend","explain_sales_change"]} ``
   ← 결과 74B: `` {"loaded":["get_sales_overview","get_sales_trend","explain_sales_change"]} ``
2. 모델 → **`explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue"} ``
   ← 결과 2,167B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+900자) ``

**답변 1**
> Yesterday = Thu 2026-11-05
>
> * Revenue: $18,240 on 201 orders
> * Same-weekday last 4 weeks average: $22,900 on 247 orders
> * Change: -$4,660 / -20.35%
>
> Explained gap:
>
> * **out_of_stock – $2,700**
>   3 bestsellers out of M and L since Wed 2026-11-04 15:00 ET
>   - Cotton chore coat `prd_chore_coat` M/L – expected $1,313.5, actual $0. Availability starts 2026-11-12 00:00-05:00
>   - Denim jacket `prd_denim_jacket` M/L – expected $796.5, actual $0. Availability starts 2026-11-12 00:00-05:00
>   - Light rain parka `prd_rain_parka` M/L – expected $590.0, actual $0. Availability starts null
>
> * **campaign_not_sent – $1,300**
>   Weekly email `cmp_weekly_1105` scheduled 2026-11-05 08:00-05:00 failed – “List import failed”. Expected $1,300, actual $0. Compared with cmp_weekly_1008, cmp_weekly_1015, cmp_weekly_1022, cmp_weekly_1029.
>
> Unexplained: -$660
>
> Total explained = -$4,000 of the -$4,660 gap.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-batch · 2회차 · ✗ 실패

토큰 12,009 · 21.714초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 1,975토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> Why did sales drop yesterday?

1. 모델 → **`a2api_load`** `` {"names":["get_sales_overview","get_sales_trend","explain_sales_change"]} ``
   ← 결과 74B: `` {"loaded":["get_sales_overview","get_sales_trend","explain_sales_change"]} ``
2. 모델 → **`explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue"} ``
   ← 결과 2,167B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+900자) ``

**답변 1**
> Yesterday = Thu 2026-11-05
>
> * Revenue: $18,240 on 201 orders
> * Same-weekday last 4 weeks average: $22,900 on 247 orders
> * Change: -$4,660 / -20.35%
>
> Explained gap:
>
> * **out_of_stock – $2,700**
>   3 bestsellers out of M and L since Wed 2026-11-04 15:00 ET
>   - Cotton chore coat `prd_chore_coat` M/L – expected $1,313.5, actual $0. Availability starts 2026-11-12 00:00-05:00
>   - Denim jacket `prd_denim_jacket` M/L – expected $796.5, actual $0. Availability starts 2026-11-12 00:00-05:00
>   - Light rain parka `prd_rain_parka` M/L – expected $590.0, actual $0. Availability starts null
>
> * **campaign_not_sent – $1,300**
>   Weekly email `cmp_weekly_1105` scheduled 2026-11-05 08:00-05:00 failed – “List import failed”. Expected $1,300, actual $0. Compared with cmp_weekly_1008, cmp_weekly_1015, cmp_weekly_1022, cmp_weekly_1029.
>
> Unexplained: -$660
>
> Total explained = -$4,000 of the -$4,660 gap.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown)
(도구 정밀도 1.00, 재현율 1.00)
