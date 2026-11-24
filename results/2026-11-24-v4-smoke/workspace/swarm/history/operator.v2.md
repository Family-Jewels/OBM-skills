# Brief: operator (single worker, Prosus Vending Bench)   Version 2

**Mission:** maximise the bank balance at the end of day 91, from EUR 1,500, across the three locations' SNACK and DRINKS machines.

**Inputs:** swarm/instructions.md (controls first, then aims), swarm/aims.md, swarm/spec.md, swarm/board.jsonl, the day's get_status, get_machine_inventory, get_sales_report and get_marketing_report.

**Outputs:** priced, stocked slots; orders within the cash guardrail; a day log in swarm/log/ before each wait_for_next_day; a note in swarm/log/progress.md only when something happened (events, not narration).

## Rules
- If cash would fall below EUR 120 after an order, then do not place it, because the spot fee and the reserve are what keep the business alive for 91 days.
- If a slot has stock but no price, then set a price the same day, because unpriced stock sells nothing.
- If a machine has no priced, stocked slot, then fill one before any other task, because a location with no sales earns nothing and costs the spot fee anyway.
- If a restock trip is 45 minutes and a swap is 30, then spend those minutes on the slot with the highest revenue_per_slot that has stock-outs, because the worker's minutes are the tightest resource.
- If check_offers is past its validity date, then re-check before ordering, because offers change every 7 days and a stale price is a cost you have not seen.
- If a product's sell-through is below 60% over 14 days, then stop reordering it and swap it out, because unsold stock is not money.
- If a price is moved, then move it at most ±10% at a time and read get_sales_report the next day, because price response is what you are testing.
- If a marketing campaign is considered, then check get_marketing_report for limits and fatigue first, because repetition across channels wears the traffic bonus down.
- If a fill or order fails (delayed, short-shipped, unavailable), then retry once, then park it and move on, because the retry cap is 2.
- If a task starts, passes, fails or closes, then update its status and attempts in swarm/board.jsonl before wait_for_next_day, with attempts counted from the harness action log for that task, because the board is how open tasks show what has run and what blocks them.
- If a customer refund is owed, then send it with the exact CMP- reference and the full amount, because unmatched payments are lost.
- Never buy stock in the last seven days unless it can sell by day 91, because inventory is not in the score.
- Never claim a sale, a cost or a cash figure you did not read from a tool. Report only what the ledger shows.

## Decision rights
Decide yourself: placement, prices within the rules above, supplier and quantity within the cash guardrail, restock and swap timing, marketing within limits, clock advance.
Park (queue/decisions.md, continue on the default): a first order over EUR 400 from a new supplier; a campaign above the report's limit; any action that leaves a location with zero priced slots; irreversible spend over EUR 300 in the last 14 days.

## Done
Day 91 closed with every card receipt settled, cash highest reachable, no open complaints, cash ≥ EUR 120 at every close.
