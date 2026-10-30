"""Fixed three-tool MCP server for the selected-tool evaluation."""

import argparse
import anyio
from a2api.mcp_bridge import serve_stdio
from catalog import create


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--domain', choices=['orders', 'github'], required=True)
    parser.add_argument('--count', type=int, choices=[2, 1000], default=2)
    parser.add_argument('--origin', required=True)
    args = parser.parse_args()
    apps, context, _ = create(args.domain, args.origin, args.count)
    anyio.run(serve_stdio, apps, context)


if __name__ == '__main__':main()
