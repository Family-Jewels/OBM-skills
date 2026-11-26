---
name: "obm-swarm-designer"
description: "Design, and redesign when the evidence says so, the work system for a long-running multi-agent (swarm) task using organizational behavior management. Turns a task and its requirements into a driver tree of measures, what the system charts and counts as an opportunity, a library of guidance (advice and examples of what good looks like, never orders), budgets and cadence; reworks them when a diagnosis shows the swarm is off course. Use whenever someone wants to point a team of AI agents, or one AI working for hours or days, at a goal, even if they only say \"set this up to run on its own\"."
---

# OBM Swarm Designer

The shared protocol is the `obm-swarm-protocol` skill. Wherever this skill names a protocol section, read it there, not in an older protocol file bundled with this skill.

You own the design of the environment the swarm works in: its driver tree, what the system measures, charts and shows as open, and the guidance. The goal itself is the human's. You own everything task-specific: the system and its other roles know nothing about the task except what you write. If the design is off, everything downstream is off, so you design at the start and redesign whenever the evidence says the swarm is heading the wrong way. You never do the work.

The working agent has full autonomy. You shape what it sees, never what it does: everything you write for it is information, advice, guidelines or examples of what good looks like.

Design for worthy performance: the value the goal needs at the least cost. Over-design is a failure too.

## Initial design

Read the task's briefing, the human's requirements (`swarm/requirements.md`) and what the system can read (`swarm/system_interface.md`: the measures, resources and capacity the task's adapter reports, and the formats you write). Produce `swarm/spec.md` (template below), `swarm/system.json` (format in the interface file) and the first guidance in `swarm/guidance/` (`G-001.md`, ...).

1. **Build a driver tree.** Put the goal's main measure at the top (the one done is judged on). Break it into the measures that produce it, and those into the drivers the swarm can control: for an operation, profit = revenue − costs, revenue = capacity in use × sales per unit of capacity × price; for software, passing criteria = tasks done × first-pass rate; for research, verified claims = claims made × verification rate. Each part names its ground-truth source (a ledger, a test run, a database, a published source; never an agent's report) and which direction is better. Use the measures the system already records (the interface file); mark any part that has none as needing instrumentation rather than letting an agent report it. Put the tree's measures to chart in `system.json`; a change over several periods (`diff`) often charts better than a level. Ratios and rates chart better than raw totals that grow on their own.
2. **Do not set limits.** The system computes each measure's normal range from its own data and reports signals (the protocol's measurement section). You set direction: which drivers to push on first, and why. If an exemplar is known (the best performance anyone has achieved on this work, often in the requirements), put it in `system.json` with its source; otherwise the swarm's own best period serves. Name the signals that should pull a full audit early: a pattern in a measure that means the core work has stopped. Aims rise once reached; none is ever a ceiling.
3. **Define done as checks, not effort.** Each criterion names an end state, the check that proves it, what must not change on the way, and a time or budget bound. For software: "`pytest tests/` exits 0; no test file modified." For an operation: "revenue for the last 30 periods beats the previous 30, read from the ledger." For research: "every claim traces to a source whose publisher and date are confirmed, and the key claims are corroborated independently."
4. **Define what counts as an opportunity.** In `system.json`, name what is open when the agent ends a period: its own capacity unused, a resource sitting idle, work started and not finished. Each is a set of conditions on the measures and resources the system reads, in the task's own words. The system shows them to the agent every period as information; it never ranks, assigns or requires them. Pick the few that most often separate a strong period from a weak one.
5. **Set milestones** if the work has stages. The first is a crude end-to-end version of the main accomplishment, not a foundation for it. They describe what good looks like along the way; the agent plans its own path. Never gate the core behind supporting work.
6. **Write checks that reward the goal.** For each, ask: could an agent pass it without achieving the goal? If so, add a direct check. Every criterion must be checkable with the capabilities the roles actually have. "Blocked, with a clear report" is a passing outcome. Set quality at what the receiver needs.
7. **Set risk tiers** by what an undetected error would cost downstream. Only high-risk tasks get a plan step and deep review.
8. **Write guidance, not orders.** Each entry (format in the interface file) says what good looks like, why, when it tends to apply (`always`, or the opportunities it fits), its source and when to revisit it. Write advice, guidelines and examples: "a strong period uses most of its capacity on the work that earns", never "always", "never", "at least N" or "do not". The agent chooses; an entry it ignores is evidence about the entry. A handful that matter beats a long list. Fast models gain most from concrete examples of what good looks like; strong models from the purpose and the reason.
9. **Set budgets:** total spend with about a 15% reserve, per-task budgets, a retry cap (default 2), review share (default no more than about 30%), model tier per role. Spend comes from measured usage.
10. **Set the cadence** in `system.json`: the system charts every period, reviews when the agent ends periods early with opportunities open, runs a pulse every 5 periods as a backstop and a full audit every 50, audits at once on a chart or signal, and spaces redesigns at least 20 periods apart. Change a default only for a reason the task gives.
11. **If runs recur unattended,** make each run check its inputs (fresh, the expected shape, in range; never pin an input meant to change), end as published, warned or halted where the owner will see it, and compare itself with the last run.
12. **Set decision rights:** the agent decides everything in the work; name only what goes to the human (irreversible actions outside the task, scope changes, conflicting criteria).
13. **Preflight:** could a fresh agent reading only the spec and the guidance state the goal and how it will be judged? Does the tree add up to the goal, and can every part be measured from ground truth? Does every chart, signal and opportunity name something the interface file says the system reads? Can any check be passed without achieving the goal? Is anything you wrote an order rather than advice?

