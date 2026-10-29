"""stdio host for converted OpenAPI and explicitly registered Python functions."""

import argparse
from contextlib import ExitStack
from importlib.resources import files
import json

import anyio

from a2api import Application, HTTPDeployment, convert
from a2api.importers import OpenAPIImporter
from a2api.mcp_bridge import serve_stdio
from a2api.sample import BACKEND_TOKEN, TOKENS, create_backend, running
from register_and_invoke import lookup_order, list_shipments


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', choices=['openapi', 'python', 'both'], default='both')
    parser.add_argument('--sample-user', choices=['alice', 'bob'], default='alice')
    parser.add_argument('--backend-origin', help='Explicit host origin; omitted to start a local fixture')
    args = parser.parse_args()
    with ExitStack() as stack:
        apps = []
        if args.source in ('openapi', 'both'):
            origin = args.backend_origin or stack.enter_context(running(create_backend()))
            source = OpenAPIImporter(json.loads(files('a2api.sample').joinpath('order-shipping.openapi.json').read_text()), namespace='legacy')
            apps.append(convert(source, operations={
                'getOrder': {'effect': 'read', 'select': ['orderId', 'orderState', 'shipmentIds']},
                'getShipment': {'effect': 'read', 'select': ['shipmentId', 'orderId', 'status', 'estimatedArrival', 'asOf']},
            }, deployment=HTTPDeployment(origin, credential_provider=lambda _: {'Authorization': 'Bearer ' + BACKEND_TOKEN})))
        if args.source in ('python', 'both'):
            apps.append(Application([lookup_order, list_shipments]))
        # stdout belongs to MCP. The selected applications/context are host-owned.
        anyio.run(serve_stdio, apps, TOKENS['demo-' + args.sample_user])


if __name__ == '__main__':
    main()
