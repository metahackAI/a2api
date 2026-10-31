"""Legacy Python code with no HTTP API or OpenAPI (docs/36, path B-2).

python examples/legacy-conversion/python_functions.py

Existing service objects are not exposed as they are. Thin, typed wrappers choose the
inputs, the public fields and the effect; the caller identity stays host-only (context).
"""

import asyncio
from dataclasses import dataclass
from typing import Literal, TypedDict

from a2api import A2APIError, Application, ExecutionContext, ToolSession, capability


# ---- existing legacy code (unchanged) -------------------------------------------------
@dataclass
class OrderRow:
    id: str
    owner: str
    state: str
    amount: int
    internal_note: str


class LegacyOrderService:
    def __init__(self):
        self.rows = {'ORD-1': OrderRow('ORD-1', 'alice', 'paid', 12000, 'fraud-check passed'),
                     'ORD-2': OrderRow('ORD-2', 'bob', 'shipped', 8000, 'vip')}

    def find_visible(self, order_id, user):
        row = self.rows.get(order_id)
        return row if row and row.owner == user else None   # the legacy permission check stays

    def cancel(self, order_id, user):
        row = self.find_visible(order_id, user)
        if row is None:
            raise KeyError(order_id)
        if row.state not in ('pending', 'paid'):
            raise ValueError('not cancellable')
        row.state = 'cancelled'
        return row


SERVICE = LegacyOrderService()


# ---- a2api wrappers -------------------------------------------------------------------
class Order(TypedDict):
    id: str
    state: Literal['pending', 'paid', 'shipped', 'cancelled']
    amount: int


def public(row: OrderRow) -> Order:
    return {'id': row.id, 'state': row.state, 'amount': row.amount}   # internal_note is never returned


@capability(id='orders.get', effect='read', keywords=['주문', '조회', 'order'])
def get_order(orderId: str, *, context: ExecutionContext) -> Order:
    """주문 번호로 내 주문의 상태와 금액을 조회한다."""
    row = SERVICE.find_visible(orderId, context.actor)
    if row is None:
        raise A2APIError('RESOURCE_NOT_FOUND', 'Order does not exist or is not visible.', status=404)
    return public(row)


@capability(id='orders.cancel', effect='write', keywords=['주문', '취소', 'cancel'])
async def cancel_order(orderId: str, *, context: ExecutionContext) -> Order:
    """내 주문을 취소한다. pending/paid 상태만 취소할 수 있다."""
    await asyncio.sleep(0)   # async legacy clients work the same way
    try:
        return public(SERVICE.cancel(orderId, context.actor))
    except KeyError:
        raise A2APIError('RESOURCE_NOT_FOUND', 'Order does not exist or is not visible.', status=404) from None
    except ValueError:
        raise A2APIError('UPSTREAM_CONFLICT', 'The order state does not allow cancellation.', status=409) from None


async def main():
    app = Application([get_order, cancel_order])
    alice = ExecutionContext('alice', 'tenant-a', frozenset())
    print('descriptor:', app.describe('orders.cancel'))
    print('get:', app.invoke('orders.get', {'orderId': 'ORD-1'}, context=alice))
    print('other user\'s order:', app.invoke('orders.get', {'orderId': 'ORD-2'}, context=alice)['error']['code'])
    print('bad input:', app.invoke('orders.get', {'id': 'ORD-1'}, context=alice)['error']['issues'])

    session = ToolSession(app, alice)
    await session.auto('ORD-1 주문 취소해줘')
    print('model tools:', [tool['function'] for tool in session.tools()])
    print('cancel:', session.render(await session.call('orders_cancel', {'orderId': 'ORD-1'})))
    print('cancel again:', session.render(await session.call('orders_cancel', {'orderId': 'ORD-1'})))


if __name__ == '__main__':
    asyncio.run(main())
