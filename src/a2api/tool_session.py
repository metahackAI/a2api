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

from .api import dispatch
from .errors import A2APIError
from .ir import ExecutionContext
from .mcp_application import DirectApplications
from .openapi_schema import check_draft_schema
from .protocol import protocol_schema
from .schema import validate_value
from .discovery_metadata import SearchPages

TOOL_PROFILE = 'a2api-tools/0.2'
SEARCH_NAME = 'a2api_search'
SEARCH_TOOL = {'type': 'function', 'function': {
    'name': SEARCH_NAME,
    'description': 'Find functions by task keywords. Selected functions become callable in the next model request. '
                   'Use an already available function directly. If moreAvailable is true, request the same query with '
                   'more=true for the next page. Repeating without more reuses the page. Refine the query if no progress.',
    'parameters': {'type': 'object', 'properties': {'query': {'type': 'string', 'maxLength': 1000},
                                                  'more': {'type': 'boolean', 'default': False}},
                   'required': ['query'], 'additionalProperties': False}}}


def tool_bytes(tools: list[dict]) -> int:
    """Compact UTF-8 JSON bytes, not model tokens or the complete prompt size."""
    return len(json.dumps(tools, ensure_ascii=False, sort_keys=True,
                          separators=(',', ':'), allow_nan=False).encode('utf-8'))


@dataclass(frozen=True)
class _Bound:
    descriptor: dict
    tool: dict


class ToolSession:
    """Select exact business input schemas, then forward calls to normal invoke.

    tools() is a fresh Chat Completions-shaped host view. Call tools() again for
    each model request. select()/call() are async, serialized within this session.
    Never share a session across clients, users, tenants, or authorization changes.
    """

    profile = TOOL_PROFILE

    def __init__(self, apps, context: ExecutionContext, *, max_tool_bytes=16000, search_limit=3):
        if not isinstance(context, ExecutionContext):
            raise TypeError('A trusted ExecutionContext is required.')
        runtime = DirectApplications(apps)

        async def request(method, arguments):
            return await asyncio.to_thread(dispatch, runtime, method, arguments, context)

        self._initialize(request, max_tool_bytes, search_limit)

    def _initialize(self, request, budget, limit):
        if type(budget) is not int or budget < tool_bytes([SEARCH_TOOL]):
            raise ValueError('max_tool_bytes must fit the complete search tool.')
        if type(limit) is not int or not 1 <= limit <= 20:
            raise ValueError('search_limit must be an integer from 1 to 20.')
        self._request_impl = request
        self.max_tool_bytes = budget
        self.search_limit = limit
        self._catalog = None
        self._active: OrderedDict[str, _Bound] = OrderedDict()
        self._lock = asyncio.Lock()
        self._pages = SearchPages()
        self._stats = {'discover': 0, 'describe': 0, 'invoke': 0, 'reused': 0, 'evicted': 0}

    @classmethod
    async def from_mcp(cls, client, *, max_tool_bytes=16000, search_limit=3):
        """Use an already connected, trusted MCP client; no connection is owned."""
        listing = await client.list_tools()
        expected = {'a2api.discover', 'a2api.describe', 'a2api.invoke'}
        if {tool.name for tool in listing.tools} != expected or len(listing.tools) != 3:
            raise ValueError('Connect an a2api MCP server exposing discover/describe/invoke.')

        async def request(method, arguments):
            result = await client.call_tool('a2api.' + method, arguments)
            return result.structured_content

        session = cls.__new__(cls)
        session._initialize(request, max_tool_bytes, search_limit)
        return session

    @property
    def stats(self):
        return dict(self._stats)

    def tools(self, *, include_search=True):
        """Known-task hosts may omit search; this changes only the model view."""
        return deepcopy([*([SEARCH_TOOL] if include_search else []),
                         *(bound.tool for bound in self._active.values())])

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
            self._pages.clear()
            self._catalog = catalog

    def _clear(self):
        self._active.clear()
        self._catalog = None
        self._pages.clear()

    async def _select(self, query, *, exact=False, more=False):
        prepared = self._pages.prepare(query, more, limit=self.search_limit, restart=exact)
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
            token = json.dumps([self._catalog, item['id'], item['version']], separators=(',', ':'))
            name = 'a2api_call_' + hashlib.sha256(token.encode()).hexdigest()[:24]
            if name in self._active:
                bound = self._active[name]
                self._stats['reused'] += 1
            else:
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
                tool = {'type': 'function', 'function': {'name': name,
                    'description': descriptor['summary'] + ' [effect: ' + descriptor['effects']['kind'] + ']',
                    'parameters': deepcopy(descriptor['inputSchema'])}}
                bound = _Bound(deepcopy(descriptor), tool)
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
