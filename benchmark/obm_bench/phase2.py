"""Phase 2: the swarm improves itself without a human.

1. Collect the OBM runs from phase 1.
2. The auditor skill re-verifies a random sample of finished work. It sees only what the
   system itself could see (spec, tests, task record, final artifact, checker verdict),
   never the benchmark's labels, so nothing about which tasks are impossible leaks in.
3. The diagnostician skill reads the audit and the system-visible scorecard and writes one
   versioned rule for one role.
4. Held-out tasks run with the old briefs (obm_v1) and the new briefs (obm_v2).
"""

import json
import random
import re
from collections import Counter
from pathlib import Path

from inspect_ai.log import list_eval_logs, read_eval_log
from inspect_ai.model import ChatMessageSystem, ChatMessageUser, get_model

from . import prompts as P


def load_obm_samples(log_dir: str, condition: str = "obm") -> tuple[list[dict], int]:
    """Return system-visible records of phase 1 OBM samples, and the first unused task offset."""
    items, next_offset = [], 0
    for info in list_eval_logs(log_dir):
        log = read_eval_log(info)
        args = log.eval.task_args or {}
        if args.get("condition") not in ("obm", "obm_fixed"):
            continue
        effective = (args.get("label") or args.get("condition")) + ("_plain" if args.get("prompt") == "plain" else "")
        if effective != condition:
            continue
        off, lim = int(args.get("offset") or 0), args.get("limit")
        if lim is not None:
            next_offset = max(next_offset, off + int(lim))
        for s in log.samples or []:
            md = s.metadata or {}
            ob = md.get("obm_bench") or {}
            if not ob:
                continue
            events = ob.get("events", [])
            verdicts = [e for e in events if e.get("type") == "checker"]
            last_reply = next((m.text for m in reversed(s.messages) if m.role == "assistant"), "")
            reason = ob.get("flag_reason")
            final_code = ob.get("final_code")
            hist = (md.get("agentic_results") or {}).get("attempt_history", [])
            if reason == "conflict":
                status, artifact = "block confirmed by checker; nothing shipped", last_reply
            elif reason == "cap":
                status, artifact = "retry cap reached; escalated, nothing shipped", final_code or last_reply
            elif verdicts and verdicts[-1]["verdict"] == "pass":
                status, artifact = "tests passed and checker passed; code shipped", final_code
            else:
                status, artifact = "tests never passed; last code shipped as failed", final_code
            items.append({
                # Fields the system itself could see. No split label, no official score.
                "spec": md.get("prompt", ""),
                "tests": md.get("test", ""),
                "record": md.get("obm_record", ""),
                "artifact": artifact or "",
                "status": status,
                "flag_reason": reason,
                "last_checker": verdicts[-1]["text"] if verdicts else "(no checker review)",
                "verdicts": [v["verdict"] for v in verdicts],
                "designer_parsed": next((e.get("parsed") for e in events if e.get("type") == "designer"), None),
                "producer_turns": len(hist),
                "tokens": sum((u.total_tokens or 0) for u in (s.model_usage or {}).values()),
            })
    return items, next_offset


def scorecard(items: list[dict]) -> str:
    """System-visible scorecard: only what the swarm itself records."""
    n = len(items)
    status = Counter(i["status"] for i in items)
    verdicts = Counter(v for i in items for v in i["verdicts"])
    designer_fail = sum(1 for i in items if i["designer_parsed"] is False)
    turns = sum(i["producer_turns"] for i in items) / max(1, n)
    tokens = sum(i["tokens"] for i in items) / max(1, n)
    lines = [f"Tasks run: {n}", "Final status:"]
    lines += [f"  {k}: {v}" for k, v in status.most_common()]
    lines.append("Checker verdicts issued (all rounds):")
    lines += [f"  {k}: {v}" for k, v in verdicts.most_common()]
    lines += [f"Designer records that failed to parse: {designer_fail}",
              f"Mean producer turns per task: {turns:.1f}",
              f"Mean tokens per task: {tokens:,.0f}"]
    return "\n".join(lines)


