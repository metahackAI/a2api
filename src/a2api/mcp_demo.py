"""Exercise the packaged stdio server with the official MCP SDK client."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from mcp import Client
from mcp.client.stdio import StdioServerParameters

from .errors import A2APIError


async def run_demo(order_id: str = "ORD-1001", sample_user: str = "alice", build_path: str | Path | None = None) -> dict:
    environment = {"PYTHONPATH": os.environ["PYTHONPATH"]} if "PYTHONPATH" in os.environ else None
    arguments = ["-m", "a2api", "mcp", "--sample-user", sample_user]
    if build_path is not None:
        arguments.extend(['--build', str(Path(build_path).resolve())])
    parameters = StdioServerParameters(command=sys.executable, args=arguments, env=environment)
    async with Client(parameters, read_timeout_seconds=15) as client:
        tools = await client.list_tools()
        found_result = await client.call_tool("a2api.discover", {"query": "배송 조회"})
        found = found_result.structured_content
        if found_result.is_error or not found or not found.get("capabilities"):
            raise A2APIError("DEMO_FAILED", "No matching capability is available for this demo caller.")
        item = found["capabilities"][0]
        described = await client.call_tool("a2api.describe", {"id": item["id"], "version": item["version"]})
        if described.is_error:
            raise A2APIError("DEMO_FAILED", "MCP description failed.")
        invoked = await client.call_tool("a2api.invoke", {
            "id": item["id"], "version": item["version"], "catalogVersion": found["catalogVersion"],
            "input": {"orderId": order_id},
        })
        return {
            "transport": "stdio", "tools": [tool.name for tool in tools.tools], "discover": found,
            "describe": {"id": item["id"], "inputSchema": described.structured_content["capability"]["inputSchema"],
                         "provenance": described.structured_content["capability"]["provenance"]},
            "isError": invoked.is_error, "invoke": invoked.structured_content,
        }
