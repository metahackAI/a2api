"""Host-side function tools over the unchanged a2api call protocol.

No model SDK dependency. One session belongs to one trusted application/context
or one connected MCP client. MCP tools/list is never modified.
"""

from __future__ import annotations

import asyncio
from collections import OrderedDict
from copy import deepcopy
from dataclasses import dataclass
import hashlib
import json
import re

from jsonschema import Draft202012Validator

from .api import dispatch
from .errors import A2APIError
from .ir import ExecutionContext
from .mcp_application import DirectApplications
from .openapi_schema import check_draft_schema
from .protocol import protocol_schema
from .schema import validate_value
from .discovery_metadata import SearchPages
from .tool_description import function_description

TOOL_PROFILE = 'a2api-tools/1.0'
SEARCH_NAME = 'a2api_search'
SEARCH_TOOL = {'type': 'function', 'function': {
    'name': SEARCH_NAME,
    'description': 'Find functions by task keywords. Selected functions become callable in the next model request. '
                   'Use an already available function directly. If moreAvailable is true, request the same query with '
                   'more=true for the next page. Repeating without more reuses the page. Refine the query if no progress.',
    'parameters': {'type': 'object', 'properties': {'query': {'type': 'string', 'maxLength': 1000},
                                                  'more': {'type': 'boolean', 'default': False}},
                   'required': ['query'], 'additionalProperties': False}}}


GROUPS = ('path', 'query', 'headers', 'body')
_WHOLE_BODY = object()
_PLAIN_OBJECT = {'type', 'properties', 'required', 'additionalProperties', 'title', 'description'}
_RESULT_HINTS = {
    'INVALID_INPUT': 'Fix the arguments using issues, then call again.',
    'RESOURCE_NOT_FOUND': 'The target was not found. Check the ID against earlier results; other functions will not change this.',
    'PERMISSION_DENIED': 'Access was denied for this caller. Other functions will not grant access; report it.',
    'UNAUTHENTICATED': 'The caller is not authenticated for this service. Report it; do not retry.',
    'UPSTREAM_CONFLICT': 'The current state does not allow this change. Report the state instead of retrying.',
    'UPSTREAM_VALIDATION_FAILED': 'The service rejected these values. Correct them only if the user gave other values.',
    'UPSTREAM_ERROR': 'The service failed. Do not retry repeatedly; report the failure.',
    'UPSTREAM_UNAVAILABLE': 'The service is unavailable now. Do not call it again for this request; report that it is unavailable.',
    'DEADLINE_EXCEEDED': 'The service did not respond in time. Do not call it again for this request; report the failure.',
    'RATE_LIMITED': 'The service is rate limited. Do not retry now; report it.',
    'OUTCOME_UNKNOWN': 'The change may or may not have been applied. Do not retry; verify with a read if available.',
    'NOT_SELECTED': 'Call only functions currently provided; search if a function is missing.',
    'SCHEMA_MISMATCH': 'The service returned an unexpected result. Report the failure.',
}
_DEFAULT_COMPLETENESS = {'complete': True, 'scope': 'single_api_response'}


def tool_bytes(tools: list[dict]) -> int:
    """Compact UTF-8 JSON bytes, not model tokens or the complete prompt size."""
    return len(json.dumps(tools, ensure_ascii=False, sort_keys=True,
                          separators=(',', ':'), allow_nan=False).encode('utf-8'))


def _local(schema: dict, node):
    """Resolve one sibling-free local $defs reference for presentation only."""
    if isinstance(node, dict) and set(node) == {'$ref'} and isinstance(node['$ref'], str) \
            and node['$ref'].startswith('#/$defs/') and '/' not in node['$ref'][8:]:
        return schema.get('$defs', {}).get(node['$ref'][8:], node)
    return node


