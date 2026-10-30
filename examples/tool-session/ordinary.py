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


class OrdinarySession:
    def __init__(self, apps, context):
        self.runtime = DirectApplications(apps)  # same lexical rank/catalog fingerprint
        self.context = context
        self._active = OrderedDict()
        self._stats = {'discover': 0, 'describe': 0, 'invoke': 0, 'reused': 0, 'evicted': 0}

    @property
    def stats(self):return dict(self._stats)

    def tools(self, *, include_search=True):
        return deepcopy([*([SEARCH_TOOL] if include_search else []), *(item['tool'] for item in self._active.values())])

    def binding(self, name):
        item = self._active.get(name)
        return deepcopy(item['binding']) if item else None

    async def select(self, query):
        self._stats['discover'] += 1
        found = self.runtime.discover(query, self.context, limit=3)
        selected = []
        for item in found['capabilities']:
            token = json.dumps([self.runtime.version, item['id'], item['version']], separators=(',', ':'))
            name = 'a2api_call_' + hashlib.sha256(token.encode()).hexdigest()[:24]
            if name not in self._active:
                app, desc = self.runtime._get(item['id'], item['version'])
                self._active[name] = {'app': app, 'binding': {'id': item['id'], 'version': item['version'],
                    'catalogVersion': self.runtime.version}, 'tool': {'type': 'function', 'function': {
                        'name': name, 'description': desc['summary'] + ' [effect: ' + desc['effects']['kind'] + ']',
                        'parameters': deepcopy(desc['inputSchema'])}}}
            else:self._stats['reused'] += 1
            selected.append({'name': name, 'id': item['id']})
        return {'selected': selected, 'omitted': [], 'evicted': [], 'moreAvailable': found['nextCursor'] is not None}

    async def prime(self, identifiers):
        for identifier in identifiers:await self.select(identifier)

    async def call(self, name, arguments):
        if name == SEARCH_NAME:return await self.select(arguments['query'])
        item = self._active[name]
        self._stats['invoke'] += 1
        return await asyncio.to_thread(item['app'].invoke, item['binding']['id'], arguments, context=self.context)
