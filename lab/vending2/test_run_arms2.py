"""Dry run of every arm's launch, with no simulator, no model and no spend. Run: python3 -I test_run_arms2.py

The real runner is imported and its main() runs for each arm. Only the simulator (briefing render, server, health
check, final score) and the Claude CLI are faked. The preflight runs for real, including the import check on engine v4,
and the step hook is executed exactly as the command written into the arm's settings, so a wrong path or quoting
would fail here rather than in a year-long run.
"""
import contextlib, io, json, shutil, subprocess, sys, tempfile, types, urllib.request
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))
import run_arms2 as R

tmp = Path(tempfile.mkdtemp())
(tmp / 'cfg-clean').mkdir()
R.HERE, R.SKILLS, R.CFG_CLEAN, R.PY = HERE, REPO / 'skills', tmp / 'cfg-clean', sys.executable
real_run = subprocess.run

def fake_run(cmd, *a, **k):  # only the benchmark's briefing render is faked; everything else really runs
    if isinstance(cmd, list) and any('sync_config' in str(x) for x in cmd):
        return types.SimpleNamespace(stdout='BRIEFING', returncode=0, stderr='')
    return real_run(cmd, *a, **k)

class FakeServer:
    def __init__(self, *a, **k): pass
    def poll(self): return None
    def terminate(self): pass
    def wait(self, timeout=None): return 0
    def kill(self): pass

class FakeResp(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): self.close()

def fake_urlopen(req, timeout=None):
    if isinstance(req, str):  # the health check
        return FakeResp(b'ok')
    state = {'sales_log': [{'day': d, 'revenue': 10.0, 'per_slot': [1, 2, 3]} for d in range(1, 92)]}
    return FakeResp(json.dumps({'state': state, 'score': {'final_balance': 1600.0, 'reward': 0.0, 'completed': True, 'days_operated': 91}}).encode())

R.subprocess = types.SimpleNamespace(run=fake_run, Popen=FakeServer, PIPE=subprocess.PIPE, STDOUT=subprocess.STDOUT,
                                     DEVNULL=subprocess.DEVNULL, TimeoutExpired=subprocess.TimeoutExpired)
R.urllib = types.SimpleNamespace(request=types.SimpleNamespace(urlopen=fake_urlopen, Request=urllib.request.Request))

calls = []
def fake_claude(args, cfg, cwd, out_stream, timeout):
    rec = {'args': args, 'timeout': timeout, 'skills': sorted(p.name for p in (Path(cfg) / 'skills').glob('*'))}
    if '--settings' in args:
        st = json.loads(args[args.index('--settings') + 1]); rec['settings'] = st
        for h in st['hooks'].get('PostToolUse', []):
            cmd = h['hooks'][0]['command']
            if h['matcher'] == '.*':  # run the step hook as Claude Code would: twice, on an unchanged file
                f = Path(cwd) / 'probe.md'; f.write_text('unchanged')
                ev = json.dumps({'hook_event_name': 'PostToolUse', 'tool_name': 'Read', 'tool_input': {'file_path': str(f)}, 'tool_response': {}})
                rec['steps_out'] = [real_run(cmd, shell=True, input=ev, capture_output=True, text=True) for _ in range(2)]
            if 'engine.py' in cmd:
                rec['cadence'] = json.loads(Path(cmd.split()[-1]).read_text())
    calls.append(rec)
    return types.SimpleNamespace(returncode=0, stderr=''), {'total_cost_usd': 0.25, 'session_id': 'S-1', 'result': 'ok', 'num_turns': 3}
R.claude = fake_claude

def launch(arm, *extra):
    calls.clear()
    sys.argv = ['run_arms2.py', '--arm', arm, '--seed', '6', '--days', '91', '--output', str(tmp / 'runs'), *extra]
    with contextlib.redirect_stdout(io.StringIO()):
        R.main()
    out = tmp / 'runs' / f'{arm}-seed6-91d'
    res = json.loads((out / 'result.json').read_text())
    shutil.rmtree(out)  # the next launch of the same arm needs the folder free
    return list(calls), res

def flags(c):
    return c['args']

ORCH, LONG = 'obm-swarm-orchestrator', 'obm-long-run'
ROLES = {'obm-swarm-auditor', 'obm-swarm-checker', 'obm-swarm-controls', 'obm-swarm-designer', 'obm-swarm-diagnostician',
         'obm-swarm-organizer', 'obm-swarm-protocol', 'obm-swarm-strategist'}

