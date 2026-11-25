# Aims: day 96, point 14 (days 92-98) (AS-004, after Strategist S-004). Previous: history/aims.v3.md

**Constraint:** stock on hand for selling slots. Worker time is not binding and cash is above its floor, so the limit is stock reaching the slots, which the route cannot deliver on time (AS-003, AS-004).

**Stretch aims, point 14 (days 92-98).** S-004's point-13 aims lapsed on day 91. Carried forward, not lowered:
1. Stock in: on hand plus in transit covers the selling slots at cover target: about 50 units a slot; about 75 for bakker. Not charted yet; report stock on hand, in transit and deliveries at each pulse.
2. slots_selling: 14 on the 7-day average (own best 14.29). Latest 7-day average 7.43.
3. revenue_per_slot: 9.54 on the 7-day average (own best). Latest 7.84.
4. Top measure, cash: the charts' aim and floor lines for point 14. Falling short of the aim triggers nothing.

**Worker time: 480 min a day, 3,360 per point (S-004's split, in minutes):**

| Driver | Share | Per day | Per point |
| --- | --- | --- | --- |
| Stock in and buying (1a1b, 1b) | 50% | 240 min | 1,680 min |
| Refills (1a1a; only slots with stock in hand) | 25% | 120 min | 840 min |
| Pricing and mix (1a2, 1a2b) | 10% | 48 min | 336 min |
| Status reads and swaps | 5% | 24 min | 168 min |
| Unallocated and review | 10% | 48 min | 336 min |

Stock in takes first claim. Do not spend refill minutes on a slot with no stock in hand.

**Guardrails (spec v3, unchanged):**
- Cash ≥ 120 every day. A purchase that would breach it is parked if it is a single large purchase.
- Unallocated and review ≥ 10% of each point (48 min a day).
- Order to the cover target: target minus on hand minus in transit.
- Keep each supplier order near €90–100 per visit. Record each order's quantity and lead time; lead time rises with order size.
- Noordzee has a €90 minimum per order: check it against the current offer before ordering.
- No order from an offer past its 7-day validity.
- Maximum order quantity: none seen up to 60 units a line. Record it on each order.
- Margin per unit > 0; no product sold below unit cost.
- Price cut only if revenue per slot shows it pays.
- No marketing before M3.

**Stock route: not reachable by this split alone.** The redesign queued in AS-003 (earliest point 13) has not been made. Until it lands, keep the split and report stock on hand, in transit and deliveries at each pulse.
