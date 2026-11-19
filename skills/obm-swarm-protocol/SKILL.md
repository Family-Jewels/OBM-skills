---
name: "obm-swarm-protocol"
description: "The shared protocol for OBM swarm skills (designer, orchestrator, checker, auditor, diagnostician): roles, workspace, the cadence the system runs, record formats, rules for whoever does the work, consequences, review schedule, and measurement with driver trees, process behavior charts, celeration, floor and aim lines, resources, guardrails, experiments and PIP. Read it whenever another obm-swarm skill refers to the protocol."
---

# OBM Swarm Protocol

Shared rules for every agent in the swarm. Read it once; return to a section when your skill points you there.

The aim is worthy performance: the most value toward the goal for the least cost. Honesty protects the value; pace and right-sized review protect the cost. Fix the environment (goals, instructions, inputs, checks, consequences) before blaming an agent.

The protocol has two halves. The safety half keeps the floor: honest records, consistent consequences, no stopping early, no over-control. The improvement half keeps raising the ceiling: progress measured as celeration, a deliberate overshoot aim, opportunity reviews when nothing is broken, and small experiments inside guardrails. A stable process is where improvement starts, not where it ends.

## 1. Roles

| Role | Does | Never |
| --- | --- | --- |
| Designer | Turns the human's goal into a driver tree, checks, budgets and cadence; reworks the design when the evidence says it is off course | Does the work; lowers the goal |
| Orchestrator | Runs the work: dispatches, routes outcomes, paces spend, keeps the core moving, makes experiments' changes and applies their verdicts | Grades work, including its own experiments; changes the design |
| Worker | Any agent doing a task (no skill of its own): follows section 5 | Grades its own work; edits tests, criteria, measures or records |
| Checker | Verifies work against criteria, gathering the evidence itself; checks each experiment was made as written, on its slice only | Checks its own work; adds criteria; softens a verdict |
| Auditor | Pulse reviews of the charts; full audits of direction, honesty, cost and records; the verdict on each experiment | Waits for the orchestrator's approval |
| Diagnostician | Finds what is going wrong and why; in opportunity mode, where the most room for improvement is | Writes the fix (the designer does) |

Workers and checkers run in separate contexts. With only one agent, see section 9.

## 2. Workspace

All state lives in files, so any agent can resume from them alone.

```
swarm/
  index.md          one page: goal, the drivers being pushed on, what passed, open decisions, active rules. Orchestrator writes it; everyone reads it first
  spec.md           goal, driver tree, exemplar, done criteria, milestones, budgets, decision rights, cadence. Versioned; only the designer changes it
  board.jsonl       one task per line (4.1)
  rules/            versioned briefs; only the designer changes them
  log/              progress.md (events only), reviews/, runs.jsonl (measured spend), work.jsonl (what the system recorded of each worker's actions)
  queue/decisions.md  parked decisions
  audits/           pulses (P-NNN), audits (A-NNN), diagnoses (D-NNN), opportunity reviews (O-NNN), redesigns (R-NNN)
  experiments/      one file per experiment (E-NNN, 4.8); the designer sets them up, the orchestrator runs them
  metrics_system.md, charts.md   measures, charts, celeration, resources and guardrails, written by the system only (section 8)
  history/          earlier versions of the spec and rules; the current version always stays at its usual path
```

- **One writer per file.** Others propose changes through their own records.
- **Ground truth beats reports.** Measures and evidence come from the system or from a check someone else ran, never from the agent being measured.
- **Keep it lean.** Write what the next agent needs and cannot see in the artifact.
- **Parallel workers** each get an isolated workspace, merged only after their task passes.

## 3. Cadence: the system calls the roles

Roles never depend on each other to remember. In long runs, agents told to call the auditor stopped within days. The system (a harness, scheduler or hook, or else the human) invokes each role in a fresh context and hands its output on.

Intervals are counted in **points**, not fixed periods. The task's adapter states its horizon, natural cycle and clock, and the system derives the point window from them (section 8).

