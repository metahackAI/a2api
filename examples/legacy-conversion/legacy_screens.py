"""A running legacy back end with abbreviated names, code values and RPC-style screen endpoints (docs/36, path C).

python examples/legacy-conversion/legacy_screens.py

The service publishes a tool catalog (GET /v1/tools: name, summary, closed input schema) and takes
calls by name (POST /v1/tools/{name} with {"input": {...}}), like many registry-style or
screen-shaped back ends. Its fields are `clmStatCd: "R10"`, `rfndMthdCd: "01"`; what the codes mean
lives in a code table in the service's source. The conversion:

1. imports the catalog (no OpenAPI, nothing executed),
2. shows readable names and words instead of abbreviations and codes, mapped back on the wire,
3. adds host-owned request values (here a change set id on writes) that are never model input,
4. passes the back end's error sentence on, through a host function that picks the safe part.
"""

from __future__ import annotations

import asyncio
import http.server
import json
import threading

from a2api import ExecutionContext, HTTPDeployment, ToolSession, convert
from a2api.importers import ToolCatalogImporter

CATALOG = {'items': [
    {'tool': 'getClmGridList', 'kind': 'read', 'summary': 'Claim grid list.', 'input_schema': {
        'type': 'object', 'additionalProperties': False, 'properties': {
            'clmStatCd': {'type': 'string', 'enum': ['R10', 'R20', 'R90'], 'description': 'Claim status code.'},
            'pageNo': {'type': 'integer', 'minimum': 0, 'description': 'Page no.'}}}},
    {'tool': 'saveRfndProc', 'kind': 'write', 'summary': 'Refund process save.', 'input_schema': {
        'type': 'object', 'additionalProperties': False, 'required': ['clmNo'], 'properties': {
            'clmNo': {'type': 'string', 'description': 'Claim no.'},
            'rfndMthdCd': {'type': 'string', 'enum': ['01', '03'], 'description': 'Refund method code.'}}}},
]}
CLAIMS = [{'clmNo': 'clm_1', 'clmStatCd': 'R10', 'clmAmt': 120}, {'clmNo': 'clm_2', 'clmStatCd': 'R90', 'clmAmt': 80}]


class LegacyService(http.server.BaseHTTPRequestHandler):
    """Stands in for the legacy back end: it only knows codes and abbreviations."""

    def log_message(self, *args):
        pass

    def reply(self, status, body):
        raw = json.dumps(body).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        self.reply(200, CATALOG)

    def do_POST(self):
        request = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        given = request['input']
        if self.path.startswith('/v1/tools/getClmGridList'):
            page = given.get('pageNo', 1)
            if page < 1:
                return self.reply(422, {'error': {'code': 'ERR_PARAM', 'message': 'Invalid paging.', 'trace': 'x'}})
            rows = [c for c in CLAIMS if 'clmStatCd' not in given or c['clmStatCd'] == given['clmStatCd']]
            return self.reply(200, {'list': rows, 'pageNo': page})
        if self.path.startswith('/v1/tools/saveRfndProc'):
            return self.reply(200, {'resultCd': '0000', 'rfndNo': 'rfnd_9', 'changeSet': request.get('change_set_id')})
        self.reply(404, {'error': {'message': 'No such screen.'}})


# From the service's code table and field comments: what a converter can read in the source.
VOCABULARY = {
    'rename': {'clmStatCd': 'claim_status', 'clmNo': 'claim_id', 'clmAmt': 'claim_amount', 'pageNo': 'page',
               'rfndMthdCd': 'refund_method', 'rfndNo': 'refund_id', 'resultCd': 'result_code', 'list': 'claims'},
    'codes': {'clmStatCd': {'R10': 'requested', 'R20': 'approved', 'R90': 'completed'},
              'rfndMthdCd': {'01': 'original_payment', '03': 'store_credit'}},
    'describe': {'pageNo': 'Page number, from 1.'},
}


def main():
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), LegacyService)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    origin = 'http://127.0.0.1:%d' % server.server_address[1]

    # 1. The running service's catalog, bound to its call-by-name endpoint.
    source = ToolCatalogImporter.from_url(origin + '/v1/tools', namespace='claims')
    kinds = {record.operation_id: record.entry['kind'] for record in source.iter_operations()}
    print('imported:', {record.id: record.status for record in source.iter_operations()})

    # 2-4. Readable vocabulary, host values on writes, the back end's error sentence.
    app = convert(source, operations={name: {'effect': 'read' if kind == 'read' else 'write'} for name, kind in kinds.items()},
                  vocabulary=VOCABULARY, deployment=HTTPDeployment(
                      origin,
                      request_values=lambda context, call: ({'body': {'change_set_id': 'cs_' + context.actor}}
                                                            if call['effect'] == 'write' else {}),
                      error_detail=lambda status, body: (body or {}).get('error', {}).get('message'),
                      idempotency_header='Idempotency-Key'))
    print('model sees:', json.dumps(app.describe('claims.get_clm_grid_list')['inputSchema']['properties']['body'], ensure_ascii=False))

    caller = ExecutionContext('alice', 'shop', frozenset())

    async def model_view():
        session = ToolSession(app, caller)
        await session.auto('refund the requested claims')
        listing = await session.call('claims_get_clm_grid_list', {'claim_status': 'requested', 'page': 1})
        refund = await session.call('claims_save_rfnd_proc', {'claim_id': 'clm_1', 'refund_method': 'original_payment'},
                                    request_id='call_1')
        bad_page = await session.call('claims_get_clm_grid_list', {'page': 0})
        return [session.render(listing), session.render(refund), session.render(bad_page)]
    for text in asyncio.run(model_view()):
        print('result:', text)
    server.shutdown()


if __name__ == '__main__':
    main()
