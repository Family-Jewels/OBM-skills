"""Stop analysis: for each working day in a Vending Bench transcript (stream.jsonl), find when the agent ended the day
(wait_for_next_day), how many of the 480 working minutes it had used, and what it did and said just before.
Read-only. usage: python3 -I extract_stops.py <stream.jsonl> <out.jsonl>"""
import json, re, sys
FOOT = re.compile(r"\[Day (\d+)/\d+[^\]]*? (\d\d):(\d\d)")   # '[Day 12/365 — Mon 05 Jan 2026 14:35 — balance ...'
def mins(h, m): return int(h) * 60 + int(m) - 540                    # minutes since 09:00
out, last_tools, last_text, clock, day, ctx = [], [], "", None, None, 0
inv = {}                                                              # latest machine/storage readings, by day
for line in open(sys.argv[1]):
    d = json.loads(line)
    t = d.get("type")
    if t == "assistant":
        u = d["message"].get("usage", {})
        c = u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
        if c: ctx = c
        for b in d["message"]["content"]:
            if b["type"] == "text" and b["text"].strip():
                last_text = b["text"].strip()
            elif b["type"] == "tool_use":
                name = b["name"].split("__")[-1]
                if name == "wait_for_next_day" and day is not None:
                    out.append({"day": day, "minutes_used": clock, "minutes_left": 480 - clock if clock is not None else None,
                                "last_tools": last_tools[-6:], "said": last_text[-600:], "context_tokens": ctx,
                                "inventory": inv.get(day)})
                    last_tools = []; last_text = ""
                else:
                    last_tools.append(name)
    elif t == "user" and isinstance(d["message"]["content"], list):
        for b in d["message"]["content"]:
            if b.get("type") != "tool_result":
                continue
            txt = b.get("content")
            txt = txt if isinstance(txt, str) else json.dumps(txt)
            m = FOOT.findall(txt)
            if m:
                dd, h, mm = m[-1]
                day, clock = int(dd), max(0, min(480, mins(h, mm)))
            if "slot" in txt.lower() and ("empty" in txt.lower() or "qty" in txt.lower() or "quantity" in txt.lower()):
                inv.setdefault(day, {})["machine"] = txt[:1500]
            if "storage" in txt.lower() or "depot" in txt.lower():
                inv.setdefault(day, {})["storage"] = txt[:800]
with open(sys.argv[2], "w") as f:
    for r in out:
        f.write(json.dumps(r) + "\n")
print(len(out), "day ends")
