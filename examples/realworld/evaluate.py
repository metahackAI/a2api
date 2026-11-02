"""RealWorld (Conduit): the official OpenAPI handed over as functions vs a2api converted from the
OpenAPI document or from each real implementation's code (Spring, Go Gin, Rust Axum, Python FastAPI).

The code is only read (static importers); calls go to conduit.py, an in-memory server that follows
the specification, in the flavor of the implementation the binding was read from.

python examples/realworld/evaluate.py verify /path/to/realworld-checkouts
python examples/realworld/evaluate.py run /path/to/realworld-checkouts --split dev --output out.jsonl
"""

from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from types import SimpleNamespace
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / 'benchmark'))

from a2api import ExecutionContext, HTTPDeployment, ToolSession, convert  # noqa: E402
from a2api.importers import (FastAPISourceImporter, GoSourceImporter, OpenAPIImporter, RustSourceImporter,  # noqa: E402
                             SpringSourceImporter, load_openapi)
from a2api.tool_session import SEARCH_NAME  # noqa: E402
from compare import norm  # noqa: E402
from conduit import serve  # noqa: E402
from conduit_tasks import TASKS, answer_json, changes, fingerprint  # noqa: E402
from evaluate import DEFAULT_BASE_URL, DEFAULT_MODEL, compact, model_arguments, model_header, run_task, wait_for_model  # noqa: E402

CONTEXT = ExecutionContext('jake', 'conduit', frozenset())
TOKEN = {'Authorization': 'Token token-jake'}
SYSTEM = '''You help the signed-in user (username: jake) of Conduit, a blogging site, through its API tools. Answer in Korean.
- Use the tools to look things up; report only what they return. Never invent slugs, ids or values.
- If the request does not say which item to act on, ask instead of calling a tool.
- Do only the changes that were asked for. Do not repeat a failed call; report the failure.'''
SEARCH_RULE = '\n- If a function you need is not in your tool list, use a2api_search; selected functions become callable on the next step.'
SOURCES = {
    'a2api-openapi': ('spec', None, '/api'),
    'a2api-spring': ('spring', (SpringSourceImporter, 'spring-boot-realworld-example-app/src/main/java'), '/api'),
    'a2api-go': ('go', (GoSourceImporter, 'golang-gin-realworld-example-app'), ''),
    'a2api-rust': ('rust', (RustSourceImporter, 'realworld-axum-sqlx/src'), ''),
    'a2api-python': ('python', (FastAPISourceImporter, 'fastapi-realworld-example-app/app'), ''),
}


def http(origin, method, path, query=None, body=None, headers=None, timeout=15):
    from urllib.error import HTTPError, URLError
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode()
    request = Request(origin + path + ('?' + urlencode(query) if query else ''), data=data, method=method,
                      headers={**({'Content-Type': 'application/json'} if data is not None else {}), **(headers or {})})
    try:
        with urlopen(request, timeout=timeout) as response:
            status, raw = response.status, response.read()
    except HTTPError as error:
        status, raw = error.code, error.read()
        error.close()
    except (URLError, TimeoutError, OSError):
        return 599, 'connection failed'
    text = raw.decode('utf-8', 'replace')
    try:
        return status, json.loads(text) if text else None
    except ValueError:
        return status, text[:500]


def application(mode, root, origin):
    """(app, {capability id: (METHOD, path template)}) for one a2api mode."""
    flavor, source, prefix = SOURCES[mode]
    if source is None:
        importer = OpenAPIImporter(load_openapi(root / 'realworld/specs/api/openapi.yml')[0], namespace='conduit',
                                   methods={'GET', 'POST', 'PUT', 'DELETE'})
        records = [r for r in importer.iter_operations() if r.status == 'imported']
        method_of = lambda r: r.method.upper()
    else:
        cls, directory = source
        importer = cls(root / directory, namespace='conduit')
        records = [r for r in importer.iter_operations() if r.status == 'imported']
        method_of = lambda r: r.method
    operations = {r.operation_id: {'effect': 'read' if method_of(r) == 'GET' else 'write'} for r in records}
    app = convert(importer, operations=operations, deployment=HTTPDeployment(
        origin, path_prefix=prefix, credential_provider=lambda context: dict(TOKEN), timeout_ms=10000, deadline_ms=15000))
    identifier = lambda r: r.capability.id if source is None else r.id
    routes = {identifier(r): (method_of(r), norm(r.path), r.path) for r in records}
    return app, routes


