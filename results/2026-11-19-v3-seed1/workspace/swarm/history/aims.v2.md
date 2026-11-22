As of day 0 (initial design, before S-001)   Constraint: worker time (480 min per working day; a slot refill costs 45 min)

| Driver | Now | Aim for the next point (day 14; the day-7 target of 36 moved for supplier lead time, see audits/R-P-001.md) | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- |
| Slots selling | 15 of 72 at day 10 | ≥ 36 of 72 by day 14 | see time split | none exceeds the cash floor |
| Worker fills per day | 0 | ~8 fills per day, every working day | fills 50% of minutes | fills never leave pricing or ordering undone |
| Units per fill | read at first fill | fill every slot to its machine maximum with the fastest-selling product | in fills | fill only priced products |
| Unit cost paid (30d) | read at first order | at or below the best check_offers quote, same week | ordering 10% of minutes | never above the best quote |
| Average net price | read at first sales report | hold until day 14; then rise where price response is read | pricing 5% of minutes | price ≥ unit cost + minimum margin |
| Cash | EUR 1,500 | ≥ EUR 120 at every close | — | hard floor EUR 120 |

Time split for the day (480 min):
- Fills (restock_machine, 45 min each): 50%
- Swaps (swap_item, 30 min each): 5%
- Pricing (set_price): 5%
- Sourcing and orders (search_web, email, check_offers, order_goods): 10%
- Reads and reports (get_status, get_machine_inventory, get_sales_report): 15%
- Marketing (run_marketing, get_marketing_report): 5% and not before day 30
- Unplanned reserve: 10%

Notes:
- First, make the constraint visible: log the minutes each call costs from the clock in log/work.jsonl.
- Fill the highest-demand slots first; choose products by sold-units evidence, starting from savoury snacks and coffee/drinks.
- Do not buy faster than cash allows: keep at least EUR 120 after any order.
- Do not run designed experiments. Read price response and product preference from normal sales reports.
- Next strategy: S-001 after point 3 (day 21).
