"""An OpenAI-compatible chat endpoint that answers through the Codex CLI (`codex exec`), so a-commerce's
own agent can run on a model Codex serves (e.g. gpt-6-luna) with nothing else changed.

python examples/acommerce/codex_model.py --port 7020 --model gpt-6-luna [--effort medium] [--log calls.jsonl]
# then: A2API_MODEL_BASE_URL=http://127.0.0.1:7020/v1 A2API_MODEL=gpt-6-luna python examples/acommerce/stack.py up

Each `POST /v1/chat/completions` becomes one `codex exec` run:
- the request's system messages replace Codex's own instructions (`model_instructions_file`); the other
  messages are the prompt;
- a `response_format` schema is asked for the way a-commerce's `structured_output: prompt` does it (the
  schema in the instructions, the JSON parsed from the answer): Codex sends schemas in strict mode,
  which the agent's schemas (optional fields, free-form `args`) do not fit;
- Codex's tools are switched off and it runs read-only in an empty folder, ephemeral, without the
  user's config (auth still comes from CODEX_HOME), and a first instruction line says there are no tools.
  What remains of Codex's own prompt is a fixed overhead per call, measured with `--overhead` and
  written to the log;
- `temperature` and `max_tokens` are not passed (Codex sets them); streamed requests get a 400, so the
  agent answers unstreamed.

Usage in the response is Codex's: prompt_tokens includes that fixed overhead.
"""

from __future__ import annotations

import argparse
import http.server
import json
import os
from pathlib import Path
import subprocess
import tempfile
import threading
import time
import uuid

CODEX = os.environ.get('CODEX_BIN', '/usr/lib/chatgpt/resources/codex')
OFF = ('apps', 'browser_use', 'browser_use_external', 'computer_use', 'image_generation', 'in_app_browser', 'multi_agent',
       'plugins', 'remote_plugin', 'shell_tool', 'skill_search', 'sleep_tool', 'tool_suggest', 'unified_exec',
       'view_image', 'goals', 'code_mode_host', 'hooks')
JSON_RULE = 'Answer with one JSON object and nothing else. It must follow this JSON Schema:\n'
# Codex still lists a code-mode `exec` tool; without this line the model sometimes tries it first (it fails
# closed), which doubles the input tokens of that call.
NO_TOOLS = 'You have no tools in this conversation: never call a tool, answer directly.'


def text_of(content):
    if isinstance(content, list):
        return '\n'.join(part.get('text', '') for part in content if isinstance(part, dict))
    return content or ''


def parts(body):
    """(instructions, prompt) from a chat completions request."""
    messages = body.get('messages') or []
    system = [text_of(m.get('content')) for m in messages if m.get('role') == 'system']
    rest = [m for m in messages if m.get('role') != 'system']
    out = (body.get('response_format') or {})
    if out.get('type') == 'json_schema':
        system.append(JSON_RULE + json.dumps((out.get('json_schema') or {}).get('schema') or {}, ensure_ascii=False))
    elif out.get('type') == 'json_object':
        system.append('Answer with one JSON object and nothing else.')
    if len(rest) == 1 and rest[0].get('role') == 'user':
        prompt = text_of(rest[0].get('content'))
    else:
        prompt = '\n\n'.join(f"[{m.get('role')}]\n{text_of(m.get('content'))}" for m in rest)
    return '\n\n'.join([NO_TOOLS] + [s for s in system if s]), prompt or '(no message)'


def json_answer(text):
    """The JSON object in an answer (a code fence or words around it are dropped), else the text."""
    start, end = text.find('{'), text.rfind('}')
    if start < 0 or end <= start:
        return text
    try:
        return json.dumps(json.loads(text[start:end + 1]), ensure_ascii=False)
    except ValueError:
        return text


class Codex:
    def __init__(self, model, effort, workdir, timeout):
        self.model, self.effort, self.workdir, self.timeout = model, effort, workdir, timeout

    def run(self, instructions, prompt):
        """(answer text, usage, error) of one codex exec run."""
        with tempfile.NamedTemporaryFile('w', suffix='.md', dir=self.workdir, delete=False) as file:
            file.write(instructions or 'Answer the request.')
        try:
            args = [CODEX, 'exec', '--ignore-user-config', '--ephemeral', '--skip-git-repo-check', '-s', 'read-only',
                    '-C', self.workdir, '-m', self.model, '-c', f'model_reasoning_effort="{self.effort}"',
                    '-c', f'model_instructions_file="{file.name}"', '-c', 'web_search="disabled"',
                    '-c', 'include_permissions_instructions=false', '-c', 'include_environment_context=false',
                    '-c', 'include_collaboration_mode_instructions=false', '--json']
            for feature in OFF:
                args += ['--disable', feature]
            done = subprocess.run(args + ['-'], input=prompt, capture_output=True, text=True, timeout=self.timeout)
        except subprocess.TimeoutExpired:
            return None, {}, f'codex exec took over {self.timeout} seconds'
        finally:
            os.unlink(file.name)
        answer, usage, error = None, {}, None
        for line in done.stdout.splitlines():
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if event.get('type') == 'item.completed' and event['item'].get('type') == 'agent_message':
                answer = event['item'].get('text')
            elif event.get('type') == 'turn.completed':
                usage = event.get('usage') or {}
            elif event.get('type') in ('turn.failed', 'error'):
                error = json.dumps(event.get('error') or event.get('message'), ensure_ascii=False)[:600]
        if answer is None and not error:
            error = f'codex exec exited {done.returncode} without an answer: {done.stderr[-400:]}'
        return answer, usage, error


