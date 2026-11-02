# b3-why-sales-dropped — ours-design-12-slow-provider

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `d86a1ff` · a2api `44c7123`

**과업**

> Why did sales drop yesterday?

- 필요한 도구: `explain_sales_change`
- 허용 도구: `get_sales_trend`, `get_sales_overview`, `search_products`, `get_inventory`
- 답에 있어야 할 사실: Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$4,660, -20%); 201 orders against 247
- 답에 있어야 할 사실: M and L sold out on the three best sellers (chore coat, rain parka, denim jacket): about -$2,700
- 답에 있어야 할 사실: the weekly email did not go out (Thu 08:00 list import failed): about -$1,300; -$660 is not explained

### a2api-acom · 1회차 · ✗ 실패

토큰 11,844 · 64.451초 · 모델 호출 2회 · 도구 호출 1회 · 첫 요청 프롬프트 4,941토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> Why did sales drop yesterday?

- 모델 판단(추론 필드): Store time: Friday, November 6, 2026, 11:00 (America/New_York). Prices in USD. Yesterday = 2026-11-05? Store time Friday Nov 6 11:00, yesterday is Thursday Nov 5 2026. We need explain sales change. Use acom_explain_sales_change. Need valid_from, valid_through, compare_mode. We need explain why sales went up or down: compares period with basis (by default same weekday over last 4 weeks) and splits difference into causes. We need valid_from = 2026-11-05, valid_through = 2026-11-05. compare_mode? Could use same_weekday_last_4_weeks. That's default. Need metric? Default revenue. Could also order_count. Probably revenue. We need to call acom_explain_sales_change. Parameters: valid_from: "2026-11-… (+189자)
1. 모델 → **`acom_explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue","max_causes":5} ``
   ← 결과 2,167B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+1,567자) ``
- 모델 판단(추론 필드): We have data: period 2026-11-05 revenue 18240, order_count 201. Compare to same weekday last 4 weeks average revenue 22900, order_count 247. Gap -4660 USD, change_rate -20.35%. Causes: 1. out_of_stock: 3 bestsellers out of M and L since Wed Nov 4 15:00. Amount -2700 USD. Products: prd_chore_coat Cotton chore coat sizes M L is_bestseller sold out at 2026-11-04 15:00 availability starts 2026-11-12 expected 1313.5 actual 0. prd_denim_jacket Denim jacket sizes M L expected 796.5. prd_rain_parka Light rain parka sizes M L expected 590 actual 0 availability starts null. 2. campaign_not_sent: Weekly email not sent: list import failed Thu 08:00. Amount -1300 USD. Campaign cmp_weekly_1105 name Weekly… (+839자)

**답변 1**
> Yesterday Thu 2026-11-05 revenue was $18,240 on 201 orders vs the same-weekday 4-week average of $22,900 on 247 orders. That’s –$4,660 / –20.4%.
>
> Explained causes from the data:
>
> * **Out of stock – $2,700 lost**
>   3 bestsellers lost sizes M and L since Wed 2026-11-04 15:00 ET:
>   - prd_chore_coat Cotton chore coat M/L – expected $1,313.5, actual $0. Availability starts 2026-11-12
>   - prd_denim_jacket Denim jacket M/L – expected $796.5, actual $0. Availability starts 2026-11-12
>   - prd_rain_parka Light rain parka M/L – expected $590.0, actual $0. Availability starts null
>
> * **Campaign not sent – $1,300 lost**
>   cmp_weekly_1105 Weekly email, email, scheduled 2026-11-05 08:00 ET
>   Status: failed – “List import failed”. Expected lift $1,300 vs the prior 4 weeks cmp_weekly_1008 / 1015 / 1022 / 1029.
>
> Unexplained remainder: –$660.
>
> Total explained gap = –$4,000 of the –$4,660 drop.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-guard · 1회차 · ✗ 실패

토큰 11,746 · 61.333초 · 모델 호출 2회 · 도구 호출 1회 · 첫 요청 프롬프트 4,941토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> Why did sales drop yesterday?

- 모델 판단(추론 필드): Store time: Friday, November 6, 2026, 11:00 (America/New_York). Prices are in USD. Yesterday is Thursday, November 5, 2026? Wait store time Friday Nov 6 11:00. Yesterday is Nov 5. Need explain sales change. We need to explain why sales went up or down. Use acom_explain_sales_change. Parameters: valid_from, valid_through, compare_mode. Need period to explain: yesterday = 2026-11-05 to 2026-11-05. compare_mode: default same_weekday_last_4_weeks? Could use same_weekday_last_4_weeks. Or previous_period? The question: why did sales drop yesterday? Likely compare to same weekday last 4 weeks average. We need metric: revenue default. Could also order_count. Use revenue. max_causes default 5. Call a… (+151자)
1. 모델 → **`acom_explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue"} ``
   ← 결과 2,167B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+1,567자) ``
