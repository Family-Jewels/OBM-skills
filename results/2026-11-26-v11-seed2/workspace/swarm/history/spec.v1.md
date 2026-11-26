# Swarm spec: Prosus Vending Bench   Version 1
## Goal
Finish the 365-day simulation with the highest bank balance (cash) possible. The receiver is the human who set the task (see swarm/requirements.md). The goal is never lowered.

## Driver tree
Ground truth for every row is the simulator's ledger and machine state, read by the system each period. None of these is an agent's report.

| Measure | = made of | Ground-truth source | Better | Push on now? |
| --- | --- | --- | --- | --- |
| cash (top) | cash at start + revenue − stock purchases − spot fee (€12/day) − marketing − refunds (after settlement) | ledger balance | up | Watch; it is the result of the rows below |
| revenue | slots_selling × revenue_per_slot | sales ledger | up | Yes |
| slots_selling | slots stocked AND priced AND with stock | machine state | up | Yes, first: capacity that earns |
| revenue_per_slot | units sold per slot × unit price | sales ledger | up | Yes, after slots are stocked: price learning from get_sales_report |
| margin per unit | unit price − unit_cost_paid_30d | purchase receipts and prices | up | Yes, once stock is steady: supplier terms and quantities |
| unit_cost_paid_30d | average paid per unit over 30 days | receipts | down | Monitor, push via buying choices |
| units_in_storage | units bought but not in a machine | depot state | down | Monitor: cash tied up, not earning |
| worker time (min/day) | capacity: 480 minutes, each fill ~45, swap ~30 | simulator clock | used share | Resource: use it on the work that earns |
| fixed costs (spot fee, marketing) | €12/day plus campaign costs | ledger | down | Only if returns do not cover them |

Parts that need no new instrumentation: all rows above are read by the system or the ledger. Price per unit and units per slot are derivable from the sales report; no measure is asked of the agent.

## Exemplar
The benchmark's scripted reference operator: cash €1,500 at day 0, €3,228 at day 30, €61,219 at day 365 (requirements.md). It knows hidden parameters the agent does not; treat the points as an aim, not a ceiling. Own best is the reference for any period before the exemplar is recorded.

## Done means
1. At day 365, cash read from the ledger AFTER the final card settlement is at least €61,219 (exemplar aim). The score is the cash balance itself; the aim is the bar to beat.
2. The business is still running at the end: no run of more than ten consecutive unpaid days, no bankruptcy.
3. Cash is not produced by starving the machines. Revenue over the last 30 periods exceeds revenue over the 30 before them (ledger), and slots_selling is not left at zero for a stretch.
4. No simulator or verifier internals are accessed. Only the supplied business tools are used.

Check 3 exists because cash can be held up by stopping purchases for a while; the goal is the balance at the end, read with the activity behind it, not a lull.

## Open questions
- Card takings settle a day late, and outstanding card receipts settle only at the end. Day-end cash understates the earning by one day of card sales; read the final figure after settlement. Whether the daily cash chart should be read alongside revenue is for the worker to judge.
- Whether the exemplar's day-30 point is reachable given the worker-time budget per day (a fill costs 45 minutes, a swap 30, reads and price changes minutes each). Not known; the charts will show it.
- Supplier reliability (delays, short shipments, going out of business) is not measured by the system. If receipts fall short of orders, this shows in units and slots_selling; no separate measure is planned.

## Milestones
| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 | End-to-end: machines stocked, priced and selling at all six slots' locations | slots_selling > 0 and revenue > 0 for 3 consecutive periods, within the first 8 periods | worker time only |
| M2 | Exemplar pace at day 30 | cash ≥ 3,228 on day 30 (ledger) | worker time only |
| M3 | Exemplar at end | cash ≥ 61,219 at day 365 after final settlement | worker time only |

M1 is deliberately crude: it proves the core loop works before any refinement. Later milestones are aims; the agent plans its own path.

## Opportunities
| ID | What is open | Why it matters |
| --- | --- | --- |
| O1 | Empty slots and worker time left at day end | Stocked, priced slots are the capacity that earns; unused time is capacity wasted. |
| O2 | Stock sits in the depot while slots are empty | Units in storage tie up cash without earning. |
| O3 | Cash available and worker time unused | A day that ends with time and cash idle can buy stock or run a price test. |

The system shows these to the agent as information only. It never ranks, assigns or requires them.

## Guidance
| ID | Title | Applies when |
| --- | --- | --- |
| G-001 | Cash is the score; each spend should earn back | always |
| G-002 | Stocked and priced slots are the earning capacity | O1 |
| G-003 | Stock in the depot is not income | O2 |
| G-004 | Idle day, idle cash: use both | O3 |
| G-005 | Price response is learned from sales, not guessed | always |

## Roles
| Role | Model tier | Budget |
| --- | --- | --- |
| Worker (the working agent, full autonomy) | the run's default tier | the run's token and dollar allocation |
| Designer (this role) | default | redesigns only, on evidence |
| Orchestrator | default | periodic: dispatch, pacing |
| Checker | not used unless a plan step is added | none |
| Auditor | default | pulses every 5 periods, full audit every 50 |
| Diagnostician | default | only on a signal |

The worker is the only role that acts in the simulator. The checker is not needed: the measures come from the ledger, not from a report.

## Checks
| Stage | Measure | Can it be passed without the goal? |
| --- | --- | --- |
| M1 | slots_selling, revenue | Only by selling, which is the core loop. Not a gate for anything else. |
| M2 | cash at day 30 | Could be passed by a short lull in purchases; check 3 (revenue trend) guards it. |
| M3 | cash at day 365 after settlement, business running | This is the goal; check 2 and check 3 guard against shortcuts. |

## Budgets
- Total: the run's allocated spend. Reserve: about 15% held back, never spent by the worker's own planning.
- Per-task: none beyond the run's worker time (480 minutes a day).
- Review share: no more than about 10%; the ledger is ground truth, so reviews are mostly the auditor's pulses.
- Retry cap: 2 for any failed call or order.

## Cadence
| Measure or role | Trigger | Output |
| --- | --- | --- |
| Charts | every period | swarm/charts.md (7 charts above) |
| Signals | slots_selling zero for 2 periods (from day 8); revenue zero for 3 periods (from day 8); cash below €100 (from day 3) | event note to the orchestrator and auditor |
| Opportunities | when the agent ends a period early with O1–O3 open | a short note to the agent |
| Pulse | every 5 periods | auditor's short review of charts and behavior |
| Full audit | every 50 periods, or at once on a signal that persists | audits/ record |
| Redesign | at least 20 periods apart, only on a diagnosis | swarm/history/ copy, then update in place |

## Decision rights
- Swarm decides: everything in the work: which slots to stock, what prices to set, which suppliers to order from, how many units, when to advertise, how to use worker time.
- Parked for the human: a change to the goal, a change to the exemplar, or an irreversible action outside the simulated business (none expected).

## Out of scope
- Accessing the verifier, simulator internals, or any state not given by the supplied business tools.
- Lowering the goal or the aims.
- Any real-world message or payment; marketing tools never send real messages.
