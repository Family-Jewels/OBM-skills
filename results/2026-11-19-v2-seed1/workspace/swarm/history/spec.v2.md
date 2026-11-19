# Swarm spec: Prosus Vending Bench, 365-day operation   Version 2 (redesign R-O-001, day 51; v1 in history/spec.v1.md)

## Goal
Maximise the bank balance at the end of simulated day 365, starting from EUR 1,500, without bankruptcy (more than 10 consecutive unpaid spot-fee days) and without leaving the network with unpaid card receipts. Receiver: the human who reads the final balance. The goal is maximisation; the exemplar below is a reference, not a cap.

Horizon: 365 simulated days = 52 full 7-day points + 1 day. Points are weeks (point k = days 7k-6 to 7k). Quarter = 13 points (days 91, 182, 273, 365).

## Driver tree

Top measure: **cash** (bank balance, end of day). Final cash = 1,500 + revenue - stock cost - fees - marketing (- refunds). Fees are fixed at EUR 12/day = EUR 4,380 over the horizon.

| Measure | = made of | Ground-truth source | Better | Ceiling (source, confidence) | Guardrail | Push on now? |
| --- | --- | --- | --- | --- | --- | --- |
| cash | opening 1,500 + revenue - stock cost - fees - marketing - refunds | bank ledger, system `cash` | up | 61,219 at day 365 (benchmark reference operator, which knows hidden parameters; medium confidence for the final level, low for intermediate levels) | cash >= 120 every day (see reserve guardrail); no unpaid fee | Yes (top) |
| revenue | sum over machines of slots_selling x revenue_per_slot | `revenue`, `machine_revenue` x6 | up | Resource ceiling: 72 slots x realised price x demand; no firm number yet (low) | none direct | Yes |
| stock cost | units bought x unit price paid | `unit_cost_paid_30d`, order receipts | down per unit sold | Own best offer seen at the same quantity (low-medium) | unit cost + margin must stay below realised price on every priced slot | Yes |
| marketing spend | campaign costs | `get_marketing_report` costs | down unless it pays back | none (instrument: revenue lift per EUR spent, measured by E-002) | campaign only if the location's revenue_last_7 rose after the last campaign and cash >= 120 + 2 days of fees | Experiment only |
| slots_selling | slots stocked AND priced | `slots_selling`, daily slot snapshot | up | 72 (resource: slots in the network; high confidence) | none | Yes: refill throughput |
| revenue_per_slot | units per selling slot-day x realised price | `revenue_per_slot` (median per point) | up | none firm; exemplar's day-30 and day-365 totals only (low) | units on a slice must not fall more than 25% vs its own line when price changes (E-001) | Yes |
| units per selling slot-day | footfall x preference match x price response x duplicate sharing | `units`, `machine_units`, sales report | up | none firm (low) | none | Yes: product mix and footfall |
| realised price | set_price per slot | `set_price` log, slot snapshot | up unless units fall faster | none firm; price response is uncertain (low) -> E-001 | price >= unit cost + margin; price change on a slice only in E-001 | Experiment only |
| footfall (traffic) | location multiplier from marketing | `get_marketing_report` multipliers | up | none (instrument) | campaign fatigue: no campaign at a location within 7 days of the last one | Experiment only |
| worker minutes used per day | sum of tool-call minutes (refill 45, swap 30, others as recorded) | `log/work.jsonl` | fully used, but on high-value actions | 480 (resource; high confidence) | never past 480; never filling a slot that will not sell | Yes |
| refill minutes per revenue | refill minutes / revenue gained from refilled slots | derived from `work.jsonl` and `machine_revenue` | down | none (instrument) | none | Yes |

Drivers the swarm controls: slot choice and refill order, product mix per slot, price per slot, purchase timing and quantity, supplier choice, marketing timing, worker minutes.
Drivers it does not control: footfall base, demand preferences, weather, season, supplier outages, card settlement timing.

Instrumentation needed (not yet recorded): refill minutes per revenue (derived); marketing lift per EUR (derived from E-002). Neither may be reported by an agent.

## Exemplar
Benchmark's scripted reference operator (knows the economy's hidden parameters): EUR 3,228 at day 30 and EUR 61,219 at day 365 from EUR 1,500.
- Implied celeration, days 0-30: 2.152 over 30 days = about x1.20 per 7-day point.
- Implied celeration, days 30-365: 18.96 over 335 days = about x1.063 per 7-day point.
- Own best: none yet. The swarm's own best celeration becomes the improvement exemplar after point 6.

