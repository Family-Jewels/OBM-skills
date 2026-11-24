"""Task profile -> configuration with bounds (engine v4). The organization review may move a setting only within its bounds.

spec['profile'] = {
  'work_shape': 'operation' | 'deliverables' | 'search',
  'feedback_lag': how long before a change shows in the top measure, in the task's clock units (periods on a calendar
                  clock, spend on a budget clock, seconds on a wall clock),
  'reversible': bool, can a bad action be undone?
}
"""
import math

SHAPES = ("operation", "deliverables", "search")

def derive(spec, window):
    pr = spec.get("profile") or {}
    shape = pr.get("work_shape", "operation")
    if shape not in SHAPES:
        shape = "operation"
    W = max(1, window or 1)
    lag_pts = math.ceil((pr.get("feedback_lag") or W) / W)
    rev = bool(pr.get("reversible", False))
    imp_gap = max(3, lag_pts + 1)
    cfg = {
        "strategy_every": imp_gap,          # points between scheduled strategies
        "method_gap": imp_gap,              # points between adopted method changes (improvement lane)
        "control_gap": 1,                   # points between adopted control changes (risk lane)
        "risk_sweep_every": 2 if rev else 1,  # routine risk sweep, in points, when no risk event fired
        "checker": {"operation": "sample_claims", "deliverables": "submissions", "search": "attempts"}[shape],
        "checker_every": 2,                 # points between claim samples (operation)
        "full_audits": 4,                   # per horizon
    }
    bounds = {
        "strategy_every": [2, 6], "method_gap": [2, 6], "control_gap": [1, 3], "risk_sweep_every": [1, 4],
        "checker": ["off", cfg["checker"]], "checker_every": [1, 4], "full_audits": [2, 8],
    }
    return {"shape": shape, "lag_points": lag_pts, "reversible": rev}, cfg, bounds

def validate(key, value, cfg, bounds):
    """Returns (ok, value or reason) for a proposed configuration change."""
    if key not in cfg:
        return False, f"'{key}' is not a setting (settings: {', '.join(cfg)})"
    b = bounds[key]
    if isinstance(cfg[key], str):
        v = str(value).strip().strip("'\"")
        return (True, v) if v in b else (False, f"'{v}' is not one of {b}")
    try:
        v = int(float(value))
    except Exception:
        return False, f"'{value}' is not a number"
    if not b[0] <= v <= b[1]:
        return False, f"{v} is outside the bounds {b[0]}-{b[1]}"
    if v == cfg[key]:
        return False, f"{key} is already {v}"
    return True, v
