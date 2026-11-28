# Swarm spec: Prosus Vending Bench, 91 simulated days   Version 2

## Goal
Maximise the bank balance at the end of day 91, starting from EUR 1,500, across three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with one SNACK and one DRINKS machine. Receiver: the human owner of the business. Cash must stay at or above the EUR 120 reserve throughout, and the business must never go more than 10 consecutive days with the EUR 12/day spot fee unpaid.

Run shape: single-agent mode (protocol section 9). The operator plays the worker; the system invokes the risk and improvement roles at the cadence in section "Cadence".

## Driver tree
Top measure first. "Push on now?" marks the drivers the operator works on in milestone 1.

| Measure | = made of | Ground-truth source | Better | Ceiling (source, confidence) | Guardrail | Push on now? |
| --- | --- | --- | --- | --- | --- | --- |
| **Final bank balance, day 91** | 1,500 + cumulative net operating profit | Bank ledger via get_status (cash, card receipts settled) | up | About EUR 5,500 at day 91: log-interpolated between the exemplar's EUR 3,228 (day 30) and EUR 61,219 (day 365). Source: exemplar. Confidence low (the curve shape between the two points is unknown) | Cash >= EUR 120 every day; spot fee paid daily | top |
| Cumulative net operating profit | revenue − unit cost paid − spot fee (EUR 12/day) − marketing − customer refunds | Ledger and get_sales_report, per day | up | As above | No loss-making restock (unit cost above selling price) | yes, via the drivers below |
| Revenue per day (cash + card) | units sold × average selling price | get_sales_report, daily `revenue` and `units` | up | Own best (none yet). Exemplar average over days 0–30 is about EUR 58/day, a reference only. Confidence low | As above | yes |
| Units sold per day | slots_selling × units per selling slot per day (demand) | get_sales_report `units` | up | Demand-limited: duplicate slots share demand, so extra slots add capacity, not customers. Confidence low | No stock-outs left unfilled when the depot holds stock | yes (through slots_selling and price) |
| slots_selling | count of slots with stock and a price, of 72 | get_machine_inventory, daily `slots_selling` | up | 72 physical slots (high confidence). Economic ceiling is lower, set by demand | Stock sold within the period: no slot filled with more than it can sell | yes, first |
| revenue_per_slot | revenue ÷ slots_selling | Derived from the daily measures | up | Own best (none yet); no external figure. Confidence low | Price response: units must not collapse when price rises | yes, through product mix and price |
| Average selling price and margin per unit | (price − unit cost paid) per unit sold | get_sales_report price field and receipts. **Needs instrumentation:** average price per unit is not in the daily measure list; request it be charted | up | No exemplar. Confidence low | Margin > 0 on every product stocked | yes, through set_price |
| unit_cost_paid_30d | unit cost paid over the last 30 days, from order receipts | order_goods receipts; check_offers at equal quantity | down | Cheapest current offer at the same quantity (own best, from check_offers). Confidence medium | Never order below cash reserve; never order more than the planned sale window | yes, through order choice |
| Productive worker minutes per day | fills × 45 + swaps × 30 + other actions (per Facts table) | System clock (get_status) and Facts table | up to 480 | 480 minutes per working day, 09:00–17:00 (clock, high confidence). Fills are the binding use: about 10 fills a day at most | Do not end the day with minutes unused while a slot is empty and stock is in the depot | yes, capacity |
| Spot fee | EUR 12 per day, network | Ledger | down | Fixed: EUR 1,092 over 91 days (high confidence). Not a driver | Unpaid for more than 10 consecutive days ends the business | no (fixed) |
| Marketing spend and traffic | campaign cost vs incremental revenue in the next 7 days | get_marketing_report (cost, limits, multipliers); sales report | up (revenue per EUR spent) | No exemplar. Confidence low | Fatigue limits in get_marketing_report; no campaign that cannot pay back before day 91 | later (milestone 3, after a clean price read) |
| Revenue last 7 vs same 7 days a month earlier | seasonality and trend check | System-computed measures `revenue_last_7`, `revenue_same_7_a_month_earlier` | up | n/a (a check, not a driver) | n/a | observe only; baseline from day 30 |
| Customer complaints open | count of open complaints | get_status / ledger | down to 0 | 0 (high confidence) | Reputation falls with open complaints | observe |

Measures the system already records (daily): cash, revenue, units, slots_selling, revenue_per_slot, revenue_last_7, revenue_same_7_a_month_earlier, unit_cost_paid_30d. Average price per unit and worker minutes per day are not in that list; both are marked for instrumentation: they come from the sales report and the clock, never from the operator's own count.

Why this order: the operator controls slots (through worker minutes and depot stock) and price directly. Demand is not controlled and is read, not pushed. Early on, the binding constraint is the worker's fill throughput, so the top priority is getting stock into sellable slots each day, with a positive margin on each product.

