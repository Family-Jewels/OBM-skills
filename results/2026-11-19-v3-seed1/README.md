# v3 seed 1: the Strategist (Vending Bench, 365-day run, stopped at day 343)

Arm `obm_v3`, seed 1, claude-haiku-5-5, $40 cap. The run hit a usage limit at day 343, so it is reported, not scored.

| Arm (seed 1) | Cash at day 343 | Final (day 365) | API cost + reviews | Slots stocked a day |
| --- | ---: | ---: | --- | ---: |
| v3: Strategist, no experiments | €27,938 | not reached | $36.08 + $1.72 | 21.3 |
| v1: skills, floor only | €14,234 | €15,006 | $18.08 + $1.03 | 10.75 |
| v2: experiments | €11,047 | €11,852 | $12.21 + $1.18 | 9.32 |
| /plan + /goal, native | €10,547 | €10,902 | $12.79 + $0.69 | 8.02 |

v3 doubled v1 at day 343, mainly by spending the worker's idle time on keeping twice as many slots stocked, and clears the
floor rule (no run below v1's worst five-seed run, €13,435). One provisional run, at twice v1's cost.

What it exposed (fixed in v4): one redesign slot served diagnoses and design changes, so 15 diagnoses and 14 design-change
requests were still queued at the end; from S-002 to S-017 the Strategist repeated the same request (restocking costs 45
minutes a slot) with no reply. Redesigns R-P-013 and R-P-019 planned a batching test whose result never reached a record.
Aim updates took 3-7 simulated days.

Files: `result.json`, `cadence.jsonl` (every engine event), `workspace/swarm/` (all records, aims, charts).
