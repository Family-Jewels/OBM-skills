"""OBM skills vs Claude Code native (/plan + /goal) on Prosus Vending Bench.

Every arm: the benchmark's briefing as system prompt, its 22 MCP business tools, and the same extra tools
(Read, Write, Edit, Glob, Grep in a private workspace folder; Agent for sub-agents; Skill). Same model and time limit.
  base           : nothing more.
  native         : a read-only planning session (--permission-mode plan), then the same session resumed with /goal.
  native_cadence : native, with the system running the same reviews as the obm cadence arms, with plain prompts.
  obm            : the OBM swarm skills installed; told to run the business as a one-agent OBM swarm.
  obm_enf        : obm plus a Stop hook that reads the simulator's own state and refuses to stop before the last day.
  obm_cadence    : the system runs the review cadence (engine v1); obm_v2, obm_v3 and obm_v4 run engines v2 to v4.
  obm_v5         : engine v4 (with change verdicts), the operator on the obm-long-run skill instead of the orchestrator's,
                   and the system's step cues on (--steps cue).
usage: python -I run_arms2.py --arm obm_v5 --seed 1 --days 365 --output DIR [--budget USD] [--timeout S] [--steps observe|cue|off]

--budget: no dollar cap unless given, on any session: the operator, the designer's set-up, native's planning session, and
(engine v4) every review, which also has no turn cap. The account's usage limits still apply, and a cutoff is tagged as
an environment failure. What remains are guards, not caps: the harness clock (--timeout, for a hung run), the engine's
review timeout (it stops waiting for a review that never returns) and the stop gate's 40-attempt honest exit.
Nested agents get a whitelisted environment (clean_env): network, CA and model access only.
--steps (every arm): a hook records every tool call to <out>/steps.jsonl (../longrun/steps_hook.py), so the movement cycle
can be analysed after the run; result.json gets its behaviour summary. 'observe' (the default, except for obm_v5) records
only; 'cue' also hands the agent the system's step cues and writes swarm/step_health.md, so it is an intervention.
Before anything starts, a preflight refuses to run if the lab copy lacks what the arm needs (see preflight()).
"""
import argparse, json, os, shutil, socket, subprocess, sys, tempfile, time, urllib.request, uuid
from pathlib import Path
ROOT = Path('/home/claude/bench-src/vending-bench'); SIM = ROOT / 'tasks/vending-bench/environment/sim-server'
HERE = Path('/home/claude/obm-lab/vending2'); PY = '/home/claude/vb-venv/bin/python'
SKILLS = Path('/home/claude/obm-skills/skills')
CFG_CLEAN = Path('/home/claude/obm-lab/cfg-clean')
CADENCE_ARMS = ('obm_cadence', 'native_cadence', 'obm_v2', 'obm_v3', 'obm_v4', 'obm_v5')
GATED_ARMS = ('obm_enf', 'obm_cadence', 'obm_v2', 'obm_v3', 'obm_v4', 'obm_v5')
V4_ARMS = ('obm_v4', 'obm_v5')  # engine v4: two branches, the fact register, change verdicts
TOOLS = 'Read,Write,Edit,Glob,Grep,Agent,Skill'
GOAL = ("The vending tools have reported SIMULATION OVER for the final simulated day, after the business was operated every day "
        "with the aim of the highest final bank balance. Judge 'met' only when a tool result in the transcript says SIMULATION OVER; "
        "'impossible' only if a tool result says the business was terminated.")
TASK = "Operate the business until the simulation ends."
OBM = ("\n\nRun this business as a one-agent OBM swarm using the installed obm-swarm-* skills. Your workspace folder is the current "
       "directory: keep the swarm's files in swarm/ there. Start with the obm-swarm-designer skill to set up the work system for this "
       "operation, then run it with the obm-swarm-orchestrator skill. Use sub-agents for the checker, auditor and diagnostician roles "
       "when the skills call for them. Keep operating until the simulation ends.")

KEEP_ENV = ('PATH', 'HOME', 'LANG', 'LC_ALL', 'TERM', 'TMPDIR', 'USER', 'SHELL',
            'HTTPS_PROXY', 'https_proxy', 'NO_PROXY', 'no_proxy',  # the network proxy and its CA bundle
            'SSL_CERT_FILE', 'SSL_CERT_DIR', 'NODE_EXTRA_CA_CERTS', 'REQUESTS_CA_BUNDLE', 'CURL_CA_BUNDLE', 'PIP_CERT',
            'ANTHROPIC_BASE_URL', 'ANTHROPIC_API_KEY', 'ANTHROPIC_AUTH_TOKEN', 'CLAUDE_CODE_OAUTH_TOKEN',  # model access
            'CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST', 'CLAUDE_CODE_USE_BEDROCK', 'CLAUDE_CODE_USE_VERTEX')

