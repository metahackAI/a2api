"""Catalog-independent MCP envelopes. Business schemas stay in describe/runtime."""

from __future__ import annotations


def _object(properties: dict, required: list[str] | None = None) -> dict:
    return {"type": "object", "properties": properties,
            "required": list(properties) if required is None else required, "additionalProperties": False}


def output_schemas(runtime=None, context=None) -> dict[str, dict]:
    # Arguments are retained for callers of the previous helper. Neither a
    # catalog nor its individual schemas are part of the advertised envelopes.
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
    metadata = {
        "capability": string, "version": string, "catalogVersion": string,
        "executionId": string, "requestId": string, "evidence": evidence,
        "stats": _object({"backendCalls": {"type": "integer", "minimum": 0}}),
    }
    success = _object({
        **metadata, "status": {"const": "succeeded"}, "data": {},
        "completeness": _object({"complete": {"const": True}, "scope": string}, ["complete"]),
        "presentation": {"type": "object"},
        "httpStatus": {"type": "integer", "minimum": 200, "maximum": 299},
    }, ["status", "data", "completeness"])
    failure = _object({
        **metadata, "status": {"const": "failed"}, "error": problem,
        "completeness": _object({"complete": {"const": False}}, ["complete"]),
    }, ["status", "error", "completeness"])
    descriptor = _object({
        "id": string, "version": string, "summary": string,
        "effects": _object({"kind": {"const": "read"}}),
        "inputSchema": {"type": "object"}, "outputSchema": {"type": "object"},
    })
    successes = {
        "discover": _object({
            "catalogVersion": string,
            "capabilities": {"type": "array", "items": _object({
                "id": string, "version": string, "title": string, "summary": string,
                "effects": {"type": "object"}, "matchedTerms": {"type": "array", "items": string},
            })},
            "nextCursor": {"type": ["string", "null"]},
        }),
        "describe": _object({"catalogVersion": string, "capability": descriptor}),
    }
    result = {name: {"type": "object", "oneOf": [schema, preflight_error]} for name, schema in successes.items()}
    result["invoke"] = {"type": "object", "oneOf": [preflight_error, failure, success]}
    return result
