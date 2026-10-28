"""Opt-in public GET verification, separate from deterministic offline tests."""

import argparse
import json
from pathlib import Path

from a2api import A2APIError, HTTPAdapter
from a2api.execution import Budget
from a2api.importers import OpenAPIImporter
from a2api.ir import ExecutionContext
from a2api.schema import validate_value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--owner', default='metahackAI')
    parser.add_argument('--repo', default='a2api')
    args = parser.parse_args()
    importer = OpenAPIImporter.from_file(Path(__file__).with_name('api.github.com.json.gz'), namespace='github')
    context = ExecutionContext('public-fixture-reader', 'public-fixture', frozenset())
    results = []
    for record in importer.iter_operations({'meta/get', 'repos/get', 'issues/list-for-repo'}):
        if record.capability is None:
            results.append({'operationId': record.operation_id, 'status': record.status})
            continue
        operation = record.capability.operations[record.operation_id]
        route = record.http_route('https://api.github.com', headers={'User-Agent': 'a2api-importer-verification'})
        adapter = HTTPAdapter({(operation.service_ref, operation.operation_ref): route})
        arguments = {} if record.operation_id == 'meta/get' else {'path': {'owner': args.owner, 'repo': args.repo}}
        if record.operation_id == 'issues/list-for-repo':
            arguments['query'] = {'per_page': 2, 'page': 1}
        budget = Budget(15000, 1)
        try:
            validate_value(operation.input_schema, arguments, code='INVALID_INPUT', status=422)
            result = adapter.call(operation, arguments, context, budget, 10000)
            validate_value(operation.output_schema, result, code='SCHEMA_MISMATCH', status=502)
            results.append({'operationId': record.operation_id, 'status': 'validated', 'backendCalls': budget.calls,
                            'resultType': type(result['result']).__name__})
        except A2APIError as error:
            results.append({'operationId': record.operation_id, 'status': 'failed', 'error': error.problem()})
    print(json.dumps({'origin': 'https://api.github.com', 'authentication': 'none', 'results': results}, indent=2))
    return 0 if all(result['status'] == 'validated' for result in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
