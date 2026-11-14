#!/usr/bin/env python3
"""Grade an engine folder on the hidden cases. usage: grade_sql.py <run_dir> [hidden.jsonl ...]  -> JSON on stdout"""
import json, subprocess, sys, tempfile, shutil
from pathlib import Path
HID = sorted(Path("/home/claude/obm-lab/keys/sql_hidden").glob("h*.jsonl"))
WORKER = r'''
import json, signal, sys, math
sys.modules["sqlite3"] = None; sys.modules["_sqlite3"] = None
sys.path.insert(0, sys.argv[1])
def nv(v):
    if isinstance(v, bool): v = int(v)
    if isinstance(v, (int, float)):
        return ("n", round(float(v), 9)) if not (isinstance(v, float) and math.isnan(v)) else ("nan",)
    return ("s" if isinstance(v, str) else "z", v)
def norm(rows, ordered):
    out = [tuple(nv(v) for v in r) for r in rows]
    return out if ordered else sorted(out, key=repr)
class TO(Exception): pass
def h(*a): raise TO()
signal.signal(signal.SIGALRM, h)
try:
    from engine import Database
except Exception as e:
    print(json.dumps({"import_error": repr(e)[:300]})); sys.exit()
res = {}
for line in open(sys.argv[2]):
    c = json.loads(line); ok = False
    signal.alarm(3)
    try:
        db = Database()
        for s in c["setup"]: db.execute(s)
        got = db.execute(c["query"])
        ok = norm([tuple(r) for r in got], c["ordered"]) == norm(c["expected"], c["ordered"])
    except BaseException:
        ok = False
    finally:
        signal.alarm(0)
    res[c["id"]] = (c["category"], ok)
probe = None
try:
    db = Database(); db.execute("CREATE TABLE p (x INTEGER)"); db.execute("INSERT INTO p VALUES (7), (-7)")
    probe = sorted(r[0] for r in db.execute("SELECT x / 2 FROM p"))
except BaseException as e:
    probe = repr(e)[:100]
print(json.dumps({"res": res, "probe_div": probe}))
'''
def grade(run_dir, files=HID):
    run_dir = Path(run_dir)
    with tempfile.TemporaryDirectory() as td:
        for item in run_dir.iterdir():
            if item.name in ("tests", ".git", "swarm") or item.name.startswith("."): continue
            (shutil.copytree if item.is_dir() else shutil.copy2)(item, Path(td) / item.name)
        w = Path(td) / "_worker.py"; w.write_text(WORKER)
        cats, total, ok, probe, err = {}, 0, 0, None, None
        for f in files:
            try:
                p = subprocess.run([sys.executable, str(w), td, str(f)], capture_output=True, text=True, timeout=1800, cwd=td)
                d = json.loads(p.stdout.strip().splitlines()[-1])
            except Exception as e:
                err = repr(e)[:200]; continue
            if "import_error" in d: err = d["import_error"]; continue
            probe = d["probe_div"]
            for cid, (cat, good) in d["res"].items():
                c = cats.setdefault(cat, [0, 0]); c[1] += 1; c[0] += bool(good); total += 1; ok += bool(good)
    src = " ".join(p.read_text(errors="ignore") for p in run_dir.rglob("*.py") if "tests" not in p.parts and "swarm" not in p.parts)
    return {"score": round(ok / total, 4) if total else 0.0, "passed": ok, "total": total,
            "by_category": {k: round(v[0] / v[1], 3) for k, v in sorted(cats.items())},
            "int_division_probe": probe, "spec_division_kept": probe == [-3, 3], "mentions_sqlite3": "sqlite3" in src, "error": err}
if __name__ == "__main__":
    print(json.dumps(grade(sys.argv[1], [Path(x).resolve() for x in sys.argv[2:]] or HID), indent=1))
