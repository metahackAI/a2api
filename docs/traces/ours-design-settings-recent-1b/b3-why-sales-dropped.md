# b3-why-sales-dropped — ours-design-settings-recent-1b

[← 실행 묶음](README.md) · 세트 `design` · a-commerce `d86a1ff` · a2api `8112189`

**과업**

> Why did sales drop yesterday?

- 필요한 도구: `explain_sales_change`
- 허용 도구: `get_sales_trend`, `get_sales_overview`, `search_products`, `get_inventory`
- 답에 있어야 할 사실: Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$4,660, -20%); 201 orders against 247
- 답에 있어야 할 사실: M and L sold out on the three best sellers (chore coat, rain parka, denim jacket): about -$2,700
- 답에 있어야 할 사실: the weekly email did not go out (Thu 08:00 list import failed): about -$1,300; -$660 is not explained

### a2api-acom-names-batch · 2회차 · ✗ 실패

토큰 18,748 · 83.907초 · 모델 호출 4회 · 도구 호출 3회 · 첫 요청 프롬프트 1,975토큰

준비: 전략 `index`, 함수 253개, 목차 6,183자(system prompt)

**질문 1**
> Why did sales drop yesterday?

- 모델 판단(추론 필드): We need to find sales drop yesterday. Store time: Friday, November 6, 2026, 11:00 (America/New_York). Yesterday is Thursday, November 5, 2026. We need explain sales change. Use analytics › sales: explain_sales_change, get_sales_overview, get_sales_trend. Probably need get_sales_overview or get_sales_trend first. explain_sales_change likely requires parameters? Need load functions. Let's load analytics sales functions.
1. 모델 → **`a2api_load`** `` {"names":["get_sales_overview","get_sales_trend","explain_sales_change"]} ``
   ← 결과 74B: `` {"loaded":["get_sales_overview","get_sales_trend","explain_sales_change"]} ``
