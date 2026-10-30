"""Original three-tool MCP server over the real pinned GET catalog."""

import argparse
import anyio
from a2api.mcp_bridge import serve_stdio
from catalog import CONTEXT, create, load_source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scale', choices=['small', 'large'], default='large')
    parser.add_argument('--origin', required=True)
    args = parser.parse_args()
    source, records, _ = load_source()
    app, _ = create(source, records, args.scale, args.origin)
    anyio.run(serve_stdio, app, CONTEXT)


if __name__ == '__main__':main()
