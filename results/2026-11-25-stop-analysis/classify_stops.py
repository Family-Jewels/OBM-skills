"""Classify early stops (more than half the working day left) by what the agent said that day. Keyword rules, checked by
hand on samples (see README). usage: python3 -I classify_stops.py <stops-*.jsonl>..."""
import json, re, sys, collections
RULES = [  # first match wins; order = most specific first
    ("follows a rule or plan to stop", r"end-game|endgame|\bM6\b|rule says|the rule|per the (spec|aims|rules)|aims say|instructions? say|don't buy|not buying|hold (cash|off)|stop (buying|ordering)"),
    ("believes demand is low", r"dead season|quiet (day|week|season)|no demand|low (sales|demand)|zero sales|sales are (low|slow)|off-season|seasonal"),
    ("waiting on stock or deliveries", r"deliver|arriv|lands? on|lands tomorrow|due (on|day)|until day \d|in transit|depot (is )?(empty|out)|out of (stock|the depot)|no (stock|energy|crisps|cola|units)|nothing (to load|to restock|in the depot|due)"),
    ("saving tokens or effort", r"token|spend(ing)? (tokens|calls|reads)|without (reading|reads|checking)|save (calls|reads)"),
    ("believes the day's work is done", r"done for|day'?s work|work (is )?done|complete for the day|finished|nothing (else|more) to do|all (slots )?(full|stocked)"),
    ("tool or reasoning error", r"error|failed|invalid|couldn't|could not|wasted"),
]
def cause(said):
    if not said.strip():
        return "no stated reason"
    for name, rx in RULES:
        if re.search(rx, said, re.I):
            return name
    return "other reason stated"
def main():
    tot = collections.Counter(); byq = collections.defaultdict(collections.Counter); n_early = n_days = 0
    for f in sys.argv[1:]:
        for line in open(f):
            x = json.loads(line)
            if x["minutes_used"] is None:
                continue
            n_days += 1
            if x["minutes_used"] > 240:
                continue
            n_early += 1
            c = cause(x["said"]); tot[c] += 1; byq[min(4, (x["day"] - 1) // 91 + 1)][c] += 1
    print(f"{n_early} early stops of {n_days} days ({n_early / n_days:.0%})")
    for c, n in tot.most_common():
        print(f"{n:5d} {n / n_early:4.0%}  {c:34s}  by quarter: " + " ".join(f"Q{q} {byq[q][c] / max(1, sum(byq[q].values())):4.0%}" for q in (1, 2, 3, 4)))

if __name__ == "__main__":
    main()
