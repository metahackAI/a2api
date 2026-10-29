"""A small JSON-valued Python typing profile for explicit callable registration."""

from __future__ import annotations

import math
import types
import typing

from .errors import A2APIError


def json_copy(value, *, code: str, status: int):
    """Copy JSON values without silently converting tuples or non-string keys."""
    import json
    def check(node):
        if node is None or type(node) in (str, bool, int):
            return
        if type(node) is float and math.isfinite(node):
            return
        if type(node) is list:
            for child in node:
                check(child)
            return
        if type(node) is dict and all(type(key) is str for key in node):
            for child in node.values():
                check(child)
            return
        raise ValueError()
    try:
        check(value)
        return json.loads(json.dumps(value, ensure_ascii=False, allow_nan=False).encode('utf-8'))
    except (ValueError, TypeError, UnicodeError, RecursionError):
        raise A2APIError(code, 'Values must contain finite UTF-8 JSON data with string object keys.', status=status) from None


def type_schema(annotation, seen: frozenset = frozenset()) -> dict:
    scalar = {str: 'string', bool: 'boolean', int: 'integer', float: 'number', type(None): 'null'}
    for kind, name in scalar.items():
        if annotation is kind:
            return {'type': name}
    origin, args = typing.get_origin(annotation), typing.get_args(annotation)
    if origin in (typing.Union, types.UnionType):
        return {'anyOf': [type_schema(child, seen) for child in args]}
    if origin is typing.Literal:
        values = json_copy(list(args), code='UNSUPPORTED_TYPE_HINT', status=400)
        if any(type(value) not in (str, bool, int, float, type(None)) for value in values):
            raise A2APIError('UNSUPPORTED_TYPE_HINT', 'Literal values must be JSON scalars.')
        return {'enum': values}
    if origin is list and len(args) == 1:
        return {'type': 'array', 'items': type_schema(args[0], seen)}
    if origin is dict and len(args) == 2 and args[0] is str:
        return {'type': 'object', 'propertyNames': {'type': 'string'}, 'additionalProperties': type_schema(args[1], seen)}
    if typing.is_typeddict(annotation):
        if annotation in seen or len(seen) >= 32:
            raise A2APIError('UNSUPPORTED_TYPE_HINT', 'Recursive TypedDict definitions require an explicit schema or wrapper.')
        try:
            hints = typing.get_type_hints(annotation, include_extras=True)
        except (NameError, TypeError, AttributeError):
            raise A2APIError('UNSUPPORTED_TYPE_HINT', 'TypedDict annotations must resolve in their defining module.') from None
        properties, required = {}, []
        for name, child in hints.items():
            qualifier = typing.get_origin(child)
            needed = name in annotation.__required_keys__
            if qualifier in (typing.Required, typing.NotRequired):
                needed = qualifier is typing.Required
                child = typing.get_args(child)[0]
            properties[name] = type_schema(child, seen | {annotation})
            if needed:
                required.append(name)
        return {'type': 'object', 'properties': properties, 'required': required, 'additionalProperties': False}
    raise A2APIError('UNSUPPORTED_TYPE_HINT', 'Use supported JSON type hints, explicit input_schema/output_schema, or a JSON-valued wrapper.')
