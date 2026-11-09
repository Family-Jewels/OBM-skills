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

## Foundations

Gilbert (1978), *Human Competence* · Rummler & Brache, *Improving Performance* · Glenn (1988), metacontingencies · Kerr (1975), "On the folly of rewarding A, while hoping for B" · Daniels, *Performance Management* · Malott (1992), rule-governed behavior in OBM · Alvero, Bucklin & Austin (2001), performance feedback · Austin (2000), the Performance Diagnostic Checklist · Risley & Hart (1968), say-do correspondence · Lerman & Iwata (1995), extinction bursts · Ferster & Skinner (1957), *Schedules of Reinforcement* · Wheeler, *Understanding Variation* · Zhong, Raghunathan & Carlini (2025), ImpossibleBench.

## License

MIT, except `benchmark/obm_bench/vendor/`, which is adapted from ImpossibleBench under its own MIT license.
