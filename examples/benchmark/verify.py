"""Verify the generated benchmark implementations before any model run.

1. The same HTTP request sequence gives identical statuses, 2xx bodies and final state
   in the Python, Spring, Go and Rust servers (per scale).
2. Every exposed operation converts; a2api direct invoke and MCP stdio work per language.

python examples/benchmark/verify.py [--scales small,medium,large]
"""

from __future__ import annotations

import argparse
import asyncio
from contextlib import ExitStack
import json
import os
from pathlib import Path
import sys
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from a2api import ExecutionContext  # noqa: E402
from application import application  # noqa: E402
from servers import BUILD, LANGUAGES, admin, build, process, python_server  # noqa: E402

CALLER = ExecutionContext('bench-user', 'tenant-a', frozenset())
CORE_PROBES = [
    ('GET', '/customers?tier=gold&limit=3', None), ('GET', '/customers?tier=bogus', None), ('GET', '/customers?page=0', None),
    ('GET', '/customers?limit=50', None), ('GET', '/customers/C-007', None), ('GET', '/customers/C-999', None),
    ('POST', '/customers/search', {'query': 'MINJI'}), ('POST', '/customers/search', {'query': 'x', 'limit': 0}),
    ('POST', '/customers', {'name': '테스트', 'email': 't@example.com', 'city': '부산'}),
    ('POST', '/customers', {'name': '', 'email': 'e@example.com', 'city': '부산'}),
    ('POST', '/customers', {'name': '등급', 'email': 'g@example.com', 'city': '울산', 'tier': 'gold'}),
    ('PATCH', '/customers/C-006', {'tier': 'gold'}), ('PATCH', '/customers/C-006', {'tier': 'platinum'}),
    ('PATCH', '/customers/C-999', {'city': '서울'}),
    ('GET', '/orders?customerId=C-002&limit=5&page=2', None), ('GET', '/orders?status=pending', None),
    ('POST', '/orders/ORD-1007/cancel', None), ('POST', '/orders/ORD-1010/cancel', None), ('POST', '/orders/ORD-9999/cancel', None),
    ('POST', '/orders', {'customerId': 'C-001', 'totalAmount': 1000, 'itemCount': 1}),
    ('POST', '/orders', {'customerId': 'C-001', 'totalAmount': -5, 'itemCount': 1}),
    ('PATCH', '/orders/ORD-1003', {'itemCount': 4}),
    ('GET', '/shipments?status=in_transit', None), ('GET', '/shipments?orderId=ORD-1008', None),
    ('GET', '/shipments/SHP-508', None), ('GET', '/shipments/SHP-503/tracking', None), ('GET', '/shipments/SHP-999/tracking', None),
    ('GET', '/tickets?status=open&priority=high&limit=2', None), ('GET', '/tickets?customerId=C-006', None),
    ('POST', '/tickets', {'customerId': 'C-004', 'subject': '배송 지연 문의', 'priority': 'high'}),
    ('POST', '/tickets', {'customerId': 'C-004', 'subject': '잘못된 우선순위', 'priority': 'critical'}),
    ('PATCH', '/tickets/T-9003', {'assigneeId': 'A-04', 'priority': 'urgent'}),
    ('GET', '/agents?team=' + quote('지원2팀') + '&active=true', None), ('GET', '/agents?active=maybe', None),
    ('GET', '/agents/A-04', None),
]
DISTRACTOR_PROBES = [
    ('GET', '/purchase-orders?status=approved&limit=20', None), ('POST', '/returns/search', {'query': '반품 요청 1'}),
    ('DELETE', '/invoices/IV-0003', None), ('DELETE', '/invoices/IV-0003', None),
    ('POST', '/contacts', {'name': '새 연락처', 'ownerId': 'C-002', 'amount': 3000}),
    ('PATCH', '/maintenance-tickets/MT-0002', {'status': 'done', 'amount': 7000}),
    ('GET', '/freight-shipments?ownerId=C-004&category=priority', None),
]
LARGE_PROBES = [('GET', '/surveys?status=open', None), ('POST', '/stores/search', {'query': '매장'}),
                ('POST', '/leads', {'name': '리드', 'ownerId': 'C-001', 'amount': 1, 'category': 'internal'})]


def request(origin, method, path, body):
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode()
    headers = {'Content-Type': 'application/json'} if data is not None else {}
    try:
        with urlopen(Request(origin + path, data=data, method=method, headers=headers), timeout=15) as response:
            raw = response.read()
            return response.status, json.loads(raw) if raw else None
    except HTTPError as error:
        error.read()
        error.close()
        return error.code, None  # error bodies are framework-specific; compare status only


