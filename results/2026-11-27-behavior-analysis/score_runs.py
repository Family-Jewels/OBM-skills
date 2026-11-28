"""Score every recorded run against the self-improvement chain's target behaviors, from ground truth where it exists.

Reads only what is in results/: result.json, cadence.jsonl, the system's metrics_system.md, the review records
in audits/ and the worker's progress logs. Nothing here trusts an agent's report as a measure: predictions are
checked against the system's daily metrics, and "acted on" means the delivered record's id appears in the
worker's log on or after the day it was delivered.

usage: python3 -I score_runs.py <results-dir> <out.json>
"""
import collections, glob, json, os, re, statistics as st, sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else None

# ---------- loaders ----------

def load_metrics(run):
    files = sorted(run.rglob("metrics_system.md"))
    if not files:
        return {}
    rows, cols = {}, None
    for line in files[0].read_text(errors="ignore").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0] == "day":
            cols = cells
            continue
        if not cols or set(cells[0]) <= set("- "):
            continue
        try:
            d = int(cells[0])
        except ValueError:
            continue
        rec = {}
        for k, v in zip(cols[1:], cells[1:]):
            try:
                rec[k] = float(v)
            except ValueError:
                rec[k] = None
        rows[d] = rec
    return rows

def load_cadence(run):
    p = run / "cadence.jsonl"
    if not p.exists():
        return []
    out = []
    for l in p.read_text(errors="ignore").splitlines():
        try:
            out.append(json.loads(l))
        except ValueError:
            pass
    return out

DAY_RE = re.compile(r"^\s*[-*#]*\s*\**\s*Day\s+(\d+)", re.I)

def load_progress(run):
    """Every worker progress log under the run (some runs wrote to the wrong folder), as (day, text) entries."""
    entries, files = [], []
    for f in sorted(run.rglob("progress.md")):
        if "history" in f.parts:
            continue
        files.append(f)
        cur_day, buf = None, []
        for line in f.read_text(errors="ignore").splitlines():
            m = DAY_RE.match(line)
            if m:
                if cur_day is not None:
                    entries.append((cur_day, "\n".join(buf)))
                cur_day, buf = int(m.group(1)), [line]
            elif cur_day is not None:
                buf.append(line)
        if cur_day is not None:
            entries.append((cur_day, "\n".join(buf)))
    return entries, files

def audits(run):
    return sorted(p for p in run.rglob("*.md") if "audits" in p.parts and "history" not in p.parts)

# ---------- predictions ----------

MEASURES = [
    ("units_per_slot", r"units per (?:selling |stocked )?slot"),
    ("revenue_per_slot", r"revenue[_ ]per[_ ]slot"),
    ("slots_selling", r"slots[_ ]selling|selling slots|stocked selling slots"),
    ("cash_gain_7", r"cash[_ ]gain[_ ]7|cash gained over 7"),
    ("revenue_last_7", r"revenue[_ ]last[_ ]7"),
    ("units", r"\bunits\b"),
    ("revenue", r"\brevenue\b"),
]
BY_DAY = re.compile(r"(?:by|through|to|until)\s+(?:day\s*|d)(\d{1,3})\b|days?\s*(\d{1,3})\s*(?:–|-|to)\s*(?:day\s*|d)?(\d{1,3})", re.I)
UP = re.compile(r"\b(rise|rises|up|above|at least|or more|reach|reaches|returns|higher|increase)", re.I)
DOWN = re.compile(r"\b(fall|falls|down|below|fewer|or less|lower|decrease)", re.I)

HEADER = re.compile(r"(?im)^\s*(?:#+\s*(?:\d+\.\s*)?|\*\*)?prediction\b")

def prediction_block(text):
    m = HEADER.search(text)
    if not m:
        return None
    block = text[m.start():m.start() + 1500]
    stop = re.search(r"\n\s*(?:\*\*|##\s*(?:\d+\.\s*)?)?(cost|revert|not changed|open|charts|why)\b", block[12:], re.I)
    return block[:12 + stop.start()] if stop else block

