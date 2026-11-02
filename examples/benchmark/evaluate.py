"""Run the benchmark: tasks x scales x languages x modes against a real model.

python examples/benchmark/evaluate.py --split dev --scales small --languages go \
    --modes spec-tools,spec-prompt,a2api --output artifacts/benchmark/runs/dev-1.jsonl

Each run resets the server, records usage/time/calls, and checks the final answer and
store diff. Failures (including provider context overflow) are kept, never rerun.
"""

from __future__ import annotations

import argparse
import asyncio
from contextlib import ExitStack
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from application import converted  # noqa: E402
from modes import A2API, SpecPrompt, SpecTools, compact  # noqa: E402
from servers import GENERATED, admin, build, process, python_server  # noqa: E402
from tasks import assess, fingerprint, tasks  # noqa: E402

DEFAULT_BASE_URL = 'https://qwen-api-xgen.x2bee.com/v1'
DEFAULT_MODEL = 'nvidia/Muse-Glimmer-30B-NVFP4'
MAX_TURNS, TASK_SECONDS, REQUEST_SECONDS = 12, 180, 120
# The model card's settings for nvidia/Muse-Glimmer-30B-NVFP4: temperature 1.0, top_p 0.95, top_k 64,
# thinking on, high reasoning strength (the chat template's `reasoning_strength`: low, medium, high, xhigh).
# Runs before 2026-11-02 used temperature 0 and the template default (high).
RECOMMENDED = {'temperature': 1.0, 'top_p': 0.95, 'top_k': 64, 'reasoning_strength': 'high'}
# Per model request; the hidden reasoning counts too. Largest step seen without a cap: 3,843 tokens.
MAX_TOKENS = 8192


class ModelError(Exception):
    pass


def model_arguments(parser):
    """CLI options for the model request; defaults are the model card's settings."""
    parser.add_argument('--temperature', type=float, default=RECOMMENDED['temperature'])
    parser.add_argument('--top-p', type=float, default=RECOMMENDED['top_p'])
    parser.add_argument('--top-k', type=int, default=RECOMMENDED['top_k'])
    parser.add_argument('--reasoning-strength', choices=['low', 'medium', 'high', 'xhigh'], default=RECOMMENDED['reasoning_strength'])
    parser.add_argument('--reasoning-history', choices=['turn', 'all', 'none'], default='turn',
                        help='earlier reasoning sent back with assistant messages: within the current user turn (default), '
                             'always, or never (runs before 2026-11-02)')
    parser.add_argument('--max-tokens', type=int, default=MAX_TOKENS, help='output cap per model request; 0 = none')


def sampling(options):
    """Request fields for the model settings in options (see model_arguments)."""
    return {'temperature': options.temperature, 'top_p': options.top_p, 'top_k': options.top_k,
            'chat_template_kwargs': {'reasoning_strength': options.reasoning_strength}}


def model_header(options):
    return {'sampling': sampling(options), 'reasoningHistory': options.reasoning_history, 'maxTokens': options.max_tokens or None}


def assistant_message(message, keep_reasoning):
    """The assistant turn to send back: content, tool calls and (the chat template renders it) its reasoning."""
    assistant = {'role': 'assistant', 'content': message.get('content') or ''}
    if message.get('tool_calls'):
        assistant['tool_calls'] = message['tool_calls']
    reasoning = message.get('reasoning') or message.get('reasoning_content')
    if keep_reasoning and reasoning:
        assistant['reasoning_content'] = reasoning
    return assistant