- 모델 판단(추론 필드): We have data: period 2026-11-05 revenue 18240 vs compare 22900, gap -4660, change_rate -20.35% Causes: out_of_stock: 3 bestsellers out of M and L since Wed Nov 4 15:00 amount -2700 products: Cotton chore coat, Denim jacket, Light rain parka campaign_not_sent: Weekly email not sent: list import failed Thu 08:00 amount -1300 unexplained -660 We should answer with key numbers. Possibly also provide details. The user asked why sales drop yesterday. Provide explanation. We might want to get campaign details? Already have. Could also get sales overview for context? Might be enough. We should answer directly and briefly with key numbers. Possibly also mention order count drop: 201 vs 247. We can pr… (+317자)

**답변 1**
> Yesterday 2026-11-05 revenue was $18,240 on 201 orders vs the same weekday average over the last 4 weeks $22,900 on 247 orders. That is –$4,660 / –20.4%.
>
> Explained causes:
>
> * **Out of stock – $2,700**
>   3 bestsellers lost sizes M and L since Wed Nov 4 15:00 ET:
>   * prd_chore_coat Cotton chore coat M/L – expected $1,313.50, actual $0.00. Sold out 2026-11-04T15:00:00-05:00, availability starts 2026-11-12T00:00:00-05:00
>   * prd_denim_jacket Denim jacket M/L – expected $796.50, actual $0.00. Sold out 2026-11-04T15:00:00-05:00, availability starts 2026-11-12T00:00:00-05:00
>   * prd_rain_parka Light rain parka M/L – expected $590.00, actual $0.00. Sold out 2026-11-04T15:00:00-05:00, availability starts null
>
> * **Campaign not sent – $1,300**
>   cmp_weekly_1105 Weekly email, channel email, scheduled 2026-11-05T08:00:00-05:00
>   Status failed – “List import failed”. Expected $1,300 vs actual $0.00. Compared with cmp_weekly_1008, cmp_weekly_1015, cmp_weekly_1022, cmp_weekly_1029.
>
> Unexplained remainder: –$660.
>
> Total explained gap = –$4,000 of the –$4,660 drop.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-batch · 1회차 · ✗ 실패

토큰 11,970 · 29.019초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 1,975토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> Why did sales drop yesterday?

- 모델 판단(추론 필드): We need to look at sales data. Use analytics sales: get_sales_overview, get_sales_trend, explain_sales_change. Store time: Friday, November 6, 2026, 11:00 (America/New_York). Yesterday is Thursday, November 5, 2026. We need to explain sales drop yesterday. Likely need get_sales_overview and explain_sales_change. We need to load functions. Let's load analytics sales functions. a2api_load names: get_sales_overview, get_sales_trend, explain_sales_change Possibly also need date range. Let's see parameters. Not known. Might need to load first. Let's load.
1. 모델 → **`a2api_load`** `` {"names":["get_sales_overview","get_sales_trend","explain_sales_change"]} ``
   ← 결과 74B: `` {"loaded":["get_sales_overview","get_sales_trend","explain_sales_change"]} ``
