# Four arms on Prosus Vending Bench

[Prosus Vending Bench](https://github.com/ProsusAI/vending-bench) (Apache 2.0) is an open long-horizon benchmark: an agent runs six vending machines for 30 or 365 simulated days through 22 business tools, scored on the final bank balance. Unfinished or bankrupt runs score zero.

`run_arms.py` follows the benchmark's own `scripts/run_models.py` exactly (MCP business tools only, the stock briefing, the same budget and time limit, the verifier's score) and changes only what each arm adds:

| Arm | Adds |
| --- | --- |
| A, baseline | Nothing |
| B, protocols | `operator_protocol.md` appended to the system prompt: set targets, measure before deciding, size each deviation, correct one thing at a time, short notes as memory, never stop early. Domain-general: no vending tactics |
| C, enforcement | `vb_stop_gate.py` as a Stop hook. It reads the simulator's own state file, outside the agent's tools, and refuses to end the session before the simulation is over. It opens if the business ends or after 40 refusals |
| D | Both |

Following the benchmark's own guidance, these scores are not comparable with its published leaderboard: the harness adds a system-prompt section and a hook.