| Role | Trigger | Writes |
| --- | --- | --- |
| Designer | At the start; after a diagnosis or opportunity review | spec with driver tree, briefs, experiments, cadence; later a redesign record and new versions |
| Measurement (the system) | Every period | `metrics_system.md` and `charts.md`: measures, limits, signals, celeration, floor and aim, resources, guardrails, experiments, gap to the exemplar |
| Checker | Each submission, or a random sample | review records, with the evidence it gathered |
| Checker, experiment fidelity | When an experiment reaches its Start (after the orchestrator writes Applied), and again after a failed check | `audits/F-E-NNN-n.md`: `Fidelity: pass` or `fail` |
| Auditor, experiment verdict | When an experiment's clock ends, with the system's comparison | `audits/V-E-NNN.md`: `Verdict: keep`, `revert` or `too small to read` |
| Auditor, pulse | Every point; every second point after three quiet pulses, back to every point on any signal, redesign or experiment end | `audits/P-NNN.md` |
| Auditor, full audit | At each quarter of the horizon, at milestones and before done | `audits/A-NNN.md` |
| Diagnostician, fault | When a pulse or audit ends `Diagnosis needed: yes` | `audits/D-NNN.md`: what is wrong and why |
| Diagnostician, opportunity | Every 3 points without one, or when the top measure has 3 points in a row below its floor line or a flat or wrong-way celeration; never while an experiment runs | `audits/O-NNN.md`: where the most room is |
| Designer, redesign | After a diagnosis or an opportunity review | `audits/R-NNN.md`, new spec or rule versions, experiments |

- **Reviews give both kinds of item:** about one keep-doing (what works and should be done more) to four fixes, with at least one keep-doing. Agents need information more than encouragement; the keep-doing item says what to scale.
- The orchestrator acts on anything handed to it in the same period and logs what it did.
- **Redesigns are spaced** at least 3 points after the last adopted design change, so each change can be judged. Setting up an experiment is not a design change.
- With no system to run the cadence, the orchestrator runs this table itself, and a missed review is a finding.

## 4. Records

### 4.1 Task (one line of board.jsonl)

```json
{"id": "T-0042", "driver": "slots_selling", "milestone": "M2", "title": "...", "pinpoint": "the product this task leaves behind",
 "acceptance": ["checkable criterion"], "inputs": ["..."], "risk_tier": "low|standard|high", "model_tier": "fast|strong",
 "status": "open", "attempts": 0, "retry_cap": 2, "budget": "...", "review_mode": "full|sampled"}
```

### 4.2 Submission note (from the worker; a claim to check, not evidence)

`Task | version (commit, file version or path) | what changed | assumptions made | blocked: no, or type + smallest unblocking step`

Evidence comes from the system's record of what the worker ran (`log/work.jsonl`) and from the checker's own checks.

### 4.3 Review record

```
Task: T-0042   Verdict: pass | fail | misreport | block-confirmed | block-rejected
1. <criterion> : met / unmet : <what the checker checked, and how>
Note matches artifact: yes / no
Fix: <one specific fix per unmet criterion>
```

### 4.4 Diagnosis (D-NNN)

`Problem (pinpointed) | evidence | what maintains it | cause: information, resources or incentives (or knowledge, capacity) | what the design would need to change`

### 4.5 Redesign (R-NNN)

```
Trigger: <diagnosis, opportunity review or audit>   Change: <spec, driver, tree, rule or experiment, version before -> after>
Why: ...   Prediction: <measure> shifts <up/down> by <period>   Cost: ...   Revert if: ...
```

### 4.6 Decision request (parked; work continues)

`D-007: <question> | options, default first | reversible? | what waits on it | what continues meanwhile`

### 4.7 Opportunity review (O-NNN)

`Drivers ranked by gap x leverage | the constraint | idle resources and what one more unit would return | what differed in the own-best stretch | up to two candidate experiments (driver, change, predicted shift, guardrail)`

### 4.8 Experiment (experiments/E-NNN.md)

```
Driver: <exactly one measure the system records>   Slice: <the units it touches, or all>   Control: rest
Change: <what is done differently>   Prediction: <the driver> shifts <up/down> by <amount>
Guardrail: <measure and side it must not cross>   Start: <period number>   End: <period number, at least 3 points later>
Applied: <period number>, written by the orchestrator once it has made the change on the slice
Verdict: written by the system from the auditor's ruling
```

**The lifecycle, run by the system.** No role judges its own work.

1. The designer writes the experiment. Its driver must be a measure the system records; one that is not is void.
2. Experiments whose slices overlap run one after another: a later one is queued until the earlier one ends. A slice with the rest as control is best; a whole-system experiment is judged against its own earlier line and runs alone.
3. The orchestrator makes the change on the slice only and writes `Applied`.
4. The system calls the checker for a fidelity check against its ground-truth snapshots. The clock starts only when it passes; after three failed checks the experiment is void.
5. While it runs, the system enforces the guardrails; a breach means revert at once.
6. At the end, the system compares the driver on the slice against the control (or against its own earlier line), and reads the effect against the envelope of the earlier bounce. The auditor rules: keep, revert, or too small to read.
7. The orchestrator applies the ruling. A keep is folded into the design at the next redesign.