## Resources
| Resource | How its use is measured |
| --- | --- |
| Worker time (the binding constraint): 480 minutes per working day, 09:00-17:00 | sum of simulated minutes of each tool call from `log/work.jsonl`; idle = 480 - used at wait_for_next_day |
| Slots: 72 across six machines (12 per machine is implied: 72/6; verify in the first snapshot) | slots_selling and stocked-but-unpriced slots, daily snapshot; idle = 72 - slots_selling |
| Capital: cash | cash in use = stock value in machines (units x unit cost paid) + committed marketing; cash idle = cash above the EUR 120 reserve not converted to stock on a selling slot |
| Demand (per location) | units and revenue per machine; traffic multiplier from marketing report |
| Depot stock | units at depot by product (inventory), so an order is not placed for stock already on hand |
| Model budget for the swarm (tokens or USD) | measured spend in `log/runs.jsonl`; pulses kept short so the budget reaches day 365 |

Idle resources: idle worker minutes while a driver is short are the first opportunity; idle capital while slots are empty is the second.

## Experiments
Budget share: at most 10% of worker minutes per day (48 minutes) across all experiments, and at most two experiments at once. Experiments are only for uncertain levers. Known fixes are in the design now (see Known fixes below), not in experiments.

Rules: one-time settings that persist; each states its capacity cost; each has a prediction; each runs on a slice of machines with the rest as control; each starts no earlier than point 4 (day 22); each lasts at least 3 points; each is reversible; guardrails enforced by the system; the auditor rules keep, revert or too small to read.

| ID | Driver (a recorded measure) | Slice | Change | Prediction | Guardrail | Start | End | Capacity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E-001 | revenue_per_slot per machine, daily | DRINKS machines at AI-LOUNGE and MAIN-LOUNGE | price on every slot raised 10% once, at start (single lever; no other change on the slice) | revenue_per_slot on slice rises >= 5% vs its own pre-start line, net of control's same-period change (difference-in-differences) | units on slice fall no more than 25% vs its own line; cash >= 120 | point 4 (day 22) | point 8 (day 56) | about 5 min/day for price checks |
| E-002 | machine_revenue, summed over the slice | MAIN-LOUNGE (both machines) | standing one-time policy: one print campaign at MAIN-LOUNGE, then none for 14 days unless the policy is renewed by the auditor; control: AI-HOUSE machines get no campaigns | machine_revenue on the slice rises by more than the campaign cost within the window, versus control | cash >= 120; no more than 2 campaigns in the window; stop if get_marketing_report shows fatigue | point 4 (day 22) | point 8 (day 56) | about 5 min/day for run_marketing calls |

Both experiments are queued if an earlier one still runs on overlapping machines (none overlap at the start). Skip E-001 if `get_sales_report` already shows a clear price-response curve by point 3; skip E-002 if the marketing report shows multipliers are already flat after a campaign. Skipping is recorded in the next pulse, with the reason.

Judgement of E-002 uses money: a campaign that did not pay back its cost in revenue within the window is a revert.

## Known fixes (applied to every machine at once, now)
1. Every stocked slot gets a price the same day (unpriced stock sells nothing).
2. Snack machines take food only; drinks machines take beverages only. Rows A-B take small products (18 units), rows C-D take large products (10 units).
3. Duplicate slots share demand: fill a second slot with a product only when the first has sold out or the slot has idle capacity.
4. Check `check_offers` at the quantity you intend to buy before `order_goods`; offers change every 7 days, so compare against the validity date. Prices paid are current prices at order time.
5. Pay the EUR 12/day fee every day; keep cash at or above EUR 120 plus 2 days of fees (EUR 144) before any purchase or campaign. Card receipts settle a day later: count them as not yet cash.
6. Swap a slot's product with `swap_item` (30 min) instead of clearing and refilling (45 min plus the clear) when the product changes.
7. Start each day with status and inventory; end each day with wait_for_next_day only after the day's refills and prices are set.
8. Refunds: `send_payment` with the exact CMP- reference and the full amount only; an unmatched payment is lost.
9. Never send an order email with quantities that was not intended: it buys immediately.
10. (R-O-001, day 51) Restock before a slot empties. Keep depot stock of at least 7 days of sales per selling slot before the next delivery, and order to that level when check_offers holds (within the cash floor and the 60% purchase rule). Prediction: slots_selling rises from 8 toward 13-17 (its days 45-48 level) within 2 points.
11. (R-O-001, day 51) Spend worker minutes where output per minute is highest, because worker time is the constraint (415 of 480 used on the day of review; 65 idle). Refill A-B snack rows (18 units, about EUR 25-40 per 45 min) before C-D drinks (about EUR 15 per 45 min). Use idle minutes at the end of the day on refills with stock on hand, never on a slot that will not sell.

