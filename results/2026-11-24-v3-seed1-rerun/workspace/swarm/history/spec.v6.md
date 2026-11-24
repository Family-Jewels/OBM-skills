# Swarm spec: Prosus Vending Bench, 365 days   Version 6
## Goal
Maximise the bank balance at the end of simulated day 365, starting from EUR 1,500. Receiver: the human owner, judged on final balance. Inventory is not in the score; unsold stock is a cost of capital, not an asset.

Operating model: one operator agent is both worker and orchestrator (protocol section 9). There is no separate checker; every measure is computed by the system from ground truth (the bank, the sales ledger, the machine inventory and the simulator clock), never from the operator's own report.

Point = 7 simulated days (one week). It matches the weekly offer cycle and gives about 52 points over the horizon. Day 30 is point 4 or 5; the first Strategist runs after point 3 (day 21).

## Driver tree
Top measure: final cash, day 365. Each row is made of the rows indented under it.

| Measure | = made of | Ground-truth source | Better | Ceiling (source, confidence) | Guardrail | Push on now? |
| --- | --- | --- | --- | --- | --- | --- |
| M0 Final cash, day 365 | 1,500 + Σ revenue − Σ unit cost paid − Σ marketing − Σ spot fees (EUR 12/day) | bank ledger (system cash series) | up | 61,219, scripted reference operator with hidden parameters (high confidence the number is reachable; per-driver values unknown) | cash ≥ EUR 120 every day; never more than 10 consecutive unpaid days | top measure, not pushed directly |
| M1 Gross margin per day | revenue − cost of units sold | cash ledger; unit_cost_paid_30d × units | up | back-solved from the reference: about EUR 176/day gross margin before marketing (low–medium confidence) | no sale below unit cost unless deliberate clearance | yes, via M2 and D3 |
| M2 Revenue per day | slots_selling × revenue_per_slot | system revenue and slots_selling | up | own best, set by the Strategist after point 3 (low confidence) | none beyond M1 | yes |
| D1 slots_selling | slots stocked, priced and selling, of 72 (6 machines × 12) | machine inventory; system slots_selling | up to demand, not to 72 | 72 slots, machine capacity (high confidence on count; low on demand, since duplicate slots share one customer pool) | no stocked slot without a price; no duplicate slot beyond sell-through | yes |
| D2 revenue_per_slot | units per slot per day × price | system revenue ÷ slots_selling | up | own best (low) | price never below unit cost | yes |
| D2a price | price set per slot | set_price log; sales report price response | at the level that maximises margin per day, read from observed response | own best (low) | not below unit cost | yes |
| D2b product mix | product placed in each slot | sales report by product and location | up; savoury snacks and coffee in the picky lounges, hearty snacks in AI-HOUSE | own best (low) | none | yes |
| D2c footfall | traffic multiplier from marketing | get_marketing_report; traffic multipliers | up while margin covers cost | report limits (medium) | fatigue across channels; spend only when payback is visible in sales | later, only after point 6 |
| D3 unit_cost_paid_30d | cost per unit paid, rolling 30 days | system, from order receipts | down | own best; quoted offers at equal quantity (medium) | no order that takes cash below the reserve; order enough that each selling slot's depot stock lasts until the next delivery could arrive: the supplier lead time (7 and 14 days seen, PO-1001, PO-1002) plus the 7-day offer cycle, up to the current D1 aim; the EUR 120 reserve is the only limit on order size (no cap beyond that cover, because a cap leaves the depot empty at refill time) | yes |
| D4 worker minutes per week used on selling work | refills, swaps, price and order actions, reads (minutes from the simulator clock) | simulator clock; system worker-time measure | revenue per worker-minute up | 480 minutes per working day, the resource ceiling (high confidence) | keep 72 min/day unused as slack; minutes of refills that fail at the depot are not counted as selling work (see D4a) | yes, as the constraint |
| D4a failed-refill minutes | minutes on refill calls that return a depot shortfall (no stock for the slot) | simulator clock, per refill call; the operator's depot read before each refill block (logged); needs instrumentation (not yet in metrics_system.md) | down, to zero | none; zero is the target (high confidence) | a refill is started only when that block's depot read shows the product for that slot | yes, as a precondition of D4 |
| D5 idle capital | cash above what the reserve and next order need, plus unsold stock at cost | system capital measure | down | none; measured only | cash reserve EUR 120 | watched, not pushed |

Resources and idle measures sit under D4 and D5 in the charts (see Resources).

