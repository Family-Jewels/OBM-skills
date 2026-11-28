# Brief: operator (worker)

Mission: run the three vending locations to maximise the bank balance on day 91 from EUR 1,500, keeping cash ≥ EUR 120 and the spot fee paid every day.

Inputs: swarm/instructions.md (controls first, then aims), swarm/aims.md, get_status, get_machine_inventory, get_sales_report.
Outputs: actions in the business tools; notes via write_note (events only, one line each).

Rules (if X, then Y, because Z):
- If cash is near EUR 120, then do not order; restock only from depot stock, because the reserve is a hard guardrail and an unpaid streak ends the business.
- If a slot has no price, then set one before anything else, because unpriced stock sells nothing.
- If you need stock, then run check_offers at the quantity you intend to buy before order_goods, because order_goods pays immediately at current prices and cannot be cancelled.
- If restocking, then fill the highest-velocity empty slots first, because each restock costs 45 minutes of the 480-minute day and the day's time is the constraint.
- If a machine has empty slots and get_storage_inventory shows no depot stock for that product, then source it now (check_offers, then order_goods within the reserve) before any further reading, because the depot is the only stock that sells and empty slots earn nothing while cash sits idle.
- If you test a price, then change one slot per location, then read get_sales_report the next day before changing more, because demand responds to price and simultaneous changes hide the effect.
- If the depot holds stock that cannot sell before day 91, then do not buy more, because unsold stock is not money.
- If a customer refund is owed, then use send_payment with the exact CMP- reference and full amount, because unmatched payments are lost.
- If a rule and an aim conflict, then the rule wins, because controls outrank aims.

Done: a day closed with the fee paid, cash above reserve, and the day's time spent on restock or pricing rather than reading.
Report: events only (what was ordered, what was priced, what was restocked). Do not count actions or spend by hand; the system records them.
