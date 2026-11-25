# Swarm spec: Prosus Vending Bench, 365-day operation   Version 3

## Goal
Maximise the bank balance at the end of simulated day 365 (SIMULATION OVER), after card receipts settle. Starting cash €1,500. Receiver: Prosus (the owner). Bankruptcy or an unfinished run scores zero, so staying solvent to day 365 is a precondition of any score.

Operator = the worker role (section 1 of the protocol). The operator runs three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with a SNACK and a DRINKS machine: 6 machines, 72 slots.

## Driver tree

Top measure: **final balance** = opening cash €1,500 + cumulative revenue − cumulative unit purchases − marketing − spot fees (€12/day network) − refunds, settled at the end.

| Measure | = made of | Ground-truth source | Better | Ceiling (source, confidence) | Guardrail | Push on now? |
| --- | --- | --- | --- | --- | --- | --- |
| **Final balance / cash** (top) | opening cash + revenue − purchases − marketing − fees − refunds | bank ledger via get_status; end settlement | higher | €61,219 at day 365 (benchmark scripted reference; medium: the figure is given, the route is not) | cash ≥ €120 every day | Indirectly, through the drivers below |
| Revenue (daily) | slots_selling × revenue_per_slot | sales report, bank ledger | higher | own best; no external figure | none beyond margin | Via 2 and 3 |
| 2. **slots_selling** | slots holding stock with a price set | get_machine_inventory | higher, up to 72 | 72 (resource ceiling, high) | worker time (refill trips) | **Yes: the constraint** |
| 2a. depot cover | days of stock on hand (depot + slots) ÷ units sold per day | get_status, depot stock, sales report | higher, up to order lead time + 2 days | lead time per supplier (2–11 days observed); medium | cash ≥ €120 | **Yes: the supply link** (instrumentation: depot stock and sell-through per day, system-measured). Cover target (v3): ≥ supplier lead time + 2 days for each fast seller. Chart row and aim requested from the system and Strategist (audits/R-P-004.md) |
| 3. revenue_per_slot | units per selling slot-day × average price | sales report ÷ slots_selling | higher | own best; medium-low (route unknown; learn from sales report) | price ≥ unit cost | **Yes** |
| 3a. units per slot-day | demand (location traffic × product fit × price response) × availability (share of days the slot has stock) | sales report | higher | availability 100%; demand from sales report | none | Yes: keep fast sellers stocked |
| 3b. average price | set_price per product | price log, ledger | higher, subject to demand response | none set by hand | price ≥ unit cost + margin floor | Yes, once price response is read |
| 4. **Revenue per worker minute** | units sold per refill trip × price ÷ 45 min (refill) | clock minutes (simulator clock, system-measured) + ledger | higher | own best | none | Later: worker time is not the binding link while slots are dry (Open questions 6) |
| 5. unit_cost_paid_30d | purchase spend ÷ units received, 30-day rolling | order receipts (actual cost) | lower | own lowest 30-day; low confidence | availability must not fall; a purchase is never chosen on unit cost alone when its lead time leaves cover short (v3) | No: guardrail, watched not pushed (v3) |
| 6. Traffic | location footprint × marketing multiplier | get_marketing_report | higher | none | fatigue; stay inside limits | Later: after day 14, moderate |
| 7. Fixed cost: spot fee | €12/day, €4,380 over the year | ledger | lower | not controllable | must be paid (10 unpaid days ends the run) | No |

Instrumentation still needed (not reported by any agent): minutes per tool call (from the simulator clock, measured by the system); units per refill trip (from stock before and after each refill); price response per location (from the sales report). Where a link has none of these, it is an uncertainty, not a gap.

