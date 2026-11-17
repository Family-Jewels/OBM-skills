# Swarm spec: Prosus Vending Bench, 365 days   Version 1

## Goal
Maximise the bank balance at the end of 365 simulated days, starting from EUR 1,500. Receiver: the business owner (the human). Unfinished or bankrupt runs score zero, so survival to day 365 is a precondition of any score.

## Driver tree

Top measure: **closing bank balance at day 365** (after outstanding card receipts settle).

Cash gain over time = revenue − costs. Each part, its ground-truth source and direction:

| Measure | = made of | Ground-truth source | Better | Push on now? |
| --- | --- | --- | --- | --- |
| Cash (closing balance) | cash_gain_7 accumulated; equals start + revenue − costs | get_status bank balance; system `cash` | up | Yes (top) |
| cash_gain_7 | revenue over 7 days − costs over 7 days | system chart | up | Yes (the weekly lead indicator) |
| Revenue | units sold × price | system `revenue`; get_sales_report | up | Yes |
| Units | slots_selling × units sold per slot per day | system `units`; get_sales_report | up | Yes |
| slots_selling | slots stocked AND priced (sell nothing otherwise) | system `slots_selling`; get_machine_inventory | up | Yes, first |
| revenue_per_slot | revenue ÷ slots_selling | system `revenue_per_slot` | up | Yes, after slots_selling is full |
| Units per slot | footfall × conversion (location, product fit) × price response | get_sales_report by location | up | Yes, via product mix and price |
| Price per unit | set_price on each slot | system price log; get_sales_report | up to elasticity limit | Yes |
| Costs | purchase cost (COGS) + spot fee (EUR 12/day network) + marketing spend + waste | order receipts; get_status; get_marketing_report | down | Yes: purchase cost |
| Purchase cost per unit | supplier price (check_offers, negotiated terms, weekly discounts) | order_goods receipts (actual cost) | down | Yes |
| Waste / stranded stock | units written off or left unsold at expiry-like exit | get_machine_inventory vs. units sold | down | Monitor |
| Marketing effect | traffic multiplier from run_marketing, net of fatigue | get_marketing_report (current multipliers) | up, with fatigue below limit | Only when it pays back |
| Operator time | trips to machines: restock 45 min, swap 30 min, price/status reads minutes; 8 h day | operator's own clock in tool replies | spend on highest-return trips | Constraint, not a target |
| Reserve | cash minus obligations (next weekly order, next spot fee, card receipts in transit) | get_status | never below reserve | Guard, always on |

Capacity note: 72 slots across 6 machines (3 locations × SNACK + DRINKS). Rows A/B take small products (18 units), C/D large (10 units); drinks slots take 10 units. Duplicate slots share demand and add capacity, not customers, so extra slots only pay when a product is scarce in its slot.

Drivers the operator controls directly: which product in which slot (swap_item), slots filled (restock_machine), price (set_price), supplier and order size (check_offers, order_goods), marketing (run_marketing), trip sequencing (time).

Instrumentation gaps: none in the system's measures for slots, revenue, units and cash. **Units per slot by location and product** is not in the standard measures; get it from get_sales_report by location each week (it is ground truth from the simulator). Purchase cost per unit must be read from order receipts, not from the quoted offer.

## Exemplar
Reference operator, scripted by the benchmark, which knows the economy's hidden parameters: about **EUR 3,228 at day 30** and **EUR 61,219 at day 365**, from EUR 1,500.
Source: benchmark reference, given in the brief; not observable in the simulation.
Use: PIP = exemplar ÷ swarm's balance at the same day. At day 30 the gap is about 2.2× on the balance; the design should watch the gap close over time, not just at the end. The exemplar is a target to reason from, not a rule. Do not treat it as achievable on day 1 (it accumulates from compounding restock and pricing decisions).
Own-best fallback: if the swarm's best 30-day revenue period is higher than the exemplar's pace in a given window, the exemplar is replaced by that period.

## Done means
1. At day 365, closing bank balance (including settled card receipts) is recorded and is as high as the run can make it. The aim per period is set by the exemplar pace, rising as reached.
2. The business is not ended: no streak of more than 10 consecutive unpaid days. Check: spot fee paid every day; check get_status daily.
3. Cash never falls below the reserve at the end of any day. Check: get_status each day against the reserve in the decision rights.
4. Revenue for the last 30 days beats the previous 30 days, read from the ledger (get_sales_report / system `revenue_last_7` and `revenue_same_7_a_month_earlier`).
5. At the last 14 days, no purchase is made that cannot be sold and paid for before day 365 (stock left over is a cost).
6. Open customer complaints (refunds owed) are settled with send_payment exactly as referenced; reputation not damaged.

Must not change on the way: no action that makes the balance drop below the reserve; no unpaid spot fee; no sale-less stock purchases beyond the weekly order plan.

## Open questions
- Reserve level: working value EUR 300, or two weekly orders plus one spot fee, whichever is larger. Confirm from early data (day 7 review).
- Price elasticity by location: AI-LOUNGE and MAIN-LOUNGE are price-sensitive (picky), AI-HOUSE less so. Confirm from sales reports before pushing prices up.
- Marketing payback: campaigns cost money immediately and fatigue accumulates across channels. Decide threshold after first campaign's measured effect.
- Supplier terms: whether negotiating for better terms beats the weekly random discounts. Test once per supplier before committing volume.

