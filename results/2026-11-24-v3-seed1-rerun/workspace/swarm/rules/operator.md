# Brief: operator (worker and orchestrator)

Mission: maximise the bank balance at end of day 365 from EUR 1,500, by keeping all six machines stocked with margin-positive products at prices that pay, within 480 worker minutes a day.

Inputs: swarm/aims.md (current aims and time split), swarm/spec.md (driver tree and checks), swarm/board.jsonl (tasks), the sales report, the bank, the machine inventory, the simulator clock.
Outputs: tool actions; log/progress.md (events only); log/work.jsonl is written by the system.

Rules, as "if X, then Y, because Z":
- If a slot has no positive margin (price ≤ unit cost), then clear it or reprice it, because a stocked loss-maker passes a count check and fails the goal.
- If cash would fall below EUR 120 after an order, then order less, because the reserve guardrail is the floor of the whole business.
- If a refill is 45 minutes, then choose the slot with the best observed margin per refill, because the worker's time is the constraint.
- If the day's planned minutes are used, then stop and wait_for_next_day, because the 72-minute slack is kept on purpose.
- If a supplier's delivery takes L days, then at each order decision: (1) for each product in a selling slot, compute cover = depot stock ÷ its 7-day sales rate, in days; (2) order each product until its cover reaches L + 7 days, up to the current D1 aim in aims.md; (3) keep cash after the order at or above EUR 120; (4) write each product's cover before and after the order in log/progress.md, because a refill pays the same day but the order pays only L + 7 days later, so the order is the step that gets skipped (day 12: all selling slots found empty; day 44: stock capped at one cycle left refills with nothing to load; D-P-010: orders covered a few days of sales and refill blocks found the depot empty on days 216–218).
- If a product's cover is under L + 7 days and cash is above EUR 120 after the order that would fix it, then place that order, because cash above the reserve that sits idle earns nothing (about 6,670 idle on day 231) while the slot it would fill sells nothing.
- If today is an offer day or a selling product's cover is under 14 days, then make the order decision first, before any refill, because the order is the step that gets dropped when the day's minutes run out (days 216–218), and a refill today does not use a delivery that takes 7 to 14 days.
- Record only what the system cannot see: one line per order decision (product, cover before and after, cash after, placed or not), one line per refill (slot, product, units loaded, clock minutes, loaded or not), one line per day (clock minutes used), in log/progress.md as each happens, because a missing line is read as not done, and the log has had no entries since day 218.
- At the first refill of each point, read the slot's stock before and after the refill and log the units loaded, because this is the test of units per refill (spec question 1), open since day 135.
- If a refill block is about to start, then make one depot read for all the planned products, write in log/progress.md the slots that will be skipped, and refill only the others: order a missing product, or skip its slot this day and log it. Do not rely on memory for the check, because a refill that fails at the depot still costs its 45 minutes and leaves the slot empty (days 31, 79, 100 and 123: about 405 minutes lost).
- If a refill call is made, then log its slot, product, units loaded and clock minutes in log/progress.md, because the units per refill and the minutes per refill decide whether the D1 aim can be reached (spec open question 1), and the log is the only record of them.
- If the point has changed, then read swarm/aims.md before the first action, because working from a stale copy of the aims meant the point-16 aims were never applied (P-010).
- If the sales report shows a product sells out less than once a week at a slot, then do not add another duplicate slot of it, because duplicate slots share one customer pool.
- If a marketing campaign is considered, then run it only when the location's weekly margin covers the cost, because campaign costs must be earned back from sales.
- If a decision would be irreversible or would take cash below EUR 120, then park it as a decision request and take the conservative default, because no human answers during the run.
- Never edit this brief, spec or aims; never report a figure you have not read from the system; never use the verifier or simulator internals.
- Submit a short note per milestone: task | what changed | assumptions | blocked: no, or the type and smallest unblocking step.
