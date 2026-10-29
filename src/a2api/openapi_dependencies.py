"""Static, local OpenAPI dependency fingerprints and operation-level impact diff."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
from urllib.parse import unquote

from .errors import A2APIError
from .ir import thaw
from .openapi_schema import schema_nodes
from .pointers import resolve, tokens

INDEX_FORMAT = 'a2api-openapi-dependencies/0.1'
SNAPSHOT_FORMAT = 'a2api-openapi-source/0.1'


def canonical_bytes(value) -> bytes:
    try:
        return (json.dumps(thaw(value), sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(',', ':')) + '\n').encode('utf-8')
    except (TypeError, ValueError, UnicodeError, RecursionError):
        raise A2APIError('DEPENDENCY_SNAPSHOT_INVALID', 'Dependency snapshots must contain finite UTF-8 JSON values.') from None


def digest(value) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def operation_key(method: str, path: str) -> str:
    return method.upper() + ' ' + path


def snapshot(importer) -> dict:
    return {'format': SNAPSHOT_FORMAT, 'sourceSha256': importer.source_hash, 'sourceName': importer.source_name,
            'namespace': importer.namespace, 'requestedMethods': sorted(importer.methods), 'document': importer.document}


def snapshot_importer(value: dict):
    from .importers import OpenAPIImporter
    if (not isinstance(value, dict) or set(value) != {'format', 'sourceSha256', 'sourceName', 'namespace', 'requestedMethods', 'document'}
            or value['format'] != SNAPSHOT_FORMAT or not isinstance(value['sourceSha256'], str)
            or len(value['sourceSha256']) != 64 or any(c not in '0123456789abcdef' for c in value['sourceSha256'])
            or not isinstance(value['sourceName'], str) or not isinstance(value['namespace'], str)
            or not isinstance(value['requestedMethods'], list) or not value['requestedMethods']
            or any(not isinstance(method, str) for method in value['requestedMethods'])):
        raise A2APIError('DEPENDENCY_SNAPSHOT_INVALID', 'The OpenAPI source snapshot has an unsupported format.')
    return OpenAPIImporter(value['document'], namespace=value['namespace'], source_name=value['sourceName'],
                           source_hash=value['sourceSha256'], methods=set(value['requestedMethods']))


def _escape(value: str) -> str:
    return value.replace('~', '~0').replace('/', '~1')


def _reference(value: str) -> str:
    if not isinstance(value, str) or not value.startswith('#/'):
        raise A2APIError('DEPENDENCY_EXTERNAL_REFERENCE', 'Dependency discovery supports document-local references only.')
    return '/' + '/'.join(_escape(key) for key in tokens(unquote(value[1:])))


def _references(value, *, schema: bool = False, depth: int = 0):
    if depth > 128:
        raise A2APIError('DEPENDENCY_DEPTH', 'Dependency discovery exceeded the supported structural depth.')
    if schema:
        for _, node in schema_nodes(value):
            if '$ref' in node:
                yield _reference(node['$ref']), True
            mapping = node.get('discriminator', {}).get('mapping', {}) if isinstance(node.get('discriminator', {}), dict) else {}
            for reference in mapping.values() if isinstance(mapping, dict) else ():
                if isinstance(reference, str) and reference.startswith('#/'):
                    yield _reference(reference), True
        return
    if isinstance(value, dict):
        if '$ref' in value:
            yield _reference(value['$ref']), False
            return
        for name, child in value.items():
            # Literal JSON data and extensions are not Reference Objects.
            if name in {'example', 'default', 'enum', 'const', 'value', 'externalDocs'} or name.startswith('x-'):
                continue
            yield from _references(child, schema=name == 'schema', depth=depth + 1)
    elif isinstance(value, list):
        for child in value:
            yield from _references(child, depth=depth + 1)


def _fingerprint(entry: dict, nodes: dict) -> str:
    return digest({key: entry[key] for key in ('operationId', 'contentDigest', 'contextDigest', 'identityDigest', 'errors')} |
                  {'dependencies': {pointer: nodes[pointer] for pointer in entry['dependencies']}})


def dependency_index(importer) -> dict:
    """Scan source structure without converting operation schemas or fetching refs."""
    from .importers.openapi import _identifier
    from .importers.schema_conversion import ImportIssue
    document, nodes, edges, node_errors = importer.document, {}, {}, {}
    components = document.get('components', {})
    for category, definitions in components.items() if isinstance(components, dict) else ():
        if isinstance(definitions, dict):
            for name, value in definitions.items():
                nodes['/components/' + _escape(category) + '/' + _escape(name)] = digest(value)

    def dependencies(initial, errors):
        pending, found, visited = sorted(initial), set(), set()
        while pending:
            pointer, is_schema = pending.pop()
            state = (pointer, is_schema)
            if state in visited:
                continue
            visited.add(state)
            found.add(pointer)
            if len(found) > 4096:
                errors.add('DEPENDENCY_LIMIT')
                nodes.setdefault(pointer, digest({'limited': pointer}))
                break
            if state not in edges:
                try:
                    value = resolve(document, pointer)
                    nodes[pointer] = digest(value)
                    edges[state] = tuple(sorted(set(_references(value, schema=is_schema))))
                    node_errors[state] = ()
                except (A2APIError, AttributeError, TypeError, ValueError, RecursionError):
                    nodes.setdefault(pointer, digest({'unresolved': pointer}))
                    edges[state], node_errors[state] = (), ('DEPENDENCY_UNRESOLVED',)
            errors.update(node_errors[state])
            pending.extend(edges[state])
        return sorted(found)

    operations = {}
    for path, method, item, operation, opid, issue in importer._operations:
        errors, initial = set(), set()
        if issue:
            errors.add(issue.code)
        if importer._ids[opid] > 1:
            errors.add('DUPLICATE_OPERATION_ID')
        try:
            # Parameters inherited from a path matter only when not overridden.
            parameters = [parameter for parameter, _ in importer._parameters(item, operation, '/paths/' + _escape(path) + '/' + method).values()]
            # Retain reference objects as well as their resolved effective values.
            overridden = {(p.get('in'), p.get('name', '').lower() if p.get('in') == 'header' else p.get('name'))
                          for p, _ in importer._parameters({}, operation, '/paths/' + _escape(path) + '/' + method).values()}
            inherited = []
            for parameter in item.get('parameters', []):
                resolved = importer._object(parameter, '/paths/' + _escape(path) + '/parameters')
                key = (resolved.get('in'), resolved.get('name', '').lower() if resolved.get('in') == 'header' else resolved.get('name'))
                if key not in overridden:
                    inherited.append(parameter)
            security = operation.get('security', document.get('security', []))
            if not isinstance(security, list) or any(not isinstance(requirement, dict) for requirement in security):
                raise A2APIError('DEPENDENCY_INVALID', 'Security requirements must be an array of objects.')
            names = {name for requirement in security for name in requirement}
            initial.update(('/components/securitySchemes/' + _escape(name), False) for name in names)
            context = {'openapi': document['openapi'], 'jsonSchemaDialect': document.get('jsonSchemaDialect'),
                       'parameters': parameters, 'security': security,
                       'servers': operation.get('servers', item.get('servers', document.get('servers', []))),
                       'pathSummary': item.get('summary'), 'pathDescription': item.get('description')}
            initial.update(_references(operation))
            initial.update(_references(inherited))
            raw_path = document['paths'][path]
            if '$ref' in raw_path:
                initial.add((_reference(raw_path['$ref']), False))
        except (ImportIssue, A2APIError, AttributeError, TypeError, ValueError, RecursionError) as error:
            # Malformed dependencies are attached to this operation; references are never fetched.
            errors.add(getattr(error, 'code', 'DEPENDENCY_INVALID'))
            context = {'invalid': True, 'pathItem': item}
        entry = {'path': path, 'method': method, 'operationId': opid,
                 'contentDigest': digest(operation), 'contextDigest': digest(context),
                 'identityDigest': digest({'idCount': importer._ids[opid],
                                          'normalizedCount': importer._capability_ids[_identifier(importer.namespace, opid)]}),
                 'dependencies': dependencies(initial, errors), 'errors': sorted(errors)}
        capability_id = _identifier(importer.namespace, opid)
        if importer._capability_ids[capability_id] > 1:
            capability_id += '_' + hashlib.sha256((method + ' ' + path).encode()).hexdigest()[:12]
        entry['capabilityId'] = capability_id
        entry['errors'] = sorted(errors)
        entry['fingerprint'] = _fingerprint(entry, nodes)
        operations[operation_key(method, path)] = entry
    result = {'format': INDEX_FORMAT, 'sourceSha256': importer.source_hash, 'documentDigest': digest(document),
              'namespace': importer.namespace, 'requestedMethods': sorted(importer.methods),
              'nodes': dict(sorted(nodes.items())), 'operations': dict(sorted(operations.items()))}
    result['indexDigest'] = digest(result)
    return result


def validate_index(index: dict) -> None:
    try:
        if index['format'] != INDEX_FORMAT or index['indexDigest'] != digest({key: value for key, value in index.items() if key != 'indexDigest'}):
            raise ValueError()
        for key, entry in index['operations'].items():
            if key != operation_key(entry['method'], entry['path']) or entry['fingerprint'] != _fingerprint(entry, index['nodes']):
                raise ValueError()
    except (KeyError, TypeError, ValueError, AttributeError):
        raise A2APIError('DEPENDENCY_SNAPSHOT_INVALID', 'Dependency index fingerprints are inconsistent.') from None


def diff_indices(before: dict, after: dict) -> dict:
    validate_index(before)
    validate_index(after)
    if before['namespace'] != after['namespace'] or tuple(before['requestedMethods']) != tuple(after['requestedMethods']):
        raise A2APIError('DEPENDENCY_SCOPE_MISMATCH', 'Dependency snapshots must use the same namespace and method selection.')
    operations, counts = [], Counter()
    for key in sorted(before['operations'].keys() | after['operations'].keys()):
        old, new = before['operations'].get(key), after['operations'].get(key)
        status = 'added' if old is None else 'removed' if new is None else 'unchanged' if old['fingerprint'] == new['fingerprint'] else 'changed'
        reasons = []
        if old and new and status == 'changed':
            for field, kind in (('contentDigest', 'operation'), ('contextDigest', 'context'), ('identityDigest', 'identity')):
                if old[field] != new[field]:
                    reasons.append({'kind': kind, 'pointer': '/paths/' + _escape(new['path']) + '/' + new['method']})
            for pointer in sorted(set(old['dependencies']) | set(new['dependencies'])):
                removed, added = pointer not in new['dependencies'], pointer not in old['dependencies']
                if removed or added or before['nodes'].get(pointer) != after['nodes'].get(pointer):
                    reasons.append({'kind': 'reference', 'pointer': pointer,
                                    'change': 'removed' if removed else 'added' if added else 'modified'})
            if tuple(old['errors']) != tuple(new['errors']):
                reasons.append({'kind': 'dependency_error', 'pointer': '/paths/' + _escape(new['path'])})
        entry = new or old
        counts[status] += 1
        operations.append({'key': key, 'method': entry['method'], 'path': entry['path'], 'operationId': entry['operationId'],
                           'status': status, 'reasons': reasons, 'errors': entry['errors']})
    changed_nodes = [pointer for pointer in sorted(before['nodes'].keys() | after['nodes'].keys())
                     if before['nodes'].get(pointer) != after['nodes'].get(pointer)]
    return {'beforeSourceSha256': before['sourceSha256'], 'afterSourceSha256': after['sourceSha256'],
            'summary': dict(sorted(counts.items())), 'changedReferences': changed_nodes, 'operations': operations}


def diff_openapi(before: str, after: str, *, namespace: str | None = None, methods: set[str] | None = None,
                 review=None) -> dict:
    from .importers import OpenAPIImporter
    if review is not None:
        from .builder import load_review, REVIEW_META
        from .schema import validate_value
        review = load_review(review) if isinstance(review, (str, Path)) else review
        validate_value(REVIEW_META, review, code='INVALID_REVIEW', status=400)
        if namespace is not None and namespace != review['source']['namespace']:
            raise A2APIError('DEPENDENCY_SCOPE_MISMATCH', 'Review and diff namespaces disagree.')
        namespace = review['source']['namespace']
    namespace = namespace or 'imported'
    old = OpenAPIImporter.from_file(before, namespace=namespace, methods=methods)
    new = OpenAPIImporter.from_file(after, namespace=namespace, methods=methods)
    before_index = dependency_index(old)
    result = diff_indices(before_index, dependency_index(new))
    if review is not None:
        if old.source_hash != review['source']['sha256']:
            raise A2APIError('SOURCE_DRIFT', 'The before document does not match the review baseline.')
        identities = {}
        for key, entry in before_index['operations'].items():
            identities.setdefault(entry['operationId'], []).append(key)
        source_keys = {}
        for operation in review['operations']:
            keys = identities.get(operation['source']['operationId'], [])
            if len(keys) != 1:
                raise A2APIError('DEPENDENCY_REVIEW_MISMATCH', 'Reviewed operations must resolve uniquely in the before document.')
            if before_index['operations'][keys[0]]['capabilityId'] != operation['source']['capabilityId']:
                raise A2APIError('DEPENDENCY_REVIEW_MISMATCH', 'The reviewed capability ID differs from the source inventory.')
            source_keys[operation['id']] = keys[0]
        if any(key not in source_keys for capability in review['capabilities'] for key in capability['operationIds']):
            raise A2APIError('INVALID_REVIEW', 'A capability references an operation outside the review settings.')
        changed = {entry['key'] for entry in result['operations'] if entry['status'] != 'unchanged'}
        result['capabilities'] = [
            {'id': capability['id'], 'version': capability['version'],
             'state': 'requires_review' if review['review']['state'] != 'reviewed' or any(source_keys[key] in changed for key in capability['operationIds']) else 'reviewed',
             'affectedOperationIds': sorted(key for key in capability['operationIds'] if source_keys[key] in changed)}
            for capability in review['capabilities']]
    return result
