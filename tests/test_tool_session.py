"""Host-selected function tools retain exact contracts over local and stdio calls."""

from contextlib import ExitStack
import importlib.util
import json
import os
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from a2api import A2APIError, Application, ExecutionContext, ToolSession, capability
from a2api.api import dispatch
from a2api.mcp_application import DirectApplications
from a2api.sample import create_backend, running
from a2api.tool_session import SEARCH_NAME, tool_bytes

ROOT = Path(__file__).resolve().parents[1]
CONTEXT = ExecutionContext('alice', 'tenant-a', frozenset())


def echo_app(count=2, *, calls=None):
    def echo(value: str, *, context: ExecutionContext) -> str:
        """Echo a value for the current caller."""
        if calls is not None:
            calls.append(value)
        return context.actor + ':' + value
    return Application([capability(id=f'sample.echo_{i:04}', effect='read')(echo) for i in range(count)])


class MutableClient:
    """Wire-bound test transport that can genuinely change catalog snapshots."""
    def __init__(self, app):
        self.runtime = DirectApplications(app)
        self.records = []
        self.drift = False

    async def list_tools(self):
        return SimpleNamespace(tools=[SimpleNamespace(name='a2api.' + method)
                                     for method in ('discover', 'describe', 'invoke')])

    async def call_tool(self, name, arguments):
        method = name.removeprefix('a2api.')
        self.records.append((method, arguments))
        try:
            if method == 'invoke' and self.drift:
                raise A2APIError('CONTRACT_DRIFT', 'changed', status=409)
            result = dispatch(self.runtime, method, arguments, CONTEXT)
        except A2APIError as error:
            result = {'error': error.problem()}
        return SimpleNamespace(structured_content=result)


