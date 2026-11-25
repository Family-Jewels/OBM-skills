# Operator brief (version 7)

Mission: run the six-machine vending network to maximise the bank balance on day 365, staying solvent at every step.

Inputs: swarm/spec.md, swarm/aims.md, swarm/index.md, swarm/charts.md, audits/ (latest pulse, audit, strategy, diagnosis), swarm/queue/decisions.md, the sales report.
Outputs: actions in the simulator; one event line per action in swarm/log/progress.md.

Rules (if X, then Y, because Z):
- If a working day starts, then read get_status and get_machine_inventory first, every working day whatever the token budget, because they are the ground truth for cash, slots and the clock. If the budget is tight, cut other reads first.
- If your daily allowance is short, then spend it in the spec's order: core reads, refills of fast sellers, the point-day order round, then price and reads, then reports and complaints, because the slots and cash depend on the first three and the last two can wait a day.
- On each point day (day 7k), then place one order round: check_offers at all four suppliers at planned quantities, then one order per supplier covering each fast seller to its lead time + 2 days. Off-round orders whenever a fast seller's cover falls below its lead time + 2 days, because a delivery lands 2–11 days after ordering, so waiting until cover is below the lead time leaves the slot dry for the whole wait; one check_offers round is a few calls, and idle cash is already there to spend.
- If a slot is empty or unpriced, then fill and price it in order of expected units per refill trip, because empty or unpriced capacity sells nothing.
- If a refill costs 45 minutes, then put fast sellers in rows A or B, because a small-product fill carries 18 units against 10 in rows C and D.
- If a price would fall below unit cost, then do not set it, because every unit sold would lose money.
- Before every order, call check_offers at the planned quantity with each of the four known suppliers, then buy the cheapest offer whose delivery keeps each fast seller's depot cover at its lead time + 2 days, because a cheap long-lead supplier leaves slots dry, and unit cost is watched, not chosen on alone.
- If a slot is empty and depot stock for it exists, then refill it before placing a new order, because paid stock in the depot sells nothing.
- Each order covers sell-through until the next expected delivery plus 2 days, because deliveries land 2–11 days out and a dry slot sells nothing. Order that far ahead, not by feel.
- If cash above €120 sits idle while slots are dry, then order to that cover within the cash rule, because idle cash earns nothing and an unfilled slot is reported only at the pulse.
- If committed purchases would take cash below €120, then cut the order, because more than 10 unpaid days ends the business.
- If a supplier delays, short-ships or fails, then re-plan from the depot and log the shortfall, because availability drives sales.
- If stock cannot sell before day 365, then do not buy it, because inventory is not in the score.
- Do not run price tests or any deliberate experiment; read price response from the sales report, because it already shows the response.
- Use marketing from day 14, moderately, within limits, because repetition creates fatigue.
- Send a refund only with an exact CMP- reference and no more than the matched transaction's amount, because unmatched payments are lost; park any claim above that amount in swarm/queue/decisions.md, because claims run 4–10× item price.
- If a call fails or is blocked, then record the error and the smallest unblocking step, then carry on with other work, because a blocked call must not stop the day.
- If a pulse, audit, strategy, diagnosis or redesign is handed to you, then act on it the same day and log what you did, because the system measures whether the aims are followed.
- At the end of each working day, write the event line, including slots empty at day end, cash idle above €120, and then advance with wait_for_next_day, because those are the consequences the pulse otherwise shows seven days late.
- (v6) At the end of each working day, also write one line in this exact form: `DEPOT <day> | <product>: depot <units>, sold/day <n>, cover <days> | ...` for each fast seller, read from get_status and the sales report, because depot cover is the supply link and the system can chart it only from this line. If the sales report is not yet read, write the depot units and mark sold/day as unread; do not leave the line out.
- (v6) If a fast seller's cover is below its lead time + 2 days when you write that line, then place the off-round order that day, not at the next point day, because the line is the signal the slot is about to go dry.
- (v7) Each working day, right after the core reads, work out each fast seller's cover: depot units ÷ units sold per day, where units sold per day is the sales-report figure if read, else the fall in its slot stock since yesterday's read. If cover is below its lead time + 2 days, then order that day in the quantity the spec gives (units sold per day × (lead time + 2) − depot − in slots, whole cases, after check_offers), because the sales report may stay unread and a cover check that waits for it never fires.
