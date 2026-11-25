# Swarm spec: Prosus Vending Bench, 365-day operation   Version 1
## Goal
Maximise the bank balance at the end of the 365th simulated day (after card receipts settle), starting from EUR 1,500, by running three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with one SNACK and one DRINKS machine (72 slots in total). The receiver is the business owner. The goal is the human's; it is not lowered here.

Reference point (exemplar, not the goal): the benchmark's scripted reference operator, which knows the hidden economy parameters, reaches about EUR 3,228 at day 30 and EUR 61,219 at day 365.

## Driver tree
Top measure: **Final cash** (end balance, day 365). Cash at day t = 1,500 + cumulative revenue − cumulative unit cost paid − spot fee (EUR 12/day, EUR 4,380 over the horizon) − marketing cost − customer refunds.

| Measure | = made of | Ground-truth source | Better | Ceiling (source, confidence) | Guardrail | Push on now? |
| --- | --- | --- | --- | --- | --- | --- |
| Final cash | revenue − unit cost paid − fixed and campaign costs | bank ledger via get_status (cash), daily `cash` measure | up | Exemplar EUR 61,219 at d365 (benchmark reference, medium confidence: path known, mechanism hidden) | cash ≥ EUR 120 every day | (top) |
| revenue | units × realised price, summed over 6 machines | get_sales_report, daily `revenue` | up | Resource ceiling: 72 slots × best selling rate × price; not yet measured (low) | none extra | via drivers |
| slots_selling | slots holding stock AND a price | get_machine_inventory, daily `slots_selling` | up | 72 slots (resource ceiling, high) | no slot kept selling below unit cost | YES, priority 1 |
| revenue_per_slot | revenue ÷ slots_selling | derived from `revenue`, `slots_selling` | up | Exemplar-implied, to be read from pulse 1 (low) | price floor per product | YES, priority 2 |
| units sold per selling slot | demand by location × share captured (assortment, price) | get_sales_report units by location and product | up | unknown; test via reads, not experiments (low) | stock-outs kept below one refill cycle | via assortment |
| realised price | set_price per slot | get_sales_report, set_price log | up to the demand curve | competitor-free; price response read from sales reports (low) | AI-LOUNGE is price-sensitive: do not raise without reading its response | via pricing |
| unit cost | supplier price at order time | order receipts; daily `unit_cost_paid_30d` | down | Lowest quoted price across suppliers at quantity (medium) | never buy below a known margin on the product | YES, priority 3 |
| margin per unit | realised price − unit cost | derived | up | derived | margin ≥ 0 on every selling slot | with 2 and 3 |
| campaign spend | run_marketing costs | get_marketing_report | must repay: incremental revenue > cost | n/a | fatigue limits in get_marketing_report; cash ≥ reserve | NO until margin is stable (M3) |
| worker time used | minutes spent per period (refill 45, swap 30, price/read/order: as the clock shows) | simulator clock, daily `worker_minutes` | fully used, not over 480 | 480 min per working day (hard resource limit, high) | never past 480 min per day | the split in aims.md |

Driver notes: revenue_last_7 and revenue_same_7_a_month_earlier are read for trend and season; they are not controls. The spot fee is fixed and not a driver.

## Exemplar
Benchmark scripted reference operator: about EUR 3,228 at day 30 and EUR 61,219 at day 365 from EUR 1,500. Source: benchmark statement given to the designer (not the simulator). Own best: none yet; it is set after the first quarter.

## Resources
| Resource | How its use is measured |
| --- | --- |
| Worker time (the binding one) | minutes per working day from the simulator clock, against 480. Refill 45, swap 30, every other call its clock cost. Measured per point |
| Cash | get_status cash, daily `cash`; reserve EUR 120 |
| Slots (72) | get_machine_inventory: holding stock and priced (selling) vs empty vs stocked-not-priced (idle capital) |
| Depot stock | units bought vs units restocked; stock left at the depot is idle capital |
| Marketing budget and fatigue | get_marketing_report limits and recent campaigns per location |
| Supplier quantities and offers | check_offers quantity and validity date (offers change every 7 days) |

## Done means
- Cash on day 365, read after card receipts settle, is as high as the run can make it. This is the score.
- Cash ≥ EUR 120 at the end of every simulated day (the reserve guardrail).
- No bankruptcy: never more than 10 consecutive unpaid days.
- Every customer refund (send_payment) matched to its exact CMP- reference and full amount; no open complaints at the end.
- Every order is traceable to a check_offers quote in the same week and a receipt.

Must not change on the way: the cash reserve; no sale below unit cost; no unpriced stock left in a slot that could sell.

## Open questions
1. Exact minutes per read or price call are not stated; the system measures them from the clock in pulse 1 and the operator's time split is then re-set in aims.md.
2. Price response and per-location demand are not known; they are read from get_sales_report. No price experiments are run (the briefing rules them out), so price moves are small and logged.
3. Whether campaign spend pays back is unknown; it stays off until the margin is stable (M3).
4. Spoilage or expiry of stock is not described; if the depot shows loss, it is recorded and reported.
5. Card settlement lag means the day-365 cash is read after settlement; the designer assumes the final card receipts settle before the end.

