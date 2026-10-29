"""Run from the repository: python examples/direct-orders/convert_and_invoke.py

Only local fixture APIs are called. No import/review/build files are written.
"""

import argparse
import json
from pathlib import Path

from a2api import HTTPDeployment, convert
from a2api.importers import OpenAPIImporter
from a2api.sample import BACKEND_TOKEN, TOKENS, create_backend, running


def run(order_id='ORD-1001'):
    source = OpenAPIImporter.from_file(
        Path(__file__).resolve().parents[2] / 'src/a2api/sample/order-shipping.openapi.json',
        namespace='legacy',
    )
    backend = create_backend()
    with running(backend) as origin:
        app = convert(source, operations={
            'getOrder': {'effect': 'read', 'select': ['orderId', 'orderState', 'shipmentIds']},
            'getShipment': {'effect': 'read', 'select': ['shipmentId', 'orderId', 'status', 'estimatedArrival', 'asOf']},
        }, deployment=HTTPDeployment(origin, credential_provider=lambda context: {
            'Authorization': 'Bearer ' + BACKEND_TOKEN,  # Local fixture credential only.
        }))
        caller = TOKENS['demo-alice']  # Trusted host context, outside business input.
        order = app.invoke('legacy.getorder', {'path': {'orderId': order_id}}, context=caller)
        if order['status'] != 'succeeded':
            return order
        shipments = []
        for identifier in order['data']['shipmentIds']:
            shipment = app.invoke('legacy.getshipment', {'path': {'shipmentId': identifier}}, context=caller)
            if shipment['status'] != 'succeeded':
                return shipment
            if shipment['data']['orderId'] != order['data']['orderId']:
                return {'status': 'failed', 'error': {'code': 'CONTRACT_DRIFT'}}
            shipments.append(shipment['data'])
        return {'status': 'succeeded', 'order': order['data'], 'shipments': shipments,
                'httpRequests': backend.sample_requests}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--order-id', default='ORD-1001')
    report = run(parser.parse_args().order_id)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report['status'] == 'succeeded' else 1)
