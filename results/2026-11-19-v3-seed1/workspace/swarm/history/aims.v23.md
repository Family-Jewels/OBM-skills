As of day 317 (after S-016), for point 46: days 316–322. Record: audits/AS-016.md. Supersedes the point-44 aims (history/aims.v22.md). Design change needed: yes (AS-016): the split below cannot reach the stretch aims at 45 min per restock call; the redesign is queued behind the next fault diagnosis.

**Top measure:** cash 25,564 vs floor 36,416 at point 45 (charts.md; required x1.13 per point; phase celeration x1.02). The aim line (122,438) triggers nothing.

**Constraint: worker time (480 min a day). Median 435 used (91%), 45 idle. Output per minute is the limit.** Idle capital (25,429) is a symptom.

| Driver (spec terms) | Now (S-016) | Stretch aim, point 46 | Priority | Guardrail |
| --- | --- | --- | --- | --- |
| Slots selling, 7-period avg | 22.9 (own best 29) | ≥ 30 | 1 | cash ≥ 120 at every close |
| Stocked slots with no price, at close | not yet charted | 0 at every close (a rule until charted) | 1, process | a stocked slot unpriced past the next working day is a missed day in the pulse; never a set_price cut on a stocked slot to free minutes |
| Stocked slots, median at close | 41 | ≥ 60 (ceiling 72) | 2, leads slots selling | depot read before each fill; only products the depot holds |
| Units, 7-period avg | 85.3 (own best 125.3) | ≥ 125 | 3, follows slots selling | never sell below unit cost; fill 18-unit rows first |

**Capacity split (480 min, 09:00–17:00), in spec terms:**
- Pricing of stocked, unpriced slots (set_price): up to 90 min (19%), first claim, only on unpriced stocked slots (about 3 min each), priced at the visit after each fill. Unused minutes go to fills.
- Worker fills (restock_machine calls, depot read first): 340 min (71%). Only products the depot holds. At 45 min per call, about 7 fills a day.
- Orders placed and quote checks (order step, check_offers): 40 min (8%).
- Reserve for runs past 16:30: 10 min (2%). Marketing 0.

**Guardrails:**
- Cash ≥ 120 after each order and at every close; no order above 40% of cash or above the lowest same-week quote.
- No fill without a depot read. A failed fill costs 45 min.
- Order step by 10:00.
- If time runs over, cut optional reads first, then quote-check extras; never a set_price on a stocked slot, a fill, or the reserve.

**Log this point (required to judge the redesign):** minutes per restock call and slots per call; stocked-but-unpriced slots at each close; fills per working day; depot cover per product; sell-through per slot (units sold ÷ slots stocked, by day); each day's work.jsonl lines (rule 21, minutes by activity).
