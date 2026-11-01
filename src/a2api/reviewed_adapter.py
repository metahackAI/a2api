"""Reviewed field mappings around the original, validated HTTP wire contract."""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Callable, Mapping

from .errors import A2APIError, contract_error
from .execution import Budget
from .http_adapter import HTTPAdapter
from .importers import ImportRecord
from .ir import ExecutionContext, Operation
from .pointers import resolve, tokens
from .schema import validate_value


@dataclass(frozen=True)
class HTTPDeployment:
    """Host-owned origin, credentials and per-call limits. Calls are never retried."""

    base_url: str
    path_prefix: str = ''
    headers: Mapping[str, str] = field(default_factory=dict, repr=False)
    credential_provider: Callable[[ExecutionContext], Mapping[str, str]] | None = field(default=None, repr=False)
    timeout_ms: int = 1500
    deadline_ms: int = 5000
    max_response_bytes: int = 1_048_576
    # Host-owned query/body values per call: (context, call) -> {"query": {...}, "body": {...}}.
    # `call` names the operation: {"operationId", "method", "path"}. Never part of model input.
    request_values: Callable[[ExecutionContext, Mapping], Mapping] | None = field(default=None, repr=False)
    # Host opt-in: (status, parsed JSON body or None) -> a short message safe to show the caller.
    # Backend error bodies are otherwise never forwarded.
    error_detail: Callable[[int, object], str | None] | None = field(default=None, repr=False)
    # Host opt-in: header that carries the caller's requestId on writes (e.g. "Idempotency-Key").
    idempotency_header: str | None = None

    def __post_init__(self) -> None:
        for name, upper in (('timeout_ms', 600_000), ('deadline_ms', 600_000), ('max_response_bytes', 64 * 1_048_576)):
            value = getattr(self, name)
            if type(value) is not int or not 1 <= value <= upper:
                raise A2APIError('INVALID_DEPLOYMENT', name + ' must be a positive integer within the supported limit.')
        if self.timeout_ms > self.deadline_ms:
            raise A2APIError('INVALID_DEPLOYMENT', 'timeout_ms must not exceed deadline_ms.')
        if self.request_values is not None and not callable(self.request_values):
            raise A2APIError('INVALID_DEPLOYMENT', 'request_values must be callable.')
        if self.error_detail is not None and not callable(self.error_detail):
            raise A2APIError('INVALID_DEPLOYMENT', 'error_detail must be callable.')
        if self.idempotency_header is not None and (not isinstance(self.idempotency_header, str)
                or not re.fullmatch(r"[!#$%&'*+.^_`|~0-9A-Za-z-]+", self.idempotency_header)):
            raise A2APIError('INVALID_DEPLOYMENT', 'idempotency_header must be an HTTP header name.')


@dataclass(frozen=True)
class ReviewedOperation:
    operation: Operation
    source: ImportRecord
    inputs: Mapping
    outputs: Mapping


def _set_field(target: dict, pointer: str, value) -> None:
    path = tokens(pointer)
    for key in path[:-1]:
        target = target.setdefault(key, {})
    target[path[-1]] = value


class ReviewedHTTPAdapter:
    def __init__(self, plans: tuple[ReviewedOperation, ...], deployments: Mapping[str, HTTPDeployment], **limits):
        self._plans = {(p.operation.service_ref, p.operation.operation_ref): p for p in plans}
        routes = {}
        for plan in plans:
            wire = plan.source.capability.operations[plan.source.operation_id]
            deployment = deployments.get(wire.service_ref)
            if not isinstance(deployment, HTTPDeployment):
                raise contract_error('A host HTTPDeployment is required for each source service')
            route = plan.source.http_route(deployment.base_url, path_prefix=deployment.path_prefix,
                                           headers=dict(deployment.headers), credential_provider=deployment.credential_provider)
            routes[(wire.service_ref, wire.operation_ref)] = route
        self._wire = HTTPAdapter(routes, **limits)

    def has_binding(self, operation: Operation) -> bool:
        plan = self._plans.get((operation.service_ref, operation.operation_ref))
        return plan is not None and plan.operation == operation

    def call(self, operation: Operation, arguments: dict, context: ExecutionContext,
             budget: Budget, timeout_ms: int) -> object:
        if not self.has_binding(operation):
            raise contract_error('Reviewed operation differs from the built deployment contract')
        plan = self._plans[(operation.service_ref, operation.operation_ref)]
        validate_value(operation.input_schema, arguments, code='INVALID_INPUT', status=422)
        wire_arguments = {}
        for name, field in plan.inputs.items():
            if name in arguments:
                _set_field(wire_arguments, field['pointer'], arguments[name])
        wire = plan.source.capability.operations[plan.source.operation_id]
        # Preserve source validation before selecting reviewed result fields.
        raw = self._wire.call(wire, wire_arguments, context, budget, timeout_ms)
        result = {}
        for name, field in plan.outputs.items():
            try:
                result[name] = resolve(raw, field['pointer'])
            except A2APIError as error:
                if error.code != 'MAPPING_ERROR' or name in operation.output_schema.get('required', ()):
                    raise
        validate_value(operation.output_schema, result, code='SCHEMA_MISMATCH', status=502)
        return result
