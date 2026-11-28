# Long-run kit: what the system does so the agent doesn't have to remember

Built from [scoring every run to date](../../results/2026-11-27-behavior-analysis). The finding behind it: every behaviour that depended on the agent remembering decayed within days or weeks. That covered calling reviewers, keeping its log, following standing rules and judging its own changes. Every behaviour the harness carried out survived the whole year. So this kit moves four jobs from the agent to the system. The [`obm-long-run`](../../skills/obm-long-run/SKILL.md) skill tells the agent what is left to it.

| File | Job it takes from the agent | Finding it answers |
| --- | --- | --- |
| `steps_hook.py` + `steps.py` | **Recording the movement cycle.** A hook writes one line per tool call: what was called, on what, whether it failed, and a content hash for reads. It turns that record into behaviour measures and hands the agent a cue when a pattern starts | No run kept a step-level record, so extra behaviour and stalls could only be guessed from cost. In 7 of 11 runs the worker's log stopped early, went silent for months or was never dated. In 3 of the 5 full logs, entries grew two to three times longer by the last quarter |
| `verify.py` (wired into engine v4) | **Judging changes.** A method change ends with one machine-readable line. The system tests it with the protocol's signal rule against limits from before the change, counted from adoption, with the chance rate beside it. A miss goes back to the designer as a request that must be answered | Prose predictions came true about as often as chance (15 of 38 against 11.9). A third named measures nobody charts, and 7 were already due when adopted |
| `skill_gate.py` | **Deciding to adopt a skill the run built for itself.** Adopted only with gap evidence, a build-or-skip decision, held-out tests run with and without the skill, and an independent review with every finding answered | Gaps were found reliably, but changes were adopted without evidence they worked, and reviews happened only when the system scheduled them |
| `test_longrun.py` | Tests for all three, including a replay on a real run where the verifier and the analysis scorer must agree | |

## The step record and its cues

Each line of `steps.jsonl`:

```json
{"i": 412, "t": 1795125318.2, "tool": "Read", "kind": "read", "target": "/ws/swarm/spec.md", "sig": "9f2c1a7e44b0", "ok": true, "out": 5120, "hash": "a1b2c3d4e5f60718"}
```

`kind` is one of read, write, run, task_read, task_act, agent, skill or other. Task tools are any MCP tools. Read-only ones are named by patterns (`get_*`, `list_*`, `check_*` and so on), and shell commands such as `cat` and `grep` count as reads. `sig` is the same for the same call made again.

The cues are the ranking signals from the design discussion: freshness, de-duplication, relevance and cost. They are computed by the system and handed over as antecedents, so the agent never has to score its own options. Each fires once, when its condition starts:

| Cue | Fires when | Says |
| --- | --- | --- |
| Freshness | A file is read again and its content hash has not changed since the agent last read it | Use what you read |
| Diversity | The same call fails a second time with the same input | Change the input or route, or record a block |
| Relevance | `no_progress_steps` steps pass with no successful state-changing action | Change something toward the goal, or record a block |
| Placement | A write lands outside the workspace roots | Records belong at their protocol paths |
| Economy | The agent's own logs grow past `log_bytes_per_window` within `window` steps | One line per event |

`steps.py summarize steps.jsonl` prints the behaviour measures for a finished run. These are the step counts by kind, state-changing share, unchanged re-reads, repeated failures, retries unchanged, the longest stretch with no state change, writes outside the workspace and bytes written to the agent's own logs. The hook writes the same panel to `step_health.md` every `health_every` steps.

### Wiring (Claude Code hooks)

```json
{"hooks": {"PostToolUse": [{"matcher": ".*", "hooks": [{"type": "command", "timeout": 20,
  "command": "python3 -I /path/to/lab/longrun/steps_hook.py /path/to/steps.json"}]}]}}
```

```json
{"steps_log": "/run/out/steps.jsonl", "health_md": "/run/ws/swarm/step_health.md", "workspace_roots": ["/run/ws"],
 "own_logs": ["swarm/log/progress.md"], "cues": true, "no_progress_steps": 20, "repeat_failures": 2,
 "window": 50, "log_bytes_per_window": 8000, "health_every": 25}
```

- **Observation only.** `"cues": false` records every step without intervening. The vending runner (`../vending2/run_arms2.py --steps observe`, the default) does this for every arm and adds the summary to `result.json`. That makes the movement cycle comparable across arms, and the step record is kept with the results. `--steps cue` makes the cues an intervention, so run it as an arm of its own.
- **Keep the step log out of the agent's write paths.** The runner writes it to the run's output folder, outside the workspace. With `../harness/protect_paths.py`, add its path to the protected list.
- **The hook never fails or blocks a tool call.** Parallel calls are serialised with a file lock.

## Change verification

The method change record ends with:

```
Prediction: slots_selling up within 2 points
```

At adoption, engine v4 registers the prediction and the routine variation before the change. A prediction it cannot judge goes to the designer as a request, never as a guess: either there is no line, or the line names a measure the system does not chart. Once the window has passed, the system writes the verdict to `charts.md` under "Change verdicts": shift as predicted, no shift, the wrong way, or not enough data. The chance rate sits beside it, and the System health panel gives hits against hits expected by chance. "No shift" and "the wrong way" are filed as requests to the designer: keep, revise or revert, with the reason.

## The build gate

```
python3 -I skill_gate.py <skill-folder>      exit 0 adopt · 1 do not adopt (reasons listed) · 2 decided not to build
```

It only reads. The folder layout is in the module's docstring: `decision.md`, `SKILL.md`, `tests/cases.jsonl`, `verification.json` and `reviews/*.md`. "Skip" and "inline" are honest exits. A reviewer who is also the author does not count. No measured gain on the held-out cases means no adoption.

## Not built yet

- **Resuming after a cutoff.** Fifteen long runs ended on a usage limit or timeout. All state is in files, but the runner does not resume from them. It needs the benchmark's own environment to build and test.
- **The obm-long-run skill in a live arm.** The runner installs `obm-swarm-*` skills only, so existing arms are unchanged. A new arm should install `obm-long-run` with the step cues on and compare against `--steps observe` on the same seeds.

## Tests

```bash
python3 -I test_longrun.py                 # the kit
python3 -I ../cadence/test_engine_v4.py    # the engine, including change verdicts (case 8)
```
