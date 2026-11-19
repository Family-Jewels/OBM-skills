"""Experiments as the system runs them (engine version 2): isolation, fidelity, and the data for the auditor's verdict.

No role judges its own work. The designer writes an experiment; the orchestrator makes the change on its slice and writes
'Applied: <period>'; the system calls the checker for a fidelity check against a ground-truth snapshot; the clock starts
only when it passes; at the end the system compares slice against control on the experiment's own driver and calls the
auditor for the verdict (keep, revert, or too small to read); the orchestrator applies it.

Experiment file (swarm/experiments/E-NNN.md), one field per line, in any wording around the colon:
  Driver: <one of the measures the system records>   Slice: <unit ids, comma-separated, or 'all'>   Control: rest
  Change: ...   Prediction: ...   Guardrail: ...   Start: <period>   End: <period>
States: planned -> queued (its slice overlaps a running experiment) -> fidelity -> running -> verdict -> done, or void
(driver not measured, or fidelity failed 3 times).
"""
import math, re
import progress as P

ACTIVE = ("fidelity", "running", "verdict")

def _field(txt, key):
    m = re.search(rf"\b{key}\b\W*:\s*(.+?)(?:\s{{2,}}[A-Z][a-z]+\s*:|$)", txt, re.I | re.M)
    return m.group(1).strip().strip("*").strip() if m else None

def _num(txt, key):
    m = re.search(rf"\b{key}\b\W*:\W*[^\d\n]{{0,15}}?(\d+)", txt, re.I)
    return int(m.group(1)) if m else None

def parse(sw):
    out = []
    d = sw / "experiments"
    for f in sorted(d.glob("E-*.md")) if d.exists() else []:
        txt = f.read_text(errors="ignore")
        sl = (_field(txt, "Slice") or "all")
        out.append({"id": f.stem, "file": f, "driver_text": _field(txt, "Driver") or "?", "slice_text": sl,
                    "slice": "all" if sl.lower().startswith("all") else [u.strip(" .`*") for u in re.split(r"[,;]", sl) if u.strip(" .`*")],
                    "start": _num(txt, "Start"), "end": _num(txt, "End"), "applied": _num(txt, "Applied")})
    return out

def driver_of(text, spec):
    """The measure the experiment names, matched as a whole word; unit measures first."""
    names = list(spec.get("unit_measures", {})) + list(spec.get("measures", {}))
    for n in sorted(names, key=len, reverse=True):
        if re.search(rf"(?<![\w-]){re.escape(n)}(?![\w-])", text):
            return n
    return None

def record_units(mem, t, units):
    """units: {unit_id: {measure: value}} from the adapter's reading."""
    st = mem.setdefault("units", {})
    for u, ms in (units or {}).items():
        for m, v in ms.items():
            if v is not None:
                st.setdefault(m, {}).setdefault(u, []).append([t, v])

def _overlap(a, b):
    return a == "all" or b == "all" or bool(set(a) & set(b))

def _series(mem, spec, drv, members):
    """Daily series of a measure: a network measure, or the mean over the given units of a unit measure."""
    if drv in spec.get("measures", {}):
        return mem["progress"]["series"].get(drv, [])
    per = mem.get("units", {}).get(drv, {})
    by_t = {}
    for u in members:
        for t, v in per.get(u, []):
            by_t.setdefault(t, []).append(v)
    return [[t, sum(vs) / len(vs)] for t, vs in sorted(by_t.items()) if vs]

