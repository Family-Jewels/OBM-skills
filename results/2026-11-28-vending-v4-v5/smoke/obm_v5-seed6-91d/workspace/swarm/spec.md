# Swarm spec: Prosus Vending Bench   Version 3 (M-003, day 70; v2 in history/spec.v2.md)

## Goal
Maximise the bank balance at the end of the 91st simulated day, starting from EUR 1,500, across three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with one SNACK and one DRINKS machine (72 slots). Receiver: the human who owns the business result. The business is run from Prosus HQ atrium, Gustav Mahlerplein 5, Amsterdam. Depot: Vending Depot, Barbara Strozzilaan 201.

Point = one simulated working day. Daily measures are read at the day close (after the overnight sales).

## Driver tree

Top measure: **Bank balance at day 91 (EUR)**. Identity: balance = 1,500 + cash takings banked + card takings settled − unit costs paid − spot fees (EUR 12/day network) − marketing spend − customer refunds. Inventory left in machines or at the depot at the end is not money, so unsold stock is lost value.

| Measure | = made of | Ground-truth source | Better | Ceiling (source, confidence) | Guardrail | Push on now? |
| --- | --- | --- | --- | --- | --- | --- |
| Bank balance, day 91 (EUR) | 1,500 + revenue settled − unit costs paid − spot fees − marketing − refunds | get_status (cash, daily); the system's ledger reconciliation | up | EUR 5,500 at day 91 (exemplar interpolated, see Exemplar; medium-low) | cash ≥ 120 at every day close | top, not pushed directly |
| Revenue (EUR; day and last 7 days) | units sold × average realised price | get_sales_report (overnight sales, system-recorded) | up | exemplar pace (medium-low) | none | via children |
| Units sold | slots_selling × units sold per selling slot per day | get_sales_report | up | demand-limited: duplicate slots share one demand pool, so the ceiling is the demand of each product-location pair; own best (low) | none | via children |
| **slots_selling** (capacity in use) | slots holding a priced product ÷ 72 | get_machine_inventory | up | 72 slots (resource ceiling, high confidence on the count) | cash ≥ 120 | **YES, first** |
| **revenue_per_slot** (EUR/day) | revenue ÷ slots_selling | system, from revenue and slots_selling | up | own best, then exemplar-implied (low) | margin per slot ≥ 0 (price above unit cost) | **YES** |
| Units sold per selling slot | product fit: savoury snacks and coffee for the picky lounges; hungry customers at AI-HOUSE buy more volume | get_sales_report by product and location | up | own best (low) | none | **YES** (mix choice) |
| Average realised price | set_price per slot; demand responds (AI-LOUNGE price-sensitive, AI-HOUSE less so) | get_sales_report price response per product and location | up to the demand-limited optimum | unknown: test first (M1 T-006) | units per slot must not fall faster than price rises | YES after the test |
| **unit_cost_paid_30d** (EUR/unit) | supplier unit price at the bought quantity (after negotiation and weekly discount) | order_goods receipts (actual cost after payment); check_offers as a forward look | down | best quote across suppliers at the quantity needed (medium) | unit cost < achieved price for that product; no stock bought that cannot be sold | **YES** |
| Worker minutes per selling slot per day | minutes spent on restock, swap, pricing and reading ÷ slots selling | Facts table (median minutes per action, every tool call) | down | 480 min ÷ 45 min per fill = about 10 fills a day (resource ceiling) | none | Resource, see below |
| Marketing traffic | run_marketing spend and its traffic multiplier, net of fatigue | get_marketing_report; sales change after campaigns | up only where the gain exceeds the cost | unknown (low): test at MAIN-LOUNGE only (M4) | per-location fatigue and cost limits in get_marketing_report | not until M4 |
| Spot fee (EUR 12/day) | fixed | get_status | — | not controllable | — | no |
| Unsold stock at the end | units bought − units sold − units still in slots | get_machine_inventory; order receipts | down | 0 at day 91 (medium) | none | late (day 75 onward) |

Instrumentation gap: the Facts table gives per-action minutes and costs, but no measure of demand per slot exists yet. The system must chart units per selling slot by product and location before the mix and price drivers are judged. Record the gap as a request to the human if the system cannot produce it. Depot cover per product and fills per restock call are also uncharted (REQ-036): until they are, the worker reads depot cover from get_storage_inventory before each restock.

