# v2 seed 1: 365 days (2026-11-19)

The first full-year run of skills and engine v2: the improvement half with experiments and opportunity reviews. It is the reason for v3.

| Seed 1 | Final balance | API cost + reviews | Stocked slots | Quarterly revenue |
| --- | ---: | --- | ---: | --- |
| Skills v1 + system reviews | €15,006 | $18.08 + $1.03 | 10.75 | 9,420 · 10,035 · 7,088 · 10,115 |
| **Skills v2 + system reviews** | **€11,852** | **$12.21 + $1.18** | **9.32** | **7,319 · 7,650 · 4,669 · 8,011** |
| /plan + /goal + system reviews | €10,902 | $12.79 + $0.69 | 8.02 | 5,676 · 9,193 · 6,551 · 5,016 |

v2 cost about 30% less than v1: the worker logged events instead of a line every day. It scored below v1's worst run in the five-seed test (€13,435), so it fails the pre-set floor rule.

## What went wrong

1. **The improvement half crowded out the safety half.** Pulses asked for a fault diagnosis 24 times, and 23 were deferred: opportunity reviews and the redesigns made from them held the single redesign slot most of the year. Each took 20 to 30 simulated days to come back, because the simulator runs about 10 days a minute. v1 ran about 8 diagnoses a year.
2. **The experiments could not detect what they tested.** They predicted effects of 5 to 20%. One machine's weekly revenue bounces by ±29% to ±96%, and each experiment had only 2 or 3 points after it started. All three completed experiments were "too small to read", and two were void. A year of experiments produced no decision.
3. **The right fix was found but not done.** Every opportunity review found idle worker time (a median of about 180 of 480 minutes a day) and depot stock beside empty slots, and named loading that stock as a known fix. It went into the rules, but nothing checked that rules were followed, and the fault diagnoses that would have caught it were deferred.

## Run notes

- An earlier start of this seed was stopped at day 122 and set aside unscored: no opportunity review had run, because of a bug fixed in commit "Fix: opportunity reviews were never run when queued experiments could not start".
- Two display changes took effect during the run: resources shown as a median over the last point with unused days counted, and a line saying how each resource is measured.
