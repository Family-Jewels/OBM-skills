# Swarm spec: Prosus Vending Bench, 365 simulated days   Version 1

## Goal
Maximise the bank balance at the end of simulated day 365, starting from EUR 1,500, without bankruptcy (more than 10 consecutive unpaid days ends the business). Receiver: the human who set the goal. The goal is not changed by this design.

Horizon: 365 days. Point = 7 simulated days (the natural cycle: weekly offers, weekly traffic and price response). Points 1-52 are whole weeks (day 364); day 365 is a 1-day stub point, counted for final cash and excluded from celeration.

## Driver tree

Cash at day 365 = 1,500 + revenue − unit costs − marketing − spot fees (EUR 12/day, EUR 4,380 over the horizon, fixed, not a driver). Unsold stock is not in the score.

| Measure | = made of | Ground-truth source | Better | Ceiling (source, confidence) | Guardrail | Push on now? |
| --- | --- | --- | --- | --- | --- | --- |
| **Final cash** (top) | opening cash + revenue − unit costs − marketing − spot fees | `cash`, daily bank ledger (get_status) | up | EUR 61,219 at day 365 (benchmark scripted reference operator; medium: it knows hidden parameters, so reachable in principle, gap size unknown) | cash ≥ EUR 120 every day; never 10 unpaid days in a row | the goal |
| Revenue | units × realised price | `revenue`, `revenue_last_7`, `revenue_same_7_a_month_earlier` (seasonal control) | up | EUR 3,228 at day 30 (exemplar checkpoint, medium) | none beyond the cash guardrail | yes, through the drivers below |
| **Slots selling** (capacity in use) | priced slots holding stock | `slots_selling` (machine inventory and price list) | up | 72 slots (resource ceiling, high) | a new slot must add a product the location is not already filling, or relieve a stock-out; duplicates add capacity, not demand | **yes, the constraint now** (refill trips) |
| Revenue per slot | revenue_last_7 ÷ slots_selling | `revenue_per_slot` | up | own best (no exemplar figure, low) | units per location-day must not fall after a price rise | yes |
| − Units per slot | units ÷ slots_selling | `units` by machine, `slots_selling` | up | own best (low) | empty high-yield slots count as lost units | yes, via refill order |
| − Realised price | revenue ÷ units | revenue, units | up while units hold | own best; price response read from get_sales_report (low until 2-3 points) | price ≥ `unit_cost_paid_30d` for that product (never sell at a loss) | yes, one product per point |
| − Product fit by location | units per product per location vs. stated preference (picky sites: savoury snacks and coffee; AI-HOUSE: hungry, less price-sensitive) | get_sales_report by location and product | up | own best (low) | no duplicate slots for a product the location already fills | yes, as read |
| Footfall reach | base footfall × marketing traffic multiplier | get_marketing_report multipliers; revenue after campaigns | up | none (low) | fatigue shown in get_marketing_report is a stop signal; spend must be repaid in revenue | no: hold until the Strategist after point 3 has read a response |
| **Unit cost paid** | cost of goods ÷ units bought | `unit_cost_paid_30d` (successful receipts) | down | lowest offer seen at the order quantity from check_offers across ≥2 suppliers (own best, medium) | buy only what sells through in about two points; unsold stock is cash tied up | yes |
| Marketing spend | run_marketing costs | ledger | down unless revenue rises | none | only with a visible traffic response | no |
| Capital idle | cash above reserve not in stock while a priced slot is empty or unpriced | cash, slots_selling, inventory | down | none | cash ≥ EUR 120 reserve (10 days of spot fee) | tracked; yes |
| Worker minutes | minutes per working day spent in tool calls | simulator clock (09:00–17:00) | used to the plan in aims.md, not beyond 480 | 480 min/day (resource ceiling) | never past 17:00 | yes, the worker's split |

Designer confidence in the tree: high on the structure (it adds up to the ledger); low on the sizes of the demand and price response, which the system reads from sales reports, not from this design.

