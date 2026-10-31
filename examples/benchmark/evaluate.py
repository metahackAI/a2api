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


class ModelError(Exception):
    pass


def chat(base_url, model, messages, tools, *, api_key=None, timeout=REQUEST_SECONDS, max_tokens=2048):
    headers = {'Content-Type': 'application/json'}
    if api_key:
        headers['Authorization'] = 'Bearer ' + api_key
    payload = {'model': model, 'messages': messages, 'temperature': 0, 'max_tokens': max_tokens, 'stream': False}
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


async def run_task(executor, question, *, base_url, model, api_key=None, request=None):
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
                                               timeout=min(REQUEST_SECONDS, remaining))
            choice = response['choices'][0]
            message = choice['message']
            usage = response.get('usage') or {}
            run['steps'].append({'seconds': round(time.monotonic() - tick, 3), 'finish': choice.get('finish_reason'),
                                 'usage': usage, 'toolBytes': len(compact(tools).encode()) if tools else 0})
            for key in run['usage']:
                run['usage'][key] += usage.get(key) or 0
            if choice.get('finish_reason') == 'length':
                raise ModelError('MODEL_OUTPUT_TRUNCATED')
            calls = message.get('tool_calls') or []
            assistant = {'role': 'assistant', 'content': message.get('content') or ''}
            if calls:
                assistant['tool_calls'] = calls
            messages.append(assistant)
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
                if business:
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
    return A2API(app, ops, max_tool_bytes=options.max_tool_bytes, search_limit=options.search_limit)


async def evaluate(options):
    output = options.output
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise SystemExit('Choose a new output path; earlier runs are never overwritten.')
    selected = [item for item in tasks(options.split) if not options.tasks or item['id'] in options.tasks.split(',')]
    modes = options.modes.split(',')
    import subprocess
    git = lambda *args: subprocess.run(['git', *args], cwd=HERE, capture_output=True, text=True).stdout.strip()
    header = {'type': 'header', 'startedAt': datetime.now(timezone.utc).isoformat(), 'model': options.model,
              'gitCommit': git('rev-parse', 'HEAD'), 'gitDirty': bool(git('status', '--porcelain', '--', '../../src', '.')),
              'baseUrl': options.base_url, 'split': options.split, 'taskFingerprint': fingerprint(options.split),
              'tasks': [item['id'] for item in selected], 'scales': options.scales, 'languages': options.languages,
              'modes': modes, 'repetitions': options.repetitions, 'maxToolBytes': options.max_tool_bytes,
              'searchLimit': options.search_limit, 'limits': {'turns': MAX_TURNS, 'taskSeconds': TASK_SECONDS}}
    with output.open('a') as sink:
        def write(record):
            sink.write(json.dumps(record, ensure_ascii=False) + '\n')
            sink.flush()
        write(header)
        counter = 0
        for repetition in range(options.repetitions):
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
                                counter += 1
                                waited = await asyncio.to_thread(wait_for_model, options.base_url, options.model,
                                                                 os.environ.get(options.api_key_env))
                                admin(origin, 'reset')
                                before = admin(origin, 'state')
                                executor = executor_for(mode, scale, spec, origin, app, ops, options)
                                run = await run_task(executor, item['question'], base_url=options.base_url,
                                                     model=options.model, api_key=os.environ.get(options.api_key_env),
                                                     request=item['request'])
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
    parser.add_argument('--api-key-env', default='A2API_MODEL_API_KEY')
    parser.add_argument('--split', choices=['dev', 'holdout'], required=True)
    parser.add_argument('--tasks', default='')
    parser.add_argument('--scales', default='small,medium,large')
    parser.add_argument('--languages', default='python,spring,go,rust')
    parser.add_argument('--modes', default='spec-tools,spec-prompt,a2api')
    parser.add_argument('--repetitions', type=int, default=1)
    parser.add_argument('--max-tool-bytes', type=int, default=32000)
    parser.add_argument('--search-limit', type=int, default=5)
    parser.add_argument('--output', type=Path, required=True)
    asyncio.run(evaluate(parser.parse_args()))


if __name__ == '__main__':
    main()