def primary_claim(block):
    """The first claim in the prediction block: its measure (None when it names nothing the system charts),
    direction and the day it is due. Secondary claims and revert conditions are ignored."""
    body = re.sub(r"^\s*(?:#+\s*(?:\d+\.\s*)?|\*\*)?prediction[^\n:.]*[:.]?\**", "", block, count=1, flags=re.I)
    units = [u.strip() for u in re.split(r"\n\s*[-*]\s+|\n\s*\d+\.\s+|\n\s*\n", body) if u.strip()]
    for u in units:
        if not (UP.search(u) or DOWN.search(u) or re.search(r"\d", u)):
            continue
        meas, pos = None, None
        for name, pat in MEASURES:
            mm = re.search(pat, u, re.I)
            if mm and (pos is None or mm.start() < pos):
                meas, pos = name, mm.start()
        first_sentence = re.split(r"(?<=[.;])\s", u)[0]
        if meas and pos is not None and pos > len(first_sentence) + 5:
            meas = None  # the measure only appears as a secondary clause
        tail = u[pos:] if pos is not None else u
        mu, md = UP.search(tail), DOWN.search(tail)
        direction = "up" if mu and (not md or mu.start() < md.start()) else "down" if md else None
        dm = BY_DAY.search(u)
        by_day = int(dm.group(1) or dm.group(3)) if dm else None
        return {"measure": meas, "dir": direction, "by_day": by_day, "text": u[:240]}
    return None

def daily(metrics, measure, d):
    m = metrics.get(d)
    if not m:
        return None
    if measure == "units_per_slot":
        s = m.get("slots_selling") or 0
        return (m.get("units") or 0) / s if s else None
    if measure == "cash_gain_7":
        p = metrics.get(d - 7)
        return m["cash"] - p["cash"] if p and m.get("cash") is not None and p.get("cash") is not None else None
    return m.get(measure)

def signal_test(metrics, measure, start, by_day, direction):
    """The protocol's own rule: against limits computed from the 28 days before the change (centre ± 2.66 × mean
    moving range), does the measure show a point beyond the limit, or 8 in a row on one side of the centre, in the
    predicted direction, between the change and the day it was due (at least 10 and at most 28 days)?"""
    pre = [v for v in (daily(metrics, measure, d) for d in range(start - 28, start)) if v is not None]
    if len(pre) < 8:
        return None
    c = st.mean(pre); mr = st.mean(abs(a - b) for a, b in zip(pre[1:], pre))
    hi, lo = c + 2.66 * mr, c - 2.66 * mr
    end = min(max(by_day or start + 20, start + 10), start + 28)
    post = [v for v in (daily(metrics, measure, d) for d in range(start + 1, end + 1)) if v is not None]
    if len(post) < 8:
        return None
    def run8(pred):
        n = 0
        for x in post:
            n = n + 1 if pred(x) else 0
            if n >= 8:
                return True
        return False
    up_sig = any(x > hi for x in post) or run8(lambda x: x > c)
    dn_sig = any(x < lo for x in post) or run8(lambda x: x < c)
    return {"hit": up_sig if direction == "up" else dn_sig, "wrong_way": dn_sig if direction == "up" else up_sig,
            "pre_centre": round(c, 2), "post_mean": round(st.mean(post), 2), "window": [start + 1, end]}

def base_rate(metrics, measure, direction, avoid, horizon):
    """How often the same test fires on days when nothing was changed: the rate a hit happens by chance or trend."""
    hits = n = 0
    for d in range(36, (horizon or 365) - 28, 3):
        if any(abs(d - a) <= 5 for a in avoid):
            continue
        r = signal_test(metrics, measure, d, d + 20, direction)
        if r is None:
            continue
        n += 1; hits += r["hit"]
    return hits / n if n else None

# ---------- per-run scoring ----------

def id_pattern(i):
    return re.compile(r"(?<![A-Z]-)(?<![A-Z])" + re.escape(i) + r"\b")

