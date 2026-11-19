# Swarm spec: Prosus Vending Bench, 365-day operation   Version 7 (redesign R-O-005, day 309; v6 in history/spec.v6.md, v5 in history/spec.v5.md, v4 in history/spec.v4.md, v3 in history/spec.v3.md, v2 in history/spec.v2.md, v1 in history/spec.v1.md)

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
| E-002 | machine_revenue, summed over the slice | MAIN-LOUNGE (both machines) | standing one-time policy: one print campaign at MAIN-LOUNGE, then none for 14 days unless the policy is renewed by the auditor; control: AI-HOUSE machines get no campaigns | machine_revenue on the slice rises by more than the campaign cost within the window, versus control | cash >= 120; no more than 2 campaigns in the window; stop if get_marketing_report shows fatigue | re-issued day 88 (R-P-010; the day-21 start was void, see E-002.md) | day 112 (point 16) | about 5 min/day for run_marketing calls |
| E-004 | machine_revenue, summed over the slice | AI-HOUSE:SNACK (rows A-B, six slots) | one-time price cut of 10% on rows A-B, set once at start and kept; no other change; control: rest (AI-LOUNGE, MAIN-LOUNGE and AI-HOUSE drinks keep current prices) | units per slot on the slice rise 20% or more vs control's same-period change, and machine_revenue on the slice rises >= 5% vs control's same-period change (difference-in-differences), by day 217 | price >= unit cost + margin on every slot; cash >= 144 before each purchase; loading (known fix 15) and ordering (known fix 17) continue on slice and control alike | start day 197 (point 29; after PO-1045 is due); end day 217. Set by R-O-003 (day 187). Not started before stock is in the slice's rows | day 197 + 20 (21 days inclusive) | about 5 min/day for price checks |
| E-005 | machine_revenue, summed over the slice | AI-HOUSE:SNACK rows C-D (priced empty slots at the machine; O-005 counts 5) | one-time setting: a priced empty slot in rows C-D is filled from depot stock even when the snapshot predicts no sales for its product (the "never fill a slot that will not sell" default is lifted on this slice only, for these rows only); no other change; control: rest, which keeps the default | machine_revenue on the slice rises by at least 20% vs control's same-period change, per day, by day 336 (demand-sharing test: A-B units per slot on AI-HOUSE:SNACK fall no more than 25%) | cash >= 144 before each purchase; price >= unit cost + margin; loading and ordering continue on slice and control alike; no fill above the 60% purchase rule | start day 316 (point 46; after the R-O-005 change has run one point); end day 336 (21 days inclusive). Fidelity check (F-E-005-1) before the start | day 316 to 336: about 45 min/day for 5 days (one fill per day, 225 min total), then about 5 min/day; inside the 48 min/day experiment budget |
| E-003 | machine_revenue, summed over the slice | AI-LOUNGE (both machines) | one-time setting: a stocked slot is filled from depot stock even when the snapshot predicts no sales for its product (the "never fill a slot that will not sell" default is lifted on this slice only); priced the same day; control: rest, which keeps the default | machine_revenue on the slice rises by at least 30% vs control's same-period change, per day, by day 133 | cash >= 144 before each purchase; no fill above the 60% purchase rule; price >= unit cost + margin; control's core work unchanged | parked at R-O-002 (day 126): fidelity failed (F-E-003-1, day 114); not started. Start = the day F-E-003-2 passes, not before day 127 | start + 20 (21 days inclusive) | about 20 min/day for refills, when running |

Both experiments are queued if an earlier one still runs on overlapping machines or overlapping controls. E-003 is queued behind E-002 for that reason. Skip E-001 if `get_sales_report` already shows a clear price-response curve by point 3; skip E-002 if the marketing report shows multipliers are already flat after a campaign. Skipping is recorded in the next pulse, with the reason.

Clock rule (R-P-010): an experiment's clock starts at its re-issued Start day, never earlier. The day-78 "running" entry for E-002 in charts.md is void: E-002.md records it as suspended from day 25 and no campaign may run until this re-issue. The auditor should re-date E-002's verdict to day 88-112.

Judgement of E-002 uses money: a campaign that did not pay back its cost in revenue within the window is a revert.

