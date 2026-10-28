"""Convert supported OAS 3.0/3.1 schemas without flattening unions or opening refs."""

from __future__ import annotations

import hashlib
from urllib.parse import unquote

from jsonschema import Draft202012Validator

from ..errors import A2APIError
from ..openapi_schema import LIST_SCHEMAS, MAP_SCHEMAS, SINGLE_SCHEMAS, schema_nodes
from ..pointers import resolve


class ImportIssue(Exception):
    def __init__(self, code: str, message: str, location: str):
        super().__init__(message)
        self.code, self.message, self.location = code, message, location

    def diagnostic(self, severity: str = "error") -> dict:
        return {"code": self.code, "message": self.message, "location": self.location, "severity": severity}


def escape(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def local_reference(document: dict, reference: str, location: str):
    if not isinstance(reference, str) or not reference.startswith("#/"):
        raise ImportIssue("EXTERNAL_REFERENCE", "Only references inside the supplied document are supported; no network or filesystem lookup is performed.", location)
    try:
        return resolve(document, unquote(reference[1:]))
    except A2APIError:
        raise ImportIssue("UNRESOLVED_REFERENCE", "Reference target is absent from the supplied document.", location) from None


ANNOTATIONS = {"type", "$ref", "$schema", "$defs", "$comment", "title", "description", "default", "examples",
               "readOnly", "writeOnly", "deprecated", "format", "contentMediaType", "contentEncoding",
               "discriminator", "xml", "externalDocs", "example"}
KNOWN = set(Draft202012Validator.VALIDATORS) | ANNOTATIONS


class SchemaConverter:
    def __init__(self, document: dict, *, max_definitions: int = 2048):
        self.document = document
        self.oas30 = document["openapi"].startswith("3.0.")
        self.max_definitions = max_definitions
        self._names = {}
        self._references = {}
        self._cache = {}
        self._warnings = {}
        self._local_warnings = []

    def _name(self, reference: str, location: str) -> str:
        local_reference(self.document, reference, location)
        if reference not in self._names:
            name = "ref_" + hashlib.sha256(reference.encode()).hexdigest()[:20]
            if name in self._references and self._references[name] != reference:
                raise ImportIssue("REFERENCE_COLLISION", "Reference identifiers collide.", location)
            self._names[reference] = name
            self._references[name] = reference
        return self._names[reference]

    def _convert(self, schema, location: str, depth: int = 0):
        if depth > 128:
            raise ImportIssue("SCHEMA_DEPTH", "Schema exceeds the supported structural depth.", location)
        if isinstance(schema, bool):
            return schema
        if not isinstance(schema, dict):
            raise ImportIssue("INVALID_SCHEMA", "Schema nodes must be objects or booleans.", location)
        for name in schema.get('required', []) if isinstance(schema.get('required', []), list) else []:
            if not isinstance(name, str):
                raise ImportIssue('INVALID_SCHEMA', 'Required property names must be strings.', location)
            child = schema.get('properties', {}).get(name, {}) if isinstance(schema.get('properties', {}), dict) else {}
            if isinstance(child, dict) and child.get('writeOnly') is True:
                raise ImportIssue('WRITE_ONLY_RESPONSE_REQUIREMENT', 'A response schema requires a writeOnly field; contextual projection needs explicit review.', location)
        if any(key in schema for key in ("$id", "$anchor", "$dynamicRef", "$dynamicAnchor", "$vocabulary")):
            raise ImportIssue("UNSUPPORTED_SCHEMA_SCOPE", "Custom schema scopes and dynamic references require a separate dialect implementation.", location)
        dialect = schema.get("$schema")
        if dialect not in (None, "https://json-schema.org/draft/2020-12/schema", "https://spec.openapis.org/oas/3.1/dialect/base"):
            raise ImportIssue("UNSUPPORTED_SCHEMA_DIALECT", "Only OAS 3.1 base and JSON Schema 2020-12 dialects are supported.", location)
        if self.oas30 and "$ref" in schema:
            if set(schema) - {"$ref"}:
                self._local_warnings.append(ImportIssue("OAS30_REF_SIBLINGS", "OAS 3.0 ignores siblings of a Reference Object; they are recorded here and not applied.", location).diagnostic("warning"))
            return {"$ref": "#/$defs/" + self._name(schema["$ref"], location + "/$ref")}
        unknown = {key for key in schema if key not in KNOWN and not key.startswith("x-")}
        if self.oas30:
            unknown.discard("nullable")
        if unknown:
            raise ImportIssue("UNSUPPORTED_SCHEMA_KEYWORD", "Unsupported schema keyword: " + ", ".join(sorted(unknown)), location)
        converted = {}
        for key, value in schema.items():
            where = location + "/" + escape(key)
            if key in ("$schema", "nullable") and (key == "$schema" or self.oas30):
                continue
            if key == "$ref":
                converted[key] = "#/$defs/" + self._name(value, where)
            elif key in MAP_SCHEMAS:
                if not isinstance(value, dict):
                    raise ImportIssue("INVALID_SCHEMA", "Schema maps must be objects.", where)
                converted[key] = {name: self._convert(child, where + "/" + escape(name), depth + 1)
                                  for name, child in value.items()}
            elif key in SINGLE_SCHEMAS:
                converted[key] = self._convert(value, where, depth + 1)
            elif key in LIST_SCHEMAS:
                if not isinstance(value, list):
                    raise ImportIssue("INVALID_SCHEMA", "Schema alternatives must be arrays.", where)
                converted[key] = [self._convert(child, where + "/" + str(index), depth + 1) for index, child in enumerate(value)]
            elif self.oas30 and key in ("exclusiveMinimum", "exclusiveMaximum"):
                if type(value) is not bool:
                    raise ImportIssue("INVALID_SCHEMA", "OAS 3.0 exclusive bounds must be booleans.", where)
                if value:
                    bound = "minimum" if key == "exclusiveMinimum" else "maximum"
                    if bound not in schema:
                        raise ImportIssue("INVALID_SCHEMA", "Exclusive bound has no corresponding numeric limit.", where)
                    converted[key] = schema[bound]
            else:
                converted[key] = value
        if self.oas30 and schema.get("nullable") is True:
            declared = schema.get("type")
            if isinstance(declared, str):
                converted["type"] = [declared, "null"]
            else:
                self._local_warnings.append(ImportIssue("NULLABLE_WITHOUT_TYPE", "OAS 3.0 nullable has no effect without an explicit type; no null branch was invented.", location).diagnostic("warning"))
        if "discriminator" in schema:
            self._local_warnings.append(ImportIssue("DISCRIMINATOR_ANNOTATION", "Discriminator metadata is retained; JSON Schema alternatives determine validation.", location).diagnostic("warning"))
        return converted

    def convert(self, schema, location: str):
        self._local_warnings = []
        result = self._convert(schema, location)
        return result, list(self._local_warnings)

    def bundle(self, roots: list) -> tuple[dict, list[dict], dict]:
        definitions = {}
        warnings = []
        pending = []
        for root in roots:
            pending.extend(node["$ref"].split("/")[-1] for _, node in schema_nodes(root) if "$ref" in node)
        while pending:
            name = pending.pop()
            if name in definitions:
                continue
            if len(definitions) >= self.max_definitions:
                raise ImportIssue("REFERENCE_LIMIT", "Too many reachable definitions in one operation.", "#/components/schemas")
            reference = self._references[name]
            if name not in self._cache:
                target = local_reference(self.document, reference, reference)
                self._local_warnings = []
                self._cache[name] = self._convert(target, reference[1:])
                self._warnings[name] = list(self._local_warnings)
            definition = self._cache[name]
            definitions[name] = definition
            warnings.extend(self._warnings[name])
            pending.extend(node["$ref"].split("/")[-1] for _, node in schema_nodes(definition) if "$ref" in node)
        ordered = dict(sorted(definitions.items()))
        return ordered, warnings, {name: self._references[name] for name in ordered}
