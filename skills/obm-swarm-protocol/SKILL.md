---
name: "obm-swarm-protocol"
description: "The shared protocol for OBM swarm skills (designer, orchestrator, checker, auditor, diagnostician): roles, workspace, the cadence the system runs, record formats, guidance never orders, rules for whoever does the work, consequences, review schedule, and measurement with driver trees, process behavior charts and PIP. Read it whenever another obm-swarm skill refers to the protocol."
---

# OBM Swarm Protocol

Shared rules for every agent in the swarm. Read it once; return to a section when your skill points you there.

The aim is worthy performance: the most value toward the goal for the least cost. Honesty protects the value; pace and right-sized review protect the cost. Fix the environment (goals, information, inputs, checks, consequences) before blaming an agent.

The working agent has full autonomy. The system curates what it sees: ground truth, what is open, and guidance from the management roles. Everything the system and the roles give it is information, advice, guidelines or examples of what good looks like. Nothing assigns, requires, forbids, blocks or caps an action (section 10).

## 1. Roles

| Role | Does | Never |
| --- | --- | --- |
| Designer | Turns the task and the human's requirements into a driver tree, what the system charts and counts as an opportunity, the first guidance, budgets and cadence; reworks the design when the evidence says it is off course | Does the work; lowers the goal; writes an order |
| Orchestrator | Runs the work with full autonomy: decides what to do, dispatches, routes outcomes, paces spend, keeps the core moving | Grades work; changes the design |
| Worker | Any agent doing a task (no skill of its own): follows section 5 | Grades its own work; edits tests, criteria, measures or records |
| Checker | Verifies work against criteria, and fact-checks proposed guidance and the agent's own stated policies against the ground truth | Checks its own work; adds criteria; softens a verdict |
| Auditor | Pulse reviews of the charts and the agent's behavior; full audits of direction, honesty, cost and records; proposes guidance | Waits for the orchestrator's approval; tells the agent what to do |
| Diagnostician | Finds what is going wrong and why | Writes the fix (the designer does) |

Workers and checkers run in separate contexts. With only one agent, see section 9.

## 2. Workspace

All state lives in files, so any agent can resume from them alone.

```
swarm/
  index.md          one page: goal, the drivers being pushed on, what passed, open decisions. Orchestrator writes it; everyone reads it first
  spec.md           goal, driver tree, exemplar, done criteria, budgets, decision rights. Versioned; only the designer changes it
  system.json       what the system charts, the signals that pull a review early, what counts as an opportunity, the exemplar, the cadence. Only the designer changes it
  system_interface.md, requirements.md   what the system can read (from the task's adapter), and the human's requirements
  guidance/         the guidance library: G-NNN.md entries (4.7) and index.md; proposed/ waits for a fact check; refuted/ and retired/ keep the history
  handoff.md        the note the system gives the agent at the end of every period
  checks/           fact checks (C-NNN) and policies.md: the agent's own stated policies with their checks
  ground_truth/     state snapshots for recent periods, written by the system
  board.jsonl       one task per line (4.1), when the work has tasks
  log/              progress.md, reviews/, runs.jsonl (measured spend), work.jsonl (what the system recorded of each worker's actions)
  queue/decisions.md  parked decisions
  audits/           pulses (P-NNN), audits (A-NNN), diagnoses (D-NNN), redesigns (R-NNN)
  metrics_system.md, charts.md   measures and process behavior charts, written by the system only (section 8)
  history/          earlier versions of the spec, system.json and guidance; the current version always stays at its usual path
```

- **One writer per file.** Others propose changes through their own records.
- **Ground truth beats reports.** Measures and evidence come from the system or from a check someone else ran, never from the agent being measured.
- **Keep it lean.** Write what the next agent needs and cannot see in the artifact.
- **Parallel workers** each get an isolated workspace, merged only after their task passes.

## 3. Cadence: the system calls the roles

Roles never depend on each other to remember. In long runs, agents told to call the auditor stopped within days. The system (a harness, scheduler or hook, or else the human) invokes each role in a fresh context and hands its output on.

