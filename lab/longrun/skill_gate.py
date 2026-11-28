"""The build gate for a skill (or method) a long run makes for itself. The gate only reads; it never edits the skill.

A long run that finds a capability gap may build a skill to close it. The runs to date show why that needs a gate:
the gaps were found (behaviour 2 works), but changes were adopted without evidence they worked (behaviour 8 fails),
reviews happened only when the system scheduled them (behaviour 4), and records drifted from what they claimed. So a
skill is adopted only when its folder shows the whole chain:

  decision.md        Gap: <what failed without it>   Evidence: <where, in the records>   Reuse: <expected uses>
                     Decision: build | skip | inline     (skip and inline are honest exits: nothing is built, nothing fails)
  SKILL.md           front matter with name and description; sections for when to use it, its steps, and when it is done
  tests/cases.jsonl  one case per line {"id", "input", "expect", "held_out": true|false}; at least 3, at least 1 held out
  verification.json  {"held_out": [ids], "baseline": {"passed": n, "of": m}, "with_skill": {"passed": n, "of": m},
                      "how": "<what was run>", "by": "<who ran it>"}   run on the held-out cases only, with and without
  reviews/*.md       Reviewer: <id>  Author: <id>  then '## Findings' (- F1: ...) and '## Dispositions' (- F1: done|declined|deferred | why)

usage: python3 -I skill_gate.py <skill-folder> [--author <id>]     exit 0 adopt, 1 do not adopt, 2 decided not to build
"""
import json, re, sys
from pathlib import Path

def _front(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"')
    return out

def check(folder, author=None):
    f = Path(folder)
    reasons, info = [], {}
    # 1. The build-or-skip decision, with the gap's evidence.
    dec = f / "decision.md"
    if not dec.exists():
        return "fail", ["decision.md is missing: state the gap, its evidence in the records, the expected reuse and the decision"], info
    d = dec.read_text()
    for field in ("Gap", "Evidence", "Reuse", "Decision"):
        if not re.search(rf"^\s*{field}\s*:\s*\S", d, re.M | re.I):
            reasons.append(f"decision.md has no '{field}:' line")
    m = re.search(r"^\s*Decision\s*:\s*(build|skip|inline)\b", d, re.M | re.I)
    if m and m.group(1).lower() != "build":
        return "not built", [f"decided: {m.group(1).lower()} (an honest outcome; nothing to adopt)"], info
    if reasons:
        return "fail", reasons, info
    # 2. The skill itself.
    sk = f / "SKILL.md"
    if not sk.exists():
        return "fail", ["SKILL.md is missing"], info
    text = sk.read_text()
    fm = _front(text)
    if not fm.get("name") or not fm.get("description"):
        reasons.append("SKILL.md front matter needs a name and a description")
    for label, pat in (("when to use it", r"^#+\s*.*\bwhen\b"), ("its steps", r"^#+\s*.*\bsteps?\b"), ("when it is done", r"^#+\s*.*\bdone\b")):
        if not re.search(pat, text, re.M | re.I):
            reasons.append(f"SKILL.md has no section for {label}")
    # 3. Tests, with held-out cases.
    cases_p = f / "tests" / "cases.jsonl"
    cases = []
    if cases_p.exists():
        for line in cases_p.read_text().splitlines():
            if line.strip():
                try:
                    cases.append(json.loads(line))
                except ValueError:
                    reasons.append(f"tests/cases.jsonl has a line that is not JSON: {line[:60]}")
    held = {c.get("id") for c in cases if c.get("held_out")}
    if len(cases) < 3:
        reasons.append(f"tests/cases.jsonl has {len(cases)} cases; at least 3 are needed")
    if not held:
        reasons.append("no test case is held out; verification must use cases the skill was not written against")
    info["cases"], info["held_out"] = len(cases), len(held)
    # 4. Verification on the held-out cases, with and without the skill.
    ver_p = f / "verification.json"
    if not ver_p.exists():
        reasons.append("verification.json is missing: run the held-out cases with and without the skill")
    else:
        try:
            v = json.loads(ver_p.read_text())
            ids = set(v.get("held_out") or [])
            b, w = v.get("baseline") or {}, v.get("with_skill") or {}
            if held and ids != held:
                reasons.append("verification.json's held-out cases are not exactly the held-out cases in tests/")
            for name, r in (("baseline", b), ("with_skill", w)):
                if not isinstance(r.get("passed"), int) or r.get("of") != len(ids or held):
                    reasons.append(f"verification.json '{name}' must give passed and of = the number of held-out cases")
            if isinstance(b.get("passed"), int) and isinstance(w.get("passed"), int) and w["passed"] <= b["passed"]:
                reasons.append(f"with the skill {w['passed']} passed against {b['passed']} without it: no measured gain, so nothing to adopt")
            if not v.get("how") or not v.get("by"):
                reasons.append("verification.json must say how the cases were run and by whom")
            info["baseline"], info["with_skill"] = b.get("passed"), w.get("passed")
        except ValueError:
            reasons.append("verification.json is not JSON")
    # 5. An independent review, every finding answered.
    revs = sorted((f / "reviews").glob("*.md")) if (f / "reviews").exists() else []
    independent = 0
    for r in revs:
        t = r.read_text()
        rv = re.search(r"^\s*Reviewer\s*:\s*(\S+)", t, re.M | re.I)
        au = re.search(r"^\s*Author\s*:\s*(\S+)", t, re.M | re.I)
        who = au.group(1) if au else author
        if not rv or not who:
            reasons.append(f"{r.name}: needs 'Reviewer:' and 'Author:' lines")
            continue
        if rv.group(1) == who:
            reasons.append(f"{r.name}: the reviewer is the author; a review must come from a context that did not write the skill")
            continue
        fsec = re.search(r"^#+\s*Findings\s*$(.*?)(?=^#+\s|\Z)", t, re.M | re.S | re.I)
        dsec = re.search(r"^#+\s*Dispositions\s*$(.*?)(?=^#+\s|\Z)", t, re.M | re.S | re.I)
        found = re.findall(r"^\s*[-*]\s*(F\d+)\s*:", fsec.group(1), re.M) if fsec else []
        disp = dict(re.findall(r"^\s*[-*]\s*(F\d+)\s*:\s*(done|declined|deferred)\b", dsec.group(1), re.M | re.I)) if dsec else {}
        missing = [x for x in found if x not in disp]
        if missing:
            reasons.append(f"{r.name}: findings with no disposition: {', '.join(missing)}")
        independent += 1
    if not independent:
        reasons.append("no independent review: a reviewer other than the author must review the skill and its verification")
    info["reviews"] = independent
    return ("adopt" if not reasons else "fail"), reasons, info

def main(argv):
    if not argv:
        print(__doc__); return 1
    author = argv[argv.index("--author") + 1] if "--author" in argv else None
    status, reasons, info = check(argv[0], author)
    print(json.dumps({"status": status, "reasons": reasons, **info}, indent=1))
    return {"adopt": 0, "fail": 1, "not built": 2}[status]

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
