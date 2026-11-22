As of day 65 (after S-003), for point 10: days 64–70.

**Constraint: worker time, as output per minute, gated by depot stock.** Median 420 of 480 min used (last 7 days, simulator clock): 60 idle min a day. A fill is made only where the depot holds the product, so stock sets how many fills happen. Fills ran 5–7 a day against a plan of 8. Energy had no cover until day 65; nuts and stroopwafel had none on day 62.

| Driver | Now (day 63 charts) | Stretch aim, end of day 70 | Time share | Guardrail |
| --- | --- | --- | --- | --- |
| Slots stocked at day end (leads slots selling) | median 23 of 72 | median ≥ 30 of 72 | fills | depot read before each fill; no fill without product in the depot |
| Slots selling (priority 1) | 7-period avg 21.0 (own best 21.0) | 7-period avg ≥ 24 of 72 | fills | cash ≥ 120 at every close; no slot left unpriced while it holds stock |
| Units sold, 7-period avg (priority 2, via units per fill) | 7-period avg 81.14 (own best 81.14) | 7-period avg ≥ 88 | fills | never sell below unit cost |
| Orders placed before 10:00 (depot cover, priority 1 process) | missed on days 59, 60, 62 | order step placed before 10:00 on every working day | sourcing and orders 48 min, first | no order above 40% of cash; no order above the best quote; cash ≥ 120 after each order |
| Unit cost paid, 30d (priority 3) | level not charted; trend rising (x1.01) | no stretch aim this point; every order at or below the best same-week quote, logged | sourcing and orders | never above the best quote |
| Cash (top measure) | 4,096.6 at point 9 | no aim of its own; floor and aim lines stand | — | hard floor 120 |

**Time split (480 min a day, 09:00–17:00), replaces the day-45 split:**
- Fills 360 min (75%): 8 restocks at 45 min each (one slot per call; spec open question 1 closed). Only where the depot holds the product.
- Sourcing and orders 48 min (10%): order step first, placed before 10:00.
- Pricing and swaps 24 min (5%).
- Reads and reports 24 min (5%): the depot read before each fill counts here.
- Reserve 24 min (5%): covers runs past 16:30.
- Marketing 0.

**Guardrails on the split:**
- Place orders before the first fill of the day. Stop fills near 16:30.
- A failed fill costs 45 min. Never run a fill without a depot read.
- If reads or pricing run over their share, cut the lowest-value pricing action, not a fill and not the reserve.
- Commit idle cash above 240 to stock in the order step, within the best quote, each order under 40% of cash, keeping the 120 floor.
- Fewer than 6 fills on 3 working days, or median stocked below 30 on day 70: the next pulse considers a diagnosis.
- Do not run designed experiments. Read price response from normal sales reports.
