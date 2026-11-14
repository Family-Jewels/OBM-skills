# Swarm spec: weekly finance report service
Version: 3

## Goal
A service that turns the ledger export into the weekly finance report (PDF and CSV), delivered to the finance team every Monday.

## Done means
1. `python -m pytest tests -q` exits 0 on the main branch.
2. `report build --week 2026-W44` produces report.pdf and report.csv whose totals match `fixtures/w44_expected.csv` exactly.
3. No file in `fixtures/` or `tests/` is modified by a producer.

## Milestones
| ID | Accomplishment | Passes when |
| M1 | Ledger parser | done (passed C-5) |
| M2 | Aggregation engine | done (passed C-10) |
| M3 | Report builder (PDF and CSV) | done (passed C-17) |
| M4 | Monday delivery and week handling | delivery job runs for weeks W44-W47 with correct week labels |

## Producers
P-1, P-2, P-3, P-5 (fast tier). Checkers C-1, C-2.

## Budgets and pacing
Total 4.0M tokens; spent 2.71M; reserve 0.6M. Review share target: 30% of spend. Retry cap: 2. Stall: 3 cycles without an accepted unit on the core.

## Decision rights
Swarm decides: implementation choices inside the spec.
Parked: new credentials or accounts, anything sent outside the team, changes to done criteria.
