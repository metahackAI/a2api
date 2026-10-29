"""Direct applications over real MCP stdio, with catalog-independent tool schemas."""

from contextlib import ExitStack
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

from jsonschema import Draft202012Validator

from a2api import A2APIError, Application, ExecutionContext, capability
from a2api.sample import TOKENS, create_backend, running

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / 'examples/native-orders/mcp_server.py'
HAS_MCP = importlib.util.find_spec('mcp') is not None
if HAS_MCP:
    from mcp import Client
    from mcp.client.stdio import StdioServerParameters
    from a2api.mcp_bridge import create_mcp_server


def compact_bytes(value):
    return len(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8'))


def echo_app(count):
    def echo(value: str) -> str:
        """Echo the requested value."""
        return value
    return Application([capability(id=f'benchmark.echo_{index}', effect='read')(echo) for index in range(count)])


@unittest.skipUnless(HAS_MCP, 'Install a2api[mcp] for direct application bridge tests')
class DirectMCPTests(unittest.IsolatedAsyncioTestCase):
    async def test_tool_list_size_and_content_are_constant_for_one_and_one_hundred_capabilities(self):
        listings = []
        for count in (1, 100):
            async with Client(create_mcp_server(echo_app(count), TOKENS['demo-alice']), read_timeout_seconds=10) as client:
                listed = await client.list_tools()
                value = listed.model_dump(mode='json', by_alias=True, exclude_none=True)
                listings.append(value)
                self.assertEqual([tool.name for tool in listed.tools], ['a2api.discover', 'a2api.describe', 'a2api.invoke'])
                self.assertNotIn('benchmark.echo_', json.dumps(value))
                self.assertNotIn('Echo the requested value.', json.dumps(value))
                found = (await client.call_tool('a2api.discover', {'query': 'echo', 'limit': 1})).structured_content
                item = found['capabilities'][0]
                described = await client.call_tool('a2api.describe', {'id': item['id'], 'version': item['version']})
                self.assertIn('value', described.structured_content['capability']['inputSchema']['properties'])
                after = await client.list_tools(cache_mode='refresh')
                self.assertEqual(value, after.model_dump(mode='json', by_alias=True, exclude_none=True))
        self.assertEqual(listings[0], listings[1])
        self.assertEqual(compact_bytes(listings[0]), compact_bytes(listings[1]))

    async def test_generic_envelope_keeps_selected_business_validation_on_the_server(self):
        app = echo_app(1)
        async with Client(create_mcp_server(app, TOKENS['demo-alice']), read_timeout_seconds=10) as client:
            tools = {tool.name: tool for tool in (await client.list_tools()).tools}
            catalog = (await client.call_tool('a2api.discover', {})).structured_content
            app.invoke = lambda *args, **kwargs: {'status': 'succeeded', 'data': 17, 'completeness': {'complete': True}}
            self.assertTrue(Draft202012Validator(tools['a2api.invoke'].output_schema).is_valid(app.invoke()))
            result = await client.call_tool('a2api.invoke', {'id': 'benchmark.echo_0', 'version': '0.1.0',
                'catalogVersion': catalog['catalogVersion'], 'input': {'value': 'ok'}})
            self.assertTrue(result.is_error)
            self.assertEqual(result.structured_content['error']['code'], 'SCHEMA_MISMATCH')
            self.assertNotIn('data', result.structured_content)

    async def test_cursor_is_bound_to_query_limit_catalog_and_caller(self):
        app = echo_app(3)
        async with Client(create_mcp_server(app, TOKENS['demo-alice']), read_timeout_seconds=10) as alice:
            first = (await alice.call_tool('a2api.discover', {'limit': 1})).structured_content
            second = (await alice.call_tool('a2api.discover', {'limit': 1, 'cursor': first['nextCursor']})).structured_content
            self.assertNotEqual(first['capabilities'], second['capabilities'])
            for arguments in ({'limit': 2, 'cursor': first['nextCursor']}, {'query': 'different', 'limit': 1, 'cursor': first['nextCursor']},
                              {'limit': 1, 'cursor': 'invalid'}):
                result = await alice.call_tool('a2api.discover', arguments)
                self.assertTrue(result.is_error)
                self.assertEqual(result.structured_content['error']['code'], 'INVALID_CURSOR')
        async with Client(create_mcp_server(app, TOKENS['demo-bob']), read_timeout_seconds=10) as bob:
            result = await bob.call_tool('a2api.discover', {'limit': 1, 'cursor': first['nextCursor']})
            self.assertEqual(result.structured_content['error']['code'], 'INVALID_CURSOR')

    async def test_host_context_is_forwarded_and_no_identity_override_can_invoke_a_body(self):
        calls = []
        @capability(id='host.identity', effect='read')
        def identity(*, context: ExecutionContext) -> str:
            calls.append(context.actor)
            return context.actor
        async with Client(create_mcp_server(Application([identity]), TOKENS['demo-alice']), read_timeout_seconds=10) as client:
            found = (await client.call_tool('a2api.discover', {})).structured_content
            base = {'id': 'host.identity', 'version': '0.1.0', 'catalogVersion': found['catalogVersion'], 'input': {}}
            for arguments, code in [({**base, 'catalogVersion': 'stale'}, 'CONTRACT_DRIFT'),
                                    ({**base, 'version': '9.0.0'}, 'NOT_FOUND'),
                                    ({**base, 'input': {'context': {'actor': 'bob'}}}, 'INVALID_INPUT'),
                                    ({**base, 'actor': 'bob'}, 'INVALID_REQUEST')]:
                result = await client.call_tool('a2api.invoke', arguments)
                self.assertTrue(result.is_error)
                self.assertEqual(result.structured_content['error']['code'], code)
            self.assertEqual(calls, [])
            result = await client.call_tool('a2api.invoke', {**base, 'requestId': 'native-request'})
            self.assertEqual(result.structured_content['data'], 'alice')
            self.assertEqual(result.structured_content['requestId'], 'native-request')
            self.assertEqual(calls, ['alice'])

    def test_ambiguous_application_ids_and_invalid_factories_are_rejected(self):
        app = echo_app(1)
        with self.assertRaises(A2APIError) as caught:
            create_mcp_server([app, app], TOKENS['demo-alice'])
        self.assertEqual(caught.exception.code, 'INVALID_CONTRACT')
        for apps in [[], ['module:path'], object()]:
            with self.assertRaises(TypeError):
                create_mcp_server(apps, TOKENS['demo-alice'])


@unittest.skipUnless(HAS_MCP, 'Install a2api[mcp] for direct application stdio tests')
class DirectStdioTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.backend = create_backend()
        self.origin = self.stack.enter_context(running(self.backend))

    def parameters(self, source='both', user='alice'):
        return StdioServerParameters(command=sys.executable,
            args=[str(SERVER), '--source', source, '--sample-user', user, '--backend-origin', self.origin],
            env={**os.environ, 'PYTHONPATH': str(ROOT / 'src')})

    async def test_both_app_types_describe_and_invoke_over_real_stdio(self):
        async with Client(self.parameters(), read_timeout_seconds=15) as client:
            listed = await client.list_tools()
            tools = {tool.name: tool for tool in listed.tools}
            before = listed.model_dump(mode='json', by_alias=True, exclude_none=True)
            found = await client.call_tool('a2api.discover', {})
            catalog = found.structured_content
            self.assertEqual({item['id'] for item in catalog['capabilities']},
                {'legacy.getorder', 'legacy.getshipment', 'orders.lookup', 'shipping.list'})
            descriptors = {}
            for item in catalog['capabilities']:
                result = await client.call_tool('a2api.describe', {'id': item['id'], 'version': item['version']})
                self.assertFalse(result.is_error)
                descriptor = result.structured_content['capability']
                self.assertEqual(set(descriptor), {'id', 'version', 'summary', 'effects', 'inputSchema', 'outputSchema'})
                self.assertNotIn('ownerId', json.dumps(descriptor))
                self.assertNotIn('context', json.dumps(descriptor))
                descriptors[item['id']] = descriptor
            self.assertEqual(self.backend.sample_requests, [])
            async def invoke(identifier, input):
                result = await client.call_tool('a2api.invoke', {'id': identifier, 'version': '0.1.0',
                    'catalogVersion': catalog['catalogVersion'], 'input': input})
                self.assertFalse(result.is_error, result)
                Draft202012Validator(tools['a2api.invoke'].output_schema).validate(result.structured_content)
                Draft202012Validator(descriptors[identifier]['outputSchema']).validate(result.structured_content['data'])
                return result.structured_content['data']
            order = await invoke('legacy.getorder', {'path': {'orderId': 'ORD-1001'}})
            shipments = [await invoke('legacy.getshipment', {'path': {'shipmentId': identifier}}) for identifier in order['shipmentIds']]
            self.assertEqual(len(shipments), 2)
            self.assertEqual(self.backend.sample_requests, ['/orders/ORD-1001', '/shipments/SHP-501', '/shipments/SHP-502'])
            native = await invoke('orders.lookup', {'orderId': 'ORD-1001'})
            self.assertEqual(native['orderId'], order['orderId'])
            self.assertEqual(len(await invoke('shipping.list', {'orderId': 'ORD-1001'})), 1)
            self.assertEqual(await invoke('shipping.list', {'orderId': 'ORD-1002'}), [])
            self.assertEqual(len(self.backend.sample_requests), 3)
            self.assertEqual(before, (await client.list_tools(cache_mode='refresh')).model_dump(mode='json', by_alias=True, exclude_none=True))

    async def test_each_application_type_can_be_hosted_alone(self):
        for source, expected in [('python', {'orders.lookup', 'shipping.list'}), ('openapi', {'legacy.getorder', 'legacy.getshipment'})]:
            async with Client(self.parameters(source), read_timeout_seconds=15) as client:
                found = (await client.call_tool('a2api.discover', {})).structured_content
                self.assertEqual({item['id'] for item in found['capabilities']}, expected)

    async def test_stdio_permission_denial_for_openapi_and_native(self):
        async with Client(self.parameters(user='bob'), read_timeout_seconds=15) as client:
            found = (await client.call_tool('a2api.discover', {})).structured_content
            for identifier, input in [('orders.lookup', {'orderId': 'ORD-1001'}),
                                      ('legacy.getorder', {'path': {'orderId': 'ORD-1001'}})]:
                result = await client.call_tool('a2api.invoke', {'id': identifier, 'version': '0.1.0',
                    'catalogVersion': found['catalogVersion'], 'input': input})
                self.assertTrue(result.is_error)
                self.assertEqual(result.structured_content['error']['code'], 'PERMISSION_DENIED')
                self.assertNotIn('data', result.structured_content)

    async def test_stdio_rejects_input_and_raw_response_errors(self):
        async with Client(self.parameters('openapi'), read_timeout_seconds=15) as client:
            found = (await client.call_tool('a2api.discover', {})).structured_content
            base = {'id': 'legacy.getorder', 'version': '0.1.0', 'catalogVersion': found['catalogVersion']}
            invalid = await client.call_tool('a2api.invoke', {**base, 'input': {'path': {'orderId': 17}}})
            self.assertEqual(invalid.structured_content['error']['code'], 'INVALID_INPUT')
            self.assertEqual(self.backend.sample_requests, [])
        broken = create_backend(transform=lambda path, payload: (200, {**payload, 'ownerId': 17, 'secret': 'must-not-escape'}))
        self.origin = self.stack.enter_context(running(broken))
        async with Client(self.parameters('openapi'), read_timeout_seconds=15) as client:
            found = (await client.call_tool('a2api.discover', {})).structured_content
            result = await client.call_tool('a2api.invoke', {'id': 'legacy.getorder', 'version': '0.1.0',
                'catalogVersion': found['catalogVersion'], 'input': {'path': {'orderId': 'ORD-1001'}}})
            self.assertTrue(result.is_error)
            self.assertEqual(result.structured_content['error']['code'], 'SCHEMA_MISMATCH')
            self.assertNotIn('must-not-escape', json.dumps(result.structured_content))

    def test_stdio_eof_and_documented_client_example(self):
        process = subprocess.run([sys.executable, str(SERVER), '--source', 'python'], input='', text=True,
            capture_output=True, timeout=15, cwd=ROOT, env={**os.environ, 'PYTHONPATH': str(ROOT / 'src')})
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stdout, '')
        demo = subprocess.run([sys.executable, str(SERVER.with_name('mcp_client.py'))], text=True, capture_output=True,
            timeout=20, cwd=ROOT, env={**os.environ, 'PYTHONPATH': str(ROOT / 'src')})
        self.assertEqual(demo.returncode, 0, demo.stderr)
        report = json.loads(demo.stdout)
        self.assertEqual(len(report['openapi']['shipments']), 2)
        self.assertEqual(report['python']['order']['orderId'], 'ORD-1001')
