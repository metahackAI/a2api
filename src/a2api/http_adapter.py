"""Explicit deployment bindings for GET-only JSON HTTP operations."""

from __future__ import annotations

import http.client
import math
import re
import socket
import time
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping
from urllib.parse import quote, quote_plus, urlencode, urlsplit

from .contracts import parse_json
from .errors import A2APIError, contract_error
from .execution import Budget
from .ir import ExecutionContext, Operation
from .pointers import resolve, tokens


@dataclass(frozen=True)
class HTTPQueryParameter:
    pointer: str
    required: bool = False
    explode: bool = True

    def __post_init__(self) -> None:
        tokens(self.pointer)
        if type(self.required) is not bool or type(self.explode) is not bool:
            raise contract_error("Query parameter required/explode must be booleans")


def _query_scalar(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str) or type(value) is int:
        return str(value)
    if isinstance(value, float) and math.isfinite(value):
        return str(value)
    raise A2APIError("INVALID_INPUT", "Query values must be finite scalars or arrays of scalars.", status=422)


@dataclass(frozen=True)
class HTTPRoute:
    base_url: str
    path: str
    path_parameters: Mapping[str, str] = field(default_factory=dict)
    headers: Mapping[str, str] = field(default_factory=dict)
    query_parameters: Mapping[str, HTTPQueryParameter] = field(default_factory=dict)
    response_envelope: str | None = None

    def __post_init__(self) -> None:
        parsed = urlsplit(self.base_url)
        try:
            parsed.port
        except ValueError:
            raise contract_error("Invalid HTTP origin port") from None
        if (parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username or parsed.password
                or parsed.query or parsed.fragment or parsed.path not in ("", "/")):
            raise contract_error("HTTP service URLs must be explicit HTTP(S) origins")
        if not self.path.startswith("/") or self.path.startswith("//") or "?" in self.path or "#" in self.path:
            raise contract_error("HTTP paths must be absolute origin-relative paths")
        names = set(re.findall(r"\{([A-Za-z][A-Za-z0-9_]*)\}", self.path))
        if names != set(self.path_parameters) or re.search(r"[{}]", re.sub(r"\{[A-Za-z][A-Za-z0-9_]*\}", "", self.path)):
            raise contract_error("HTTP path placeholders do not match their parameter bindings")
        if any(k.lower() in {"host", "x-a2api-actor", "x-a2api-tenant"} for k in self.headers):
            raise contract_error("Deployment headers cannot override trusted routing/context")
        if any(not isinstance(name, str) or not name or not isinstance(binding, HTTPQueryParameter)
               for name, binding in self.query_parameters.items()):
            raise contract_error("Query bindings must map names to HTTPQueryParameter values")
        if self.response_envelope is not None and (not isinstance(self.response_envelope, str) or not self.response_envelope):
            raise contract_error("Response envelope must be a nonempty field name")
        object.__setattr__(self, "path_parameters", MappingProxyType(dict(self.path_parameters)))
        object.__setattr__(self, "headers", MappingProxyType(dict(self.headers)))
        object.__setattr__(self, "query_parameters", MappingProxyType(dict(self.query_parameters)))