## Milestones

| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 | Crude end-to-end: all 6 machines stocked and priced, orders placed, sales and cash flowing, day-30 balance recorded | All 6 machines have ≥1 priced selling slot by day 3; balance tracked daily; no unpaid fee; day-30 balance ≥ EUR 1,500 and trending to exemplar pace | Planned in detail (board) |
| M2 | Weekly operating rhythm: check_offers → order → restock → price review every 7 days, reading sales report per location | Four consecutive weeks with the rhythm completed and cash_gain_7 positive | One line |
| M3 | Pricing and product mix per location tuned to elasticity and preference (savoury snacks, coffee) | slots_selling at full stock on every machine; revenue_per_slot rising two weeks running | One line |
| M4 | Marketing and supplier terms: use only where payback is measured | Each campaign's uplift is measured against limits; total marketing spend ≤ 15% of revenue | One line |
| M5 | Scale and hold to day 365, then wind down: stop buying what cannot sell, settle card receipts, finish balance | Done criteria 1–6 | One line |

Never gate the core behind supporting work: M1 must not wait for marketing, supplier negotiation or perfect pricing.

## Roles

| Role | Brief | Model tier | Retry cap | Budget |
| --- | --- | --- | --- | --- |
| Operator (orchestrates and works the business) | `rules/operator.md` | strong | n/a (environment failures retried, not penalised) | Tool-call and time budget: 8 h/day, see Budgets |
| Checker (reviews the weekly plan and each order before it spends cash) | `rules/checker.md` (short: verify inputs and reserve) | fast | 2 | Sampled after first week |

## Checks

| Stage | Measure | Can it be passed without the goal? |
| --- | --- | --- |
| Each day | cash vs. reserve; spot fee paid; slots_selling | Yes if reserve is kept but nothing is sold: so also require revenue and units trend (below) |
| Each week | cash_gain_7 > 0; revenue_last_7 vs. revenue_same_7_a_month_earlier | Yes if cash is stable through inventory build-up: check stock not sitting idle (units vs. slots_selling) |
| Each month | balance vs. exemplar pace (PIP); revenue_per_slot trend | Yes, a flat balance with shrinking costs: check revenue_per_slot too |
| Milestone | M1–M5 pass criteria above | Checked against system measures, not the operator's report |
| Final | Done criteria 1–6 | Balance is the goal itself; criteria 2–6 guard against a balance that is only a near-term illusion |

## Budgets
- Money: no reserve kept aside is spent on marketing; reserve ≥ EUR 300 or two weekly orders plus one spot fee, whichever is larger. Weekly order plan spend cap ≈ 85% of free cash after reserve (about 15% reserve on the working balance).
- Time: each simulated day is 8 hours. Plan the day as: 1 status/offers read, the trips needed (45 min per restock, 30 min per swap), and price changes. Keep ≥ 1 hour unspent as slack for overruns.
- Review share: no more than about 30% of the operator's effort on checking (the checker reviews the weekly order and any single order above 25% of free cash).
- Tokens: no more than the simulation's own tool budget; avoid repeated reads of unchanged data.

## Cadence

| Measure or role | Trigger | Output |
| --- | --- | --- |
| Measurement (system) | Every day | `swarm/metrics_system.md`, `swarm/charts.md` (cash, revenue, units, slots_selling, revenue_per_slot, cash_gain_7 charts with limits) |
| Operator daily check | Every simulated day, 09:00 | get_status and machine inventory; reserve check; restock/swap queue for the day; log in `swarm/log/progress.md` |
| Operator weekly rhythm | Every 7 days, when offers change (check validity date) | check_offers at the needed quantity; order_goods within cap; restock plan; price review per location; sales report by location |
| Checker (weekly order) | Before each weekly order above 25% of free cash, and at the first order after any new supplier | Review record (4.3) |
| Auditor pulse | Every 5 days | `audits/P-NNN.md`: signals on charts vs. routine variation; up to three pivots |
| Auditor full audit | Every 50 days, at each milestone, on day 365 before done, and immediately if a chart signals a wrong-direction change | `audits/A-NNN.md` |
| Diagnostician | When a pulse or audit ends "Diagnosis needed: yes" | `audits/D-NNN.md` |
| Designer redesign | After a diagnosis, or a full audit finds the direction wrong; spaced ≥ 20 days apart | `audits/R-NNN.md`; spec and rules versions |
| Milestone reviews | M1 at day 30; M2 at day 60; M3 at day 120; M4 at day 200; M5 at day 330 | Full audit (A-NNN) |

## Decision rights
- **Swarm (operator) decides:** product per slot, restock and swap sequence, prices within a location's reasonable band, supplier choice and order size within the weekly cap, marketing campaigns within the limits report, customer refunds with send_payment.
- **Parked (decision request, work continues on the default):** any single spend above 25% of free cash; any new supplier with unfamiliar terms; any marketing campaign while fatigue is above its limit; any change to the reserve; any action that could drop cash below the reserve; any scope change (e.g., leaving a location).

## Out of scope
- Accessing the verifier or simulator internals; the exemplar is used as a reference only.
- Any action outside the supplied business tools.
- Operator reporting to a human during the run: records go to `swarm/`, and the final balance is the output.
