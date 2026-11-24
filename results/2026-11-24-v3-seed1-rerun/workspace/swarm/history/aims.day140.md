As of day 140 (after S-006, AS-006). Applies from day 141 to the close of point 21 (days 141-147). Replaces the day-115 aims (history/aims.day115.md).

Constraint: refill yield. Worker time is now spent (latest 405 of 480; cap 408 usable), so minutes are no longer the limit. The minutes buy too few selling slots: slots stocked at day end median 7, latest 8, against the ≥12 that R-P-005 predicted by day 133. Plan each refill minute on a slot the depot holds, priced and at margin. The 408-min cap and the 72-min slack still hold.

| Driver (priority order) | Now (charts, day 140) | Aim for point 21 (days 141-147) | Share of 408 usable min | Guardrail |
| --- | --- | --- | --- | --- |
| D4 minutes used on selling work | latest 405; 7-day median 0; 4 of 7 days unused | median ≥380 a day; no unused day; never above 408 | — (total) | 72 min kept unused; refill only where the depot holds the product; failed-refill minutes zero |
| D1 slots selling, 7-period average | 8.57 (own best 12.57) | ≥12.6. Path check: slots stocked at day end, median ≥12 | 270 min (6 refills × 45): empty slots with depot stock first | no slot stocked below unit cost; no duplicate slot beyond sell-through |
| D2 revenue_per_slot, 7-period average | 10.64 (own best 11.66) | ≥11.0; price at or above unit cost on every slot | 75 min: swaps, price, mix | price never below unit cost |
| D3 unit_cost_paid_30d | level ×1.01 per point, flat | no aim; not rising | 63 min: orders and reads | quotes at equal quantity; no order that takes cash below EUR 120; cover = lead time + 7-day cycle |
| Slack | — | none | 72 min, kept unused | no extra calls |
| M0 final cash (top measure) | 4,026.61 at close of point 20; floor line 4,587.02 | ≥4,751 at close of point 21 (latest × 1.18); floor line at point 21 about 4,954 | — | cash ≥ EUR 120 every day |

Daily order: unchanged from the spec cadence (read aims.md at the first action of each point; sales read and bank first; refills first, depot-checked; then swaps and price/mix; then orders and reads; stop at 408 min).

Known limit: D1 ≥12.6 is not reachable at the current refill yield (AS-006). Design change needed: yes.
