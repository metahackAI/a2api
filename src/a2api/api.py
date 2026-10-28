"""Shared request contracts for HTTP and MCP bindings."""

from __future__ import annotations

from copy import deepcopy

from jsonschema import Draft202012Validator

from .errors import A2APIError
from .ir import ExecutionContext
from .runtime import Runtime

_STRING = {"type": "string", "minLength": 1}
_PROPERTIES = {
    "discover": {
        "query": {"type": "string", "maxLength": 1000},
        "limit": {"type": "integer", "minimum": 1, "maximum": 50},
        "cursor": _STRING,
    },
    "describe": {"id": _STRING, "version": _STRING},
    "invoke": {
        "id": _STRING, "version": _STRING, "catalogVersion": _STRING,
        "input": {"type": "object"},
        "requestId": {"type": "string", "minLength": 1, "maxLength": 128},
    },
}
_REQUIRED = {"discover": [], "describe": ["id", "version"],
             "invoke": ["id", "version", "catalogVersion", "input"]}
METHODS = tuple(_PROPERTIES)


def input_schema(method: str) -> dict:
    if method not in _PROPERTIES:
        raise A2APIError("NOT_FOUND", "Unknown a2api method.", status=404)
    return deepcopy({"type": "object", "properties": _PROPERTIES[method],
                     "required": _REQUIRED[method], "additionalProperties": False})


def dispatch(runtime: Runtime, method: str, payload: dict, context: ExecutionContext) -> dict:
    if not Draft202012Validator(input_schema(method)).is_valid(payload):
        raise A2APIError("INVALID_REQUEST", "Request fields do not match the endpoint contract.")
    if method == "discover":
        return runtime.discover(payload.get("query", ""), context,
                                limit=payload.get("limit", 10), cursor=payload.get("cursor"))
    if method == "describe":
        return runtime.describe(payload["id"], payload["version"], context)
    return runtime.invoke(payload["id"], payload["version"], payload["catalogVersion"],
                          payload["input"], context, request_id=payload.get("requestId"))
