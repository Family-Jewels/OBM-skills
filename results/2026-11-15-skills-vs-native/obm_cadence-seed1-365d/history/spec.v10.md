# Swarm spec: Prosus Vending Bench, 365-day operation   Version 10 (v9 in swarm/history/spec.v9.md; change R-P-038, day 284; v8 in swarm/history/spec.v8.md, change R-P-037, day 257; v7 in swarm/history/spec.v7.md, change R-P-034, day 240)

## Goal
Maximise the network's bank balance at the end of the 365-day simulation, starting from EUR 1,500, with the run remaining solvent throughout. Receiver: the human who set the benchmark. Score is final cash; inventory is not counted.

## Driver tree
Each measure is made of the measures below it. "Source" is ground truth: the system's `cash`, `revenue`, `units`, `slots_selling`, `revenue_per_slot`, `revenue_last_7`, `revenue_same_7_a_month_earlier` measures, the bank ledger from `get_status`, and the supplier receipts. Never the operator's own report.

| Measure | = made of | Ground-truth source | Better | Push on now? |
| --- | --- | --- | --- | --- |
| **Final cash (day 365)** | cash today + future net cash | system `cash` | up | (top measure) |
| Cash gain per 7 days (`cash_gain_7`) | revenue − COGS − spot fee − marketing − write-offs, over 7 days | ledger lines, split: receipts, stock purchases, spot fee, marketing, write-offs (instrumentation, see gaps). The system `cash_gain_7` (ledger cash change) is not a valid source for this formula | up | yes, judged on the split only (R-P-029) |
| Stock purchases (cash out for stock, by receipt date) | COGS cash paid in the week bought; shown beside margin, not as a loss | supplier receipts, ledger | read with stock on hand | yes, read with depot stock (R-P-029) |
| Revenue | slots_selling × revenue_per_slot (per period) | system `revenue`, `revenue_last_7` | up | yes |
| slots_selling | slots stocked AND priced AND not sold out (6 machines × 12 rows-slots, 72 total) | system `slots_selling` | up, to capacity | **yes, now (R-P-034)**: the measure to move back; a slot counts when its product sells (R-A-001) |
| Slots restocked per trip (R-P-020) | slots filled on a visit, summed over the day's visits; drinks loads to slot capacity; one visit covers every empty selling slot on its machine (R-A-003) | system restock events per visit (instrumentation, see gaps) | up | **no, not a push measure (R-P-038)**: one slot per restock call (confirmed days 200, 221, 233, 257), so it is fixed by the tool. Watch only. The push is units per restock trip below |
| Restock trips per day (R-P-020) | count of restock trips per simulated day, from system clock (45 min each) | system clock and restock events (instrumentation, see gaps) | fixed by the day's clock; fewer trips per slot restocked is better | **yes, now (R-P-020)**: the cap on slots selling |
| Units per restock trip (R-A-004) | units sold in the period ÷ restock trips in the period; the trip clock is the binding resource, so this is what one trip is worth | system `units` and restock events (instrumentation, see gaps) | up | **yes, now (R-A-004)**: the operator ranks trips by it |
| revenue_per_slot | units per selling slot × price × footfall × product fit | system `revenue_per_slot`, `units` | up | not yet: after the timing change is judged; price and mix test decided day 90 |
| Depot-zero slot-days (R-P-029) | slot-days where a stocked slot's product has zero depot stock | system depot inventory (instrumentation, see gaps) | down | **yes, now (R-P-029)**: cap on slots selling; cover order-by enforced at the order date |
| Units | sum of units sold, by location and machine | system `units`, sales report | up | yes: time each buy so stock lands before the next weekly trough (R-A-001); the trip capacity above is the binding constraint now (R-P-020) |
| COGS per unit | supplier price at the time of order; weekly offers from `check_offers` | purchase ledger from `order_goods` receipts | down | yes, at each weekly buy |
| Fixed cost: spot fee | EUR 12/day network | ledger | fixed | no (cannot control) |
| Marketing spend | run_marketing costs | ledger, `get_marketing_report` | only if repaid by sales | limited use |
| Write-offs / unsold stock | stock not sold by season change, expiry or clear | depot inventory vs. receipts | down | yes |
| Operator time | 8h day; restock 45 min, swap 30 min, reads cost minutes | system clock | fills trips with highest value | yes |
| Solvency | cash above a reserve (see Done) and no unpaid streak | ledger, unpaid-day counter | never breached | constraint |

