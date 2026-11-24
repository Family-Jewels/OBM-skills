# Instructions for the worker (assembled by the system each period from swarm/controls.md and swarm/aims.md; do not edit)

Controls set the bounds; aims say what to push within them. When they conflict, the controls win. To challenge a control, say so in your log: the next review will file it as a request.

## Controls (risk branch)

# Controls (risk branch; owned by the controls owner)

Bounds the worker stays within. Controls win over aims. Each control names its risk and a review point.

- Before any order_goods call, open the T-0002 comparison table itself and confirm (a) it exists (at least two suppliers, each priced at two quantities, with validity dates), (b) every offer you would order from is unexpired: its valid_through_day is later than today, and (c) the row each such offer rests on is in the table, dated on or before today, and today's log cites that row's line. Do not rely on the board's task status, which lags. If the table is missing, an offer has expired, or a row is absent, do not order: on that same working day, as your first step, re-run check_offers and record the new quotes with new validity dates in the table, then order. Do not wait for the weekly cycle to do this. Meanwhile you may restock from stock on hand, within the restock ceiling in the next control. Write each order's line in the table at once after placing it. Where a finding's summary and its table disagree, the table governs: re-count from the table rows any supplier you name as cheapest before ordering. | guards: stock bought before the supplier comparison, at a price quoted on expired offers, or on a miscounted summary, locking cash the reserve needs (unit_cost_paid_30d; cash ≥ 120); an order placed with no quote row present at the time (PO-1023, day 71), so the record cannot show what it was bought on; purchasing stalled for days on an expired quote | review at point 13 | from REQ-001, D-001, REQ-007, REQ-017 (D-004), REQ-010 (D-005; restock clause revised for D-007 by C-006), REQ-038 (A-002), REQ-051 (A-003), REQ-056 (D-013)
- Price pass first, then restock, with the 216-minute restock ceiling as a mark, not a stop: before the day's first restock_machine trip, if no set_price pass has run today (count only set_price calls made today; yesterday's pass does not count), run the price pass first: one set_price for each slot that holds stock, as today's machine inventory shows it (5 to 7 slots now, about 5 min each, so about 25 to 35 min). Then restock. Until the day's restock minutes reach 216 (45% of the 480-minute day), restock freely. Past 216, restock continues while minutes remain, once the price pass and any swap the aims call for are done, up to the 480-minute day. Before each trip past 216, if the order cycle is due today and its gate is open (control above), keep 50 minutes for check_offers and order_goods. The 35% restock share is an aim for the improvement branch to restate, not a bound. | guards: restock taking the day's time before price setting or a swap (price 5–9% vs 25%; swaps 0% vs 15%), so the price moves the aims need are not made (cash ≥ 120; the top measure); restock taking the minutes a due order needs, starving purchasing (D-014) | review at point 13 | from D-007 (REQ-010); D-009 (REQ-010 and REQ-032); D-010 and D-011 (REQ-010, REQ-037, REQ-041); REQ-050 (A-003); REQ-057 (D-014)
- A log line that states a day's sales copies the figures from the get_sales_report output you read that day and carries that report's date. Do not log a day's sales figure you did not read that day, and do not log a figure under another day's date. The same holds for quotes and orders: a T-0002 row or log line states only quotes obtained and orders placed on that day, never a future-dated quote or order (a plan such as "re-quote on day N" is not a quote). | guards: the record carrying another day's sales as this day's, which the price decisions then read; a quote or order written before it exists, which the order gate then reads as orderable | review at point 13 | from D-010 (REQ-041; cause of the day-48 mislabel not yet established); REQ-049 (P-011); REQ-056 (D-013)

## Aims and capacity split (improvement branch)

Aims for days 78-84 (point 12). Version 8, day 80, after redirect S-005 (AS-005). Old aims: history/aims.v7.md.

Constraint: restock fills at the 216-minute ceiling (controls.md). Four fills a day at 45 minutes each; depot stock covers the empty slots. Worker time is not the limit (about 170 minutes a day idle). Purchasing feeds the depot and is due now: last order day 73.

| Driver | Now (latest) | Aim for days 78-84 | Guardrail |
| --- | --- | --- | --- |
| slots_selling | 14 at day 80; 7-day mean 12.6 (own best 14.43) | 14 as the 7-day mean | Restock best sellers first, only to slots with depot stock on hand; stop at the 216-minute ceiling |
| Supplier purchasing | 4% of the day (plan 20%) | One order cycle this week, placed before any product's depot falls under one fill (10 units); 10% of the day (48 minutes) on order days | Order gate in controls.md: comparison table and unexpired offers before any order_goods |
| revenue_per_slot | 11.89 at day 80; 7-day mean 10.55 (own best 10.57) | 11.0 as the 7-day mean | Price at or above unit cost: unit_cost_paid_30d 1.116 at day 80 and rising; units per slot-day not falling |
| Top measure: cash | 4,627.93 at day 80 | Floor and aim lines are set by the system; no aim here | Cash ≥ 120 at every day close |

Price pass on every stocked slot each day, before the first restock trip, and before the day closes. Restock trips go only to slots with depot stock on hand.

Basis: every share is a percent of the 480-minute day; minutes = share × 480. The restock ceiling (216 minutes, 45%, controls.md) governs the day's maximum.

## Capacity split
- 45% restock fills, from depot stock only: restock_machine
- 15% price setting and tests: set_price
- 10% supplier purchasing, inside the order guardrail: check_offers, order_goods
- 16% reads and admin: get_status, get_sales_report, get_machine_inventory, get_storage_inventory, read_notes, write_note, list_emails, read_email, set_reminder, get_marketing_report
- 14% slack: none

Order of the day: get_status and get_storage_inventory, then get_sales_report, then set_price on every stocked slot, then check_offers and order_goods if an order cycle is due (inside the order guardrail), then restock fills within the depot stock shown and under the 216-minute ceiling, then the remaining reads and notes.

Methods: swarm/spec.md and swarm/rules/.

Methods: swarm/spec.md and swarm/rules/.
