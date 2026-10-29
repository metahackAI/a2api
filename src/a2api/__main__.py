from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request

from .contracts import load_contract
from .errors import A2APIError
from .sample import TOKENS, authenticate, create_backend, running, sample_runtime
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
    importer = commands.add_parser("import-openapi", help="Import an OpenAPI 3.0/3.1 JSON/YAML document into disabled Capability IR")
    importer.add_argument("path")
    importer.add_argument("--namespace", default="imported")
    importer.add_argument("--output", required=True)
    importer.add_argument("--operation", action="append", help="Import only this operationId; may be repeated")
    importer.add_argument("--methods", nargs="+", type=str.upper, choices=["GET", "HEAD", "POST", "PUT", "PATCH", "DELETE"],
                          help="HTTP methods to import (default: GET); generated capabilities remain disabled")
    importer.add_argument("--strict", action="store_true", help="Exit unsuccessfully if selected operations are unsupported")
    build = commands.add_parser("build", help="Build executable read contracts from pinned imports and explicit review settings")
    build.add_argument("--imports", required=True, help="Directory produced by import-openapi")
    build.add_argument("--review", required=True, help="a2api review JSON file")
    build.add_argument("--output", required=True, help="New directory for a self-contained build")
    reviewed = commands.add_parser("review-demo", help="Verify OpenAPI import, review build and the full MCP stdio flow")
    reviewed.add_argument("--order-id", default="ORD-1001")
    reviewed.add_argument("--sample-user", choices=("alice", "bob", "limited"), default="alice")
    demo = commands.add_parser("demo", help="Start temporary HTTP APIs and verify the full discovery flow")
    demo.add_argument("--order-id", default="ORD-1001")
    serve = commands.add_parser("serve", help="Run local sample backend and a2api HTTP gateway")
    serve.add_argument("--port", type=int, default=8000)
    serve.add_argument("--backend-port", type=int, default=8001)
    for name, help_text in (("mcp", "Run the local sample as a stdio MCP server"),
                            ("mcp-demo", "Verify discover/describe/invoke using the official MCP client")):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("--sample-user", choices=("alice", "bob", "limited"), default="alice")
        command.add_argument("--build", help="Reviewed local order/shipment sample build; backend is the loopback fixture")
        if name == "mcp-demo":
            command.add_argument("--order-id", default="ORD-1001")
    args = parser.parse_args(argv)
    try:
        if args.command == "build":
            from .builder import build_contracts, write_build
            result = build_contracts(args.imports, args.review)
            report = write_build(result, args.output)
            print(json.dumps({'output': args.output, **result.summary(), 'contracts': report['contracts']}, ensure_ascii=False, indent=2))
            return 0
        if args.command == "import-openapi":
            from .importers import OpenAPIImporter, write_import
            importer = OpenAPIImporter.from_file(args.path, namespace=args.namespace, methods=set(args.methods) if args.methods else None)
            report = write_import(importer, args.output, operation_ids=set(args.operation) if args.operation else None)
            print(json.dumps({'output': str(args.output), **report['summary']}, ensure_ascii=False, indent=2))
            return 1 if args.strict and report['summary']['statuses'].get('unsupported', 0) else 0
        if args.command == "validate":
            capability = load_contract(args.path)
            print(json.dumps({"valid": True, "id": capability.id, "version": capability.version,
                              "enabled": capability.enabled, "steps": [s.id for s in capability.steps]}, ensure_ascii=False))
            return 0
        if args.command in ("mcp", "mcp-demo", "review-demo"):
            try:
                import anyio
                from .mcp_bridge import serve_stdio
            except ModuleNotFoundError:
                raise A2APIError("DEPENDENCY_MISSING", 'Install the MCP extra: python -m pip install -e ".[mcp]"') from None
            if args.command == "review-demo":
                from .review_demo import run_review_demo
                result = anyio.run(run_review_demo, args.order_id, args.sample_user)
                print(json.dumps(result, ensure_ascii=False, indent=2))
                return 0 if result['mcp']['invoke'].get('status') == 'succeeded' else 1
            if args.command == "mcp":
                from .builder import load_build
                from .review_demo import sample_built_runtime
                built = load_build(args.build) if args.build else None
                if built is not None and (built.review['review']['scope'] != 'sample' or built.review['source']['namespace'] != 'legacy_orders'):
                    raise A2APIError('BUILD_SCOPE_MISMATCH', 'The sample CLI accepts local order/shipment fixture builds only.')
                # Only protocol messages go to stdout. The host chooses this demo identity.
                with running(create_backend()) as backend_url:
                    runtime = sample_built_runtime(built, backend_url) if built is not None else sample_runtime(backend_url)
                    anyio.run(serve_stdio, runtime, TOKENS["demo-" + args.sample_user])
                return 0
            from .mcp_demo import run_demo
            result = anyio.run(run_demo, args.order_id, args.sample_user, args.build)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if result["invoke"].get("status") == "succeeded" else 1
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
