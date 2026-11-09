#!/usr/bin/env python3
"""Smoke test for phase 2 with the scripted fake model. No API key needed.

Runs a small phase 1 (OBM only), then run_phase2.py end to end, and checks:
  - the auditor and diagnostician ran and a rule was written to rules_v2.json
  - held-out tasks do not overlap the phase 1 tasks
  - obm_v2 producers receive the new rule and obm_v1 producers do not
Usage: python tests/smoke_phase2.py [work_dir]
"""

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import scripted_model  # noqa: F401,E402  (registers the "scripted" provider)
from inspect_ai import eval as inspect_eval  # noqa: E402
from inspect_ai.log import list_eval_logs, read_eval_log  # noqa: E402

import run_phase2  # noqa: E402
from obm_bench.tasks import obm_impossible_lcb  # noqa: E402


def task_ids(log_dir: str, label: str | None = None) -> dict:
    ids = {}
    for info in list_eval_logs(log_dir):
        log = read_eval_log(info)
        a = log.eval.task_args
        if label and (a.get("label") or a.get("condition")) != label:
            continue
        ids.setdefault(a["split"], set()).update(str(s.id) for s in log.samples)
    return ids


def main() -> int:
    work = Path(sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp(prefix="obm_p2_"))
    p1 = work / "phase1"
    splits = ["original", "conflicting"]
    tasks = [obm_impossible_lcb(condition="obm", split=s, limit=4, max_attempts=3, sandbox="local", prompt="plain")
             for s in splits]
    inspect_eval(tasks, model="scripted/test", log_dir=str(p1), display="none")

    out = work / "phase2"
    sys.argv = ["run_phase2.py", "--phase1-log-dir", str(p1), "--model", "scripted/test",
                "--out-dir", str(out), "--audit-size", "6", "--heldout-limit", "3", "--epochs", "1",
                "--max-attempts", "3", "--sandbox", "local", "--splits", *splits]
    rc = run_phase2.main()

    failures = []
    if rc != 0:
        failures.append(f"run_phase2 exited {rc}")
    rules = json.loads((out / "rules_v2.json").read_text())
    if "producer" not in rules or "blocked report" not in rules["producer"]:
        failures.append(f"rule not written as expected: {rules}")
    for f in ["changes/A-001.md", "changes/RC-001.md", "phase2_meta.json"]:
        if not (out / f).exists():
            failures.append(f"missing {f}")

    p1_ids, v1_ids = task_ids(str(p1)), task_ids(str(out / "logs"), "obm_v1")
    for s in splits:
        overlap = p1_ids.get(s, set()) & v1_ids.get(s, set())
        if overlap:
            failures.append(f"held-out tasks overlap phase 1 on {s}: {overlap}")
        if not v1_ids.get(s):
            failures.append(f"no held-out samples for {s}")

    for info in list_eval_logs(str(out / "logs")):
        log = read_eval_log(info)
        label = log.eval.task_args.get("label")
        for smp in log.samples:
            system = smp.messages[0].text if smp.messages and smp.messages[0].role == "system" else ""
            has_rule = "Local rules" in system and "RC-001" in system
            if label == "obm_v2" and not has_rule:
                failures.append(f"{log.eval.task} {smp.id}: v2 producer missing the new rule")
            if label == "obm_v1" and has_rule:
                failures.append(f"{log.eval.task} {smp.id}: v1 producer has the rule")

    print(f"Work dir: {work}")
    if failures:
        print("PHASE 2 SMOKE TEST FAILED")
        print("\n".join(failures))
        return 1
    print("PHASE 2 SMOKE TEST PASSED: audit, diagnosis, versioned rule and held-out v1/v2 runs all work.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
