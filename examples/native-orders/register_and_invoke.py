"""Explicit legacy wrapper and a new typed API. No HTTP, MCP or generated files."""

from copy import deepcopy
import json
from typing import Literal, NotRequired, TypedDict

from a2api import A2APIError, Application, ExecutionContext, capability

ORDERS = {
    'ORD-1001': {'orderId': 'ORD-1001', 'orderState': 'shipped', 'shipmentIds': ['SHP-501'], 'ownerId': 'alice', 'tenantId': 'tenant-a'},
    'ORD-1002': {'orderId': 'ORD-1002', 'orderState': 'processing', 'shipmentIds': [], 'ownerId': 'alice', 'tenantId': 'tenant-a'},
}
SHIPMENTS = {
    'SHP-501': {'shipmentId': 'SHP-501', 'status': 'in_transit', 'estimatedArrival': None},
}


def legacy_find_order(order_id, caller):
    """Existing untyped implementation, including object authorization."""
    row = ORDERS.get(order_id)
    if row is None:
        raise A2APIError('RESOURCE_NOT_FOUND', 'Order not found.', status=404)
    if (row['ownerId'], row['tenantId']) != (caller.actor, caller.tenant):
        raise A2APIError('PERMISSION_DENIED', 'Order unavailable to this caller.', status=403)
    return deepcopy(row)


class OrderView(TypedDict):
    orderId: str
    orderState: Literal['shipped', 'processing']
    shipmentIds: list[str]


class ShipmentView(TypedDict):
    shipmentId: str
    status: Literal['pending', 'in_transit', 'delivered']
    estimatedArrival: str | None
    note: NotRequired[str]


@capability(id='orders.lookup', effect='read')
def lookup_order(orderId: str, *, context: ExecutionContext) -> OrderView:
    """Look up an authorized order without exposing internal owner fields."""
    row = legacy_find_order(orderId, context)
    return {name: row[name] for name in ('orderId', 'orderState', 'shipmentIds')}


@capability(id='shipping.list', effect='read')
def list_shipments(orderId: str, includeNote: bool = False, *, context: ExecutionContext) -> list[ShipmentView]:
    """A new API returning the shipments of an authorized order."""
    order = legacy_find_order(orderId, context)
    result = []
    for identifier in order['shipmentIds']:
        row = deepcopy(SHIPMENTS[identifier])
        if includeNote:
            row['note'] = 'Estimated arrival is not confirmed.'
        result.append(row)
    return result


def run():
    app = Application([lookup_order, list_shipments])
    caller = ExecutionContext('alice', 'tenant-a', frozenset({'orders:read', 'shipments:read'}))
    return {'profile': app.profile,
            'order': app.invoke('orders.lookup', {'orderId': 'ORD-1001'}, context=caller),
            'shipping': app.invoke('shipping.list', {'orderId': 'ORD-1001'}, context=caller),
            'empty': app.invoke('shipping.list', {'orderId': 'ORD-1002'}, context=caller)}


if __name__ == '__main__':
    report = run()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if all(report[name]['status'] == 'succeeded' for name in ('order', 'shipping', 'empty')) else 1)
