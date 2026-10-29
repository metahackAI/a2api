"""Official MCP client tests; install a2api[mcp] to run this suite."""

import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from contextlib import ExitStack

from jsonschema import Draft202012Validator

from a2api import Catalog, Runtime, compile_contract
from a2api.sample import TOKENS, create_backend, running, sample_manifest, sample_runtime

HAS_MCP = importlib.util.find_spec('mcp') is not None
if HAS_MCP:
    from mcp import Client
    from mcp.client.stdio import StdioServerParameters
    from mcp.shared.exceptions import MCPError
    from a2api.mcp_bridge import create_mcp_server

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['a2api.discover', 'a2api.describe', 'a2api.invoke']


@unittest.skipUnless(HAS_MCP, 'Install a2api[mcp] to test MCP interoperability')
class BridgeTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.backend = create_backend()
        origin = self.stack.enter_context(running(self.backend))
        self.runtime = sample_runtime(origin)

    def client(self, *, user='alice', runtime=None, **options):
        return Client(create_mcp_server(runtime or self.runtime, TOKENS['demo-' + user]), **options)

    def arguments(self, **updates):
        arguments = {'id': 'order.shipping_status', 'version': '0.1.0',
                     'catalogVersion': self.runtime.catalog.version, 'input': {'orderId': 'ORD-1001'}}
        arguments.update(updates)
        return arguments

    def assert_result(self, result, schema):
        self.assertIsNotNone(result.structured_content)
        self.assertEqual(len(result.content), 1)
        self.assertEqual(json.loads(result.content[0].text), result.structured_content)
        Draft202012Validator(schema).validate(result.structured_content)
        return result.structured_content

    async def test_fixed_tool_list_schemas_and_annotations(self):
        async with self.client() as client:
            before = await client.list_tools()
            self.assertEqual([tool.name for tool in before.tools], NAMES)
            for tool in before.tools:
                Draft202012Validator.check_schema(tool.input_schema)
                Draft202012Validator.check_schema(tool.output_schema)
                self.assertTrue(tool.annotations.read_only_hint)
                self.assertFalse(tool.annotations.destructive_hint)
                self.assertNotIn('actor', tool.input_schema['properties'])
                self.assertFalse(tool.input_schema['additionalProperties'])
            await client.call_tool('a2api.discover', {'query': '배송'})
            after = await client.list_tools(cache_mode='refresh')
            self.assertEqual([t.model_dump() for t in before.tools], [t.model_dump() for t in after.tools])
        self.assertEqual(self.backend.sample_requests, [])

    async def test_discover_describe_invoke_and_business_output_schema(self):
        async with self.client() as client:
            tools = {tool.name: tool for tool in (await client.list_tools()).tools}
            found = await client.call_tool('a2api.discover', {'query': '배송 조회'})
            self.assertFalse(found.is_error)
            discovery = self.assert_result(found, tools['a2api.discover'].output_schema)
            item = discovery['capabilities'][0]
            described = await client.call_tool('a2api.describe', {'id': item['id'], 'version': item['version']})
            description = self.assert_result(described, tools['a2api.describe'].output_schema)
            invoked = await client.call_tool('a2api.invoke', {
                'id': item['id'], 'version': item['version'], 'catalogVersion': discovery['catalogVersion'],
                'input': {'orderId': 'ORD-1001'}, 'requestId': 'mcp-test-1',
            })
            self.assertFalse(invoked.is_error)
            result = self.assert_result(invoked, tools['a2api.invoke'].output_schema)
            self.assertEqual(result['status'], 'succeeded')
            self.assertEqual(result['requestId'], 'mcp-test-1')
            self.assertEqual(result['stats']['backendCalls'], 3)
            self.assertEqual([s['shipmentId'] for s in result['data']['shipments']], ['SHP-501', 'SHP-502'])
            self.assertNotIn('ownerId', json.dumps(result))
            self.assertNotIn('tenantId', json.dumps(result))
            Draft202012Validator(description['capability']['outputSchema']).validate(result['data'])
            invalid = copy.deepcopy(result)
            invalid['data']['shipments'][0]['status'] = 'made-up-status'
            self.assertTrue(Draft202012Validator(tools['a2api.invoke'].output_schema).is_valid(invalid))
            self.assertFalse(Draft202012Validator(description['capability']['outputSchema']).is_valid(invalid['data']))
            self.assertNotIn('provenance', description['capability'])
            self.assertNotIn('operations', description['capability'])

    async def test_empty_shipping_collection(self):
        async with self.client() as client:
            result = await client.call_tool('a2api.invoke', self.arguments(input={'orderId': 'ORD-1002'}))
            self.assertFalse(result.is_error)
            self.assertEqual(result.structured_content['data']['shipments'], [])
            self.assertEqual(result.structured_content['stats']['backendCalls'], 1)

    async def test_preflight_errors_have_is_error_and_conform_to_output_schema(self):
        async with self.client() as client:
            tools = {tool.name: tool for tool in (await client.list_tools()).tools}
            for arguments, code in [(self.arguments(catalogVersion='stale'), 'CONTRACT_DRIFT'),
                                     (self.arguments(input={}), 'INVALID_INPUT'),
                                     (self.arguments(version='9.9.9'), 'NOT_FOUND')]:
                with self.subTest(code=code):
                    result = await client.call_tool('a2api.invoke', arguments)
                    self.assertTrue(result.is_error)
                    payload = self.assert_result(result, tools['a2api.invoke'].output_schema)
                    self.assertEqual(payload['error']['code'], code)
        self.assertEqual(self.backend.sample_requests, [])

    async def test_invalid_controls_and_context_spoofing_are_rejected(self):
        async with self.client() as client:
            for name, arguments in [('a2api.discover', {'limit': True}),
                                     ('a2api.discover', {'actor': 'bob', 'tenant': 'tenant-b'}),
                                     ('a2api.describe', {'id': 'order.shipping_status'}),
                                     ('a2api.invoke', self.arguments(actor='bob'))]:
                with self.subTest(name=name, arguments=arguments):
                    result = await client.call_tool(name, arguments)
                    self.assertTrue(result.is_error)
                    self.assertEqual(result.structured_content['error']['code'], 'INVALID_REQUEST')
        self.assertEqual(self.backend.sample_requests, [])

    async def test_insufficient_scope_filters_catalog_and_result_schema(self):
        async with self.client(user='limited') as client:
            tools = {tool.name: tool for tool in (await client.list_tools()).tools}
            self.assertEqual(list(tools), NAMES)
            self.assertNotIn('order.shipping_status', json.dumps(tools['a2api.invoke'].output_schema))
            result = await client.call_tool('a2api.discover', {})
            self.assertFalse(result.is_error)
            self.assertEqual(result.structured_content['capabilities'], [])
            for name, arguments in [('a2api.describe', {'id': 'order.shipping_status', 'version': '0.1.0'}),
                                     ('a2api.invoke', self.arguments())]:
                result = await client.call_tool(name, arguments)
                payload = self.assert_result(result, tools[name].output_schema)
                self.assertTrue(result.is_error)
                self.assertEqual(payload['error']['code'], 'NOT_FOUND')
        self.assertEqual(self.backend.sample_requests, [])

    async def test_object_access_failure_preserves_failed_envelope(self):
        async with self.client() as client:
            tools = {tool.name: tool for tool in (await client.list_tools()).tools}
            result = await client.call_tool('a2api.invoke', self.arguments(input={'orderId': 'ORD-2001'}))
            self.assertTrue(result.is_error)
            payload = self.assert_result(result, tools['a2api.invoke'].output_schema)
            self.assertEqual(payload['status'], 'failed')
            self.assertEqual(payload['error']['code'], 'PERMISSION_DENIED')
            self.assertEqual(payload['stats']['backendCalls'], 1)
            self.assertNotIn('data', payload)

    async def test_upstream_schema_failure_is_mcp_tool_error(self):
        def transform(path, payload):
            payload['unexpected'] = 'private-backend-value'
            return 200, payload
        backend = create_backend(transform=transform)
        origin = self.stack.enter_context(running(backend))
        async with self.client(runtime=sample_runtime(origin)) as client:
            result = await client.call_tool('a2api.invoke', self.arguments())
            self.assertTrue(result.is_error)
            self.assertEqual(result.structured_content['error']['code'], 'SCHEMA_MISMATCH')
            self.assertNotIn('private-backend-value', json.dumps(result.structured_content))

    async def test_unexpected_host_error_is_sanitized(self):
        def broken(*args, **kwargs):
            raise RuntimeError('do-not-expose-this-secret')
        self.runtime.discover = broken
        async with self.client() as client:
            result = await client.call_tool('a2api.discover', {})
            self.assertTrue(result.is_error)
            self.assertEqual(result.structured_content['error']['code'], 'INTERNAL_ERROR')
            self.assertNotIn('do-not-expose-this-secret', result.content[0].text)

    async def test_bridge_rejects_invalid_output_from_a_host(self):
        self.runtime.discover = lambda *args, **kwargs: {'unexpected': 'payload'}
        async with self.client() as client:
            result = await client.call_tool('a2api.discover', {})
            self.assertTrue(result.is_error)
            self.assertEqual(result.structured_content['error']['code'], 'SCHEMA_MISMATCH')

    async def test_unknown_tool_and_tools_cursor_are_protocol_errors(self):
        async with self.client() as client:
            with self.assertRaises(MCPError) as caught:
                await client.call_tool('a2api.unknown', {})
            self.assertEqual(caught.exception.code, -32602)
            with self.assertRaises(MCPError) as caught:
                await client.list_tools(cursor='unknown', cache_mode='refresh')
            self.assertEqual(caught.exception.code, -32602)

    async def test_discovery_cursor_round_trip(self):
        manifest = sample_manifest()
        manifest['version'] = '0.2.0'
        catalog = Catalog([compile_contract(sample_manifest()), compile_contract(manifest)], allow_samples=True)
        runtime = Runtime(catalog, self.runtime.adapter)
        async with self.client(runtime=runtime) as client:
            first = (await client.call_tool('a2api.discover', {'limit': 1})).structured_content
            second = (await client.call_tool('a2api.discover', {'limit': 1, 'cursor': first['nextCursor']})).structured_content
            self.assertEqual(first['capabilities'][0]['version'], '0.1.0')
            self.assertEqual(second['capabilities'][0]['version'], '0.2.0')

    async def test_independent_host_contexts_share_runtime_without_identity_leak(self):
        import asyncio
        async with self.client() as alice, self.client(user='bob') as bob:
            first, second = await asyncio.gather(
                alice.call_tool('a2api.invoke', self.arguments()),
                bob.call_tool('a2api.invoke', self.arguments(input={'orderId': 'ORD-2001'})),
            )
            self.assertFalse(first.is_error)
            self.assertFalse(second.is_error)
            self.assertEqual(first.structured_content['data']['orderId'], 'ORD-1001')
            self.assertEqual(second.structured_content['data']['orderId'], 'ORD-2001')

    async def test_legacy_mcp_handshake_is_supported(self):
        async with self.client(mode='legacy') as client:
            self.assertEqual([tool.name for tool in (await client.list_tools()).tools], NAMES)
            result = await client.call_tool('a2api.discover', {})
            self.assertFalse(result.is_error)

    def test_factory_requires_host_context(self):
        with self.assertRaises(TypeError):
            create_mcp_server(self.runtime, {'actor': 'alice', 'tenant': 'tenant-a'})