## Exemplar
Benchmark scripted reference operator (knows the economy's hidden parameters): about €3,228 at day 30 and €61,219 at day 365, from €1,500. Implied growth from day 30 to day 365 is about ×19 over 335 days, roughly ×1.063 per 7-day point. This is the ceiling for the top measure. The route is not known to the operator; learning it from the sales report is the main uncertainty.

## Resources
| Resource | How its use is measured |
| --- | --- |
| **Worker time** (the constraint): 480 min per working day, 09:00–17:00 | Minutes used per day from the simulator clock, by tool: refill 45, swap 30, price and reads by clock delta. Idle = 480 − used. Refill trips per day = refill minutes ÷ 45 |
| Slots: 72 across six machines | Selling = stocked and priced. Idle = empty or unpriced. In use % = selling ÷ 72 |
| Capital (cash) | In use = cash committed to stock in slots and depot, plus marketing. Idle = cash above the €120 reserve not committed. Capital is a resource here, not a score |
| Depot stock | Units at the depot not in a slot (idle stock) |
| Marketing allowance | Used against the limits in get_marketing_report, per location |
| Supplier offers | Valid for a week; check_offers prices at the quantity planned, for each of the four known suppliers. Supplier breadth in use = suppliers priced at volume ÷ 4 |

## Done means
- Day 365 reached with the business solvent: cash ≥ €120 on every day; no run of more than 10 consecutive unpaid days.
- Final balance read from the ledger after card receipts settle. Any refund sent only with an exact CMP- reference and full amount; no open legitimate complaints at the end.
- Not changed on the way: records, the goal, and the boundary of the business tools (no simulator or verifier access).
- Checks that cannot be passed without the goal: slots_selling = 72 alone does not pass. It passes only with revenue_per_slot ≥ unit cost and cash rising. Unit cost lowered alone does not pass; it must hold availability.

## Open questions
1. Does one restock_machine call (45 min) fill one slot or a whole machine? Settle at milestone 1 by reading stock and clock before and after one call. This is a measurement, not an experiment: no arms, no deliberate comparison.
2. The goal is "maximise", so the floor line needs an end value. Proposed: the benchmark's €61,219 at day 365 as the goal anchor. The system confirms this in the adapter.
3. The overshoot aim is read as: the aim reaches the goal anchor at the midpoint of the remaining horizon. The system computes the line; confirm the reading.
4. Starting slots, stock and prices are not known until the first get_status. Aims are set from the first read.
5. Price response per location (AI-LOUNGE is price-sensitive; AI-HOUSE less so; MAIN-LOUNGE has the highest footfall) is learned from the sales report, not tested.
6. Worker-time record conflict (D-P-002): charts show a median of 450 of 480 min used, the pulse read about 150 min, and the work log is missing. The system's chart rule counts any day whose calls ran past 17:00 as fully used, so the 94% may overstate use. The system supplies the simulator's daily clock readings; until they settle this, the sourcing rule below does not assume worker time is the constraint. (v3) Partly settled: charts now show median 315 of 480 min used (66%) with 2 unused days in 7. Still open: daily clock readings and minutes by tool, which the system must publish regardless of token budget.
8. (v3) Depot cover (2a) is named the supply link but is not charted and has no aim. Requested in audits/R-P-004.md; until charted, the operator logs depot stock and sell-through in its end-of-day line.
7. Refund basis: complaint claims run 4–10× item price. Designer decision (v2): a refund is limited to the matched transaction's amount; the excess is parked, not paid. Revisit if a claim is shown to match a real transaction.

## Milestones
| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 | Days 0–7: crude end-to-end. All six machines stocked and priced in the order the worker time reaches; first two supplier catalogues and offers read; refill-trip unit measured (open question 1) | By end of day 7 (point 1): slots_selling ≥ 36, no unpriced stock, cash ≥ €120 on every day | ≤ 60% of day-minutes on refills; the rest as in aims.md |
| M2 | Days 8–21: revenue per refill trip raised by choosing rows and products; price set from the sales report; purchases at the cheapest current offer whose delivery keeps cover at lead time + 2 days (v3) | At point 3 (day 21): revenue_per_slot above its day-7 level; unit_cost_paid_30d not above its day-7 level; cash on or above the floor line, or the Strategist brought forward | As above |
| M3 | Days 22–91: sustain high slots_selling; moderate marketing from day 14; first quarter audit at day 91 (point 13) | Quarter audit passes; cash on or above floor line | As above |
| M4 | Days 92–182: keep the drivers the Strategist names; second audit at day 182 | Quarter audit passes | As above |
| M5 | Days 183–273: as M4; third audit at day 273 | Quarter audit passes | As above |
| M6 | Days 274–365: end-game. Stop buying stock that will not sell before day 365; settle card receipts; final audit at day 365 | Final balance confirmed; no stock bought after its sell-through can no longer reach the end | As above |

## Roles
| Role | Brief | Model tier | Retry cap | Budget |
| --- | --- | --- | --- | --- |
| Operator (the worker) | swarm/rules/operator.md | strong | 2 per failed call, then park and report | Cash rules below |
| Measurement | the system only | n/a | n/a | n/a |
| Auditor | obm-swarm-auditor | standard | n/a | n/a |
| Strategist | obm-swarm-strategist | strong | n/a | n/a |
| Diagnostician | obm-swarm-diagnostician | strong | n/a | n/a |
| Designer | obm-swarm-designer | strong | n/a | n/a |
| Checker | not used: the simulator ledger is the ground truth; the operator submits no work to check | n/a | n/a | n/a |

## Checks
| Stage | Measure | Can it be passed without the goal? |
| --- | --- | --- |
| Every day | cash ≥ €120 | No. It guards solvency, the precondition of the goal |
| Points 1, 3 | slots_selling and revenue_per_slot together | Stocking unprofitable items can raise slots_selling. Paired with revenue_per_slot vs unit cost, it cannot |
| Every purchase | Depot cover of each fast seller ≥ its lead time + 2 days (v3). unit_cost_paid_30d watched, not pushed; availability held | Buying cheap long-lead stock lowers cost but leaves slots dry; the cover check fails it. Buying cheap stock nobody buys fails the revenue check |
| Quarters | revenue_last_7 vs revenue_same_7_a_month_earlier | Seasonal demand can move this. Read as a ratio, not an absolute |
| Day 365 | final balance from the ledger | None |

## Budgets
- Total: deployable cash = cash above €120, less the 15% reserve (held unspent).
- Up to 85% of deployable cash may go to stock and marketing. Purchases are sized to cover per slot (sell-through to the next delivery + 2 days) within the €120 reserve. No cap is tied to refill minutes (v3: the old refill-linked cap is removed).
- Marketing: moderate use only, within limits; no more than one campaign per location per week until its fatigue has cleared.
- Review share: none beyond system pulses and audits; the operator does not check its own work.

## Cadence
One point = 7 simulated days. Horizon 365 days ≈ 52 points.

| Measure or role | Trigger | Output |
| --- | --- | --- |
| Measurement (system) | Every simulated day | swarm/metrics_system.md, swarm/charts.md |
| Operator | Every working day 09:00; end of day after its last action | Actions; log/progress.md events; reads charts and handed results |
| Pulse review (auditor) | Every point (day 7, 14, 21 …). After 3 quiet pulses, every second point. Back to every point on any signal, redesign or new aims | audits/P-NNN.md |
| Full audit | Days 91, 182, 273, 365 (points 13, 26, 39, 52); at milestones M1–M6; before done | audits/A-NNN.md |
| Diagnostician | When a pulse or audit ends "Diagnosis needed: yes" | audits/D-NNN.md |
| Strategist | After points 3, 6, 9 … (days 21, 42, 63 …). Brought forward (after ≥ 2 points) when cash is 3 points in a row below the floor line, or celeration is flat or wrong-way | audits/S-NNN.md |
| Designer, aim update | Right after each Strategist redirect | aims.md (copy of old in history/), audits/AS-NNN.md ending "Design change needed: yes/no" |
| Designer, redesign | After a diagnosis; or after an aim update that needs a design change. Spaced ≥ 3 points apart | audits/R-NNN.md, new spec or rule versions |
| Hand-off | Every pulse, audit, strategy, diagnosis, redesign | Given to the operator the same day; the operator logs what it did |

## Decision rights
- **The operator decides:** which slot to fill next; what to price each product at (never below unit cost); which supplier and quantity to order (after check_offers at all known suppliers); refill order and rows; marketing within limits; refunds for legitimate complaints with exact references, up to the matched transaction; when to stop buying stock.
- **Parked (queued in swarm/queue/decisions.md, work continues):** any commitment that takes cash below €120 once paid; any change that drops a location or a machine; long supplier terms that bind beyond a week; any action the operator cannot reverse within a week's cash; any refund claim above the matched transaction amount.
- **Only the designer changes:** the spec, the driver tree, the checks, the rules.
- **Only the Strategist sets:** the aims' direction and the capacity split.

## Out of scope
- Experiments, A/B arms, or deliberate price tests. Price response is read from the sales report.
- Any access to the verifier or the simulator's internals. Only the supplied business tools.
- Lowering the goal, or any aim treated as a ceiling. Aims rise once reached.
- Marketing copy: the wording does not change demand, so it is not optimised.
