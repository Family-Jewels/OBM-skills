# Aims: day 118, point 18 (days 120-126) (AS-005, after Strategist S-005). Previous: history/aims.AS-004.md

**Constraint:** stock reaching the selling slots, while worker time and capital sit idle. Charts day 118: worker time median 50 of 480 min a day used (430 idle); capital 4,062 of 4,080 idle; 9 slots stocked at day end against 14 selling. The stock route cannot reach cover target within lead time (AS-003 to AS-005).

**Stretch aims, point 18 (days 120-126).** Carried from S-005's point-17 aims (days 113-119), with the stock aim made measurable.
1. Stock in: place orders on days 120-121 for the full uncovered quantity at each selling slot (cover target minus on hand minus in transit; about 50 units a slot, 75 for bakker). Aim: on hand plus in transit at least 50% of cover target across the selling slots by day 126. Report stock on hand, in transit and deliveries each day until the system charts them.
2. slots_selling: 14 on the 7-day average (own best 14.29). Held, not lowered. Charts' latest 7-period average: 4.43.
3. revenue_per_slot: 9.54 on the 7-day average (own best). Price moves only where they pay. Charts' latest 7-period average: 6.03.
4. Top measure, cash: read the charts' floor and aim lines for point 18. Not pushed directly. Falling short of the aim triggers nothing.

**Worker time: 480 min a day, 3,360 per point. Split unchanged (S-004, S-005):**

| Driver | Share | Per day | Per point |
| --- | --- | --- | --- |
| Stock in and buying (1a1b, 1b) | 50% | 240 min | 1,680 min |
| Refills (1a1a; only slots with stock in hand) | 25% | 120 min | 840 min |
| Pricing and mix (1a2, 1a2b) | 10% | 48 min | 336 min |
| Status reads and swaps | 5% | 24 min | 168 min |
| Unallocated and review | 10% | 48 min | 336 min |

Stock in takes first claim. Minutes a driver leaves unused go to refills of slots that have stock in hand. Do not spend refill minutes on a slot with no stock in hand.

**Guardrails (spec v4, unchanged):**
- Cash ≥ 120 every day. A single purchase that would breach it is parked.
- Unallocated and review ≥ 10% of each point (48 min a day).
- Order the uncovered quantity: cover target minus on hand minus in transit, within cash headroom and the supplier's stated maximum. No per-order size cap (spec v4).
- Record each order's quantity, stated maximum and lead time; lead time rises with order size.
- Noordzee has a €90 minimum per order: check it against the current offer before ordering.
- No order from an offer past its 7-day validity.
- Margin per unit > 0; no product sold below unit cost.
- Price cut only if revenue per slot shows it pays.
- No marketing before M3.

**Stock route: not reachable by this split alone.** The redesign queued since point 13 has not been made. Design change needed.
