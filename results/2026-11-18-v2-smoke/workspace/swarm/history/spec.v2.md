# Swarm spec: Prosus Vending Bench, 91 simulated days   Version 2 (v1 in history/spec.v1.md; change R-O-001)

## Goal
Maximise bank cash on the final simulated day (day 91), starting from EUR 1,500, across three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with a SNACK and a DRINKS machine. Receiver: the human who owns the run. Inventory is not money: unsold stock at the end scores zero.

Cash identity (the top measure is built from this, read from the ledger, never self-reported):
cash(91) = 1,500 + Σ revenue − Σ goods bought − Σ spot fees (EUR 12/day) − Σ marketing − Σ refunds, settled (card takings lag one day; outstanding card receipts settle at the end).

## Driver tree
Top measure: **final cash, day 91**. Top-level floor and aim lines are computed by the system from this measure (protocol 8).

| Measure | = made of | Ground-truth source | Better | Ceiling (source, confidence) | Guardrail | Push on now? |
| --- | --- | --- | --- | --- | --- | --- |
| Final cash, day 91 (top) | 1,500 + revenue − goods bought − fees − marketing − refunds | bank ledger (get_status, system cash record) | up | ~EUR 5,500 on day 91: exemplar path (EUR 3,228 at d30, EUR 61,219 at d365) interpolated geometrically; **low-medium** (interpolation, not measured) | cash ≥ EUR 120 at every close | via drivers |
| Revenue per day | slots_selling × revenue_per_slot | get_sales_report, daily | up | own best stretch; no per-day exemplar given (medium) | none | derived |
| slots_selling (0–72) | slots with price > 0 and stock > 0 at close | machine inventory, daily | up | 72 physical slots (high) | restock only if cash after purchase ≥ EUR 120 | **yes, M2–M3** |
| revenue_per_slot (EUR/slot/day) | units_per_slot_day × net_unit_price | sales report ÷ slots selling | up | own best (low) | net price ≥ unit cost | **yes** |
| units_per_slot_day | distinct demand captured ÷ slots sharing it (duplicate product slots share one demand pool; extra slots add capacity, not customers) | sales report by product | up | own best; revenue-max mix from E-002 (low) | no stock-out | **yes, mix first** |
| net_unit_price | list price × (1 − discount) at the revenue-maximising level | set_price log; sales report | at the peak of the observed price curve | peak of E-001 response curve (low until 2 price points per location) | price ≥ unit cost | **yes, E-001** |
| Stock availability (stock-out slot-days) | slot-days with stock = 0 while priced | machine inventory, daily | down to 0 | 0 physical (high) | none | yes (restock timing) |
| Footfall per location | base × traffic multiplier | get_marketing_report (multiplier); sales report (units) | up | multiplier and fatigue limits from get_marketing_report (medium) | marketing spend ≤ incremental gross margin within 7 days; no fatigue flag | later, E-003 |
| Unit cost paid | goods bought ÷ units bought | order receipts; check_offers quotes | down | lowest verified quote at the order quantity (medium) | cost ≤ price − margin floor | **yes, E-004** |
| Sell-through by day 91 | units sold ÷ units bought | ledger and machine inventory | up to 100% | 100% physical (high) | no purchase after day 84 unless expected sales before day 91 cover its cost | harvest (M5) |
| Spot fees | EUR 12/day, fixed | ledger | fixed | EUR 1,092 over 91 days (high) | paid every day; 10 consecutive unpaid days ends the run | no lever |
| Marketing spend | campaigns × cost | get_marketing_report | ≤ 1× incremental gross margin | n/a | cap per location per fatigue report | test only, E-003 |
| Refunds and open complaints | complaints opened − closed | ledger, complaints | 0 open | 0 (high) | open complaints at close = 0 | yes (reactive) |