class HTTPAdapter:
    def __init__(self, routes: Mapping[tuple[str, str], HTTPRoute], *, max_response_bytes: int = 1_048_576):
        if type(max_response_bytes) is not int or max_response_bytes < 1:
            raise contract_error("HTTP response limit must be a positive integer")
        self._routes = MappingProxyType(dict(routes))
        self.max_response_bytes = max_response_bytes

    def has_binding(self, operation: Operation) -> bool:
        return (operation.service_ref, operation.operation_ref) in self._routes

    def call(self, operation: Operation, arguments: dict, context: ExecutionContext,
             budget: Budget, timeout_ms: int) -> object:
        route = self._routes.get((operation.service_ref, operation.operation_ref))
        if route is None:
            raise A2APIError("BINDING_NOT_FOUND", "No deployed HTTP binding exists.", status=503)
        path = route.path
        for name, pointer in route.path_parameters.items():
            value = resolve(arguments, pointer)
            text = _query_scalar(value)
            if text in (".", ".."):
                raise A2APIError("INVALID_INPUT", "HTTP path arguments cannot be relative path segments.", status=422)
            path = path.replace("{" + name + "}", quote(text, safe=""))
        query = []
        for name, binding in route.query_parameters.items():
            try:
                value = resolve(arguments, binding.pointer)
            except A2APIError as error:
                if error.code != "MAPPING_ERROR":
                    raise
                if binding.required:
                    raise A2APIError("INVALID_INPUT", "A required query parameter is absent.", status=422) from None
                continue
            if isinstance(value, (list, tuple)):
                values = [_query_scalar(item) for item in value]
                if not values:
                    raise A2APIError("INVALID_INPUT", "Empty query arrays have no representation in this form profile.", status=422)
                if binding.explode:
                    query.extend(urlencode({name: item}) for item in values)
                else:
                    # Delimiters remain literal; reserved characters inside each item are encoded.
                    query.append(quote_plus(name) + "=" + ",".join(quote_plus(item) for item in values))
            else:
                query.append(urlencode({name: _query_scalar(value)}))
        if query:
            path += "?" + "&".join(query)
        parsed = urlsplit(route.base_url)
        call_deadline = min(budget.deadline, time.monotonic() + timeout_ms / 1000)

        def remaining() -> float:
            result = min(budget.remaining(), call_deadline - time.monotonic())
            if result <= 0:
                raise A2APIError("DEADLINE_EXCEEDED", "Backend call deadline was exceeded.", status=504)
            return result

        cls = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
        connection = cls(parsed.hostname, parsed.port, timeout=remaining())
        headers = {**route.headers, "Accept": "application/json", "X-A2API-Actor": context.actor, "X-A2API-Tenant": context.tenant}
        budget.claim()
        response = None
        try:
            connection.connect()
            transport_socket = connection.sock
            transport_socket.settimeout(remaining())
            connection.request("GET", path, headers=headers)
            connection.sock.settimeout(remaining())
            response = connection.getresponse()
            if response.status != 200:
                code, status = {
                    401: ("PERMISSION_DENIED", 403), 403: ("PERMISSION_DENIED", 403),
                    404: ("RESOURCE_NOT_FOUND", 404), 429: ("RATE_LIMITED", 429),
                }.get(response.status, ("UPSTREAM_ERROR", 502))
                raise A2APIError(code, "Backend did not return a successful JSON result.", status=status)
            mime = response.getheader("Content-Type", "").split(";")[0].strip().lower()
            if mime != "application/json" and not (mime.startswith("application/") and mime.endswith("+json")):
                raise A2APIError("INVALID_RESPONSE", "Backend response is not JSON.", status=502)
            if response.getheader("Content-Encoding", "identity").lower() != "identity":
                raise A2APIError("INVALID_RESPONSE", "Compressed backend responses are unsupported.", status=502)
            body = bytearray()
            while not response.isclosed():
                transport_socket.settimeout(remaining())
                chunk = response.read1(min(65536, self.max_response_bytes + 1 - len(body)))
                if not chunk:
                    break
                body.extend(chunk)
                if len(body) > self.max_response_bytes:
                    raise A2APIError("RESPONSE_TOO_LARGE", "Backend result exceeds the response limit.", status=502)
            remaining()
            if response.length not in (None, 0):
                raise A2APIError("INVALID_RESPONSE", "Backend response ended before its declared length.", status=502)
            try:
                payload = parse_json(body.decode("utf-8"))
                return {route.response_envelope: payload} if route.response_envelope is not None else payload
            except (ValueError, UnicodeError):
                raise A2APIError("INVALID_RESPONSE", "Backend did not return strict UTF-8 JSON.", status=502) from None
        except (TimeoutError, socket.timeout):
            raise A2APIError("DEADLINE_EXCEEDED", "Backend call timed out.", status=504) from None
        except (OSError, http.client.HTTPException):
            raise A2APIError("UPSTREAM_UNAVAILABLE", "Backend connection failed.", status=502) from None
        finally:
            if response is not None:
                response.close()
            connection.close()
