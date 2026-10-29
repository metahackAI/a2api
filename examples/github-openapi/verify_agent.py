"""Opt-in live verification: two direct reads and two actual MCP stdio reads."""

import argparse
import json
import os
from pathlib import Path
import sys

import anyio
from jsonschema import Draft202012Validator
from mcp import Client
from mcp.client.stdio import StdioServerParameters

from agent_app import API_VERSION, ISSUES, PUBLIC_CONTEXT, REPOSITORY, create_app


def checked(result, descriptor):
    if result['status'] != 'succeeded':
        raise RuntimeError(json.dumps(result['error']))
    Draft202012Validator(descriptor['outputSchema']).validate(result['data'])
    assert result['completeness'] == {'complete': True, 'scope': 'single_api_response'}
    return result['data']


async def verify(owner='metahackAI', repo='a2api', *, origin='https://api.github.com',
                 state='open', page=1, per_page=5):
    inputs = {REPOSITORY: {'owner': owner, 'repo': repo},
              ISSUES: {'owner': owner, 'repo': repo, 'state': state, 'page': page, 'perPage': per_page}}
    app = create_app(origin)
    direct = {identifier: checked(app.invoke(identifier, value, context=PUBLIC_CONTEXT), app.describe(identifier))
              for identifier, value in inputs.items()}
    parameters = StdioServerParameters(command=sys.executable,
        args=[str(Path(__file__).with_name('mcp_server.py')), '--origin', origin],
        env={'PYTHONPATH': os.environ['PYTHONPATH']} if 'PYTHONPATH' in os.environ else None)
    async with Client(parameters, read_timeout_seconds=20) as client:
        tools = await client.list_tools()
        assert [tool.name for tool in tools.tools] == ['a2api.discover', 'a2api.describe', 'a2api.invoke']
        tool_listing = json.dumps(tools.model_dump(mode='json', by_alias=True, exclude_none=True))
        assert all(identifier not in tool_listing for identifier in inputs)
        found = await client.call_tool('a2api.discover', {'query': 'github'})
        assert not found.is_error, found
        catalog = found.structured_content
        assert {item['id'] for item in catalog['capabilities']} == set(inputs)
        stdio = {}
        for item in catalog['capabilities']:
            described = await client.call_tool('a2api.describe', {'id': item['id'], 'version': item['version']})
            assert not described.is_error, described
            descriptor = described.structured_content['capability']
            assert descriptor == app.describe(item['id'])
            invoked = await client.call_tool('a2api.invoke', {'id': item['id'], 'version': item['version'],
                'catalogVersion': catalog['catalogVersion'], 'input': inputs[item['id']]})
            assert not invoked.is_error, invoked
            stdio[item['id']] = checked(invoked.structured_content, descriptor)
    # Data may change between reads; validate each response instead of requiring equality.
    return {'origin': origin, 'apiVersion': API_VERSION, 'authentication': 'none',
            'tools': [tool.name for tool in tools.tools], 'httpReads': 4,
            'direct': direct, 'stdio': stdio}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--owner', default='metahackAI')
    parser.add_argument('--repo', default='a2api')
    parser.add_argument('--origin', default='https://api.github.com')
    parser.add_argument('--state', choices=['open', 'closed', 'all'], default='open')
    parser.add_argument('--page', type=int, default=1)
    parser.add_argument('--per-page', type=int, default=5)
    args = parser.parse_args()
    async def run():
        return await verify(args.owner, args.repo, origin=args.origin, state=args.state,
                            page=args.page, per_page=args.per_page)
    print(json.dumps(anyio.run(run), ensure_ascii=False, indent=2))