class SpecTools:
    """Every OpenAPI operation as one function; raw HTTP results (the usual way to hand over a spec)."""
    mode = 'spec-tools'

    def __init__(self, document, origin):
        self.origin, self.operations, self._tools = origin, {}, []
        components = document['components']

        def resolve(node):
            if isinstance(node, dict):
                if '$ref' in node:
                    target = document
                    for part in node['$ref'].lstrip('#/').split('/'):
                        target = target[part]
                    return resolve(target)
                return {key: resolve(value) for key, value in node.items()}
            return [resolve(item) for item in node] if isinstance(node, list) else node
        del components
        for path, item in document['paths'].items():
            for method, operation in item.items():
                operation = resolve(operation)
                properties, required, params = {}, [], []
                for parameter in operation.get('parameters', []):
                    schema = dict(parameter['schema'])
                    if parameter.get('description'):
                        schema['description'] = parameter['description']
                    properties[parameter['name']] = schema
                    params.append((parameter['name'], parameter['in']))
                    if parameter.get('required'):
                        required.append(parameter['name'])
                body = operation.get('requestBody')
                if body:
                    properties['body'] = body['content']['application/json']['schema']
                    required.append('body')
                name = operation['operationId']
                self.operations[name] = (method.upper(), path, params)
                self._tools.append({'type': 'function', 'function': {
                    'name': name, 'description': operation.get('summary') or operation.get('description', ''),
                    'parameters': {'type': 'object', 'properties': properties, 'required': required, 'additionalProperties': False}}})

    async def setup(self, question):
        return {'functions': len(self._tools)}

    def system(self):
        return SYSTEM

    def tools(self):
        return self._tools

    async def call(self, name, arguments):
        if name not in self.operations:
            return compact({'error': 'unknown function'}), None
        method, template, params = self.operations[name]
        path, query = template, {}
        for parameter, location in params:
            if parameter in arguments:
                if location == 'path':
                    path = path.replace('{' + parameter + '}', quote(str(arguments[parameter]), safe=''))
                else:
                    query[parameter] = str(arguments[parameter]).lower() if isinstance(arguments[parameter], bool) else str(arguments[parameter])
        if '{' in path:
            return compact({'error': 'missing path parameter'}), None
        status, body = await asyncio.to_thread(http, self.origin, method, '/api' + path, query, arguments.get('body'), TOKEN)
        return compact({'status': status, 'body': body}), {'method': method, 'path': norm(template), 'ok': 200 <= status < 300}


class A2API:
    def __init__(self, mode, app, routes):
        self.mode, self.app, self.routes, self.session = mode, app, routes, None

    async def setup(self, question):
        self.session = ToolSession(self.app, CONTEXT)
        result = await self.session.auto(question)
        return {'strategy': result['strategy'], 'functions': len(self.session.tools())}

    def system(self):
        return SYSTEM + (SEARCH_RULE if self.session.strategy != 'all' else '')

    def tools(self):
        return self.session.tools()

    async def call(self, name, arguments):
        binding = None if name == SEARCH_NAME else self.session.binding(name)
        payload = await self.session.call(name, arguments)
        text = self.session.render(payload)
        if binding is None:
            return text, None
        method, path, _ = self.routes.get(binding['id'], ('?', '?', ''))
        executed = not (payload.get('error', {}).get('code') == 'INVALID_INPUT' and 'status' not in payload)
        return text, {'method': method, 'path': path, 'ok': payload.get('status') == 'succeeded', 'executed': executed}


def servers():
    flavors = {}
    for flavor in ('spec', 'spring', 'go', 'rust', 'python'):
        flavors[flavor] = serve(flavor)
    return flavors


def state(origin):
    return http(origin, 'GET', '/__state')[1]


def verify(root):
    """Without a model: every converted operation answers through its flavor, with valid outputs."""
    flavors = servers()
    report = {}
    probes = {  # (METHOD, normalized path) -> (path values in order, body)
        ('GET', '/tags'): ([], None), ('GET', '/articles'): ([], None), ('GET', '/articles/feed'): ([], None),
        ('GET', '/articles/{}'): (['go-error-handling'], None), ('GET', '/articles/{}/comments'): (['writing-a-tiny-compiler'], None),
        ('GET', '/profiles/{}'): (['alice'], None), ('GET', '/user'): ([], None),
        ('POST', '/profiles/{}/follow'): (['carol'], None), ('DELETE', '/profiles/{}/follow'): (['carol'], None),
        ('POST', '/articles/{}/favorite'): (['go-error-handling'], None), ('DELETE', '/articles/{}/favorite'): (['go-error-handling'], None),
        ('PUT', '/user'): ([], {'user': {'bio': 'probe'}}),
        ('POST', '/users/login'): ([], {'user': {'email': 'jake@conduit.test', 'password': 'jakejake'}}),
        ('POST', '/users'): ([], {'user': {'username': 'probe', 'email': 'probe@conduit.test', 'password': 'probepw12'}}),  # Go: min=4
        ('POST', '/articles'): ([], {'article': {'title': 'Probe article', 'description': 'd', 'body': 'b', 'tagList': ['x']}}),
        ('PUT', '/articles/{}'): (['training-for-a-marathon'], {'article': {'body': 'updated'}}),
        ('POST', '/articles/{}/comments'): (['go-error-handling'], {'comment': {'body': 'probe comment'}}),
        ('DELETE', '/articles/{}/comments/{}'): (['writing-a-tiny-compiler', '4'], None),
        ('DELETE', '/articles/{}'): (['draft-notes'], None),
    }
    for mode, (flavor, _, _) in SOURCES.items():
        _, origin = flavors[flavor]
        http(origin, 'POST', '/__reset')
        app, routes = application(mode, root, origin)
        results = {}
        for capability, (method, path, raw) in sorted(routes.items(), key=lambda item: item[1][0] != 'GET'):
            values, body = probes[(method, path)]
            schema = app.describe(capability)['inputSchema']['properties']
            arguments = {}
            if 'path' in schema:
                names = re.findall(r'\{([^{}]+)\}', raw)  # in route order
                arguments['path'] = dict(zip(names, values))
                for name in names:
                    if schema['path']['properties'][name].get('type') == 'integer':
                        arguments['path'][name] = int(arguments['path'][name])
            if body is not None:
                arguments['body'] = body
            result = app.invoke(capability, arguments, context=CONTEXT)
            results[f'{method} {path}'] = result['status'] if result['status'] == 'succeeded' else result['error']['code'] + ': ' + result['error']['detail'][:120]
        report[mode] = results
        bad = {key: value for key, value in results.items() if value != 'succeeded'}
        print(f'{mode}: {len(results) - len(bad)}/{len(results)} succeeded', json.dumps(bad, ensure_ascii=False)[:600])
    return report


