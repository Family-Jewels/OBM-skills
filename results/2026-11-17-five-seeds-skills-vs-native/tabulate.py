import json, collections, re, glob, os, sys
B = __import__("os").environ.get("SEEDS_DIR", "/home/claude/vb-runs/seeds")
FREEZE = re.compile(r"(freeze|frozen|pause (all )?(new )?(order|purchas|buy)|halt (all )?(order|purchas|buy)|no new (orders|purchases)|stop (all )?(order|purchas|buy))", re.I)
rows = {}
for arm in ("obm_cadence", "native_cadence"):
    for s in range(1, 6):
        d = f"{B}/{arm}-seed{s}-365d"
        if not os.path.exists(d):
            d = f"{B}/{arm}-seed{s}"
        if not os.path.exists(f"{d}/result.json"):
            continue
        r = json.load(open(f"{d}/result.json"))
        ev = collections.Counter()
        redesign_periods = []
        for l in open(f"{d}/cadence.jsonl"):
            e = json.loads(l)
            k = e.get("kind") or e.get("event")
            ev[k] += 1
            if k == "redesign":
                redesign_periods.append(e.get("period"))
        hits = []
        for f in glob.glob(f"{d}/workspace/**/*.md", recursive=True):
            for i, line in enumerate(open(f, errors="ignore")):
                if FREEZE.search(line):
                    hits.append((os.path.relpath(f, d), i + 1, line.strip()[:200]))
        rows[(arm, s)] = dict(
            score=r["final_balance"], days=r["days_operated"], cost=r["api_cost_usd"],
            cad=r.get("cadence_cost_usd"), slots=r["avg_stocked_slots"], q=r["revenue_by_quarter"],
            pulses=ev["pulse"], audits=ev["audit"], diag=ev["diagnosis"], deferred=ev["diagnosis_deferred"],
            redesigns=ev["redesign"], redesign_periods=redesign_periods,
            plan_versions=len(glob.glob(f"{d}/workspace/swarm/history/plan-v*.md")),
            freeze_hits=hits)
json.dump({f"{a}|{s}": v for (a, s), v in rows.items()}, open(sys.argv[1] if len(sys.argv) > 1 else "/dev/stdout", "w"), indent=1)
for (a, s), v in sorted(rows.items(), key=lambda x: (x[0][1], x[0][0])):
    print(f"{a:15s} s{s} €{v['score']:>9,.0f} d{v['days']} ${v['cost']:.2f}+{v['cad']} slots {v['slots']} Q{[round(x) for x in v['q']]} "
          f"P{v['pulses']} A{v['audits']} D{v['diag']} def{v['deferred']} R{v['redesigns']}@{v['redesign_periods']} pv{v['plan_versions']} freezeHits {len(v['freeze_hits'])}")