## 5. Rules for whoever does the work

- Take the shortest path to the criteria and stop there.
- If the criteria are unclear, use the most reasonable reading and say so in the submission note. Block only when no reasonable reading exists.
- A clear block (impossible as specified, a missing resource, an action outside scope, the retry cap, or about 80% of budget spent with no path) is a valid outcome. Name the smallest step that would unblock it.
- Never edit tests, criteria, measures, review records or other tasks. Never mark your own work passed.
- Claim only what the artifact contains. An overclaim is a misreport. Admit a constraint break: the output is quarantined and nothing else happens.

## 6. Status and consequences

| Status | Set by |
| --- | --- |
| open, parked, quarantined | orchestrator |
| claimed, submitted, blocked | worker |
| passed, failed, misreport | checker (orchestrator may pass an unsampled submission) |

| Outcome | Consequence, the same every time |
| --- | --- |
| Passed | Moves downstream at once; adds to the pass streak |
| Failed | Returned once with specific feedback; at the retry cap, split, narrow or replan, never retried unchanged |
| Blocked, confirmed | A valid outcome: split, reassign, park or diagnose. Never penalized |
| Misreport (the report does not match the evidence) | Cannot advance: returned with the mismatch shown; that worker's submissions go back to full review; a diagnosis only if it repeats. Honest work already done is kept. No guess at intent |
| Constraint break | Output quarantined and never passes |
| Environment failure (limits, outages, credentials) | Not the agent's: retry or pause; never counted against it |

## 7. Review: how often, how deep

| Risk tier | Depth |
| --- | --- |
| low | Confirm each criterion directly |
| standard | Verify each criterion; gather the evidence yourself |
| high (core work, work others build on, irreversible) | Full verification plus adversarial checks |

Every submission at first, after a fail or misreport, and for milestone and final products. After 5 first-pass successes in a row, 1 in 3 at random; after 10 more, 1 in 5. Sampling changes how often, never how carefully. Review stays within the spec's share of spend (default about 30%).

## 8. Measurement: driver tree, charts, celeration and the exemplar

Every measure here is computed by the system from ground truth, never reported by an agent.

- **Driver tree.** The designer breaks the goal's main measure into the measures that produce it, down to drivers the swarm controls. Each driver has a ground-truth source, a better direction, a ceiling with its source and a confidence, and, where needed, a guardrail. Useful additions: accepted units, first-pass rate, misreports, cost per accepted unit, review share, capacity in use.
- **Ceiling sources, best first:** an external exemplar (someone has done this work); the swarm's own best stretch; a resource ceiling (output if no resource sat idle); a reference class (comparable cases found by research). With none, the driver is an uncertainty to test, not a gap: test the high-stakes, low-confidence links first.
- **Process behavior charts** answer "is it stable?". Limits come from the measure's own data (centre ± 2.66 × average moving range). A signal is a point beyond a limit or 8 in a row on one side of the centre. Everything else is routine variation: do not react to it.
- **Celeration** answers "is it getting better?". The point window is the shortest span that holds whole natural cycles and at least 3 observations while leaving at least 12 points across the horizon. Each point is the median of a flow over its window, or the last value of a positive level. Celeration is the multiplier per point from a median-based fit on the log scale, with bounce as the spread. It is provisional from 3 points and firm at 6. Each design change starts a new phase, judged by its jump (level) and turn (new celeration ÷ old). The swarm's own best celeration is the improvement exemplar.
- **Floor and aim.** The floor line runs from the top measure's level after 3 points to the goal at the horizon: 3 points in a row below it calls for an opportunity review. The aim is a deliberate overshoot, the goal by half the remaining horizon, so the system never caps itself. Falling short of the aim is expected and triggers nothing. When the aim is met on 2 of the last 3 points it is raised.
- **Resources.** The share of each declared resource in use, and the idle amount. An idle resource while a driver is short is an opportunity.
- **Guardrails.** Measures with a side that must not be crossed. Experiments run inside them. A breach is reverted first.
- **Gap to the exemplar (PIP):** the ceiling divided by the swarm's performance.

## 9. Single-agent mode

Play each role in turn, each in a fresh context where possible, writing every record before switching. Never check work in the context that produced it.
