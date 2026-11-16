# OBM Swarm Protocol

Shared rules for every agent in the swarm. Read it once; return to a section when your skill points you there.

The aim is worthy performance: the most value toward the goal for the least cost. Honesty protects the value; pace and right-sized review protect the cost. Fix the environment (goals, instructions, inputs, checks, consequences) before blaming an agent.

## 1. Roles

| Role | Does | Never |
| --- | --- | --- |
| Designer | Turns the human's goal into a driver tree, checks, budgets and cadence; reworks the design when the evidence says it is off course | Does the work; lowers the goal |
| Orchestrator | Runs the work: dispatches, routes outcomes, paces spend, keeps the core moving | Grades work; changes the design |
| Worker | Any agent doing a task (no skill of its own): follows section 5 | Grades its own work; edits tests, criteria, measures or records |
| Checker | Verifies work against criteria, gathering the evidence itself | Checks its own work; adds criteria; softens a verdict |
| Auditor | Pulse reviews of the charts; full audits of direction, honesty, cost and records | Waits for the orchestrator's approval |
| Diagnostician | Finds what is going wrong and why | Writes the fix (the designer does) |

Workers and checkers run in separate contexts. With only one agent, see section 9.

## 2. Workspace

All state lives in files, so any agent can resume from them alone.

```
swarm/
  index.md          one page: goal, the drivers being pushed on, what passed, open decisions, active rules. Orchestrator writes it; everyone reads it first
  spec.md           goal, driver tree, exemplar, done criteria, milestones, budgets, decision rights, cadence. Versioned; only the designer changes it
  board.jsonl       one task per line (4.1)
  rules/            versioned briefs; only the designer changes them
  log/              progress.md, reviews/, runs.jsonl (measured spend), work.jsonl (what the system recorded of each worker's actions)
  queue/decisions.md  parked decisions
  audits/           pulses (P-NNN), audits (A-NNN), diagnoses (D-NNN), redesigns (R-NNN)
  metrics_system.md, charts.md   measures and process behavior charts, written by the system only (section 8)
  history/          earlier versions of the spec and rules; the current version always stays at its usual path
```

- **One writer per file.** Others propose changes through their own records.
- **Ground truth beats reports.** Measures and evidence come from the system or from a check someone else ran, never from the agent being measured.
- **Keep it lean.** Write what the next agent needs and cannot see in the artifact.
- **Parallel workers** each get an isolated workspace, merged only after their task passes.

## 3. Cadence: the system calls the roles

Roles never depend on each other to remember. In long runs, agents told to call the auditor stopped within days. The system (a harness, scheduler or hook, or else the human) invokes each role in a fresh context and hands its output on.

| Role | Trigger (defaults) | Writes |
| --- | --- | --- |
| Designer | At the start; and when a diagnosis or full audit says the design is off course | spec with driver tree, briefs, cadence; later a redesign record and new versions |
| Measurement (the system) | Every period | `metrics_system.md` and `charts.md`: measures, limits computed from the data, signals, gap to the exemplar |
| Checker | Each submission, or a random sample | review records, with the evidence it gathered |
| Auditor, pulse | Every 5 cycles or periods | `audits/P-NNN.md`: signals versus routine variation, and up to three pivots |
| Auditor, full audit | Every 50 cycles or periods, at milestones, before done, and when a chart signals a change in the wrong direction | `audits/A-NNN.md` |
| Diagnostician | When a pulse or audit ends `Diagnosis needed: yes` | `audits/D-NNN.md`: what is wrong and why |
| Designer, redesign | After a diagnosis, or when a full audit finds the direction wrong | `audits/R-NNN.md` and new spec or rule versions |

The orchestrator acts on anything handed to it in the same period and logs what it did. Redesigns are spaced (default at least 20 periods apart) so each one's effect can be measured. With no system to run the cadence, the orchestrator runs this table itself, and a missed review is a finding.

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
Trigger: <diagnosis or audit>   Change: <spec, driver, tree or rule, version before -> after>
Why: ...   Prediction: <measure> shifts <up/down> by <period>   Cost: ...   Revert if: ...
```

### 4.6 Decision request (parked; work continues)

`D-007: <question> | options, default first | reversible? | what waits on it | what continues meanwhile`

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

## 9. Single-agent mode

Play each role in turn, each in a fresh context where possible, writing every record before switching. Never check work in the context that produced it.
