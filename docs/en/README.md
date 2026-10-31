# a2api documentation (English)

a2api turns existing APIs and functions into a compact call protocol that LLMs can search, describe and invoke, whatever the API size. The Korean documents in [`docs/`](../) are the development record; these English pages cover what a user needs.

- [Converting an existing API](legacy-conversion-guide.md): OpenAPI + code, code only (Spring, Go net/http and Gin, Rust Axum, Python FastAPI), Python functions, tool catalogs and legacy vocabularies; results on real open-source projects.
- [Call protocol `a2api-call/1.0`](call-protocol.md): descriptors, the three requests, results and error codes.
- [Host profile `a2api-tools/1.0`](tool-session.md): `ToolSession` — readable function names, flat inputs, search, budgets and the 1.1 host behavior.

```bash
pip install "a2api[mcp,openapi,source]"
```

```python
from a2api import ExecutionContext, HTTPDeployment, ToolSession, convert
from a2api.importers import OpenAPIImporter

source = OpenAPIImporter.from_file('openapi.json', namespace='shop', methods={'GET', 'POST'})
app = convert(source, operations={'getOrder': {'effect': 'read'}, 'cancelOrder': {'effect': 'write'}},
              deployment=HTTPDeployment('https://orders.internal'))
print(app.invoke('shop.getorder', {'path': {'id': 'ORD-1'}}, context=ExecutionContext('alice', 'tenant-a', frozenset())))
```

Evaluation records (Korean): [34](../34-completion-results.ko.md) (1.0 benchmark), [39](../39-improvement-results.ko.md) (1.1: a-commerce, RealWorld, conversion coverage).
