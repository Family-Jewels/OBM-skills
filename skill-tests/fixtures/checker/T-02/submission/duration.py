import re

UNITS = {"h": 3600, "m": 60, "s": 1}

def parse_duration(text):
    """'1h30m' -> 5400. Units: h, m, s."""
    parts = re.findall(r"(\d+)([a-z])", text)
    if not parts or "".join(n + u for n, u in parts) != text:
        raise ValueError(text)
    total = 0
    for n, u in parts:
        if u not in UNITS:
            raise ValueError(text)
        total += int(n) * UNITS[u]
    return total
