# b3-why-sales-dropped — ours-design-settings-recent-1

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `d86a1ff` · a2api `8112189`

**과업**

> Why did sales drop yesterday?

- 필요한 도구: `explain_sales_change`
- 허용 도구: `get_sales_trend`, `get_sales_overview`, `search_products`, `get_inventory`
- 답에 있어야 할 사실: Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$4,660, -20%); 201 orders against 247
- 답에 있어야 할 사실: M and L sold out on the three best sellers (chore coat, rain parka, denim jacket): about -$2,700
- 답에 있어야 할 사실: the weekly email did not go out (Thu 08:00 list import failed): about -$1,300; -$660 is not explained

### a2api-acom · 1회차 · ✗ 실패

토큰 11,987 · 18.766초 · 모델 호출 2회 · 도구 호출 1회 · 첫 요청 프롬프트 4,941토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> Why did sales drop yesterday?

- 모델 판단(추론 필드): Store time: Friday, November 6, 2026, 11:00 (America/New_York). Yesterday is Thursday, November 5, 2026. We need explain sales change. Use acom_explain_sales_change. Valid_from = 2026-11-05, valid_through = 2026-11-05. Compare mode? default same_weekday_last_4_weeks. Could be previous_period? Probably same weekday last 4 weeks. We need metric: revenue default. Maybe also order_count? Use default revenue. We need max_causes? default 5. Call acom_explain_sales_change with valid_from 2026-11-05, valid_through 2026-11-05, compare_mode same_weekday_last_4_weeks. Potentially also get sales overview to confirm drop. First call explain_sales_change. Also could get sales trend to see context. Let's d… (+23자)
1. 모델 → **`acom_explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue","max_causes":5} ``
   ← 결과 2,167B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+1,567자) ``
- 모델 판단(추론 필드): We have data: Period 2026-11-05 revenue 18,240 USD, order_count 201 Compare to same weekday last 4 weeks average revenue 22,900 USD, order_count 247 Gap -4,660 USD (-20.35%) Causes: 1. out_of_stock: 3 bestsellers out of M and L since Wed Nov 4 15:00: prd_chore_coat, prd_denim_jacket, prd_rain_parka. Amount -2,700 USD Details per product expected vs actual. 2. campaign_not_sent: Weekly email not sent: list import failed Thu 08:00. cmp_weekly_1105. Amount -1,300 USD Unexplained -660 USD Total explained causes: -4,000, unexplained -660 = -4,660 We can provide answer. Maybe also get campaign details to confirm. Might be good to fetch campaign details. Also could check sales overview for yesterda… (+324자)

**답변 1**
> Yesterday was Thu 2026-11-05.
>
> * **Period:** revenue $18,240 • 201 orders
> * **Same-Thu last 4 weeks avg:** revenue $22,900 • 247 orders
> * **Change:** -$4,660 revenue, -20.35%
>
> Explained causes from the data:
>
> 1. **Out of stock – 3 bestsellers M/L since Wed Nov 4 15:00**
>    * -$2,700 revenue vs the 4-week weekday baseline
>    * prd_chore_coat – Cotton chore coat M/L – expected $1,313.50, actual $0.00 – sold out 2026-11-04T15:00-05:00, availability starts 2026-11-12T00:00-05:00
>    * prd_denim_jacket – Denim jacket M/L – expected $796.50, actual $0.00 – sold out 2026-11-04T15:00-05:00, availability starts 2026-11-12T00:00-05:00
>    * prd_rain_parka – Light rain parka M/L – expected $590.00, actual $0.00 – sold out 2026-11-04T15:00-05:00, availability starts null
>
> 2. **Campaign not sent**
>    * cmp_weekly_1105 – Weekly email – email – scheduled 2026-11-05T08:00:00-05:00
>    * Status: failed – “List import failed”
>    * -$1,300 revenue vs the comparable weekly emails cmp_weekly_1008, cmp_weekly_1015, cmp_weekly_1022, cmp_weekly_1029
>
> Unexplained remainder: -$660
>
> So the $4,660 drop is mainly the stock-out of the three bestseller sizes in M/L and the missed weekly email on Thu 08:00.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom-names-batch · 1회차 · ✗ 실패

토큰 20,554 · 30.88초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 1,975토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> Why did sales drop yesterday?

- 모델 판단(추론 필드): We need to look up sales data. Likely use analytics › sales: explain_sales_change, get_sales_overview, get_sales_trend. Need date. Store time: Friday, November 6, 2026, 11:00 (America/New_York). Yesterday is Thursday, November 5, 2026. We need explain_sales_change. Probably needs period. Let's load functions. We need a2api_load to load explain_sales_change etc.
1. 모델 → **`a2api_load`** `` {"names":["get_sales_overview","explain_sales_change","get_sales_trend"]} ``
   ← 결과 74B: `` {"loaded":["get_sales_overview","explain_sales_change","get_sales_trend"]} ``
- 모델 판단(추론 필드): Now we need explain sales change for yesterday. valid_from = 2026-11-05, valid_through = 2026-11-05. compare_mode? default compare with same weekday last 4 weeks? Could use same_weekday_last_4_weeks. Or previous_period? Sales drop yesterday vs what? Probably vs average of same weekday last 4 weeks. Could also do previous_period (Nov 4). The question "Why did sales drop yesterday?" likely compared to previous day or average. Might be best to get sales overview for yesterday and previous day, and explain_sales_change. Let's call explain_sales_change with valid_from 2026-11-05 valid_through 2026-11-05 compare_mode same_weekday_last_4_weeks, metric revenue default. Also maybe get sales trend to … (+903자)
2. 모델 → **`a2api_batch`** `` {"calls":[{"name":"explain_sales_change","arguments":{"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue","max_causes":5}},{"name":"get_sales_overview","arguments":{"valid_from":"2026-11-05","valid_through":"2026-11-05","acom:metrics":["revenue","order_count","average_order_value"]}},{"name":"get_sales_trend","arguments":{"valid_from":"2026-10-30","valid_through":"2026-11-06","acom:granularity":"day","acom:metrics":["revenue","order_count"]}}]} ``
   ← 결과 3,686B: `` {"batch":[{"name":"explain_sales_change","result":{"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-… (+2,400자) ``
- 모델 판단(추론 필드): We have data. Explain sales change: period revenue $18,240 vs compare to same weekday last 4 weeks average $22,900. Gap -$4,660, change rate -20.35%. Main cause: out_of_stock 3 bestsellers out of M and L since Wed Nov 4 15:00. Amount -$2,700. Products: Cotton chore coat sizes M L expected $1,313.5 actual 0; Denim jacket expected $796.5; Light rain parka expected $590. Also total 2 causes shown? It says items shown 1 of 2, omitted. total 2. So there is another cause. Unexplained -$660. We should report why sales dropped yesterday. Possibly also note order count dropped from 247 avg to 201. We might need to get second cause. Let's call explain_sales_change again with max_causes maybe 10 to get… (+196자)
3. 모델 → **`explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue","max_causes":10} ``
   ← 결과 2,167B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+1,567자) ``
