# Swarm spec: Prosus Vending Bench   Version 1
## Goal
Maximise the bank balance on the last simulated day (day 91), starting from EUR 1,500, across three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with one SNACK and one DRINKS machine (72 slots). Receiver: the human operating the business. Cash reserve EUR 120 is a guardrail on every day. More than 10 consecutive unpaid days ends the business, so the spot fee (EUR 12/day network) is never left unpaid.

## Driver tree

Top measure: **Bank balance, day 91** = 1,500 + Σ revenue − Σ unit cost paid − Σ spot fees (EUR 12/day) − Σ marketing spend ± card settlement lag (card takings settle a day later; outstanding receipts settle at the end).

| Measure | = made of | Ground-truth source | Better | Ceiling (source, confidence) | Guardrail | Push on now? |
| --- | --- | --- | --- | --- | --- | --- |
| Bank balance, day 91 | 1,500 + revenue − unit cost paid − fees − marketing | get_status (bank balance); system ledger | up | ~EUR 5,500 at day 91, log-linear interpolation between the reference operator's EUR 3,228 (day 30) and EUR 61,219 (day 365); low confidence (the reference knows hidden parameters, so the real curve may differ) | cash ≥ EUR 120 reserve every day | top (goal) |
| revenue (daily, revenue_last_7) | units × realised price | get_sales_report; system daily measure `revenue`, `revenue_last_7` | up | none direct; exemplar-implied, see above | none beyond cash reserve | via children |
| units | slots_selling × units sold per selling slot per day (demand-limited) | get_sales_report (`units`) | up | demand-limited: ceiling unknown until price test; medium-low confidence | units must not fall at a location after a price change beyond the price test's result | via children |
| slots_selling | slots stocked AND priced (count, 0–72) | get_machine_inventory; system `slots_selling` | up | 72 (machine layout, high confidence) | none | **yes, priority 1** |
| revenue_per_slot | revenue ÷ slots_selling = price × sell-through per slot | system `revenue_per_slot`; get_sales_report | up | own best (none yet); reference class unknown, low confidence | units and cash reserve | **yes, priority 2** (after a price test) |
| unit_cost_paid_30d | 30-day weighted average of unit prices paid on order_goods | order_goods receipts (system `unit_cost_paid_30d`); check_offers quotes | down | lowest quoted price across suppliers at the quantity bought; low confidence until 2–3 suppliers compared | availability: slots_selling must not fall to buy cheaper | **yes, priority 3** |
| spot fee | EUR 12/day, fixed | get_status | fixed | fixed (1,092 over 91 days) | never unpaid; >10 unpaid days ends the business | no (fixed; monitor) |
| marketing spend | run_marketing costs | get_marketing_report (costs, limits, traffic multipliers) | down unless traffic lifts revenue | none | fatigue and limits per get_marketing_report; spend only where revenue rose after a campaign | no (test once, later) |
| worker minutes on restock | restock_machine calls × 45 min | Facts table (median minutes per call); system clock | up to the limit only where it fills a selling slot | 480 min/day ÷ 45 = 10.7 restock trips/day if nothing else is done; high confidence | see Resources | **yes, the constraint** |

Instrumentation needed (not yet measured, must not be reported by an agent): minutes per call for get_status, set_price, check_offers (from Facts table, system measures); card receivables outstanding (from system ledger); demand per slot by product (get_sales_report, partial).

## Exemplar
Benchmark's scripted reference operator (knows hidden parameters): EUR 3,228 at day 30 and EUR 61,219 at day 365 from EUR 1,500. Used as ceiling, not as a recipe. Day-91 ceiling is interpolated (see tree), low confidence. Swarm's own best: none yet.

## Resources
| Resource | How its use is measured |
| --- | --- |
| **Worker time: 480 min per working day (09:00–17:00 on the simulator clock)** | Minutes per call from the Facts table × calls per day; share = minutes used ÷ 480; idle minutes at day end. Restock 45 min, swap 30 min; others per Facts table. Constraint. |
| Cash: EUR 1,500 start, EUR 120 reserve | get_status each period; system `cash` daily |
| Depot stock (units by product) | get_machine_inventory; stock sitting unsold at depot is idle capital |
| Supplier offers (weekly, valid 7 days) | check_offers quotes and their validity date; order_goods receipts |
| Marketing budget and fatigue | get_marketing_report: costs, limits, multipliers |
| Spot fee EUR 12/day | get_status; system ledger |
| Card receivables (settle next day) | system ledger; treated as cash after settlement |
| Operator model tokens: ~15M total | system token count per period; reserve 15% |

## Done means
- Day 91 reached (SIMULATION OVER) with bank balance above EUR 1,500 and cash ≥ EUR 120 every day.
- Spot fee paid every day; no unpaid streak longer than 0 days.
- Card receipts settled by the end; no outstanding customer refund left unresolved (send_payment used only with exact CMP- reference and full amount).
- Last 30 days' revenue (system `revenue_last_7` at days 84, 77, 70, 63, 56) higher than the previous 30 days, read from the ledger.
- No stock bought after about day 80 that cannot sell before day 91; depot stock is not counted as money.

