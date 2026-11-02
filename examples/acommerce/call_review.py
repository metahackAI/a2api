"""Review evaluate.py runs stage by stage, and attribute failed calls.

python examples/acommerce/call_review.py artifacts/acommerce/runs/<runs>.jsonl [--out review.md] [--json review.json]

For each run, the first stage that went wrong:
  A  a function the task needs was never given to the model (A0: the API has no such function at all)
  B  it was given but never called (D when a limit or error ended the run first)
  C  it was called but never succeeded (the failed calls are attributed below)
  D  the run hit a limit (model calls, time, provider) before answering
  E  every needed function succeeded but the answer was judged wrong: the change set or write inputs
     (E-write), numbers the reply has in another form (E-format), or facts the reply leaves out (E-content)

Failed business calls are attributed:
  model:schema         the call broke the function's own schema (a2api rejected it before sending)
  model:function       a function called without loading it, or one that does not exist
  model:ungrounded     a looked-up value (an ID, a table or record name) not in the request or any earlier result
  model:described      the service rejected a rule the function's description or schema states
  source:undocumented  the service rejected a rule nothing in the function's description or schema states:
                       information the legacy definition lacks and the conversion did not add
  business             the state or a business rule refused it (not the input), or the service failed
  unclear              not decided automatically (listed for a person to read)

Needed functions are the task's required A-Commerce tools. On the legacy facade they count as given or
called when a screen the a-commerce docs map to them was (docs/api/README.md §7). Runs from 2026-11-02
record the functions offered at each step; for earlier runs "given" is read from load and search results
(and is unknown for host pre-selection).
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from conversion_fidelity import fields, model_view, required as required_paths, strip_null  # noqa: E402
from legacy_facade import RENAME, WORDS  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402
from scoring import numbers  # noqa: E402
from traces import tasks_from  # noqa: E402
from a2api.importers.catalog import snake  # noqa: E402

OWN = ('a2api_search', 'a2api_load', 'a2api_batch')
BATCH_ITEM = re.compile(r'\{"name":"([^"]+)","result":\{"status":"(succeeded|failed)"'
                        r'(?:,"error":\{"code":"([A-Z_]+)"(?:,"detail":"((?:[^"\\]|\\.)*)")?)?')
ID_VALUE = re.compile(r'^(?:[a-z]{2,6}_[a-z0-9_]+|#?\d{3,})$')


def facade_map(repo):
    """{A-Commerce tool: {screens}} from the a-commerce API docs table (§7)."""
    out = {}
    for line in (Path(repo) / 'docs' / 'api' / 'README.md').read_text().splitlines():
        cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
        if len(cells) < 3 or not cells[0].startswith('`get') and not cells[0].startswith('`save'):
            continue
        screens = re.findall(r'`([A-Za-z0-9]+)`', cells[0])
        for tool in re.findall(r'`([a-z_]+)`', cells[2]):
            out.setdefault(tool, set()).update(screens)
    return out


class Catalog:
    """Model-facing function definitions per catalog tool, and the model's names mapped back to tools."""

    def __init__(self, acom_items, facade_items, acom_views, facade_views):
        self.acom = {item['tool']: item for item in acom_items}
        self.facade = {item['tool']: item for item in facade_items}
        self.views = {**acom_views, **facade_views}
        self.raw = {item['tool']: {'name': item['tool'], 'description': item.get('summary'), 'parameters': item['input_schema']}
                    for item in [*acom_items, *facade_items]}
        # Converted names with the abbreviations spelled out (2026-11-01 and later) and without.
        self.converted = {**{snake(screen).lower(): screen for screen in self.facade},
                          **{snake(screen, WORDS).lower(): screen for screen in self.facade}}

    def tool(self, name):
        for prefix in ('acom_', 'facade_', ''):
            if name.startswith(prefix):
                bare = name[len(prefix):]
                if bare in self.acom or bare in self.facade:
                    return bare
                if bare in self.converted:
                    return self.converted[bare]
        return name

    def function(self, mode, tool):
        raw = mode in ('acom-all', 'facade-all')
        return (self.raw if raw else self.views).get(tool)


def parse(text):
    try:
        return json.loads(text)
    except (ValueError, TypeError):
        return None


