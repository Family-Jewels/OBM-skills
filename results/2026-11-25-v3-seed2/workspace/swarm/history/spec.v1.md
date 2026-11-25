# Swarm spec: Prosus Vending Bench, 365-day run   Version 1
## Goal
Maximise the bank balance on the last simulated day (day 365), starting from EUR 1,500, across three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with one SNACK and one DRINKS machine (72 slots). Receiver: the human who set the business briefing. Inventory is not part of the score. The run must not go bankrupt (more than 10 consecutive unpaid days ends it).

## Driver tree

Top measure: **Final bank balance, day 365 (EUR)** = cash at day 365 + card receipts settled at the end
= 1,500 + Σ revenue − Σ (unit cost paid × units sold) − Σ spot fees (EUR 12/day) − Σ marketing spend.

| Measure | = made of | Ground-truth source | Better | Ceiling (source, confidence) | Guardrail | Push on now? |
| --- | --- | --- | --- | --- | --- | --- |
| 1. Final bank balance (EUR) | cash + settled card receipts; see 2 and 3 | get_status cash each day; ledger at end | higher | 61,219 at day 365 (benchmark exemplar; high confidence as a number, low as a path) | cash ≥ EUR 120 at every close; no unpaid spot-fee day | Via 2 and 3 |
| 2. Revenue per day (EUR) | = slots_selling × revenue_per_slot | get_sales_report (daily revenue, by location) | higher | not yet known; M1 baseline, then exemplar-implied (see Exemplar) | none beyond the top measure's | Via 2a, 2b |
| 2a. slots_selling (count) | slots holding stock and a price, that sell | get_machine_inventory (stock, price per slot) at each daily open | higher, until demand runs out | 72 slots (resource ceiling, high confidence); demand lowers it in practice | selling slot sold out before 17:00 = under-stocked; stocked slot with no sale in 7 days = idle capital | **Yes, first. Constraint: worker time (refills)** |
| 2b. revenue_per_slot (EUR/slot/day) | = price × units per slot per day | get_sales_report by product and location | higher | own best, set after M1 baseline; test by M2 | price ≥ unit cost × 1.2 (except clearance, day 351+) | **Yes, after M1 baseline** |
| 2b-i. units per slot per day | product fit to location × footfall × availability; duplicate slots of one product share its demand | get_sales_report; refill and sold-out times from log/work.jsonl | higher | demand limit per product, unknown until M2 | sold-out before close = under-stocked, not over-priced | Yes, via product mix and refill timing |
| 2b-ii. price (EUR/unit) | set_price per slot | set_price log; sales report price response | higher while units hold | not known; learn from sales report (no experiments) | at or above unit cost × 1.2 | Yes, by rule |
| 3. Unit cost paid (EUR/unit) = unit_cost_paid_30d | order receipts at the price paid | system's receipt ledger | lower | lowest per-unit quote at the ordered quantity across checked suppliers (medium-low confidence; M1 finds it) | never buy beyond what will sell; cash ≥ EUR 120 after the order | **Yes, from day 7** |
| 4. Fixed and discretionary costs (EUR/day) | spot fee EUR 12/day + marketing | ledger | lower per EUR of revenue | fixed fee; marketing has a per-location limit in get_marketing_report | spot fee paid daily (unpaid streak ≤ 10, target 0); marketing paid back within 30 days | Hold, no push until a demand-limited location is identified |
| 5. Worker time on drivers 2a–3 (min/day) | refill 45 min, swap 30 min, price, purchase, read, marketing calls, each as the clock logs them | simulator clock and call log (log/work.jsonl), 480 min/day | higher share on 2a–3; total ≤ 480 | 480 min/day (resource ceiling) | total ≤ 480; refill minutes ≤ 300/day unless stock-out count is falling | **Yes. This is the constraint** |

Notes on the tree:
- Revenue is slots × revenue per slot, but slots add capacity, not demand: duplicate slots of one product share its customers. Revenue growth therefore comes first from more distinct products that fit each location, then from more slots of a product that sells out before the next refill.
- Refill throughput (refills per day × units per refill) is the physical link between the depot and driver 2a. Each refill fills a slot to its capacity (18 units for rows A/B, 10 for C/D and all DRINKS slots), so fill to full every time.
- Cash can be kept by investing nothing. Every check for a stage therefore names a direct driver (2a, 2b, 3) as well as cash.

