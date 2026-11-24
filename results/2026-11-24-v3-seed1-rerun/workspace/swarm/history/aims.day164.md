As of day 164, point 24 (after S-007, AS-007). Applies from day 164 to the close of day 168 (point 24, days 162-168). Replaces the day-140 aims (history/aims.day140.md). S-007's point-23 aims (days 155-161) closed before they were issued; these restate them for point 24.

Constraint: refill yield. Slots stocked at day end median 2 over the last 7 days (charts), against the ≥12 that D1 at 12.6 needs. Minutes are the symptom: the clock reads median 0 of 480, which cannot be checked from the workspace yet (AS-007). Refill only where the depot holds the product for that slot. The 408-min cap and the 72-min slack still hold.

| Driver (priority order) | Now (charts, day 164) | Aim for point 24 (days 164-168) | Share of 408 usable min | Guardrail |
| --- | --- | --- | --- | --- |
| D4 minutes used on selling work | 7-day median 0 (clock reading, unverified) | median ≥380 a day; no unused day; never above 408 | — (total) | 72 min kept unused; failed-refill minutes zero |
| D1 slots selling, 7-period average | 6.14 (own best 12.57) | ≥12.6. Path check: slots stocked at day end, median ≥12 | 270 min (6 refills × 45): empty slots with depot stock first | no slot stocked below unit cost; no duplicate slot beyond sell-through |
| D2 revenue_per_slot, 7-period average | 8.72 (own best 11.93) | ≥11.9; price at or above unit cost on every slot | 75 min: swaps, price, mix | price never below unit cost |
| D3 unit_cost_paid_30d | 1.188, level | no aim; not rising | 63 min: orders and reads | quotes at equal quantity; no order that takes cash below EUR 120; cover = lead time + 7-day cycle |
| Slack | — | none | 72 min, kept unused | no extra calls |
| M0 final cash (top measure) | 4,105.81 at close of point 23 (day 161); floor line 5,848 at point 23 | ≥4,846 at close of point 24 (latest × 1.18); the system's floor line governs | — | cash ≥ EUR 120 every day |

Notes: read this file at the first action of each point. Before each refill, check the depot holds the product for that slot; if not, skip the slot and log it. Log each day's minutes in log/progress.md so the clock reading can be checked. Daily order: unchanged (sales read and bank first; refills first, depot-checked; then swaps and price/mix; then orders and reads; stop at 408 min).

Known limit: D1 ≥12.6 is not reachable at the current refill yield (AS-007). Design change needed: yes.