## Done means
- Simulation reaches day 365 (SIMULATION OVER) with no bankruptcy and no unpaid-days breach.
- Final bank balance is recorded in the ledger, and every card receipt is settled.
- Reserve guardrail (cash >= 120 each day) never breached; any breach is recorded with its cause.
- Each quarter's full audit (A-001 to A-004) is written, and each experiment has a verdict (V-E-NNN).
- No misreport in the records: every operator submission note matches `log/work.jsonl` and the ledger.

Checks (could a check be passed without the goal?):
| Stage | Measure | Can it be passed without the goal? |
| --- | --- | --- |
| Each day | every stocked slot is priced; cash >= 120 | Yes (doing nothing passes if cash is not spent). Add: revenue_last_7 >= revenue_same_7_a_month_earlier after point 4, or the pulse names the cause |
| Each week | purchase: receipts match check_offers quote and the order was sensible for the slot snapshot | Yes if the order is small. Add: units bought per slot sold last week within a range set by the auditor |
| Each point | celeration of cash and revenue_last_7 vs the floor line and the aim | Passing the floor line is the goal's direction, not the goal |
| Each quarter | full audit: direction, experiment verdicts, spend vs progress | Full audit reads the ledger, not reports |

## Milestones
| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 | Crude end-to-end loop: all 72 slots reviewed, the highest-value slots stocked and priced, the fee paid daily, the ledger read, charts written every day | day 21 (point 3) ends with cash >= 120 every day, slots_selling >= 24, and the pulse shows the loop running with no unpaid fee | about 10% of the first three weeks |
| M2 | Core operating loop at scale: all 72 slots selling by ~day 70 (re-dated from day 35 at R-O-001; the level of 60 is unchanged), weekly purchase review, marketing and price settings on the current policy | slots_selling >= 60 for 2 points; revenue_last_7 rising point-on-point; 0 misreports | about 25% of the horizon |
| M3 | Experiments run, verdicts issued, design updated once with the verdict | E-001 and E-002 have verdicts by day 56; any keep is in the spec at the next redesign (spaced 3 points after the last change) | experiment budget as above |
| M4 | Quarterly audits held; cash celeration at or above the floor line | A-001 (day 91), A-002 (day 182), A-003 (day 273) written, each with direction verdict | per quarter |
| M5 | Horizon end | day 365 reached; done criteria met | final |

Milestone 1 is the only one planned in detail (board.jsonl). The rest are not gating: the loop runs in parallel with each.

## Roles
Single-agent mode (protocol section 9): one operator plays every role, each in a fresh context where possible, and writes every record before switching. Never check work in the context that produced it.

| Role | Brief | Model tier | Retry cap | Budget |
| --- | --- | --- | --- | --- |
| Operator (orchestrator and worker) | rules/operator.md | strong | 2 per task | operating capital (see Budgets) and the model budget |
| Checker (incl. experiment fidelity) | rules/checker.md | strong | 2 | <= 30% of spend |
| Auditor (pulse, full audits, verdicts) | rules/auditor.md | strong | 2 | <= 30% of spend |
| Diagnostician (fault and opportunity) | rules/diagnostician.md | strong | 2 | as needed; called only on triggers |
| Designer (redesign only) | this file | strong | 2 | as needed |

## Checks by stage
Covered in Done means. Risk tiers: high = any purchase above EUR 150, any price change on more than 3 slots at once, any campaign, any experiment start; standard = weekly routine; low = read-only status.

## Budgets
- Operating capital: the cash balance. Reserve guardrail is EUR 120 (hard floor) plus 2 days of fees (EUR 24) = EUR 144 as the purchase floor. No single purchase above 60% of cash above the floor.
- Marketing: at most EUR 50 per campaign, at most one campaign per location per 14 days (fatigue).
- Model budget: spend from `log/runs.jsonl`. Reserve 15% of the total. Review share at most 30%. Pulses are kept under about 1,000 words so the budget reaches day 365.

## Cadence
Points are 7 simulated days. Quarters are 13 points.

