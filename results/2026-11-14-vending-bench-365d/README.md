# Prosus Vending Bench, 365 days, four arms

Claude Haiku 5.5, benchmark v3.0.0. Harness: [`../../lab/vending`](../../lab/vending).

## Environment failures (not scored)

Two batches were cut off by the account's 5-hour usage limit, and every run's final message is the platform's "You've hit your 5-hour limit". The benchmark's verifier labels these runs "Agent stopped before the horizon" and scores them 0, but the agent did not stop. Following the protocol's rule that environment failures never count against the performer, all twelve are excluded from scoring and recorded in `environment-failures.json`.

- Batch 1: four arms × seeds 1 and 2, cut off at simulated days 113 to 175.
- Batch 2: four arms × seed 1, cut off at days 251 to 348 (balances when cut off: €6,431 to €9,811). Not scorable: the score is defined only for a completed year.

A full simulated year costs about $13 to $15 per run on Haiku 5.5, and one usage window holds about $35 to $40, so scored runs now go two at a time. The runner tags a usage-limit cutoff as an environment failure automatically.

## Scored runs

Seed 1. The scripted reference operator, which knows the economy's hidden parameters, averages about €61,219 at 365 days.

| Arm | Final balance | Completed | Cost | Turns | Time |
| --- | ---: | --- | ---: | ---: | ---: |
| A, baseline | €8,510.03 | 365 of 365 days | $12.18 | 1,984 | 36 min |
| D, protocols + enforcement | €10,854.58 | 365 of 365 days | $10.14 | 2,141 | 44 min |
| B, protocols | pending | | | | |
| C, enforcement | pending | | | | |

D's stop gate never had to refuse a stop. One seed per arm is a lead, not a result: at 30 days the same seed varied by about €600 between runs.