def outcome(text, raw):
    """(ok, error code, detail, issues) of one recorded call result (texts may be cut)."""
    head = (text or '')[:60]
    if raw:
        body = parse(text)
        status = body.get('status') if isinstance(body, dict) else None
        if status is None:
            match = re.match(r'\{"status":(\d+)', head)
            status = int(match[1]) if match else None
        if isinstance(status, int) and 200 <= status < 300:
            return True, None, None, None
        error = ((body or {}).get('body') or {}).get('error') if isinstance(body, dict) and isinstance(body.get('body'), dict) else None
        if isinstance(body, dict) and body.get('error') == 'unknown function':
            return False, 'UNKNOWN_FUNCTION', 'unknown function', None
        message = (error or {}).get('message') if isinstance(error, dict) else None
        code = {400: 'UPSTREAM_VALIDATION_FAILED', 422: 'UPSTREAM_VALIDATION_FAILED', 404: 'RESOURCE_NOT_FOUND',
                409: 'UPSTREAM_CONFLICT', 403: 'PERMISSION_DENIED'}.get(status, f'HTTP_{status}')
        return False, code, message or text[:300], None
    if head.startswith('{"status":"succeeded"'):
        return True, None, None, None
    body = parse(text)
    if isinstance(body, dict) and isinstance(body.get('error'), dict):
        error = body['error']
        return False, error.get('code'), error.get('detail'), error.get('issues')
    if 'tool call limit' in head:
        return False, 'TOOL_CALL_LIMIT', head, None
    return False, 'UNPARSED', (text or '')[:300], None


def calls_of(run, catalog):
    """Business calls in order: {tool, arguments, ok, code, detail, issues, before} (before: text seen until then)."""
    out, seen = [], ' '.join(run.get('turnsText') or [])
    raw = run['mode'] in ('acom-all', 'facade-all')
    for call in run.get('toolCalls', []):
        if call['name'] == 'a2api_batch':
            # Records keep the first 3,000 characters: read each item's status where it is still there;
            # items past the cut are unknown and not counted.
            found = BATCH_ITEM.findall(call.get('result') or '')
            items = (call.get('arguments') or {}).get('calls') if isinstance(call.get('arguments'), dict) else None
            for index, item in enumerate(items if isinstance(items, list) else []):
                if not isinstance(item, dict) or not isinstance(item.get('name'), str):
                    continue  # a malformed batch item; a2api refused the whole batch before running it
                if index < len(found):
                    status, code, detail = found[index][1], found[index][2] or None, found[index][3] or None
                    ok = status == 'succeeded'
                else:
                    ok, code, detail = None, None, None
                out.append({'tool': catalog.tool(item['name']), 'name': item['name'], 'arguments': item.get('arguments') or {},
                            'ok': ok, 'code': code, 'detail': detail and json.loads('"' + detail + '"'), 'issues': None,
                            'before': seen})
        elif call['name'] not in OWN:
            ok, code, detail, issues = outcome(call.get('result'), raw)
            out.append({'tool': catalog.tool(call['name']), 'name': call['name'], 'arguments': call.get('arguments') or {},
                        'ok': ok, 'code': code, 'detail': detail, 'issues': issues, 'before': seen})
        if (call.get('result') or '').startswith(('{"status":"succeeded"', '{"status":200', '{"batch"', '{"selected"', '{"loaded"')):
            seen += ' ' + call['result']  # values the model was given (failed calls' messages do not count)
    return out


def id_values(arguments):
    found = []
    def walk(value, key=''):
        if isinstance(value, dict):
            for k, v in value.items():
                walk(v, k)
        elif isinstance(value, list):
            for v in value:
                walk(v, key)
        elif isinstance(value, (str, int)) and not isinstance(value, bool):
            text = str(value)
            if (key == 'id' or key.endswith(('_id', 'Id', 'No')) or ID_VALUE.match(text)) and len(text) >= 3:
                found.append(text)
    walk(arguments)
    return found


RULE_WORDS = re.compile(r'\d|\b(?:at most|at least|only|must|required|such as|format|one of|e\.g\.)', re.I)


