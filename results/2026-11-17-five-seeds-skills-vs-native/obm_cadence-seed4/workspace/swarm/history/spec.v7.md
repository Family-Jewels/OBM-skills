# Swarm spec: Prosus Vending Bench, 365-day operation   Version 7 (v6 in swarm/history/spec.v6.md; change in audits/R-P-034.md)

## Goal
Maximise the bank balance at the end of simulated day 365, starting from EUR 1,500, without going bankrupt or leaving more than 10 consecutive days unpaid. Unfinished or bankrupt runs score zero. Receiver: the business owner, who reads the final balance from the ledger. Inventory is not in the score; only cash is.

## Driver tree
Top measure is cash. Revenue, units and slots are diagnostic: they can rise while cash falls (below-cost sales, marketing that never pays back), so no check may pass on them alone.

| Measure | = made of | Ground-truth source | Better | Push on now? |
| --- | --- | --- | --- | --- |
| **Final cash (B365)** | 1,500 + Σ daily (revenue − cost of goods − spot fee − marketing − refunds), settled at the end | Bank ledger via get_status; card settlement lag of 1 day, outstanding card receipts settle at end | up | top |
| Revenue (per day) | slots_selling × revenue_per_slot | get_sales_report (sales ledger) | up, but only with margin | diagnostic |
| slots_selling | slots holding stock and a price, of 72 | get_machine_inventory | up | diagnostic. v7: not pushed on. Adding slots did not add revenue (R-P-024: slots +32%, revenue +6%); new slots only where the sales report shows a stock-out with demand (operator rules 4c, 5) |
| **Fills per day** (v6) | fills done that day; a day that stops with a sold-out slot still holding storage stock must have a logged reason | fill log in log/runs.jsonl; stop reason for any day that stops with such a slot open (operator rule 8) | up | **yes, now** (v6): the 5-trip cap is the operator's own budget (audits/A-003.md) and bound with stock waiting on days 157 to 170 (audits/D-P-024.md). The v5 "watch only" call rested on the day-125 test, which only held while storage bound |
| **Revenue per visit** (v7) | revenue on the day ÷ fills done that day (units per visit × price) | revenue from get_sales_report ÷ fill count in log/runs.jsonl (operator-computed until charted) | up, with margin | **yes, now** (v7): visits per day are the binding limit (audits/D-P-034.md). Each visit must sell more: prefer the fill that sells most units, and mix and price per slot. Judged on this, not on slot count |
| **Sold-out selling slots** (v4) | slot-days where a slot with a product and price holds 0 units at end of day | get_machine_inventory, daily (operator-computed until charted) | down | **yes, now**: the cost of a stock-out, which the sales report hides |
| **Storage per sold-out slot** (v4) | units in storage for each sold-out slot, at the day's start | storage count from get_machine_inventory (operator-computed until charted) | up to the trips needed | **yes, now** (v5): a sold-out slot with no storage stock is a supply cause; cover is set by Done means 7 |
| **Order-to-shelf lead time** (v4) | days from order to landing, per supplier (landing day − order day); effective lead time = quoted days + 1 landing day | runs.jsonl order, due and landing days (operator logs each order from day 109) | down | **yes, now** (v5): sets the cover in Done means 7. Quoted 4, effective 5 (PO-1037 to PO-1046 landed 1 day late on 11 of 11) |
| revenue_per_slot | units per selling slot × price | revenue ÷ slots_selling (system) | up | yes, via price and mix |
| Units sold | Σ over locations and products of footfall × share captured × in-stock fraction | get_sales_report by location and product | up, with margin | yes, via mix and availability |
| Share captured (per product) | preference fit (savoury snacks, coffee) × price response | get_sales_report by product and price history | up | yes, via assortment and price tests |
| Footfall per location | base footfall × marketing multiplier × season/weather | get_marketing_report (multipliers); sales report | up | later, only after payback test |
| Gross margin per unit | price − unit cost paid | price from set_price log; unit cost from order_goods receipts | up | **yes, now** (no sale below cost) |
| Cost of goods | Σ units bought × actual unit price | order receipts (actual cost after payment) | down | yes: supplier choice, quantity, timing against weekly offers |
| Spot fee | EUR 12 per day, fixed | ledger | fixed | no |
| Marketing spend | per campaign cost | get_marketing_report | down unless cash_gain_7 covers it | later |
| Cash float | cash − reserve | ledger | up | yes: keep above reserve |
| cash_gain_7 | cash(t) − cash(t−7) | ledger (system-charted) | up | the weekly check |
| **Check-3 value (v3)** | cash(t) − cash(t−7) + Δ stock at cost | ledger + order receipts (operator-computed until charted); stock at unit cost, counted only if sold or bought within the last 14 days (older unsold stock counted at 0) | up | the weekly check (replaces cash_gain_7 in check 3 only) |
| revenue_last_7 vs revenue_same_7_a_month_earlier | trend, seasonality-adjusted | system | up | diagnostic |

