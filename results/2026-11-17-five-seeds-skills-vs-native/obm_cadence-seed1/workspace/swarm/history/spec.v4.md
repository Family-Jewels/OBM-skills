# Swarm spec: Prosus Vending Bench, 365 simulated days   Version 4
## Goal
Maximise the bank balance at the end of the 365-day simulation, starting from EUR 1,500, without bankruptcy (more than 10 consecutive unpaid days ends the business) and without leaving complaints open. Receiver: the human operator who reads the final balance.

## Driver tree
Measures are per simulated period unless stated. "Source" is ground truth; the operator never reports these about itself.

| Measure | = made of | Ground-truth source | Better | Push on now? |
| --- | --- | --- | --- | --- |
| Final bank balance (day 365) | Start 1,500 + cumulative revenue − cumulative cost of goods − cumulative spot fees (EUR 12/day) − cumulative marketing − refunds, with card receipts settled at end | Bank/cash ledger via get_status; system `cash` | Up | Yes (top measure, judged at the end) |
| cash_gain_7 | Cash on this calendar date − cash on the date 7 calendar days earlier (a missing day's row is not skipped; the window is dated, not a row count) | System (charts.md) | Up | Watch; signal = trend change |
| Revenue (per day) | slots_selling × revenue_per_slot | get_sales_report; system `revenue` | Up | Yes |
| slots_selling | Slots holding priced stock with demand, summed over 6 machines (72 slots total) | get_machine_inventory; system `slots_selling` | Up toward every demand-bearing slot | **Yes, first** (capacity in use) |
| revenue_per_slot | Units sold per selling slot × unit price | get_sales_report; system `revenue_per_slot` | Up | Yes (price and mix) |
| Units | Sum of units sold across slots | get_sales_report; system `units` | Up | Yes (restock and mix) |
| revenue_last_7 vs revenue_same_7_a_month_earlier | Seasonal control: last 7 days revenue against the same 7 days a month earlier | system measures | Up (ratio above 1) | Read only; separates seasonality from our effect |
| Gross margin per unit | Unit price − unit cost paid at order (order_goods receipts) | Order receipts ledger; **needs instrumentation** (operator logs each receipt's actual cost in log/runs.jsonl) | Up | Yes (supplier terms, price) |
| Stock-out share | Selling slots empty ÷ slots that should sell | get_machine_inventory; **needs instrumentation** (system to add per-slot empty days) | Down | Yes (restock cadence) |
| Restock trips per day (throughput) | Slot fills completed per day; depot-to-slot lag = depot units not yet in slots | Operator tool-call log; depot and slot counts from get_machine_inventory; **needs instrumentation** (system to chart trips and depot-minus-slot units) | Up (trips); down (lag) | Yes, with slots_selling (v3, day 77) |
| Marketing return | Revenue gained at a location in the 14 days after a campaign ÷ campaign cost | get_marketing_report + sales; **needs instrumentation** | Up | Later (after M4) |
| Fixed cost | EUR 12/day spot fee | Ledger | Fixed | No lever; never let it go unpaid |

Operator-controlled drivers (leaves of the tree): (a) which product sits in which slot (swap_item, restock_machine); (b) how many slots are kept filled (restock trips, 45 min each, within the 8-hour day); (c) price per product (set_price); (d) which supplier and offer to buy from (check_offers weekly, order_goods); (e) quantity bought per order; (f) marketing spend per location and channel (run_marketing, get_marketing_report).

Priority: (a) to (d) first. Marketing is a later lever because fatigue and cost can erase the gain.
Redesign v2 (day 23, see audits/R-P-003.md): quantity per order (e) is pushed now, sized per product from demand. Stock-out share is the measure it should move.
Redesign v3 (day 77, see audits/R-P-010.md): the binding constraint is restock throughput (b), not quantity (e). Restock trips come before ordering; orders net off depot stock. Restock trips per day and depot-to-slot lag are pushed now.
Redesign v4 (day 112, see audits/R-A-002.md): direction unchanged; the binding driver (b) was steered without a chart. Restock trips per day and depot-minus-slot units are now charted by the system (Cadence). Push (b) with slots_selling; stock-out share is the test. Operator brief unchanged.

## Exemplar
Scripted reference operator of the benchmark. It knows the economy's hidden parameters. Reference trajectory: about EUR 3,228 at day 30 and about EUR 61,219 at day 365, from EUR 1,500. Use it as the gap measure (PIP = exemplar ÷ swarm balance at the same day). It is an aim, not a plan: the swarm must not try to read hidden parameters, the verifier, or simulator internals. Aims rise once reached; none is a ceiling. Until the operator's own history exists, the own best period serves.

## Done means
1. The simulation reaches SIMULATION OVER at day 365 with the business still operating (no bankruptcy, no run of more than 10 unpaid days).
2. Final balance is the top measure; reported with its exemplar gap at days 30, 100, 200 and 365.
3. Cash stays above a reserve of EUR 150 (about 12 days of spot fees) at the close of every day after day 3. Reserve breach is a failure of the operating loop, not a reason to stop buying stock that will sell.
4. Revenue over the last 30 days exceeds the previous 30 days, read from the ledger, at every full-period check after day 60, unless a seasonal control (revenue_same_7_a_month_earlier) explains the fall.
5. Complaints open at the end: zero. Every refund (send_payment with a CMP- reference) matched exactly.
6. No open order or payment unresolved at the end, and card receipts accounted for.

Must not change on the way: the reserve; the 10-day unpaid-fee limit; the record of spend in log/runs.jsonl.

## Open questions
- Hidden demand parameters: unknown to the swarm. Learn only from get_sales_report by location (price response, preferences, weather, season).
- Whether a supplier can short-ship or go out of business: check each delivery against the order.
- Whether the simulator's marketing fatigue recovers within a week: measure it on the charts before repeating a campaign.

## Milestones
| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 | Crude end-to-end loop: a supplier found, stock bought, all six machines stocked and priced, daily check of cash and sales running | slots_selling ≥ 1 in each of the six machines by day 3; cash recorded daily; ledger entry for every order | Day 0–3 |
| M2 | Restock and price loop running every day: 72-slot capacity used where demand exists | slots_selling at or near the count of demand-bearing slots for 7 consecutive days; revenue_last_7 rising for 14 days | Day 4–30 |
| M3 | Supplier and mix optimisation: cheaper unit cost, product choice per location (savoury snacks and coffee at AI-LOUNGE; hungry-customer products at AI-HOUSE; high-footfall mix at MAIN-LOUNGE) | gross margin per unit up on the charts; revenue_per_slot up; no stock-out signal | Day 31–120 |
| M4 | Marketing used at MAIN-LOUNGE and AI-HOUSE where the return is measured positive | marketing return above 1 over 14 days per campaign; no fatigue signal | Day 121–250 |
| M5 | Hold to the end: keep the loop, rest on the charts, close the books | SIMULATION OVER reached; balance and gap reported | Day 251–365 |

M1 is a crude end-to-end version of the whole business (buy, stock, price, sell, count cash), not a foundation for later refinements. Supporting analysis never gates the daily loop.

## Roles
| Role | Brief | Model tier | Retry cap | Budget |
| --- | --- | --- | --- | --- |
| Operator (worker, daily loop) | rules/operator.md | Strong | 2 per task | Each day's tool calls fit in the 8-hour day (about 1 restock trip per 45 min) |
| Measurement (system) | none: writes metrics_system.md and charts.md daily | — | — | — |
| Auditor (system) | pulses every 5 days; full audits per Cadence | Strong | — | Reviewed against charts, not the operator's notes |
| Diagnostician (system) | on request from a pulse or audit | Strong | — | — |
| Designer (this role) | redesigns only on callback | Strong | — | — |

Single-agent mode (protocol section 9): the operator plays worker and runs its own checks from the ledger; it never judges its own work as done.

## Checks
| Stage | Measure | Can it be passed without the goal? |
| --- | --- | --- |
| M1 | slots_selling ≥ 1 in all six machines by day 3 | Yes, a few cheap slots can pass. Add: revenue > 0 on each machine within 5 days |
| M2 | slots_selling near demand count for 7 days | Yes, stocking without pricing sells nothing. Add: revenue_per_slot rising |
| M3 | gross margin per unit up | Yes, raising prices can cut units. Add: units not falling at the same time (revenue_per_slot up) |
| M4 | marketing return above 1 | Yes, a single lucky campaign. Add: two campaigns both above 1 |
| Final | final balance vs exemplar | Yes, a bigger reserve with no sales keeps cash flat. Add: revenue last 30 days beats the prior 30 |

## Budgets
- Money (the business): hold a reserve of EUR 150 at every daily close after day 3. Spend on stock and marketing only when the expected revenue from it, read from the charts, exceeds its cost.
- Agent budget: the operator's tool calls fit in the 8-hour working day each simulated day. Review share: no more than about 30% of calls spent on reading or auditing.
- Reserve for the swarm's own calls: about 15%.

## Cadence
| Measure or role | Trigger | Output |
| --- | --- | --- |
| Cash, revenue, units, slots_selling, revenue_per_slot, revenue_last_7, revenue_same_7_a_month_earlier | Every simulated day (system) | metrics_system.md |
| cash_gain_7, revenue, slots_selling, revenue_per_slot, units | Every simulated day (system) | charts.md with limits from own data |
| Restock trips per day; depot-minus-slot units (v4: system must chart both by day 116; until then the operator logs trips in log/runs.jsonl) | Every simulated day (system) | charts.md, with limits from own data |
| Since-redesign table | Every simulated day (system): apply the 8-in-a-row rule to each row, not only the 25-point mean | charts.md |
| Exemplar gap (PIP) | Every simulated day (system): exemplar balance ÷ swarm balance, as defined in Exemplar; not the gain ratio | charts.md |
| Operator daily loop: read status, sales, inventory; restock; price; log | Every day, before wait_for_next_day | log/progress.md, log/runs.jsonl |
| check_offers and any new order | Weekly, when offers change (every 7 days; check validity date) | log/runs.jsonl |
| Auditor pulse | Every 5 simulated days | audits/P-NNN.md (signals against routine variation; up to three pivots) |
| Auditor full audit | Every 50 days (days 50, 100, 150, ...), at milestones M1–M5, and before done | audits/A-NNN.md |
| Immediate audit | A chart signals a change in the wrong direction (cash_gain_7 falling past its limit, or slots_selling dropping) | audits/A-NNN.md |
| Diagnostician | When a pulse or audit says "Diagnosis needed: yes" | audits/D-NNN.md |
| Designer redesign | After a diagnosis, or a full audit finding the direction wrong; spaced at least 20 days apart | audits/R-NNN.md and new spec or rule versions |
| Reserve check | Daily close | Recorded in progress.md; any breach handled that day |
| Exemplar gap | Days 30, 100, 200, 365 | Reported to the operator |

## Decision rights
Swarm decides: prices, product per slot, restock schedule, which supplier and quantity (within the reserve), marketing within the cost limits, refunds and complaints.
Parked (written to queue/decisions.md with the default taken at once so the day continues): any purchase or marketing spend that would take cash below the reserve; any change to location footprint (no new machines or sites); any action the system's rules do not list.

## Out of scope
Changing the business rules, the hidden parameters, the verifier, or the simulator. Any access to these is forbidden. Any action the business tools do not provide.
