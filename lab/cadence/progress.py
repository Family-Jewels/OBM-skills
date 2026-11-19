"""Progress measures, computed by the system from ground truth (engine version 2).

XmR charts (charts.py) say whether a process is stable. This module says whether it is getting better and how much room
is left, following Precision Teaching's standard celeration practice:

- Timing comes from the task. The adapter states the horizon, the task's natural cycle and its clock (periods, or budget
  spent). A point window is the shortest span that holds whole cycles and at least 3 observations while still leaving at
  least 12 points across the horizon (3 to start, then 3 for each of three phases). If no window meets all three, the
  horizon is too short for celeration and only level charts are used.
- Each point is the median of a flow (an amount per period) over its window, or the last value of a positive level.
  Values at or below zero sit under the record floor and are left out of the fit.
- Celeration is the multiplier per point from a median-based fit on the log scale: quarter-intersect up to 7 points,
  then Theil-Sen (the median of all pairwise slopes). Its range is the middle half of the pairwise slopes. Bounce is the
  envelope at +/- 2 standard deviations of the log residuals, as a multiplier (top / bottom).
- A celeration is provisional below 6 points. A new phase starts at each redesign; the change is read as a jump (level)
  and a turn (new celeration / old).
- For the top measure: the floor line runs from the level after 3 points to the target at the horizon (the decision rules
  fire against it); the aim line is a deliberate overshoot, the same target by half the remaining horizon. Falling short of
  the aim triggers nothing. When the aim is met on 2 of the last 3 points it is redrawn from there toward double the target.
"""
import math

MIN_OBS, MIN_POINTS, START, FIRM = 3, 12, 3, 6

