"""Tests for the seed batch driver, with a fake runner (no simulator, no model). Run: python3 -I test_seed_batch.py"""
import json, os, subprocess, sys, tempfile, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
tmp = Path(tempfile.mkdtemp())
runs, out, plan = tmp / 'runs', tmp / 'batch', tmp / 'plan.json'
fake = tmp / 'fake_runner.py'
fake.write_text(r'''
import json, sys, time, os
from pathlib import Path
a = sys.argv[1:]
plan = json.loads(Path(os.environ['FAKE_PLAN']).read_text())
if '--resume' in a:
    d = Path(a[a.index('--resume') + 1]); n = d.name
    rs = json.loads((d / 'resume.json').read_text())
    (d / 'result.json').write_text(json.dumps({'final_balance': 20000, 'completed': True, 'days_operated': 3, 'error': None,
                                               'resumes': len(rs['cutoffs']), 'api_cost_usd': 1.0}))
    (d / 'resume.json').rename(d / 'resume.done.json'); sys.exit(0)
arm, seed, days, outd = a[a.index('--arm') + 1], a[a.index('--seed') + 1], a[a.index('--days') + 1], Path(a[a.index('--output') + 1])
n = f'{arm}-seed{seed}-{days}d'; d = outd / n; d.mkdir(parents=True, exist_ok=True); (d / 'workspace' / 'swarm').mkdir(parents=True)
(d / 'workspace' / 'swarm' / 'spec.md').write_text('spec'); (d / 'stream.jsonl').write_text('big transcript'); (d / 'steps.jsonl').write_text('{"i": 1}\n')
modes = plan.get(n, ['ok']); i = len(list((outd / 'cutoffs').glob(n + '-*'))) if (outd / 'cutoffs').exists() else 0
mode = modes[min(i, len(modes) - 1)]
if mode == 'ok':
    (d / 'result.json').write_text(json.dumps({'final_balance': 15000, 'completed': True, 'days_operated': 3, 'error': None, 'api_cost_usd': 1.0}))
elif mode == 'pause':
    sd = Path(os.environ['FAKE_STATEDIR']); sd.mkdir(parents=True, exist_ok=True); (sd / 'state.json').write_text('{"day": 2}')
    (d / 'resume.json').write_text(json.dumps({'statedir': str(sd), 'cfg': str(d), 'phase': 'run', 'session_id': 'S',
        'cutoffs': [{'day': 2, 'time': float(os.environ['FAKE_CUT_AT']), 'phase': 'run',
                     'message': "You've hit your 5-hour limit · resets 7:20pm (America/Chicago)"}], 'results': [], 'elapsed': 1}))
elif mode == 'timeout':
    (d / 'result.json').write_text(json.dumps({'final_balance': 0, 'completed': False, 'days_operated': 1, 'error': 'Wall-clock timeout'}))
elif mode == 'crash':
    pass   # the process went away: no result, no resume record
''')
# 2026-11-28 23:00 UTC = 17:00 in Chicago: the window resets at 19:20 Chicago = 01:20 UTC on 29 Nov
cut_at = 1795906800.0
plan.write_text(json.dumps({'obm_v5-seed1-3d': ['pause'], 'obm_v4-seed2-3d': ['crash', 'ok'], 'obm_v5-seed2-3d': ['timeout', 'ok']}))
env = {**os.environ, 'SEED_BATCH_RUNS': str(runs), 'SEED_BATCH_OUT': str(out), 'SEED_BATCH_RUNNER': str(fake), 'SEED_BATCH_DAYS': '3',
       'SEED_BATCH_ORDER': 'obm_v4:1,obm_v5:1,obm_v4:2,obm_v5:2', 'FAKE_PLAN': str(plan), 'FAKE_STATEDIR': str(tmp / 'state'),
       'FAKE_CUT_AT': str(cut_at)}

