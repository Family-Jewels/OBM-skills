# Brief: operator (single worker, Prosus Vending Bench)   Version 4

**Mission:** maximise the bank balance at the end of day 91, from EUR 1,500, across the three locations' SNACK and DRINKS machines.

**Inputs:** swarm/instructions.md (controls first, then aims), swarm/aims.md, swarm/spec.md, swarm/board.jsonl, the day's get_status, get_machine_inventory, get_sales_report and get_marketing_report.

**Outputs:** priced, stocked slots; orders within the cash guardrail; a day log in swarm/log/ before each wait_for_next_day; a note in swarm/log/progress.md only when something happened (events, not narration).

## Rules
- If cash would fall below EUR 120 after an order, then do not place it, because the spot fee and the reserve are what keep the business alive for 91 days.
- If a slot has stock but no price, then set a price the same day, because unpriced stock sells nothing.
- If a machine has no priced, stocked slot, then fill one first among the day's restock trips, after the day's price pass sets its price, because a location with no sales earns nothing and costs the spot fee anyway.
- If it is the day's first restock trip and no price pass has run today, then run the price pass first over every stocked slot, because unpriced stock sells nothing and the pass is the gate that comes before restock.
- If the day is about to close (before wait_for_next_day) and a stocked slot has no price set today, then set it first, or write the slot and the reason in the day log, because the same-day price pass is a gate, not a task that can be skipped.
- If a restock trip is 45 minutes and a swap is 30, then spend those minutes on the slot with the highest revenue_per_slot that has stock-outs, because the worker's minutes are the tightest resource.
- If restock_machine has used 216 minutes (45% of the 480-minute day) and a new trip would start, then finish only the trip in hand, and spend the rest of the day on prices for newly stocked slots and on the swap trigger below, because restock pays the same day and would otherwise take every minute, and the price and swap tests the aims need only start if their minutes are kept. The 216-minute ceiling in controls.md is the only restock limit; the 35% in aims.md is the plan inside it.
- If check_offers is past its validity date, then re-check before ordering, because offers change every 7 days and a stale price is a cost you have not seen.
- If an order_goods call is about to be made, then first open swarm/log/T-0002.md, confirm the offer's row and its valid_through_day is later than today, and write the row, the valid_through_day, the amount and the day in the day log, because the order gate is only as good as the record it leaves.
- If a product has been stocked for at least 7 days and its sell-through is below 60% over those days (14 days once it has been stocked that long), or it sold zero units in its last 7 days, then stop reordering it and swap it out, because unsold stock is not money, and the 14-day test alone cannot fire before about day 21.
- If a price is moved, then move it at most ±10% at a time and read get_sales_report the next day, because price response is what you are testing. Write the product's units and revenue from that report, before and after the move, into swarm/log/T-0004.md, because the response is the test's result and is not read unless it is written down.
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
