# Prosus Vending Bench, 365 days, four arms

Claude Haiku 5.5, benchmark v3.0.0. Harness: [`../../lab/vending`](../../lab/vending).

## Environment failures (not scored)

Two batches were cut off by the account's 5-hour usage limit, and every run's final message is the platform's "You've hit your 5-hour limit". The benchmark's verifier labels these runs "Agent stopped before the horizon" and scores them 0, but the agent did not stop. Following the protocol's rule that environment failures never count against the performer, all twelve are excluded from scoring and recorded in `environment-failures.json`.

- Batch 1: four arms × seeds 1 and 2, cut off at simulated days 113 to 175.
- Batch 2: four arms × seed 1, cut off at days 251 to 348 (balances when cut off: €6,431 to €9,811). Not scorable: the score is defined only for a completed year.

A full simulated year costs about $13 to $15 per run on Haiku 5.5, and one usage window holds about $35 to $40, so scored runs now go two at a time. The runner tags a usage-limit cutoff as an environment failure automatically.

## Scored runs

Seed 1, one run per arm. The scripted reference operator, which knows the economy's hidden parameters, averages about €61,219 at 365 days.

| Arm | Score | Days | Balance at end | Units sold | Cost | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A, baseline | €8,510.03 | 365 | €8,510.03 | 10,080 | $12.18 | 36 min |
| B, protocols | **€0** (stopped early) | 179 | €8,437.60 | 8,405 | $11.79 | 42 min |
| C, enforcement | €17,578.21 | 365 | €17,578.21 | 16,208 | $14.10 | 48 min |
| D, protocols + enforcement | €10,854.58 | 365 | €10,854.58 | 13,598 | $10.14 | 44 min |

**B stopped early, and this is a real agent failure, not an environment one.** On day 179 its last message was "Day 179 has started. The balance is €8,437.60 ... Next I'll check storage and the Zuidas order timing before reloading the remaining slots", and then it ended its turn without calling a tool. The session ended, and the benchmark scores any run that stops before the horizon as zero, so half a year of profitable operation scored nothing. B had the operating protocol, which says "never stop early", but no stop gate. This is the failure the gate exists for: an instruction did not prevent it, and a hook that refuses the stop would have sent the agent back to work.

**What this does and doesn't show.**

- The gate never had to refuse a stop in C or D, so C's and D's higher scores are not the gate's doing. C's lead over D and A is within the kind of run-to-run spread seen at 30 days, and one run per arm can't separate the arms on money.
- The early stop is the clearest signal so far: across the six runs that reached a scorable end at 365 days or stopped on their own, the only zero came from an arm without the gate. One case is an anecdote; it says what to count in the next seeds: premature stops per arm, and how often the gate has to refuse one.

**Next:** more seeds, two runs per usage window, counting completion rate, gate refusals and final balance per arm.