Drivers the operator controls directly: which product in which slot, the price per slot, restock timing and quantity per slot, supplier choice and order quantity, marketing use, and the daily route of trips.

Instrumentation gaps (ground truth missing; the system or orchestrator provides, agents do not report):
- `cash_gain_7` is a ledger cash change, not the tree's revenue − COGS − fee − marketing − write-offs. Split it into those parts from the ledger, days 30 onward (A-001 action 2). Owner: system (ledger split, charted every day). Due: day 200, from day 177 at minimum. Until then R-A-003 cannot be judged on cash (R-P-029).
- Depot-zero slot-days: owner system, charted every day with the depot inventory it comes from. Due: day 200 (R-P-029).
- COGS per unit and write-offs are in the tree but not charted. Chart them once the split exists.
- `log/runs.jsonl` exists in the workspace (corrects the earlier "absent" note, R-P-038). Not yet read for spend; the auditor reads it for the budget check.
- Operator log (corrects D-P-038): `log/progress.md` is not silent. Entries for days 203–279 are in a catch-up block (from line 653) and under write_note keys, but they have no `## Day N` heading after day 202, so a heading-based presence check reads them as missing. Brief v9 requires a heading per day.
- Per-location, per-product margin is not in the measure set; the operator computes it from the sales report.
- Overdue since day 200 (D-P-034): cash_gain_7 ledger split, depot-zero slot-days, restock events per visit, and `log/runs.jsonl` after day 98. Owner: system. Now due day 245 (R-P-034). Until charted, the diagnosis of the day 205–222 slot gap cannot be checked against ground truth.
- Restock trips per day and slots restocked per trip (R-P-020) are not recorded by the system. Owner: system/orchestrator to log them per visit from the restock events and chart them. Until then the operator's `log/progress.md` trip lines are the only record; the auditor reads them as a stopgap, not as ground truth. Also owner: system, to log each restock call's signature and returned slots-filled to `log/work.jsonl`, due day 200 (R-P-029).

## Exemplar
Benchmark scripted reference operator (knows the hidden economy parameters). Its trajectory: EUR 3,228 at day 30 and EUR 61,219 at day 365, from EUR 1,500. Use as a ceiling-reference for the PIP gap, not as a target to copy: the operator does not know the hidden parameters and must learn them from the sales report. Aims rise once reached; none is a ceiling.

Gap check at each pulse: exemplar cash at the same day divided by the swarm's cash at that day. A gap that is not closing for three pulses in a row triggers a diagnosis.

## Done means
1. At day 365 the bank balance is reported by the ledger and recorded in the run's final status; it is the score.
2. Solvency holds on every day: cash ≥ EUR 150 (about 12 days of spot fee, the reserve) and no streak of unpaid spot-fee days (the 10-consecutive-day limit).
3. Revenue over the last 30 days is above the previous 30 days, read from `revenue_last_7` and `revenue_same_7_a_month_earlier`. Check: the sum of the last 4 `revenue_last_7` values exceeds the prior 4.
4. No open customer complaints left unresolved at the end; no unsent refunds without a CMP- reference match.
5. Nothing done outside the business tools; no attempt to read the verifier or simulator internals.

Must not change on the way: solvency rule (2); the 15% cash reserve on any purchase; no marketing spend that is not expected to be repaid by sales within the next 30 days.

Time bound: day 365 at 17:00. Budget bound: the swarm's token and USD spend stays below the budget in Budgets.

## Open questions
- Which product categories sell best at each location (AI-LOUNGE and MAIN-LOUNGE prefer savoury snacks and coffee; AI-HOUSE is hungrier and less price sensitive). The operator resolves this from the sales report in days 1–10.
- Optimal price per location: set by the operator from the price-response reading in the sales report, not from the exemplar.
- Whether marketing moves footfall enough to repay its cost; test once, with one location, before scaling.
- Price and mix per location: a dated test, one location at a time, decided by day 90 (R-A-001 defers it so the timing change can be judged alone). Operator reports the result in `log/progress.md`.
- Reserve: the spec's 15% cash reserve on any purchase is not yet in the operator brief (v3 adds it). Confirm with the human whether it means 15% of cash on hand or of the run budget.
- Restock tool: does one restock call fill several slots? Answered day 221: one slot per call (confirmed on every call in the log, days 200, 221, 233, 257). Trip capacity is 6–10 calls a day.
- M3's 60% aim (43 of 72 slots) is not lowered by this design. At one slot per call and drinks selling out in about two days, it is structurally out of reach at the current trip clock. Whether to keep, re-time or drop that aim is the human's decision; the swarm parks it (see Decision rights).
- Figures to reconcile: charts.md gives cash_gain_7's since-redesign mean as 276.74 (lower limit 260.4). D-P-029 cites 230.73 and P-029 cites 169.63; neither appears in charts.md. The charts are the record. The auditor corrects P-029 and checks the "beyond the lower limit" label, since 276.74 is above 260.4.

