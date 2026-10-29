"""An unaffected capability stays usable over official MCP stdio after a source update."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from jsonschema import Draft202012Validator

from a2api.builder import build_contracts, write_build
from a2api.incremental_demo import sample_importer, sample_review
from a2api.importers import write_import
from a2api.regeneration import regenerate

HAS_MCP = importlib.util.find_spec('mcp') is not None
ROOT = Path(__file__).resolve().parents[1]
if HAS_MCP:
    from mcp import Client
    from mcp.client.stdio import StdioServerParameters


@unittest.skipUnless(HAS_MCP, 'Install a2api[mcp] for incremental stdio tests')
class IncrementalStdioTests(unittest.IsolatedAsyncioTestCase):
    async def test_unaffected_capability_is_visible_and_pending_capability_cannot_invoke(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            importer = sample_importer()
            write_import(importer, directory / 'imports')
            baseline = build_contracts(directory / 'imports', sample_review())
            document = importer.document
            document['components']['schemas']['Shipment']['properties']['status']['enum'].append('returned')
            source = directory / 'updated.json'
            source.write_text(json.dumps(document))
            updated = regenerate(baseline, source)
            write_build(updated, directory / 'build')
            environment = {**os.environ, 'PYTHONPATH': str(ROOT / 'src')}
            parameters = StdioServerParameters(command=sys.executable,
                args=['-m', 'a2api', 'mcp', '--build', str(directory / 'build')], env=environment)
            async with Client(parameters, read_timeout_seconds=15) as client:
                tools = {tool.name: tool for tool in (await client.list_tools()).tools}
                found = await client.call_tool('a2api.discover', {'query': ''})
                self.assertFalse(found.is_error)
                catalog = found.structured_content
                self.assertEqual([item['id'] for item in catalog['capabilities']], ['order.summary'])
                result = await client.call_tool('a2api.invoke', {'id': 'order.summary', 'version': '0.1.0',
                    'catalogVersion': catalog['catalogVersion'], 'input': {'orderId': 'ORD-1001'}})
                self.assertFalse(result.is_error)
                self.assertEqual(result.structured_content['stats']['backendCalls'], 1)
                self.assertEqual(result.structured_content['data'], {'orderId': 'ORD-1001', 'orderState': 'shipped'})
                Draft202012Validator(tools['a2api.invoke'].output_schema).validate(result.structured_content)
                for method in ('describe', 'invoke'):
                    arguments = {'id': 'order.shipping_status', 'version': '0.1.0'}
                    if method == 'invoke':
                        arguments.update(catalogVersion=catalog['catalogVersion'], input={'orderId': 'ORD-1001'})
                    pending = await client.call_tool('a2api.' + method, arguments)
                    self.assertTrue(pending.is_error)
                    self.assertEqual(pending.structured_content['error']['code'], 'NOT_FOUND')


@unittest.skipUnless(HAS_MCP, 'Install a2api[mcp] for incremental demo')
class IncrementalDemoTests(unittest.TestCase):
    def test_packaged_cli_demo_reuses_order_and_quarantines_shipping(self):
        process = subprocess.run([sys.executable, '-m', 'a2api', 'incremental-demo'], cwd=ROOT,
            env={**os.environ, 'PYTHONPATH': str(ROOT / 'src')}, text=True, capture_output=True, timeout=25)
        self.assertEqual(process.returncode, 0, process.stderr)
        report = json.loads(process.stdout)
        self.assertEqual(report['regeneration']['convertedOperations'], 1)
        self.assertEqual(report['regeneration']['reusedOperations'], 1)
        self.assertEqual(report['regeneration']['requiresReview'], 1)
        self.assertTrue(report['reviewPreserved'])
        self.assertTrue(report['mcp']['pendingCapabilityHidden'])
        self.assertEqual(report['mcp']['invoke']['stats']['backendCalls'], 1)
