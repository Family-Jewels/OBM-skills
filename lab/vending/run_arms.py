"""Four-arm runs on Prosus Vending Bench, built on its scripts/run_models.py.

Identical to the stock runner (MCP business tools only, same briefing, same budget and timeout) except:
  B (protocols): the operator protocol is appended to the system prompt.
  C (enforcement): a Stop hook that refuses to end the session before the simulation is over.
  D: both.
usage: python -I run_arms.py --arms A B C D --seeds 1 2 3 --days 30 --budget 5 --timeout 1800 --output DIR [--workers N]
"""
import argparse, json, os, socket, subprocess, sys, tempfile, time, urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
ROOT = Path('/home/claude/bench-src/vending-bench'); SIM = ROOT / 'tasks/vending-bench/environment/sim-server'
HERE = Path('/home/claude/obm-lab/vending'); PY = '/home/claude/vb-venv/bin/python'
sys.path.insert(0, str(SIM)); sys.path.insert(0, str(ROOT / 'scripts'))
from vending import config
import sync_config
ARMS = {'A': (False, False), 'B': (True, False), 'C': (False, True), 'D': (True, True)}
CLEAN = {k: v for k, v in os.environ.items() if k not in ('CLAUDE_CODE_SYNC_SKILLS', 'CLAUDE_CODE_SYNC_PLUGINS', 'CLAUDE_CODE_ENABLE_CFC')}
CLEAN['CLAUDE_CONFIG_DIR'] = '/home/claude/obm-lab/cfg-clean'

def run(arm, seed, a):
    protocol, gate = ARMS[arm]
    out = a.output / f'{arm}-seed{seed}-{a.days}d'; out.mkdir(parents=True, exist_ok=False)
    env = {k: v for k, v in CLEAN.items() if not k.startswith('VENDING_')}
    with tempfile.TemporaryDirectory(prefix='vb-') as tmp:
        temp = Path(tmp)
        with socket.socket() as s: s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]
        env.update(VENDING_SEED=str(seed), VENDING_SIM_DAYS=str(a.days), VENDING_STATE_PATH=str(temp / 'state.json'),
                   VENDING_RESUME='0', VENDING_PORT=str(port), VENDING_HOST='127.0.0.1')
        prompt = subprocess.run([PY, '-I', '-c', 'import sys;sys.path[:0]=[sys.argv[1],sys.argv[2]];from vending import config;'
                                 'import sync_config;config.reload();print(sync_config.render(),end="")', str(SIM), str(ROOT / 'scripts')],
                                env=env, capture_output=True, text=True, check=True).stdout
        (out / 'instruction.md').write_text(prompt)
        log = (out / 'server.log').open('w')
        server = subprocess.Popen([PY, str(SIM / 'server.py')], env=env, stdout=log, stderr=subprocess.STDOUT, cwd=str(SIM))
        t0 = time.monotonic(); result, error = {}, None
        try:
            for _ in range(200):
                try: urllib.request.urlopen(f'http://127.0.0.1:{port}/healthz', timeout=1).close(); break
                except Exception:
                    if server.poll() is not None: raise RuntimeError('sim failed to start')
                    time.sleep(.1)
            mcp = {'mcpServers': {'vending': {'type': 'http', 'url': f'http://127.0.0.1:{port}/mcp'}}}
            cmd = ['claude', '-p', 'Operate the business until the simulation ends.', '--model', a.model, '--output-format', 'stream-json',
                   '--verbose', '--restricted', '--tools', '', '--strict-mcp-config', '--mcp-config', json.dumps(mcp),
                   '--allowedTools', 'mcp__vending', '--system-prompt', prompt, '--max-budget-usd', str(a.budget), '--no-session-persistence']
            if protocol: cmd += ['--append-system-prompt', (HERE / 'operator_protocol.md').read_text()]
            if gate:
                settings = {'hooks': {'Stop': [{'hooks': [{'type': 'command', 'command': f'python3 -I {HERE / "vb_stop_gate.py"}', 'timeout': 30}]}]}}
                cmd += ['--settings', json.dumps(settings)]
                env.update(VB_STATE=str(temp / 'state.json'), VB_GATE_LOG=str(out / 'gate.jsonl'), VB_DAYS=str(a.days), VB_GATE_CAP='40')
            (out / 'harness.json').write_text(json.dumps({'arm': arm, 'protocol': protocol, 'stop_gate': gate, 'model': a.model,
                                                          'budget_usd': a.budget, 'timeout_s': a.timeout, 'cmd_flags': [c for c in cmd if not c.startswith(('{', 'You operate', '# Operating'))]}, indent=1))
            with (out / 'stream.jsonl').open('w') as so:
                proc = subprocess.run(cmd, cwd=temp, env=env, stdout=so, stderr=subprocess.PIPE, text=True, timeout=a.timeout)
            (out / 'stderr.txt').write_text(proc.stderr)
            for line in (out / 'stream.jsonl').read_text().splitlines():
                try:
                    d = json.loads(line)
                    if d.get('type') == 'result': result = d
                except ValueError: pass
            if proc.returncode: error = f'CLI exit {proc.returncode}'
        except subprocess.TimeoutExpired: error = 'Wall-clock timeout'
        except Exception as e: error = str(e)
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
            except subprocess.TimeoutExpired: server.kill(); server.wait()
            log.close()
    rec = {**{k: v for k, v in score.items() if not isinstance(v, (dict, list))}, 'arm': arm, 'seed': seed, 'days': a.days,
           'api_cost_usd': result.get('total_cost_usd'), 'turns': result.get('num_turns'), 'subtype': result.get('subtype'),
           'runtime_seconds': round(elapsed, 1), 'error': error,
           'gate_refusals': sum(1 for l in (out / 'gate.jsonl').read_text().splitlines() if '"allow": false' in l) if (out / 'gate.jsonl').exists() else None}
    (out / 'result.json').write_text(json.dumps(rec, indent=1)); print(json.dumps(rec), flush=True); return rec

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--arms', nargs='+', default=list(ARMS)); ap.add_argument('--seeds', type=int, nargs='+', default=[1, 2, 3])
    ap.add_argument('--days', type=int, default=30); ap.add_argument('--budget', type=float, default=5)
    ap.add_argument('--timeout', type=int, default=1800); ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--workers', type=int, default=4); ap.add_argument('--model', default='claude-haiku-5-5')
    a = ap.parse_args()
    jobs = [(arm, s) for s in a.seeds for arm in a.arms]
    with ThreadPoolExecutor(a.workers) as ex: recs = list(ex.map(lambda j: run(j[0], j[1], a), jobs))
    (a.output / 'summary.json').write_text(json.dumps(recs, indent=1))
