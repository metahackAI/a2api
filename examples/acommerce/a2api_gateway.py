"""a2api as a gateway in front of a-commerce: the legacy facade, converted, in its own manifest format.

python examples/acommerce/a2api_gateway.py --port 7011     # then start the agent with
A2API_AGENT_COMMERCE_URL=http://127.0.0.1:7011 python examples/acommerce/stack.py up

a-commerce's own agent reads tools from `GET /v1/tools?set=facade` and calls `POST
/v1/tools/{tool}?set=facade` with `{"input": ...}`. This gateway answers those two with the facade
converted by a2api (readable names and words from `legacy_facade.VOCABULARY`, summaries read from
the screens' code, snake_case names) and runs each call through `ConvertedAPI.invoke`, so the
agent, its search, planner and limits stay the same and only the tool representation changes.
Every other request (change sets, store settings, the A-Commerce tools) passes through unchanged.
The caller's bearer token is forwarded per request.
"""

from __future__ import annotations

import argparse
import http.server
import json
from pathlib import Path
import sys
import threading
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from a2api import ExecutionContext, HTTPDeployment, convert  # noqa: E402
from a2api.importers import ToolCatalogImporter  # noqa: E402
from legacy_facade import VOCABULARY, error_detail, facade_options  # noqa: E402

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
    """The converted facade: manifest entries and calls, built once from the real manifest."""

    def __init__(self, commerce, token):
        status, raw, _ = forward(commerce, 'GET', '/v1/tools?set=facade', None, {'Authorization': 'Bearer ' + token})
        if status != 200:
            raise SystemExit(f'facade manifest: {status} {raw[:200]!r}')
        items = json.loads(raw)['items']
        source = ToolCatalogImporter(items, namespace='facade')
        self.app = convert(source, operations=facade_options(items), vocabulary=VOCABULARY, deployment=HTTPDeployment(
            commerce, credential_provider=lambda context: {'Authorization': CALLER.authorization},
            request_values=lambda context, call: {'query': {'set': 'facade'}}, error_detail=error_detail,
            timeout_ms=30000, deadline_ms=35000, max_response_bytes=4 * 1048576))
        self.entries, self.ids = [], {}
        originals = {item['tool']: item for item in items}
        for record in source.iter_operations():
            if record.status != 'imported':
                continue
            descriptor = self.app.describe(record.id)
            name = record.id.split('.', 1)[1]
            self.ids[name] = record.id
            self.entries.append({**originals[record.operation_id], 'tool': name, 'path': f'/v1/tools/{name}',
                                 'summary': descriptor['summary'],
                                 'input_schema': descriptor['inputSchema']['properties']['body']})

    def manifest(self):
        return {'items': self.entries}

    def call(self, name, payload):
        if name not in self.ids:
            return 404, {'error': {'code': 'unknown_tool', 'class': 'not_found', 'message': f'There is no tool {name}.'}}
        given = payload.get('input', {}) if isinstance(payload, dict) else {}
        result = self.app.invoke(self.ids[name], {'body': given}, context=ExecutionContext('agent', 'store', frozenset()))
        if result['status'] == 'succeeded':
            return 200, result['data']
        problem = result['error']
        message = problem['detail']
        if problem.get('issues'):
            message += ' Issues: ' + json.dumps(problem['issues'], ensure_ascii=False, separators=(',', ':'))
        return problem['status'], {'error': {'code': problem['code'].lower(), 'class': CLASSES.get(problem['code'], 'internal'),
                                             'message': message}}


def serve(port, commerce, token):
    facade = Facade(commerce, token)

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
            if 'set=facade' in query.split('&'):
                CALLER.authorization = self.headers.get('Authorization', '')
                if self.command == 'GET' and path == '/v1/tools':
                    return self.reply(200, json.dumps(facade.manifest(), ensure_ascii=False).encode())
                if self.command == 'POST' and path.startswith('/v1/tools/'):
                    status, out = facade.call(path.rsplit('/', 1)[1], json.loads(body or b'{}'))
                    return self.reply(status, json.dumps(out, ensure_ascii=False).encode())
            headers = {key: value for key, value in self.headers.items()
                       if key.lower() not in ('host', 'content-length', 'connection', 'accept-encoding')}
            status, raw, content_type = forward(commerce, self.command, self.path, body, headers)
            self.reply(status, raw, content_type)

        do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = handle_any

    server = http.server.ThreadingHTTPServer(('127.0.0.1', port), Handler)
    print(json.dumps({'gateway': f'http://127.0.0.1:{port}', 'tools': [e['tool'] for e in facade.entries]}), flush=True)
    server.serve_forever()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=7011)
    parser.add_argument('--commerce', default='http://127.0.0.1:7001')
    options = parser.parse_args()
    from stack import token
    serve(options.port, options.commerce, token('admin', agent=True))


if __name__ == '__main__':
    main()
