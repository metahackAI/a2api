"""OpenAPI -> in-memory read binding -> actual HTTP, with no build workflow."""

from contextlib import ExitStack
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from jsonschema import Draft202012Validator

from a2api import A2APIError, HTTPDeployment, convert
from a2api.importers import OpenAPIImporter
from a2api.sample import BACKEND_TOKEN, TOKENS, create_backend, running
from test_openapi import specification

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'src/a2api/sample/order-shipping.openapi.json'
OPTIONS = {
    'getOrder': {'effect': 'read', 'select': ['orderId', 'orderState', 'shipmentIds']},
    'getShipment': {'effect': 'read', 'select': ['shipmentId', 'orderId', 'status', 'estimatedArrival', 'asOf']},
}


class ConversionTests(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.document = json.loads(SOURCE.read_text())
        self.backend = None

    def app(self, *, document=None, options=None, transform=None, provider=None):
        self.backend = create_backend(transform=transform)
        origin = self.stack.enter_context(running(self.backend))
        source = OpenAPIImporter(document or self.document, namespace='legacy')
        application = convert(source, operations=options or OPTIONS,
            deployment=HTTPDeployment(origin, credential_provider=provider or (lambda _: {'Authorization': 'Bearer ' + BACKEND_TOKEN})))
        return application

    def invoke(self, app, identifier='legacy.getorder', input=None, context=None):
        return app.invoke(identifier, {'path': {'orderId': 'ORD-1001'}} if input is None else input,
                          context=context or TOKENS['demo-alice'])

    def assert_error(self, code, action):
        with self.assertRaises(A2APIError) as caught:
            action()
        self.assertEqual(caught.exception.code, code, caught.exception.problem())

    def test_order_then_two_shipments_calls_actual_http_without_generated_files(self):
        source = OpenAPIImporter.from_file(SOURCE, namespace='legacy')
        backend = create_backend()
        origin = self.stack.enter_context(running(backend))
        with patch('pathlib.Path.write_text', side_effect=AssertionError('No generated text files')), \
                patch('pathlib.Path.write_bytes', side_effect=AssertionError('No generated binary files')), \
                patch('a2api.builder.build_contracts', side_effect=AssertionError('No review builder')), \
                patch('a2api.importers.write_import', side_effect=AssertionError('No import bundle')):
            app = convert(source, operations=OPTIONS,
                deployment=HTTPDeployment(origin, credential_provider=lambda _: {'Authorization': 'Bearer ' + BACKEND_TOKEN}))
            order = self.invoke(app)
            self.assertEqual(order['status'], 'succeeded', order)
            shipments = [self.invoke(app, 'legacy.getshipment', {'path': {'shipmentId': identifier}})
                         for identifier in order['data']['shipmentIds']]
        self.assertTrue(all(result['status'] == 'succeeded' for result in shipments), shipments)
        self.assertEqual(backend.sample_requests, ['/orders/ORD-1001', '/shipments/SHP-501', '/shipments/SHP-502'])
        self.assertNotIn('ownerId', json.dumps([order, shipments]))
        self.assertNotIn('tenantId', json.dumps([order, shipments]))
        self.assertEqual(order['completeness'], {'complete': True, 'scope': 'single_api_response'})
        self.assertTrue(all(not record.capability.enabled for record in source.iter_operations()))

    def test_empty_order_needs_no_shipping_call(self):
        app = self.app()
        result = self.invoke(app, input={'path': {'orderId': 'ORD-1002'}})
        self.assertEqual(result['data']['shipmentIds'], [])
        self.assertEqual(self.backend.sample_requests, ['/orders/ORD-1002'])

    def test_descriptor_has_only_call_fields_and_omits_unused_private_definitions(self):
        app = self.app()
        description = app.describe('legacy.getorder')
        self.assertEqual(set(description), {'id', 'version', 'summary', 'effects', 'inputSchema', 'outputSchema'})
        self.assertEqual(app.profile, 'a2api-call/0.1')
        self.assertNotIn('ownerId', json.dumps(description))
        self.assertNotIn('tenantId', json.dumps(description))
        self.assertNotIn('fixture.invalid', json.dumps(description))
        for key in ('inputSchema', 'outputSchema'):
            Draft202012Validator.check_schema(description[key])
        description['outputSchema']['properties'].clear()
        self.assertIn('orderId', app.describe('legacy.getorder')['outputSchema']['properties'])
        self.assertEqual(self.backend.sample_requests, [])

    def test_bad_or_spoofed_input_never_reaches_provider_or_backend(self):
        calls = []
        app = self.app(provider=lambda context: calls.append(context) or {'Authorization': 'Bearer ' + BACKEND_TOKEN})
        for value in [{}, {'path': {'orderId': 7}}, {'path': {'orderId': ''}},
                      {'path': {'orderId': 'ORD-1001'}, 'actor': 'bob'},
                      {'path': {'orderId': 'ORD-1001'}, 'headers': {'Authorization': 'secret'}},
                      {'path': {'orderId': float('nan')}}, [], {'path': {'orderId': '\ud800'}}]:
            result = self.invoke(app, input=value)
            self.assertEqual(result['error']['code'], 'INVALID_INPUT', result)
        self.assertEqual(calls, [])
        self.assertEqual(self.backend.sample_requests, [])
        result = app.invoke('legacy.getorder', {'path': {'orderId': 'ORD-1001'}}, context={'actor': 'alice'})
        self.assertEqual(result['error']['code'], 'UNAUTHENTICATED')

    def test_host_credentials_and_trusted_context_preserve_backend_object_authorization(self):
        contexts = []
        app = self.app(provider=lambda context: contexts.append(context) or {'Authorization': 'Bearer ' + BACKEND_TOKEN})
        for context in [TOKENS['demo-bob'], TOKENS['demo-alice']]:
            result = self.invoke(app, input={'path': {'orderId': 'ORD-2001' if context.actor == 'alice' else 'ORD-1001'}}, context=context)
            self.assertEqual(result['error']['code'], 'PERMISSION_DENIED', result)
        self.assertEqual([context.actor for context in contexts], ['bob', 'alice'])
        self.assertEqual(len(self.backend.sample_requests), 2)  # No automatic retries.

    def test_provider_failure_is_private_and_prevents_http_call(self):
        def provider(_):
            raise ValueError('secret credential material')
        app = self.app(provider=provider)
        result = self.invoke(app)
        self.assertEqual(result['error']['code'], 'CREDENTIALS_UNAVAILABLE')
        self.assertNotIn('secret', json.dumps(result))
        self.assertEqual(self.backend.sample_requests, [])

    def test_raw_response_is_validated_before_select_even_for_unselected_fields(self):
        def invalid(_path, payload):
            payload['ownerId'] = 17
            payload['secret'] = 'must-not-escape'
            return 200, payload
        result = self.invoke(self.app(transform=invalid))
        self.assertEqual(result['error']['code'], 'SCHEMA_MISMATCH', result)
        self.assertNotIn('must-not-escape', json.dumps(result))
        self.assertNotIn('data', result)

    def test_optional_selected_fields_remain_optional(self):
        self.document['components']['schemas']['Order']['properties']['note'] = {'type': ['string', 'null']}
        app = self.app(options={'getOrder': {'effect': 'read', 'select': ['orderId', 'note']}})
        self.assertEqual(self.invoke(app)['data'], {'orderId': 'ORD-1001'})
        self.assertEqual(app.describe('legacy.getorder')['outputSchema']['required'], ['orderId'])

    def test_selected_nested_references_keep_needed_definitions_and_constraints(self):
        schemas = self.document['components']['schemas']
        schemas['Order']['properties']['shipmentIds']['items'] = {'$ref': '#/components/schemas/ShipmentId'}
        schemas['ShipmentId'] = {'type': 'string', 'pattern': '^SHP-'}
        app = self.app(options={'getOrder': {'effect': 'read', 'select': ['shipmentIds']}})
        schema = app.describe('legacy.getorder')['outputSchema']
        self.assertEqual(len(schema['$defs']), 1)
        validator = Draft202012Validator(schema)
        self.assertTrue(validator.is_valid(self.invoke(app)['data']))
        self.assertFalse(validator.is_valid({'shipmentIds': ['ORD-1001']}))
        self.assertNotIn('ownerId', json.dumps(schema))

    def test_source_and_selection_mutations_do_not_change_bound_application(self):
        options = {'getOrder': {'effect': 'read', 'select': ['orderId']}}
        source = OpenAPIImporter(self.document, namespace='legacy')
        backend = create_backend()
        origin = self.stack.enter_context(running(backend))
        app = convert(source, operations=options, deployment=HTTPDeployment(origin,
            credential_provider=lambda _: {'Authorization': 'Bearer ' + BACKEND_TOKEN}))
        options['getOrder']['select'].append('ownerId')
        source.document['paths'].clear()
        self.assertEqual(self.invoke(app)['data'], {'orderId': 'ORD-1001'})

    def test_unknown_capability_is_unavailable_without_http(self):
        app = self.app(options={'getOrder': {'effect': 'read'}})
        self.assert_error('NOT_FOUND', lambda: app.describe('legacy.getshipment'))
        result = self.invoke(app, 'legacy.getshipment')
        self.assertEqual(result['error']['code'], 'NOT_FOUND')
        self.assertEqual(self.backend.sample_requests, [])

    def test_conversion_rejects_bad_options_unsupported_sources_and_non_read_methods(self):
        source = OpenAPIImporter(self.document)
        deployment = HTTPDeployment('http://127.0.0.1:1')
        for options in [{}, {'effect': 'write'}, {'effect': 'unknown'}, {'effect': 'read', 'selekt': ['orderId']}]:
            self.assert_error('INVALID_CONVERSION', lambda: convert(source, operations={'getOrder': options}, deployment=deployment))
        for selected in [[], ['orderId', 'orderId'], [7], None, 'orderId', ['missing']]:
            self.assert_error('INVALID_SELECTION', lambda: convert(source, operations={'getOrder': {'effect': 'read', 'select': selected}}, deployment=deployment))
        self.assert_error('INVALID_SELECTION', lambda: convert(source, operations={'missing': {'effect': 'read'}}, deployment=deployment))
        self.document['paths']['/orders/{orderId}']['get']['responses'] = {'default': {'description': 'No success schema'}}
        bad = OpenAPIImporter(self.document)
        self.assert_error('CONVERT_OPERATION_UNSUPPORTED', lambda: convert(bad, operations={'getOrder': {'effect': 'read'}}, deployment=deployment))
        bad.document['paths']['/orders/{orderId}']['post'] = bad.document['paths']['/orders/{orderId}'].pop('get')
        write_source = OpenAPIImporter(bad.document, methods={'POST'})
        self.assert_error('CONVERT_METHOD_UNSUPPORTED', lambda: convert(write_source, operations={'getOrder': {'effect': 'read'}}, deployment=deployment))

    def test_unselected_unsupported_operations_are_not_converted(self):
        self.document['paths']['/shipments/{shipmentId}']['get']['responses'] = {}
        source = OpenAPIImporter(self.document, namespace='legacy')
        with patch.object(source, '_import', wraps=source._import) as imported:
            app = convert(source, operations={'getOrder': {'effect': 'read', 'select': ['orderId']}},
                          deployment=HTTPDeployment('http://127.0.0.1:1'))
        self.assertEqual(imported.call_count, 1)
        self.assertEqual(app.describe('legacy.getorder')['id'], 'legacy.getorder')


class ConversionWireTests(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.requests, self.status, self.payload = [], 200, {'id': '1'}
        owner = self
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass
            def do_GET(self):
                owner.requests.append(self.path)
                raw = b'' if owner.status == 204 else json.dumps(owner.payload).encode()
                self.send_response(owner.status)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)
            def do_HEAD(self):
                owner.requests.append(self.path)
                self.send_response(200)
                self.send_header('Content-Length', '0')
                self.end_headers()
        self.origin = self.stack.enter_context(running(ThreadingHTTPServer(('127.0.0.1', 0), Handler)))

    def app(self, spec, operation='items/get', **options):
        return convert(OpenAPIImporter(spec, namespace='inventory', methods={'GET', 'HEAD'}),
            operations={operation: {'effect': 'read', **options}}, deployment=HTTPDeployment(self.origin, path_prefix='/v1'))

    def test_path_query_optional_and_header_serialization_remain_in_adapter(self):
        source = specification('3.1.2')
        source['paths']['/items/{id}']['get']['parameters'].append({'in': 'header', 'name': 'X-Locale', 'schema': {'type': 'string'}})
        app = self.app(source)
        result = app.invoke('inventory.items.get', {'path': {'id': 'a/b ?#'}, 'query': {'limit': 2},
            'headers': {'x-locale': 'ko'}}, context=TOKENS['demo-alice'])
        self.assertEqual(result['data'], self.payload)
        parsed = urlsplit(self.requests[0])
        self.assertEqual(parsed.path, '/v1/items/a%2Fb%20%3F%23')
        self.assertEqual(parse_qs(parsed.query), {'limit': ['2']})
        result = app.invoke('inventory.items.get', {'path': {'id': '2'}}, context=TOKENS['demo-alice'])
        self.assertEqual(result['status'], 'succeeded')
        self.assertEqual(urlsplit(self.requests[1]).query, '')

    def test_original_array_union_null_and_open_object_schemas_remain_executable(self):
        variants = [({'type': 'array', 'items': {'type': 'integer'}}, [1, 2]),
                    ({'oneOf': [{'type': 'integer'}, {'type': 'null'}]}, None),
                    ({'type': 'object', 'additionalProperties': {'type': 'integer'}}, {'extension': 1})]
        for schema, payload in variants:
            spec = specification('3.1.2')
            spec['components']['schemas']['Item'] = schema
            self.payload = payload
            app = self.app(spec)
            result = app.invoke('inventory.items.get', {'path': {'id': '1'}}, context=TOKENS['demo-alice'])
            self.assertEqual(result['status'], 'succeeded', result)
            self.assertEqual(result['data'], payload)
            Draft202012Validator(app.describe('inventory.items.get')['outputSchema']).validate(payload)

    def test_head_and_multiple_response_status_schemas_are_preserved(self):
        spec = specification('3.1.2')
        spec['paths']['/items/{id}']['head'] = {'operationId': 'items/head', 'responses': {'200': {'description': 'Empty'}}}
        app = self.app(spec, operation='items/head')
        result = app.invoke('inventory.items.head', {'path': {'id': '1'}}, context=TOKENS['demo-alice'])
        self.assertEqual(result['data'], None)
        self.assertEqual(result['httpStatus'], 200)
        spec['paths']['/items/{id}']['get']['responses']['206'] = {'content': {'application/json': {'schema': {'type': 'integer'}}}}
        app = self.app(spec)
        self.status, self.payload = 206, 17
        result = app.invoke('inventory.items.get', {'path': {'id': '1'}}, context=TOKENS['demo-alice'])
        self.assertEqual(result['data'], 17)
        self.assertEqual(result['httpStatus'], 206)
        self.status = 200  # This value is only valid for the 206 branch.
        result = app.invoke('inventory.items.get', {'path': {'id': '1'}}, context=TOKENS['demo-alice'])
        self.assertEqual(result['error']['code'], 'SCHEMA_MISMATCH')

    def test_github_large_spec_selected_operation_converts_and_invokes_local_fixture(self):
        source = OpenAPIImporter.from_file(ROOT / 'examples/github-openapi/api.github.com.json.gz', namespace='github')
        self.payload = {'enabled': True}
        app = convert(source, operations={'repos/check-vulnerability-alerts': {'effect': 'read'}}, deployment=HTTPDeployment(self.origin))
        # This GitHub endpoint declares an empty 204 response, so a JSON 200 is rejected.
        result = app.invoke('github.repos.check_vulnerability_alerts',
            {'path': {'owner': 'octocat', 'repo': 'Hello-World'}}, context=TOKENS['demo-alice'])
        self.assertEqual(result['error']['code'], 'UPSTREAM_ERROR', result)
        self.assertEqual(self.requests[-1], '/repos/octocat/Hello-World/vulnerability-alerts')
        self.status = 204
        result = app.invoke('github.repos.check_vulnerability_alerts',
            {'path': {'owner': 'octocat', 'repo': 'Hello-World'}}, context=TOKENS['demo-alice'])
        self.assertEqual(result['status'], 'succeeded', result)
        self.assertIsNone(result['data'])
        self.assertEqual(result['httpStatus'], 204)