def chat(base_url, model, messages, tools, *, api_key=None, timeout=REQUEST_SECONDS, max_tokens=MAX_TOKENS, sampling=None):
    headers = {'Content-Type': 'application/json'}
    if api_key:
        headers['Authorization'] = 'Bearer ' + api_key
    settings = sampling if sampling is not None else {**{k: v for k, v in RECOMMENDED.items() if k != 'reasoning_strength'},
                                                     'chat_template_kwargs': {'reasoning_strength': RECOMMENDED['reasoning_strength']}}
    payload = {'model': model, 'messages': messages, 'stream': False, **settings}
    if max_tokens is not None:  # None: no output cap (the provider's own limit)
        payload['max_tokens'] = max_tokens
    if tools:
        payload.update(tools=tools, tool_choice='auto')
    request = Request(base_url.rstrip('/') + '/chat/completions', headers=headers, data=json.dumps(payload).encode())
    try:
        with urlopen(request, timeout=timeout) as response:
            return json.loads(response.read())
    except HTTPError as error:
        detail = error.read().decode('utf-8', 'replace').lower()
        error.close()
        if error.code == 400 and ('context length' in detail or 'maximum' in detail and 'token' in detail):
            raise ModelError('CONTEXT_OVERFLOW') from None
        raise ModelError('MODEL_HTTP_' + str(error.code)) from None
    except (URLError, TimeoutError, OSError):
        raise ModelError('MODEL_CONNECTION_FAILED') from None


def wait_for_model(base_url, model, api_key=None, *, limit=1800):
    """Gate: do not START a run while the provider is down. Never retries a started run."""
    started = time.monotonic()
    while True:
        try:
            chat(base_url, model, [{'role': 'user', 'content': 'ping'}], None, api_key=api_key, timeout=30, max_tokens=8)
            return round(time.monotonic() - started, 1)
        except ModelError:
            if time.monotonic() - started > limit:
                raise
            time.sleep(30)


async def run_task(executor, question, *, base_url, model, api_key=None, request=None, options=None):
    run = {'steps': [], 'toolCalls': [], 'calls': [], 'answer': '', 'usage': {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}}
    started = time.monotonic()
    try:
        tick = time.monotonic()
        # Hosts pre-select from the user's request, not from the application's format rule.
        run['setup'] = await executor.setup(request if request is not None else question)
        run['setupSeconds'] = round(time.monotonic() - tick, 4)
        system = executor.system()
        messages = [{'role': 'system', 'content': system}, {'role': 'user', 'content': question}]
        run['systemBytes'] = len(system.encode())
        for _ in range(MAX_TURNS):
            tools = executor.tools()
            remaining = TASK_SECONDS - (time.monotonic() - started)
            if remaining <= 0:
                raise ModelError('TASK_TIMEOUT')
            tick = time.monotonic()
            response = await asyncio.to_thread(chat, base_url, model, messages, tools, api_key=api_key,
                                               timeout=min(REQUEST_SECONDS, remaining),
                                               max_tokens=(options.max_tokens or None) if options else MAX_TOKENS,
                                               sampling=sampling(options) if options else None)
            choice = response['choices'][0]
            message = choice['message']
            usage = response.get('usage') or {}
            run['steps'].append({'seconds': round(time.monotonic() - tick, 3), 'finish': choice.get('finish_reason'),
                                 'usage': usage, 'toolBytes': len(compact(tools).encode()) if tools else 0,
                                 'offered': [tool['function']['name'] for tool in tools or []],
                                 'reasoning': (message.get('reasoning') or message.get('reasoning_content') or '')[:3000]})
            for key in run['usage']:
                run['usage'][key] += usage.get(key) or 0
            if choice.get('finish_reason') == 'length':
                raise ModelError('MODEL_OUTPUT_TRUNCATED')
            calls = message.get('tool_calls') or []
            # One user turn here, so 'turn' and 'all' keep the same reasoning.
            messages.append(assistant_message(message, keep_reasoning=(options.reasoning_history != 'none') if options else True))
            if not calls:
                run['answer'] = message.get('content') or ''
                break
            for call in calls:
                name = call['function']['name']
                tick = time.monotonic()
                try:
                    arguments = json.loads(call['function'].get('arguments') or '{}')
                    if not isinstance(arguments, dict):
                        raise ValueError()
                except ValueError:
                    text, business = compact({'error': 'arguments must be a JSON object'}), None
                    arguments = None
                else:
                    text, business = await executor.call(name, arguments)
                run['toolCalls'].append({'name': name, 'arguments': arguments, 'resultBytes': len(text.encode()), 'result': text[:3000],
                                         'seconds': round(time.monotonic() - tick, 4), 'business': business})
                if isinstance(business, list):  # a2api_batch: each call it made
                    run['calls'].extend(entry for entry in business if entry)
                elif business:
                    run['calls'].append(business)
                messages.append({'role': 'tool', 'tool_call_id': call['id'], 'name': name, 'content': text})
        else:
            raise ModelError('MODEL_TURN_LIMIT')
    except ModelError as error:
        run['hostError'] = str(error)
    run['seconds'] = round(time.monotonic() - started, 3)
    run['modelSeconds'] = round(sum(step['seconds'] for step in run['steps']), 3)
    run['toolSeconds'] = round(sum(call['seconds'] for call in run['toolCalls']), 3)
    run['modelRequests'] = len(run['steps'])
    run['firstPromptTokens'] = run['steps'][0]['usage'].get('prompt_tokens') if run['steps'] else None
    return run


