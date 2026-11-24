Aims for point 4 (days 25-28). Version 2, day 25, after redirect S-001. Old aims: history/aims.v0.md.

Constraint: worker time. 410 of 480 minutes used (85%) in the last point; restock_machine takes 80% of the day's minutes. Output per worker-minute is the limit. Idle cash (about 1,670) is a symptom, not the constraint.

| Driver | Now (latest) | Aim for day 28 | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- |
| revenue_per_slot | 9.32 (7-day average 7.9; own best 10.29) | 10.3 on the 7-day average | 15% price setting | Price not below unit cost (about 1.01); units per slot-day not falling |
| slots_selling | 14 at day end (own best 14.43) | 15 at day end on day 28 | 45% restock fills | Restock at or under 45% of worker minutes |
| Product mix | 0 swaps out of non-selling slots this point | 2 swaps out of non-selling slots in point 4 | 15% product swaps | Gross margin per unit ≥ 0 |
| Top measure: cash | 1,948.93 at day 25 | Floor and aim lines are set by the system; no aim here | (outcome) | Cash ≥ 120 at every day close |

Work the restock share down from 80% toward 45%: fill each trip fuller on the slots with the highest revenue_per_slot, and spend the freed minutes on price tests and product swaps.

## Capacity split
- 45% restock fills of demanded slots, fuller per trip: restock_machine
- 15% price setting and tests: set_price
- 15% product swaps out of non-selling slots: swap_item, clear_slot
- 10% supplier purchasing (hold; cash is idle): check_offers, order_goods
- 10% reads and admin: get_status, get_sales_report, get_machine_inventory, read_notes, write_note
- 5% marketing (M3 test set-up): run_marketing

Order of the day: reads first (get_status, get_sales_report), then fills on the highest-yield slots, then prices for newly stocked slots, then swaps. Order stock only when check_offers shows a price inside the guardrail and the quote is unexpired.