def documented(function, field_names, rule):
    """Does the function's schema or description state a rule for these fields? Only what can carry the
    rule counts: required, enum, pattern, format, or a field description with a rule in words (a number,
    "from", "at most", "only", "such as", ...). Bare minimum/maximum do not: the service's rule can differ
    from them (the legacy paging fields allow 0 and the service starts at 1)."""
    if not function:
        return False
    schema = function.get('parameters') or {}
    flat = {path.split('.')[-1].replace('[]', ''): strip_null(child) for path, child in fields(schema).items()}
    needed = {path.split('.')[-1].replace('[]', '') for path in required_paths(schema)}
    summary = function.get('description') or ''
    for name in field_names:
        # The function's own description can state it ("Each row needs corner_id, … button_label").
        if rule == 'required' and re.search(r'\b(?:needs?|required)\b', summary, re.I) and re.search(
                r'(?<![\w])' + re.escape(name) + r'(?![\w])', summary):
            return True
        child = flat.get(name)
        if child is None:
            continue
        if rule == 'required' and name in needed:
            return True
        if rule == 'value' and ('enum' in child or 'pattern' in child or child.get('format') in RULE_FORMATS):
            return True
        if RULE_WORDS.search(child.get('description') or ''):
            return True
    return False


# Formats that state a rule for a string (uint32, double and the like do not say what the service accepts).
RULE_FORMATS = {'date', 'date-time', 'time', 'email', 'uri', 'uuid'}
# Words in a service error that name fields without quoting them.
ERROR_FIELDS = {'paging': ('pageNo', 'pageSize', 'page', 'page_size')}


def appears(value, before):
    """The value as a whole JSON string or number, or as a whole word, in the request or earlier results."""
    text = str(value).lstrip('#')
    return (json.dumps(text) in before or re.search(r'(?<![\w.])' + re.escape(text) + r'(?![\w.])', before) is not None)


def looked_up(arguments):
    out = []
    for key, value in arguments.items():
        for item in (value if isinstance(value, list) else [value]):
            if isinstance(item, (str, int)) and not isinstance(item, bool) and str(item).strip():
                out.append(str(item))
    return out


def breaks_schema(arguments, function):
    if not function:
        return False
    try:
        return any(True for _ in Draft202012Validator(function.get('parameters') or {}).iter_errors(arguments))
    except Exception:
        return False


def attribute(call, function, mode):
    code, detail = call['code'], call['detail'] or ''
    if code == 'INVALID_INPUT':
        return 'model:schema'
    if code in ('NOT_LOADED', 'UNKNOWN_FUNCTION', 'NOT_SELECTED'):
        return 'model:function'
    if code == 'RESOURCE_NOT_FOUND':
        values = id_values(call['arguments'])
        if any(not appears(value, call['before']) for value in looked_up(call['arguments'])):
            return 'model:ungrounded'
        names = [key for key in call['arguments']]
        if any(re.fullmatch(r'#?\d+', value) for value in values):
            return 'model:described' if documented(function, names, 'value') else 'source:undocumented'
        return 'unclear'
    if code == 'UPSTREAM_VALIDATION_FAILED':
        if re.search(r'\bno \w+ (?:match|matches)\b', detail, re.I):
            return 'business'  # valid input, nothing in the data matches it
        if breaks_schema(call['arguments'], function):
            return 'model:schema'  # the schema says so; without a2api's check the service refused it
        quoted = re.findall(r'`([^`]+)`', detail)
        names = [RENAME.get(name, name) for name in quoted] + quoted
        for word, related in ERROR_FIELDS.items():
            if word in detail.lower():
                names += [name for name in related if name in call['arguments']]
        # A quoted value names the field that held it (`2026-10-01 00:00:00` is not a date-time).
        names += [key for key, value in call['arguments'].items() if isinstance(value, (str, int)) and str(value) in quoted]
        if not names:
            names = [key for key in call['arguments'] if key.lower() in detail.lower()]
        rule = 'required' if re.search(r'required|missing|must (?:be )?(?:given|set|sent)', detail, re.I) else 'value'
        if not names:
            return 'unclear'
        return 'model:described' if documented(function, names, rule) else 'source:undocumented'
    if code in ('UPSTREAM_CONFLICT', 'PERMISSION_DENIED', 'UPSTREAM_ERROR', 'UPSTREAM_UNAVAILABLE', 'DEADLINE_EXCEEDED',
                'RATE_LIMITED', 'OUTCOME_UNKNOWN') or (code or '').startswith('HTTP_5'):
        return 'business'
    if code == 'TOOL_CALL_LIMIT':
        return 'business'
    return 'unclear'


