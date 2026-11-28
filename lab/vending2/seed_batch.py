"""The v4/v5 seed batch (results/2026-11-28-vending-v4-v5/PLAN.md): what runs next, start it detached, file what finished.

Order, alternating arms by seed: obm_v4 s1, obm_v5 s1, obm_v4 s2, ... obm_v5 s5, 365 days each, one run at a time.
Each run is in one of these states:
  done      its result.json is filed in the batch folder
  finished  its result.json is in the run folder, not yet filed
  paused    the usage limit stopped it; resume.json holds what is needed to continue it from where it stopped
  running   the lock names a live process
  pending   none of the above
A paused run blocks the batch until the reset time the CLI named: the limit is the account's, so any other run would be cut
off at once. A run that ended for another environment reason (the harness clock, a crash, a container that went away) is
moved to <runs>/cutoffs/, logged in the batch's environment-failures.json, and run again from the start. A run the agent
itself ended early is a result like any other and is filed: that is what the stop gate exists to prevent, not to hide.

usage: python3 -I seed_batch.py status | tick [--dry]
  tick: file whatever finished; then, if nothing is running or waiting, resume the first paused run or start the first
        pending one, detached from this shell. Prints one JSON line saying what it did and what to wait for.
Environment overrides (tests): SEED_BATCH_RUNS, SEED_BATCH_OUT, SEED_BATCH_RUNNER, SEED_BATCH_ORDER ("arm:seed,..."),
SEED_BATCH_DAYS, SEED_BATCH_NOW (epoch seconds).
"""
import datetime as dt, gzip, json, os, re, shutil, subprocess, sys, time
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent if (HERE.parent.parent / 'results').exists() else Path('/home/user/OBM-skills')
RUNS = Path(os.environ.get('SEED_BATCH_RUNS', '/home/claude/runs/seeds'))
BATCH = Path(os.environ.get('SEED_BATCH_OUT', str(REPO / 'results' / '2026-11-28-vending-v4-v5')))
RUNNER = os.environ.get('SEED_BATCH_RUNNER', '/home/claude/obm-lab/vending2/run_arms2.py')
DAYS = int(os.environ.get('SEED_BATCH_DAYS', '365'))
ORDER = ([(x.split(':')[0], int(x.split(':')[1])) for x in os.environ['SEED_BATCH_ORDER'].split(',')]
         if os.environ.get('SEED_BATCH_ORDER') else [(arm, s) for s in range(1, 6) for arm in ('obm_v4', 'obm_v5')])
LOCK = RUNS / 'batch.lock'
GZIP = ('steps.jsonl', 'actions.jsonl')
KEEP = ('result.json', 'cadence.jsonl', 'steps.jsonl', 'actions.jsonl', 'gate.jsonl', 'resume.done.json', 'runner.log', 'workspace')

def now():
    return float(os.environ.get('SEED_BATCH_NOW') or time.time())

def name(arm, seed):
    return f'{arm}-seed{seed}-{DAYS}d'

def alive(pid):
    """A detached run is re-parented when this process exits; if nothing reaps it, a finished run stays a zombie, which
    os.kill(pid, 0) still reports as alive. So a zombie counts as finished."""
    try:
        os.kill(pid, 0)
    except (OSError, TypeError):
        return False
    try:
        return Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()[0] != 'Z'
    except (OSError, IndexError):
        return True

def lock():
    if LOCK.exists():
        try:
            lk = json.loads(LOCK.read_text())
        except ValueError:
            return None
        return lk if alive(lk.get('pid')) else None
    return None

def env_failure(res):
    """True when the run ended for a reason that is the environment's, not the agent's."""
    err = str(res.get('error') or '')
    return bool(err) and not err.startswith('environment: usage limit')  # a usage limit pauses; it never reaches here

def reset_time(cutoff):
    """When the account's usage window resets, from the CLI's message ('resets 7:20pm (America/Chicago)'); else 5 hours on."""
    t0 = cutoff.get('time') or now()
    m = re.search(r'resets\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)\s*\(([^)]+)\)', cutoff.get('message') or '', re.I)
    if m:
        try:
            tz = ZoneInfo(m.group(4).strip())
            h = int(m.group(1)) % 12 + (12 if m.group(3).lower() == 'pm' else 0); mi = int(m.group(2) or 0)
            base = dt.datetime.fromtimestamp(t0, tz)
            r = base.replace(hour=h, minute=mi, second=0, microsecond=0)
            if r.timestamp() <= t0:
                r += dt.timedelta(days=1)
            return r.timestamp() + 120  # a two-minute margin
        except Exception:
            pass
    return t0 + 5 * 3600

def state(arm, seed):
    n = name(arm, seed); d = RUNS / n
    if (BATCH / n / 'result.json').exists():
        return 'done', {}
    lk = lock()
    if lk and lk.get('name') == n:
        return 'running', lk
    if (d / 'result.json').exists():
        return 'finished', {}
    if (d / 'resume.json').exists():
        rs = json.loads((d / 'resume.json').read_text())
        if not Path(rs.get('statedir', '/nonexistent'), 'state.json').exists():
            return 'lost', {'why': 'paused, but its simulator state is gone (a new container)'}
        return 'paused', {'resume_after': reset_time(rs['cutoffs'][-1]), 'day': rs['cutoffs'][-1].get('day')}
    if d.exists():
        return 'lost', {'why': 'no result and no resume record: the process or its container went away'}
    return 'pending', {}

