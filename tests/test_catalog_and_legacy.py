"""Tool catalogs (call by name), host request values, legacy vocabulary and host error details."""

import asyncio
import http.server
import json
import threading
import unittest

from a2api import ExecutionContext, HTTPDeployment, ToolSession, convert
from a2api.errors import A2APIError
from a2api.importers import ToolCatalogImporter

CALLER = ExecutionContext('alice', 'tenant-a', frozenset())
CATALOG = {'items': [
    {'tool': 'search_claims', 'kind': 'read', 'summary': 'Claim grid list.', 'input_schema': {
        'type': 'object', 'additionalProperties': False, 'properties': {
            'clmStatCd': {'type': 'string', 'enum': ['R10', 'R90'], 'description': 'Claim status code.'},
            'pageSize': {'type': 'integer', 'format': 'uint32', 'minimum': 1}}}},
    {'tool': 'refund', 'kind': 'write', 'summary': 'Refund process save.', 'input_schema': {
        'type': 'object', 'additionalProperties': False, 'required': ['clmNo'], 'properties': {
            'clmNo': {'type': 'string'}, 'rfndMthdCd': {'type': 'string', 'enum': ['01', '03']}}}},
    {'tool': 'bad', 'summary': 'not an object', 'input_schema': {'type': 'string'}},
]}
VOCABULARY = {'rename': {'clmStatCd': 'claim_status', 'clmNo': 'claim_id', 'rfndMthdCd': 'refund_method'},
              'codes': {'clmStatCd': {'R10': 'requested', 'R90': 'completed'}, 'rfndMthdCd': {'01': 'original_payment', '03': 'store_credit'}},
              'describe': {'pageSize': 'Rows per page (at most 100).'}}


