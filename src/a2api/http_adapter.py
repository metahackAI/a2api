"""Explicit HTTP bindings; mutation transport is separate from activation policy."""

from __future__ import annotations

import http.client
import json
import math
import re
import socket
import time
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Callable, Mapping
from urllib.parse import quote, quote_plus, urlencode, urlsplit

from .contracts import parse_json
from .errors import A2APIError, contract_error
from .execution import Budget
from .ir import ExecutionContext, Operation
from .pointers import resolve, tokens
from .schema import validate_value

HTTP_METHODS = frozenset({"GET", "HEAD", "POST", "PUT", "PATCH", "DELETE"})
MANAGED_HEADERS = frozenset({"host", "x-a2api-actor", "x-a2api-tenant", "accept", "accept-encoding",
                             "content-type", "content-length", "transfer-encoding", "connection", "expect", "upgrade", "trailer"})
SENSITIVE_HEADERS = frozenset({"authorization", "proxy-authorization", "cookie"})
HEADER_NAME = re.compile(r"[!#$%&'*+.^_`|~0-9A-Za-z-]+")


_UPSTREAM_DETAIL = {
    400: "The backend rejected the request values.",
    401: "The backend did not accept the caller's credentials.",
    403: "The backend denied access for this caller.",
    404: "The backend reported that the target does not exist.",
    409: "The backend reported that the current state does not allow this request.",
    422: "The backend rejected the request values.",
    429: "The backend is rate limiting this caller.",
    503: "The backend reported that it is temporarily unavailable.",
}


def json_media_type(value: str) -> bool:
    return isinstance(value, str) and (value == "application/json" or
            re.fullmatch(r"application/[a-z0-9!#$&^_.+-]+\+json", value) is not None)


def _header_values(headers: Mapping[str, str]) -> dict[str, str]:
    if not isinstance(headers, Mapping):
        raise contract_error("HTTP headers must be a mapping")
    result = {}
    for name, value in headers.items():
        if not isinstance(name, str) or not HEADER_NAME.fullmatch(name) or name.lower() in MANAGED_HEADERS:
            raise contract_error("HTTP headers cannot override managed routing, framing or context fields")
        if name.lower() in result:
            raise contract_error("HTTP header names must be unique ignoring case")
        if not isinstance(value, str) or any(ord(c) < 32 or ord(c) == 127 or ord(c) > 255 for c in value):
            raise contract_error("HTTP header values must be printable Latin-1 strings")
        result[name.lower()] = value
    return result


def _argument(arguments, pointer: str, required: bool):
    try:
        return True, resolve(arguments, pointer)
    except A2APIError as error:
        if error.code != "MAPPING_ERROR":
            raise
        if required:
            raise A2APIError("INVALID_INPUT", "A required HTTP argument is absent.", status=422) from None
        return False, None


@dataclass(frozen=True)
class HTTPHeaderParameter:
    pointer: str
    required: bool = False

    def __post_init__(self) -> None:
        tokens(self.pointer)
        if type(self.required) is not bool:
            raise contract_error("Header parameter required must be boolean")


@dataclass(frozen=True)
class HTTPResponse:
    """A declared success response. None denotes an empty body."""
    media_type: str | None = "application/json"

    def __post_init__(self) -> None:
        if self.media_type is not None and not json_media_type(self.media_type):
            raise contract_error("HTTP response codecs support JSON media types or an empty body")


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
    raise A2APIError("INVALID_INPUT", "HTTP parameter values must be finite scalars.", status=422)


