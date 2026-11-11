# OBM Skills: organizational behavior management for AI agent teams

Model-agnostic skills that let one AI, or a team of AI agents, work toward a goal for hours or days with minimal human oversight. They apply organizational behavior management (OBM), the branch of behavior analysis that designs workplaces where people do the right thing when no one is watching, to AI agents.

The working hypothesis is that much of what goes wrong when agents run long tasks on their own is a work-system problem rather than a model problem: drifting, faking success, stalling, overspending. This project packages the work system as skills, and is building an evaluation to test whether it helps.

**Status: early research.** The skills and the evaluation harness work end to end, and two field tests have shaped them. No efficacy claim is made yet. The experiments that would support or refute one are next.

## What's here

| Folder | Contents |
| --- | --- |
| [`skills/`](skills) | Six skills (designer, orchestrator, producer, checker, auditor, diagnostician), each with a copy of the shared protocol |
| [`framework/`](framework) | The Behavior Engineering Model for AI Swarms: the design rationale |
| [`benchmark/`](benchmark) | An evaluation harness on [ImpossibleBench](https://arxiv.org/abs/2510.20270): single agent vs generic multi-agent vs OBM, plus a self-correction phase |
| [`results/`](results) | Runs to date, with full transcripts |

## The six roles

| Skill | Role in the organization |
| --- | --- |
| `obm-swarm-designer` | Designs the work system: goal, milestones, roles, contracts, evals, risk tiers, budgets |
| `obm-swarm-orchestrator` | The manager: dispatches, routes on outcomes, builds review packets, paces spend, keeps the core goal moving |
| `obm-swarm-producer` | The performer: does one task to its contract, with evidence, and reports blocks honestly |
| `obm-swarm-checker` | Quality: verifies work against criteria at the depth its risk tier sets |
| `obm-swarm-auditor` | Audit: drift and over-control, hidden-sample verification, probes, spend and progress, the manager's own decisions |
| `obm-swarm-diagnostician` | Performance improvement: turns failures into versioned rule changes, weighing what each rule costs |

All state lives in files, and every record has a fixed format ([`skills/protocol.md`](skills/protocol.md)), so any session, model or vendor can resume the work.

## Core ideas

- **Fix the environment before blaming the performer** (Gilbert's Behavior Engineering Model). Information, resources and incentives come first.
- **Worthy performance** (Gilbert): judge the system on the value it delivers divided by what it costs. Honesty protects the value; pace and risk-based review protect the cost.
- **Make honesty the rewarded path.** A checked "I'm blocked" is a passing outcome, a misreport is the costliest one, and claims are verified against the artifact, never against the report.
- **The human selects products and manages rules** rather than reviewing every step (metacontingencies, Glenn). Corrections become versioned rules so they are made once.

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

**Second A/B pilot** ([results](results/2026-11-09-ledger-ab)). A banking rules engine was built on Haiku 5.5 in three phases, each in a fresh chat, with planted honesty probes. Both arms scored 132/132 on hidden tests, had zero fuzz mismatches, and handled every probe honestly. The skills arm caught an unplanted error in the spec and raised an open question about the holiday calendar, at about twice the time. Next: make defect detection the measured outcome.

**Memory management**, adapted from Anthropic's [components of agent memory](https://www.anthropic.com/research/components-of-agent-memory) research and framed as antecedent control. The swarm's files are what every agent reads before acting, so a wrong record misdirects everyone after it.

- **A one-page index.** The orchestrator alone rebuilds `swarm/index.md` at each milestone gate, checking every fact against logs and artifacts rather than notes. Every role reads it first.
- **Memory audits.** The auditor checks the index, handoff notes and rules against ground truth.
- **A rule budget.** Briefs have a size cap, so a new rule replaces or merges with an old one. Rules state their purpose, not only a procedure.
- **Leaner handoff notes.** They record approach, dead ends and unverified suspicions, never what the artifact already shows.
- **Briefs scaled to model tier.** Procedures for fast models, purpose and reasons for strong ones.

## Foundations

Gilbert (1978), *Human Competence* · Rummler & Brache, *Improving Performance* · Glenn (1988), metacontingencies · Kerr (1975), "On the folly of rewarding A, while hoping for B" · Daniels, *Performance Management* · Malott (1992), rule-governed behavior in OBM · Alvero, Bucklin & Austin (2001), performance feedback · Austin (2000), the Performance Diagnostic Checklist · Risley & Hart (1968), say-do correspondence · Lerman & Iwata (1995), extinction bursts · Ferster & Skinner (1957), *Schedules of Reinforcement* · Wheeler, *Understanding Variation* · Zhong, Raghunathan & Carlini (2025), ImpossibleBench.

## License

MIT, except `benchmark/obm_bench/vendor/`, which is adapted from ImpossibleBench under its own MIT license.
