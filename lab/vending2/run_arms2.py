"""Pilot: OBM skills vs Claude Code native (/plan + /goal) on Prosus Vending Bench.

Every arm: the benchmark's briefing as system prompt, its 22 MCP business tools, and the same extra tools
(Read, Write, Edit, Glob, Grep in a private workspace folder; Agent for sub-agents; Skill). Same model, budget, time limit.
  base     : nothing more.
  native   : a read-only planning session (--permission-mode plan), then the same session resumed with /goal.
  obm      : the six OBM swarm skills installed; told to run the business as a one-agent OBM swarm.
  obm_enf  : obm plus a Stop hook that reads the simulator's own state and refuses to stop before the last day.
usage: python -I run_arms2.py --arm obm_enf --seed 1 --days 365 --budget 40 --timeout 7000 --output DIR
"""
import argparse, json, os, shutil, socket, subprocess, sys, tempfile, time, urllib.request, uuid
from pathlib import Path
ROOT = Path('/home/claude/bench-src/vending-bench'); SIM = ROOT / 'tasks/vending-bench/environment/sim-server'
HERE = Path('/home/claude/obm-lab/vending2'); PY = '/home/claude/vb-venv/bin/python'
SKILLS = Path('/home/claude/obm-skills/skills')
TOOLS = 'Read,Write,Edit,Glob,Grep,Agent,Skill'
GOAL = ("The vending tools have reported SIMULATION OVER for the final simulated day, after the business was operated every day "
        "with the aim of the highest final bank balance. Judge 'met' only when a tool result in the transcript says SIMULATION OVER; "
        "'impossible' only if a tool result says the business was terminated.")
TASK = "Operate the business until the simulation ends."
OBM = ("\n\nRun this business as a one-agent OBM swarm using the installed obm-swarm-* skills. Your workspace folder is the current "
       "directory: keep the swarm's files in swarm/ there. Start with the obm-swarm-designer skill to set up the work system for this "
       "operation, then run it with the obm-swarm-orchestrator skill. Use sub-agents for the checker, auditor and diagnostician roles "
       "when the skills call for them. Keep operating until the simulation ends.")

def clean_env():
    e = {k: v for k, v in os.environ.items() if not k.startswith(('VENDING_', 'VB_', 'GATE_'))
         and k not in ('CLAUDE_CODE_SYNC_SKILLS', 'CLAUDE_CODE_SYNC_PLUGINS', 'CLAUDE_CODE_ENABLE_CFC')}
    return e

