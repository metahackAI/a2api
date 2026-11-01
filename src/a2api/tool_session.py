"""Host-side function tools over the unchanged a2api call protocol.

No model SDK dependency. One session belongs to one trusted application/context
or one connected MCP client. MCP tools/list is never modified.
"""

from __future__ import annotations

import asyncio
from collections import OrderedDict
from copy import deepcopy
from dataclasses import dataclass, field
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
LOAD_NAME = 'a2api_load'
LOAD_TOOL = {'type': 'function', 'function': {
    'name': LOAD_NAME,
    'description': 'Make functions from the function index callable; their parameters are provided in the next model '
                   'request. Load every function you plan to use in one call, by its name in the index.',
    'parameters': {'type': 'object', 'properties': {'names': {'type': 'array', 'minItems': 1, 'maxItems': 10,
                                                             'items': {'type': 'string', 'maxLength': 128}}},
                   'required': ['names'], 'additionalProperties': False}}}
BATCH_NAME = 'a2api_batch'
BATCH_TOOL = {'type': 'function', 'function': {
    'name': BATCH_NAME,
    'description': 'Make several function calls in one step when none needs the result of another, for example one '
                   'call per item of a list. Each call is checked and run like a direct call; the results come back '
                   'in the same order. Use functions from your tool list.',
    'parameters': {'type': 'object', 'properties': {'calls': {'type': 'array', 'minItems': 1, 'maxItems': 20, 'items': {
        'type': 'object', 'properties': {'name': {'type': 'string', 'maxLength': 128}, 'arguments': {'type': 'object'}},
        'required': ['name', 'arguments'], 'additionalProperties': False}}},
                   'required': ['calls'], 'additionalProperties': False}}}
INDEX_HEAD = ('Function index (every function of this service). Load the ones you need with a2api_load, then call '
              'them. Calls that do not depend on each other (such as one call per item of a list) can be made '
              'together in one step. If a function you expect is not listed where you looked, load the closest '
              'name: unknown names come back with suggestions. If no function fits the request, say so instead '
              'of guessing.')
INDEX_WRITES = ' [write] marks a function that changes data.'


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
    'SEARCH_LIMIT': 'Searching again will not find more. Use the functions you have, or tell the user what is missing.',
    'NOT_LOADED': 'Its parameters are in your tool list now; call it again with them.',
    'UNKNOWN_FUNCTION': 'Use a name from the function index, or tell the user what is missing.',
}
# Names of ID inputs/outputs that link functions (order_id, orderId, order_ids); a bare `id` is ambiguous.
_ID_NAME = re.compile(r'[a-z][a-z0-9]*(?:_[a-z0-9]+)*_ids?|[a-z][a-zA-Z0-9]*Ids?')
_DEFAULT_COMPLETENESS = {'complete': True, 'scope': 'single_api_response'}
NO_NEW_MATCHES = ('No new functions: every match was already offered in this conversation. If they cannot answer, '
                  'tell the user what is missing instead of searching again.')


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


