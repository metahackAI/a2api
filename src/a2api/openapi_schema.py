"""Schema checks for disabled OpenAPI imports, separate from executable MVP schemas."""

from __future__ import annotations

from collections.abc import Iterator

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from .errors import A2APIError, contract_error
from .pointers import resolve

MAP_SCHEMAS = {"properties", "patternProperties", "$defs", "dependentSchemas"}
SINGLE_SCHEMAS = {"items", "additionalProperties", "unevaluatedProperties", "unevaluatedItems",
                  "propertyNames", "contains", "not", "if", "then", "else", "contentSchema"}
LIST_SCHEMAS = {"allOf", "anyOf", "oneOf", "prefixItems"}


def schema_nodes(schema: dict | bool, pointer: str = "") -> Iterator[tuple[str, dict]]:
    if isinstance(schema, bool):
        return
    if not isinstance(schema, dict):
        raise contract_error("Schema nodes must be objects or booleans")
    yield pointer, schema
    for key in MAP_SCHEMAS & schema.keys():
        for name, child in schema[key].items():
            escaped = name.replace("~", "~0").replace("/", "~1")
            yield from schema_nodes(child, f"{pointer}/{key}/{escaped}")
    for key in SINGLE_SCHEMAS & schema.keys():
        yield from schema_nodes(schema[key], f"{pointer}/{key}")
    for key in LIST_SCHEMAS & schema.keys():
        for index, child in enumerate(schema[key]):
            yield from schema_nodes(child, f"{pointer}/{key}/{index}")


def check_draft_schema(schema: dict) -> None:
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError:
        raise contract_error("Imported schema is not valid JSON Schema 2020-12") from None
    for _, node in schema_nodes(schema):
        if any(key in node for key in ("$id", "$anchor", "$dynamicRef", "$dynamicAnchor", "$vocabulary")):
            raise contract_error("Imported schemas cannot change reference scope or vocabulary")
        if "$schema" in node and node["$schema"] != "https://json-schema.org/draft/2020-12/schema":
            raise contract_error("Imported schemas must use the 2020-12 dialect")
        if "$ref" in node:
            ref = node["$ref"]
            if not isinstance(ref, str) or not ref.startswith("#/$defs/"):
                raise contract_error("Imported schemas may reference bundled local definitions only")
            try:
                resolve(schema, ref[1:])
            except A2APIError:
                raise contract_error("Imported schema has an unresolved local reference") from None