## Exemplar
Benchmark scripted reference operator (knows the economy's hidden parameters): EUR 3,228 at day 30, EUR 61,219 at day 365, from EUR 1,500. Its day-30 level is above a constant-rate path to day 365 (which would give about EUR 2,040 at day 30), so the reference front-loads its growth. Use it as a checkpoint and a ceiling, not as a method. The swarm's own best celeration is the improvement exemplar once measured.

## Resources
| Resource | How its use is measured |
| --- | --- |
| **Worker time** (first and binding) | minutes per working day from the simulator clock; 480 per day; refill 45, swap 30, every other tool call costs its own minutes (system reads them from the clock). Used share per point against the split in aims.md. |
| Cash (capital) | in use = stock at cost in machines and depot; idle = cash above EUR 120 not in stock while a priced slot is empty; reserve held daily |
| Slots | 72 across six machines (12 per machine, to be confirmed from the inventory read). Capacity per slot: snack rows A/B 18 units, rows C/D 10 units, all drinks slots 10 units. In use = priced and stocked; idle = empty or unpriced |
| Depot stock | units bought and not yet in a machine; cash tied up |
| Supplier terms | `unit_cost_paid_30d` against the best offer seen |
| Customer footfall | not controlled by the swarm; moved only by marketing, measured through the traffic multiplier |

## Measurement (system writes `metrics_system.md` and `charts.md` every simulated day)
- Daily measures: cash, revenue, units, slots_selling, revenue_per_slot, revenue_last_7, revenue_same_7_a_month_earlier (blank until day 37), unit_cost_paid_30d.
- Level charts for each measure: centre and limits computed from its own data (centre ± 2.66 × average moving range); signal = a point beyond a limit, or 8 in a row on one side of the centre.
- Celeration per measure over 7-day points (median-based fit on the log scale, with bounce); provisional from 3 points, firm at 6.
- Top measure (cash): floor line from its level at point 3 to EUR 61,219 at day 365; aim line reaching that value by half the remaining horizon (a deliberate overshoot). Falling short of the aim triggers nothing; three points below the floor brings the Strategist forward.
- Worker time: minutes used per working day against 480, read from the simulator clock, with each tool call's minutes and the refill's 45.
- Slots and capital: slots_selling / 72 (in use) and the idle count; cash and stock at cost, in use and idle.
- Guardrails: cash-reserve line at EUR 120 (flagged on any close below it); minutes past 480; price below unit cost.
- Gap to exemplar: EUR 61,219 ÷ cash at each point.
- Each design change starts a new phase, judged by its level jump and its celeration turn.

## Done means
- Simulated day 365 is reached (SIMULATION OVER) with the business still running (no run of more than 10 unpaid days).
- Final bank balance is the score. Card receipts outstanding at the end are settled (the simulator does this).
- Checks, each passed on the ground-truth ledger:
  - cash ≥ EUR 120 at the close of every day;
  - revenue_last_7 beats revenue_same_7_a_month_earlier at the last 3 points (seasonally clean growth);
  - unit_cost_paid_30d at or below the best offer seen at the order quantity;
  - no slot priced below the unit cost paid for its product;
  - no stock bought in the final 30 days that cannot sell before day 365.

## Open questions
1. Slot layout: 12 slots per machine is assumed from 72 ÷ 6. Confirm from get_machine_inventory on day 1.
2. Demand per location and product, and price response: unknown until get_sales_report reads (points 1-3).
3. Whether unit cost falls with order quantity: read from check_offers at two quantities before the first large order.
4. Size of the marketing traffic response: unknown. Read from revenue after the first campaign, not assumed.
5. Supplier reliability (delays, short-ships, closures): assume at least two suppliers from day 1; the single-supplier risk is a guardrail.
6. The exemplar gives only day-30 and day-365 values. The path between them is the floor and aim line (computed by the system).
7. Adapter facts to confirm with the system: point window (7 days, weekly cycle); the stub day 365 handling.
8. Not a design gap but a constraint: this run allows no experiments. Uncertain links (price response, product fit, marketing response) are read from ordinary sales reports and the charts, one lever per product per point, with no control groups.

## Milestones
| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 (days 1-21, points 1-3) | Crude end-to-end operation: every machine selling | all six machines have at least one priced, stocked slot; cash ≥ EUR 120 every day; offers from ≥2 suppliers recorded; first sales-by-product read done | 480 min per day; stock spend leaves cash ≥ EUR 120 |
| M2 (days 22-91, to quarter 1 audit) | Revenue per slot and slots selling both above their M1 levels | both above M1 level at 3 points; unit cost paid flat or falling | as M1 |
| M3 (days 92-182) | Growth beyond seasonal lift | revenue_last_7 above revenue_same_7_a_month_earlier for 3 points; floor line met | as M1 |
| M4 (days 183-273) | Hold and extend the level | aim line met on 2 of the last 3 points, or floor line met with reserve held | as M1 |
| M5 (days 274-365) | Close-out for maximum final cash | no unsellable stock bought after day 335; card receipts settled; final balance read | as M1 |

Milestones M2-M5 are one line each; M2 is replanned after the Strategist's first redirect.

## Roles
| Role | Brief | Model tier | Retry cap | Budget |
| --- | --- | --- | --- | --- |
| Operator (worker) | rules/operator.md | strong | 2 per task | 480 min per working day; tool calls only within the minutes |
| Pulse auditor | obm-swarm-auditor skill, pulse mode | fast | n/a | one short read of charts per point |
| Full auditor | obm-swarm-auditor skill, full audit | strong | n/a | at quarter points and milestones |
| Strategist | obm-swarm-strategist skill | strong | n/a | after points 3, 6, 9 ... 51 |
| Diagnostician | obm-swarm-diagnostician skill | strong | n/a | on demand |
| Designer | obm-swarm-designer skill | strong | n/a | on demand |

No separate checker: the operator submits no work to be checked. The system's daily ledger (cash, revenue, units, inventory) is the check; a check on a single day's actions is never run by the operator on itself.

## Checks
| Stage | Measure | Can it be passed without the goal? |
| --- | --- | --- |
| Every day | cash ≥ EUR 120 | Yes, by hoarding cash. Paired with revenue and slots_selling checks, so hoarding fails the later checks |
| Every point | revenue_last_7 and slots_selling | Yes, by stocking duplicate slots that add no sales. Paired with revenue_per_slot and units per slot |
| Every point | unit_cost_paid_30d | Yes, by buying cheap stock that does not sell. Paired with sell-through (units per slot) |
| Every point | realised price vs unit cost | Yes, by setting high prices that kill units. Paired with units per slot and the revenue check |
| Quarter and milestone | revenue vs the same period a month earlier | Seasonal lift can pass it. The check is taken from the seasonal control, so only growth beyond the season counts |
| End | final balance vs floor and aim | No; it is the goal |

## Budgets
- Total: no USD budget for the operator; the money budget is the cash itself.
- Reserve: EUR 120 cash, guardrail (10 days of spot fee). Breach is put right first.
- Time: 480 minutes per working day; the split is in aims.md. Unused minutes are idle, not saved.
- Review share: pulse reads are a few minutes of charts per point; the full audit is at quarter points only.

## Cadence
| Measure or role | Trigger | Output |
| --- | --- | --- |
| Measurement (system) | every simulated day | `metrics_system.md`, `charts.md` |
| Operator | every working day | actions, minutes used, cash at close |
| Pulse auditor | every point (7 days); thins to every second point after 3 quiet pulses, back to every point on any signal, redesign or new aims | `audits/P-NNN.md` |
| Full audit | at points 13, 26, 39, 52 (days 91, 182, 273, 364 + day 365 stub), at milestones, and before done | `audits/A-NNN.md` |
| Diagnostician | a pulse or audit says `Diagnosis needed: yes` | `audits/D-NNN.md` |
| Strategist | after points 3, 6, 9 ... 51; brought forward (after at least 2 points since the last) when cash or the top measure is 3 points in a row below floor, or celeration is flat or wrong-way | `audits/S-NNN.md` |
| Designer, aim update | right after each Strategist redirect | `aims.md`, `audits/AS-NNN.md` (ends `Design change needed: yes/no`) |
| Designer, redesign | after a diagnosis, or an aim update that needs a design change; spaced at least 3 points after the last adopted change | `audits/R-NNN.md`, spec and rule versions |
| Results to operator | each Strategist and each redesign | handed to operator the same day |

## Decision rights
- Swarm decides (operator, within the guardrails): which slot to refill and in what order; which product fills which slot; prices above unit cost; which supplier to buy from and quantities at the quoted offer; marketing within the limits get_marketing_report shows, once revenue has responded to earlier spend.
- Parked (decision request, work continues): any order that leaves cash below EUR 120; changing the assortment of all six machines in one point; a marketing campaign after fatigue is shown; any action that removes a machine's last priced slot; anything that would breach the time plan by more than the slack.

## Out of scope
- Changing the goal, the reserve, the spot fee or the 365-day horizon.
- Reading or using the verifier or simulator internals. Only the supplied business tools.
- Experiments, control groups, and writing ground-truth measures by hand.
- Real-world messages; run_marketing never sends them.
