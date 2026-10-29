"""Serve the two public GitHub capabilities over MCP stdio."""

import argparse

import anyio

from a2api.mcp_bridge import serve_stdio
from agent_app import PUBLIC_CONTEXT, create_app


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--origin', default='https://api.github.com', help='Host-only override for local fixtures')
    args = parser.parse_args()
    # stdout is exclusively the MCP protocol.
    anyio.run(serve_stdio, create_app(args.origin), PUBLIC_CONTEXT)
