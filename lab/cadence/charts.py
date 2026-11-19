"""Process behavior charts (XmR) and the gap to an exemplar (Gilbert's PIP), computed by the system from ground truth.

Limits come from each measure's own data, never from an agent: centre = mean, limits = mean +/- 2.66 x mean moving range.
A signal is a point beyond a limit, or 8 points in a row on one side of the centre. Everything inside the limits is
routine variation. Limits are fixed from the first `baseline_points` points of a phase (provisional after `min_points`).
A new phase starts when a redesign is adopted (the old limits are kept to judge whether it shifted the process) or when
a signal has persisted for `baseline_points` periods (the process now runs at a new level).
"""

def xmr(vals):
    m = sum(vals) / len(vals)
    mr = sum(abs(a - b) for a, b in zip(vals[1:], vals)) / max(1, len(vals) - 1)
    return {"center": round(m, 2), "lower": round(m - 2.66 * mr, 2), "upper": round(m + 2.66 * mr, 2)}

def signal(vals, lim, run=8):
    if not vals or not lim:
        return None
    x = vals[-1]
    if x > lim["upper"]:
        return "up", "beyond the upper limit"
    if x < lim["lower"]:
        return "down", "beyond the lower limit"
    tail = vals[-run:]
    if len(tail) == run and all(v > lim["center"] for v in tail):
        return "up", f"{run} in a row above the centre"
    if len(tail) == run and all(v < lim["center"] for v in tail):
        return "down", f"{run} in a row below the centre"
    return None

def interp(points, d):
    ks = sorted((int(k), v) for k, v in points.items())
    for (d0, v0), (d1, v1) in zip(ks, ks[1:]):
        if d0 <= d <= d1:
            return v0 + (v1 - v0) * (d - d0) / (d1 - d0)
    return None

