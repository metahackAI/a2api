"""python examples/acommerce/replay_guard.py artifacts/acommerce/runs/<runs>.jsonl

Count variant notes by replaying ToolSession(variant_note=3) over recorded calls (run records keep only
the first 3,000 characters of a result, which can cut the note off). Also counts would-be notes in modes
without the guard."""
import json, sys
sys.path.insert(0, 'src')
from a2api.tool_session import _target
kind = {i['tool']: i['kind'] for i in json.load(open('artifacts/acommerce/manifest-acom.json'))['items']}
def name_of(name):
    return name[5:] if name.startswith('acom_') else name
def replay(r):
    seen, notes, turn = {}, 0, None
    def one(name, args, ok):
        nonlocal notes
        k = kind.get(name_of(name))
        if k is None or not ok:
            return
        if k != 'read':
            seen.clear(); return
        target, condition = _target(args or {})
        conditions = seen.setdefault((name, target), [])
        if condition in conditions:
            return
        conditions.append(condition)
        notes += len(conditions) >= 3
    for c in r['toolCalls']:
        if c.get('turn', 0) != turn:
            turn = c.get('turn', 0); seen.clear()
        if c['name'] == 'a2api_batch':
            try:
                results = json.loads(c['result'])['batch']
            except Exception:
                results = None
            for i, x in enumerate((c['arguments'] or {}).get('calls', [])):
                ok = results is None or (i < len(results) and results[i]['result'].get('status') == 'succeeded')
                one(x['name'], x['arguments'], ok)
        elif c['name'] not in ('a2api_load', 'a2api_search'):
            one(c['name'], c['arguments'], '"status":"succeeded"' in c['result'][:40])
    return notes
path = sys.argv[1]
runs = [json.loads(l) for l in open(path) if '"type": "run"' in l]
for mode in dict.fromkeys(r['mode'] for r in runs):
    group = [r for r in runs if r['mode'] == mode]
    counts = [replay(r) for r in group]
    print(f"{mode}: notes {sum(counts)}, runs with a note {sum(c > 0 for c in counts)}/{len(group)}, passed {sum(r['done'] for r in group)}")