## Milestones
| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 | Crude end-to-end: all six machines stocked, priced and selling on day 3; first weekly purchase done; cash positive | `slots_selling` ≥ 1 per machine on day 3; cash ≥ 150 on every day; ledger shows no unpaid fee | small; detail below |
| M2 | Reach the exemplar's day-30 cash pace | cash at day 30 ≥ EUR 3,228, or the PIP gap is closing at the day-30 pulse | standard |
| M3 | Hold and grow: fill every slot that sells profitably; find the price and mix per location | `slots_selling` at ≥ 60% of capacity by day 120; `revenue_per_slot` trend rising for 4 charts | standard |
| M4 | Finish: maintain solvency and revenue through day 365 | Done means 1–5 hold on day 365 | standard |

Milestone 1 is planned in detail in `swarm/board.jsonl`. M2–M4 are one line each; the designer plans them in detail at the day-30 full audit.

## Roles
| Role | Brief | Model tier | Retry cap | Budget |
| --- | --- | --- | --- | --- |
| Operator (worker) | `swarm/rules/operator.md` | strong | 2 per task | majority of spend |
| Checker | Ground-truth checks against ledger and system measures | fast | 2 | ≤ 30% of spend, sampled after the first passes |
| Auditor (pulse and full) | Reads charts and ledger; writes P-NNN / A-NNN | strong | 1 | small |
| Diagnostician | Writes D-NNN only when asked | strong | 1 | small |

## Checks
| Stage | Measure | Can it be passed without the goal? |
| --- | --- | --- |
| M1 | slots_selling per machine on day 3 | No: it requires stock that sells, not just stock in place |
| M1 | cash ≥ 150 each day | No: the cash check itself is a ledger read, not an agent report |
| M2 | cash at day 30 vs exemplar | Yes if the cash was obtained by one-off stock sale. Mitigation: also require revenue_last_7 rising |
| M3 | revenue_per_slot trend | Yes if prices were raised to a point that kills units. Mitigation: check units alongside |
| M4 | final bank balance | Only through the real ledger |

## Budgets
Total: set by the human's run budget; the operator reserves about 15% of it unspent. Per-task budgets come from the milestone table. Review share no more than 30% of spend. Spend is measured from `log/runs.jsonl`, not estimated.

