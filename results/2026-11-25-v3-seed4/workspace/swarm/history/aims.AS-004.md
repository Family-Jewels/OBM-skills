# Aims: day 96, points 14-15 (days 92-105) (AS-004, with R-P-008). Previous: history/aims.v4.md

**Constraint:** stock on hand in the selling slots. Cash is not binding (3,827 vs 120 reserve). Worker time is not binding: median 65 of 480 min a day at point 12, 3 of 7 days unused. Idle minutes become sales only when stock reaches the slots, so spend them on stock in first.

**Stretch aims, points 14-15 (days 92-105).** Carried forward from S-004, not lowered:
1. slots_selling: 14 on the 7-day average by day 105 (own best 14.29). Latest 7-day average 7.43.
2. revenue_per_slot: 9.54 on the 7-day average (own best). Latest 7.84.
3. Stock in: on hand plus in transit covers the selling slots at cover target: about 50 units a slot (about 75 for bakker). Report stock on hand, in transit and deliveries per point in the progress note until the system charts them.
4. Top measure, cash: the charts' aim and floor lines. Falling short of the aim triggers nothing.

**Worker time: 480 min a day. Each share is a floor for its driver, not a cap (R-P-008).**

| Driver | Share | Per day | Per point |
| --- | --- | --- | --- |
| Stock in and buying (1a1b, 1b; kanaal and noordzee first) | 50% | 240 min | 1,680 min |
| Refills (1a1a; only slots with stock in hand) | 25% | 120 min | 840 min |
| Pricing and mix (1a2, 1a2b) | 10% | 48 min | 336 min |
| Status reads and swaps | 5% | 24 min | 168 min |
| Unallocated and review | 10% | 48 min | 336 min |

Stock in takes first claim. Minutes a driver leaves unused go to refills of slots that have stock in hand. Do not spend refill minutes on a slot with no stock.

**Guardrails (spec v4, operator brief v4):**
- Cash ≥ 120 every day. A single purchase that would breach it is parked.
- Unallocated and review ≥ 10% of each point (48 min a day).
- Order the uncovered quantity: cover target minus on hand minus in transit. At kanaal and noordzee, order the full uncovered quantity on each visit, within cash headroom and the supplier's stated maximum.
- Zuidas orders stay near €120 until their lead time at size is recorded.
- Noordzee has a €90 minimum per order: check it against the current offer before ordering.
- No order from an offer past its 7-day validity.
- Record each order's quantity, stated maximum and lead time.
- Margin per unit > 0; no product sold below unit cost.
- Price cut only if revenue per slot shows it pays.
- No marketing before M3.

The €90–100 per-visit cap in earlier aims is withdrawn. It was a log pattern, not a goal rule, and it blocks the cover target.
