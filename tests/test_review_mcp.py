"""Disk OpenAPI import/build followed by the official MCP stdio client."""

import importlib.util
import asyncio
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from jsonschema import Draft202012Validator
from a2api import load_build

ROOT = Path(__file__).resolve().parents[1]
HAS_MCP = importlib.util.find_spec('mcp') is not None
if HAS_MCP:
    from mcp import Client
    from mcp.client.stdio import StdioServerParameters


@unittest.skipUnless(HAS_MCP, 'Install a2api[mcp] for reviewed stdio pipeline tests')
class ReviewedStdioTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.imports = self.directory / 'imports'
        self.built = self.directory / 'built'
        self.environment = {**os.environ, 'PYTHONPATH': str(ROOT / 'src')}
        imported = self.command('import-openapi', str(ROOT / 'src/a2api/sample/order-shipping.openapi.json'),
                                '--namespace', 'legacy_orders', '--output', str(self.imports))
        self.assertEqual(imported.returncode, 0, imported.stderr)
        self.assertEqual(json.loads(imported.stdout)['statuses'], {'imported': 2})
        built = self.command('build', '--imports', str(self.imports), '--review', str(ROOT / 'src/a2api/sample/order-shipping.review.json'),
                             '--output', str(self.built))
        self.assertEqual(built.returncode, 0, built.stderr)
        self.summary = json.loads(built.stdout)

    def command(self, *arguments):
        return subprocess.run([sys.executable, '-m', 'a2api', *arguments], cwd=ROOT, env=self.environment,
                              text=True, capture_output=True, timeout=25)

    def client(self, user='alice'):
        return Client(StdioServerParameters(command=sys.executable, args=['-m', 'a2api', 'mcp', '--build', str(self.built),
                      '--sample-user', user], env=self.environment), read_timeout_seconds=15)

    async def test_import_build_discover_describe_invoke_over_actual_stdio(self):
        async with self.client() as client:
            tools = {tool.name: tool for tool in (await client.list_tools()).tools}
            self.assertEqual(set(tools), {'a2api.discover', 'a2api.describe', 'a2api.invoke'})
            found = await client.call_tool('a2api.discover', {'query': '주문 배송 조회'})
            self.assertFalse(found.is_error)
            discovery = found.structured_content
            item = discovery['capabilities'][0]
            described = await client.call_tool('a2api.describe', {'id': item['id'], 'version': item['version']})
            manifest = described.structured_content['capability']
            self.assertEqual(set(manifest), {'id', 'version', 'summary', 'effects', 'inputSchema', 'outputSchema'})
            full = load_build(self.built).capabilities[0].describe()
            self.assertEqual(full['provenance']['reviewSha256'], self.summary['reviewSha256'])
            self.assertEqual(full['provenance']['sourceSha256'], self.summary['sourceSha256'])
            for order, calls, shipment_count in [('ORD-1001', 3, 2), ('ORD-1002', 1, 0)]:
                invoked = await client.call_tool('a2api.invoke', {'id': item['id'], 'version': item['version'],
                    'catalogVersion': discovery['catalogVersion'], 'input': {'orderId': order}})
                self.assertFalse(invoked.is_error, invoked)
                result = invoked.structured_content
                self.assertEqual(result['status'], 'succeeded')
                self.assertEqual(result['stats']['backendCalls'], calls)
                self.assertEqual(len(result['data']['shipments']), shipment_count)
                Draft202012Validator(tools['a2api.invoke'].output_schema).validate(result)
                self.assertNotIn('ownerId', json.dumps(result))
                self.assertNotIn('tenantId', json.dumps(result))
            denied = await client.call_tool('a2api.invoke', {'id': item['id'], 'version': item['version'],
                'catalogVersion': discovery['catalogVersion'], 'input': {'orderId': 'ORD-2001'}})
            self.assertTrue(denied.is_error)
            self.assertEqual(denied.structured_content['error']['code'], 'PERMISSION_DENIED')
            self.assertNotIn('data', denied.structured_content)

    async def test_scope_filtering_applies_to_built_capability_over_stdio(self):
        async with self.client('limited') as client:
            found = await client.call_tool('a2api.discover', {'query': '배송'})
            self.assertEqual(found.structured_content['capabilities'], [])
            result = await client.call_tool('a2api.describe', {'id': 'order.shipping_status', 'version': '0.1.0'})
            self.assertTrue(result.is_error)
            self.assertEqual(result.structured_content['error']['code'], 'NOT_FOUND')

    async def test_tampered_build_cannot_start_mcp_or_emit_protocol_output(self):
        path = self.built / 'build.json'
        report = json.loads(path.read_text())
        report['enabled'] = 9
        path.write_text(json.dumps(report))
        process = await asyncio.to_thread(self.command, 'mcp', '--build', str(self.built))
        self.assertEqual(process.returncode, 1)
        self.assertEqual(process.stdout, '')
        self.assertEqual(json.loads(process.stderr)['code'], 'BUILD_DRIFT')

    async def test_one_command_review_demo_reproduces_full_pipeline(self):
        process = await asyncio.to_thread(self.command, 'review-demo')
        self.assertEqual(process.returncode, 0, process.stderr)
        result = json.loads(process.stdout)
        self.assertEqual(result['import']['statuses'], {'imported': 2})
        self.assertEqual(result['build']['enabled'], 1)
        self.assertEqual(result['mcp']['invoke']['stats']['backendCalls'], 3)
        self.assertEqual(result['mcp']['invoke']['status'], 'succeeded')
        self.assertIn('outputSchema', result['mcp']['describe'])
        self.assertNotIn('provenance', result['mcp']['describe'])
