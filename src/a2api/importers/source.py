"""Bounded static source records, directly connected to the HTTP execution IR."""

from __future__ import annotations

from dataclasses import dataclass
import importlib
import json
import os
from pathlib import Path
import re

from ..errors import A2APIError
from ..http_adapter import HTTPRoute, HTTPResponse, HTTPQueryParameter, HTTPHeaderParameter, HTTP_METHODS
from ..ir import Operation, freeze
from ..openapi_schema import check_draft_schema


class Unsupported(ValueError):
    """A source construct has no supported static interpretation."""


def text(node):
    return node.text.decode('utf-8') if node is not None else ''


def walk(node, kind=None):
    pending = [node]
    while pending:
        current = pending.pop()
        if kind is None or current.type == kind:
            yield current
        pending.extend(reversed(current.named_children))


def named(node, name):
    return node.child_by_field_name(name)


def literal(node):
    if node is None:
        raise Unsupported('A literal value is required.')
    value = text(node)
    if node.type == 'raw_string_literal':
        return value[1:-1]
    try:
        return json.loads(value)
    except ValueError:
        raise Unsupported('Dynamic values are outside this source profile.') from None


def object_schema(properties, required=()):
    return {'type': 'object', 'properties': properties, 'required': list(required), 'additionalProperties': False}


def split_types(value):
    result, start, depth = [], 0, 0
    for index, char in enumerate(value):
        depth += char in '<(['
        depth -= char in '>)]'
        if char == ',' and depth == 0:
            result.append(value[start:index].strip()); start = index + 1
    return result + [value[start:].strip()]


def identifier(namespace, operation):
    return namespace + '.' + '.'.join(re.sub('[^a-z0-9_]', '_', part.casefold()) for part in operation.split('.'))


@dataclass(frozen=True)
class SourceRecord:
    operation_id: str
    path: str
    method: str
    id: str
    title: str
    operation: Operation | None
    binding: dict | None
    location: str
    diagnostics: tuple = ()
    version: str = '0.1.0'

    @property
    def status(self):
        return 'imported' if self.operation is not None else 'unsupported'

    def summary(self):
        return {'operationId': self.operation_id, 'path': self.path, 'method': self.method,
                'status': self.status, 'location': self.location, 'diagnostics': list(self.diagnostics)}

    def http_route(self, base_url, *, path_prefix='', headers=None, credential_provider=None):
        binding = self.binding
        if binding is None:
            raise A2APIError('CONVERT_OPERATION_UNSUPPORTED', 'No supported source HTTP binding exists.')
        return HTTPRoute(base_url=base_url, path=path_prefix.rstrip('/') + self.path,
            path_parameters=binding['path'], query_parameters={key: HTTPQueryParameter(**value) for key, value in binding['query'].items()},
            headers=headers or {}, response_envelope='result', method=self.method,
            request_body_pointer=binding.get('body'), request_body_required=binding.get('bodyRequired', False),
            responses={int(key): HTTPResponse(value) for key, value in binding['responses'].items()},
            response_status_field='httpStatus', credential_provider=credential_provider,
            header_parameters={key: HTTPHeaderParameter(**value) for key, value in binding.get('headers', {}).items()})