## Milestones
| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 (days 0–28, points 1–4) | Crude end-to-end: all six machines stocked, priced and selling, supplier quotes taken, cash never below reserve | by day 28: slots_selling ≥ 48 of 72; cash ≥ EUR 120 every day; cash at day 30 read from the ledger and recorded against the EUR 3,228 exemplar | operator time and the first two quarterly budgets; no USD cap beyond the swarm budget below |
| M2 (days 29–91) | Margin: weekly check_offers before each order, pricing by location, refill cycle kept under one stock-out | unit_cost_paid_30d falls or holds while revenue_per_slot rises; quarter-1 audit passes | as above |
| M3 (days 92–182) | Campaigns only where they repay: one moderate campaign per location at most, judged against revenue_last_7 | incremental revenue over 14 days exceeds campaign cost, else the campaign is not repeated | as above |
| M4 (days 183–273) | Sustain and scale the pattern that the Strategist's aims show works | quarter-3 audit passes; celeration of final cash not flat | as above |
| M5 (days 274–365) | Close out: stop buying stock that cannot sell before day 365, settle refunds and card receipts, end with no open complaints | day-365 cash read after settlement; no open complaints | as above |

## Roles
| Role | Brief | Model tier | Retry cap | Budget |
| --- | --- | --- | --- | --- |
| Operator (orchestrator and worker in one: section 9, single-agent mode) | rules/operator.md | strong | 2 per action | the swarm budget below |
| Checker (verifies each order and refill claim against the ledger and receipt) | rules/checker.md | fast | 1 | within the review share |
| Auditor (pulse and full audits) | the obm-swarm-auditor skill | strong | 1 | within the review share |
| Strategist | the obm-swarm-strategist skill | strong | 1 | not part of the operating budget |
| Diagnostician, designer | their skills | strong | 1 | as needed, after a fault only |

## Checks
| Stage | Measure | Can it be passed without the goal? |
| --- | --- | --- |
| Each order | units and cost match the receipt; cash moved by the receipt amount | no: it checks what was actually paid |
| Each refill | slot holds the stated product and is priced; minutes charged match the clock | no: it reads the inventory and clock |
| Each point | cash, revenue, units, slots_selling, revenue_per_slot match the ledger | no: system-computed |
| Milestones and quarters | final cash path against the floor and aim, and the reserve | no: cash is the goal itself |

Note: a high cash balance could come from stocking nothing and holding cash. The check against slots_selling and the floor line rules that out.

## Budgets
- Swarm spend (model usage): USD 2.00 total. Reserve 15% (USD 0.30) kept back. Review share no more than 30% of spend.
- Operating capital: EUR 1,500 starting cash; reserve EUR 120 never spent; spot fee EUR 12/day is paid from cash.
- Operator time: 480 min per working day; target split in aims.md.

## Cadence
| Measure or role | Trigger | Output |
| --- | --- | --- |
| Measurement (system) | every simulated day | metrics_system.md, charts.md |
| Point | 7 simulated days (weekly offers and revenue_last_7 cycle) | one point = one week; horizon = 52 points |
| Auditor, pulse | every point; every second point after three quiet pulses; back to every point on any signal, redesign or new aims | audits/P-NNN.md |
| Auditor, full audit | day 91, 182, 273 and 365 (each quarter); each milestone close; before done | audits/A-NNN.md |
| Strategist | after point 3 (day 21), then every 3 points (days 42, 63, …); brought forward (after at least 2 points) when cash sits 3 points in a row below the floor line, or celeration is flat or wrong-way | audits/S-NNN.md |
| Designer, aim update | right after each Strategist redirect | aims.md and audits/AS-NNN.md |
| Diagnostician | when a pulse or audit ends "Diagnosis needed: yes" | audits/D-NNN.md |
| Designer, redesign | after a diagnosis; or after an aim update needing a design change (spaced 3 points after the last adopted change) | audits/R-NNN.md, spec.vN |
| Checker | every order and every refill at first; after 5 clean in a row, 1 in 3 sampled; after 10 more, 1 in 5 | review records |
| Weekly supplier pricing | each week, before any order (offers change every 7 days) | check_offers recorded with its validity date |

## Measurement spec (what the system writes; the designer does not write these)
- metrics_system.md, daily measures: cash, revenue, units, slots_selling, revenue_per_slot, revenue_last_7, revenue_same_7_a_month_earlier, unit_cost_paid_30d, plus worker_minutes (minutes used of 480) and resources in use and idle.
- charts.md: level charts with process limits computed from each measure's own data (centre ± 2.66 × average moving range) on 7-day points; signals (a point beyond a limit, or 8 in a row one side of the centre); celeration per measure over 7-day points, with bounce and a provisional/firm flag; the top measure's floor line (from its level at point 3 to the goal at the horizon) and aim line (deliberate overshoot: goal reached by half the remaining horizon); slots and capital in use vs idle; the cash-reserve guardrail at EUR 120; gap to the exemplar (ceiling ÷ current).
- Process limits are not set by hand. The reserve line is EUR 120, fixed by the brief.

## Decision rights
- Swarm decides: prices within the rules above; which slots to restock and with what; which supplier and quantity to order from after check_offers; the refill order; refunds; the weekly time split inside the aims.
- Parked (queued in queue/decisions.md, with a default): any campaign spend outside M3; any cut to the reserve; any stock purchase that cannot sell before day 365; any change to the spec or the goal.

## Out of scope
Price experiments (ruled out by the briefing); changing the goal, the reserve, or the spot fee; reading the verifier or simulator internals; any tool outside the business tools.
