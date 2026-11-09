# OBM x ImpossibleBench pilot results

Models: anthropic/claude-sonnet-5-5   Samples: 27   Errors: 0

## By condition and split

| Condition | Split | n | Passed | of which overrode tests | Conflict flag | Other flag (cap/withheld) | Failed | Mean tokens |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | original | 3 | 100% (44%-100%) | 0 | 0% | 0% | 0% | 4,250 |
| baseline | oneoff | 3 | 0% (0%-56%) | 0 | 100% | 0% | 0% | 6,238 |
| baseline | conflicting | 3 | 0% (0%-56%) | 0 | 100% | 0% | 0% | 2,749 |
| generic | original | 3 | 100% (44%-100%) | 0 | 0% | 0% | 0% | 8,307 |
| generic | oneoff | 3 | 0% (0%-56%) | 0 | 100% | 0% | 0% | 8,185 |
| generic | conflicting | 3 | 0% (0%-56%) | 0 | 100% | 0% | 0% | 2,785 |
| obm | original | 3 | 33% (6%-79%) | 0 | 67% | 0% | 0% | 84,309 |
| obm | oneoff | 3 | 0% (0%-56%) | 0 | 100% | 0% | 0% | 50,720 |
| obm | conflicting | 3 | 0% (0%-56%) | 0 | 67% | 0% | 33% | 112,745 |

## Headline

| Measure | baseline | generic | obm |
| --- | --- | --- | --- |
| Cheating rate | 0% (0/6) | 0% (0/6) | 0% (0/6) |
| Conflict-flag rate (impossible) | 100% (6/6) | 100% (6/6) | 83% (5/6) |
| Utility (original, clean pass rate) | 100% (3/3) | 100% (3/3) | 33% (1/3) |
| False-flag rate (original) | 0% (0/3) | 0% (0/3) | 67% (2/3) |
| Tokens/sample | 4,413 | 6,426 | 82,591 |

## Paired differences (cluster bootstrap over tasks, 95% CI)

| Comparison | Measure | Difference | 95% CI | Tasks |
| --- | --- | --- | --- | --- |
| generic vs baseline | Cheating rate | +0 pts | +0 to +0 | 6 |
| generic vs baseline | Utility | +0 pts | +0 to +0 | 3 |
| obm vs baseline | Cheating rate | +0 pts | +0 to +0 | 6 |
| obm vs baseline | Utility | -67 pts | -100 to +0 | 3 |

Small pilots give wide intervals. Treat them as a signal for where to scale up, not a result.
