# v1.1 seed 1 (Vending Bench, 365 days)

Arm `obm_v11` (engine v1.1 at 9a27318), claude-haiku-5-5, $40 cap. Completed all 365 days, no error.

| Measure | v1.1 seed 1 | v1 seed 1 |
| --- | --- | --- |
| Final balance | **EUR 13,457** | EUR 15,006 |
| Revenue by quarter | 7,480 / 7,160 / 6,692 / 6,678 | 9,420 / 10,035 / 7,088 / 10,115 |
| Slots stocked a day | 9.38 | 10.75 |
| API cost (all roles) | $18.91, of which reviews and checks $1.23 | $18.08 |
| Pulses / audits / diagnoses / redesigns | 11 / 7 / 6 / 5 | 37 / 7 / 8 / not counted |
| Fact checks | 18 | none (no checker ran) |

v1.1 loses this seed by EUR 1,549 and lands EUR 22 above the floor of EUR 13,435.

## What the agent did with its time

From the simulator's clock (`capacity_used_share` in `workspace/swarm/metrics_system.md`). An early end is a day with
less than half of the 480 working minutes used. v1's runs kept no transcript, so this cannot be compared with v1; base
v3 ended 52% of days early in its first quarter and 88% in its last (results/2026-11-25-stop-analysis).

| Quarter | Working time used | Days ended early | Agent context, median |
| --- | --- | --- | --- |
| 1 | 37% | 64% | 268k tokens |
| 2 | 33% | 71% | 536k |
| 3 | 31% | 67% | 731k |
| 4 | 31% | 71% | 178k (after compaction) |

The opportunity view and the daily note did not get the agent to use more of its day. The engine logged 322 execution
events (a day ended with time unused while something was open), almost one a day.

## Guidance and fact checks

- The designer wrote 5 entries from the brief. Reviews and redesigns proposed 28 more. The fact checks ruled on 26:
  11 accepted, 1 untestable, 14 refuted; 2 were still waiting at the end. Most accepted proposals revised existing entries
  (G-001 three times, G-008 four times, G-003 once), so the library ended with 9 entries
  (`workspace/swarm/guidance/index.md`). Refuted ones are kept with their reason in `guidance/refuted/`.
- Refutations were specific, for example a claim that batches were "bought at recent higher prices" against the
  received prices in the state snapshot.
- **The agent wrote no notes of its own**, so the check of its own policies (R5) had nothing to check. Its beliefs lived
  only in its conversation. The checker quoted 149 claims from proposed guidance instead, and the engine wrongly sent 15
  of them to the agent as checks of "your note". Fixed for later seeds (706eaa5).

## Reviews

- Mean lag from the event or signal that called a review to its delivery: **19.9 days**. Reviews run while the simulator
  keeps going, at a day every few seconds.
- Only 11 pulses ran (v1: 37). Only one pulse or audit runs at a time, and audits held the slot for long stretches.

## Fixed after this run (general)

- 706eaa5: only files the agent wrote count as its notes.
- e52a8e2: underscores inside names are kept when the engine reads records (this run's stamps show `metricssystem.md`).

Files: `result.json`, `cadence.jsonl` (every engine event), `workspace/swarm/` (design, guidance, checks, audits,
hand-offs, charts, measures).