| Role | Trigger (defaults) | Writes |
| --- | --- | --- |
| Designer | At the start; and when a diagnosis says the design is off course | spec, system.json and the first guidance; later a redesign record, new versions and guidance proposals |
| Measurement (the system) | Every period | `metrics_system.md` and `charts.md`: measures, limits computed from the data, signals, gap to the exemplar, and the agent's behavior and cost as information |
| Hand-off (the system) | Every period | `handoff.md`: capacity used, what was open when the period ended and what is open now, the guidance that fits, anything new |
| Checker, work | Each submission, or a random sample | review records, with the evidence it gathered |
| Checker, fact check | When guidance is proposed, and when the agent's own notes change (default every 5 periods) | `checks/C-NNN.md`; accepted guidance enters the library, refuted guidance is kept with its reason |
| Auditor, pulse | On what the agent does (a period ended with capacity unused while opportunities were open, repeated early ends, a statement the ground truth refutes), and every 5 periods as a backstop | `audits/P-NNN.md`: signals versus routine variation, what the agent did with what was open, and guidance proposals |
| Auditor, full audit | Every 50 periods, at milestones, before done, and when a chart or a designer's signal fires | `audits/A-NNN.md` |
| Diagnostician | When a pulse or audit ends `Diagnosis needed: yes` | `audits/D-NNN.md`: what is wrong and why |
| Designer, redesign | After a diagnosis | `audits/R-NNN.md`, new versions of the spec or system.json, guidance proposals |

What the system hands the agent is information and advice; the agent decides what to do with it. Reviews change the environment (what the system shows, counts as an opportunity, or advises), never the agent. Redesigns are spaced (default at least 20 periods apart) so each one's effect can be measured. With no system to run the cadence, the orchestrator runs this table itself, and a missed review is a finding.

## 4. Records

### 4.1 Task (one line of board.jsonl)

```json
{"id": "T-0042", "driver": "capacity_in_use", "milestone": "M2", "title": "...", "pinpoint": "the product this task leaves behind",
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
Trigger: <diagnosis>   Change: <spec, system.json or guidance, version before -> after>
Why: ...   Prediction: <measure> shifts <up/down> by <period>   Cost: ...   Revert if: ...
```

### 4.6 Decision request (parked; work continues)

`D-007: <question> | options, default first | reversible? | what waits on it | what continues meanwhile`

### 4.7 Guidance entry (G-NNN; proposals go to guidance/proposed/)

```
# <short title>
Applies when: always | <opportunity ids>
What good looks like: <advice, a guideline or an example>
Why: <the reason and the evidence>
Source: <brief | review or diagnosis id>
Revisit: <period>
```

A proposal may add `Revises: G-NNN` or `Retires: G-NNN`.

### 4.8 Fact check (C-NNN)

```
Proposal: <path> | Verdict: accepted | untestable | refuted | Reason: <one line>
Statement: "<quote>" | File: <path> | Verdict: supported | refuted | untestable | Evidence: <numbers, with periods>
```

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
| Misreport | Task reset, back to full review, diagnosis opened |
| Constraint break | Output quarantined and never passes |
| Environment failure (limits, outages, credentials) | Not the agent's: retry or pause; never counted against it |

## 7. Review: how often, how deep

| Risk tier | Depth |
| --- | --- |
| low | Confirm each criterion directly |
| standard | Verify each criterion; gather the evidence yourself |
| high (core work, work others build on, irreversible) | Full verification plus adversarial checks |

Every submission at first, after a fail or misreport, and for milestone and final products. After 5 first-pass successes in a row, 1 in 3 at random; after 10 more, 1 in 5. Sampling changes how often, never how carefully. Review stays within the spec's share of spend (default about 30%).

## 8. Measurement: driver tree, charts and the exemplar

- **Driver tree.** The designer breaks the goal's main measure into the measures that produce it, down to drivers the swarm controls, each with a ground-truth source and a better direction. Useful additions: accepted units, first-pass rate, misreports, cost per accepted unit, review share, capacity in use.
- **Process behavior charts.** The system charts each measure every period. Limits come from the measure's own data (centre ± 2.66 × average moving range), never from an agent. A signal is a point beyond a limit or 8 in a row on one side of the centre. Everything else is routine variation: do not react to it.
- **Redesigns are tested on the charts.** After a redesign the old limits are kept: a real effect shows as a signal against them by the predicted period.
- **Gap to the exemplar (PIP).** Exemplar performance divided by the swarm's, where an exemplar is known; otherwise the swarm's own best period. A large gap with no improving signal is a reason to diagnose.
- **Behavior and cost are information.** The system also records the agent's capacity used, the opportunities open when each period ended and its context size, and each role's cost. They are shown beside the results and can prompt a review. They are never targets or limits.

## 9. Single-agent mode

Play each role in turn, each in a fresh context where possible, writing every record before switching. Never check work in the context that produced it.

## 10. Guidance, never orders

- **Guidance is advice.** An entry says what good looks like, why, when it tends to apply, where it came from and when to revisit it. It never requires, forbids or caps an action, and it stays advice however often it applies.
- **Facts first.** Guidance that rests on a claim enters the library only after a fact check against the ground truth.
- **The agent's own notes stay its own.** A policy or belief the agent writes is fact-checked and the result shown to it; it never becomes a rule by being written down.
- **Judge results, never obedience.** Reviews judge results and behavior against the ground truth. Guidance the agent did not use is evidence about the guidance or the environment.
