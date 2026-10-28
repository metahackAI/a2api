"""MCP result schemas, including each visible capability's business output."""

from __future__ import annotations

from copy import deepcopy

from .errors import A2APIError
from .ir import ExecutionContext, thaw
from .runtime import Runtime


def _object(properties: dict, required: list[str] | None = None) -> dict:
    return {"type": "object", "properties": properties,
            "required": list(properties) if required is None else required, "additionalProperties": False}


def output_schemas(runtime: Runtime, context: ExecutionContext) -> dict[str, dict]:
    string = {"type": "string"}
    problem = _object({
        "type": string, "title": string, "status": {"type": "integer"}, "detail": string,
        "code": string, "issues": {"type": "array", "items": {"type": "object"}},
    }, ["type", "title", "status", "detail", "code"])
    preflight_error = _object({"error": problem})
    evidence = {"type": "array", "items": _object({
        "step": string, "itemIndex": {"type": "integer", "minimum": 0}, "operation": string,
        "source": string, "observedAt": {"type": "string", "format": "date-time"},
    })}
    common = {
        "capability": string, "version": string, "catalogVersion": string,
        "executionId": string, "requestId": string,
        "evidence": evidence, "stats": _object({"backendCalls": {"type": "integer", "minimum": 0}}),
    }
    invocation_variants = [preflight_error, _object({
        **common, "status": {"const": "failed"}, "error": problem,
        "completeness": _object({"complete": {"const": False}}),
    })]
    for capability in runtime.catalog.capabilities:
        try:
            visible = runtime.catalog.get(capability.id, capability.version, context)
        except A2APIError as error:
            if error.code == "NOT_FOUND":
                continue
            raise
        invocation_variants.append(_object({
            **common, "capability": {"const": visible.id}, "version": {"const": visible.version},
            "status": {"const": "succeeded"}, "data": thaw(visible.output_schema),
            "completeness": _object({"complete": {"const": True}}),
            "presentation": {"type": "object"},
        }))
    successes = {
        "discover": _object({
            "catalogVersion": string,
            "capabilities": {"type": "array", "items": _object({
                "id": string, "version": string, "title": string, "summary": string,
                "effects": {"type": "object"}, "matchedTerms": {"type": "array", "items": string},
            })},
            "nextCursor": {"type": ["string", "null"]},
        }),
        "describe": _object({"catalogVersion": string, "capability": {"type": "object"}}),
    }
    result = {name: {"type": "object", "oneOf": [schema, preflight_error]} for name, schema in successes.items()}
    result["invoke"] = {"type": "object", "oneOf": invocation_variants}
    return deepcopy(result)
