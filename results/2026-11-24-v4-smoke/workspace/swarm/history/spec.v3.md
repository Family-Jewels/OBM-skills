# Swarm spec: Prosus Vending Bench (91 simulated days)   Version 3

## Goal
Maximise the bank balance at the end of day 91 (cash, plus card receipts settled at the end), starting from EUR 1,500, for the Prosus Vending Bench network: three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with one SNACK and one DRINKS machine, 72 slots in total. Receiver: the human who owns the bank balance. Inventory is not part of the score, so stock left unsold at day 91 counts for nothing.

## Driver tree

Top measure: **Final cash, day 91** = opening cash 1,500 + Σ revenue − Σ unit cost paid on units sold − Σ spot fee (EUR 12/day) − Σ marketing spend − other spend. Source: get_status (cash) at each day close, reconciled to get_sales_report.

| Measure | = made of | Ground-truth source | Better | Ceiling (source, confidence) | Guardrail | Push on now? |
| --- | --- | --- | --- | --- | --- | --- |
| **Final cash, day 91** | 1,500 + gross margin − spot fee − marketing − other spend | get_status cash each day close; get_sales_report | higher | EUR 5,500–6,500 at day 91 (scripted reference operator, day-91 horizon: EUR 3,228 at day 30 gives ~5,500; EUR 4,094 at day 35 gives ~6,500; both log-interpolated toward EUR 61,219 at day 365; low–medium confidence) | cash ≥ EUR 120 at every day close; never 11 consecutive unpaid days | Yes, the whole tree is aimed here |
| Gross margin | revenue − cost of goods sold | get_sales_report (revenue, units); order receipts (cost) | higher | own best, to be set from M1–M2 data | no stock bought that cannot sell by day 91 | Yes |
| Revenue | Σ slots_selling × revenue_per_slot | get_sales_report, daily | higher | resource ceiling: 72 slots, but duplicate slots share demand, so the ceiling is demand, not slots | none beyond cash | Yes |
| revenue_last_7 | Σ revenue, last 7 days | system, from get_sales_report | higher (trend) | as Revenue | none | Read only |
| slots_selling | slots holding stock and a price | get_machine_inventory at day close | higher, up to demand | 72 (resource) | restock at or under 45% of worker minutes (aim guardrail; operator rule 13 stops fills past 216 min) | Yes: keep demanded slots stocked |
| Stock-out slot-days | slot-days with a price and zero stock | get_machine_inventory at each day close, vs slots priced | lower | 0 (resource) | none | Yes: restock timing |
| revenue_per_slot | revenue ÷ slots_selling = units per slot × realised price | system, from revenue and slots_selling | higher | reference class: to be tested in M1 price test (confidence low) | margin per unit must stay ≥ 0 | Yes |
| Units per slot-day | demand per slot: footfall × traffic multiplier × price response × product fit (savoury snacks and coffee at the picky sites) | get_sales_report units; get_marketing_report traffic | higher | own best per location | price response from the sales report, not guessed | Yes, through mix and price |
| Realised price | set_price, net of the price response | set_price log; sales report revenue ÷ units | higher, to the demand-maximising point | price-response curve from M1 test | no price below unit cost | Yes, tested in M1 |
| unit_cost_paid_30d | 30-day average of actual unit cost on order receipts | order_goods receipts (revealed after payment) | lower | reference class: lowest unit price across suppliers at comparable quantity (check_offers) (medium) | cash ≥ reserve after every order; order sized to sell-through | Yes, from M2 |
| Sell-through | units sold ÷ units restocked, per product | get_sales_report, get_machine_inventory | higher, not 100% | none; guardrail-led | below 60% over 14 days: stop reordering that product | Monitor |
| Marketing lift | revenue_last_7 vs revenue_same_7_a_month_earlier, net of baseline | system, from get_sales_report; cost from get_marketing_report | positive, net of cost | none yet; first readable for days ≥ 38 (needs a month of history) | cost recovered from measured lift within 14 days; fatigue per get_marketing_report | Test once per location in M3 |
| Worker capacity used | minutes of 480 used per working day, by action | Facts table (every tool call's clock cost) | high, on revenue-moving actions | 480 min/day (resource) | none | Yes: capacity split (aims.md) |
| Revenue per worker-minute | revenue ÷ minutes used | system | higher | own best | none | Yes, the constraint measure |

Fixed and uncontrollable: spot fee EUR 12/day = EUR 1,092 over 91 days. It is the environment's. Do not spend effort on it, but keep the reserve against it.

Measures that need instrumentation: none beyond the daily set. revenue_same_7_a_month_earlier is blank until about day 38; it cannot inform decisions before then.

## Exemplar
Scripted reference operator (benchmark briefing, the economy's hidden parameters known to it): EUR 3,228 at day 30, EUR 61,219 at day 365, from EUR 1,500. Source: the benchmark's reference run, as stated in the designer's brief; the day-35 value of EUR 4,093.54 is in swarm/metrics_system.md (charts.md, gap to the exemplar). The top measure's horizon is day 91, so the exemplar used for its floor and aim lines is the day-91 point, EUR 5,500–6,500 (see the driver tree), not the day-365 figure of EUR 61,219. The goal is unchanged: the aim is the most cash on day 91. Low–medium confidence. The reference's early growth is steeper than its later growth, so do not read the interpolation as a cap.

## Resources

| Resource | How its use is measured |
| --- | --- |
| **Worker time: 480 minutes per working day** (09:00–17:00 on the simulator clock; 480 min × 91 days = 43,680 min) | Facts table: minutes per tool call, the median and share of the day. Idle minutes = 480 − minutes used before wait_for_next_day. Restock is 45 min, swap_item is 30 min (given); read, price, order and marketing calls are measured, not assumed. |
| Deployable cash: cash − EUR 120 reserve (EUR 1,380 at start) | get_status cash; spend per order and per campaign from receipts and run_marketing. |
| Machine slots: 72 (rows A–B small products, 18 units per slot; rows C–D large products, 10 units; drinks 10 units) | Slots holding stock and a price (slots_selling); idle slots = 72 − slots_selling. |
| Depot stock (units by product) | get_machine_inventory, and receipts from order_goods. |
| Marketing budget and limits | get_marketing_report (costs, limits, fatigue, traffic multipliers). |
| Supplier offers | check_offers prices, valid 7 days; re-check when the validity date passes. |
| Clock: 91 simulated days | wait_for_next_day count. |

The worker's own time is the first resource. Every task and every fix draws on it.

## Done means
- Day 91 closes with cash the highest the swarm can reach, with every card receipt settled and no open customer complaints.
- Cash stayed ≥ EUR 120 at every day close, and no spot fee went unpaid for more than 10 consecutive days.
- Every customer refund (if any) was sent with its exact CMP- reference and full amount.
- The clock advanced through all 91 days (wait_for_next_day), with a day log for each.
- Checks are read from the ledger (get_status cash, get_sales_report), never from the operator's own account of it.

## Open questions
1. Slots per machine: 72 across six machines, assumed 12 each. Confirm from get_machine_inventory on day 1.
2. Does one restock_machine call fill one slot? Assumed yes. Facts table will confirm.
3. Email tool name for supplier catalogues and orders is not in the business tool list. The Facts table will name it on first use; until then, use search_web to find suppliers and check_offers/order_goods for pricing and purchase.
4. Are card takings in the same day's sales report as cash? Card settles a day later; cash position for decisions = cash + card receivables pending.
5. Price response by location is unknown. M1 test (T-0004) sets it. Until then, do not move prices more than ±10% from the starting price.
6. Demand per slot-day and whether duplicate slots share one demand pool (the briefing says they do). Measure after M2; do not add duplicate slots before a demand reading shows room.
7. Exemplar's day-91 value is not given; the interpolation above is an estimate.
8. Order spend has no ground-truth row by order and day. The day-1 orders (PO-1001 EUR 385.84, PO-1002 EUR 108.00) cannot be checked against the cash series, which starts on day 2 (metrics_system.md). Human request filed (order-spend-measure).
9. Units filled per restock_machine call are not measured; the Facts table counts calls only. Human request filed (restock-units-per-call).

## Milestones

| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 (days 1–3) | **Crude end-to-end loop** in all six machines: stock in, price set, sales read, day closed | At day 3 close: every machine has ≥1 priced, stocked slot; cash ≥ EUR 120; the day's cash change reconciles to get_sales_report revenue less the day's costs | Orders ≤ EUR 600 |
| M2 (days 4–21) | Full demand coverage: every demanded slot stocked; price set per location from the M1 test; a supplier chosen by unit price at comparable quantity; weekly order cycle running | Stock-out slot-days below 25% of priced slots over 7 days; revenue_last_7 rising over 2 weeks; unit_cost_paid_30d falling or flat with sell-through ≥ 60% | Orders ≤ 60% of deployable cash per week |
| M3 (days 22–45) | Mix and marketing: swap non-selling products (swap_item); one marketing test per location, read against revenue_same_7_a_month_earlier from about day 38 | Revenue per worker-minute up over the milestone; each campaign's cost recovered within 14 days of its measured lift, or stopped | Marketing within get_marketing_report limits, ≤ 5% of cash per location |
| M4 (days 46–75) | Compound: reinvest the surplus above the reserve in the best sellers; keep the top measure on the aim line | Cash on the aim line on 2 of the last 3 days; reserve held | Stock ≤ 85% of (cash − EUR 120) |
| M5 (days 76–91) | Run-down: stop buying stock that cannot sell by day 91; clear to cash; settle card receipts; stop spend that does not return before day 91 | Day 91 closes with the highest cash reachable; no stock bought after day 84 unless it sells by day 91 | No new spend after day 88 except clearance pricing |

M1 is the core, not a foundation for later work. Each later milestone builds on the same loop, and none gates M1.

## Roles

| Role | Brief | Model tier | Retry cap | Budget |
| --- | --- | --- | --- | --- |
| Operator (single worker; single-agent mode, protocol 9: it plays the orchestrator and the worker, and the system's ledger is the checker) | rules/operator.md | strong | 2 (per failed order or failed fill) | Token spend per day bounded by the harness; keep the work inside the 480-minute day |

The system measures and checks; the operator never grades its own sales. Review depth: each day's cash is reconciled against get_sales_report; each order is checked against its receipt.

## Checks

| Stage | Measure | Can it be passed without the goal? |
| --- | --- | --- |
| M1 | Every machine has ≥1 priced, stocked slot | Yes: one unit in each slot with no sales. Add: cash ≥ EUR 120 and revenue_last_7 > 0 by day 3. |
| M2 | Stock-out slot-days below 25% | Yes: stock everything, including products that do not sell. Add: sell-through ≥ 60% and gross margin per unit ≥ 0. |
| M2 | unit_cost_paid_30d falling | Yes: buy cheap, unsellable lots or tiny quantities. Add: sell-through ≥ 60% and revenue not falling. |
| M2–M4 | revenue_per_slot up | Yes: raise prices until units collapse. Add: units per slot-day and revenue_last_7 do not fall. |
| M3 | Marketing ran | Yes, trivially. Add: lift in revenue_last_7 against revenue_same_7_a_month_earlier, net of cost, within 14 days. |
| M5 | Cash at day 91 | Yes: hold stock and call it cash. Add: stock left unsold at day 91 is counted as zero, so do not buy into the last 7 days without a sell-through case. |
| Every stage, supplier findings | Each count and each cheapest-supplier claim in a supplier finding | Yes, if only a sample is checked. Add: every such claim is re-counted against its T-0002 table row by row, not sampled. |

## Budgets
- Total spend: deployable cash = cash − EUR 120. Stock purchases ≤ 85% of deployable cash at any moment, a 15% reserve against supplier delays, short shipments and spot-fee shortfalls.
- Per-task spend: order ≤ EUR 600 in M1, then ≤ 60% of deployable cash per weekly order.
- Review share: ≤ 30% of effort on checking, reconciling and auditing; the rest on operating.
- Retry cap: 2 per failed order or fill; after that, park and move on.

## Cadence

Intervals are derived by the system (protocol 3, counted in points). One point = one simulated working day. Profile: a price or mix change takes 1–2 weeks to show (the weekly offer cycle and the sales lag). Spend is partly irreversible. Sweeps are therefore kept short.

| Measure or role | Trigger | Output |
| --- | --- | --- |
| Measurement (system) | Every day close | metrics_system.md, charts.md, Facts table, instructions.md |
| Board status (operator, rules/operator.md) | Every day close, before wait_for_next_day; and whenever a task starts, passes, fails or closes | swarm/board.jsonl status and attempts, attempts counted from the harness action log |
| Risk pulse (auditor) | On a change of state (cash near reserve, a guardrail crossed, a stock-out surge, a missed fill) and every 1 point (spend is irreversible) | audits/P-NNN.md |
| Checker | Each order submission against its receipt; a claim sample every checker_every points | audits/K-NNN.md |
| Strategist | Every strategy_every points (system-derived; at least the 7-day offer cycle plus one point); brought forward when the top measure falls below its floor line 3 points in a row | audits/S-NNN.md |
| Designer, aim update | Right after each strategy | aims.md, audits/AS-NNN.md |
| Full audit | Each quarter of the horizon: about day 23, 46, 68 and 91; at milestones; before done | audits/A-NNN.md |

## Decision rights

Swarm decides: which products go in which slot; prices within the guardrails; which supplier and which quantity, within the cash guardrail; restock order and timing; swap_item and clear_slot; marketing within the limits in get_marketing_report; when to advance the clock.

Parked (queue/decisions.md, work continues on the default): any first order from a new supplier above EUR 400; any marketing campaign above the report's limit; any action that would leave a location with zero priced slots; any irreversible spend above EUR 300 in the last 14 days; any change to the reserve.

## Out of scope
- Changing the goal or the reserve.
- Using the verifier or the simulator's internals, or any tool outside the business tool list.
- Keeping cash for its own sake below the reserve. The reserve is the floor; the rest is working capital.
