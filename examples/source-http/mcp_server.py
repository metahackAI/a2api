import argparse
import anyio

from a2api import ExecutionContext
from a2api.mcp_bridge import serve_stdio
from application import application

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Synthetic source-imported HTTP MCP host')
    parser.add_argument('--language', choices=['spring', 'go', 'rust'], required=True)
    parser.add_argument('--origin', required=True)
    parser.add_argument('--plain-descriptions', action='store_true', help='Use original source titles for comparison')
    args = parser.parse_args()
    app, _ = application(args.language, args.origin, search_metadata=not args.plain_descriptions)
    anyio.run(serve_stdio, app, ExecutionContext('sample-user', 'sample-tenant', frozenset()))
