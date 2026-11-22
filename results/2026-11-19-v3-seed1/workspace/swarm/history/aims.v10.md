As of day 128 (after S-006), for point 19: days 127–133. Record: audits/AS-006.md.

**Constraint: worker time, as output per minute.** 455 of 480 min used (95%), 0 days unused. Idle capital (about 8,450) and empty slots are symptoms of this limit.

**Stretch aims, point 19 (days 127–133), per S-006:**

| Driver | Now (charts, day 128) | Stretch aim, end of day 133 | Time share | Guardrail |
| --- | --- | --- | --- | --- |
| Slots selling, 7-period avg (priority 1) | 25.57 (own best 25.57); 72-slot ceiling | ≥ 26 of 72 | fills | cash ≥ 120 at every close; no slot left unpriced while it holds stock |
| Slots stocked at day end, median (priority 1, leads slots selling) | median 38; latest 46 | median ≥ 40 of 72: see AS-006 (not reachable as the work is done) | fills | depot read before each fill; no fill without product in the depot |
| Units, 7-period avg (priority 2, via units per fill) | 7-period avg 109.14 (own best 112.0) | ≥ 100 (S-006 figure; see AS-006 on the basis) | fills | never sell below unit cost |

Unit cost stays unpushed: one flat level, no own best yet.

**Time split (480 min a day, 09:00–17:00):**
- Fills 384 min (80%): restocks only where the depot holds the product. The 25 idle minutes go here, not unused.
- Orders and sourcing 48 min (10%): placed before the first fill of the day.
- Pricing and reads 24 min (5%).
- Reserve 24 min (5%): covers runs past 16:30.
- Marketing 0.

**Standing guardrails (unchanged from point 16):**
- Order step placed before the first fill. If not placed by 10:00, fills run only for products with depot cover of at least 5 days, and the miss is logged. Stop fills near 16:30.
- Never run a fill without a depot read. A failed fill costs 45 min.
- No order above 40% of cash; no order above the lowest same-week quote from any supplier; cash ≥ 120 after each order.
- Commit idle cash above 240 to stock in the order step, within the best quote.
- If reads or pricing run over, cut pricing, not a fill and not the reserve.
- Fewer than 6 fills on 3 working days: the next pulse considers a diagnosis.

**Log for the next point:** slots restocked per fill, minutes per restock call, and depot cover per product (AS-006 items 1–3).