async def evaluate(options):
    if options.output.exists():
        raise SystemExit('Choose a new output path; earlier runs are never overwritten.')
    tasks = [t for t in TASKS if t['split'] == options.split and (not options.only or t['id'] in options.only.split(','))]
    modes = options.modes.split(',')
    flavors = servers()
    document = load_openapi(options.root / 'realworld/specs/api/openapi.yml')[0]
    git = lambda *a: subprocess.run(['git', *a], cwd=HERE, capture_output=True, text=True).stdout.strip()
    with options.output.open('a') as sink:
        def write(record):
            sink.write(json.dumps(record, ensure_ascii=False, default=list) + '\n')
            sink.flush()
        write({'type': 'header', 'startedAt': datetime.now(timezone.utc).isoformat(), 'model': options.model, 'split': options.split,
               **model_header(options),
               'modes': modes, 'tasks': [t['id'] for t in tasks], 'fingerprint': fingerprint(options.split), 'gitCommit': git('rev-parse', 'HEAD')})
        for repetition in range(options.repeat):
            for index, task in enumerate(tasks):
                order = modes[(index + repetition) % len(modes):] + modes[:(index + repetition) % len(modes)]
                for mode in order:
                    await asyncio.to_thread(wait_for_model, options.base_url, options.model)
                    flavor = 'spec' if mode == 'spec-tools' else SOURCES[mode][0]
                    _, origin = flavors[flavor]
                    http(origin, 'POST', '/__reset')
                    if mode == 'spec-tools':
                        executor = SpecTools(document, origin)
                    else:
                        app, routes = application(mode, options.root, origin)
                        executor = A2API(mode, app, routes)
                    before = state(origin)
                    run = await run_task(executor, task['question'], base_url=options.base_url, model=options.model, request=task['request'],
                                         options=options)
                    after = state(origin)
                    context = SimpleNamespace(json=answer_json(run['answer']), answer=run['answer'], diff=changes(before, after),
                                              calls=[c for c in run['calls'] if c.get('executed', True)])
                    passed = bool(task['check'](context)) and not run.get('hostError')
                    run.update(type='run', task=task['id'], kind=task['kind'], mode=mode, repetition=repetition, passed=passed,
                               diff={k: {kk: sorted(map(list, vv)) for kk, vv in v.items()} for k, v in context.diff.items()})
                    write(run)
                    print(json.dumps({'task': task['id'], 'mode': mode, 'passed': passed, 'error': run.get('hostError'),
                                      'tokens': run['usage']['total_tokens'], 'seconds': run['seconds'],
                                      'calls': [f"{c['method']} {c['path']} {'ok' if c['ok'] else 'x'}" for c in run['calls']]},
                                     ensure_ascii=False), flush=True)
        write({'type': 'footer', 'finishedAt': datetime.now(timezone.utc).isoformat()})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['verify', 'run', 'fingerprint'])
    parser.add_argument('root', type=Path, nargs='?')
    parser.add_argument('--base-url', default=os.environ.get('A2API_MODEL_BASE_URL', DEFAULT_BASE_URL))
    parser.add_argument('--model', default=os.environ.get('A2API_MODEL', DEFAULT_MODEL))
    model_arguments(parser)
    parser.add_argument('--split', choices=['dev', 'holdout'], default='dev')
    parser.add_argument('--modes', default='spec-tools,a2api-openapi,a2api-spring,a2api-go,a2api-rust,a2api-python')
    parser.add_argument('--only', default='')
    parser.add_argument('--repeat', type=int, default=1)
    parser.add_argument('--output', type=Path)
    options = parser.parse_args()
    if options.command == 'fingerprint':
        print(fingerprint('holdout'))
    elif options.command == 'verify':
        verify(options.root)
    else:
        asyncio.run(evaluate(options))


if __name__ == '__main__':
    main()
