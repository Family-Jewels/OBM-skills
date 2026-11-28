---
name: "obm-long-run"
description: "Run one long task (hours or days) as a single agent inside a system that records every step, measures from ground truth, runs reviews in fresh contexts, judges every change, and refuses an early stop. Covers choosing the next action, writing one line per event, building a skill for yourself only when the records show a recurring gap and only through the build gate, changing methods with a prediction the system judges, and stopping or escalating honestly. Use whenever one AI works toward a goal long enough that context resets, drift, record bloat or early stopping become risks."
---

# OBM Long Run

The shared protocol is the `obm-swarm-protocol` skill. Wherever this skill names a protocol section, read it there.

You are one agent doing a long task. The system around you does everything mechanical: a harness, hooks, a scheduler, or else the human. It records every tool call, measures the work from ground truth, runs reviews in fresh contexts, judges each change you adopt, and refuses an early stop. What it does, you never do or duplicate; judgment is yours. These rules come from scoring every run to date (`results/2026-11-27-behavior-analysis`). The reason for each is given.

Your priorities, in order:

1. **Move the goal's main measure, through its constraint first.** Across 17 year-long runs, the final score tracked one driver (r = 0.95). The best run put the worker's own time into it.
2. **Stay honest.** Claim only what the artifact shows. A clear block is a valid result.
3. **Spend the least.** Take no step and write no record the goal does not need.

## What the system does, so you don't

| The system | So you |
| --- | --- |
| Records every tool call (`log/steps.jsonl`) | Never log your actions or counts. Self-counted figures drifted from the system's (40 slots against 19) |
| Measures from ground truth (`metrics_system.md`, `charts.md`, the Facts table) | Read them; never report a measure yourself |
| Starts every review in a fresh context, on its schedule | Never wait for a reviewer or rely on yourself to call one. In 22 runs no agent started one on its own; when the agent ran the cadence, it was abandoned on day 15 |
| Judges each adopted change against its prediction line | Write the line; answer the verdict |
| Hands you a cue when a step pattern starts: an unchanged re-read, the same failure again, many steps with no state change, a write outside the workspace, the log growing | Act on it in your next step |
| Holds the stop gate with honest exits, and measures spend | Stop only by one of the four exits below |

If none of this exists, see "Without a system" at the end.

## Every step: choose the next action

Rank what you could do next by these rules, in order. This is the whole decision: do not deliberate past it.

1. **Repair first.** Restore a crossed guardrail; make a correction handed to you.
2. **The constraint.** Take the action that changes state on the driver the current aims name (`instructions.md`), or that clears the blocker on the critical path. Reading is not progress: when the system says many steps have passed with no state change, the next step changes something or records a block.
3. **Freshness.** Never re-read what has not changed; use what you read.
4. **Diversity.** Never repeat a failed action unchanged. After two identical failures, change the input or the route, or record a block with the smallest step that would unblock it.
5. **Authority.** Ground truth (a test run, the system's measure) beats a note, and a note beats memory.
6. **Cost.** Take the cheapest action that settles the open question, using the Facts table. Reversible beats irreversible.

Before a costly or irreversible action, state in one line the gap, the action and the signal you expect. Not before every step.

## Records: one line per event

- **One file at the protocol's path** (`swarm/log/progress.md`). In two runs the log moved outside `swarm/`, away from where the reviewers are pointed.
- **One line per event**, under 300 characters: a fix made, a change adopted, a decision parked, a block, a stall. Never restate a measure, count or action the system has. In three of five year-long logs, daily lines grew two to three times longer, and every period's reading paid for them.
- **Before your context runs low,** write a handoff note: your approach, dead ends and unverified suspicions. Leave out anything the artifacts already show.

## Building a skill for yourself

Build a skill only when the records show a gap that will recur. Each link leaves a record in the skill's folder. The build gate (`lab/longrun/skill_gate.py`, run by the system) adopts the skill only when every record is there. You never adopt your own skill by copying it into place.

1. **The task as checks.** Criteria a check can test, using capabilities you actually have. One run's designer wrote criteria needing code execution nobody had, and blocked solvable work.
2. **The gap, with evidence.** Cite where it shows: a record, a chart, a failed step. Search the existing skills first; reuse beats building.
3. **Build, skip or inline**, with the expected reuse (`decision.md`). Skip and inline are honest outcomes, not failures.
4. **Tests first.** At least three cases (`tests/cases.jsonl`), some held out: you do not look at those while writing.
5. **The skill.** When to use it, its steps, and when it is done (`SKILL.md`). Keep it short, with rules as "if X, then Y, because Z".
6. **Verification.** Run the held-out cases with and without the skill and record both (`verification.json`). No measured gain means nothing to adopt.
7. **Review.** A reviewer in a context that did not write the skill reviews it. You answer every finding: done, declined or deferred, with the reason.
8. **The gate decides.** Then apply the skill as a state where you can: a setting, a template, or a checklist file the system hands you each period. Not a habit to remember: in the experiments, the one change that passed its fidelity check was a one-time setting (a price), and every change that needed the worker to keep acting failed.

## Changing how the work is done

- **Change one method at a time.** End its record (protocol 4.5) with exactly `Prediction: <measure> <up|down> within <N> points`, on a measure the system charts. The window counts from adoption. If the measure is not charted, ask the human to instrument it; do not count it yourself.
- **The system's verdict comes back as a request.** Keep, revise or revert, and say why. Prose predictions came true about as often as chance alone would give (15 of 38 against 11.9). So the verdict is the system's, with the chance rate beside it, not yours.
- **Do not stack changes.** Wait until the last change's window has passed, or its effect cannot be told apart from the next one.

## Stop or escalate

There are four honest ways to stop:

- **Done:** a fresh judge runs the done checks and says met.
- **Impossible:** with the evidence.
- **Blocked:** every remaining path is parked or blocked, and the smallest unblocking step is named.
- **Reserve reached:** the budget reserve is spent.

Never stop otherwise. One run ended its turn on day 179 of 365 and scored zero with €8,438 in the bank. A parked decision is never a reason to sit idle. Usage limits and outages are the environment's, not yours: pause, and resume from the files.

## Never

- Edit tests, criteria, measures, the step log, review records, controls, budgets, hooks or the gate.
- Mark your own work passed, judge your own prediction, or review your own skill.
- Pause the core work to fix records.
- Count by hand what the system counts.

## Without a system

If nothing records your steps or runs your reviews, run the protocol's cadence table yourself (section 3). Write a step line only for state-changing actions, and record every missed review as a finding. Expect this arrangement to decay, and ask the human for the hooks in `lab/longrun`. In the runs to date it lasted about two weeks.