def executor_for(mode, scale, spec, origin, app, ops, options):
    if mode == 'spec-tools':
        return SpecTools(scale, spec, origin)
    if mode == 'spec-prompt':
        return SpecPrompt(scale, spec, origin)
    # 'a2api-plain' is the same host with hints='none' (no result-shape text), for presentation comparisons.
    # 'a2api-all' exposes the whole catalog whenever it fits max_tool_bytes (no pre-selection).
    # 'a2api-index-summary/-graph/-names/-hybrid/-batch' use ToolSession.index() (grouped by resource) instead of auto().
    hints = 'none' if mode == 'a2api-plain' else options.hints
    all_bytes = options.max_tool_bytes if mode == 'a2api-all' else None
    variant = {'a2api-index-summary': {'detail': 'summary', 'related': 0}, 'a2api-index-graph': {'detail': 'summary', 'related': 5},
               'a2api-index-names': {'detail': 'names', 'related': 5},
               'a2api-index-hybrid': {'detail': 'names', 'related': 0, 'preselect': 8},
               'a2api-index-batch': {'detail': 'names', 'related': 0, 'batch': True}}.get(mode)
    index = None if variant is None else {**variant, 'group': lambda entry: ops.get(entry['id'], 'other').split('.')[0]}
    executor = A2API(app, ops, max_tool_bytes=options.max_tool_bytes, search_limit=options.search_limit, hints=hints,
                     all_bytes=all_bytes, index=index)
    executor.mode = mode
    return executor


