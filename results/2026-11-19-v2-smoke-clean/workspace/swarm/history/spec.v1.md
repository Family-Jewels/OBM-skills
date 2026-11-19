# Swarm spec: Prosus Vending Bench, 91-day operation   Version 1

## Goal
Maximise the bank balance at the end of 91 simulated days, starting from EUR 1,500, across three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with one SNACK and one DRINKS machine (72 slots). Receiver: the human operator who reads the final balance. Inventory is not in the score.

## Driver tree

Top measure: **final bank balance** = cash at day 91 + card receipts settled at the end.
Identity: final balance = 1,500 + Σ revenue − Σ unit cost paid − Σ spot fees (EUR 12/day, fixed) − Σ marketing − Σ refunds.

| Measure | = made of | Ground-truth source | Better | Ceiling (source, confidence) | Guardrail | Push on now? |
| --- | --- | --- | --- | --- | --- | --- |
| Final balance (top) | cash + settled card receipts, day 91 | bank ledger via get_status; system daily `cash` | up | ~EUR 5,500 at day 91 (exemplar: 3,228 at d30, 61,219 at d365, log-linear interpolation; low-to-medium confidence) | cash >= EUR 120 every day (see reserve) | yes, all drivers below |
| Revenue (daily) | slots_selling × revenue_per_slot | system `revenue`, `slots_selling`, `revenue_per_slot` | up | none fixed | none | via the two drivers below |
| slots_selling | slots with stock and a price, of 72 | system snapshot, per slot | up toward 72 | 72 (machine count; high) | depot stock sitting idle while a slot is empty | yes, step 1 |
| revenue_per_slot | units per selling slot × average price | sales report + system | up | own best, set by day 21 (medium) | price >= 1.3 × unit cost paid | yes |
| Units per location | traffic × conversion × price response | sales report; system `units`, `machine_units` | up | location's own best (low) | none | via price, mix, marketing |
| Price per SKU | set_price choice | ledger of set_price calls and sales | learned elasticity | none | price >= 1.3 × unit cost paid; change <= 15% per week per SKU | yes (test first, T-004) |
| Product mix per slot | swap_item choice | machine inventory | more units per slot | none | keep >= 2 SKUs per machine | yes |
| Marketing traffic multiplier | run_marketing campaigns | get_marketing_report (multiplier, fatigue, cost) | up | fatigue limit in report (high) | spend <= 10% of location's last-7-day revenue; no fatigue breach | test in E-002 only |
| Cost: unit_cost_paid_30d | cost paid ÷ units bought, trailing 30 days | order receipts; system `unit_cost_paid_30d` | down | lowest offer at equal quantity seen in trailing 30 days (own best; medium) | never buy a SKU whose unit cost > 0.75 × its planned price | yes, via check_offers and supplier mix |
| Operator time used | Σ minutes of restock (45), swap (30), other calls | run log `log/work.jsonl` | use up to 408 of 480 min/day | 480 min/day (high) | keep 72 min/day unused as reserve | yes, sequencing |
| Sell-through (30-day) | units sold ÷ units stocked | ledger | up | none (low) | depot stock unsold after 14 days → markdown | yes, endgame |
| Fixed cost: spot fee | EUR 12/day | bank ledger | — | fixed | fees unpaid > 3 consecutive days → pause all spend | monitored only |

**Direction (set by the designer):** push first on slots_selling (step 1: every slot stocked and priced with a product that sells), then price and mix (cheap, fast, learnable within a week), then unit cost and sequencing of trips, then marketing as a tested lever. Why: idle slots are the largest measurable gap; price response is the highest-stakes link with the least confidence, so it is tested in milestone 1.

**Measures to record (system adapter request):** the eight daily measures (cash, revenue, units, slots_selling, revenue_per_slot, revenue_last_7, revenue_same_7_a_month_earlier, unit_cost_paid_30d) plus per-machine machine_revenue, machine_units, machine_stocked_slots for the six machines, daily snapshot of all 72 slots (product, price, stock, sales that day), capital in use (stock value at cost on machines and in depot) and idle (depot stock not in a slot; cash above EUR 500). Not yet recorded and needing instrumentation: sell-through and days-unsold per SKU (from order ledger and sales), fee-paid streak, open complaint count, marketing fatigue (from get_marketing_report). Each is read from ground truth, never from an agent.

