"""Nested/array public field selection and host-configured HTTP limits."""

import copy
import http.server
import json
import threading
import time
import unittest

from jsonschema import Draft202012Validator

from a2api import ExecutionContext, HTTPDeployment, convert
from a2api.errors import A2APIError
from a2api.importers import OpenAPIImporter

CALLER = ExecutionContext('alice', 'tenant-a', frozenset())
OWNER = {'type': 'object', 'required': ['login', 'internal'], 'properties': {
    'login': {'type': 'string'}, 'internal': {'type': 'string'}}}
THING = {'type': 'object', 'required': ['id', 'name', 'secret', 'owner'], 'properties': {
    'id': {'type': 'string'}, 'name': {'type': 'string'}, 'secret': {'type': 'string'},
    'note': {'type': ['string', 'null']}, 'owner': {'$ref': '#/components/schemas/Owner'}}}
DOCUMENT = {
    'openapi': '3.1.0', 'info': {'title': 'Things', 'version': '1'},
    'paths': {
        '/things': {'get': {'operationId': 'listThings', 'summary': 'List things', 'responses': {'200': {
            'description': 'ok', 'content': {'application/json': {'schema': {
                'type': 'object', 'required': ['items', 'total'], 'properties': {
                    'items': {'type': 'array', 'maxItems': 10, 'items': {'$ref': '#/components/schemas/Thing'}},
                    'total': {'type': 'integer'}, 'hasMore': {'type': 'boolean'}}}}}}}}},
        '/things/{id}': {'get': {'operationId': 'getThing', 'summary': 'Get thing', 'parameters': [
            {'name': 'id', 'in': 'path', 'required': True, 'schema': {'type': 'string'}}],
            'responses': {'200': {'description': 'ok', 'content': {'application/json': {
                'schema': {'$ref': '#/components/schemas/Thing'}}}}}}},
        '/owners': {'get': {'operationId': 'listOwners', 'summary': 'List owners', 'responses': {'200': {
            'description': 'ok', 'content': {'application/json': {'schema': {
                'type': 'array', 'items': {'$ref': '#/components/schemas/Owner'}}}}}}}},
        '/slow': {'get': {'operationId': 'slow', 'summary': 'Slow', 'responses': {'200': {
            'description': 'ok', 'content': {'application/json': {'schema': {'type': 'object'}}}}}}},
    },
    'components': {'schemas': {'Thing': THING, 'Owner': OWNER}},
}
ROWS = [{'id': 'T-1', 'name': 'one', 'secret': 's1', 'note': None, 'owner': {'login': 'ann', 'internal': 'x'}},
        {'id': 'T-2', 'name': 'two', 'secret': 's2', 'owner': {'login': 'bob', 'internal': 'y'}}]


class Handler(http.server.BaseHTTPRequestHandler):
    payloads = {}

    def do_GET(self):
        if self.path == '/slow':
            time.sleep(0.4)
        body = json.dumps(self.payloads.get(self.path.split('?')[0], {})).encode()
        try:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass  # the timeout test closes the client connection first

    def log_message(self, *args):
        pass


class SelectPathTests(unittest.TestCase):
    def setUp(self):
        Handler.payloads = {'/things': {'items': copy.deepcopy(ROWS), 'total': 2, 'hasMore': False},
                            '/things/T-1': copy.deepcopy(ROWS[0]), '/owners': [r['owner'] for r in ROWS], '/slow': {}}
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.origin = 'http://127.0.0.1:%d' % self.server.server_address[1]

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()

    def app(self, operations, **limits):
        return convert(OpenAPIImporter(copy.deepcopy(DOCUMENT), namespace='t'), operations=operations,
                       deployment=HTTPDeployment(self.origin, **limits))

    def test_array_items_and_nested_fields_are_projected_and_validated(self):
        app = self.app({'listThings': {'effect': 'read', 'select': ['items[].id', 'items[].owner.login', 'total']}})
        schema = app.describe('t.listthings')['outputSchema']
        self.assertNotIn('secret', json.dumps(schema))
        self.assertNotIn('internal', json.dumps(schema))
        self.assertEqual(schema['properties']['items']['maxItems'], 10)
        result = app.invoke('t.listthings', {}, context=CALLER)
        self.assertEqual(result['data'], {'items': [{'id': 'T-1', 'owner': {'login': 'ann'}},
                                                    {'id': 'T-2', 'owner': {'login': 'bob'}}], 'total': 2})
        Draft202012Validator(schema).validate(result['data'])

    def test_root_arrays_optional_and_nullable_fields_are_preserved(self):
        app = self.app({'listOwners': {'effect': 'read', 'select': ['[].login']},
                        'getThing': {'effect': 'read', 'select': ['id', 'note', 'owner.login']}})
        self.assertEqual(app.invoke('t.listowners', {}, context=CALLER)['data'], [{'login': 'ann'}, {'login': 'bob'}])
        schema = app.describe('t.getthing')['outputSchema']
        self.assertEqual(schema['required'], ['id', 'owner'])
        data = app.invoke('t.getthing', {'path': {'id': 'T-1'}}, context=CALLER)['data']
        self.assertEqual(data, {'id': 'T-1', 'note': None, 'owner': {'login': 'ann'}})

    def test_unselected_invalid_raw_fields_still_fail(self):
        app = self.app({'listThings': {'effect': 'read', 'select': ['items[].id']}})
        Handler.payloads['/things']['items'][1]['secret'] = 7
        result = app.invoke('t.listthings', {}, context=CALLER)
        self.assertEqual(result['error']['code'], 'SCHEMA_MISMATCH')
        self.assertNotIn('data', result)

    def test_invalid_and_overlapping_paths_are_rejected(self):
        for selected in (['items[].missing'], ['items', 'items[].id'], ['items[].id', 'items[]'],
                         ['items.id'], ['owner[x]'], ['.id'], ['items[].id.']):
            with self.assertRaises(A2APIError) as caught:
                self.app({'listThings': {'effect': 'read', 'select': selected}})
            self.assertIn(caught.exception.code, ('INVALID_SELECTION', 'UNSUPPORTED_SELECTION'), selected)

    def test_deployment_limits_are_host_configurable(self):
        slow = self.app({'slow': {'effect': 'read'}}, timeout_ms=100, deadline_ms=200)
        self.assertEqual(slow.invoke('t.slow', {}, context=CALLER)['error']['code'], 'DEADLINE_EXCEEDED')
        patient = self.app({'slow': {'effect': 'read'}}, timeout_ms=2000, deadline_ms=3000)
        self.assertEqual(patient.invoke('t.slow', {}, context=CALLER)['status'], 'succeeded')
        small = self.app({'listThings': {'effect': 'read'}}, max_response_bytes=20)
        self.assertEqual(small.invoke('t.listthings', {}, context=CALLER)['error']['code'], 'RESPONSE_TOO_LARGE')
        for limits in ({'timeout_ms': 0}, {'timeout_ms': 5000, 'deadline_ms': 1000}, {'max_response_bytes': '1'}):
            with self.assertRaises(A2APIError):
                HTTPDeployment(self.origin, **limits)


if __name__ == '__main__':
    unittest.main()
