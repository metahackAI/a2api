"""Two real read operations, optionally padded with clearly synthetic functions."""

from importlib.resources import files
import json
from pathlib import Path
import sys

from a2api import Application, HTTPDeployment, capability, convert
from a2api.importers import OpenAPIImporter
from a2api.sample import BACKEND_TOKEN, TOKENS

ROOT = Path(__file__).resolve().parents[2]
ORDER_IDS = ['legacy.getorder', 'legacy.getshipment']
GITHUB_IDS = ['github.repository.get', 'github.issues.list']


def create(domain, origin, count=2):
    if count not in (2, 1000):raise ValueError('Use count=2 or count=1000.')
    if domain == 'orders':
        source = OpenAPIImporter(json.loads(files('a2api.sample').joinpath('order-shipping.openapi.json').read_text()), namespace='legacy')
        app = convert(source, operations={
            'getOrder': {'effect': 'read', 'select': ['orderId', 'orderState', 'shipmentIds'],
                         'summary': '주문 번호로 주문 상태와 연결된 배송 번호 목록을 조회한다.',
                         'keywords': ['order', '주문', 'orderId']},
            'getShipment': {'effect': 'read', 'select': ['shipmentId', 'orderId', 'status', 'estimatedArrival', 'asOf'],
                            'summary': '배송 번호로 배송 상태와 도착 예정일을 조회한다. 주문 응답의 shipmentIds를 사용한다.',
                            'keywords': ['shipment', 'shipping', '배송', 'shipmentId']},
        }, deployment=HTTPDeployment(origin, credential_provider=lambda _: {'Authorization': 'Bearer ' + BACKEND_TOKEN}))
        context, known = TOKENS['demo-alice'], ORDER_IDS
    elif domain == 'github':
        sys.path.insert(0, str(ROOT / 'examples/github-openapi'))
        from agent_app import create_app, PUBLIC_CONTEXT
        app, context, known = create_app(origin), PUBLIC_CONTEXT, GITHUB_IDS
    else:raise ValueError('Use domain=orders or github.')
    apps = [app]
    if count > 2:
        def synthetic(code: str, limit: int = 3) -> str:
            """Synthetic fixture; not a company or GitHub operation."""
            return 'synthetic:' + code
        categories = [('product', '상품 가격 product price'), ('billing', '청구서 결제 billing invoice'),
                      ('account', '계정 account profile'), ('stock', '재고 inventory stock')]
        functions = []
        for i in range(count - 2):
            category, words = categories[i % len(categories)]
            functions.append(capability(id=f'fixture.{category}_{i:04}', effect='read',
                summary=f'{words} 합성 조회 기능 {i}; code로 조회하며 limit은 최대 결과 수다.')(synthetic))
        apps.append(Application(functions))
    return apps, context, known
