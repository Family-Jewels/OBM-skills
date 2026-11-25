# Aims: day 25 (AS-001, after Strategist S-001). Previous: history/aims.v0.md

**Constraint:** stocked slots (6 stocked at day end; 7 selling). Worker time is not the limit (median 60 of 480 min a day used). Cash is not binding now (1,428 vs 120 reserve).

**Stretch aims, rest of point 4 (through day 28):**
1. slots_selling: 24 selling by day 28 (from 7). Refills must add about 18 slots over days 25-28.
2. revenue_per_slot: at least 7.89 (own best) on 2 of 3 points while slots rise.
3. unit_cost_paid_30d: falling; each order paid within 5% of the lowest offer seen on that product.
4. Top measure, cash: at least 1,580 by day 28 (floor line); aim line 1,697.

**Worker time, per day (480) and per point (3,360), per spec Resources:**

| Driver | Share | Per day | Per point |
| --- | --- | --- | --- |
| Refills (1a1, about 6.9 refills a day at 45 min) | 65% | 312 min | 2,184 min (about 48 refills) |
| Pricing and mix (1a2) | 10% | 48 min | 336 min |
| Buying and offers (1b) | 10% | 48 min | 336 min |
| Status reads and swaps | 5% | 24 min | 168 min |
| Unallocated and review | 10% | 48 min | 336 min |

Refills take first claim. The other drivers keep their current use.

**Guardrails (from spec):**
- Cash ≥ 120 every day. A refill or purchase that would breach it waits (parked if it is a single large purchase).
- Unallocated and review ≥ 10% of each point.
- Margin per unit > 0; no product sold below unit cost; never buy below reserve.
- Price cut only if revenue per slot shows it pays.
- No marketing before M3.

**Trigger for the Designer:** if a point ends with fewer than about 40 refills despite the minutes, the refill route must change. Redesign then, not before.
