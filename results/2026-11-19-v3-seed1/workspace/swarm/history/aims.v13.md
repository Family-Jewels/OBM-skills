As of day 191 (after S-009), for point 28: days 190–196. Record: audits/AS-009.md. Design change needed: yes (aim 1 cannot be met at 45 min a slot; the batch test that would show whether one restock call fills several slots has not been logged).

**Constraint: worker time, as output per minute.** Median 465 of 480 min used (charts, last 7 days): 97%, 15 min idle. Idle capital (about 12,750) and 22 empty slots are symptoms of this limit. The output per minute must change; the aims are not lowered.

| Driver | Now (charts, day 191) | Aim, end of point 28 | Time share | Guardrail |
| --- | --- | --- | --- | --- |
| Slots selling, 7-period avg (priority 1) | 22.86 (own best 29.0) | ≥ 29 | fills | cash ≥ 120 at every close; no slot left unpriced while it holds stock |
| Slots stocked at day end, median (priority 1, leads slots selling) | median 50 of 72 | ≥ 50 | fills | depot read before each fill; no fill without product in the depot |
| Units, 7-period avg (priority 2, follows slots) | 74.43 (own best 125.29) | ≥ 110 | fills | never sell below unit cost |

Unit cost is not pushed this point.

**Test this point (decides aim 1):** one restock call for several empty slots of one machine, only where the depot holds the product. Log minutes per call and slots per call (R-P-013 item 2). If one call fills several slots, the fill loop changes; if not, aim 1 stays out of reach at this capacity.

**Capacity split (480 min a day, 09:00–17:00):**
- Fills 424 min (88%): restock only where the depot holds the product.
- Orders 32 min (7%): order step by 10:00; commit idle cash above 240 within the best quote.
- Pricing and reads 16 min (3%).
- Reserve 8 min (2%): covers runs past 16:30.
- Marketing 0.

**Guardrails (standing rules stand):**
- Cash ≥ 120 after each order and at every close.
- Never run a fill without a depot read. A failed fill costs 45 min.
- Order step by 10:00. If missed, fills run only for products with depot cover of at least 5 days, and the miss is logged. Stop fills near 16:30.
- No order above 40% of cash; no order above the lowest same-week quote from any supplier.
- If reads or pricing run over, cut pricing, not a fill and not the reserve.
- Fewer than 6 fills on 3 working days: the next pulse considers a diagnosis.

**Log for the next point:** slots restocked per call, minutes per restock call, fills per working day, depot cover per product, and slots emptied per day.
