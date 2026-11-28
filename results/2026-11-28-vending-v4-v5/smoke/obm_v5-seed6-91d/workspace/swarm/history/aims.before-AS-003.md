Aims for day 42 (next point, days 40 to 42). Version AS-002, from strategy S-002. Read every day.

Constraint: supply. A fill can only place the stock already in the depot, and suppliers take 5 to 15 days, so order before the depot cover falls below the lead time. Worker time is now nearly full (430 of 480 minutes, median of the last 7 days). Cash and capital are not the limit (about 2,500 cash; about 2,180 of capital idle). Keep every order above the cash reserve: cash ≥ 144 after any order.

Inside the controls: the order-before-restock check and the lowest-quote check in controls.md win any conflict with an aim.

| Driver | Now (day 39) | Aim for day 42 | Guardrail |
| --- | --- | --- | --- |
| slots_selling | 7-day average 16.0 (18 on day 39) | 7-day average at least 17 | cash ≥ 120 at every close |
| unit_cost_paid_30d | 0.99 (1.026 on days 32 to 36) | at most 0.98; buy at the lowest check_offers quote | unit cost < achieved price; no stock bought that cannot sell |
| order_goods | about 3 a point | at least 5 in days 36 to 42, each before the restock it feeds | a stated reason per order: product, quantity, expected sales a day |
| revenue_per_slot | 7-day average 10.13 (AS-001 aim 10.5 not yet reached) | hold at least 10.5 | price above unit cost for each product |

Spend the idle minutes first on sourcing: check_offers and order_goods before the next restock_machine.

## Capacity split
- 50% Restock slots: restock_machine, swap_item; only from depot stock on hand
- 30% Source and buy: order_goods, check_offers, get_storage_inventory, search_web, list_emails, read_email
- 15% Pay, price and read: set_price, send_payment, get_sales_report, get_machine_inventory, get_status
- 5% Notes and day close: write_note, wait_for_next_day

Notes: the split is a share of the 480 available minutes (the plan basis, spec.md Resources). Pair each restock visit with one sourcing step the same day (check_offers, or order_goods when depot cover is below the supplier's lead time). Set a price on every restocked slot in the same visit.
