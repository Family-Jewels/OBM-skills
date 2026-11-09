#!/usr/bin/env python3
"""Phase 2: audit -> diagnose -> one rule change -> held-out test. No human in the loop.

Reads the OBM runs from a phase 1 log directory, has the auditor skill re-verify a random
sample, has the diagnostician skill write one rule for one role, then runs tasks phase 1
never saw with the old briefs (obm_v1) and the new briefs (obm_v2).

Example
  python run_phase2.py --phase1-log-dir logs/pilot --model anthropic/claude-sonnet-5-5 \
      --heldout-limit 10 --epochs 3 --out-dir phase2
  python analyze.py phase2/logs --out phase2/results
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path

from obm_bench import phase2 as P2
from obm_bench.tasks import SPLITS, obm_impossible_lcb


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--phase1-log-dir", required=True)
    ap.add_argument("--model", required=True, help="Model for every role, including auditor and diagnostician")
    ap.add_argument("--checker-model", default=None)
    ap.add_argument("--out-dir", default="phase2")
    ap.add_argument("--audit-size", type=int, default=12)
    ap.add_argument("--heldout-offset", type=int, default=None,
                    help="First held-out task (default: right after the tasks phase 1 used)")
    ap.add_argument("--heldout-limit", type=int, default=10, help="Held-out tasks per split")
    ap.add_argument("--splits", nargs="+", default=SPLITS, choices=SPLITS)
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--max-attempts", type=int, default=10)
    ap.add_argument("--with-baseline", action="store_true", help="Also run baseline on the held-out tasks")
    ap.add_argument("--sandbox", default="docker", choices=["docker", "local"])
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--max-connections", type=int, default=10)
    ap.add_argument("--skip-heldout", action="store_true", help="Only audit and diagnose")
    ap.add_argument("--prompt", default="plain", choices=["hint", "plain"],
                    help="Task-text variant: audits phase 1's OBM runs of this variant and tests held-out tasks with it")
    args = ap.parse_args()

    out = Path(args.out_dir)
    (out / "changes").mkdir(parents=True, exist_ok=True)

    # 1. Collect phase 1 OBM runs (system-visible fields only)
    suffix = "_plain" if args.prompt == "plain" else ""
    items, next_offset = P2.load_obm_samples(args.phase1_log_dir, condition="obm" + suffix)
    if not items:
        print("No OBM samples found in the phase 1 logs.")
        return 1
    card = P2.scorecard(items)
    print(f"Phase 1 OBM samples: {len(items)}\n{card}\n")

    # 2. Audit
    sample = P2.audit_sample(items, args.audit_size, args.seed)
    audit_text, audit_meta = asyncio.run(P2.run_audit(args.model, sample, card))
    (out / "changes" / "A-001.md").write_text(audit_text)
    print(f"Audit findings: {audit_meta['findings']}")

    # 3. Diagnose and write one versioned rule
    diag_text, diag_meta = asyncio.run(P2.run_diagnosis(args.model, audit_text, card, {}))
    change = P2.parse_rule_change(diag_text)
    rules_path = out / "rules_v2.json"
    rules = P2.write_rules(rules_path, {}, change)
    (out / "changes" / "RC-001.md").write_text(
        f"# RC-001\n\nTarget: {change['target']}\n\nRule: {change['rule']}\n\n"
        f"Expected effect: {change['expected_effect']}\nMeasure: {change['measure']}\n"
        f"Revert if: {change['revert_if']}\n\n## Diagnostician reasoning\n\n{diag_text}\n")
    (out / "phase2_meta.json").write_text(json.dumps({
        "phase1_samples": len(items), "audit_size": len(sample), "audit": audit_meta,
        "diagnosis": diag_meta, "change": change, "rules": rules}, indent=2))
    print(f"Rule change -> {change['target']}: {change['rule'] or '(none)'}")

    if change["target"] == "none":
        print("The diagnostician made no change, so there is no v2 to test. See changes/RC-001.md.")
        return 0
    if args.skip_heldout:
        return 0

    # 4. Held-out tasks: v1 (old briefs) vs v2 (new rule), same tasks
    offset = args.heldout_offset if args.heldout_offset is not None else next_offset
    print(f"Held-out tasks: offset {offset}, {args.heldout_limit} per split, {args.epochs} epochs")
    from inspect_ai import eval as inspect_eval

    common = dict(limit=args.heldout_limit, offset=offset, max_attempts=args.max_attempts,
                  sandbox=args.sandbox, checker_model=args.checker_model, prompt=args.prompt)
    tasks = []
    for s in args.splits:
        tasks.append(obm_impossible_lcb(condition="obm", split=s, label="obm_v1", **common))
        tasks.append(obm_impossible_lcb(condition="obm", split=s, label="obm_v2",
                                        rules_file=str(rules_path.resolve()), **common))
        if args.with_baseline:
            tasks.append(obm_impossible_lcb(condition="baseline", split=s, **common))
    logs = inspect_eval(tasks, model=args.model, epochs=args.epochs, log_dir=str(out / "logs"),
                        max_connections=args.max_connections, max_tasks=len(tasks), fail_on_error=False)
    bad = [l for l in logs if l.status != "success"]
    print(f"\nFinished {len(logs)} task runs; {len(bad)} not successful. Analyze with:\n"
          f"  python analyze.py {out / 'logs'} --out {out / 'results'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
