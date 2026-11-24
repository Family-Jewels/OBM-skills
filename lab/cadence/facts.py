"""Fact register and pursuit measure (engine v4), from the harness's own log of the worker's actions.

The action log is a JSONL file written by a generic hook after every task tool call: {"tool", "period", "clock"}, where
'clock' is the task's clock after the call, in the capacity's units (simulated minutes, dollars spent, seconds). The cost of
an action is the clock's advance since the previous action in the same period (the first one: since spec['action_clock']
['start'], or it is skipped). Nothing here knows the task.

The aims file states the planned capacity split in a fixed section the engine reads:
    ## Capacity split
    - 75% fills: restock_machine
    - 10% sourcing and orders: check_offers, place_order
Each line: a share, a label, then the action (tool) names it covers. Tools not named count as 'other'.
"""
import json, re, statistics
from pathlib import Path
from mdtext import section

def load_actions(path):
    p = Path(path) if path else None
    if not p or not p.exists():
        return []
    out = []
    for line in p.read_text().splitlines():
        try:
            r = json.loads(line)
            if r.get("tool") and r.get("period") is not None and isinstance(r.get("clock"), (int, float)):
                out.append(r)
        except Exception:
            pass
    return out

def short(tool):
    return tool.split("__")[-1]

def costs(actions, start=None):
    """[(period, tool, cost)] from the clock's advance between actions in the same period."""
    out, prev, last = [], {}, None
    for a in actions:
        p, c = a["period"], a["clock"]
        # within a period: since the previous action; a period's first action: since the period's start when the clock
        # resets each period (start given), else since the last action before it (a cumulative clock: budget, seconds)
        base = prev.get(p, start if start is not None else last)
        if base is not None and c >= base:
            out.append((p, short(a["tool"]), c - base))
        prev[p] = c; last = c
    return out

def register(cs, period, window):
    """Per tool: calls, median cost, and share of all cost over the last window of periods."""
    by = {}
    for p, t, c in cs:
        by.setdefault(t, []).append((p, c))
    recent_total = sum(c for p, _, c in cs if p > period - window) or 0
    rows = []
    for t, xs in by.items():
        cc = [c for _, c in xs]
        rc = sum(c for p, c in xs if p > period - window)
        rows.append({"tool": t, "calls": len(xs), "median": statistics.median(cc), "recent_share": rc / recent_total if recent_total else 0})
    rows.sort(key=lambda r: -r["recent_share"])
    return rows

def parse_split(aims_text):
    body = section(aims_text, "Capacity split")
    if not body:
        return []
    out = []
    for line in body.splitlines():
        mm = re.match(r"\s*[-*]\s*(\d+(?:\.\d+)?)\s*%\s*([^:]+):\s*(.*)$", line)
        if mm:
            tools = [short(x.strip().strip("`")) for x in re.split(r"[,;]", mm.group(3)) if x.strip()]
            out.append({"label": mm.group(2).strip(), "planned": float(mm.group(1)) / 100, "tools": [t for t in tools if t]})
    return out

def pursuit(split, cs, period, window, available=None):
    """Planned vs actual share of capacity per label over the last window.

    With `available` (the capacity per period, from the adapter's reading), shares are of the capacity of the periods
    worked, the same basis as the plan, and the capacity left unused is measured too: a split line that names no actions
    (slack, reserve) is compared with it. Without it, shares are of all cost spent."""
    recent = [(p, t, c) for p, t, c in cs if p > period - window]
    spent = sum(c for _, _, c in recent)
    if not split or not spent:
        return []
    days = len({p for p, _, _ in recent})
    total = max(spent, (available or 0) * days)
    unused = 1 - spent / total
    idle_lines = [x for x in split if not [t for t in x["tools"] if t.lower() not in ("none", "-", "—")]]
    idle_plan = sum(x["planned"] for x in idle_lines)
    rows, named = [], set()
    for x in split:
        if x in idle_lines:
            act = unused * (x["planned"] / idle_plan if idle_plan else 1 / len(idle_lines))
        else:
            named |= set(x["tools"])
            act = sum(c for _, t, c in recent if t in x["tools"]) / total
        rows.append({"label": x["label"], "planned": x["planned"], "actual": act, "gap": act - x["planned"]})
    rest = max(0.0, 1 - sum(x["planned"] for x in split))
    other = sum(c for _, t, c in recent if t not in named) / total
    rows.append({"label": "other (not in the split)", "planned": rest, "actual": other, "gap": other - rest})
    if total > spent and not idle_lines:
        rows.append({"label": "unused capacity", "planned": 0.0, "actual": unused, "gap": unused})
    return rows

def off_plan(rows, threshold=0.25, min_planned=0.2):
    """Labels whose actual share missed the plan by more than the threshold (a fault: the plan was not followed)."""
    return [r["label"] for r in rows if r["planned"] >= min_planned and abs(r["gap"]) > threshold]

def parse_proposed(text):
    out = []
    for line in section(text, "Facts", suffix=False).splitlines():
        line = line.strip().lstrip("-*").strip()
        if line:
            parts = [p.strip() for p in line.split("|")]
            src = next((p.split(":", 1)[1].strip() for p in parts if p.lower().startswith("source:")), "")
            out.append({"fact": parts[0][:200], "source": src[:200]})
    return out

def markdown(reg, prow, proposed, cap_unit, split=None):
    md = (f"\n## Facts measured by the system (from the harness's log of every action; cost in {cap_unit})\n\n"
          "Read these instead of asking: they are measured, not assumed.\n\n")
    if reg:
        md += "| action | calls | median cost | share of capacity, last point |\n| --- | --- | --- | --- |\n"
        for r in reg[:15]:
            md += f"| {r['tool']} | {r['calls']} | {round(r['median'], 2)} | {r['recent_share']:.0%} |\n"
    else:
        md += "No actions logged yet.\n"
    seen = {r["tool"] for r in reg}
    never = list(dict.fromkeys(t for x in (split or []) for t in x["tools"] if t not in seen))
    if never:  # named in the plan but never called: measured as zero, not missing
        md += "\nNamed in the capacity split but never called (0 calls, measured): " + ", ".join(never) + ".\n"
    if prow:
        md += ("\n## Pursuit: planned vs actual capacity split (last point; plan from swarm/aims.md; shares of the capacity of "
               "the periods worked when the task reports it, else of what was spent)\n\n"
               "| label | planned | actual | gap |\n| --- | --- | --- | --- |\n")
        for r in prow:
            md += f"| {r['label']} | {r['planned']:.0%} | {r['actual']:.0%} | {r['gap']:+.0%} |\n"
    if proposed:
        md += "\n## Facts proposed by roles (not measured by the system; each with its cited source)\n\n"
        for f in proposed[-10:]:
            md += f"- {f['fact']} (source: {f['source'] or 'none cited'}; from {f['from']})\n"
    return md
