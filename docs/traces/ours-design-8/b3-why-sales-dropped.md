# b3-why-sales-dropped — ours-design-8

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> Why did sales drop yesterday?

- 필요한 도구: `explain_sales_change`
- 허용 도구: `get_sales_trend`, `get_sales_overview`, `search_products`, `get_inventory`
- 답에 있어야 할 사실: Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$4,660, -20%); 201 orders against 247
- 답에 있어야 할 사실: M and L sold out on the three best sellers (chore coat, rain parka, denim jacket): about -$2,700
- 답에 있어야 할 사실: the weekly email did not go out (Thu 08:00 list import failed): about -$1,300; -$660 is not explained

### a2api-acom-names · 1회차 · ✗ 실패

토큰 10,555 · 20.463초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 1,621토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> Why did sales drop yesterday?

1. 모델 → **`a2api_load`** `` {"names":["explain_sales_change","get_sales_overview","get_sales_trend"]} ``
   ← 결과 74B: `` {"loaded":["explain_sales_change","get_sales_overview","get_sales_trend"]} ``
2. 모델 → **`explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue"} ``
   ← 결과 2,320B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+900자) ``

**답변 1**
> Yesterday = 2026-11-05, store time.
>
> Revenue
> * 2026-11-05: $18,240  / 201 orders
> * Same weekday last 4 weeks avg: $22,900 / 247 orders
> * Gap: -$4,660  / -20.35%
>
> Explained causes for the revenue drop:
>
> 1. **Out of stock – 3 bestsellers M/L since Wed Nov 4 15:00 ET**
>    * Impact: -$2,700
>    * prd_chore_coat – Cotton chore coat, sizes M, L. Sold out 2026-11-04T15:00:00-05:00, availability starts 2026-11-12T00:00:00-05:00. Expected $1,313.5 → actual $0
>    * prd_denim_jacket – Denim jacket, sizes M, L. Sold out 2026-11-04T15:00:00-05:00, availability starts 2026-11-12T00:00:00-05:00. Expected $796.5 → actual $0
>    * prd_rain_parka – Light rain parka, sizes M, L. Sold out 2026-11-04T15:00:00-05:00, availability starts null. Expected $590 → actual $0
>
> 2. **Campaign not sent**
>    * Weekly email cmp_weekly_1105 failed to send 2026-11-05T08:00:00-05:00
>    * Error: List import failed
>    * Impact: -$1,300  Expected $1,300 → actual $0
>    * Compared with cmp_weekly_1008, cmp_weekly_1015, cmp_weekly_1022, cmp_weekly_1029
>
> Unexplained remainder: -$660
>
> Total explained: -$4,000 of the -$4,660 gap.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names · 2회차 · ✗ 실패

토큰 10,586 · 20.939초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 1,621토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> Why did sales drop yesterday?

1. 모델 → **`a2api_load`** `` {"names":["explain_sales_change","get_sales_overview","get_sales_trend"]} ``
   ← 결과 74B: `` {"loaded":["explain_sales_change","get_sales_overview","get_sales_trend"]} ``
2. 모델 → **`explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue","max_causes":5} ``
   ← 결과 2,320B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+900자) ``

**답변 1**
> Yesterday = 2026-11-05 (store day)
>
> * Revenue: $18,240 on 201 orders
> * Same-weekday last 4 weeks average: $22,900 on 247 orders
> * Change: -$4,660 revenue, -20.35%
>
> Explained causes for the revenue gap:
>
> 1. **Out of stock – 3 bestsellers M/L**
>    * Cotton chore coat M/L, Denim jacket M/L, Light rain parka M/L sold out since Wed 2026-11-04 15:00 ET
>    * Impact: -$2,700
>      * Cotton chore coat expected $1,313.5 → actual $0.0, availability starts 2026-11-12
>      * Denim jacket expected $796.5 → actual $0.0, availability starts 2026-11-12
>      * Light rain parka expected $590.0 → actual $0.0, availability starts null
>
> 2. **Campaign not sent**
>    * Weekly email cmp_weekly_1105 scheduled 2026-11-05 08:00 ET failed – “List import failed”
>    * Impact: -$1,300 vs the same weekly emails on 2026-10-08 / 10-15 / 10-22 / 10-29
>
> Unexplained remainder: -$660
>
> Total explained gap = -$4,000 of the -$4,660 drop.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-norelated · 1회차 · ✗ 실패

