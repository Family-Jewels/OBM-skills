# Swarm spec: Prosus Vending Bench, 365 simulated days   Version 2 (changes: audits/R-P-001.md; prior version history/spec.v1.md)

## Goal
Maximise the bank balance at the end of day 365, starting from EUR 1,500, by running six vending machines (SNACK and DRINKS at AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE). Receiver: the human who owns the network. Unfinished or bankrupt scores zero; more than 10 consecutive unpaid days ends the business. Never lower this goal.

Identity of the top measure: final bank balance = 1,500 + sum over days of (revenue − unit cost paid − spot fee €12/day − marketing − refunds − other spend). Cash in the bank is the measure the system charts as `cash`.

## Driver tree
Each part is read by the system from ground truth. Ceiling confidence: H/M/L.

| Measure | = made of | Ground-truth source | Better | Ceiling (source, confidence) | Guardrail | Push on now? |
| --- | --- | --- | --- | --- | --- | --- |
| **Final bank balance (cash)** | 1,500 + Σ(revenue − unit cost − spot fee − marketing − refunds − other) | get_status cash; ledger | up | 61,219 at day 365 (benchmark scripted reference, M: it knows hidden parameters, so a real ceiling is not proven) | cash ≥ EUR 120 every close | top measure, judged by the system |
| Revenue | units × average net price | get_sales_report; `revenue` | up | Exemplar revenue pace; no own best yet (own best) | none | via drivers below |
| Units sold | slots selling × units per selling slot-day | get_sales_report; `units` | up | Demand ceiling not known (reference class: exemplar) | never sell below unit cost | via drivers below |
| **Slots selling (capacity in use)** | slots stocked, priced and not empty, out of 72 | get_machine_inventory; `slots_selling` | up | 72 slots (resource ceiling, H) | none | **Yes, priority 1** |
| Worker fills per day | 480 min ÷ (45 min per fill + other calls) | get_status clock; work.jsonl minutes | up, to the time left after reads and pricing | about 10 fills per day with nothing else (resource ceiling, H) | fills never cut below the pricing and order minimum | **Yes, priority 1 (the constraint)** |
| Units per fill | units restocked per fill, weighted to fastest sellers | restock receipts; sales report | up | Machine capacity: 18 units small rows, 10 units large rows and drinks (resource ceiling, H) | fill only products with a set price | **Yes, priority 2** |
| Revenue per slot | revenue ÷ slots selling (daily) | `revenue_per_slot` | up | Exemplar-implied pace (benchmark, M) | none | Yes, follows priority 1–2 |
| Units per selling slot-day | demand by location and product, after stock-outs | get_sales_report by location | up | Own best, to be set after day 30 (own best, L) | none | Watch, not pushed directly |
| Average net price | set price − unit cost, sold-weighted | set_price log; sales report | up, but not at the cost of units | Reference class: price response read from sales report (L) | price ≥ unit cost + minimum margin; AI-LOUNGE is price-sensitive | Yes, after day 14, once price response is read |
| **Unit cost paid, 30 days (cost driver)** | cost paid per unit, from order receipts | `unit_cost_paid_30d`; order receipts | down | Lowest quote seen at the same quantity (own best, M) | never pay more than the best check_offers quote in the same week | Yes, priority 3 |
| Spot fee | fixed €12/day | ledger | — | fixed | must be paid each day | not controllable |
| Marketing spend | per campaign cost | get_marketing_report | down unless traffic gain pays back | — | fatigue limit from get_marketing_report | Not until day 30 |
| Refunds and complaints | refund amounts; open complaints | ledger; complaints | down | 0 | open complaints lower reputation | Watch |

Seasonality check: `revenue_last_7` against `revenue_same_7_a_month_earlier` (both system-measured). Read it, do not act on it alone.

## Exemplar
Benchmark scripted reference operator (knows hidden parameters): about EUR 3,228 at day 30 and EUR 61,219 at day 365 from EUR 1,500. Implied growth: about 7.7% per day to day 30, then about 0.9% per day on average to day 365. Source: system brief. Gap to the exemplar (PIP) is computed by the system.

## Resources
| Resource | How its use is measured |
| --- | --- |
| **Worker time (480 min per working day, 09:00–17:00)** | Minutes per day used by each tool call, read from the simulator clock: refill 45, swap 30, price or read calls a few minutes each. Share by activity (section Time split in aims.md). This is the binding constraint. |
| Machine slots (72: 6 machines × SNACK/DRINKS slots) | slots_selling ÷ 72; idle slots = empty or unpriced |
| Capital | Cash in bank (cash), capital in stock (depot plus in slots), idle cash above the reserve |
| **Supplier lead time** | Days from order_goods to delivery, read from receipts. Observed: 3 days (PO-1003), 4 (PO-1004), 5 (PO-1001, PO-1002); PO-1005 took 14 (late). Stock cannot be filled before its delivery day, so orders are planned a lead time ahead of the fills they enable. |
| Supplier credit and card settlement | Card receipts settle a day later; outstanding card receipts settle at end |
| Marketing budget | Spend per location per week against get_marketing_report limits |

## Done means
- Day 365 reached (SIMULATION OVER) with bank balance as large as possible.
- Cash at every daily close ≥ EUR 120, and spot fee paid every day (zero unpaid days).
- Each order's unit cost ≤ the best check_offers quote for the same quantity and week.
- No price set below unit cost; no slot left unpriced while it holds stock.
- Revenue for the last 30 days exceeds the previous 30 (read from the sales report).

