from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request

from .contracts import load_contract
from .errors import A2APIError
from .sample import authenticate, create_backend, running, sample_runtime
from .server import create_server


def post(url: str, path: str, payload: dict, token: str = "demo-alice") -> tuple[int, dict]:
    request = urllib.request.Request(url + path, data=json.dumps(payload).encode(),
                                     headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as response:
        with response:
            return response.code, json.loads(response.read())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="a2api read-only capability MVP")
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate", help="Validate and compile a capability contract")
    validate.add_argument("path")
    demo = commands.add_parser("demo", help="Start temporary HTTP APIs and verify the full discovery flow")
    demo.add_argument("--order-id", default="ORD-1001")
    serve = commands.add_parser("serve", help="Run local sample backend and a2api HTTP gateway")
    serve.add_argument("--port", type=int, default=8000)
    serve.add_argument("--backend-port", type=int, default=8001)
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            capability = load_contract(args.path)
            print(json.dumps({"valid": True, "id": capability.id, "version": capability.version,
                              "enabled": capability.enabled, "steps": [s.id for s in capability.steps]}, ensure_ascii=False))
            return 0
        with running(create_backend(port=args.backend_port if args.command == "serve" else 0)) as backend_url:
            runtime = sample_runtime(backend_url)
            with running(create_server(runtime, authenticate, port=args.port if args.command == "serve" else 0)) as gateway:
                if args.command == "serve":
                    print(json.dumps({"gateway": gateway, "sampleBackend": backend_url,
                                      "demoTokens": ["demo-alice", "demo-bob", "demo-limited"]}), flush=True)
                    import threading
                    threading.Event().wait()
                else:
                    status, found = post(gateway, "/discover", {"query": "배송 조회"})
                    if status != 200 or not found.get("capabilities"):
                        raise A2APIError("DEMO_FAILED", "Discovery failed.")
                    item = found["capabilities"][0]
                    status, described = post(gateway, "/describe", {"id": item["id"], "version": item["version"]})
                    if status != 200 or described.get("capability", {}).get("id") != item["id"]:
                        raise A2APIError("DEMO_FAILED", "Description failed.")
                    status, result = post(gateway, "/invoke", {
                        "id": item["id"], "version": item["version"], "catalogVersion": found["catalogVersion"],
                        "input": {"orderId": args.order_id},
                    })
                    print(json.dumps({"discover": found, "describe": {"id": item["id"], "inputSchema": described["capability"]["inputSchema"]},
                                      "invoke": result}, ensure_ascii=False, indent=2))
                    return 0 if status == 200 and result.get("status") == "succeeded" else 1
    except A2APIError as error:
        print(json.dumps(error.problem(), ensure_ascii=False), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
