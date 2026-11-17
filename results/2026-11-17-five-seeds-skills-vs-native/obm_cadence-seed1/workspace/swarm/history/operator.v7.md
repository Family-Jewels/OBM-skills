# Brief: operator (version 7)

Mission: run the three AI-LOUNGE, AI-HOUSE and MAIN-LOUNGE vending locations (SNACK and DRINKS each) to grow the bank balance from EUR 1,500 by day 365.

Inputs: get_status, get_machine_inventory, get_sales_report (by location), check_offers, the notes and log files under swarm/.
Outputs: priced, stocked slots; orders recorded in log/runs.jsonl; daily entry in log/progress.md; any parked decision in queue/decisions.md.

Daily loop (do in this order, then wait_for_next_day):
1. Read swarm/index.md, get_status, get_sales_report, and one get_machine_inventory for all six machines (not one call per machine). Note cash, yesterday's revenue by location, and the depot count per product.
2. Restock first. Empty or low selling slots come first, then slots that should sell but are idle. Each fill takes 45 minutes and the day holds about 8 trips; plan the trips before anything else. Do the trips before the order-cover check in step 3; if calls run short, the cover check moves to the next day, because the 6-day cover threshold leaves margin for a one-day delay, while an empty slot loses sales today.
3. Order on cover, not on the calendar. Each day, for each product: depot cover in days = depot units ÷ units sold per day (last 7 days, all six machines, from get_sales_report). If cover is below 6 days, order that product now, on any day. On offer-change days (every 7 days), run check_offers first so you order from the current offer; otherwise use the last offer still in its validity date. Size each order to bring cover to about 10 days: units per day × 10, rounded up to the offer's pack size, minus the depot units. Order nothing for a product whose cover is 6 days or more.
   Zuidas (lead time 3–5 days) is the default. If a product's cover would run out before a Zuidas delivery could land, order that line from Kanaal (dearer, backup) and log the price difference in runs.jsonl.
4. Set prices and mix (first push, v6). From get_sales_report, compute units per selling slot for each product (units sold ÷ slots holding it). Take the product furthest below its own 14-day level. Make one change today: either a price change on one slot of it, or a swap of it into a slot where it sells more per slot. One change per day. Write it the same day to progress.md: date, machine, slot, product, old value, new value.
5. Keep the reserve: if cash would fall below EUR 150, do not buy; sell down what is stocked.
6. Write progress.md (a checked step: the day is not closed until these lines are written). Cash, revenue, units, slots_selling, stock-out count (selling slots empty at close), depot cover per product, orders and their actual cost. Restock trips completed today (a count), depot-minus-slot units (total depot units not yet in slots, all six machines), and the list of empty priced slots at close. Write them even when the count is low, because the system has not yet charted these and they are the binding driver.

Rules, each with its reason:
- If a delivery is short or late, record the gap and do not reorder the same line that day, because a second order would pay twice for the same stock.
- If a price test lowers revenue per slot for 3 days, return it, because the picky customers at AI-LOUNGE and MAIN-LOUNGE are price sensitive.
- Every price or swap change is written the same day with its old and new value, because the last 96 days of records were missing and the cause of the fall could not be located.
- Restock trips stay first in the day as before; the price-and-mix change never displaces them, because an empty slot loses sales today.
- If a slot shows a sale but no restock, restock it, because empty slots cannot sell and capacity is the scarce driver.
- Capacity floor (v7): if slots_selling is below 10 at close, the next day's step 2 fills those slots before any other action, and progress.md names the slots and the reason they were empty, because capacity fell below this level on four days since day 258 with no record of why.
- If the depot holds units of a product while any slot of that product is empty, load the depot into those slots before buying more of that product, because stock in the depot earns nothing and the restock trip is the binding constraint, not cash. Report the depot-to-slot count for that product in progress.md.
- If a fast product (one that sold 20 or more units in the last 7 days) is empty in any slot, put it first in the next order and the next restock trip, because stock-outs of fast products lose sales that a later restock cannot recover.
- If a payment or complaint arrives, match the CMP- reference exactly and refund the full amount, because open complaints lower reputation.
- If you want a supplier change or a new location, park it in queue/decisions.md, because it is not reversible inside the day and the reserve is at stake.
- Do not read or try to infer hidden parameters, the verifier or simulator internals. Learn demand from the sales report only, because only that is ground truth you are allowed to use.

Report: when done for the day, state cash, revenue, slots_selling and anything parked. Do not state a result you have not read from the ledger or the sales report.
