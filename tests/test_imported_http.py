"""Import -> explicit deployment -> real loopback HTTP -> response validation."""

from contextlib import ExitStack
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import unittest
from urllib.parse import parse_qs, urlsplit

from a2api import A2APIError, HTTPAdapter
from a2api.execution import Budget
from a2api.importers import OpenAPIImporter
from a2api.sample import TOKENS, running, sample_manifest, sample_runtime, create_backend
from a2api.schema import validate_value
from test_openapi import FIXTURE, imported, specification


class ImportedHTTPTests(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.requests = []

    def serve(self, payload):
        requests = self.requests

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                requests.append({'url': urlsplit(self.path), 'actor': self.headers.get('X-A2API-Actor')})
                body = json.dumps(payload).encode()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        return self.stack.enter_context(running(ThreadingHTTPServer(('127.0.0.1', 0), Handler)))

    def call(self, record, arguments, payload):
        origin = self.serve(payload)
        route = record.http_route(origin, path_prefix='/v1')
        operation = record.capability.operations[record.operation_id]
        validate_value(operation.input_schema, arguments, code='INVALID_INPUT', status=422)
        adapter = HTTPAdapter({(operation.service_ref, operation.operation_ref): route})
        result = adapter.call(operation, arguments, TOKENS['demo-alice'], Budget(5000, 1), 1500)
        validate_value(operation.output_schema, result, code='SCHEMA_MISMATCH', status=502)
        return result

    def test_optional_query_omitted_or_encoded_and_path_cannot_change_origin(self):
        record = imported()
        result = self.call(record, {'path': {'id': 'a/b ?#'}}, {'id': 'value', 'extension': 5})
        self.assertEqual(result, {'result': {'id': 'value', 'extension': 5}})
        self.assertEqual(self.requests[-1]['url'].path, '/v1/items/a%2Fb%20%3F%23')
        self.assertEqual(self.requests[-1]['url'].query, '')
        self.assertEqual(self.requests[-1]['actor'], 'alice')
        self.call(record, {'path': {'id': '1'}, 'query': {'limit': 2}}, {'id': 'value'})
        self.assertEqual(parse_qs(self.requests[-1]['url'].query), {'limit': ['2']})

    def test_scalar_arrays_and_booleans_use_openapi_form_serialization(self):
        source = specification('3.1.2')
        source['paths']['/items/{id}']['get']['parameters'] = [
            {'name': 'labels', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string'}}},
            {'name': 'fields', 'in': 'query', 'explode': False, 'schema': {'type': 'array', 'items': {'type': 'string'}}},
            {'name': 'active', 'in': 'query', 'required': True, 'schema': {'type': 'boolean'}},
        ]
        record = imported(source)
        self.call(record, {'path': {'id': '1'}, 'query': {'labels': ['a & b', 'c'], 'fields': ['id,key', 'name'], 'active': False}}, {'id': '1'})
        self.assertEqual(parse_qs(self.requests[0]['url'].query), {'labels': ['a & b', 'c'], 'fields': ['id,key,name'], 'active': ['false']})
        self.assertIn('fields=id%2Ckey,name', self.requests[0]['url'].query)
        operation = record.capability.operations[record.operation_id]
        adapter = HTTPAdapter({(operation.service_ref, operation.operation_ref): record.http_route('http://127.0.0.1:1')})
        with self.assertRaises(A2APIError) as caught:
            adapter.call(operation, {'path': {'id': '1'}}, TOKENS['demo-alice'], Budget(1000, 1), 500)
        self.assertEqual(caught.exception.code, 'INVALID_INPUT')
        with self.assertRaises(A2APIError) as caught:
            adapter.call(operation, {'path': {'id': '1'}, 'query': {'labels': [], 'active': True}},
                         TOKENS['demo-alice'], Budget(1000, 1), 500)
        self.assertEqual(caught.exception.code, 'INVALID_INPUT')
        self.assertEqual(len(self.requests), 1)

    def test_raw_root_array_survives_import_adapter_and_validation(self):
        source = specification()
        source['paths']['/items/{id}']['get']['responses']['200']['content']['application/json']['schema'] = {
            'type': 'array', 'items': {'$ref': '#/components/schemas/Item'}}
        result = self.call(imported(source), {'path': {'id': '1'}}, [{'id': '1'}, {'id': '2'}])
        self.assertEqual(len(result['result']), 2)
        with self.assertRaises(A2APIError) as caught:
            self.call(imported(source), {'path': {'id': '1'}}, [{'id': 1}])
        self.assertEqual(caught.exception.code, 'SCHEMA_MISMATCH')

    def test_real_github_issue_example_and_pagination_through_http(self):
        from a2api.importers.schema_conversion import local_reference
        importer = OpenAPIImporter.from_file(FIXTURE, namespace='github')
        record = next(importer.iter_operations({'issues/list-for-repo'}))
        media = importer.document['paths'][record.path]['get']['responses']['200']['content']['application/json']
        example = media['examples']['default']
        if '$ref' in example:
            example = local_reference(importer.document, example['$ref'], '')
        result = self.call(record, {'path': {'owner': 'octocat', 'repo': 'Hello-World'}, 'query': {'per_page': 2, 'page': 1}}, example['value'])
        self.assertEqual(result['result'], example['value'])
        self.assertEqual(self.requests[0]['url'].path, '/v1/repos/octocat/Hello-World/issues')
        self.assertEqual(parse_qs(self.requests[0]['url'].query), {'per_page': ['2'], 'page': ['1']})
        self.assertFalse(record.capability.enabled)

    def test_optional_mapped_operation_input_is_omitted_without_breaking_runtime(self):
        manifest = sample_manifest()
        manifest['inputSchema']['properties']['locale'] = {'type': 'string'}
        manifest['operations'][0]['inputSchema']['properties']['locale'] = {'type': 'string'}
        manifest['binding']['steps'][0]['input']['locale'] = {'from': 'input', 'pointer': '/locale'}
        origin = self.stack.enter_context(running(create_backend()))
        runtime = sample_runtime(origin, manifest)
        observed = []
        original = runtime.adapter.call

        def call(operation, arguments, *args):
            if operation.id == 'demo.getOrder':
                observed.append(arguments)
            return original(operation, arguments, *args)

        runtime.adapter.call = call
        for value in ({'orderId': 'ORD-1001'}, {'orderId': 'ORD-1001', 'locale': 'ko'}):
            result = runtime.invoke(capability_id='order.shipping_status', version='0.1.0', catalog_version=runtime.catalog.version,
                                    input=value, context=TOKENS['demo-alice'])
            self.assertEqual(result['status'], 'succeeded', result)
        self.assertNotIn('locale', observed[0])
        self.assertEqual(observed[1]['locale'], 'ko')
