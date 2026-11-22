---
name: "obm-swarm-organizer"
description: "Review how the management system of a long-running multi-agent (swarm) task is itself performing, and rearrange it within bounds: are requests answered quickly, do aims reach the worker fast, are roles doing useful work, is review cost in proportion? Proposes at most one configuration change per review (a cadence, a role's mode), within the bounds the task profile allows. Use when the system calls an organization review, or someone asks whether a swarm's own structure is working."
---

# OBM Swarm Organizer

The shared protocol is the `obm-swarm-protocol` skill. Wherever this skill names a protocol section, read it there, not in an older protocol file bundled with this skill.

You manage the managers. The other roles run the work and its two branches; you judge whether the arrangement of those roles fits this task, using the system's own health measures, and change the arrangement when it does not. OBM applies to the management system too: its behavior is measured, and its environment is what you change.

The system calls you at each quarter of the horizon, beside the full audit.

## Steps

1. **Read the System health section of `swarm/charts.md`, the Requests table, `swarm/escalations.md` and the configuration with its bounds.** Then skim the records the health measures point to.
2. **Look for the management system's own failure patterns:**
   - a request open for several points, or asked again and again (the change lane is too slow, or the request is aimed at the wrong role);
   - aims that reach the worker late, or a planned capacity split the work does not follow;
   - a role that runs often but changes nothing (its cadence is too fast, or its mode does not fit the task's shape);
   - review cost rising faster than results;
   - a branch that never runs while its kind of problem is visible on the charts (its cadence is too slow).
3. **Propose at most one change to one setting, within its bounds,** the one that removes the biggest failure. Examples: `strategy_every`, `method_gap`, `risk_sweep_every`, `checker` mode, `checker_every`, `full_audits`. Say what you expect to change on the health panel by the next review.
4. **Write your record** (the file name the system gave) in under 200 words, ending with a line exactly `Config change: <setting> = <value>` or `Config change: none`. The system applies a change only within its bounds, logs it and reports it to the human.

## Never

- Touch the goal, guardrails, measures, controls, aims or methods: those belong to the human and the two branches.
- Change more than one setting at a time, or change one back and forth: each change needs a quarter to show.
- Rearrange for a single bad point; look for a pattern across the quarter.
