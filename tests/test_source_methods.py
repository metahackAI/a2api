"""Cross-importer HTTP effects, validation and MCP behavior, without language SDKs."""

from contextlib import ExitStack
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import json
from pathlib import Path
import socket
import sys
import unittest

from a2api import A2APIError, ExecutionContext, HTTPDeployment, convert
from a2api.importers import OpenAPIImporter
from a2api.sample import running
from test_source_importers import CASES, HAS_SOURCE, ROOT

HAS_MCP = importlib.util.find_spec('mcp') is not None


@unittest.skipUnless(HAS_SOURCE, 'Install a2api[source]')
class SourceHTTPTests(unittest.TestCase):
    def setUp(self):
        stack = ExitStack();self.addCleanup(stack.close)
        self.requests, self.values, self.bad_raw, self.disconnect = [], {}, False, False
        test = self
        class Handler(BaseHTTPRequestHandler):
            def handle_method(self):
                test.requests.append((self.command, self.path))
                data = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))) or 'null')
                key = self.path.rsplit('/', 1)[-1]
                status, value = 200, None
                if self.command == 'POST' and self.path == '/items':
                    key = 'I-2';test.values[key] = {'id': key, 'name': data['name'], 'internalNote': 'private'}
                    value, status = test.values[key], 201
                elif self.command in ('PUT', 'PATCH'):
                    test.values[key]['name'] = data['name'];value = test.values[key]
                elif self.command == 'DELETE':
                    test.values.pop(key, None);status = 204
                    if test.disconnect:
                        self.connection.shutdown(socket.SHUT_RDWR);self.connection.close();return
                elif self.command == 'POST':
                    value = [{'id': v['id'], 'name': v['name']} for v in test.values.values() if data.get('q', '') in v['name']]
                elif key not in test.values:
                    status, value = 404, {'error': 'not found'}
                else:value = test.values[key]
                if test.bad_raw and isinstance(value, dict):value = {**value, 'internalNote': 42}
                body = b'' if status == 204 or self.command == 'HEAD' else json.dumps(value).encode()
                self.send_response(status);self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(body)));self.end_headers();self.wfile.write(body)
            do_GET = do_HEAD = do_POST = do_PUT = do_PATCH = do_DELETE = handle_method
            def log_message(self, *_):pass
        self.origin = stack.enter_context(running(ThreadingHTTPServer(('127.0.0.1', 0), Handler)))
        self.context = ExecutionContext('alice', 'tenant', frozenset())

    def app(self, cls, directory):
        source = cls.from_directory(ROOT / 'examples/source-http' / directory, namespace='sample')
        rows = list(source.iter_operations()); options, ids = {}, {}
        for row in rows:
            effect = 'read' if row.method in ('GET', 'HEAD') or row.path == '/items/search' else 'write'
            options[row.operation_id] = {'effect': effect}
            if row.method not in ('HEAD', 'DELETE') and row.path != '/items/search':
                options[row.operation_id]['select'] = ['id', 'name']
            ids[(row.method, row.path)] = row.id
        return convert(source, operations=options, deployment=HTTPDeployment(self.origin)), ids, source

    def test_every_importer_executes_all_methods_checks_schemas_and_exposes_selected_fields(self):
        for cls, directory, _ in CASES:
            with self.subTest(importer=cls.__name__):
                self.values.clear();self.requests.clear();app, ids, _ = self.app(cls, directory)
                def call(method, path='/items/{id}', input=None):
                    return app.invoke(ids[(method, path)], input or {'path': {'id': 'I-2'}}, context=self.context)
                created = call('POST', '/items', {'body': {'name': 'new'}})
                self.assertEqual(created['httpStatus'], 201, created)
                self.assertEqual(created['data'], {'id': 'I-2', 'name': 'new'})
                self.assertEqual(call('GET')['data']['name'], 'new')
                self.assertIsNone(call('HEAD')['data'])
                self.assertEqual(call('PUT', input={'path': {'id': 'I-2'}, 'body': {'name': 'replace'}})['data']['name'], 'replace')
                self.assertEqual(call('PATCH', input={'path': {'id': 'I-2'}, 'body': {'name': 'patch'}})['data']['name'], 'patch')
                self.assertEqual(call('POST', '/items/search', {'body': {'q': 'patch'}})['data'], [{'id': 'I-2', 'name': 'patch'}])
                self.assertEqual(call('DELETE')['httpStatus'], 204)
                self.assertEqual(call('GET')['error']['code'], 'RESOURCE_NOT_FOUND')
                self.assertEqual(len(self.requests), 8)
                before = len(self.requests)
                for bad in [{'body': {'name': 2}}, {'body': {'name': 'x'}, 'context': {}}, {'body': {'name': 'x'}, 'origin': 'http://other.invalid'}]:
                    self.assertEqual(call('POST', '/items', bad)['error']['code'], 'INVALID_INPUT')
                self.assertEqual(len(self.requests), before)

    def test_raw_schema_failure_and_unknown_write_outcome_do_not_retry(self):
        for cls, directory, _ in CASES:
            with self.subTest(importer=cls.__name__):
                app, ids, _ = self.app(cls, directory)
                self.values['I-2'] = {'id': 'I-2', 'name': 'ok', 'internalNote': 'private'}
                self.requests.clear();self.bad_raw = True
                result = app.invoke(ids[('GET', '/items/{id}')], {'path': {'id': 'I-2'}}, context=self.context)
                self.assertEqual(result['error']['code'], 'SCHEMA_MISMATCH', result)
                self.assertNotIn('data', result)
                self.assertEqual(len(self.requests), 1)
                self.bad_raw = False;self.disconnect = True
                result = app.invoke(ids[('DELETE', '/items/{id}')], {'path': {'id': 'I-2'}}, context=self.context)
                self.assertEqual(result['error']['code'], 'OUTCOME_UNKNOWN', result)
                self.assertNotIn('I-2', self.values)
                self.assertEqual(len(self.requests), 2)
                self.disconnect = False

    def test_effects_are_explicit_and_read_delete_is_rejected_before_binding(self):
        cls, directory, _ = CASES[0];_, _, source = self.app(cls, directory)
        for row in source.iter_operations():
            if row.method not in ('PUT', 'PATCH', 'DELETE'):continue
            with self.assertRaises(A2APIError) as caught:
                convert(source, operations={row.operation_id: {'effect': 'read'}}, deployment=HTTPDeployment(self.origin))
            self.assertEqual(caught.exception.code, 'INVALID_CONVERSION')
        self.assertEqual(self.requests, [])

    def test_openapi_explicit_write_has_same_direct_envelope_and_import_stays_disabled(self):
        source = OpenAPIImporter({'openapi': '3.1.0', 'info': {'title': 'sample', 'version': '1'}, 'paths': {
            '/items': {'post': {'operationId': 'create', 'requestBody': {'required': True, 'content': {'application/json': {'schema': {
                'type': 'object', 'properties': {'name': {'type': 'string'}}, 'required': ['name'], 'additionalProperties': False}}}},
                'responses': {'201': {'description': 'created', 'content': {'application/json': {'schema': {'type': 'object',
                    'properties': {'id': {'type': 'string'}, 'name': {'type': 'string'}, 'internalNote': {'type': 'string'}},
                    'required': ['id', 'name']}}}}}}}}}, namespace='openapi', methods={'POST'})
        app = convert(source, operations={'create': {'effect': 'write', 'select': ['id', 'name']}}, deployment=HTTPDeployment(self.origin))
        result = app.invoke('openapi.create', {'body': {'name': 'test'}}, context=self.context)
        self.assertEqual(result['status'], 'succeeded', result)
        self.assertEqual(app.describe('openapi.create')['effects'], {'kind': 'write'})
        self.assertTrue(all(not record.capability.enabled for record in source.iter_operations()))

    @unittest.skipUnless(HAS_MCP, 'Install a2api[mcp]')
    def test_real_stdio_exercises_write_and_read_contracts_and_hints(self):
        import asyncio
        spec = importlib.util.spec_from_file_location('source_application', ROOT / 'examples/source-http/application.py')
        module = importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        # The verifier imports its sibling application; no user module auto-discovery.
        previous = sys.modules.get('application')
        sys.modules['application'] = module
        try:
            spec = importlib.util.spec_from_file_location('source_verify', ROOT / 'examples/source-http/verify.py')
            verify = importlib.util.module_from_spec(spec);spec.loader.exec_module(verify)
        finally:
            if previous is None:sys.modules.pop('application', None)
            else:sys.modules['application'] = previous
        self.values['I-1'] = {'id': 'I-1', 'name': 'original', 'internalNote': 'private'}
        result = asyncio.run(verify.verify('spring', self.origin))
        self.assertEqual(len(result['direct']), 8)
        self.assertEqual(len(result['stdio']), 8)
        self.assertEqual(len(self.requests), 16)
        self.assertTrue(result['writeEffectAdvertised'])


if __name__ == '__main__':unittest.main()
