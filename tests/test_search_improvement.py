"""Exact identity, field relevance and bounded conditional host pagination."""

from copy import deepcopy
import importlib.util
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from a2api import A2APIError, Application, ExecutionContext, ToolSession, capability
from a2api.api import dispatch
from a2api.discovery_metadata import schema_search_fields, search_tokens
from a2api.mcp_application import DirectApplications
from a2api.tool_session import SEARCH_NAME, tool_bytes

CONTEXT = ExecutionContext('alice', 'tenant-a', frozenset())


def sample(count=12):
    def read(value: str = 'ok') -> str:return value
    return Application([capability(id=f'catalog.item_{index:02}', effect='read',
        summary='Read an item', keywords=['item'])(read) for index in range(count)])


class Client:
    def __init__(self, app):self.runtime = DirectApplications(app)

    async def list_tools(self):
        return SimpleNamespace(tools=[SimpleNamespace(name='a2api.' + method) for method in ('discover', 'describe', 'invoke')])

    async def call_tool(self, name, arguments):
        try:result = dispatch(self.runtime, name.removeprefix('a2api.'), arguments, CONTEXT)
        except A2APIError as error:result = {'error': error.problem()}
        return SimpleNamespace(structured_content=result)


class SearchIndexTests(unittest.TestCase):
    def test_exact_id_excludes_prefix_neighbors_but_keeps_real_versions(self):
        def get() -> str:return 'ok'
        target = capability(id='api.get', effect='read')(get)
        neighbor = capability(id='api.get_branch', effect='read')(get)
        wire = DirectApplications(Application([neighbor, target]))
        found = wire.discover('api.get', CONTEXT, limit=1)
        self.assertEqual([item['id'] for item in found['capabilities']], ['api.get'])
        self.assertIsNone(found['nextCursor'])

        class Versions(Application):
            def descriptors(self):
                base = super().descriptors()[0]
                return tuple({**deepcopy(base), 'version': version} for version in ('1.0', '2.0'))
        versioned = DirectApplications(Versions([target]))
        first = versioned.discover('api.get', CONTEXT, limit=1)
        second = versioned.discover('api.get', CONTEXT, limit=1, cursor=first['nextCursor'])
        self.assertEqual(second['capabilities'][0]['version'], '2.0')

    def test_root_fields_beat_incidental_nested_fields_and_body_repetition(self):
        schema = {'type': 'object', 'properties': {'default_branch': {'type': 'string'},
            'archived': {'type': 'boolean'}}, 'additionalProperties': False}
        nested = {'type': 'object', 'properties': {'head': {'type': 'object',
            'properties': {'repo': schema}}}}
        def get() -> dict:return {}
        target = capability(id='api.repository', effect='read', summary='Get a repository', output_schema=schema)(get)
        other = capability(id='api.pull', effect='read', summary='Get pull requests', output_schema=nested)(get)
        wire = DirectApplications(Application([other, target]))
        result = wire.discover('repository default branch archived', CONTEXT)
        self.assertEqual(result['capabilities'][0]['id'], 'api.repository')
        self.assertNotIn('default_branch', schema_search_fields(nested)[0])
        self.assertNotIn('default_branch', schema_search_fields(nested)[1])
        cycle = {'$ref': '#/$defs/cycle', '$defs': {'cycle': {'$ref': '#/$defs/cycle'}}}
        self.assertEqual(schema_search_fields(cycle), ('', ''))
        self.assertEqual(schema_search_fields({'oneOf': [schema]}), ('', ''))
        self.assertEqual(schema_search_fields({'$ref': 'https://never-fetch.invalid/schema'}), ('', ''))
        self.assertEqual(schema['properties']['archived'], {'type': 'boolean'})

    def test_name_boundaries_and_original_operation_aliases(self):
        terms = search_tokens('defaultBranch default_branch get-purchase/order')
        self.assertTrue({'default', 'branch', 'get', 'purchase', 'order'} <= terms)
        from a2api import HTTPDeployment, convert
        from a2api.importers import OpenAPIImporter
        source = OpenAPIImporter({'openapi': '3.1.0', 'info': {'title': 'orders', 'version': '1'},
            'paths': {'/orders': {'get': {'operationId': 'getPurchaseOrder', 'summary': 'Read purchase data',
                'responses': {'200': {'description': 'ok', 'content': {'application/json': {'schema': {'type': 'string'}}}}}}}}}, namespace='legacy')
        app = convert(source, operations={'getPurchaseOrder': {'effect': 'read'}}, deployment=HTTPDeployment('http://127.0.0.1:1'))
        wire = DirectApplications(app)
        for query in ('getPurchaseOrder', 'get_purchase_order', 'get-purchase/order'):
            self.assertEqual(wire.discover(query, CONTEXT)['capabilities'][0]['id'], 'legacy.getpurchaseorder')
        self.assertNotIn('aliases', app.describe('legacy.getpurchaseorder'))

    def test_cursor_binds_caller_and_search_revision(self):
        app = sample()
        wire = DirectApplications(app)
        first = wire.discover('item', CONTEXT, limit=1)
        for caller in (ExecutionContext('bob', 'tenant-a', frozenset()),
                       ExecutionContext('alice', 'tenant-b', frozenset()),
                       ExecutionContext('alice', 'tenant-a', frozenset({'other'}))):
            with self.assertRaises(A2APIError):wire.discover('item', caller, limit=1, cursor=first['nextCursor'])
        with patch('a2api.mcp_application.SEARCH_REVISION', 'test-new-ranking'):
            changed = DirectApplications(app)
        self.assertNotEqual(wire.version, changed.version)
        with self.assertRaises(A2APIError):changed.discover('item', CONTEXT, limit=1, cursor=first['nextCursor'])


