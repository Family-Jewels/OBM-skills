# v3 seed 1, rerun: 365 days, complete (EUR 9,787)

Arm `obm_v3`, base v3 (skills and lab identical to `skills-v3`, cf5c7cc), seed 1, claude-haiku-5-5, $40 cap. Complete:
365 days, no errors, API cost $20.60 of which reviews $1.24, 34 minutes.

The same code and seed as the first v3 run (`2026-11-19-v3-seed1`), which reached €27,938 at day 343:

| Day | First v3 run | This rerun |
| ---: | ---: | ---: |
| 91 | €5,788 | €3,145 |
| 183 | €11,919 | €5,247 |
| 343 | €27,938 | €8,963 |
| 365 | not reached (usage limit) | €9,787 |
| Slots stocked a day | 21.3 | 7.0 |
| Worker tool calls | 4,216 (343 days) | 1,985 (365 days) |

The rerun's worker left most of its day idle: at day 95 the charts showed a median of 55 of 480 minutes used, with 3 of the
last 7 days unused. The first run's worker used about 440. With identical code and seed, the outcome swung by a factor of
about three, so a single run says little about a version. This run is below the floor of €13,435.
