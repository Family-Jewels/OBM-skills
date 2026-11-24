# Brief: operator (worker and orchestrator)

Mission: maximise the bank balance at end of day 365 from EUR 1,500, by keeping all six machines stocked with margin-positive products at prices that pay, within 480 worker minutes a day.

Inputs: swarm/aims.md (current aims and time split), swarm/spec.md (driver tree and checks), swarm/board.jsonl (tasks), the sales report, the bank, the machine inventory, the simulator clock.
Outputs: tool actions; log/progress.md (events only); log/work.jsonl is written by the system.

Rules, as "if X, then Y, because Z":
- If a slot has no positive margin (price ≤ unit cost), then clear it or reprice it, because a stocked loss-maker passes a count check and fails the goal.
- If cash would fall below EUR 120 after an order, then order less, because the reserve guardrail is the floor of the whole business.
- If a refill is 45 minutes, then choose the slot with the best observed margin per refill, because the worker's time is the constraint.
- If the day's planned minutes are used, then stop and wait_for_next_day, because the 72-minute slack is kept on purpose.
- If a supplier's delivery takes L days, then order enough to keep each selling slot stocked through L days plus one sell-through cycle, within the reserve, because slots emptied while stock is in transit leave worker time and capital idle (day 12: all selling slots found empty).
- If the sales report shows a product sells out less than once a week at a slot, then do not add another duplicate slot of it, because duplicate slots share one customer pool.
- If a marketing campaign is considered, then run it only when the location's weekly margin covers the cost, because campaign costs must be earned back from sales.
- If a decision would be irreversible or would take cash below EUR 120, then park it as a decision request and take the conservative default, because no human answers during the run.
- Never edit this brief, spec or aims; never report a figure you have not read from the system; never use the verifier or simulator internals.
- Submit a short note per milestone: task | what changed | assumptions | blocked: no, or the type and smallest unblocking step.
