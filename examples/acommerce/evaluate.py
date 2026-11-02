"""Run a-commerce's own task set (eval/tasks) through tool layers driven by our host, and score them
with a-commerce's rules (scoring.py). Their own agent harness is run with `cargo xtask eval`.

python examples/acommerce/evaluate.py --set design --modes facade-all,acom-all,a2api-acom,a2api-facade \
    --output artifacts/acommerce/runs/ours-design-1.jsonl

Modes (same model, system prompt, limits and scoring):
  facade-all    every screen of the legacy facade as a function (raw catalog)
  acom-all      every A-Commerce tool as a function (raw catalog; may exceed the model context)
  a2api-acom    the A-Commerce catalog converted by a2api (ToolCatalogImporter) through ToolSession
  a2api-facade  the facade converted by a2api, with the host's legacy metadata (legacy_facade.py)
  a2api-facade-all  the converted facade, every screen given at once like facade-all (no search): the
                    conversion's names, words and descriptions against the raw screens, nothing else
  a2api-acom-index  the converted catalog as an index in the system prompt (name + first summary sentence,
                    by domain); the model loads what it needs with a2api_load (ToolSession.index)
  a2api-acom-graph  the index, and each result names functions that take IDs it returned (related=5)
  a2api-acom-names  names only by domain, with related next steps
  a2api-acom-names-norelated  names only by domain, no related next steps
  a2api-acom-hybrid  names only by domain, and the host search's 8 candidates loaded up front (as auto())
  a2api-acom-names-batch  names only, and a2api_batch (several independent calls in one step; each call
                    counts toward the tool-call limit)
  …-guard           any a2api mode with ToolSession(variant_note=3): the third read of one function for the
                    same target with other conditions carries a note to answer from what was found
Writes are previewed into one change set per task (a person approves later); nothing is approved.
"""

from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timezone
import glob
import json
import os
from pathlib import Path
import sys
import time

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / 'benchmark'))

from a2api import ExecutionContext, HTTPDeployment, ToolSession, convert  # noqa: E402
from a2api.importers import ToolCatalogImporter  # noqa: E402
from a2api.importers.catalog import snake  # noqa: E402
from a2api.tool_session import BATCH_NAME, LOAD_NAME, SEARCH_NAME  # noqa: E402
from legacy_facade import VOCABULARY, WORDS, error_detail, facade_options  # noqa: E402
from evaluate import (DEFAULT_BASE_URL, DEFAULT_MODEL, ModelError, assistant_message, chat, model_arguments,  # noqa: E402
                      model_header, sampling, trim_reasoning, wait_for_model)
from scoring import score  # noqa: E402
from stack import COMMERCE, REPO, call, token  # noqa: E402

CLOCK = '2026-11-06T11:00'
LIMITS = {'model_calls': 12, 'tool_calls': 20, 'seconds': 120}
RESULT_CHARS = 6000
SYSTEM = '''You are the back-office assistant of the Northwind online store, working for the operator.
Store time: Friday, November 6, 2026, 11:00 (America/New_York). Prices are in USD.
- Use the tools to look things up. Never invent numbers, ids or results; report what the tools return.
- A change you make is only a preview that goes into one change set for a person to approve. You cannot approve,
  publish, pay or send anything yourself; say what is waiting for approval.
- If something does not exist or a rule forbids it, say so plainly instead of guessing.
- Answer the operator directly and briefly, with the key numbers.'''
SEARCH_RULE = '\n- If a function you need is not in your tool list, use a2api_search to find it; selected functions become callable on the next step.'
INDEX_VARIANTS = {'index': {'detail': 'summary', 'related': 0}, 'graph': {'detail': 'summary', 'related': 5},
                  'names': {'detail': 'names', 'related': 5}, 'names-norelated': {'detail': 'names', 'related': 0},
                  'hybrid': {'detail': 'names', 'related': 0, 'preselect': 8},
                  'names-batch': {'detail': 'names', 'related': 0, 'batch': True}}


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def clip(text):
    return text if len(text) <= RESULT_CHARS else text[:RESULT_CHARS] + '…[truncated]'


class Host:
    """Per-task host state: caller token, one lazily created change set."""

    def __init__(self, agent_token, task):
        self.token, self.task, self.change_set_id = agent_token, task, None

    def change_set(self):
        if self.change_set_id is None:
            status, body = call(COMMERCE, 'POST', '/v1/platform/change-sets',
                                {'title': self.task['id'], 'request_text': self.task['turns'], 'interpretation': [],
                                 'conversation_id': None}, bearer=self.token)
            if status != 200:
                raise RuntimeError(f'change set: {status} {body}')
            self.change_set_id = body['id']
        return self.change_set_id

    def read_change_set(self):
        if self.change_set_id is None:
            return None
        status, body = call(COMMERCE, 'GET', f'/v1/platform/change-sets/{self.change_set_id}', bearer=self.token)
        return body if status == 200 else None


