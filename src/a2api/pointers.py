"""Strict JSON Pointer; no expression evaluation or string interpolation."""

from __future__ import annotations

import re
from typing import Any, Mapping

from .errors import A2APIError, contract_error


def tokens(pointer: str) -> list[str]:
    if pointer == "":
        return []
    if not pointer.startswith("/") or re.search(r"~(?![01])", pointer):
        raise contract_error("Invalid JSON Pointer")
    return [p.replace("~1", "/").replace("~0", "~") for p in pointer[1:].split("/")]


def resolve(value: Any, pointer: str) -> Any:
    for key in tokens(pointer):
        if isinstance(value, Mapping) and key in value:
            value = value[key]
        elif isinstance(value, (list, tuple)) and re.fullmatch(r"0|[1-9][0-9]*", key) and int(key) < len(value):
            value = value[int(key)]
        else:
            raise A2APIError("MAPPING_ERROR", "A required mapped value is absent.", status=502)
    return value


def schema_at(schema: Mapping, pointer: str) -> Mapping:
    for key in tokens(pointer):
        if schema.get("type") != "object" or key not in schema.get("properties", {}):
            raise contract_error("Mapping points outside a supported object schema")
        if key not in schema.get("required", []):
            raise contract_error("A mapped source field must be required")
        schema = schema["properties"][key]
    return schema
