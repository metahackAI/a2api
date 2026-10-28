"""Local fixtures and demo credentials; no production integrations."""

from __future__ import annotations

import copy
import hmac
import json
import threading
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
from urllib.parse import unquote

from ..catalog import Catalog
from ..contracts import compile_contract
from ..errors import A2APIError
from ..http_adapter import HTTPAdapter, HTTPRoute
from ..ir import ExecutionContext
from ..runtime import Runtime
from ..server import send_json

BACKEND_TOKEN = "local-sample-service-token"
TOKENS = {
    "demo-alice": ExecutionContext("alice", "tenant-a", frozenset({"orders:read", "shipments:read"})),
    "demo-bob": ExecutionContext("bob", "tenant-b", frozenset({"orders:read", "shipments:read"})),
    "demo-limited": ExecutionContext("alice", "tenant-a", frozenset({"orders:read"})),
}


def authenticate(authorization: str | None) -> ExecutionContext:
    for token, context in TOKENS.items():
        if hmac.compare_digest((authorization or "").encode(), ("Bearer " + token).encode()):
            return context
    raise A2APIError("UNAUTHENTICATED", "A valid local demo bearer token is required.", status=401)


def sample_manifest() -> dict:
    return json.loads(files(__package__).joinpath("order-shipping.json").read_text(encoding="utf-8"))


def sample_runtime(backend_url: str, manifest: dict | None = None) -> Runtime:
    capability = compile_contract(manifest if manifest is not None else sample_manifest())
    routes = {
        ("demo-orders", "getOrder"): HTTPRoute(backend_url, "/orders/{id}", {"id": "/orderId"}, {"Authorization": "Bearer " + BACKEND_TOKEN}),
        ("demo-shipping", "getShipment"): HTTPRoute(backend_url, "/shipments/{id}", {"id": "/shipmentId"}, {"Authorization": "Bearer " + BACKEND_TOKEN}),
    }
    return Runtime(Catalog([capability], allow_samples=True), HTTPAdapter(routes))


def create_backend(*, port: int = 0, transform=None) -> ThreadingHTTPServer:
    orders = {
        "ORD-1001": {"orderId": "ORD-1001", "orderState": "shipped", "shipmentIds": ["SHP-501", "SHP-502"], "ownerId": "alice", "tenantId": "tenant-a"},
        "ORD-1002": {"orderId": "ORD-1002", "orderState": "processing", "shipmentIds": [], "ownerId": "alice", "tenantId": "tenant-a"},
        "ORD-2001": {"orderId": "ORD-2001", "orderState": "shipped", "shipmentIds": ["SHP-601"], "ownerId": "bob", "tenantId": "tenant-b"},
        "ORD-1003": {"orderId": "ORD-1003", "orderState": "created", "shipmentIds": [], "ownerId": "bob", "tenantId": "tenant-a"},
    }
    shipments = {
        "SHP-501": {"shipmentId": "SHP-501", "orderId": "ORD-1001", "status": "in_transit", "estimatedArrival": "2026-10-29T18:00:00+09:00", "asOf": "2026-10-28T15:00:00+09:00", "ownerId": "alice", "tenantId": "tenant-a"},
        "SHP-502": {"shipmentId": "SHP-502", "orderId": "ORD-1001", "status": "delivered", "estimatedArrival": None, "asOf": "2026-10-28T15:00:00+09:00", "ownerId": "alice", "tenantId": "tenant-a"},
        "SHP-601": {"shipmentId": "SHP-601", "orderId": "ORD-2001", "status": "pending", "estimatedArrival": None, "asOf": "2026-10-28T15:00:00+09:00", "ownerId": "bob", "tenantId": "tenant-b"},
    }
    requests = []
    lock = threading.Lock()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            with lock:
                requests.append(self.path)
            if not hmac.compare_digest(self.headers.get("Authorization", "").encode(), ("Bearer " + BACKEND_TOKEN).encode()):
                send_json(self, 401, {"error": "service authentication required"})
                return
            parts = self.path.split("/")
            data = None
            if len(parts) == 3:
                collection = {"orders": orders, "shipments": shipments}.get(parts[1], {})
                data = collection.get(unquote(parts[2]))
            if data is None:
                send_json(self, 404, {"error": "not found"})
                return
            if (data["ownerId"] != self.headers.get("X-A2API-Actor") or data["tenantId"] != self.headers.get("X-A2API-Tenant")):
                send_json(self, 403, {"error": "object access denied"})
                return
            status, payload = (200, copy.deepcopy(data))
            if transform:
                status, payload = transform(self.path, payload)
            send_json(self, status, payload)

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.sample_requests = requests
    return server


@contextmanager
def running(server: ThreadingHTTPServer):
    thread = threading.Thread(target=lambda: server.serve_forever(poll_interval=0.01), daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
