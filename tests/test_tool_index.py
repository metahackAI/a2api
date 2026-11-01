"""ToolSession.index(): an index of every function, functions loaded on request, related next steps."""

import asyncio
import http.server
import json
import threading
import unittest

from a2api import ExecutionContext, HTTPDeployment, ToolSession, convert
from a2api.importers import ToolCatalogImporter
from a2api.tool_session import BATCH_NAME, INDEX_HEAD, LOAD_NAME, render_result, tool_bytes

CALLER = ExecutionContext('alice', 'tenant-a', frozenset())


def entry(tool, kind, summary, properties, required=(), consumes=(), produces=()):
    return {'tool': tool, 'kind': kind, 'summary': summary, 'consumes': [{'name': n} for n in consumes],
            'produces': [{'name': n} for n in produces],
            'input_schema': {'type': 'object', 'additionalProperties': False, 'required': list(required),
                             'properties': properties}}


ID = {'type': 'string'}
CATALOG = [
    entry('list_orders', 'read', 'List recent orders. Newest first.', {'customer_id': ID, 'status': ID, 'cursor': ID},
          produces=['order_id']),
    entry('get_order', 'read', 'Read one order with its deliveries.', {'order_id': ID}, ['order_id'],
          consumes=['order_id'], produces=['delivery_id', 'customer_id']),
    entry('track_shipment', 'read', 'Where a delivery is now.', {'delivery_id': ID}, ['delivery_id'], consumes=['delivery_id']),
    entry('cancel_order', 'write', 'Cancel an order that has not shipped.', {'order_id': ID}, ['order_id'], consumes=['order_id']),
    entry('get_customer', 'read', 'Read one member.', {'customer_id': ID}, ['customer_id'], consumes=['customer_id']),
]
RESULTS = {
    'list_orders': {'items': [{'id': 'ord_1', 'order_id': 'ord_1'}]},
    'get_order': {'id': 'ord_1', 'customer_id': 'cus_1', 'deliveries': [{'delivery_id': 'dlv_1', 'state': 'stuck'}]},
    'track_shipment': {'delivery_id': 'dlv_1', 'last_scan': 'Newark'},
    'cancel_order': {'preview': True},
    'get_customer': {'id': 'cus_1', 'name': 'Ann'},
}


class Handler(http.server.BaseHTTPRequestHandler):
    seen = []

    def log_message(self, *args):
        pass

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers['Content-Length'] or 0)) or b'{}')
        tool = self.path.split('?')[0].rsplit('/', 1)[1]
        Handler.seen.append((tool, body['input']))
        raw = json.dumps(RESULTS[tool]).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


