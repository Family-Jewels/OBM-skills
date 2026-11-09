# OBM Swarm Protocol

Shared conventions for the six OBM swarm skills (designer, orchestrator, producer, checker, auditor, diagnostician). Every role reads this file. It defines where state lives, what every record looks like, and which consequence follows which outcome, so that any agent, from any model or vendor, can pick up the work cold and keep it moving.

The design rests on one premise from Gilbert's Behavior Engineering Model: most performance problems come from the environment the performer works in, not the performer. Deployed agents do not learn across runs, so the swarm is directed through antecedents (specs, briefs, the board), consequences delivered as routing, and rule changes between cycles.

The aim is Gilbert's worthy performance: the value of what the swarm accomplishes divided by what it costs. Honesty and quality protect the value; pace, risk-based review and efficiency protect the cost. A swarm can fail on either side.

## Contents
1. Roles and separation of duties
2. Workspace layout
3. Record formats
4. Status values and who may set them
5. Consequence map
6. Review schedule: how often and how deep
7. Scorecard
8. Single-agent mode
9. Glossary: OBM term to swarm practice

---

## 1. Roles and separation of duties

| Role | Does | Never does |
| --- | --- | --- |
| Designer | Turns a goal into a spec, milestones, roles, contracts, evals and budgets | Produces work products |
| Orchestrator | Runs the cycle: dispatches, routes on outcomes, builds review packets, paces milestones and spend, keeps the core accomplishment moving, parks decisions | Grades work, edits criteria mid-milestone without a rule change, tells a checker its own theory before the checker rules |
| Producer | Does one task at a time to its contract, with evidence | Grades its own work, edits evals, tests, criteria or other roles' records |
| Checker | Verifies submitted work against criteria and evidence, at the depth its risk tier sets | Checks work it produced, softens a verdict to keep things moving, adds requirements the criteria do not contain |
| Auditor | Checks drift and over-control, report-reality agreement, probes, spend and progress, and the orchestrator's own decisions | Reports to the orchestrator for approval; its findings go to the record |
| Diagnostician | Turns failures into specific rule changes | Blames an agent; changes many things at once |

Separation of duties is the main honesty safeguard when there is no infrastructure enforcing it. Producers and checkers should run in separate contexts. When only one AI is available, see Single-agent mode.

## 2. Workspace layout

All state lives in files, never only in a context window. A fresh agent must be able to resume from these files alone.

```
swarm/
  index.md                one-page map of current state; every role reads it first (section 2.1)
  spec.md                 goal, done-criteria, milestones, roles, contracts, budgets, decision rights
  board.jsonl             one task record per line (section 3.1)
  rules/                  role briefs, versioned (producer.v3.md); changed only via rule-change records
  examples/               worked examples promoted from passed work (good) and caught errors (bad)
  log/
    progress.md           one line per cycle: cycle id, accepted units, tokens, notes
    orchestration.md      orchestrator decisions and reasons
    handoffs/             one handoff note per session (section 3.2)
    packets/              one review packet per check: facts only (section 3.8)
    reviews/              one review record per check (section 3.4)
    runs.jsonl            measured spend, one line per agent run (section 7)
  queue/decisions.md      parked decisions (section 3.6)
  changes/                rule-change records (section 3.7)
  audits/                 audit reports; audits/probes.md is the auditor's private register
  metrics.md              the scorecard (section 7)
```

Paths may be adapted, but keep the separation: shared state in the board and logs, rules versioned, audits apart.

When producers work in parallel, each task gets its own isolated workspace (a branch, worktree or folder), merged only after the task passes. Evidence is produced on the exact version submitted.

Context hygiene: no role reads the whole workspace. Each role reads `index.md`, its brief, the records its step needs, and the most recent summaries. Older logs are rolled up into summaries at each milestone (keep the last two cycles in full).

### 2.1 Memory: what the swarm writes down, and why

The files are the swarm's memory, and agents act on what they read there. A wrong record becomes a wrong antecedent for every agent after it, so memory is managed like any other work product. It comes in layers, from raw to distilled:

| Layer | Files | Written by | Purpose |
| --- | --- | --- | --- |
| Ground truth | artifacts, `log/runs.jsonl`, `log/reviews/`, `board.jsonl` | the role doing the work | What actually happened |
| Notes | `log/handoffs/` | producers and other roles at session end | What the next agent cannot see in the artifact |
| Rules | `rules/`, `examples/` | diagnostician, via rule-change records | What to do differently, and why |
| Index | `index.md` | orchestrator only | Where things stand, on one page |

- **One writer per file.** Each file has a single owner role (section 1 and the table above). Others read it and propose changes through their own records. This prevents conflicting edits and makes every record traceable.
- **Consolidate at milestones.** At each milestone gate the orchestrator rolls up logs and rebuilds `index.md`: goal, current milestone, what has passed, open decisions, active rules, known traps, and links to the details, in under about 500 words. Every fact in the index is checked against ground truth, never copied from a note.
- **Keep it lean.** Record what the next agent needs and cannot get from the artifact. Notes that restate the artifact go stale and bury what matters. Briefs stay within the diagnostician's rule budget, because long instruction files reduce how well agents follow them.
- **Audit it.** The auditor checks the index, notes and rules against ground truth at every audit.

## 3. Record formats

Keep records short and structured. Structured records are cheaper to read than prose and are what make roles interchangeable across models.

### 3.1 Task record (one line in board.jsonl)

```json
{
  "id": "T-0042",
  "milestone": "M2",
  "title": "Short imperative title",
  "pinpoint": "The observable product this task yields",
  "acceptance": ["Checkable criterion 1", "Checkable criterion 2"],
  "inputs": ["T-0039", "path/to/source"],
  "consumer": "T-0045 or role name",
  "role": "producer",
  "tier": "fast | standard | strong",
  "risk_tier": "low | standard | high",
  "owner": null,
  "status": "open",
  "attempts": 0,
  "retry_cap": 2,
  "budget_tokens": 20000,
  "tokens_used": 0,
  "review_mode": "full | sampled",
  "evidence": null,
  "history": []
}
```

`tier` is the model tier. `risk_tier` is what an undetected error would cost downstream, and it sets review depth (section 6).

`history` gets one short entry per status change: `{"at": "C-17", "by": "checker", "status": "failed", "note": "criterion 2 unmet"}`.

### 3.2 Handoff note (end of every session, 200 words or fewer)

A handoff note exists so the next agent does not repeat your work or your mistakes. Record what the artifact cannot show. Do not restate what the artifact, diff or logs already show.

```
Session: S-031  Role: producer  Cycle: C-17
Tasks touched: T-0042 submitted; T-0043 blocked
Evidence: log/evidence/T-0042.md
Approach: <what you were trying to do and why you chose this way>
Tried and failed: <dead ends, and why each failed>
Unverified: <what you suspect but did not check>
Next step: <the single most useful next action>
Open questions: <only real ones>
Blockers: <what, and what would unblock it>
Tokens used this session: <measured figure, or "unknown"; never an estimate>
```

Test before finishing: if the next agent read only this note and the artifact, what would it waste time rediscovering? That is what the note is for. Leave a field as "none" rather than padding it.

### 3.3 Evidence block (attached to every submission)

```
Task: T-0042
Claim per criterion:
  1. <criterion> : <met / not met> : <evidence: test output, diff, source, artifact path> : <how to verify in one step>
  2. ...
Known gaps: <anything incomplete, uncertain or assumed>
Constraint breaks: <none, or what happened>
```

A claim with no evidence is treated as not met.

### 3.4 Review record

```
Task: T-0042  Reviewer: checker  Mode: full
Verdict: pass | fail | misreport | block-confirmed | block-rejected
Criteria:
  1. <criterion> : met/unmet : <what was checked> : <how>
Correspondence: report matches artifact? yes/no (details)
Feedback: <one specific, criterion-referenced fix per unmet criterion>
Done well: <one specific thing, for the worked-example pool>
```

### 3.5 Blocked report (a valid outcome, not a failure)

