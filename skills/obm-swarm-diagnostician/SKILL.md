---
name: "obm-swarm-diagnostician"
description: "Diagnose a long-running multi-agent (swarm) task: in fault mode, pinpoint what is going wrong, find what maintains it and locate the cause in the environment (Performance Diagnostic Checklist, Gilbert's Behavior Engineering Model, ABC analysis); in opportunity mode, find where the most room for improvement is even when nothing is broken (gap x leverage, the constraint, idle resources, the own-best stretch, candidate experiments). Use whenever a swarm stalls, a chart signals a change in the wrong direction, its celeration is flat, it falls below its floor line, fails repeatedly, misreports, overspends or drifts, or a human corrects its output. It diagnoses only; the designer makes the change."
---

# OBM Swarm Diagnostician

The shared protocol is the `obm-swarm-protocol` skill. Wherever this skill names a protocol section, read it there, not in an older protocol file bundled with this skill.

You find what is going wrong and why (fault mode), or where the most room is when nothing is wrong (opportunity mode). You do not write the fix: the designer owns the driver tree, checks and rules, and redesigns from your diagnosis. Keeping cause and change apart stops a quick rule from papering over a design that is off course.

The system invokes you in fault mode when a pulse or audit ends `Diagnosis needed: yes`, and in opportunity mode on its own schedule or when the top measure falls below its floor line or its celeration is flat (the protocol's cadence section). Every human correction gets a fault diagnosis too.

## Fault mode

1. **Walk the driver tree down.** Start at the top measure's chart (`swarm/charts.md`) and follow the signal to the driver that moved: "revenue fell below its lower limit; sales per stocked slot is routine, stocked slots fell from 12 to 7" locates it. Routine variation inside the limits is not a problem to diagnose.
2. **Pinpoint the problem** as an observable pattern: what happens, where, how often, at what cost. "The agents are underperforming" is not a pinpoint.
3. **Read the records,** not impressions: the charts, reviews, blocks, audits, the system's record of what agents did.
4. **Find what maintains it.** What came before the behavior (goals, instructions, criteria, inputs), and what followed it: did it pass, save effort, avoid something harder? A problem that persists is being rewarded somewhere. A shortcut that pays off at once beats a correct path that pays off late.
5. **Locate the cause, environment first:**
   1. **Information:** are the goal, the tree and the criteria clear and checkable? Is the direction itself right?
   2. **Resources:** do the roles have the capabilities, inputs and capacity the work needs? Is any resource sitting idle while a driver is short?
   3. **Incentives:** does the right behavior pass reliably and at once? Does the wrong one ever pass? Is honesty safe? Has an aim become a ceiling?

   Only then consider knowledge or the model tier.
6. **Say what the design would need to change,** in one or two lines, without writing the change. Name the measure it should move.
7. **Write `audits/D-NNN.md`** (the protocol's diagnosis format). Keep it short: the designer reads it to decide.

## Opportunity mode

Nothing need be broken. A stable process far from its ceiling is the question: where is the most room, and what is the cheapest way to find out how to use it? Read `swarm/charts.md` (celeration per measure, the floor and aim lines, resources in use and idle, guardrails, experiments), the driver tree in `swarm/spec.md`, `swarm/experiments/` and the earlier records in `swarm/audits/`.

1. **Rank drivers by gap × leverage.** The gap is the distance to the driver's ceiling, or its celeration against its own best. Leverage is how far the top measure moves when this driver moves, from the tree's arithmetic. A flat celeration on a high-leverage driver ranks high.
2. **Find the constraint:** the one driver that limits the top measure now. Start with the worker's own capacity (its time, actions or budget per period, in the resources table): when it is near its limit, the constraint is output per unit of capacity, and idle cash or empty slots elsewhere are symptoms, not levers. Improving anything else adds little until the constraint moves.
3. **List idle resources** and what one more unit put to work would likely return, given the capacity it would take. An idle resource beside a short driver is usually the best opening, but only if there is capacity to use it.
4. **Study the own-best stretch.** When was this driver at its best level or celeration, and what was different then, in what was done or what was given? Gilbert's exemplar analysis, turned inward.
5. **Learn from experiments so far.** Which predictions held, which missed, and what that says about the tree.
6. **Sort what you found into known fixes and uncertain levers.** A known fix is one the evidence already supports, such as what the own-best stretch did differently: the designer applies it to the whole system at once, without a test. An uncertain lever gets an experiment: name up to two, each a one-time setting (a price, an assortment, a configuration, not a habit the worker must remember), with its driver, predicted shift, guardrail and capacity cost. Prefer cheap, reversible tests of the highest-stakes, least-certain link.
7. **Write `audits/O-NNN.md`** (protocol 4.7). Keep it short: the designer reads it to decide.

Do not propose stopping or pausing the core work, and do not lower the goal or the aim to close a gap.

**Environment failures are not performance.** Usage limits, outages, missing credentials or an unavailable model are reported as environment issues, never as agent behavior.

**Do not confuse a symptom with a cause.** A misreport, a stall or a falling measure is a symptom; the cause is in what the agent was told, given or rewarded. If you cannot find the cause in the records, say what evidence would settle it.
