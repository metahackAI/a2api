"""Review a-commerce's own agent runs stage by stage, as call_review.py does for evaluate.py runs.

python examples/acommerce/own_review.py RAW.md A2API.md --mode own-facade-raw --mode own-facade-a2api \
    --converted facade-converted.json [--out review.md] [--json review.json]

Each report is `cargo xtask eval --logs DIR --out REPORT.md` (the logs in `<report without .md>-logs/`);
`--mode` names its tool set: own-facade-raw (the legacy facade as is), own-facade-a2api /
own-facade-a2api-lookup (the facade through a2api_gateway.py, without / with the order number lookup)
or own-acom (A-Commerce tools). Read from each run's log:

- given: the tools the agent's own search offered its planner (`search_tools` candidates, every turn);
- calls: each `call_tool` step, its input and the error it got, attributed with call_review's rules
  against the definition the agent saw (the raw screen, the converted screen from `--converted`, or
  the A-Commerce tool);
- limits: a reply that says "I stopped after ..., the limit for one turn" (or that no model answered).

Done and missing come from the report's rows, matched to the logs in the order the runs started.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from call_review import Catalog, facade_map, judge, markdown, summary  # noqa: E402
from own_traces import report_rows  # noqa: E402
from traces import tasks_from  # noqa: E402

MODES = ('own-facade-raw', 'own-facade-a2api', 'own-facade-a2api-lookup', 'own-acom')
# The gateway passes a2api's own codes; the services answer with a class (and codes of their own).
GATEWAY_CODES = {'invalid_input': 'INVALID_INPUT', 'unknown_tool': 'UNKNOWN_FUNCTION'}
CLASSES = {'invalid_input': 'UPSTREAM_VALIDATION_FAILED', 'not_found': 'RESOURCE_NOT_FOUND',
           'invalid_state': 'UPSTREAM_CONFLICT', 'conflict': 'UPSTREAM_CONFLICT', 'rule': 'UPSTREAM_CONFLICT',
           'permission': 'PERMISSION_DENIED', 'forbidden': 'PERMISSION_DENIED',
           'upstream_unavailable': 'UPSTREAM_UNAVAILABLE', 'internal': 'UPSTREAM_ERROR'}
SPLIT = re.compile(r'; (?=(?:fact|tool|change set|called|must not|no change set)\b)')


def code_of(error, mode):
    error = error or {}
    if mode.startswith('own-facade-a2api'):
        code = (error.get('code') or '').lower()
        if code in GATEWAY_CODES:
            return GATEWAY_CODES[code]
        if code.startswith(('upstream_', 'resource_')) or code in ('deadline_exceeded', 'outcome_unknown', 'rate_limited'):
            return code.upper()
    return CLASSES.get(error.get('class'), 'UPSTREAM_ERROR' if error.get('class') == 'internal' else (error.get('code') or 'UNKNOWN'))


def run_from_log(data, row, mode, catalog, task, repetition):
    turns = data['log'].get('turns') or []
    seen = ' '.join((task or {}).get('turns') or [turn.get('text') or '' for turn in turns])
    offered, calls, replies, host_error = set(), [], [], None
    for turn in turns:
        for step in turn['log'].get('steps') or []:
            if step['kind'] == 'search_tools':
                offered |= {catalog.tool(item['tool']) for item in step.get('output') or [] if isinstance(item, dict)}
            if step['kind'] != 'call_tool' or not step.get('tool'):
                continue
            given = step.get('input') or {}
            given = given.get('args', given) if isinstance(given, dict) and set(given) == {'args'} else given
            ok = step.get('status') == 'completed'
            error = step.get('error') or {}
            tool = catalog.tool(step['tool'])
            offered.add(tool)
            calls.append({'tool': tool, 'name': step['tool'], 'arguments': given if isinstance(given, dict) else {},
                          'ok': ok, 'code': None if ok else code_of(error, mode),
                          'detail': None if ok else (error.get('message') or step.get('summary')), 'issues': None, 'before': seen})
            if ok:
                seen += ' ' + json.dumps(step.get('output'), ensure_ascii=False)
        reply = turn.get('reply_text') or ''
        replies.append(reply + ' ' + json.dumps(turn.get('blocks') or [], ensure_ascii=False))
        if 'the limit for one turn' in reply:
            host_error = host_error or 'LIMIT'
        models = turn['log'].get('model_calls') or []
        if models and not any(call.get('succeeded') for call in models):
            host_error = host_error or 'MODEL'
    missing = [item for item in SPLIT.split(row['missing']) if item and item != '—'] if row else []
    run = {'task': data['task'], 'mode': mode, 'repetition': repetition, 'done': bool(row and row['done']),
           'missing': missing, 'hostError': host_error, 'replies': replies}
    return run, offered, calls


def functions(mode, catalog, converted):
    if mode == 'own-acom':
        items = catalog.acom
    elif mode == 'own-facade-raw':
        items = catalog.facade
    else:
        items = {converted['screens'][item['tool']]: item for item in converted['items']}
    return {tool: {'name': item['tool'], 'description': item.get('summary'), 'parameters': item['input_schema']}
            for tool, item in items.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('reports', nargs='+')
    parser.add_argument('--mode', action='append', default=[], choices=MODES, help='one per report')
    parser.add_argument('--repo', default=None)
    parser.add_argument('--acom', default=str(HERE.parents[1] / 'artifacts' / 'acommerce' / 'manifest-acom.json'))
    parser.add_argument('--facade', default=str(HERE.parents[1] / 'artifacts' / 'acommerce' / 'manifest-facade-22.json'))
    parser.add_argument('--converted', type=Path, help='a2api_gateway.py --dump of the same facade')
    parser.add_argument('--out', type=Path)
    parser.add_argument('--json', type=Path)
    options = parser.parse_args()
    if len(options.mode) != len(options.reports):
        raise SystemExit('Give one --mode per report.')
    if options.repo is None:
        from stack import REPO
        options.repo = REPO
    tasks, fmap = tasks_from(options.repo), facade_map(options.repo)
    acom = json.loads(Path(options.acom).read_text())['items']
    facade = json.loads(Path(options.facade).read_text())['items']
    catalog = Catalog(acom, facade, {}, {})
    converted = json.loads(options.converted.read_text()) if options.converted else None
    reviews = []
    for report, mode in zip(options.reports, options.mode):
        if mode.startswith('own-facade-a2api') and not converted:
            raise SystemExit('a2api modes need --converted.')
        defined = functions(mode, catalog, converted)
        rows = report_rows(report)
        logs = Path(str(Path(report).with_suffix('')) + '-logs')
        runs = {}
        for path in sorted(logs.glob('*.json')):
            data = json.loads(path.read_text())
            turns = data['log'].get('turns') or []
            runs.setdefault(data['task'], []).append((turns[0].get('started_at') if turns else '', data))
        for task_id, group in runs.items():
            group.sort(key=lambda item: item[0])
            for number, (_, data) in enumerate(group):
                row = (rows.get(task_id) or [])[number] if number < len(rows.get(task_id) or []) else None
                task = tasks.get(task_id)
                run, offered, calls = run_from_log(data, row, mode, catalog, task, number)
                reviews.append(judge(run, task, offered, True, calls, defined.get, fmap))
    rows = summary(reviews)
    text = markdown(rows, reviews, ', '.join(Path(p).stem for p in options.reports))
    text = text.replace('\n\n', '\n\na-commerce 자체 에이전트. "모델에게 줌"은 에이전트의 도구 검색이 계획기에 준 후보다. '
                        '판정 기준 함수 정의: 원본 화면 / a2api 변환 화면(`--converted`) / A-Commerce 도구.\n\n', 1)
    if options.out:
        options.out.write_text(text)
    else:
        print(text)
    if options.json:
        options.json.write_text(json.dumps({'summary': rows, 'runs': reviews}, ensure_ascii=False, indent=1))
    for r in rows:
        print(json.dumps({k: r[k] for k in ('mode', 'runs', 'passed', 'given', 'called', 'succeeded', 'neededAvailable', 'stages', 'attribution')},
                         ensure_ascii=False), file=sys.stderr)


if __name__ == '__main__':
    main()