@dataclass(frozen=True)
class HTTPRoute:
    base_url: str
    path: str
    path_parameters: Mapping[str, str] = field(default_factory=dict)
    headers: Mapping[str, str] = field(default_factory=dict, repr=False)
    query_parameters: Mapping[str, HTTPQueryParameter] = field(default_factory=dict)
    response_envelope: str | None = None
    method: str = "GET"
    request_body_pointer: str | None = None
    request_body_required: bool = False
    request_media_type: str = "application/json"
    responses: Mapping[int, HTTPResponse] = field(default_factory=lambda: {200: HTTPResponse()})
    response_status_field: str | None = None
    header_parameters: Mapping[str, HTTPHeaderParameter] = field(default_factory=dict)
    credential_provider: Callable[[ExecutionContext], Mapping[str, str]] | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        parsed = urlsplit(self.base_url)
        try:
            parsed.port
        except ValueError:
            raise contract_error("Invalid HTTP origin port") from None
        if (parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username or parsed.password
                or parsed.query or parsed.fragment or parsed.path not in ("", "/")):
            raise contract_error("HTTP service URLs must be explicit HTTP(S) origins")
        if (not self.path.startswith("/") or self.path.startswith("//") or "?" in self.path or "#" in self.path
                or not self.path.isascii() or any(ord(c) <= 32 or ord(c) == 127 for c in self.path)):
            raise contract_error("HTTP paths must be absolute origin-relative paths")
        names = set(re.findall(r"\{([A-Za-z][A-Za-z0-9_]*)\}", self.path))
        if names != set(self.path_parameters) or re.search(r"[{}]", re.sub(r"\{[A-Za-z][A-Za-z0-9_]*\}", "", self.path)):
            raise contract_error("HTTP path placeholders do not match their parameter bindings")
        _header_values(self.headers)
        if not isinstance(self.method, str) or self.method not in HTTP_METHODS:
            raise contract_error("Unsupported HTTP method; use an uppercase supported method")
        for pointer in self.path_parameters.values():
            tokens(pointer)
        if self.request_body_pointer is not None:
            tokens(self.request_body_pointer)
        if type(self.request_body_required) is not bool or (self.request_body_required and self.request_body_pointer is None):
            raise contract_error("Required request bodies need an explicit pointer")
        if self.method in {"GET", "HEAD"} and self.request_body_pointer is not None:
            raise contract_error("GET/HEAD request bodies are outside the HTTP adapter profile")
        if not json_media_type(self.request_media_type):
            raise contract_error("HTTP request bodies require an explicit JSON media type")
        if not self.responses or any(type(status) is not int or not 200 <= status <= 299 or not isinstance(response, HTTPResponse)
                                     for status, response in self.responses.items()):
            raise contract_error("HTTP routes must declare explicit 2xx success response codecs")
        if any((self.method == "HEAD" or status in {204, 205}) and response.media_type is not None
               for status, response in self.responses.items()):
            raise contract_error("HEAD/204/205 success responses must use an empty body codec")
        if any(not isinstance(name, str) or not name or not isinstance(binding, HTTPQueryParameter)
               for name, binding in self.query_parameters.items()):
            raise contract_error("Query bindings must map names to HTTPQueryParameter values")
        if self.response_envelope is not None and (not isinstance(self.response_envelope, str) or not self.response_envelope):
            raise contract_error("Response envelope must be a nonempty field name")
        if self.response_status_field is not None and (not isinstance(self.response_status_field, str) or
                not self.response_status_field or not self.response_envelope or self.response_status_field == self.response_envelope):
            raise contract_error("HTTP status metadata needs a distinct field inside a response envelope")
        for name, binding in self.header_parameters.items():
            _header_values({name: ""})
            if name.lower() in SENSITIVE_HEADERS or not isinstance(binding, HTTPHeaderParameter):
                raise contract_error("Caller header bindings cannot supply credentials")
        if len({name.lower() for name in self.header_parameters}) != len(self.header_parameters):
            raise contract_error("Header parameter names must be unique ignoring case")
        if {name.lower() for name in self.headers} & {name.lower() for name in self.header_parameters}:
            raise contract_error("Static and caller header bindings cannot overlap")
        if self.credential_provider is not None and not callable(self.credential_provider):
            raise contract_error("HTTP credential provider must be callable")
        object.__setattr__(self, "path_parameters", MappingProxyType(dict(self.path_parameters)))
        object.__setattr__(self, "headers", MappingProxyType(dict(self.headers)))
        object.__setattr__(self, "query_parameters", MappingProxyType(dict(self.query_parameters)))
        object.__setattr__(self, "header_parameters", MappingProxyType(dict(self.header_parameters)))
        object.__setattr__(self, "responses", MappingProxyType(dict(self.responses)))


