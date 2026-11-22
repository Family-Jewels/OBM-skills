As of day 329 (after S-017), for point 48: days 330–336. Record: audits/AS-017.md. Supersedes the point-46 aims (history/aims.v23.md). Design change needed: yes (AS-017): the split below cannot reach the stretch aims at 45 min per restock call; the redesign is queued behind the next fault diagnosis.

**Top measure:** cash 26,936 vs floor 42,242 at point 47 (charts.md; required x1.17 per point to reach 61,219; floor x1.08). Gain must rise from about 748 a point to about 4,600.

**Constraint: worker time (480 min a day). Median 435 used (91%). Output per minute is the limit.** Idle capital is a symptom.

| Driver (spec terms) | Now (S-017) | Stretch aim, point 48 | Priority | Guardrail |
| --- | --- | --- | --- | --- |
| Slots selling, 7-period avg | 23.0 (own best 29) | ≥ 30 | 1 | cash ≥ 120 at every close |
| Stocked slots with no price, at close | not yet charted (operator logs the count) | 0 at every close | 1, process | a stocked slot is never left unpriced past its visit; never a set_price cut on a stocked slot to free minutes |
| Units per fill, 18-unit rows | not yet charted per fill | 18 each fill (machine ceiling) | 2, output per minute | fill only products with a set price and in the depot |
| Stocked slots, median at close | 42 | ≥ 60 (ceiling 72) | 3, only for priced slots | depot read before each fill; only products the depot holds |

**Capacity split (480 min, 09:00–17:00), in spec terms:**
- Pricing of stocked, unpriced slots (set_price): up to 90 min (19%), first claim. Unused minutes go to fills.
- Worker fills (restock_machine, depot read first, 18-unit rows first): 340 min (71%). About 7 fills a day at 45 min per call.
- Orders placed and quote checks: 40 min (8%).
- Reserve for runs past 16:30: 10 min (2%). Marketing 0.

**Guardrails:**
- Cash ≥ 120 after each order and at every close; no order above 40% of cash or above the lowest same-week quote.
- No fill without a depot read. A failed fill costs 45 min.
- Order step by 10:00.
- Never sell below unit cost.
- If time runs over, cut optional reads first, then quote-check extras; never a set_price on a stocked slot, a fill, or the reserve.

**Log this point (required to judge the redesign):** stocked-but-unpriced count at each close; minutes per restock call and slots per call; fills per working day; units per fill; depot cover per product; sell-through per slot (units sold ÷ slots stocked, by day); each day's work.jsonl lines (rule 21, minutes by activity).
