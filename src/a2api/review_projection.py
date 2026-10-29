"""Conservative conversion of explicitly selected source fields to MVP schemas."""

from __future__ import annotations

import copy

from .errors import A2APIError
from .pointers import resolve, tokens
from .schema import KEYWORDS, check_schema

ANNOTATIONS = {'$schema', '$defs', '$comment', 'title', 'description', 'default', 'examples', 'example',
               'deprecated', 'readOnly', 'writeOnly', 'xml', 'externalDocs', 'discriminator'}


def unsupported(detail: str) -> A2APIError:
    return A2APIError('UNSUPPORTED_PROJECTION', detail)


def dereference(root: dict, node: dict, seen: frozenset = frozenset()) -> dict:
    if not isinstance(node, dict):
        raise unsupported('Selected schemas must have explicit object-valued declarations.')
    if '$ref' not in node:
        return node
    ref = node['$ref']
    if not isinstance(ref, str) or not ref.startswith('#/$defs/') or ref in seen:
        raise unsupported('Selected schemas require finite bundled local references.')
    if set(node) - {'$ref'} - ANNOTATIONS:
        raise unsupported('Schema reference validation siblings require a separate conversion rule.')
    try:
        target = resolve(root, ref[1:])
    except A2APIError:
        raise unsupported('Selected schema reference is unresolved.') from None
    return dereference(root, target, seen | {ref})


def field_schema(root: dict, pointer: str) -> tuple[dict, bool]:
    node, required = root, True
    for key in tokens(pointer):
        node = dereference(root, node)
        if node.get('type') != 'object' or key not in node.get('properties', {}):
            raise unsupported('Field pointers may traverse declared object properties only.')
        # Dependencies and alternatives on a parent cannot be faithfully flattened.
        if set(node) - KEYWORDS - ANNOTATIONS - {'$ref'} - {k for k in node if k.startswith('x-')}:
            raise unsupported('Selected field ancestors contain unsupported validation rules.')
        required = required and key in node.get('required', [])
        node = node['properties'][key]
    return node, required


def normalize(root: dict, node: dict, *, direction: str, depth: int = 0, seen: frozenset = frozenset()) -> dict:
    if depth > 64:
        raise unsupported('Selected schemas exceed the supported finite depth.')
    if isinstance(node, dict) and '$ref' in node:
        ref = node['$ref']
        if ref in seen:
            raise unsupported('Recursive selected values require a separate executable profile.')
        node = dereference(root, node)
        seen = seen | {ref}
    if not isinstance(node, dict) or 'type' not in node:
        raise unsupported('Selected values must declare an MVP-compatible type.')
    if (direction == 'input' and node.get('readOnly')) or (direction == 'output' and node.get('writeOnly')):
        raise unsupported('Selected readOnly/writeOnly fields require contextual review projection.')
    unknown = set(node) - KEYWORDS - ANNOTATIONS - {k for k in node if k.startswith('x-')}
    if unknown:
        raise unsupported('Selected schemas contain validation rules outside the executable MVP profile.')
    result = {key: copy.deepcopy(value) for key, value in node.items()
              if key in KEYWORDS and key != 'x-a2api-semanticType'}
    if node['type'] == 'object':
        if node.get('additionalProperties') is not False:
            raise unsupported('Whole selected objects must be closed; select their individual fields instead.')
        result['properties'] = {key: normalize(root, value, direction=direction, depth=depth + 1, seen=seen)
                                for key, value in node.get('properties', {}).items()}
    elif node['type'] == 'array':
        if 'items' not in node:
            raise unsupported('Selected arrays must declare their item schema.')
        result['items'] = normalize(root, node['items'], direction=direction, depth=depth + 1, seen=seen)
    return result


def projected_schema(root: dict, fields: dict, *, direction: str) -> dict:
    properties, required = {}, []
    for name, field in sorted(fields.items()):
        try:
            node, guaranteed = field_schema(root, field['pointer'])
            needed = field.get('required', guaranteed)
            if direction == 'input' and guaranteed and not needed:
                raise unsupported('Required source inputs cannot become optional reviewed inputs.')
            if direction == 'output' and needed and not guaranteed:
                raise unsupported('Optional source results cannot become guaranteed reviewed results.')
            properties[name] = normalize(root, node, direction=direction)
        except A2APIError as error:
            raise A2APIError(error.code, error.detail, issues=[{'schema': direction, 'field': name,
                             'sourcePointer': field['pointer']}]) from None
        if needed:
            required.append(name)
    return {'type': 'object', 'properties': properties, 'required': required, 'additionalProperties': False}


def required_leaves(root: dict, node: dict | None = None, pointer: str = '', depth: int = 0) -> set[str]:
    if depth > 64:
        raise unsupported('Source input requirements exceed the supported finite depth.')
    node = dereference(root, root if node is None else node)
    if node.get('type') != 'object' or not node.get('required'):
        return {pointer} if pointer else set()
    paths = set()
    for key in node['required']:
        if key not in node.get('properties', {}):
            raise unsupported('Required source fields need explicit property declarations.')
        escaped = key.replace('~', '~0').replace('/', '~1')
        paths.update(required_leaves(root, node['properties'][key], pointer + '/' + escaped, depth + 1))
    return paths


def check_input_coverage(root: dict, fields: dict, projected: dict) -> None:
    pointers = [tokens(field['pointer']) for field in fields.values()]
    for index, left in enumerate(pointers):
        if not left:
            raise unsupported('Request mappings must select named fields, not the whole input root.')
        for right in pointers[index + 1:]:
            if left == right[:len(left)] or right == left[:len(right)]:
                raise unsupported('Request field pointers must not overlap.')
    required = [tokens(fields[name]['pointer']) for name in projected['required']]
    for leaf in required_leaves(root):
        path = tokens(leaf)
        if not any(path[:len(prefix)] == prefix for prefix in required):
            raise unsupported('Reviewed input mappings omit a required source field.')


def annotate(schemas: dict, annotations: list, semantic_types: dict) -> None:
    from .openapi_schema import schema_nodes
    for annotation in annotations:
        schema = schemas[annotation['schema']]
        nodes = dict(schema_nodes(schema))
        pointer = annotation['pointer']
        if pointer not in nodes:
            raise unsupported('Semantic annotations must select a generated schema node.')
        node = nodes[pointer]
        if 'x-a2api-semanticType' in node:
            raise unsupported('Semantic annotations must not overlap.')
        node['x-a2api-semanticType'] = annotation['semanticType']
    for schema in schemas.values():
        check_schema(schema, semantic_types)
