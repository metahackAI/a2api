# b3-why-sales-dropped — ours-design-7

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `7e1557b` · a2api `d8f82a8`

**과업**

> Why did sales drop yesterday?

- 필요한 도구: `explain_sales_change`
- 허용 도구: `get_sales_trend`, `get_sales_overview`, `search_products`, `get_inventory`
- 답에 있어야 할 사실: Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$4,660, -20%); 201 orders against 247
- 답에 있어야 할 사실: M and L sold out on the three best sellers (chore coat, rain parka, denim jacket): about -$2,700
- 답에 있어야 할 사실: the weekly email did not go out (Thu 08:00 list import failed): about -$1,300; -$660 is not explained

### a2api-acom · 1회차 · ✗ 실패

토큰 11,748 · 18.051초 · 모델 호출 2회 · 도구 호출 1회 · 첫 요청 프롬프트 4,941토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> Why did sales drop yesterday?

1. 모델 → **`acom_explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue","max_causes":5} ``
   ← 결과 2,167B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+900자) ``

**답변 1**
> Yesterday 2026-11-05 revenue was $18,240 on 201 orders vs the same weekday last 4 weeks average $22,900 on 247 orders.
> Gap: -$4,660 revenue, -20.35%.
>
> Explained causes:
>
> * **Out of stock – $2,700**
>   3 bestsellers out of M and L since Wed Nov 4 15:00 ET
>   - prd_chore_coat Cotton chore coat M/L – expected $1,313.50, actual $0.00; availability starts 2026-11-12
>   - prd_denim_jacket Denim jacket M/L – expected $796.50, actual $0.00; availability starts 2026-11-12
>   - prd_rain_parka Light rain parka M/L – expected $590.00, actual $0.00; availability starts null
>
> * **Campaign not sent – $1,300**
>   cmp_weekly_1105 Weekly email, channel email, scheduled 2026-11-05T08:00:00-05:00
>   Status: failed – List import failed. Expected $1,300 vs $0 actual. Compared with cmp_weekly_1008, cmp_weekly_1015, cmp_weekly_1022, cmp_weekly_1029.
>
> Unexplained: -$660
>
> Total explained gap = -$4,000 of the -$4,660 drop.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom · 2회차 · ✗ 실패

토큰 11,674 · 16.757초 · 모델 호출 2회 · 도구 호출 1회 · 첫 요청 프롬프트 4,941토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> Why did sales drop yesterday?

1. 모델 → **`acom_explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue","max_causes":5} ``
   ← 결과 2,167B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+900자) ``

**답변 1**
> Yesterday 2026-11-05 revenue was $18,240 on 201 orders vs the same weekday average over the last 4 weeks $22,900 on 247 orders. That is –$4,660 / –20.4%.
>
> Explained causes from the data:
>
> * **Out of stock – $2,700**
>   3 bestsellers sold out in sizes M and L since Wed Nov 4 15:00 ET
>   - prd_chore_coat Cotton chore coat M/L – expected $1,313.5, actual $0.0; availability starts 2026-11-12
>   - prd_denim_jacket Denim jacket M/L – expected $796.5, actual $0.0; availability starts 2026-11-12
>   - prd_rain_parka Light rain parka M/L – expected $590.0, actual $0.0; availability starts null
>
> * **Campaign not sent – $1,300**
>   cmp_weekly_1105 Weekly email, channel email, scheduled 2026-11-05T08:00:00-05:00
>   Status: failed – “List import failed”. Expected $1,300 vs actual $0.0. Compared with cmp_weekly_1008, cmp_weekly_1015, cmp_weekly_1022, cmp_weekly_1029.
>
> Unexplained remainder: –$660.
>
> Total explained gap = –$4,000, leaving –$660 unexplained of the –$4,660 drop.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-index · 1회차 · ✗ 실패

토큰 24,301 · 19.687초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 6,980토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> Why did sales drop yesterday?

1. 모델 → **`a2api_load`** `` {"names":["explain_sales_change"]} ``
   ← 결과 35B: `` {"loaded":["explain_sales_change"]} ``
