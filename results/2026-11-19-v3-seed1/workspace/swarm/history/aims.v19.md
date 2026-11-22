As of day 276 (after S-013), for point 40: days 274–280. Record: audits/AS-013.md. Supersedes the point-37 aims (history/aims.v18.md). Design change needed: yes (the restock step must change if restock stays at 45 min per slot; see AS-013).

**Constraint: worker time (480 min a day), 95% used (455 min median). Output per minute is the limit.** Idle capital (about 21,400) and 35 empty slots are symptoms. Restock minutes per call and slots per call are not charted, so the size of the gap is unknown.

| Driver (spec terms) | Now (day 273–276) | Stretch aim, point 40 | Priority | Guardrail |
| --- | --- | --- | --- | --- |
| Slots selling, 7-period avg | 21.9 (own best 29) | ≥ 28 | 1 | cash ≥ 120 at every close |
| Stocked slots, median at day end | 33 (latest 37) | ≥ 60 (ceiling 72) | 2, leads slots selling | depot read before each fill; only products the depot holds |
| Units, 7-period avg | 99.9 | ≥ 115 (about 4.1 per selling slot at 28) | 3, follows slots selling | never sell below unit cost |
| Stocked slots with no price, at close | not yet charted | 0 at every close (a rule, not an aim, until charted) | 1, process | a stocked slot unpriced past the next working day is a missed day in the pulse |

**Capacity split (480 min, 09:00–17:00):**
- Worker fills (restock calls, with depot read first): 360 min (75%). First claim. Only products the depot holds.
- Stocked slots with no price (set_price): 60 min (13%). Stocked, unpriced slots only.
- Orders placed and unit cost (order step, quote checks): 42 min (9%).
- Reserve: 18 min (4%). Marketing 0.

**Guardrails (carried forward):**
- Cash ≥ 120 after each order and at every close.
- No fill without a depot read. A failed fill costs 45 min.
- Order step by 10:00. No order above 40% of cash or above the lowest same-week quote.
- If reads or pricing run over, cut optional reads first, then quote-check extras; never a set_price on a stocked slot, a fill, or the reserve.
- Fewer than 6 fills on 3 working days: the next pulse considers a diagnosis.

**Log this point:** minutes per restock call and slots per call (the restock batch test); stocked-but-unpriced slots at each close; fills per working day; depot cover per product.