def tick(at=None):
    e = dict(env, SEED_BATCH_NOW=str(at)) if at else env
    r = json.loads(subprocess.run([sys.executable, '-I', str(HERE / 'seed_batch.py'), 'tick'], env=e, capture_output=True, text=True, check=True).stdout)
    if r.get('pid'):  # wait for the detached fake run to finish, as the session's background watch would
        for _ in range(100):
            try:
                os.kill(r['pid'], 0); os.waitpid(r['pid'], os.WNOHANG); time.sleep(0.05)
            except (OSError, ChildProcessError):
                break
        time.sleep(0.2)
    return r

H = 3600; W = 5 * H + 120                      # a window, and the margin the driver adds
t = cut_at - 6 * H
r = tick(t); assert r['action'] == 'started' and r['started'] == 'obm_v4-seed1-3d', r
r = tick(t + 60); assert r['filed'][0]['run'] == 'obm_v4-seed1-3d' and r['action'] == 'waiting', r   # next run waits for the refresh
assert r['run'] == 'obm_v5-seed1-3d' and r['resume_after'] == t + W and 'refreshes' in r['why'], r
assert json.loads((tmp / 'window.json').read_text())['next_reset'] == t + W
assert (out / 'obm_v4-seed1-3d' / 'result.json').exists() and (out / 'obm_v4-seed1-3d' / 'workspace' / 'swarm' / 'spec.md').exists()
assert not (out / 'obm_v4-seed1-3d' / 'stream.jsonl').exists()                                                   # the transcript stays behind
import gzip
assert gzip.open(out / 'obm_v4-seed1-3d' / 'steps.jsonl.gz').read() == b'{"i": 1}\n'                       # the step log, compressed
r = tick(t + W + 60); assert r['action'] == 'started' and r['started'] == 'obm_v5-seed1-3d', r             # alternates arms, at the refresh
r = tick(cut_at + 60)
assert r['action'] == 'waiting' and r['run'] == 'obm_v5-seed1-3d' and r['resume_after_utc'] == '2026-11-29 01:22 UTC', r  # the account's limit blocks the batch
assert json.loads((tmp / 'window.json').read_text())['next_reset'] == r['resume_after']                     # the CLI's reset replaces the estimate
t = cut_at + 3 * H
r = tick(t); assert r['action'] == 'resumed' and r['started'] == 'obm_v5-seed1-3d' and r['resume'], r
r = tick(t + 60); assert r['filed'][0]['run'] == 'obm_v5-seed1-3d' and r['action'] == 'waiting' and r['resume_after'] == t + W, r
t += W + 60
r = tick(t); assert r['started'] == 'obm_v4-seed2-3d', r
r = tick(t + 60); assert r['failures'][0]['run'] == 'obm_v4-seed2-3d' and r['action'] == 'waiting', r      # a crash: logged; the rerun waits too
t += W + 60
r = tick(t); assert r['started'] == 'obm_v4-seed2-3d', r
r = tick(t + W + 60); assert r['filed'][0]['run'] == 'obm_v4-seed2-3d' and r['started'] == 'obm_v5-seed2-3d', r  # a run past the refresh starts at once
t += W + 60
r = tick(t + W + 60); assert r['failures'][0]['why'] == 'Wall-clock timeout' and r['started'] == 'obm_v5-seed2-3d', r    # the harness clock: run again
t += W + 60
r = tick(t + W + 60); assert r['filed'][0]['run'] == 'obm_v5-seed2-3d' and r['action'] == 'complete', r
fails = json.loads((out / 'environment-failures.json').read_text())
assert [f['run'] for f in fails] == ['obm_v4-seed2-3d', 'obm_v5-seed2-3d'], fails
st = [json.loads(l) for l in subprocess.run([sys.executable, '-I', str(HERE / 'seed_batch.py'), 'status'], env=env, capture_output=True,
                                            text=True, check=True).stdout.splitlines()]
assert [s['state'] for s in st] == ['done'] * 4 and st[1]['resumes'] == 1, st
print('all seed batch tests passed')