def file_run(n, failure=None):
    """Copy what the analysis needs into the batch folder (the transcript and the simulator log stay behind)."""
    src = RUNS / n
    dst = (BATCH / 'environment-failures' / f'{n}-{int(now())}') if failure else BATCH / n
    dst.mkdir(parents=True, exist_ok=True)
    for k in KEEP:
        p = src / k
        if p.is_dir():
            shutil.copytree(p, dst / k, dirs_exist_ok=True)
        elif p.exists() and k in GZIP:  # a year's step and action logs run to megabytes
            with open(p, 'rb') as fi, gzip.open(dst / (k + '.gz'), 'wb') as fo:
                shutil.copyfileobj(fi, fo)
        elif p.exists():
            shutil.copy2(p, dst / k)
    if failure:
        reg = BATCH / 'environment-failures.json'
        rows = json.loads(reg.read_text()) if reg.exists() else []
        rows.append({'run': n, 'why': failure, 'filed_at': now()})
        reg.write_text(json.dumps(rows, indent=1))
        (RUNS / 'cutoffs').mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(RUNS / 'cutoffs' / f'{n}-{int(now())}'))
    return dst

def launch(arm, seed, resume=False, dry=False):
    n = name(arm, seed)
    cmd = [sys.executable, '-I', RUNNER] + (['--resume', str(RUNS / n)] if resume else
                                           ['--arm', arm, '--seed', str(seed), '--days', str(DAYS), '--output', str(RUNS)])
    if dry:
        return {'would_run': cmd}
    RUNS.mkdir(parents=True, exist_ok=True)
    logf = open(RUNS / f'{n}.runner.log', 'a')
    p = subprocess.Popen(cmd, stdout=logf, stderr=subprocess.STDOUT, start_new_session=True, cwd=str(Path(RUNNER).parent))
    LOCK.write_text(json.dumps({'pid': p.pid, 'name': n, 'started': now(), 'cmd': cmd}))
    return {'started': n, 'pid': p.pid, 'resume': resume}

def tick(dry=False):
    out = {'filed': [], 'failures': []}
    lk = lock()
    if lk:
        return {**out, 'action': 'running', 'run': lk['name'], 'pid': lk['pid'], 'wait_for': 'the run to finish'}
    if LOCK.exists() and not dry:
        LOCK.unlink()
    for arm, seed in ORDER:  # file whatever finished, move whatever was lost
        st, info = state(arm, seed); n = name(arm, seed)
        if st == 'finished':
            res = json.loads((RUNS / n / 'result.json').read_text())
            log = RUNS / f'{n}.runner.log'
            if log.exists():
                shutil.copy2(log, RUNS / n / 'runner.log')
            if env_failure(res):
                if not dry:
                    file_run(n, failure=res.get('error'))
                out['failures'].append({'run': n, 'why': res.get('error')})
            else:
                if not dry:
                    file_run(n)
                out['filed'].append({'run': n, 'final_balance': res.get('final_balance'), 'completed': res.get('completed'),
                                     'days': res.get('days_operated'), 'cost': res.get('api_cost_usd')})
        elif st == 'lost':
            if not dry:
                file_run(n, failure=info['why'])
            out['failures'].append({'run': n, 'why': info['why']})
    for arm, seed in ORDER:  # a paused run comes first, and blocks the batch until its reset
        st, info = state(arm, seed)
        if st == 'paused':
            if now() < info['resume_after']:
                return {**out, 'action': 'waiting', 'run': name(arm, seed), 'paused_at_day': info['day'],
                        'resume_after': info['resume_after'],
                        'resume_after_utc': dt.datetime.fromtimestamp(info['resume_after'], dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}
            return {**out, 'action': 'resumed', **launch(arm, seed, resume=True, dry=dry)}
    for arm, seed in ORDER:
        if state(arm, seed)[0] == 'pending':
            return {**out, 'action': 'started', **launch(arm, seed, dry=dry)}
    return {**out, 'action': 'complete', 'runs': len(ORDER)}

def status():
    rows = []
    for arm, seed in ORDER:
        st, info = state(arm, seed)
        res = {}
        if st == 'done':
            res = json.loads((BATCH / name(arm, seed) / 'result.json').read_text())
        rows.append({'run': name(arm, seed), 'state': st, **({k: res.get(k) for k in ('final_balance', 'completed', 'days_operated',
                                                                                     'api_cost_usd', 'resumes')} if res else {}),
                     **{k: v for k, v in info.items() if k in ('day', 'resume_after', 'why')}})
    return rows

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'status'
    if cmd == 'tick':
        print(json.dumps(tick(dry='--dry' in sys.argv)))
    else:
        for r in status():
            print(json.dumps(r))