2. 모델 → **`explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks"} ``
   ← 결과 2,167B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+900자) ``

**답변 1**
> Yesterday Thu 2026-11-05 sales were down vs the same weekday average of the last 4 weeks.
>
> * Period revenue: $18,240 on 201 orders
> * Same-weekday last 4 weeks average: $22,900 on 247 orders
> * Gap: -$4,660 revenue, -20.4%
>
> Explained causes:
>
> 1. **Out of stock – $2,700 lost**
>    3 bestsellers lost sizes M and L from Wed 2026-11-04 15:00 ET onward
>    * Cotton chore coat – M/L, bestseller. Expected $1,313.5, actual $0. Availability starts 2026-11-12 00:00 ET
>    * Denim jacket – M/L, bestseller. Expected $796.5, actual $0. Availability starts 2026-11-12 00:00 ET
>    * Light rain parka – M/L, bestseller. Expected $590.0, actual $0. Availability starts unknown
>
> 2. **Campaign not sent – $1,300 lost**
>    Weekly email cmp_weekly_1105 scheduled 2026-11-05 08:00 ET failed: “List import failed”. Expected $1,300, actual $0. Compared with cmp_weekly_1008, 1015, 1022, 1029.
>
> Unexplained remainder: -$660.
>
> Total explained ≈ $4,000 of the $4,660 drop.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-index · 2회차 · ✗ 실패

토큰 24,250 · 17.428초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 6,980토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> Why did sales drop yesterday?

1. 모델 → **`a2api_load`** `` {"names":["explain_sales_change"]} ``
   ← 결과 35B: `` {"loaded":["explain_sales_change"]} ``
2. 모델 → **`explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue"} ``
   ← 결과 2,167B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+900자) ``

**답변 1**
> Sales were down on Thu 2026-11-05 vs the same weekday average over the last 4 weeks.
>
> * Period revenue: $18,240 on 201 orders
> * Same-weekday 4-week average: $22,900 on 247 orders
> * Gap: -$4,660 revenue, -20.4%
>
> Explained causes from the data:
>
> * **Out of stock – $2,700 lost**
>   3 bestsellers sold out of M and L since Wed 2026-11-04 15:00 ET
>   - Cotton chore coat, M/L, bestseller – expected $1,313.5, actual $0. Availability starts 2026-11-12
>   - Denim jacket, M/L, bestseller – expected $796.5, actual $0. Availability starts 2026-11-12
>   - Light rain parka, M/L, bestseller – expected $590.0, actual $0. Availability starts null
>
> * **Campaign not sent – $1,300 lost**
>   Weekly email cmp_weekly_1105 failed to send at 2026-11-05 08:00 ET. Error: List import failed. Expected $1,300 vs $0 actual. Compared with cmp_weekly_1008, cmp_weekly_1015, cmp_weekly_1022, cmp_weekly_1029.
>
> Unexplained remainder: -$660.
>
> Total explained loss $4,000 of the $4,660 gap.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-graph · 1회차 · ✗ 실패

토큰 24,255 · 16.567초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 6,980토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> Why did sales drop yesterday?

1. 모델 → **`a2api_load`** `` {"names":["explain_sales_change"]} ``
   ← 결과 35B: `` {"loaded":["explain_sales_change"]} ``
2. 모델 → **`explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue"} ``
   ← 결과 2,320B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+900자) ``

**답변 1**
> Yesterday 2026-11-05 revenue was $18,240 on 201 orders vs the same weekday average over the last 4 weeks $22,900 on 247 orders. That is –$4,660 / –20.4%.
>
> Explained causes:
>
> * **Out of stock – $2,700**
> 3 bestsellers lost sizes M/L since Wed 2026-11-04 15:00 ET
>   * Cotton chore coat M/L – expected $1,313.5, actual $0. Sold out 2026-11-04 15:00, availability starts 2026-11-12
>   * Denim jacket M/L – expected $796.5, actual $0. Sold out 2026-11-04 15:00, availability starts 2026-11-12
>   * Light rain parka M/L – expected $590.0, actual $0. Sold out 2026-11-04 15:00, availability starts unknown
>
> * **Campaign not sent – $1,300**
> Weekly email cmp_weekly_1105 scheduled 2026-11-05 08:00 ET failed – “List import failed”. Expected lift $1,300 vs the four prior weekly sends 2026-10-08/15/22/29.
>
> Unexplained remainder: –$660.
>
> Total explained gap ≈ $4,000 of the $4,660 drop.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-graph · 2회차 · ✗ 실패

토큰 24,293 · 17.017초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 6,980토큰

준비: 전략 `index`, 함수 253개, 목차 29,192자(system prompt)

**질문 1**
> Why did sales drop yesterday?

1. 모델 → **`a2api_load`** `` {"names":["explain_sales_change"]} ``
   ← 결과 35B: `` {"loaded":["explain_sales_change"]} ``
2. 모델 → **`explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue","max_causes":5} ``
   ← 결과 2,320B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+900자) ``