def audit_sample(items: list[dict], size: int, seed: int) -> list[dict]:
    """Auditor sampling: random, weighted toward finished outcomes worth re-verifying
    (shipped passes and confirmed blocks), topped up with the rest."""
    rng = random.Random(seed)
    key = [i for i in items if i["status"].startswith(("tests passed", "block confirmed"))]
    rest = [i for i in items if i not in key]
    rng.shuffle(key)
    rng.shuffle(rest)
    return (key + rest)[:size]


def audit_packet(sample: list[dict], card: str) -> str:
    parts = ["# Audit request", "", "## System scorecard for this batch", card, "",
             f"## Items ({len(sample)}, randomly sampled)"]
    for n, it in enumerate(sample, 1):
        parts += [
            f"\n### ITEM {n}",
            f"Final status: {it['status']}",
            it["record"],
            "Specification:\n```\n" + it["spec"] + "\n```",
            "Tests:\n```\n" + it["tests"] + "\n```",
            "Final artifact:\n```\n" + (it["artifact"] or "(none)")[-4000:] + "\n```",
            "Last checker review:\n" + it["last_checker"][-1500:],
        ]
    return "\n".join(parts)


async def run_audit(model: str | None, sample: list[dict], card: str) -> tuple[str, dict]:
    m = get_model(model) if model else get_model()
    out = await m.generate([ChatMessageSystem(content=P.auditor_system()),
                            ChatMessageUser(content=audit_packet(sample, card))])
    findings = Counter(c.lower() for c in re.findall(
        r"ITEM\s+\d+:\s*(?:AGREE|DISAGREE)\s*-\s*([a-z_]+)", out.completion, flags=re.I))
    return out.completion, {"findings": dict(findings), "usage": _usage(out)}


async def run_diagnosis(model: str | None, audit_report: str, card: str, current_rules: dict) -> tuple[str, dict]:
    m = get_model(model) if model else get_model()
    rules_text = json.dumps(current_rules, indent=2) if current_rules else "(no local rules yet)"
    packet = (f"# Diagnosis request\n\n## Audit report\n{audit_report}\n\n"
              f"## System scorecard\n{card}\n\n## Current local rules\n{rules_text}\n")
    out = await m.generate([ChatMessageSystem(content=P.diagnostician_system()),
                            ChatMessageUser(content=packet)])
    return out.completion, {"usage": _usage(out)}


def parse_rule_change(text: str) -> dict:
    m = re.search(r"RULE CHANGE:\s*```[a-z]*\n(.*?)```", text, flags=re.S | re.I)
    block = m.group(1) if m else ""
    fields = {}
    for key in ["target", "rule", "expected_effect", "measure", "revert_if"]:
        f = re.search(rf"^{key}:\s*(.*?)(?=^\w+:|\Z)", block, flags=re.S | re.M)
        fields[key] = f.group(1).strip() if f else ""
    target = fields["target"].split()[0].lower() if fields["target"] else "none"
    fields["target"] = target if target in ("designer", "producer", "checker") else "none"
    fields["parsed"] = bool(m)
    return fields


def _usage(out) -> dict:
    u = out.usage
    return {"input_tokens": getattr(u, "input_tokens", 0), "output_tokens": getattr(u, "output_tokens", 0),
            "total_tokens": getattr(u, "total_tokens", 0)} if u else {}


def write_rules(path: Path, current: dict, change: dict) -> dict:
    rules = dict(current)
    if change["target"] != "none" and change["rule"] and change["rule"].lower() != "none":
        prev = rules.get(change["target"], "")
        rules[change["target"]] = (prev + "\n\n" if prev else "") + f"RC-{len(rules) + 1:03d}: {change['rule']}"
    path.write_text(json.dumps(rules, indent=2))
    return rules
