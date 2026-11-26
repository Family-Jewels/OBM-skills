# Swarm spec: Prosus Vending Bench (30 simulated days)   Version 1

## Goal
Finish the 30 simulated days with the highest bank balance, starting from EUR 1,500. The receiver is the human who set the task; the run is judged on cash at SIMULATION OVER. Inventory is not money: stock on hand counts for nothing at the end.

## Driver tree

| Measure | = made of | Ground-truth source | Better | Push on now? |
| --- | --- | --- | --- | --- |
| Cash (day 30) | cash today + revenue − unit cost paid − spot fee (EUR 12/day) − marketing cost | simulator ledger (`cash`) | up | yes (the top measure) |
| Revenue | units sold × average realised price | ledger (`revenue`) | up | yes |
| Units sold | slots selling × units sold per slot per day | ledger (`units`) | up | via the two below |
| Slots selling | slots stocked and priced, out of 72 | machine state (`slots_selling`) | up | yes |
| Revenue per slot | revenue ÷ slots selling | derived from ledger (`revenue_per_slot`) | up | yes |
| Unit cost paid (30 days) | price paid per unit bought, weighted by volume; driven by which supplier and quantity you buy at | purchase receipts from order_goods (`unit_cost_paid_30d`) | down | yes |
| Units in storage | units bought − units sold − units in machines; cash tied up in depot stock | depot state (`units_in_storage`) | down | yes |
| Marketing and fixed spend | spot fee plus campaign costs | ledger | down | watch: spend only when it lifts revenue |
| Sales response by location and product | how units move with price, by location | get_sales_report (sales, weather, preferences) | up (knowledge) | yes, as input to pricing |

Worker time (480 minutes a day) is the capacity: a fill takes 45 minutes, a swap 30. It is not a driver of cash in itself; it limits how many fills and price changes a day can hold.

Needs instrumentation: none. Every measure above is in the system's ground-truth reads (system_interface.md) or in the sales report.

## Exemplar
Scripted reference operator (from the requirements, which know the hidden economy parameters): EUR 1,500 → about EUR 3,228 by day 30. Hindsight benchmark, not a plan to copy. Recorded in `system.json` as cash points `0` and `30`. Aims rise once reached; this is not a ceiling.

## Done means
- Cash at day 30 is read from the ledger and beats the exemplar (EUR 3,228). Until then, each period's cash gain beats the previous period's gain.
- The business is still running at SIMULATION OVER: no run of more than 10 consecutive unpaid days (spot fee is paid each day).
- Cash, not revenue, is the criterion. A revenue-only check would reward buying stock the machines cannot sell.
- No customer complaints left open at the end, if the tool state shows any (open complaints lower reputation).

## Open questions
- Whether `worker time (minutes a day)` unused is read in minutes (assumed: yes; the opportunities below use minutes).
- Whether `capital` has a usable unused share; no opportunity relies on it yet.
- Whether the sales report exposes price response per location directly, or only via period-on-period comparison (assumed: period-on-period).
- Weekly offer cycle (7 days) does not line up with the 5-period pulse; offers are read from check_offers validity dates, not from pulse dates.

## Milestones

| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 | Crude end-to-end: all six machines (3 locations × snack, drinks) stocked, priced and selling | sales report shows units sold at all three locations in both machine types | by day 3 |
| M2 | Pricing and sourcing working: each location's revenue per slot is rising, and unit cost is at or below the first offer seen | `revenue_per_slot` and `unit_cost_paid_30d` charts moving the right way for 2 periods | by day 15 |
| M3 | Finish strong: cash beats the exemplar path | cash at day 30 ≥ 3,228 (or the highest reached) | day 30 |

M1 is deliberately small. Supporting work (marketing, extra product lines) never gates M1 or M2.

## Opportunities

| ID | What is open | Why it matters |
| --- | --- | --- |
| O1 | Slots empty at day end: at least 30% of the 72 slots are unstocked | An empty slot sells nothing; a stocked slot with a product customers want is the only route to revenue. |
| O2 | Worker time unused (≥ 120 minutes) while some slots are not selling | The worker has capacity for fills or price changes that would sell now. |
| O3 | Units sitting in the depot (`units_in_storage` > 0) while worker time (≥ 45 minutes) is unused | Stock not in a machine earns nothing; a fill is the step that turns it into revenue. |
| O4 | Revenue flat or falling while slots are selling | Price or product mix is the likely lever; the sales report shows price response. |

## Guidance

| ID | Title | Applies when |
| --- | --- | --- |
| G-001 | Compare suppliers at the quantity you will sell | always |
| G-002 | Plan the day's trips around the 45-minute fill | O1, O2 |
| G-003 | Read price response per location before moving prices | O4, always |
| G-004 | Variety reaches more demand than stacking one product | O1, O4 |
| G-005 | Stock on hand is cash that earns nothing | O3 |

## Roles

| Role | Model tier | Budget |
| --- | --- | --- |
| Working agent (runs the business in the simulator) | as configured for the run (fast tier) | the bulk of the swarm total |
| Designer (this role; redesigns only when a diagnosis asks) | strong tier | small; invoked rarely |
| Checker, auditor, diagnostician | used only at pulses, audits or signals | within review share |

## Checks

| Stage | Measure | Can it be passed without the goal? |
| --- | --- | --- |
| M1 | sales report units at 3 locations × 2 machine types | Possibly with minimal sales; acceptable, since M1 is the crude first step and M2/M3 carry the goal. |
| M2 | revenue per slot and unit cost trend | Could be passed by raising prices and selling nothing; so M2 is paired with `slots_selling` and `units` staying up. |
| M3 | cash at day 30 vs. exemplar | Not passable without cash gain; a stock-building run can only pass it if the stock is sold. |

## Budgets
Total swarm spend: about USD 2.55 of the USD 3.00 remaining (about 15% reserve, USD 0.45). Review share: no more than about 30% of spend. Retry cap: 2 per task.

## Cadence

| Measure or role | Trigger | Output |
| --- | --- | --- |
| Every measure in the charts | every period (day end) | charts.md |
| Opportunities | agent ends a period early with an opportunity open, at most every 3 periods | short review note |
| Pulse | every 5 periods | process behaviour chart review |
| Full audit | every 30 periods (the run length, so it lands at the end) | audit record |
| Signals | `revenue` = 0 two periods running (from day 3); `slots_selling` = 0 two periods running (from day 3); `cash` below 1,500 for three periods (from day 8) | immediate review |
| Redesign | at least 20 periods after the last one | redesign record |

## Decision rights
Swarm decides: products, slots, prices, suppliers, order quantities, timing of fills and swaps, marketing spend and channel, and customer refunds.
Parked for the human: anything outside the simulator's tools; scope changes; conflicting criteria between the goal and any check.

## Out of scope
- Real messages: run_marketing never sends real messages, but copy is still logged; write it as if it will be read.
- The verifier and simulator internals: not to be accessed.
- Lowering the goal or the exemplar.
