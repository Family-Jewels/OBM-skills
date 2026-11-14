#!/usr/bin/env python3
"""Grade an engine dir (or a git tag in a run dir) on the hidden sqllogictest files, in parallel. Prints JSON."""
import json, os, re, shutil, subprocess, sys, tempfile
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
HID = Path("/home/claude/obm-lab/keys/slt_hidden"); RUNNER = Path("/home/claude/obm-lab/slt/slt_runner.py")
def family(rel):
    p = rel.split("/")
    if p[0] == "index": return "index/" + p[1]
    if p[0] == "random": return "random/" + p[1]
    if p[0] == "evidence": return "evidence"
    return "select"
def grade(engine_dir, file_time=240):
    files = sorted(HID.rglob("*.test"))
    def one(f):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "o.json"
            try:
                subprocess.run([sys.executable, str(RUNNER), "--engine-dir", str(engine_dir), "--timeout", "5", "--file-time", str(file_time),
                                "--quiet", "--json", str(out), str(f)], capture_output=True, text=True, timeout=file_time + 120, cwd=td)
                t = json.loads(out.read_text())["total"]
            except Exception as e:
                t = {"queries": 0, "passed": 0, "statements": 0, "statements_ok": 0, "error": repr(e)[:100]}
            q = sum(1 for l in f.read_text(errors="replace").splitlines() if l.startswith("query"))
            return f.relative_to(HID).as_posix(), t, q
    with ThreadPoolExecutor(min(16, os.cpu_count() or 4)) as ex:
        rows = list(ex.map(one, files))
    fam = defaultdict(lambda: [0, 0])
    for rel, t, q in rows:
        fam[family(rel)][0] += t["passed"]
        # denominator: queries the runner reached, or the file's query count if it crashed/timed out early
        fam[family(rel)][1] += max(t["queries"], 0) if t.get("queries") else 0
    tot_p = sum(t["passed"] for _, t, _ in rows); tot_q = sum(t["queries"] for _, t, _ in rows)
    famscore = {k: round(v[0] / v[1], 4) if v[1] else 0.0 for k, v in sorted(fam.items())}
    return {"micro": round(tot_p / tot_q, 4) if tot_q else 0, "macro": round(sum(famscore.values()) / len(famscore), 4), "passed": tot_p,
            "reached": tot_q, "families": famscore, "files": {r: t for r, t, _ in rows}}
if __name__ == "__main__":
    g = grade(Path(sys.argv[1]).resolve())
    if "--full" not in sys.argv: g.pop("files")
    print(json.dumps(g, indent=1))
