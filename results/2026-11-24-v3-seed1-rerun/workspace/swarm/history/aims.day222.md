As of day 222 (after S-009, AS-009). Applies to point 33 (days 225-231), the next point; point 32 (days 218-224) is already read. Replaces the point-28 aims (history/aims.day191.md). The S-009 aims for point 31 closed before they could be issued, so they are restated here for point 33.

Constraint: depot-fed refill yield. A refill that finds no depot stock still costs its 45 minutes, and stocked slots are far below the level D1 needs. Worker minutes read 0 of 480 (median) on the clock, which is unverified against the operator's log (spec open question 7). The 408-min cap and the 72-min slack still hold.

| Driver (priority order) | Now (charts, day 222) | Aim for point 33 (days 225-231) | Share of 408 usable min | Guardrail |
| --- | --- | --- | --- | --- |
| D4 minutes used on selling work (constraint) | 7-day median 0 of 480 (clock, unverified) | median ≥380 a day on the clock, matching the refill log; no unused day; never above 408 | total | 72 min kept unused; failed-refill minutes (D4a) zero; a day whose clock reading is below its logged refill minutes is unmeasured, not zero |
| D1 slots selling, 7-period average | 10.0 (own best 12.57); stocked at day end latest 7, median 10 | ≥12.6 (above own best); stocked at day end median ≥12 | 270 min: 6 refills × 45; empty slots with depot stock first | refill only where the depot read shows the product; no slot stocked below unit cost; no duplicate slot beyond sell-through |
| D2 revenue_per_slot, 7-period average | 8.28 (own best 12.63) | ≥12.6; price at or above unit cost on every slot | 75 min: swaps, price, mix | price never below unit cost |
| D3 unit_cost_paid_30d | 1.188 (last read); falling, not rising | no numeric aim; not rising | 63 min: orders and reads | order covers lead time (7 or 14 days) + 7-day cycle, up to the D1 aim; no order that takes cash below EUR 120 |
| Slack | — | none | 72 min, kept unused | no extra calls |
| M0 final cash (top measure) | 6,668.42 (latest, charts); floor line 12,121.02; aim line 61,219 | ≥7,868.74 at close of point 33 (6,668.42 × 1.18); the system's floor line governs | — | cash ≥ EUR 120 every day |

Split check: 270 + 75 + 63 = 408 usable; + 72 slack = 480.

Notes: read this file at the first action of each point. Before each refill block, one depot read; refill only the slots it shows stocked; skip and log the rest. Log every refill call (slot, product, units, clock minutes) and each day's minutes in log/progress.md; the log is the record that settles the clock and the refill yield. Daily order unchanged (sales read and bank first; refills first, depot-checked; then swaps and price/mix; then orders and reads; stop at 408 min). If the depot read shows fewer stocked products than the 6 refills, the unused refill minutes stay unused; they are not moved to another driver here.

Known limit: D1 ≥12.6 is not reachable as the work is done. Refill yield (units and slots per refill) is unknown because the log has no entries after day 135, slot counts (selling vs stocked) are not reconciled (AS-008), and the clock reading is not settled (D-P-006). Design change needed: yes (see audits/AS-009.md).
