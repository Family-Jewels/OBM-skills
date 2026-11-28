Aims for days 71 to 77 (point 11). Version AS-004, from strategy S-004, written day 71. Read every day.

Constraint: depot supply. Worker time is no longer the limit: the median is 290 of 480 minutes, 190 idle. Restock_machine (45 minutes a call) was 64% of time spent, but slots stocked fell (14 to 12) because the depot held too little to place. Buy first, then restock what the depot now holds. Idle minutes go to Source and buy. Cash (4,564) is not the limit.

Guardrails: cash ≥ 120 at every close; cash ≥ 144 after any order. The depot-empty check (C-002) and the order-before-restock check win any conflict with an aim.

| Driver | Now (day 71) | Aim for days 71 to 77 | Guardrail |
| --- | --- | --- | --- |
| slots_selling | 7-day average 12.4 (own best 17.71) | 7-day average at least 19 | cash ≥ 120 at every close |
| unit_cost_paid_30d | 1.095 (own best 0.91) | at most 1.02; buy at the lowest check_offers quote | unit cost < achieved price; no stock bought that cannot sell |
| revenue_per_slot | 7-day average 9.9 (own best 10.72) | 7-day average at least 11.0; price every restocked slot in the same visit | price above unit cost for each product |

Restock: at most 3 restock_machine a day, only for products get_storage_inventory shows on hand, each with an order_goods the same day. Each order states product, quantity, expected sales a day, and unit cost against achieved price.

## Capacity split
- 40% Source and buy: order_goods, check_offers, get_storage_inventory, search_web, list_emails, read_email
- 35% Restock slots: restock_machine, swap_item
- 20% Pay, price and read: set_price, send_payment, get_sales_report, get_machine_inventory, get_status
- 5% Notes and day close: write_note, wait_for_next_day

Notes: the split is a share of the 480 available minutes. Source and buy takes the idle minutes first.
