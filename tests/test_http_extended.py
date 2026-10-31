"""HTTP methods, codecs, credentials and activation boundaries over real sockets."""

import copy
import contextlib
from contextlib import ExitStack
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import io
from pathlib import Path
import tempfile
import threading
import time
import unittest

from jsonschema import Draft202012Validator

from a2api import A2APIError, Catalog, HTTPAdapter, HTTPHeaderParameter, HTTPResponse, HTTPRoute, Runtime, compile_contract
from a2api.execution import Budget
from a2api.importers import OpenAPIImporter
from a2api.ir import ExecutionContext, Operation
from a2api.sample import TOKENS, running, sample_manifest
from a2api.schema import validate_value
from test_openapi import specification


def mutation_spec():
    source = specification('3.1.2')
    path = source['paths']['/items/{id}']
    for method in ('post', 'put', 'patch'):
        operation = copy.deepcopy(path['get'])
        operation['operationId'] = 'items/' + method
        operation['parameters'] = [{'name': 'If-Match', 'in': 'header', 'schema': {'type': 'string'}}]
        operation['requestBody'] = {'required': True, 'content': {'application/json': {
            'schema': {'type': 'object', 'properties': {'name': {'type': 'string'}, 'active': {'type': 'boolean'}},
                       'required': ['name'], 'additionalProperties': False}}}}
        operation['responses'] = {'201' if method == 'post' else '202' if method == 'patch' else '200': copy.deepcopy(path['get']['responses']['200'])}
        path[method] = operation
    path['head'] = {'operationId': 'items/head', 'responses': {'200': {'description': 'Metadata'}}}
    return source