- 모델 판단(추론 필드): Store time: Friday, November 6, 2026, 11:00 (America/New_York). So yesterday is Thursday, November 5, 2026. We need explain why sales drop yesterday. Need sales overview? Probably get sales trend for yesterday vs previous? Explain sales change. We need valid_from and valid_through for yesterday: 2026-11-05 to 2026-11-05. Compare mode? Could use same_weekday_last_4_weeks or previous_period. The question: why did sales drop yesterday? Likely compare to previous period? Could be same weekday last 4 weeks average. We need explain_sales_change with valid_from 2026-11-05, valid_through 2026-11-05, compare_mode same_weekday_last_4_weeks (default). Metric revenue default. Also maybe get sales overvi… (+71자)
2. 모델 → **`explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue"} ``
   ← 결과 2,167B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+1,567자) ``
- 모델 판단(추론 필드): We have data. Yesterday is 2026-11-05? Store time is Friday November 6 2026 11:00. Yesterday is 2026-11-05. Yes. Explain sales change: revenue 18,240 vs compare 22,900, gap -4,660 USD, change rate -20.35%. Causes: out_of_stock 3 bestsellers out of M and L since Wed Nov 4 15:00 amount -2,700 USD. Products: Cotton chore coat, Denim jacket, Light rain parka. Expected 2,700 actual 0. Campaign not sent: Weekly email not sent list import failed Thu 08:00 amount -1,300 USD. Unexplained -660 USD. We should answer briefly with key numbers. Possibly also get sales overview for context? Might be enough. The user asked why sales drop yesterday. Provide explanation. We should cite numbers. No need for fu… (+421자)

**답변 1**
> Yesterday = Thu 2026-11-05, store time Fri 2026-11-06.
>
> Revenue was $18,240 on 201 orders vs the same-weekday last-4-weeks average of $22,900 on 247 orders.
> Change: -$4,660 / -20.35%.
>
> Explained causes for the revenue gap:
>
> * **Out of stock – $2,700 lost**
>   3 bestsellers sold out in sizes M and L since Wed 2026-11-04 15:00 ET:
>   - Cotton chore coat – prd_chore_coat, M/L, bestseller. Expected $1,313.5, actual $0. Availability starts 2026-11-12 00:00 ET
>   - Denim jacket – prd_denim_jacket, M/L, bestseller. Expected $796.5, actual $0. Availability starts 2026-11-12 00:00 ET
>   - Light rain parka – prd_rain_parka, M/L, bestseller. Expected $590.0, actual $0. Availability starts null
>
> * **Campaign not sent – $1,300 lost**
>   Weekly email cmp_weekly_1105 was scheduled 2026-11-05 08:00 ET but failed: “List import failed”. Expected $1,300, actual $0. Compared with cmp_weekly_1008, cmp_weekly_1015, cmp_weekly_1022, cmp_weekly_1029.
>
> Unexplained remainder: -$660.
>
> So ~ $4,000 of the $4,660 drop is accounted for by the stockouts of the three M/L bestsellers and the missed weekly email.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-batch-guard · 1회차 · ✗ 실패

토큰 12,856 · 38.841초 · 모델 호출 3회 · 도구 호출 2회 · 첫 요청 프롬프트 1,975토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> Why did sales drop yesterday?

- 모델 판단(추론 필드): We need to look up sales data. Use analytics sales: get_sales_overview, get_sales_trend, explain_sales_change. Store time: Friday, November 6, 2026, 11:00 (America/New_York). Yesterday is Thursday, November 5, 2026. We need to explain sales drop yesterday. Likely need get_sales_trend and explain_sales_change. We need to load functions. Let's load analytics sales functions. a2api_load names: get_sales_overview, get_sales_trend, explain_sales_change Possibly also need date range. Let's load.
1. 모델 → **`a2api_load`** `` {"names":["get_sales_overview","get_sales_trend","explain_sales_change"]} ``
   ← 결과 74B: `` {"loaded":["get_sales_overview","get_sales_trend","explain_sales_change"]} ``
- 모델 판단(추론 필드): Store time: Friday, November 6, 2026, 11:00 (America/New_York). So yesterday is Thursday, November 5, 2026. We need explain why sales drop yesterday. Need compare yesterday vs something. Probably compare to same weekday last 4 weeks average? Or previous period? The explain_sales_change function can explain why sales went up or down: compares a period with a basis (by default same weekday over last 4 weeks) and splits difference into causes. We need valid_from and valid_through for period to explain. Yesterday = 2026-11-05. So valid_from = 2026-11-05, valid_through = 2026-11-05. compare_mode: default same_weekday_last_4_weeks? The function has compare_mode enum: same_weekday_last_4_weeks, pre… (+1,398자)
2. 모델 → **`a2api_batch`** `` {"calls":[{"name":"get_sales_trend","arguments":{"valid_from":"2026-10-29","valid_through":"2026-11-05","acom:granularity":"day","acom:metrics":["revenue","order_count"]}},{"name":"explain_sales_change","arguments":{"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue","max_causes":5}}]} ``
   ← 결과 3,709B: `` {"batch":[{"name":"get_sales_trend","result":{"status":"succeeded","data":{"items":[{"observation_date":"2026-10-29","acom:metric":"revenue","value":{"value":22600.0,"currency":"USD"}},{"observation_date":"2026-10-29","acom:metric":"order_count","value":247},{"observation_date":"2026-10-30","acom:metric":"revenue","value":{"value":21930.0,"currency":"USD"}},{"observation_date":"2026-10-30","acom:metric":"order_count","value":238},{"observation_date":"2026-10-31","acom:metric":"revenue","value":{"value":27410.0,"currency":"USD"}},{"observation_date":"2026-10-31","acom:metric":"order_count","val… (+2,400자) ``
- 모델 판단(추론 필드): We have data. Store time Friday Nov 6 2026 11:00 America/New_York. Yesterday is 2026-11-05 (Thursday). Sales trend shows revenue 18,240 USD, order_count 201. Compare to same weekday last 4 weeks average revenue 22,900 USD, order_count 247. Change rate -20.35%, gap -4,660 USD. Explain sales change: causes: out_of_stock: 3 bestsellers out of M and L since Wed Nov 4 15:00. Amount -2,700 USD. Products: Cotton chore coat, Denim jacket, Light rain parka. Expected 2,700, actual 0. campaign_not_sent: Weekly email not sent: list import failed Thu 08:00. Amount -1,300 USD. Campaign cmp_weekly_1105 failed. Unexplained -660 USD. Total explained -4,000, unexplained -660 = -4,660. We should answer operato… (+420자)

**답변 1**
> Yesterday = Thu 2026-11-05, store time America/New_York.
>
> * Revenue: $18,240  | Orders: 201
> * Same-weekday last 4 weeks average: $22,900 revenue | 247 orders
> * Change: -$4,660 revenue, -20.35%
>
> Explained drop vs that baseline:
>
> * **out_of_stock – $2,700**
>   3 bestsellers out of M and L since Wed Nov 4 15:00 ET
>   - Cotton chore coat – sizes M, L – sold out 2026-11-04T15:00:00-05:00, availability starts 2026-11-12. Expected $1,313.5, actual $0
>   - Denim jacket – sizes M, L – sold out 2026-11-04T15:00:00-05:00, availability starts 2026-11-12. Expected $796.5, actual $0
>   - Light rain parka – sizes M, L – sold out 2026-11-04T15:00:00-05:00, availability starts null. Expected $590.0, actual $0
>
> * **campaign_not_sent – $1,300**
>   Weekly email cmp_weekly_1105 not sent. Scheduled 2026-11-05T08:00:00-05:00, status failed – “List import failed”. Expected $1,300, actual $0. Compared with cmp_weekly_1008, cmp_weekly_1015, cmp_weekly_1022, cmp_weekly_1029.
>
> Unexplained: -$660
>
> Total accounted gap = -$4,000 out of -$4,660.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8 not shown)
(도구 정밀도 1.00, 재현율 1.00)