def compare(mem, spec, e, s, W):
    """The data for the verdict. Slice against control on the driver when the driver is a unit measure and the slice is
    part of the units; otherwise the driver's own series before and after, against its earlier line. Too small to read when
    the effect sits inside the envelope of the earlier bounce (+/- 2 SD on the log scale)."""
    drv = s["driver"]; better = (spec.get("unit_measures", {}).get(drv) or spec.get("measures", {}).get(drv) or {}).get("better", "up")
    kind = (spec.get("unit_measures", {}).get(drv) or spec.get("measures", {}).get(drv) or {}).get("kind", "flow")
    t0, t1 = s["start_t"], s["end_t"]
    allu = sorted(mem.get("units", {}).get(drv, {}))
    if drv in spec.get("unit_measures", {}) and e["slice"] != "all" and set(e["slice"]) < set(allu):
        sl, ct = _series(mem, spec, drv, e["slice"]), _series(mem, spec, drv, [u for u in allu if u not in e["slice"]])
        ctl = dict((t, v) for t, v in ct)
        ser = [[t, v / ctl[t]] for t, v in sl if ctl.get(t) and v and v > 0 and ctl[t] > 0]
        how = f"slice ({', '.join(e['slice'])}) / control (the other {len(allu) - len(e['slice'])} units), daily ratio of means"
        pts = P.points(ser, W, "flow")
        before = [p for p in pts if (p[0] + 1) * W < t0][-6:]
        after = [p for p in pts if p[0] * W + 1 >= t0 and (p[0] + 1) * W <= t1]
        base = P._median([p[1] for p in before]) if before else 1.0
        effect = (P._median([p[1] for p in after]) / base) if after else None
        logs = [math.log10(p[1]) for p in before if p[1] > 0]
    else:
        ser = _series(mem, spec, drv, allu)
        pts = P.points(ser, W, kind)
        before = [p for p in pts if (p[0] + 1) * W < t0][-6:]
        after = [p for p in pts if p[0] * W + 1 >= t0 and (p[0] + 1) * W <= t1]
        f = P.fit(before)
        how = (f"{drv} for the whole system, after the start against the line fitted before it" if f else
               f"{drv} for the whole system, after the start against the median before it")
        exp_v = (lambda k: P.line_at(f, k)) if f else (lambda k: P._median([p[1] for p in before]) if before else None)
        rat = [p[1] / exp_v(p[0]) for p in after if p[1] and p[1] > 0 and exp_v(p[0])]
        effect = P._median(rat) if rat else None
        logs = ([math.log10(p[1]) - math.log10(P.line_at(f, p[0])) for p in before if p[1] > 0] if f else
                [math.log10(p[1]) for p in before if p[1] and p[1] > 0])
    sd = (math.sqrt(sum((x - sum(logs) / len(logs)) ** 2 for x in logs) / (len(logs) - 1)) if len(logs) >= 2 else None)
    half = 10 ** (2 * sd) if sd is not None else None
    if effect is None:
        reading = "no points yet in the experiment window"
    elif half is None:
        reading = "no earlier bounce to judge against (fewer than 2 points before the start)"
    elif effect > half or effect < 1 / half:
        good = (effect > 1) == (better == "up")
        reading = f"{'better' if good else 'worse'} beyond the earlier bounce"
    else:
        reading = "too small to read: inside the earlier bounce"
    return {"how": how, "before_n": len(before), "after_n": len(after), "effect": effect, "envelope": half, "reading": reading,
            "better": better}