def update(cfg, mem, period, measures, unit):
    """Record this period, recompute limits and signals. Returns (markdown, new bad-direction signals)."""
    cc = cfg.get("charts", {})
    specs = cc.get("measures", [])
    nb, mp, bp = cc.get("not_before", 0), cc.get("min_points", 8), cc.get("baseline_points", 20)
    st = mem.setdefault("charts", {"series": {}, "phase": {}, "reported": {}, "last_redesign": None})
    rows, since, bad = [], [], []
    for sp in specs:
        name, src = sp["name"], sp.get("from", sp["name"])
        v = measures.get(src)
        if v is None:
            continue
        ser = st["series"].setdefault(name, [])
        if sp.get("diff"):  # change over the last `diff` periods (1 = day to day)
            raw = st.setdefault("raw", {}).setdefault(src, [])
            raw.append(v); k = int(sp["diff"])
            del raw[:-(k + 1)]
            if len(raw) <= k:
                continue
            v = round(v - raw[0], 2)
        ser.append([period, v])
        ph = st["phase"].setdefault(name, {"start": nb, "limits": None, "frozen": False, "prev": None, "sig_since": None})
        pts = [x for d, x in ser if d >= ph["start"]]
        if not ph["frozen"] and len(pts) >= mp:
            ph["limits"] = xmr(pts[:bp]); ph["frozen"] = len(pts) >= bp
        lim = ph["limits"] or ph["prev"]
        sig = signal(pts if ph["limits"] else [x for d, x in ser if d >= ph["start"]], lim)
        better = sp.get("better", "up")
        if sig:
            ph["sig_since"] = ph["sig_since"] or period
            if ph["frozen"] and period - ph["sig_since"] >= bp:  # the process runs at a new level: new phase
                ph.update({"prev": ph["limits"], "start": period - bp + 1, "limits": None, "frozen": False, "sig_since": None})
                pts = [x for d, x in ser if d >= ph["start"]]; ph["limits"] = xmr(pts); ph["frozen"] = True
                sig = None
        else:
            ph["sig_since"] = None
        good = sig and (sig[0] == better)
        status = "—" if not lim else ("routine variation" if not sig else f"{'IMPROVEMENT' if good else 'WORSE'}: {sig[1]}")
        key = f"{name}:{sig[0] if sig else ''}"
        if sig and not good and st["reported"].get(name) != key:
            bad.append(f"{name} {sig[1]}")
        st["reported"][name] = key if sig else ""
        lim_s = (f"{lim['center']} | {lim['lower']} | {lim['upper']}" + ("" if ph["frozen"] else " (provisional)")) if lim else "collecting | | "
        rows.append(f"| {name} | {better} | {ph['start']} | {lim_s} | {v} | {status} |")
        if ph["prev"] and st["last_redesign"]:
            after = [x for d, x in ser if d >= st["last_redesign"][1]]
            if after:
                pl = ph["prev"]; m = round(sum(after) / len(after), 2)
                shift = signal(after, pl)
                since.append(f"| {name} | {pl['center']} ({pl['lower']} to {pl['upper']}) | {m} | {len(after)} | "
                             f"{('shift ' + shift[0] + ': ' + shift[1]) if shift else 'no shift yet'} |")
    md = [f"# Process behavior charts (written by the system every {unit}; do not edit)", "",
          "Limits come from each measure's own data (centre +/- 2.66 x average moving range), never from an agent. Inside the limits "
          "is routine variation: do not react to it. A signal is a point beyond a limit or 8 in a row on one side of the centre.", "",
          f"| measure | better | phase since {unit} | centre | lower | upper | latest | status |", "| --- | --- | --- | --- | --- | --- | --- | --- |"] + rows
    if since:
        r = st["last_redesign"]
        md += ["", f"## Since redesign {r[0]} (adopted {unit} {r[1]}): judged against the limits from before it", "",
               "| measure | before: centre (limits) | since: mean | points | shift |", "| --- | --- | --- | --- | --- |"] + since
    ex = cfg.get("exemplar")
    if ex and measures.get(ex["measure"]) is not None:
        e = interp(ex["points"], period); a = measures[ex["measure"]]; o = ex.get("origin", 0)
        if e is not None:
            pip = round((e - o) / (a - o), 1) if a - o > 0 else None
            md += ["", "## Gap to the exemplar (PIP = exemplar gain / actual gain)", "",
                   f"{ex['measure']} at {unit} {period}: actual {a}, exemplar {round(e, 2)} ({ex.get('source', 'exemplar')}). "
                   + (f"PIP = {pip}: the exemplar has gained {pip}x as much." if pip else
                      f"PIP not defined yet: the exemplar has gained {round(e - o, 2)} from {o}; the swarm has gained {round(a - o, 2)}.")]
    best = []
    bw = int(cc.get("own_best_window", 7))  # v1: 7 periods; v2: the task's point window
    for sp in specs:
        ser = st["series"].get(sp["name"], [])
        if len(ser) >= 2 * bw:
            avgs = [sum(x for _, x in ser[i - bw:i]) / bw for i in range(bw, len(ser) + 1)]
            hi = max(avgs) if sp.get("better", "up") == "up" else min(avgs)
            best.append(f"| {sp['name']} | {round(hi, 2)} | {round(avgs[-1], 2)} |")
    if best:
        md += ["", f"## Own best ({bw}-period average)", "", "| measure | best so far | latest |", "| --- | --- | --- |"] + best
    return "\n".join(md) + "\n", bad

def new_phase(mem, rid, period):
    """A redesign was adopted: keep today's limits to judge it, and start collecting the new process's own."""
    st = mem.setdefault("charts", {"series": {}, "phase": {}, "reported": {}, "last_redesign": None})
    st["last_redesign"] = [rid, period]
    for ph in st["phase"].values():
        if ph["limits"]:
            ph.update({"prev": ph["limits"], "start": period, "limits": None, "frozen": False, "sig_since": None})