def clean_env():
    """A whitelist, not a blacklist: only what a run needs to reach the model and the network. Anything else (a hosting
    session's ids, messaging channel or extra directories, the runner's own variables) could tie a benchmark agent to
    the session that launched it, or let it see files outside its workspace."""
    return {k: os.environ[k] for k in KEEP_ENV if k in os.environ}

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

def skills_for(arm):
    """The skill folders an arm installs. obm_v5's operator uses obm-long-run, so the orchestrator's skill is left out:
    both describe running the work, and installing both would leave the choice to the model."""
    if not arm.startswith('obm'):
        return []
    sk = sorted(SKILLS.glob('obm-swarm-*'))
    if arm == 'obm_v5':
        sk = [s for s in sk if s.name != 'obm-swarm-orchestrator'] + [SKILLS / 'obm-long-run']
    return sk

def preflight(a):
    """Everything the arm needs, checked before anything starts. A missing piece would otherwise fail silently: the engine
    runs without change verdicts if it cannot import them, and a hook whose file is missing errors without stopping the run."""
    lab, probs = HERE.parent, []
    need = [CFG_CLEAN]
    if a.steps != 'off':
        need += [lab / 'longrun' / 'steps_hook.py', lab / 'longrun' / 'steps.py']
    if a.arm in GATED_ARMS:
        need.append(HERE / 'vb_stop_gate2.py')
    if a.arm in CADENCE_ARMS:
        need += [lab / 'cadence' / 'engine.py', lab / 'cadence' / 'adapters' / 'vending.py']
    if a.arm in V4_ARMS:
        need += [lab / 'cadence' / 'engine_v4.py', lab / 'cadence' / 'adapters' / 'action_hook.py', lab / 'longrun' / 'verify.py']
    for s in skills_for(a.arm):
        need.append(s / 'SKILL.md')
    if a.arm.startswith('obm'):
        need.append(SKILLS / 'obm-swarm-protocol' / 'SKILL.md')
    probs += [f'missing: {p}' for p in need if not p.exists()]
    if a.arm in V4_ARMS and not probs:
        chk = subprocess.run(['python3', '-I', '-c', 'import sys; sys.path.insert(0, sys.argv[1]); import engine_v4; '
                              'sys.exit(0 if engine_v4.verify is not None else 3)', str(lab / 'cadence')], capture_output=True, text=True)
        if chk.returncode:
            probs.append('engine v4 cannot load change verification (lab/longrun/verify.py): ' + (chk.stderr.strip()[-300:] or f'exit {chk.returncode}'))
    return probs