class SearchPageTests(unittest.IsolatedAsyncioTestCase):
    async def test_repeats_more_cap_and_input_validation_without_api_execution(self):
        host = ToolSession(sample(), CONTEXT)
        before = await host.call(SEARCH_NAME, {'query': 'item', 'more': True})
        self.assertEqual(before['error']['code'], 'SEARCH_NOT_STARTED')
        first = await host.call(SEARCH_NAME, {'query': 'item'})
        repeated = await host.call(SEARCH_NAME, {'query': 'item'})
        self.assertEqual(first['selected'], repeated['selected'])
        self.assertTrue(first['progress'])
        self.assertFalse(repeated['progress'])
        second = await host.call(SEARCH_NAME, {'query': 'ITEM', 'more': True})
        third = await host.select('item', more=True)
        self.assertEqual((second['page'], third['page']), (2, 3))
        names = [item['name'] for page in (first, second, third) for item in page['selected']]
        self.assertEqual(len(set(names)), 9)
        self.assertFalse(third['moreAvailable'])
        self.assertTrue(third['pageLimitReached'])
        requests = host.stats['discover']
        limited = await host.call(SEARCH_NAME, {'query': 'item', 'more': True})
        self.assertEqual(limited['error']['code'], 'SEARCH_PAGE_LIMIT')
        self.assertEqual(host.stats['discover'], requests)
        self.assertEqual(host.stats['invoke'], 0)
        self.assertLessEqual(tool_bytes(host.tools()), 16000)
        for value in (1, 'yes', None):
            result = await host.call(SEARCH_NAME, {'query': 'item', 'more': value})
            self.assertEqual(result['error']['code'], 'INVALID_INPUT')

    async def test_end_limit_change_and_catalog_drift_clear_cursors(self):
        client = Client(sample(4))
        host = await ToolSession.from_mcp(client)
        await host.select('item')
        end = await host.select('item', more=True)
        self.assertFalse(end['moreAvailable'])
        self.assertEqual((await host.call(SEARCH_NAME, {'query': 'item', 'more': True}))['error']['code'], 'SEARCH_EXHAUSTED')
        client.runtime = DirectApplications(sample(5))
        drift = await host.call(SEARCH_NAME, {'query': 'item', 'more': True})
        # No cursor is used after an exhausted page; explicitly repeat that page.
        self.assertEqual(drift['error']['code'], 'SEARCH_EXHAUSTED')
        drift = await host.call(SEARCH_NAME, {'query': 'item'})
        self.assertEqual(drift['error']['code'], 'CONTRACT_DRIFT')
        self.assertEqual(len(host.tools()), 1)
        self.assertEqual((await host.call(SEARCH_NAME, {'query': 'item', 'more': True}))['error']['code'], 'SEARCH_NOT_STARTED')
        await host.select('item')
        host.search_limit = 1
        self.assertEqual((await host.call(SEARCH_NAME, {'query': 'item', 'more': True}))['error']['code'], 'SEARCH_NOT_STARTED')

    async def test_prime_does_not_choose_last_version_after_paging(self):
        def get() -> str:return 'ok'
        class Versions(Application):
            def descriptors(self):
                base = super().descriptors()[0]
                return tuple({**deepcopy(base), 'version': version} for version in ('1.0', '2.0'))
        host = ToolSession(Versions([capability(id='api.get', effect='read')(get)]), CONTEXT, search_limit=1)
        await host.select('api.get')
        await host.select('api.get', more=True)
        with self.assertRaises(A2APIError) as caught:await host.prime(['api.get'])
        self.assertEqual(caught.exception.code, 'AMBIGUOUS_SELECTION')

    @unittest.skipUnless(importlib.util.find_spec('mcp'), 'Install a2api[mcp]')
    async def test_real_mcp_next_page_keeps_fixed_tool_list(self):
        from mcp import Client as MCPClient
        from a2api.mcp_bridge import create_mcp_server
        async with MCPClient(create_mcp_server(sample(), CONTEXT), read_timeout_seconds=10) as client:
            before = (await client.list_tools()).model_dump(mode='json')
            host = await ToolSession.from_mcp(client)
            await host.select('item')
            page = await host.select('item', more=True)
            self.assertEqual(page['page'], 2)
            after = (await client.list_tools(cache_mode='refresh')).model_dump(mode='json')
            self.assertEqual(before, after)
            self.assertEqual(len(after['tools']), 3)
