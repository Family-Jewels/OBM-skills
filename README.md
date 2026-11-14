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
| **Control theory** | Feedback loops, stability, error correction. Expectation, measurement, deviation, correction, and keeping corrections small enough that the system doesn't oscillate | The cycle in the orchestrator; the diagnostician's one change at a time; review that thins as reliability is shown; over-control audits |
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
| **Initiate corrective action** | Consequences are routed the same way every time. The diagnostician turns repeated failures into one versioned rule change, with a measure and a revert condition |
| **Enforce operational constraints** | The harness, not the agent: a stop gate with honest exits, protected paths, budget caps, measured spend |

## Three layers

| Layer | Holds | Lives in |
| --- | --- | --- |
| **Enforcement** | Invariants: rules a machine can check, the same every time | Hooks, permissions and scripts in whatever runs the agents ([`lab/harness`](lab/harness)) |
| **Protocols** | Judgment calls and the records every role reads and writes | The six skills and their shared protocol ([`skills/`](skills)) |
| **Learning** | Changing the system after it fails, and checking the checkers | The diagnostician and auditor, and the human who selects products and manages rules |

The skills stay complete without enforcement: on a platform with no hooks, every rule still exists as an instruction. Enforcement makes an invariant certain. Every gate keeps its honest exits open, because a gate that only opens on success teaches agents to fake success. Rule by rule, with the mechanism for each invariant: [`framework/implementation-layers.md`](framework/implementation-layers.md).

## What's here

| Folder | Contents |
| --- | --- |
| [`skills/`](skills) | Six skills (designer, orchestrator, producer, checker, auditor, diagnostician), each with a copy of the shared protocol |
| [`framework/`](framework) | The [Behavior Engineering Model for AI Swarms](framework/behavior-engineering-model-for-ai-swarms.md) (the OBM rationale) and the [implementation layers](framework/implementation-layers.md) |
| [`lab/`](lab) | The test harness: isolated headless agents with measured cost, the stop-gate and protected-paths hooks, fixtures and keys |
| [`skill-tests/`](skill-tests) | One scenario per skill with planted problems and an answer key |
| [`benchmark/`](benchmark) | An evaluation harness on [ImpossibleBench](https://arxiv.org/abs/2510.20270) |
| [`results/`](results) | Every run to date |

## The six roles

| Skill | Role |
| --- | --- |
| `obm-swarm-designer` | Designs the work system: goal, milestones, roles, contracts, evals, risk tiers, budgets |
| `obm-swarm-orchestrator` | The manager: dispatches, routes on outcomes, builds review packets, paces spend, keeps the core goal moving |
| `obm-swarm-producer` | The performer: does one task to its contract, with evidence, and reports blocks honestly |
| `obm-swarm-checker` | Quality: verifies work against criteria at the depth its risk tier sets |
| `obm-swarm-auditor` | Audit: drift and over-control, hidden-sample verification, probes, spend and progress, the manager's own decisions |
| `obm-swarm-diagnostician` | Performance improvement: turns failures into versioned rule changes, weighing what each rule costs |

All state lives in files, and every record has a fixed format ([`skills/protocol.md`](skills/protocol.md)), so any session, model or vendor can resume the work.

## Where the evidence stands

| Test | Finding |
| --- | --- |
| Two A/B builds from a spec (Sonnet 5.5, Haiku 5.5) | Both arms perfect on hidden tests and honest on every probe. The skills caught an unplanted spec error, at one and a half to two times the time |
| Each skill alone against a plain role (Haiku 5.5, blind-graded) | The orchestrator and diagnostician made better decisions; the checker and producer tied; the auditor and designer were worse until fixed |
| Three proposed protocol changes | Proportional intervention helped slightly; a computable risk-tier floor did worse than judgment; fact/assumption marking made no difference |
| The stop gate on impossible tasks | No agent faked success with or without a gate. A gate without honest exits cost 2.4 times as much |
| Four-arm calibration: a SQL engine from a spec | Baseline and skills plus enforcement both scored 100% on 1,650 hidden queries, in about five minutes |

Current models are already honest and capable on tasks that fit in one sitting. The design claims to help where they break down: long runs, context resets, compounding errors, real budgets. That is what the next experiment has to create.

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