def claude(args, cfg, cwd, out_stream, timeout):
    env = clean_env(); env['CLAUDE_CONFIG_DIR'] = str(cfg)
    with out_stream.open('a') as so:
        p = subprocess.run(['claude', *args], cwd=cwd, env=env, stdout=so, stderr=subprocess.PIPE, text=True, timeout=timeout)
    res = {}
    for line in out_stream.read_text().splitlines():
        try:
            d = json.loads(line)
            if d.get('type') == 'result': res = d
        except ValueError: pass
    return p, res

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--arm', required=True, choices=['base', 'native', 'obm', 'obm_enf', 'obm_cadence']); ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--days', type=int, default=365); ap.add_argument('--budget', type=float, default=40)
    ap.add_argument('--timeout', type=int, default=7000); ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--model', default='claude-haiku-5-5'); ap.add_argument('--audit-every', type=int, default=30); ap.add_argument('--pulse-every', type=int, default=7)
    a = ap.parse_args()
    out = a.output / f'{a.arm}-seed{a.seed}-{a.days}d'; out.mkdir(parents=True, exist_ok=False)
    ws = out / 'workspace'; ws.mkdir()
    cfg = out / 'cfg'; shutil.copytree('/home/claude/obm-lab/cfg-clean', cfg, ignore=shutil.ignore_patterns('projects', 'sessions', 'shell-snapshots', 'session-env'))
    if a.arm.startswith('obm'):  # obm, obm_enf, obm_cadence
        (cfg / 'skills').mkdir(exist_ok=True)
        for s in SKILLS.glob('obm-swarm-*'): shutil.copytree(s, cfg / 'skills' / s.name)
    statedir = Path(tempfile.mkdtemp(prefix='vbs-' + uuid.uuid4().hex[:6] + '-', dir='/var/tmp'))
    simenv = clean_env()
    with socket.socket() as s: s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]
    simenv.update(VENDING_SEED=str(a.seed), VENDING_SIM_DAYS=str(a.days), VENDING_STATE_PATH=str(statedir / 'state.json'),
                  VENDING_RESUME='0', VENDING_PORT=str(port), VENDING_HOST='127.0.0.1')
    prompt = subprocess.run([PY, '-I', '-c', 'import sys;sys.path[:0]=[sys.argv[1],sys.argv[2]];from vending import config;'
                             'import sync_config;config.reload();print(sync_config.render(),end="")', str(SIM), str(ROOT / 'scripts')],
                            env=simenv, capture_output=True, text=True, check=True).stdout
    (out / 'instruction.md').write_text(prompt)
    log = (out / 'server.log').open('w')
    server = subprocess.Popen([PY, str(SIM / 'server.py')], env=simenv, stdout=log, stderr=subprocess.STDOUT, cwd=str(SIM))
    t0 = time.monotonic(); results, error = [], None
    stream = out / 'stream.jsonl'
    try:
        for _ in range(200):
            try: urllib.request.urlopen(f'http://127.0.0.1:{port}/healthz', timeout=1).close(); break
            except Exception:
                if server.poll() is not None: raise RuntimeError('sim failed to start')
                time.sleep(.1)
        mcp = json.dumps({'mcpServers': {'vending': {'type': 'http', 'url': f'http://127.0.0.1:{port}/mcp'}}})
        common = ['--model', a.model, '--output-format', 'stream-json', '--verbose', '--tools', TOOLS, '--strict-mcp-config',
                  '--mcp-config', mcp, '--allowedTools', 'mcp__vending', TOOLS, '--system-prompt', prompt]
        if a.arm in ('obm_enf', 'obm_cadence'):
            hook = {'hooks': {'Stop': [{'hooks': [{'type': 'command', 'timeout': 30,
                    'command': f'python3 -I {HERE / "vb_stop_gate2.py"} {statedir / "state.json"} {out / "gate.jsonl"} {a.days} 40'}]}]}}
            if a.arm == 'obm_cadence':
                ccfg = {'workspace': str(ws), 'log': str(out / 'cadence.jsonl'), 'adapter': 'adapters.vending:VendingState',
                        'adapter_args': {'state_path': str(statedir / 'state.json')}, 'unit': 'day', 'horizon': a.days,
                        'pulse_every': a.pulse_every, 'audit_every': a.audit_every, 'model': a.model, 'hook_event': 'PostToolUse',
                        'signals': [{'measure': 'revenue', 'op': '==', 'value': 0, 'periods': 2, 'min_gap': 3, 'not_before': 8, 'label': 'revenue zero two days running'}],
                        'budgets': {'pulse': 0.6, 'audit': 1.5, 'diagnosis': 1.5}}
                (statedir / 'cadence.json').write_text(json.dumps(ccfg))
                hook['hooks']['PostToolUse'] = [{'matcher': 'mcp__vending__wait_for_next_day', 'hooks': [{'type': 'command', 'timeout': 1600,
                    'command': f'python3 -I /home/claude/obm-lab/cadence/engine.py {statedir / "cadence.json"}'}]}]
            common += ['--settings', json.dumps(hook)]
        left = a.budget
        if a.arm == 'obm_cadence':
            design = ("Use the obm-swarm-designer skill to design the work system for operating this business for the whole simulation. "
                      "The system prompt is the business briefing. Write it into swarm/ in the current directory, including the cadence table "
                      "(protocol section 2.2): the system will write ground-truth measures to swarm/metrics_system.md every simulated day, run "
                      f"a short auditor pulse review every {a.pulse_every} simulated days and a full audit every {a.audit_every}, and run the diagnostician when an audit asks for it, handing their "
                      "results to the operator. You cannot use the business tools; design only.")
            p, r = claude(['-p', design, '--permission-mode', 'acceptEdits', '--max-budget-usd', '2', '--model', a.model, '--output-format',
                           'stream-json', '--verbose', '--tools', TOOLS, '--allowedTools', TOOLS, '--strict-mcp-config', '--system-prompt', prompt],
                          cfg, ws, stream, 1200)
            results.append(r); left -= r.get('total_cost_usd') or 0
            run_prompt = (TASK + "\n\nYou are the orchestrator of a one-agent OBM swarm: use the obm-swarm-orchestrator skill, with the work "
                          "system the designer left in swarm/ (read swarm/index.md and swarm/spec.md first). You do the operating yourself. You do "
                          "not need to call the other roles: the system writes ground-truth measures to swarm/metrics_system.md every day, runs "
                          f"a pulse review every {a.pulse_every} simulated days, a full audit every {a.audit_every} and a diagnosis when needed, and hands you their results in the result "
                          "of wait_for_next_day. Act on what it hands you and log what you did. Keep operating until the simulation ends.")
            p, r = claude(['-p', run_prompt, '--permission-mode', 'acceptEdits', '--max-budget-usd', f'{left:.2f}', *common], cfg, ws, stream, a.timeout)
            results.append(r)
        elif a.arm == 'native':
            plan_prompt = (TASK + "\n\nBefore operating, plan. You are in plan mode: read the briefing, look around with the read-only "
                           "tools you have, and write a plan for running the whole simulation well. Do not operate yet.")
            p, r = claude(['-p', plan_prompt, '--permission-mode', 'plan', '--max-budget-usd', f'{min(3, left):.2f}', *common], cfg, ws, stream, 1800)
            results.append(r); left -= r.get('total_cost_usd') or 0
            sid = r.get('session_id')
            p, r = claude(['-p', '/goal ' + GOAL, '--resume', sid, '--permission-mode', 'acceptEdits', '--max-budget-usd', f'{left:.2f}', *common],
                          cfg, ws, stream, a.timeout)
            results.append(r)
        else:
            p, r = claude(['-p', TASK + (OBM if a.arm.startswith('obm') else ''), '--permission-mode', 'acceptEdits',
                           '--max-budget-usd', f'{left:.2f}', *common], cfg, ws, stream, a.timeout)
            results.append(r)
        if p.returncode: error = f'CLI exit {p.returncode}'
        (out / 'stderr.txt').write_text(p.stderr)
        last = str(results[-1].get('result', '')).lower()
        if 'hit your' in last and 'limit' in last: error = 'environment: usage limit reached (not an agent stop)'
    except subprocess.TimeoutExpired: error = 'Wall-clock timeout'
    except Exception as e: error = repr(e)
    finally:
        elapsed = time.monotonic() - t0
        try:
            req = urllib.request.Request(f'http://127.0.0.1:{port}/verifier/finalize', method='POST')
            with urllib.request.urlopen(req, timeout=30) as r: art = json.load(r)
            (out / 'trajectory.json').write_text(json.dumps(art['state'])); score = art['score']
        except Exception as e:
            score = {'reward': 0., 'completed': False}; error = error or f'finalize failed: {e}'
        server.terminate()
        try: server.wait(timeout=10)
        except subprocess.TimeoutExpired: server.kill()
        log.close(); shutil.rmtree(statedir, ignore_errors=True); shutil.rmtree(cfg, ignore_errors=True)
    cadence_events = [json.loads(l) for l in (out / 'cadence.jsonl').read_text().splitlines()] if (out / 'cadence.jsonl').exists() else []
    cadence_cost = sum(e.get('cost') or 0 for e in cadence_events)
    sl = json.loads((out / 'trajectory.json').read_text()).get('sales_log', []) if (out / 'trajectory.json').exists() else []
    q = lambda lo, hi: round(sum(d['revenue'] for d in sl if lo <= d['day'] <= hi), 2)
    rec = {**{k: v for k, v in score.items() if not isinstance(v, (dict, list))}, 'arm': a.arm, 'seed': a.seed, 'days': a.days,
           'api_cost_usd': round(sum(r.get('total_cost_usd') or 0 for r in results) + cadence_cost, 3), 'cadence_cost_usd': round(cadence_cost, 3),
           'audits': sum(1 for e in cadence_events if e.get('event') == 'audit'), 'pulses': sum(1 for e in cadence_events if e.get('event') == 'pulse'), 'diagnoses': sum(1 for e in cadence_events if e.get('event') == 'diagnosis'), 'turns': sum(r.get('num_turns') or 0 for r in results),
           'runtime_seconds': round(elapsed, 1), 'error': error,
           'avg_stocked_slots': round(sum(len(d.get('per_slot', [])) for d in sl) / len(sl), 2) if sl else None,
           'revenue_by_quarter': [q(1, 91), q(92, 182), q(183, 273), q(274, 366)] if a.days >= 300 else None,
           'gate_refusals': sum(1 for l in (out / 'gate.jsonl').read_text().splitlines() if '"allow": false' in l) if (out / 'gate.jsonl').exists() else None,
           'subagents_started': sum(l.count('"name":"Agent"') for l in stream.read_text().splitlines()) if stream.exists() else 0,
           'skills_invoked': sum(l.count('"name":"Skill"') for l in stream.read_text().splitlines()) if stream.exists() else 0,
           'workspace_files': sorted(str(p.relative_to(ws)) for p in ws.rglob('*') if p.is_file())[:50]}
    (out / 'result.json').write_text(json.dumps(rec, indent=1)); print(json.dumps(rec))

if __name__ == '__main__':
    main()
