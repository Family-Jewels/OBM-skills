Aims for days 50 to 56 (point 8). Version AS-003, from strategy S-003, written day 52. Read every day.

Constraint: output per worker minute, and depot supply behind it. A restock_machine call takes about 45 minutes and stocks only what the depot holds. Slots stayed empty while restock ran, so minutes went out with nothing to place. Cash (about 3,350) and idle capital (about 3,050) are not the limit; buy stock early enough that the depot holds it when the restock comes. Cash ≥ 120 at every close; cash ≥ 144 after any order.

Inside the controls: the depot-empty check (C-002) and the order-before-restock check win any conflict with an aim.

| Driver | Now (day 52) | Aim for days 50 to 56 | Guardrail |
| --- | --- | --- | --- |
| slots_selling | 7-day average about 17.1 (20 on day 52; own best 17.71) | 7-day average at least 18 | cash ≥ 120 at every close |
| unit_cost_paid_30d | 0.995 (own best 0.91) | at most 0.96; buy at the lowest check_offers quote | unit cost < achieved price; no stock bought that cannot sell |
| revenue_per_slot | 7-day average about 9.3 (own best 10.72) | 7-day average at least 10.0; price every restocked slot in the same visit | price above unit cost for each product |
| order_goods | not a driver on the chart; the supply step | at least 5 in days 50 to 56, each before the restock it feeds | a stated reason per order: product, quantity, expected sales a day; cash ≥ 144 after the order |

## Capacity split
- 40% Restock slots: restock_machine, swap_item; only for products the depot holds now
- 35% Source and buy: order_goods, check_offers, get_storage_inventory, search_web, list_emails, read_email
- 20% Pay, price and read: set_price, send_payment, get_sales_report, get_machine_inventory, get_status
- 5% Notes and day close: write_note, wait_for_next_day

Notes: the split is a share of the 480 available minutes. Check depot stock (get_storage_inventory) before each restock. Where depot cover of a product is below its supplier's lead time, order first.
