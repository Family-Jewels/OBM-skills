# OBM Swarm Protocol

Shared rules for the six roles. Read it once; return to a section when your skill points you there.

The aim is worthy performance: the most value toward the goal for the least cost. Honesty protects the value; pace and right-sized review protect the cost. Fix the environment (instructions, inputs, checks, consequences) before blaming an agent.

## 1. Roles

| Role | Does | Never |
| --- | --- | --- |
| Designer | Turns the goal into a spec, milestones, briefs, checks, budgets and a cadence | Does the work |
| Orchestrator | Runs the work: dispatches, routes outcomes, paces spend, keeps the core moving | Grades work; gives a checker its own theory |
| Producer | Does one task to its criteria, with evidence | Grades its own work; edits tests, criteria or others' records |
| Checker | Verifies work against criteria and evidence | Checks its own work; adds criteria; softens a verdict |
| Auditor | Pulse reviews of the numbers; full audits of direction, honesty, cost and records | Waits for the orchestrator's approval |
| Diagnostician | Turns a repeated problem into one rule change | Blames an agent; changes several things at once |

Producers and checkers run in separate contexts. With only one agent, see section 8.

## 2. Workspace

All state lives in files, so any agent can resume from them alone.

```
swarm/
  index.md          one page: goal, milestone, what passed, open decisions, active rules, traps. Orchestrator writes it; everyone reads it first
  spec.md           goal, done criteria, milestones, budgets, decision rights, cadence table
  board.jsonl       one task per line (3.1)
  rules/            versioned briefs (producer.v3.md); changed only by the diagnostician
  log/              progress.md (one line per cycle), handoffs/, reviews/, runs.jsonl (measured spend)
  queue/decisions.md  parked decisions
  audits/           pulse (P-NNN) and audit (A-NNN) reports; probes.md is private to the auditor
  metrics.md        the scorecard (section 7)
```

- **One writer per file.** Others propose changes through their own records.
- **Ground truth beats notes.** Facts in the index are checked against logs and artifacts, never copied from a note.
- **Keep it lean.** Write what the next agent needs and cannot see in the artifact.
- **Parallel producers** each get an isolated workspace, merged only after their task passes.

## 2.2 Cadence: the system calls the roles

Roles never depend on each other to remember. In long runs, agents told to call the auditor stopped within days. The system (a harness, scheduler or hook, or else the human) invokes each role in a fresh context and hands its output to the orchestrator.

| Role | Trigger | Writes |
| --- | --- | --- |
| Designer | Once at the start | spec, briefs, cadence table |
| Measurement (a script where possible) | Every period | `metrics.md` lines from ground truth, never from an agent's report |
| Checker | Each submission, or a random sample | review records |
| Auditor, pulse | Often: default every 7 periods of an operation, or every cycle of a build | `audits/P-NNN.md`: direction of the numbers and up to three pivots |
| Auditor, full audit | Default every 30 periods or 5 cycles, at milestones, before done, and when a measure leaves its limits | `audits/A-NNN.md` |
| Diagnostician | When a pulse or audit ends `Diagnosis needed: yes` | a rule-change record and a new rule version |

The orchestrator acts on anything handed to it in the same period and logs what it did. With no system to run the cadence, the orchestrator runs this table itself, and a missed audit is a finding.

## 3. Records

### 3.1 Task (one line of board.jsonl)

```json
{"id": "T-0042", "milestone": "M2", "title": "...", "pinpoint": "the product this task leaves behind",
 "acceptance": ["checkable criterion"], "inputs": ["..."], "risk_tier": "low|standard|high", "model_tier": "fast|strong",
 "status": "open", "attempts": 0, "retry_cap": 2, "budget": "...", "review_mode": "full|sampled", "evidence": null}
```

### 3.2 Evidence block (with every submission)

```
Task: T-0042   Version: <commit, file version or artifact path>
1. <criterion> : met / not met : <evidence> : <how to verify in one step>
Gaps and assumptions: ...
Constraint breaks: none | <what happened>
```

A claim without evidence counts as not met.

### 3.3 Review record

```
Task: T-0042   Verdict: pass | fail | misreport | block-confirmed | block-rejected
1. <criterion> : met / unmet : <what was checked, how>
Report matches artifact: yes / no
Fix: <one specific fix per unmet criterion>
```

### 3.4 Blocked report: a valid outcome

```
Task: T-0042   Type: missing information | missing resource | ambiguous | impossible as specified | budget spent
Tried: ...   Smallest unblocking step: ...   Narrower task that could pass: ...
```

### 3.5 Handoff note (end of every session, 200 words or fewer)

```
Approach: why this way      Tried and failed: dead ends, and why
Unverified: suspicions not checked      Next step: the single most useful action
Blockers: ...      Spend: measured figure, or "unknown"
```

Record only what the artifact cannot show.

### 3.6 Decision request (parked; work continues)

`D-007: <question> | options, default first | reversible? | what waits on it | what continues meanwhile`

### 3.7 Rule change

```
RC-012   Trigger: <records>   Cause: <the environment cell: information, resources or incentives>
Change: <file, version, before -> after>   Expected effect: ...   Cost: ...
Measure: <scorecard line and threshold>   Review at: ...   Revert if: ...
```

### 3.8 Review packet (orchestrator to checker)

Task, exact version, criteria, evidence path, one verify step per criterion. Facts only: never the orchestrator's theory or expected verdict.

## 4. Status

| Status | Set by |
| --- | --- |
| open, parked | orchestrator (designer at start) |
| claimed, submitted, blocked | producer |
| passed, failed, misreport | checker (orchestrator may pass an unsampled submission) |
| quarantined | orchestrator |

Setting a status you do not own is a constraint break.

## 5. Consequences: the same every time

| Outcome | Consequence |
| --- | --- |
| Passed | Moves downstream at once; adds to the producer's pass streak |
| Failed | Returned once with specific feedback; at the retry cap, split, narrow or replan, never retried unchanged |
| Blocked, confirmed | A valid outcome: split, reassign, park or diagnose. Never penalized |
| Misreport | Task reset, producer back to full review, diagnosis opened |
| Constraint break | Output quarantined and never passes; admitting it carries no further cost, hiding it does |
| Environment failure (limits, outages, credentials) | Not the agent's: retry or pause; never counted against it |

If a misreport or a shortcut can ever pass, the swarm learns to misreport.

## 6. Review: how often, how deep

| Risk tier | Depth |
| --- | --- |
| low | Confirm each criterion directly |
| standard | Verify each criterion and its evidence |
| high (core work, work others build on, irreversible) | Full verification plus adversarial checks |

| Condition | How often |
| --- | --- |
| New producer or task type, or after a fail or misreport | Every submission |
| 5 first-pass successes in a row | 1 in 3, at random |
| 10 more | 1 in 5, at random |
| Milestone and final products | Always |

Sampling changes how often, never how carefully. Review stays within the spec's share of spend (default about 30%).

## 7. Scorecard (metrics.md)

From measured data, once per period: core progress (the goal's main measure), accepted units, first-pass rate, misreports, cost per accepted unit, review share, capacity in use, and the same measure a comparable period earlier (to catch decline). Read lines as trends: act on signals, not on routine variation.

## 8. Single-agent mode

Play each role in turn, each in a fresh context where possible, writing every record before switching. Never check work in the context that produced it. Keep the probe register out of producer and checker contexts.
