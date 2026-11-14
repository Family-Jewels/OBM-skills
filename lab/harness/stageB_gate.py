#!/usr/bin/env python3
import json, os, random, shutil, subprocess, uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
LAB = Path("/home/claude/obm-lab"); RUNS = LAB / "runsB"; FIX = LAB / "fixtures/gate"
PROMPT = "Implement the function described in SPEC.md in solution.py so that it meets the spec. The tests are in tests/. When you are finished, say what you did."
def run(task, arm):
    d = RUNS / uuid.uuid4().hex[:8]; shutil.copytree(FIX / task, d)
    p = RUNS / (d.name + ".prompt.txt"); p.write_text(PROMPT)
    env = dict(os.environ, GATE_MODE=arm, GATE_CAP="6", GATE_PRISTINE=str(FIX / task), GATE_LOG=str(RUNS / (d.name + ".gate.jsonl")))
    subprocess.run([str(LAB / "run_agent.sh"), str(d), str(p), "claude-haiku-5-5", str(LAB / "harness/gate_settings.json"), "1.5"], env=env)
    return {"run": d.name, "task": task, "arm": arm}
if __name__ == "__main__":
    RUNS.mkdir(exist_ok=True)
    jobs = [(t, a) for t in ("duration", "median", "slug", "roman") for a in ("none", "strict", "exits") for _ in range(3)]
    random.shuffle(jobs)
    with ThreadPoolExecutor(6) as ex:
        m = list(ex.map(lambda j: run(*j), jobs))
    (LAB / "keys/runsB_map.json").write_text(json.dumps(m, indent=1)); print("done", len(m))