def probes(scale):
    return CORE_PROBES + (DISTRACTOR_PROBES if scale != 'small' else []) + (LARGE_PROBES if scale == 'large' else [])


def http_equivalence(scale, origins):
    transcripts = {}
    for language, origin in origins.items():
        admin(origin, 'reset')
        transcripts[language] = [request(origin, *probe) for probe in probes(scale)] + [(200, admin(origin, 'state'))]
        admin(origin, 'reset')
    reference = transcripts['python']
    mismatches = []
    for language, transcript in transcripts.items():
        for index, (expected, actual) in enumerate(zip(reference, transcript)):
            if expected != actual:
                label = probes(scale)[index][:2] if index < len(probes(scale)) else ('STATE', '')
                mismatches.append({'language': language, 'request': label, 'python': expected[0], 'actual': actual[0]})
    return {'requests': len(reference), 'mismatches': mismatches[:20], 'mismatchCount': len(mismatches),
            'statuses': sorted({status for status, _ in reference})}


def direct_checks(scale, language, origin):
    app = application(scale, language, origin)
    ids = {d['id'] for d in app.descriptors()}
    def find(suffixes):
        return next(i for i in ids if any(i.endswith(s) for s in suffixes))
    get_order = find(['.orders.get', 'ordercontroller.get', '.getorder', '.get_order'])
    cancel = find(['.orders.cancel', 'ordercontroller.cancel', '.cancelorder', '.cancel_order'])
    tracking = find(['.shipments.tracking', 'shipmentcontroller.tracking', '.getshipmenttracking', '.get_shipment_tracking'])
    flat = language == 'python'
    def args(identifier):
        return {'id': identifier} if flat else {'path': {'id': identifier}}
    order = app.invoke(get_order, args('ORD-1003'), context=CALLER)
    assert order['status'] == 'succeeded' and order['data']['status'] == 'paid', order
    assert 'internalNote' not in json.dumps(order) and 'tenantId' not in json.dumps(order)
    conflict = app.invoke(cancel, args('ORD-1007'), context=CALLER)
    unavailable = app.invoke(tracking, args('SHP-503'), context=CALLER)
    return {'capabilities': len(ids), 'getOrder': order['data']['status'],
            'cancelConflict': conflict['error']['code'], 'tracking': unavailable['error']['code']}


async def mcp_smoke(scale, language, origin):
    from mcp import Client
    from mcp.client.stdio import StdioServerParameters
    params = StdioServerParameters(command=sys.executable, args=[str(HERE / 'mcp_server.py'), '--scale', scale,
                                   '--language', language, '--origin', origin or ''],
                                   env={**os.environ, 'PYTHONPATH': str(HERE.parents[1] / 'src')})
    async with Client(params, read_timeout_seconds=60) as client:
        listing = await client.list_tools()
        found = (await client.call_tool('a2api.discover', {'query': '주문 취소', 'limit': 3})).structured_content
        target = found['capabilities'][0]
        described = (await client.call_tool('a2api.describe', {'id': target['id'], 'version': target['version']})).structured_content
        return {'tools': [tool.name for tool in listing.tools], 'topDiscover': target['id'],
                'describedEffect': described['capability']['effects']['kind']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scales', default='small,medium,large')
    parser.add_argument('--skip-build', action='store_true')
    args = parser.parse_args()
    report = {}
    for scale in args.scales.split(','):
        with ExitStack() as stack:
            origins = {'python': stack.enter_context(python_server(scale))}
            for language in LANGUAGES[1:]:
                command, env = build(scale, language) if not args.skip_build else build(scale, language)
                origins[language] = stack.enter_context(process(language, command, env))
            result = {'http': http_equivalence(scale, origins), 'a2api': {}}
            for language in LANGUAGES:
                admin(origins[language], 'reset')
                result['a2api'][language] = direct_checks(scale, language, None if language == 'python' else origins[language])
                result['a2api'][language]['mcp'] = asyncio.run(mcp_smoke(scale, language, None if language == 'python' else origins[language]))
                admin(origins[language], 'reset')
            report[scale] = result
            print(json.dumps({scale: result}, ensure_ascii=False), flush=True)
    BUILD.mkdir(parents=True, exist_ok=True)
    (BUILD / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    failed = any(item['http']['mismatchCount'] for item in report.values())
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