**Needs instrumentation (not charted by the system today):** gross margin per unit by product; marketing spend by location and campaign; COGS per day. Until charted, the operator computes them from ledger and order receipts and writes them into log/progress.md, marked as operator-computed. Request the system to chart them as soon as it can.

## Exemplar
Scripted reference operator (benchmark), which knows the hidden economy parameters: EUR 3,228 at day 30, EUR 61,219 at day 365, from EUR 1,500. Source: benchmark reference run, given in the brief.

Pace checkpoints (my geometric interpolation between the two known points, not exemplar data; the exemplar's own intermediate values are unknown):

| Day | Target cash (at least) |
| --- | --- |
| 30 | 3,228 (exemplar) |
| 90 | ~5,470 |
| 180 | ~12,000 |
| 270 | ~26,500 |
| 365 | 61,219 (exemplar) |

Gap to exemplar (PIP) = exemplar cash ÷ swarm cash at the same day. Read it at every pulse. Aims rise once reached; none is a ceiling. Beating the path is the goal, not a failure.

## Done means
1. **Final**: at the end of day 365, the ledger cash is read and recorded; no day in the run had more than 10 consecutive unpaid days; all card receipts are settled. Passing criteria: final cash ≥ 61,219 (exemplar); any value above is better.
2. **Every period**: cash ≥ reserve (see Budgets). Could be passed by hoarding cash and never stocking, so it is only a floor; the real check is 3 and 4.
3. **Every 7 days**: check-3 value (cash_gain_7 plus Δ stock at cost, with the 14-day rule in the driver tree) ≥ the checkpoint pace for that day (table above, linear in 7-day steps). Read from the ledger and order receipts, not from revenue. Restocking is not a loss on this check; unsold stock older than 14 days earns nothing on it. Check 2 still reads cash alone, and check 4 still requires cash_gain_7 (cash only) to be positive.
4. **Every 7 days**: revenue_last_7 ≥ revenue_same_7_a_month_earlier, and cash_gain_7 positive. Growth bought with a loss-making price or marketing that did not pay back fails here.
5. **Every price change**: new price ≥ unit cost of that product plus its share of the spot fee; not below cost in any slot.
6. **No stock-outs left unexplained**: each slot with zero stock for 2+ days has a logged reason (no demand, no supply, or price).
7. **Every order (v5)**: units ordered for each selling line ≥ (effective lead time + 1 day) × that line's sell-through per day, where effective lead time = quoted days + 1 landing day (5 + 1 = 6 days at present). Read from check_offers, the sales report and runs.jsonl. Overstock can pass it, so checks 2 to 4 and the weekly cap bound it.

Must not change on the way: no tool misuse, no simulator or verifier access, no real-message channels, no action outside the business tools.

## Open questions
- Price response per product per location (AI-LOUNGE most price sensitive; AI-HOUSE least; MAIN-LOUNGE high footfall). Answer with price tests, read from the sales report.
- Whether demand is shared across duplicate slots (it is, per the briefing): extra slots add capacity, not customers. Test before buying duplicates.
- Whether the A/B small-product rows (18 units) or C/D large-product rows (10 units) cap sales per visit more than demand does.
- Actual supplier prices and whether weekly offers beat a fixed supplier.
- Marketing: whether any campaign pays back within 14 days at the current traffic multiplier.
- (v4) Does the 5-trip cap bind? Days 110 to 156: no, storage bound (audits/R-P-020.md). Days 157 to 170: yes, five fills a day with sold-out slots and stock waiting (audits/D-P-024.md). Open for the designer's next check: whether the 8-hour day is enforced by the tools or is the operator's own; the day-117 to 125 test showed the tools allowed a sixth fill.
- (v6) Is the 8-hour day a business rule or a self-set budget? Test: log each day's reads and price changes against the hours. Unanswered; the change below does not depend on it.
- (v6) cash_gain_7 IMPROVEMENT signal (charts.md, 8 points above centre) is not yet explained. Attribute it from ledger reads before the next redesign.
- (v4) The diagnosis reads "6 to 10 of 72 slots still empty" while slots_selling is 8–10. The system must state which slots the empty count covers before sold-out slot-days is charted.
- (v4) The chart's exemplar series is a straight line between day 30 and day 365 (its day-103 value is 15,865), not exemplar data. PIP on the charts is therefore an interpolated gap; read it as indicative until the exemplar has a measured path.

## Milestones
| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 (days 0–30) | Crude end-to-end operation: all six machines stocked, priced and selling, reading the ledger each day, paying the fee, reaching the day-30 target | cash ≥ 3,228 on day 30, no unpaid days, every slot with stock has a price ≥ its cost | ~8% of starting cash in stock per week, rest is working float |
| M2 (days 31–90) | Mix and price tuned per location; supplier cost lowered; first marketing payback test | cash ≥ ~5,470 on day 90; cash_gain_7 at checkpoint pace in the last 4 weeks | as above |
| M3 (days 91–180) | Sustained restock cadence on every selling slot; marketing only where payback proven | cash ≥ ~12,000 on day 180 | as above |
| M4 (days 181–270) | Scale: fill unused capacity where the sales report shows demand; hold margin | cash ≥ ~26,500 on day 270 | as above |
| M5 (days 271–365) | Harvest and close: stop buying stock that cannot sell by day 365, settle cards, final balance | final cash ≥ 61,219 | remaining cash above reserve |

M1 is planned in detail on the board. M2–M5 are one line each; the designer plans each when the previous one passes. Nothing in M1 waits on any supporting work.

## Roles
| Role | Brief | Model tier | Retry cap | Budget |
| --- | --- | --- | --- | --- |
| Operator (orchestrator and worker in one) | swarm/rules/operator.md | strong | 2 per order decision | the day's time and cash budget (see Budgets) |
| Checker (sampled) | swarm/rules/checker.md | strong | n/a | ≤ 30% of decisions reviewed |
| Auditor (pulse and full) | swarm/rules/auditor.md | strong | n/a | per cadence |
| Diagnostician (on request) | swarm/rules/diagnostician.md | strong | n/a | per diagnosis |

Single-agent mode applies (protocol section 9): the operator plays each role in turn, writing each record before switching. The checker never checks its own orders in the same context that placed them where feasible; otherwise the operator checks the ledger arithmetic itself and logs that it did.

## Checks
| Stage | Measure | Can it be passed without the goal? |
| --- | --- | --- |
| Each period | cash ≥ reserve | Yes, by never stocking. So it is a floor, not a pass. |
| Each 7 days | check-3 value (cash + stock at cost, 14-day rule) on checkpoint pace | Partly: stock can be bought and counted. Blocked by the 14-day rule and check 6, and by check 4 needing cash_gain_7 positive. |
| Each 7 days | revenue_last_7 vs same 7 days a month earlier, with cash_gain_7 positive | Revenue alone: yes via loss-making sales. Hence the pairing. |
| Each price change | price ≥ cost | Units can rise with price cuts; this blocks the cut. |
| Each order | spend ≤ weekly cap and cost per unit vs last offer | Cheapest supplier with unsellable stock: blocked by the sell-through check (below). |
| Each product line, after 14 days | units sold per slot per day vs stock on hand | Restocking a product that does not sell: caught here. |
| Each order (v5) | units ordered per selling line ≥ (effective lead time + 1) × daily sell-through | Overstock passes it; checks 2–4 and the weekly cap bound it. |

## Budgets
- **Cash reserve**: max(EUR 300, 15% of bank balance). Never spend below it. It covers the spot fee and card lag.
- **Weekly order cap**: 60% of cash above reserve per 7 days, so 40% stays for the rest of the week.
- **Per-order**: a single order above EUR 1,500 or above 30% of free cash is parked (see decision rights).
- **Marketing**: at most one campaign per location per 14 days, and only after its previous campaign's payback was read. Spend ≤ 5% of cash per campaign.
- **Time**: 8 working hours. Each fill is 45 min, each swap 30 min, each location read about 25 min (operator's own estimate from the log: three reads took about 75 min; to be verified by logging read times, v7). Reads and price changes come first and must be done each day. Fills then continue while a sold-out slot with storage stock is open, until the day's reads and price changes are done or the 8 hours run out. The flat 5-trip cap is retired (v6, audits/R-P-024.md). The day-117 to 125 test showed the tools allow a sixth fill, so the cap was never a tool limit.
- **Review share**: ≤ 30% of decisions. Full checks on orders above EUR 500 and on every price below the day's median price.
- **Model spend**: strong tier for all roles; the operator makes one decision per block, not per call.
- **Reserve on the budget itself**: keep about 15% unallocated across the run.

## Cadence
| Measure or role | Trigger | Output |
| --- | --- | --- |
| Measurement (system) | Every simulated day | swarm/metrics_system.md, swarm/charts.md |
| Operator: status read | Start of each day | log/progress.md line: cash, reserve, slots_selling, orders due |
| Operator: weekly offers | Every 7 days, on the validity date | check_offers and order decision, logged in runs.jsonl |
| Operator: restock and price review | Each day with a signal or a sales report change | fill/price actions, logged |
| Fills, sold-out slots, storage, lead time (v4) | Every simulated day, from day 109 (operator-computed until the system charts them) | charts.md rows once charted; until then log/progress.md |
| Checker | Each order above EUR 500 and each price change below the median; otherwise sampled | review record (4.3) |
| Auditor, pulse | Every 5 simulated days | audits/P-NNN.md |
| Auditor, full audit | Every 50 days (50, 100, …, 350), at milestones (30, 90, 180, 270, 365), and immediately when cash_gain_7 or revenue shows a signal in the wrong direction | audits/A-NNN.md |
| Diagnostician | When a pulse or audit ends "Diagnosis needed: yes" | audits/D-NNN.md |
| Designer, redesign | After a diagnosis, or a full audit finds direction wrong; at least 20 days after the previous redesign | audits/R-NNN.md, spec and rule versions |

## Decision rights
- **Swarm (operator) decides**: which products to stock in which slot; prices within the margin rule; which supplier to buy from among those quoted; restock quantities within the budgets above; refunds under EUR 20 per the payment rules; slot-level stock adjustments; timing of weekly orders.
- **Parked (decision request, D-NNN in queue/decisions.md, default first, work continues)**: any single order above EUR 1,500 or above 30% of free cash; any product sold below cost; any multi-week supplier commitment; marketing above the budget limits; any action that cannot be reversed; any change to the goal, to checks, or to the budgets (designer only).

## Out of scope
- Anything beyond the business tools; no access to the verifier or simulator internals.
- Real messages: marketing channels log copy only, and suppliers are contacted only for catalogues and terms.
- Changing the goal, the exemplar, or the day-365 end date.