## Exemplar
Scripted reference operator (benchmark), which knows the economy's hidden parameters: EUR 3,228 at day 30 and EUR 61,219 at day 365, from EUR 1,500. Source: benchmark statement given in the task. The day-91 value is not given; the designer's goal line is a log-linear interpolation, ~EUR 5,500 at day 91. Low-to-medium confidence. Treat it as a reference pace, not a guaranteed ceiling. Own best: set by the system once 3 points exist.

**Goal line and aim (the system computes the lines from the adapter):** Floor line runs from the top measure's level at point 3 to the goal at day 91. Goal G = EUR 5,500 at day 91. Aim = a deliberate overshoot: G reached at half the remaining horizon after point 3 (~day 56), so the aim sits above the exemplar's pace and never caps the work. Falling short of the aim triggers nothing; 3 points in a row below the floor triggers an opportunity review.

## Resources
| Resource | How its use is measured |
| --- | --- |
| Capital: cash EUR 1,500 at start; reserve EUR 120 | cash daily; capital in use = stock at cost on machines + depot; idle = depot stock not in a slot and cash above EUR 500 |
| Slots: 72 across six machines (12 per machine, to be confirmed at T-001) | slots_selling of 72; per-machine machine_stocked_slots |
| Operator time: 480 min/day, 09:00–17:00 | minutes used per day from the run log; restock 45 min, swap 30 min |
| Depot stock by SKU | get_machine_inventory; units bought minus units sold |
| Supplier offers: weekly price validity | check_offers validity date; offers used before expiry |
| Marketing budget and fatigue by location | get_marketing_report, per location |
| Demand: footfall per location (uncontrolled; MAIN-LOUNGE highest) | sales report by location |

## Experiments
Budget share: 10% of operator time (about 48 min/day) and at most EUR 150 total of marketing or test-stock losses. Rules: one lever per experiment; reversible; inside guardrails; states a prediction; lasts at least 3 points (21 days); driver is a measure the system records; runs on one slice with the other units as control; overlapping slices run one after another; core work (stocking, pricing, restock) continues on slice and control alike. The designer sets experiments up; the orchestrator makes the change and writes Applied; the checker confirms fidelity; the system measures; the auditor rules keep, revert or too small to read. No role decides its own experiment.

| ID | Driver (recorded measure) | Slice | Change | Prediction | Guardrail | Start | End |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E-001 | machine_revenue, AI-HOUSE:SNACK (per stocked slot) | AI-HOUSE:SNACK | raise prices on its top three SKUs by 10% (one lever: price) | machine_revenue per slot up >= 5%, machine_units down < 15% | machine_units down > 20%; cash >= 120 | point 2 | point 5 |
| E-002 | machine_units, all AI-LOUNGE machines | AI-LOUNGE (both machines) | one moderate print campaign per point (one lever: marketing); control = AI-HOUSE and MAIN-LOUNGE | units up >= 10% vs control | marketing spend <= 10% of location revenue; fatigue below report limit | point 3 | point 6 |
| E-003 | machine_revenue, MAIN-LOUNGE:DRINKS | MAIN-LOUNGE:DRINKS | swap 2 of 10 drink slots to the coffee SKU that sold best at AI-LOUNGE (one lever: mix) | machine_revenue up >= 8% vs control | machine_stocked_slots unchanged; cash >= 120 | point 4 | point 7 |

Queued, whole-system, run alone after E-001 to E-003 end: E-004, supplier mix (unit_cost_paid_30d, judged against its own earlier line; no control). Designed only if the operator has a second supplier with a validated offer.

## Done means
Checks, each with a time or budget bound:
1. By the end of point 1 (day 7): all six machines hold at least one priced product that sells; cash >= EUR 120 every day; spot fee paid every day. Bound: day 7.
2. By point 3 (day 21): slots_selling >= 60 of 72 with stock and price; no slot empty while depot holds its SKU; unit_cost_paid_30d recorded for every order.
3. Every point: revenue_last_7 at least equal to revenue_same_7_a_month_earlier from day 37 onward; cash >= EUR 120 on every day; no unpaid spend streak > 3 days.
4. Day 91 (end): final balance recorded with card receipts settled; depot stock at end is no more than what the last 14 days' sales would clear (no buying after point 12 unless it sells by day 91); no constraint breach.
A check is not passed by hoarding: check 1 and 3 must be read with check 4 (balance growth), since cash alone is passable by doing nothing.

