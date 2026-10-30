"""Bounded, schema-derived output hints for selected host function tools."""

import json

from .errors import A2APIError
from .pointers import resolve
from .review_projection import ANNOTATIONS


def output_hint(schema):
    def node(value):
        seen = set()
        for _ in range(32):
            if not isinstance(value, dict):return {}
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


def function_description(descriptor):
    return (descriptor['summary'] + ' [effect: ' + descriptor['effects']['kind'] + '] '
            + output_hint(descriptor['outputSchema']))