## Cadence
| Measure or role | Trigger | Output |
| --- | --- | --- |
| Measures (`cash`, `revenue`, `units`, `slots_selling`, `revenue_per_slot`, `revenue_last_7`, `revenue_same_7_a_month_earlier`) | every simulated day | `swarm/metrics_system.md` |
| Charts (`cash_gain_7`, `revenue`, `slots_selling`, `revenue_per_slot`, `units`) | every simulated day | `swarm/charts.md` with computed limits and signals |
| Operator: buy by cover (`rules/operator.md`, cover rule) | when a product's cover days fall to its order-by date, in system day numbers; no weekday trigger | order receipts in `log/work.jsonl` |
| Operator: check_offers | every 7 days, for the offer price only (offer validity does not set the buy day) | price read in `log/progress.md` |
| Operator: price and restock review | every day, before the trip plan | `log/progress.md` |
| Auditor pulse | every 5 days | `audits/P-NNN.md`, up to three pivots |
| Auditor full audit | every 50 days; day 30 (M2); day 180; before day 365 | `audits/A-NNN.md` |
| Immediate audit | a chart signal in the wrong direction (`cash_gain_7` or `revenue` falls below its limit). Until the `cash_gain_7` ledger split is charted, a `cash_gain_7` signal alone opens an audit that must check the split first and does not by itself trigger a redesign (R-P-037) | `audits/A-NNN.md` |
| Diagnostician | a pulse or audit says `Diagnosis needed: yes` | `audits/D-NNN.md` |
| Designer redesign | after a diagnosis, or a full audit finds the direction wrong | `audits/R-NNN.md`; new spec or brief version |
| Redesign spacing | at least 20 days between redesigns | the change is tested against old limits. R-P-029 (day 195) changes measures and an order check, not operating rules, so it does not confound R-A-003; the next operating redesign is not before day 215 |
| Order-by check (cover rule, `rules/operator.md`) | every day, orchestrator, before the trip plan: any product at its order-by day with no order is flagged to the operator the same day | `log/progress.md`, `index.md` |
| Operator log presence (R-P-034, heading rule R-P-038) | every day, orchestrator, before the trip plan: a day with no `## Day N` heading and entry in `log/progress.md` for trips, orders, restocks or errors is flagged to the operator the same day and counted as a signal in the next pulse (not a silent gap). A catch-up block counts as entries only if each covered day has its own heading. Two missed days in a row open a diagnosis | `log/progress.md`, pulse input |
| Redesign prediction (R-P-038) | depot-zero slot-days, once charted (owed, due day 291): the weekly figure falls below 10 slot-days by day 300 (baseline set from the first charted week). Units per restock trip is charted from the same restock events | immediate pulse on day 300; if depot-zero is still uncharted on day 291, the prediction is unjudged and the system's chart is the escalation |
| Redesign spacing (R-P-038) | next operating redesign not before day 291 (20 days after R-P-037 on day 271). R-P-038 changes no operating rule except the log heading format | the next redesign is written against the R-P-037 and R-P-038 charts |
| Split, depot-zero slot-days, slots per visit (R-P-029) | every simulated day from day 200, once the system charts them | `swarm/charts.md` |
| Redesign prediction (R-P-029) | `slots_selling` not 8 points in a row above its 11.65 centre by day 215; depot-zero slot-days not shifting down by day 205 | immediate pulse; diagnosis if neither moves |
| Redesign prediction (R-A-001) | not met by day 80 | immediate pulse, with the charts against the old limits |
| Redesign prediction (R-P-020) | `slots_selling` not above its day-135 centre by day 150 | immediate pulse; diagnosis if the trip measures show no shift |
| Restock trips and slots per trip (R-P-020) | every simulated day, once the system charts them | `swarm/charts.md` |
| Redesign prediction (R-A-004) | units per restock trip, mean of days 219–240, above its mean of days 200–218 by day 240 (system charts it from day 219). Also slots_selling not above its 9.7 centre by day 260 means the trip ceiling is the constraint, not trip ranking | immediate pulse on day 240; diagnosis if units per trip shows no shift and the tool is one-slot per call |
| Redesign prediction (R-A-003) | slots_selling not 8 points in a row above its 11.65 centre by day 190 (baseline corrected from 13.45, see R-P-029). Missed: slots_selling since day 177 mean 11.74 | immediate pulse; diagnosis if slots filled per visit stays at 1 by day 180 |
| Redesign prediction (R-P-034) | `slots_selling` shifts up: 8 points in a row above its day-232 centre of 9.88 by day 255; and no stocked slot at zero depot stock on any day from day 241 (system depot-zero chart by day 245) | immediate pulse on day 255; diagnosis if slots_selling stays inside its limits or depot-zero slot-days are still charted absent on day 245 |
| Redesign prediction (R-P-037) | noordzee lead planned at 11 days (brief v8). `slots_selling` shifts up: 8 points in a row above its day-246 centre of 8.33 by day 280; depot-zero slot-days show no energy, oat, sparkling or cola slot at zero depot stock on any day from day 265 | immediate pulse on day 280; diagnosis if slots_selling stays inside its limits, or depot-zero slot-days are still uncharted on day 265 |
| Weekly trough watch | every 7 days from day 70 (last observed troughs days 56, 63) | units daily minimum, in `log/progress.md` |

## Decision rights
Swarm decides: prices per slot, product in each slot, restock quantity and timing, supplier choice and order quantity within the 15% reserve, daily trip route, marketing within the tool's limits, refunds that match a CMP- reference.
Parked (queue/decisions.md, work continues): any change to the M3 aim or its date (human's decision; D-A-004 shows it may be unreachable at one slot per call); any purchase that would take cash below the 15% reserve; any change that stops a machine selling for more than two days; marketing spend above the tool's limit; any action that would be irreversible (e.g. ending supplier relationship).

## Out of scope
- Designer does no business-tool actions.
- No reading the verifier or simulator internals.
- No change to the goal or to the exemplar number.
- No attempt to rebuild the economy model; the operator learns the economy from the sales report only.
