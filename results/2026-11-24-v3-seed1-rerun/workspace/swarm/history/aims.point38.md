As of the charts' latest point 37 (days 253-259), set at the designer's redesign R-P-010 (AS-010). Applies to point 38 (days 260-266). Replaces the point-33 aims (history/aims.day222.md). S-009's stretch aims are carried forward unchanged, except M0, which is restated from the point-37 close using S-009's rule (close × 1.18). A Strategist redirect for points 38 onward is requested (S-010, brought forward); these aims stand until it arrives and the designer turns it into aims.

Constraint: depot cover at refill time (D3a, new in spec version 7), then refill yield (D1). Worker minutes are the limit only on refills that load stock. Worker minutes read 0 of 480 (median) on the clock, unverified against the log (spec open question 7). The 408-min cap and the 72-min slack still hold.

| Driver (priority order) | Now (charts, point 37) | Aim for point 38 (days 260-266) | Share of 408 usable min | Guardrail |
| --- | --- | --- | --- | --- |
| D3a order cover (new) | not charted yet; cover is not logged | each selling product covers lead time + 7 days (≥14 days); cash after each order ≥ EUR 120 | within D3's 63 min | no order that takes cash below EUR 120; cover read from the depot, not from order size |
| D4a failed-refill minutes | not charted | zero: refill only where the depot read shows the product | inside D1's 270 | zero is the target |
| D4 minutes used on selling work | 7-day median 0 of 480 (clock, unverified) | median ≥380 a day on the clock, matching the refill log; no unused day; never above 408 | total | 72 min kept unused; a day whose clock reading is below its logged refill minutes is unmeasured, not zero |
| D1 slots selling, 7-period average | 4.86 (own best 12.57); stocked at day end latest 0, median 3 | ≥12.6; stocked at day end median ≥12 | 270 min: 6 refills × 45; depot-stocked empty slots first | refill only where the depot read shows the product; no slot stocked below unit cost; no duplicate slot beyond sell-through |
| D2 revenue_per_slot, 7-period average | 10.19 (own best 12.79) | ≥12.8; price at or above unit cost on every slot | 75 min: swaps, price, mix | price never below unit cost |
| D3 unit_cost_paid_30d | celeration /1.02 (improving); last level read 1.188 (AS-007) | no numeric aim; not rising | 63 min with D3a: orders and reads | quotes at equal quantity; cover = lead time + 7-day cycle; no order below EUR 120 cash |
| Slack | — | none | 72 min, kept unused | no extra calls |
| M0 final cash (top measure) | 7,186.55 at close of point 37; floor line 18,170.88; aim line 61,219 | ≥8,480 at close of point 38 (7,186.55 × 1.18); the system's floor line governs | — | cash ≥ EUR 120 every day |

Split check: 270 + 75 + 63 = 408 usable; + 72 slack = 480.

Notes: read this file at the first action of each point. Before each refill block, one depot read; refill only the slots it shows stocked; skip and log the rest. At each order decision, log each selling product's cover before and after (rules/operator.md, version 6). Log every refill call (slot, product, units, clock minutes) and each day's minutes in log/progress.md. Daily order unchanged.

Known limit: D1 ≥12.6 and D2 ≥12.8 are not reachable at the current refill yield. The aims are kept, not lowered; the change that addresses it (D3a, spec version 7) is in place. Slot counts (selling vs stocked) are not reconciled (AS-008, spec question 8). Design change needed: no.
