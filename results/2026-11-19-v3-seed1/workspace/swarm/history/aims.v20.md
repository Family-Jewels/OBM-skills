As of day 289 (after S-014), for point 42: days 288–294. Record: audits/AS-014.md. Supersedes the point-40 aims (history/aims.v19.md). Spec (version 9) and rules unchanged here. Design change needed: yes (see AS-014: at 45 min per slot, 370 fill minutes cannot reach the aims).

**Constraint: worker time (480 min a day), 96% used (460 min median). Output per minute is the limit.** Idle capital (about 22,700) and 39 empty slots are symptoms. Restock minutes per call and slots per call are still not logged, so the 45-min-per-slot cost is an assumption.

| Driver (spec terms) | Now (day 281–287) | Stretch aim, point 42 | Priority | Guardrail |
| --- | --- | --- | --- | --- |
| Slots selling, 7-period avg | 25.0 (own best 29) | ≥ 30 | 1 | cash ≥ 120 at every close |
| Stocked slots, median at day end | 33 (latest 36) | ≥ 60 (ceiling 72) | 2, leads slots selling | depot read before each fill; only products the depot holds |
| Units, 7-period avg | 109.0 | ≥ 125 (own best 125.3) | 3, follows slots selling | never sell below unit cost |
| Stocked slots with no price, at close | not yet charted | 0 at every close (a rule, not an aim, until charted) | 1, process | a stocked slot unpriced past the next working day is a missed day in the pulse |

**Capacity split (480 min, 09:00–17:00):**
- Worker fills (restock calls, with depot read first): 370 min (77%). First claim. Only products the depot holds.
- Stocked slots with no price (set_price): 60 min (13%). Stocked, unpriced slots only.
- Orders placed and unit cost (order step, quote checks): 42 min (9%).
- Reserve for runs past 16:30: 8 min (2%). Marketing 0.

**Guardrails (carried forward):**
- Cash ≥ 120 after each order and at every close.
- No fill without a depot read. A failed fill costs 45 min.
- Order step by 10:00. No order above 40% of cash or above the lowest same-week quote.
- If reads or pricing run over, cut optional reads first, then quote-check extras; never a set_price on a stocked slot, a fill, or the reserve.
- Fewer than 6 fills on 3 working days: the next pulse considers a diagnosis.

**Log this point (required to judge the redesign):** minutes per restock call and slots per call (the batch test); stocked-but-unpriced slots at each close; fills per working day; depot cover per product; each day's work.jsonl line.
