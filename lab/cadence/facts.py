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
    out, prev = [], {}
    for a in actions:
        p, c = a["period"], a["clock"]
        base = prev.get(p, start)
        if base is not None and c >= base:
            out.append((p, short(a["tool"]), c - base))
        prev[p] = c
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
    m = re.search(r"^#+\s*Capacity split\s*$(.*?)(?=^#+\s|\Z)", aims_text or "", re.M | re.S | re.I)
    if not m:
        return []
    out = []
    for line in m.group(1).splitlines():
        mm = re.match(r"\s*[-*]\s*(\d+(?:\.\d+)?)\s*%\s*([^:]+):\s*(.*)$", line)
        if mm:
            tools = [short(x.strip().strip("`")) for x in re.split(r"[,;]", mm.group(3)) if x.strip()]
            out.append({"label": mm.group(2).strip(), "planned": float(mm.group(1)) / 100, "tools": [t for t in tools if t]})
    return out

def pursuit(split, cs, period, window):
    """Planned vs actual share of capacity per label over the last window. Actual shares are of all cost spent."""
    recent = [(t, c) for p, t, c in cs if p > period - window]
    total = sum(c for _, c in recent)
    if not split or not total:
        return []
    rows, named = [], set()
    for s in split:
        named |= set(s["tools"])
        act = sum(c for t, c in recent if t in s["tools"]) / total
        rows.append({"label": s["label"], "planned": s["planned"], "actual": act, "gap": act - s["planned"]})
    other = sum(c for t, c in recent if t not in named) / total
    rows.append({"label": "other (not in the split)", "planned": max(0.0, 1 - sum(s["planned"] for s in split)), "actual": other,
                 "gap": other - max(0.0, 1 - sum(s["planned"] for s in split))})
    return rows

def off_plan(rows, threshold=0.25, min_planned=0.2):
    """Labels whose actual share missed the plan by more than the threshold (a fault: the plan was not followed)."""
    return [r["label"] for r in rows if r["planned"] >= min_planned and abs(r["gap"]) > threshold]

def parse_proposed(text):
    m = re.search(r"^#+\s*Facts\s*$(.*?)(?=^#+\s|\Z)", text or "", re.M | re.S | re.I)
    out = []
    for line in (m.group(1).splitlines() if m else []):
        line = line.strip().lstrip("-*").strip()
        if line:
            parts = [p.strip() for p in line.split("|")]
            src = next((p.split(":", 1)[1].strip() for p in parts if p.lower().startswith("source:")), "")
            out.append({"fact": parts[0][:200], "source": src[:200]})
    return out

def markdown(reg, prow, proposed, cap_unit, as_of=None):
    md = (f"\n## Facts measured by the system (from the harness's log of every action; cost in {cap_unit}"
          + (f"; as of {as_of}, so the step log may already hold later calls" if as_of else "") + ")\n\n"
          "Read these instead of asking: they are measured, not assumed. The last column is each action's share of the time that "
          "was spent, not of the time available; how much of the working day is in use is under Resources.\n\n")
    if reg:
        md += "| action | calls | median cost | share of the time spent, last point |\n| --- | --- | --- | --- |\n"
        for r in reg[:15]:
            md += f"| {r['tool']} | {r['calls']} | {round(r['median'], 2)} | {r['recent_share']:.0%} |\n"
    else:
        md += "No actions logged yet.\n"
    if prow:
        md += ("\n## Pursuit: planned vs actual capacity split (last point; plan from swarm/aims.md)\n\n"
               "| label | planned | actual | gap |\n| --- | --- | --- | --- |\n")
        for r in prow:
            md += f"| {r['label']} | {r['planned']:.0%} | {r['actual']:.0%} | {r['gap']:+.0%} |\n"
    if proposed:
        md += "\n## Facts proposed by roles (not measured by the system; each with its cited source)\n\n"
        for f in proposed[-10:]:
            md += f"- {f['fact']} (source: {f['source'] or 'none cited'}; from {f['from']})\n"
    return md
