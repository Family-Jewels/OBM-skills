As of day 0 (after design, S-000 initial)   Constraint: worker time (480 min/day, mainly restock trips at 45 min each); cash for first stock is the second constraint on days 1–3

| Driver | Now | Aim for the next point | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling | 0 | 48 by day 7; 72 by day 14 | 62% restocking | cash ≥ EUR 120 |
| revenue_per_slot | n/a (no data) | up two weeks running after the price test (M3) | 8% pricing | units not down beyond the test threshold at any location |
| unit_cost_paid_30d | n/a | down 10% from the first order by day 45 | 12% sourcing | slots_selling must not fall to buy cheaper |
| revenue_last_7 | 0 | EUR 1,000 per 7 days by day 30 (low confidence; the reference's day-30 cash implies this order of magnitude) | all of the above | cash ≥ EUR 120 |

## Capacity split
- 62% restocking: restock_machine
- 6% re-slotting: swap_item, clear_slot
- 8% pricing: set_price
- 12% sourcing: search_web, check_offers, order_goods
- 9% reading: get_status, get_machine_inventory, get_sales_report
- 3% marketing: get_marketing_report, run_marketing

Notes:
- Each period, first read get_status (cash, reserve, fee). If cash is near EUR 120, stop buying and only restock from depot stock.
- Do the restock loop every day: fill the highest-velocity empty slots first, then the rest. Restock is the constraint; reading and sourcing are kept short.
- Price tests: one slot per location at a time, read get_sales_report next period, then apply the winner. Do not change all prices at once.
- Buy only after check_offers at the intended quantity; order_goods pays immediately. Expect delivery overnight through the depot.
- Email (catalogues) uses the email tool from the tool list; it is part of sourcing time.
- wait_for_next_day, write_note and read_notes are not worker-time capacity and are not in the split.
