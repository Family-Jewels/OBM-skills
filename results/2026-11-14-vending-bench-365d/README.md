# Prosus Vending Bench, 365 days, four arms

Claude Haiku 5.5, benchmark v3.0.0. Harness: [`../../lab/vending`](../../lab/vending).

## Environment failures (not scored)

The first batch (four arms × seeds 1 and 2, started 2026-11-14 afternoon) was cut off in every run by the account's 5-hour usage limit, at simulated days 113 to 175. Each run's final message is the platform's "You've hit your 5-hour limit". The benchmark's verifier labels these runs "Agent stopped before the horizon" and scores them 0, but the agent did not stop. Following the protocol's rule that environment failures are never counted against the performer, all eight are excluded from scoring and recorded in `environment-failures.json`. The runner now tags this case as an environment failure automatically.

## Scored runs

In progress: seed 1, all four arms, restarted after the limit reset with a $25 cap per run.
