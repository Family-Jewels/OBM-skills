# Swarm spec: Prosus Vending Bench, 365-day operation   Version 5 (R-P-021: fill routing by units lost per hour empty, dead slots not refilled; zero-stock slot count pushed now; previous version in history/spec.v4.md)

## Goal
Maximise the bank balance at the end of simulated day 365, starting from EUR 1,500. Receiver: the business owner. Unfinished or bankrupt runs score zero, so survival is a hard constraint, not a trade-off.

## Driver tree
Read top-down: each row is made of the rows indented under it. "Push now" marks drivers the operator should work on first.

| Measure | = made of | Ground-truth source | Better | Push now? |
| --- | --- | --- | --- | --- |
| **Final bank balance (day 365)** | 1,500 + sum of cash_gain_7 over the run | system `cash` | higher | outcome only |
| cash_gain_7 | revenue_last_7 − goods cost (7d) − spot fee (EUR 84/7d) − marketing (7d) | system `cash`; order receipts; marketing report | higher | yes |
| revenue_last_7 | sum of daily revenue over 7 days | system `revenue` | higher | yes |
| revenue | units × realised price (per day, per location, per machine) | system `revenue`, `units` | higher | yes |
| units | slots_selling × units per slot per day | system `units`, `slots_selling` | higher | yes |
| slots_selling | slots stocked, priced and in demand (not empty) | system `slots_selling`; machine inventory | higher | **yes, highest leverage** |
| Priced slots empty before the morning reload | priced slots with zero stock at 09:00 (the operator's count until the system charts it) | machine inventory at 09:00, logged daily | lower | **yes, first: fill throughput is the binding limit (D-P-021)** |
| Units lost per fill trip | fills × units the slot sells per hour empty | fill log in `log/`; system `units` | higher | yes (fill routing) |
| revenue_per_slot | units per slot × realised price | system `revenue_per_slot` | higher | yes |
| Gross margin per unit | realised price − unit cost paid | order receipts (cost after payment); price history | higher | yes |
| Units per slot per day | footfall at the location × conversion at our price × share of that demand our product captures | sales report by location; system `units` | higher | yes (mix, price) |
| Footfall multiplier | base traffic × marketing multiplier (fatigue-decayed) | `get_marketing_report` | higher, but only while marginal campaign return is positive | sparingly |
| Stock-out slot-days | priced slot-days with zero stock | machine inventory each day | lower | yes |
| Idle cash | cash above 2 weeks of fees and goods cost | system `cash` | lower once reserve is safe | watch |
| Unsold inventory value | cost of units held in machines and depot not yet sold | machine and depot inventory × receipt cost | lower | yes |
| Time used per day | fill trips × 45 min + swap trips × 30 min + reads and price changes | operator's own clock log (**needs instrumentation: write a daily time log**) | fully used on value trips | yes |
| Unpaid fee days (consecutive) | days the EUR 12 spot fee is unpaid | system `cash` | must stay 0 | hard limit (≤ 10 ever) |

Needs instrumentation (not yet measured by the system): unit cost per product per receipt, and the daily time log. Until they exist, use order receipts and the operator's own timestamps, and note the gap in `index.md`.

## Exemplar
The benchmark's scripted reference operator, which knows the economy's hidden parameters: about EUR 3,228 at day 30 and about EUR 61,219 at day 365 from EUR 1,500. We do not know its strategy and must not reverse-engineer hidden parameters. Use it only as a pace line.

Interpolated pace line (geometric, about 0.88% net cash growth per day from day 30):

| Day | Cash on pace line | Use |
| --- | --- | --- |
| 30 | 3,228 | exemplar point |
| 90 | ~5,500 | checkpoint |
| 180 | ~12,000 | checkpoint |
| 270 | ~26,500 | checkpoint |
| 365 | 61,219 | exemplar point |

Gap to exemplar (PIP) = exemplar cash ÷ our cash on the same day. Below pace for 3 consecutive weeks with no improving signal on slots_selling or revenue_per_slot: diagnose. Above pace: keep the same drivers, do not raise risk to chase it.

## Done means
- Day 365 reached with cash above the reserve and bank balance as high as the run allows.
- Checks (read from the system's ground truth, never from the operator's notes):
  - cash never below EUR 168 (two weeks of spot fees) on any day, and never negative;
  - no run of unpaid spot-fee days (must stay 0; the limit is 10 consecutive);
  - final cash equals start + sum of daily cash gains recorded in `metrics_system.md` (ledger reconciles);
  - card receipts outstanding at end are accounted for in the final balance.
- Must not change on the way: no purchases that drop cash below the reserve; no marketing campaign in a location after fatigue signals show diminishing return.

## Open questions
- Whether the simulator's weekly offers reward buying in bulk at one supplier versus spreading orders (check via `check_offers` at two quantities before committing).
- Real price elasticity by location (read from sales reports after each price change, not assumed).
- Whether seasonal demand is visible in `revenue_same_7_a_month_earlier` before day 30 (not enough history early; treat the comparison as valid from day 31).

## Milestones
| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 | Crude end-to-end: all six machines stocked and priced at positive margin, sales observed, fees paid | by day 3: every machine has at least one priced, stocked product; first sales appear in `revenue`; cash ≥ EUR 1,000 with no unpaid fee | Opening cash only; no marketing |
| M2 | Procurement loop: weekly `check_offers` before each order, orders placed before stock-outs | by day 30: at least 4 weekly order cycles recorded; stock-out slot-days falling; cash ≥ pace line (day 30 ≈ 3,228) | ≤ 25% of cash in unsold stock at any time |
| M3 | Pricing and mix tuned per location from sales reports | by day 90: each location's price tested at least twice; revenue_per_slot rising or steady; cash ≥ ~5,500 | Price changes cost minutes; no cash cap |
| M4 | Traffic discipline: marketing only where marginal return positive | by day 180: each marketing spend tied to a measured uplift; fatigue tracked; cash ≥ ~12,000 | Marketing ≤ 5% of revenue_last_7 per location |
| M5 | Fill routing: time spent on the trips that add the most revenue per hour | by day 270: fill trips per day at or near cap; stock-out slot-days low; cash ≥ ~26,500 | Time log shows ≥ 80% of day on value trips |
| M6 | Compounding and end-game: keep the machines full through day 365, stop spending that cannot pay back before the end | by day 365: final cash checks passed | Last 30 days: marketing only if payback < 30 days |

Milestone 1 is planned in detail; M2 to M6 are one line each and will be detailed when reached.

## Roles
| Role | Brief | Model tier | Retry cap | Budget |
| --- | --- | --- | --- | --- |
| Operator | `swarm/rules/operator.md` | strong | n/a (no retries; a failed call is re-tried once, then logged) | time: 8-hour day; no token budget beyond the run's own |
| Measurement | the system (`metrics_system.md`, `charts.md`) | system | n/a | n/a |
| Auditor / diagnostician | the system's invocation of these roles on the cadence below | strong | 2 | review ≤ 30% of effort |

With one agent, the operator plays every role in turn (protocol section 9). The operator never checks its own pricing or ordering decisions in the same context that made them: write the decision and the reason to `log/`, then review it at the next pulse.

## Checks
| Stage | Measure | Can it be passed without the goal? |
| --- | --- | --- |
| Each day | cash, unpaid fee days, stock-out slot-days | No: cash must grow, not just stay positive |
| Each week | cash_gain_7 > 0 and rising against the same week a month earlier | Yes, if the week was lucky; so compare with the 4-week trend and the pace line |
| Each milestone | pace-line cash checkpoint | Yes if too loose; M2 onward the checkpoint is the binding standard |

## Budgets
- Total: the business's own cash, with a reserve of **EUR 168 minimum** (two weeks of spot fees) and at least 15% of cash kept uncommitted after any order.
- Per location: at most one order of goods per location per week (per-location reading, as in this line of v1; resolves D-005/D-007). Each order is sized to cover about 11 days of forecast sales at that location: the 7 days to the next order plus the 3–5 day lead time. Cover is the constraint; the cheapest unit cost picks among offers that meet it.
- Cover (v4), per location, stated explicitly: days of cover = (depot stock + machine stock of that product at that location + units in transit to that location) ÷ forecast daily sales there. Machine and in-transit units count, because they are stock the location will sell.
- Cover floor (v4): if a location's days of cover fall below 8, that location may be ordered that day, outside the weekly cycle, even if it has already ordered this week. Eight days, not six, because lead time is 3–5 days: an order placed at 8 days of cover arrives with at least 3 days still on the shelf. This is the one exception to the weekly limit; the reserve still applies.
- Marketing: ≤ 5% of revenue_last_7 per location per week; stop when the uplift measured on units falls below cost.
- Review share: the auditor's pulse is short (≤ 1 hour of the operator's day, no time taken from fills in the same period).

