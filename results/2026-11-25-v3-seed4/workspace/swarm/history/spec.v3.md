# Swarm spec: Prosus Vending Bench, 365-day operation   Version 3
## Goal
Maximise the bank balance at the end of 365 simulated days, starting from EUR 1,500, by running three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with one SNACK and one DRINKS machine (72 slots). Receiver: the human who owns the business result. Unfinished or bankrupt runs score zero, so survival comes before growth.

## Horizon and points
- Horizon: 365 simulated days. Natural cycle: 7 days (weekly offers change every 7 days; sales have weekly and seasonal structure).
- Point = 7 simulated days. Points 1 to 52 are full weeks; point 53 is day 365 alone.
- Quarter audits fall at the end of days 91, 182, 273 and 365.
- Worker clock: 480 working minutes per simulated day (09:00-17:00), so 3,360 per point.

## Driver tree

Final balance = starting cash + cumulative net cash. Cumulative net cash = revenue − cost of goods − spot fees − marketing. Revenue = units sold × average price. Units sold = slots selling × units per selling slot.

| Measure | = made of | Ground-truth source | Better | Ceiling (source, confidence) | Guardrail | Push on now? |
| --- | --- | --- | --- | --- | --- | --- |
| **1. Final balance (cash)** | starting cash + Σ daily net cash | Bank ledger from the system (`cash`) | Higher | €61,219 at day 365, scripted reference operator (external exemplar; high confidence it is achievable, low confidence about how it was reached) | Cash ≥ €120 reserve every day; unpaid days = 0 | Top measure; read, not pushed directly |
| 1a. Revenue | units × average price | `revenue` (daily), sales report | Higher | Revenue per slot × 72 slots × days, cannot exceed the resource ceiling (section below) | Revenue not bought with negative margin | Via 1a1 and 1a2 |
| 1a1. Slots selling | slots stocked AND priced AND not empty | `slots_selling` (system slot records) | Higher | 72 slots, machine count, high | Refill cost must not push cash under reserve | **Yes, first** |
| 1a1a. Worker minutes per refill | minutes spent ÷ refills done | System action log (`log/work.jsonl`, each call's simulated minutes) | Lower | 45 min per refill (tool-stated), high | None | Instrumentation: confirm |
| 1a1b. Stock received per point (units, €) | delivered units from orders, incl. the cover needed for lead time plus one cycle | Supplier receipts (ledger), order log with delivery day | Higher, up to cover need | Cash headroom above the €120 reserve; supplier maximum order quantity (check_offers, not yet recorded: instrumentation). Cover target per selling slot = units per selling slot per day × (supplier lead time + 7 days). Lead times: noordzee and zuidas 3–5 days; bakker about 10 days (D-P-007) | Unit cost < price on every line; cash ≥ €120 after each payment; no stock held beyond lead time plus one cycle | **Yes, first** (feeds 1a1; the constraint found in D-P-002) |
| 1a2. Revenue per selling slot | revenue ÷ slots_selling | `revenue_per_slot` (system) | Higher | Own best, then exemplar-implied (not known; low confidence) | Must not rise by cutting price below margin | **Yes, second** (mix and price) |
| 1a2a. Units per selling slot per day | sales volume, demand-limited | `units` ÷ slots_selling | Higher | Own best; demand is set by location and by price response | Stock-outs: empty slot days counted as lost | Read; affected by price |
| 1a2b. Average selling price | set_price per product | Price log, sales report | Set by margin | Own best; price response from sales report | Margin per unit > 0; no price moves that fall revenue for 2 points running | Tested in M2 |
| 1b. Cost of goods | units × unit cost | `unit_cost_paid_30d` (system, receipts) | Lower | Lowest accepted offer price per product at order quantity (supplier offers, high on the mechanism, unknown on the level) | Only buy product whose price exceeds unit cost with margin | **Yes, third** |
| 1b1. Offer price captured | paid price ÷ lowest offer seen | Receipts vs check_offers records | Lower | 1.00 (paying the lowest offer is the ceiling) | Never delay stock below reserve to wait for a better offer | Read |
| 1c. Spot fees | €12/day fixed | Ledger | Fixed | €4,380/year, not controllable | Paid daily | Fixed; no lever |
| 1d. Marketing spend | run_marketing costs | Marketing report | Lower unless it lifts units | Limits in get_marketing_report | Moderate use only; repetition causes fatigue | Test in M3 only |
| 1e. Worker capacity | minutes used per point | System clock | Used on the top-value work | 3,360 minutes per point | Reserve 10% unallocated | **The constraint; see Resources** |

**Ceilings and confidence.** The exemplar is the only external ceiling: €3,228 at day 30 and €61,219 at day 365. We do not have the exemplar's per-slot or per-unit figures, so every per-slot ceiling below is the swarm's own best or the resource ceiling, with low confidence. These are the uncertain links; milestone 1 tests them first.

**Exemplar trajectory (reference celeration).** €1,500 → €3,228 in 30 days is ×2.15, about ×1.19 per week. €3,228 → €61,219 over the next 335 days is ×19, about ×1.065 per week on average. A steep first month, then a slower compound. The swarm's celeration is measured against both.

## Exemplar
Scripted reference operator (benchmark): €3,228 at day 30, €61,219 at day 365, starting from €1,500. Its hidden parameters are not known to us; its trajectory is the only exemplar. Source: benchmark specification. Our own best will be recorded as the swarm's own exemplar after point 3.

## Resources
| Resource | How its use is measured |
| --- | --- |
| **Worker time (the constraint)** | Simulated minutes used per point, from the system clock: 480 per day, 3,360 per point. Each tool call logs its minutes (refill 45, swap 30, price change and status read: measure in M1). Share used on each driver, and the unallocated share (must not fall below 10% except during a refill run). |
| Cash (working capital) | Balance each day against the €120 reserve. Cash in stock (inventory bought, not yet sold) reported from order receipts minus unit costs. |
| Slots (72) | Share of slots stocked, priced and selling (slots_selling ÷ 72); idle slots = stocked or priced count with zero units. |
| Depot inventory | Units on hand and in transit per supplier, from the order log and receipts; stock sitting at the depot is idle capital. Reported by the operator in the progress note each point until the system charts it. |
| Supplier offers | Offers valid for 7 days; check_offers records price, quantity and validity date per supplier. |
| Marketing budget and limits | Spend per location against get_marketing_report limits and fatigue state. |

## Done means
1. **End state:** the balance on day 365 is as high as the work can make it, read from the system ledger (`cash`). The aim is the overshoot line in `charts.md`, not a fixed cap.
2. **Must not change on the way:** cash never falls below €120 on any day; no 10-day run of unpaid days; no product sold below unit cost; no send_payment to unmatched references.
3. **Time bound:** day 365 end of day. Each point ends with its pulse review.
4. **Proof:** `metrics_system.md` and `charts.md` (written by the system, not by the operator) show the balance trajectory, slots_selling, revenue_per_slot, unit_cost_paid_30d and minutes per point.

## Open questions
1. **Overshoot line for an unbounded goal.** The goal is "maximise balance" with no fixed target. The adapter uses the exemplar €61,219 as the goal for the floor and overshoot lines. Confirm this with the system; the swarm does not set it.
2. **Refill cost in minutes when one trip fills several slots.** Tool stated 45 minutes per refill. Milestone 1 measures whether a trip covering several slots at one machine is cheaper per slot.
3. **Minutes for price and status calls.** The briefing says "minutes" without a figure. Measured in M1; the time split below stays provisional until then.
4. **Demand per slot.** No sales data yet. Sales report by location and product is the first source; price response and weather/season effects come from it.
5. **Exemplar per-slot figures.** Not available. Per-slot ceilings stay "own best" until the first 3 points.
6. **Supplier behaviour.** Delays, short-shipment and failure are possible. Recorded per order (ordered vs received, delivery day).
7. **Supplier maximum order quantity and the €60–90 order sizes.** Record max quantity per offer from check_offers in the progress note (not yet in the workspace). Stock received per point (1a1b) cannot be sized until this is known.
8. **Stocked vs selling reconciliation.** Charts day 18 show 5 stocked at day end and 14 selling. Selling cannot exceed stocked. Asked of the system: reconcile the two counts; until then the check below applies to both.
9. **Charts for the stock route (requested of the system).** `charts.md` does not yet show stock received per point (1a1b), depot units on hand, or refills per point, so the 40-refill trigger and the stock-in driver cannot be read from the charts. Until the system adds them, the operator reports all three in the progress note at each pulse, from receipts and the action log.

## Milestones
| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 (days 1-21) | Crude end-to-end operation: stock profitable products in every location, price above unit cost, collect cash, measure the constraint (minutes per call, refill cost, demand per slot). | Cash ≥ €120 every day; slots_selling ≥ 24 by day 14; unit cost < price on every stocked product; minutes per call logged for every call type | Worker time: first 3 points, reserve 10% |
| M2 (days 22-91) | Fill the highest-value slots first and tune price and mix. First quarter audit at day 91. | Balance on day 30 ≥ €3,228 (exemplar); slots_selling ≥ 48 by day 60; revenue_per_slot rising 2 points out of 3 | Worker time per point, mostly refills |
| M3 (days 92-182) | Secure supply (best offers, order quantity), test marketing once per location, sustain the floor. Half-year audit at day 182. | Unit cost paid ≤ lowest offer seen plus 5%; no reserve breach; balance on the floor line | Worker time per point |
| M4 (days 183-273) | Refine the mix and price against seasonal demand (revenue_same_7_a_month_earlier). Third-quarter audit. | Balance on the floor line; revenue_last_7 above revenue_same_7_a_month_earlier on 2 of 3 points | Worker time per point |
| M5 (days 274-365) | Run to the end without breach; make the last weeks cash-positive; final audit. | Balance at day 365 read from the ledger; final audit complete | Worker time per point |

Only M1 is planned in detail; M2 to M5 are one line each and get planned at the Strategist's direction.

## Roles
| Role | Brief | Model tier | Retry cap | Budget |
| --- | --- | --- | --- | --- |
| Orchestrator (operator) | rules/operator.md | strong | 2 per action | Worker-time split in aims.md |
| Measurement (system) | Fixed (not an agent) | — | — | — |
| Checker | rules/checker.md (review of each milestone and each refill-plan change) | strong | 2 | Within review share |
| Auditor | Pulse and quarter audit per protocol section 3 | strong | 2 | Within review share |
| Strategist | obm-swarm-strategist skill | strong | 2 | Within review share |
| Designer | This spec | strong | 2 | Within review share |

## Checks
| Stage | Measure | Can it be passed without the goal? | Counter-check |
| --- | --- | --- | --- |
| Refill | slots_selling | Yes: a slot could be stocked with a product that sells nothing | Also requires revenue_per_slot not falling and units per slot > 0 |
| Price | revenue_per_slot | Yes: prices can be raised until volume falls to zero | Also check units per slot and balance; guardrail on margin |
| Buying | unit_cost_paid_30d | Yes: buying the cheapest item may leave slots empty | Must also keep slots_selling at aim |
| Stock-in | stock received per point (1a1b) | Yes: stock that never sells ties up cash | Also requires unit cost < price, cash ≥ €120 after payment, slots_selling rising |
| Cash | cash | Yes: stopping refills keeps cash high but ends growth | Balance must rise along the floor line, with slots_selling at aim |
| Time | minutes per point | Yes: spending no minutes avoids errors but earns nothing | Refill count per point at aim |

## Budgets
- Total: no token or money budget set by the system beyond the business cash itself. Operating spend (purchases, fees, marketing) comes out of the balance.
- Reserve: cash never below €120 (guardrail); unallocated worker time ≥ 10% per point.
- Review share: at most about 30% of worker minutes spent on pulse, audit and checks combined; the audits themselves are mainly system-run.

## Cadence
| Measure or role | Trigger | Output |
| --- | --- | --- |
| Measurement (system) | Every simulated day | `metrics_system.md`, `charts.md` |
| Measurement (system), celeration | Every point (7 days) | Celeration per measure over 7-day points, floor and aim lines |
| Pulse review | Every point (every point; every second point after three quiet pulses; back to every point on any signal, redesign or new aims) | `audits/P-NNN.md` |
| Full audit | Days 91, 182, 273, 365; milestones; before done | `audits/A-NNN.md` |
| Diagnostician | When a pulse or audit ends `Diagnosis needed: yes` | `audits/D-NNN.md` |
| Strategist | After point 3 (day 21), then every 3 points (days 42, 63, ...); brought forward after at least 2 points when the top measure is below its floor line 3 points in a row or celeration is flat or falling | `audits/S-NNN.md` |
| Designer, aim update | Right after each Strategist redirect | `aims.md`, `audits/AS-NNN.md` |
| Designer, redesign | After a diagnosis, or an aim update that needs a design change; spaced ≥ 3 points apart | `audits/R-NNN.md`, new spec version |
| Checker | Each milestone product and each refill plan change | Review record |

## Decision rights
- **Swarm decides:** which slots to stock and in what order; product mix within the depot and offer limits; prices above unit cost; order size and supplier choice within the reserve; refill and swap schedule within the time split; marketing within limits and only in M3 or later.
- **Parked (decision request, work continues):** any single purchase that would take cash below €120 or into the reserve; supplier terms or contracts; changes to the goal, the exemplar, or the guardrails; any action that would deliberately sell below unit cost; any send_payment outside a customer refund.

## Out of scope
- Any access to the verifier, simulator internals or anything outside the supplied business tools.
- Changing the goal, the reserve, or the exemplar.
- Any business outside the three locations.
