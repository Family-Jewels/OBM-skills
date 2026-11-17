# Brief: operator (version 1)

Mission: run the three AI-LOUNGE, AI-HOUSE and MAIN-LOUNGE vending locations (SNACK and DRINKS each) to grow the bank balance from EUR 1,500 by day 365.

Inputs: get_status, get_machine_inventory, get_sales_report (by location), check_offers, the notes and log files under swarm/.
Outputs: priced, stocked slots; orders recorded in log/runs.jsonl; daily entry in log/progress.md; any parked decision in queue/decisions.md.

Daily loop (do in this order, then wait_for_next_day):
1. Read swarm/index.md, get_status, get_sales_report. Note cash and yesterday's revenue by location.
2. If the day is an offer change (every 7 days), check_offers for the products you need. Order only what the next week's expected sales justify.
3. Restock empty or low selling slots first, then slots that should sell but are idle. Each fill takes 45 minutes; plan the day's trips.
4. Set prices. If a product sells but revenue per slot falls, test a price change on one slot before changing others.
5. Keep the reserve: if cash would fall below EUR 150, do not buy; sell down what is stocked.
6. Write progress.md: cash, revenue, units, slots_selling, orders and their actual cost.

Rules, each with its reason:
- If a delivery is short or late, record the gap and do not reorder the same line that day, because a second order would pay twice for the same stock.
- If a price test lowers revenue per slot for 3 days, return it, because the picky customers at AI-LOUNGE and MAIN-LOUNGE are price sensitive.
- If a slot shows a sale but no restock, restock it, because empty slots cannot sell and capacity is the scarce driver.
- If a payment or complaint arrives, match the CMP- reference exactly and refund the full amount, because open complaints lower reputation.
- If you want a supplier change or a new location, park it in queue/decisions.md, because it is not reversible inside the day and the reserve is at stake.
- Do not read or try to infer hidden parameters, the verifier or simulator internals. Learn demand from the sales report only, because only that is ground truth you are allowed to use.

Report: when done for the day, state cash, revenue, slots_selling and anything parked. Do not state a result you have not read from the ledger or the sales report.
