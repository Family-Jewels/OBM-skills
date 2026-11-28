"""The decision rules in PLAN.md, computed from the filed runs, so the verdict is arithmetic, not judgment.

usage: python3 -I evaluate.py [batch-folder]     (default: the folder this file is in)
"""
import itertools, json, statistics as st, sys
from pathlib import Path

B = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
FLOOR = 13435  # v1's worst five-seed run, in euros
ARMS = ('obm_v4', 'obm_v5')

def load(arm, seed):
    p = B / f'{arm}-seed{seed}-365d' / 'result.json'
    return json.loads(p.read_text()) if p.exists() else None

def sign_flip_p(diffs):
    """Exact one-sided p for a mean paired gain at least this large, over every sign assignment."""
    obs = st.mean(diffs); n = 0; hits = 0
    for signs in itertools.product((1, -1), repeat=len(diffs)):
        n += 1; hits += st.mean(s * abs(d) for s, d in zip(signs, diffs)) >= obs - 1e-9
    return hits / n

rows, pairs = [], []
for seed in range(1, 6):
    r4, r5 = load('obm_v4', seed), load('obm_v5', seed)
    rows.append((seed, r4, r5))
    if r4 and r5:
        pairs.append((seed, r4['final_balance'], r5['final_balance']))
out = {'seeds_with_both_arms': len(pairs)}
print(f"| Seed | obm_v4 | obm_v5 | Difference (v5 - v4) |\n| --- | ---: | ---: | ---: |")
for seed, r4, r5 in rows:
    f = lambda r: f"€{r['final_balance']:,.0f}" + ('' if r.get('completed') else ' (stopped)') if r else 'not yet'
    d = f"€{r5['final_balance'] - r4['final_balance']:+,.0f}" if r4 and r5 else ''
    print(f"| {seed} | {f(r4)} | {f(r5)} | {d} |")
if pairs:
    diffs = [b - a for _, a, b in pairs]
    wins = sum(d > 0 for d in diffs)
    out.update({'v5_wins': wins, 'mean_gain': round(st.mean(diffs), 2), 'sd_gain': round(st.stdev(diffs), 2) if len(diffs) > 1 else None,
                'sign_flip_p_one_sided': round(sign_flip_p(diffs), 3)})
    if len(pairs) == 5:
        out['primary_rule_met'] = wins >= 4 and st.mean(diffs) > 0
for arm in ARMS:
    rs = [r for _, *rr in rows for r in rr if r and r.get('arm') == arm]
    if rs:
        out[arm] = {'runs': len(rs), 'mean': round(st.mean(r['final_balance'] for r in rs), 2),
                    'below_floor': sum(r['final_balance'] < FLOOR for r in rs), 'safe': all(r['final_balance'] >= FLOOR for r in rs),
                    'mean_cost_usd': round(st.mean(r.get('api_cost_usd') or 0 for r in rs), 2),
                    'mean_stocked_slots': round(st.mean(r.get('avg_stocked_slots') or 0 for r in rs), 2),
                    'resumes': sum(r.get('resumes', 0) for r in rs)}
print('\n' + json.dumps(out, indent=1))
