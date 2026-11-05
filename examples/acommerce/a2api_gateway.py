"""a2api as a gateway in front of a-commerce: the legacy facade, converted, in its own manifest format.

    python examples/acommerce/a2api_gateway.py --port 7011 --commerce http://127.0.0.1:7001
    # then point the agent's commerce URL at the gateway, e.g.
    A2API_AGENT_COMMERCE_URL=http://127.0.0.1:7011 python examples/acommerce/stack.py up

a-commerce's own agent reads tools from `GET /v1/tools?set=facade` and calls `POST
/v1/tools/{tool}?set=facade` with `{"input": ...}`. This gateway answers those two with the facade
converted by a2api (readable names and words from `legacy_facade.VOCABULARY`, summaries read from
the screens' code, snake_case names) and runs each call through `ConvertedAPI.invoke`, which turns
names and code words back into the screen's fields and codes, and the screen's codes in results into
words. The agent, its search, planner and limits stay the same; only the tool representation changes.
Each converted entry keeps the screen's other manifest fields as they are (`address`, `kind`, ...).
Every other request (change sets, store settings, the A-Commerce tools) passes through unchanged.

The facade manifest is read once, with the bearer token of the first `GET /v1/tools?set=facade`
(or `--token`), so the gateway needs no credentials of its own; each call forwards its caller's token.

    python examples/acommerce/a2api_gateway.py --dump converted.json --manifest facade-manifest.json
writes the converted manifest and, per converted tool, the screen it calls (no service needed).
"""

from __future__ import annotations

import argparse
import http.server
import json
import os
from pathlib import Path
import re
import sys
import threading
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from a2api import ExecutionContext, HTTPDeployment, convert  # noqa: E402
from a2api.importers import ToolCatalogImporter  # noqa: E402
from legacy_facade import HANDLES, RENAME, VOCABULARY, WORDS, error_detail, facade_options  # noqa: E402

CALLER = threading.local()
CLASSES = {'INVALID_INPUT': 'invalid_input', 'UPSTREAM_VALIDATION_FAILED': 'invalid_input',
           'RESOURCE_NOT_FOUND': 'not_found', 'PERMISSION_DENIED': 'forbidden', 'UNAUTHENTICATED': 'unauthenticated',
           'UPSTREAM_CONFLICT': 'invalid_state', 'RATE_LIMITED': 'rate_limited',
           'UPSTREAM_UNAVAILABLE': 'upstream_unavailable', 'DEADLINE_EXCEEDED': 'upstream_unavailable'}


def forward(origin, method, path, body, headers, timeout=60):
    request = Request(origin + path, data=body, method=method, headers=headers)
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.status, response.read(), response.headers.get('Content-Type', 'application/json')
    except HTTPError as error:
        raw = error.read()
        error.close()
        return error.code, raw, error.headers.get('Content-Type', 'application/json')
    except (URLError, TimeoutError, OSError):
        return 502, json.dumps({'error': {'code': 'gateway_upstream', 'class': 'upstream_unavailable',
                                          'message': 'The commerce service did not answer.'}}).encode(), 'application/json'


class Facade:
    """The converted facade: manifest entries and calls, built once from the facade manifest items."""

    def __init__(self, items, commerce, lookup=True):
        self.lookup = lookup
        source = ToolCatalogImporter(items, namespace='facade', words=WORDS)
        self.app = convert(source, operations=facade_options(items), vocabulary=VOCABULARY, deployment=HTTPDeployment(
            commerce, credential_provider=lambda context: {'Authorization': CALLER.authorization},
            request_values=lambda context, call: {'query': {'set': 'facade'}}, error_detail=error_detail,
            timeout_ms=30000, deadline_ms=35000, max_response_bytes=4 * 1048576))
        self.entries, self.ids, self.screens = [], {}, {}
        originals = {item['tool']: item for item in items}
        for record in source.iter_operations():
            if record.status != 'imported':
                raise SystemExit(f'facade screen {record.operation_id} was not converted: {record.diagnostics}')
            descriptor = self.app.describe(record.id)
            name = record.id.split('.', 1)[1]
            self.ids[name], self.screens[name] = record.id, record.operation_id
            # Only the representation changes; address, kind and the other manifest fields stay the screen's.
            self.entries.append({**originals[record.operation_id], 'tool': name, 'path': f'/v1/tools/{name}',
                                 'summary': descriptor['summary'],
                                 'input_schema': descriptor['inputSchema']['properties']['body']})

    def manifest(self):
        return {'items': self.entries, 'total': len(self.entries)}

    def resolve(self, name, given):
        """A number people see (`20402`, `#20402`) where the screen takes a key: look the key up with the
        screen the HANDLES table names, and use it when exactly one row matches."""
        names = {screen: tool for tool, screen in self.screens.items()}
        for field, (screen, by, key) in HANDLES.get(self.screens[name], {}).items():
            field, by, key = (RENAME.get(item, item) for item in (field, by, key))
            value = given.get(field) if isinstance(given, dict) else None
            if not isinstance(value, str) or not re.fullmatch(r'#?[0-9]+', value.strip()) or screen not in names:
                continue
            found = self.app.invoke(self.ids[names[screen]], {'body': {by: value.strip()}},
                                    context=ExecutionContext('agent', 'store', frozenset()))
            rows = next((item for item in (found.get('data') or {}).values() if isinstance(item, list)), []) \
                if found['status'] == 'succeeded' and isinstance(found.get('data'), dict) else []
            keys = {row.get(key) for row in rows if isinstance(row, dict) and row.get(key)}
            if len(keys) == 1:
                given = {**given, field: keys.pop()}
        return given

    def call(self, name, payload):
        if name not in self.ids:
            return 404, {'error': {'code': 'unknown_tool', 'class': 'not_found', 'message': f'There is no tool {name}.'}}
        given = payload.get('input', {}) if isinstance(payload, dict) else {}
        if self.lookup:
            given = self.resolve(name, given)
        result = self.app.invoke(self.ids[name], {'body': given}, context=ExecutionContext('agent', 'store', frozenset()))
        if result['status'] == 'succeeded':
            return 200, result['data']
        problem = result['error']
        message = problem['detail']
        if problem.get('issues'):
            message += ' Issues: ' + json.dumps(problem['issues'], ensure_ascii=False, separators=(',', ':'))
        return problem['status'], {'error': {'code': problem['code'].lower(), 'class': CLASSES.get(problem['code'], 'internal'),
                                             'message': message}}


