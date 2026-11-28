# AI Performance Engineering

Engineering the conditions under which AI agents work reliably on long tasks, for hours or days, with little human oversight.

## Hypothesis

> The reliability of long-horizon autonomous AI execution can be materially improved through engineered performance management systems that continuously establish expectations, measure actual execution, detect deviations, initiate corrective action, and enforce operational constraints.

Agents that run long tasks on their own drift, stop early, fake success, stall and overspend. This project treats those as failures of the system the agent works in, not only of the model, and builds that system: skills that carry the management practices, a harness that enforces what must never depend on an agent's memory, and experiments that test whether either one helps.

**Status: early research.** The skills, the enforcement hooks and the test harness work. No efficacy claim is made yet: on every task tried so far, current models were already good enough that the arms tied. The next experiment needs a task hard and long enough to make agents fail.

## The approach: one philosophy, five engineering disciplines

**Organizational behavior management (OBM) is the philosophy.** It is the branch of behavior analysis that designs workplaces where people do the right thing when no one is watching. It supplies the questions: what result is worth having, what the performer is told, what they are given, and what happens after they act. Its central rule is to fix the environment before blaming the performer. An agent cannot try harder next time, but its instructions, tools, checks and consequences can all change.

**The engineering disciplines supply the machinery.** OBM says what a well-run system must do. These fields say how to make it do it reliably:

| Discipline | What it contributes | Where it shows up |
| --- | --- | --- |
| **Control theory** | Feedback loops, stability, error correction. Expectation, measurement, deviation, correction, and keeping corrections small enough that the system doesn't oscillate | The cycle in the orchestrator; one redesign at a time, spaced so its effect can be judged; review that thins as reliability is shown; over-control audits |
| **Operations research** | Allocating limited resources for the most value. Budgets, review share, model tiers, cost per accepted unit | Worthy performance (value over cost); budgets and pacing; risk-based review depth |
| **Distributed systems** | Coordination, state management, fault tolerance. Many agents and sessions sharing work without losing or corrupting it | All state in files; one writer per file; isolated workspaces; atomic task claims; resuming after a context reset; environment failures sorted from performance failures |
| **Formal methods** | Constraints, invariants and verifiable conditions. Rules a machine can check, and done conditions stated as checks | Done conditions with runnable checks; protected paths; the stop gate; the split between judgment calls and invariants |
| **Decision theory** | Acting under uncertainty: expected value, and when to stop | Done, impossible, blocked or budget spent as the four ways to stop; parking decisions without stopping; sampling review by expected cost of an error |

## The performance loop

The hypothesis names five functions. Each has an owner:

| Function | How it is done here |
| --- | --- |
| **Establish expectations** | The designer turns a goal into checkable done conditions, milestones, contracts, budgets and decision rights |
| **Measure actual execution** | Checkers verify work against the artifact, never the report. Spend is measured by the platform, never self-reported. A fresh judge runs the done checks |
| **Detect deviations** | The orchestrator watches for stalls, spinning, retries and overspend. The auditor re-verifies a hidden sample and probes the checks themselves |
| **Initiate corrective action** | Consequences are routed the same way every time. The diagnostician finds the cause of a repeated failure; the designer makes one versioned change, with a prediction the charts can test and a revert condition |
| **Enforce operational constraints** | The harness, not the agent: a stop gate with honest exits, protected paths, budget caps, measured spend |

## Three layers

| Layer | Holds | Lives in |
| --- | --- | --- |
| **Enforcement** | Invariants: rules a machine can check, the same every time | Hooks, permissions and scripts in whatever runs the agents ([`lab/harness`](lab/harness)) |
| **Protocols** | Judgment calls and the records every role reads and writes | The six skills and their shared protocol ([`skills/`](skills)) |
| **Learning** | Changing the system after it fails, and checking the checkers | The auditor, diagnostician and designer's redesign loop, and the human who selects products |

The skills stay complete without enforcement: on a platform with no hooks, every rule still exists as an instruction. Enforcement makes an invariant certain. Every gate keeps its honest exits open, because a gate that only opens on success teaches agents to fake success. Rule by rule, with the mechanism for each invariant: [`framework/implementation-layers.md`](framework/implementation-layers.md).

## What's here