class RawCatalog:
    """Every catalog entry as a function, called by name; raw results (the usual way to hand over an API)."""

    def __init__(self, mode, items, host, facade):
        self.mode, self.host, self.facade = mode, host, facade
        self.kinds = {item['tool']: item['kind'] for item in items}
        self._tools = [{'type': 'function', 'function': {'name': item['tool'], 'description': item['summary'],
                                                         'parameters': item['input_schema']}} for item in items]

    async def setup(self, request):
        return {'functions': len(self._tools)}

    async def turn(self, line):
        return None

    def system(self):
        return SYSTEM

    def tools(self):
        return self._tools

    async def call(self, name, arguments, call_id=None):
        if name not in self.kinds:
            return compact({'error': 'unknown function'}), None
        body = {'input': arguments}
        if not self.facade and self.kinds[name] != 'read':
            body['change_set_id'] = await asyncio.to_thread(self.host.change_set)
        path = f'/v1/tools/{name}' + ('?set=facade' if self.facade else '')
        status, result = await asyncio.to_thread(call, COMMERCE, 'POST', path, body, bearer=self.host.token)
        return clip(compact({'status': status, 'body': result})), (name, 200 <= status < 300)


class A2APIExecutor:
    def __init__(self, mode, app, names, host, search_streak=None, index=None, max_tool_bytes=16000, variant_note=None,
                 whole=False):
        self.mode, self.app, self.names, self.host = mode, app, names, host
        self.search_streak, self.session, self.max_tool_bytes = search_streak, None, max_tool_bytes
        self.variant_note, self.whole = variant_note, whole
        index = dict(index) if index is not None else None
        self.batch = bool(index and index.pop('batch', False))
        self.index, self.index_text = index, None  # ToolSession.index() options, or None for auto()

    async def setup(self, request):
        self.session = ToolSession(self.app, ExecutionContext('adm_sj', 'store_northwind', frozenset()),
                                   max_search_streak=self.search_streak, max_tool_bytes=self.max_tool_bytes,
                                   batch=self.batch, variant_note=self.variant_note)
        if self.index is not None:
            result = await self.session.index(request, **self.index)
            self.index_text = result['text']
            return {'strategy': 'index', 'functions': result['functions'], 'indexChars': len(result['text']),
                    'hostCalls': self.session.stats}
        result = await (self.session.auto(request, all_bytes=self.max_tool_bytes) if self.whole else self.session.auto(request))
        return {'strategy': result['strategy'], 'functions': len(self.session.tools()), 'hostCalls': self.session.stats}

    async def turn(self, line):
        """A later turn: the host searches the new request too (no model turn); earlier functions stay."""
        await self.session.focus(line)  # a new request: related next steps ranked again, variant count reset
        if self.session.strategy == 'index':
            return None
        if self.session.strategy != 'search':
            return None
        found = await self.session.select(' '.join(line.split())[:1000])
        return [item['name'] for item in found['selected']]

    def system(self):
        if self.session.strategy == 'index':
            return SYSTEM + '\n\n' + self.index_text
        return SYSTEM + (SEARCH_RULE if self.session.strategy != 'all' else '')

    def tools(self):
        return self.session.tools()

    async def call(self, name, arguments, call_id=None):
        if name == BATCH_NAME and self.batch:
            payload = await self.session.call(name, arguments, request_id=call_id)
            text = self.session.render(payload, max_chars=RESULT_CHARS)
            calls = []  # every call in the batch, as if made directly
            for item in payload.get('batch') or []:
                binding = self.session.binding(item['name'])
                if binding is not None:
                    calls.append((self.names.get(binding['id'], binding['id']), item.get('status') == 'succeeded'))
                else:
                    calls.append(None)
            return text, calls
        business = name not in (SEARCH_NAME, LOAD_NAME)
        payload = await self.session.call(name, arguments, request_id=call_id if business else None)
        # Read after the call: a function called straight from the index is loaded by the call itself.
        binding = self.session.binding(name) if business else None
        # a2api bounds the result structurally (largest arrays first) instead of cutting the JSON text.
        text = self.session.render(payload, max_chars=RESULT_CHARS)
        if binding is None:
            return text, None
        return text, (self.names.get(binding['id'], binding['id']), payload.get('status') == 'succeeded')


