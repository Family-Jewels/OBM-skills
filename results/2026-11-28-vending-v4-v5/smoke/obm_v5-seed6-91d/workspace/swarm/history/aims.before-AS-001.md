As of day 0 (after the initial design, spec v1)   Constraint: worker time, 480 minutes per working day (about 10 fills a day at 45 minutes each, before walking and pricing). Capital is second: it binds only when the next order would take cash below EUR 144.

| Driver | Now | Aim for the next point (by day 3 unless stated) | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling | 0 | 18 slots selling by day 3; 36 by day 10; 60 by day 30 | 45% | cash ≥ 120 at every day close |
| revenue_per_slot | not yet measured | a positive figure from the first sales report; not below its week-1 median by day 7; up 10% by day 21 | 15% | price above unit cost for each product |
| unit_cost_paid_30d | not yet measured | 5% below the first 30-day value by day 30, from quotes at the quantity bought | 15% | unit cost < achieved price; no unsellable stock bought |

## Capacity split
- 45% Restock slots: restock_machine, swap_item, clear_slot
- 15% Source and buy: search_web, check_offers, order_goods, list_emails, read_email
- 15% Price and read: set_price, get_sales_report, get_machine_inventory, get_storage_inventory, get_status
- 5% Marketing test: run_marketing, get_marketing_report
- 10% Notes and day close: write_note, read_notes, wait_for_next_day
- 10% Reserve for refunds and complaints: send_payment

Notes: Each morning: get_status, then get_machine_inventory. Then order only what fits the cash guardrail, restock, and set a price on every slot in the same visit (unpriced stock sells nothing). Read get_sales_report before each day close. Marketing stays at zero until M4 unless the Strategist redirects. The supplier email tool is not yet named in the spec (open question 1); until it is, use search_web and check_offers.

Methods: swarm/spec.md and swarm/rules/.