## Open questions
1. Is restock_machine's 45 minutes per slot or per machine visit? The design assumes per slot; the first fill decides this.
2. Travel between locations: does moving between machines cost minutes beyond the tool calls? Read from the clock.
3. Does a restock fill a slot to its maximum or to a chosen quantity? Read from the first receipt.
4. Price response by location (AI-LOUNGE most price-sensitive) is not known; read it from get_sales_report during normal operation. No designed experiments.
5. Supplier reliability (delays, short-shipping, failure) is not known beyond the lead times above. Track it from receipts against orders; do not assume it.
7. Minutes conflict (audits/D-P-001.md): the charts' resource median (65 min a day) disagrees with work.jsonl (about 400 min on day 7). The system settles it from the simulator clock; it is not changed here.
6. Whether the system's point and horizon match: the design assumes one point = 7 days (the weekly offer cycle), so about 52 points. The system derives the actual window.
No instrumentation gap: all top-level measures are in the system's daily list.

## Milestones
| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 | Crude end-to-end: all six machines stocked and priced with the best available products, first sales read, cash above reserve every close | By day 7 the day-7 target was missed (slots_selling 15 at day 10 on stock that arrived day 6–11). Carried to day 14 with the target unchanged: slots_selling ≥ 36; cash ≥ 120 at every close; each order priced at or below the best quote; get_sales_report read for all three locations | Initial cash minus the reserve; M1 uses no more than EUR 800 of stock in the first two weeks |
| M2 | Full coverage: slots_selling ≥ 60 and refill loop running at ~10 fills per day | By day 30: slots_selling ≥ 60 on 5 of the last 7 days; revenue_last_7 rising for 3 points | Ongoing stock spend within cash minus reserve |
| M3 | Price and mix tuned from read sales data | By day 90: average net price up without units dropping below the prior 30-day level | Within the time split |
| M4 | Marketing used only where traffic pays back | By day 182: each campaign's cost recovered by sales within 14 days, or none run | Marketing ≤ 5% of worker time and ≤ 5% of revenue |
| M5 | Run to day 365 with the loop steady | Full audit at day 273 and day 365 passes | — |

## Roles
The operator is the only worker and does every role in turn (protocol section 9): orchestrator, checker of its own records by the system, and diagnostician by the system's audits. The system invokes each role at the cadence below.

| Role | Brief | Model tier | Retry cap | Budget |
| --- | --- | --- | --- | --- |
| Operator (worker and orchestrator) | rules/operator.md | strong | 2 per action | Worker time 480 min per day |
| Designer | this spec | strong | — | As the system allows |
| Strategist | obm-swarm-strategist skill | strong | — | As the system allows |

## Checks
| Stage | Measure | Can it be passed without the goal? |
| --- | --- | --- |
| M1 | slots_selling ≥ 36 by day 7 | Yes: slots can be filled with low-margin or slow products. Add: revenue_per_slot must be rising by day 14 |
| Each day | cash ≥ 120 at close | No: this is direct |
| Each order | unit cost ≤ best quote, same week | Yes: the operator could buy the cheapest quote and sell nothing. Add: slots_selling must not fall after the order |
| Each price change | price ≥ unit cost + minimum margin | Yes: a price could be correct but still zero units. Add: units must not fall more than 30% after a price rise |
| Day 365 | bank balance | Direct |

## Budgets
- Total: the full business cash at start (EUR 1,500) minus the reserve. Reserve: EUR 120 hard floor, with a working reserve of EUR 120 more before any order that uses more than 40% of cash.
- Idle capital: cash above EUR 240 with no order open may be committed to stock, in one or more orders each within the best quote, each under 40% of cash. Capital is not to sit idle while slots are short.
- Review share: the system's pulses and audits only. The operator does not review its own records.
- Marketing: no spend before day 30.

## Cadence
| Measure or role | Trigger | Output |
| --- | --- | --- |
| Measurement (system) | Every day | metrics_system.md, charts.md |
| Operator daily loop | Each working day: read board.jsonl and status, fill and price, order, log the day, then wait_for_next_day. A day with no log line counts as missed in the pulse | log/progress.md, log/runs.jsonl, log/work.jsonl |
| Pulse review (auditor) | Every point (7 days) | audits/P-NNN.md |
| Full audit (auditor) | Quarter ends: about day 91, 182, 273, 365; milestones; before done | audits/A-NNN.md |
| Strategist | After points 3, 6, 9, …; brought forward after at least 2 points when the top measure is below its floor 3 points in a row, or celeration is flat or wrong-way | audits/S-NNN.md |
| Designer, aim update | Right after each Strategist redirect | aims.md, audits/AS-NNN.md |
| Diagnostician | When a pulse or audit says Diagnosis needed: yes | audits/D-NNN.md |
| Designer, redesign | After a diagnosis, or an aim update that needs a design change; at least 3 points after the last adopted change | audits/R-NNN.md, spec/rules versions |

## Decision rights
Swarm decides: which products go into which slot, prices (above unit cost), order quantities within the reserve, supplier choice among quotes, marketing within the limit above, the order of fills and swaps within the time split.
Parked (log in queue/decisions.md, continue with the default): any single order above 40% of cash; changing the supplier that just failed to deliver; any action that cannot be reversed (clear_slot of stock that could be sold); refunds beyond the stated complaint.

## Out of scope
Tool-surface access beyond the business tools; the simulator's internals and verifier; new locations; anything outside the six machines.