## Exemplar
Scripted reference operator (benchmark, knows the economy's hidden parameters): bank about EUR 3,228 at day 30 and about EUR 61,219 at day 365, from EUR 1,500.
- Day 91 is not given. Interpolating the 30→365 growth as a constant daily factor (×1.0087/day) gives about EUR 5,500 at day 91. Confidence medium-low; the 365 figure is beyond the horizon and is used only to show the ceiling's shape.
- **Day-91 ceiling for the top measure: EUR 5,500** (the figure the floor and aim lines are judged against through the horizon). EUR 61,219 is the day-365 exemplar, not a target for this horizon.
- The exemplar's day-30 figure (≈ +EUR 1,730 in 30 days) is the pace to beat in the first month. The swarm's own best is none yet.
- **Exemplar path this spec uses (REQ-040, M-003):** the constant-factor interpolation above, i.e. bank = 3,228 × e^(0.008785 × (day − 30)). It gives about EUR 3,715 at day 46, about EUR 4,580 at day 70 and about EUR 5,500 at day 91. The PIP in swarm/charts.md ("Gap to the exemplar": EUR 5,997.72 at day 46, EUR 10,152.3 at day 70) does not follow this path. The path the system's PIP reads is set in the system's adapter, not in this workspace; the human is asked to confirm it or change the chart (see Requests in audits/M-003.md). Until then, PIP values are not used to set aims.

## Resources
| Resource | How its use is measured |
| --- | --- |
| **Worker time: 480 minutes per working day** (09:00–17:00 on the simulator clock) | Minutes spent per day, summed from the tool calls the system records (Facts table: restock_machine 45, swap_item 30, others as measured). Read from the simulator's clock, not from the worker's own count. Near its limit ⇒ more output per minute is the opportunity. **Basis of the split (REQ-007): a share of the 480 available minutes**, the basis of the plan in aims.md. A share of time spent is a different basis and is not used for the plan. |
| Cash | Bank balance at each day close (get_status). Reserve EUR 120 is the guardrail. Capital in use = value of stock held in slots and at the depot. |
| Machine slots (72) | slots_selling ÷ 72, per location and per machine |
| Depot stock | Units at the depot not yet in a slot (get_storage_inventory, per product). Idle depot stock while slots are empty is a symptom of a restock bottleneck. |
| Supplier quotes and discounts | check_offers results per supplier and quantity; each offer is valid for 7 simulated days, and quotes its lead time |
| Reorder trigger and order size (REQ-008, M-003) | Order from a supplier when depot cover for a product (units on hand ÷ units sold per day) falls below that supplier's quoted lead time plus 7 days, and no order for it is open. Order size: expected units a day × (lead time + 7 days), at the lowest quote whose lead time meets that cover. From day 84, size to what can sell before day 91 (expected units a day × days left). Lead times on record: zuidas 2 to 5 days (D1→D6; D37→D39); noordzee 3 (D37→D40); bakker about 14 to 15 (D1→D16); kanaal not yet measured (use its quote). Source: swarm/log/progress.md. |
| Marketing budget and fatigue | get_marketing_report: cost, limits, recent campaigns, traffic multipliers |

The worker's own capacity (time) is the constraint on the first point. Capital is the second constraint: it binds only when the next order would take cash below the reserve plus two days of spot fees (EUR 120 + 24). Capital is idle now (about EUR 4,500), so the cover rule above is sized from capital, not from cash.

## Done means
- At day 91 close, bank balance is as high as the business can make it, read from the ledger, not the worker's record.
- Cash stays at or above EUR 120 at every day close; no more than 10 consecutive unpaid days (the business ends).
- Revenue over the last 30 days exceeds revenue over the previous 30 days (from get_sales_report).
- Every stocked slot has a price. Every card takings balance is settled at the end.
- No open customer complaints at the end. Refunds, if any, paid with the exact CMP- reference and full amount.
- Must not change: the controls in swarm/controls.md (owned by the risk branch); no access to the verifier or simulator internals; only the business tools are used.

## Open questions
1. Supplier channel (answered in version 2, REQ-008): quotes come from check_offers (each valid 7 days, quoting a lead time); orders go through order_goods (paid at order, received after the lead time). Suppliers on record: zuidas, bakker, kanaal, noordzee. The Facts table shows no action that sends email; list_emails and read_email read replies and catalogues. Any negotiation by email is not a measured action.
2. Whether "cash" in the daily measures includes card takings not yet settled. Working assumption: cash = banked balance from get_status; card receipts are tracked separately until they settle.
3. Demand per slot and price elasticity per location are unknown. M1 T-006 tests them.
4. Whether the day-91 exemplar should be interpolated (done here) or taken from the benchmark once published.
5. Whether restock time includes walking to the depot. The Facts table will show it; no assumption is made here.
6. Which day the units, revenue and revenue_last_7 columns in swarm/metrics_system.md date to (REQ-044). That file is written by the system, so the designer cannot define it; the human is asked to have the system define it. Until then, a claim about units on a given day cannot be checked against the row for that day.
7. Stocked slots and selling slots disagree at day 70 (10 stocked at day end against 11 selling). The two measures do not yet share a definition; units per selling slot and stocked minus selling slots (REQ-012) wait on the human's measure.

## Milestones
| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 | Crude end-to-end loop: buy, restock, price, sell, read sales, reinvest, across all three locations | By the close of day 3: at least 18 slots selling with a price, cash ≥ 120 at each close, a sales report read for each location, and one price test recorded in a note | 3 working days, 480 min each, no tool call outside the business tools |
| M2 | Fill toward capacity with positive margin per slot | slots_selling ≥ 36 by day 10; revenue_per_slot not below its week-1 median; unit cost below achieved price on every product | to day 10 |
| M3 | Tune mix and price per location; negotiate unit cost | Per-product units and price reviewed each 7 days; unit_cost_paid_30d down 5% from the first 30-day value | days 10–30 |
| M4 | Test marketing at MAIN-LOUNGE (highest footfall) against the cost | A campaign whose revenue gain over 7 days exceeds its cost, or stop | days 20–45 |
| M5 | Hold capacity; clear down stock before the end | slots_selling ≥ 60 by day 45 (if the demand test allows); unsold stock ≈ 0 by day 88 | days 45–91 |

Only M1 is planned in detail. M2–M5 are one line each; the Strategist and designer re-plan them after the first redirect. The M2 to M5 dates have passed or are close; the Strategist's next redirect sets the aims for the remaining horizon, and the designer does not re-plan milestones here.

## Roles
| Role | Brief | Model tier | Retry cap | Budget |
| --- | --- | --- | --- | --- |
| Operator (worker, orchestrator in single-agent mode) | swarm/rules/operator.md | strong | 2 | the business's own cash, with the reserve; agent-side per-day budget set by the system |
| Checker (risk) | samples the operator's claims against get_status and get_sales_report | strong | — | review share ≤ 30% of the operator's time |
| Strategist, designer, controls owner, auditor (improvement and risk branches) | by protocol section 1 | strong | — | by the system |

## Checks
| Stage | Measure | Can it be passed without the goal? |
| --- | --- | --- |
| M1 | slots with a price (count) | Yes: stock cheap items no one buys. Add: revenue_per_slot ≥ 0 and a sales report read per location. |
| All | cash held (higher is better) | Yes: hoard cash and never restock. Add: slots_selling and revenue per day. |
| All | unit_cost_paid_30d down | Yes: buy cheap, unsellable stock. Add: unit cost < achieved price, and units sold per product. |
| M4 | marketing traffic | Yes: spend without gain. Add: 7-day revenue gain must exceed cost, or the campaign stops. |

## Budgets
- Total: the business's cash, 1,500 at start, minus the EUR 120 reserve. Orders pay immediately at current prices; no cancellation.
- Two floors, two decisions (REQ-034): **EUR 120** is the cash that must stay at every day close (the guardrail; Done means). **EUR 144** is the cash an order must leave behind: the EUR 120 reserve plus EUR 24 for two days of spot fees. Both apply; neither is wrong. A chart guardrail of 120 and an instruction of 144 for orders are the same rule at two points.
- Review share: at most 30% of operator time (about 144 minutes a day is the ceiling for checks and records).
- Spend is measured from the business's own records (runs.jsonl), not estimated.

## Cadence
| Measure or role | Trigger | Output |
| --- | --- | --- |
| Measurement (system) | Every point (day close) | metrics_system.md, charts.md, instructions.md |
| Risk pulse (auditor) | Guardrail crossed (cash < 120), a chart signal in the wrong direction, a measure missing, or the capacity split off plan; plus a routine sweep every risk_sweep_every points (1, since mistakes cannot be undone: a bad order is final) | audits/P-NNN.md |
| Checker | Claim sample every checker_every points | audits/K-NNN.md |
| Diagnostician | When faults are reported | audits/D-NNN.md |
| Controls owner | Each open request to controls | controls.md, audits/C-NNN.md |
| Strategist | Every strategy_every points (system-derived, at least 3); brought forward on a floor breach or a turn to flat | audits/S-NNN.md |
| Designer (aim update) | Right after each strategy | aims.md, audits/AS-NNN.md |
| Designer (method change) | Each open designer request, at least method_gap points apart | spec or rule versions, audits/M-NNN.md |
| Full audit | Each quarter of the horizon, at milestones (M1 end, M3 end) and before done (day 91) | audits/A-NNN.md |
| Organizer | Beside each full audit | audits/O-NNN.md |

Intervals are the system's, derived from the profile; none is set here.

## Decision rights
- **Swarm decides:** which products go in which slot; set_price within the guardrails; restock and swap order; which quoted supplier to order from; quantities within the cash guardrail and the order-size rule; the M1 price test design.
- **Parked (decisions/ queue, work continues):** any order that would take cash below EUR 144; any campaign spend (run_marketing) before M4 or above the limit in get_marketing_report; any change of scope (e.g. a fourth machine); any refund or complaint response with an unclear amount; anything touching controls.md or the verifier.
- Orders are irreversible. A purchase needs a stated reason: the product, quantity, expected sales per day, and the unit cost compared with the achieved price.

## Out of scope
- Accessing the verifier, simulator internals or any file the briefing does not name.
- Actions beyond the 91 simulated days, and the day-365 figure as a target.
- Changing the goal or the reserve.
