"""Shared request contracts for HTTP and MCP bindings."""

from __future__ import annotations

from jsonschema import Draft202012Validator

from .errors import A2APIError
from .ir import ExecutionContext
from .runtime import Runtime
from .protocol import METHODS, request_schema

def input_schema(method: str) -> dict:
    return request_schema(method)


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
