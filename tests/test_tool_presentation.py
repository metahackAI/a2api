"""a2api-tools/0.4 host presentation: names, flat inputs, compact results, auto strategy."""

import json
import unittest
from contextlib import ExitStack

from a2api import Application, ExecutionContext, HTTPDeployment, ToolSession, capability, convert
from a2api.importers import OpenAPIImporter
from a2api.sample import BACKEND_TOKEN, TOKENS, create_backend, running
from a2api.tool_session import SEARCH_NAME, flatten_input, render_result
from test_conversion import SOURCE

CALLER = TOKENS['demo-alice']


def many(count):
    functions = []
    def make(index):
        def handler(value: str) -> str:
            return '%d:%s' % (index, value)
        handler.__doc__ = 'Inventory widget lookup number %d.' % index
        return handler
    for index in range(count):
        handler = make(index)
        functions.append(capability(id='stock.widget_%03d' % index, effect='read', keywords=['widget'])(handler))
    return Application(functions)


class FlattenTests(unittest.TestCase):
    def test_http_groups_flatten_and_conflicts_stay_nested(self):
        schema = {'type': 'object', 'additionalProperties': False, 'required': ['path', 'body'], 'properties': {
            'path': {'type': 'object', 'additionalProperties': False, 'required': ['id'], 'properties': {'id': {'type': 'string'}}},
            'query': {'type': 'object', 'additionalProperties': False, 'properties': {'limit': {'type': 'integer'}}},
            'body': {'$ref': '#/$defs/Patch'}}, '$defs': {'Patch': {'type': 'object', 'additionalProperties': False,
                'properties': {'name': {'type': 'string'}}}}}
        parameters, layout, groups = flatten_input(schema)
        self.assertEqual(set(parameters['properties']), {'id', 'limit', 'name'})
        self.assertEqual(parameters['required'], ['id'])
        self.assertEqual(groups, ('path', 'body'))
        clash = json.loads(json.dumps(schema))
        clash['properties']['query']['properties']['id'] = {'type': 'string'}
        self.assertIsNone(flatten_input(clash))
        optional = json.loads(json.dumps(schema))
        optional['properties']['query']['required'] = ['limit']
        self.assertIsNone(flatten_input(optional))
        array_body = json.loads(json.dumps(schema))
        array_body['properties']['body'] = {'type': 'array', 'items': {'type': 'string'}}
        parameters, layout, _ = flatten_input(array_body)
        self.assertEqual(parameters['properties']['body']['type'], 'array')
        self.assertIsNone(flatten_input({'type': 'object', 'properties': {'value': {'type': 'string'}}}))


class PresentationTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.stack = ExitStack()
        self.backend = create_backend()
        origin = self.stack.enter_context(running(self.backend))
        self.app = convert(OpenAPIImporter(json.loads(SOURCE.read_text()), namespace='legacy'), operations={
            'getOrder': {'effect': 'read', 'select': ['orderId', 'orderState', 'shipmentIds']},
            'getShipment': {'effect': 'read'}}, deployment=HTTPDeployment(origin,
                credential_provider=lambda _: {'Authorization': 'Bearer ' + BACKEND_TOKEN}))

    async def asyncTearDown(self):
        self.stack.close()

    async def test_readable_names_flat_arguments_and_compact_results(self):
        session = ToolSession(self.app, CALLER)
        result = await session.auto('ORD-1001 order status')
        self.assertEqual(result, {'strategy': 'all', 'functions': 2})
        tools = session.tools()
        self.assertEqual([tool['function']['name'] for tool in tools], ['legacy_getorder', 'legacy_getshipment'])
        self.assertNotIn(SEARCH_NAME, json.dumps(tools))
        self.assertEqual(tools[0]['function']['parameters']['required'], ['orderId'])
        order = await session.call('legacy_getorder', {'orderId': 'ORD-1001'})
        self.assertEqual(order['data']['orderId'], 'ORD-1001')
        nested = await session.call('legacy_getorder', {'path': {'orderId': 'ORD-1001'}})
        self.assertEqual(nested['data'], order['data'])
        text = render_result(order)
        self.assertNotIn(' ', text.replace('ORD-1001', ''))
        self.assertNotIn('completeness', text)
        self.assertEqual(json.loads(text)['data'], order['data'])
        bad = await session.call('legacy_getorder', {'order': 'ORD-1001'})
        rendered = json.loads(session.render(bad))
        self.assertEqual(rendered['error']['code'], 'INVALID_INPUT')
        self.assertIn('hint', rendered)
        self.assertTrue(any(issue.get('missing') == ['orderId'] for issue in rendered['error']['issues']))
        missing = json.loads(render_result(await session.call('legacy_getorder', {'orderId': 'ORD-404'})))
        self.assertEqual(missing['error']['code'], 'RESOURCE_NOT_FOUND')
        self.assertIn('earlier results', missing['hint'])

    async def test_textual_http_parameters_accept_json_scalars(self):
        @capability(id='orders.page', effect='read', input_schema={'type': 'object', 'additionalProperties': False,
            'properties': {'query': {'type': 'object', 'additionalProperties': False, 'properties': {
                'page': {'type': 'string'}, 'active': {'type': 'string'}}}, 'body': {'type': 'object',
                'additionalProperties': False, 'properties': {'limit': {'type': 'string'}}}}}, output_schema={})
        def page(query: dict = {}, body: dict = {}) -> dict:
            return {'query': query, 'body': body}
        session = ToolSession(Application([page]), CALLER)
        await session.auto()
        self.assertEqual((await session.call('orders_page', {'page': 2, 'active': True}))['data']['query'],
                         {'page': '2', 'active': 'true'})
        # Body members are JSON values, not text: no conversion there.
        self.assertEqual((await session.call('orders_page', {'limit': 3}))['error']['code'], 'INVALID_INPUT')

    async def test_hint_styles_describe_effects_without_extra_shape(self):
        @capability(id='notes.add', effect='write')
        def add(text: str) -> dict[str, str]:
            """Add a note."""
            return {'id': 'N-1'}
        plain = ToolSession(Application([add]), CALLER, hints='none')
        await plain.auto()
        self.assertEqual(plain.tools()[0]['function']['description'], 'Add a note. [write]')
        read = ToolSession(self.app, CALLER, hints='none')
        await read.auto()
        self.assertNotIn('Returns', json.dumps(read.tools()))
        self.assertNotIn('[read]', json.dumps(read.tools()))
        with self.assertRaises(ValueError):
            ToolSession(self.app, CALLER, hints='verbose')

    async def test_hash_naming_and_wire_shape_remain_available(self):
        session = ToolSession(self.app, CALLER, naming='hash', flatten=False)
        await session.prime(['legacy.getorder'])
        tool = session.tools(include_search=False)[0]['function']
        self.assertTrue(tool['name'].startswith('a2api_call_'))
        self.assertIn('path', tool['parameters']['properties'])
        self.assertEqual((await session.call(tool['name'], {'path': {'orderId': 'ORD-1001'}}))['status'], 'succeeded')

    async def test_auto_falls_back_to_presearch_for_large_catalogs(self):
        session = ToolSession(many(80), CALLER)
        result = await session.auto('widget lookup number 7')
        self.assertEqual(result['strategy'], 'search')
        self.assertEqual(len(result['preselected']['selected']), 8)
        tools = session.tools()
        self.assertEqual(tools[0]['function']['name'], SEARCH_NAME)
        self.assertEqual(len(tools), 9)
        # The model's own searches keep the smaller search_limit page size.
        self.assertEqual(len((await session.select('widget'))['selected']), 5)
        narrow = ToolSession(many(80), CALLER)
        self.assertEqual(len((await narrow.auto('widget lookup', preselect=2))['preselected']['selected']), 2)
        small = ToolSession(many(4), CALLER, max_tool_bytes=900)
        self.assertEqual((await small.auto('widget'))['strategy'], 'search')
        self.assertEqual(small.tools()[0]['function']['name'], SEARCH_NAME)

    async def test_name_collisions_get_hash_suffixes(self):
        @capability(id='a.b_c', effect='read')
        def first() -> str:
            """First."""
            return '1'

        @capability(id='a_b.c', effect='read')
        def second() -> str:
            """Second."""
            return '2'
        session = ToolSession(Application([first, second]), CALLER)
        await session.auto()
        names = [tool['function']['name'] for tool in session.tools()]
        self.assertEqual(names[0], 'a_b_c')
        self.assertTrue(names[1].startswith('a_b_c_') and len(names[1]) == 14)
        self.assertEqual([(await session.call(name, {}))['data'] for name in names], ['1', '2'])


if __name__ == '__main__':
    unittest.main()