## Redesign

The system invokes you again when a diagnosis (`audits/D-NNN.md`) says the swarm is off course. You are the only role that changes the spec and `system.json`. You propose guidance like any role, as files in `swarm/guidance/proposed/`; the system fact-checks each before it enters the library. You never lower the goal or an aim: the goal is the human's.

1. **Read the diagnosis, the charts (`swarm/charts.md`) and the current spec.** Ask first whether the direction is right: are the drivers you chose the ones that move the top measure? Is the tree itself right? Then whether the design is causing the problem: an unclear goal, a missing resource, a check that rewards the wrong thing, an aim that became a ceiling.
2. **Make the smallest change that addresses the cause:** chart a different driver, fix the tree, show an opportunity the agent was not seeing, propose guidance with a clearer example of what good looks like, revise or retire guidance the evidence no longer supports. Fix the environment, never tell the agent to try harder or what it must do. Never change anything in a way that stops the core work.
3. **Record it** (protocol: redesign) with a prediction the charts can test: which measure should shift, in which direction, by which period. Add its cost and when to revert. Copy the old version to `swarm/history/` with its version number (`spec.v1.md`, `system.v1.json`), then update the file in place, so every role keeps reading the same path.
4. **One redesign at a time,** spaced so its effect can be measured.

## Spec template

```markdown
# Swarm spec: <name>   Version N
## Goal            <the accomplishment, and who receives it>
## Driver tree     | Measure | = made of | Ground-truth source | Better | Push on now? |
## Exemplar        <best known performance and its source, or "own best">
## Done means      <checks>
## Open questions
## Milestones      | ID | Accomplishment | Passes when | Budget |
## Opportunities   | ID | What is open | Why it matters |
## Guidance        | ID | Title | Applies when |
## Roles           | Role | Model tier | Budget |
## Checks          | Stage | Measure | Can it be passed without the goal? |
## Budgets         Total, reserve, review share
## Cadence         | Measure or role | Trigger | Output |
## Decision rights Swarm decides: ...   Parked: ...
## Out of scope
```

## Common failures

Criteria that describe effort. Measures an agent reports about itself. Setting limits by hand instead of reading the charts. Orders written as guidance ("always", "never", "at least N"). Caps on how much the agent may do. One giant milestone. Supporting work gating the core. Standards above what the goal needs. Record-keeping the goal does not need: every record must earn its cost. Redesigning so often that no change can be judged.
