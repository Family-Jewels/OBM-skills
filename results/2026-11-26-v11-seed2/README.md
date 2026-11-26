# v1.1 seed 2 (Vending Bench, 365 days)

Arm `obm_v11` (engine at 706eaa5: seed 1's code plus the two fixes listed in seed 1's README), claude-haiku-5-5, $40 cap.
Completed all 365 days, no error.

| Measure | v1.1 seed 2 | v1 seed 2 |
| --- | --- | --- |
| Final balance | **EUR 5,914** | EUR 14,171 |
| Revenue by quarter | 5,390 / 4,036 / 3,976 / 2,481 | 6,152 / 11,528 / 9,876 / 8,859 |
| Slots stocked a day | 6.4 | 11.5 |
| API cost (all roles) | $15.55, of which reviews and checks $0.87 | $19.58 |
| Pulses / audits / diagnoses / redesigns | 7 / 5 / 4 / 3 | 37 / 8 / 8 / not counted |
| Fact checks | 12 | none |

**This run is below the floor of EUR 13,435**, so under the fixed rules v1.1 cannot count as better than v1, whatever
seeds 3 to 5 show.

## What the agent did with its time

| Quarter | Working time used | Days ended early (under half used) | Agent context, median |
| --- | --- | --- | --- |
| 1 | 32% | 68% | 223k tokens |
| 2 | 22% | 78% | 418k |
| 3 | 22% | 78% | 573k |
| 4 | 14% | 86% | 722k |

The engine logged 356 execution events (a day ended with time unused while something was open). The agent kept orders
small and waited for each delivery: "Sales are low again, probably empty slots. PO-1063 arrives tomorrow, so I'll wait
for it." This is the pattern the base v3 stop analysis found (waiting on stock after small, late orders).

## What the diagnoses found

- D-P-005 (day 60): on 10 of 21 days, the agent used under 10% of its time while stock waited in the depot and most
  slots were empty. It names information as the main cause, and also says the designer's opportunity labels pulled two
  ways: one read as a cue to buy on idle days, another as a cue to clear the depot.
- D-A-005 (day 309): 3 of about 35 priced slots selling. Nothing in the environment shows the cost of idle capacity or how
  many days of stock are on hand, and the two charts meant to show idle time and deliveries cannot signal (the lower
  limit of capacity used is -0.66).

## Guidance and fact checks

The fact checks ruled on 14 proposals: 4 accepted, 10 refuted; 2 were still waiting at the end. The library ended with
9 entries. The agent again wrote no notes of its own, so there was nothing of its own to check; with the fix, nothing was
mislabelled as its note. Mean review lag: 17.0 days.

Files: `result.json`, `cadence.jsonl`, `workspace/swarm/`.