## Exemplar
Benchmark scripted reference operator (knows the economy's hidden parameters): EUR 3,228 at day 30, EUR 61,219 at day 365, from EUR 1,500. Source: benchmark specification, given to the designer; confidence high on the two numbers, none on the path between them.
Implied cash celeration from day 30 to day 365: 61,219 / 3,228 = 18.97 over 47.9 seven-day points, about ×1.063 per point. Implied average net gain from day 0 to 365: about EUR 164/day. The exemplar's daily revenue path is not known; M1–M2 measure ours.
Own best: none yet. Improvement exemplar = the swarm's own best celeration, set from point 3 onward.

## Resources

| Resource | How its use is measured |
| --- | --- |
| **Worker time (primary)**: 480 min per working day, 09:00–17:00 | simulator clock at each call; minutes per call logged to log/work.jsonl; refill 45 and swap 30 are fixed; read, price, order and marketing calls are measured in M1 and replace the design assumptions in aims.md |
| Capital: cash (EUR) | cash at each close; reserve EUR 120 (guardrail); operating planning reserve EUR 204 (EUR 120 + one point of spot fees) |
| Capital in use vs idle | in use = units in selling slots × unit cost paid; idle = stock held in the depot or in unselling slots, plus cash above the planning reserve that is not converted into stock for slots that sell out |
| Slots: 72 across six machines | in use = stocked, priced and selling; idle = empty, unpriced, or stocked with no sale in 7 days |
| Supplier offers and order quantities | check_offers validity date and quote per point; order_goods receipts |
| Marketing budget per location | get_marketing_report limits, costs and current traffic multiplier |
| Depot stock | get_machine_inventory; not in the score, but cash tied up in it is idle capital |

## Measurement (the system writes it; the operator does not)
- Daily measures written each simulated day to metrics_system.md: cash, revenue, units, slots_selling, revenue_per_slot, revenue_last_7, revenue_same_7_a_month_earlier, unit_cost_paid_30d.
- charts.md: process behaviour charts for each daily measure, limits = centre ± 2.66 × average moving range computed from the data; signal = a point beyond a limit or 8 in a row on one side of the centre.
- Celeration per measure over 7-day points (point k = days 7(k−1) to 7k−1). The 7-day window holds the weekday cycle and the weekly offer refresh.
- Top measure (cash) with floor line (from cash after point 3 to the goal at day 365) and the deliberate overshoot aim (computed by the system from the adapter; not set by hand).
- Worker time chart: minutes used per day against 480, by activity.
- Slots and capital in use and idle; cash-reserve guardrail line at EUR 120.
- Seasonality: revenue compared with revenue_same_7_a_month_earlier, not with the previous point alone.

## Done means
- Final bank balance at day 365 is as high as the drivers allow. Checks along the way, each with a direct driver:
  - Cash ≥ EUR 120 at every daily close (guardrail, breach put right first).
  - Spot fee paid every day; no unpaid streak.
  - Every selling slot priced at or above unit cost × 1.2, except clearance.
  - Each weekly order placed only after at least two checked quotes; unit_cost_paid_30d at or below the lowest quote for that point.
  - Refill minutes ≤ 300/day; sold-out-before-close count falling over the last 2 points.
  - Revenue_last_7 beats revenue_same_7_a_month_earlier once data exists.
- End state (day 351–365): no stock bought that cannot sell by day 365; clearance pricing on remaining stock from day 351; no open orders; card receipts settled and counted.

## Open questions
1. Does the system's cash measure include card receipts not yet settled (they settle a day later, and outstanding receipts settle at the end)? Design assumes: top measure = cash + outstanding card receipts; the daily cash measure is read as reported.
2. Minutes per call for reads, price changes, orders and marketing are not in the briefing. Design assumes a few minutes each (planning figures in aims.md); M1 measures them.
3. Product demand by location is unknown. M1 gives the baseline by observation only.
4. Whether the swarm's aim line is "goal plus half the remaining horizon's gain" or another overshoot form: the system's adapter defines it, not the designer.
5. Supplier delivery delays or short shipments: goods arrive at the depot; refill only from arrived stock. Check arrival before planning refills.
6. Exemplar path is only known at day 30 and day 365.

## Milestones

| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 (days 0–13, points 1–2) | Crude end-to-end: all six machines selling at prices above cost; first weekly order at a checked quote; baseline of minutes per call, quotes and units per product | By day 14: each of six machines has a selling priced slot with revenue > 0 in the sales report; zero unpaid spot-fee days; cash ≥ EUR 120 at every close; baseline tables in log/ | Stock purchases ≤ EUR 1,000 of starting cash, keeping ≥ EUR 120 |
| M2 (days 14–30, points 3–4) | Revenue running and rising: sold-out-before-close count falling; first demand read per product per location | revenue_last_7 higher than the previous point for 2 points running; cash at day 30 at or above the exemplar's EUR 3,228 is the aim, not the pass | Purchases within cash guardrail; marketing ≤ limit |
| M3 (days 31–91, points 5–13) | Refill routine keeps selling slots stocked within the refill budget; product mix fitted to each location; supplier terms compared every week | Quarter audit at day 91: unit cost at or below the lowest quote each week; refill minutes ≤ 300/day on average | As above |
| M4 (days 92–182, points 14–26) | Price per product and location set by sales-report response; marketing only where units per slot are demand-limited, with payback within 30 days | Quarter audit at day 182 passes; revenue_per_slot celeration at or above the exemplar's implied ×1.06 per point, or a diagnosis is open | As above |
| M5 (days 183–273, points 27–39) | Sustain and scale the working system; add slots only where a product sells out | Quarter audit at day 273 passes; no guardrail breached in the last 13 points | As above |
| M6 (days 274–365, points 40–52) | Endgame: stop buying what cannot sell by day 365; clearance from day 351; settle card receipts | Day 365 close: final cash, no open orders, card receipts settled; final audit written | Purchases only for expected sales before day 365 |

Only M1 is planned in detail (board.jsonl). Later milestones are one line each and are re-planned at each quarter audit.

## Roles

| Role | Brief | Model tier | Retry cap | Budget |
| --- | --- | --- | --- | --- |
| Operator (orchestrator and worker, one agent; see protocol section 9) | rules/operator.md | session model | 2 per action | Worker time 480 min/day; cash ≥ EUR 120 |
| Checker (sampled) | Verifies each weekly purchase against its quotes and each price rule change against the sales report; the operator's own review, in its own fresh context where possible | session model | 1 | ≤ 30 min/day of worker time |
| Auditor, Strategist, Designer, Diagnostician | Run by the system on schedule; not operator tasks | system | n/a | n/a |

## Budgets
- Money: starting EUR 1,500; hard reserve EUR 120; planning reserve EUR 204 (about 15% of the starting capital plus one point of fees, the working rule). No purchase or marketing spend may cross the hard reserve.
- Time: 480 min per day. Review share ≤ 30% of worker time (≤ 144 min/day), in practice much less.
- Retry cap 2 per action; a failed action is not retried unchanged.

## Cadence

| Measure or role | Trigger | Output |
| --- | --- | --- |
| Daily measures (cash, revenue, units, slots_selling, revenue_per_slot, revenue_last_7, revenue_same_7_a_month_earlier, unit_cost_paid_30d) | Every simulated day at close | metrics_system.md, charts.md (system) |
| Operator daily round | Every simulated day at 09:00: status, inventory, refill and price by priority (see rules/operator.md) | log/progress.md (events), log/work.jsonl (actions, minutes) |
| Purchasing (check_offers, then order_goods) | Each point boundary: days 0, 7, 14, …, 357 (quotes valid 7 days) | Order record with the quotes compared |
| Sales read and learning | Each point, at the boundary | log/progress.md: units and price response per product and location |
| Pulse review (auditor) | Every point: days 7, 14, …, 364; every second point after three quiet pulses; back to every point on any signal or redesign | audits/P-NNN.md |
| Full audit | Milestone M1 close (day 14) and each quarter: days 91, 182, 273, 365 | audits/A-NNN.md |
| Strategist | After points 3, 6, 9, …: days 21, 42, 63, …, 357; brought forward (after at least 2 points) if cash, the top measure, is 3 points in a row below its floor line, or celeration is flat or wrong-way | audits/S-NNN.md |
| Designer, aim update | Right after each Strategist redirect | aims.md, audits/AS-NNN.md |
| Diagnostician | A pulse or audit ends "Diagnosis needed: yes" | audits/D-NNN.md |
| Designer, redesign | After a diagnosis; not sooner than 3 points (21 days) after the last adopted design change | audits/R-NNN.md, spec.v1.md etc. in history/ |
| Checker (sampled) | Every purchase batch and pricing-rule change until 5 clean in a row; then 1 in 3 | review records |
| Final close | Day 365 | Final audit and settlement check |

## Decision rights
- **Swarm decides:** which product goes into which slot; prices within the rule; order quantities and supplier choice among checked quotes; refills and swaps in priority order; marketing within the per-location limit and payback rule; clearance timing from day 351.
- **Parked (queue/decisions.md; work continues):** any action that would take cash below EUR 120 or leave a spot fee unpaid; a supplier with unverified terms or unusual contract conditions; marketing above a location's limit; a purchase that cannot sell by day 365; any change to this spec or the aims outside the system's cadence.

## Out of scope
- Any use of the verifier, simulator internals or anything outside the supplied business tools.
- Deliberate experiments or A/B price tests (the business has none; learn from get_sales_report).
- Changing marketing copy (wording does not change demand).
- Stopping early: the run continues to SIMULATION OVER.
