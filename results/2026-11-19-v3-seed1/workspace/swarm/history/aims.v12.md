As of day 171 (after S-008), for point 25: days 169–175. Record: audits/AS-008.md. Design change needed: yes (output per minute must change; the aims below are not reachable at 45 min a slot).

**Constraint: worker time, as output per minute.** Median 410 of 480 min used (85%), 70 min idle, none unused in the last 7 days. Idle capital (about 80%) and 52 empty slots are symptoms of this limit.

| Driver | Now (charts, day 171) | Aim, end of point 25 | Time share | Guardrail |
| --- | --- | --- | --- | --- |
| Slots stocked at day end, median (priority 1, leads slots selling) | median 20 of 72 | ≥ 26 (level held at point 21) | fills | depot read before each fill; no fill without product in the depot |
| Slots selling, 7-period avg (priority 1) | 20.14 (own best 29.0) | ≥ 26 | fills | cash ≥ 120 at every close; no slot left unpriced while it holds stock |
| Units, 7-period avg (priority 2, via units per fill) | 93.57 (own best 125.29) | ≥ 108 | fills | never sell below unit cost |

Unit cost is not pushed this point.

**Capacity split (480 min a day, 09:00–17:00):**
- Fills 408 min (85%): restocks only where the depot holds the product.
- Orders and sourcing 40 min (8%): order step placed before the first fill of the day.
- Pricing and reads 24 min (5%).
- Reserve 8 min (2%): covers runs past 16:30.
- Marketing 0.

**Guardrails (standing rules stand):**
- Order step before the first fill. If not placed by 10:00, fills run only for products with depot cover of at least 5 days, and the miss is logged. Stop fills near 16:30.
- Never run a fill without a depot read. A failed fill costs 45 min.
- No order above 40% of cash; no order above the lowest same-week quote from any supplier; cash ≥ 120 after each order and at every close.
- Commit idle cash above 240 to stock in the order step, within the best quote.
- If reads or pricing run over, cut pricing, not a fill and not the reserve.
- Fewer than 6 fills on 3 working days: the next pulse considers a diagnosis.

**Log for the next point:** slots restocked per fill, minutes per restock call, depot cover per product, and slots emptied per day (AS-008 items 1–3).
