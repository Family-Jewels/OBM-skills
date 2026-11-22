As of day 45 (after S-002), for the point ending day 49.

**Constraint: worker time.** 435 of 480 min used (median, last 7 days, simulator clock), 91%. Each restock is one slot at 45 min, so worker time sets how many slots get restocked. Stock and cash are not the limit.

| Driver | Now (day 45, charts) | Stretch aim, end of day 49 | Time share | Guardrail |
| --- | --- | --- | --- | --- |
| Slots selling (priority 1) | 7-period avg 18.86 (own best 19.14) | ≥ 24 of 72 (7-period avg) | fills | cash ≥ 120 at every close; no slot left unpriced while it holds stock |
| Slots stocked at day end (leads slots selling) | median 20, latest 23 of 72 | ≥ 36 of 72 | fills | depot read before each fill; no fill without product in the depot |
| Units sold, 7-period avg (priority 2, via units per fill) | 71.71 (own best 78.14) | ≥ 78 | fills | never sell below unit cost |
| Unit cost paid, 30d (priority 3) | rising, wrong way (charts) | ≤ 1.00, at or below the best check_offers quote the same week | sourcing and orders 58 min | never above the best quote |
| Cash (top measure) | 3,033 (charts, day 45) | no aim of its own here; floor and aim lines stand | — | hard floor 120 |

**Time split (480 min a day, 09:00–17:00), replaces the day-37 split:**
- Fills 336 min (70%): 7 restocks at 45 min = 315, plus 21 spare. Seven is the most the split allows; 8 would need 360 min.
- Sourcing and orders 58 min (12%), order step placed first.
- Pricing and swaps 38 min (8%).
- Reads and reports 24 min (5%), including the depot read before each fill.
- Reserve 24 min (5%), against runs past 17:00.
- Marketing 0.

**Guardrails on the split:**
- Place orders before the last fill of the day. Stop fills when the clock nears 16:30.
- A failed fill costs 45 min. Never run a fill without a depot read.
- If reads or pricing run over their share, cut the lowest-value pricing action, not a fill and not the reserve.
- Commit idle cash above 240 to stock within the best quote, each order under 40% of cash, keeping the 120 floor.
- Do not run designed experiments. Read price response from normal sales reports.
