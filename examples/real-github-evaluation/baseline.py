"""Ordinary search/function host with the same whole-tool byte/LRU policy."""

from collections import OrderedDict
import importlib.util
import json
from pathlib import Path

from a2api import A2APIError
from a2api.schema import validate_value
from a2api.tool_session import SEARCH_NAME, SEARCH_TOOL, tool_bytes

_spec = importlib.util.spec_from_file_location('comparison_ordinary',
    Path(__file__).resolve().parents[1] / 'tool-session/ordinary.py')
_ordinary = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ordinary)
OrdinarySession = _ordinary.OrdinarySession


class BaselineSession(OrdinarySession):
    def __init__(self, apps, context, *, max_tool_bytes=16000):
        super().__init__(apps, context)
        self.max_tool_bytes = max_tool_bytes

    async def select(self, query, *, more=False):
        original = OrderedDict(self._active)
        result = await super().select(query, more=more)
        available = self._active
        retained, protected = original, set()
        selected, omitted, evicted = [], [], []
        for item in result['selected']:
            name = item['name']
            candidate = OrderedDict(retained)
            candidate.pop(name, None)
            candidate[name] = available[name]
            removed = []
            while tool_bytes([SEARCH_TOOL, *(value['tool'] for value in candidate.values())]) > self.max_tool_bytes:
                victim = next((key for key in candidate if key != name and key not in protected), None)
                if victim is None:break
                candidate.pop(victim)
                removed.append(victim)
            if tool_bytes([SEARCH_TOOL, *(value['tool'] for value in candidate.values())]) > self.max_tool_bytes:
                omitted.append({'id': item['id'], 'reason': 'SCHEMA_BUDGET'})
                continue
            retained = candidate
            protected.add(name)
            evicted.extend(removed)
            selected.append(item)
        self._active = retained
        self._stats['evicted'] += len(evicted)
        return {**result, 'selected': selected, 'omitted': omitted, 'evicted': evicted}

    async def call(self, name, arguments):
        try:
            try:json.dumps(arguments, allow_nan=False)
            except (ValueError, TypeError, RecursionError):
                raise A2APIError('INVALID_INPUT', 'Arguments must be finite JSON.') from None
            if name == SEARCH_NAME:
                validate_value(SEARCH_TOOL['function']['parameters'], arguments, code='INVALID_INPUT', status=400)
            else:
                if name not in self._active:
                    raise A2APIError('NOT_SELECTED', 'Function is not active in this session; search again.')
                validate_value(self._active[name]['tool']['function']['parameters'], arguments, code='INVALID_INPUT', status=400)
                self._active.move_to_end(name)
            return await super().call(name, arguments)
        except A2APIError as error:return {'error': error.problem()}