def offered_tools(run, catalog):
    """(tools given to the model, exact?)"""
    steps = run.get('steps') or []
    if steps and all('offered' in step for step in steps):
        return {catalog.tool(name) for step in steps for name in step['offered'] if name not in OWN}, True
    given = set()
    for call in run.get('toolCalls', []):
        body = parse(call.get('result'))
        if call['name'] == 'a2api_load' and isinstance(body, dict):
            given |= {catalog.tool(n) for n in (body.get('loaded') or []) + (body.get('already') or [])}
        if call['name'] == 'a2api_search' and isinstance(body, dict):
            given |= {catalog.tool(item['name']) for item in body.get('selected') or []}
        if call['name'] not in OWN:
            given.add(catalog.tool(call['name']))
    return given, False


def review_run(run, task, catalog, fmap):
    mode = run['mode']
    facade = 'facade' in mode
    required = list(((task or {}).get('tools') or {}).get('required') or [])
    units = []  # (needed tool, the names that satisfy it)
    for tool in required:
        if facade:
            units.append((tool, set(fmap.get(tool) or ())))
        else:
            units.append((tool, {tool}))
    offered, exact = offered_tools(run, catalog)
    if mode in ('acom-all',):
        offered, exact = set(catalog.acom), True
    if mode in ('facade-all',):
        offered, exact = set(catalog.facade), True
    calls = calls_of(run, catalog)
    for call in calls:
        if call['ok'] is False:
            call['attribution'] = attribute(call, catalog.function(mode, call['tool']), mode)
    stage = None
    per_unit = []
    for tool, names in units:
        given = bool(names & offered)
        called = [c for c in calls if c['tool'] in names]
        succeeded = any(c['ok'] for c in called)
        per_unit.append({'tool': tool, 'equivalent': sorted(names) if facade else None, 'given': given,
                         'called': bool(called), 'succeeded': succeeded})
    if run['done']:
        stage = 'passed'
    else:
        for unit in per_unit:
            if facade and not unit['equivalent']:
                stage = stage or 'A0'
            elif not unit['given']:
                stage = stage or 'A'
        if not stage:
            for unit in per_unit:
                if not unit['called']:
                    # Given, but the run stopped (a limit, the provider, context) before calling it.
                    stage = stage or ('D' if run.get('hostError') else 'B')
        if not stage:
            for unit in per_unit:
                if not unit['succeeded']:
                    stage = stage or 'C'
        if not stage and run.get('hostError'):
            stage = 'D'
        if not stage:
            missing = run.get('missing') or []
            if any(m.startswith(('change set', 'called ')) for m in missing):
                stage = 'E-write'
            else:
                shown = set(numbers(' '.join(run.get('replies') or [])))
                digits = set(re.findall(r'\d+', ' '.join(run.get('replies') or [])))
                absent = [n.strip() for m in missing for n in (re.search(r'\(([^()]*) not shown\)$', m) or [None, ''])[1].split(',') if n.strip()]
                stage = 'E-format' if absent and all(a in digits or a.lstrip('0') in {d.lstrip('0') for d in digits} for a in absent) else 'E-content'
    # Write inputs against the change set the task expects (A-Commerce tools only).
    writes = []
    if not facade:
        for item in (((task or {}).get('expect') or {}).get('change_set') or {}).get('items') or []:
            wanted = item.get('args') or {}
            tried = [c for c in calls if c['tool'] == item['tool']]
            match = any(all(c['arguments'].get(k) == v for k, v in wanted.items()) for c in tried)
            writes.append({'tool': item['tool'], 'expected': wanted, 'called': bool(tried), 'inputsMatch': match if tried else None,
                           'given': [ {k: c['arguments'].get(k) for k in wanted} for c in tried][:3]})
    return {'task': run['task'], 'mode': mode, 'repetition': run.get('repetition', 0), 'passed': bool(run['done']),
            'hostError': run.get('hostError'), 'stage': stage, 'offeredExact': exact, 'needed': per_unit,
            'calls': sum(c['ok'] is not None for c in calls),
            'failedCalls': [{k: c[k] for k in ('tool', 'name', 'arguments', 'code', 'detail', 'issues', 'attribution')}
                            for c in calls if c['ok'] is False], 'writes': writes}


