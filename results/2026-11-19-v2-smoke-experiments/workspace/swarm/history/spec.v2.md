# Swarm spec: Prosus Vending Bench   Version 2 (R-O-001, day 32; v1 in history/spec.v1.md)
## Goal
Maximise the bank balance at the end of 91 simulated days, starting from EUR 1,500, by running three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with one SNACK and one DRINKS machine (72 slots in total). Receiver: the operator's bank account. Inventory is not money; unsold stock at the end is worth nothing to the score.

Time base: one point = one simulated day for level charts and the daily snapshot. Celeration, pulse reviews and floor/aim use **7-day points** (13 points across 91 days, which satisfies the 12-point minimum and holds whole weekly demand cycles).

## Driver tree

Identity: final cash = start cash + revenue − unit costs paid − spot fees (EUR 12/day, EUR 1,092 over 91 days) − marketing spend ± card settlement timing.

| Measure | = made of | Ground-truth source | Better | Ceiling (source, confidence) | Guardrail | Push on now? |
| --- | --- | --- | --- | --- | --- | --- |
| **Final cash (day 91)** | revenue − unit costs − fixed fees − marketing + settled card receipts | bank ledger via `cash` daily measure; card settlement at end | up | EUR 61,219 at day 365, benchmark reference operator (exemplar, confidence low: the 91-day horizon is shorter than its reference point, and the exemplar knows hidden parameters). Day-30 exemplar EUR 3,228 is the usable checkpoint (confidence medium). | cash ≥ EUR 120 every day (see reserve) | yes, top measure |
| Revenue | slots_selling × revenue_per_slot, summed daily | `revenue`, daily ledger | up | Resource ceiling: all 72 slots selling at the best revenue_per_slot observed (confidence medium) | — | yes |
| slots_selling (capacity in use) | slots stocked AND priced AND with stock, count of 72 | daily slot snapshot | up while margin positive | 72 (hard resource); demand, not slots, is usually binding (confidence medium) | do not stock a slot whose unit margin is ≤ 0 | yes, after M1 |
| revenue_per_slot | units per slot per day × average price | `revenue_per_slot` daily | up | own best stretch; reference-class guess until M1 probe is read (confidence low) | price must keep unit margin > 0 | yes |
| Units per slot-day (demand) | footfall × location preference match × price response × traffic multiplier | `units`, per-machine `machine_units` | up | Exemplar-implied; unknown (confidence low; a test, not a gap) | no unit sold below cost | partly, via mix and placement |
| Average price | set_price per product, within the price response curve | sales report price response; `revenue`/`units` | up to the elastic optimum | own best stretch (confidence low until E-001) | unit margin ≥ 0; no price that cuts units by more than the revenue gain | yes, tested by E-001 |
| Unit margin | price − unit_cost_paid_30d | `unit_cost_paid_30d` and price ledger | up | none fixed; compare against best supplier offer per product | margin ≥ 0 per product | yes |
| unit_cost_paid_30d | weighted supplier unit prices bought over 30 days | order receipts (actual cost after payment) | down | lowest current offer across ≥2 suppliers at the planned quantity (confidence medium) | do not buy quantities that sit unsold beyond the horizon | yes |
| Marketing traffic | campaign timing × limits × fatigue | `get_marketing_report` traffic multipliers | up when it pays back | earned-back test in E-002 (confidence low) | spend per campaign ≤ limit; no repetition inside fatigue window | only via E-002 |
| Fixed costs | spot fee, EUR 12/day | ledger | down (not controllable) | — | never leave a day unpaid (10 consecutive unpaid days ends the business) | monitor |
| Time (minutes/day) | fills 45 min, swaps 30 min, reads and price changes minutes; 480 min/day | action log (work.jsonl) | spent on the highest-return action | 480 min/day (hard) | do not spend time that leaves a slot empty with positive margin | yes |

Measures the system must instrument (not yet recorded by an agent; the system computes them): `machine_revenue`, `machine_units`, `machine_stocked_slots` per machine (six machines), daily slot snapshots, `revenue_last_7`, `revenue_same_7_a_month_earlier` (available from day 30), `unit_cost_paid_30d`.

## Exemplar
Benchmark scripted reference operator (knows the economy's hidden parameters): EUR 3,228 at day 30 and EUR 61,219 at day 365, from EUR 1,500. Source: task briefing. Use the day-30 point as the usable checkpoint on the floor line (projected to day 91 by the system's celeration fit); treat the day-365 figure as a ceiling reference, not a day-91 target. The swarm's own best celeration is the improvement exemplar once measured.

Floor and aim for the top measure (final cash, computed by the system on 7-day points): the floor runs from the cash level after 3 points to the day-30 exemplar (EUR 3,228) and on to the day-91 goal; 3 points in a row below it call for an opportunity review. The aim is a deliberate overshoot beyond the exemplar's path (the system sets it from the remaining horizon, not from a cap), so the swarm is never capped by the floor; it is raised whenever it is met on 2 of the last 3 points.