def record(namespace, opid, path, method, inputs, output, location, *, title=None, statuses=(200,),
           path_bindings=None, query_bindings=None, header_bindings=None, body=False, body_required=True):
    if method not in HTTP_METHODS:
        raise Unsupported('Supported methods are GET, HEAD, POST, PUT, PATCH and DELETE (UPDATE uses PUT/PATCH).')
    if body and method in ('GET', 'HEAD'):
        raise Unsupported('GET/HEAD request bodies are outside the HTTP adapter profile.')
    if not path.startswith('/') or re.search(r'[?#*]', path):
        raise Unsupported('Only explicit origin-relative paths without wildcards are supported.')
    placeholders = set(re.findall(r'\{([^{}]+)\}', path))
    if placeholders != set(path_bindings or {}):
        raise Unsupported('Path placeholders must match explicitly bound parameters.')
    if any(not re.fullmatch('[A-Za-z_][A-Za-z0-9_]*', key) for key in placeholders):
        raise Unsupported('Pattern, greedy and nested path parameters require an explicit wrapper.')
    if not statuses or any(type(code) is not int or not 200 <= code <= 299 for code in statuses):
        raise Unsupported('Declare a finite set of successful HTTP statuses.')
    for group, bindings in [('query', query_bindings or {}), ('headers', header_bindings or {})]:
        for key, binding in bindings.items():
            binding['pointer'] = '/' + group + '/' + key.replace('~', '~0').replace('/', '~1')
            schema = inputs['properties'][group]['properties'][key]
            if schema.get('anyOf') and len(schema['anyOf']) == 2 and schema['anyOf'][1] == {'type': 'null'}:
                schema = schema['anyOf'][0]
                inputs['properties'][group]['properties'][key] = schema
            if schema.get('type') == 'array' and group == 'query':
                schema['minItems'] = max(1, schema.get('minItems', 0))
                scalar = schema.get('items', {})
            else:
                scalar = schema
            if scalar.get('type') not in ('string', 'integer', 'number', 'boolean'):
                raise Unsupported('HTTP form parameters require scalar values or scalar query arrays.')
    if method == 'HEAD':
        output = {'type': 'null'}
    empty = output == {'type': 'null'}
    if any(code in (204, 205) for code in statuses) and not empty:
        raise Unsupported('204/205 require a statically empty response.')
    wire_output = object_schema({'result': output, 'httpStatus': {'type': 'integer', 'enum': list(statuses)}}, ['result', 'httpStatus'])
    for schema in (inputs, wire_output):
        check_draft_schema(schema)
    wire = Operation(opid, namespace, opid, freeze(inputs), freeze(wire_output), method)
    bindings = {'path': path_bindings or {}, 'query': query_bindings or {}, 'headers': header_bindings or {},
                'responses': {code: None if empty else 'application/json' for code in statuses}}
    if body:
        bindings.update(body='/body', bodyRequired=body_required)
    return SourceRecord(opid, path, method, identifier(namespace, opid), title or opid, wire,
                        freeze(bindings), location)


class SourceImporter:
    """Common in-memory inventory; concrete importers never execute project code."""

    language = ''
    extension = ''

    def __init__(self, directory, *, namespace='source'):
        if not re.fullmatch(r'[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)*', namespace):
            raise A2APIError('INVALID_SOURCE', 'Use a lowercase dotted namespace.')
        try:
            from tree_sitter import Language, Parser
            grammar = importlib.import_module('tree_sitter_' + self.language)
        except ImportError:
            raise A2APIError('DEPENDENCY_MISSING', 'Source import requires: pip install "a2api[source]"') from None
        root = Path(directory)
        if not root.is_dir():
            raise A2APIError('INVALID_SOURCE', 'Select an existing source directory.')
        self.namespace, self.units, self.diagnostics = namespace, [], []
        parser = Parser(Language(grammar.language()))
        total, count = 0, 0
        for base, directories, files in os.walk(root, followlinks=False):
            directories[:] = sorted(d for d in directories if not d.startswith('.') and d not in
                                    ('target', 'node_modules', 'vendor', 'artifacts', 'build', 'dist'))
            for filename in sorted(files):
                path = Path(base) / filename
                if path.suffix != self.extension or path.is_symlink():
                    continue
                count += 1
                if path.stat().st_size > 1024 * 1024 or count > 4096:
                    raise A2APIError('SOURCE_LIMIT', 'Source input exceeds file count/size limits.')
                raw = path.read_bytes()
                total += len(raw)
                if total > 32 * 1024 * 1024:
                    raise A2APIError('SOURCE_LIMIT', 'Source input exceeds 32 MiB.')
                try:
                    raw.decode('utf-8')
                except UnicodeDecodeError:
                    raise A2APIError('INVALID_SOURCE', 'Source files must be UTF-8.') from None
                tree = parser.parse(raw)
                location = str(path.relative_to(root))
                if tree.root_node.has_error:
                    self.diagnostics.append({'code': 'SOURCE_PARSE_ERROR', 'location': location})
                    continue
                self.units.append((location, tree.root_node))
        self._records = list(self._extract())
        ids = [item.operation_id for item in self._records]
        if len(ids) != len(set(ids)) or len({item.id for item in self._records}) != len(ids):
            raise A2APIError('DUPLICATE_SOURCE_OPERATION', 'Ambiguous handler IDs; select a smaller source directory.')

    @classmethod
    def from_directory(cls, directory, *, namespace='source'):
        return cls(directory, namespace=namespace)

    def iter_operations(self, operation_ids=None):
        ids = {item.operation_id for item in self._records}
        if operation_ids is not None and not set(operation_ids).issubset(ids):
            raise A2APIError('INVALID_SELECTION', 'Selected source handler is absent or cannot be parsed.', issues=self.diagnostics)
        yield from (item for item in self._records if operation_ids is None or item.operation_id in operation_ids)

    def unsupported(self, opid, path, method, location, reason):
        return SourceRecord(opid, path, method, identifier(self.namespace, opid), opid, None, None, location,
                            ({'code': 'SOURCE_UNSUPPORTED', 'detail': str(reason), 'location': location},))

    def _extract(self):
        raise NotImplementedError