## Exemplar
Benchmark's scripted reference operator (knows the hidden economy parameters): about EUR 3,228 at day 30 and EUR 61,219 at day 365, from EUR 1,500. Source: the benchmark brief. The reference's day-91 value is not given; the figure in the driver tree is a log-interpolation and is a reference only, with low confidence. Use it to judge direction and pace, not as a target that caps the swarm. Own best: none yet; the first measured baseline becomes the own-best line.

## Resources
| Resource | How its use is measured |
| --- | --- |
| **Worker time (binding)** | 480 minutes per working day, read from the simulator clock (get_status) at the start and end of each action. Per action from the Facts table: restock_machine 45 min, swap_item 30 min, all other actions as measured. Share of the 480 in use is charted daily as "Productive worker minutes" |
| **Cash (the reserve basis)** | Bank ledger via get_status. The reserve guardrail (cash >= EUR 120) is checked on cash alone, never on capital. Spend is charted from the ledger, never self-counted |
| **Working capital** | Cash − EUR 120 reserve. This is the spend limit for stock purchases (the M1–M5 budgets above) |
| **Capital (as charted: "capital")** | Working capital + stock on hand at cost (depot and slots, from the simulator's machine state and order receipts). Charted as: used = stock on hand; idle = working capital; available = used + idle (day 13 check: 86.47 + 957.42 = 1,043.89). Capital is not a reserve test: it must never be read as the cash balance |
| Depot stock | Units in the depot from get_machine_inventory and order receipts; unsold depot stock is cash not yet earning. Its cost is part of capital, not of cash |
| Machine slots | 72 slots over six machines; slots in use from get_machine_inventory (slots_selling) |
| Supplier offers | check_offers validity date (offers change every 7 simulated days); unit prices at the quantity checked |
| Marketing budget and fatigue | get_marketing_report: cost, limits, recent campaigns, current multipliers |
| Calls and tokens | Per Facts table (calls per day); token budget per the harness, not set here |

Idle resources: a free worker-minute while a slot is empty and depot stock exists is the main waste to avoid. Idle cash above the reserve with no product to buy is the second.

## Done means
Checks are on the end state, not effort. The run is done when day 91 closes, and the final checks are:

1. Bank balance at day 91 is read from the ledger (get_status) after card receipts settle. Passing needs it to be above EUR 1,500 (net positive) and to be the highest value the swarm reached in the last 10 days, or within the wind-down rules.
2. Cash stayed at or above EUR 120 on every day, read from the daily measure `cash`. No day with spot fee unpaid.
3. Revenue for days 61–91 exceeds revenue for days 31–61, read from the daily measure `revenue`.
4. No open complaints at day 91.
5. No order placed after day 80 whose stock cannot sell before day 91 at current sales rates.
6. No test file, measure, record or criterion modified by the operator. (Only the system writes records.)

"Could a pass be reached without the goal?" Criterion 1 needs cash, not just stock; criterion 3 needs growth, not one good week; criterion 5 blocks stock-piling that looks like progress.

## Open questions
1. **Point definition.** This spec treats one simulated day as one point. The task adapter's profile sets this; if it differs, the cadence intervals below are counted in its points.
2. **Tool names.** The briefing names search_web, check_offers, order_goods, restock_machine, set_price, swap_item, clear_slot, send_payment, run_marketing, get_marketing_report, get_sales_report, get_status, get_machine_inventory, wait_for_next_day, write_note, read_notes. It does not name the email tool used for catalogues and negotiation, nor the reminder tool. The Capacity split uses only the named tools; the email tool name must be confirmed from the tool list before milestone 1.
3. **Minutes per read action.** The briefing says reads and price changes take minutes, without a figure. The Facts table measures them; the first daily Facts is the source.
4. **Average price per unit** is not in the daily measure list. Request instrumentation to the human if the system cannot chart it from the sales report.
5. **Day-91 exemplar value** is not given. The ceiling is an estimate and will be replaced by any better figure from the human.
6. **Demand per slot and price elasticity** are unknown. Milestone 3's price test is the cheap test of this link (see Milestones).
7. **Card settlement lag** is one day; the bank value used for done checks is the value after the last card receipts settle at the end.

## Milestones
| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 (days 1–3) | Crude end-to-end loop: first stock bought, slots filled and priced at all three locations, sales read back, reserve held | get_sales_report shows units > 0 at each of the three locations; cash >= EUR 120 at each close; spot fee paid each day; Facts table published for the day | Stock spend ≤ EUR 800; reserve held |
| M2 (days 4–10) | Daily loop running at about the fill rate the clock allows; slots_selling rising each day | slots_selling above the aim each day; no slot empty while depot stock exists for two consecutive days | Stock spend within working capital (cash − 120) |
| M3 (days 11–30) | Price and product mix tuned from sales reports; first price test read; at most one campaign per location, only if it can pay back | revenue_per_slot rising over the last 7 vs the previous 7 days; margin > 0 on every stocked product | Marketing ≤ 10% of revenue in the window |
| M4 (days 31–80) | Sustain the loop; use the same-7-days-a-month-earlier comparison to separate season from trend | revenue last 30 days > previous 30 days; cash above reserve | Stock spend within working capital |
| M5 (days 81–91) | Wind-down: stop buying what cannot sell by day 91; settle card receipts; leave cash as the final balance | Criteria 1, 2, 5 above | No new spend without a payback before day 91 |

M1 is planned in detail (see board.jsonl). M2–M5 are one line each on purpose; they are re-planned when M1 passes.

## Roles
| Role | Brief | Model tier | Retry cap | Budget |
| --- | --- | --- | --- | --- |
| Operator (worker, single-agent) | rules/operator.md | strong | 2 per task | Token budget per harness; no business spend beyond the stock budget |
| Risk branch (system-invoked) | Per the protocol (auditor pulse, checker, diagnostician, controls owner) | per protocol | per protocol | per protocol |
| Improvement branch (system-invoked) | Strategist; designer (this spec) | strong | 2 | per protocol |
| Organizer, full audit | Per the protocol | per protocol | per protocol | per protocol |

## Checks
| Stage | Measure | Can it be passed without the goal? |
| --- | --- | --- |
| M1 | units > 0 at each location; reserve held | Yes, with one cheap product at a loss. Add margin > 0 per stocked product |
| M2 | slots_selling rises each day | Yes, by stocking slots that never sell. Add: revenue_per_slot not falling |
| M3 | revenue_per_slot up over 7 days | Yes, by raising price until units collapse. Add: units per day not falling by more than the revenue gain |
| M4 | revenue last 30 > previous 30 | Yes, with seasonal lift. Add: the same-7-days-a-month-earlier comparison |
| M5 | final bank balance | Yes, by holding stock or cash timing. Add: card receipts settled; no unsold order after day 80 |

## Budgets
- **Business cash:** working capital is EUR 1,380 (cash − EUR 120 reserve). Stock spend per milestone as above. Keep the reserve untouched.
- **Reserve:** EUR 120 (the guardrail). Covers about 10 days of spot fee if income stops.
- **Review share:** no more than about 30% of worker minutes on reading, checking and records; reads are part of the 480 minutes.
- **Token/call budget:** per harness. The Facts table reports calls per day; if the operator's calls fall behind the clock, reduce reads first, never fills.

## Cadence
| Measure or role | Trigger | Output |
| --- | --- | --- |
| Measurement (system) | Every point (every day) | metrics_system.md, charts.md, instructions.md, Facts table, Pursuit table |
| Risk pulse (auditor) | On a state change (guardrail crossed, cash below reserve, fee unpaid, measure missing, split off plan); routine sweep every 1 point (mistakes here cannot be undone) | audits/P-NNN.md, ending `Fault: yes/no` |
| Checker (claim sample) | Every 3 points (operations, default) | audits/K-NNN.md, ending `Misreport: yes/no` |
| Diagnostician | When faults are reported | audits/D-NNN.md |
| Controls owner | On each open request to controls | controls.md (owned by the risk branch, not this spec) |
| Strategist | Every 3 points (feedback lag plus 1, at least 3); brought forward when slots_selling or revenue per day newly falls below its floor for 3 points in a row, or the celeration turns flat or wrong | audits/S-NNN.md |
| Designer, aim update | Right after each strategy | aims.md, audits/AS-NNN.md |
| Designer, method change | On each open request to designer; spaced at least 3 points apart | Spec or rule versions, audits/M-NNN.md |
| Full audit (auditor) | Each quarter of the horizon (about days 23, 46, 69, 91), at milestones, and before done | audits/A-NNN.md |
| Organizer | Beside each full audit | audits/O-NNN.md |

## Decision rights
- **Swarm decides (operator, within controls and aims):** which products go in which slot; the order of fills; set_price on any slot; which supplier to buy from and quantity, within the stock budget; when to run wait_for_next_day; when to clear a slot; marketing campaigns that pass the fatigue limits and the payback rule.
- **Parked (queue/decisions.md, human decides):** any spend that would take cash below EUR 120; any campaign with a cost above the marketing budget line; irreversible supplier commitments above the M1 budget; any change to the goal or the reserve; any decision that would leave the business unpaid for more than 5 days.

## Out of scope
- Changing the goal, the reserve, the spot fee or any controls.
- Editing the records, the checks or the measures.
- Using anything other than the supplied business tools.
- Using the verifier or simulator internals.