## Resources
| Resource | How its use is measured |
| --- | --- |
| Cash | daily `cash`; capital in use = cash committed to stock on hand plus depot stock value; idle = cash above EUR 120 reserve that earns nothing |
| Slots (72) | `slots_selling`; idle = empty, unpriced or zero-margin slots |
| Machine time (480 min/day) | minutes logged per action in work.jsonl; idle minutes at end of day |
| Depot stock | unit count and value by product from inventory; stock unsold at day 84 is a finding |
| Marketing budget and limits | `get_marketing_report` limits and spend per location |
| Supplier offers (weekly validity) | offer validity date recorded before each order |
| Operator run tokens/spend | runs.jsonl, per period |

## Experiments
Budget share: about 10% of daily machine time (≈48 min/day) and no more than EUR 60 of marketing spend in total across the run. Rules: each experiment is reversible, stays inside the guardrails, states a prediction, lasts at least 3 points (21 days here, or 14 days at minimum per the 2-point rule below — use 14 days: two weekly points), and its driver is a measure the system records. Each lasts at least 3 points after its fidelity check passes (3 points = 21 days). Slices must not overlap; a whole-system experiment is not allowed. The system measures; the auditor rules keep, revert or too small to read.

| ID | Driver (recorded measure) | Slice | Change | Prediction | Guardrail | Start | End |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E-001 | machine_revenue on AI-HOUSE:SNACK | AI-HOUSE:SNACK, judged against its own earlier line | raise prices on the top-selling product by 10%, hold for 21 days | machine_revenue shifts up by ≥5% against its own 7-day line, with machine_units falling by no more than the revenue gain | unit margin ≥ 0; machine_units not below 60% of the prior 7-day line; cash ≥ 120 | day 7 (after the M1 baseline week) | day 28 |
| E-002 | machine_units on MAIN-LOUNGE:SNACK and MAIN-LOUNGE:DRINKS | MAIN-LOUNGE (both machines), against their own earlier line | one print campaign in week 2 (day 14), no further campaigns at MAIN-LOUNGE for 21 days | machine_units rises ≥10% over the 7 days after the print, and the uplift covers the campaign cost within the window | spend ≤ get_marketing_report limit; no second campaign inside the fatigue window; cash ≥ 120 | day 14 | day 35 |
| E-003 | slots_selling | AI-HOUSE:DRINKS and AI-HOUSE:SNACK (both machines), against their own earlier count | load all depot stock with unit margin > 0 into empty AI-HOUSE slots within 24 hours of landing, for 21 days (fill-within-24h test) | slots_selling on the AI-HOUSE slice rises from 0 to ≥6 by day 40 (7 days after start), with its machine_revenue at least 50% above its prior 7-day line | unit margin ≥ 0; no stock unsold past day 84; cash ≥ 120; no stock bought for this slice beyond the depot | day 33 (after fidelity passes) | day 54 |

Queued after E-003 (not before its ruling): E-001 re-run on AI-HOUSE:SNACK once that slot is stocked, price 1.50 → 1.65 for 21 days, driver machine_revenue. It may not overlap E-003's slice while E-003 runs.

Queued (not started): a price test on AI-LOUNGE (price-sensitive picky customers) after E-001 ends, and a product-mix test on AI-HOUSE for hungry customers. Both only after the first two rulings, and no earlier than day 35 so that the last ruling lands before a new one begins.

## Done means
- The run ends at day 91 with the business open: no unpaid spot fee in any run of more than 10 days, and the final day's card receipts settled.
- Final cash (after settlement of outstanding card receipts) exceeds the day-0 cash of EUR 1,500, and exceeds the prior best run's value if one exists in the record.
- Cash never fell below EUR 120 on any day of the run (reserve guardrail).
- Unsold depot stock at day 84 is valued at no more than EUR 150, so that the last weeks are not spent buying stock that cannot be sold before the end.
- Every decision that changed prices, marketing or stock is in log/progress.md with the day and the measure that prompted it.
- Checks are read from the system's ledger and snapshots, not from the operator's own report.

## Open questions
1. The exemplar's day-365 figure is beyond this 91-day horizon. No day-91 exemplar is given; the floor line uses the day-30 checkpoint. Confirm with the human whether a day-91 benchmark exists.
2. Slot layout is assumed to be 12 slots per machine (72/6, rows A–D). Confirm from `get_machine_inventory` on day 0.
3. Card takings settle one day later and outstanding card receipts settle at the end; the reserve guardrail uses cash on hand, so the last two days' card balance needs a separate read.
4. The price response curve and demand per location are unknown. M1's price probe (T-0004) resolves the most important one.
5. Whether the system's per-machine measures distinguish SNACK and DRINKS demand exactly (duplicate slots share demand), so that slot count changes do not look like demand changes.
6. Marketing limits and fatigue windows are only known from get_marketing_report; E-002 assumes the window is at least 14 days.

