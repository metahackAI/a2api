"""In-memory HTTP contract conversion with explicitly selected read/write effects."""

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
from .importers.source import SourceImporter, SourceRecord
from .ir import ExecutionContext, Operation, freeze, thaw
from .openapi_schema import check_draft_schema, schema_nodes
from .pointers import resolve, tokens
from .review_projection import ANNOTATIONS
from .reviewed_adapter import HTTPDeployment
from .schema import validate_value
from .protocol import PROTOCOL_PROFILE
from .discovery_metadata import search_keywords, summary_override

CALL_PROFILE = PROTOCOL_PROFILE


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


_ITEMS = '[]'


def _select_tree(selected: tuple[str, ...]) -> dict:
    """Parse field paths such as name, owner.login, items[].id or [].login into a tree."""
    tree: dict = {}
    for path in selected:
        steps = []
        for index, part in enumerate(path.split('.')):
            name = part
            arrays = 0
            while name.endswith('[]'):
                name, arrays = name[:-2], arrays + 1
            if ('[' in name or ']' in name or (not name and (index or not arrays))):
                raise A2APIError('INVALID_SELECTION', 'select paths use field names joined by "." with optional "[]" for array items.')
            steps += ([name] if name else []) + [_ITEMS] * arrays
        node = tree
        for step in steps[:-1]:
            node = node.setdefault(step, {})
            if node is True:
                raise A2APIError('INVALID_SELECTION', 'select paths must not overlap.')
        if steps[-1] in node:
            raise A2APIError('INVALID_SELECTION', 'select paths must not overlap.')
        node[steps[-1]] = True
    return tree


def _nullable_branch(node):
    """Return X for a sibling-free {"anyOf": [X, {"type": "null"}]} wrapper, else None."""
    if not isinstance(node, dict) or set(node) - ANNOTATIONS - {key for key in node if key.startswith('x-')} != {'anyOf'}:
        return None
    branches = node['anyOf']
    if not isinstance(branches, list) or len(branches) != 2 or {'type': 'null'} not in branches:
        return None
    other = branches[0] if branches[1] == {'type': 'null'} else branches[1]
    return other if other != {'type': 'null'} else None


def _plain(node, root: dict, kind: str):
    """Follow finite local references to a plain object/array node without validation siblings."""
    seen = set()
    nullable = False
    for _ in range(64):
        branch = _nullable_branch(node)
        if branch is not None:
            node, nullable = branch, True
            continue
        if not (isinstance(node, dict) and '$ref' in node):
            break
        ref = node['$ref']
        annotations = ANNOTATIONS | {key for key in node if key.startswith('x-')}
        if (not isinstance(ref, str) or not ref.startswith('#/$defs/') or ref in seen
                or set(node) - annotations - {'$ref'}):
            raise A2APIError('UNSUPPORTED_SELECTION', 'select requires finite local references without validation siblings.')
        seen.add(ref)
        node = resolve(root, ref[1:])
    allowed = ({'type', 'properties', 'required', 'additionalProperties'} if kind == 'object'
               else {'type', 'items', 'minItems', 'maxItems'})
    declared = node.get('type') if isinstance(node, dict) else None
    kinds = {declared} if isinstance(declared, str) else set(declared) if isinstance(declared, list) else set()
    if (not isinstance(node, dict) or kind not in kinds or not kinds <= {kind, 'null'}
            or set(node) - allowed - ANNOTATIONS - {key for key in node if key.startswith('x-')}):
        raise A2APIError('UNSUPPORTED_SELECTION', 'select paths may traverse only plain objects, arrays and local object references.')
    if kind == 'array' and not isinstance(node.get('items'), dict):
        raise A2APIError('UNSUPPORTED_SELECTION', 'Selected arrays must declare one item schema.')
    return node, ([kind, 'null'] if 'null' in kinds or nullable else kind)


def _project_schema(node, tree, root: dict):
    if tree is True:
        return copy.deepcopy(node)
    if _ITEMS in tree:
        if len(tree) != 1:
            raise A2APIError('INVALID_SELECTION', 'Select either array items or object fields at one level.')
        plain, kind = _plain(node, root, 'array')
        result = {key: plain[key] for key in ('minItems', 'maxItems') if key in plain}
        return {'type': kind, 'items': _project_schema(plain['items'], tree[_ITEMS], root), **result}
    plain, kind = _plain(node, root, 'object')
    properties = plain.get('properties', {})
    if any(name not in properties for name in tree):
        raise A2APIError('INVALID_SELECTION', 'select names must be declared response fields.')
    return {'type': kind, 'properties': {name: _project_schema(properties[name], child, root) for name, child in tree.items()},
            'required': [name for name in tree if name in plain.get('required', [])], 'additionalProperties': False}


def _project(value, tree):
    """Apply a validated selection; raw validation already ran and public validation follows."""
    if tree is True or value is None:
        return value
    if _ITEMS in tree:
        return [_project(item, tree[_ITEMS]) for item in value] if isinstance(value, list) else value
    if not isinstance(value, dict):
        return value
    return {name: _project(value[name], child) for name, child in tree.items() if name in value}


def _output_schema(wire: Operation, selected: tuple[str, ...] | None) -> dict:
    root = thaw(wire.output_schema)
    node = root['properties']['result']
    if selected is not None:
        node = _project_schema(node, _select_tree(selected), root)
    return _bundle(node, root)