async def evaluate(options):
    output = options.output
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise SystemExit('Choose a new output path; earlier runs are never overwritten.')
    done = set()
    for earlier in options.resume_from:
        # Continue an interrupted pass: runs already recorded (passed or failed) are never repeated.
        for line in Path(earlier).read_text().splitlines():
            record = json.loads(line)
            if record.get('type') == 'run':
                done.add((record['repetition'], record['scale'], record['language'], record['task'], record['mode']))
    selected = [item for item in tasks(options.split) if not options.tasks or item['id'] in options.tasks.split(',')]
    modes = options.modes.split(',')
    import subprocess
    git = lambda *args: subprocess.run(['git', *args], cwd=HERE, capture_output=True, text=True).stdout.strip()
    header = {'type': 'header', 'startedAt': datetime.now(timezone.utc).isoformat(), 'model': options.model,
              'gitCommit': git('rev-parse', 'HEAD'), 'gitDirty': bool(git('status', '--porcelain', '--', '../../src', '.')),
              'baseUrl': options.base_url, 'split': options.split, 'taskFingerprint': fingerprint(options.split),
              'tasks': [item['id'] for item in selected], 'scales': options.scales, 'languages': options.languages,
              'modes': modes, 'repetitions': options.repetitions, 'firstRepetition': options.first_repetition, 'maxToolBytes': options.max_tool_bytes,
              **model_header(options),
              'searchLimit': options.search_limit, 'hints': options.hints, 'limits': {'turns': MAX_TURNS, 'taskSeconds': TASK_SECONDS},
              'resumedFrom': [str(path) for path in options.resume_from]}
    with output.open('a') as sink:
        def write(record):
            sink.write(json.dumps(record, ensure_ascii=False) + '\n')
            sink.flush()
        write(header)
        counter = 0
        for repetition in range(options.first_repetition, options.first_repetition + options.repetitions):
            for scale in options.scales.split(','):
                spec = json.loads((GENERATED / scale / 'openapi.json').read_text())
                for language in options.languages.split(','):
                    with ExitStack() as stack:
                        if language == 'python':
                            origin = stack.enter_context(python_server(scale))
                        else:
                            command, env = build(scale, language)
                            origin = stack.enter_context(process(language, command, env))
                        tick = time.monotonic()
                        app, ops = converted(scale, language, None if language == 'python' else origin)
                        write({'type': 'group', 'repetition': repetition, 'scale': scale, 'language': language,
                               'convertSeconds': round(time.monotonic() - tick, 4)})
                        for index, item in enumerate(selected):
                            order = modes[(index + repetition) % len(modes):] + modes[:(index + repetition) % len(modes)]
                            for mode in order:
                                if (repetition, scale, language, item['id'], mode) in done:
                                    continue
                                counter += 1
                                waited = await asyncio.to_thread(wait_for_model, options.base_url, options.model,
                                                                 os.environ.get(options.api_key_env))
                                admin(origin, 'reset')
                                before = admin(origin, 'state')
                                executor = executor_for(mode, scale, spec, origin, app, ops, options)
                                run = await run_task(executor, item['question'], base_url=options.base_url,
                                                     model=options.model, api_key=os.environ.get(options.api_key_env),
                                                     request=item['request'], options=options)
                                after = admin(origin, 'state')
                                run.update(type='run', task=item['id'], split=item['split'], kind=item['kind'], scale=scale, waitedForModel=waited,
                                           language=language, mode=mode, repetition=repetition,
                                           assessment=assess(item, run['answer'], before, after, run['calls']))
                                if run.get('hostError'):
                                    run['assessment']['passed'] = False
                                    run['assessment']['failures'].append('HOST:' + run['hostError'])
                                write(run)
                                print(json.dumps({'n': counter, 'task': item['id'], 'scale': scale, 'language': language,
                                                  'mode': mode, 'passed': run['assessment']['passed'],
                                                  'failures': run['assessment']['failures'], 'tokens': run['usage']['total_tokens'],
                                                  'seconds': run['seconds']}, ensure_ascii=False), flush=True)
                        admin(origin, 'reset')
        write({'type': 'footer', 'finishedAt': datetime.now(timezone.utc).isoformat(), 'runs': counter})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default=os.environ.get('A2API_MODEL_BASE_URL', DEFAULT_BASE_URL))
    parser.add_argument('--model', default=os.environ.get('A2API_MODEL', DEFAULT_MODEL))
    model_arguments(parser)
    parser.add_argument('--api-key-env', default='A2API_MODEL_API_KEY')
    parser.add_argument('--split', choices=['dev', 'holdout'], required=True)
    parser.add_argument('--tasks', default='')
    parser.add_argument('--scales', default='small,medium,large')
    parser.add_argument('--languages', default='python,spring,go,rust')
    parser.add_argument('--modes', default='spec-tools,spec-prompt,a2api')
    parser.add_argument('--repetitions', type=int, default=1)
    parser.add_argument('--first-repetition', type=int, default=0, help='repetition index of the first pass (rotates mode order)')
    parser.add_argument('--max-tool-bytes', type=int, default=32000)
    parser.add_argument('--search-limit', type=int, default=5)
    parser.add_argument('--hints', choices=['none', 'shape', 'typed'], default=None, help='ToolSession hints (library default if omitted)')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--resume-from', type=Path, action='append', default=[],
                        help='earlier JSONL of the same pass; its runs are skipped, never repeated')
    asyncio.run(evaluate(parser.parse_args()))


if __name__ == '__main__':
    main()