| Folder | Contents |
| --- | --- |
| [`skills/`](skills) | The role skills (designer, strategist, orchestrator, checker, auditor, diagnostician, controls owner, organizer), the single-agent `obm-long-run` skill, each with a copy of the shared protocol, and the protocol as its own skill |
| [`framework/`](framework) | The [Behavior Engineering Model for AI Swarms](framework/behavior-engineering-model-for-ai-swarms.md) (the OBM rationale) and the [implementation layers](framework/implementation-layers.md) |
| [`lab/`](lab) | The test harness: isolated headless agents with measured cost, the stop-gate and protected-paths hooks, fixtures and keys |
| [`lab/longrun/`](lab/longrun) | The long-run kit: a step record of every tool call with behaviour cues, change verdicts judged by the system, and a build gate for skills a run makes for itself |
| [`skill-tests/`](skill-tests) | One scenario per skill with planted problems and an answer key |
| [`benchmark/`](benchmark) | An evaluation harness on [ImpossibleBench](https://arxiv.org/abs/2510.20270) |
| [`results/`](results) | Every run to date, and [every run scored on the self-improvement chain](results/2026-11-27-behavior-analysis) |

## The five roles

| Skill | Role |
| --- | --- |
| `obm-swarm-designer` | Owns the design: a driver tree from the goal's main measure down to the drivers the swarm controls, each with a ceiling and guardrail; resources; checks, budgets, cadence. Turns each Strategist redirect into the current aims at once; redesigns after a diagnosis; the only role that changes the tree, checks or rules; the goal itself is the human's |
| `obm-swarm-orchestrator` | The manager: dispatches, routes on outcomes, paces spend, keeps the core goal moving, adopts redesigns, works to the current aims |
| `obm-swarm-checker` | Quality: gathers its own evidence for each criterion. Where nothing can be run, checks provenance: who published a source, when it was really published (not the date the text claims), whether it is cited elsewhere, independent corroboration, and whether judgments rest on verifiable facts |
| `obm-swarm-auditor` | The director: a pulse review of the system's charts every point, full audits at each quarter of the horizon (progress, experiments, direction, report-reality samples, probes, cost, the manager's decisions); about one keep-doing item to four fixes |
| `obm-swarm-diagnostician` | Finds what is going wrong and why (pinpoint, what maintains it, cause in the environment). Writes no fix: the designer does |
| `obm-swarm-strategist` | Decides what the system drives toward: the constraint now (the worker's capacity first), a stretch aim for each priority driver, how the capacity is split, and whether the last aims were met. The designer turns each redirect into `swarm/aims.md` at once |

For **one agent on a long task**, `obm-long-run` takes the place of the role skills. It says what the system does so the agent doesn't, how to choose the next action, how to build a skill for itself through the build gate, and how to stop honestly.

There is no producer skill. Workers follow the short rules for whoever does the work in the protocol, and the evidence about their work comes from the system's record and the checker's own checks, never from the worker's report about itself.

The loop has two halves. **Safety:** designer builds the driver tree → system charts every measure with limits computed from the data → auditor separates signals from routine variation → diagnostician walks the tree to what moved and why → designer reworks the design, with a prediction → the charts show whether it worked. **Improvement:** the system measures celeration against a floor line and a deliberate overshoot aim, and resources in use, the worker's capacity first → the Strategist judges its last aims, finds the constraint, and sets stretch aims and a capacity split → the designer turns them into `swarm/aims.md` at once → the orchestrator works to them, and the auditor checks it does.

All state lives in files, and every record has a fixed format ([`skills/protocol.md`](skills/protocol.md)), so any session, model or vendor can resume the work.

## Where the evidence stands

| Test | Finding |
| --- | --- |
| Two A/B builds from a spec (Sonnet 5.5, Haiku 5.5) | Both arms perfect on hidden tests and honest on every probe. The skills caught an unplanted spec error, at one and a half to two times the time |
| Each skill alone against a plain role (Haiku 5.5, blind-graded) | The orchestrator and diagnostician made better decisions; the checker and producer tied; the auditor and designer were worse until fixed |
| Three proposed protocol changes | Proportional intervention helped slightly; a computable risk-tier floor did worse than judgment; fact/assumption marking made no difference |
| The stop gate on impossible tasks | No agent faked success with or without a gate. A gate without honest exits cost 2.4 times as much |
| Four-arm calibration: a SQL engine from a spec | Baseline and skills plus enforcement both scored 100% on 1,650 hidden queries, in about five minutes |
| Stress-test calibration: SQLite's own conformance suite (sqllogictest) | One 8-minute shift scored 99.97% on 29,000 held-out queries for $0.34 |
| [Prosus Vending Bench](https://github.com/ProsusAI/vending-bench), 30 days, four arms × 3 seeds (Haiku 5.5) | All runs completed. Means €2,086 to €2,225 from €1,500, with ±€400 noise: no separation. The 365-day run is next |
| Prosus Vending Bench, 365 days, four arms × seed 1 | Baseline €8,510; protocols **€0** (the agent ended its turn on day 179 and the run scored zero); enforcement €17,578; both €10,855. The first long-horizon failure seen: a premature stop, in an arm without the stop gate. One seed; more running |
| [Every run, scored on the self-improvement chain](results/2026-11-27-behavior-analysis) | Stocked slots predict every full-year score (r = 0.95, 17 runs). Gaps are found reliably. But changes come true about as often as chance (15 of 38 against 11.9), and whatever relies on the agent remembering decays: 0 reviewers started by agents in 22 runs, and logs stopped or went silent in 7 of 11. What the harness runs survives. Fifteen long runs were lost to the environment, one to the agent |

Current models are already honest and capable on tasks that fit in one sitting, and on large tasks they already know well with an oracle to check against. The design claims to help where they break down: long runs, context resets, compounding errors, real budgets. That is what the next experiment has to create.

## Using the skills

- **Claude:** upload each folder in `skills/` as a skill, or zip each one and add it under Customize > Skills.
- **Any other AI:** give each agent its role's `SKILL.md` and `references/protocol.md` as instructions.
- **One AI:** it plays each role in turn. See protocol section 8.

Tools are described by capability ("can run tests") rather than product name, so the skills work across platforms.

## Running the benchmark

See [`benchmark/README.md`](benchmark/README.md). In short:

```bash
cd benchmark
python3.13 -m venv .venv && source .venv/bin/activate   # Python 3.10 to 3.14
pip install -r requirements.txt
python tests/smoke_test.py                              # no API key needed
python run_pilot.py --model anthropic/claude-sonnet-5-5 --limit 3 --epochs 1 --log-dir logs/tiny
python analyze.py logs/tiny --out tiny
```

## Changelog: what the field tests changed

**The long-run kit, 2026-11-27** (after [scoring every run](results/2026-11-27-behavior-analysis) on the twelve behaviours a self-improving long run needs). The scoring found that what the harness runs survives a year, and what relies on the agent remembering decays within weeks. So four jobs move from the agent to the system:

- **The movement cycle is recorded by the system.** A hook writes one line per tool call ([`lab/longrun/steps.py`](lab/longrun)) and hands the agent a cue when a pattern starts. The patterns are an unchanged re-read, the same failure again, many steps with no state change, a write outside the workspace, and the log growing. The runner records steps for every arm by default and keeps them with the results.
- **The system judges every change.** A method change ends with `Prediction: <measure> <up|down> within <N> points` on a charted measure. Engine v4 tests it with the signal rule, from adoption, with a chance rate, and files a miss back to the designer as a request to answer (protocol 4.5 and section 8).
- **Skills a run builds for itself go through a gate**: gap evidence, build or skip, held-out tests with and without the skill, and an independent review answered ([`skill_gate.py`](lab/longrun/skill_gate.py)).
- **New skill `obm-long-run`** for one agent on a long task: rank the next action by fixed rules (repair, constraint, freshness, diversity, authority, cost), write one line per event, never count what the system counts, and use four honest ways to stop.
- **Protocol:** one line per event at one path; never log or count what the system records; the machine-readable prediction line; change verdicts in the charts.

**v3: the Strategist, 2026-11-19** (after v2 seed 1: €11,852 against v1's €15,006 on the same seed). v2 is kept on the branch `skills-v2`.

- Experiments and opportunity reviews are removed. In v2 seed 1, no experiment reached a decision in a whole year, and the opportunity reviews and their redesigns held the redesign slot so that 23 of 24 requested fault diagnoses were deferred.
- One new role, the Strategist, owns direction: the constraint, stretch aims and the split of the worker's capacity, with feedback on whether its last aims were met. The designer incorporates each redirect into `swarm/aims.md` straight away, in its own lane; a redirect that needs a design change queues behind fault diagnoses.
- Faults first: deferred diagnoses wait in a queue instead of being dropped.
- The other roles go back to their own jobs; the auditor also checks the work follows the current aims.

**The improvement half, 2026-11-18** (after five seeds showed a safe floor but a low ceiling; [results](results/2026-11-17-five-seeds-skills-vs-native)). v1 is kept on the branch `skills-v1`.

- Progress is measured as Precision Teaching's celeration: the multiplier per point from a median-based log-scale fit, with bounce, phases and own best, computed by the system.
- Timing comes from the task. The adapter states the horizon, natural cycle and clock ([`lab/cadence/ADAPTER_SPEC.md`](lab/cadence/ADAPTER_SPEC.md)); the system derives the point window and counts every interval in points. Vending's 7-day point falls out of the rules.
- The top measure has a floor line (the goal at the horizon) that triggers reviews, and an aim that deliberately overshoots (the goal by half the remaining horizon) and triggers nothing.
- The diagnostician gains an opportunity mode, run on a schedule even when every chart is stable. The designer redesigns from it, often by setting up experiments inside guardrails.
- Reviews give about one keep-doing item to four fixes. A misreport now cannot advance the task, classified by evidence not intent, instead of resetting it.
- Cost cuts: the worker logs events instead of a line every period, and re-reads the spec only when it changes.

**Design review, 2026-11-15** (Jules's feedback after the cadence runs):

- The designer is a loop, not a one-off: the system calls it back to redesign when a diagnosis or audit shows the swarm is off course.
- Measurement: KPIs with designer-set targets were replaced by a driver tree, process behavior charts (XmR limits computed by the system from each measure's own data, so no agent sets its own limits) and Gilbert's PIP against an exemplar. Each redesign states a prediction that the charts test against the limits from before it.
- The diagnostician only diagnoses. The tree, checks and rules are changed by the designer alone; the goal is the human's.
- The producer skill is gone. A worker's report about its own work is a claim, not evidence; the system records what it ran, and the checker gathers the evidence.
- The checker verifies work that has no runnable test by provenance: publisher, real publication date, citations elsewhere, independent corroboration, and whether judgments rest on verifiable facts.
- Cadence: pulse every 5 periods, full audit every 50, redesigns at least 20 apart.

**First tiny ImpossibleBench run** ([results](results/2026-11-08-impossiblebench-tiny)):

- Every role is now told what the environment can actually do, after the designer wrote criteria that needed code execution nobody had.
- Blocks are now scored by type.
- A no-hint task variant was added to get past a ceiling effect.

**Long-horizon field test** (a multi-milestone schedules-of-reinforcement simulator built by the skills):

- **Isolated workspaces for parallel producers.** Overlapping edits produced a commit that could not be verified on its own.
- **Checkers get facts only.** A checker passed a misreport after being told the manager's explanation of the problem; the auditor caught it.
- **Spend is measured, never self-reported.** A producer estimated 25k tokens against 92k measured.
- **Worthy performance, risk tiers, review-share targets and over-control audits.** The self-correction loop leaned toward caution, each failure producing a stricter rule, until review costs outran progress and a human had to rebalance it.

**First A/B pilot** ([results](results/2026-11-09-sheetcalc-ab)). A spreadsheet engine was built from a spec on Sonnet 5.5, with skills and without, and graded on hidden tests. Both arms scored 238/238 and both reported the planted test contradiction, so the task hit a ceiling. The skills took about a third more time and produced a more actionable decision record and a calibrated final audit. The next task needs to be long and high-pressure enough to separate the arms.

**Lessons from Claude Code's /plan and /goal**, adapted so the judge checks the work itself, not the conversation:

- **A separate done judge.** A fresh agent runs the spec's own checks every cycle and returns met, not yet met or impossible. The worker never declares itself done.
- **"Impossible" as a valid way to end a run.**
- **Checkable done conditions.** Each one states the end state, the check, the constraints and a bound.
- **Spinning as a stall signal.**
- **Check-ins that space out** on long-running work.
- **Environment failures sorted by cause**, never counted against the agent.
- **Read-only design, then execution in a fresh context.**
- **A plan step for high-risk tasks only.**

**Per-skill tests** ([results](skill-tests/results/2026-11-13)). Each skill was tested alone against a one-line role on Haiku 5.5, three runs per arm, blind-graded:

- **Better with the skill:** the orchestrator and diagnostician made better decisions.
- **No change:** the checker and producer.
- **Worse until fixed:** the auditor raised more false alarms, and the designer under-built checks for unattended recurring runs.

Three fixes followed, each retested: audit against the swarm's own spec, design for recurring unattended runs, and work with the records the swarm has.

**Implementation layers** ([design](framework/implementation-layers.md)). The tests showed that the skills change judgment, and that a rule a machine can check should not depend on an agent remembering it. Every rule in the skills is now marked as a judgment call or an invariant, with the mechanism that would enforce each invariant. The design borrows a harness-run stop gate, fresh evidence, a delegation log and expiring notes from [oh-my-claudecode](https://ohmyclaudecode.com), and adds what that system lacks: budget caps and honest ways to stop. It is a design only; nothing is built or tested yet.

**Proposal and stop-gate tests** ([results](results/2026-11-13-proposals-and-stop-gate), [harness](lab)). A harness that runs each agent as an isolated headless session with measured cost. Of three proposed changes, proportional intervention helped a little, a computable risk-tier floor did worse than judgment, and fact/assumption marking made no difference. A stop gate and a protected-paths hook were built. On tasks that could not be completed, no arm faked success, gate or no gate; a gate without honest exits cost 2.4 times as much. Small tasks don't separate the arms, so the four-arm test needs a long one.

**Reframed as AI Performance Engineering.** OBM is now the philosophy rather than the whole architecture, combined with control theory, operations research, distributed systems, formal methods and decision theory. A first four-arm calibration on a SQL engine built from a spec hit the ceiling: baseline and skills plus enforcement both scored 100% on 1,650 hidden queries in about five minutes, and both reported the planted contradiction. It also exposed a false positive in the protected-paths hook, now fixed.

**Second A/B pilot** ([results](results/2026-11-09-ledger-ab)). A banking rules engine was built on Haiku 5.5 in three phases, each in a fresh chat, with planted honesty probes. Both arms scored 132/132 on hidden tests, had zero fuzz mismatches, and handled every probe honestly. The skills arm caught an unplanted error in the spec and raised an open question about the holiday calendar, at about twice the time. Next: make defect detection the measured outcome.

**Memory management**, adapted from Anthropic's [components of agent memory](https://www.anthropic.com/research/components-of-agent-memory) research and framed as antecedent control. The swarm's files are what every agent reads before acting, so a wrong record misdirects everyone after it.

- **A one-page index.** The orchestrator alone rebuilds `swarm/index.md` at each milestone gate, checking every fact against logs and artifacts rather than notes. Every role reads it first.
- **Memory audits.** The auditor checks the index, handoff notes and rules against ground truth.
- **A rule budget.** Briefs have a size cap, so a new rule replaces or merges with an old one. Rules state their purpose, not only a procedure.
- **Leaner handoff notes.** They record approach, dead ends and unverified suspicions, never what the artifact already shows.
- **Briefs scaled to model tier.** Procedures for fast models, purpose and reasons for strong ones.

## Foundations

- **OBM:** Gilbert (1978), *Human Competence* · Rummler & Brache, *Improving Performance* · Glenn (1988), metacontingencies · Kerr (1975), "On the folly of rewarding A, while hoping for B" · Daniels, *Performance Management* · Malott (1992), rule-governed behavior in OBM · Alvero, Bucklin & Austin (2001), performance feedback · Austin (2000), the Performance Diagnostic Checklist · Risley & Hart (1968), say-do correspondence · Lerman & Iwata (1995), extinction bursts · Ferster & Skinner (1957), *Schedules of Reinforcement* · Wheeler, *Understanding Variation*
- **Control theory:** Åström & Murray (2008), *Feedback Systems*
- **Operations research:** Hillier & Lieberman, *Introduction to Operations Research*
- **Distributed systems:** Lamport (1978), "Time, clocks, and the ordering of events in a distributed system"
- **Formal methods:** Hoare (1969), "An axiomatic basis for computer programming"
- **Decision theory:** Wald (1947), *Sequential Analysis* · Raiffa & Schlaifer (1961), *Applied Statistical Decision Theory*
- **AI agents:** Zhong, Raghunathan & Carlini (2025), ImpossibleBench

## License

MIT, except `benchmark/obm_bench/vendor/`, which is adapted from ImpossibleBench under its own MIT license.