## Known fixes (applied to every machine at once, now)
1. Every stocked slot gets a price the same day (unpriced stock sells nothing).
2. Snack machines take food only; drinks machines take beverages only. Rows A-B take small products (18 units), rows C-D take large products (10 units).
3. Duplicate slots share demand: fill a second slot with a product only when the first has sold out or the slot has idle capacity.
4. Check `check_offers` at the quantity you intend to buy before `order_goods`; offers change every 7 days, so compare against the validity date. Prices paid are current prices at order time.
5. Pay the EUR 12/day fee every day; keep cash at or above EUR 120 plus 2 days of fees (EUR 144) before any purchase or campaign. Card receipts settle a day later: count them as not yet cash.
6. Swap a slot's product with `swap_item` (30 min) instead of clearing and refilling (45 min plus the clear) when the product changes.
7. Start each day with status and inventory; end each day with wait_for_next_day only after the day's refills and prices are set.
8. Refunds: `send_payment` with the exact CMP- reference and the full amount only; an unmatched payment is lost. (R-O-003, day 187) Check each claim against the item's price first: pay up to the item price only; any amount above it is parked as a decision request. O-003 found about EUR 290 paid on 19 claims, many at 9-11x item price (P-019).
9. Never send an order email with quantities that was not intended: it buys immediately.
10. (R-O-001, day 51) Restock before a slot empties. Keep depot stock of at least 7 days of sales per selling slot before the next delivery, and order to that level when check_offers holds (within the cash floor and the 60% purchase rule). Prediction: slots_selling rises from 8 toward 13-17 (its days 45-48 level) within 2 points.
11. (R-O-001, day 51) Spend worker minutes where output per minute is highest, because worker time is the constraint (415 of 480 used on the day of review; 65 idle). Refill A-B snack rows (18 units, about EUR 25-40 per 45 min) before C-D drinks (about EUR 15 per 45 min). Never fill a slot that will not sell. (R-O-002: loading moved from end-of-day leftover minutes to the start of the day, known fix 15. R-P-010: the worker-time constraint is unverified; charts.md reads 38% of worker time in use, so the binding step is loading depot stock into slots, not minutes. Refill rule kept; see 14.)
12. (R-P-010, day 86) Order timing: the 7-day depot target cannot be met with 6-8 day deliveries. Order when depot stock falls below 8 days of sales plus 1 day of safety, to 8 days (operator rule, 7 and 8 replaced). The target level of 7 days is no longer the trigger. Prediction: slots_selling reaches >= 12 at point 14 (day 98) and does not fall below 8 at any point after day 98 (charts.md, slots_selling).
13. (R-P-010, day 86) The day-38 hold "no price change on AI-LOUNGE or MAIN-LOUNGE DRINKS" is retired: its stated reason (the E-001/E-002 overlap) ended at E-001's verdict (day 56). Prices on those machines are set within guardrails, as for all machines. If the owner wants the hold back, it is reinstated in queue/decisions.md.
14. (R-P-010, day 86) Reconcile delivered units daily: units received (order receipts) = units in depot + units in machines + units sold. Until `log/` is present in the workspace, this is a standing parked item, not an input; no cause is assigned to the ~400 unaccounted units until it is reconciled. PO-1019 and PO-1020 (due day 79) are checked on day 86: if still undelivered, the supplier is parked (operator rule, new).
15. (R-O-002, day 126) Load at the start of the day. Before any other work each day, every priced slot with quantity 0 whose product has depot stock is loaded from depot stock, in the order of known fix 11 (A-B snack rows first, then AI-HOUSE and AI-LOUNGE drinks rows). Loading is no longer left to end-of-day minutes, which is why 68 of 72 slots sat empty while 18 priced slots had stock on hand. (R-O-004, day 253) No fixed refill count: load until every such slot is loaded or the day's minutes reach 450 (30 minutes kept for prices and the purchase review); the rest the next day. The count cap of about 10 is retired: at 45 min a refill it left about 425 of 480 minutes idle while 25 priced slots sat empty (snapshot 00258). It uses stock already paid for, so it adds no purchase. Prediction: from day 127, the day-end count of priced empty slots with depot stock on hand is 0 (or the pulse names the cause); slots_selling >= 12 by point 20 (day 140) and not below 8 after that. Revert to the end-of-day rule only if cash falls below 144 or if the loaded slots show no machine_revenue after 2 points while depot stock is still on hand (the auditor rules).
16. (R-O-002, day 126) MAIN-LOUNGE drinks: stop restocking MAIN-LOUNGE:DRINKS (zero revenue since day 102). Its depot drinks are loaded only into AI-HOUSE and AI-LOUNGE drinks rows that sold in the last 7 days. The O-002 idea of moving that stock to snack rows is not possible: snack machines take food only (known fix 2), so it is not adopted.
17. (R-O-003, day 187) Order trigger uses the lead time quoted on the offer, and applies to every product sold in the last 7 days, not only to the rows that have just run out. Lead time = due day minus paid day, as stated on the order; plus 1 day of safety. When depot stock on hand is below that many days of sales, or below one full load of the priced slots that hold the product (whichever fires first), order to two full loads: row capacity (18 for rows A-B, 10 for rows C-D, drinks rows as the machine reports) x the priced slots holding it, less depot on hand (check_offers and the cash floor first). (R-O-004, day 253) Order size is set by slot capacity, not by recent sales: sizing to last week's sales, which were low because slots were empty, kept the slots empty. The 8-day sizing is retired. Reason: the 8-day figure is replaced by the quoted lead time, because PO-1045 (paid day 187, due day 197) quotes 10 days; O-003's 11-day figure (PO-1028) is older and not used. Whole-system now, because idle cash (about EUR 6,500 above the floor) is not a constraint. Prediction: the day-end count of priced empty slots whose product is not in depot falls to 0 once PO-1044 and PO-1045 are delivered (days 188 and 197); gummy-bears-150g (no open order, last delivery day 171) is ordered the day this applies.
18. (R-O-005, day 309) Order trigger also fires on empty slots with no stock. The sales test in known fix 17 never fires for a product whose slots are empty, because an empty slot sells nothing and so shows no recent sales: drinks and choco sat at zero depot stock for weeks on that account (O-005). Any product with a priced empty slot and no depot stock is now due for ordering to two full loads, after check_offers and the cash floor. Prediction: drinks and choco depot stock is above zero at point 46 (day 322); the day-end count of priced empty slots with no depot stock and no open order falls to 0 by point 47 (day 329); slots_selling holds at 14 or above at point 47 and its celeration turns up from flat. Cost: one order per product, paid now; cash stays above 144 by the 60% rule.

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
| Each day (R-O-003) | loading: the start-of-day log line reads "load: N priced empty with depot stock; M loaded; minutes used"; the day-end snapshot has 0 priced empty slots with depot stock, or the pulse names the cause | Yes if the log line is omitted. The snapshot count is the check; the log line alone does not pass |
| Each week | purchase: receipts match check_offers quote and the order was sensible for the slot snapshot | Yes if the order is small. Add: units bought per slot sold last week within a range set by the auditor |
| Each point | celeration of cash and revenue_last_7 vs the floor line and the aim | Passing the floor line is the goal's direction, not the goal |
| Each quarter | full audit: direction, experiment verdicts, spend vs progress | Full audit reads the ledger, not reports |

