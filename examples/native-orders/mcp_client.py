"""Run actual stdio calls: python examples/native-orders/mcp_client.py"""

import json
import os
from pathlib import Path
import sys

import anyio
from mcp import Client
from mcp.client.stdio import StdioServerParameters


async def run():
    parameters = StdioServerParameters(command=sys.executable, args=[str(Path(__file__).with_name('mcp_server.py'))],
        env={'PYTHONPATH': os.environ['PYTHONPATH']} if 'PYTHONPATH' in os.environ else None)
    async with Client(parameters, read_timeout_seconds=15) as client:
        tools = await client.list_tools()
        found = await client.call_tool('a2api.discover', {})
        if found.is_error:
            raise RuntimeError('Discovery failed')
        catalog = found.structured_content
        for item in catalog['capabilities']:
            described = await client.call_tool('a2api.describe', {'id': item['id'], 'version': item['version']})
            if described.is_error:
                raise RuntimeError('Description failed')
        async def invoke(identifier, input):
            result = await client.call_tool('a2api.invoke', {'id': identifier, 'version': '0.1.0',
                'catalogVersion': catalog['catalogVersion'], 'input': input})
            if result.is_error:
                raise RuntimeError('Invocation failed: ' + result.structured_content['error']['code'])
            return result.structured_content['data']
        order = await invoke('legacy.getorder', {'path': {'orderId': 'ORD-1001'}})
        shipments = [await invoke('legacy.getshipment', {'path': {'shipmentId': identifier}}) for identifier in order['shipmentIds']]
        native_order = await invoke('orders.lookup', {'orderId': 'ORD-1001'})
        native_shipments = await invoke('shipping.list', {'orderId': 'ORD-1001'})
        return {'transport': 'stdio', 'tools': [tool.name for tool in tools.tools],
                'capabilities': [item['id'] for item in catalog['capabilities']],
                'openapi': {'order': order, 'shipments': shipments},
                'python': {'order': native_order, 'shipments': native_shipments}}


if __name__ == '__main__':
    print(json.dumps(anyio.run(run), ensure_ascii=False, indent=2))
