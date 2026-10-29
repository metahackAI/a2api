"""CLI source diff through pinned approval to the actual MCP protocol."""

from contextlib import redirect_stdout
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from a2api.__main__ import main
from a2api.incremental_demo import sample_importer

HAS_MCP = importlib.util.find_spec('mcp') is not None
ROOT = Path(__file__).resolve().parents[1]
if HAS_MCP:
    from mcp import Client
    from mcp.client.stdio import StdioServerParameters


@unittest.skipUnless(HAS_MCP, 'Install a2api[mcp] for reapproval stdio tests')
class ReapprovalStdioTests(unittest.IsolatedAsyncioTestCase):
    async def test_cli_detect_prepare_approve_and_mcp_shipping_invocation(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            # Keep the raw fixture bytes so existing review pins match exactly.
            source = ROOT / 'src/a2api/sample/order-shipping.incremental.openapi.json'
            review = ROOT / 'src/a2api/sample/order-shipping.incremental.review.json'
            imports, baseline = directory / 'imports', directory / 'baseline'
            document = sample_importer().document
            document['components']['schemas']['Shipment']['properties']['status']['enum'].append('returned')
            changed = directory / 'updated.openapi.json'
            changed.write_text(json.dumps(document), encoding='utf-8')
            pending, proposal, approved = directory / 'pending', directory / 'review.json', directory / 'approved'
            def command(args):
                output = io.StringIO()
                with redirect_stdout(output):
                    code = main(args)
                self.assertEqual(code, 0, output.getvalue())
                return json.loads(output.getvalue())
            command(['import-openapi', str(source), '--namespace', 'legacy_orders', '--output', str(imports)])
            command(['build', '--imports', str(imports), '--review', str(review), '--output', str(baseline)])
            diff = command(['diff-openapi', '--before', str(source), '--after', str(changed), '--review', str(review)])
            self.assertEqual(diff['summary'], {'changed': 1, 'unchanged': 1})
            command(['regenerate', '--previous', str(baseline), '--source', str(changed), '--output', str(pending)])
            environment = {**os.environ, 'PYTHONPATH': str(ROOT / 'src')}
            def server(build):
                return StdioServerParameters(command=sys.executable, args=['-m', 'a2api', 'mcp', '--build', str(build)], env=environment)
            async with Client(server(pending), read_timeout_seconds=15) as client:
                catalog = (await client.call_tool('a2api.discover', {'query': ''})).structured_content
                self.assertEqual([row['id'] for row in catalog['capabilities']], ['order.summary'])
                unavailable = await client.call_tool('a2api.describe', {'id': 'order.shipping_status', 'version': '0.1.0'})
                self.assertTrue(unavailable.is_error)
            command(['prepare-review', '--build', str(pending), '--capability', 'order.shipping_status@0.1.0', '--output', str(proposal)])
            reviewed = json.loads(proposal.read_text())
            reviewed['reviews'][0]['settings']['capabilities'][0]['outputSchema']['properties']['shipments']['items']['properties']['status']['enum'].append('returned')
            proposal.write_text(json.dumps(reviewed), encoding='utf-8')
            report = command(['approve-review', '--build', str(pending), '--review', str(proposal), '--reviewed-by',
                              'MCP fixture suite', '--reviewed-at', '2026-10-29T03:00:00Z', '--output', str(approved)])
            self.assertEqual(report['requiresReview'], 0)
            self.assertEqual((approved / 'review.json').read_bytes(), (baseline / 'review.json').read_bytes())
            self.assertEqual((approved / 'contracts/order.summary.0.1.0.json').read_bytes(),
                             (baseline / 'contracts/order.summary.0.1.0.json').read_bytes())
            async with Client(server(approved), read_timeout_seconds=15) as client:
                discovery = await client.call_tool('a2api.discover', {'query': ''})
                current = discovery.structured_content
                self.assertEqual({row['id'] for row in current['capabilities']}, {'order.summary', 'order.shipping_status'})
                described = await client.call_tool('a2api.describe', {'id': 'order.shipping_status', 'version': '0.1.0'})
                self.assertEqual(described.structured_content['capability']['provenance']['reviewedBy'], 'MCP fixture suite')
                arguments = {'id': 'order.shipping_status', 'version': '0.1.0', 'catalogVersion': catalog['catalogVersion'],
                             'input': {'orderId': 'ORD-1001'}}
                stale = await client.call_tool('a2api.invoke', arguments)
                self.assertTrue(stale.is_error)
                self.assertEqual(stale.structured_content['error']['code'], 'CONTRACT_DRIFT')
                arguments['catalogVersion'] = current['catalogVersion']
                invoked = await client.call_tool('a2api.invoke', arguments)
                self.assertFalse(invoked.is_error, invoked)
                self.assertEqual(invoked.structured_content['status'], 'succeeded')
                self.assertEqual(invoked.structured_content['stats']['backendCalls'], 3)
                self.assertEqual(len(invoked.structured_content['data']['shipments']), 2)
                order = await client.call_tool('a2api.invoke', {**arguments, 'id': 'order.summary'})
                self.assertFalse(order.is_error, order)
                self.assertEqual(order.structured_content['stats']['backendCalls'], 1)


@unittest.skipUnless(HAS_MCP, 'Install a2api[mcp] for packaged reapproval demo')
class ReapprovalDemoTests(unittest.TestCase):
    def test_packaged_demo(self):
        process = subprocess.run([sys.executable, '-m', 'a2api', 'reapproval-demo'], cwd=ROOT,
            env={**os.environ, 'PYTHONPATH': str(ROOT / 'src')}, text=True, capture_output=True, timeout=25)
        self.assertEqual(process.returncode, 0, process.stderr)
        result = json.loads(process.stdout)
        self.assertTrue(result['reviewPreserved'])
        self.assertTrue(result['unaffectedContractPreserved'])
        self.assertFalse(result['mcp']['isError'])
        self.assertEqual(result['mcp']['invoke']['stats']['backendCalls'], 3)