def a2api_app(items, host, *, facade):
    """The catalog converted by a2api. Writes preview into the host's change set (a host value)."""
    if facade:
        options, vocabulary = facade_options(items), VOCABULARY
    else:
        options = {item['tool']: {'effect': 'read' if item['kind'] == 'read' else 'write'} for item in items}
        vocabulary = None
    source = ToolCatalogImporter(items, namespace='facade' if facade else 'acom', words=WORDS if facade else None)

    def values(context, call_info):
        if facade:
            return {'query': {'set': 'facade'}}
        return {'body': {'change_set_id': host.change_set()}} if call_info['effect'] == 'write' else {}
    app = convert(source, operations=options, deployment=HTTPDeployment(
        COMMERCE, credential_provider=lambda context: {'Authorization': 'Bearer ' + host.token},
        request_values=values, error_detail=error_detail, timeout_ms=30000, deadline_ms=35000,
        max_response_bytes=4 * 1048576), vocabulary=vocabulary)
    names = {record.id: record.operation_id for record in source.iter_operations()}
    return app, names, source


async def run_turns(executor, task, options):
    run = {'steps': [], 'toolCalls': [], 'tools': [], 'usage': {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0},
           'replies': []}
    started = time.monotonic()
    try:
        run['setup'] = await executor.setup(task['turns'][0])
        messages = [{'role': 'system', 'content': executor.system()}]
        for number, line in enumerate(task['turns']):
            if number:
                run.setdefault('turnSelections', []).append(await executor.turn(line))
            messages.append({'role': 'user', 'content': line})
            turn_started, tool_calls = time.monotonic(), 0
            for _ in range(LIMITS['model_calls']):
                remaining = LIMITS['seconds'] - (time.monotonic() - turn_started)
                if remaining <= 0:
                    raise ModelError('TURN_TIMEOUT')
                tick = time.monotonic()
                try:
                    # The model's earlier reasoning goes back within the user turn (its tool loop), for the
                    # last --reasoning-keep steps by default; never across turns.
                    trim_reasoning(messages, options.reasoning_history, options.reasoning_keep)
                    offered = executor.tools()
                    response = await asyncio.to_thread(chat, options.base_url, options.model, messages, offered,
                                                       timeout=min(120, remaining), max_tokens=options.max_tokens or None,
                                                       sampling=sampling(options))
                except ModelError as error:
                    # A request cut by the turn's own time limit is that limit, not a provider failure.
                    if str(error) == 'MODEL_CONNECTION_FAILED' and time.monotonic() - turn_started >= LIMITS['seconds'] - 1:
                        raise ModelError('TURN_TIMEOUT') from None
                    raise
                choice = response['choices'][0]
                message, usage = choice['message'], response.get('usage') or {}
                run['steps'].append({'seconds': round(time.monotonic() - tick, 3), 'finish': choice.get('finish_reason'),
                                     'usage': usage, 'toolBytes': len(compact(executor.tools()).encode()),
                                     'contentChars': len(message.get('content') or ''),
                                     # What the model wrote at this step (its reasoning field, when the server
                                     # returns one), so a trace shows why it called what it called.
                                     'reasoning': (message.get('reasoning') or message.get('reasoning_content') or '')[:3000],
                                     'content': (message.get('content') or '')[:2000],
                                     'calls': [item['id'] for item in message.get('tool_calls') or []],
                                     'offered': [tool['function']['name'] for tool in offered]})
                for key in run['usage']:
                    run['usage'][key] += usage.get(key) or 0
                if choice.get('finish_reason') == 'length':
                    # Keep what the model was writing when it hit the output limit (diagnosis only).
                    content = message.get('content') or ''
                    run['truncated'] = {'content': content[:2000] + ('…' + content[-1500:] if len(content) > 3500 else content[2000:]),
                                        'toolCalls': [compact(item.get('function'))[:1500] for item in message.get('tool_calls') or []]}
                    raise ModelError('MODEL_OUTPUT_TRUNCATED')
                calls = message.get('tool_calls') or []
                messages.append(assistant_message(message, keep_reasoning=options.reasoning_history != 'none'))
                if not calls:
                    run['replies'].append(message.get('content') or '')
                    break
                for item in calls:
                    tool_calls += 1
                    name = item['function']['name']
                    tick = time.monotonic()
                    try:
                        arguments = json.loads(item['function'].get('arguments') or '{}')
                        if not isinstance(arguments, dict):
                            raise ValueError()
                    except ValueError:
                        text, business = compact({'error': 'arguments must be a JSON object'}), None
                        arguments = None
                    else:
                        size = len(arguments['calls']) if name == BATCH_NAME and isinstance(arguments.get('calls'), list) else 1
                        text, business = (await executor.call(name, arguments, item['id'])
                                          if tool_calls + size - 1 <= LIMITS['tool_calls']
                                          else (compact({'error': 'tool call limit reached for this turn'}), None))
                    run['toolCalls'].append({'id': item['id'], 'turn': number, 'name': name, 'arguments': arguments, 'result': text[:3000],
                                             'resultBytes': len(text.encode()), 'seconds': round(time.monotonic() - tick, 3)})
                    if isinstance(business, list):  # a2api_batch: each call counts toward the tool-call limit
                        tool_calls += max(0, len(business) - 1)
                        run['tools'].extend(entry for entry in business if entry)
                    elif business:
                        run['tools'].append(business)
                    messages.append({'role': 'tool', 'tool_call_id': item['id'], 'name': name, 'content': text})
            else:
                raise ModelError('MODEL_CALL_LIMIT')
    except ModelError as error:
        run['hostError'] = str(error)
    run['seconds'] = round(time.monotonic() - started, 3)
    run['modelRequests'] = len(run['steps'])
    run['firstPromptTokens'] = run['steps'][0]['usage'].get('prompt_tokens') if run['steps'] else None
    run['reply'] = run['replies'][-1] if run['replies'] else ''
    return run