def serve(port, codex, log, overhead, host='127.0.0.1'):
    lock = threading.Lock()

    def record(entry):
        if log:
            with lock, open(log, 'a') as out:
                out.write(json.dumps(entry, ensure_ascii=False) + '\n')

    class Handler(http.server.BaseHTTPRequestHandler):
        protocol_version = 'HTTP/1.1'

        def log_message(self, *args):
            pass

        def reply(self, status, body):
            raw = json.dumps(body, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self):
            if self.path.rstrip('/').endswith('/models'):
                return self.reply(200, {'object': 'list', 'data': [{'id': codex.model, 'object': 'model'}]})
            self.reply(404, {'error': {'message': 'not found'}})

        def do_POST(self):
            if not self.path.rstrip('/').endswith('/chat/completions'):
                return self.reply(404, {'error': {'message': 'not found'}})
            body = json.loads(self.rfile.read(int(self.headers.get('Content-Length') or 0)) or b'{}')
            if body.get('stream'):
                return self.reply(400, {'error': {'message': 'This endpoint answers unstreamed only.', 'type': 'invalid_request_error'}})
            instructions, prompt = parts(body)
            tick = time.monotonic()
            answer, usage, error = codex.run(instructions, prompt)
            seconds = round(time.monotonic() - tick, 2)
            schema = ((body.get('response_format') or {}).get('json_schema') or {}).get('name')
            record({'at': time.strftime('%Y-%m-%dT%H:%M:%S'), 'schema': schema, 'seconds': seconds, 'ok': error is None,
                    'error': error, 'usage': usage, 'overhead': overhead, 'instructionsChars': len(instructions),
                    'promptChars': len(prompt)})
            if error:
                return self.reply(502, {'error': {'message': error, 'type': 'codex_error'}})
            if body.get('response_format'):
                answer = json_answer(answer)
            prompt_tokens = usage.get('input_tokens', 0)
            completion = usage.get('output_tokens', 0) + usage.get('reasoning_output_tokens', 0)
            self.reply(200, {'id': 'chatcmpl-' + uuid.uuid4().hex, 'object': 'chat.completion', 'created': int(time.time()),
                             'model': codex.model,
                             'choices': [{'index': 0, 'message': {'role': 'assistant', 'content': answer}, 'finish_reason': 'stop'}],
                             'usage': {'prompt_tokens': prompt_tokens, 'completion_tokens': completion,
                                       'total_tokens': prompt_tokens + completion,
                                       'prompt_tokens_details': {'cached_tokens': usage.get('cached_input_tokens', 0)},
                                       'completion_tokens_details': {'reasoning_tokens': usage.get('reasoning_output_tokens', 0)}}})

    server = http.server.ThreadingHTTPServer((host, port), Handler)
    print(json.dumps({'endpoint': f'http://{host}:{port}/v1', 'model': codex.model, 'effort': codex.effort,
                      'overheadTokens': overhead}), flush=True)
    server.serve_forever()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--port', type=int, default=7020)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--model', default='gpt-6-luna')
    parser.add_argument('--effort', default='medium', help="Codex model_reasoning_effort (gpt-6-luna's default is medium)")
    parser.add_argument('--timeout', type=int, default=300, help='seconds one codex exec run may take')
    parser.add_argument('--log', type=Path, help='one JSON line per call: seconds, usage, errors')
    parser.add_argument('--overhead', action='store_true',
                        help="first measure the input tokens Codex adds to an empty request (logged with every call)")
    options = parser.parse_args()
    workdir = tempfile.mkdtemp(prefix='codex-model-')
    codex = Codex(options.model, options.effort, workdir, options.timeout)
    overhead = None
    if options.overhead:
        _, usage, error = codex.run('Answer with the word ok.', 'ok')
        overhead = usage.get('input_tokens') if not error else None
    serve(options.port, codex, options.log, overhead, options.host)


if __name__ == '__main__':
    main()
