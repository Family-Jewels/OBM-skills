"""Request ledger (engine v4): every request between roles is filed, merged with repeats, answered and escalated by code.

A role's record may end with a section
    ## Requests
    - to: designer | key: chart-minutes-per-restock | Chart minutes per restock call and slots per call.
'to' is one of: controls, designer, strategist, human. 'key' is a short slug the role chooses; a request with the same
'to' and 'key' as an earlier one is a repeat: merged into it if open, or reopening it if closed (asked += 1 either way),
never queued twice; asked 3 times escalates to the human.

A job that takes requests answers each in a section
    ## Dispositions
    - REQ-007: done | added the chart
    - REQ-008: declined | the restock cost is fixed by the environment (see Facts)
    - REQ-009: deferred | needs two more points of data
An unanswered request goes back to open. 'deferred' keeps it open.
"""
import re

TARGETS = ("controls", "designer", "strategist", "human")
BRANCH = {"controls": "risk", "designer": "improvement", "strategist": "improvement", "human": "human"}
ESCALATE_AGE, ESCALATE_ASKED = 3, 3  # points open; times asked

def _section(text, title):
    m = re.search(rf"^#+\s*{title}\s*$(.*?)(?=^#+\s|\Z)", text or "", re.M | re.S | re.I)
    return m.group(1) if m else ""

def parse_requests(text):
    out = []
    for line in _section(text, "Requests").splitlines():
        line = line.strip().lstrip("-*").strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split("|")]
        f = {}
        rest = []
        for p in parts:
            m = re.match(r"(to|key)\s*:\s*(.+)$", p, re.I)
            if m:
                f[m.group(1).lower()] = m.group(2).strip()
            else:
                rest.append(p)
        to = (f.get("to") or "").lower().split()[0] if f.get("to") else ""
        to = {"controls owner": "controls", "control": "controls"}.get(to, to)
        if to not in TARGETS or not rest:
            continue
        key = re.sub(r"[^a-z0-9-]+", "-", (f.get("key") or rest[0][:40]).lower()).strip("-")[:48]
        out.append({"to": to, "key": key, "text": " | ".join(rest)[:400]})
    return out

def parse_dispositions(text):
    out = {}
    for line in _section(text, "Dispositions").splitlines():
        m = re.match(r"\s*[-*]?\s*(REQ-\d+)\s*:\s*(done|declined|deferred)\b\s*[|:—-]*\s*(.*)$", line, re.I)
        if m:
            out[m.group(1).upper()] = (m.group(2).lower(), m.group(3).strip()[:300])
    return out

class Ledger:
    def __init__(self, mem):
        self.m = mem.setdefault("ledger", {"n": 0, "reqs": []})

    @property
    def reqs(self):
        return self.m["reqs"]

    def file(self, frm, items, point, period):
        """File parsed requests from record 'frm'. Returns the list of (req, 'new'|'merged')."""
        done = []
        for it in items:
            same = next((r for r in reversed(self.reqs) if r["to"] == it["to"] and r["key"] == it["key"]), None)
            if same:  # a repeat: merged into the open one, or reopens a closed one (keeping its count, so repeats escalate)
                same["asked"] += 1; same["text"] = it["text"]; same["last_from"] = frm
                if same["status"] in ("done", "declined"):
                    same["reason"] = f"reopened by {frm} after '{same['status']}: {same['reason'][:80]}'"
                    same["status"] = "open"; same["closed_point"] = None
                    done.append((same, "reopened"))
                else:
                    done.append((same, "merged"))
                continue
            self.m["n"] += 1
            r = {"id": f"REQ-{self.m['n']:03d}", "from": frm, "to": it["to"], "key": it["key"], "text": it["text"], "status": "open",
                 "opened_point": point, "opened_period": period, "asked": 1, "reason": "", "closed_point": None, "escalated": []}
            self.reqs.append(r); done.append((r, "new"))
        return done

    def open_for(self, to):
        tos = (to,) if isinstance(to, str) else tuple(to)
        return [r for r in self.reqs if r["to"] in tos and r["status"] == "open"]

    def take(self, reqs, job_id):
        for r in reqs:
            r["status"] = "in_progress"; r["job"] = job_id

    def answer(self, job_id, text, point):
        """Apply a job's dispositions. Requests the job held but did not answer go back to open."""
        disp = parse_dispositions(text)
        res = []
        for r in self.reqs:
            if r.get("job") != job_id or r["status"] != "in_progress":
                continue
            d = disp.get(r["id"])
            if d and d[0] in ("done", "declined"):
                r["status"], r["reason"], r["closed_point"] = d[0], d[1], point
            else:
                r["status"] = "open"; r["reason"] = d[1] if d else "not answered"
            res.append((r["id"], r["status"]))
        return res

    def escalations(self, point):
        """Requests to escalate now: open too long or asked too often (each reason once per request)."""
        out = []
        for r in self.reqs:
            if r["status"] not in ("open", "in_progress"):
                continue
            why = []
            if point - r["opened_point"] >= ESCALATE_AGE and "age" not in r["escalated"]:
                why.append(f"open {point - r['opened_point']} points"); r["escalated"].append("age")
            if r["asked"] >= ESCALATE_ASKED and "asked" not in r["escalated"]:
                why.append(f"asked {r['asked']} times"); r["escalated"].append("asked")
            if r["to"] == "human" and "human" not in r["escalated"]:
                why.append("addressed to the human"); r["escalated"].append("human")
            if why:
                out.append((r, "; ".join(why)))
        return out

    def table(self, point, limit=20):
        live = [r for r in self.reqs if r["status"] in ("open", "in_progress")]
        recent = [r for r in self.reqs if r["status"] not in ("open", "in_progress") and r["closed_point"] is not None
                  and point - r["closed_point"] <= 3]
        if not live and not recent:
            return "\n## Requests (filed and tracked by the system)\n\nNone open.\n"
        rows = ["\n## Requests (filed and tracked by the system; answer each in a '## Dispositions' section when it is handed to you)\n",
                "| id | from | to | key | age (points) | asked | status | reason |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
        for r in (live + recent)[-limit:]:
            rows.append(f"| {r['id']} | {r['from']} | {r['to']} | {r['key']} | {point - r['opened_point']} | {r['asked']} | {r['status']} | "
                        f"{(r['reason'] or '').replace('|', '/')[:120]} |")
        return "\n".join(rows) + "\n"

    def prompt_list(self, reqs):
        return "\n".join(f"- {r['id']} (from {r['from']}, asked {r['asked']}x, key {r['key']}): {r['text']}" for r in reqs)
