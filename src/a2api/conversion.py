"""In-memory OpenAPI conversion and single-call GET/HEAD execution."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
import json
from types import MappingProxyType
from typing import Mapping

from .errors import A2APIError
from .execution import Budget
from .http_adapter import HTTPAdapter
from .importers import OpenAPIImporter
from .ir import ExecutionContext, Operation, freeze, thaw
from .openapi_schema import check_draft_schema, schema_nodes
from .pointers import tokens
from .review_projection import ANNOTATIONS, dereference
from .reviewed_adapter import HTTPDeployment
from .schema import validate_value

CALL_PROFILE = 'a2api-call/0.1'


def _bundle(node, root: dict) -> dict:
    """Keep local reference scope and only definitions reachable from this view."""
    result = copy.deepcopy(node) if isinstance(node, dict) and '$defs' not in node else {'allOf': [copy.deepcopy(node)]}
    definitions = root.get('$defs', {})
    needed, pending = set(), [result]
    while pending:
        current = pending.pop()
        for _, child in schema_nodes(current):
            if '$ref' not in child:
                continue
            path = tokens(child['$ref'][1:])
            if len(path) < 2 or path[0] != '$defs' or path[1] not in definitions:
                raise A2APIError('UNSUPPORTED_CONVERSION', 'Public schemas require resolved bundled local references.')
            name = path[1]
            if name not in needed:
                needed.add(name)
                pending.append(definitions[name])
    if needed:
        result['$defs'] = {name: copy.deepcopy(definitions[name]) for name in sorted(needed)}
    result['$schema'] = 'https://json-schema.org/draft/2020-12/schema'
    check_draft_schema(result)
    return result


def _output_schema(wire: Operation, selected: tuple[str, ...] | None) -> dict:
    root = thaw(wire.output_schema)
    node = root['properties']['result']
    if selected is not None:
        node = dereference(root, node)
        allowed = {'type', 'properties', 'required', 'additionalProperties'} | ANNOTATIONS
        if node.get('type') != 'object' or set(node) - allowed:
            raise A2APIError('UNSUPPORTED_SELECTION', 'select requires a plain object response or a plain local object reference.')
        if any(name not in node.get('properties', {}) for name in selected):
            raise A2APIError('INVALID_SELECTION', 'select names must be declared top-level response fields.')
        node = {'type': 'object', 'properties': {name: node['properties'][name] for name in selected},
                'required': [name for name in selected if name in node.get('required', [])], 'additionalProperties': False}
    return _bundle(node, root)


@dataclass(frozen=True)
class _Call:
    descriptor_json: str
    wire: Operation
    output_schema: Mapping
    selected: tuple[str, ...] | None


@dataclass(frozen=True)
class ConvertedAPI:
    """A bound read-only application. No review/build files or registry needed."""

    _calls: Mapping[str, _Call] = field(repr=False)
    _adapter: HTTPAdapter = field(repr=False)

    @property
    def profile(self) -> str:
        return CALL_PROFILE

    def _get(self, capability_id: str) -> _Call:
        if not isinstance(capability_id, str) or capability_id not in self._calls:
            raise A2APIError('NOT_FOUND', 'This application does not expose the requested capability.', status=404)
        return self._calls[capability_id]

    def describe(self, capability_id: str) -> dict:
        return json.loads(self._get(capability_id).descriptor_json)

    def descriptors(self) -> tuple[dict, ...]:
        """Host-side catalog snapshot; not the MCP tools/list payload."""
        return tuple(self.describe(identifier) for identifier in self._calls)

    def invoke(self, capability_id: str, input: dict, *, context: ExecutionContext) -> dict:
        """Return a compact success/error envelope; never automatically retry."""
        try:
            call = self._get(capability_id)
            if not isinstance(context, ExecutionContext):
                raise A2APIError('UNAUTHENTICATED', 'A trusted host ExecutionContext is required.', status=401)
            if not isinstance(input, dict):
                raise A2APIError('INVALID_INPUT', 'Business input must be a JSON object.', status=422)
            try:
                arguments = json.loads(json.dumps(input, ensure_ascii=False, allow_nan=False).encode('utf-8'))
            except (ValueError, TypeError, UnicodeError, RecursionError):
                raise A2APIError('INVALID_INPUT', 'Business input must contain finite UTF-8 JSON values.', status=422) from None
            raw = self._adapter.call(call.wire, arguments, context, Budget(5000, 1), 1500)
            data = raw['result']
            if call.selected is not None:
                data = {name: data[name] for name in call.selected if name in data}
            validate_value(call.output_schema, data, code='SCHEMA_MISMATCH', status=502)
            result = {'status': 'succeeded', 'data': data,
                      'completeness': {'complete': True, 'scope': 'single_api_response'}}
            if 'httpStatus' in raw:
                result['httpStatus'] = raw['httpStatus']
            return result
        except A2APIError as error:
            return {'status': 'failed', 'error': error.problem(), 'completeness': {'complete': False}}
        except RecursionError:
            return {'status': 'failed', 'error': A2APIError('SCHEMA_EVALUATION_FAILED',
                    'Schema evaluation exceeded the supported depth.', status=422).problem(),
                    'completeness': {'complete': False}}


def convert(source: OpenAPIImporter, *, operations: Mapping[str, Mapping], deployment: HTTPDeployment) -> ConvertedAPI:
    """Bind explicitly selected read operations in memory, without activating drafts.

    operations maps source operationId to {"effect": "read", "select": [fields]}.
    Omit select to expose the original JSON response. It never implies authorization.
    """
    if not isinstance(source, OpenAPIImporter) or not isinstance(deployment, HTTPDeployment):
        raise A2APIError('INVALID_CONVERSION', 'convert requires an OpenAPIImporter and an explicit HTTPDeployment.')
    if not isinstance(operations, Mapping) or not operations:
        raise A2APIError('INVALID_SELECTION', 'Select one or more operation IDs with read effect settings.')
    settings = {}
    for identifier, options in operations.items():
        if (not isinstance(identifier, str) or not identifier or not isinstance(options, Mapping)
                or set(options) - {'effect', 'select'} or options.get('effect') != 'read'):
            raise A2APIError('INVALID_CONVERSION', 'Each operation must explicitly declare effect=read and only supported options.')
        selected = options.get('select')
        if 'select' in options and (not isinstance(selected, list) or not selected
                or any(not isinstance(name, str) or not name for name in selected) or len(set(selected)) != len(selected)):
            raise A2APIError('INVALID_SELECTION', 'select must be a nonempty list of unique top-level field names.')
        settings[identifier] = tuple(selected) if selected is not None else None
    calls, routes = {}, {}
    for record in source.iter_operations(set(settings)):
        if record.method.upper() not in {'GET', 'HEAD'}:
            raise A2APIError('CONVERT_METHOD_UNSUPPORTED', 'Direct conversion executes GET/HEAD operations only.',
                             issues=[{'operationId': record.operation_id, 'method': record.method.upper()}])
        if record.status != 'imported' or record.capability is None:
            raise A2APIError('CONVERT_OPERATION_UNSUPPORTED', 'A selected operation is unavailable for conversion.',
                             issues=[{'operationId': record.operation_id, 'status': record.status,
                                      'diagnostics': thaw(record.diagnostics)}])
        wire = record.capability.operations[record.operation_id]
        selected = settings[record.operation_id]
        public_output = _output_schema(wire, selected)
        public_input = thaw(wire.input_schema)
        check_draft_schema(public_input)
        descriptor = {'id': record.capability.id, 'version': record.capability.version,
                      'summary': record.capability.title, 'effects': {'kind': 'read'},
                      'inputSchema': public_input, 'outputSchema': public_output}
        route = record.http_route(deployment.base_url, path_prefix=deployment.path_prefix,
                                  headers=dict(deployment.headers), credential_provider=deployment.credential_provider)
        routes[(wire.service_ref, wire.operation_ref)] = route
        calls[descriptor['id']] = _Call(json.dumps(descriptor, ensure_ascii=False, allow_nan=False), wire,
                                       freeze(public_output), selected)
    return ConvertedAPI(MappingProxyType(calls), HTTPAdapter(routes))
