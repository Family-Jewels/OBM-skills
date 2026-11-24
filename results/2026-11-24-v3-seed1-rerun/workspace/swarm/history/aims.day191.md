As of day 191, point 28 (days 190-196) (after S-008, AS-008). Applies from day 191 to the close of day 196. Replaces the point-24 aims (history/aims.day164.md). S-008's point-27 aims (days 183-189) closed before they could be issued, so they are restated here for point 28.

Constraint: refill yield, not the minute count. Slots stocked at day end: 7-day median 9, latest 4, against the ≥12 that D1 at 12.6 needs. Worker minutes read 0 of 480 (median), which is not yet verified (spec open question 7). Refill only where the depot holds the product for that slot. The 408-min cap and the 72-min slack still hold.

| Driver (priority order) | Now (charts, day 191) | Aim for point 28 (days 190-196) | Share of 408 usable min | Guardrail |
| --- | --- | --- | --- | --- |
| D4 minutes used on selling work | 7-day median 0 of 480 (clock reading, unverified) | median ≥380 a day; no unused day; never above 408 | — (total) | 72 min kept unused; failed-refill minutes zero |
| D1 slots selling, 7-period average | 10.57 (own best 12.57) | ≥12.6. Path check: slots stocked at day end, 7-day median ≥12 | 270 min (6 refills × 45): empty slots with depot stock first | no slot stocked below unit cost; no duplicate slot beyond sell-through |
| D2 revenue_per_slot, 7-period average | 9.28 (own best 12.63) | ≥12.6; price at or above unit cost on every slot | 75 min: swaps, price, mix | price never below unit cost |
| D3 unit_cost_paid_30d | 1.188 (last read, AS-007); not rising | no aim; not rising | 63 min: orders and reads | quotes at equal quantity; no order that takes cash below EUR 120; cover = lead time + 7-day cycle |
| Slack | — | none | 72 min, kept unused | no extra calls |
| M0 final cash (top measure) | 5,521.87 at close of point 27 (day 189); floor line 8,085.42 | ≥6,516 at close of point 28 (5,521.87 × 1.18); the system's floor line governs | — | cash ≥ EUR 120 every day |

Notes: read this file at the first action of each point. Before each refill, check the depot holds the product for that slot; if not, skip the slot and log it. Log each day's minutes in log/progress.md so the clock reading can be checked. Daily order: unchanged (sales read and bank first; refills first, depot-checked; then swaps and price/mix; then orders and reads; stop at 408 min).

Known limit: D1 ≥12.6 is not reachable at the current refill yield, and slot counts (slots selling vs stocked) are not yet reconciled (AS-008). Design change needed: yes.