class IndexTests(unittest.TestCase):
    def setUp(self):
        Handler.seen = []
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        origin = 'http://127.0.0.1:%d' % self.server.server_address[1]
        self.source = ToolCatalogImporter(CATALOG, namespace='shop')
        self.app = convert(self.source, deployment=HTTPDeployment(origin), operations={
            item['tool']: {'effect': item['kind']} for item in CATALOG})

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()

    def test_index_lists_every_function_without_binding_schemas(self):
        async def scenario():
            session = ToolSession(self.app, CALLER)
            built = await session.index('where is my order', group=lambda item: 'orders' if 'order' in item['id'] else 'other')
            self.assertEqual((built['strategy'], built['functions']), ('index', 5))
            text = built['text']
            self.assertTrue(text.startswith(INDEX_HEAD))
            self.assertIn('## orders\ncancel_order [write]: Cancel an order that has not shipped.', text)
            self.assertIn('list_orders: List recent orders.', text)  # first sentence only
            self.assertNotIn('Newest first', text)
            self.assertNotIn('shop_', text)  # the shared namespace is not repeated
            self.assertEqual(session.stats['describe'], 0)
            self.assertEqual([tool['function']['name'] for tool in session.tools()], [LOAD_NAME])
            names = await ToolSession(self.app, CALLER).index(detail='names')
            self.assertEqual(names['text'].splitlines()[1], 'cancel_order, get_customer, get_order, list_orders, track_shipment')
        asyncio.run(scenario())

    def test_load_then_call_and_unknown_names_get_suggestions(self):
        async def scenario():
            session = ToolSession(self.app, CALLER)
            await session.index()
            loaded = await session.call(LOAD_NAME, {'names': ['get_order', 'track_shipment', 'find_parcel']})
            self.assertEqual(loaded['loaded'], ['get_order', 'track_shipment'])
            self.assertEqual(loaded['unknown'], ['find_parcel'])
            self.assertIn('Unknown names', json.loads(render_result(loaded))['note'])
            self.assertEqual([tool['function']['name'] for tool in session.tools()], [LOAD_NAME, 'get_order', 'track_shipment'])
            again = await session.call(LOAD_NAME, {'names': ['get_order']})
            self.assertEqual(json.loads(render_result(again))['note'], 'These functions are already callable; call them.')
            result = await session.call('get_order', {'order_id': 'ord_1'})
            self.assertEqual(result['status'], 'succeeded')
            self.assertNotIn('related', result)  # related next steps are off by default
            missing = await session.call('find_parcel', {})
            self.assertEqual(missing['error']['code'], 'UNKNOWN_FUNCTION')
        asyncio.run(scenario())

    def test_calling_from_the_index_runs_valid_reads_and_holds_writes(self):
        async def scenario():
            session = ToolSession(self.app, CALLER)
            await session.index()
            read = await session.call('get_order', {'order_id': 'ord_1'})
            self.assertEqual(read['status'], 'succeeded')
            invalid = await session.call('track_shipment', {'parcel': 'x'})
            self.assertEqual(invalid['error']['code'], 'INVALID_INPUT')
            write = await session.call('cancel_order', {'order_id': 'ord_1'})
            self.assertEqual(write['error']['code'], 'NOT_LOADED')
            self.assertEqual([tool for tool, _ in Handler.seen], ['get_order'])  # the change was not sent
            self.assertEqual([tool['function']['name'] for tool in session.tools()],
                             [LOAD_NAME, 'get_order', 'track_shipment', 'cancel_order'])
            self.assertEqual((await session.call('cancel_order', {'order_id': 'ord_1'}))['status'], 'succeeded')
        asyncio.run(scenario())

    def test_related_names_functions_that_take_returned_ids(self):
        async def scenario():
            session = ToolSession(self.app, CALLER)
            await session.index('where is the delivery of my order', related=3, relations=self.source.relations())
            result = await session.call('get_order', {'order_id': 'ord_1'})
            self.assertEqual(result['related'], {'delivery_id': ['track_shipment'], 'customer_id': ['get_customer']})
            note = json.loads(render_result(result))['next']
            self.assertTrue(note.startswith('Functions that take IDs from this result: '))
            self.assertIn('track_shipment (delivery_id)', note)
            # Inputs named like IDs link functions when the host gives no relations.
            inferred = ToolSession(self.app, CALLER)
            await inferred.index('cancel my order', related=5)
            self.assertGreater(inferred.stats['describe'], 0)
            listed = await inferred.call('list_orders', {})
            self.assertEqual(set(listed['related']['order_id']), {'get_order', 'cancel_order'})
            self.assertEqual(listed['related']['order_id'][0], 'cancel_order')  # ranked by the request
        asyncio.run(scenario())

    def test_preselect_loads_search_matches_next_to_the_index(self):
        async def scenario():
            session = ToolSession(self.app, CALLER)
            built = await session.index('track the delivery shipment', detail='names', preselect=2)
            self.assertIn('Functions already in your tool list are loaded', built['text'].splitlines()[0])
            names = [tool['function']['name'] for tool in session.tools()]
            self.assertEqual(names[0], LOAD_NAME)
            self.assertIn('track_shipment', names)
            self.assertLessEqual(len(names), 3)
            self.assertEqual((await session.call('track_shipment', {'delivery_id': 'dlv_1'}))['status'], 'succeeded')
        asyncio.run(scenario())

    def test_functions_left_out_by_the_budget_are_named_with_what_to_do(self):
        async def scenario():
            probe = ToolSession(self.app, CALLER)
            await probe.index()
            await probe.call(LOAD_NAME, {'names': ['get_order', 'track_shipment']})
            session = ToolSession(self.app, CALLER, max_tool_bytes=tool_bytes(probe.tools()) + 10)
            await session.index()
            loaded = await session.call(LOAD_NAME, {'names': ['get_order', 'track_shipment', 'get_customer']})
            self.assertEqual(loaded['loaded'], ['get_order', 'track_shipment'])
            self.assertEqual(loaded['omitted'], [{'name': 'get_customer', 'reason': 'SCHEMA_BUDGET'}])
            self.assertIn('load them again when you need them', json.loads(render_result(loaded))['note'])
            session.tools()  # the next model request shows the loaded functions
            later = await session.call(LOAD_NAME, {'names': ['get_customer']})  # now an older function leaves
            self.assertEqual(later['loaded'], ['get_customer'])
            self.assertEqual(len(later['evicted']), 1)
        asyncio.run(scenario())

    def test_load_accepts_a_heading_joined_to_a_name(self):
        async def scenario():
            session = ToolSession(self.app, CALLER)
            await session.index(group=lambda entry: 'orders')
            loaded = await session.call(LOAD_NAME, {'names': ['orders.get_order', 'orders › track_shipment', 'GET_CUSTOMER',
                                                              'get_order']})
            self.assertEqual(loaded['loaded'], ['get_order', 'track_shipment', 'get_customer'])
            self.assertEqual(loaded['unknown'], [])
        asyncio.run(scenario())

    def test_batch_runs_independent_calls_in_one_step(self):
        async def scenario():
            session = ToolSession(self.app, CALLER, batch=True)
            await session.index()
            self.assertEqual([tool['function']['name'] for tool in session.tools()], [LOAD_NAME])  # nothing to batch yet
            await session.call(LOAD_NAME, {'names': ['get_order', 'track_shipment']})
            self.assertEqual([tool['function']['name'] for tool in session.tools()][:2], [LOAD_NAME, BATCH_NAME])
            result = await session.call(BATCH_NAME, {'calls': [
                {'name': 'get_order', 'arguments': {'order_id': 'ord_1'}},
                {'name': 'track_shipment', 'arguments': {'parcel': 'x'}},
                {'name': LOAD_NAME, 'arguments': {'names': ['get_customer']}},
                {'name': 'cancel_order', 'arguments': {'order_id': 'ord_1'}}]}, request_id='call_7')
            outcome = [(item['name'], item.get('status') or item['error']['code']) for item in result['batch']]
            self.assertEqual(outcome, [('get_order', 'succeeded'), ('track_shipment', 'INVALID_INPUT'),
                                       (LOAD_NAME, 'INVALID_INPUT'), ('cancel_order', 'NOT_LOADED')])
            self.assertEqual([tool for tool, _ in Handler.seen], ['get_order'])
            text = render_result(result, max_chars=800)
            view = json.loads(text)
            self.assertEqual([item['name'] for item in view['batch']], ['get_order', 'track_shipment', LOAD_NAME, 'cancel_order'])
            self.assertEqual(view['batch'][0]['result']['status'], 'succeeded')
            self.assertEqual((await session.call(BATCH_NAME, {'calls': []}))['error']['code'], 'INVALID_INPUT')
            plain = ToolSession(self.app, CALLER)
            await plain.index()
            self.assertEqual((await plain.call(BATCH_NAME, {'calls': []}))['error']['code'], 'UNKNOWN_FUNCTION')
        asyncio.run(scenario())

    def test_variant_note_after_the_same_read_with_other_conditions(self):
        async def scenario():
            session = ToolSession(self.app, CALLER, variant_note=3)
            await session.index()
            await session.call(LOAD_NAME, {'names': ['list_orders', 'get_order', 'cancel_order']})
            first = await session.call('list_orders', {'customer_id': 'cus_1'})
            second = await session.call('list_orders', {'customer_id': 'cus_1', 'cursor': 'o20'})  # paging: not another condition
            self.assertNotIn('variants', first)
            self.assertNotIn('variants', second)
            for order in ('ord_1', 'ord_2', 'ord_3'):  # one read per item: other targets
                self.assertNotIn('variants', await session.call('get_order', {'order_id': order}))
            await session.call('list_orders', {})
            third = await session.call('list_orders', {'customer_id': 'cus_1'})  # same as the first: a repeat
            self.assertEqual(third.get('repeated'), 1)
            self.assertNotIn('variants', await session.call('list_orders', {'customer_id': 'cus_2'}))
            self.assertNotIn('variants', await session.call('list_orders', {'customer_id': 'cus_3'}))
            # Without ID filters every call is about the same target: the third other condition gets the note.
            fresh = ToolSession(self.app, CALLER, variant_note=3)
            await fresh.index()
            await fresh.call(LOAD_NAME, {'names': ['list_orders', 'cancel_order']})
            results = [await fresh.call('list_orders', arguments) for arguments in ({}, {'status': 'a'}, {'status': 'b'})]
            self.assertEqual([item.get('variants') for item in results], [None, None, 3])
            self.assertIn('answer with what you found', json.loads(render_result(results[-1]))['note'])
            await fresh.call('cancel_order', {'order_id': 'ord_1'})  # a change: reading again is new
            self.assertNotIn('variants', await fresh.call('list_orders', {'status': 'c'}))
            await fresh.focus('another request')
            self.assertNotIn('variants', await fresh.call('list_orders', {'status': 'd'}))
            with self.assertRaises(ValueError):
                ToolSession(self.app, CALLER, variant_note=1)
        asyncio.run(scenario())

    def test_relations_read_from_catalog_entries(self):
        relations = self.source.relations()
        self.assertEqual(relations['shop.get_order'], {'consumes': ['order_id'], 'produces': ['delivery_id', 'customer_id']})
        self.assertEqual(relations['shop.list_orders']['consumes'], [])


if __name__ == '__main__':
    unittest.main()