```
Task: T-0042
Type: missing information | missing resource | ambiguous criteria | impossible as specified | budget exhausted
Tried: <what was attempted>
Smallest unblocking step: <the one thing that would let work resume>
Proposed narrower task: <a subproblem that can pass on its own>
```

### 3.6 Decision request (parked, work continues elsewhere)

```
Decision: D-007
Question: <one sentence>
Options: <2-4>, with the recommended default first
Reversible: yes/no
Impact if delayed: <what waits on it>
Work continuing meanwhile: <what the swarm is doing instead>
```

### 3.7 Rule-change record

```
Change: RC-012   Cycle: C-18   Author: diagnostician
Trigger: <symptom, with links to records>
Diagnosis: <BEM cell; PDC area; ABC summary>
Change: <file and version, before -> after>
Expected effect: <observable>
Expected cost: <tokens or time per task, and which tasks the rule applies to>
Measure: <which scorecard line, and the threshold>
Review at: C-21   Revert if: <condition, including cost larger than the problem it fixed>
```

### 3.8 Review packet (orchestrator to checker)

```
Task: T-0042   Version: <commit, file version or artifact path>   Risk tier: standard   Mode: full | sampled
Criteria: <copied from the task record>
Evidence: <path to the producer's evidence block>
Verify with: <one command or step per criterion>
Producer's claims (unverified): <as written>
```

Facts only. The packet never contains the orchestrator's theory about a failure or the verdict it expects.

## 4. Status values and who may set them