Instrumentation gaps (not to be filled by an agent's self-report): footfall per location is not reported directly; estimate it from the sales report and the marketing multiplier and log the method. The duplicate-slot demand sharing rule must be confirmed from the sales report by day 14.

## Exemplar
Scripted reference operator (benchmark): EUR 3,228 at day 30, EUR 61,219 at day 365, from EUR 1,500. Day 91 is interpolated: 3,228 × (61,219 ÷ 3,228)^(61/335) ≈ EUR 5,500. Source: benchmark statement, not a measured run in this environment. Own best stretch is the improvement exemplar once the system has points.

## Targets (set by the system, not by hand)
- Floor line: from the top measure's level after 3 points (day 21) to the day-91 goal (~EUR 5,500). Three points in a row below it call for an opportunity review.
- Aim: deliberate overshoot. The aim reaches the day-91 goal by the halfway point of the remaining horizon, then keeps rising. It is raised when met on 2 of the last 3 points. Missing the aim triggers nothing.
- Limits: centre ± 2.66 × average moving range, computed from the measure's own data.

## Resources
| Resource | How its use is measured |
| --- | --- |
| Cash (bank and card receivable) | Balance each close. Idle = cash above the EUR 120 reserve while slots are idle |
| Capital in stock | Stock at cost in machines and depot. Capital in use = stock at cost ÷ (cash + stock at cost). Idle = stock at cost unsold for 7+ days |
| Selling slots (72) | slots_selling. Idle = 72 − slots_selling |
| Operator minutes (480/day) | Fill 45 min, swap 30 min, status and price calls minutes each. Idle = minutes not spent on a driver action |
| Supplier quotes | check_offers valid 7 days. Idle = quotes valid and unused while stock is short |
| Marketing headroom per location | Traffic multiplier and fatigue from get_marketing_report. Idle = headroom with no campaign in the last 14 days |
| Deliveries | Lots delayed or short-shipped (count, days late) |

## Experiments
Budget: experiments take at most 10% of operator minutes (about 48 min/day averaged), at most 7 slots changed at once, and at most EUR 150 of cash exposed. Rules: each experiment is reversible, stays inside the guardrails, states a prediction, lasts at least 3 points (21 days), and only one runs per driver at a time (different drivers may run together). The orchestrator writes the result against the system's charts at the end (protocol 4.8). Files: `swarm/experiments/E-00N.md`.

| ID | Driver | Change | Prediction | Guardrail | Start | End |
| --- | --- | --- | --- | --- | --- | --- |
| E-001 | net_unit_price | Price +10% on half the selling slots at each location, other half held at baseline | At AI-HOUSE, revenue_per_slot on the +10% half ≥ baseline half. At AI-LOUNGE, units fall by more than 10% on the +10% half | revenue_per_slot on the test half ≥ 90% of baseline half; cash ≥ EUR 120 | day 8 | day 28 |
| E-002 | units_per_slot_day | Replace duplicate-product slots with distinct products the segment buys (savoury snacks, coffee), via swap_item | Distinct products sold per machine rise; total units per machine rise by ≥ 10% | no new stock-out; no swap of a slot still holding stock | day 29 | day 49 |
| E-003 | Footfall per location | One campaign per location, channel varied (print, slack, mail), within fatigue limits | Units per day rise ≥ 10% in the 7 days after the campaign against the same weekday the prior week | campaign cost ≤ incremental gross margin in 7 days; no fatigue flag | day 50 | day 70 |
| E-004 | Unit cost paid | Compare check_offers at two quantities across two suppliers (zuidas, bakker); for identical SKUs, order the cheaper lot at the better quantity | Identical SKUs at zuidas ≥ 15% below the prior order; overall unit cost falls ≥ 5% (keep bar) | no order that drops cash below EUR 120; no delivery more than 2 days late | day 30 | day 56 |
| E-005 | Stock availability (stock-out slot-days) | Fill the fastest-selling priced drinks slots to full depth on each restock trip; at most 7 slots changed at once; stock bought ≤ EUR 150 at cost | slots_selling ≥ 25 by day 42; stock-out slot-days fall by ≥ half against days 22–29 by day 56 | cash ≥ EUR 120 at every close; exposure ≤ EUR 150; quotes ≤ 7 days old | day 30 | day 56 |

No experiments after day 70. Days 71–91 are harvest.

## Done means
- Day 91 close: cash settled, card receivables included, no pending orders, no open complaints. Final figure recorded in `swarm/log/progress.md`.
- Check, every close: cash ≥ EUR 120 (guardrail; a breach is reverted first).
- Check, every order: receipt cost ≤ quoted price at order; cost recorded against the order.
- Check, end of day 91: final cash is compared with the aim line; the gap is written into the final audit.
- Check, not passable without the goal: revenue_last_7 > revenue_same_7_a_month_earlier on each point from day 37, read from the system's charts. A cash balance held idle does not pass this.
- Check, days 71–91: no stock bought whose expected sales before day 91 do not cover its cost.

## Open questions
1. Is the day-91 exemplar value (~EUR 5,500) a sound target? It is an interpolation. Request an exemplar value at day 91 if the benchmark provides one.
2. Is the cash guardrail measured on bank cash, or cash plus pending card receipts? Default: bank cash, with card receivables shown separately.
3. Does the marketing multiplier decay, and how fast does fatigue recover? Unknown until E-003; use get_marketing_report every point.
4. Does `revenue_same_7_a_month_earlier` (the 7 days ending 30 days earlier) exist before day 37? Default: n/a before day 37.
5. Operator call budget: the briefing gives no call quota, only time. Default: minutes are the budget.
6. Does the sales report flag test slots (E-001) and show duplicate-slot sharing (E-002)? E-001 ran without slot-level data and was inconclusive; E-002's sharing check (due day 14) is not recorded. Request both from the system; until then E-002 is judged on product-level units only.
7. Which count is the selling-slot figure: the charts' resource table shows 12 used, while slots_selling reads 19 on the same day. Request the system to reconcile the two.

## Milestones
| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 (days 1–7) | Crude end-to-end: all six machines selling, daily ledger recorded, cash held above reserve | By end of day 7: each of the 6 machines has ≥ 1 slot with sales > 0 in the sales report; cash ≥ EUR 120 at every close; tasks T-001 to T-004 logged | ≤ EUR 600 on stock |
| M2 (days 8–21) | slots_selling ≥ 36 with price ≥ unit cost; E-001 running | At day 21: slots_selling ≥ 36; no slot priced below cost; E-001 started day 8 with its prediction logged | Stock only from cash above reserve |
| M3 (days 22–42) | slots_selling ≥ 60; revenue_per_slot at or above its own best; E-001 and E-002 closed | At day 42: ≥ 60 slots selling; both experiments with keep or revert results | As M2 |
| M4 (days 43–70) | 72 slots where unit margin is positive; mix and price set from results; E-003 and E-004 closed | At day 70: slots_selling ≥ 66; no slot with negative unit margin; E-003 and E-004 results written | As M2 |
| M5 (days 71–91) | Harvest: maximise cash at day 91 | Day 91: no purchase outside the sell-through rule; final close recorded; card receipts settled | No new stock after day 84 unless it passes the sell-through rule |

## Roles
| Role | Brief | Model tier | Retry cap | Budget |
| --- | --- | --- | --- | --- |
| Operator (orchestrator and worker) | `swarm/rules/operator.md` | strong | 2 per task | 480 operator minutes per day |
| Ledger checker | `swarm/rules/checker.md` | fast | 2 | about 5% of operator minutes |
| Auditor (pulse and full) | `swarm/rules/auditor.md` | strong | 2 | reads charts only; no business calls |
| Diagnostician | `swarm/rules/diagnostician.md` | strong | 2 | reads charts and logs only |
| Designer | this spec | strong | 2 | invoked on diagnosis or opportunity review |

## Budgets
- Total: EUR 1,500 starting cash; reserve EUR 120 (8% of start), never spent on stock, marketing or experiments.
- Review share: about 5% of operator minutes (ledger reconciliation at each order and each close). Default cap 30% is not needed here.
- Experiments: 10% of operator minutes, 7 slots at once, EUR 150 exposed.
- Per-task budgets: each daily close is one task; each restock trip is one task.

## Cadence
The system derives intervals from the task: point = 7 simulated days, so 13 points over 91 days. Natural cycle is weekly, so point windows are 7 days.

| Measure or role | Trigger | Output |
| --- | --- | --- |
| Measurement (system) | Every simulated day at close | `swarm/metrics_system.md`, `swarm/charts.md` |
| Operator, daily close | Every day, after the sales report | Daily line in `swarm/log/progress.md`; cash ≥ EUR 120 check |
| Ledger checker | Each order (receipt against quote); each point on a random day | Review record (4.3) |
| Auditor, pulse | Every point (days 7, 14, … 91). Every second point after 3 quiet pulses. Back to every point on any signal, redesign or experiment end (days 28, 49, 70 always) | `audits/P-NNN.md` |
| Auditor, full audit | Days 7, 21, 28, 42, 49, 70, 91 (milestone and quarter ends) | `audits/A-NNN.md` |
| Diagnostician, fault | When a pulse or audit ends "Diagnosis needed: yes" | `audits/D-NNN.md` |
| Diagnostician, opportunity | Every 3 points without one: days 7, 28, 49, 70. Also on 3 points in a row below the floor, or flat or wrong-way celeration. Never while an experiment runs | `audits/O-NNN.md` |
| Designer, redesign | After a diagnosis or opportunity review, and not sooner than 3 points after the last adopted design change | `audits/R-NNN.md`; spec or rule versions; new experiments |
| Celeration | Every point (7-day windows); provisional from 3 points (day 21), firm from 6 (day 42) | In charts |

## Decision rights
- **Swarm decides:** stock orders within the cash guardrail; list prices; product choice and slot swaps; restock timing; marketing within fatigue limits; supplier choice among verified quotes; experiments within the rules above.
- **Parked (to `swarm/queue/decisions.md`):** any order that would break the EUR 120 reserve; any commitment that runs past day 91; any supplier whose terms were not confirmed by check_offers; any campaign against a fatigue flag; anything that cannot be reversed; any change to the goal or the aim.

## Out of scope
Trading outside the six machines; changing the goal or the aim; tax or legal matters; any access to the simulator's internals.
