"""Order/shipment source update with an unaffected capability exercised over MCP."""

from __future__ import annotations

import hashlib
from importlib.resources import files
import json
import os
from pathlib import Path
import sys
import tempfile

from .builder import build_contracts, write_build
from .contracts import parse_json
from .importers import OpenAPIImporter, write_import
from .ir import thaw
from .regeneration import regenerate


def sample_importer() -> OpenAPIImporter:
    raw = files('a2api.sample').joinpath('order-shipping.incremental.openapi.json').read_bytes()
    return OpenAPIImporter(parse_json(raw.decode('utf-8')), namespace='legacy_orders',
                           source_name='order-shipping.incremental.openapi.json', source_hash=hashlib.sha256(raw).hexdigest())


def sample_review() -> dict:
    return parse_json(files('a2api.sample').joinpath('order-shipping.incremental.review.json').read_text(encoding='utf-8'))


async def run_incremental_demo() -> dict:
    from mcp import Client
    from mcp.client.stdio import StdioServerParameters
    with tempfile.TemporaryDirectory(prefix='a2api-incremental-') as temporary:
        directory = Path(temporary)
        importer, review = sample_importer(), sample_review()
        write_import(importer, directory / 'imports')
        approved = build_contracts(directory / 'imports', review)
        write_build(approved, directory / 'baseline')
        document = importer.document
        document['components']['schemas']['Shipment']['properties']['status']['enum'].append('returned')
        source = directory / 'updated.openapi.json'
        source.write_text(json.dumps(document, ensure_ascii=False), encoding='utf-8')
        updated = regenerate(approved, source)
        write_build(updated, directory / 'updated')
        environment = {'PYTHONPATH': os.environ['PYTHONPATH']} if 'PYTHONPATH' in os.environ else None
        parameters = StdioServerParameters(command=sys.executable,
            args=['-m', 'a2api', 'mcp', '--build', str(directory / 'updated')], env=environment)
        async with Client(parameters, read_timeout_seconds=15) as client:
            found = await client.call_tool('a2api.discover', {'query': ''})
            discovery = found.structured_content
            item = next(item for item in discovery['capabilities'] if item['id'] == 'order.summary')
            described = await client.call_tool('a2api.describe', {'id': item['id'], 'version': item['version']})
            invoked = await client.call_tool('a2api.invoke', {'id': item['id'], 'version': item['version'],
                'catalogVersion': discovery['catalogVersion'], 'input': {'orderId': 'ORD-1001'}})
            pending = await client.call_tool('a2api.describe', {'id': 'order.shipping_status', 'version': '0.1.0'})
            return {'regeneration': updated.summary(), 'reviewPreserved': review == sample_review(),
                    'capabilitiesStatus': thaw(updated.review_status),
                    'mcp': {'transport': 'stdio', 'discover': discovery,
                            'describedCapability': described.structured_content['capability']['id'],
                            'isError': invoked.is_error, 'invoke': invoked.structured_content,
                            'pendingCapabilityHidden': pending.is_error and pending.structured_content['error']['code'] == 'NOT_FOUND'}}
