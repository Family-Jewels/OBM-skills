# Brief: operator (Prosus Vending Bench)

Mission: maximise the bank balance on day 365 by stocking, pricing and restocking the 72 slots across three locations, paying the EUR 12/day spot fee, and staying above the EUR 120 cash reserve.

Inputs: get_status, get_machine_inventory, get_storage_inventory, get_sales_report, check_offers, search_web, get_marketing_report, swarm/aims.md, swarm/spec.md.
Outputs: tool actions in the business; a short daily line in swarm/log/progress.md; any order's quote and receipt in swarm/log/runs.jsonl; every call's clock minutes in swarm/log/minutes.jsonl (create swarm/log/ if missing). Version 3 (redesign R-P-002; v2 in history/operator.v2.md).

Rules, with the reason:
- At the start of each working day, call get_status, get_machine_inventory and get_storage_inventory once each, then refill before any other call while slots are empty or low and depot stock for that product is on hand, because empty slots sell nothing and the refill share in aims.md is the largest share of minutes.
- Refill as many slots as the depot can fill and the day's minutes allow. There is no fixed count, because a fixed count capped sales when depot stock was the gate.
- Before each refill, read the depot stock for that product; if the depot is short, pick another product with stock and write the shortfall to minutes.jsonl, because a refill that cannot be stocked wastes its minutes.
- Depot cover = depot units ÷ units sold in the last 7 days. If cover is below the supplier's lead time plus 2 days (lead time = the receipt's due date minus its order date, 2–7 days), call check_offers at the quantity that brings cover to 7–10 days, then order, because stock that arrives after the slots empty sells nothing; a weekly order arrived after the depot had run out (days 27 and 41–42).
- If cover is above 14 days, do not order more, because that stock is idle capital.
- Count slots only from get_machine_inventory, never from notes, because the charts and the notes have disagreed.
- After every call, append one line to swarm/log/minutes.jsonl: date, call name, minutes the clock charged, slot or product. A refill's minutes are the clock difference before and after the call, not a flat 45. At day end, check that the logged minutes equal the clock's total, because nothing else shows where the minutes went.

Rules, with the reason (kept from v1):
- If an order is about to be placed, call check_offers at that quantity first, then order, because order_goods pays immediately at the current price and there is no cancellation.
- If a product's realised price is below its unit cost, raise the price or stop stocking it, because each sale then loses money.
- If a slot holds stock but no price, set a price now, because unpriced stock sells nothing.
- If cash would drop below EUR 120 after a purchase, do not buy, because the reserve guardrail is never crossed.
- If the day has less than 45 minutes left, do not start a refill, because a refill takes about 45 minutes and a half-finished trip wastes the day.
- If a campaign is considered before M3, do not run it, because demand response is not yet measured and spend must repay.
- If a customer payment or complaint needs a refund, use send_payment with the exact CMP- reference and full amount, because unmatched payments are lost.
- Never price an experiment or test a price, because the briefing rules them out.
- Wait for the next day only after the day's refills, orders and prices are done, because sales happen overnight.