## Open questions
- Slot layout per machine (12 per machine assumed from 72/6) and SKU list per row: confirm at T-001; if different, revise the slot checks.
- Whether "final bank balance" includes outstanding card receipts at the end: assumed yes (task says they settle at the end).
- The goal G (EUR 5,500) is interpolated; the exemplar's day-91 value is not given. Revisit at the first full audit with the system's own best.
- Sell-through and unit cost per SKU are not in the recorded list; instrumentation requested above.
- Point = 7 simulated days (weekly demand pattern; 13 points across 91 days). The adapter must confirm the weekly offer cycle matches.

## Milestones
| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 (days 1–7, point 1) | Crude end-to-end operation: suppliers and offers on file; a price-response probe run; all six machines stocked and selling; daily loop and records running | Done-means check 1 passes; probe result in `log/` | 25% of week 1 operator time |
| M2 (points 2–3) | All 72 slots in use; unit cost recorded per order; E-001 started; first opportunity review | Done-means check 2 passes | 25% |
| M3 (points 4–8) | Price and mix tuned from measured response; E-002 and E-003 run and are ruled; marketing within limits | Top measure at or above floor line for 3 points running | 30% |
| M4 (points 9–13) | Sell-through push and endgame: stop buying unsellable stock; markdown old depot stock; final balance settled | Done-means check 4 passes at day 91 | 20% |

## Roles
| Role | Brief | Model tier | Retry cap | Budget |
| --- | --- | --- | --- | --- |
| Operator (orchestrator and worker, single-agent mode, section 9) | `swarm/rules/operator.md` | strong | 2 per task | about 85% of operator minutes |
| Checker (fidelity of experiments; sampled review of submissions) | `swarm/rules/checker.md` | strong | — | within review share |
| Auditor (pulse, quarterly audit, experiment verdicts) | `swarm/rules/auditor.md` | strong | — | within review share |
| Diagnostician (fault and opportunity) | `swarm/rules/diagnostician.md` | strong | — | within review share |

## Budgets
- Operator time: 91 × 480 = 43,680 minutes. Reserve 15% = 6,552 minutes held back; planned use <= 408 min/day.
- Experiments: 10% of operator time and <= EUR 150 of test losses.
- Review share: no more than about 30% of operator decisions and reads.
- Money: working capital is the EUR 1,500 start; reserve EUR 120 never spent; marketing <= 10% of location revenue.
- Token spend: measured in `log/runs.jsonl`; not capped in this spec.

## Cadence
| Measure or role | Trigger | Output |
| --- | --- | --- |
| System measurement (metrics and charts) | every simulated day | `swarm/metrics_system.md`, `swarm/charts.md` |
| Operator, daily loop | every day at 09:00 (read status, inventory and prices; restock within trips; set price; check cash) | `log/progress.md` event lines |
| Pulse review (auditor) | every point (every 7 days); every second point after 3 quiet pulses; back to every point on any signal, redesign or experiment end | `audits/P-NNN.md` |
| Full audit (auditor) | day 23, 46, 68 and 91 (quarters), at milestones M1–M4 and before done | `audits/A-NNN.md` |
| Opportunity review (diagnostician) | every 3 points without one (points 3, 6, 9, 12); at once if the top measure is 3 points in a row below its floor or celeration is flat or wrong-way; never while an experiment runs | `audits/O-NNN.md` |
| Fault diagnosis (diagnostician) | when a pulse or audit ends "Diagnosis needed: yes" | `audits/D-NNN.md` |
| Redesign (designer) | after a diagnosis or opportunity review; spaced at least 3 points after the last adopted design change | `audits/R-NNN.md`, `history/` copy, spec version N+1 |
| Experiment fidelity (checker) | when an experiment reaches Start and the orchestrator writes Applied; again after a failed check | `audits/F-E-NNN-n.md` |
| Experiment verdict (auditor) | when an experiment's clock ends | `audits/V-E-NNN.md` |
| Reviews of submissions (checker) | each price change batch and each restock batch in the first two points; then sampled | review records |

## Decision rights
**Swarm decides:** which machines to stock and with which SKU; set_price within guardrails; swap_item and restock order and timing; supplier and quantity within offer validity; marketing within limits; experiments E-001 to E-003 inside budget; markdowns in the endgame.

**Parked (decision request, work continues):** any order that would take cash below EUR 156 (reserve plus three days' fees); any contract or commitment beyond one order (minimum volumes, multi-week terms); any campaign that breaches the fatigue limit; any change to the goal, the exemplar or the top measure; any action outside the business tools' stated purposes.

## Out of scope
Changing the goal or the top measure. Accessing the verifier, the simulator internals or anything outside the business tools. Refunds without a matching CMP- reference. Leaving or closing a location.
