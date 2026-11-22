As of day 150 (after S-007), for point 22: days 148–154. Record: audits/AS-007.md. Design change needed: yes (the stock aim cannot be met as the work is done).

**Constraint: worker time, as output per minute.** Median 410 of 480 min used (85%), latest 435, 70 min idle. Idle capital (about 10,400) and 46 empty slots are symptoms of this limit.

**Stretch aims, point 22 (days 148–154), per S-007:**

| Driver | Now (charts, day 147) | Stretch aim, end of day 154 | Time share | Guardrail |
| --- | --- | --- | --- | --- |
| Slots stocked at day end, median (priority 1, leads slots selling) | median 26 of 72 | ≥ 38 (own best median). Not reachable on the current design: see AS-007 | fills | depot read before each fill; no fill without product in the depot |
| Slots selling, 7-period avg (priority 1) | 26.14 (own best 29.0); 72-slot ceiling | ≥ 29 | fills | cash ≥ 120 at every close; no slot left unpriced while it holds stock |
| Units, 7-period avg (priority 2, via units per fill) | 108.29 (own best 125.29) | ≥ 120 | fills | never sell below unit cost |

Unit cost is not pushed this point.

**Capacity split (480 min a day, 09:00–17:00):**
- Fills 408 min (85%): restocks only where the depot holds the product. The 70 idle minutes go here.
- Orders and sourcing 40 min (8%): order step placed before the first fill of the day.
- Pricing and reads 24 min (5%).
- Reserve 8 min (2%): covers runs past 16:30.
- Marketing 0.

**Guardrails (point 16 standing rules stand):**
- Order step before the first fill. If not placed by 10:00, fills run only for products with depot cover of at least 5 days, and the miss is logged. Stop fills near 16:30.
- Never run a fill without a depot read. A failed fill costs 45 min.
- No order above 40% of cash; no order above the lowest same-week quote from any supplier; cash ≥ 120 after each order and at every close.
- Commit idle cash above 240 to stock in the order step, within the best quote.
- If reads or pricing run over, cut pricing, not a fill and not the reserve.
- Fewer than 6 fills on 3 working days: the next pulse considers a diagnosis.

**Log for the next point:** slots restocked per fill, minutes per restock call, depot cover per product, and slots emptied per day (AS-007 items 1–3).