def flatten_input(schema: dict):
    """Present an HTTP {path,query,headers,body} input as one flat object when lossless.

    Returns (parameters, layout, required_groups) or None. The wire input is unchanged:
    call() restores the original structure before the normal invoke validation.
    """
    properties = schema.get('properties')
    if (schema.get('type') != 'object' or not isinstance(properties, dict) or not properties
            or set(properties) - set(GROUPS) or schema.get('additionalProperties') is not False
            or set(schema) - _PLAIN_OBJECT - {'$schema', '$defs'}):
        return None
    required = [group for group in GROUPS if group in schema.get('required', [])]
    flat, flat_required, layout = {}, [], {}
    for group in GROUPS:
        if group not in properties:
            continue
        node = _local(schema, properties[group])
        plain = (isinstance(node, dict) and node.get('type') == 'object' and isinstance(node.get('properties'), dict)
                 and node.get('additionalProperties') is False and not set(node) - _PLAIN_OBJECT)
        if not plain:
            if group != 'body' or 'body' in flat:
                return None
            flat['body'], layout['body'] = deepcopy(properties[group]), _WHOLE_BODY
            if group in required:
                flat_required.append('body')
            continue
        inner_required = node.get('required', [])
        if group not in required and inner_required:
            return None  # an optional group with required members has no flat equivalent
        for name, child in node['properties'].items():
            if name in flat:
                return None
            flat[name], layout[name] = deepcopy(child), group
            if name in inner_required:
                flat_required.append(name)
    parameters = {'type': 'object', 'properties': flat, 'required': flat_required, 'additionalProperties': False}
    for key in ('$schema', '$defs'):
        if key in schema:
            parameters[key] = deepcopy(schema[key])
    return parameters, layout, tuple(required)


def model_parameters(schema: dict) -> dict:
    """Model view only: drop $schema and show optional `X | null` (default null) members as X.

    Omitting such a member means the same as sending null, so the view is a strict subset.
    """
    view = {key: value for key, value in schema.items() if key != '$schema'}
    properties = view.get('properties')
    if view.get('type') == 'object' and isinstance(properties, dict):
        required = set(view.get('required', []))
        simplified = {}
        for name, child in properties.items():
            branches = child.get('anyOf') if isinstance(child, dict) else None
            if (name not in required and isinstance(branches, list) and len(branches) == 2
                    and {'type': 'null'} in branches and set(child) <= {'anyOf', 'default'}
                    and child.get('default', None) is None):
                child = deepcopy(branches[0] if branches[1] == {'type': 'null'} else branches[1])
            simplified[name] = child
        view['properties'] = simplified
    return view


def _restore(arguments: dict, layout: dict, required_groups: tuple) -> dict:
    result = {group: {} for group in required_groups}
    for name, value in arguments.items():
        group = layout[name]
        if group is _WHOLE_BODY:
            result['body'] = value
        else:
            result.setdefault(group, {})[name] = value
    return result