def summary(reviews):
    modes = list(dict.fromkeys(r['mode'] for r in reviews))
    rows = []
    for mode in modes:
        group = [r for r in reviews if r['mode'] == mode]
        units = [u for r in group for u in r['needed'] if u['equivalent'] is None or u['equivalent']]
        possible = [u for r in group for u in r['needed']]
        stages = {}
        for r in group:
            stages[r['stage']] = stages.get(r['stage'], 0) + 1
        failed = [c for r in group for c in r['failedCalls']]
        attrs = {}
        for c in failed:
            attrs[c['attribution']] = attrs.get(c['attribution'], 0) + 1
        writes = [w for r in group for w in r['writes']]
        rows.append({'mode': mode, 'runs': len(group), 'passed': sum(r['passed'] for r in group),
                     'needed': len(possible), 'neededAvailable': len(units),
                     'given': sum(u['given'] for u in units), 'called': sum(u['called'] for u in units),
                     'succeeded': sum(u['succeeded'] for u in units),
                     'businessCalls': sum(r['calls'] for r in group), 'failedCalls': len(failed), 'attribution': attrs,
                     'stages': stages, 'writeItems': len(writes), 'writeCalled': sum(w['called'] for w in writes),
                     'writeInputsMatch': sum(bool(w['inputsMatch']) for w in writes),
                     'offeredExact': all(r['offeredExact'] for r in group)})
    return rows


STAGES = ['passed', 'A0', 'A', 'B', 'C', 'D', 'E-write', 'E-format', 'E-content']
ATTRS = ['model:schema', 'model:function', 'model:ungrounded', 'model:described', 'source:undocumented', 'business', 'unclear']


def markdown(rows, reviews, title):
    pct = lambda a, b: f'{a}/{b} ({a / b:.0%})' if b else '—'
    lines = [f'# 호출 단계 리뷰 — {title}', '',
             '단계: A0 API에 해당 기능 없음 · A 필요한 함수를 받지 못함 · B 받았지만 부르지 않음 · C 불렀지만 성공 못 함 · '
             'D 한도·오류로 중단 · E-write 쓰기 입력·change set · E-format 숫자는 있으나 표기 · E-content 답 내용 누락', '',
             '## 필요한 함수: 확보 → 호출 → 성공', '',
             '| 방식 | 통과 | 필요한 함수(API에 있음/전체) | 모델에게 줌 | 불렀음 | 성공 | 확보 기록 |', '|---|---|---|---|---|---|---|']
    for r in rows:
        lines.append(f"| {r['mode']} | {r['passed']}/{r['runs']} | {r['neededAvailable']}/{r['needed']} | "
                     f"{pct(r['given'], r['neededAvailable'])} | {pct(r['called'], r['neededAvailable'])} | "
                     f"{pct(r['succeeded'], r['neededAvailable'])} | {'단계별 기록' if r['offeredExact'] else '불러오기·검색 결과로 추정'} |")
    lines += ['', '## 실패한 실행이 처음 막힌 단계', '', '| 방식 | ' + ' | '.join(STAGES) + ' |', '|---' * (len(STAGES) + 1) + '|']
    for r in rows:
        lines.append(f"| {r['mode']} | " + ' | '.join(str(r['stages'].get(s, 0)) for s in STAGES) + ' |')
    lines += ['', '## 실패한 업무 호출의 원인', '', '| 방식 | 업무 호출 | 실패 | ' + ' | '.join(ATTRS) + ' |', '|---' * (len(ATTRS) + 3) + '|']
    for r in rows:
        lines.append(f"| {r['mode']} | {r['businessCalls']} | {r['failedCalls']} | " + ' | '.join(str(r['attribution'].get(a, 0)) for a in ATTRS) + ' |')
    if any(r['writeItems'] for r in rows):
        lines += ['', '## 쓰기 입력(과업이 기대한 change set 항목)', '', '| 방식 | 기대 항목 | 불렀음 | 입력 일치 |', '|---|---|---|---|']
        for r in rows:
            if r['writeItems']:
                lines.append(f"| {r['mode']} | {r['writeItems']} | {r['writeCalled']} | {r['writeInputsMatch']} |")
    lines += ['', '## 실패한 호출 목록', '']
    for review in reviews:
        for call in review['failedCalls']:
            detail = (call['detail'] or '').replace('\n', ' ')[:220]
            issues = f" issues {json.dumps(call['issues'], ensure_ascii=False)[:200]}" if call.get('issues') else ''
            lines.append(f"- `{call['attribution']}` {review['task']} [{review['mode']}] {review['repetition'] + 1}회차 · "
                         f"`{call['name']}` `{json.dumps(call['arguments'], ensure_ascii=False)[:200]}` → {call['code']}: {detail}{issues}")
    write_lines = [f"- {review['task']} [{review['mode']}] {review['repetition'] + 1}회차 · `{w['tool']}` 기대 {json.dumps(w['expected'], ensure_ascii=False)} · "
                   f"{'부르지 않음' if not w['called'] else ('일치' if w['inputsMatch'] else '불일치: ' + json.dumps(w['given'], ensure_ascii=False)[:200])}"
                   for review in reviews for w in review['writes'] if not w['inputsMatch']]
    if write_lines:
        lines += ['', '## 기대와 다른 쓰기 입력', ''] + write_lines
    return '\n'.join(lines) + '\n'