토큰 11,433 · 20.677초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 1,621토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> Why did sales drop yesterday?

1. 모델 → **`a2api_load`** `` {"names":["explain_sales_change","get_sales_overview","get_sales_trend","get_cs_overview"]} ``
   ← 결과 92B: `` {"loaded":["explain_sales_change","get_sales_overview","get_sales_trend","get_cs_overview"]} ``
2. 모델 → **`explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue","max_causes":5} ``
   ← 결과 2,167B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+900자) ``

**답변 1**
> Yesterday = store day 2026-11-05.
>
> * Revenue: $18,240 on 201 orders
> * Same-weekday last 4 weeks average: $22,900 on 247 orders
> * Change: -$4,660 revenue, -20.35%
>
> Explained causes for the revenue gap:
>
> 1. **Out of stock – 3 bestsellers M/L since Wed Nov 4 15:00 ET**
>    * Impact: -$2,700
>    * prd_chore_coat – Cotton chore coat, sizes M, L. Bestseller. Sold out 2026-11-04T15:00:00-05:00, availability starts 2026-11-12T00:00:00-05:00. Expected $1,313.5, actual $0
>    * prd_denim_jacket – Denim jacket, sizes M, L. Bestseller. Sold out 2026-11-04T15:00:00-05:00, availability starts 2026-11-12T00:00:00-05:00. Expected $796.5, actual $0
>    * prd_rain_parka – Light rain parka, sizes M, L. Bestseller. Sold out 2026-11-04T15:00:00-05:00, availability starts null. Expected $590.0, actual $0
>
> 2. **Campaign not sent**
>    * Weekly email cmp_weekly_1105 not sent. Scheduled 2026-11-05T08:00:00-05:00, status failed, error: List import failed
>    * Impact: -$1,300. Expected $1,300, actual $0. Compared with cmp_weekly_1008, cmp_weekly_1015, cmp_weekly_1022, cmp_weekly_1029
>
> Unexplained remainder: -$660
>
> So the drop is mainly the stock-out of the three bestsellers in M/L and the missed weekly email on 2026-11-05.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-norelated · 2회차 · ✗ 실패

토큰 10,605 · 20.944초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 1,621토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> Why did sales drop yesterday?

1. 모델 → **`a2api_load`** `` {"names":["explain_sales_change","get_sales_overview","get_sales_trend"]} ``
   ← 결과 74B: `` {"loaded":["explain_sales_change","get_sales_overview","get_sales_trend"]} ``
2. 모델 → **`explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue","max_causes":5} ``
   ← 결과 2,167B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+900자) ``

**답변 1**
> Yesterday = Thu 2026-11-05, store time.
>
> Revenue was $18,240 on 201 paid orders vs the same-weekday last-4-weeks average of $22,900 on 247 orders.
> Change: -$4,660 revenue, -20.35% vs the 4-week weekday average.
>
> Explained causes for the revenue gap:
>
> * **Out of stock – 3 bestsellers M/L since Wed Nov 4 15:00 ET**  
>   -$2,700 revenue vs expected
>   * prd_chore_coat – Cotton chore coat, sizes M, L. Bestseller. Sold out 2026-11-04T15:00:00-05:00, availability starts 2026-11-12T00:00:00-05:00. Expected $1,313.5, actual $0
>   * prd_denim_jacket – Denim jacket, sizes M, L. Bestseller. Sold out 2026-11-04T15:00:00-05:00, availability starts 2026-11-12T00:00:00-05:00. Expected $796.5, actual $0
>   * prd_rain_parka – Light rain parka, sizes M, L. Bestseller. Sold out 2026-11-04T15:00:00-05:00, availability starts null. Expected $590.0, actual $0
>
> * **Campaign not sent**  
>   -$1,300 revenue vs expected
>   * cmp_weekly_1105 – Weekly email, channel email. Scheduled 2026-11-05T08:00:00-05:00, status failed. Error: List import failed. Compared with cmp_weekly_1008, cmp_weekly_1015, cmp_weekly_1022, cmp_weekly_1029.
>
> Unexplained remainder: -$660.
>
> So the drop is mainly the stock-out of the three M/L bestsellers from 4 Nov 15:00 onward and the failed weekly email send on 5 Nov 08:00.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown)
(도구 정밀도 1.00, 재현율 1.00)
