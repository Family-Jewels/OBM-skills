# Prosus Vending Bench, 30 days, four arms, 2026-11-14

Claude Haiku 5.5, benchmark v3.0.0, seeds 1 to 3, $5 and 30 minutes per run. Harness: [`../../lab/vending`](../../lab/vending).

| Arm | Seed 1 | Seed 2 | Seed 3 | Mean | Cost (3 runs) |
| --- | ---: | ---: | ---: | ---: | ---: |
| A, baseline | €1,929 | €2,341 | €2,012 | €2,094 | $0.79 |
| B, protocols | €1,871 | €2,433 | €2,370 | €2,225 | $1.11 |
| C, enforcement | €2,375 | €2,140 | €1,882 | €2,132 | $0.55 |
| D, both | €2,763 | €1,810 | €1,684 | €2,086 | $1.10 |

Start: €1,500. Scripted reference with privileged knowledge of the economy: about €3,228 on average (€3,303 on seed 1). A separate check on the unmodified stock harness scored €2,568 on seed 1, so the same seed varies by about €600 between runs.

- **No separation.** The variation within an arm (about ±€400) is larger than any gap between arms. Twelve runs can't detect an effect of this size.
- **Every run finished all 30 days.** The stop gate never had to refuse a stop, so at this horizon arm C is the same as the baseline in practice.
- **The protocol was followed.** Every B and D run kept `plan`, `scorecard` and `index` notes, and most kept `rules` (see each run's `notes.json`); baseline runs kept ad-hoc status notes. Following it did not change the money.
- **Next:** the 365-day variant, where context runs long and early stopping becomes possible.