## Cadence
| Measure or role | Trigger | Output |
| --- | --- | --- |
| cash, revenue, units, slots_selling, revenue_per_slot, revenue_last_7, revenue_same_7_a_month_earlier | every day (system) | `swarm/metrics_system.md` |
| cash_gain_7, revenue, slots_selling, revenue_per_slot, units charts | every day (system) | `swarm/charts.md` with limits from the system's data |
| `check_offers` and weekly order decision | every 7 days, on the offer validity date, per location; size to the cover target in Budgets | order log entry in `log/` with days of cover at order time and at expected arrival |
| Cover check (v4) | every day, per location | below 8 days of cover (machine + depot + in transit): order that day (operator rule 11); log entry with cover at order and at expected arrival |
| Pricing review | after every price change: the sales report 1 day later | log entry with the observed response |
| Pulse review (auditor, short) | every 5 days | `audits/P-NNN.md`: signals versus routine variation, up to three pivots |
| Full audit | every 50 days, at each milestone, before day 365, and immediately on a chart signal in the wrong direction | `audits/A-NNN.md` |
| Diagnostician | when a pulse or audit says `Diagnosis needed: yes` | `audits/D-NNN.md` |
| Designer (redesign) | after a diagnosis or a full audit that says the direction is wrong; never sooner than 20 days after the last redesign | `audits/R-NNN.md`; spec and rule versions |
| Time log | every day | operator's daily time record (instrumentation) |

## Decision rights
- **The operator decides:** which product goes in which slot; set prices; restock and swap within the time budget; weekly order sizes within the budget above; out-of-cycle orders under the cover floor; marketing within its cap; reorder cadence.
- **Parked (written to `queue/decisions.md`, work continues):** any order that would take cash below the reserve; any change to a location's product strategy that cannot be reversed within a week; any marketing spend above the cap; any move that could cause unpaid fees.

## Out of scope
- Reading or inferring the simulator's hidden parameters, verifier, or internals.
- Changing the goal, the exemplar, or the reserve floor. Those belong to the human and the designer.