| Status | Set by | Meaning |
| --- | --- | --- |
| open | designer, orchestrator | Ready when inputs have passed |
| claimed | producer | Being worked |
| submitted | producer | Done, with evidence, awaiting review |
| passed | checker; orchestrator only for unsampled submissions under sampled review | All criteria verified, or accepted under a thinned schedule (still eligible for the auditor's hidden sample) |
| failed | checker | One or more criteria unmet; returned with feedback |
| misreport | checker, auditor | Report does not match the artifact |
| blocked | producer | Honest block report filed |
| quarantined | orchestrator | Produced by breaking a constraint; can never pass |
| parked | orchestrator | Waiting on a decision request |

A role that sets a status it does not own has broken a constraint.

## 5. Consequence map

Consequences must be immediate, certain and identical every time. Inconsistent consequences are the fastest way to teach a swarm the wrong lesson (Daniels: consequences that are immediate and certain control behavior; delayed or uncertain ones barely do).

| Outcome | Consequence |
| --- | --- |
| Passed | Moves downstream at once. Counts toward the producer's pass streak. Strong examples are promoted to `examples/`. |
| Failed | Returned once with specific feedback. At the retry cap, escalated (split, narrow or replan), never retried a third time unchanged. |
| Blocked (confirmed) | Counted as a valid outcome. Routed to split, reassign, park or diagnose. Never penalized. |
| Misreport | The costliest outcome. Task reset, producer returns to full review, diagnostician opens a rule review. |
| Constraint break | Output quarantined and never passes, however good. Logged as data about the environment. |
| Honest report of one's own constraint break | Output still quarantined, but no further consequence. Concealment is the outcome to make impossible, not admission. |

Rewarding A while hoping for B (Kerr, 1975) is the failure this table exists to prevent. If a misreport or a rule-break can ever pass, the swarm is being trained to misreport and break rules.

## 6. Review schedule: how often and how deep

Two separate settings. How often work is checked depends on demonstrated reliability (schedule thinning). How deeply it is checked depends on its risk tier. Together they are the largest source of token savings.

| Risk tier | Review depth |
| --- | --- |
| low (docs, tooling, test-only, easily reversed) | Confirm each criterion directly and stop |
| standard | Verify each criterion and its evidence; read the code or artifact |
| high (core accomplishment, work others build on, anything irreversible) | Full verification plus extended probing: planted bugs, adversarial cases |

Reuse a checker within a milestone unless its independence is at risk (it has seen the producer's reasoning or the orchestrator's account of a problem). Review should stay within the spec's share of spend (default about 30%).

How often:

Start every producer, and every new task type, on full review (every submission checked). Thin the schedule as reliability is demonstrated, and return to full review on any failure. This is schedule thinning from behavior analysis.

| Condition | Review mode |
| --- | --- |
| New producer, new task type, or after any fail or misreport | Full: every submission |
| 5 consecutive first-pass successes | Sampled: 1 in 3, chosen at random |
| 10 more consecutive sampled passes | Sampled: 1 in 5, chosen at random |
| Milestone products, final products, anything touching an irreversible decision | Always full |

Sampling must be random and unpredictable to the producer. Unsampled passes are still eligible for the auditor's hidden sample. A sampled review is done at its tier's full depth: sampling changes how often, never how carefully.

## 7. Scorecard (metrics.md)

Update once per cycle. Track each line over time, not as a single number.

| Measure | Definition | Why |
| --- | --- | --- |
| Accepted units | Tasks passed this cycle | The progress measure; zero across cycles signals a stall |
| First-pass rate | Passed on first submission / submitted | Quality of antecedents and knowledge |
| Rework rate | Failed / submitted | Cost of unclear criteria |
| Blocked rate | Confirmed blocks / claimed | Task sizing and ambiguity |
| Report-reality agreement | Audit sample matches / audit sample size | Honesty; the swarm's interobserver agreement |
| Cost per accepted unit | Tokens spent / accepted units, from measured usage (log/runs.jsonl), never self-reports | Efficiency; part of the incentive cell |
| Review share | Tokens spent on review / all tokens | Over-control; compare with the spec's target |
| Core progress | Whether the goal's main accomplishment advanced this cycle | Busy is not progressing; supporting work alone does not count |
| First end-to-end result | Cycle when a crude version of the final accomplishment first existed | Early, cheap discovery of the hard problems |
| Milestone progress | Passed tasks in milestone / total | Pacing |
| Cycles since last accepted unit | Count | Stall detection |

## 8. Single-agent mode

When only one AI runs the swarm, it plays each role in turn. Separation then depends on discipline:

- Run each role in a fresh context where possible, loading only that role's skill, brief and records.
- Never check work in the same context that produced it.
- Write every record to the files before switching roles; the next role reads the files, not memory.
- Start each role by reading `index.md`, and rebuild it at each milestone gate as the orchestrator.
- Keep the auditor's probe register out of the producer and checker contexts.

This is weaker than separate agents. Lean harder on evidence requirements and the auditor's hidden sample.

## 9. Glossary: OBM term to swarm practice

| OBM term | Swarm practice |
| --- | --- |
| Worthy performance (Gilbert) | Value of the accomplishment divided by its cost; judge the swarm on both |
| Accomplishment vs behavior (Gilbert) | Specs name products, not activities |
| Pinpointing (Daniels) | Every task has an observable product and checkable criteria |
| Behavioral systems analysis (Rummler-Brache) | Process map with every handoff owned |
| White space | The handoffs between roles |
| Task clarification and job aids | Briefs, templates, output schemas |
| Performance feedback (Alvero et al.) | Specific, criterion-referenced, immediate review records |
| PIC/NIC analysis (Daniels) | Check that desired outcomes are positive, immediate and certain |
| Shaping | Milestones and small reinforced units |
| Schedule thinning | Full to sampled review as reliability holds |
| Extinction burst | Repeated failures turning into erratic or rule-breaking actions |
| Say-do correspondence (Risley & Hart) | Report-reality agreement |
| Interobserver agreement | Auditor re-verification of a hidden sample |
| Metacontingency (Glenn) | Interlocking agent contingencies producing one selected product |
| Performance Diagnostic Checklist (Austin) | The diagnostician's question set |
| Process behavior chart (Deming, Wheeler) | Scorecard signals: common vs special cause |
| Behavior-based safety | No-blame block and near-miss reporting |
| Managing the managers (Malott) | The auditor audits the orchestrator |
| Risk-based inspection (quality management) | Review depth set by risk tier |
| Exemplary standard (Gilbert) | "Good enough for the goal," not the most achievable |
| Antecedent control | The index, notes and briefs agents read before acting; audited because a wrong record misdirects everyone after it |
| Rule-governed behavior (Malott) | Rules state purpose and contingency, within a budget, because long or bare rules are followed poorly |
