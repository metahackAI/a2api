"""discover / describe / invoke with deterministic read-only composition."""

from __future__ import annotations

import threading
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from uuid import uuid4

from .catalog import Catalog
from .errors import A2APIError, contract_error
from .execution import Budget
from .http_adapter import HTTPAdapter
from .ir import ExecutionContext, ValueRef, thaw
from .pointers import resolve
from .schema import validate_value


class Runtime:
    def __init__(self, catalog: Catalog, adapter: HTTPAdapter):
        self.catalog = catalog
        self.adapter = adapter
        for capability in catalog.capabilities:
            if capability.enabled:
                for operation in capability.operations.values():
                    if not adapter.has_binding(operation):
                        raise contract_error("An active operation has no deployed HTTP binding")

    def discover(self, query: str, context: ExecutionContext, **options) -> dict:
        return self.catalog.discover(query, context, **options)

    def describe(self, capability_id: str, version: str, context: ExecutionContext) -> dict:
        return self.catalog.describe(capability_id, version, context)

    def invoke(self, capability_id: str, version: str, catalog_version: str,
               input: dict, context: ExecutionContext, *, request_id: str | None = None) -> dict:
        capability = self.catalog.get(capability_id, version, context)
        if catalog_version != self.catalog.version:
            raise A2APIError("CONTRACT_DRIFT", "Catalog changed; discover and describe again.", status=409)
        if request_id is not None and (not isinstance(request_id, str) or not 1 <= len(request_id) <= 128):
            raise A2APIError("INVALID_REQUEST", "requestId must be a nonempty string of at most 128 characters.")
        # Detach trusted context and caller input from concurrent caller mutations.
        try:
            input = json.loads(json.dumps(input, allow_nan=False))
        except (TypeError, ValueError):
            raise A2APIError("INVALID_INPUT", "Input must contain finite JSON values.", status=422) from None
        validate_value(capability.input_schema, input, code="INVALID_INPUT", status=422)
        budget = Budget(capability.execution["deadlineMs"], capability.execution["maxBackendCalls"])
        result = {
            "capability": capability.id, "version": capability.version,
            "catalogVersion": self.catalog.version, "executionId": "exec-" + uuid4().hex,
            "requestId": request_id or uuid4().hex,
        }
        values = {}
        evidence = []
        evidence_lock = threading.Lock()

        def value(ref: ValueRef, item: object = None) -> object:
            source = {"input": input, "context": context.values(), "item": item}
            if ref.source == "step":
                return resolve(values[ref.step], ref.pointer)
            if ref.source == "literal":
                return thaw(ref.value)
            return resolve(source[ref.source], ref.pointer)

        def call(step, item=None, index=0):
            budget.remaining()
            operation = capability.operations[step.operation_id]
            arguments = {}
            for key, ref in step.inputs.items():
                try:
                    arguments[key] = value(ref, item)
                except A2APIError as error:
                    if error.code != "MAPPING_ERROR" or key in operation.input_schema.get("required", []):
                        raise
            validate_value(operation.input_schema, arguments, code="INVALID_INPUT", status=422)
            data = self.adapter.call(operation, arguments, context, budget, capability.execution["backendTimeoutMs"])
            validate_value(operation.output_schema, data, code="SCHEMA_MISMATCH", status=502)
            for check in step.checks:
                if resolve(data, check.result_pointer) != value(check.equals, item):
                    status = 403 if check.code == "PERMISSION_DENIED" else 502
                    raise A2APIError(check.code, "Backend result failed an identity or relationship check.", status=status)
            budget.remaining()
            with evidence_lock:
                evidence.append({"step": step.id, "itemIndex": index, "operation": operation.id,
                                 "source": operation.service_ref, "observedAt": datetime.now(timezone.utc).isoformat()})
            return {key: data[key] for key in step.select} if step.select else data

        try:
            for step in capability.steps:
                budget.remaining()
                if step.foreach is None:
                    values[step.id] = call(step)
                    continue
                items = value(step.foreach)
                if not isinstance(items, list) or len(items) > step.max_items:
                    raise A2APIError("FANOUT_EXCEEDED", "Collection exceeds the declared execution bound.", status=502)
                if not items:
                    values[step.id] = []
                    continue
                outputs = [None] * len(items)
                with ThreadPoolExecutor(max_workers=min(step.parallelism, len(items))) as pool:
                    futures = {pool.submit(call, step, item, index): index for index, item in enumerate(items)}
                    try:
                        for future in as_completed(futures):
                            outputs[futures[future]] = future.result()
                    except Exception:
                        budget.cancelled.set()
                        for future in futures:
                            future.cancel()
                        raise
                values[step.id] = outputs
            data = {key: value(ref) for key, ref in capability.outputs.items()}
            validate_value(capability.output_schema, data, code="SCHEMA_MISMATCH", status=502)
            budget.remaining()
            result.update(status="succeeded", data=data, completeness={"complete": True},
                          presentation=capability.describe()["presentation"])
        except A2APIError as error:
            budget.cancelled.set()
            result.update(status="failed", error=error.problem(), completeness={"complete": False})
        order = {s.id: index for index, s in enumerate(capability.steps)}
        result["evidence"] = sorted(evidence, key=lambda e: (order[e["step"]], e["itemIndex"]))
        result["stats"] = {"backendCalls": budget.calls}
        return result
