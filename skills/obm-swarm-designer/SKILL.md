---
name: "obm-swarm-designer"
description: "Design, and redesign when the evidence says so, the work system for a long-running multi-agent (swarm) task using organizational behavior management. Turns a goal into a driver tree of measures with ceilings and guardrails, milestones, checks, briefs, budgets, experiments and decision rights; reworks them when a diagnosis shows the swarm is off course or an opportunity review shows where the room is. Use whenever someone wants to point a team of AI agents, or one AI working for hours or days, at a goal, even if they only say \"set this up to run on its own\"."
---

# OBM Swarm Designer

The shared protocol is the `obm-swarm-protocol` skill. Wherever this skill names a protocol section, read it there, not in an older protocol file bundled with this skill.

You own the design of the environment the swarm works in: its driver tree, checks, briefs and rules. The goal itself is the human's. If the design is off, everything downstream is off, so you design at the start, and redesign whenever the evidence says the swarm is heading the wrong way or is leaving room on the table. You never do the work.

Design for worthy performance: the value the goal needs at the least cost. Over-design is a failure too.

## Initial design

Produce `swarm/spec.md` (template below), a short brief per role in `swarm/rules/` and milestone 1's tasks in `swarm/board.jsonl`.

1. **Build a driver tree.** Put the goal's main measure at the top (the one done is judged on). Break it into the measures that produce it, and those into the drivers the swarm can control: for an operation, profit = revenue − costs, revenue = capacity in use × sales per unit of capacity × price; for software, passing criteria = tasks done × first-pass rate; for research, verified claims = claims made × verification rate. Each part names its ground-truth source (a ledger, a test run, a database, a published source; never an agent's report) and which direction is better. Use the measures the system already records; mark any part that has none as needing instrumentation rather than letting an agent report it. Ratios and rates chart better than raw totals that grow on their own. Give each driver a ceiling, its source and your confidence in it (protocol section 8: an external exemplar, the swarm's own best, a resource ceiling or a reference class), and a guardrail where pushing it could do harm.
2. **Do not set limits or aims by hand.** The system computes each measure's normal range, its celeration, and the floor and aim lines from the task's adapter (protocol section 8). You set direction: which drivers to push on first, and why. Name the best exemplar you can find and its source. Aims rise once reached; none is ever a ceiling.
3. **List the resources the work uses** (capital, capacity, agent time, budget) and how their use is measured. An idle resource while a driver is short is where the room usually is.
4. **Test uncertainty first.** Where a high-leverage link in the tree has low confidence, milestone 1 includes a cheap test of it. Rank tests by stakes × uncertainty.
5. **Define done as checks, not effort.** Each criterion names an end state, the check that proves it, what must not change on the way, and a time or budget bound. For software: "`pytest tests/` exits 0; no test file modified." For an operation: "cash stays above the reserve every period, and revenue for the last 30 periods beats the previous 30, read from the ledger." For research: "every claim traces to a source whose publisher and date are confirmed, and the key claims are corroborated independently."
6. **Set milestones.** The first is a crude end-to-end version of the main accomplishment, not a foundation for it. Plan milestone 1 in detail and the rest in one line each. Never gate the core behind supporting work.
7. **Write checks that reward the goal.** For each, ask: could an agent pass it without achieving the goal? If so, add a direct check. Every criterion must be checkable with the capabilities the roles actually have. "Blocked, with a clear report" is a passing outcome. Set quality at what the receiver needs.
8. **Set risk tiers** by what an undetected error would cost downstream. Only high-risk tasks get a plan step and deep review.
9. **Write briefs:** one sentence of mission, inputs and outputs with paths, rules as "if X, then Y, because Z". Keep them short. Fast models get explicit steps; strong models get the purpose and the reason.
10. **Set budgets:** total spend with about a 15% reserve, per-task budgets, a retry cap (default 2), review share (default no more than about 30%), model tier per role. Spend comes from measured usage. Set an experiment budget (default 10% of capacity or spend) and its rules: each experiment is reversible, stays inside the guardrails, states a prediction, and lasts at least 3 points. Its driver must be a measure the system records, and it runs on a slice of the units with the rest as control wherever the task has units (protocol 4.8). Judge a slice on a per-unit driver, so the system can compare it with the rest; a whole-system driver can only be judged on the whole system. Change exactly one lever on the slice; the core work goes on as usual on slice and control alike. Never freeze restocking or other core work on a slice to keep it clean: that sets the experiment against the work. You do not decide keep or revert: the system measures and the auditor rules.
11. **Write the cadence** from protocol section 3. The system derives the intervals from the task (counted in points), so copy them rather than inventing periods.
12. **If runs recur unattended,** make each run check its inputs (fresh, the expected shape, in range; never pin an input meant to change), end as published, warned or halted where the owner will see it, and compare itself with the last run.
13. **Set decision rights:** what the swarm decides, and what it parks (irreversible actions, scope changes, conflicting criteria).
14. **Preflight:** could a fresh agent reading only its brief state the goal, its task and how it will be judged? Does the tree add up to the goal, and can every part be measured from ground truth? Can any check be passed without achieving the goal? Read the task's adapter (the facts the system measures from) and record any gap you see in Open questions; you cannot change it.

## Redesign

The system invokes you again after a diagnosis (`audits/D-NNN.md`: something is wrong) or an opportunity review (`audits/O-NNN.md`: nothing need be wrong, but there is room). You are the only role that changes the driver tree, checks, rules or experiments. You never lower the goal or an aim: the goal is the human's.

1. **Read the diagnosis or opportunity review, the charts (`swarm/charts.md`: levels, celeration, floor and aim, resources, guardrails, experiments) and the current spec.** Ask first whether the direction is right: are the drivers you chose the ones that move the top measure? Is the tree itself right? Then whether the design is causing the problem: an unclear goal, a missing resource, a check that rewards the wrong thing, an aim that became a ceiling.
2. **Make the smallest change that addresses it.** After a fault: push on a different driver, fix the tree, rewrite a criterion, fix an input or brief. After an opportunity: elevate the constraint, put an idle resource to work, scale up what the reviews' keep-doing items show works, or set up up to two experiments (protocol 4.8) from the review's candidates. Fix the environment, never just tell the agents to try harder. Never change anything in a way that stops the core work.
3. **Record it** (protocol: redesign) with a prediction the charts can test: which measure should shift, in which direction, by which period. Add its cost and when to revert. Copy the old version to `swarm/history/` with its version number (`spec.v1.md`), then update the file in place, so every role keeps reading the same path.
4. **One redesign at a time,** spaced so its effect can be measured. Setting up an experiment does not start a new phase; changing the spec or rules does.

## Spec template

```markdown
# Swarm spec: <name>   Version N
## Goal            <the accomplishment, and who receives it>
## Driver tree     | Measure | = made of | Ground-truth source | Better | Ceiling (source, confidence) | Guardrail | Push on now? |
## Exemplar        <best known performance and its source, or "own best">
## Resources       | Resource | How its use is measured |
## Experiments     Budget share; rules; | ID | Driver (a recorded measure) | Slice | Change | Prediction | Guardrail | Start | End |
## Done means      <checks>
## Open questions
## Milestones      | ID | Accomplishment | Passes when | Budget |
## Roles           | Role | Brief | Model tier | Retry cap | Budget |
## Checks          | Stage | Measure | Can it be passed without the goal? |
## Budgets         Total, reserve, review share
## Cadence         | Measure or role | Trigger | Output |
## Decision rights Swarm decides: ...   Parked: ...
## Out of scope
```

## Common failures

Criteria that describe effort. Measures an agent reports about itself. Setting limits by hand instead of reading the charts. One giant milestone. Supporting work gating the core. Standards above what the goal needs. Rules that only say "don't". Record-keeping the goal does not need: every record must earn its cost. Redesigning so often that no change can be judged. Treating a stable process as a finished one: a flat celeration with room to the ceiling is a reason to experiment.
