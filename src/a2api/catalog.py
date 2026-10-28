"""An immutable catalog with authorization-filtered lexical discovery."""

from __future__ import annotations

import base64
import hashlib
import json
from types import MappingProxyType

from .errors import A2APIError, contract_error
from .ir import Capability, ExecutionContext


class Catalog:
    def __init__(self, capabilities: list[Capability], *, allow_samples: bool = False):
        entries = {}
        for capability in capabilities:
            key = (capability.id, capability.version)
            if key in entries:
                raise contract_error("Duplicate capability ID and version")
            entries[key] = capability
        self._entries = MappingProxyType(entries)
        self._allow_samples = allow_samples
        serialized = "\n".join(entries[k].manifest_json for k in sorted(entries))
        self.version = "sha256:" + hashlib.sha256(serialized.encode()).hexdigest()

    @property
    def capabilities(self) -> tuple[Capability, ...]:
        return tuple(self._entries.values())

    def _visible(self, capability: Capability, context: ExecutionContext) -> bool:
        return (capability.enabled and (self._allow_samples or not capability.sample_only)
                and capability.required_scopes.issubset(context.scopes))

    def get(self, capability_id: str, version: str, context: ExecutionContext) -> Capability:
        capability = self._entries.get((capability_id, version))
        if capability is None or not self._visible(capability, context):
            raise A2APIError("NOT_FOUND", "Capability is unavailable for this caller and version.", status=404)
        return capability

    def describe(self, capability_id: str, version: str, context: ExecutionContext) -> dict:
        return {"catalogVersion": self.version, "capability": self.get(capability_id, version, context).describe()}

    def discover(self, query: str, context: ExecutionContext, *, limit: int = 10, cursor: str | None = None) -> dict:
        if not isinstance(query, str) or len(query) > 1000 or type(limit) is not int or not 1 <= limit <= 50:
            raise A2APIError("INVALID_REQUEST", "query must be a string and limit must be between 1 and 50.")
        words = query.casefold().split()
        matches = []
        for capability in self._entries.values():
            if not self._visible(capability, context):
                continue
            raw = capability.describe()
            intent = raw["intent"]
            text = " ".join([raw["id"], raw["title"], intent["summary"], *intent["useWhen"], *intent.get("keywords", [])]).casefold()
            score = sum(word in text for word in words)
            if words and score == 0:
                continue
            matches.append((score, capability.id, capability.version, {
                "id": capability.id, "version": capability.version, "title": capability.title,
                "summary": intent["summary"], "effects": raw["effects"],
                "matchedTerms": [word for word in words if word in text],
            }))
        matches.sort(key=lambda m: (-m[0], m[1], m[2]))
        view = hashlib.sha256(json.dumps([self.version, query, limit, context.actor, context.tenant, sorted(context.scopes)]).encode()).hexdigest()
        offset = 0
        if cursor is not None:
            try:
                value = json.loads(base64.urlsafe_b64decode(cursor.encode()).decode())
                if value["view"] != view or type(value["offset"]) is not int or not 0 <= value["offset"] <= len(matches):
                    raise ValueError()
                offset = value["offset"]
            except (ValueError, KeyError, TypeError, AttributeError, UnicodeError):
                raise A2APIError("INVALID_CURSOR", "Cursor does not match this catalog, query, or caller.") from None
        next_offset = offset + limit
        next_cursor = (base64.urlsafe_b64encode(json.dumps({"view": view, "offset": next_offset}).encode()).decode()
                       if next_offset < len(matches) else None)
        return {"catalogVersion": self.version, "capabilities": [m[3] for m in matches[offset:next_offset]],
                "nextCursor": next_cursor}
