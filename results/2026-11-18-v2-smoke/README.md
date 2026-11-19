# v2 smoke run: 91 days, seed 6, 2026-11-18

A check that skills and engine v2 work end to end with a real model before the five-seed test. It is one run on a seed outside the test set (seeds 1–5), so it is not evidence that v2 is better.

Prosus Vending Bench, arm `obm_v2`, Haiku 5.5, 91 days. 91 days is the shortest horizon that still gives at least 12 weekly points.

| Measure | Result |
| --- | --- |
| Completed | 91 of 91 days; no usage-limit rejection |
| Final balance | €4,861 from €1,500 |
| For context: day-91 balance in the ten v1 runs (seeds 1–5, both arms) | €2,835 to €5,812 |
| Cost | $3.80 in all, of which reviews $0.18 |
| Worker file writes and edits | 68 (seed 5 in v1: 820 over 365 days, about 205 per 91) |
| Preflight | Clean: 7-day points, 13 across the horizon |
| Reviews | 5 pulses, 2 full audits handed over (a third still running at the end), 1 opportunity review, 1 diagnosis, 2 redesigns |
| Experiments | 5 set up and ended. Kept: full-depth restocking of fast slots, cheapest verified supplier. Inconclusive: price, product mix, marketing |

## What the first opportunity review found

At day 28, opportunity review O-001 ranked stock availability first: 19 of 72 slots selling, €1,582 idle above the reserve, and drinks selling out in about a day. That is the same opening the best /plan + /goal run found by luck in seed 5 of the five-seed test. The designer turned it into an experiment (full-depth fills, using the idle cash) with predictions. The orchestrator kept it at its end.

## Bugs found and fixed during the run

1. **Experiment dates were not parsed.** The designer wrote "Start: day 8"; the parser accepted only a bare number, so every experiment showed "no Start line". Fixed at day ~30.
2. **Points were numbered from 0,** which confused a reviewer. Labels are now 1-based, with the period range.
3. **"Selling slots" mixed two meanings:** slots stocked at day end (the resource) and slots that sold that day (a measure). The resource is renamed.
4. **A full audit blocked the weekly pulses** while it ran. The simulator runs about 5 days a minute, so a 3-minute audit held off pulses for 20 days, and from day 46 to the end no pulse ran. Pulses and audits now run side by side (fixed after the run).
5. **Overlapping experiments could hold off opportunity reviews indefinitely.** Reviews still wait while an experiment runs, but never more than 6 points (fixed after the run).

Fixes 1–3 took effect during the run, because the engine is read fresh each period. Fixes 4 and 5 apply from the next run.