@unittest.skipUnless(HAS_MCP, 'Install a2api[mcp] to test stdio interoperability')
class StdioTests(unittest.IsolatedAsyncioTestCase):
    def parameters(self, user='alice'):
        return StdioServerParameters(command=sys.executable, args=['-m', 'a2api', 'mcp', '--sample-user', user],
                                     env={'PYTHONPATH': str(ROOT / 'src')})

    async def test_official_client_executes_real_stdio_server(self):
        async with Client(self.parameters(), read_timeout_seconds=10) as client:
            self.assertEqual([t.name for t in (await client.list_tools()).tools], NAMES)
            found = (await client.call_tool('a2api.discover', {'query': '배송 조회'})).structured_content
            item = found['capabilities'][0]
            described = await client.call_tool('a2api.describe', {'id': item['id'], 'version': item['version']})
            self.assertFalse(described.is_error)
            result = await client.call_tool('a2api.invoke', {'id': item['id'], 'version': item['version'],
                                            'catalogVersion': found['catalogVersion'], 'input': {'orderId': 'ORD-1001'}})
            self.assertFalse(result.is_error)
            self.assertEqual(result.structured_content['stats']['backendCalls'], 3)
            self.assertEqual(len(result.structured_content['data']['shipments']), 2)

    async def test_stdio_host_identity_and_error_flag(self):
        async with Client(self.parameters('bob'), read_timeout_seconds=10) as client:
            found = (await client.call_tool('a2api.discover', {})).structured_content
            arguments = {'id': 'order.shipping_status', 'version': '0.1.0',
                         'catalogVersion': found['catalogVersion'], 'input': {'orderId': 'ORD-2001'}}
            result = await client.call_tool('a2api.invoke', arguments)
            self.assertFalse(result.is_error)
            self.assertEqual(result.structured_content['stats']['backendCalls'], 2)
            arguments['input']['orderId'] = 'ORD-1001'
            denied = await client.call_tool('a2api.invoke', arguments)
            self.assertTrue(denied.is_error)
            self.assertEqual(denied.structured_content['error']['code'], 'PERMISSION_DENIED')

    async def test_stdio_legacy_initialization_and_tool_calls(self):
        async with Client(self.parameters(), mode='legacy', read_timeout_seconds=10) as client:
            self.assertEqual([tool.name for tool in (await client.list_tools()).tools], NAMES)
            result = await client.call_tool('a2api.discover', {})
            self.assertFalse(result.is_error)
            self.assertEqual(result.structured_content['capabilities'][0]['id'], 'order.shipping_status')

    def test_stdio_eof_exits_without_printing_nonprotocol_stdout(self):
        result = subprocess.run([sys.executable, '-m', 'a2api', 'mcp'], input='', text=True,
                                capture_output=True, timeout=15, cwd=ROOT,
                                env={**os.environ, 'PYTHONPATH': str(ROOT / 'src')})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '')

    def test_mcp_demo_command_is_reproducible(self):
        result = subprocess.run([sys.executable, '-m', 'a2api', 'mcp-demo'], capture_output=True, text=True,
                                timeout=20, cwd=ROOT, env={**os.environ, 'PYTHONPATH': str(ROOT / 'src')})
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['tools'], NAMES)
        self.assertFalse(report['isError'])
        self.assertEqual(report['invoke']['status'], 'succeeded')
        self.assertEqual(report['invoke']['stats']['backendCalls'], 3)


if __name__ == '__main__':
    unittest.main()
