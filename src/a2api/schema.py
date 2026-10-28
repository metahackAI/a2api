"""A deliberately closed JSON Schema 2020-12 profile for the MVP."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Mapping

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError

from .errors import A2APIError, contract_error
from .ir import thaw

SCHEMA_URI = "https://json-schema.org/draft/2020-12/schema"
KEYWORDS = {
    "$schema", "type", "properties", "required", "additionalProperties", "items",
    "minItems", "maxItems", "uniqueItems", "minLength", "maxLength", "minimum",
    "maximum", "enum", "const", "format", "title", "description", "examples",
    "x-a2api-semanticType",
}
FORMATS = FormatChecker(formats=[])


@FORMATS.checks("date-time")
def is_datetime(value: object) -> bool:
    if not isinstance(value, str):
        return True
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}[Tt](?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:\.\d+)?(?:[Zz]|[+-](?:[01]\d|2[0-3]):[0-5]\d)", value):
        return False
    try:
        datetime.fromisoformat(value.upper().replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def check_schema(schema: dict, semantic_types: dict) -> None:
    if not isinstance(schema, dict):
        raise contract_error("The MVP requires object-valued schemas")
    unknown = set(schema) - KEYWORDS
    if unknown:
        raise contract_error("Unsupported schema keyword: " + ", ".join(sorted(unknown)))
    if schema.get("$schema", SCHEMA_URI) != SCHEMA_URI:
        raise contract_error("Unsupported schema dialect")
    if schema.get("format") not in (None, "date-time"):
        raise contract_error("Unsupported format; the MVP supports date-time only")
    if "type" not in schema:
        raise contract_error("Every schema node must declare its type")
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError:
        raise contract_error("Invalid JSON Schema structure") from None
    semantic = schema.get("x-a2api-semanticType")
    if semantic:
        if semantic not in semantic_types or schema["type"] != semantic_types[semantic]["baseType"]:
            raise contract_error("Unknown or incompatible semantic type")
    if schema["type"] == "object":
        if schema.get("additionalProperties") is not False:
            raise contract_error("MVP object schemas must be closed")
        for child in schema.get("properties", {}).values():
            check_schema(child, semantic_types)
        if not set(schema.get("required", [])).issubset(schema.get("properties", {})):
            raise contract_error("Required field is not declared")
    elif schema["type"] == "array":
        if "items" not in schema:
            raise contract_error("Array items must have a schema")
        check_schema(schema["items"], semantic_types)
    elif any(key in schema for key in ("properties", "items", "additionalProperties", "required")):
        raise contract_error("Object/array keywords require the corresponding single type")


def validate_value(schema: Mapping, value: object, *, code: str, status: int) -> None:
    errors = list(Draft202012Validator(thaw(schema), format_checker=FORMATS).iter_errors(value))
    if errors:
        # ValidationError.message may contain private data; return paths/rules only.
        issues = [{"path": "/" + "/".join(str(x) for x in e.absolute_path), "rule": e.validator}
                  for e in errors[:10]]
        raise A2APIError(code, "Value does not conform to the declared schema.", status=status, issues=issues)


def compatible(source: Mapping, target: Mapping) -> None:
    def types(s: Mapping) -> set:
        t = s.get("type")
        return {t} if isinstance(t, str) else set(t)
    if not types(source).issubset(types(target)):
        raise contract_error("Mapping has incompatible JSON types")
    if source.get("x-a2api-semanticType") != target.get("x-a2api-semanticType"):
        raise contract_error("Mapping has incompatible semantic types")
    if source.get("type") == "array" and target.get("type") == "array":
        compatible(source["items"], target["items"])
    if source.get("type") == "object" and target.get("type") == "object":
        for key in target.get("required", []):
            if key not in source.get("required", []):
                raise contract_error("Mapped object may omit a required field")
        for key, child in source.get("properties", {}).items():
            if key not in target.get("properties", {}):
                raise contract_error("Mapped object has an undeclared field")
            compatible(child, target["properties"][key])
