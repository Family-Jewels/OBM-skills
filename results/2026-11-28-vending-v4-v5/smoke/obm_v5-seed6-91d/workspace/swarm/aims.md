Aims for days 83 to 89 (point 12). Version AS-005, from strategy S-005 (redirect), written day 82. Read every day.

Constraint: depot supply. Slots stay empty because the depot holds too little to place (7 of 72 stocked, median of the last 7 days). Worker time is idle: 195 of 480 minutes used. Cash (5,185) and capital are not the limit. Top measure: bank balance at day 91, EUR 5,500 (spec).

Guardrails: cash ≥ 120 at every close; cash ≥ 144 after any order. The controls in swarm/controls.md win any conflict with an aim.

| Driver | Now (day 82) | Aim for days 83 to 89 | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling | 7-day average 10.0 (own best 17.71) | 7-day average at least 17 | 30% Restock slots, after supply | cash ≥ 120 at every close |
| unit_cost_paid_30d | 1.162 | at most 1.00; buy at the lowest check_offers quote in lots large enough to use idle capital | 45% Source and buy | unit cost < achieved price; no stock bought that cannot sell |
| revenue_per_slot | 7-day average 9.68 (own best 10.95) | 7-day average at least 11.0; price every restocked slot in the same visit | 20% Pay, price and read | price above unit cost for each product |

Source and buy takes the idle minutes first, every day: get_storage_inventory, then check_offers and order_goods for each product the depot will run short of before its supplier's lead time (controls 1 and 2). Each order states product, quantity, expected sales a day, and unit cost against achieved price.

Restock: at most 3 restock_machine a day, only for products get_storage_inventory shows on hand, each with an order_goods the same day.

## Capacity split
- 45% Source and buy: get_storage_inventory, check_offers, order_goods, search_web, list_emails, read_email
- 30% Restock slots: restock_machine, swap_item
- 20% Pay, price and read: set_price, send_payment, get_sales_report, get_machine_inventory, get_status
- 5% Notes and day close: write_note, wait_for_next_day

Notes: the split is a share of the 480 available minutes. Restock at 30% covers three restock_machine calls (135 minutes). Source and buy goes first.