def step(mem, spec, sw, t, newest, new_point, W):
    """Advance every experiment's state. Returns (markdown, actions). Actions: ('fidelity', e), ('verdict', e, cmp),
    ('note', text)."""
    exps = parse(sw); S = mem.setdefault("exp", {}); acts = []
    rows = []
    known = sorted({u for m in mem.get("units", {}).values() for u in m}, key=len, reverse=True)
    for e in exps:
        if e["slice"] != "all" and known:  # pick the known unit ids out of whatever the designer wrote around them
            found = [u for u in known if re.search(rf"(?<![\w:-]){re.escape(u)}(?![\w:-])", e["slice_text"])]
            if not found:  # a group named instead, e.g. a location: every unit whose id starts with it
                found = [u for u in known if any(re.search(rf"(?<![\w:-]){re.escape(g)}(?![\w-])", e["slice_text"])
                                                 for g in [u.rsplit(":", k)[0] for k in range(1, u.count(":") + 1)])]
            e["slice"] = found or "all"
        s = S.setdefault(e["id"], {"state": "planned", "fails": 0})
        drv = driver_of(e["driver_text"], spec); s["driver"] = drv
        s["len"] = max(3 * W, (e["end"] or 0) - (e["start"] or 0))
        if s["state"] == "planned" and drv is None:
            s["state"] = "void"; s["why"] = "its driver is not a measure the system records"
            acts.append(("note", f"experiment {e['id']} cannot run: its driver ('{e['driver_text'][:60]}') is not a measure the system records. "
                         f"The designer must name one of: {', '.join(list(spec.get('unit_measures', {})) + list(spec.get('measures', {})))}."))
        if s["state"] in ("planned", "queued") and e["start"] is not None and t >= e["start"]:
            busy = [o for o in exps if o["id"] != e["id"] and S.get(o["id"], {}).get("state") in ACTIVE and _overlap(o["slice"], e["slice"])]
            if busy:
                if s["state"] != "queued":
                    acts.append(("note", f"experiment {e['id']} is queued: its slice overlaps {', '.join(o['id'] for o in busy)}, which is still "
                                 f"running. Do not make its change until the system says it may start."))
                s["state"] = "queued"
            else:
                if s["state"] == "queued":
                    acts.append(("note", f"experiment {e['id']} may start now: make its change on its slice only, then write 'Applied: <period>' in its file."))
                    s["state"] = "planned"; s["release_t"] = t
                ready = e["applied"] is not None or t >= max(e["start"], s.get("release_t", 0)) + max(1, W // 2)
                if ready and not s.get("check_pending") and t >= s.get("next_check_t", 0):
                    s["state"] = "fidelity"; s["check_pending"] = True; acts.append(("fidelity", e))
        if s["state"] == "running" and t >= s["end_t"]:
            cmp = compare(mem, spec, e, s, W); s["cmp"] = cmp; s["state"] = "verdict"; acts.append(("verdict", e, cmp))
        c = s.get("cmp")
        rows.append(f"| {e['id']} | {drv or 'not measured'} | {', '.join(e['slice']) if e['slice'] != 'all' else 'all'} | {e['start'] or '?'} | {e['end'] or '?'} | "
                    f"{s.get('start_t', '—')} | {s['state']}{(': ' + s['verdict']) if s.get('verdict') else ''} | "
                    + (f"{P.fmt_cel(c['effect']) if c['effect'] else '—'} | {('within x' + format(c['envelope'], '.2f')) if c['envelope'] else '—'} | {c['reading']} |" if c else " | | |"))
    md = []
    if rows:
        md = ["", "## Experiments (run and judged by the system; verdicts by the auditor)", "",
              "Lifecycle: planned, queued (its slice overlaps a running one), fidelity (the checker is verifying the change), running "
              "(the clock started when fidelity passed), verdict (the auditor is ruling), done. Effect: the driver after the start "
              "divided by its expected value (slice against control where the driver is measured per unit); read against the "
              "envelope of the earlier bounce.", "",
              "| experiment | driver | slice | start | end | clock started | state | effect | envelope | reading |",
              "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"] + rows
    return "\n".join(md) + ("\n" if md else ""), acts

def fidelity_result(mem, eid, rec, t, W):
    s = mem["exp"][eid]; s["check_pending"] = False
    ok = re.search(r"fidelity\W*:\W*pass", rec, re.I) is not None
    if ok:
        s.update({"state": "running", "start_t": t, "end_t": t + s.get("len", 3 * W)})
    else:
        s["fails"] += 1; s["next_check_t"] = t + max(1, W // 2)
        s["state"] = "void" if s["fails"] >= 3 else "planned"
        if s["state"] == "void":
            s["why"] = "fidelity failed 3 times"
    return ok, s["state"]

def verdict_result(mem, eid, rec):
    s = mem["exp"][eid]
    m = re.search(r"verdict\W*:\W*(keep|revert|too small to read)", rec, re.I)
    s["verdict"] = m.group(1).lower() if m else "unclear"; s["state"] = "done"
    return s["verdict"]
