# Swarm spec: Prosus Vending Bench   Version 1

## Goal
Finish the 365-day simulation with the highest bank balance (cash). Receiver: the human who set the task (requirements.md). The goal is never lowered.

## Driver tree
| Measure | = made of | Ground-truth source | Better | Push on now? |
| --- | --- | --- | --- | --- |
| cash (goal) | opening EUR 1,500 + revenue − cost of goods paid − spot fees (EUR 12/day) − marketing spend − other outgoings | simulator bank ledger | up | via the parts below |
| revenue | units sold × average unit price, across six machines | sales ledger (get_sales_report) | up | yes: price and availability |
| units | slots_selling × units each selling slot sells per day (demand differs by location) | sales ledger | up | yes |
| slots_selling | slots that are stocked AND priced | machine state | up | yes, first |
| revenue_per_slot | revenue ÷ slots_selling | derived from ledger and machine state | up | diagnostic |
| unit_cost_paid_30d | cost paid ÷ units bought, 30-day window | supplier receipts (order_goods) | down | yes: buying at current offers and choosing suppliers |
| units_in_storage | stock at the depot not yet in a slot | depot state | down (but not to zero: empty slots earn nothing) | yes: stock what will sell |
| worker time (minutes a day) | capacity: 480 minutes; a fill costs 45, a swap 30 | simulator clock | used well, not used up | a resource, not a measure |
| capital | cash plus value of stock on hand | simulator balance | deployed where it earns | a resource |

Instrumentation gap: marketing traffic multipliers (get_marketing_report) are not charted; the swarm reads them directly when deciding campaigns.

## Exemplar
Scripted reference operator (knows hidden parameters): cash 1,500 → about 3,228 by day 30 → about 61,219 by day 365 (requirements.md). Used as aim on the cash chart. Not a ceiling.

## Done means
- At the end of day 365 the simulator reports SIMULATION OVER, with the final bank balance read from the ledger as the score.
- The business is not ended: no run of more than 10 consecutive unpaid days, and the bank never negative.
- No open customer complaint or unpaid refund left unresolved at the end (open complaints lower reputation, which lowers traffic).
- Card receipts outstanding at the end are settled by the simulator; nothing is left to chase.

The no-bankruptcy check alone can be passed by an operator that never spends; the cash check is the direct one that rewards the goal.

## Open questions
- How fast demand responds to price per location (AI-LOUNGE and MAIN-LOUNGE picky and price-sensitive; AI-HOUSE hungrier and less price-sensitive). Answer from sales reports, not assumed.
- Whether the marketing multiplier pays back at each location's footfall.
- Whether supplier discount offers (valid one week) beat the current catalogue price enough to justify order sizes.

## Milestones
| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 | First working operation: every machine that can sell has stock and a price, and revenue is reported each day | revenue > 0 on each of the first 3 days with all six machines reachable | first 3 days |
| M2 | Pricing and restocking learned from evidence | cash at day 30 at or above the exemplar (3,228), or the swarm can say from the sales reports why not | by day 30 |
| M3 | Sustained operation | cash_gain_30d positive in most 30-day windows, slots_selling kept high | through day 365 |

Milestones describe good progress; the agent chooses its path.

## Opportunities
| ID | What is open | Why it matters |
| --- | --- | --- |
| O1 | Machine slots are empty or unstocked while worker time is still spare | Revenue is capacity in use; an empty slot earns nothing and a fill is the only way to change it |
| O2 | Stock sits in storage while worker time is spare | Stock in storage is cash not earning; placing it is the cheapest sale |
| O3 | Cash is idle while machine slots are empty | Money not put to work in stock or marketing is money the machines cannot earn with |

The system shows these as information only.

## Guidance
| ID | Title | Applies when |
| --- | --- | --- |
| G-001 | Opening days: fill what can sell, then learn | always |
| G-002 | Price from sales evidence, in small steps | always |
| G-003 | Use the worker-time budget on slots that earn | O1, O2 |
| G-004 | Buy against current offers, sized to what will sell | O2, O3 |
| G-005 | Marketing as a bounded bet, read against sales | O3 |

## Roles
| Role | Model tier | Budget |
| --- | --- | --- |
| Working agent (runs the operation; full autonomy) | as configured for the run | the run's allowance |

## Checks
| Stage | Measure | Can it be passed without the goal? |
| --- | --- | --- |
| M1 | revenue > 0 on each early day | Only partly: revenue can be earned at any price; M1 is a floor, the cash check decides |
| M2 | cash at day 30 vs exemplar | No: requires cash, not activity |
| Done | final cash from ledger | No: it is the goal |

## Budgets
Total: the run's allowance, with about 15% held in reserve. Review share: no more than about 30% of spend on reviews. Retry cap: 2 per failed call.

## Cadence
| Measure or role | Trigger | Output |
| --- | --- | --- |
| all charted measures | every day | chart update in swarm/charts.md |
| early period end with O1, O2 or O3 open | event, at most every 3 days | review |
| revenue or slots_selling at zero two days | signal | immediate pulse |
| cash below 150 | signal (not before day 3) | immediate pulse |
| pulse | every 5 days | short check of charts and opportunities |
| full audit | every 50 days | direction, honesty and spend |
| redesign | no sooner than 20 days apart | spec and system.json changes |

## Decision rights
Swarm decides: all operating choices inside the simulator (suppliers, orders, prices, stocking, marketing, refunds, the order of work within a day).
Parked for the human: anything outside the task (none expected); a conflict between the goal and any rule stated in the briefing.

## Out of scope
Anything not in the simulator: real messages, real money, the verifier or simulator internals. Marketing copy is never graded.
