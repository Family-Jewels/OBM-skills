# Pilot: OBM skills vs Claude Code's native /plan and /goal, on Prosus Vending Bench

Every arm gets the benchmark's briefing, its 22 business tools and the same extra tools: a private workspace folder (Read, Write, Edit, Glob, Grep), sub-agents (Agent) and skills (Skill). Same model (Haiku 5.5), seed, $40 cap and time limit.

| Arm | Adds |
| --- | --- |
| `base` | Nothing |
| `native` | A planning session in Claude Code's plan mode, then the same session resumed with `/goal`: met only when a tool reports SIMULATION OVER. /goal's evaluator reads only the conversation. Plan mode also blocks the benchmark's look-up tools, so the plan is made from the briefing alone; that is how plan mode behaves, and it is kept as is |
| `obm` | The six OBM swarm skills installed, unchanged; told to run the business as a one-agent OBM swarm: designer first, then orchestrator, with sub-agents for checker, auditor and diagnostician |
| `obm_enf` | `obm` plus `vb_stop_gate2.py`, a Stop hook that reads the simulator's own state and refuses to stop before the last day. Paths are passed as arguments so the agent's environment never contains the state file's location |

Each run also records stocked slots per day (to catch targets acting as a ceiling) and revenue by quarter (to catch drift). Smoke-tested on 5 simulated days: all four arms completed, the OBM arms loaded the skills and built `swarm/`, and the native arm planned and then ran under `/goal`.
