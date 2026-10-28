import json
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import ExitStack

from a2api import A2APIError, Catalog, HTTPRoute, compile_contract
from a2api.sample import TOKENS, create_backend, running, sample_manifest, sample_runtime


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)

    def start(self, *, transform=None, manifest=None):
        backend = create_backend(transform=transform)
        url = self.stack.enter_context(running(backend))
        return sample_runtime(url, manifest), backend

    def invoke(self, runtime, order_id='ORD-1001', token='demo-alice', **overrides):
        arguments = dict(capability_id='order.shipping_status', version='0.1.0', catalog_version=runtime.catalog.version,
                         input={'orderId': order_id}, context=TOKENS[token])
        arguments.update(overrides)
        return runtime.invoke(**arguments)

    def test_real_http_composition_order_and_safe_projection(self):
        runtime, backend = self.start()
        found = runtime.discover('배송 조회', TOKENS['demo-alice'])
        item = found['capabilities'][0]
        self.assertEqual(runtime.describe(item['id'], item['version'], TOKENS['demo-alice'])['capability']['id'], item['id'])
        result = self.invoke(runtime)
        self.assertEqual(result['status'], 'succeeded', result)
        self.assertEqual([s['shipmentId'] for s in result['data']['shipments']], ['SHP-501', 'SHP-502'])
        self.assertEqual([s['status'] for s in result['data']['shipments']], ['in_transit', 'delivered'])
        self.assertIsNone(result['data']['shipments'][1]['estimatedArrival'])
        self.assertNotIn('ownerId', json.dumps(result))
        self.assertNotIn('tenantId', json.dumps(result))
        self.assertEqual(result['stats']['backendCalls'], 3)
        self.assertEqual(len(result['evidence']), 3)
        self.assertEqual(backend.sample_requests[0], '/orders/ORD-1001')
        self.assertCountEqual(backend.sample_requests[1:], ['/shipments/SHP-501', '/shipments/SHP-502'])

    def test_empty_shipments_succeed_without_extra_calls(self):
        runtime, backend = self.start()
        result = self.invoke(runtime, 'ORD-1002')
        self.assertEqual(result['status'], 'succeeded', result)
        self.assertEqual(result['data']['shipments'], [])
        self.assertEqual(backend.sample_requests, ['/orders/ORD-1002'])

    def test_scope_filtering_and_direct_lookup_are_consistent(self):
        runtime, backend = self.start()
        self.assertEqual(runtime.discover('', TOKENS['demo-limited'])['capabilities'], [])
        with self.assertRaises(A2APIError) as caught:
            self.invoke(runtime, token='demo-limited')
        self.assertEqual(caught.exception.code, 'NOT_FOUND')
        self.assertEqual(backend.sample_requests, [])

    def test_object_permissions_for_other_tenant_and_same_tenant_other_actor(self):
        runtime, backend = self.start()
        for order_id in ('ORD-2001', 'ORD-1003'):
            result = self.invoke(runtime, order_id)
            self.assertEqual(result['error']['code'], 'PERMISSION_DENIED', result)
            self.assertNotIn('data', result)
        self.assertEqual(len(backend.sample_requests), 2)

    def test_input_version_and_catalog_errors_make_no_backend_calls(self):
        runtime, backend = self.start()
        for overrides in ({'input': {}}, {'input': {'orderId': 123}}, {'input': {'orderId': 'ORD-1001', 'actor': 'bob'}},
                          {'version': '9.9.9'}, {'catalog_version': 'stale'}):
            with self.subTest(overrides=overrides), self.assertRaises(A2APIError):
                self.invoke(runtime, **overrides)
        self.assertEqual(backend.sample_requests, [])

    def test_schema_drift_and_private_error_data(self):
        def transform(path, payload):
            payload['internalSecret'] = 'not-for-the-model'
            return 200, payload
        runtime, backend = self.start(transform=transform)
        result = self.invoke(runtime)
        self.assertEqual(result['error']['code'], 'SCHEMA_MISMATCH', result)
        self.assertNotIn('not-for-the-model', json.dumps(result))
        self.assertNotIn('data', result)
        self.assertEqual(len(backend.sample_requests), 1)

    def test_malformed_timestamp_is_rejected(self):
        for timestamp in ('2026-10-28T15:00:00', '2026-10-28T15:00:00+09:99'):
            def transform(path, payload):
                if path.startswith('/shipments/'):
                    payload['asOf'] = timestamp
                return 200, payload
            runtime, _ = self.start(transform=transform)
            result = self.invoke(runtime)
            self.assertEqual(result['error']['code'], 'SCHEMA_MISMATCH', result)

    def test_order_identity_drift_stops_before_shipping(self):
        def transform(path, payload):
            payload['orderId'] = 'ORD-different'
            return 200, payload
        runtime, backend = self.start(transform=transform)
        result = self.invoke(runtime)
        self.assertEqual(result['error']['code'], 'CONTRACT_DRIFT', result)
        self.assertEqual(len(backend.sample_requests), 1)

    def test_shipping_order_relation_is_checked(self):
        def transform(path, payload):
            if path.startswith('/shipments/'):
                payload['orderId'] = 'ORD-different'
            return 200, payload
        runtime, _ = self.start(transform=transform)
        result = self.invoke(runtime)
        self.assertEqual(result['error']['code'], 'PRECONDITION_FAILED', result)
        self.assertNotIn('data', result)

    def test_runtime_rechecks_returned_tenant(self):
        def transform(path, payload):
            payload['tenantId'] = 'other-tenant'
            return 200, payload
        runtime, _ = self.start(transform=transform)
        result = self.invoke(runtime)
        self.assertEqual(result['error']['code'], 'PERMISSION_DENIED', result)

    def test_missing_resource_and_rate_limit_are_not_retried(self):
        runtime, backend = self.start()
        result = self.invoke(runtime, 'missing')
        self.assertEqual(result['error']['code'], 'RESOURCE_NOT_FOUND', result)
        self.assertEqual(len(backend.sample_requests), 1)
        limited, limited_backend = self.start(transform=lambda path, payload: (429, {'secret': 'private'}))
        result = self.invoke(limited)
        self.assertEqual(result['error']['code'], 'RATE_LIMITED', result)
        self.assertEqual(len(limited_backend.sample_requests), 1)
        self.assertNotIn('private', json.dumps(result))

    def test_timeout_and_response_size_limits(self):
        def transform(path, payload):
            time.sleep(0.12)
            return 200, payload
        manifest = sample_manifest()
        manifest['execution']['backendTimeoutMs'] = 30
        manifest['execution']['deadlineMs'] = 60
        runtime, backend = self.start(transform=transform, manifest=manifest)
        result = self.invoke(runtime)
        self.assertEqual(result['error']['code'], 'DEADLINE_EXCEEDED', result)
        self.assertEqual(len(backend.sample_requests), 1)
        runtime, _ = self.start()
        runtime.adapter.max_response_bytes = 32
        result = self.invoke(runtime)
        self.assertEqual(result['error']['code'], 'RESPONSE_TOO_LARGE', result)

    def test_fanout_overflow_is_not_silently_truncated(self):
        def transform(path, payload):
            payload['shipmentIds'] = [f'SHP-{i}' for i in range(11)]
            return 200, payload
        runtime, backend = self.start(transform=transform)
        result = self.invoke(runtime)
        self.assertEqual(result['error']['code'], 'SCHEMA_MISMATCH', result)
        self.assertEqual(len(backend.sample_requests), 1)

    def test_concurrent_invocations_keep_context_and_budgets_separate(self):
        runtime, _ = self.start()
        def invoke(index):
            if index % 2:
                return self.invoke(runtime, 'ORD-2001', 'demo-bob')
            return self.invoke(runtime)
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(invoke, range(8)))
        for index, result in enumerate(results):
            self.assertEqual(result['status'], 'succeeded', result)
            self.assertEqual(result['data']['orderId'], 'ORD-2001' if index % 2 else 'ORD-1001')
            self.assertEqual(result['stats']['backendCalls'], 2 if index % 2 else 3)
        self.assertEqual(len({r['executionId'] for r in results}), 8)

    def test_discovery_pagination_is_tied_to_query_context_and_snapshot(self):
        first = compile_contract(sample_manifest())
        manifest = sample_manifest()
        manifest['version'] = '0.2.0'
        catalog = Catalog([first, compile_contract(manifest)], allow_samples=True)
        page = catalog.discover('shipping', TOKENS['demo-alice'], limit=1)
        next_page = catalog.discover('shipping', TOKENS['demo-alice'], limit=1, cursor=page['nextCursor'])
        self.assertNotEqual(page['capabilities'][0]['version'], next_page['capabilities'][0]['version'])
        for cursor, query, context in [(page['nextCursor'], 'changed', TOKENS['demo-alice']),
                                       (page['nextCursor'], 'shipping', TOKENS['demo-bob']),
                                       ('invalid', 'shipping', TOKENS['demo-alice'])]:
            with self.subTest(cursor=cursor), self.assertRaises(A2APIError):
                catalog.discover(query, context, limit=1, cursor=cursor)

    def test_untrusted_routes_cannot_supply_an_origin_or_context(self):
        for origin, path, headers in [('http://user:pass@example.com', '/x', {}),
                                       ('http://example.com', '//evil.example/x', {}),
                                       ('http://example.com', '/x', {'X-A2API-Actor': 'bob'})]:
            with self.subTest(origin=origin), self.assertRaises(A2APIError):
                HTTPRoute(origin, path, headers=headers)


if __name__ == '__main__':
    unittest.main()