# base: no dollar cap, the step record only (observation: no cue ever reaches the agent)
cs, res = launch('base')
assert len(cs) == 1 and '--max-budget-usd' not in flags(cs[0]) and cs[0]['skills'] == []
assert list(cs[0]['settings']['hooks']) == ['PostToolUse'] and len(cs[0]['settings']['hooks']['PostToolUse']) == 1
assert [p.returncode for p in cs[0]['steps_out']] == [0, 0] and [json.loads(p.stdout) for p in cs[0]['steps_out']] == [{}, {}]
assert res['budget_usd'] is None and res['steps_mode'] == 'observe' and res['steps']['steps'] == 2 and res['steps']['unchanged_rereads'] == 1
assert cs[0]['timeout'] == 21600

# native: no cap on the planning session or on /goal
cs, res = launch('native')
assert len(cs) == 2 and '--max-budget-usd' not in flags(cs[0]) and 'plan' in flags(cs[0])
assert '--max-budget-usd' not in flags(cs[1]) and '--resume' in flags(cs[1])

# native_cadence: the system's reviews with plain prompts, no stop gate
cs, res = launch('native_cadence')
st = cs[1]['settings']['hooks']
assert 'Stop' not in st and cs[1]['cadence']['prompts'] == 'plain'
assert [h['matcher'] for h in st['PostToolUse']] == ['mcp__vending__wait_for_next_day', '.*']

# obm_enf: every role skill and the orchestrator; the stop gate
cs, res = launch('obm_enf')
assert set(cs[0]['skills']) == ROLES | {ORCH} and LONG not in cs[0]['skills'] and 'Stop' in cs[0]['settings']['hooks']

# obm_v4: design, then the operator, neither capped; engine v4 with the fact register and no review caps; steps observed
cs, res = launch('obm_v4')
d, run = cs
assert '--max-budget-usd' not in flags(d) and '--settings' not in flags(d)
assert '--max-budget-usd' not in flags(run) and 'obm-swarm-orchestrator' in flags(run)[1]
h = run['settings']['hooks']
assert 'Stop' in h and [x['matcher'] for x in h['PostToolUse']] == ['mcp__vending__wait_for_next_day', 'mcp__vending__.*', '.*']
assert h['PreToolUse'][0]['matcher'] == 'mcp__vending__wait_for_next_day'
assert run['cadence']['version'] == 4 and run['cadence']['action_log'].endswith('actions.jsonl')
assert run['cadence']['job_caps'] is False and run['cadence']['budgets'] == {}
assert {m['name'] for m in run['cadence']['charts']['measures']} >= {'slots_selling', 'revenue', 'cash_gain_7', 'cash', 'unit_cost_paid_30d'}
assert set(run['skills']) == ROLES | {ORCH} and [json.loads(p.stdout) for p in run['steps_out']] == [{}, {}]
for x in h['PostToolUse'] + h['PreToolUse'] + h['Stop']:     # every hook command points at a file that exists
    script = next(t for t in x['hooks'][0]['command'].split() if t.endswith('.py'))
    assert Path(script).exists(), script

# obm_v5: the operator on obm-long-run (the orchestrator's skill left out), step cues on
cs, res = launch('obm_v5')
d, run = cs
assert set(run['skills']) == ROLES | {LONG}, run['skills']
assert 'obm-long-run' in flags(run)[1] and 'obm-swarm-orchestrator' not in flags(run)[1] and '--max-budget-usd' not in flags(run)
assert run['cadence']['version'] == 4 and res['steps_mode'] == 'cue'
outs = [json.loads(p.stdout) for p in run['steps_out']]
assert outs[0] == {} and 'has not changed' in outs[1]['hookSpecificOutput']['additionalContext']   # the cue reaches the agent

# a dollar cap only when asked for: what the designer spent comes off it
cs, res = launch('obm_v4', '--budget', '40')
assert flags(cs[0])[flags(cs[0]).index('--max-budget-usd') + 1] == '40.00'
assert flags(cs[1])[flags(cs[1]).index('--max-budget-usd') + 1] == '39.75' and res['budget_usd'] == 40.0