class HTTPAdapter:
    def __init__(self, routes: Mapping[tuple[str, str], HTTPRoute], *, max_response_bytes: int = 1_048_576,
                 max_request_bytes: int = 1_048_576):
        if type(max_response_bytes) is not int or max_response_bytes < 1:
            raise contract_error("HTTP response limit must be a positive integer")
        self._routes = MappingProxyType(dict(routes))
        self.max_response_bytes = max_response_bytes
        if type(max_request_bytes) is not int or max_request_bytes < 1:
            raise contract_error("HTTP request limit must be a positive integer")
        self.max_request_bytes = max_request_bytes

    def has_binding(self, operation: Operation) -> bool:
        route = self._routes.get((operation.service_ref, operation.operation_ref))
        return route is not None and route.method == operation.http_method

    def call(self, operation: Operation, arguments: dict, context: ExecutionContext,
             budget: Budget, timeout_ms: int) -> object:
        route = self._routes.get((operation.service_ref, operation.operation_ref))
        if route is None:
            raise A2APIError("BINDING_NOT_FOUND", "No deployed HTTP binding exists.", status=503)
        if route.method != operation.http_method:
            raise contract_error("Deployed HTTP method differs from the operation contract")
        validate_value(operation.input_schema, arguments, code="INVALID_INPUT", status=422)
        path = route.path
        for name, pointer in route.path_parameters.items():
            value = resolve(arguments, pointer)
            text = _query_scalar(value)
            if text in (".", ".."):
                raise A2APIError("INVALID_INPUT", "HTTP path arguments cannot be relative path segments.", status=422)
            path = path.replace("{" + name + "}", quote(text, safe=""))
        query = []
        for name, binding in route.query_parameters.items():
            present, value = _argument(arguments, binding.pointer, binding.required)
            if not present:
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
        headers = _header_values(route.headers)
        for name, binding in route.header_parameters.items():
            present, value = _argument(arguments, binding.pointer, binding.required)
            if present:
                try:
                    headers.update(_header_values({name: _query_scalar(value)}))
                except A2APIError:
                    raise A2APIError("INVALID_INPUT", "An HTTP header argument is invalid.", status=422) from None
        body = None
        if route.request_body_pointer is not None:
            present, value = _argument(arguments, route.request_body_pointer, route.request_body_required)
            if present:
                try:
                    body = json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":")).encode("utf-8")
                except (TypeError, ValueError, UnicodeError, RecursionError):
                    raise A2APIError("INVALID_INPUT", "HTTP body must contain finite UTF-8 JSON values.", status=422) from None
                if len(body) > self.max_request_bytes:
                    raise A2APIError("REQUEST_TOO_LARGE", "HTTP body exceeds the request limit.", status=422)
                headers["Content-Type"] = route.request_media_type
        if route.credential_provider is not None:
            try:
                credentials = _header_values(route.credential_provider(context))
                if set(credentials) & {name.lower() for name in headers}:
                    raise ValueError("Conflicting credential fields")
                headers.update(credentials)
            except Exception:
                raise A2APIError("CREDENTIALS_UNAVAILABLE", "Host could not supply valid HTTP credentials.", status=503) from None
        media = sorted({response.media_type for response in route.responses.values() if response.media_type is not None})
        headers.update({"Accept": ", ".join(media) or "application/json", "Accept-Encoding": "identity",
                        "X-A2API-Actor": context.actor, "X-A2API-Tenant": context.tenant})
        parsed = urlsplit(route.base_url)
        call_deadline = min(budget.deadline, time.monotonic() + timeout_ms / 1000)

        def remaining() -> float:
            result = min(budget.remaining(), call_deadline - time.monotonic())
            if result <= 0:
                raise A2APIError("DEADLINE_EXCEEDED", "Backend call deadline was exceeded.", status=504)
            return result

        cls = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
        connection = cls(parsed.hostname, parsed.port, timeout=remaining())
        budget.claim()
        response = None
        request_started = False
        try:
            connection.connect()
            transport_socket = connection.sock
            transport_socket.settimeout(remaining())
            request_started = True
            connection.request(route.method, path, body=body, headers=headers)
            connection.sock.settimeout(remaining())
            response = connection.getresponse()
            codec = route.responses.get(response.status)
            if codec is None:
                code, status = {
                    400: ("UPSTREAM_VALIDATION_FAILED", 422),
                    401: ("PERMISSION_DENIED", 403), 403: ("PERMISSION_DENIED", 403),
                    404: ("RESOURCE_NOT_FOUND", 404), 429: ("RATE_LIMITED", 429),
                    409: ("UPSTREAM_CONFLICT", 409), 422: ("UPSTREAM_VALIDATION_FAILED", 422),
                    503: ("UPSTREAM_UNAVAILABLE", 503),
                }.get(response.status, ("UPSTREAM_ERROR", 502))
                # Status-derived wording only; the backend body is never forwarded.
                raise A2APIError(code, _UPSTREAM_DETAIL.get(response.status, "Backend did not return a successful JSON result.")
                                 + f" (HTTP {response.status})", status=status)
            mime = response.getheader("Content-Type", "").split(";")[0].strip().lower()
            if codec.media_type is not None and not (mime == codec.media_type or codec.media_type == "application/json" and json_media_type(mime)):
                raise A2APIError("INVALID_RESPONSE", "Backend response has an undeclared JSON media type.", status=502)
            if codec.media_type is not None and response.getheader("Content-Encoding", "identity").lower() != "identity":
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
                if codec.media_type is None:
                    if body:
                        raise A2APIError("INVALID_RESPONSE", "Backend returned content for a declared empty response.", status=502)
                    payload = None
                else:
                    payload = parse_json(body.decode("utf-8"))
                result = {route.response_envelope: payload} if route.response_envelope is not None else payload
                if route.response_status_field is not None:
                    result[route.response_status_field] = response.status
                validate_value(operation.output_schema, result, code="SCHEMA_MISMATCH", status=502)
                return result
            except (ValueError, UnicodeError, RecursionError):
                raise A2APIError("INVALID_RESPONSE", "Backend did not return strict UTF-8 JSON.", status=502) from None
        except A2APIError as error:
            if request_started and route.method not in {"GET", "HEAD"} and error.code in {"DEADLINE_EXCEEDED", "EXECUTION_STOPPED"}:
                raise A2APIError("OUTCOME_UNKNOWN", "Backend did not confirm the mutation outcome; no automatic retry was made.", status=502) from None
            raise
        except (TimeoutError, socket.timeout):
            if request_started and route.method not in {"GET", "HEAD"}:
                raise A2APIError("OUTCOME_UNKNOWN", "Backend did not confirm the mutation outcome; no automatic retry was made.", status=502) from None
            raise A2APIError("DEADLINE_EXCEEDED", "Backend call timed out.", status=504) from None
        except (OSError, http.client.HTTPException):
            if request_started and route.method not in {"GET", "HEAD"}:
                raise A2APIError("OUTCOME_UNKNOWN", "Backend did not confirm the mutation outcome; no automatic retry was made.", status=502) from None
            raise A2APIError("UPSTREAM_UNAVAILABLE", "Backend connection failed.", status=502) from None
        finally:
            if response is not None:
                response.close()
            connection.close()
