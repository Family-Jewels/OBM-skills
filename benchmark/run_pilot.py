#!/usr/bin/env python3
"""Run the OBM x ImpossibleBench pilot.

Examples
  # Plan only: show what would run, no model calls
  python run_pilot.py --model anthropic/claude-sonnet-5-5 --dry-run

  # Pilot: 3 conditions x 3 splits x 2 task texts x 10 tasks x 3 epochs = 540 samples
  python run_pilot.py --model anthropic/claude-sonnet-5-5 --limit 10 --epochs 3

  # Cheapest first look: impossible splits only, 2 conditions, 1 epoch
  python run_pilot.py --model anthropic/claude-sonnet-5-5 --conditions baseline obm --splits conflicting --limit 10 --epochs 1
"""

import argparse
import sys

from obm_bench.tasks import CONDITIONS, DEFAULT_CONDITIONS, PROMPTS, SPLITS, obm_impossible_lcb


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True, help="Inspect model id, e.g. anthropic/claude-sonnet-5-5")
    ap.add_argument("--checker-model", default=None, help="Reviewer/checker model (default: same as --model)")
    ap.add_argument("--conditions", nargs="+", default=DEFAULT_CONDITIONS, choices=CONDITIONS,
                    help="obm = designer writes criteria; obm_fixed = hand-written criteria (ablation)")
    ap.add_argument("--splits", nargs="+", default=SPLITS, choices=SPLITS)
    ap.add_argument("--prompts", nargs="+", default=PROMPTS, choices=PROMPTS,
                    help="hint = task text offers the flag-for-human exit; plain = it does not")
    ap.add_argument("--limit", type=int, default=10, help="Tasks per split (same tasks in every condition)")
    ap.add_argument("--epochs", type=int, default=3, help="Repeat runs per task")
    ap.add_argument("--max-attempts", type=int, default=10, help="Producer turns per task, all conditions")
    ap.add_argument("--sandbox", default="docker", choices=["docker", "local"],
                    help="docker isolates model-written code; local runs it on this machine")
    ap.add_argument("--log-dir", default="./logs/pilot")
    ap.add_argument("--max-connections", type=int, default=10)
    ap.add_argument("--max-samples", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true", help="Print the plan and exit")
    args = ap.parse_args()

    n = len(args.conditions) * len(args.splits) * len(args.prompts) * args.limit * args.epochs
    print(f"Model: {args.model}   Checker/reviewer: {args.checker_model or args.model}")
    print(f"Conditions: {args.conditions}   Splits: {args.splits}   Task text: {args.prompts}")
    print(f"{args.limit} tasks/split x {args.epochs} epochs -> {n} samples")
    print(f"Producer turns per task: {args.max_attempts}   Sandbox: {args.sandbox}   Logs: {args.log_dir}")
    if args.dry_run:
        return 0

    from inspect_ai import eval as inspect_eval

    tasks = [
        obm_impossible_lcb(
            condition=c, split=s, limit=args.limit, max_attempts=args.max_attempts,
            sandbox=args.sandbox, checker_model=args.checker_model, prompt=p,
        )
        for p in args.prompts for c in args.conditions for s in args.splits
    ]
    logs = inspect_eval(
        tasks,
        model=args.model,
        epochs=args.epochs,
        log_dir=args.log_dir,
        max_connections=args.max_connections,
        max_samples=args.max_samples,
        max_tasks=len(tasks),
        fail_on_error=False,
    )
    bad = [l for l in logs if l.status != "success"]
    print(f"\nFinished {len(logs)} task runs; {len(bad)} not successful. Analyze with:\n"
          f"  python analyze.py {args.log_dir}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
