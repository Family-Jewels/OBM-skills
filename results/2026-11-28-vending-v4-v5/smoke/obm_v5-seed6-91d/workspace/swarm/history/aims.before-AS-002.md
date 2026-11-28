Aims for day 28 (next point). Version AS-001, from strategy S-001. Read every day.

Constraint: restock minutes that do not become selling slots. Restock is 70% of time spent (45 min a fill). Restocks are not all turning into selling slots, and units per selling slot swing (1.8 on day 21, 4.9 on day 24), so unpriced or unsold stock may be taking fills. Depot supply is the second limit: suppliers take 5 to 15 days, so order before depot cover falls below the lead time. Capital is idle (about 1,400 of 1,637), so cash does not bind; keep every order above the cash reserve of EUR 144.

| Driver | Now (day 24) | Aim for day 28 | Guardrail |
| --- | --- | --- | --- |
| slots_selling | 15 (18 on day 23) | at least 18 slots holding a priced product | cash ≥ 120 at every close |
| revenue_per_slot | 10.66 day, 9.76 7-day average | 7-day average at least 10.5 (own best 10.35) | price above unit cost for each product |
| unit_cost_paid_30d | 0.969 | at most 0.95; day-30 aim of 0.864 stands | unit cost < achieved price; no stock bought that cannot sell |

Fill the whole day: 480 minutes. Day 24 used 360. If 45 minutes or more remain after the sales read, do one more restock_machine with a price on each slot.

## Capacity split
- 70% Restock slots: restock_machine
- 12% Source and buy: order_goods, check_offers, get_storage_inventory, search_web, list_emails, read_email
- 15% Price and read: set_price, get_sales_report, get_machine_inventory, get_status
- 3% Notes and day close: write_note, wait_for_next_day
