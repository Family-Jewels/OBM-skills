# Swarm spec: Prosus Vending Bench, 25-day run   Version 1

## Goal
Maximise the bank balance at the end of simulated day 25, starting from EUR 1,500, while keeping the business solvent (no bankruptcy; no run of more than 10 consecutive unpaid spot-fee days). Receiver: the owner of the account. Unfinished or bankrupt runs score zero.

## Driver tree
Final balance = opening cash + sum of daily (revenue − goods cost − marketing − spot fee) + card receivables settled at end. Inventory is not money, so unsold stock on the last days is worth zero.

| Measure | = made of | Ground-truth source | Better | Push on now? |
|---|---|---|---|---|
| Final bank balance (score) | cash_gain_7 accumulated; card receipts settled at end | bank balance from get_status; end-of-run settlement | Higher | Top; read, never aimed at directly |
| cash_gain_7 | cash(t) − cash(t−7) | system chart, from bank ledger | Higher, and positive every 7 days | Watch |
| Revenue (per day) | units sold × realised price | get_sales_report (per location, per machine) | Higher | Yes, via the two drivers below |
| slots_selling | slots that have stock AND a price | get_machine_inventory, all six machines | Higher up to demand; not a goal in itself | Yes, but only where revenue_per_slot holds |
| revenue_per_slot | revenue ÷ slots_selling | system measure, from sales ledger | Higher | Yes, primary lever for capacity decisions |
| units | units sold per day | sales ledger | Higher at a positive margin | Yes |
| Units per slot (demand captured) | units ÷ slots_selling | sales ledger ÷ inventory ledger | Higher | Yes: product choice and placement |
| Realised price per unit | price set × (1 − discount), from sales ledger | sales ledger | Set where units per slot stays high | Yes: pricing, tested slot by slot |
| Gross margin per unit | realised price − landed unit cost | sales ledger minus order receipts (actual cost after payment) | Higher, and above zero | Yes: supplier choice and check_offers before ordering |
| Landed unit cost | order receipts ÷ units received | order receipts (NEEDS INSTRUMENTATION: operator keeps a receipts log in notes; system does not chart it) | Lower | Yes |
| Fixed and discretionary costs per day | spot fee (EUR 12) + marketing + trip time | bank ledger; get_marketing_report | Lower for marketing unless it lifts units | Marketing only with measured lift |
| Operator time used per day | restock 45 min, swap 30 min, reads and price changes | the clock | Used on the highest-value slots first | Yes: schedules trips to the best revenue_per_slot machines |
| Cash headroom | cash − reserve | bank ledger | Stays above reserve every day | Guard, not a target |
| Unpaid spot-fee days, consecutive | count of days the fee was not paid | bank ledger | 0 | Guard, must never reach 10 |

Seasonality check: revenue_last_7 against revenue_same_7_a_month_earlier. Note: the one-month-earlier comparison has no data in a 25-day run, so the system reports it as unavailable until day 38; do not wait for it. Use the same-period sales report for weather and weekday effects where the sales report gives them.

Push first, in order: (1) fill the slots that sell at positive margin, (2) raise units per slot through product mix and price, (3) cut landed cost through supplier choice, (4) marketing only once a location's units have been measured before and after a campaign.

## Exemplar
Scripted reference operator (benchmark), which knows the economy's hidden parameters: about EUR 3,228 at day 30 and EUR 61,219 at day 365, from EUR 1,500.
- Caveat 1: this run ends at day 25, and the exemplar figures are at days 30 and 365. There is no day-25 figure. A geometric interpolation between day 0 (1,500) and day 30 (3,228) gives roughly EUR 2,800 at day 25. This is an estimate, not a measured point. Use it as a pace marker, not a target.
- Caveat 2: the exemplar has hidden parameters the swarm cannot see. Its numbers show what is possible; they do not tell the operator what to do. Do not try to infer hidden parameters as a substitute for measuring the sales ledger.
- Aims rise once reached. None is a ceiling.

## Done means
1. At end of day 25: bank balance is as high as the operator can make it. Ground truth: bank balance at settlement, with card receipts settled.
2. Cash never falls below reserve (EUR 200) on any day. Ground truth: daily bank ledger.
3. No run of 10 or more consecutive unpaid spot-fee days. Ground truth: bank ledger.
4. Every restock and price change is traceable to a sales-ledger or check_offers read taken that day. Ground truth: operator log in notes.
5. At day 25: no stock is bought that cannot sell before the end; no order is open. Ground truth: order receipts and final inventory.
Time bound: day 25, 17:00.

## Open questions
- Price response per product per location (AI-LOUNGE and MAIN-LOUNGE are price-sensitive; AI-HOUSE less so). Learn from get_sales_report across days; do not assume.
- Whether a second drinks or snack slot at the same product adds units or only capacity (task statement: duplicates share demand, extra slots add capacity only). Test once with one extra slot, then judge by units per slot.
- Marketing lift size. Unknown until measured.

