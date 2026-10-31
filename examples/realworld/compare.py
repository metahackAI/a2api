"""Compare what a2api reads from real RealWorld (Conduit) server code with the official OpenAPI document.

Static only: the importers parse the source files; nothing is built or executed.

python examples/realworld/compare.py /path/to/realworld-checkouts [--json out.json]

For each of the 19 Conduit operations (matched by method + path) it reports whether the code import
found it, and compares path/query/body field names, the body root key and the response top-level keys.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from a2api.importers import GoSourceImporter, OpenAPIImporter, RustSourceImporter, SpringSourceImporter, load_openapi
from a2api.ir import thaw

SOURCES = {
    'spring': (SpringSourceImporter, 'spring-boot-realworld-example-app/src/main/java'),
    'go-gin': (GoSourceImporter, 'golang-gin-realworld-example-app'),
    'rust-axum': (RustSourceImporter, 'realworld-axum-sqlx/src'),
}
try:
    from a2api.importers import FastAPISourceImporter
    SOURCES['python-fastapi'] = (FastAPISourceImporter, 'fastapi-realworld-example-app/app')
except ImportError:
    pass


def norm(path):
    path = re.sub(r'/api(?=/)', '', path, count=1)
    return re.sub(r'\{[^}]+\}|:[A-Za-z_]+', '{}', path.rstrip('/') or '/')


def unwrap(schema):
    if isinstance(schema, dict) and 'anyOf' in schema:
        branches = [b for b in schema['anyOf'] if b != {'type': 'null'}]
        return unwrap(branches[0]) if len(branches) == 1 else schema
    return schema if isinstance(schema, dict) else {}


def shape(schema, depth=2):
    """Field names down to `depth` levels: {'article': {'title': {}, ...}}."""
    schema = unwrap(schema)
    if depth == 0:
        return {}
    if schema.get('type') == 'array' or 'items' in schema:
        return shape(schema.get('items', {}), depth)
    return {key: shape(child, depth - 1) for key, child in (schema.get('properties') or {}).items()}


def resolve(document, node):
    while isinstance(node, dict) and '$ref' in node:
        target = document
        for part in node['$ref'].lstrip('#/').split('/'):
            target = target[part]
        node = target
    if isinstance(node, dict):
        return {key: resolve(document, child) for key, child in node.items()}
    if isinstance(node, list):
        return [resolve(document, child) for child in node]
    return node


def spec_operations(document):
    found = {}
    for path, item in document['paths'].items():
        for method, operation in item.items():
            if method not in ('get', 'post', 'put', 'delete', 'patch'):
                continue
            operation = resolve(document, operation)
            params = {where: sorted(p['name'] for p in operation.get('parameters', []) if p['in'] == where) for where in ('path', 'query')}
            body = (((operation.get('requestBody') or {}).get('content') or {}).get('application/json') or {}).get('schema')
            responses = [r for code, r in operation['responses'].items() if code.startswith('2')]
            output = ((responses[0].get('content') or {}).get('application/json') or {}).get('schema') if responses else None
            found[(method.upper(), norm(path))] = {'id': operation['operationId'], 'path': params['path'], 'query': params['query'],
                                                   'body': shape(body) if body else None, 'output': shape(output) if output else None}
    return found


def code_operations(importer):
    found, unsupported = {}, []
    for item in importer.iter_operations():
        if item.operation is None:
            unsupported.append({'id': item.operation_id, 'method': item.method, 'path': item.path,
                                'reason': item.diagnostics[0]['detail'] if item.diagnostics else ''})
            continue
        inputs = thaw(item.operation.input_schema)['properties']
        output = thaw(item.operation.output_schema)['properties']['result']
        found[(item.method, norm(item.path))] = {
            'id': item.operation_id, 'path': sorted((inputs.get('path') or {}).get('properties') or {}),
            'query': sorted((inputs.get('query') or {}).get('properties') or {}),
            'body': shape(inputs['body']) if 'body' in inputs else None,
            'output': shape(output) if output and output != {'type': 'null'} else None,
            'warnings': [d['code'] for d in item.diagnostics]}
    return found, unsupported


def compare(expected, actual):
    """Field-name agreement per part: path names are compared by count (names may differ), others by name."""
    checks = {'path': len(expected['path']) == len(actual['path']), 'query': expected['query'] == actual['query']}
    checks['body'] = expected['body'] == actual['body'] if expected['body'] or actual['body'] else True
    if expected['output'] is None:
        checks['output'] = actual['output'] is None
    elif actual['output'] is None or actual['output'] == {}:
        checks['output'] = None  # open/unknown output: not checked
    else:
        checks['output'] = set(expected['output']) == set(actual['output']) and all(
            set(expected['output'][key]) <= set(actual['output'].get(key, {})) for key in expected['output'])
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('--untyped-output', default='reject', choices=['reject', 'open'])
    parser.add_argument('--json', type=Path)
    options = parser.parse_args()
    document = load_openapi(options.root / 'realworld/specs/api/openapi.yml')[0]
    spec = spec_operations(document)
    report = {'spec': len(spec), 'sources': {}}
    for name, (cls, directory) in SOURCES.items():
        try:
            importer = cls(options.root / directory, namespace='conduit', untyped_output=options.untyped_output)
            found, unsupported = code_operations(importer)
        except Exception as error:  # an importer that cannot read the project at all
            report['sources'][name] = {'error': f'{type(error).__name__}: {error}'}
            print(f'{name}: ERROR {error}')
            continue
        rows = []
        for key, expected in spec.items():
            actual = found.get(key)
            rows.append({'operation': expected['id'], 'found': actual is not None,
                         'checks': compare(expected, actual) if actual else None,
                         'warnings': actual['warnings'] if actual else None,
                         'actual': actual, 'expected': expected})
        matched = sum(row['found'] for row in rows)
        exact = sum(1 for row in rows if row['found'] and all(v is not False for v in row['checks'].values()))
        extra = [found[key]['id'] for key in found if key not in spec]
        report['sources'][name] = {'imported': len(found), 'unsupported': unsupported, 'matched': matched,
                                   'allFieldsAgree': exact, 'extra': extra, 'rows': rows}
        print(f'{name}: imported {len(found)}, unsupported {len(unsupported)}, matched {matched}/{len(spec)}, '
              f'field names agree {exact}/{len(spec)}')
        for row in rows:
            if not row['found']:
                print(f"   missing {row['operation']}")
            elif any(v is False for v in row['checks'].values()):
                bad = [k for k, v in row['checks'].items() if v is False]
                print(f"   differs {row['operation']}: {bad} expected={ {k: row['expected'][k] for k in bad} } "
                      f"actual={ {k: row['actual'][k] for k in bad} }"[:600])
        for item in unsupported[:10]:
            print(f"   unsupported {item['method']} {item['path']} {item['id']}: {item['reason'][:140]}")
    if options.json:
        options.json.write_text(json.dumps(report, indent=1, default=str))


if __name__ == '__main__':
    main()