- 모델 판단(추론 필드): Now we have two causes: 1 out_of_stock -$2,700 2 campaign_not_sent -$1,300 Total explained -$4,000, unexplained -$660, gap -$4,660. We should answer operator directly briefly with key numbers. Also maybe mention sales overview: revenue $18,240, orders 201, AOV $90.75. Drop vs average. We should respond with explanation. Possibly note stockouts of Cotton chore coat, Denim jacket, Light rain parka sizes M/L since Nov 4 15:00. Weekly email not sent due to list import failed. Provide summary. No need further calls. Answer.

**답변 1**
> Yesterday 2026-11-05 vs the same Thursday of the last 4 weeks
>
> * Revenue: $18,240  vs  $22,900 average
> * Orders: 201  vs  247 average
> * AOV: $90.75
> * Change: -$4,660  / -20.35%
>
> Explained gap:
>
> 1. **out_of_stock – $2,700**
>    3 bestsellers out of M/L since Wed Nov 4 15:00 EST
>    * Cotton chore coat – sizes M, L – bestseller
>      sold out 2026-11-04T15:00:00-05:00, availability starts 2026-11-12T00:00:00-05:00
>      expected $1,313.5, actual $0
>    * Denim jacket – sizes M, L – bestseller
>      sold out 2026-11-04T15:00:00-05:00, availability starts 2026-11-12T00:00:00-05:00
>      expected $796.5, actual $0
>    * Light rain parka – sizes M, L – bestseller
>      sold out 2026-11-04T15:00:00-05:00, availability starts null
>      expected $590.0, actual $0
>
> 2. **campaign_not_sent – $1,300**
>    Weekly email cmp_weekly_1105 failed to send
>    scheduled 2026-11-05T08:00:00-05:00, status failed, error “List import failed”
>    expected $1,300, actual $0
>
> Unexplained: -$660
>
> The stockouts of the three bestseller M/L styles account for ~58% of the revenue shortfall vs the 4-week Thursday average, with the missed weekly email adding another ~28%.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8 not shown)
(도구 정밀도 1.00, 재현율 1.00)
