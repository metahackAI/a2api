"""Compile validated contracts into immutable IR before registering them."""

from __future__ import annotations

import json
import math
from importlib.resources import files
from pathlib import Path

from jsonschema import Draft202012Validator

from .errors import A2APIError, contract_error
from .ir import Capability, Check, Operation, Step, ValueRef, freeze
from .pointers import schema_at, tokens
from .schema import check_schema, compatible, validate_value
from .openapi_schema import check_draft_schema

META = json.loads(files("a2api").joinpath("schemas/capability.schema.json").read_text())
CONTEXT_SCHEMA = {"type": "object", "properties": {"actor": {"type": "string"}, "tenant": {"type": "string"}}, "required": ["actor", "tenant"]}


def parse_json(text: str) -> object:
    def pairs(items: list) -> dict:
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("Duplicate JSON key")
            result[key] = value
        return result

    def invalid_constant(value: str) -> None:
        raise ValueError("Non-finite JSON number")

    def finite_float(value: str) -> float:
        result = float(value)
        if not math.isfinite(result):
            raise ValueError("Non-finite JSON number")
        return result

    return json.loads(text, object_pairs_hook=pairs, parse_constant=invalid_constant, parse_float=finite_float)


def load_contract(path: str | Path) -> Capability:
    try:
        manifest = parse_json(Path(path).read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as exc:
        raise contract_error("Contract must contain strict UTF-8 JSON") from exc
    return compile_contract(manifest)


def compile_contract(manifest: dict) -> Capability:
    errors = list(Draft202012Validator(META).iter_errors(manifest))
    if errors:
        issues = [{"path": "/" + "/".join(map(str, e.absolute_path)), "rule": e.validator} for e in errors[:10]]
        raise A2APIError("INVALID_CONTRACT", "Contract does not match the MVP profile.", issues=issues)
    # Roundtrip detaches all IR data from the caller and rejects non-JSON values.
    try:
        serialized = json.dumps(manifest, ensure_ascii=False, sort_keys=True, allow_nan=False)
        manifest = json.loads(serialized)
    except (TypeError, ValueError):
        raise contract_error("Contract must be JSON-serializable") from None
    schemas = [manifest["inputSchema"], manifest["outputSchema"]]
    for operation in manifest["operations"]:
        schemas.extend([operation["inputSchema"], operation["outputSchema"]])
    imported = manifest.get("schemaProfile", "mvp") == "openapi-draft"
    if imported and (manifest["enabled"] or manifest["lifecycle"] != "draft"
                     or manifest["provenance"]["kind"] != "source"
                     or manifest["provenance"]["reviewState"] != "unreviewed"):
        raise contract_error("The openapi-draft schema profile is for disabled, unreviewed source imports only")
    checked = set()
    for schema in schemas:
        if imported:
            key = json.dumps(schema, sort_keys=True, separators=(",", ":"))
            if key not in checked:
                check_draft_schema(schema)
                checked.add(key)
        else:
            check_schema(schema, manifest["semanticTypes"])
        if schema["type"] != "object":
            raise contract_error("Capability and operation roots must be objects")
    for example in manifest["examples"]:
        if "input" in example:
            validate_value(manifest["inputSchema"], example["input"], code="INVALID_CONTRACT", status=400)
    operations = {}
    for raw in manifest["operations"]:
        if raw["id"] in operations:
            raise contract_error("Duplicate operation ID")
        operations[raw["id"]] = Operation(raw["id"], raw["serviceRef"], raw["operationRef"],
                                           freeze(raw["inputSchema"]), freeze(raw["outputSchema"]))
    raw_steps = {}
    for raw in manifest["binding"]["steps"]:
        if raw["id"] in raw_steps or raw["operationId"] not in operations:
            raise contract_error("Duplicate step ID or unknown operation")
        raw_steps[raw["id"]] = raw
    dependencies = {}
    for name, raw in raw_steps.items():
        refs = list(raw["input"].values()) + [c["equals"] for c in raw.get("checks", [])]
        if "foreach" in raw:
            refs.append(raw["foreach"])
        deps = set(raw.get("dependsOn", [])) | {r["step"] for r in refs if r["from"] == "step"}
        if name in deps or not deps.issubset(raw_steps):
            raise contract_error("Self dependency or unknown step reference")
        dependencies[name] = deps
    ordered = []
    while len(ordered) < len(raw_steps):
        ready = [name for name in raw_steps if name not in ordered and dependencies[name].issubset(ordered)]
        if not ready:
            raise contract_error("Cyclic step dependencies")
        ordered.extend(ready)
    steps = []
    output_schemas = {}

    def ref_schema(ref: ValueRef, item_schema: dict | None = None, *, required: bool = True) -> dict:
        tokens(ref.pointer)
        if ref.source == "literal":
            raise contract_error("Literal mappings are outside the executable MVP profile")
        source = {"input": manifest["inputSchema"], "context": CONTEXT_SCHEMA, "item": item_schema}.get(ref.source)
        if ref.source == "step":
            source = output_schemas.get(ref.step)
        if source is None:
            raise contract_error("Mapping source is unavailable")
        return schema_at(source, ref.pointer, require_required=required)

    for name in ordered:
        raw = raw_steps[name]
        operation = operations[raw["operationId"]]
        foreach = ValueRef.from_dict(raw["foreach"]) if "foreach" in raw else None
        item_schema = None
        if foreach:
            collection = ref_schema(foreach)
            if collection.get("type") != "array":
                raise contract_error("foreach source must be an array")
            if collection.get("maxItems", float("inf")) > raw["maxItems"]:
                raise contract_error("foreach source exceeds its declared bound")
            item_schema = collection["items"]
        elif any(k in raw for k in ("maxItems", "parallelism", "emptyCollection")):
            raise contract_error("Collection options require foreach")
        inputs = {key: ValueRef.from_dict(ref) for key, ref in raw["input"].items()}
        required = set(operation.input_schema.get("required", []))
        properties = operation.input_schema.get("properties", {})
        if not required.issubset(inputs) or not set(inputs).issubset(properties):
            raise contract_error("Step inputs do not cover exactly declared operation fields")
        for key, ref in inputs.items():
            compatible(ref_schema(ref, item_schema, required=key in required), properties[key])
        checks = []
        for check in raw.get("checks", []):
            ref = ValueRef.from_dict(check["equals"])
            compatible(schema_at(operation.output_schema, check["resultPointer"]), ref_schema(ref, item_schema))
            checks.append(Check(check["resultPointer"], ref, check["code"]))
        result_schema = operation.output_schema
        select = tuple(raw["select"]) if "select" in raw else None
        if select:
            if not set(select).issubset(result_schema.get("required", [])):
                raise contract_error("Selected result fields must be declared and required")
            result_schema = {"type": "object", "properties": {k: result_schema["properties"][k] for k in select},
                             "required": list(select), "additionalProperties": False}
        steps.append(Step(name, operation.id, freeze(inputs), tuple(sorted(dependencies[name])), tuple(checks),
                          foreach, raw.get("maxItems", 1), raw.get("parallelism", 1), select))
        output_schemas[name] = ({"type": "array", "items": result_schema, "maxItems": raw["maxItems"]}
                                if foreach else result_schema)
    outputs = {key: ValueRef.from_dict(value) for key, value in manifest["binding"]["output"].items()}
    target = manifest["outputSchema"]
    if not set(target.get("required", [])).issubset(outputs) or not set(outputs).issubset(target["properties"]):
        raise contract_error("Output mapping does not cover declared result fields")
    for key, ref in outputs.items():
        compatible(ref_schema(ref), target["properties"][key])
    worst_case = sum(s.max_items if s.foreach else 1 for s in steps)
    if worst_case > manifest["execution"]["maxBackendCalls"]:
        raise contract_error("Worst-case composition exceeds the backend call budget")
    if manifest["enabled"]:
        if manifest["lifecycle"] != "reviewed" or manifest["provenance"]["reviewState"] != "reviewed":
            raise contract_error("An enabled capability must be reviewed")
        if manifest["provenance"]["kind"] == "illustrative":
            raise contract_error("Illustrative contracts cannot be enabled")
        if set(manifest["contextRequirements"]) != {"actor", "tenant"}:
            raise contract_error("Active MVP capabilities require actor and tenant context")
        if manifest["policy"]["resourceRelationshipCheck"] != "explicit_checks":
            raise contract_error("Active MVP policies must use explicit response checks")
        for effect in [manifest["effects"]] + [r["effects"] for r in manifest["operations"]]:
            if effect["kind"] != "read" or effect["externalWrites"]:
                raise contract_error("The MVP executes read-only operations only")
        for step in steps:
            protected = {c.equals.pointer for c in step.checks if c.equals.source == "context" and c.code == "PERMISSION_DENIED"}
            if not {"/actor", "/tenant"}.issubset(protected):
                raise contract_error("Every active step needs actor and tenant checks")
            for key, ref in step.inputs.items():
                if operations[step.operation_id].input_schema["properties"][key].get("x-a2api-semanticType"):
                    if not any(c.equals == ref and c.code == "CONTRACT_DRIFT" for c in step.checks):
                        raise contract_error("Semantic identifiers need request/response identity checks")
    return Capability(manifest["id"], manifest["version"], manifest["title"], manifest["enabled"],
                      manifest["provenance"]["kind"] != "source", frozenset(manifest["policy"]["requiredScopes"]),
                      freeze(manifest["inputSchema"]), freeze(manifest["outputSchema"]), freeze(operations),
                      tuple(steps), freeze(outputs), freeze(manifest["execution"]), serialized)