def score_run(run):
    rj = run / "result.json"
    r = json.loads(rj.read_text())
    rec = {"run": str(run.relative_to(ROOT)), "arm": r.get("arm"), "seed": r.get("seed"), "horizon": r.get("days"),
           "days": r.get("days_operated"), "completed": r.get("completed"), "final_balance": r.get("final_balance"),
           "cost": r.get("api_cost_usd"), "review_cost": r.get("cadence_cost_usd"), "tool_calls": r.get("tool_calls"),
           "turns": r.get("turns"), "stocked_slots": r.get("avg_stocked_slots"), "stopped": r.get("termination_reason"),
           "error": r.get("error")}
    ev = load_cadence(run)
    metrics = load_metrics(run)
    rec["has_metrics"] = bool(metrics)
    if metrics:
        rec["mean_slots_selling"] = round(st.mean(m.get("slots_selling") or 0 for m in metrics.values()), 2)
    if not ev:
        return rec
    kinds = collections.Counter(e["event"] for e in ev)
    rec["events"] = dict(kinds)
    # latency of each review from start to hand-over, in simulated days
    started = {e["id"]: e["period"] for e in ev if e["event"] == "started" and e.get("id")}
    lat = collections.defaultdict(list); delivered = {}
    for e in ev:
        if e.get("delivered") is not None and e.get("id"):
            delivered[e["id"]] = (e["event"], e["delivered"])
            lat[e["event"]].append(e["delivered"] - e.get("period", e["delivered"]))
    rec["latency_days"] = {k: {"n": len(v), "median": st.median(v), "max": max(v)} for k, v in lat.items()}
    asked = kinds.get("diagnosis_deferred", 0) + kinds.get("diagnosis_queued", 0) + kinds.get("diagnosis", 0)
    rec["diagnosis"] = {"run": kinds.get("diagnosis", 0), "deferred_or_queued": kinds.get("diagnosis_deferred", 0) + kinds.get("diagnosis_queued", 0),
                        "share_served": round(kinds.get("diagnosis", 0) / asked, 2) if asked else None}
    # review records
    recs = audits(run)
    text = {p.stem: p.read_text(errors="ignore") for p in recs}
    def count(pat):
        return sum(1 for t in text.values() if re.search(pat, t, re.I | re.M))
    rec["records"] = {"total": len(recs), "fault_yes": count(r"^Fault:\s*yes"), "fault_no": count(r"^Fault:\s*no"),
                      "diagnosis_needed_yes": count(r"^\**Diagnosis needed:?\**\s*yes"),
                      "misreport_yes": count(r"^Misreport:\s*yes"), "misreport_no": count(r"^Misreport:\s*no")}
    # requests (v3 onward): repeats of the same key
    keys = collections.Counter()
    for stem, t in text.items():
        for m in re.finditer(r"^-\s*to:\s*(\w+)\s*\|\s*key:\s*([\w-]+)", t, re.M | re.I):
            keys[(m.group(1).lower(), m.group(2).lower())] += 1
    if keys:
        rec["requests"] = {"asks": sum(keys.values()), "distinct": len(keys),
                           "max_repeats": max(keys.values()), "top": [f"{a}:{k} x{n}" for (a, k), n in keys.most_common(3)]}
    # predictions in redesign / method records, judged by the protocol's signal rule against the system's metrics
    preds = []
    starts = sorted(d for i, (k, d) in delivered.items() if k == "redesign")
    for stem, t in sorted(text.items()):
        if not re.match(r"^(R|M)-", stem):
            continue
        blk = prediction_block(t)
        start = delivered.get(stem, (None, None))[1]
        if start is None:
            m = re.search(r"day (\d+)", t[:200], re.I)
            start = int(m.group(1)) if m else None
        p = {"id": stem, "start": start, "has_prediction": bool(blk)}
        c = primary_claim(blk) if blk else None
        if c:
            p.update(c)
            p["charted"] = c["measure"] is not None
            if c["measure"] and c["dir"] and start is not None and metrics:
                j = signal_test(metrics, c["measure"], start, c["by_day"], c["dir"])
                if j:
                    p.update(j)
                    p["chance"] = base_rate(metrics, c["measure"], c["dir"], starts, r.get("days"))
        preds.append(p)
    if preds:
        judged = [p for p in preds if "hit" in p]
        rec["predictions"] = {"records": len(preds),
                              "with_prediction": sum(p["has_prediction"] for p in preds),
                              "primary_charted": sum(1 for p in preds if p.get("charted")),
                              "primary_uncharted": sum(1 for p in preds if p.get("charted") is False),
                              "judged": len(judged),
                              "hits": sum(p["hit"] for p in judged),
                              "wrong_way": sum(p["wrong_way"] for p in judged),
                              "expected_by_chance": round(sum(p["chance"] or 0 for p in judged), 2),
                              "detail": preds}
    # the worker acting on what it was handed
    entries, files = load_progress(run)
    rec["progress_logs"] = [str(f.relative_to(run)) for f in files]
    if files:
        nbytes = sum(f.stat().st_size for f in files)
        rec["progress_bytes"] = nbytes
        rec["progress_bytes_per_day"] = round(nbytes / max(1, r.get("days_operated") or 1))
        by_q = collections.defaultdict(list)
        for d, t in entries:
            by_q[min(3, (d - 1) * 4 // max(1, r.get("days") or 365))].append(len(t))
        rec["entry_chars_by_quarter"] = [round(st.mean(by_q[q])) if by_q[q] else None for q in range(4)]
        logged = sorted({d for d, _ in entries})
        last_logged = logged[-1] if logged else 0
        rec["log_last_day"] = last_logged
        rec["log_max_gap_days"] = max([b - a for a, b in zip(logged, logged[1:])] or [0])
        acted, lags = 0, []
        handed = [(i, k, d) for i, (k, d) in delivered.items()
                  if k in ("pulse", "audit", "diagnosis", "redesign", "strategist", "aims", "opportunity", "verdict")]
        alive = [(i, k, d) for i, k, d in handed if d <= last_logged]  # only what arrived while the log was still kept
        for i, k, d in alive:
            pat = id_pattern(i)
            days = [ed for ed, t in entries if ed >= d - 1 and pat.search(t)]
            if days:
                acted += 1; lags.append(min(days) - d)
        rec["acted_on"] = {"handed": len(handed), "handed_while_logging": len(alive), "mentioned_in_log": acted,
                           "share": round(acted / len(alive), 2) if alive else None,
                           "median_lag_days": st.median(lags) if lags else None}
    # the worker's structured logs: on which day did each stop?
    for name in ("work.jsonl", "runs.jsonl"):
        fs = [f for f in run.rglob(name) if "history" not in f.parts]
        if fs:
            last = 0
            for l in fs[0].read_text(errors="ignore").splitlines():
                try:
                    last = max(last, int(json.loads(l).get("day") or 0))
                except (ValueError, TypeError):
                    pass
            rec[f"{name}_last_day"] = last
    return rec

def main():
    runs = sorted({p.parent for p in ROOT.rglob("result.json")})
    out = [score_run(r) for r in runs]
    if OUT:
        OUT.write_text(json.dumps(out, indent=1, default=str))
    for o in out:
        p = o.get("predictions") or {}
        a = o.get("acted_on") or {}
        print(f"{o['run'][:52]:52s} €{(o['final_balance'] or 0):>7,.0f} d{o['days']} ${(o['cost'] or 0):5.2f} "
              f"slots {o.get('stocked_slots')} | diag served {(o.get('diagnosis') or {}).get('share_served')} "
              f"| pred {p.get('with_prediction')}/{p.get('records')} charted {p.get('primary_charted')} judged {p.get('judged')} "
              f"hits {p.get('hits')} (chance {p.get('expected_by_chance')}) wrong {p.get('wrong_way')} "
              f"| log→d{o.get('log_last_day')} gap {o.get('log_max_gap_days')} acted {a.get('mentioned_in_log')}/{a.get('handed_while_logging')} "
              f"| B/day {o.get('progress_bytes_per_day')}")

if __name__ == "__main__":
    main()
