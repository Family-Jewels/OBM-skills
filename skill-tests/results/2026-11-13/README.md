# Skill tests on Haiku 5.5, 2026-11-12 to 13

Each skill was tested alone against a plain one-line role, on the scenarios in [`../../fixtures`](../../fixtures). All runs used Claude Haiku 5.5 as isolated agents. A separate judge agent graded them against the [answer key](../../answer-key.md), seeing only random folder names. Scores are in the `scores*.json` files; `run_map.json` says which folder was which arm.

**Summary:** two skills changed decisions for the better (orchestrator, diagnostician), two made no difference to outcomes (checker, producer), and two were worse in specific ways until fixed (auditor, designer). The orchestrator also needed a fix. Three runs per arm is enough to see a pattern, not to prove one.

## Round 1: menus gave the answers away

The first version of the tests listed the situations and offered a menu of actions or categories. Both arms scored the same on every test (checker 7/7, orchestrator 9/9, auditor 5/5, diagnostician 3/3). The menus named the concepts the skills teach, so the test measured whether a model can pick the right option, which Haiku can. Those fixtures are not kept here.

## Round 2 and repeats: open-ended instructions

Three runs per arm, except checker and producer (one run each, tied).

| Skill | With skill | Plain role | Reading |
| --- | --- | --- | --- |
| Checker | 7/7 | 7/7 | Tie. Haiku already catches false reports, untested criteria, bad blocks and a manager's push to pass. |
| Producer | 7/7 | 7/7 | Tie. Both noticed the out-of-date rate table and declined to claim the criterion met. The skill arm filed a formal block. |
| Orchestrator | 9, 8.5, 8.5 of 9 | 7.5, 8, 8 of 9 | Skill better on consequences, worse on throughput (below). |
| Diagnostician | 3, 3, 3 of 3 | 2.5, 3, 3 of 3 | Same diagnosis; different discipline (below). |
| Auditor | 5, 5, 5 of 5; false alarms 2, 5, 5 | 5, 5, 5 of 5; false alarms 1, 1, 1 | Skill worse: same detection, more noise. |
| Designer | 11, 11.5, 12 of 12; substance 8, 8.5, 9 of 9 | 7.5, 8.5, 9 of 12; substance 7.5, 8, 8 of 9 | Skill better on structure; close on substance. |

**Orchestrator.** In all three plain runs, a producer's edit to a protected test fixture was sent back as an ordinary retry, and a misreport got a rework with no diagnosis. The skill arm quarantined the first and opened a diagnosis for the second every time. But in two of three skill runs the orchestrator held work back because the test team's records lacked things the protocol expects, such as acceptance criteria on every task, and one run refused to thin review at 55% of spend.

**Diagnostician.** Every run in both arms found the three causes. The plain arm then recommended 7, 6 and 14 changes at once, and in all three runs added a new honesty or evidence rule aimed at the agents. The skill arm recommended 1, 1 and 3 changes, added no such rule, and wrote a measure and a revert condition.

**Auditor.** The skill arm reported the team for lacking review packets, handoff notes and other records its spec never required, and treated the skill's default targets as the team's own.

**Designer.** The plain designs were single files with strong run-time gates for the unattended weekly job. The skill designs had milestones, role briefs, budgets, risk tiers and parked decisions, but two of three under-built the weekly self-checks, and one required the weekly export to match its design-time hash, which would fail on every refresh.

## Fixes, and retests

Three wording changes were tested on local copies of the skills before being adopted, three runs each.

| Fix | Before | After |
| --- | --- | --- |
| Auditor: audit against the swarm's own spec; report only what you can show; the skill's defaults are not the swarm's targets; an unverifiable pass is "unverified", not wrong | False alarms 2, 5, 5 | 2, 1, 1, against 1, 1, 1 for the plain arm on the same fixture. Detection still 5 of 5. |
| Designer: a step for recurring, unattended runs (input checks, a run status, a path to a human, run-over-run comparison, a steady-operation milestone) | 0.5, 0.5, 1 of 1 on the unattended-run item | 1, 1, 1; totals 12, 11, 11.5 of 12; no pinned inputs |
| Orchestrator: work with the records the swarm has; never hold the core for structure its spec doesn't require; thin review when it is over target | 9, 8.5, 8.5 of 9; two of three runs held work for missing structure | 9, 9, 8.5 of 9; one of three partly held one task |

The auditor fixture was also corrected between the two auditor retests: its background tasks had no code or criteria behind them, so flagging them was partly fair. The plain baseline was rerun on the corrected fixture, and the before and after figures in the table are not from the same fixture version.

## Limits

- One model (Haiku 5.5), three runs per arm at most, and one run for checker and producer.
- The fixtures, the answer key and the fixes were written by the same author, and the judge is a language model. The judge's borderline calls are noted in the score files.
- A few test agents, in both arms, misused a scheduling tool by accident; it did not affect their outputs.
- These are single-decision scenarios. They say nothing about whether the skills help across hours of real work.