def read_manifest(commerce, authorization):
    status, raw, _ = forward(commerce, 'GET', '/v1/tools?set=facade', None, {'Authorization': authorization})
    if status != 200:
        raise RuntimeError(f'facade manifest: {status} {raw[:200]!r}')
    return json.loads(raw)['items']


def serve(port, commerce, token=None, host='127.0.0.1', lookup=True):
    lock, state = threading.Lock(), {}
    if token:
        state['facade'] = Facade(read_manifest(commerce, 'Bearer ' + token), commerce, lookup)

    def facade(authorization):
        with lock:
            if 'facade' not in state:
                state['facade'] = Facade(read_manifest(commerce, authorization), commerce, lookup)
            return state['facade']

    class Handler(http.server.BaseHTTPRequestHandler):
        protocol_version = 'HTTP/1.1'

        def log_message(self, *args):
            pass

        def reply(self, status, raw, content_type='application/json'):
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def handle_any(self):
            length = int(self.headers.get('Content-Length') or 0)
            body = self.rfile.read(length) if length else None
            path, _, query = self.path.partition('?')
            if 'set=facade' in query.split('&') and path.startswith('/v1/tools'):
                CALLER.authorization = self.headers.get('Authorization', '')
                try:
                    converted = facade(CALLER.authorization)
                except RuntimeError as error:
                    return self.reply(502, json.dumps({'error': {'code': 'gateway_manifest', 'class': 'upstream_unavailable',
                                                                 'message': str(error)}}).encode())
                if self.command == 'GET' and path == '/v1/tools':
                    return self.reply(200, json.dumps(converted.manifest(), ensure_ascii=False).encode())
                if self.command == 'POST' and path.startswith('/v1/tools/'):
                    try:
                        payload = json.loads(body or b'{}')
                    except ValueError:
                        payload = None
                    status, out = converted.call(path.rsplit('/', 1)[1], payload)
                    return self.reply(status, json.dumps(out, ensure_ascii=False).encode())
            headers = {key: value for key, value in self.headers.items()
                       if key.lower() not in ('host', 'content-length', 'connection', 'accept-encoding')}
            status, raw, content_type = forward(commerce, self.command, self.path, body, headers)
            self.reply(status, raw, content_type)

        do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = handle_any

    server = http.server.ThreadingHTTPServer((host, port), Handler)
    print(json.dumps({'gateway': f'http://{host}:{port}', 'commerce': commerce, 'lookup': lookup,
                      'tools': [e['tool'] for e in state['facade'].entries] if 'facade' in state else 'on first request'}),
          flush=True)
    server.serve_forever()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--port', type=int, default=7011)
    parser.add_argument('--host', default='127.0.0.1')
    # Not ACOM_COMMERCE_URL: that is what the agent is pointed at (this gateway) and would loop.
    parser.add_argument('--commerce', default=os.environ.get('A2API_GATEWAY_COMMERCE', 'http://127.0.0.1:7001'),
                        help='the real commerce origin the screens and every other request go to')
    parser.add_argument('--token', default=os.environ.get('A2API_GATEWAY_TOKEN'),
                        help='read the facade manifest at start with this bearer token (else on the first request)')
    parser.add_argument('--dev-token', action='store_true', help='use the local stack\'s dev token (stack.py)')
    parser.add_argument('--manifest', type=Path, help='with --dump: a facade manifest file instead of the service')
    parser.add_argument('--dump', type=Path, help='write the converted manifest and the tool → screen table, then exit')
    parser.add_argument('--no-lookup', action='store_true',
                        help='pass order numbers through as given (no key lookup through the order list screen)')
    options = parser.parse_args()
    token = options.token
    if options.dev_token:
        from stack import token as dev_token
        token = dev_token('admin', agent=True)
    if options.dump:
        if options.manifest:
            items = json.loads(options.manifest.read_text())['items']
        elif token:
            items = read_manifest(options.commerce, 'Bearer ' + token)
        else:
            raise SystemExit('--dump needs --manifest, --token or --dev-token.')
        converted = Facade(items, options.commerce)
        options.dump.write_text(json.dumps({**converted.manifest(), 'screens': converted.screens}, ensure_ascii=False, indent=1))
        print(json.dumps({'dumped': str(options.dump), 'tools': len(converted.entries)}))
        return
    serve(options.port, options.commerce, token, options.host, lookup=not options.no_lookup)


if __name__ == '__main__':
    main()