**답변 1**
> Yesterday (Thu 2026-11-05) revenue was $18,240 on 201 orders vs the same-weekday 4-week average of $22,900 on 247 orders. That’s –$4,660 / –20.4%.
>
> Explained causes:
>
> * **Out of stock – $2,700**
>   3 bestsellers lost sizes M and L from Wed 2026-11-04 15:00 ET:
>   * Cotton chore coat – M/L – expected $1,313.5, actual $0. Availability starts 2026-11-12
>   * Denim jacket – M/L – expected $796.5, actual $0. Availability starts 2026-11-12
>   * Light rain parka – M/L – expected $590.0, actual $0. Availability starts unknown
>
> * **Campaign not sent – $1,300**
>   Weekly email cmp_weekly_1105 failed to send at 2026-11-05 08:00 ET. Error: List import failed. Expected lift $1,300 vs the four prior weekly sends 2026-10-08/15/22/29.
>
> Unexplained remainder: –$660.
>
> Total explained gap = –$4,000 of the –$4,660 drop.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names · 1회차 · ✗ 실패

토큰 10,577 · 20.899초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 1,621토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> Why did sales drop yesterday?

1. 모델 → **`a2api_load`** `` {"names":["explain_sales_change","get_sales_overview","get_sales_trend"]} ``
   ← 결과 74B: `` {"loaded":["explain_sales_change","get_sales_overview","get_sales_trend"]} ``
2. 모델 → **`explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue","max_causes":5} ``
   ← 결과 2,320B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+900자) ``

**답변 1**
> Yesterday = store day 2026-11-05.
>
> * Revenue: $18,240 on 201 orders
> * Same-weekday last 4 weeks average: $22,900 on 247 orders
> * Change: -$4,660 revenue, -20.35%
>
> Explained causes for the revenue gap:
>
> 1. **Out of stock – 3 bestsellers M/L since Wed Nov 4 15:00**
>    * Amount: -$2,700
>    * Cotton chore coat – sizes M, L – sold out 2026-11-04T15:00:00-05:00, availability starts 2026-11-12T00:00:00-05:00. Expected $1,313.5, actual $0
>    * Denim jacket – sizes M, L – sold out 2026-11-04T15:00:00-05:00, availability starts 2026-11-12T00:00:00-05:00. Expected $796.5, actual $0
>    * Light rain parka – sizes M, L – sold out 2026-11-04T15:00:00-05:00, availability starts null. Expected $590.0, actual $0
>
> 2. **Campaign not sent**
>    * Weekly email cmp_weekly_1105 not sent: list import failed Thu 08:00, scheduled 2026-11-05T08:00:00-05:00, status failed
>    * Amount: -$1,300. Expected $1,300, actual $0
>
> Unexplained remainder: -$660
>
> Total explained gap = -$4,000 of the -$4,660 drop.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names · 2회차 · ✗ 실패

토큰 10,709 · 23.145초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 1,621토큰

준비: 전략 `index`, 함수 253개, 목차 4,577자(system prompt)

**질문 1**
> Why did sales drop yesterday?

1. 모델 → **`a2api_load`** `` {"names":["explain_sales_change","get_sales_overview","get_sales_trend"]} ``
   ← 결과 74B: `` {"loaded":["explain_sales_change","get_sales_overview","get_sales_trend"]} ``
2. 모델 → **`explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue","max_causes":5} ``
   ← 결과 2,320B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+900자) ``

**답변 1**
> Yesterday = store day 2026-11-05.
>
> * Revenue: $18,240 on 201 orders
> * Same-weekday last 4 weeks average: $22,900 on 247 orders
> * Change: -$4,660 revenue, -20.35%
>
> Explained causes for the revenue gap:
>
> 1. **out_of_stock – 3 bestsellers out of M and L since Wed Nov 4 15:00**
>    * Amount: -$2,700
>    * prd_chore_coat – Cotton chore coat, sizes M, L, sold out 2026-11-04T15:00:00-05:00, availability starts 2026-11-12T00:00:00-05:00. Expected $1,313.5, actual $0
>    * prd_denim_jacket – Denim jacket, sizes M, L, sold out 2026-11-04T15:00:00-05:00, availability starts 2026-11-12T00:00:00-05:00. Expected $796.5, actual $0
>    * prd_rain_parka – Light rain parka, sizes M, L, sold out 2026-11-04T15:00:00-05:00, availability starts null. Expected $590.0, actual $0
>
> 2. **campaign_not_sent – Weekly email not sent: list import failed Thu 08:00**
>    * Amount: -$1,300
>    * cmp_weekly_1105 – Weekly email, channel email, campaign_status failed, scheduled_time 2026-11-05T08:00:00-05:00, error_message “List import failed”. Expected $1,300, actual $0. Compared with cmp_weekly_1008, cmp_weekly_1015, cmp_weekly_1022, cmp_weekly_1029.
>
> Unexplained remainder: -$660.
>
> The two identified causes account for $4,000 of the $4,660 drop; stockouts of the three bestsellers in M/L are the largest driver.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown)
(도구 정밀도 1.00, 재현율 1.00)