def render_result(payload: dict) -> str:
    """Compact model-facing text for a call()/search result; the envelope stays available to hosts."""
    if not isinstance(payload, dict):
        raise TypeError('render_result expects a call() or search result.')
    if 'selected' in payload:
        view = {key: value for key, value in payload.items() if value not in ([], None)}
    elif payload.get('status') == 'succeeded':
        view = {'status': 'succeeded', 'data': payload.get('data')}
        if payload.get('httpStatus') not in (None, 200):
            view['httpStatus'] = payload['httpStatus']
        if payload.get('completeness') not in (None, _DEFAULT_COMPLETENESS):
            view['completeness'] = payload['completeness']
    else:
        problem = payload.get('error', {})
        error = {'code': problem.get('code'), 'detail': problem.get('detail')}
        if problem.get('issues'):
            error['issues'] = problem['issues']
        view = {'status': 'failed', 'error': error}
        if problem.get('code') in _RESULT_HINTS:
            view['hint'] = _RESULT_HINTS[problem['code']]
    return json.dumps(view, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


@dataclass(frozen=True)
class _Bound:
    descriptor: dict
    tool: dict
    layout: dict | None = None
    required_groups: tuple = ()
    textual: frozenset = frozenset()


def _textual(parameters: dict, layout: dict | None) -> frozenset:
    """Flat members sent as URL/header text whose declared type is exactly string."""
    if layout is None:
        return frozenset()
    return frozenset(name for name, group in layout.items() if group in ('path', 'query', 'headers')
                     and parameters['properties'].get(name, {}).get('type') == 'string')


def _as_text(arguments: dict, textual: frozenset) -> dict:
    """HTTP path/query/header values are text on the wire: send JSON numbers/booleans as their text form."""
    return {name: (json.dumps(value) if name in textual and type(value) in (int, float, bool) else value)
            for name, value in arguments.items()}


class ToolSession:
    """Select exact business input schemas, then forward calls to normal invoke.

    tools() is a fresh Chat Completions-shaped host view. Call tools() again for
    each model request. select()/call() are async, serialized within this session.
    Never share a session across clients, users, tenants, or authorization changes.
    """

    profile = TOOL_PROFILE

    def __init__(self, apps, context: ExecutionContext, *, max_tool_bytes=16000, search_limit=5,
                 naming='readable', flatten=True, hints='none'):
        if not isinstance(context, ExecutionContext):
            raise TypeError('A trusted ExecutionContext is required.')
        runtime = DirectApplications(apps)

        async def request(method, arguments):
            return await asyncio.to_thread(dispatch, runtime, method, arguments, context)

        self._initialize(request, max_tool_bytes, search_limit, naming, flatten, hints)

    def _initialize(self, request, budget, limit, naming='readable', flatten=True, hints='none'):
        if type(budget) is not int or budget < tool_bytes([SEARCH_TOOL]):
            raise ValueError('max_tool_bytes must fit the complete search tool.')
        if type(limit) is not int or not 1 <= limit <= 20:
            raise ValueError('search_limit must be an integer from 1 to 20.')
        if naming not in ('readable', 'hash') or not isinstance(flatten, bool) or hints not in ('none', 'shape', 'typed'):
            raise ValueError('naming must be readable or hash, flatten a boolean, hints none, shape or typed.')
        self._request_impl = request
        self.max_tool_bytes = budget
        self.search_limit = limit
        self.naming = naming
        self.flatten = flatten
        self.hints = hints
        self._catalog = None
        self._active: OrderedDict[str, _Bound] = OrderedDict()
        self._names: dict[str, str] = {}
        self._strategy = None
        self._lock = asyncio.Lock()
        self._pages = SearchPages()
        self._stats = {'discover': 0, 'describe': 0, 'invoke': 0, 'reused': 0, 'evicted': 0}

    @classmethod
    async def from_mcp(cls, client, *, max_tool_bytes=16000, search_limit=5, naming='readable', flatten=True, hints='none'):
        """Use an already connected, trusted MCP client; no connection is owned."""
        listing = await client.list_tools()
        expected = {'a2api.discover', 'a2api.describe', 'a2api.invoke'}
        if {tool.name for tool in listing.tools} != expected or len(listing.tools) != 3:
            raise ValueError('Connect an a2api MCP server exposing discover/describe/invoke.')

        async def request(method, arguments):
            result = await client.call_tool('a2api.' + method, arguments)
            return result.structured_content

        session = cls.__new__(cls)
        session._initialize(request, max_tool_bytes, search_limit, naming, flatten, hints)
        return session

    @property
    def stats(self):
        return dict(self._stats)

    @property
    def strategy(self):
        """'all' or 'search' after auto(); None when the host selects explicitly."""
        return self._strategy

    def tools(self, *, include_search=None):
        """Fresh model view. include_search=None omits search only after auto() chose 'all'."""
        if include_search is None:
            include_search = self._strategy != 'all'
        return deepcopy([*([SEARCH_TOOL] if include_search else []),
                         *(bound.tool for bound in self._active.values())])

    render = staticmethod(render_result)

    def binding(self, name):
        """Host audit reference; do not add these fields to model arguments."""
        bound = self._active.get(name)
        if bound is None:
            return None
        return {'id': bound.descriptor['id'], 'version': bound.descriptor['version'],
                'catalogVersion': self._catalog}

    async def _request(self, method, arguments):
        self._stats[method] += 1
        payload = await self._request_impl(method, arguments)
        validate_value(protocol_schema(method + '_response'), payload, code='SCHEMA_MISMATCH', status=502)
        if 'error' in payload and 'status' not in payload:
            problem = payload['error']
            raise A2APIError(problem['code'], problem['detail'], status=problem['status'],
                             issues=problem.get('issues'))
        return payload

    def _adopt_catalog(self, catalog):
        if self._catalog != catalog:
            self._active.clear()
            self._names.clear()
            self._pages.clear()
            self._catalog = catalog

    def _clear(self):
        self._active.clear()
        self._names.clear()
        self._catalog = None
        self._pages.clear()

    def _name(self, item) -> str:
        token = json.dumps([self._catalog, item['id'], item['version']], separators=(',', ':'))
        if token in self._names:
            return self._names[token]
        digest = hashlib.sha256(token.encode()).hexdigest()
        if self.naming == 'hash':
            name = 'a2api_call_' + digest[:24]
        else:
            name = re.sub(r'[^A-Za-z0-9_]+', '_', item['id']).strip('_')[:48] or 'call'
            if not name[0].isalpha():
                name = 'f_' + name[:46]
            if name == SEARCH_NAME or name in self._names.values():
                name = name[:39] + '_' + digest[:8]
        self._names[token] = name
        return name

    async def _bind(self, item, name) -> _Bound:
        described = await self._request('describe', {'id': item['id'], 'version': item['version']})
        if described['catalogVersion'] != self._catalog:
            self._clear()
            raise A2APIError('CONTRACT_DRIFT', 'Catalog changed during selection; search again.', status=409)
        descriptor = described['capability']
        validate_value(protocol_schema('descriptor'), descriptor, code='SCHEMA_MISMATCH', status=502)
        if (descriptor['id'], descriptor['version']) != (item['id'], item['version']):
            raise A2APIError('SCHEMA_MISMATCH', 'Describe returned a different capability.', status=502)
        for schema in (descriptor['inputSchema'], descriptor['outputSchema']):
            check_draft_schema(schema)
        flat = flatten_input(descriptor['inputSchema']) if self.flatten else None
        parameters = flat[0] if flat else deepcopy(descriptor['inputSchema'])
        if self.hints != 'typed':  # 0.4+ model view; hints='typed' keeps the 0.3 descriptions and parameters
            parameters = model_parameters(parameters)
        tool = {'type': 'function', 'function': {'name': name,
            'description': function_description(descriptor, self.hints), 'parameters': parameters}}
        layout = flat[1] if flat else None
        return _Bound(deepcopy(descriptor), tool, layout, flat[2] if flat else (), _textual(parameters, layout))

    async def _select(self, query, *, exact=False, more=False, limit=None):
        prepared = self._pages.prepare(query, more, limit=limit or self.search_limit, restart=exact)
        try:
            found = await self._request('discover', prepared['arguments'])
        except A2APIError as error:
            if prepared['arguments'].get('cursor') is not None and error.code in ('INVALID_CURSOR', 'CONTRACT_DRIFT'):
                self._clear()
                raise A2APIError('CONTRACT_DRIFT', 'Search view changed; start a new search.', status=409) from None
            raise
        if prepared['arguments'].get('cursor') is not None and prepared['catalog'] != found['catalogVersion']:
            self._clear()
            raise A2APIError('CONTRACT_DRIFT', 'Search catalog changed; start a new search.', status=409)
        self._adopt_catalog(found['catalogVersion'])
        entries = found['capabilities']
        if exact:
            entries = [item for item in entries if item['id'] == query]
            if len(entries) != 1 or found['nextCursor']:
                # Do not silently choose a version or claim a partially searched ID is unique.
                raise A2APIError('AMBIGUOUS_SELECTION' if entries else 'NOT_FOUND',
                                 'Prime requires one uniquely discoverable capability ID; use select for task search.')
        selected, omitted, evicted = [], [], []
        protected = set()
        for item in entries:
            name = self._name(item)
            if name in self._active:
                bound = self._active[name]
                self._stats['reused'] += 1
            else:
                bound = await self._bind(item, name)
            retained = OrderedDict(self._active)
            retained.pop(name, None)
            retained[name] = bound
            removed = []
            while tool_bytes([SEARCH_TOOL, *(entry.tool for entry in retained.values())]) > self.max_tool_bytes:
                victim = next((key for key in retained if key != name and key not in protected), None)
                if victim is None:
                    break
                retained.pop(victim)
                removed.append(victim)
            if tool_bytes([SEARCH_TOOL, *(entry.tool for entry in retained.values())]) > self.max_tool_bytes:
                omitted.append({'id': item['id'], 'reason': 'SCHEMA_BUDGET'})
                continue
            self._active = retained
            self._stats['evicted'] += len(removed)
            evicted.extend(removed)
            protected.add(name)
            selected.append({'name': name, 'id': item['id']})
        page = self._pages.commit(prepared, found)
        return {'selected': selected, 'omitted': omitted, 'evicted': evicted, **page}

    async def select(self, query: str, *, more=False):
        """A host search: discover + descriptions without an intervening model turn."""
        async with self._lock:
            validate_value(SEARCH_TOOL['function']['parameters'], {'query': query, 'more': more}, code='INVALID_INPUT', status=400)
            return await self._select(query, more=more)

    async def prime(self, identifiers: list[str]):
        """Host-known IDs become callable before the first model request.

        Raises if any ID is ambiguous, missing or the complete set cannot fit.
        Priming never executes a business API.
        """
        async with self._lock:
            if not isinstance(identifiers, list) or any(not isinstance(item, str) or not item for item in identifiers):
                raise ValueError('prime requires a list of nonempty capability IDs.')
            for identifier in identifiers:
                await self._select(identifier, exact=True)
            active = {bound.descriptor['id'] for bound in self._active.values()}
            if not set(identifiers) <= active:
                raise A2APIError('SCHEMA_BUDGET', 'The requested known function set does not fit max_tool_bytes.')

    async def auto(self, question: str = '', *, max_functions: int = 64, preselect: int = 8, all_bytes: int = 6000):
        """Host strategy without a model turn.

        A catalog whose complete function set fits `all_bytes` (and max_functions and
        max_tool_bytes) is exposed whole: it costs about as much as a pre-selected set and
        never needs a search. Otherwise the host pre-searches the user's question for up to
        `preselect` candidates and keeps the search tool. Never executes a business API.
        """
        if (not isinstance(question, str) or type(max_functions) is not int or not 1 <= max_functions <= 512
                or type(preselect) is not int or not 1 <= preselect <= 20 or type(all_bytes) is not int or all_bytes < 0):
            raise ValueError('auto requires a question string, max_functions 1-512, preselect 1-20 and all_bytes >= 0.')
        async with self._lock:
            entries, cursor, catalog = [], None, None
            while True:
                found = await self._request('discover', {'query': '', 'limit': 50, **({'cursor': cursor} if cursor else {})})
                if catalog is not None and found['catalogVersion'] != catalog:
                    self._clear()
                    raise A2APIError('CONTRACT_DRIFT', 'Catalog changed while listing; call auto again.', status=409)
                catalog = found['catalogVersion']
                entries.extend(found['capabilities'])
                cursor = found['nextCursor']
                if cursor is None or len(entries) > max_functions:
                    break
            self._adopt_catalog(catalog)
            if cursor is None and len(entries) <= max_functions:
                bound = OrderedDict()
                for item in entries:
                    name = self._name(item)
                    bound[name] = self._active.get(name) or await self._bind(item, name)
                if tool_bytes([entry.tool for entry in bound.values()]) <= min(self.max_tool_bytes, all_bytes):
                    self._active = bound
                    self._strategy = 'all'
                    return {'strategy': 'all', 'functions': len(bound)}
            self._strategy = 'search'
            query = ' '.join(question.split())[:1000]
            preselected = await self._select(query, limit=preselect) if query else None
            return {'strategy': 'search', 'functions': len(self._active), 'preselected': preselected}

    async def call(self, name: str, arguments: dict):
        """Return search results or the original validated invoke envelope; no retry."""
        async with self._lock:
            try:
                try:
                    json.dumps(arguments, allow_nan=False)
                except (TypeError, ValueError, RecursionError):
                    raise A2APIError('INVALID_INPUT', 'Arguments must be finite JSON.') from None
                if name == SEARCH_NAME:
                    validate_value(SEARCH_TOOL['function']['parameters'], arguments, code='INVALID_INPUT', status=400)
                    return await self._select(arguments['query'], more=arguments.get('more', False))
                bound = self._active.get(name)
                if bound is None:
                    raise A2APIError('NOT_SELECTED', 'Function is not active in this session; search again.')
                if bound.layout is None:
                    validate_value(bound.descriptor['inputSchema'], arguments, code='INVALID_INPUT', status=400)
                else:
                    try:
                        arguments = _as_text(arguments, bound.textual)
                        validate_value(bound.tool['function']['parameters'], arguments, code='INVALID_INPUT', status=400)
                        arguments = _restore(arguments, bound.layout, bound.required_groups)
                    except A2APIError:
                        # Hosts may still send the original wire shape; the model sees the flat view.
                        if not Draft202012Validator(bound.descriptor['inputSchema']).is_valid(arguments):
                            raise
                    validate_value(bound.descriptor['inputSchema'], arguments, code='INVALID_INPUT', status=400)
                self._active.move_to_end(name)
                result = await self._request('invoke', {'id': bound.descriptor['id'],
                    'version': bound.descriptor['version'], 'catalogVersion': self._catalog, 'input': arguments})
                if result.get('status') == 'succeeded':
                    validate_value(bound.descriptor['outputSchema'], result.get('data'),
                                   code='SCHEMA_MISMATCH', status=502)
                if result.get('error', {}).get('code') == 'CONTRACT_DRIFT':
                    self._clear()
                return result
            except A2APIError as error:
                if error.code == 'CONTRACT_DRIFT':
                    self._clear()
                return {'error': error.problem()}
            except Exception:
                return {'error': A2APIError('HOST_PROTOCOL_ERROR',
                    'The host could not complete this call; no automatic retry was made.', status=502).problem()}
