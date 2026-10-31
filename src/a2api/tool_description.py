"""Bounded, schema-derived output hints for selected host function tools."""

import json
import re

from .errors import A2APIError
from .pointers import resolve
from .review_projection import ANNOTATIONS


def output_hint(schema):
    def node(value):
        seen = set()
        for _ in range(32):
            if not isinstance(value, dict):return {}
            branches = value.get('anyOf')
            if (isinstance(branches, list) and len(branches) == 2 and {'type': 'null'} in branches
                    and not set(value) - ANNOTATIONS - {'anyOf'}):
                # A nullable wrapper (Go slices/pointers, Java references): describe the value branch.
                value = branches[0] if branches[1] == {'type': 'null'} else branches[1]
                continue
            if any(key in value for key in ('allOf', 'anyOf', 'oneOf', 'not', 'if', 'then', 'else')):return {}
            ref = value.get('$ref')
            if ref is None:return value
            if (not isinstance(ref, str) or not ref.startswith('#/$defs/') or ref in seen
                    or set(value) - ANNOTATIONS - {'$ref'} - {key for key in value if key.startswith('x-')}):return {}
            seen.add(ref)
            try:value = resolve(schema, ref[1:])
            except A2APIError:return {}
        return {}

    def kind(value):
        value = node(value).get('type')
        allowed = {'string', 'number', 'integer', 'boolean', 'null', 'object', 'array'}
        if isinstance(value, str):return value if value in allowed else 'JSON'
        if isinstance(value, list) and value and all(isinstance(item, str) and item in allowed for item in value):
            return '|'.join(dict.fromkeys(value))
        return 'JSON'

    root = node(schema)
    prefix = 'Returns ' + kind(root)
    if root.get('type') == 'array':
        root = node(root.get('items'))
        prefix = 'Returns array items'
    fields = root.get('properties')
    if root.get('type') != 'object' or not isinstance(fields, dict):return prefix + '.'
    required = root.get('required', [])
    entries = []
    for name, value in list(fields.items())[:6]:
        label = json.dumps(name, ensure_ascii=True)
        if len(label) > 80:break
        entries.append(label + ':' + kind(value) + (' (required)' if name in required else ' (optional)'))
    if len(fields) > len(entries):entries.append('+' + str(len(fields) - len(entries)) + ' other fields')
    return prefix + (' fields: ' + ', '.join(entries) if entries else '') + '.'


_FIELD = re.compile(r'[A-Za-z_][A-Za-z0-9_]{0,47}')


def _resolve(schema, value):
    """Local refs and nullable wrappers only; composites stay opaque (returns {})."""
    seen = set()
    for _ in range(32):
        if not isinstance(value, dict):
            return {}
        branches = value.get('anyOf')
        if (isinstance(branches, list) and len(branches) == 2 and {'type': 'null'} in branches
                and not set(value) - ANNOTATIONS - {'anyOf'}):
            value = branches[0] if branches[1] == {'type': 'null'} else branches[1]
            continue
        if any(key in value for key in ('allOf', 'anyOf', 'oneOf', 'not', 'if', 'then', 'else')):
            return {}
        ref = value.get('$ref')
        if ref is None:
            return value
        if (not isinstance(ref, str) or not ref.startswith('#/$defs/') or ref in seen
                or set(value) - ANNOTATIONS - {'$ref'} - {key for key in value if key.startswith('x-')}):
            return {}
        seen.add(ref)
        try:
            value = resolve(schema, ref[1:])
        except A2APIError:
            return {}
    return {}


def output_shape(schema, *, max_fields=12):
    """Compact result shape such as {items:[{id,status}],total,hasMore?}: names only, '?' = optional."""
    budget = [max_fields]

    def shape(value, depth):
        value = _resolve(schema, value)
        declared = value.get('type')
        kinds = set(declared) if isinstance(declared, list) else {declared}
        if 'array' in kinds:
            inner = shape(value.get('items'), depth)
            return '[' + inner + ']'
        if 'object' in kinds and isinstance(value.get('properties'), dict):
            if depth >= 3:
                return '{...}'
            parts = []
            for name, child in value['properties'].items():
                if budget[0] <= 0 or not isinstance(name, str) or not _FIELD.fullmatch(name):
                    parts.append('...')
                    break
                budget[0] -= 1
                inner = shape(child, depth + 1)
                parts.append(name + ('' if name in value.get('required', []) else '?') + (':' + inner if inner else ''))
            return '{' + ','.join(parts) + '}'
        return ''

    root = _resolve(schema, schema)
    result = shape(root, 0)
    if result:
        return 'Returns ' + result + '.'
    declared = root.get('type')
    return 'Returns ' + (declared if isinstance(declared, str) and declared in ('string', 'number', 'integer', 'boolean', 'null')
                         else 'JSON') + '.'


def function_description(descriptor, style='shape'):
    """'none' (summary, [write] marks writes), 'shape' (compact result names) or 0.3 'typed'."""
    if style == 'none':
        return descriptor['summary'] + (' [write]' if descriptor['effects']['kind'] == 'write' else '')
    if style == 'typed':
        return (descriptor['summary'] + ' [effect: ' + descriptor['effects']['kind'] + '] '
                + output_hint(descriptor['outputSchema']))
    return descriptor['summary'] + ' [' + descriptor['effects']['kind'] + '] ' + output_shape(descriptor['outputSchema'])