## Exemplar
Scripted reference operator (knows the economy's hidden parameters): about EUR 3,228 at day 30 and EUR 61,219 at day 365 from EUR 1,500. Back-solved: day 30 requires about EUR 58/day net gain on average; day 365 requires about EUR 176/day gross margin after spot fees (EUR 4,380 over the year) and before marketing. These are aggregates; per-driver exemplar values are not known and the Strategist must treat them as unknown until observed. Improvement exemplar: the swarm's own best celeration.

## Constraint
The worker's time, not capital, is the binding limit from about day 20 on. One refill is 45 minutes, so at most about 10 refills a day with nothing else. Before that, capital is the co-constraint: EUR 1,500 must fill and price the first selling slots without falling under the reserve.

## Resources
| Resource | How its use is measured |
| --- | --- |
| Worker time (480 min per working day, 09:00–17:00) | Minutes spent per day from the simulator clock, by activity: refill 45, swap 30, price, order, read (each call's cost, read from the clock). Share in use and idle each day. Always the first resource on the charts. |
| Cash | Cash balance daily; cash in use = cost of stock in machines and depot plus marketing committed; idle = cash above the reserve and the next order. |
| Slots (72: 6 machines × 12) | Slots selling, slots stocked but unpriced, slots empty. Idle = empty or unpriced. |
| Depot stock (capital in use) | Value at cost of stock not yet sold; age in days; by product before each refill block. Refill failures for lack of depot stock are counted per week. |
| Marketing allowance | Cost and remaining limit per location from get_marketing_report. |
| Supplier order capacity | Orders placed, delivery delays and short-shipments from receipts. |

## Done means
- The simulation runs to day 365 with the business still open (no bankruptcy) and all card receipts settled at the end.
- Final cash is the measure of success; the system reports it against the floor and aim lines (section 8 of the protocol).
- Checks that cannot be passed without achieving the goal: (1) cash grows week on week against the floor line, not just stays above EUR 120 (staying above the reserve by doing nothing passes the reserve check and fails this one); (2) units sold are read together with margin, since units can rise by selling at a loss; (3) slots_selling counts only slots with a positive margin, since a slot stocked with a loss-making product passes a count check and fails this one.

## Open questions
1. Does restock_machine fill a whole slot, or a fixed number of units? (Measured from the first refill; the log decides the refill quantity.) Still open at day 174: the log has no entries after day 135. From version 6 every refill call is logged with slot, product, units loaded and clock minutes (rules/operator.md, version 5). This answer, with minutes per refill, decides whether the D1 aim is reachable: at 45 minutes a refill, 12 stocked slots need 540 minutes, above the 408 usable.
2. Time cost of price and status calls: assumed a few minutes each; the simulator clock confirms this on day 1.
3. Is the EUR 12 spot fee charged automatically each day? Assumed yes; cash is checked before each day ends.
4. Supplier lead time and reliability: observed 7 days (PO-1001) and 14 days (PO-1002, PO-1004 about 2 days); reliability still open; record each delivery in the log.
5. Per-driver exemplar values (price response, product mix, footfall) are unknown; the Strategist sets own-best aims after the first three points.
6. The revenue_same_7_a_month_earlier measure has no value until day 37; show it as not available before then, not as zero.
7. Adapter gap: the system measures worker minutes from the simulator clock and must not take the operator's self-report of time; confirm it does so from day 1. Open at day 121 (D-P-005): the chart shows zero minutes on the latest day while the log shows about 410 min of clock use on day 108. The auditor must settle which reading is the simulator clock before D4 and D4a are judged. Still open at day 163 (D-P-006): the clock median is 0 minutes over the last 7 days, while the log shows 365 to 410 minutes a day on days 118 to 135. Until settled, a day whose clock reading is below its logged refill minutes is unmeasured for D4, not zero, and the diagnostician is called. The designer does not change the adapter.
8. Slot count reconciliation (AS-001, D-P-002): slots_selling (11) and slots stocked at day end (5) disagreed at day 26. The system must reconcile them before the D1 aim is judged. Not changed by R-P-002.
9. Margin per slot (D2a price-finding method; D3 unit-cost comparison across offers) has no working method in this design (AS-001). Next redesign, not R-P-002.

## Milestones
| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 | Crude end-to-end: every one of the 6 machines has at least one priced, selling slot, bought from a checked supplier offer | 6 of 6 machines show ≥1 slot selling with price above unit cost; cash ≥ EUR 120 after the first order; a day has closed with a sales record | ≤ EUR 900 committed in M1; ≤ 150 worker minutes |
| M2 | Day-30 level reached, about EUR 3,228 | cash at day 30 at or above the reference, read from the bank | cash-neutral; worker minutes per day within 480 |
| M3 | End of quarter 1 (day 91): cash growing week on week, D3 falling | Q1 full audit passes; floor line not broken for 3 points | as above |
| M4 | Mid-year (day 182): slots_selling and revenue_per_slot both rising | Q2 full audit passes | as above |
| M5 | Quarter 3 (day 273): capacity in use near 480 min/day with slack held | Q3 full audit passes | as above |
| M6 | Final: day 365 | final cash read from the bank; card receipts settled | as above |

Milestone 1 is planned in detail on the board; M2–M6 are one line each.

## Roles
| Role | Brief | Model tier | Retry cap | Budget |
| --- | --- | --- | --- | --- |
| Operator (worker and orchestrator) | rules/operator.md | strong | 2 per task | ≤ 85% of worker minutes per day (72 min kept as slack) |
| Measurement (system) | none; computed daily | — | — | — |
| Auditor (system-invoked) | per protocol | strong | — | per cadence |
| Strategist (system-invoked) | obm-swarm-strategist | strong | — | per cadence |
| Designer (system-invoked) | obm-swarm-designer | strong | — | per cadence |

## Checks
| Stage | Measure | Can it be passed without the goal? |
| --- | --- | --- |
| Every day | cash ≥ EUR 120 | Yes, by doing nothing. Read with the floor line, so it cannot be the only check. |
| Every week | M1 gross margin positive, D3 not rising | Hard to pass without the goal; this is the direct check. |
| Every week | slots_selling, with positive margin per slot | Counts only margin-positive slots, so stocking loss-makers does not pass. |
| Every point | revenue_per_slot against unit cost | Revenue alone can rise by selling at a loss; this check cannot. |
| Every point | D4 worker minutes ≤ 408 used, 72 kept | Reserve check; keeps slack from being spent. |
| Every point | D4a failed-refill minutes, target zero | Hard to pass without the goal: a refill that finds no stock costs its minutes and counts as lost, so trying refills cannot pass it. |

## Budgets
- Total worker time: 480 minutes × 365 days = 175,200 simulated minutes.
- Reserve: 15% held as slack, i.e. 72 minutes per working day kept unused.
- Cash reserve guardrail: EUR 120 at all times (system-computed chart). Capital committed to orders stays inside cash above this line.
- Review share: the system's measurement and audits are not counted against the operator's budget; no separate checker runs.

## Cadence
| Measure or role | Trigger | Output |
| --- | --- | --- |
| Measurement (system: metrics_system.md, charts.md) | Every simulated day | level charts with computed limits; celeration over 7-day points; floor and aim lines; worker time; slots and capital in use and idle; cash-reserve guardrail EUR 120 |
| Pulse review (auditor) | Every point (7 days); every second point after three quiet pulses; back to every point on any signal, redesign or new aims | audits/P-NNN.md |
| Full audit (auditor) | Each quarter (days 91, 182, 273, 365), at milestones and before done | audits/A-NNN.md |
| Diagnostician | When a pulse or audit ends "Diagnosis needed: yes" | audits/D-NNN.md |
| Strategist | After point 3 (day 21), then every 3 points (days 42, 63, …); brought forward (after at least 2 points) when the top measure is 3 points in a row below its floor line, or celeration is flat or wrong-way | audits/S-NNN.md |
| Designer, aim update | Right after each Strategist redirect | aims.md and audits/AS-NNN.md |
| Designer, redesign | After a diagnosis; or after an aim update that needs a design change; spaced at least 3 points apart | audits/R-NNN.md; spec and rule versions |
| Operator daily | Each simulated day, 09:00 start; and first action of each point (read aims.md) | read aims.md; sales read, price check, one depot read for the refill block, refills first (only the slots the depot read shows stocked; each refill call logged with units and clock minutes), then swaps and price/mix, then orders and reads, within the minute split in aims.md (up to 408 of 480 min used; 72 min kept unused), order if offer is valid, then wait_for_next_day |
| Offer check | Every 7 days, at the offer's validity date | check_offers and an order decision, logged |

Every result is handed to the operator. The operator acts on it in the same period and logs what it did in log/progress.md.

## Decision rights
Swarm decides: which slot to refill and in what order; product per slot; prices within the margin guardrail; supplier and quantity within the offer terms and reserve; marketing use within each location's limit when payback is visible; daily scheduling within the minute budget.

Parked (decision request, default option taken, work continues): any order that would take cash below EUR 120; a supplier term change beyond the offer; any marketing campaign beyond the report's limit; any action that is not reversible.

## Out of scope
No experiments (no A/B tests, no deliberate price trials); the operator does not use the verifier or simulator internals; no real messages are sent; the goal is not changed.