## Milestones
| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 | Crude end-to-end loop: all six machines stocked, priced and selling; daily ledger and reserve held; price probe read | By day 3, every machine has ≥1 slot stocked and priced; cash ≥ EUR 120 each day; no unpaid spot fee; probe result logged by day 8 | ≈ 15% of run budget |
| M2 | Full selling capacity with positive unit margin; supplier comparison in place | slots_selling ≥ 36 of 72 by day 21 (demand-limited; more is not automatically better); every selling product has unit margin > 0 | ≈ 25% |
| M3 | E-001 and E-002 run to rulings and the rulings applied | both verdicts in audits/ by day 35; kept changes folded into a redesign at least 3 points after the last adopted change | ≈ 20% |
| M4 | Hold and harvest through day 91 | floor and aim checks passed or explained; end-of-run stock and settlement done per Done means | ≈ 40% |

Milestone 1 is planned in detail (board.jsonl). Milestones 2–4 are one line each and will be planned by the designer at the day-14 redesign if needed.

## Roles
| Role | Brief | Model tier | Retry cap | Budget |
| --- | --- | --- | --- | --- |
| Operator (orchestrator and worker in single-agent mode, section 9) | rules/operator.md | strong | 2 per task | ≈ 70% of run budget |
| Checker (experiment fidelity, submission checks) | system-called; obm-swarm-checker | strong | — | ≤ 10% |
| Auditor (pulse, full audit, verdict) | system-called; obm-swarm-auditor | strong | — | ≤ 10% |
| Diagnostician | system-called; obm-swarm-diagnostician | strong | — | ≤ 5% |
| Designer (redesigns only) | this spec | strong | — | reserve |

## Budgets
Total: the run's stated token and USD budget, with about 15% held in reserve. Review share (checks, audits, diagnoses) no more than about 30% of spend, sampled after 5 clean first-pass submissions. Per-period spend recorded in log/runs.jsonl; if spend exceeds 85% of the per-period plan, the operator switches to the minimum daily loop (read status, collect, price, restock only if slot margin > 0).

## Cadence
| Measure or role | Trigger | Output |
| --- | --- | --- |
| Measurement (system) | Every simulated day | metrics_system.md, charts.md (cash, revenue, units, slots_selling, revenue_per_slot, revenue_last_7, revenue_same_7_a_month_earlier, unit_cost_paid_30d; six per-machine measures; daily slot snapshots; reserve guardrail EUR 120) |
| Operator daily loop | Every simulated day, at 09:00 and before wait_for_next_day | log/progress.md entry; log/runs.jsonl spend; action list |
| Checker, submission | Each submission (first, after a fail, milestone and final products); then sampled | reviews/ records |
| Checker, experiment fidelity | When an experiment's Applied is written, and again after a failed check | audits/F-E-NNN-n.md |
| Auditor, experiment verdict | When an experiment's clock ends | audits/V-E-NNN.md |
| Auditor, pulse | Every 7-day point (days 7, 14, … 91); every second point after three quiet pulses; back to every point on any signal, redesign or experiment end | audits/P-NNN.md |
| Auditor, full audit | At each quarter of the horizon (days 23, 46, 68, 91), at milestones (M1–M4) and before done | audits/A-NNN.md |
| Diagnostician, fault | When a pulse or audit ends `Diagnosis needed: yes` | audits/D-NNN.md |
| Diagnostician, opportunity | Every 3 points (21 days) without one; or when the top measure is 3 points in a row below its floor line or has flat or wrong-way celeration; never while an experiment runs | audits/O-NNN.md |
| Designer, redesign | After a diagnosis or opportunity review; spaced ≥ 3 points after the last adopted change | audits/R-NNN.md, spec and rule versions |

Reviews give about one keep-doing item and up to four fixes, with at least one keep-doing.

## Decision rights
Swarm (operator) decides: pricing within the guardrails; which slots to stock and what product; order quantity and supplier choice within the cash reserve; routing and timing of fills, swaps and collections; marketing within the limit and fatigue rules; running an experiment already written by the designer.

Parked (decision request in queue/decisions.md, default applied, work continues): any change to the spec's guardrails or reserve; any action that cannot be reversed (clearing a machine's slots with stock on it at a cost, a supplier commitment beyond the next weekly offer); any price below unit cost; any marketing campaign outside the limit; ending the business early.

## Out of scope
Any change to the goal, to the exemplar, or to the reserve figure. Accessing the simulator internals or the verifier. Reporting of measures by the operator itself: measures come from the system's ledger and snapshots only.