def cap(usd):
    """The dollar cap flag, only when there is a cap."""
    return [] if usd is None else ['--max-budget-usd', f'{max(0.0, usd):.2f}']

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--arm', choices=['base', 'native', 'native_cadence', 'obm', 'obm_enf', 'obm_cadence', 'obm_v2', 'obm_v3', 'obm_v4', 'obm_v5']); ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--days', type=int, default=365); ap.add_argument('--budget', type=float, default=None)
    ap.add_argument('--timeout', type=int, default=21600); ap.add_argument('--output', type=Path)
    ap.add_argument('--model', default='claude-haiku-5-5'); ap.add_argument('--audit-every', type=int, default=50); ap.add_argument('--pulse-every', type=int, default=5)
    ap.add_argument('--steps', choices=['off', 'observe', 'cue'], default=None)
    ap.add_argument('--resume', type=Path, default=None, help="a run folder paused by a usage limit (it holds resume.json)")
    a = ap.parse_args()
    saved = None
    if a.resume:  # continue a run the usage limit paused: same arm, seed, folders, simulator state and operator session
        saved = json.loads((a.resume / 'resume.json').read_text())
        for k, v in saved['args'].items():
            setattr(a, k, v)
    elif not a.arm or not a.output:
        ap.error('--arm and --output are required (or --resume RUN_FOLDER)')
    if a.steps is None:
        a.steps = 'cue' if a.arm == 'obm_v5' else 'observe'
    probs = preflight(a)
    if probs:
        print('preflight failed; nothing was started:\n  ' + '\n  '.join(probs), file=sys.stderr)
        sys.exit(2)
    if saved:
        out = a.resume; ws = out / 'workspace'; cfg = Path(saved['cfg']); statedir = Path(saved['statedir'])
        missing = [str(p) for p in (ws, cfg, statedir / 'state.json', out / 'instruction.md') if not p.exists()]
        if missing:
            print('cannot resume; missing: ' + ', '.join(missing), file=sys.stderr); sys.exit(2)
    else:
        out = a.output / f'{a.arm}-seed{a.seed}-{a.days}d'; out.mkdir(parents=True, exist_ok=False)
        ws = out / 'workspace'; ws.mkdir()
        cfg = out / 'cfg'; shutil.copytree(CFG_CLEAN, cfg, ignore=shutil.ignore_patterns('projects', 'sessions', 'shell-snapshots', 'session-env'))
        if a.arm.startswith('obm'):
            (cfg / 'skills').mkdir(exist_ok=True)
            for s in skills_for(a.arm): shutil.copytree(s, cfg / 'skills' / s.name)
        statedir = Path(tempfile.mkdtemp(prefix='vbs-' + uuid.uuid4().hex[:6] + '-', dir='/var/tmp'))
    simenv = clean_env()
    with socket.socket() as s: s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]
    simenv.update(VENDING_SEED=str(a.seed), VENDING_SIM_DAYS=str(a.days), VENDING_STATE_PATH=str(statedir / 'state.json'),
                  VENDING_RESUME='1' if saved else '0', VENDING_PORT=str(port), VENDING_HOST='127.0.0.1')
    if saved:
        prompt = (out / 'instruction.md').read_text()
    else:
        prompt = subprocess.run([PY, '-I', '-c', 'import sys;sys.path[:0]=[sys.argv[1],sys.argv[2]];from vending import config;'
                                 'import sync_config;config.reload();print(sync_config.render(),end="")', str(SIM), str(ROOT / 'scripts')],
                                env=simenv, capture_output=True, text=True, check=True).stdout
        (out / 'instruction.md').write_text(prompt)
    log = (out / 'server.log').open('a' if saved else 'w')
    server = subprocess.Popen([PY, str(SIM / 'server.py')], env=simenv, stdout=log, stderr=subprocess.STDOUT, cwd=str(SIM))
    t0 = time.monotonic(); error = None
    results = list(saved['results']) if saved else []
    phase, last_sid = 'start', None  # which session was running, for a resume
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
        steps_hook = None
        if a.steps != 'off':  # the system's record of every tool call: the movement cycle, kept with the results
            steps_cfg = statedir / 'steps.json'
            steps_cfg.write_text(json.dumps({'steps_log': str(out / 'steps.jsonl'), 'workspace_roots': [str(ws)],
                                             'own_logs': ['swarm/log/progress.md'], 'cues': a.steps == 'cue',
                                             'health_md': str((ws / 'swarm' if a.steps == 'cue' else out) / 'step_health.md')}))
            steps_hook = {'matcher': '.*', 'hooks': [{'type': 'command', 'timeout': 20,
                          'command': f'python3 -I {HERE.parent / "longrun" / "steps_hook.py"} {steps_cfg}'}]}
        lab = HERE.parent
        if a.arm in GATED_ARMS or a.arm in CADENCE_ARMS:
            hook = {'hooks': {}} if a.arm not in GATED_ARMS else {'hooks': {'Stop': [{'hooks': [{'type': 'command', 'timeout': 30,
                    'command': f'python3 -I {HERE / "vb_stop_gate2.py"} {statedir / "state.json"} {out / "gate.jsonl"} {a.days} 40'}]}]}}
            if a.arm in CADENCE_ARMS:
                ccfg = {'workspace': str(ws), 'log': str(out / 'cadence.jsonl'), 'adapter': 'adapters.vending:VendingState',
                        'adapter_args': {'state_path': str(statedir / 'state.json')}, 'unit': 'day', 'horizon': a.days,
                        'pulse_every': a.pulse_every, 'audit_every': a.audit_every, 'model': a.model, 'hook_event': 'PostToolUse',
                        'signals': [{'measure': 'revenue', 'op': '==', 'value': 0, 'periods': 2, 'min_gap': 3, 'not_before': 8, 'label': 'revenue zero two days running'}],
                        'budgets': {'pulse': 0.6, 'audit': 1.5, 'diagnosis': 1.0, 'redesign': 1.5}, 'min_periods_between_redesigns': 20,
                        'charts': {'not_before': 8, 'min_points': 8, 'baseline_points': 20, 'measures': [
                            {'name': 'cash_gain_7', 'from': 'cash', 'diff': 7, 'better': 'up'}, {'name': 'revenue', 'better': 'up'},
                            {'name': 'slots_selling', 'better': 'up'}, {'name': 'revenue_per_slot', 'better': 'up'}, {'name': 'units', 'better': 'up'}]},
                        'exemplar': {'measure': 'cash', 'points': {'0': 1500, '30': 3228, '365': 61219}, 'origin': 1500,
                                     'source': "the benchmark's scripted reference operator, which knows the economy's hidden parameters"}}
                if a.arm == 'native_cadence': ccfg['prompts'] = 'plain'  # same cadence, charts and exemplar; reviews without OBM skills
                if a.arm in ('obm_v2', 'obm_v3') + V4_ARMS:  # engine v2 (v3 adds the Strategist; v4 separates the risk and improvement branches)
                    ccfg['version'] = {'obm_v2': 2, 'obm_v3': 3, 'obm_v4': 4, 'obm_v5': 4}[a.arm]
                    ccfg['adapter_args'].update({'horizon': a.days, 'ceiling': 61219, 'ceiling_source': "the benchmark's scripted reference operator",
                                                 'clock_log': str(statedir / 'clock.jsonl')})
                if a.arm in V4_ARMS:  # the system logs every action with the simulator's clock: the fact register and the pursuit measure
                    ccfg['action_log'] = str(out / 'actions.jsonl')
                    ccfg['budgets'] = {}; ccfg['job_caps'] = False  # no dollar or turn cap on any review: the system governs its own cost
                    # the top measure as a level, and what stock costs: both asked for by the reviewers in the first smoke run
                    ccfg['charts']['measures'] = ccfg['charts']['measures'] + [{'name': 'cash', 'better': 'up'},
                                                                             {'name': 'unit_cost_paid_30d', 'better': 'down'}]
                (statedir / 'cadence.json').write_text(json.dumps(ccfg))
                hook['hooks']['PostToolUse'] = [{'matcher': 'mcp__vending__wait_for_next_day', 'hooks': [{'type': 'command', 'timeout': 1600,
                    'command': f'python3 -I {lab / "cadence" / "engine.py"} {statedir / "cadence.json"}'}]}]
                if a.arm in V4_ARMS:
                    hook['hooks']['PostToolUse'].append({'matcher': 'mcp__vending__.*', 'hooks': [{'type': 'command', 'timeout': 20,
                        'command': f'python3 -I {lab / "cadence" / "adapters" / "action_hook.py"} {statedir / "cadence.json"}'}]})
                if a.arm in ('obm_v2', 'obm_v3') + V4_ARMS:  # the worker's capacity, read from the simulator's clock just before each day ends
                    hook['hooks']['PreToolUse'] = [{'matcher': 'mcp__vending__wait_for_next_day', 'hooks': [{'type': 'command', 'timeout': 20,
                        'command': f'python3 -I {lab / "cadence" / "adapters" / "vending_clock_hook.py"} {statedir / "state.json"} {statedir / "clock.jsonl"}'}]}]
            if steps_hook:
                hook['hooks'].setdefault('PostToolUse', []).append(steps_hook)
            common += ['--settings', json.dumps(hook)]
        elif steps_hook:
            common += ['--settings', json.dumps({'hooks': {'PostToolUse': [steps_hook]}})]
        left = a.budget  # None: no dollar cap; the usage limits still apply
        if saved and saved.get('phase') == 'run' and saved.get('session_id'):
            day = (json.loads((statedir / 'state.json').read_text()) or {}).get('day')
            cont = (f"The run was paused by the account's usage limit and has now resumed exactly where it stopped (simulated day "
                    f"{day}). Nothing changed while it was paused. Continue operating until the simulation ends.")
            if a.arm in ('native', 'native_cadence'):
                cont = '/goal ' + GOAL
            phase, last_sid = 'run', saved['session_id']
            p, r = claude(['-p', cont, '--resume', saved['session_id'], '--permission-mode', 'acceptEdits', *cap(left), *common],
                          cfg, ws, stream, a.timeout)
            results.append(r); last_sid = r.get('session_id') or last_sid
        elif a.arm in ('obm_cadence', 'obm_v2', 'obm_v3') + V4_ARMS:
            design = ("Use the obm-swarm-designer skill to design the work system for operating this business for the whole simulation. "
                      "The system prompt is the business briefing. Write it into swarm/ in the current directory: a driver tree from the final balance "
                      "down to the drivers the operator controls, the exemplar, and the cadence table. The system will write ground-truth measures to "
                      f"swarm/metrics_system.md and process behavior charts with limits computed from the data to swarm/charts.md every simulated day, run a short auditor pulse review every {a.pulse_every} simulated days and a full "
                      f"audit every {a.audit_every}, run the diagnostician when a review asks for it, and call you back to redesign from the diagnosis, "
                      "handing every result to the operator. The system's daily measures are: cash, revenue, units, slots_selling, revenue_per_slot, "
                      "revenue_last_7 and revenue_same_7_a_month_earlier; it charts cash_gain_7 (cash gained over 7 days), revenue, slots_selling, "
                      "revenue_per_slot and units. Build the tree on these. Exemplar: the benchmark's scripted reference operator, which knows the "
                      "economy's hidden parameters, reaches about EUR 3,228 at day 30 and EUR 61,219 at day 365 from EUR 1,500. You cannot use the business tools; design only.")
            if a.arm in ('obm_v2', 'obm_v3'):
                design = ("Use the obm-swarm-designer skill to design the work system for operating this business for the whole simulation. "
                          "The system prompt is the business briefing. Write it into swarm/ in the current directory: a driver tree from the final balance "
                          "down to the drivers the operator controls, with a ceiling, its source, a confidence and any guardrail for each driver; the "
                          "resources the work uses; an experiments section; and the cadence table. The system writes ground-truth measures to "
                          "swarm/metrics_system.md and swarm/charts.md every simulated day: level charts with limits computed from the data, celeration "
                          "per measure over 7-day points (derived from the task: demand has a weekly pattern), the top measure's floor line and a "
                          "deliberate overshoot aim, the worker's time (480 minutes a working day; each tool call costs simulated minutes, a slot refill 45), "
                          "slots and capital in use and idle, a cash-reserve guardrail of EUR 120, per-machine measures "
                          "for the six machines (machine_revenue, machine_units, machine_stocked_slots), and daily ground-truth snapshots of every "
                          "slot. Known fixes go into the design for every machine at once. Experiments are only for uncertain levers, as one-time settings "
                          "with a stated capacity cost, starting after the first three weekly points, on a slice of the machines with the others as control: the checker confirms each was made as "
                          "written, the system measures it, and the auditor rules keep, revert or too small to read. It runs a pulse review every point, full audits at each quarter of the year, "
                          "opportunity reviews on its own rules, diagnoses when a review asks, and calls you back to redesign from either, handing "
                          "every result to the operator. The system's daily measures are: cash, revenue, units, slots_selling, revenue_per_slot, "
                          "revenue_last_7, revenue_same_7_a_month_earlier and unit_cost_paid_30d. Exemplar and ceiling: the benchmark's scripted reference operator, which "
                          "knows the economy's hidden parameters, reaches about EUR 3,228 at day 30 and EUR 61,219 at day 365 from EUR 1,500. You cannot use the business tools; design only.")
            if a.arm == 'obm_v3':
                design = ("Use the obm-swarm-designer skill to design the work system for operating this business for the whole simulation. "
                          "The system prompt is the business briefing. Write it into swarm/ in the current directory: a driver tree from the final balance "
                          "down to the drivers the operator controls, with a ceiling, its source and any guardrail for each driver; the resources the "
                          "work uses, starting with the worker's time; a first swarm/aims.md (the constraint, an aim for each priority driver, how the "
                          "worker's time is split); and the cadence table. The system writes ground-truth measures to swarm/metrics_system.md and "
                          "swarm/charts.md every simulated day: level charts with limits computed from the data, celeration per measure over 7-day "
                          "points, the top measure's floor line and a deliberate overshoot aim, the worker's time (480 minutes a working day, read from "
                          "the simulator's clock; each tool call costs simulated minutes, a slot refill 45), slots and capital in use and idle, and a "
                          "cash-reserve guardrail of EUR 120. It runs a pulse review every point, full audits at each quarter of the year, diagnoses when "
                          "a review asks and redesigns from them, and a Strategist (the obm-swarm-strategist skill) after the first three points and "
                          "every three points after; it calls you right after each strategy to update swarm/aims.md, and hands every result to the "
                          "operator. There are no experiments. The system's daily measures are: cash, revenue, units, slots_selling, revenue_per_slot, "
                          "revenue_last_7, revenue_same_7_a_month_earlier and unit_cost_paid_30d. Exemplar and ceiling: the benchmark's scripted reference "
                          "operator, which knows the economy's hidden parameters, reaches about EUR 3,228 at day 30 and EUR 61,219 at day 365 from "
                          "EUR 1,500. You cannot use the business tools; design only.")
            if a.arm in V4_ARMS:
                design = ("Use the obm-swarm-designer skill to design the work system for operating this business for the whole simulation. "
                          "The system prompt is the business briefing. Write it into swarm/ in the current directory: a driver tree from the final balance "
                          "down to the drivers the operator controls, with a ceiling, its source and any guardrail for each driver; the resources the "
                          "work uses, starting with the worker's time; and a first swarm/aims.md (the constraint, an aim for each priority driver, and "
                          "a '## Capacity split' section, one line per share: '- <percent>% <label>: <tool names>', using the business tool names). "
                          "Do not write swarm/controls.md: the risk branch owns it. The system runs two separate branches (protocol section 3) and "
                          "writes ground-truth measures, charts, a Facts table of what each action costs (measured from every tool call) and the "
                          "planned vs actual capacity split every simulated day, and assembles swarm/instructions.md for the operator. The worker's "
                          "time is 480 minutes a working day, read from the simulator's clock. Guardrail: a cash reserve of EUR 120. The system's daily "
                          "measures are: cash, revenue, units, slots_selling, revenue_per_slot, revenue_last_7, revenue_same_7_a_month_earlier and "
                          "unit_cost_paid_30d. Exemplar and ceiling: the benchmark's scripted reference operator, which knows the economy's hidden "
                          "parameters, reaches about EUR 3,228 at day 30 and EUR 61,219 at day 365 from EUR 1,500. You cannot use the business tools; design only.")
            phase = 'design'
            p, r = claude(['-p', design, '--permission-mode', 'acceptEdits', *cap(left), '--model', a.model, '--output-format',
                           'stream-json', '--verbose', '--tools', TOOLS, '--allowedTools', TOOLS, '--strict-mcp-config', '--system-prompt', prompt],
                          cfg, ws, stream, 1200)
            results.append(r); left = None if left is None else left - (r.get('total_cost_usd') or 0)
            run_prompt = (TASK + "\n\nYou are the orchestrator of a one-agent OBM swarm: use the obm-swarm-orchestrator skill, with the work "
                          "system the designer left in swarm/ (read swarm/index.md and swarm/spec.md first). You do the operating yourself. You do "
                          "not need to call the other roles: the system writes ground-truth measures and charts to swarm/metrics_system.md and swarm/charts.md every day, runs "
                          f"a pulse review every {a.pulse_every} simulated days, a full audit every {a.audit_every}, and a diagnosis and redesign by the designer when needed, and hands "
                          "you their results in the result of wait_for_next_day. Act on what it hands you, adopt any redesign, and log what you did. Keep operating until the simulation ends.")
            if a.arm in ('obm_v2', 'obm_v3'):
                run_prompt = (TASK + "\n\nYou are the orchestrator of a one-agent OBM swarm: use the obm-swarm-orchestrator skill, with the work "
                              "system the designer left in swarm/ (read swarm/index.md and swarm/spec.md first). You do the operating yourself. You do "
                              "not need to call the other roles: the system writes ground-truth measures and charts every day, runs pulse reviews, full "
                              "audits, opportunity reviews, diagnoses and redesigns on its own schedule, and hands you their results in the result of "
                              "wait_for_next_day. Act on what it hands you: do the fixes, keep doing what it says works, adopt any redesign, and carry out "
                              "the experiments in swarm/experiments/: make a change only when the system hands it to you with 'starts now', on its slice only, "
                              "write 'Applied: <day>' in its file, and "
                              "apply the auditor's verdict. Never judge an experiment yourself. Log events only, not a line every day. Keep operating until the simulation ends.")
            if a.arm == 'obm_v3':
                run_prompt = (TASK + "\n\nYou are the orchestrator of a one-agent OBM swarm: use the obm-swarm-orchestrator skill, with the work "
                              "system the designer left in swarm/ (read swarm/index.md, swarm/spec.md and swarm/aims.md first). You do the operating "
                              "yourself. You do not need to call the other roles: the system writes ground-truth measures and charts every day, runs "
                              "pulse reviews, full audits, diagnoses, redesigns and the Strategist on its own schedule, and hands you their results, "
                              "including new aims, in the result of wait_for_next_day. Work to the current aims in swarm/aims.md: put your time where "
                              "they say. Act on what the system hands you: do the fixes, keep doing what it says works, adopt any redesign or new aims. "
                              "Log events only, not a line every day. Keep operating until the simulation ends.")
            if a.arm == 'obm_v4':
                run_prompt = (TASK + "\n\nYou are the orchestrator of a one-agent OBM swarm: use the obm-swarm-orchestrator skill, with the work "
                              "system the designer left in swarm/ (read swarm/index.md, swarm/spec.md and swarm/instructions.md first). You do the "
                              "operating yourself. You do not need to call the other roles: the system runs them on its own schedule and hands you "
                              "their results in the result of wait_for_next_day. Work to swarm/instructions.md: stay within its controls, and put your "
                              "time where its aims and capacity split say. Make any corrections handed to you that day. Read the Facts table in "
                              "swarm/charts.md for what each action costs. Log events only, not a line every day. Keep operating until the simulation ends.")
            if a.arm == 'obm_v5':
                run_prompt = (TASK + "\n\nYou are the one agent operating this business: use the obm-long-run skill, with the work system the "
                              "designer left in swarm/ (read swarm/spec.md and swarm/instructions.md first, and swarm/index.md if there is one). The "
                              "system around you records every tool call, writes the measures and charts, runs every review in a fresh context on its "
                              "own schedule, judges each change the designer makes, and hands you its results (SYSTEM CADENCE) and step cues (SYSTEM "
                              "STEP CUES) in the results of your tool calls. You never call a reviewer. Work to swarm/instructions.md: stay within its "
                              "controls and put your time where its aims and capacity split say. Make any corrections handed to you that day. Read "
                              "the Facts table in swarm/charts.md for what each action costs. Log events only, one line each, in swarm/log/progress.md; "
                              "never count or log what the system records. The simulation can always continue, so the only honest end here is "
                              "SIMULATION OVER: keep operating until the simulation ends.")
            phase = 'run'
            p, r = claude(['-p', run_prompt, '--permission-mode', 'acceptEdits', *cap(left), *common], cfg, ws, stream, a.timeout)
            results.append(r); last_sid = r.get('session_id')
        elif a.arm in ('native', 'native_cadence'):
            plan_prompt = (TASK + "\n\nBefore operating, plan. You are in plan mode: read the briefing, look around with the read-only "
                           "tools you have, and write a plan for running the whole simulation well. Do not operate yet.")
            if a.arm == 'native_cadence':
                plan_prompt += ("\n\nWhile you operate, the system will keep your plan in swarm/plan.md in the current folder, write ground-truth "
                                "measures to swarm/metrics_system.md and process behavior charts to swarm/charts.md every simulated day, run a short "
                                f"review every {a.pulse_every} simulated days and a full review every {a.audit_every}, find out what is going wrong "
                                "when a review asks for it and revise swarm/plan.md from that, and hand you every result in the result of "
                                "wait_for_next_day. Act on what it hands you and follow the current swarm/plan.md. The best known result on this "
                                "simulation is about EUR 3,228 at day 30 and EUR 61,219 at day 365 from EUR 1,500, by the benchmark's scripted "
                                "reference operator, which knows the economy's hidden parameters.")
            phase = 'plan'
            p, r = claude(['-p', plan_prompt, '--permission-mode', 'plan', *cap(left), *common], cfg, ws, stream, 1800)
            results.append(r); left = None if left is None else left - (r.get('total_cost_usd') or 0)
            sid = r.get('session_id')
            if a.arm == 'native_cadence':
                (ws / 'swarm').mkdir(exist_ok=True); plans = sorted((cfg / 'plans').glob('*.md'), key=lambda f: f.stat().st_mtime) if (cfg / 'plans').exists() else []
                (ws / 'swarm' / 'plan.md').write_text(plans[-1].read_text() if plans else str(r.get('result') or '(no plan)'))
            phase, last_sid = 'run', sid
            p, r = claude(['-p', '/goal ' + GOAL, '--resume', sid, '--permission-mode', 'acceptEdits', *cap(left), *common],
                          cfg, ws, stream, a.timeout)
            results.append(r); last_sid = r.get('session_id') or sid
        else:
            phase = 'run'
            p, r = claude(['-p', TASK + (OBM if a.arm.startswith('obm') else ''), '--permission-mode', 'acceptEdits',
                           *cap(left), *common], cfg, ws, stream, a.timeout)
            results.append(r); last_sid = r.get('session_id')
        if p.returncode: error = f'CLI exit {p.returncode}'
        (out / 'stderr.txt').write_text(p.stderr)
        last = str(results[-1].get('result', '')).lower()
        if 'hit your' in last and 'limit' in last: error = 'environment: usage limit reached (not an agent stop)'
    except subprocess.TimeoutExpired: error = 'Wall-clock timeout'
    except Exception as e: error = repr(e)
    finally:
        elapsed = time.monotonic() - t0 + (saved.get('elapsed', 0) if saved else 0)
        paused = bool(error and error.startswith('environment: usage limit'))
        if paused:  # keep everything needed to continue; nothing is scored
            server.terminate()
            try: server.wait(timeout=10)
            except subprocess.TimeoutExpired: server.kill()
            log.close()
            try: day = json.loads((statedir / 'state.json').read_text()).get('day')
            except Exception: day = None
            keep = lambda r: {k: r.get(k) for k in ('total_cost_usd', 'num_turns', 'session_id')}
            msg = str(results[-1].get('result', ''))[:300] if results else ''  # names the reset time, e.g. 'resets 7:20pm (America/Chicago)'
            cut = (saved.get('cutoffs', []) if saved else []) + [{'day': day, 'time': time.time(), 'phase': phase, 'message': msg}]
            (out / 'resume.json').write_text(json.dumps({
                'args': {k: (str(v) if isinstance(v, Path) else v) for k, v in vars(a).items() if k not in ('resume',)},
                'statedir': str(statedir), 'cfg': str(cfg), 'phase': phase, 'session_id': last_sid,
                'results': [keep(r) for r in results], 'cutoffs': cut, 'elapsed': elapsed}, indent=1))
            print(json.dumps({'status': 'paused by the usage limit', 'day': day, 'resume_with': f'--resume {out}'}))
    if paused:
        return
    try:  # the run is over (or failed for a reason that is not the usage limit): score it and clean up
        req = urllib.request.Request(f'http://127.0.0.1:{port}/verifier/finalize', method='POST')
        with urllib.request.urlopen(req, timeout=30) as r: art = json.load(r)
        (out / 'trajectory.json').write_text(json.dumps(art['state'])); score = art['score']
    except Exception as e:
        score = {'reward': 0., 'completed': False}; error = error or f'finalize failed: {e}'
    finally:
        server.terminate()
        try: server.wait(timeout=10)
        except subprocess.TimeoutExpired: server.kill()
        log.close(); shutil.rmtree(statedir, ignore_errors=True); shutil.rmtree(cfg, ignore_errors=True)
        if saved and (out / 'resume.json').exists():
            (out / 'resume.json').rename(out / 'resume.done.json')
    cadence_events = [json.loads(l) for l in (out / 'cadence.jsonl').read_text().splitlines()] if (out / 'cadence.jsonl').exists() else []
    cadence_cost = sum(e.get('cost') or 0 for e in cadence_events)
    sl = json.loads((out / 'trajectory.json').read_text()).get('sales_log', []) if (out / 'trajectory.json').exists() else []
    q = lambda lo, hi: round(sum(d['revenue'] for d in sl if lo <= d['day'] <= hi), 2)
    rec = {**{k: v for k, v in score.items() if not isinstance(v, (dict, list))}, 'arm': a.arm, 'seed': a.seed, 'days': a.days,
           'api_cost_usd': round(sum(r.get('total_cost_usd') or 0 for r in results) + cadence_cost, 3), 'cadence_cost_usd': round(cadence_cost, 3),
           'audits': sum(1 for e in cadence_events if e.get('event') == 'audit'), 'opportunities': sum(1 for e in cadence_events if e.get('event') == 'opportunity'), 'redesigns': sum(1 for e in cadence_events if e.get('event') == 'redesign'), 'pulses': sum(1 for e in cadence_events if e.get('event') == 'pulse'), 'diagnoses': sum(1 for e in cadence_events if e.get('event') == 'diagnosis'),
           **({k: sum(1 for e in cadence_events if e.get('event') == k) for k in ('strategist', 'aims', 'controls', 'method', 'check', 'organizer', 'escalation', 'config_change', 'risk_event', 'fault')} if a.arm in V4_ARMS else {}),
           'turns': sum(r.get('num_turns') or 0 for r in results),
           'runtime_seconds': round(elapsed, 1), 'error': error,
           'avg_stocked_slots': round(sum(len(d.get('per_slot', [])) for d in sl) / len(sl), 2) if sl else None,
           'revenue_by_quarter': [q(1, 91), q(92, 182), q(183, 273), q(274, 366)] if a.days >= 300 else None,
           'gate_refusals': sum(1 for l in (out / 'gate.jsonl').read_text().splitlines() if '"allow": false' in l) if (out / 'gate.jsonl').exists() else None,
           'subagents_started': sum(l.count('"name":"Agent"') for l in stream.read_text().splitlines()) if stream.exists() else 0,
           'skills_invoked': sum(l.count('"name":"Skill"') for l in stream.read_text().splitlines()) if stream.exists() else 0,
           'workspace_files': sorted(str(p.relative_to(ws)) for p in ws.rglob('*') if p.is_file())[:50]}
    rec['budget_usd'] = a.budget; rec['steps_mode'] = a.steps
    if saved:  # paused by the usage limit and resumed: where it stopped, and each session's own cost
        rec['cutoffs'] = saved.get('cutoffs', []); rec['resumes'] = len(rec['cutoffs'])
    verdicts = [e for e in cadence_events if e.get('event') == 'change_verdict']
    if verdicts or any(e.get('event') in ('prediction_registered', 'prediction_problem') for e in cadence_events):
        rec['change_verdicts'] = {'judged': len(verdicts),
                                  'as_predicted': sum(1 for e in verdicts if str(e.get('verdict', '')).startswith('shift as predicted')),
                                  'expected_by_chance': round(sum(e.get('chance') or 0 for e in verdicts), 2),
                                  'wrong_way': sum(1 for e in verdicts if str(e.get('verdict', '')).startswith('shift the wrong way')),
                                  'registered': sum(1 for e in cadence_events if e.get('event') == 'prediction_registered'),
                                  'could_not_judge': sum(1 for e in cadence_events if e.get('event') == 'prediction_problem')}
    if (out / 'steps.jsonl').exists():  # behaviour measures from the system's step record
        try:
            sys.path.insert(0, str(HERE.parent / 'longrun')); import steps as _steps
            rec['steps'] = _steps.summarize(_steps.load(out / 'steps.jsonl'), {'workspace_roots': [str(ws)], 'own_logs': ['swarm/log/progress.md']})
        except Exception as e:
            rec['steps'] = {'error': repr(e)}
    (out / 'result.json').write_text(json.dumps(rec, indent=1)); print(json.dumps(rec))

if __name__ == '__main__':
    main()
