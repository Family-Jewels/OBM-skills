"""The smoke checks in PLAN.md, applied to a run folder. Each check passes or fails on the run's own records.

usage: python3 -I smoke_check.py <run-folder> [<run-folder> ...]
"""
import collections, gzip, json, sys
from pathlib import Path

def jsonl(p):
    if not p.exists() and Path(str(p) + '.gz').exists():
        return [json.loads(l) for l in gzip.open(str(p) + '.gz', 'rt') if l.strip()]
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []

def check(d):
    d = Path(d); r = json.loads((d / 'result.json').read_text()); ev = jsonl(d / 'cadence.jsonl'); steps = jsonl(d / 'steps.jsonl')
    pre = next((e for e in ev if e['event'] == 'preflight'), {})
    kinds = collections.Counter(e['event'] for e in ev)
    adopted = [e for e in ev if e['event'] == 'adopted' and e.get('branch') == 'improvement']
    reg, prob = kinds['prediction_registered'], kinds['prediction_problem']
    restated = kinds['prediction_restated']; verdicts = [e for e in ev if e['event'] == 'change_verdict']
    early = [e for e in adopted if e['period'] <= 70]
    tc = r.get('tool_calls') or 0; task_steps = sum(1 for s in steps if s.get('kind', '').startswith('task'))
    sw = d / 'workspace' / 'swarm'
    logs = [str(p.relative_to(d)) for p in (d / 'workspace').rglob('progress.md') if 'history' not in p.parts]
    st = r.get('steps') or {}; n = max(1, st.get('steps') or 0)
    cues = st.get('cues') or {}
    esc = kinds['escalation']; days = r.get('days_operated') or 0
    checks = [
        ('preflight passed and verification is on', pre.get('verification') is True,
         f"verification {pre.get('verification')}; problems: {pre.get('problems')}"),
        ('every day completed', bool(r.get('completed')) and days == r.get('days'), f"{days} of {r.get('days')} days; error {r.get('error')}"),
        ('every adopted change registered with a prediction, or its restatement asked for and answered',
         len(adopted) == reg + prob and prob <= restated + sum(1 for e in ev if e['event'].startswith('request_') and 'prediction-' in str(e.get('key', ''))),
         f"{len(adopted)} adopted; {reg} registered; {prob} could not be judged as written; {restated} restated"),
        ('a verdict, if a change was adopted by day 70', (not early) or bool(verdicts),
         f"{len(early)} adopted by day 70; verdicts: " + ', '.join(f"{v['id']} {v['verdict']}" for v in verdicts)),
        ('the step log holds every business call', tc == 0 or abs(task_steps - tc) <= 0.05 * tc, f"{task_steps} task steps against {tc} tool calls"),
        ('records at their protocol paths', not st.get('stray_writes') and all(l.startswith('workspace/swarm/') for l in logs),
         f"logs {logs or 'none'}; stray writes {st.get('stray_writes') or 'none'}"),
        ('cues fire, but on fewer than 1 step in 10 (cue arm)', r.get('steps_mode') != 'cue' or (0 < sum(cues.values()) < n / 10),
         f"cues {cues} over {n} steps"),
    ]
    info = {'final_balance': r.get('final_balance'), 'cost_usd': r.get('api_cost_usd'), 'review_cost_usd': r.get('cadence_cost_usd'),
            'cost_per_day': round((r.get('api_cost_usd') or 0) / max(1, days), 4), 'runtime_s': r.get('runtime_seconds'),
            'stocked_slots': r.get('avg_stocked_slots'), 'escalations_per_10_days': round(10 * esc / max(1, days), 2),
            'reviews': {k: kinds[k] for k in ('pulse', 'check', 'diagnosis', 'controls', 'strategist', 'aims', 'method', 'audit', 'organizer') if kinds[k]},
            'faults': kinds['fault'], 'requests_new': kinds['request_new'], 'config_changes': kinds['config_change'],
            'step_summary': {k: st.get(k) for k in ('steps', 'state_changing_share', 'reread_share', 'repeat_failures', 'longest_no_progress', 'own_log_bytes')}}
    return checks, info

if __name__ == '__main__':
    for d in sys.argv[1:]:
        checks, info = check(d)
        print(f"\n## {Path(d).name}: {'PASS' if all(ok for _, ok, _ in checks) else 'FAIL'}\n")
        for name, ok, why in checks:
            print(f"- [{'x' if ok else ' '}] {name}: {why}")
        print('\n' + json.dumps(info, indent=1))
