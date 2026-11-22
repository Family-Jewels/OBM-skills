# Swarm spec: Prosus Vending Bench, 365 simulated days   Version 11 (changes: audits/R-P-028.md; prior version history/spec.v10.md)

## Goal
Maximise the bank balance at the end of day 365, starting from EUR 1,500, by running six vending machines (SNACK and DRINKS at AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE). Receiver: the human who owns the network. Unfinished or bankrupt scores zero; more than 10 consecutive unpaid days ends the business. Never lower this goal.

Identity of the top measure: final bank balance = 1,500 + sum over days of (revenue − unit cost paid − spot fee €12/day − marketing − refunds − other spend). Cash in the bank is the measure the system charts as `cash`.

## Driver tree
Each part is read by the system from ground truth. Ceiling confidence: H/M/L.

| Measure | = made of | Ground-truth source | Better | Ceiling (source, confidence) | Guardrail | Push on now? |
| --- | --- | --- | --- | --- | --- | --- |
| **Final bank balance (cash)** | 1,500 + Σ(revenue − unit cost − spot fee − marketing − refunds − other) | get_status cash; ledger | up | 61,219 at day 365 (benchmark scripted reference, M: it knows hidden parameters, so a real ceiling is not proven) | cash ≥ EUR 120 every close | top measure, judged by the system |
| Revenue | units × average net price | get_sales_report; `revenue` | up | Exemplar revenue pace; no own best yet (own best) | none | via drivers below |
| Units sold | slots selling × units per selling slot-day | get_sales_report; `units` | up | Demand ceiling not known (reference class: exemplar) | never sell below unit cost | via drivers below |
| **Slots selling (capacity in use)** | slots stocked, priced and not empty, out of 72 | get_machine_inventory at close; `slots_selling` | up | 72 slots (resource ceiling, H) | none | **Yes, priority 1** |
| **Stocked slots with no price, at close** | count of slots holding stock with no set price | get_machine_inventory at close (system to chart; until then the operator logs the tool's count in the daily line) | down, to 0 | 0 (a stocked unpriced slot sells nothing, H) | never a set_price cut on a stocked slot to free minutes | **Yes, priority 1 (process, R-P-019)** |
| **Depot cover (days of stock ahead of fills)** | depot units by product ÷ units the next 5 days of fills need | simulator depot state (needs instrumentation: the system to chart it; until then the operator reads get_storage_inventory before each fill and logs it in the daily line) | up, to the planning target | planning target = planning lead time + 5 days of fills. Planning lead time = the longest of the last three receipts from the supplier ordered from, not less than 3 days (R-P-007: receipts of 10 and 13 days, so the target is 15–18 days, not 5) (M). **Until receipts per supplier are charted (open question 11): planning lead time 13 days for every supplier, so the planning target and the order trigger are 18 days of cover. The number is the trigger, not 5 days** (R-P-011) (M) | no order above 40% of cash; no order above the best quote | **Yes, priority 1 (leading measure for slots selling)** |
| Orders arriving before cover runs out | count of orders whose delivery day is on or before the day that product's cover runs out; read from receipts and the depot count | supplier receipts; get_storage_inventory (checked by the system) | up, to every order | every order (designer rule, R-P-007: an order that lands after the stock is gone has not done its job, H) | cash ≥ 120 after each order | Yes, priority 1 (process) |
| Orders placed per working day | count of orders placed by 10:00 for each product whose cover is under the planning target, from the order log | progress.md order lines; supplier receipts (checked by the system) | up to one order placed each working day for each such product | one per product per day (designer rule, M) | cash ≥ 120 after each order | Yes, priority 1 (process) |
| Worker fills per day | 480 min ÷ (45 min per fill + other calls); fills run until 16:30 while an empty slot has its product in the depot | get_status clock; work.jsonl minutes | up, to the time left after reads and pricing | about 10 fills per day with nothing else (resource ceiling, H) | fills never cut below the pricing and order minimum; a fill is made only when the depot holds the product | Yes, after depot cover is in hand |
| Minutes per restock call; slots restocked per call | minutes of each restock_machine call (work.jsonl) and slots filled by that call (restock receipt) | work.jsonl; restock receipts (system to chart both; until then the operator logs them in the daily line) | minutes per slot down; slots per call up | Measured: one slot per call, 45 min per call (daily lines, days 285–286; open questions 1 and 3 closed). Batching is not available; this is a fixed cost of the fill (H) | a call is made only for slots whose product is in the depot | Measured; watch, not pushed directly |
| Units per fill | units restocked per fill, weighted to fastest sellers; the fill's output per minute | restock receipts; sales report | up | Machine capacity: 18 units small rows, 10 units large rows and drinks (resource ceiling, H) | fill only products with a set price | **Yes, priority 1 (the lever on output per minute: fill the 18-unit rows first; R-A-002)** |
| Revenue per slot | revenue ÷ slots selling (daily) | `revenue_per_slot` | up | Exemplar-implied pace (benchmark, M) | none | Yes, follows priority 1–2 |
| Units per selling slot-day | demand by location and product, after stock-outs | get_sales_report by location | up | Own best, to be set after day 30 (own best, L) | none | Watch, not pushed directly |
| Average net price | set price − unit cost, sold-weighted | set_price log; sales report | up, but not at the cost of units | Reference class: price response read from sales report (L) | price ≥ unit cost + minimum margin; AI-LOUNGE is price-sensitive | Yes, after day 14, once price response is read |
| **Unit cost paid, 30 days (cost driver)** | cost paid per unit, from order receipts | `unit_cost_paid_30d`; order receipts; per-order quote logged (paid and best check_offers quote) | down | Lowest quote seen at the same quantity (own best, M) | never pay more than the best check_offers quote in the same week | Yes, priority 3 |
| Idle capital | cash above EUR 240 with no order open | `capital` row in charts.md | down | 0 (spec budget rule) | cash ≥ 120 | Yes, priority 1 (process) while a product is under target; otherwise a watch (R-P-019: idle cash with covers at target is held, because fill minutes bind) |
| Spot fee | fixed €12/day | ledger | — | fixed | must be paid each day | not controllable |
| Marketing spend | per campaign cost | get_marketing_report | down unless traffic gain pays back | — | fatigue limit from get_marketing_report | Not until day 30 |
| Refunds and complaints | refund amounts; open complaints | ledger; complaints | down | 0 | open complaints lower reputation | Watch |

Seasonality check: `revenue_last_7` against `revenue_same_7_a_month_earlier` (both system-measured). Read it, do not act on it alone.

Counts are read from the tools' output, never from the operator's memory or notes. The daily count in charts.md is the count the system uses.

## Exemplar
Benchmark scripted reference operator (knows hidden parameters): about EUR 3,228 at day 30 and EUR 61,219 at day 365 from EUR 1,500. Implied growth: about 7.7% per day to day 30, then about 0.9% per day on average to day 365. Source: system brief. Gap to the exemplar (PIP) is computed by the system.

## Resources
| Resource | How its use is measured |
| --- | --- |
| **Worker time (480 min per working day, 09:00–17:00)** | Minutes per day used by each tool call, read from the simulator clock: refill 45, swap 30, price or read calls a few minutes each. Share by activity (section Time split in aims.md). This is the binding constraint. A failed fill counts as a full fill. |
| Machine slots (72: 6 machines × SNACK/DRINKS slots) | slots_selling ÷ 72; idle slots = empty or unpriced |
| Capital | Cash in bank (cash), capital in stock (depot plus in slots), idle cash above the reserve |
| **Supplier lead time** | Days from order_goods to delivery, read from receipts. Observed: 3 days (PO-1003), 4 (PO-1004), 5 (PO-1001, PO-1002); PO-1005 took 14 (late). Recent: PO-1052 took 13 days and PO-1060 took 10 (audits/D-P-007.md), against the 3–5 assumed above. Stock cannot be filled before its delivery day, so orders are planned a planning lead time ahead of the fills they enable (driver tree, depot cover). |
| Supplier credit and card settlement | Card receipts settle a day later; outstanding card receipts settle at end |
| Marketing budget | Spend per location per week against get_marketing_report limits |

## Done means
- Day 365 reached (SIMULATION OVER) with bank balance as large as possible.
- Cash at every daily close ≥ EUR 120, and spot fee paid every day (zero unpaid days).
- Each order's unit cost ≤ the best check_offers quote for the same quantity and week.
- No price set below unit cost; no slot left unpriced while it holds stock.
- Revenue for the last 30 days exceeds the previous 30 (read from the sales report).

## Open questions
1. Closed (R-A-002): restock_machine's cost is 45 minutes per slot, one slot per call (progress.md, days 285–286; work.jsonl days 7–19).
2. Travel between locations: does moving between machines cost minutes beyond the tool calls? Read from the clock.
3. Closed (R-A-002): a restock fills a slot to its machine maximum (18 units small rows, 10 large rows and drinks), per the receipts logged on days 285–286.
4. Price response by location (AI-LOUNGE most price-sensitive) is not known; read it from get_sales_report during normal operation. No designed experiments.
5. Supplier reliability (delays, short-shipping, failure) is not known beyond the lead times above. Track it from receipts against orders; do not assume it. Open: lead times rose from 3–5 days to 10–13 days after day 79 (PO-1052, PO-1060). Whether this is a supplier change or random is not settled; receipts from PO-1062 onward settle it (audits/D-P-007.md). Until then the planning lead time follows the latest receipts, so the design does not depend on the answer.
6. Whether the system's point and horizon match: the design assumes one point = 7 days (the weekly offer cycle), so about 52 points. The system derives the actual window.
7. Minutes conflict (audits/D-P-001.md): settled by the simulator clock in charts.md. The current charts show worker time 440 of 480 min (median, last 7 days), not the 290 used in the diagnosis D-P-003 (days 25–35). The charts are used.
8. Count conflict: the operator's daily lines (days 25–35) report 45–55 slots stocked; the system's count at day 37 is 27 stocked, 22 selling. The system's count is used. The system to reconcile the depot and slot counts against its own state (D-P-003 item 7).
9. Depot cover needs instrumentation: the system does not yet chart depot units by product. Requested in R-P-003 and again in R-P-004; until it does, the operator logs the get_storage_inventory read in the daily line.
10. Supplier minimums (Zuidas EUR 75, Noordzee EUR 90): are small orders caused by these minimums or by sizing? The order log (size, supplier minimum, reason for any higher quote) settles it; read it at the next pulse.
11. Supplier lead time per order and depot cover per product are not yet charted by the system (requested in D-P-007 items 1 and 2). The system is asked to chart both; the operator logs them in the daily line until it does. Closing 1, 3 and 5 is for the next pulse, from receipts.
12. (R-P-013) Fill minutes per restock call, slots restocked per call, and fills per working day are not charted; they are read from work.jsonl and receipts until the system charts them. Requested: the system to chart these three, and idle capital against depot cover. Closing 1 and 3 is the first test in aims.md point 26.
13. (R-P-019) Is the constraint fill minutes or stock? Daily lines for days 250–253 record depot covers at or near the 18-day target while 25 slots sat empty, which points to minutes, not orders (D-P-019's order hypothesis is not supported by those lines). work.jsonl fill times and the last-fill clock per day settle it. Requested again: the system to chart depot cover per product and stocked-unpriced slots (items 9, 11, 12).
14. (D-P-028) Stocked-but-unpriced slots (item 9's count, charted or logged) and minutes by activity per day are not in the system's charts, and work.jsonl has no entries after day 19, so the diagnosis could not settle whether fill minutes go to unpriced slots. Requested: the system to chart the stocked-unpriced count at each close and minutes by activity from the clock. Until then the operator logs both in the daily line and work.jsonl (rules 14, 21).
15. (D-P-028) charts.md gives the point-44 cash floor as 33,812 and aims.md (point 44) gave 31,393. Aims now use the charts figure. The system is asked to reconcile its floor line with the aim file's source.
No instrumentation gap otherwise: all top-level measures are in the system's daily list.

## Milestones
| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 | Crude end-to-end: all six machines stocked and priced with the best available products, first sales read, cash above reserve every close | Done (day 14 target, carried from day 7). Missed at day 14 on lead time; now complete per the record. | Initial cash minus the reserve; M1 uses no more than EUR 800 of stock in the first two weeks |
| M2 | Full coverage: slots_selling ≥ 60 and refill loop running at ~10 fills per day | By day 30: slots_selling ≥ 60 on 5 of the last 7 days; revenue_last_7 rising for 3 points. OVERDUE: not met at day 37 (22 selling). Target not lowered. Interim stepping stones: aims.md point 6 (≥ 30 by day 42) and point 7. | Ongoing stock spend within cash minus reserve |
| M3 | Price and mix tuned from read sales data | By day 90: average net price up without units dropping below the prior 30-day level | Within the time split |
| M4 | Marketing used only where traffic pays back | By day 182: each campaign's cost recovered by sales within 14 days, or none run | Marketing ≤ 5% of worker time and ≤ 5% of revenue |
| M5 | Run to day 365 with the loop steady | Full audit at day 273 and day 365 passes | — |

## Roles
The operator is the only worker and does every role in turn (protocol section 9): orchestrator, checker of its own records by the system, and diagnostician by the system's audits. The system invokes each role at the cadence below.

| Role | Brief | Model tier | Retry cap | Budget |
| --- | --- | --- | --- | --- |
| Operator (worker and orchestrator) | rules/operator.md (v13) | strong | 2 per action | Worker time 480 min per day |
| Designer | this spec | strong | — | As the system allows |
| Strategist | obm-swarm-strategist skill | strong | — | As the system allows |

## Checks
| Stage | Measure | Can it be passed without the goal? |
| --- | --- | --- |
| M1 | slots_selling ≥ 36 by day 7 | Yes: slots can be filled with low-margin or slow products. Add: revenue_per_slot must be rising by day 14 |
| Each day | cash ≥ 120 at close | No: this is direct |
| Each day | cash above 240 with no order open, and a product under the planning target with no order placed | Yes: cash can sit idle while the day's other work is done. Add: a working day with idle cash, a product under target and no order placed counts as missed in the pulse; two such misses in one point make the next pulse say Diagnosis needed: yes (R-P-011, reworded R-P-013). Cash above 240 with every product at or above target is not a miss: stock beyond target waits on fill minutes, the constraint |
| Each working day | fills run until 16:30 while an empty slot has its product in the depot (the reserve for runs past 16:30 is 8 min) | Yes: a day can end early with the work undone. Add: a working day whose last fill is before 16:30 with such a slot still empty counts as missed in the pulse; two such misses in one point make the next pulse say Diagnosis needed: yes (R-P-013) |
| Each order | unit cost ≤ lowest quote from any supplier for that product, same week; the order's quote, the lowest quote and its supplier logged. A higher quote is taken only when the lowest supplier's minimum order is not met, with the minimum and the combined order logged | Yes: the operator could buy the cheapest quote and sell nothing. Add: slots_selling must not fall after the order |
| Each working day | an order placed by 10:00 for every product whose depot cover is under the planning target (18 days until receipts are charted; see driver tree), and sized so cover after delivery is at or above the target (read from the depot count) | Yes: an order placed late, or small, still counts as an order. Add: a day with no order by 10:00 and cover under the target counts as missed in the pulse; an order that leaves cover below target after delivery counts as undersized; two such misses in one point make the next pulse say Diagnosis needed: yes (R-P-019) |
| Each week | one check_offers per product per week, at the week's first order step; every order that week uses that quote, logged with its check day | Yes: the operator could skip checks and buy on a stale quote. Add: an order whose quote is from an earlier week counts as unchecked in the pulse; quote-check minutes averaged over a point are at most 5 a day (work.jsonl) |
| Each order | delivery day on or before the day that product's cover runs out (cover before the order ÷ fills per day); a later delivery counts as missed. Read from receipts and the depot count | No: an order that lands after the stock is gone does not restock the slot, so this is direct. This replaces the placement-only pass that let PO-1052 (13 days) count as done |
| Each day | slots empty for lack of stock (count) | Yes: a slot can be empty while the other work is done. Add: the count is logged each day; any day with a slot empty for lack of stock while its product's cover is zero is missed in the pulse |
| Each fill | depot holds the product (get_storage_inventory read first) | No: a fill with no stock is a lost 45 min, so this is direct |
| Each fill visit | every stocked slot at the machine has a set price before the operator leaves it (get_machine_inventory read after the fill; unpriced ones priced in the same visit) | No: a stocked unpriced slot sells nothing, so this is direct (D-P-028). Add: the stocked-unpriced count is logged at each close; a close with any count above 0 is missed in the pulse |
| Each day | work.jsonl has the day's minutes by activity (rule 21) | No: this is the record the time split is judged on (D-P-028). Missing lines count as missed in the pulse |
| Each price change | price ≥ unit cost + minimum margin | Yes: a price could be correct but still zero units. Add: units must not fall more than 30% after a price rise |
| Day 365 | bank balance | Direct |

## Budgets
- Total: the full business cash at start (EUR 1,500) minus the reserve. Reserve: EUR 120 hard floor, with a working reserve of EUR 120 more before any order that uses more than 40% of cash.
- Idle capital: cash above EUR 240 with no order open may be committed to stock, in one or more orders each within the best quote, each under 40% of cash. Capital is not to sit idle while slots are short; the daily order step (operator rule 17) is how it is committed.
- Review share: the system's pulses and audits only. The operator does not review its own records.
- Marketing: no spend before day 30.

## Cadence
| Measure or role | Trigger | Output |
| --- | --- | --- |
| Measurement (system) | Every day | metrics_system.md, charts.md |
| Operator daily loop | Each working day: read board.jsonl and status, order step, fill and price, log the day, then wait_for_next_day. A day with no log line counts as missed in the pulse | log/progress.md, log/runs.jsonl, log/work.jsonl |
| Pulse review (auditor) | Every point (7 days) | audits/P-NNN.md |
| Full audit (auditor) | Quarter ends: about day 91, 182, 273, 365; milestones; before done | audits/A-NNN.md |
| Strategist | After points 3, 6, 9, …; brought forward after at least 2 points when the top measure is below its floor 3 points in a row, or celeration is flat or wrong-way | audits/S-NNN.md |
| Designer, aim update | Right after each Strategist redirect | aims.md, audits/AS-NNN.md |
| Diagnostician | When a pulse or audit says Diagnosis needed: yes | audits/D-NNN.md |
| Designer, redesign | After a diagnosis, or an aim update that needs a design change; at least 3 points after the last adopted change | audits/R-NNN.md, spec/rules versions |

## Decision rights
Swarm decides: which products go into which slot, prices (above unit cost), order quantities within the reserve, supplier choice among quotes, marketing within the limit above, the order of fills and swaps within the time split.
Parked (log in queue/decisions.md, continue with the default): any single order above 40% of cash; changing the supplier that just failed to deliver; any action that cannot be reversed (clear_slot of stock that could be sold); refunds beyond the stated complaint; any complaint balance above the verified slot price (open: D-001 to D-006).

## Out of scope
Tool-surface access beyond the business tools; the simulator's internals and verifier; new locations; anything outside the six machines.