| Measure or role | Trigger | Output |
| --- | --- | --- |
| Measurement (the system) | Every day | `swarm/metrics_system.md` and `swarm/charts.md` updated; `log/slot_snapshots.jsonl` appended (72 rows per day) |
| Measurement, celeration | Every point (days 7, 14, ..., 364) | celeration per measure and floor/aim update on `charts.md` |
| Auditor, pulse | Every point (52 pulses); every second point after 3 quiet pulses; back to every point on any signal, redesign or experiment end | `audits/P-NNN.md` |
| Auditor, full audit | Days 91, 182, 273, 365; at M1 (day 21) and before done | `audits/A-NNN.md` |
| Checker, submission | Each weekly purchase plan and each experiment's start; sampled after 5 first-pass successes (1 in 3), then after 10 more (1 in 5) | review record in `log/reviews/` |
| Checker, experiment fidelity | When E-NNN reaches its start (point 4, day 22), and again after a failed check | `audits/F-E-NNN-n.md` with `Fidelity: pass` or `fail` |
| Auditor, experiment verdict | At the end of each experiment's window (E-001: day 56; E-002: day 56) | `audits/V-E-NNN.md` with `Verdict: keep`, `revert` or `too small to read` |
| Diagnostician, fault | When a pulse or audit ends `Diagnosis needed: yes`; or top measure below floor 3 points in a row | `audits/D-NNN.md` |
| Diagnostician, opportunity | Every 3 points without one (days 21, 42, 63, ...), skipped while an experiment runs; or top measure 3 points in a row below its floor | `audits/O-NNN.md` |
| Designer, redesign | After a diagnosis or opportunity review; spaced at least 3 points after the last adopted change | `audits/R-NNN.md`, new spec version, history copy |

## Decision rights
Swarm decides: prices within guardrails; which slots to refill and in what order; product mix and quantity per slot; supplier choice and orders within budget; marketing within the budget; refunds with the exact CMP- reference; the daily order of work.
Parked (decision request in `queue/decisions.md`, work continues): any purchase above 60% of cash above the floor; any change to the goal, aims or done criteria; any experiment whose guardrail is unclear; any supplier that has not delivered on a prior order; any action with no reversal.

## Out of scope
Changing the goal or the exemplar; creating new locations or machines; reading the verifier or simulator internals; using tools outside the business tool set.

## Open questions
1. Tool-call minute costs for reads, price changes and swaps are not given; the first day's `work.jsonl` must record them, and the designer should update the worker-minute ceilings after point 1.
2. Per-machine slot count (12 per machine implied) and whether restock quantity per slot is capped: verify in the first snapshot.
3. "Same 7 a month earlier" is defined as the 7-day window ending 28 days earlier (keeps weekdays aligned); the seasonal shift over Nov-Feb is not covered beyond that.
4. Aim rule: the aim is the geometric line that reaches the goal at the midpoint of the remaining horizon, then continues at the same celeration; if met on 2 of the last 3 points, the aim is raised by 25%. This is a designer choice; the auditor should check whether it makes the aim unreachable.
5. Card receipts settle a day later; the reserve guardrail uses cash plus settled card and reports unsettled card separately.
6. The swarm's own model budget in this session is small (about USD 2); if it binds before day 365, pulses drop to the quarterly audit and the daily charts are the only daily work. The designer must be told this before the redesign after point 13.
7. Demand is shared across duplicate slots; the exact sharing rule and the price response curve are unknown until get_sales_report shows them.
8. The exemplar's day-30 and day-365 totals are the only external ceilings; no intermediate ceiling exists. Confidence on intermediate floors is low.
9. (R-O-001) `log/work.jsonl` is not in the workspace, yet charts.md shows 415 of 480 minutes used on day 51 while O-001 read 0. The orchestrator must confirm the path; until then the worker-minute chart is the reading used, and refill minutes per revenue cannot be derived.
10. (R-O-001) Depot-depth size (7 days of sales per slot, known fix 10) is not yet an experiment. If slots_selling does not rise within 2 points of day 51, the auditor should name it as the candidate experiment for the first free slot (E-001 ends day 56) on AI-HOUSE machines, which share no slice with E-001 or E-002.

## Preflight
- Could a fresh agent reading only its brief state the goal, its task and how it will be judged? Yes: the goal is the final balance; tasks are the milestones; judged by the floor and the done criteria.
- Does the tree add up? Cash = revenue - stock cost - fees - marketing - refunds; revenue = slots_selling x revenue_per_slot summed over machines. Yes.
- Can every part be measured from ground truth? Yes except refill minutes per revenue and marketing lift, which are derived from the ledger and the work log, never reported by an agent.
- Can any check be passed without the goal? Two were (cash >= 120; slots priced); the added checks in Done means cover that.
