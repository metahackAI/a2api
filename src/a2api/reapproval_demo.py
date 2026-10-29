"""Source change through selective reapproval to real MCP stdio execution."""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile

from .builder import build_contracts, load_build, write_build
from .incremental_demo import sample_importer, sample_review
from .importers import write_import
from .ir import thaw
from .reapproval import approve_review, prepare_review, write_review
from .regeneration import regenerate


async def run_reapproval_demo() -> dict:
    from mcp import Client
    from mcp.client.stdio import StdioServerParameters
    with tempfile.TemporaryDirectory(prefix='a2api-reapproval-') as temporary:
        directory = Path(temporary)
        importer, review = sample_importer(), sample_review()
        write_import(importer, directory / 'imports')
        baseline = build_contracts(directory / 'imports', review)
        write_build(baseline, directory / 'baseline')
        # Changing a referenced response enum affects only its consuming cap.
        importer.document['components']['schemas']['Shipment']['properties']['status']['enum'].append('returned')
        source = directory / 'updated.openapi.json'
        source.write_text(json.dumps(importer.document), encoding='utf-8')
        pending = regenerate(baseline, source)
        write_build(pending, directory / 'pending')
        proposal = prepare_review(pending, ['order.shipping_status@0.1.0'])
        # The source pin is current; the business output enum is still the old
        # review setting. Explicitly accept the new value in the selected review.
        proposal['reviews'][0]['settings']['capabilities'][0]['outputSchema']['properties']['shipments']['items']['properties']['status']['enum'].append('returned')
        write_review(proposal, directory / 'shipping.review.json')
        approved = approve_review(pending, proposal, reviewed_by='a2api reapproval demo fixture suite',
                                  reviewed_at='2026-10-29T00:00:00Z')
        write_build(approved, directory / 'approved')
        loaded = load_build(directory / 'approved')
        before = next(cap for cap in baseline.capabilities if cap.id == 'order.summary')
        after = next(cap for cap in loaded.capabilities if cap.id == 'order.summary')
        environment = {'PYTHONPATH': os.environ['PYTHONPATH']} if 'PYTHONPATH' in os.environ else None
        parameters = StdioServerParameters(command=sys.executable,
            args=['-m', 'a2api', 'mcp', '--build', str(directory / 'approved')], env=environment)
        async with Client(parameters, read_timeout_seconds=15) as client:
            found = await client.call_tool('a2api.discover', {'query': ''})
            catalog = found.structured_content
            described = await client.call_tool('a2api.describe', {'id': 'order.shipping_status', 'version': '0.1.0'})
            invoked = await client.call_tool('a2api.invoke', {'id': 'order.shipping_status', 'version': '0.1.0',
                'catalogVersion': catalog['catalogVersion'], 'input': {'orderId': 'ORD-1001'}})
            return {'pending': thaw(pending.review_status), 'approved': thaw(loaded.review_status),
                    'reviewPreserved': thaw(loaded.review) == review,
                    'unaffectedContractPreserved': before.manifest_json == after.manifest_json,
                    'mcp': {'discover': catalog, 'describedCapability': described.structured_content['capability']['id'],
                            'isError': invoked.is_error, 'invoke': invoked.structured_content}}
