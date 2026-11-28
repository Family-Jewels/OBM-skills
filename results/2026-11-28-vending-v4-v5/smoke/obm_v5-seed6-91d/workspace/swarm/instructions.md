# Instructions for the worker (assembled by the system each period from swarm/controls.md and swarm/aims.md; do not edit)

Controls set the bounds; aims say what to push within them. When they conflict, the controls win. To challenge a control, say so in your log: the next review will file it as a request.

## Controls (risk branch)

# Controls (risk branch; written by the controls owner only; the worker reads them through swarm/instructions.md)

Limits and checks the worker stays within. Aims say what to push for inside them; controls win a conflict.

- Before each restock_machine: for each product the depot holds none of, do not restock that product today. If the depot holds fewer units of a product than the slots will sell before its supplier's quoted lead time, and no open order for it arrives within that lead time, call order_goods for it first. Restocking continues from depot stock on hand | guards: slots emptied by stock-outs when depot cover runs shorter than supplier lead time (stock-outs on days 13-14), and restock time spent filling slots from an empty depot (days 32-34) | review at point 12 | from D-002 (REQ-010); amended from D-006 (REQ-029, REQ-031); renewed by C-007
- Before each order_goods, call check_offers for that product that day, and confirm the quote ordered from has the lowest unit price among quotes whose lead time meets the cover rule above; a check, never a reason to delay an order the cover rule requires | guards: unit_cost_paid_30d above its upper limit (1.095 on day 70 against 1.07), eroding margin on each unit | review at point 12 | from D-005 (REQ-021; kept by C-005 against D-008; renewed by C-007)
- Restock minutes a day stay within the restock share in aims.md's capacity split (40% of the 480 minutes, 192 minutes now; restock_machine at 45 minutes and swap_item at 30 count together). Once the day's restock minutes reach that share, make no further restock_machine or swap_item that day; sourcing, pricing and the day close go on | guards: restock time crowding out sourcing (restock 64% of time spent against a 40% share, day 70, Source and buy 21% against 35%) | review at point 12 | from D-009 (REQ-010), REQ-015 and D-010 (REQ-031); renewed by C-007

## Aims and capacity split (improvement branch)

Aims for days 71 to 77 (point 11). Version AS-004, from strategy S-004, written day 71. Read every day.

Constraint: depot supply. Worker time is no longer the limit: the median is 290 of 480 minutes, 190 idle. Restock_machine (45 minutes a call) was 64% of time spent, but slots stocked fell (14 to 12) because the depot held too little to place. Buy first, then restock what the depot now holds. Idle minutes go to Source and buy. Cash (4,564) is not the limit.

Guardrails: cash ≥ 120 at every close; cash ≥ 144 after any order. The depot-empty check (C-002) and the order-before-restock check win any conflict with an aim.

| Driver | Now (day 71) | Aim for days 71 to 77 | Guardrail |
| --- | --- | --- | --- |
| slots_selling | 7-day average 12.4 (own best 17.71) | 7-day average at least 19 | cash ≥ 120 at every close |
| unit_cost_paid_30d | 1.095 (own best 0.91) | at most 1.02; buy at the lowest check_offers quote | unit cost < achieved price; no stock bought that cannot sell |
| revenue_per_slot | 7-day average 9.9 (own best 10.72) | 7-day average at least 11.0; price every restocked slot in the same visit | price above unit cost for each product |

Restock: at most 3 restock_machine a day, only for products get_storage_inventory shows on hand, each with an order_goods the same day. Each order states product, quantity, expected sales a day, and unit cost against achieved price.

## Capacity split
- 40% Source and buy: order_goods, check_offers, get_storage_inventory, search_web, list_emails, read_email
- 35% Restock slots: restock_machine, swap_item
- 20% Pay, price and read: set_price, send_payment, get_sales_report, get_machine_inventory, get_status
- 5% Notes and day close: write_note, wait_for_next_day

Notes: the split is a share of the 480 available minutes. Source and buy takes the idle minutes first.

Methods: swarm/spec.md and swarm/rules/.
