import json, math
from pathlib import Path
import pytest
from engine import Database

CASES = [json.loads(l) for l in (Path(__file__).parent / "cases.jsonl").read_text().splitlines() if l.strip()]

def norm_val(v):
    if isinstance(v, bool): v = int(v)
    if isinstance(v, (int, float)): return ("n", round(float(v), 9))
    return ("s" if isinstance(v, str) else "z", v)

def norm(rows, ordered):
    out = [tuple(norm_val(v) for v in r) for r in rows]
    return out if ordered else sorted(out, key=repr)

@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_case(case):
    db = Database()
    for s in case["setup"]:
        db.execute(s)
    got = db.execute(case["query"])
    assert norm(got, case["ordered"]) == norm(case["expected"], case["ordered"])
