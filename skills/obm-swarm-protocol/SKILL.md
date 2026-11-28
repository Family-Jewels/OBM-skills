---
name: "obm-swarm-protocol"
description: "The shared protocol for OBM swarm skills (designer, strategist, orchestrator, checker, auditor, diagnostician, controls owner, organizer, long run): roles, the risk and improvement branches, workspace, the cadence the system runs, requests and dispositions, record formats, rules for whoever does the work, consequences, review schedule, and measurement with driver trees, process behavior charts, celeration, floor and aim lines, resources, guardrails and PIP. Read it whenever another obm-swarm skill refers to the protocol."
---

# OBM Swarm Protocol

Shared rules for every agent in the swarm. Read it once; return to a section when your skill points you there.

The aim is worthy performance: the most value toward the goal for the least cost. Honesty protects the value; pace and right-sized review protect the cost. Fix the environment (goals, instructions, inputs, checks, consequences) before blaming an agent.

The work is managed by two separate branches, so neither can starve the other:

- **The risk branch keeps the floor:** honest records, controls the worker stays within, faults found and closed, no over-control. Risk monitor (the auditor's risk pulse), checker, diagnostician, controls owner. It changes `swarm/controls.md` only.
- **The improvement branch raises the ceiling:** progress measured as celeration, a deliberate overshoot aim, the Strategist deciding what the system drives toward, the designer turning that into aims and methods. It changes `swarm/aims.md`, `swarm/spec.md` and the rules.

The full audit is independent of both, and the organizer reviews how the arrangement itself is working. The worker reads one file the system assembles, `swarm/instructions.md`: controls first, then aims; when they conflict, controls win. A stable process is where improvement starts, not where it ends.

## 1. Roles

| Role | Does | Never |
| --- | --- | --- |
| Designer (improvement) | Turns the human's goal into a driver tree, checks, budgets and cadence; turns the Strategist's redirects into the current aims at once; changes methods from the improvement branch's requests | Does the work; lowers the goal; changes the controls |
| Strategist (improvement) | Decides what the system drives toward: the constraint now, a stretch aim for each priority driver, and how the worker's capacity is split; judges whether its last aims were met | Designs the work system, diagnoses faults or touches the work; lowers the human's goal |
| Orchestrator | Runs the work: dispatches, routes outcomes, paces spend, keeps the core moving, works to the current aims | Grades work; changes the design or the aims |
| Worker | Any agent doing a task (no skill of its own): follows section 5 | Grades its own work; edits tests, criteria, measures or records |
| Checker (risk) | Verifies work against criteria, gathering the evidence itself; in operations, samples the worker's claims | Checks its own work; adds criteria; softens a verdict |
| Auditor | Risk pulses (risk branch): is anything broken, false or about to cross a line? Full audits (third line, independent of both branches): outcome, controls, improvement changes, honesty, requests, cost | Waits for the orchestrator's approval; judges whether the work could be better in a pulse |
| Diagnostician (risk) | Finds what is broken and why | Writes the fix (the controls owner does); diagnoses a shortfall against the aims (the Strategist's) |
| Controls owner (risk) | Writes `controls.md`: the fewest, smallest limits and checks that close the faults, each with its risk and a review point; answers challenges | Sets aims or methods; keeps a control past review without a reason |
| Organizer | At each quarter, reviews the management system's own health and may change one setting within its bounds | Touches the goal, guardrails, measures, controls or aims |

Workers and checkers run in separate contexts. With only one agent, see section 9.

## 2. Workspace

All state lives in files, so any agent can resume from them alone.

```
swarm/
  index.md          one page: goal, the drivers being pushed on, what passed, open decisions, active rules. Orchestrator writes it; everyone reads it first
  spec.md           goal, driver tree, exemplar, done criteria, milestones, budgets, decision rights, cadence. Versioned; only the designer changes it
  aims.md           the current aims and capacity split (4.7). Versioned; the designer writes it from the Strategist's redirects
  controls.md       the limits and checks the worker stays within. Versioned; only the controls owner writes it
  instructions.md   assembled by the system each period from controls.md and aims.md; the worker reads this
  escalations.md    written by the system: what needs the human (old or repeated requests, configuration changes)
  board.jsonl       one task per line (4.1)
  rules/            versioned briefs; only the designer changes them
  log/              progress.md (events only, one line each), reviews/, runs.jsonl (measured spend), work.jsonl and steps.jsonl (what the system recorded of each action and each tool call)
  queue/decisions.md  parked decisions
  audits/           risk pulses (P-NNN), claim samples (K-NNN), diagnoses (D-NNN), control changes (C-NNN), strategies (S-NNN), aim updates (AS-NNN), method changes (M-NNN), full audits (A-NNN), organization reviews (O-NNN)
  metrics_system.md, charts.md   measures, charts, celeration, resources, guardrails and change verdicts, written by the system only (section 8)
  step_health.md    behaviour measures from the step record (re-reads, repeated failures, steps with no state change), written by the system
  history/          earlier versions of the spec and rules; the current version always stays at its usual path
```

- **One writer per file.** Others propose changes through their own records.
- **Ground truth beats reports.** Measures and evidence come from the system or from a check someone else ran, never from the agent being measured.
- **Keep it lean.** Write what the next agent needs and cannot see in the artifact.
- **One line per event, at one path.** `log/progress.md`, under 300 characters a line. Never restate a measure, count or action the system records. In year-long runs, logs that did grew two to three times longer by the last quarter, and self-counted figures drifted from the system's.
- **Parallel workers** each get an isolated workspace, merged only after their task passes.

## 3. Cadence: the system calls the roles

Roles never depend on each other to remember. In long runs, agents told to call the auditor stopped within days. The system (a harness, scheduler or hook, or else the human) invokes each role in a fresh context and hands its output on. Everything mechanical is done by the system, not by an agent: routing, merging repeated requests, triggers, measuring what the work actually did, recording every step, and judging whether an adopted change did what it predicted. In 22 recorded runs, no agent started a reviewer on its own.

Intervals are counted in **points**, not fixed periods (section 8). The task's adapter states a **profile** (the shape of the work, how long a change takes to show, whether mistakes can be undone), and the system derives the settings below from it. Each setting has bounds, and the organizer may move one within them per review.

| Branch | Role | Trigger | Writes |
| --- | --- | --- | --- |
| — | Measurement (the system) | Every period | `metrics_system.md`, `charts.md` (levels, celeration, floor and aim, resources, guardrails, Facts, Pursuit, Requests, System health), `instructions.md` |
| Improvement | Designer, initial design | At the start | spec with driver tree, briefs, first `aims.md` |
| Risk | Risk pulse (auditor) | On a risk event, once when it starts: a guardrail crossed, a chart signal in the wrong direction, a measure gone missing, the work off its planned split; plus a routine sweep every `risk_sweep_every` points (1 if mistakes cannot be undone, else 2) | `audits/P-NNN.md`, ending `Fault: yes/no` |
| Risk | Checker | Each submission (deliverables), each attempt (search), or a claim sample every `checker_every` points (operations) | review records; `audits/K-NNN.md` ending `Misreport: yes/no` |
| Risk | Diagnostician | When faults are reported; all reported since the last diagnosis at once, the latest evidence per fault key | `audits/D-NNN.md`; filed automatically as a request to the controls owner |
| Risk | Controls owner | Every open request to `controls`, at once; at least `control_gap` points between adopted changes | `controls.md`, `audits/C-NNN.md` |
| Improvement | Strategist | Every `strategy_every` points (the feedback lag plus a point, at least 3); brought forward (after at least 2) when the top measure newly falls below its floor or its celeration newly turns flat or wrong | `audits/S-NNN.md` |
| Improvement | Designer, aim update | Right after each strategy | `aims.md`, `audits/AS-NNN.md` |
| Improvement | Designer, method change | Every open request to `designer`, at once; at least `method_gap` points between adopted changes | spec or rule versions, `audits/M-NNN.md`, a new chart phase |
| Third line | Full audit (auditor) | At each quarter of the horizon (or `full_audits` per horizon), at milestones and before done | `audits/A-NNN.md` |
| Organization | Organizer | Beside each full audit | `audits/O-NNN.md`, ending `Config change: <setting> = <value>` or `none` |

- **Reviews give both kinds of item:** about one keep-doing (what works and should be done more) to four fixes, with at least one keep-doing. Agents need information more than encouragement; the keep-doing item says what to scale.
- The orchestrator acts on anything handed to it in the same period and logs what it did.
- **The branches never share a queue or a change slot.** A stream of faults cannot hold back a strategy, and a strategy cannot hold back a fix.
- **Triggers fire on a change of state,** once when a condition starts, not every period it lasts.
- **Changes are spaced within each lane** so each can be judged; every adopted change is marked on the charts with its branch.
- **Against over-control:** every control names its risk and a review point, and the improvement branch can challenge one by request.
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

`Fault (pinpointed, with its key) | evidence | what maintains it | cause: information, resources or incentives (or knowledge, capacity) | what would need to change: a control, or a request to the designer`

### 4.5 Method change (M-NNN) and control change (C-NNN)

```
Trigger: <the requests answered>   Change: <spec, driver, tree, rule or control, version before -> after>
Why: ...   Cost: ...   Revert if: ...
Prediction: <measure> <up|down> within <N> points
```

End a method change with that last line exactly, naming a measure the system charts. The system judges it (section 8), counting from the period the change is adopted. A prediction it cannot judge, with no line or a measure it does not chart, goes back to the designer as a request. A measure the charts lack goes to the human as a request for instrumentation, never to an agent to count.

### 4.6 Decision request (parked; work continues)

`D-007: <question> | options, default first | reversible? | what waits on it | what continues meanwhile`

### 4.7 Strategy (S-NNN) and aims (aims.md)

Strategy: `Last aims: met or missed, and what that shows | the constraint now (the worker's capacity first) | for each priority driver: its stretch aim for the next point, and why | how the capacity is split across the drivers | anything the aims cannot reach without a design change`

aims.md, written by the designer from the strategy:

```
As of <period> (after S-NNN)   Constraint: <driver or resource>
| Driver | Now | Aim for the next point | Share of capacity | Guardrail |
## Capacity split
- <percent>% <label>: <action names, as the Facts table lists them>
Notes: <what to do first each period, in the spec's terms>
```

The system reads the `## Capacity split` section and measures the actual split from the worker's actions (the Pursuit table).

### 4.8 Requests and dispositions

Anything one role needs from another goes through the system, never by asking a role directly. End your record with:

```
## Requests
- to: <controls|designer|strategist|human> | key: <short-slug> | <the ask>
```

The system files each request, merges a repeat of the same `to` and `key` into the earlier one (reopening it if it was closed), counts how often it was asked, and shows every request's status in the Requests table on the charts. Check the table before asking: reuse an open key. A role handed requests answers every one:

```
## Dispositions
- REQ-007: done | <what changed>
- REQ-008: declined | <why>
- REQ-009: deferred | <what it waits for>
```

An unanswered request goes back to open. The system escalates to the human (`escalations.md`) a request open 3 points or asked 3 times, anything addressed to `human`, and every configuration change.

### 4.9 Facts

The system logs every action the worker takes, with the task's clock, and publishes a Facts table: per action, the number of calls, the median cost and its share of capacity. Read it; never ask for a fact it already measures. A fact you can support from ground truth that the system cannot measure goes in a `## Facts` section of your record: `- <fact> | source: <where in the ground truth>`; it is listed as proposed, with its source.

## 5. Rules for whoever does the work

- Take the shortest path to the criteria and stop there.
- If the criteria are unclear, use the most reasonable reading and say so in the submission note. Block only when no reasonable reading exists.
- A clear block (impossible as specified, a missing resource, an action outside scope, the retry cap, or about 80% of budget spent with no path) is a valid outcome. Name the smallest step that would unblock it.
- Never edit tests, criteria, measures, review records or other tasks. Never mark your own work passed.
- Never count or log by hand what the system records (actions, measures, spend). Log events only.
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
- **Floor and aim.** The floor line runs from the top measure's level after 3 points to the goal at the horizon: 3 points in a row below it brings the Strategist forward. The aim is a deliberate overshoot, the goal by half the remaining horizon, so the system never caps itself. Falling short of the aim is expected and triggers nothing. When the aim is met on 2 of the last 3 points it is raised.
- **Resources.** The share of each declared resource in use, and the idle amount. One resource is always the worker's own capacity (time, actions or budget per period): when it is near its limit, more output per unit of it is the opportunity, and idle resources elsewhere are symptoms. Otherwise an idle resource while a driver is short is an opportunity.
- **Guardrails.** Measures with a side that must not be crossed. Aims stay inside them. A breach is put right first.
- **Gap to the exemplar (PIP):** the ceiling divided by the swarm's performance.
- **Change verdicts.** For each adopted change, the system tests its prediction with the chart rule above. It uses limits from before the change, over the predicted window counted from adoption. It also states the chance rate: how often the same test fires on that measure where nothing changed. A verdict near the chance rate is weak evidence. A miss is filed as a request to the designer to keep, revise or revert the change, with a reason. In the runs to date, prose predictions came true about as often as chance alone would give (15 of 38 against 11.9).

## 9. Single-agent mode

Play each role in turn, each in a fresh context where possible, writing every record before switching. Never check work in the context that produced it. For one agent on a long task, use the `obm-long-run` skill.
