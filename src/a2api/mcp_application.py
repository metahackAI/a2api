"""Small wire adapter for already bound direct-call applications; no registry IO."""

from __future__ import annotations

import base64
from copy import deepcopy
import hashlib
import json

from .conversion import ConvertedAPI
from .errors import A2APIError
from .native import Application


def agent_descriptor(raw: dict) -> dict:
    """Project legacy manifests or direct descriptors to the same public view."""
    return {'id': raw['id'], 'version': raw['version'],
            'summary': raw['summary'] if 'summary' in raw else raw['intent']['summary'],
            'effects': {'kind': raw['effects']['kind']},
            'inputSchema': raw['inputSchema'], 'outputSchema': raw['outputSchema']}


class DirectApplications:
    """Expose selected applications through the existing three-method wire API."""

    def __init__(self, apps):
        apps = apps if isinstance(apps, (list, tuple)) else [apps]
        if not apps or any(not isinstance(app, (ConvertedAPI, Application)) for app in apps):
            raise TypeError('Supply a ConvertedAPI, Application, or a nonempty list of these applications.')
        self._entries = {}
        for app in apps:
            for descriptor in app.descriptors():
                key = (descriptor['id'], descriptor['version'])
                if key in self._entries:
                    raise A2APIError('INVALID_CONTRACT', 'MCP applications must have distinct capability ID/version pairs.')
                self._entries[key] = (app, descriptor)
        serialized = json.dumps([self._entries[key][1] for key in sorted(self._entries)],
                                ensure_ascii=False, sort_keys=True, allow_nan=False, separators=(',', ':'))
        self.version = 'sha256:' + hashlib.sha256(serialized.encode()).hexdigest()
        self.writable = any(descriptor['effects']['kind'] == 'write' for _, descriptor in self._entries.values())

    def _get(self, identifier, version):
        entry = self._entries.get((identifier, version))
        if entry is None:
            raise A2APIError('NOT_FOUND', 'This MCP server does not expose the requested capability/version.', status=404)
        return entry

    def discover(self, query, context, *, limit=10, cursor=None):
        words = query.casefold().split()
        matches = []
        for (identifier, version), (_, descriptor) in self._entries.items():
            text = (identifier + ' ' + descriptor['summary']).casefold()
            terms = [word for word in words if word in text]
            if words and not terms:
                continue
            matches.append((-len(terms), identifier, version, {
                'id': identifier, 'version': version, 'title': identifier, 'summary': descriptor['summary'],
                'effects': descriptor['effects'], 'matchedTerms': terms}))
        matches.sort(key=lambda match: match[:3])
        view = hashlib.sha256(json.dumps([self.version, query, limit, context.actor, context.tenant,
                                         sorted(context.scopes)]).encode()).hexdigest()
        offset = 0
        if cursor is not None:
            try:
                data = json.loads(base64.urlsafe_b64decode(cursor).decode())
                if data['view'] != view or type(data['offset']) is not int or not 0 <= data['offset'] <= len(matches):
                    raise ValueError()
                offset = data['offset']
            except (ValueError, KeyError, TypeError, UnicodeError):
                raise A2APIError('INVALID_CURSOR', 'Cursor does not match this catalog, query, or caller.') from None
        next_offset = offset + limit
        next_cursor = (base64.urlsafe_b64encode(json.dumps({'view': view, 'offset': next_offset}).encode()).decode()
                       if next_offset < len(matches) else None)
        return {'catalogVersion': self.version, 'capabilities': [entry[3] for entry in matches[offset:next_offset]],
                'nextCursor': next_cursor}

    def describe(self, identifier, version, context):
        _, descriptor = self._get(identifier, version)
        # Fresh data keeps a host or transport from mutating the bound catalog.
        return {'catalogVersion': self.version, 'capability': deepcopy(descriptor)}

    def invoke(self, identifier, version, catalog_version, input, context, *, request_id=None):
        app, _ = self._get(identifier, version)
        if catalog_version != self.version:
            raise A2APIError('CONTRACT_DRIFT', 'Catalog changed; discover and describe again.', status=409)
        result = app.invoke(identifier, input, context=context)
        if request_id is not None:
            result = {**result, 'requestId': request_id}
        return result
