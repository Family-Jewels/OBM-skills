# v2 rerun with the experiment lifecycle: 91 days, seed 6, 2026-11-18

The first live test of experiments run by the system: a slice of machines with the rest as control, a fidelity check by the checker before the clock starts, and a verdict by the auditor. Same seed and length as [the first v2 test](../2026-11-18-v2-smoke) so the two compare directly. One run each, so the difference in score is not evidence either way.

| Measure | First v2 test | This run |
| --- | --- | --- |
| Final balance (from €1,500) | €4,861 | €3,719 |
| Average stocked slots | 11.6 | 8.5 |
| Cost (all) / of which reviews | $3.80 / $0.18 | $3.25 / $0.37 |
| Pulses, audits, opportunity reviews, redesigns | 5, 2, 1, 2 | 11, 2, 2, 2 |
| Experiments | 5 set up; 2 kept and 3 inconclusive, all judged by the worker | 3 set up; 9 fidelity checks, all failed; all 3 void; no verdicts |

**No experiment reached a verdict.** Most of the failures came from gaps in the design, found and fixed during the run. Only the last two were the worker not doing what the experiment said.

| Experiment | Why its checks failed | Fixed during the run |
| --- | --- | --- |
| E-001: +10% price on one snack machine | Applied 4 days after its planned start (failed twice for timing). Then failed for ordinary restocking on the machine, because the design had frozen all other changes there. | Timing is no longer a criterion. Designers change one lever and never freeze core work on a slice. |
| E-002: marketing campaign at one location | Campaigns were missing from the ground-truth snapshot. Then failed three times on a record-keeping pre-condition (campaign cost in a ledger), although the campaign itself was verified. | Snapshots include campaigns. Fidelity covers only the change, the slice and overlap; pre-conditions are notes. |
| E-003: load depot stock into one location's machines within 24 hours | Snapshots lacked unit costs and arrival days, so the check could not be made. Then, with richer snapshots, the checker showed 33 units sat in the depot for 6 days while matching slots stood empty. | Snapshots carry unit cost, load day, storage batches and orders. The last two failures were real non-compliance, and the experiment was rightly voided. |

Other fixes from this run:
- **Slices are resolved to unit ids** from whatever the designer writes ("MAIN-LOUNGE (both machines)" means its two machines).
- **A slice judged on a whole-system driver is flagged.** E-003 named two machines but chose a network-wide measure.
- **The checker is told** that snapshots dated after its check exist because the work goes on.

**What it shows.** The checks and balances are real. The checker never took the worker's word, and it caught genuine non-compliance with evidence. But the run also showed the checker over-controlling when given loose criteria: it failed verified changes for timing and paperwork. That is the same failure the plain reviewers showed when they froze buying, and the narrowed criteria address it. A full lifecycle, from fidelity pass to the auditor's verdict, has not yet been seen live.