- 모델 판단(추론 필드): We need explain sales change for yesterday (2026-11-05). Compare mode? Default same_weekday_last_4_weeks? The description: compares period with basis (by default same weekday over last 4 weeks). The function has compare_mode parameter. Options: same_weekday_last_4_weeks, previous_period, custom. We likely want compare to same weekday last 4 weeks average. Use valid_from = 2026-11-05, valid_through = 2026-11-05. compare_mode = same_weekday_last_4_weeks. metric default revenue. Let's call explain_sales_change.
2. 모델 → **`explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue"} ``
   ← 결과 2,167B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+1,567자) ``
- 모델 판단(추론 필드): We have explanation. Sales drop yesterday: revenue 18,240 vs average 22,900 (same weekday last 4 weeks). Change -20.35%, gap -$4,660. Causes: 1. out_of_stock: 3 bestsellers out of M and L since Wed Nov 4 15:00: Cotton chore coat, Denim jacket, Light rain parka. Amount -$2,700. Expected $2,700, actual 0. 2. campaign_not_sent: Weekly email not sent due to list import failed Thu 08:00. Amount -$1,300. Unexplained -$660. We could also provide sales overview for yesterday vs comparison. Possibly get_sales_overview to confirm numbers? Already have. Possibly want order count drop too? Might be okay. We could also give sales trend for recent days to show context. Could call get_sales_trend for last … (+739자)
3. 모델 → **`get_sales_trend`** `` {"valid_from":"2026-10-29","valid_through":"2026-11-05","acom:granularity":"day","acom:metrics":["revenue","order_count"]} ``
   ← 결과 1,452B: `` {"status":"succeeded","data":{"items":[{"observation_date":"2026-10-29","acom:metric":"revenue","value":{"value":22600.0,"currency":"USD"}},{"observation_date":"2026-10-29","acom:metric":"order_count","value":247},{"observation_date":"2026-10-30","acom:metric":"revenue","value":{"value":21930.0,"currency":"USD"}},{"observation_date":"2026-10-30","acom:metric":"order_count","value":238},{"observation_date":"2026-10-31","acom:metric":"revenue","value":{"value":27410.0,"currency":"USD"}},{"observation_date":"2026-10-31","acom:metric":"order_count","value":295},{"observation_date":"2026-11-01","ac… (+852자) ``
- 모델 판단(추론 필드): Now we have trend. Provide answer. Probably summarize: Revenue dropped 20.3% vs same weekday avg: $18,240 vs $22,900, gap -$4,660. Causes: - Out of stock bestsellers sizes M/L since Nov 4 15:00: Cotton chore coat (-$1,313.5 expected), Denim jacket (-$796.5), Light rain parka (-$590) total -$2,700. - Weekly email campaign not sent due to list import failure at 08:00 Nov 5, expected +$1,300, actual $0. - Unexplained -$660. Maybe also mention order count drop 201 vs 247. Provide concise answer. We should not invent beyond data. Make sure to note availability starts for chore coat and denim jacket Nov 12, rain parka unknown. We can give final. Potential to also get_sales_overview for period to c… (+29자)

**답변 1**
> Sales on Thu 2026-11-05 dropped vs the same weekday average over the last 4 weeks.
>
> * Period 2026-11-05
>   * Revenue: $18,240  | Orders: 201
> * Basis same_weekday_last_4_weeks 2026-10-08 / 2026-10-15 / 2026-10-22 / 2026-10-29
>   * Revenue: $22,900  | Orders: 247
> * Change: -$4,660 revenue, -20.35%
>
> Explained causes for revenue:
>
> 1. **out_of_stock – 3 bestsellers out of M and L since Wed Nov 4 15:00**
>    * Amount: -$2,700. Expected $2,700, actual $0
>    * prd_chore_coat – Cotton chore coat, sizes M,L
>      * sold out at 2026-11-04T15:00:00-05:00, availability starts 2026-11-12T00:00:00-05:00
>      * expected $1,313.5, actual $0
>    * prd_denim_jacket – Denim jacket, sizes M,L
>      * sold out at 2026-11-04T15:00:00-05:00, availability starts 2026-11-12T00:00:00-05:00
>      * expected $796.5, actual $0
>    * prd_rain_parka – Light rain parka, sizes M,L
>      * sold out at 2026-11-04T15:00:00-05:00, availability starts null
>      * expected $590.0, actual $0
>
> 2. **campaign_not_sent – Weekly email not sent: list import failed Thu 08:00**
>    * Campaign cmp_weekly_1105 “Weekly email”, channel email, status failed
>    * Scheduled 2026-11-05T08:00:00-05:00, error_message: List import failed
>    * Amount: -$1,300. Expected $1,300, actual $0
>    * Compared with cmp_weekly_1008, cmp_weekly_1015, cmp_weekly_1022, cmp_weekly_1029
>
> Unexplained remainder: -$660
>
> Daily trend for context:
> 2026-10-29 $22,600 / 247 orders
> 2026-10-30 $21,930 / 238 orders
> 2026-10-31 $27,410 / 295 orders
> 2026-11-01 $24,880 / 270 orders
> 2026-11-02 $18,150 / 199 orders
> 2026-11-03 $18,940 / 207 orders
> 2026-11-04 $19,320 / 211 orders
> 2026-11-05 $18,240 / 201 orders

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown)
(도구 정밀도 1.00, 재현율 1.00)

### a2api-acom · 2회차 · ✗ 실패

토큰 11,918 · 46.874초 · 모델 호출 2회 · 도구 호출 1회 · 첫 요청 프롬프트 4,941토큰

준비: 전략 `search`, 함수 9개

**질문 1**
> Why did sales drop yesterday?

- 모델 판단(추론 필드): Store time: Friday, November 6, 2026, 11:00 America/New_York. Yesterday is Thursday, November 5, 2026. Need explain sales change. Use acom_explain_sales_change. Need valid_from, valid_through, compare_mode. We should compare yesterday vs same weekday last 4 weeks? Default compare_mode same_weekday_last_4_weeks. That seems reasonable. Need metric default revenue. Could ask for revenue. valid_from = 2026-11-05, valid_through = 2026-11-05. Compare_mode = same_weekday_last_4_weeks. Let's call acom_explain_sales_change. Also maybe get sales overview for context? The explain function gives causes. Let's call it. Parameters: valid_from = "2026-11-05", valid_through = "2026-11-05", compare_mode = "s… (+83자)
1. 모델 → **`acom_explain_sales_change`** `` {"valid_from":"2026-11-05","valid_through":"2026-11-05","compare_mode":"same_weekday_last_4_weeks","acom:metric":"revenue"} ``
   ← 결과 2,167B: `` {"status":"succeeded","data":{"items":[{"cause":"out_of_stock","detail":"3 bestsellers out of M and L since Wed Nov 4 15:00","amount":{"value":-2700.0,"currency":"USD"},"evidence":["prd_chore_coat","prd_denim_jacket","prd_rain_parka"],"expected":{"value":2700.0,"currency":"USD"},"actual":{"value":0.0,"currency":"USD"},"since":"2026-11-04T15:00:00-05:00","products":[{"product_id":"prd_chore_coat","name":"Cotton chore coat","sizes":["M","L"],"is_bestseller":true,"sold_out_at":"2026-11-04T15:00:00-05:00","availability_starts":"2026-11-12T00:00:00-05:00","expected":{"value":1313.5,"currency":"USD"… (+1,567자) ``
- 모델 판단(추론 필드): Need explain. Data: period 2026-11-05 revenue 18,240 vs compare avg 22,900, gap -4,660 (-20.35%). Causes: - out_of_stock: 3 bestsellers out of M and L since Wed Nov 4 15:00: Cotton chore coat, Denim jacket, Light rain parka. Amount -2,700 USD. - campaign_not_sent: Weekly email not sent: list import failed Thu 08:00, cmp_weekly_1105. Amount -1,300 USD. Unexplained -660 USD. Need answer briefly with key numbers. Possibly also mention order count: 201 vs 247. Provide summary. Maybe also check campaign details? Could call acom_get_campaign for cmp_weekly_1105 to give more details. Might be helpful. The explain already gave error message. Possibly enough. The user asked why did sales drop yesterd… (+411자)

**답변 1**
> Yesterday (Thu 2026-11-05) revenue was $18,240 on 201 orders vs the same-Thursday average of the last 4 weeks $22,900 on 247 orders.
>
> Change vs same weekday last 4 weeks: **-$4,660 / -20.35%**
>
> Explained causes:
>
> * **Out of stock – –$2,700**
>   3 bestsellers sold out in M/L since Wed 2026-11-04 15:00 ET:
>   * prd_chore_coat – Cotton chore coat M/L – expected $1,313.50, actual $0.00, availability starts 2026-11-12
>   * prd_denim_jacket – Denim jacket M/L – expected $796.50, actual $0.00, availability starts 2026-11-12
>   * prd_rain_parka – Light rain parka M/L – expected $590.00, actual $0.00, availability starts unknown
>
> * **Campaign not sent – –$1,300**
>   cmp_weekly_1105 “Weekly email”, scheduled 2026-11-05T08:00:00-05:00
>   Status: failed – List import failed. Expected lift $1,300 vs the four prior weekly emails cmp_weekly_1008, cmp_weekly_1015, cmp_weekly_1022, cmp_weekly_1029.
>
> Unexplained remainder: **-$660**
>
> So ~ $4,000 of the $4,660 drop is accounted for by the stockouts + missed weekly email.

**채점**: ✗ 실패 — 빠진 것: fact "Thu Nov 5: $18,240 against a Thursday average of $22,900 (-$" (20 not shown); fact "the weekly email did not go out (Thu 08:00 list import faile" (8 not shown)
(도구 정밀도 1.00, 재현율 1.00)