class ExtendedHTTPTests(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.requests = []
        self.state = {}
        self.response_status = None
        self.response_body = None
        self.response_media = 'application/json'
        self.drop_response = False
        self.delay = 0
        self.lock = threading.Lock()
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def handle_call(self):
                raw = self.rfile.read(int(self.headers.get('Content-Length', 0)))
                with owner.lock:
                    owner.requests.append({'method': self.command, 'path': self.path, 'body': raw, 'headers': dict(self.headers.items())})
                if raw:
                    owner.state.update(json.loads(raw) if isinstance(json.loads(raw), dict) else {'value': json.loads(raw)})
                if self.command == 'DELETE':
                    owner.state.clear()
                if owner.drop_response:
                    self.close_connection = True
                    return
                time.sleep(owner.delay)
                status = owner.response_status or {'POST': 201, 'PATCH': 202, 'DELETE': 204}.get(self.command, 200)
                payload = owner.response_body if owner.response_body is not None else json.dumps({'id': '123', **owner.state}).encode()
                if status in (204, 205):
                    payload = b''
                self.send_response(status)
                self.send_header('Content-Type', owner.response_media)
                # HEAD declares representation length but sends no content.
                self.send_header('Content-Length', str(len(payload)))
                self.end_headers()
                if self.command != 'HEAD':
                    try:
                        self.wfile.write(payload)
                    except (BrokenPipeError, ConnectionResetError):
                        pass

            do_GET = do_HEAD = do_POST = do_PUT = do_PATCH = do_DELETE = handle_call

        self.origin = self.stack.enter_context(running(ThreadingHTTPServer(('127.0.0.1', 0), Handler)))

    def records(self, source=None):
        return {r.method: r for r in OpenAPIImporter(source or mutation_spec(), namespace='inventory',
                methods={'GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE'}).iter_operations()}

    def call_record(self, record, arguments, **deployment):
        self.assertEqual(record.status, 'imported', record.summary())
        operation = record.capability.operations[record.operation_id]
        validate_value(operation.input_schema, arguments, code='INVALID_INPUT', status=422)
        adapter = HTTPAdapter({(operation.service_ref, operation.operation_ref): record.http_route(self.origin, **deployment)})
        result = adapter.call(operation, arguments, TOKENS['demo-alice'], Budget(1000, 1), 800)
        validate_value(operation.output_schema, result, code='SCHEMA_MISMATCH', status=502)
        return result

    def direct(self, route, arguments=None, **limits):
        operation = Operation('test', 'fixture', 'operation', {}, {}, route.method)
        adapter = HTTPAdapter({('fixture', 'operation'): route}, **limits)
        budget = Budget(1500, 1)
        return adapter.call(operation, arguments or {}, TOKENS['demo-alice'], budget, 1000)

    def test_imported_create_read_replace_accept_head_delete_lifecycle(self):
        records = self.records()
        arguments = {'path': {'id': '123'}, 'body': {'name': '한글', 'active': False}, 'headers': {'if-match': '"v1"'}}
        created = self.call_record(records['post'], arguments, credential_provider=lambda context: {'Authorization': 'Bearer fixture-' + context.actor})
        self.assertEqual(created, {'result': {'id': '123', 'name': '한글', 'active': False}, 'httpStatus': 201})
        self.assertEqual(self.state['name'], '한글')
        self.assertEqual(self.requests[-1]['headers']['authorization'], 'Bearer fixture-alice')
        self.assertEqual(self.requests[-1]['headers']['if-match'], '"v1"')
        self.assertEqual(self.requests[-1]['headers']['Content-Type'], 'application/json')
        self.assertEqual(self.call_record(records['get'], {'path': {'id': '123'}})['result']['name'], '한글')
        arguments['body'] = {'name': 'replaced'}
        self.assertEqual(self.call_record(records['put'], arguments)['httpStatus'], 200)
        self.assertEqual(self.call_record(records['patch'], arguments)['httpStatus'], 202)
        self.assertEqual(self.call_record(records['head'], {'path': {'id': '123'}}), {'result': None, 'httpStatus': 200})
        self.assertEqual(self.call_record(records['delete'], {'path': {'id': '123'}}), {'result': None, 'httpStatus': 204})
        self.assertEqual(self.state, {})
        self.assertEqual([r['method'] for r in self.requests], ['POST', 'GET', 'PUT', 'PATCH', 'HEAD', 'DELETE'])
        self.assertTrue(all(not record.capability.enabled for record in records.values()))

    def test_multiple_success_codes_keep_status_and_schema_correlated(self):
        source = mutation_spec()
        source['paths']['/items/{id}']['post']['responses'] = {
            '201': {'content': {'application/json': {'schema': {'type': 'object', 'required': ['id'], 'properties': {'id': {'type': 'string'}}}}}},
            '202': {'content': {'application/json': {'schema': {'type': 'object', 'required': ['job'], 'properties': {'job': {'type': 'integer'}}}}}},
            '204': {'description': 'Empty'},
        }
        record = self.records(source)['post']
        validator = Draft202012Validator(record.capability.describe()['outputSchema'])
        for code, value in ((201, {'id': '1'}), (202, {'job': 2}), (204, None)):
            validator.validate({'result': value, 'httpStatus': code})
        for code, value in ((201, {'job': 2}), (202, {'id': '1'}), (204, {'id': '1'})):
            self.assertFalse(validator.is_valid({'result': value, 'httpStatus': code}))

    def test_direct_adapter_validates_imported_request_and_response_contracts(self):
        record = self.records()['post']
        operation = record.capability.operations[record.operation_id]
        adapter = HTTPAdapter({(operation.service_ref, operation.operation_ref): record.http_route(self.origin)})
        budget = Budget(1000, 1)
        with self.assertRaises(A2APIError) as caught:
            adapter.call(operation, {'path': {'id': '123'}, 'body': {'name': 7}}, TOKENS['demo-alice'], budget, 500)
        self.assertEqual(caught.exception.code, 'INVALID_INPUT')
        self.assertEqual(budget.calls, 0)
        self.assertEqual(self.requests, [])
        self.response_body = b'{"id":123,"private":"must-not-escape"}'
        with self.assertRaises(A2APIError) as caught:
            adapter.call(operation, {'path': {'id': '123'}, 'body': {'name': 'valid'}}, TOKENS['demo-alice'], budget, 500)
        self.assertEqual(caught.exception.code, 'SCHEMA_MISMATCH')
        self.assertNotIn('must-not-escape', json.dumps(caught.exception.problem()))
        self.assertEqual(budget.calls, 1)

    def test_optional_body_and_explicit_json_null_are_distinct(self):
        route = HTTPRoute(self.origin, '/items', method='POST', request_body_pointer='/body', responses={201: HTTPResponse()})
        for arguments in ({}, {'body': None}, {'body': [True, '한글']}, {'body': 7}):
            self.direct(route, arguments)
        self.assertEqual([r['body'] for r in self.requests], [b'', b'null', '[true,"한글"]'.encode(), b'7'])
        self.assertNotIn('Content-Type', self.requests[0]['headers'])

    def test_body_limits_invalid_json_and_missing_fields_fail_before_network(self):
        route = HTTPRoute(self.origin, '/items', method='POST', request_body_pointer='/body', request_body_required=True, responses={201: HTTPResponse()})
        for arguments, limits, code in [({}, {}, 'INVALID_INPUT'), ({'body': float('nan')}, {}, 'INVALID_INPUT'),
                                         ({'body': '\ud800'}, {}, 'INVALID_INPUT'), ({'body': 'too large'}, {'max_request_bytes': 3}, 'REQUEST_TOO_LARGE')]:
            with self.subTest(code=code), self.assertRaises(A2APIError) as caught:
                self.direct(route, arguments, **limits)
            self.assertEqual(caught.exception.code, code)
        self.assertEqual(self.requests, [])

    def test_method_binding_mismatch_and_write_activation_are_rejected(self):
        manifest = sample_manifest()
        manifest['operations'][0]['httpMethod'] = 'POST'
        with self.assertRaises(A2APIError):
            compile_contract(manifest)
        capability = compile_contract(sample_manifest())
        operation = capability.operations['demo.getOrder']
        adapter = HTTPAdapter({(operation.service_ref, operation.operation_ref): HTTPRoute(self.origin, '/items', method='POST')})
        budget = Budget(1000, 1)
        with self.assertRaises(A2APIError):
            adapter.call(operation, {'orderId': '123'}, TOKENS['demo-alice'], budget, 500)
        self.assertEqual(budget.calls, 0)
        with self.assertRaises(A2APIError):
            Runtime(Catalog([capability], allow_samples=True), adapter)
        self.assertEqual(self.requests, [])

    def test_credentials_follow_host_context_on_each_call(self):
        observed = []

        def credentials(context):
            observed.append(context.actor)
            return {'Authorization': 'Bearer fixture-' + context.actor}

        route = HTTPRoute(self.origin, '/items', credential_provider=credentials)
        adapter = HTTPAdapter({('fixture', 'operation'): route})
        operation = Operation('test', 'fixture', 'operation', {}, {})
        for actor in ('alice', 'bob'):
            adapter.call(operation, {}, ExecutionContext(actor, 'fixture', frozenset()), Budget(1000, 1), 800)
        self.assertEqual(observed, ['alice', 'bob'])
        self.assertEqual([r['headers']['authorization'] for r in self.requests], ['Bearer fixture-alice', 'Bearer fixture-bob'])
        self.assertNotIn('fixture-alice', repr(route))

    def test_bad_credentials_and_header_input_do_not_escape_or_send(self):
        def failure(context):
            raise ValueError('secret-must-not-escape')

        for provider in (failure, lambda c: {'Host': 'other'}, lambda c: {'Authorization': 'bad\r\nvalue'}, lambda c: None):
            with self.subTest(provider=provider), self.assertRaises(A2APIError) as caught:
                self.direct(HTTPRoute(self.origin, '/items', credential_provider=provider))
            self.assertEqual(caught.exception.code, 'CREDENTIALS_UNAVAILABLE')
            self.assertNotIn('secret', str(caught.exception.problem()))
        route = HTTPRoute(self.origin, '/items', header_parameters={'If-Match': HTTPHeaderParameter('/revision', True)})
        for arguments in ({}, {'revision': 'bad\r\nHost: other'}):
            with self.assertRaises(A2APIError) as caught:
                self.direct(route, arguments)
            self.assertEqual(caught.exception.code, 'INVALID_INPUT')
        self.assertEqual(self.requests, [])

    def test_response_media_empty_codec_and_declared_success_are_enforced(self):
        self.response_status = 201
        self.response_media = 'application/vnd.fixture+json'
        route = HTTPRoute(self.origin, '/items', method='POST', responses={201: HTTPResponse('application/vnd.fixture+json')})
        self.direct(route)
        self.assertEqual(self.requests[0]['headers']['Accept'], 'application/vnd.fixture+json')
        self.response_media = 'application/json'
        with self.assertRaises(A2APIError) as caught:
            self.direct(route)
        self.assertEqual(caught.exception.code, 'INVALID_RESPONSE')
        self.response_status = 200
        with self.assertRaises(A2APIError) as caught:
            self.direct(HTTPRoute(self.origin, '/items', responses={200: HTTPResponse(None)}))
        self.assertEqual(caught.exception.code, 'INVALID_RESPONSE')
        self.response_status = 202
        with self.assertRaises(A2APIError) as caught:
            self.direct(HTTPRoute(self.origin, '/items'))
        self.assertEqual(caught.exception.code, 'UPSTREAM_ERROR')

    def test_error_responses_are_sanitized_and_not_retried(self):
        self.response_body = b'{"secret":"private-backend-details"}'
        route = HTTPRoute(self.origin, '/items', method='POST')
        for status, code in ((401, 'PERMISSION_DENIED'), (409, 'UPSTREAM_CONFLICT'), (422, 'UPSTREAM_VALIDATION_FAILED'), (429, 'RATE_LIMITED'), (302, 'UPSTREAM_ERROR'), (400, 'UPSTREAM_VALIDATION_FAILED'), (503, 'UPSTREAM_UNAVAILABLE')):
            self.response_status = status
            before = len(self.requests)
            with self.assertRaises(A2APIError) as caught:
                self.direct(route)
            self.assertEqual(caught.exception.code, code)
            self.assertNotIn('private-backend-details', json.dumps(caught.exception.problem()))
            self.assertEqual(len(self.requests), before + 1)

    def test_mutation_response_loss_reports_unknown_with_single_attempt(self):
        self.drop_response = True
        route = HTTPRoute(self.origin, '/items', method='POST', request_body_pointer='/body')
        with self.assertRaises(A2APIError) as caught:
            self.direct(route, {'body': {'name': 'committed-before-response'}})
        self.assertEqual(caught.exception.code, 'OUTCOME_UNKNOWN')
        self.assertEqual(self.state['name'], 'committed-before-response')
        self.assertEqual(len(self.requests), 1)

    def test_mutation_timeout_reports_unknown_after_backend_has_written(self):
        self.delay = 0.08
        route = HTTPRoute(self.origin, '/items', method='POST', request_body_pointer='/body')
        operation = Operation('test', 'fixture', 'operation', {}, {}, 'POST')
        adapter = HTTPAdapter({('fixture', 'operation'): route})
        with self.assertRaises(A2APIError) as caught:
            adapter.call(operation, {'body': {'name': 'written-before-timeout'}}, TOKENS['demo-alice'], Budget(500, 1), 30)
        self.assertEqual(caught.exception.code, 'OUTCOME_UNKNOWN')
        self.assertEqual(self.state['name'], 'written-before-timeout')
        self.assertEqual(len(self.requests), 1)

    def test_invalid_route_declarations_fail_at_configuration(self):
        for changes in ({'method': 'TRACE'}, {'method': 'post'}, {'request_body_pointer': '/body'},
                        {'method': 'HEAD'}, {'responses': {204: HTTPResponse()}}, {'responses': {302: HTTPResponse(None)}},
                        {'headers': {'Content-Length': '2'}}, {'headers': {'X-Test': 'bad\nvalue'}},
                        {'header_parameters': {'Authorization': HTTPHeaderParameter('/token')}},
                        {'header_parameters': {'Host': HTTPHeaderParameter('/host')}},
                        {'headers': {'X-Test': 'a', 'x-test': 'b'}}, {'response_status_field': 'status'}):
            with self.subTest(changes=changes), self.assertRaises(A2APIError):
                HTTPRoute(self.origin, '/items', **changes)
        for path in ('/raw path', '/bad\r\nHeader: value', '/한글'):
            with self.subTest(path=path), self.assertRaises(A2APIError):
                HTTPRoute(self.origin, path)


class ExtendedImportTests(unittest.TestCase):
    def test_cli_selects_write_methods_and_roundtrips_generated_ir(self):
        from a2api.__main__ import main
        from a2api import load_contract
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            source = directory / 'source.json'
            source.write_text(json.dumps(mutation_spec()))
            output = directory / 'generated'
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                code = main(['import-openapi', str(source), '--namespace', 'cli', '--output', str(output),
                             '--methods', 'post', '--operation', 'items/post', '--strict'])
            self.assertEqual(code, 0, stream.getvalue())
            self.assertEqual(json.loads(stream.getvalue())['statuses'], {'imported': 1})
            report = json.loads((output / 'report.json').read_text())
            self.assertEqual(report['requestedMethods'], ['POST'])
            capability = load_contract(output / report['operations'][0]['contract'])
            self.assertEqual(capability.operations['items/post'].http_method, 'POST')
            self.assertFalse(capability.enabled)

    def test_method_selection_defaults_to_get_and_rejects_unsupported_values(self):
        records = list(OpenAPIImporter(mutation_spec()).iter_operations())
        self.assertTrue(all(r.status == 'skipped' for r in records if r.method != 'get'))
        for methods in (set(), {'TRACE'}, {'CONNECT'}, 'POST'):
            with self.subTest(methods=methods), self.assertRaises(A2APIError):
                OpenAPIImporter(mutation_spec(), methods=methods)

    def test_request_only_fields_are_not_validated_as_response_fields(self):
        source = mutation_spec()
        schema = source['paths']['/items/{id}']['post']['requestBody']['content']['application/json']['schema']
        schema['properties']['name']['writeOnly'] = True
        record = next(OpenAPIImporter(source, methods={'POST'}).iter_operations({'items/post'}))
        self.assertEqual(record.status, 'imported', record.summary())
        del schema['properties']['name']['writeOnly']
        schema['properties']['name']['readOnly'] = True
        record = next(OpenAPIImporter(source, methods={'POST'}).iter_operations({'items/post'}))
        self.assertEqual(record.diagnostics[0]['code'], 'READ_ONLY_REQUEST_REQUIREMENT')

    def test_unsupported_body_success_and_header_shapes_are_diagnosed(self):
        for edit, code in [
            (lambda op: op['requestBody'].update(content={'multipart/form-data': {'schema': {'type': 'object'}}}), 'UNSUPPORTED_REQUEST_BODY'),
            (lambda op: op.update(responses={'2XX': {'description': 'Range'}}), 'UNSUPPORTED_SUCCESS_RANGE'),
            (lambda op: op.update(responses={'201': {'content': {'text/plain': {'schema': {'type': 'string'}}}}}), 'UNSUPPORTED_RESPONSE'),
            (lambda op: op['parameters'][0].update(name='Authorization'), 'UNSUPPORTED_HEADER_PARAMETER'),
            (lambda op: op['parameters'][0].update(schema={'type': 'array', 'items': {'type': 'string'}}), 'UNSUPPORTED_HEADER_SERIALIZATION'),
        ]:
            source = mutation_spec()
            edit(source['paths']['/items/{id}']['post'])
            record = next(OpenAPIImporter(source, methods={'POST'}).iter_operations({'items/post'}))
            self.assertEqual(record.status, 'unsupported', record.summary())
            self.assertEqual(record.diagnostics[0]['code'], code)