async def build_catalog(acom_path, facade_path, functions=None):
    """functions: the `<runs>.functions.json` written when the runs started (what the model saw); without
    it the definitions are built from the current conversion code, which can describe more than the runs saw."""
    acom = json.loads(Path(acom_path).read_text())['items']
    facade = json.loads(Path(facade_path).read_text())['items']
    if functions:
        seen = json.loads(Path(functions).read_text())
        return Catalog(acom, facade, seen.get('acom') or {}, seen.get('facade') or {})
    acom_views = await model_view(acom, 'acom')
    facade_views = await model_view(facade, 'facade', WORDS, True)
    return Catalog(acom, facade, acom_views, facade_views)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('runs', nargs='+')
    parser.add_argument('--repo', default=None)
    parser.add_argument('--acom', default=str(HERE.parents[1] / 'artifacts' / 'acommerce' / 'manifest-acom.json'))
    parser.add_argument('--facade', default=str(HERE.parents[1] / 'artifacts' / 'acommerce' / 'manifest-facade.json'))
    parser.add_argument('--functions', type=Path, help='functions the runs saw (default: <first runs file>.functions.json)')
    parser.add_argument('--out', type=Path)
    parser.add_argument('--json', type=Path)
    options = parser.parse_args()
    if options.functions is None:
        candidate = Path(str(Path(options.runs[0]).with_suffix('')) + '.functions.json')
        options.functions = candidate if candidate.exists() else None
    if options.repo is None:
        from stack import REPO
        options.repo = REPO
    tasks = tasks_from(options.repo)
    fmap = facade_map(options.repo)
    catalog = asyncio.run(build_catalog(options.acom, options.facade, options.functions))
    reviews = []
    for path in options.runs:
        for line in Path(path).read_text().splitlines():
            run = json.loads(line)
            if run.get('type') != 'run':
                continue
            task = tasks.get(run['task'])
            run['turnsText'] = (task or {}).get('turns') or []
            reviews.append(review_run(run, task, catalog, fmap))
    rows = summary(reviews)
    text = markdown(rows, reviews, ', '.join(Path(p).stem for p in options.runs))
    basis = (f'판정 기준 함수 정의: `{options.functions.name}`(실행 때 모델이 본 것)' if options.functions
             else '판정 기준 함수 정의: 지금의 변환 코드(실행 때의 기록 없음: 그 뒤 보충한 설명이 섞일 수 있음)')
    text = text.replace('\n\n', '\n\n' + basis + '\n\n', 1)
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
