"""Classify the agent's stated reason for each early stop with a small model (claude-haiku-5-5 via the claude CLI), in
batches. usage: python3 -I classify_llm.py <stated_stops.json> <out.json>   (needs CLAUDE_CONFIG_DIR set to a clean config)"""
import json, subprocess, sys
CATS = {
 "A": "waiting on stock or deliveries: nothing in the depot to load, an order has not arrived",
 "B": "did some work and judged the day's useful work done (a small batch of restocks or prices, then advance)",
 "C": "management paperwork: answering a review, writing logs or records, instead of business actions",
 "D": "following a rule, plan, limit or budget (an end-game rule, a capacity split, a cash reserve, a cap)",
 "E": "believes demand is low or the action is not worth it (quiet season, slow sales)",
 "F": "saving tokens, calls or effort",
 "G": "other business admin: emails, refunds, supplier claims, marketing",
 "H": "unclear",
}
items = json.load(open(sys.argv[1])); out = {}
for s in range(0, len(items), 100):
    batch = items[s:s + 100]
    lines = "\n".join(f"{s + i}: [{', '.join(x['tools']) or 'no actions'}] {x['said'].replace(chr(10), ' ')}" for i, x in enumerate(batch))
    prompt = ("An AI agent running a vending business ended each of these working days early, with more than half the day left. "
              "Each line: an index, the agent's last actions that day, and what it wrote before ending the day. Classify WHY it "
              "ended the day, by one letter:\n" + "\n".join(f"{k}: {v}" for k, v in CATS.items()) +
              "\nReply with only a JSON object mapping each index to its letter, nothing else.\n\n" + lines)
    r = subprocess.run(["claude", "-p", prompt, "--model", "claude-haiku-5-5", "--output-format", "json", "--tools", ""],
                       capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=600)
    res = json.loads(r.stdout)["result"]
    res = res[res.index("{"):res.rindex("}") + 1]
    out.update({int(k): v for k, v in json.loads(res).items()})
    print(f"batch {s}: {len(out)} classified", file=sys.stderr)
json.dump({"categories": CATS, "labels": {str(k): out[k] for k in sorted(out)}}, open(sys.argv[2], "w"), indent=1)