def load_tasks(task_set):
    tasks = []
    for path in sorted(glob.glob(str(REPO / 'eval' / 'tasks' / task_set / '*.yml'))):
        tasks.extend(yaml.safe_load(Path(path).read_text()) or [])
    return tasks


def prepare(task, admin_token):
    # Every run starts from the demo store: facade writes apply at once, so a read task must not
    # see what an earlier run changed.
    status, body = call(COMMERCE, 'POST', '/v1/platform/demo/reset', bearer=admin_token, timeout=120)
    if status != 200:
        raise RuntimeError(f'reset: {status} {body}')
    status, body = call(COMMERCE, 'PUT', '/v1/platform/demo-clock', {'now': CLOCK, 'is_running': False}, bearer=admin_token)
    if status != 200:
        raise RuntimeError(f'clock: {status} {body}')


async def evaluate(options):
    if options.output.exists():
        raise SystemExit('Choose a new output path; earlier runs are never overwritten.')
    options.output.parent.mkdir(parents=True, exist_ok=True)
    tasks = [t for t in load_tasks(options.set) if not options.only or t['id'] in options.only.split(',')]
    # Runs an earlier, interrupted pass already recorded (passed or failed) are never repeated, except a run
    # the provider never answered at all (an outage, not the model's result).
    done_before = {(run['task'], run['mode'], run.get('repetition', 0))
                   for earlier in options.resume_from for run in (json.loads(line) for line in earlier.read_text().splitlines())
                   if run.get('type') == 'run' and not (run.get('hostError') and run.get('modelRequests') == 0)}
    modes = options.modes.split(',')
    agent_token, admin_token = token('admin', agent=True), token('admin')
    manifests = {}
    for name, query in (('acom', ''), ('facade', '?set=facade')):
        status, body = call(COMMERCE, 'GET', '/v1/tools' + query, bearer=agent_token)
        manifests[name] = body['items']
    import subprocess
    git = lambda *a: subprocess.run(['git', *a], cwd=HERE, capture_output=True, text=True).stdout.strip()
    header = {'type': 'header', 'startedAt': datetime.now(timezone.utc).isoformat(), 'model': options.model,
              'set': options.set, 'modes': modes, 'tasks': [t['id'] for t in tasks], 'limits': LIMITS,
              'searchStreak': options.search_streak, **model_header(options),
              'resumedFrom': [str(path) for path in options.resume_from],
              'maxToolBytes': options.max_tool_bytes, 'indexGroup': options.index_group,
              'resultChars': RESULT_CHARS, 'gitCommit': git('rev-parse', 'HEAD'), 'catalog': {k: len(v) for k, v in manifests.items()},
              'acommerceCommit': subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=REPO, capture_output=True, text=True).stdout.strip()}
    # The functions the model will see, for call_review.py to judge failed calls against (not what a later
    # conversion describes).
    from function_snapshot import model_views
    Path(str(options.output.with_suffix('')) + '.functions.json').write_text(
        json.dumps(await model_views(manifests['acom'], manifests['facade']), ensure_ascii=False))
    with options.output.open('a') as sink:
        def write(record):
            sink.write(json.dumps(record, ensure_ascii=False) + '\n')
            sink.flush()
        write(header)
        for repetition in range(options.repeat):
            for index, task in enumerate(tasks):
                order = modes[(index + repetition) % len(modes):] + modes[:(index + repetition) % len(modes)]
                for mode in order:
                    if (task['id'], mode, repetition) in done_before:
                        continue
                    await asyncio.to_thread(wait_for_model, options.base_url, options.model)
                    prepare(task, admin_token)
                    host = Host(agent_token, task)
                    facade = 'facade' in mode
                    items = manifests['facade' if facade else 'acom']
                    if mode.startswith('a2api'):
                        app, names, source = a2api_app(items, host, facade=facade)
                        guard = mode.endswith('-guard')
                        base = mode[:-len('-guard')] if guard else mode
                        variant = base.split('-', 2)[2] if base.count('-') >= 2 else None
                        whole = variant == 'all'
                        variant = None if whole else variant
                        index = None
                        if variant:
                            depth = 2 if options.index_group == 'resource' else 1  # catalog address: domain.resource.verb
                            # ' › ', not '.': a dotted heading reads as part of the function name.
                            domains = {f"{source.namespace}.{snake(item['tool'])}": ' › '.join(item['address'].split('.')[:depth])
                                       for item in items if 'address' in item}
                            index = {**INDEX_VARIANTS[variant], 'relations': source.relations(),
                                     'group': lambda entry, domains=domains: domains.get(entry['id'], 'other')}
                        executor = A2APIExecutor(mode, app, names, host, options.search_streak, index, options.max_tool_bytes,
                                                 3 if guard else None, whole)
                    else:
                        executor = RawCatalog(mode, items, host, facade)
                    run = await run_turns(executor, task, options)
                    change_set = host.read_change_set()
                    done, missing, precision, recall, unchecked = score(
                        task, tool_names_scored=not facade, reply=run['reply'], blocks=[], tools=run['tools'],
                        change_set=change_set)
                    if run.get('hostError'):
                        done = False
                        missing = missing + ['HOST:' + run['hostError']]
                    run.update(type='run', task=task['id'], kind=task['kind'], mode=mode, repetition=repetition,
                               done=done, missing=missing, precision=precision, recall=recall, unchecked=unchecked,
                               changeSet={'id': host.change_set_id, 'state': (change_set or {}).get('state'),
                                          'items': [i.get('tool') for i in (change_set or {}).get('items') or []]})
                    write(run)
                    print(json.dumps({'task': task['id'], 'mode': mode, 'done': done, 'missing': missing[:3],
                                      'tokens': run['usage']['total_tokens'], 'seconds': run['seconds'],
                                      'tools': [t[0] for t in run['tools']]}, ensure_ascii=False), flush=True)
        write({'type': 'footer', 'finishedAt': datetime.now(timezone.utc).isoformat()})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default=os.environ.get('A2API_MODEL_BASE_URL', DEFAULT_BASE_URL))
    parser.add_argument('--model', default=os.environ.get('A2API_MODEL', DEFAULT_MODEL))
    parser.add_argument('--set', choices=['design', 'held_out'], default='design')
    parser.add_argument('--modes', default='facade-all,acom-all,a2api-acom,a2api-facade')
    parser.add_argument('--only', default='')
    parser.add_argument('--repeat', type=int, default=1)
    parser.add_argument('--search-streak', type=int, default=None, help='ToolSession max_search_streak for a2api modes')
    # Runs before 2026-11-01 17:00 used --max-tokens 2048 --max-tool-bytes 16000 --index-group domain; runs from
    # then until 2026-11-02 used --max-tokens 0 --temperature 0 --reasoning-history none.
    model_arguments(parser)
    parser.add_argument('--max-tool-bytes', type=int, default=32000, help='ToolSession max_tool_bytes for a2api modes')
    parser.add_argument('--index-group', choices=['domain', 'resource'], default='resource',
                        help='index headings: catalog domain, or domain.resource')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--resume-from', type=Path, action='append', default=[],
                        help='earlier JSONL of the same pass; its runs are skipped, never repeated')
    parser.add_argument('--turn-seconds', type=int, default=LIMITS['seconds'],
                        help='time limit per user turn; raise it only to match a slower model server')
    options = parser.parse_args()
    LIMITS['seconds'] = options.turn_seconds
    asyncio.run(evaluate(options))


if __name__ == '__main__':
    main()