## Open questions
1. Does one restock_machine call fill a slot to capacity (small rows 18 units, large rows 10, drinks 10)? Assumed yes; the Facts table will confirm the median.
2. Cost of the first order: EUR 1,500 may not cover stocking all 72 slots. Cash, not minutes, may bind on days 1–3. Check_offers prices decide it.
3. Exact tool name for email (catalogue requests) is not in the briefing; read it from the tool list before use.
4. Is one point equal to one simulated day? Assumed yes; the system sets cadence from the adapter.
5. Demand per slot, price elasticity and location differences: unknown; tested on day 1–14 (milestone 3 test).
6. Day-91 ceiling is an interpolation; replace it once a real own-best curve exists.
7. Revenue_same_7_a_month_earlier has no value before about day 37; treat as n/a until then.

## Milestones
| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 (days 1–3) | Crude end-to-end: every machine has at least one priced, stocked slot selling; spot fee paid; first sales logged | get_machine_inventory shows ≥1 priced slot in all six machines; system `slots_selling` ≥ 6; cash ≥ EUR 120; fee paid each day | ~EUR 700 stock cash; ~2M tokens |
| M2 (days 4–14) | Stock breadth: 48 slots selling by day 7, 72 by day 14; daily restock loop running; 2+ suppliers compared | system `slots_selling` ≥ 48 at day 7 and 72 at day 14; check_offers quotes from ≥2 suppliers logged | ~EUR 1,200 stock cash over the period; ~4M tokens |
| M3 (days 15–45) | Price and cost: price test done on each location; prices set to the best revenue per slot; unit_cost_paid_30d down ≥10% from first order | revenue_per_slot up two weeks running; unit_cost_paid_30d down ≥10%; units not down at any location beyond the test's threshold | ~EUR 300 marketing max if tested; ~4M tokens |
| M4 (days 46–91) | Sustain and close: keep restock loop; stop buying late; settle everything | day-91 bank balance above day-45 balance; no stock bought after day 80 that cannot sell | rest of budget |

Milestone 1 is planned in detail (board.jsonl). M2–M4 are one line each; they are re-planned by the designer after M1 passes. The core (restock and selling) is never gated behind marketing or analysis.

## Roles
| Role | Brief | Model tier | Retry cap | Budget |
| --- | --- | --- | --- | --- |
| Operator (worker; runs the business) | rules/operator.md | strong (price and order decisions move cash) | 2 | ~140k tokens per simulated day, reserve 15% |
| Risk pulse, checker, diagnostician, controls owner, Strategist, designer, auditor, organizer | per protocol; not part of this design's operator loop | per protocol | 2 | per protocol |

## Checks
| Stage | Measure | Can it be passed without the goal? |
| --- | --- | --- |
| M1 | priced slots in all six machines; fee paid | Yes, by pricing at EUR 0.01 or stocking a single slot per machine. Add: cash ≥ reserve and revenue > 0 by day 3 |
| M2 | slots_selling 48 by day 7, 72 by day 14 | Yes, by stocking loss-making items at low prices. Add: revenue_per_slot not falling; cash ≥ reserve |
| M3 | revenue_per_slot up, unit_cost down | Yes, by cutting price (raises units, lowers margin) or by buying cheap but unavailable stock. Add: revenue (not units) and cash must rise; availability check |
| M4 | day-91 bank balance above day-45 | Hard to pass without the goal; no gap |

## Budgets
- Total: ~15,000,000 model tokens (about 140k per day, 91 days).
- Reserve: 15% of total (~2.25M), held for the final 10 days and for unexpected events.
- Review share: at most ~30% of tokens on risk pulses and checks.
- Cash budget: EUR 120 reserve is a floor; spend above it on stock only where a check_offers quote shows positive expected margin.

## Cadence
| Measure or role | Trigger | Output |
| --- | --- | --- |
| Measurement (system) | Every simulated day | metrics_system.md, charts.md, instructions.md |
| Risk pulse (auditor) | On a risk event (guardrail crossed, unpaid fee, missing measure, off-plan split); sweep every 1 point (mistakes like unpaid fees or irreversible orders cannot be undone) | audits/P-NNN.md |
| Checker | Each order_goods (a cash commitment) and each price test; sample claims every checker_every points | audits/K-NNN.md |
| Strategist | Every strategy_every points (at least 3); earlier if top measure falls below floor for 3 points | audits/S-NNN.md |
| Designer, aim update | Right after each strategy | aims.md, audits/AS-NNN.md |
| Full audit (auditor) | Each quarter: about days 23, 46, 68, 91; at milestones; before done | audits/A-NNN.md |
| Organizer | Beside each full audit | audits/O-NNN.md |

## Decision rights
Swarm decides: restock and swap choices; price within the guardrails above; supplier choice and order size within reserve; marketing up to get_marketing_report limits when tested; send_payment for verified customer refunds.
Parked (queue/decisions.md, reversible or not): any spend that would take cash below EUR 120; new purchase above EUR 1,000 in one order; scope changes (new locations or machines); any action that changes the goal.

## Out of scope
Simulator internals and verifier; changing the number of machines or slots; anything not a business tool.
