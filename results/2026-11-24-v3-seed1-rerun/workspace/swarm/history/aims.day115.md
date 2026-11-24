As of day 115 (after S-005, AS-005). Applies from day 115 to the close of point 17 (days 113-119). Replaces the day-95 aims (history/aims.day95.md).

Constraint: worker time as spent. Charts (day 115): 7-day median 0 of 480 min used, 4 of 7 days unused. Plan on minutes actually being spent. The 408-min cap and the 72-min slack still hold.

| Driver (priority order) | Now (charts, day 115) | Aim for point 17 (days 113-119) | Share of 408 usable min | Guardrail |
| --- | --- | --- | --- | --- |
| D4 minutes used on selling work | 7-day median 0; 4 of 7 days unused | median ≥380 a day; never above 408; no unused day | — (total) | never above 408 used; 72 min kept unused |
| D1 slots selling, 7-period average | 4.86 (own best 12.57) | ≥14 | 270 min (6 refills × 45): empty slots first | no slot stocked below unit cost; no duplicate slot beyond sell-through |
| D2 revenue_per_slot, 7-period average | 7.71 (own best 9.38) | ≥10.0 | 75 min: swaps, price, mix | price at or above unit cost on every slot |
| D3 unit_cost_paid_30d | ×1.06 per point, wrong way | no aim; falling | 63 min: orders and reads | no order that takes cash below EUR 120; cover selling slots through the 7-14 day lead time |
| Slack | — | none | 72 min, kept unused | do not spend on extra calls |
| M0 final cash (top measure) | 3,660.59 at point 16 (day 112); floor 3,317.89 | ≥4,320 at close of point 17 (latest × 1.18) | — | cash ≥ EUR 120 every day |

Daily order:
1. Read the sales report and the bank before any trip.
2. Refills first, up to 270 min: empty slots first, checked margin-positive product, depot stock confirmed. Log quantity and clock cost of each call, and slots stocked per refill-minute.
3. Then swaps and price/mix within 75 min. Price at or above unit cost. No experiments.
4. Then orders and reads within 63 min, within the EUR 120 reserve.
5. Stop at 408 min used.

Known limit: D1 ≥14 is not reachable at the current refill yield (AS-005); the aim stands as the Strategist set it, and the pending redesign changes what refill minutes buy.