class Handler(http.server.BaseHTTPRequestHandler):
    seen = []
    keys = []

    def log_message(self, *args):
        pass

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers['Content-Length'] or 0)) or b'{}')
        Handler.seen.append((self.path, body))
        Handler.keys.append(self.headers.get('Idempotency-Key'))
        if self.path.startswith('/v1/tools/refund') and body['input'].get('clmNo') == 'missing':
            status, out = 404, {'error': {'code': 'claim_not_found', 'message': 'There is no claim missing.', 'secret': 'x'}}
        elif self.path.startswith('/v1/tools/search_claims'):
            status, out = 200, {'list': [{'clmNo': 'clm_1', 'clmStatCd': 'R10'}, {'clmNo': 'clm_2', 'clmStatCd': 'R77'}]}
        else:
            status, out = 200, {'preview_id': 'prv_1', 'input': body['input']}
        raw = json.dumps(out).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        Handler.seen, Handler.keys = [], []
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.origin = 'http://127.0.0.1:%d' % self.server.server_address[1]

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()

    def app(self, **options):
        source = ToolCatalogImporter(CATALOG, namespace='legacy')
        deployment = HTTPDeployment(self.origin, request_values=options.pop('request_values', None),
                                    error_detail=options.pop('error_detail', None),
                                    idempotency_header=options.pop('idempotency_header', None))
        return convert(source, operations={'search_claims': {'effect': 'read'}, 'refund': {'effect': 'write'}},
                       deployment=deployment, **options), source

    def test_catalog_records_unsupported_entries_and_binds_call_by_name(self):
        app, source = self.app()
        records = {r.operation_id: r for r in source.iter_operations()}
        self.assertEqual(records['bad'].status, 'unsupported')
        self.assertEqual(records['refund'].entry['kind'], 'write')
        descriptor = app.describe('legacy.refund')
        self.assertEqual(descriptor['inputSchema']['required'], ['body'])
        result = app.invoke('legacy.refund', {'body': {'clmNo': 'clm_1'}}, context=CALLER)
        self.assertEqual(result['data']['preview_id'], 'prv_1')
        self.assertEqual(Handler.seen[-1], ('/v1/tools/refund', {'input': {'clmNo': 'clm_1'}}))
        # Optional-only inputs still send the envelope.
        app.invoke('legacy.search_claims', {}, context=CALLER)
        self.assertEqual(Handler.seen[-1][1], {'input': {}})
        with self.assertRaises(A2APIError):
            convert(source, operations={'bad': {'effect': 'read'}}, deployment=HTTPDeployment(self.origin))
        camel = ToolCatalogImporter([{'tool': 'getClmGridList', 'input_schema': {'type': 'object'}},
                                     {'tool': 'get_clm_grid_list', 'input_schema': {'type': 'object'}}], namespace='legacy')
        first, second = camel.iter_operations()
        self.assertEqual((first.id, first.status, second.status), ('legacy.get_clm_grid_list', 'imported', 'unsupported'))

    def test_host_request_values_are_added_per_call_and_cannot_replace_business_fields(self):
        app, _ = self.app(request_values=lambda context, call: (
            {'query': {'set': 'facade'}, 'body': {'change_set_id': 'cs_' + context.actor}} if call['effect'] == 'write'
            else {'query': {'set': 'facade'}}))
        app.invoke('legacy.refund', {'body': {'clmNo': 'clm_1'}}, context=CALLER)
        self.assertEqual(Handler.seen[-1], ('/v1/tools/refund?set=facade', {'input': {'clmNo': 'clm_1'}, 'change_set_id': 'cs_alice'}))
        app.invoke('legacy.search_claims', {'body': {'pageSize': 2}}, context=CALLER)
        self.assertEqual(Handler.seen[-1], ('/v1/tools/search_claims?set=facade', {'input': {'pageSize': 2}}))
        clash, _ = self.app(request_values=lambda context, call: {'body': {'input': 'x'}})
        self.assertEqual(clash.invoke('legacy.refund', {'body': {'clmNo': 'c'}}, context=CALLER)['error']['code'], 'HOST_VALUE_CONFLICT')
        broken, _ = self.app(request_values=lambda context, call: 1 / 0)
        self.assertEqual(broken.invoke('legacy.refund', {'body': {'clmNo': 'c'}}, context=CALLER)['error']['code'], 'HOST_VALUES_UNAVAILABLE')

    def test_vocabulary_shows_readable_names_and_words_and_maps_them_back(self):
        app, _ = self.app(vocabulary=VOCABULARY)
        schema = app.describe('legacy.refund')['inputSchema']['properties']['body']
        self.assertEqual(schema['required'], ['claim_id'])
        self.assertEqual(schema['properties']['refund_method']['enum'], ['original_payment', 'store_credit'])
        listing_schema = app.describe('legacy.search_claims')['inputSchema']['properties']['body']['properties']
        self.assertEqual(listing_schema['pageSize']['description'], 'Rows per page (at most 100).')
        result = app.invoke('legacy.refund', {'body': {'claim_id': 'clm_1', 'refund_method': 'store_credit'}}, context=CALLER)
        self.assertEqual(Handler.seen[-1][1], {'input': {'clmNo': 'clm_1', 'rfndMthdCd': '03'}})
        self.assertEqual(result['data']['input'], {'claim_id': 'clm_1', 'refund_method': 'store_credit'})
        listing = app.invoke('legacy.search_claims', {'body': {'claim_status': 'requested'}}, context=CALLER)
        self.assertEqual(Handler.seen[-1][1], {'input': {'clmStatCd': 'R10'}})
        self.assertEqual(listing['data']['list'], [{'claim_id': 'clm_1', 'claim_status': 'requested'},
                                                    {'claim_id': 'clm_2', 'claim_status': 'R77'}])
        legacy_name = app.invoke('legacy.refund', {'body': {'clmNo': 'clm_1'}}, context=CALLER)
        self.assertEqual(legacy_name['error']['code'], 'INVALID_INPUT')
        with self.assertRaises(A2APIError):
            convert(ToolCatalogImporter(CATALOG), operations={'refund': {'effect': 'write'}},
                    deployment=HTTPDeployment(self.origin), vocabulary={'rename': {'a': 'x', 'b': 'x'}})

    def test_model_view_is_flat_and_readable(self):
        app, _ = self.app(vocabulary=VOCABULARY)

        async def run():
            session = ToolSession(app, CALLER)
            await session.auto('refund')
            tools = {tool['function']['name']: tool['function'] for tool in session.tools()}
            result = await session.call('legacy_refund', {'claim_id': 'clm_1', 'refund_method': 'original_payment'})
            return tools, result
        tools, result = asyncio.run(run())
        self.assertEqual(set(tools['legacy_refund']['parameters']['properties']), {'claim_id', 'refund_method'})
        self.assertEqual(tools['legacy_refund']['description'], 'Refund process save. [write]')
        self.assertEqual(result['status'], 'succeeded')
        self.assertEqual(Handler.seen[-1][1], {'input': {'clmNo': 'clm_1', 'rfndMthdCd': '01'}})

    def test_request_id_reaches_the_backend_on_writes_only_when_the_host_opts_in(self):
        plain, _ = self.app()
        plain.invoke('legacy.refund', {'body': {'clmNo': 'clm_1'}}, context=CALLER, request_id='call_0')
        keyed, _ = self.app(idempotency_header='Idempotency-Key')
        keyed.invoke('legacy.refund', {'body': {'clmNo': 'clm_1'}}, context=CALLER, request_id='call_1')
        keyed.invoke('legacy.search_claims', {}, context=CALLER, request_id='call_2')
        keyed.invoke('legacy.refund', {'body': {'clmNo': 'clm_1'}}, context=CALLER)

        async def run():
            session = ToolSession(keyed, CALLER)
            await session.auto('refund')
            return await session.call('legacy_refund', {'clmNo': 'clm_1'}, request_id='call_3')
        self.assertEqual(asyncio.run(run())['status'], 'succeeded')
        self.assertEqual(Handler.keys, [None, 'call_1', None, None, 'call_3'])
        self.assertEqual(keyed.invoke('legacy.refund', {'body': {'clmNo': 'c'}}, context=CALLER, request_id='')['error']['code'],
                         'INVALID_REQUEST')
        with self.assertRaises(A2APIError):
            HTTPDeployment(self.origin, idempotency_header='Bad Header')

    def test_search_says_when_nothing_new_matched(self):
        app, _ = self.app()

        async def run():
            session = ToolSession(app, CALLER)
            first = await session.call('a2api_search', {'query': 'refund'})
            again = await session.call('a2api_search', {'query': 'refund process'})
            return first, again, session.render(first), session.render(again)
        first, again, first_text, again_text = asyncio.run(run())
        self.assertIn('legacy_refund', first['added'])
        self.assertEqual(again['added'], [])
        self.assertNotIn('note', first_text)
        self.assertIn('No new functions', again_text)

    def test_numbers_for_string_ids_and_repeated_failures(self):
        app, _ = self.app()

        async def run():
            session = ToolSession(app, CALLER)
            await session.auto('refund')
            coerced = await session.call('legacy_refund', {'clmNo': 20431})
            first = await session.call('legacy_search_claims', {'pageSize': 0})
            again = await session.call('legacy_search_claims', {'pageSize': 0})
            return coerced, first, again, session.render(again)
        coerced, first, again, text = asyncio.run(run())
        self.assertEqual(coerced['status'], 'succeeded')
        self.assertEqual(Handler.seen[-1][1], {'input': {'clmNo': '20431'}})
        self.assertNotIn('repeated', first)
        self.assertEqual(again['repeated'], 1)
        self.assertIn('already failed 1 time', text)

        async def reads():
            session = ToolSession(app, CALLER)
            await session.auto('claims')
            one = await session.call('legacy_search_claims', {'pageSize': 2})
            two = await session.call('legacy_search_claims', {'pageSize': 2})
            await session.call('legacy_refund', {'clmNo': 'clm_1'})
            three = await session.call('legacy_search_claims', {'pageSize': 2})
            return one, two, three, session.render(two)
        one, two, three, note = asyncio.run(reads())
        self.assertEqual((one.get('repeated'), two.get('repeated'), three.get('repeated')), (None, 1, None))
        self.assertIn('already have this data', note)

    def test_backend_error_messages_only_through_host_extraction(self):
        hidden, _ = self.app()
        error = hidden.invoke('legacy.refund', {'body': {'clmNo': 'missing'}}, context=CALLER)['error']
        self.assertEqual(error['code'], 'RESOURCE_NOT_FOUND')
        self.assertNotIn('There is no claim', error['detail'])
        shown, _ = self.app(error_detail=lambda status, body: (body or {}).get('error', {}).get('message'))
        error = shown.invoke('legacy.refund', {'body': {'clmNo': 'missing'}}, context=CALLER)['error']
        self.assertIn('There is no claim missing.', error['detail'])
        self.assertNotIn('secret', error['detail'])
        failing, _ = self.app(error_detail=lambda status, body: 1 / 0)
        self.assertEqual(failing.invoke('legacy.refund', {'body': {'clmNo': 'missing'}}, context=CALLER)['error']['code'],
                         'RESOURCE_NOT_FOUND')


if __name__ == '__main__':
    unittest.main()
