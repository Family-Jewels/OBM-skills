# Operator brief (v1)

Mission: run the six Prosus Vending Bench machines to maximise the bank balance at day 365, staying solvent.

Inputs: `swarm/spec.md`, `swarm/index.md`, the latest `swarm/charts.md`, `get_status`, `get_machine_inventory`, `get_sales_report`.
Outputs: priced, stocked slots; order receipts; `log/progress.md` entry each day.

Rules:
- If cash is below EUR 150, then stop all non-essential purchases and marketing, because the spot fee and the 10-day unpaid limit would end the business.
- If a purchase would take cash below EUR 150, then park it as a decision, because that floor is what keeps the run alive through a bad week (spec: Done means 2).
- If a slot is empty or sold out and the product sells, then restock it first, because slots_selling is the cheapest lever on revenue.
- If a price change is made, then read `get_sales_report` before changing it again, because price response needs a few days to show.
- If units fall while revenue holds, then check the price, because a high price can hide a drop in demand.
- If a chart signal appears in the wrong direction, then flag it in `log/progress.md` the same day, because an immediate audit follows.
- Check offers (`check_offers`) before ordering, and order only at the current offer price, because prices change every 7 days.
- Log every purchase, price and restock action in `log/work.jsonl` with its outcome.
- Do not edit the spec, measures or the charts. Claim only what the ledger and sales report show.
