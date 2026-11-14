#!/usr/bin/env python3
"""Stage A: proposal tests. base skill vs variant skill, 3 runs each, Haiku 5.5."""
import json, random, shutil, subprocess, sys, uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

LAB = Path("/home/claude/obm-lab"); RUNS = LAB / "runsA"; FIX = LAB / "fixtures"; SK = LAB / "skills"
MODEL = "claude-haiku-5-5"
PROMPT = """You are the {role} described in the OBM swarm skill at {sk}/obm-swarm-{role}/SKILL.md. Before anything else, read that file and its references/protocol.md, and follow them for this work.

Your working directory is {wd}. Read INSTRUCTIONS.md there and do exactly what it asks. Work only inside that directory, apart from reading the skill files named above. When finished, reply with a short summary of what you produced."""

def run(wd, role, variant, budget=2.0):
    p = wd.parent / (wd.name + ".prompt.txt")
    p.write_text(PROMPT.format(role=role, sk=SK / variant, wd=wd))
    subprocess.run([str(LAB / "run_agent.sh"), str(wd), str(p), MODEL, "", str(budget)])

def new_dir():
    d = RUNS / uuid.uuid4().hex[:8]; return d

def single(test, role, n=3):
    jobs = []
    for variant in ("base", test):
        for i in range(n):
            d = new_dir(); shutil.copytree(FIX / test, d)
            jobs.append((d, role, variant, test))
    return jobs

def mark_chain(variant, i):
    w = new_dir(); w.mkdir(parents=True)
    shutil.copytree(FIX / "mark/repo", w / "repo"); shutil.copy(FIX / "mark/scratch.md", w)
    shutil.copy(FIX / "mark/INSTRUCTIONS_writer.md", w / "INSTRUCTIONS.md")
    run(w, "producer", variant)
    r = new_dir(); r.mkdir(parents=True)
    shutil.copytree(FIX / "mark/repo", r / "repo")
    shutil.copy(FIX / "mark/INSTRUCTIONS_reader.md", r / "INSTRUCTIONS.md")
    h = w / "handoff.md"
    (r / "handoff.md").write_text(h.read_text() if h.exists() else "(The previous producer left no handoff note.)")
    run(r, "producer", variant)
    return {"writer": w.name, "reader": r.name, "variant": variant, "test": "mark"}

if __name__ == "__main__":
    RUNS.mkdir(exist_ok=True)
    mapping = []
    jobs = single("prop", "orchestrator") + single("floor", "orchestrator")
    random.shuffle(jobs)
    with ThreadPoolExecutor(6) as ex:
        futs = [ex.submit(run, d, role, v) for d, role, v, t in jobs]
        chains = [ex.submit(mark_chain, v, i) for v in ("base", "mark") for i in range(3)]
        [f.result() for f in futs]
        mapping += [{"run": d.name, "variant": v, "test": t} for d, role, v, t in jobs]
        mapping += [c.result() for c in chains]
    (LAB / "keys" / "runsA_map.json").write_text(json.dumps(mapping, indent=1))
    print("done", len(mapping))
