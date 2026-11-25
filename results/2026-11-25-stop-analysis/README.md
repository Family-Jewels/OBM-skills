# Stop analysis: why the working agent ends its day early (base v3, six runs)

Read-only analysis of the working agent's full transcripts from the six base v3 runs (seeds 1–4, including the two runs
cut by a usage limit): 1,803 working days. A day counts as ended early when the agent called `wait_for_next_day` with
more than half of its 480 working minutes left. Minutes come from the simulator's own clock in each tool result.

| Quarter | Days | Ended early | Median minutes used | Median context per call |
| --- | ---: | ---: | ---: | ---: |
| 1 (days 1–91) | 522 | 52% | 225 | 277k tokens |
| 2 | 505 | 60% | 100 | 549k |
| 3 | 408 | 74% | 0 | 749k |
| 4 | 368 | 88% | 0 | 821k |

## Why it stops

Each early stop was classified by what the agent wrote that day (492 stated reasons, classified by claude-haiku-5-5
with fixed categories, then spot-checked by hand). The 705 stops with no text at all were given the last reason the
agent had stated in that run, since it usually ends several days in a row without comment.

| Cause | Share of early stops | Q1 → Q4 |
| --- | ---: | --- |
| A. Waiting on stock or deliveries (nothing in the depot to load) | 26% | 54% → 10% |
| B. Did a small batch of work, then judged the day done | 25% | 16% → 24% (33% in Q3) |
| Silent, before any stated reason in that run | 22% | 19% → 27% |
| D. Following a rule, plan, limit or self-set schedule ("refill every other day", an end-game rule) | 11% | 1% → 17% |
| E. Believes demand is low ("dead season", "lighter pace") | 6% | 1% → 14% |
| C. Management paperwork (answering reviews, logs) | 4% | flat |
| H. Unclear | 4% | |
| G. Other admin (emails, refunds, marketing) | 2% | |
| F. Saving tokens or calls | 1% | |

Early in the year, the agent mostly stops because there is nothing to load: its own orders are small and late, and
deliveries take 5–13 days. Later, it mostly stops by its own policy: a small batch and done, a schedule it set itself,
a belief that demand is low, or a rule in its spec (an end-game rule told one run to stop buying from day 333).
Stopping grows with context length, but one run's context was compacted from about 800k to 144k tokens in the last
quarter and its working minutes stayed near zero, so length alone does not explain it: the policies persisted.

## v1

v1 has no transcripts, so minutes cannot be measured. Its agent made 7.1–8.3 tool calls a day against v3's 4.6–5.4,
stocked 9–11 slots a day against 7–9, and its revenue peaked in the second quarter on four of five seeds. It shares the
pattern in a milder form. Seed 3 fell late in both arms, so part of that seed's slump may be the simulated market.

## Files

`extract_stops.py` (day ends from a transcript), `classify_stops.py` (keyword first pass), `classify_llm.py` (the
model classification), `data/` (the extracted day ends per run, the stated reasons and their labels).