## Milestones
| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 | Crude end-to-end loop: all 72 slots reviewed, the highest-value slots stocked and priced, the fee paid daily, the ledger read, charts written every day | day 21 (point 3) ends with cash >= 120 every day, slots_selling >= 24, and the pulse shows the loop running with no unpaid fee | about 10% of the first three weeks |
| M2 | Core operating loop at scale: all 72 slots selling by ~day 70 (re-dated from day 35 at R-O-001; the level of 60 is unchanged), weekly purchase review, marketing and price settings on the current policy | slots_selling >= 60 for 2 points; revenue_last_7 rising point-on-point; 0 misreports | about 25% of the horizon |
| M3 | Experiments run, verdicts issued, design updated once with the verdict | E-001 verdict done (day 56); E-002 by day 112 and E-003 by day 133; any keep is in the spec at the next redesign (spaced 3 points after the last change) | experiment budget as above |
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
| Auditor, experiment verdict | At the end of each experiment's window (E-001: day 56, done; E-002: day 112; E-003: day 133) | `audits/V-E-NNN.md` with `Verdict: keep`, `revert` or `too small to read` |
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
10. (R-O-001) Depot-depth size (7 days of sales per slot, known fix 10) is not yet an experiment. If slots_selling does not rise within 2 points of day 51, the auditor should name it as the candidate experiment for the first free slot (E-001 ends day 56) on AI-HOUSE machines, which share no slice with E-001 or E-002. (R-P-010: slots_selling did not rise; depot depth is now a whole-system fix (known fix 12), not an experiment.)
11. (R-P-010) The `log/` directory is absent from the workspace: no work.jsonl, runs.jsonl, ledger or slot snapshots were found. Every worker-minute, spend and ledger figure in this spec is unverified. The orchestrator must restore the log path before the next pulse.
12. (R-P-010) D-P-010 cites figures that charts.md does not show (slots limit 7.84 and 2.83-18.17; cash_gain_7 beyond the upper limit; cash 3,164). charts.md is the reading of record; D-P-010 is superseded on those numbers. The causes it ranks (information, supply chain, incentives) are unchanged.
13. (R-P-010) Worker minutes: charts.md reads median 75 used of 480 (16%); D-P-010 reads 60. Neither is verified (see 11). If verified, worker time is idle and the constraint is depot supply and the day-38 hold.
14. (R-O-002) charts.md now reads 180 of 480 minutes (38%, median of last 7 days); O-002 read 28%. Both unverified without `log/work.jsonl`. Whichever is right, the loading step (known fix 15) is the constraint on the evidence in the snapshots: 18 priced slots with depot stock and zero quantity. The orchestrator confirms the reading before the next pulse.
15. (R-O-002) E-003's fill-policy lift cannot be verified from the snapshot (F-E-003-1, fail). The slot table needs a `fill_rule` column. Until F-E-003-2 passes, AI-LOUNGE keeps the default fill rule, and E-003 has no clock. Adding the column is an adapter change the designer cannot make; the orchestrator raises it with the owner.
16. (R-O-002) The workspace holds snapshots up to 00135 while charts.md, the pulses and this redesign are at day 126. Dates in this record follow the stated day 126. The orchestrator must confirm which day the snapshots belong to.
17. (R-O-003) Lead time conflict: O-003 cites 11 days (PO-1028); the order table shows paid-to-delivered of 2-4 days for PO-1031 to PO-1043 and a quoted 10 days for PO-1045. Known fix 17 uses the quoted figure on each order; the auditor should check whether the quoted lead times are stable.
18. (R-O-003) Snapshot 00188 (latest in the workspace) shows 5 products with depot stock (choco 54, cola 50, energy 40, oat 30, sparkling 32) and most of those rows still at quantity 0. The loading log (known fix 15) is not in the workspace, so whether the loading step was run is unverified. Dates: the request is for day 187; the newest snapshot is 00188.
19. (R-O-003) E-004's start day depends on PO-1044 and PO-1045 for nuts-mix, stroopwafel and crisps (AI-HOUSE:SNACK rows A-B hold nuts, stroopwafel and gummy). If either is late, E-004 starts at the first day all six rows have stock, and the auditor re-dates its window.
20. (R-O-004) The worker-minute chart (median 90 of 480 at P-025) and the snapshot evidence (about 25 priced empty slots with depot stock at day 258) agree that loading is not running at the rate the stock allows. Whether the worker stopped (budget, usage limit, outage) or the minutes measure misses work cannot be settled: `log/` is still absent. This redesign does not depend on that answer, but its prediction does: if `runs.jsonl` shows the worker was out of budget on days 235 to 258, the fix is environmental and the orchestrator raises it with the owner before the next pulse. Restoring the log path is a standing blocker since R-P-010.
21. (R-O-005) The aim (122,438 by the midpoint of the remaining horizon, x1.20 per point) is out of reach at the current celeration (x1.04; x1.26 needed from point 44). The aim and goal are the human's and are not changed here. The owner should be told that the aim will not be met and that the floor (x1.08) is the line that matters.
22. (R-O-005) O-005 reads median worker use at 280 of 480 and charts.md at 250 (52%); both are system or log readings for different windows. Neither changes the design: idle worker time is large either way. The 480-minute resource is measured by the system's clock; `log/work.jsonl` remains absent and is still a standing blocker.
23. (R-O-005) E-005's slice: O-005 counts 5 empty priced slots in AI-HOUSE:SNACK rows C-D. Rows A-B hold six slots at this machine (E-004), so rows C-D should hold six too; the count is unverified. The checker confirms the empty priced slots at fidelity (F-E-005-1), and the slice is whatever is found there.

## Preflight
- Could a fresh agent reading only its brief state the goal, its task and how it will be judged? Yes: the goal is the final balance; tasks are the milestones; judged by the floor and the done criteria.
- Does the tree add up? Cash = revenue - stock cost - fees - marketing - refunds; revenue = slots_selling x revenue_per_slot summed over machines. Yes.
- Can every part be measured from ground truth? Yes except refill minutes per revenue and marketing lift, which are derived from the ledger and the work log, never reported by an agent.
- Can any check be passed without the goal? Two were (cash >= 120; slots priced); the added checks in Done means cover that.
