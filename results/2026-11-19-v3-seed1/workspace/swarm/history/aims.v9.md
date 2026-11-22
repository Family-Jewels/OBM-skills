As of day 107 (after S-005), for point 16: days 106–112. Record: audits/AS-005.md.

**Constraint: worker time, as output per minute.** 455 of 480 min used (95%). Idle capital and empty slots are symptoms of this limit.

**Stretch aims, point 16 (days 106–112):**

| Driver | Now (day 105 charts) | Stretch aim, end of day 112 | Time share | Guardrail |
| --- | --- | --- | --- | --- |
| Slots selling (priority 1) | 7-period avg 23.29; own best 23.29 | 7-period avg ≥ 25 of 72 | fills | cash ≥ 120 at every close; no slot left unpriced while it holds stock |
| Slots stocked at day end (priority 1, leads slots selling) | median 25; latest 30 | median ≥ 32 of 72 at risk: see AS-005 | fills | depot read before each fill; no fill without product in the depot |
| Units, 7-period avg (priority 2, via units per fill) | 7-period avg 95.9; own best 96.0 | 7-period avg ≥ 96 | fills | never sell below unit cost |

No aim this point for: depot cover and orders placed before cover runs out (no charted level yet; spec checks apply), or unit cost (level not charted; one point only).

**Time split (480 min a day, 09:00–17:00), per Strategist S-005:**
- Fills 378 min (79%): restocks only where the depot holds the product.
- Orders and sourcing 48 min (10%): placed before the first fill of the day.
- Pricing and reads 30 min (6%): read price response from sales reports. No experiments.
- Reserve 24 min (5%): covers runs past 16:30.
- Marketing 0.

**Standing guardrails (unchanged from point 13):**
- Order step placed before the first fill. If not placed by 10:00, fills run only for products with depot cover of at least 5 days, and the miss is logged. Stop fills near 16:30.
- Never run a fill without a depot read. A failed fill costs 45 min.
- No order above 40% of cash; no order above the lowest same-week quote from any supplier; cash ≥ 120 after each order.
- Commit idle cash above 240 to stock in the order step, within the best quote.
- If reads or pricing run over, cut pricing, not a fill and not the reserve.
- Fewer than 6 fills on 3 working days: the next pulse considers a diagnosis.

**Log for the next point:** slots restocked per fill, and minutes per restock call (AS-005 item 2).
