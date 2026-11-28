"""Change verification by the system: did a method change do what it predicted?

What the runs showed (results/2026-11-27-behavior-analysis): predictions were prose, a third named measures nobody
charts, some were already due when the change was adopted, and the reviewers who judged them later had no chance rate.
Of 38 that could be judged, 15 showed the predicted shift against 11.9 expected by chance. So the verdict moves from
the reviewers to the system, under four rules:

1. A prediction is one machine-readable line in the change record:
       Prediction: <measure> <up|down> within <N> points
   where <measure> is one the system charts. Anything else is returned to the designer, never guessed at.
2. The window is counted from the period the change is adopted, not from when the record was written.
3. The verdict uses the protocol's signal rule against limits from before the change (centre +/- 2.66 x mean moving
   range): a point beyond the limit, or 8 in a row on the predicted side of the centre.
4. Every verdict carries the chance rate: how often the same test fires on the same measure where nothing changed.
   A hit that chance produces half the time is weak evidence; the verdict says so.

Nothing here knows the task. Series are lists of [period, value].
"""
import re, statistics as st

LINE = re.compile(r"^\s*\**\s*Prediction\s*\**\s*:\s*\**\s*`?([A-Za-z0-9_]+)`?\s+(up|down)\s+within\s+(\d+)\s+(points?|periods?|days?)\b",
                  re.I | re.M)

def parse(record, charted):
    """(prediction, problem). A problem means the designer must restate it; the system never guesses."""
    m = LINE.search(record or "")
    if not m:
        return None, ("no machine-readable prediction. End the record with one line exactly 'Prediction: <measure> <up|down> "
                      "within <N> points', using a measure the system charts: " + ", ".join(charted) + ".")
    meas, d, n, unit = m.group(1), m.group(2).lower(), int(m.group(3)), m.group(4).lower()
    if meas not in charted:
        return None, (f"the prediction names '{meas}', which the system does not chart, so ground truth cannot judge it. Restate it "
                      f"on one of: {', '.join(charted)}; or ask the human for the measure to be instrumented.")
    if n < 1:
        return None, "the prediction's window must be at least 1 point."
    return {"measure": meas, "dir": d, "n": n, "unit": "point" if unit.startswith("point") else "period"}, None

def limits(vals):
    c = st.mean(vals)
    mr = st.mean(abs(a - b) for a, b in zip(vals[1:], vals)) if len(vals) > 1 else 0.0
    return c, c - 2.66 * mr, c + 2.66 * mr, mr

def _run(vals, pred, k=8):
    n = 0
    for v in vals:
        n = n + 1 if pred(v) else 0
        if n >= k:
            return True
    return False

def test(series, start, end, direction, pre_periods=28, min_pre=8, min_post=5):
    """The signal rule on (start, end]; limits from [start - pre_periods, start). None when there is too little data."""
    pre = [v for p, v in series if start - pre_periods <= p < start and v is not None]
    post = [v for p, v in series if start < p <= end and v is not None]
    if len(pre) < min_pre or len(post) < min_post:
        return None
    c, lo, hi, mr = limits(pre)
    up = any(v > hi for v in post) or _run(post, lambda v: v > c)
    dn = any(v < lo for v in post) or _run(post, lambda v: v < c)
    return {"hit": up if direction == "up" else dn, "wrong_way": dn if direction == "up" else up, "centre": round(c, 3),
            "lower": round(lo, 3), "upper": round(hi, 3), "mr": round(mr, 3), "post_mean": round(st.mean(post), 3), "n_post": len(post)}

def chance(series, length, direction, avoid=(), pre_periods=28, step=3, guard=5):
    """How often the same test fires on this series where no change was adopted (ramp-up, season and drift land here)."""
    if not series:
        return None
    first, last = series[0][0], series[-1][0]
    hits = n = 0
    for s in range(first + pre_periods, last - length + 1, step):
        if any(abs(s - a) <= guard for a in avoid):
            continue
        r = test(series, s, s + length, direction, pre_periods)
        if r is None:
            continue
        n += 1; hits += r["hit"]
    return round(hits / n, 3) if n else None

def judge(pred, series, period, per_point, avoid=()):
    """Judge one registered prediction once its window has passed. Returns the verdict dict or None if not due yet."""
    length = pred["n"] * (per_point if pred["unit"] == "point" else 1)
    length = max(length, 10)  # at least long enough for a run of 8 to show
    end = pred["adopted"] + length
    if period < end:
        return None
    r = test(series, pred["adopted"], end, pred["dir"], min_post=max(5, int(0.7 * length + 0.999)))  # most of the window observed
    if r is None:
        return {"verdict": "not enough data", "window": [pred["adopted"] + 1, end]}
    p = chance(series, length, pred["dir"], avoid=[a for a in avoid if a != pred["adopted"]])
    v = "shift as predicted" if r["hit"] else ("shift the wrong way" if r["wrong_way"] else "no shift")
    if r["hit"] and p is not None and p >= 0.5:
        v += " (weak: chance produces this at least half the time)"
    return {"verdict": v, "window": [pred["adopted"] + 1, end], "chance": p, **r}

def detectable(series, start, pre_periods=28):
    """Routine variation before a change: a single point must clear 2.66 mean moving ranges; 8 in a row catches less."""
    pre = [v for p, v in series if start - pre_periods <= p < start and v is not None]
    if len(pre) < 8:
        return None
    c, lo, hi, mr = limits(pre)
    return {"centre": round(c, 3), "beyond_limit_needs": round(hi - c, 3), "mr": round(mr, 3)}

def register(mem, change_id, record, charted, adopted, series_of):
    """Called when a method change is adopted. Returns a problem string for the designer, or None if registered."""
    pred, problem = parse(record, charted)
    if problem:
        mem.setdefault("predictions", []).append({"id": change_id, "adopted": adopted, "problem": problem})
        return problem
    d = detectable(series_of(pred["measure"]), adopted)
    mem.setdefault("predictions", []).append({"id": change_id, "adopted": adopted, **pred, "detectable": d})
    return None

def update(mem, period, per_point, series_of):
    """Judge every prediction whose window has passed. Returns the new verdicts."""
    out = []
    starts = [p["adopted"] for p in mem.get("predictions", [])]
    for p in mem.get("predictions", []):
        if p.get("problem") or p.get("verdict"):
            continue
        j = judge(p, series_of(p["measure"]), period, per_point, starts)
        if j:
            p.update(j); p["judged_at"] = period
            out.append(p)
    return out

def markdown(mem, unit="period"):
    rows = mem.get("predictions", [])
    if not rows:
        return ""
    md = ["\n## Change verdicts (judged by the system with the protocol's signal rule; chance = the same test where nothing changed)\n",
          "| change | adopted | prediction | window | verdict | chance |", "| --- | --- | --- | --- | --- | --- |"]
    for p in rows[-12:]:
        if p.get("problem"):
            md.append(f"| {p['id']} | {unit} {p['adopted']} | not judged | | {p['problem'][:120]} | |")
            continue
        pr = f"{p['measure']} {p['dir']} within {p['n']} {p['unit']}s"
        if p.get("verdict"):
            ch = "" if p.get("chance") is None else f"{p['chance']:.0%}"
            md.append(f"| {p['id']} | {unit} {p['adopted']} | {pr} | {p['window'][0]}-{p['window'][1]} | {p['verdict']} | {ch} |")
        else:
            md.append(f"| {p['id']} | {unit} {p['adopted']} | {pr} | | pending | |")
    return "\n".join(md) + "\n"
