import json
import unittest
import urllib.request
from contextlib import ExitStack
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from a2api.__main__ import post
from a2api.errors import A2APIError
from a2api.execution import Budget
from a2api.http_adapter import HTTPAdapter, HTTPRoute
from a2api.sample import TOKENS, authenticate, create_backend, running, sample_runtime
from a2api.server import create_server


class GatewayTests(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.backend = create_backend()
        base = self.stack.enter_context(running(self.backend))
        self.runtime = sample_runtime(base)
        self.gateway = self.stack.enter_context(running(create_server(self.runtime, authenticate)))

    def test_discover_describe_invoke_over_http(self):
        status, found = post(self.gateway, '/discover', {'query': '배송'})
        self.assertEqual(status, 200)
        item = found['capabilities'][0]
        status, described = post(self.gateway, '/describe', {'id': item['id'], 'version': item['version']})
        self.assertEqual(status, 200)
        self.assertEqual(described['capability']['inputSchema']['required'], ['orderId'])
        status, result = post(self.gateway, '/invoke', {'id': item['id'], 'version': item['version'],
                               'catalogVersion': found['catalogVersion'], 'input': {'orderId': 'ORD-1001'}, 'requestId': 'test-http'})
        self.assertEqual(status, 200, result)
        self.assertEqual(result['status'], 'succeeded')
        self.assertEqual(result['requestId'], 'test-http')
        self.assertEqual(result['stats']['backendCalls'], 3)

    def test_authentication_and_scope_visibility(self):
        status, result = post(self.gateway, '/discover', {}, token='invalid')
        self.assertEqual(status, 401)
        self.assertEqual(result['code'], 'UNAUTHENTICATED')
        status, result = post(self.gateway, '/discover', {}, token='demo-limited')
        self.assertEqual(status, 200)
        self.assertEqual(result['capabilities'], [])
        status, _ = post(self.gateway, '/describe', {'id': 'order.shipping_status', 'version': '0.1.0'}, token='demo-limited')
        self.assertEqual(status, 404)
        self.assertEqual(self.backend.sample_requests, [])

    def test_caller_cannot_override_trusted_context(self):
        status, result = post(self.gateway, '/discover', {'actor': 'bob', 'tenant': 'tenant-b'})
        self.assertEqual(status, 400, result)
        self.assertEqual(self.backend.sample_requests, [])

    def test_stale_snapshot_and_foreign_order_status(self):
        payload = {'id': 'order.shipping_status', 'version': '0.1.0', 'catalogVersion': 'stale', 'input': {'orderId': 'ORD-2001'}}
        status, result = post(self.gateway, '/invoke', payload)
        self.assertEqual(status, 409, result)
        payload['catalogVersion'] = self.runtime.catalog.version
        status, result = post(self.gateway, '/invoke', payload)
        self.assertEqual(status, 403, result)
        self.assertEqual(result['status'], 'failed')
        self.assertNotIn('data', result)

    def test_unknown_fields_paths_and_invalid_pagination(self):
        for path, payload, expected in [('/unknown', {}, 404), ('/discover', {'limit': 0}, 400),
                                        ('/describe', {'id': []}, 400), ('/invoke', {}, 400),
                                        ('/discover', {'cursor': 'invalid'}, 400)]:
            with self.subTest(path=path, payload=payload):
                status, _ = post(self.gateway, path, payload)
                self.assertEqual(status, expected)

    def test_malformed_json_and_content_type(self):
        for raw, content_type, expected in [(b'{"query":"x","query":"y"}', 'application/json', 400),
                                             (b'{}', 'text/plain', 415), (b'{"query":NaN}', 'application/json', 400)]:
            request = urllib.request.Request(self.gateway + '/discover', data=raw,
                                              headers={'Authorization': 'Bearer demo-alice', 'Content-Type': content_type})
            with self.subTest(raw=raw), self.assertRaises(urllib.error.HTTPError) as caught:
                urllib.request.urlopen(request, timeout=2)
            self.assertEqual(caught.exception.code, expected)
            caught.exception.close()


class AdapterTests(unittest.TestCase):
    def call_raw(self, payload: bytes, *, status=200, content_type='application/json', declared_length=None):
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                self.send_response(status)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', str(len(payload) if declared_length is None else declared_length))
                self.end_headers()
                self.wfile.write(payload)

        with running(ThreadingHTTPServer(('127.0.0.1', 0), Handler)) as origin:
            runtime = sample_runtime(origin)
            operation = runtime.catalog.capabilities[0].operations['demo.getOrder']
            return runtime.adapter.call(operation, {'orderId': 'ORD-1001'}, TOKENS['demo-alice'], Budget(1000, 1), 500)

    def test_bad_json_duplicate_keys_and_nonfinite_numbers(self):
        for payload in (b'not JSON', b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":1e999}'):
            with self.subTest(payload=payload), self.assertRaises(A2APIError) as caught:
                self.call_raw(payload)
            self.assertEqual(caught.exception.code, 'INVALID_RESPONSE')

    def test_redirects_and_nonjson_are_not_accepted(self):
        with self.assertRaises(A2APIError) as caught:
            self.call_raw(b'{}', status=302)
        self.assertEqual(caught.exception.code, 'UPSTREAM_ERROR')
        with self.assertRaises(A2APIError) as caught:
            self.call_raw(b'{}', content_type='text/html')
        self.assertEqual(caught.exception.code, 'INVALID_RESPONSE')

    def test_truncated_response_is_not_accepted_as_complete_json(self):
        with self.assertRaises(A2APIError) as caught:
            self.call_raw(b'{}', declared_length=10)
        self.assertEqual(caught.exception.code, 'INVALID_RESPONSE')

    def test_budget_is_enforced_before_an_additional_attempt(self):
        budget = Budget(1000, 1)
        budget.claim()
        with self.assertRaises(A2APIError) as caught:
            budget.claim()
        self.assertEqual(caught.exception.code, 'CALL_BUDGET_EXCEEDED')


if __name__ == '__main__':
    unittest.main()
