"""MCP stdio server exposing one generated benchmark API through the three a2api tools."""

import argparse
from pathlib import Path
import sys

import anyio

sys.path.insert(0, str(Path(__file__).resolve().parent))

from a2api import ExecutionContext  # noqa: E402
from a2api.mcp_bridge import serve_stdio  # noqa: E402
from application import application  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scale', choices=['small', 'medium', 'large'], required=True)
    parser.add_argument('--language', choices=['python', 'spring', 'go', 'rust'], required=True)
    parser.add_argument('--origin', default='', help='Running server origin (not used for python)')
    args = parser.parse_args()
    app = application(args.scale, args.language, args.origin or None)
    anyio.run(serve_stdio, app, ExecutionContext('bench-user', 'tenant-a', frozenset()))


if __name__ == '__main__':
    main()
