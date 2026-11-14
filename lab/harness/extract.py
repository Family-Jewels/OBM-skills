import json, sys
def result(stream):
    r = None
    for l in open(stream):
        try: d = json.loads(l)
        except Exception: continue
        if d.get("type") == "result": r = d
    return r
if __name__ == "__main__":
    for s in sys.argv[1:]:
        r = result(s)
        print(s, None if r is None else (r.get("subtype"), round(r.get("total_cost_usd", 0), 3), r.get("num_turns")))
