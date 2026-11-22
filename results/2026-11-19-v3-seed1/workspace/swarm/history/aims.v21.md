As of day 303 (after S-015), for point 44: days 302–308. Record: audits/AS-015.md. Supersedes the point-42 aims (history/aims.v20.md). Spec (version 10) and rules unchanged here. Design change needed: yes (see AS-015: the restock step is the constraint and cannot reach the stocked-slot aim as the work is done).

**Top measure:** cash 24,576 vs floor 31,393 (required x1.11 per point). Celeration is collecting (2 points in the new phase).

**Constraint: worker time (480 min a day). Median 455 min used (95%), 25 min idle. Output per minute is the limit.** Idle capital (24,456, 7% used) is a symptom.

| Driver (spec terms) | Now | Stretch aim, point 44 | Priority | Guardrail |
| --- | --- | --- | --- | --- |
| Slots selling, 7-period avg | 23.9 (own best 29) | ≥ 30 | 1 | cash ≥ 120 at every close |
| Stocked slots with no price, at close | not yet charted | 0 at every close (a rule until charted) | 1, process | a stocked slot unpriced past the next working day is a missed day in the pulse; never a set_price cut on a stocked slot to free minutes |
| Stocked slots, median at close | 46 (up from 33) | ≥ 60 (ceiling 72) | 2, leads slots selling | depot read before each fill; only products the depot holds |
| Units, 7-period avg | 95.1 (own best 125.3) | ≥ 125 | 3, follows slots selling | never sell below unit cost; fill 18-unit rows first |

**Capacity split (480 min, 09:00–17:00), in spec terms:**
- Pricing of stocked, unpriced slots (set_price): 90 min (19%). First claim: it converts stock already paid for.
- Worker fills (restock calls, depot read first): 330 min (69%). Only products the depot holds.
- Orders placed and quote checks (order step, check_offers): 52 min (11%).
- Reserve for runs past 16:30: 8 min (2%). Marketing 0.

**Guardrails:**
- Cash ≥ 120 after each order and at every close; no order above 40% of cash or above the lowest same-week quote.
- No fill without a depot read. A failed fill costs 45 min.
- Order step by 10:00.
- If time runs over, cut optional reads first, then quote-check extras; never a set_price on a stocked slot, a fill, or the reserve.

**Log this point (required to judge the redesign):** minutes per restock call and slots per call; stocked-but-unpriced slots at each close; fills per working day; depot cover per product; each day's work.jsonl line.