## Milestones
| ID | Accomplishment | Passes when | Budget |
|---|---|---|---|
| M1 (days 1–3) | End-to-end loop: every one of the six machines has stocked, priced slots that sold at least once; cash above reserve | get_sales_report shows units > 0 at all six machines by day 3; cash ≥ EUR 200; fee paid | ~30% of opening cash in stock, the rest held as reserve |
| M2 (days 4–12) | Positive-margin operation running everywhere: slots_selling set by revenue_per_slot; supplier choice set from check_offers | Every selling slot has realised margin > 0 on last 7 days; revenue_last_7 ≥ prior 7 days (or explained by weather/weekday) | Up to 60% of cash at any one time in open stock |
| M3 (days 13–21) | Growth from measured levers: price and mix tuned per slot; marketing only where lift is measured | cash_gain_7 positive in each 7-day window; units per slot not falling | Marketing capped at EUR 100 total unless measured lift justifies more |
| M4 (days 22–25) | Close-out: stop buying stock that cannot sell by day 25; settle open items; final balance read | No open orders; final stock sells or is written off; bank balance confirmed | Spend only what sells by day 25 |

## Roles
| Role | Brief | Model tier | Retry cap | Budget |
|---|---|---|---|---|
| Operator (one agent, runs the business) | swarm/rules/operator.md | Strong tier (pricing and ordering decisions carry the money) | 2 per failed action | Token budget per day: see Budgets |
| Pulse auditor (system) | obm-swarm-auditor | System-run | n/a | n/a |
| Diagnostician (system) | obm-swarm-diagnostician, when a review asks | System-run | n/a | n/a |

## Checks
| Stage | Measure | Can it be passed without the goal? |
|---|---|---|
| M1 | Units > 0 at all six machines by day 3 | Yes, if the sold units are cheap and priced at a loss. Add: margin > 0 on those units. |
| M2 | Margin > 0 on every selling slot; revenue_last_7 vs prior 7 | Revenue can rise while margin falls. Add: cash_gain_7 positive. |
| M3 | cash_gain_7 positive each window | Could be passed by stopping marketing and cutting stock. Acceptable: that still raises the balance. |
| M4 | Final bank balance, no open orders | Yes, it is the goal. |
| Guard (every day) | Cash ≥ EUR 200; unpaid-fee run < 10 | Passing by holding cash and selling nothing fails the goal; the guards only stop insolvency. |

## Budgets
- Money: spend is capped by cash above reserve (EUR 200). Cash never goes below reserve on purpose.
- Stock: no more than 60% of cash in open stock at any time from M2 on.
- Marketing: EUR 100 total unless measured lift shows otherwise.
- Reserve: 15% of opening cash is held back from stock purchases (EUR 225); the EUR 200 guard is the hard floor.
- Operator time: 8 working hours per day. Plan trips before reading. Each restock is 45 min, each swap 30 min. Read first, then act, and take the highest-revenue-per-slot trips first.
- Review share: the auditor pulse uses no more than about 30% of the operator's effort in any review window.
- Retry cap: 2 per failed order or failed action; after that, record the failure and move on.

## Cadence
| Measure or role | Trigger | Output |
|---|---|---|
| Daily measures (cash, revenue, units, slots_selling, revenue_per_slot, revenue_last_7, revenue_same_7_a_month_earlier) | every simulated day | swarm/metrics_system.md |
| Charts: cash_gain_7, revenue, slots_selling, revenue_per_slot, units | every simulated day, with limits computed by the system from its own data | swarm/charts.md |
| Operator daily log (orders, receipts, prices, marketing) | end of every day | notes (write_note) |
| Pulse audit (short review of charts) | every 5 simulated days: days 5, 10, 15, 20, 25 | audits/ pulse note |
| Full audit | every 50 days, at milestones, and before done. Under 25 days, the day-25 pass is the only full audit, run at the close-out. | audits/ full audit |
| Immediate audit | any chart signals a change in the wrong direction (chart reports a shift beyond its computed limit against the direction we want) | audits/ note |
| Diagnosis | when a review asks for it | audits/D-NNN.md |
| Redesign | after a diagnosis or audit that finds the design is the cause; spaced at least 20 days apart | swarm/history/spec.vN.md, then update this file |

## Decision rights
Swarm (operator) decides: which products to stock in which slot; prices; supplier choice within the budgets above; order sizes; when to restock, swap or clear a slot; marketing within the EUR 100 cap; when to stop buying for close-out.

Parked (raised in the next pulse, not decided alone): any order that would take cash below EUR 200; any marketing spend beyond EUR 100; any change to the goal, to the done criteria or to the reserve; any supplier that asks for prepayment outside normal terms; any action that is irreversible and not in the budgets above.

## Out of scope
- Long-term growth beyond day 25 (the exemplar's day-365 figure does not apply to this run).
- Negotiating new long contracts.
- Any use of verifier, simulator internals or non-business tools.
