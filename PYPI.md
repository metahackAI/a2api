# a2api

**a2api turns existing APIs and functions into a small call protocol that LLM hosts can search, describe and invoke cheaply — at any API size.**

Convert what you already have — an OpenAPI document, a Java/Spring MVC, Go `net/http` or Rust Axum source tree, or plain Python functions — and call it directly, through three fixed MCP tools, or as selected function tools for a model. No review files, build directories or registry are required for the first call.

```bash
pip install a2api                 # core: convert, invoke, ToolSession
pip install "a2api[mcp]"          # MCP stdio bridge
pip install "a2api[openapi]"      # YAML OpenAPI documents
pip install "a2api[source]"       # Spring / Go / Rust source importers
```

## Python functions

```python
from typing import TypedDict
from a2api import Application, ExecutionContext, capability

class Order(TypedDict):
    id: str
    status: str

@capability(id="orders.get", effect="read")
def get_order(id: str) -> Order:
    """Get one order by ID."""
    return {"id": id, "status": "paid"}

@capability(id="orders.cancel", effect="write")
async def cancel_order(id: str, *, context: ExecutionContext) -> Order:
    """Cancel an order. Writes are never retried automatically."""
    return {"id": id, "status": "cancelled"}

app = Application([get_order, cancel_order])
caller = ExecutionContext("alice", "tenant-a", frozenset())
print(app.invoke("orders.get", {"id": "ORD-1"}, context=caller))
# {'status': 'succeeded', 'data': {'id': 'ORD-1', 'status': 'paid'}, 'completeness': {...}}
```

Type hints and `TypedDict`s become JSON Schemas; inputs and outputs are validated on every call; `context` is host-only and never part of the model's input.

## OpenAPI or source code → HTTP calls

```python
from a2api import HTTPDeployment, convert
from a2api.importers import OpenAPIImporter, SpringSourceImporter

source = OpenAPIImporter.from_file("orders.openapi.json", namespace="shop")
# or: SpringSourceImporter.from_directory("src/main/java", namespace="shop")  (GoSourceImporter, RustSourceImporter)
app = convert(source, operations={
    "listOrders": {"effect": "read", "select": ["items[].id", "items[].status", "total", "hasMore"]},
    "cancelOrder": {"effect": "write"},
}, deployment=HTTPDeployment("https://orders.internal", credential_provider=lambda ctx: {...}, timeout_ms=5000))
```

`select` keeps only public fields (nested paths and `[]` array items supported) after the raw response is validated against the original schema. Credentials and origins stay with the host.

## Model hosts: ToolSession

```python
from a2api import ToolSession

session = ToolSession(app, caller)               # or ToolSession.from_mcp(mcp_client)
await session.auto(user_question)                # small catalog: all functions; large: host pre-search
tools = session.tools()                          # Chat Completions function tools for this request
result = await session.call(name, arguments)     # validated invoke, never retried
text = session.render(result)                    # compact model-facing result with failure hints
```

Small catalogs are exposed directly; large catalogs get one `a2api_search` tool plus the functions the host pre-selected from the question. Function parameters are the exact business input schema (HTTP `path/query/body` flattened when lossless).

## MCP

```python
import anyio
from a2api.mcp_bridge import serve_stdio
anyio.run(serve_stdio, app, caller)   # tools: a2api.discover / a2api.describe / a2api.invoke
```

The MCP tool list is always the same three tools, whatever the catalog size.

## Protocol

`a2api-call` defines discover/describe/invoke requests, a six-field capability descriptor and structured errors; the JSON Schema ships in the package (`a2api.protocol_schema()`). `a2api-tools` defines how hosts present selected capabilities to models.

## Evaluation

The repository contains a benchmark that implements the same API in Python, Spring, Go and Rust at three sizes and compares a2api with passing the OpenAPI specification to the model. See `docs/34-completion-results.ko.md` in the source repository for the measured accuracy, context size, latency and stability, including failures.

Licensed under MIT.