# a usage-limit cutoff pauses the run (nothing scored, state kept); --resume continues the operator's own session
limit_once = {'hit': False}
def claude_with_limit(args, cfg, cwd, out_stream, timeout):
    p, r = fake_claude(args, cfg, cwd, out_stream, timeout)
    st = calls[-1].get('settings', {}).get('hooks', {}).get('Stop')
    if st and '--resume' not in args and not limit_once['hit']:  # the operator's first session: the simulator has reached day 120
        state = Path(next(t for t in st[0]['hooks'][0]['command'].split() if t.endswith('state.json')))
        state.write_text(json.dumps({'day': 120}))
        limit_once['hit'] = True
        return p, {**r, 'session_id': 'S-op', 'result': "You've hit your 5-hour limit · resets 7:20pm"}
    return p, r
R.claude = claude_with_limit
calls.clear()
sys.argv = ['run_arms2.py', '--arm', 'obm_v5', '--seed', '6', '--days', '91', '--output', str(tmp / 'runs-pause')]
with contextlib.redirect_stdout(io.StringIO()):
    R.main()
out = tmp / 'runs-pause' / 'obm_v5-seed6-91d'
rs = json.loads((out / 'resume.json').read_text())
assert not (out / 'result.json').exists() and rs['phase'] == 'run' and rs['session_id'] == 'S-op' and rs['cutoffs'][0]['day'] == 120
assert Path(rs['statedir'], 'state.json').exists() and Path(rs['cfg']).exists() and rs['args']['arm'] == 'obm_v5'
calls.clear()
sys.argv = ['run_arms2.py', '--resume', str(out)]
with contextlib.redirect_stdout(io.StringIO()):
    R.main()
assert len(calls) == 1 and flags(calls[0])[flags(calls[0]).index('--resume') + 1] == 'S-op', flags(calls[0])[:6]
assert 'resumed exactly where it stopped (simulated day 120)' in flags(calls[0])[1]
assert '--settings' in flags(calls[0]) and 'Stop' in calls[0]['settings']['hooks']   # the same hooks as before the pause
res = json.loads((out / 'result.json').read_text())
assert res['resumes'] == 1 and res['cutoffs'][0]['day'] == 120 and res['error'] is None and res['arm'] == 'obm_v5'
assert (out / 'resume.done.json').exists() and not (out / 'resume.json').exists() and not Path(rs['statedir']).exists()
R.claude = fake_claude

# the nested agents' environment is a whitelist: the network and model access pass, nothing that names a hosting session
import os
saved = dict(os.environ)
os.environ.update({'HTTPS_PROXY': 'http://127.0.0.1:1', 'ANTHROPIC_BASE_URL': 'https://api.example', 'CLAUDE_CODE_SESSION_ID': 'x',
                   'CLAUDE_CODE_MESSAGING_TOKEN': 'x', 'CLAUDE_ADDITIONAL_DIRECTORIES': '/home/user/OBM-skills', 'VENDING_SEED': '9'})
e = R.clean_env()
assert e['HTTPS_PROXY'] and e['ANTHROPIC_BASE_URL'] and not {'CLAUDE_CODE_SESSION_ID', 'CLAUDE_CODE_MESSAGING_TOKEN',
                                                              'CLAUDE_ADDITIONAL_DIRECTORIES', 'VENDING_SEED'} & set(e)
os.environ.clear(); os.environ.update(saved)

# the preflight refuses to start when the lab copy lacks what the arm needs, before anything is created
broken = tmp / 'lab-without-longrun'; shutil.copytree(HERE.parent, broken, ignore=shutil.ignore_patterns('longrun', '__pycache__'))
R.HERE = broken / 'vending2'
sys.argv = ['run_arms2.py', '--arm', 'obm_v5', '--output', str(tmp / 'runs-broken')]
err = io.StringIO()
try:
    with contextlib.redirect_stderr(err):
        R.main()
    raise AssertionError('preflight should have refused')
except SystemExit as e:
    assert e.code == 2 and 'verify.py' in err.getvalue() and 'steps_hook.py' in err.getvalue(), err.getvalue()
assert not (tmp / 'runs-broken').exists()
R.HERE = HERE
R.SKILLS = tmp / 'no-skills'; (tmp / 'no-skills').mkdir()
sys.argv = ['run_arms2.py', '--arm', 'obm_v5', '--output', str(tmp / 'runs-broken')]
try:
    with contextlib.redirect_stderr(io.StringIO()):
        R.main()
    raise AssertionError('preflight should have refused')
except SystemExit as e:
    assert e.code == 2
print('all runner dry-run tests passed')
