"""Evaluation baseline: ordinary host search + function tools, no call wire.

Uses the SAME converted applications/validation and lexical ranker to isolate
information delivery, not importer/runtime cost or developer effort. This is
an example baseline, not a second product API or independent HTTP SDK.
"""

import asyncio
from collections import OrderedDict
from copy import deepcopy
import hashlib
import json

from a2api.mcp_application import DirectApplications
from a2api.tool_session import SEARCH_NAME, SEARCH_TOOL
from a2api.discovery_metadata import SearchPages
from a2api.tool_description import function_description


class OrdinarySession:
    def __init__(self, apps, context):
        self.runtime = DirectApplications(apps)  # same lexical rank/catalog fingerprint
        self.context = context
        self._active = OrderedDict()
        self._pages = SearchPages()
        self._stats = {'discover': 0, 'describe': 0, 'invoke': 0, 'reused': 0, 'evicted': 0}

    @property
    def stats(self):return dict(self._stats)

    def tools(self, *, include_search=True):
        return deepcopy([*([SEARCH_TOOL] if include_search else []), *(item['tool'] for item in self._active.values())])

    def binding(self, name):
        item = self._active.get(name)
        return deepcopy(item['binding']) if item else None

    async def select(self, query, *, more=False):
        self._stats['discover'] += 1
        prepared = self._pages.prepare(query, more, limit=3)
        found = self.runtime.discover(context=self.context, **prepared['arguments'])
        selected = []
        for item in found['capabilities']:
            token = json.dumps([self.runtime.version, item['id'], item['version']], separators=(',', ':'))
            name = 'a2api_call_' + hashlib.sha256(token.encode()).hexdigest()[:24]
            if name not in self._active:
                app, desc = self.runtime._get(item['id'], item['version'])
                self._active[name] = {'app': app, 'binding': {'id': item['id'], 'version': item['version'],
                    'catalogVersion': self.runtime.version}, 'tool': {'type': 'function', 'function': {
                        'name': name, 'description': function_description(desc, 'typed'),
                        'parameters': deepcopy(desc['inputSchema'])}}}
            else:self._stats['reused'] += 1
            selected.append({'name': name, 'id': item['id']})
        return {'selected': selected, 'omitted': [], 'evicted': [], **self._pages.commit(prepared, found)}

    async def prime(self, identifiers):
        for identifier in identifiers:await self.select(identifier)

    async def call(self, name, arguments):
        if name == SEARCH_NAME:return await self.select(arguments['query'], more=arguments.get('more', False))
        item = self._active[name]
        self._stats['invoke'] += 1
        return await asyncio.to_thread(item['app'].invoke, item['binding']['id'], arguments, context=self.context)