class ToolSessionTests(unittest.IsolatedAsyncioTestCase):
    async def test_known_tools_need_no_model_search_and_input_is_exact(self):
        app = echo_app()
        host = ToolSession(app, CONTEXT)
        await host.prime(['sample.echo_0001'])
        tool = host.tools(include_search=False)[0]['function']
        self.assertEqual(tool['parameters'], app.describe('sample.echo_0001')['inputSchema'])
        self.assertNotIn('outputSchema', tool)
        for field in ('catalogVersion', 'version', 'context'):
            self.assertNotIn(field, tool['parameters']['properties'])
        tool['parameters']['required'].clear()
        name = tool['name']
        self.assertEqual((await host.call(name, {}))['error']['code'], 'INVALID_INPUT')
        self.assertEqual((await host.call(name, {'value': 'yes'}))['data'], 'alice:yes')
        before = host.stats
        self.assertEqual((await host.call(name, {'value': 'again'}))['data'], 'alice:again')
        self.assertEqual(host.stats['describe'], before['describe'])
        self.assertEqual(host.stats['discover'], before['discover'])
        self.assertEqual(host.stats['invoke'], 2)

    async def test_unknown_large_catalog_exposes_only_selected_functions(self):
        host = ToolSession(echo_app(1000), CONTEXT, search_limit=1)
        self.assertEqual(len(host.tools()), 1)
        result = await host.call(SEARCH_NAME, {'query': 'sample.echo_0753'})
        self.assertEqual(len(result['selected']), 1)
        self.assertEqual(len(host.tools()), 2)
        encoded = json.dumps(host.tools())
        self.assertNotIn('sample.echo_0000', encoded)
        self.assertNotIn('outputSchema', encoded)
        self.assertNotIn('inputSchema', json.dumps(result))
        name = result['selected'][0]['name']
        self.assertEqual((await host.call(name, {'value': 'large'}))['data'], 'alice:large')
        await host.select('sample.echo_0753')
        self.assertEqual(host.stats, {'discover': 2, 'describe': 1, 'invoke': 1, 'reused': 1, 'evicted': 0})
        # Large catalogs also support known functions without model-side search.
        await host.prime(['sample.echo_0753'])
        self.assertEqual(len(host.tools(include_search=False)), 1)

    async def test_budget_evicts_whole_tools_and_refuses_oversized_schema(self):
        app = echo_app(3)
        probe = ToolSession(app, CONTEXT, search_limit=1)
        await probe.prime(['sample.echo_0000'])
        budget = tool_bytes(probe.tools())
        host = ToolSession(app, CONTEXT, max_tool_bytes=budget, search_limit=1)
        first = (await host.select('sample.echo_0000'))['selected'][0]['name']
        second = await host.select('sample.echo_0001')
        self.assertEqual(second['evicted'], [first])
        self.assertLessEqual(tool_bytes(host.tools()), budget)
        self.assertEqual((await host.call(first, {'value': 'x'}))['error']['code'], 'NOT_SELECTED')
        tiny = ToolSession(app, CONTEXT, max_tool_bytes=tool_bytes(probe.tools()[:1]))
        result = await tiny.select('sample.echo_0000')
        self.assertEqual(result['omitted'][0]['reason'], 'SCHEMA_BUDGET')
        self.assertEqual(len(tiny.tools()), 1)
        with self.assertRaises(A2APIError):
            await tiny.prime(['sample.echo_0000'])

    async def test_refs_enum_bounds_defaults_and_result_validation_are_preserved(self):
        schema = {'type': 'object', 'properties': {'value': {'$ref': '#/$defs/value', 'default': 1}},
                  '$defs': {'value': {'type': 'integer', 'minimum': 1, 'maximum': 3, 'enum': [1, 3]}},
                  'required': [], 'additionalProperties': False}
        invoked = []
        @capability(id='sample.bounded', effect='read', input_schema=schema)
        def bounded(value: int = 1) -> int:
            invoked.append(value)
            return value
        app = Application([bounded])
        host = ToolSession(app, CONTEXT)
        await host.prime(['sample.bounded'])
        function = host.tools(include_search=False)[0]['function']
        self.assertEqual(function['parameters'], app.describe('sample.bounded')['inputSchema'])
        for bad in ({'value': 2}, {'value': 4}, {'value': '1'}, {'value': 1, 'context': {}}, {'value': float('nan')}):
            self.assertEqual((await host.call(function['name'], bad))['error']['code'], 'INVALID_INPUT')
        self.assertEqual(invoked, [])
        self.assertEqual((await host.call(function['name'], {}))['data'], 1)
        self.assertEqual((await host.call(function['name'], {'value': 3}))['data'], 3)
        self.assertEqual(invoked, [1, 3])
        app.invoke = lambda *a, **kw: {'status': 'succeeded', 'data': 'invalid',
                                      'completeness': {'complete': True}}
        self.assertEqual((await host.call(function['name'], {'value': 3}))['error']['code'], 'SCHEMA_MISMATCH')

    async def test_drift_invalidates_bindings_without_retry_and_contexts_are_separate(self):
        calls = []
        app = echo_app(calls=calls)
        client = MutableClient(app)
        host = await ToolSession.from_mcp(client)
        await host.prime(['sample.echo_0000'])
        name = host.tools(include_search=False)[0]['function']['name']
        client.drift = True
        self.assertEqual((await host.call(name, {'value': 'no'}))['error']['code'], 'CONTRACT_DRIFT')
        self.assertEqual(len(host.tools()), 1)
        self.assertEqual([x[0] for x in client.records].count('invoke'), 1)
        self.assertEqual(calls, [])
        client.drift = False
        client.runtime = DirectApplications(echo_app(3))
        await host.prime(['sample.echo_0002'])
        replacement = host.tools(include_search=False)[0]['function']['name']
        self.assertNotEqual(replacement, name)
        self.assertEqual((await host.call(name, {'value': 'old'}))['error']['code'], 'NOT_SELECTED')
        bob = ToolSession(app, ExecutionContext('bob', 'tenant-b', frozenset()))
        self.assertEqual((await bob.call(name, {'value': 'no'}))['error']['code'], 'NOT_SELECTED')
        await bob.prime(['sample.echo_0000'])
        bob_name = bob.tools(include_search=False)[0]['function']['name']
        self.assertEqual((await bob.call(bob_name, {'value': 'ok'}))['data'], 'bob:ok')