def derive_window(horizon, cycle=1, clock="period"):
    """Shortest window of whole cycles holding >= MIN_OBS observations, leaving >= MIN_POINTS points over the horizon."""
    cycle = max(1, int(cycle))
    w = cycle * (math.ceil(MIN_OBS / cycle) if clock == "period" else 1)
    n = int(horizon // w) if w else 0
    ok = n >= MIN_POINTS
    why = (f"{w} {'periods' if clock == 'period' else 'clock units'} per point: whole cycles of {cycle}, at least {MIN_OBS} "
           f"observations each, {n} points across the horizon of {horizon}")
    if not ok:
        why = f"horizon {horizon} too short for celeration: a point of {w} leaves {n} points, fewer than {MIN_POINTS}"
    return {"w": w, "n": n, "ok": ok, "why": why}

def _median(xs):
    s = sorted(xs); n = len(s)
    return None if not n else (s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2)

def _quantile(xs, q):
    s = sorted(xs)
    if not s:
        return None
    i = q * (len(s) - 1); lo = math.floor(i); hi = math.ceil(i)
    return s[lo] + (s[hi] - s[lo]) * (i - lo)

def points(series, w, kind="flow", now=None):
    """series: [(t, value)]. Returns [(k, value, n_obs)] for each completed window k (t in ((k)*w, (k+1)*w])."""
    if not series:
        return []
    now = series[-1][0] if now is None else now
    groups = {}
    for t, v in series:
        if v is None:
            continue
        groups.setdefault(int(math.ceil(t / w)) - 1 if t > 0 else 0, []).append(v)
    out = []
    for k in sorted(groups):
        if now < (k + 1) * w:
            continue  # window still open
        vals = groups[k]
        out.append((k, _median(vals) if kind == "flow" else vals[-1], len(vals)))
    return out

def fit(pts):
    """Median-based fit of log10(value) on point index. pts: [(k, value, n)]. None below START usable points."""
    xy = [(k, math.log10(v)) for k, v, _ in pts if v is not None and v > 0]
    n = len(xy)
    if n < START:
        return None
    pair = [(y2 - y1) / (x2 - x1) for i, (x1, y1) in enumerate(xy) for x2, y2 in xy[i + 1:] if x2 != x1]
    if n <= 7:  # quarter-intersect: median point of each half, the middle point left out when n is odd
        h = n // 2
        a, b = xy[:h], xy[n - h:]
        x1, y1 = _median([x for x, _ in a]), _median([y for _, y in a])
        x2, y2 = _median([x for x, _ in b]), _median([y for _, y in b])
        slope = (y2 - y1) / (x2 - x1) if x2 != x1 else 0.0
        method = "quarter-intersect"
    else:
        slope = _median(pair); method = "Theil-Sen"
    icpt = _median([y - slope * x for x, y in xy])
    res = [y - (icpt + slope * x) for x, y in xy]
    sd = math.sqrt(sum(r * r for r in res) / max(1, n - 1)) if n > 1 else 0.0
    return {"n": n, "slope": slope, "icpt": icpt, "cel": 10 ** slope, "lo": 10 ** _quantile(pair, 0.25),
            "hi": 10 ** _quantile(pair, 0.75), "bounce": 10 ** (4 * sd), "method": method, "provisional": n < FIRM,
            "first_k": xy[0][0], "last_k": xy[-1][0]}

def line_at(f, k):
    return 10 ** (f["icpt"] + f["slope"] * k)

def fmt_cel(c):
    if c is None:
        return "—"
    return f"x{c:.2f}" if c >= 1 else f"/{1 / c:.2f}"

def verdict(f, better="up"):
    """'flat' when the middle half of pairwise slopes spans x1.0; 'wrong way' when all of it points the wrong way."""
    if not f:
        return "collecting"
    if f["lo"] <= 1.0 <= f["hi"]:
        return "flat"
    up = f["lo"] > 1.0
    return "improving" if up == (better == "up") else "wrong way"

def update(mem, spec, t, measures, resources):
    """Record this reading, recompute progress. Returns (markdown, events). Events: dicts with 'kind' in
    new_point, below_floor, flat_or_wrong, below_own_line, aim_raised, guardrail."""
    st = mem.setdefault("progress", {"series": {}, "phases": [0], "lines": None, "aim_raises": 0, "last_point": -1,
                                     "flags_reported": {}, "best_cel": {}})
    win = mem.setdefault("window", derive_window(spec["horizon"], spec.get("cycle", 1), spec.get("clock", "period")))
    w = win["w"]; events = []
    flows = spec.get("measures", {})
    for name, m in flows.items():
        v = measures.get(m.get("from", name))
        if v is not None:
            st["series"].setdefault(name, []).append([t, v])
    top = spec["top"]; tb = flows[top].get("better", "up")
    md = ["", "## Progress: celeration (written by the system; do not edit)", "",
          f"Point window: {win['why']}." if win["ok"] else f"Celeration off: {win['why']}. Use the level charts above."]
    if not win["ok"]:
        return "\n".join(md) + "\n", events
    allpts = {name: points(st["series"].get(name, []), w, m.get("kind", "flow"), now=t) for name, m in flows.items()}
    tp = allpts.get(top, [])
    newest = tp[-1][0] if tp else -1
    if newest > st["last_point"]:
        st["last_point"] = newest
        events.append({"kind": "new_point", "k": newest})
    phase_start = st["phases"][-1]  # point index where the current phase begins
    rows = []
    fits = {}
    for name, m in flows.items():
        pts = allpts[name]
        cur = [p for p in pts if p[0] >= phase_start]
        f = fit(cur); fits[name] = f
        better = m.get("better", "up")
        if f and not f["provisional"]:
            b = st["best_cel"].get(name)
            good = (f["cel"] > b) if (b is not None and better == "up") else ((f["cel"] < b) if b is not None else True)
            if good:
                st["best_cel"][name] = f["cel"]
        rows.append(f"| {name} | {m.get('kind', 'flow')} | {better} | {len(cur)} | "
                    + (f"{fmt_cel(f['cel'])}{' (provisional)' if f['provisional'] else ''} | {fmt_cel(f['lo'])} to {fmt_cel(f['hi'])} | "
                       f"x{f['bounce']:.1f} | {fmt_cel(st['best_cel'].get(name))} | {verdict(f, better)} |" if f else
                       f"collecting | | | {fmt_cel(st['best_cel'].get(name))} | collecting |"))
    md += ["", f"Celeration is the multiplier per point ({w} {spec.get('unit', 'period')}s), fitted on the log scale in the current phase "
           f"(since point {phase_start + 1}). Range: the middle half of the pairwise slopes. Bounce: the envelope at +/- 2 SD, top / bottom. "
           f"Provisional below {FIRM} points.", "",
           "| measure | kind | better | points | celeration | range | bounce | own best | status |",
           "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"] + rows
    # Top measure: floor line and stretch aim.
    target = spec.get("goal", {}).get("value")
    total = max(1, int(spec["horizon"] // w))
    usable = [p for p in tp if p[1] and p[1] > 0]
    if target and st["lines"] is None and len(usable) >= START:
        k0, v0, _ = usable[START - 1]
        left = max(1, total - 1 - k0)
        st["lines"] = {"k0": k0, "v0": v0, "target": target, "floor": (target / v0) ** (1 / left) if v0 > 0 else None,
                       "aim_k0": k0, "aim_v0": v0, "aim_target": target, "aim": (target / v0) ** (1 / max(1, left / 2))}
    L = st["lines"]
    if L and usable:
        k, v, _ = usable[-1]
        floor_v = L["v0"] * L["floor"] ** (k - L["k0"])
        aim_at = lambda kk: min(L["aim_v0"] * L["aim"] ** (kk - L["aim_k0"]), L["aim_target"])  # the aim star: the target, then held
        aim_v = aim_at(k)
        f = fits.get(top)
        md += ["", f"## Top measure: {top}", "",
               f"Floor line (minimum celeration to reach {L['target']:,.0f} by the horizon): {fmt_cel(L['floor'])} per point from point "
               f"{L['k0'] + 1}. Aim line (a deliberate overshoot: {L['aim_target']:,.0f} by half the remaining horizon): {fmt_cel(L['aim'])} per "
               f"point from point {L['aim_k0'] + 1}. Falling short of the aim is expected and triggers nothing.", "",
               f"Latest point {k + 1} ({spec.get('unit', 'period')}s {k * w + 1}-{(k + 1) * w}): {v:,.2f}; floor line {floor_v:,.2f}; aim line {aim_v:,.2f}. Required celeration from here to the target: "
               f"{fmt_cel((L['target'] / v) ** (1 / max(1, total - 1 - k)) if v > 0 else None)}; actual (this phase): {fmt_cel(f['cel']) if f else 'collecting'}."]
        last3 = [p for p in usable if p[0] > L["k0"]][-3:]
        below = [p for p in last3 if p[1] < L["v0"] * L["floor"] ** (p[0] - L["k0"])]
        if len(last3) == 3 and len(below) == 3:
            events.append({"kind": "below_floor", "k": k, "label": f"{top}: 3 points in a row below the floor line"})
        since_aim = [p for p in usable if p[0] > L["aim_k0"]][-3:]  # judged only on points after the aim was drawn
        met = [p for p in since_aim if p[1] >= aim_at(p[0])]
        if len(since_aim) == 3 and len(met) >= 2:
            L["aim_raises"] = L.get("aim_raises", 0) + 1
            L.update({"aim_k0": k, "aim_v0": v, "aim_target": L["aim_target"] * 2})
            L["aim"] = (L["aim_target"] / v) ** (1 / max(1, (total - 1 - k) / 2))
            events.append({"kind": "aim_raised", "k": k, "label": f"aim met on 2 of the last 3 points: redrawn toward {L['aim_target']:,.0f}"})
    ftop = fits.get(top)
    if ftop and verdict(ftop, tb) in ("flat", "wrong way"):
        events.append({"kind": "flat_or_wrong", "k": newest, "label": f"{top} celeration {verdict(ftop, tb)} ({fmt_cel(ftop['cel'])}, range "
                       f"{fmt_cel(ftop['lo'])} to {fmt_cel(ftop['hi'])})"})
    if ftop:
        cur = [p for p in tp if p[0] >= phase_start and p[1] and p[1] > 0][-3:]
        if len(cur) == 3 and all(p[1] < line_at(ftop, p[0]) for p in cur):
            events.append({"kind": "below_own_line", "k": newest, "label": f"{top}: 3 points in a row below its own celeration line"})
    # Jump and turn at the last phase change.
    if len(st["phases"]) > 1:
        ps, pp = st["phases"][-1], st["phases"][-2]
        old = fit([p for p in tp if pp <= p[0] < ps]); new = fit([p for p in tp if p[0] >= ps])
        first = [p for p in tp if p[0] >= ps and p[1] and p[1] > 0][:1]
        jump = (first[0][1] / line_at(old, first[0][0])) if (old and first) else None
        turn = (new["cel"] / old["cel"]) if (old and new) else None
        md += ["", f"## Since the phase change at point {ps + 1}", "",
               f"Jump (first point / old line projected): {fmt_cel(jump) if jump else 'needs a point and an old line'}. "
               f"Turn (new celeration / old): {fmt_cel(turn) if turn else 'needs 3 points in the new phase'}."]
    # Resources.
    if resources:
        md += ["", "## Resources (used / available, written by the system)", "", "| resource | used | available | in use | idle |",
               "| --- | --- | --- | --- | --- |"]
        for rname, r in resources.items():
            u, a = r.get("used"), r.get("available")
            pct = f"{100 * u / a:.0f}%" if (u is not None and a) else "—"
            md.append(f"| {rname} | {u} | {a} | {pct} | {round(a - u, 2) if (u is not None and a is not None) else '—'} |")
    # Guardrails.
    gr = []
    for g in spec.get("guardrails", []):
        v = measures.get(g["measure"])
        if v is None:
            continue
        breach = (g.get("min") is not None and v < g["min"]) or (g.get("max") is not None and v > g["max"])
        gr.append(f"| {g['label']} | {g['measure']} {'>=' if g.get('min') is not None else '<='} "
                  f"{g.get('min') if g.get('min') is not None else g.get('max')} | {v} | {'BREACHED' if breach else 'ok'} |")
        if breach:
            events.append({"kind": "guardrail", "label": f"guardrail breached: {g['label']} ({g['measure']} = {v})"})
    if gr:
        md += ["", "## Guardrails (a side that must not be crossed; experiments stay inside them)", "",
               "| guardrail | rule | latest | status |", "| --- | --- | --- | --- |"] + gr
    return "\n".join(md) + "\n", events

def new_phase(mem):
    st = mem.get("progress")
    if st is not None:
        st["phases"].append(st["last_point"] + 1)
