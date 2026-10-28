"""Small local HTTP host. Supply trusted authentication; not a production server."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Callable

from jsonschema import Draft202012Validator

from .contracts import parse_json
from .errors import A2APIError
from .ir import ExecutionContext
from .runtime import Runtime


def send_json(handler: BaseHTTPRequestHandler, status: int, value: object, *, problem: bool = False) -> None:
    payload = json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/problem+json; charset=utf-8" if problem else "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(payload)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    try:
        handler.wfile.write(payload)
    except (BrokenPipeError, ConnectionResetError):
        pass


def create_server(runtime: Runtime, authenticate: Callable[[str | None], ExecutionContext],
                  host: str = "127.0.0.1", port: int = 0) -> ThreadingHTTPServer:
    string = {"type": "string", "minLength": 1}
    schemas = {
        "/discover": {"query": {"type": "string", "maxLength": 1000}, "limit": {"type": "integer", "minimum": 1, "maximum": 50}, "cursor": string},
        "/describe": {"id": string, "version": string},
        "/invoke": {"id": string, "version": string, "catalogVersion": string, "input": {"type": "object"}, "requestId": {"type": "string", "minLength": 1, "maxLength": 128}},
    }
    required = {"/discover": [], "/describe": ["id", "version"], "/invoke": ["id", "version", "catalogVersion", "input"]}

    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup()
            self.connection.settimeout(10)

        def log_message(self, *args):
            pass

        def do_POST(self):
            try:
                context = authenticate(self.headers.get("Authorization"))
                if not isinstance(context, ExecutionContext):
                    raise A2APIError("UNAUTHENTICATED", "Host did not establish a trusted context.", status=401)
                if self.path not in schemas:
                    raise A2APIError("NOT_FOUND", "Unknown a2api endpoint.", status=404)
                if self.headers.get("Transfer-Encoding"):
                    raise A2APIError("INVALID_REQUEST", "Chunked request bodies are unsupported.")
                try:
                    length = int(self.headers.get("Content-Length", "0"))
                except ValueError:
                    raise A2APIError("INVALID_REQUEST", "Invalid Content-Length.") from None
                if not 1 <= length <= 131072:
                    raise A2APIError("INVALID_REQUEST", "A JSON body between 1 and 131072 bytes is required.", status=413)
                if self.headers.get("Content-Type", "").split(";")[0].strip().lower() != "application/json":
                    raise A2APIError("INVALID_REQUEST", "Content-Type must be application/json.", status=415)
                try:
                    payload = parse_json(self.rfile.read(length).decode("utf-8"))
                except (ValueError, UnicodeError):
                    raise A2APIError("INVALID_REQUEST", "Request body must be strict UTF-8 JSON.") from None
                schema = {"type": "object", "properties": schemas[self.path], "required": required[self.path], "additionalProperties": False}
                if not Draft202012Validator(schema).is_valid(payload):
                    raise A2APIError("INVALID_REQUEST", "Request fields do not match the endpoint contract.")
                if self.path == "/discover":
                    result = runtime.discover(payload.get("query", ""), context,
                                              limit=payload.get("limit", 10), cursor=payload.get("cursor"))
                elif self.path == "/describe":
                    result = runtime.describe(payload["id"], payload["version"], context)
                else:
                    result = runtime.invoke(payload["id"], payload["version"], payload["catalogVersion"],
                                            payload["input"], context, request_id=payload.get("requestId"))
                send_json(self, result.get("error", {}).get("status", 200), result)
            except A2APIError as error:
                send_json(self, error.status, error.problem(), problem=True)
            except (TimeoutError, ConnectionError):
                self.close_connection = True
            except Exception:
                send_json(self, 500, A2APIError("INTERNAL_ERROR", "An unexpected host error occurred.", status=500).problem(), problem=True)

    return ThreadingHTTPServer((host, port), Handler)
