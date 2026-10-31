"""Legacy API with an OpenAPI document AND its source code (docs/36, path A).

python examples/legacy-conversion/openapi_and_code.py --language go

1. Read the OpenAPI document and list operations it cannot convert (with reasons).
2. Cross-check the documented routes against the routes found in the source code.
3. Convert the chosen operations from OpenAPI: effect, public fields, summary, keywords.
4. Call the running legacy server directly, then through a model-facing ToolSession.

Uses the benchmark's generated API (OpenAPI + Spring/Go/Rust sources); needs that language's toolchain.
"""

import argparse
import asyncio
from contextlib import ExitStack
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'benchmark'))

from a2api import ExecutionContext, HTTPDeployment, ToolSession, convert  # noqa: E402
from a2api.importers import GoSourceImporter, OpenAPIImporter, RustSourceImporter, SpringSourceImporter  # noqa: E402
from generate import generate  # noqa: E402
from servers import GENERATED, build, process  # noqa: E402

SOURCES = {'spring': (SpringSourceImporter, 'spring/src/main/java'), 'go': (GoSourceImporter, 'go'),
           'rust': (RustSourceImporter, 'rust/src')}


def report(source):
    """Step 1: what the document contains and what cannot be converted, with reasons."""
    records = list(source.iter_operations())
    unsupported = [record.summary() for record in records if record.status != 'imported']
    return {(record.method.upper(), record.path): record.operation_id for record in records if record.status == 'imported'}, unsupported


def cross_check(documented, language, scale):
    """Step 2: routes in the code but not in the document (or the reverse) mean the document is stale."""
    importer, folder = SOURCES[language]
    code = importer.from_directory(GENERATED / scale / folder, namespace='code')
    implemented = {(record.method.upper(), record.path) for record in code.iter_operations() if record.status == 'imported'}
    return {'onlyInCode': sorted(implemented - set(documented)), 'onlyInDocument': sorted(set(documented) - implemented)}


async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--language', choices=sorted(SOURCES), default='go')
    parser.add_argument('--scale', choices=['small', 'medium', 'large'], default='small')
    args = parser.parse_args()
    if not (GENERATED / args.scale / 'openapi.json').exists():
        generate(GENERATED.parent / 'generated')

    source = OpenAPIImporter.from_file(GENERATED / args.scale / 'openapi.json', namespace='shop',
                                       methods={'GET', 'POST', 'PATCH', 'DELETE'})
    documented, unsupported = report(source)
    print('1. documented operations:', len(documented), '| unsupported:', unsupported)
    print('2. document vs code:', cross_check(documented, args.language, args.scale))

    # 3. Expose only what the agent needs. GET is read; POST is read or write as the host decides.
    operations = {
        'listOrders': {'effect': 'read', 'select': ['items[].id', 'items[].status', 'items[].totalAmount',
                                                     'items[].createdAt', 'total', 'hasMore'],
                       'keywords': ['주문 목록', 'orders']},
        'getOrder': {'effect': 'read', 'select': ['id', 'customerId', 'status', 'totalAmount', 'shipmentIds']},
        'cancelOrder': {'effect': 'write', 'select': ['id', 'status'],
                        'summary': '주문을 취소한다. pending/paid 상태만 가능하며 그 외는 409.'},
    }
    with ExitStack() as stack:
        command, env = build(args.scale, args.language)
        origin = stack.enter_context(process(args.language, command, env))
        app = convert(source, operations=operations, deployment=HTTPDeployment(
            origin, credential_provider=lambda context: {'X-Caller': context.actor},  # per-user credential hook
            timeout_ms=5000, deadline_ms=8000))
        caller = ExecutionContext('alice', 'tenant-a', frozenset())
        print('3. descriptor:', json.dumps(app.describe('shop.getorder'), ensure_ascii=False)[:300], '...')

        # 4a. Direct call: the business input keeps OpenAPI locations (path/query/body).
        print('4a. getOrder:', app.invoke('shop.getorder', {'path': {'id': 'ORD-1003'}}, context=caller))
        print('    cancel shipped order:', app.invoke('shop.cancelorder', {'path': {'id': 'ORD-1007'}}, context=caller)['error'])

        # 4b. Model host: flat arguments, compact results; tools() goes into each model request.
        session = ToolSession(app, caller)
        print('4b. auto:', await session.auto('ORD-1003 주문 상태 알려줘'))
        print('    tools:', [tool['function']['name'] for tool in session.tools()])
        result = await session.call('shop_listorders', {'customerId': 'C-002', 'limit': 2})
        print('    model-facing result:', session.render(result))


if __name__ == '__main__':
    asyncio.run(main())