@unittest.skipUnless(importlib.util.find_spec('mcp'), 'Install a2api[mcp]')
class ToolSessionStdioTests(unittest.IsolatedAsyncioTestCase):
    async def test_model_host_refreshes_tools_and_reuses_the_same_conversation(self):
        spec = importlib.util.spec_from_file_location('selected_model_client', ROOT / 'examples/model-client/client.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        client = MutableClient(echo_app())
        host = await ToolSession.from_mcp(client)
        messages = [{'role': 'system', 'content': 'test'}]
        step = 0
        def response(base, model, history, tools, **options):
            nonlocal step
            step += 1
            if step == 1:
                self.assertEqual([item['function']['name'] for item in tools], [SEARCH_NAME])
                name, arguments = SEARCH_NAME, {'query': 'sample.echo_0000'}
            elif step in (2, 4):
                self.assertEqual(len(tools), 2)
                name = next(item['function']['name'] for item in tools if item['function']['name'] != SEARCH_NAME)
                arguments = {'value': 'yes'}
            else:
                return {'model': model, 'choices': [{'finish_reason': 'stop', 'message': {'content': 'alice:yes'}}],
                        'usage': {'prompt_tokens': 10, 'completion_tokens': 2, 'total_tokens': 12}}
            return {'model': model, 'choices': [{'finish_reason': 'tool_calls', 'message': {'content': None,
                'tool_calls': [{'id': str(step), 'type': 'function', 'function': {
                    'name': name, 'arguments': json.dumps(arguments)}}]}}],
                'usage': {'prompt_tokens': 10, 'completion_tokens': 2, 'total_tokens': 12}}
        with patch.object(module, 'chat', side_effect=response):
            for question in ('echo yes', 'again'):
                result = await module.run_question(client, question, base_url='https://unused.invalid/v1',
                    model='test', binding='selected', session=host, messages=messages)
                self.assertNotIn('hostError', result)
                self.assertTrue(result['usageAvailable'])
        self.assertEqual(host.stats['discover'], 1)
        self.assertEqual(host.stats['describe'], 1)
        self.assertEqual(host.stats['invoke'], 2)

    async def test_real_http_stdio_chain_reuses_tools_without_changing_mcp_listing(self):
        from mcp import Client
        from mcp.client.stdio import StdioServerParameters
        with ExitStack() as stack:
            backend = create_backend()
            origin = stack.enter_context(running(backend))
            params = StdioServerParameters(command=sys.executable,
                args=[str(ROOT / 'examples/native-orders/mcp_server.py'), '--source', 'openapi',
                      '--backend-origin', origin], env={**os.environ, 'PYTHONPATH': str(ROOT / 'src')})
            async with Client(params, read_timeout_seconds=15) as client:
                before = (await client.list_tools()).model_dump(mode='json', by_alias=True)
                host = await ToolSession.from_mcp(client, search_limit=1)
                found = await host.select('legacy.getorder')
                order = await host.call(found['selected'][0]['name'], {'path': {'orderId': 'ORD-1001'}})
                found = await host.select('legacy.getshipment')
                shipment_name = found['selected'][0]['name']
                for shipment_id in order['data']['shipmentIds']:
                    result = await host.call(shipment_name, {'path': {'shipmentId': shipment_id}})
                    self.assertEqual(result['data']['orderId'], order['data']['orderId'])
                self.assertEqual(backend.sample_requests,
                    ['/orders/ORD-1001', '/shipments/SHP-501', '/shipments/SHP-502'])
                self.assertEqual(host.stats['describe'], 2)
                after = (await client.list_tools(cache_mode='refresh')).model_dump(mode='json', by_alias=True)
                self.assertEqual(before, after)
                self.assertEqual(len(after['tools']), 3)
