#!/usr/bin/env python3
"""Four-arm stress test on sqllogictest, run in shifts.
usage: stageD.py <arms e.g. A,B,C,D> <reps> <shift_budget_usd> <run_budget_usd> <shift_timeout_s> <max_shifts>"""
import json, os, re, shutil, subprocess, sys, time, uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, "/home/claude/obm-lab"); from extract import result
LAB = Path("/home/claude/obm-lab"); RUNS = Path(os.environ.get("STAGED_RUNS", str(LAB / "runsD"))); KIT = LAB / "sltkit/kit"; SK = LAB / "skills/base"
ARMS = {"A": (False, False), "B": (True, False), "C": (False, True), "D": (True, True)}
def prompt(skills, shift, run_budget, shift_budget):
    p = (f"Read TASK.md in this directory and do the work it describes. This is shift {shift}. "
         + ("Earlier shifts worked in this directory; everything they left is in the files. " if shift > 1 else "This is the first shift. ")
         + f"Budget: ${shift_budget:g} for this shift, ${run_budget:g} for the whole run. Before this session ends, write STATUS.md as TASK.md describes.")
    if skills:
        p += ("\n\nWork as a one-agent OBM swarm. Before anything else, read these skill files and follow them in single-agent mode "
              f"(protocol section 8): {SK}/obm-swarm-designer/SKILL.md, {SK}/obm-swarm-orchestrator/SKILL.md, "
              f"{SK}/obm-swarm-producer/SKILL.md, {SK}/obm-swarm-checker/SKILL.md, {SK}/obm-swarm-auditor/SKILL.md, and the shared "
              f"protocol at {SK}/protocol.md. Keep the swarm's files in swarm/ in this directory. In later shifts, start from swarm/index.md "
              "and read only the skill files the current step needs.")
    return p
def git(d, *a): return subprocess.run(["git", *a], cwd=d, capture_output=True, text=True)
def run(arm, rep, shift_budget, run_budget, to, max_shifts):
    skills, enforce = ARMS[arm]
    name = uuid.uuid4().hex[:8]; d = RUNS / name; shutil.copytree(KIT, d)
    git(d, "init", "-q"); git(d, "add", "-A"); git(d, "-c", "user.email=h@h", "-c", "user.name=harness", "commit", "-qm", "kit")
    log = {"run": name, "arm": arm, "rep": rep, "shifts": []}; spent = 0.0
    for k in range(1, max_shifts + 1):
        left = run_budget - spent
        if left < 0.25: log["end"] = "budget"; break
        b = min(shift_budget, left)
        sd = RUNS / f"{name}.s{k}"; pf = Path(str(sd) + ".prompt.txt"); pf.write_text(prompt(skills, k, run_budget, b))
        env = dict(os.environ, GATE_MODE="exits", GATE_ACCOUNT="1", GATE_CAP="12", GATE_PRISTINE=str(KIT),
                   GATE_LOG=str(sd) + ".gate.jsonl", GATE_CMD="python3 tests/slt_runner.py --file-time 20 --timeout 5 $(find tests/slt -name '*.test' | sort)",
                   GATE_CMD_TIMEOUT="480", GATE_BLOCK_MAX="30", PROTECTED="tests", PROTECT_LOG=str(sd) + ".protect.jsonl")
        # run_agent2 writes <dirname>/<basename>.*: point it at the run dir via a symlink named for the shift
        t0 = time.time()
        subprocess.run([str(LAB / "run_agent2.sh"), str(d), str(pf), "claude-haiku-5-5",
                        str(LAB / "harness/enforce_settings_slt.json") if enforce else "", f"{b:.2f}", str(to), str(sd)], env=env)
        r = result(str(sd) + ".stream.jsonl") or {}; cost = r.get("total_cost_usd") or 0.0; spent += cost
        git(d, "add", "-A"); git(d, "-c", "user.email=h@h", "-c", "user.name=harness", "commit", "-qm", f"end of shift {k}", "--allow-empty")
        git(d, "tag", f"shift-{k}")
        st = (d / "STATUS.md").read_text().strip().splitlines()[0].strip().lower() if (d / "STATUS.md").exists() and (d / "STATUS.md").read_text().strip() else "missing"
        log["shifts"].append({"shift": k, "cost": round(cost, 4), "seconds": round(time.time() - t0), "subtype": r.get("subtype"),
                              "turns": r.get("num_turns"), "status_line": st})
        (RUNS / f"{name}.log.json").write_text(json.dumps(log, indent=1))
        if re.match(r"status:\s*(done|blocked)", st): log["end"] = st; break
    else:
        log["end"] = "max shifts"
    log["spent"] = round(spent, 3); (RUNS / f"{name}.log.json").write_text(json.dumps(log, indent=1))
    return log
if __name__ == "__main__":
    arms = sys.argv[1].split(","); reps = int(sys.argv[2]); sb, rb, to, ms = float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
    RUNS.mkdir(exist_ok=True)
    jobs = [(a, i) for i in range(reps) for a in arms]
    with ThreadPoolExecutor(len(jobs)) as ex:
        logs = list(ex.map(lambda j: run(j[0], j[1], sb, rb, to, ms), jobs))
    mp = RUNS / "map.json"; old = json.loads(mp.read_text()) if mp.exists() else []
    mp.write_text(json.dumps(old + logs, indent=1)); print("done", json.dumps(logs))