def _dumps(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def _arrays(value, path=''):
    """(serialized size, path, list) for every array with more than one item."""
    if isinstance(value, list):
        if len(value) > 1:
            yield len(_dumps(value)), path, value
        for index, item in enumerate(value):
            yield from _arrays(item, f'{path}[{index}]')
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from _arrays(item, f'{path}.{key}' if path else key)


def _strings(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, str):
                yield len(item), value, key
            else:
                yield from _strings(item)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            if isinstance(item, str):
                yield len(item), value, index
            else:
                yield from _strings(item)


def _fit(view, max_chars):
    """Shrink a result view to max_chars without cutting JSON: shorten the largest arrays first
    (keeping their first items) and then the longest strings, and say what was left out."""
    view = json.loads(_dumps(view))
    omitted = {}
    while len(_dumps(view)) > max_chars:
        arrays = sorted(_arrays(view.get('data', view)), key=lambda row: -row[0])
        if arrays and arrays[0][2] and len(arrays[0][2]) > 1:
            _, path, items = arrays[0]
            total = omitted.get(path, {}).get('of', len(items))
            del items[max(1, len(items) // 2):]
            omitted[path] = {'path': path, 'shown': len(items), 'of': total}
            view['omitted'] = list(omitted.values())
            continue
        strings = sorted(_strings(view.get('data', view)), key=lambda row: -row[0])
        if strings and strings[0][0] > 80:
            length, owner, key = strings[0]
            owner[key] = owner[key][:max(40, length // 2)] + '…'
            continue
        return _dumps(view)[:max_chars]  # nothing left to shorten structurally
    return _dumps(view)


def render_result(payload: dict, *, max_chars: int | None = None) -> str:
    """Compact model-facing text for a call()/search result; the envelope stays available to hosts.

    max_chars bounds the text the way a host bounds tool results. Instead of cutting the JSON (which
    drops whatever comes last, such as rule checks after a long list of changes), the largest arrays
    keep their first items and `omitted` lists how many were left out.
    """
    if not isinstance(payload, dict):
        raise TypeError('render_result expects a call() or search result.')
    if isinstance(payload.get('batch'), list):
        # Each call keeps its own share of the bound, so one long result cannot push out the others.
        # A share too small to keep valid JSON (a short error) is shown whole.
        share = None if max_chars is None else max(200, max_chars // max(1, len(payload['batch'])))
        parts = []
        for item in payload['batch']:
            result = {key: value for key, value in item.items() if key != 'name'}
            text = render_result(result, max_chars=share)
            try:
                json.loads(text)
            except ValueError:
                text = render_result(result)
            parts.append('{"name":' + _dumps(item.get('name')) + ',"result":' + text + '}')
        return '{"batch":[' + ','.join(parts) + ']}'
    if 'selected' in payload:
        view = {key: value for key, value in payload.items() if value not in ([], None) and key not in ('added', 'new')}
        if payload.get('selected') and not payload.get('new', payload.get('added', [None])):
            # The model already has every match: say so, or it rephrases the same search again and again.
            view['note'] = NO_NEW_MATCHES
    elif 'loaded' in payload:
        view = {key: value for key, value in payload.items() if value not in ([], None)}
        if payload.get('unknown'):
            view['note'] = ('Unknown names are not in the function index; use names from the index'
                            + (', such as those in suggest.' if payload.get('suggest') else '.'))
        elif payload.get('already') and not payload.get('loaded'):
            view['note'] = 'These functions are already callable; call them.'
        if payload.get('omitted'):
            # Without this the model takes the omitted functions as loaded, or as missing from the service.
            view['note'] = ((view['note'] + ' ') if 'note' in view else '') + (
                'Omitted functions did not fit with the others loaded in this call; load them again when you need '
                'them (the functions used least recently are then unloaded).')
    elif payload.get('status') == 'succeeded':
        view = {'status': 'succeeded', 'data': payload.get('data')}
        if payload.get('httpStatus') not in (None, 200):
            view['httpStatus'] = payload['httpStatus']
        if payload.get('completeness') not in (None, _DEFAULT_COMPLETENESS):
            view['completeness'] = payload['completeness']
        if payload.get('repeated'):
            view['note'] = (f"Same call and result as {payload['repeated']} earlier time(s); you already have this data. "
                            'Use it, or answer the user.')
        if payload.get('variants'):
            view['note'] = (f"This is read {payload['variants']} of this function for the same target with other "
                            'conditions. If these results cannot answer the request, the data is not kept in this form: '
                            'answer with what you found and say what cannot be answered.')
        if payload.get('related'):
            view['next'] = 'Functions that take IDs from this result: ' + '; '.join(
                f"{', '.join(names)} ({key})" for key, names in payload['related'].items())
    else:
        problem = payload.get('error', {})
        error = {'code': problem.get('code'), 'detail': problem.get('detail')}
        if problem.get('issues'):
            error['issues'] = problem['issues']
        view = {'status': 'failed', 'error': error}
        if problem.get('code') in _RESULT_HINTS:
            view['hint'] = _RESULT_HINTS[problem['code']]
        if payload.get('repeated'):
            view['hint'] = (f"This exact call already failed {payload['repeated']} time(s); repeating it will fail again. "
                            'Change the arguments as the error says, or tell the user what is wrong.')
    text = _dumps(view)
    if max_chars is not None and len(text) > max_chars:
        if type(max_chars) is not int or max_chars < 200:
            raise ValueError('max_chars must be an integer of at least 200.')
        text = _fit(view, max_chars)
    return text


@dataclass(frozen=True)
class _Bound:
    descriptor: dict
    tool: dict
    layout: dict | None = None
    required_groups: tuple = ()
    textual: dict = field(default_factory=dict)


def _textual(parameters: dict, layout: dict | None) -> dict:
    """Flat members whose declared type is exactly string: {name: 'url' | 'body'}."""
    if layout is None:
        return {}
    return {name: 'url' if group in ('path', 'query', 'headers') else 'body' for name, group in layout.items()
            if parameters['properties'].get(name, {}).get('type') == 'string'}


def _as_text(arguments: dict, textual: dict) -> dict:
    """A number where a string is declared means its digits (an ID like 20431).

    URL/header values are text on the wire, so numbers and booleans are sent as their text form;
    a JSON body string member takes an integer's text form only (lossless)."""
    def text_form(name, value):
        where = textual.get(name)
        if where == 'url' and type(value) in (int, float, bool):
            return json.dumps(value)
        if where == 'body' and type(value) is int:
            return str(value)
        return value
    return {name: text_form(name, value) for name, value in arguments.items()}


def _id_key(name):
    """`order_ids`/`orderIds` -> `order_id`/`orderId`; None for names that are not IDs."""
    if not isinstance(name, str) or not _ID_NAME.fullmatch(name):
        return None
    return name[:-1] if name.endswith(('_ids', 'Ids')) else name


def _returned_ids(value, found, budget=400):
    """ID names with a value somewhere in a result (bounded walk)."""
    stack = [value]
    while stack and budget > 0:
        node = stack.pop()
        budget -= 1
        if isinstance(node, dict):
            for key, item in node.items():
                if isinstance(item, (dict, list)):
                    stack.append(item)
                elif item not in (None, '') and _id_key(key):
                    found.add(_id_key(key))
                elif key == 'id' and item not in (None, ''):
                    found.add('id')
        elif isinstance(node, list):
            stack.extend(node[:20])
    return found


_PAGING = {'cursor', 'page', 'page_no', 'pageNo', 'offset', 'next_cursor', 'page_token'}


def _target(arguments):
    """(IDs it is about, the other conditions) of a call, each as canonical JSON; paging is neither."""
    ids, rest = {}, {}
    for key, value in arguments.items():
        if key in _PAGING:
            continue
        (ids if key == 'id' or _id_key(key) else rest)[key] = value
    canonical = lambda value: json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)
    return canonical(ids), canonical(rest)


def _first_sentence(text, limit=110):
    text = ' '.join(str(text).split())
    match = re.search(r'(?<=[.!?])\s', text)
    text = text[:match.start()] if match else text
    if len(text) > limit:
        text = text[:limit].rsplit(' ', 1)[0] + '…'
    return text


class ToolSession:
    """Select exact business input schemas, then forward calls to normal invoke.

    tools() is a fresh Chat Completions-shaped host view. Call tools() again for
    each model request. select()/call() are async, serialized within this session.
    Never share a session across clients, users, tenants, or authorization changes.
    """

    profile = TOOL_PROFILE

    def __init__(self, apps, context: ExecutionContext, *, max_tool_bytes=16000, search_limit=5,
                 naming='readable', flatten=True, hints='none', max_search_streak=None, batch=False, variant_note=None):
        if not isinstance(context, ExecutionContext):
            raise TypeError('A trusted ExecutionContext is required.')
        runtime = DirectApplications(apps)

        async def request(method, arguments):
            return await asyncio.to_thread(dispatch, runtime, method, arguments, context)

        self._initialize(request, max_tool_bytes, search_limit, naming, flatten, hints, max_search_streak, batch,
                         variant_note)

    def _initialize(self, request, budget, limit, naming='readable', flatten=True, hints='none', max_search_streak=None,
                    batch=False, variant_note=None):
        if type(budget) is not int or budget < tool_bytes([SEARCH_TOOL]):
            raise ValueError('max_tool_bytes must fit the complete search tool.')
        if type(limit) is not int or not 1 <= limit <= 20:
            raise ValueError('search_limit must be an integer from 1 to 20.')
        if naming not in ('readable', 'hash') or not isinstance(flatten, bool) or hints not in ('none', 'shape', 'typed'):
            raise ValueError('naming must be readable or hash, flatten a boolean, hints none, shape or typed.')
        if max_search_streak is not None and (type(max_search_streak) is not int or not 1 <= max_search_streak <= 50):
            raise ValueError('max_search_streak must be None or an integer from 1 to 50.')
        if not isinstance(batch, bool):
            raise ValueError('batch must be a boolean.')
        if variant_note is not None and (type(variant_note) is not int or not 2 <= variant_note <= 20):
            raise ValueError('variant_note must be None or an integer from 2 to 20.')
        # variant_note=N: the Nth read of one function for the same target with other filters (the same
        # IDs, other conditions; not paging) carries a note to answer from what was found. A model
        # otherwise keeps re-filtering when the data cannot answer the request.
        self.variant_note, self._variants = variant_note, {}
        # batch=True offers a2api_batch: several independent calls in one model step.
        self.batch = batch
        # Searches in a row without calling a function; the host may cap them (a search loop otherwise
        # runs until the model's call limit when the catalog has no function for the request).
        self.max_search_streak, self._streak = max_search_streak, 0
        self._offered = set()  # every function offered in this session, also those evicted since
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
        self._failed = {}  # (name, arguments) -> times this exact call failed in the session
        self._reads = {}  # (name, arguments) -> times this exact read succeeded since the last write
        self._used, self._tick = {}, 0  # recency for eviction; the tool list order never changes
        # Functions selected since the model last received the list: another search must not push
        # them out before the model has seen them (parallel searches otherwise evict each other).
        self._unseen = set()
        # Strategy 'index': every function by name, loaded on request (see index()).
        self._index, self._bound, self._strip = {}, {}, ''
        self._related, self._consumers, self._produces, self._rank = 0, {}, {}, {}

    @classmethod
    async def from_mcp(cls, client, *, max_tool_bytes=16000, search_limit=5, naming='readable', flatten=True, hints='none',
                       max_search_streak=None, batch=False, variant_note=None):
        """Use an already connected, trusted MCP client; no connection is owned."""
        listing = await client.list_tools()
        expected = {'a2api.discover', 'a2api.describe', 'a2api.invoke'}
        if {tool.name for tool in listing.tools} != expected or len(listing.tools) != 3:
            raise ValueError('Connect an a2api MCP server exposing discover/describe/invoke.')

        async def request(method, arguments):
            result = await client.call_tool('a2api.' + method, arguments)
            return result.structured_content

        session = cls.__new__(cls)
        session._initialize(request, max_tool_bytes, search_limit, naming, flatten, hints, max_search_streak, batch,
                            variant_note)
        return session

    @property
    def stats(self):
        return dict(self._stats)

    @property
    def strategy(self):
        """'all' or 'search' after auto(), 'index' after index(); None when the host selects explicitly."""
        return self._strategy

    def _front(self):
        return LOAD_TOOL if self._strategy == 'index' else SEARCH_TOOL

    def _fixed(self, include_search=True, *, budget=False):
        """The session's own tools ahead of the business functions. a2api_batch joins once a function
        is callable: offered before, it changed which functions a model chose to load. The budget
        always counts it."""
        batch = self.batch and (budget or bool(self._active))
        return [*([self._front()] if include_search else []), *([BATCH_TOOL] if batch else [])]

    def tools(self, *, include_search=None):
        """Fresh model view. include_search=None omits search only after auto() chose 'all'.

        After index(), the load function takes the place of search."""
        if include_search is None:
            include_search = self._strategy != 'all'
        self._unseen.clear()  # the model receives these definitions now
        return deepcopy([*self._fixed(include_search), *(bound.tool for bound in self._active.values())])

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
            self._bound.clear()
            self._pages.clear()
            self._catalog = catalog

    def _clear(self):
        self._active.clear()
        self._unseen.clear()
        self._names.clear()
        self._bound.clear()
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
            # index() drops a namespace every ID shares: it would repeat on every index line.
            identifier = item['id'][len(self._strip):] if item['id'].startswith(self._strip) else item['id']
            name = re.sub(r'[^A-Za-z0-9_]+', '_', identifier).strip('_')[:48] or 'call'
            if not name[0].isalpha():
                name = 'f_' + name[:46]
            if name in (SEARCH_NAME, LOAD_NAME) or name in self._names.values():
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
        selected, omitted, evicted, added = [], [], [], []
        protected = set()
        for item in entries:
            name = self._name(item)
            if name not in self._active:
                added.append(name)
            if name in self._active:
                bound = self._active[name]
                self._stats['reused'] += 1
            else:
                bound = await self._bind(item, name)
            removed = self._admit(name, bound, protected)
            if removed is None:
                omitted.append({'id': item['id'], 'reason': 'SCHEMA_BUDGET'})
                continue
            evicted.extend(removed)
            selected.append({'name': name, 'id': item['id']})
        page = self._pages.commit(prepared, found)
        added = [name for name in added if name in self._active]
        new = [item['name'] for item in selected if item['name'] not in self._offered]
        self._offered.update(item['name'] for item in selected)
        return {'selected': selected, 'added': added, 'new': new, 'omitted': omitted, 'evicted': evicted, **page}

    def _admit(self, name, bound, protected):
        """Make one bound function active within max_tool_bytes; returns the evicted names, or None
        when it cannot fit. Functions keep their place in the list (a stable prompt prefix for
        server caches); recency only decides which function leaves when the budget is exceeded."""
        retained = OrderedDict(self._active)
        retained.setdefault(name, bound)
        self._tick += 1
        self._used[name] = self._tick
        removed, fixed = [], self._fixed(budget=True)
        while tool_bytes([*fixed, *(entry.tool for entry in retained.values())]) > self.max_tool_bytes:
            candidates = [key for key in retained if key != name and key not in protected and key not in self._unseen]
            victim = min(candidates, key=lambda key: self._used.get(key, 0)) if candidates else None
            if victim is None:
                break
            retained.pop(victim)
            removed.append(victim)
        if tool_bytes([*fixed, *(entry.tool for entry in retained.values())]) > self.max_tool_bytes:
            return None
        if name not in self._active:
            self._unseen.add(name)
        self._active = retained
        self._stats['evicted'] += len(removed)
        protected.add(name)
        return removed

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

    async def auto(self, question: str = '', *, max_functions: int = 64, preselect: int = 8, all_bytes: int = 10000):
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
            entries, cursor, catalog = await self._list(max_functions)
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

    async def _list(self, max_functions):
        """Every catalog entry (stops once more than max_functions were read); never executes."""
        entries, cursor, catalog = [], None, None
        while True:
            found = await self._request('discover', {'query': '', 'limit': 50, **({'cursor': cursor} if cursor else {})})
            if catalog is not None and found['catalogVersion'] != catalog:
                self._clear()
                raise A2APIError('CONTRACT_DRIFT', 'Catalog changed while listing; start again.', status=409)
            catalog = found['catalogVersion']
            entries.extend(found['capabilities'])
            cursor = found['nextCursor']
            if cursor is None or len(entries) > max_functions:
                return entries, cursor, catalog

    async def index(self, question: str = '', *, detail='summary', group=None, related=0, relations=None,
                    preselect=0, max_functions=2000):
        """Host strategy for catalogs too large to send whole: the model reads an index of every
        function and loads only the ones it chooses.

        Returns {'strategy': 'index', 'functions': n, 'text': ...}. The host puts `text` in the
        system prompt (it never changes during the session, so it stays in the cached prompt
        prefix); tools() then holds a2api_load and the loaded functions. detail='summary' lists each
        name with the first sentence of its summary, 'names' only the names. group(entry) -> str
        (entry: the discover item) sorts the index under headings.

        related=N (0 disables) adds to a successful call's result up to N functions that take an ID
        it returned, ranked by the user's request (see focus()). Links come from `relations`
        ({capability id: {'consumes': [...], 'produces': [...]}}, e.g. ToolCatalogImporter.relations())
        and, for functions it does not cover, from inputs named like IDs (order_id, orderId).

        preselect=N (0 disables) also loads up to N functions the host search finds for the
        question, as auto() does: when they fit, the model calls them without a load step, and the
        index covers what the search missed. Never executes a business API.
        """
        if (not isinstance(question, str) or detail not in ('summary', 'names') or (group is not None and not callable(group))
                or type(related) is not int or not 0 <= related <= 20 or (relations is not None and not isinstance(relations, dict))
                or type(preselect) is not int or not 0 <= preselect <= 20
                or type(max_functions) is not int or not 1 <= max_functions <= 10000):
            raise ValueError('index requires a question string, detail summary or names, a callable group, '
                             'related 0-20, a relations dict, preselect 0-20 and max_functions 1-10000.')
        if tool_bytes([LOAD_TOOL]) > self.max_tool_bytes:
            raise ValueError('max_tool_bytes must fit the complete load tool.')
        async with self._lock:
            entries, cursor, catalog = await self._list(max_functions)
            if cursor is not None:
                raise A2APIError('INDEX_TOO_LARGE', f'The catalog has more than {max_functions} functions.', status=413)
            namespaces = {item['id'].split('.', 1)[0] for item in entries if '.' in item['id']}
            strip = namespaces.pop() + '.' if len(namespaces) == 1 and all('.' in item['id'] for item in entries) else ''
            if strip != self._strip:
                self._clear()
                self._strip = strip
            self._adopt_catalog(catalog)
            self._strategy = 'index'
            self._index = {self._name(item): item for item in entries}
            self._related, self._consumers, self._produces = related, {}, {}
            if related:
                relations = relations or {}
                for name, item in self._index.items():
                    declared = relations.get(item['id'])
                    if declared is None:
                        bound = self._bound.get(name) or await self._bind(item, name)
                        self._bound[name] = bound
                        consumes = bound.tool['function']['parameters'].get('properties', {})
                        declared = {'consumes': list(consumes)}
                    for key in filter(None, map(_id_key, declared.get('consumes', ()))):
                        self._consumers.setdefault(key, []).append(name)
                    self._produces[name] = [key for key in map(_id_key, declared.get('produces', ())) if key]
                await self._focus(question)
            groups = {}
            for name, item in sorted(self._index.items()):
                groups.setdefault(str(group(item)) if group else '', []).append((name, item))
            lines = [INDEX_HEAD + (INDEX_WRITES if detail == 'summary' else '')
                     + (' Functions already in your tool list are loaded; call them directly.' if preselect else '')]
            for heading, members in sorted(groups.items()):
                if detail == 'names':
                    lines.append((heading + ': ' if heading else '') + ', '.join(name for name, _ in members))
                    continue
                if heading:
                    lines.append('## ' + heading)
                lines.extend(f"{name}{' [write]' if item['effects'].get('kind') != 'read' else ''}: "
                             f"{_first_sentence(item['summary'])}" for name, item in members)
            text = '\n'.join(lines)
            query = ' '.join(question.split())[:1000]
            preselected = await self._select(query, limit=preselect) if preselect and query else None
            return {'strategy': 'index', 'functions': len(self._index), 'text': text, 'preselected': preselected}

    async def focus(self, question: str):
        """The user's current request (each new user turn, in any strategy): ranks the related functions
        results name, and starts the variant_note count again."""
        if not isinstance(question, str):
            raise ValueError('focus requires a question string.')
        async with self._lock:
            await self._focus(question)

    async def _focus(self, question):
        query = ' '.join(question.split())[:1000]
        self._rank, self._variants = {}, {}  # a new request may search again
        if not query or not self._related:
            return
        found = await self._request('discover', {'query': query, 'limit': 50})
        if found['catalogVersion'] == self._catalog:
            for position, item in enumerate(found['capabilities']):
                self._rank.setdefault(self._name(item), position)

    async def _load(self, names):
        if self._catalog is None:
            raise A2APIError('CONTRACT_DRIFT', 'The catalog changed; the host must build the index again.', status=409)
        loaded, already, unknown, omitted, evicted, protected = [], [], [], [], [], set()
        for asked in dict.fromkeys(names):
            name = self._resolve(asked)
            item = self._index.get(name)
            if item is None:
                unknown.append(asked)
            elif name in loaded or name in already:
                continue
            elif name in self._active:
                self._tick += 1
                self._used[name] = self._tick
                protected.add(name)
                already.append(name)
            else:
                bound = self._bound.get(name) or await self._bind(item, name)
                self._bound[name] = bound
                removed = self._admit(name, bound, protected)
                if removed is None:
                    omitted.append({'name': name, 'reason': 'SCHEMA_BUDGET'})
                    continue
                evicted.extend(removed)
                loaded.append(name)
        self._offered.update(loaded)
        result = {'loaded': loaded, 'already': already, 'unknown': unknown, 'omitted': omitted, 'evicted': evicted}
        if unknown:
            suggest = []
            for name in unknown[:3]:
                found = await self._request('discover', {'query': re.sub(r'[_\W]+', ' ', name)[:1000], 'limit': 3})
                suggest.extend(self._name(item) for item in found['capabilities']
                               if found['catalogVersion'] == self._catalog and self._name(item) in self._index)
            result['suggest'] = [name for name in dict.fromkeys(suggest) if name not in self._active][:5]
        return result

    def _resolve(self, name):
        """The index name meant: also when a heading was joined to it (`fulfillment.claim.get_claim`) or
        its case changed; None when there is none."""
        if name in self._index:
            return name
        tail = re.split(r'[\s./›:>|]+', name.strip())[-1] if name.strip() else name
        for candidate in (tail, name.lower(), tail.lower()):
            if candidate in self._index:
                return candidate
        return None

    def _next_steps(self, name, data):
        """{id name: [functions taking it]} for IDs a successful result returned; at most `related` functions.
        An ID many functions take is shown only through functions that match the user's request."""
        returned = _returned_ids(data, set())
        if not returned:
            return {}
        returned |= set(self._produces.get(name, ()))
        candidates = []
        for key in returned:
            takers = self._consumers.get(key, ())
            for other in takers:
                rank = self._rank.get(other)
                if other != name and (rank is not None or len(takers) <= 3):
                    candidates.append((rank if rank is not None else len(self._index), other, key))
        related, chosen = {}, set()
        for _, other, key in sorted(candidates):
            if other not in chosen and len(chosen) < self._related:
                chosen.add(other)
                related.setdefault(key, []).append(other)
        return related

    async def call(self, name: str, arguments: dict, *, request_id: str | None = None):
        """Return search results or the original validated invoke envelope; no retry.

        request_id (for example the model's tool-call id) names one intended call; a host that
        delivers the same call twice passes the same id, which the backend can deduplicate when the
        deployment sets idempotency_header. A failed call whose exact name and arguments already
        failed in this session carries `repeated` (earlier failures), shown to the model as a hint.
        With batch=True, a2api_batch returns {'batch': [{'name', ...each call's own result}]}: every
        call goes through call() exactly as if made directly (request ids `<request_id>.<n>`).
        """
        if name == BATCH_NAME and self.batch:
            try:
                validate_value(BATCH_TOOL['function']['parameters'], arguments, code='INVALID_INPUT', status=400)
            except A2APIError as error:
                return {'error': error.problem()}
            results = []
            for index, item in enumerate(arguments['calls']):
                if item['name'] in (SEARCH_NAME, LOAD_NAME, BATCH_NAME):
                    result = {'error': A2APIError('INVALID_INPUT', f"{item['name']} cannot run inside {BATCH_NAME}.").problem()}
                else:
                    result = await self.call(item['name'], item['arguments'],
                                             request_id=None if request_id is None else f'{request_id}.{index}')
                results.append({'name': item['name'], **result})
            return {'batch': results}
        if name in (SEARCH_NAME, LOAD_NAME):
            if self.max_search_streak is not None and self._streak >= self.max_search_streak:
                return {'error': A2APIError('SEARCH_LIMIT', f'{self._streak} searches in a row found no function to call '
                                            'for this request.', status=429).problem()}
            self._streak += 1
            return await self._call(name, arguments, request_id)
        self._streak = 0
        result = await self._call(name, arguments, request_id)
        try:
            key = (name, json.dumps(arguments, sort_keys=True, allow_nan=False))
        except (TypeError, ValueError, RecursionError):
            return result
        bound = self._active.get(name)
        if 'error' in result:
            earlier = self._failed.get(key, 0)
            self._failed[key] = earlier + 1
            if earlier:
                result = {**result, 'repeated': earlier}
        elif bound is not None and bound.descriptor['effects']['kind'] == 'read':
            earlier = self._reads.get(key, 0)
            self._reads[key] = earlier + 1
            if earlier:
                result = {**result, 'repeated': earlier}
            elif self.variant_note is not None:
                target, condition = _target(arguments)
                seen = self._variants.setdefault((name, target), set())
                seen.add(condition)
                if len(seen) >= self.variant_note:
                    result = {**result, 'variants': len(seen)}
        else:
            self._reads.clear()  # after a change, reading again is new information
            self._variants.clear()
        if self._related and result.get('status') == 'succeeded' and not result.get('repeated'):
            related = self._next_steps(name, result.get('data'))
            if related:
                result = {**result, 'related': related}
        return result

    async def _call(self, name, arguments, request_id):
        async with self._lock:
            try:
                try:
                    json.dumps(arguments, allow_nan=False)
                except (TypeError, ValueError, RecursionError):
                    raise A2APIError('INVALID_INPUT', 'Arguments must be finite JSON.') from None
                if name == SEARCH_NAME:
                    validate_value(SEARCH_TOOL['function']['parameters'], arguments, code='INVALID_INPUT', status=400)
                    return await self._select(arguments['query'], more=arguments.get('more', False))
                if name == LOAD_NAME and self._strategy == 'index':
                    validate_value(LOAD_TOOL['function']['parameters'], arguments, code='INVALID_INPUT', status=400)
                    return await self._load(arguments['names'])
                bound = self._active.get(name)
                if bound is None and self._strategy == 'index' and name in self._index and self._catalog is not None:
                    # Called straight from the index: load it. A read whose arguments are valid runs
                    # now; a change waits until the model has seen its parameters.
                    bound = self._bound.get(name) or await self._bind(self._index[name], name)
                    self._bound[name] = bound
                    if self._admit(name, bound, set()) is None:
                        raise A2APIError('SCHEMA_BUDGET', 'The function does not fit max_tool_bytes.', status=413)
                    self._offered.add(name)
                    if bound.descriptor['effects']['kind'] != 'read':
                        raise A2APIError('NOT_LOADED', f'{name} was called before it was loaded, so nothing was done.',
                                         status=409)
                if bound is None and self._strategy == 'index':
                    raise A2APIError('UNKNOWN_FUNCTION', f'There is no function {name} in the function index.', status=404)
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
                self._tick += 1
                self._used[name] = self._tick
                result = await self._request('invoke', {'id': bound.descriptor['id'],
                    'version': bound.descriptor['version'], 'catalogVersion': self._catalog, 'input': arguments,
                    **({'requestId': request_id} if request_id is not None else {})})
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
