"""Legacy HTTP API with source code but NO OpenAPI (docs/36, path B).

python examples/legacy-conversion/code_only.py --language spring   # or go / rust

1. Read routes and DTOs from the source (no code is executed; no OpenAPI is generated).
2. Review what was found: method, path, handler location and unsupported constructs with reasons.
3. Decide exposure per route: effect (the host decides; POST search is read), public fields, wording.
4. Convert and call the running legacy server; the same app can be served over MCP.
"""

import argparse
from contextlib import ExitStack
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'benchmark'))

from a2api import ExecutionContext, HTTPDeployment, convert  # noqa: E402
from a2api.importers import GoSourceImporter, RustSourceImporter, SpringSourceImporter  # noqa: E402
from generate import generate  # noqa: E402
from servers import GENERATED, build, process  # noqa: E402

SOURCES = {'spring': (SpringSourceImporter, 'spring/src/main/java'), 'go': (GoSourceImporter, 'go'),
           'rust': (RustSourceImporter, 'rust/src')}
# Host decisions, written once per route: effect, public fields and wording. The importer never
# guesses business meaning; tenantId/internalNote/audit are simply not selected.
CUSTOMER = ['id', 'name', 'email', 'tier', 'status']
EXPOSE = {
    ('GET', '/customers'): {'effect': 'read', 'summary': '고객 목록(등급·상태·도시 필터, page/limit)을 조회한다.',
                            'select': ['items[].' + name for name in CUSTOMER] + ['total', 'hasMore']},
    ('POST', '/customers/search'): {'effect': 'read', 'summary': '이름·이메일 부분 문자열로 고객을 검색한다.',
                                    'select': ['items[].' + name for name in CUSTOMER] + ['total', 'hasMore']},
    ('GET', '/orders'): {'effect': 'read', 'summary': '주문 목록(고객 ID·상태 필터, page/limit)을 조회한다.',
                         'select': ['items[].id', 'items[].status', 'items[].totalAmount', 'total', 'hasMore']},
    ('POST', '/tickets'): {'effect': 'write', 'summary': '고객의 지원 티켓을 만든다. 필수: customerId, subject, priority(low|normal|high|urgent).',
                           'select': ['id', 'customerId', 'subject', 'status', 'priority']},
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--language', choices=sorted(SOURCES), default='spring')
    args = parser.parse_args()
    importer, folder = SOURCES[args.language]
    if not (GENERATED / 'small' / folder).exists():
        generate(GENERATED.parent / 'generated')

    source = importer.from_directory(GENERATED / 'small' / folder, namespace='shop')
    records = list(source.iter_operations())
    print('1. routes found:', len(records), '| parse diagnostics:', source.diagnostics)
    for record in records[:3]:
        print('   ', record.summary())
    print('2. unsupported:', [record.summary() for record in records if record.status != 'imported'])

    # Select by (method, path) so the same table works for Spring, Go and Rust handler names.
    operations = {record.operation_id: EXPOSE[(record.method.upper(), record.path)] for record in records
                  if record.status == 'imported' and (record.method.upper(), record.path) in EXPOSE}
    print('3. exposing:', json.dumps(operations, ensure_ascii=False)[:400], '...')

    with ExitStack() as stack:
        command, env = build('small', args.language)
        origin = stack.enter_context(process(args.language, command, env))
        app = convert(source, operations=operations, deployment=HTTPDeployment(origin, timeout_ms=5000, deadline_ms=8000))
        caller = ExecutionContext('alice', 'tenant-a', frozenset())
        print('4. capability ids:', sorted(d['id'] for d in app.descriptors()))
        search = next(d['id'] for d in app.descriptors() if '검색' in d['summary'])
        print('   search:', app.invoke(search, {'body': {'query': 'minji'}}, context=caller))
        create = next(d['id'] for d in app.descriptors() if d['effects']['kind'] == 'write')
        # Rust/Java DTOs declare required fields, so a2api rejects this before the call (INVALID_INPUT);
        # Go structs do not, so the Go server itself answers 400 (UPSTREAM_VALIDATION_FAILED).
        print('   create (missing priority):', app.invoke(create, {'body': {'customerId': 'C-004', 'subject': 'x'}}, context=caller)['error']['code'])
        print('   serve over MCP: anyio.run(serve_stdio, app, caller)   # a2api.mcp_bridge')


if __name__ == '__main__':
    main()