@dataclass(frozen=True)
class _Call:
    descriptor_json: str
    wire: Operation
    output_schema: Mapping
    selected: tuple[str, ...] | None
    search_terms: tuple[str, ...] = ()
    keywords: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()


@dataclass(frozen=True)
class ConvertedAPI:
    """A host-selected HTTP application. No review/build files or registry needed."""

    _calls: Mapping[str, _Call] = field(repr=False)
    _adapter: HTTPAdapter = field(repr=False)
    _timeout_ms: int = 1500
    _deadline_ms: int = 5000

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

    def search_metadata(self, *, structured=False):
        """Host-only index terms; never added to the public descriptor."""
        if structured:
            return {identifier: {'terms': call.search_terms, 'keywords': call.keywords, 'aliases': call.aliases}
                    for identifier, call in self._calls.items()}
        return {identifier: call.search_terms for identifier, call in self._calls.items()}

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
            raw = self._adapter.call(call.wire, arguments, context, Budget(self._deadline_ms, 1), self._timeout_ms)
            data = raw['result']
            if call.selected is not None:
                data = _project(data, _select_tree(call.selected))
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


def convert(source, *, operations: Mapping[str, Mapping], deployment: HTTPDeployment) -> ConvertedAPI:
    """Bind selected source/OpenAPI operations without activating imported drafts.

    operations maps IDs to effect, optional select, summary and search keywords.
    Omit select to expose the original JSON response. It never implies authorization.
    """
    if not isinstance(source, (OpenAPIImporter, SourceImporter)) or not isinstance(deployment, HTTPDeployment):
        raise A2APIError('INVALID_CONVERSION', 'convert requires a supported importer and an explicit HTTPDeployment.')
    if not isinstance(operations, Mapping) or not operations:
        raise A2APIError('INVALID_SELECTION', 'Select one or more operation IDs with explicit effect settings.')
    settings = {}
    for identifier, options in operations.items():
        if (not isinstance(identifier, str) or not identifier or not isinstance(options, Mapping)
                or set(options) - {'effect', 'select', 'summary', 'keywords'} or options.get('effect') not in ('read', 'write')):
            raise A2APIError('INVALID_CONVERSION', 'Each operation must explicitly declare effect=read or write and only supported options.')
        selected = options.get('select')
        if 'select' in options and (not isinstance(selected, list) or not selected
                or any(not isinstance(name, str) or not name for name in selected) or len(set(selected)) != len(selected)):
            raise A2APIError('INVALID_SELECTION', 'select must be a nonempty list of unique field paths.')
        summary = summary_override(options['summary']) if 'summary' in options else None
        keywords = search_keywords(options.get('keywords'))
        settings[identifier] = (tuple(selected) if selected is not None else None, options['effect'], summary, keywords)
    calls, routes = {}, {}
    for record in source.iter_operations(set(settings)):
        if record.status != 'imported' or (record.operation if isinstance(record, SourceRecord) else record.capability) is None:
            raise A2APIError('CONVERT_OPERATION_UNSUPPORTED', 'A selected operation is unavailable for conversion.',
                             issues=[{'operationId': record.operation_id, 'status': record.status,
                                      'diagnostics': thaw(record.diagnostics)}])
        wire = record.operation if isinstance(record, SourceRecord) else record.capability.operations[record.operation_id]
        selected, effect, summary, keywords = settings[record.operation_id]
        if (wire.http_method in ('PUT', 'PATCH', 'DELETE') and effect != 'write'
                or wire.http_method in ('GET', 'HEAD') and effect != 'read'):
            raise A2APIError('INVALID_CONVERSION', 'GET/HEAD require read; PUT/PATCH/DELETE require write. POST needs an explicit read/write effect.')
        public_output = _output_schema(wire, selected)
        public_input = thaw(wire.input_schema)
        check_draft_schema(public_input)
        source_summary = record.title if isinstance(record, SourceRecord) else record.capability.title
        source_terms = (source_summary,)
        if not isinstance(record, SourceRecord):
            imported = record.capability.describe()
            source_terms += (imported['intent']['summary'],)
            tags = imported['provenance']['source'].get('tags', [])
            if isinstance(tags, list):
                source_terms += tuple(tag for tag in tags if isinstance(tag, str))
        descriptor = {'id': record.id if isinstance(record, SourceRecord) else record.capability.id,
                      'version': record.version if isinstance(record, SourceRecord) else record.capability.version,
                      'summary': summary if summary is not None else source_summary, 'effects': {'kind': effect},
                      'inputSchema': public_input, 'outputSchema': public_output}
        route = record.http_route(deployment.base_url, path_prefix=deployment.path_prefix,
                                  headers=dict(deployment.headers), credential_provider=deployment.credential_provider)
        routes[(wire.service_ref, wire.operation_ref)] = route
        calls[descriptor['id']] = _Call(json.dumps(descriptor, ensure_ascii=False, allow_nan=False), wire,
                                       freeze(public_output), selected, tuple(dict.fromkeys((*keywords, *source_terms))),
                                       keywords, (record.operation_id,))
    return ConvertedAPI(MappingProxyType(calls), HTTPAdapter(routes, max_response_bytes=deployment.max_response_bytes),
                        deployment.timeout_ms, deployment.deadline_ms)
