"""Exercise real GitHub contracts against a loopback HTTP fixture; no GitHub calls."""

import copy
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path

from a2api import HTTPAdapter
from a2api.execution import Budget
from a2api.importers import OpenAPIImporter
from a2api.importers.schema_conversion import local_reference
from a2api.ir import ExecutionContext
from a2api.sample import running
from a2api.schema import validate_value


def main():
    source = Path(__file__).resolve().parents[1] / 'github-openapi/api.github.com.json.gz'
    importer = OpenAPIImporter.from_file(source, namespace='github', methods={'GET', 'POST', 'PUT', 'PATCH', 'DELETE'})
    selected = {'issues/create', 'issues/get', 'issues/update', 'issues/lock', 'issues/remove-all-labels'}
    records = {r.operation_id: r for r in importer.iter_operations(selected)}
    assert all(r.capability and not r.capability.enabled for r in records.values())
    # The official list example uses the same Issue response schema as create/get/update.
    example = importer.document['paths']['/repos/{owner}/{repo}/issues']['get']['responses']['200']['content']['application/json']['examples']['default']
    if '$ref' in example:
        example = local_reference(importer.document, example['$ref'], '')
    issue = copy.deepcopy(example['value'][0])
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def handle_call(self):
            assert self.headers.get('Authorization') == 'Bearer fixture-only'
            raw = self.rfile.read(int(self.headers.get('Content-Length', '0')))
            body = json.loads(raw) if raw else {}
            requests.append({'method': self.command, 'path': self.path})
            for field in ('title', 'state'):
                if field in body:
                    issue[field] = body[field]
            status = {'POST': 201, 'GET': 200, 'PATCH': 200, 'PUT': 204, 'DELETE': 204}[self.command]
            payload = json.dumps(issue).encode() if status != 204 else b''
            self.send_response(status)
            if payload:
                self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        do_POST = do_GET = do_PATCH = do_PUT = do_DELETE = handle_call

    context = ExecutionContext('local-demo', 'local-fixture', frozenset())
    path = {'owner': 'fixture', 'repo': 'local', 'issue_number': issue['number']}
    calls = [('issues/create', {'path': {'owner': 'fixture', 'repo': 'local'}, 'body': {'title': 'Transport fixture'}}),
             ('issues/get', {'path': path}), ('issues/update', {'path': path, 'body': {'state': 'closed'}}),
             ('issues/lock', {'path': path, 'body': {'lock_reason': 'resolved'}}),
             ('issues/remove-all-labels', {'path': path})]
    results = []
    with running(ThreadingHTTPServer(('127.0.0.1', 0), Handler)) as origin:
        routes = {(r.capability.operations[r.operation_id].service_ref, r.operation_id):
                  r.http_route(origin, credential_provider=lambda _: {'Authorization': 'Bearer fixture-only'})
                  for r in records.values()}
        adapter = HTTPAdapter(routes)
        for operation_id, arguments in calls:
            record = records[operation_id]
            operation = record.capability.operations[operation_id]
            validate_value(operation.input_schema, arguments, code='INVALID_INPUT', status=422)
            budget = Budget(5000, 1)
            result = adapter.call(operation, arguments, context, budget, 1500)
            validate_value(operation.output_schema, result, code='SCHEMA_MISMATCH', status=502)
            results.append({'operationId': operation_id, 'method': record.method.upper(),
                            'httpStatus': result.get('httpStatus', 200), 'schemaValidated': True, 'backendCalls': budget.calls})
    assert len(requests) == 5 and issue['state'] == 'closed'
    print(json.dumps({'transport': 'loopback HTTP', 'externalRequests': 0, 'enabledCapabilities': 0, 'calls': results}, indent=2))


if __name__ == '__main__':
    main()
