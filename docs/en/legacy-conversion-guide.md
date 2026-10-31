# Converting an existing (legacy) API to a2api

Updated 2026-11-01 for a2api 1.1 (`pip install "a2api[mcp,openapi,source]"`). Korean original: [36](../36-legacy-conversion-guide.ko.md).

This guide turns an API that already runs in production into a2api capabilities an LLM can call. Pick a path:

- **Path A — you have OpenAPI and the code.** Convert from OpenAPI; use the code to check that the document matches the implementation.
- **Path B — you have code but no OpenAPI.** Spring MVC, Go (net/http, Gin), Rust Axum and Python FastAPI routes and DTOs are read from the source; plain Python code is registered as functions; other stacks follow B-3.
- **Path C — the running service publishes a tool catalog** (name, summary, input schema) and takes calls by name. Import the catalog; show legacy abbreviations and codes as readable names and words with a vocabulary.

Every snippet comes from an example that runs: [`examples/legacy-conversion/`](../../examples/legacy-conversion/README.md) (`openapi_and_code.py` A, `code_only.py` B-1, `python_functions.py` B-2, `legacy_screens.py` C). Results on real open-source projects are in section 9.

```text
                         ┌─ the document matches the code ───────────────► Path A
OpenAPI exists ──────────┤
                         └─ outdated or partial ─┬─ the framework can regenerate it → regenerate, Path A
                                                 └─ Spring/Go/Rust/FastAPI code ─────→ Path B-1
No OpenAPI ─┬─ the service publishes a tool catalog and takes calls by name ──────────► Path C
            ├─ Spring MVC / Go net/http, Gin / Rust Axum / Python FastAPI ─────────────► Path B-1
            ├─ Python functions without HTTP ─────────────────────────────────────────► Path B-2
            └─ other stacks (Node, C#, PHP, Echo, Chi, Actix, Flask, Django…) ─────────► Path B-3
```

Every path produces the same thing: an **in-memory a2api app** (`ConvertedAPI` or `Application`). Call it as a library, serve it as three MCP tools, or attach it to a model host's `ToolSession`. No import files, review or build directories are needed.

## 1. Concepts

| Concept | Meaning | Decided by |
|---|---|---|
| capability | One function an LLM can call, usually one API operation or one Python function | the developer chooses what to expose |
| descriptor | Six fields — `id`, `version`, `summary`, `effects.kind`, `inputSchema`, `outputSchema` — the contract the model sees | importer, then the developer edits the summary |
| effect | `read` or `write`. GET/HEAD are read; PUT/PATCH/DELETE are write; **POST must be declared** | the developer (never guessed) |
| select | Response fields sent to the model; internal fields are removed on the server | the developer |
| deployment | Origin, per-user credentials, limits, host request values | the host |
| context | The caller (`ExecutionContext(actor, tenant, scopes)`); never model input | the host's authentication layer |

Every call returns the same envelope:

```python
{'status': 'succeeded', 'data': {...}, 'completeness': {'complete': True, 'scope': 'single_api_response'}}
{'status': 'failed', 'error': {'code': 'RESOURCE_NOT_FOUND', 'detail': '...', 'status': 404, ...}, 'completeness': {'complete': False}}
```

Execution order: validate input → call the original service (never retried) → validate the raw response → select public fields → validate the public response. The original service keeps enforcing authorization; connecting it to a2api grants nothing.

## 2. Path A — OpenAPI and code

### A-1. Read the document and check what cannot be converted

```python
from a2api.importers import OpenAPIImporter

source = OpenAPIImporter.from_file('openapi.json', namespace='shop',
                                   methods={'GET', 'POST', 'PATCH', 'DELETE'})   # default: GET only
for record in source.iter_operations():
    if record.status != 'imported':
        print(record.summary())   # operationId, method, path, status, diagnostics (reason codes)
```

OpenAPI 3.0/3.1, JSON, YAML (`a2api[openapi]`) and `.gz`. External `$ref` files are not followed (bundle first). CLI: `python -m a2api import-openapi openapi.json --namespace shop --methods GET POST PATCH DELETE --output report-dir`.

| Reason | Meaning | What to do |
|---|---|---|
| `NO_SUPPORTED_SUCCESS` | no 2xx response schema (e.g. redirect-only) | add a JSON success schema or a 204 |
| `UNSUPPORTED_RESPONSE` | non-JSON success (file, text) | leave it out or wrap it (B-2) |
| `UNSUPPORTED_REQUEST_BODY` | multipart/form body | leave it out or wrap it |
| `UNSUPPORTED_PARAMETER_SCHEMA` | a parameter without defined serialization (a **required** nullable query, object parameters) | simplify. Since 1.1 an optional nullable query/header parameter is converted: null is sent by omitting it (`NULL_PARAMETER_OMITTED`) |
| `GET_REQUEST_BODY` | body on GET | fix the document |
| `METHOD_NOT_SELECTED` | method not in `methods` | add it if needed |

The GitHub REST document converts 1,230 of 1,254 operations with all methods selected.

### A-2. Check the document against the code

```python
from a2api.importers import GoSourceImporter   # SpringSourceImporter, RustSourceImporter, FastAPISourceImporter

documented = {(r.method.upper(), r.path) for r in source.iter_operations() if r.status == 'imported'}
code = GoSourceImporter.from_directory('service/', namespace='code')
implemented = {(r.method.upper(), r.path) for r in code.iter_operations() if r.status == 'imported'}
print('code only:', implemented - documented, 'document only:', documented - implemented)
```

Routes only in the document are not implemented (do not expose them). Business routes only in the code: regenerate the document, or convert those routes with Path B-1 and attach both apps. Type differences surface as `SCHEMA_MISMATCH` at the first call.

### A-3. Choose operations and settings

```python
from a2api import ExecutionContext, HTTPDeployment, convert

operations = {
    'listOrders': {'effect': 'read',
                   'select': ['items[].id', 'items[].status', 'items[].totalAmount', 'total', 'hasMore'],
                   'keywords': ['order list', 'orders']},
    'getOrder': {'effect': 'read', 'select': ['id', 'customerId', 'status', 'totalAmount', 'shipmentIds']},
    'cancelOrder': {'effect': 'write', 'select': ['id', 'status'],
                    'summary': 'Cancel an order. Only pending/paid orders; otherwise 409.'},
}
```

- Keys are `operationId`s. Public IDs are `namespace.operationid` (lowercase; `/` and `.` separate segments).
- `effect` is required; contradictions (GET as write) fail with `INVALID_CONVERSION`.
- `select` paths: `'id'`, `'owner.login'`, `'items[].id'`, `'[].login'`. Leave internal fields out.
- `summary` replaces the document's summary: write the constraints the model must know in one sentence.
- `keywords` are search-only words (never shown to the model).

### A-4. Connection, authentication and host values

```python
app = convert(source, operations=operations, deployment=HTTPDeployment(
    'https://orders.internal',                     # path prefix: path_prefix='/api'
    credential_provider=lambda context: {'Authorization': 'Bearer ' + token_for(context.actor)},
    timeout_ms=5000, deadline_ms=8000,
))
```

- `credential_provider(context)` builds headers **per call** from the trusted context. Use per-user credentials.
- Fixed headers: `headers={...}`. Authentication and cookies are never model input.
- (1.1) **Host request values**: `request_values=lambda context, call: {'query': {...}, 'body': {...}}`, where `call` carries `operationId`, `method`, `path`, `effect`. Use it for preview flags, change-set IDs or tenants. A name that collides with model input fails with `HOST_VALUE_CONFLICT` before any call.
- (1.1) **Backend error sentences**: bodies of failed responses are not forwarded by default. `error_detail=lambda status, body: ...` picks a safe part (e.g. `body['error']['message']`), appended to `detail` (≤ 500 characters).
- (1.1) **Idempotency on writes**: with `idempotency_header='Idempotency-Key'`, the `request_id` of `invoke(..., request_id=...)` or `ToolSession.call(..., request_id=...)` is sent in that header on **write** operations only. a2api still never retries.
- A write that times out after being sent is `OUTCOME_UNKNOWN`; confirm with a read.

### A-5. Call and check

```python
caller = ExecutionContext('alice', 'tenant-a', frozenset())
app.invoke('shop.getorder', {'path': {'id': 'ORD-1003'}}, context=caller)
app.invoke('shop.cancelorder', {'path': {'id': 'ORD-1007'}}, context=caller)['error']['code']   # 'UPSTREAM_CONFLICT'
```

Direct input keeps the HTTP locations `{'path', 'query', 'headers', 'body'}`; `ToolSession` shows them flat to the model. Status mapping: 400/422 → `UPSTREAM_VALIDATION_FAILED`, 401/403 → `PERMISSION_DENIED`, 404 → `RESOURCE_NOT_FOUND`, 409 → `UPSTREAM_CONFLICT`, 429 → `RATE_LIMITED`, 503 → `UPSTREAM_UNAVAILABLE`, others → `UPSTREAM_ERROR`, timeout → `DEADLINE_EXCEEDED`.

## 3. Path B-1 — code only: Spring, Go, Rust, FastAPI

Source importers **never execute** project code. Java/Go/Rust are parsed with tree-sitter; Python with the standard `ast` module.

| Importer | Routes and inputs | DTOs and outputs | Not supported → what to do |
|---|---|---|---|
| `SpringSourceImporter` | `@RestController` + class/method mappings; `@PathVariable`, `@RequestParam`, `@RequestHeader`, `@RequestBody`; principals/request objects are host values | scalars, List/Set/Map, records/POJOs (inheritance, concrete generics, Lombok `@Getter/@Data/@Value`, public getters in outputs), enums, `@Valid` constraints, `@ResponseStatus`. (1.1) A raw `ResponseEntity`/`Map` return is followed through `ResponseEntity.ok(...)`, `status(201).body(...)`, `new HashMap<>(){{ put(...) }}`, service field method return types, `Optional.map(lambda).orElseThrow()` and same-class helpers. `spring.jackson.*` in application properties/YAML (root wrapping, naming strategy, inclusion) is applied | dynamic path constants, WebFlux, custom serializers, `ResponseBodyAdvice` or binder advice. Exception-only `@RestControllerAdvice` no longer blocks |
| `GoSourceImporter` | net/http `HandleFunc("METHOD /path", h)`, `r.PathValue`, `r.URL.Query().Get`, typed `json.NewDecoder(r.Body).Decode`. (1.1) **Gin**: `Group("/p")` prefixes, also through registration functions that take a router (across packages); `:param`; `c.Param`, `c.Query`, `DefaultQuery`, `QueryArray`; `ShouldBind*`/`Bind*`; validator objects whose `Bind(c)` passes the receiver to a binder | structs with JSON tags (anonymous and embedded structs; `binding:"required,min,max,email,oneof"`), pointers/slices/maps, `time.Time`; `Encode(v)` or `c.JSON(2xx, v)` with a concrete type, or `gin.H{...}` whose values have readable types (locals, function and method results) | Echo/Chi, closures, `c.GetRawData`, forms/files. `_test.go` files are ignored |
| `RustSourceImporter` | `Router::new().route(...)` chains; (1.1) `.merge(...)` and literal `.nest("/p", ...)`, `{p}` and `:p` paths, handlers resolved by module path; `Path`/`Query`/`Json`. `State`, `Extension`, headers and the project's `FromRequest` types (an authenticated user) come from the request context (`CONTEXT_EXTRACTOR` note) | named-field and newtype Serde structs (rename, rename_all, default, skip, flatten), generics with defaults (`Body<T = Article>`), hand-written `Serialize` that writes a string, `Option`/`Vec`/`HashMap`, `Json<T>`, `Result<T>`/`Result<T, E>`, `(StatusCode, Json<T>)`, `()` | Actix, wildcard routes, data-carrying enums, `#[serde(with = ...)]` |
| `FastAPISourceImporter` (1.1) | read with `ast` only: `APIRouter(prefix=)` and `include_router(prefix=)` followed from the application (a prefix from a settings default is noted); `@router.get/post/...`; path, `Query`/`Path`/`Body(embed, alias)`/`Header`; route `dependencies=[Depends(...)]` and inputs inside `Depends(fn)` | Pydantic models (inheritance and mixins, `Field(alias=, ...)`, `alias_generator` when it is a known camel/pascal converter), `Optional`/`List`/`Dict`/`Literal`/`Enum`; `response_model` or the return annotation; `status_code` | form/file, non-JSON `response_class`, unknown alias functions. Test files are ignored |

```python
from a2api.importers import SpringSourceImporter

source = SpringSourceImporter.from_directory('src/main/java', namespace='shop')
for record in source.iter_operations():
    print(record.summary())   # operationId, path, method, status, location, diagnostics
```

`location` points at the code. Selecting an unsupported handler fails `convert`; types are never guessed. (1.1) When only the **response** type cannot be read, `untyped_output='open'` imports the operation with an open output schema `{}` and an `OUTPUT_UNTYPED` warning; inputs are never guessed. Two handlers with the same operation ID no longer abort the import: the first is kept and the later one is reported.

Expose by `(method, path)` so one table works across languages:

```python
EXPOSE = {('GET', '/customers'): {'effect': 'read', 'summary': 'List customers (tier/status/city filters, page/limit).'},
          ('POST', '/customers/search'): {'effect': 'read'},     # a read POST must say so
          ('POST', '/tickets'): {'effect': 'write', 'summary': 'Create a ticket. Required: customerId, subject, priority (low|normal|high|urgent).'}}
operations = {r.operation_id: EXPOSE[(r.method.upper(), r.path)] for r in source.iter_operations()
              if r.status == 'imported' and (r.method.upper(), r.path) in EXPOSE}
app = convert(source, operations=operations, deployment=HTTPDeployment('http://customers.internal:8080'))
```

Language differences follow each language's real JSON behavior: required body fields come from `@NotBlank`/`@NotNull` (Spring), `binding:"required"` (Gin; net/http has none), non-`Option` fields (Rust) and fields without defaults (Pydantic). A Gin update form pre-filled from the stored record before `Bind` is read as a partial update. When enums or required inputs are not in the code, write them in the summary.

`ToolSession` sends JSON numbers/booleans given for string path/query/header parameters as text; (1.1) an integer given for a string body field (an ID like `20431`) is sent as its digits.

## 4. Path B-2 — Python functions without HTTP

Register thin wrappers that decide inputs, public fields and effects:

```python
from typing import Literal, TypedDict
from a2api import A2APIError, Application, ExecutionContext, capability

class Order(TypedDict):
    id: str
    state: Literal['pending', 'paid', 'shipped', 'cancelled']
    amount: int

@capability(id='orders.get', effect='read', keywords=['order', 'lookup'])
def get_order(orderId: str, *, context: ExecutionContext) -> Order:
    """Look up the state and amount of one of my orders."""
    row = SERVICE.find_visible(orderId, context.actor)
    if row is None:
        raise A2APIError('RESOURCE_NOT_FOUND', 'Order does not exist or is not visible.', status=404)
    return {'id': row.id, 'state': row.state, 'amount': row.amount}

app = Application([get_order])
```

Schemas come from type hints (`str/int/float/bool/None`, `Literal`, `X | None`, `list[X]`, `dict[str, X]`, `TypedDict`); `context` is keyword-only and never model input; sync and `async def` both work; raise `A2APIError` for business errors.

## 5. Path B-3 — other stacks

1. Generate OpenAPI where the framework can (NestJS swagger, ASP.NET Swashbuckle/NSwag, Echo/Chi swag, Actix utoipa) and follow Path A.
2. For a few routes, hand-write a small OpenAPI document for just those routes.
3. To combine calls or reshape results, wrap the existing HTTP calls in Python (B-2).

## 5-1. Path C — tool catalogs, call-by-name services and legacy vocabulary (1.1)

Registry-style back ends and screen-shaped legacy services often publish `GET /v1/tools` (`tool`, `summary`, closed `input_schema`) and take `POST /v1/tools/{name}` with `{"input": {...}}`.

```python
from a2api.importers import ToolCatalogImporter

source = ToolCatalogImporter.from_url(origin + '/v1/tools', namespace='claims')     # or ToolCatalogImporter(list_or_dict)
kinds = {r.operation_id: r.entry['kind'] for r in source.iter_operations()}       # entry: the catalog item
app = convert(source, operations={n: {'effect': 'read' if k == 'read' else 'write'} for n, k in kinds.items()},
              vocabulary=VOCABULARY, deployment=HTTPDeployment(origin, request_values=..., error_detail=...))
```

`call_path`, the body envelope (`envelope='input'`) and key names are configurable. camelCase names keep their words in IDs (`getClmGridList` → `claims.get_clm_grid_list`).

**Vocabulary.** Abbreviated fields (`clmStatCd`) and code values (`"R10"`) are hard for a model. Write only what the source's code tables and field comments say:

```python
VOCABULARY = {
    'rename': {'clmStatCd': 'claim_status', 'clmNo': 'claim_id', 'pageNo': 'page'},     # inputs and outputs
    'codes': {'clmStatCd': {'R10': 'requested', 'R20': 'approved', 'R90': 'completed'}},
    'describe': {'pageNo': 'Page number, from 1.'},                                      # rules only the code knows
}
```

The model sends `claim_status: "requested"`; a2api validates against the public schema, maps names and words back to the legacy ones, and maps responses the same way (unknown codes pass through). Rules that live only in people's heads (discount caps, return windows) cannot be recovered this way; on a-commerce such screen APIs stayed unable to solve rule-dependent tasks ([39](../39-improvement-results.ko.md)).

## 6. Connecting a model

MCP server (three tools whatever the API size):

```python
import anyio
from a2api.mcp_bridge import serve_stdio
anyio.run(serve_stdio, [http_app, python_app], caller)
```

Chat Completions function calling:

```python
from a2api import ToolSession
session = ToolSession([http_app, python_app], caller)
await session.auto(user_message)            # small catalogs whole; otherwise 8 pre-searched functions + a search tool
tools = session.tools()                     # read again before every model request
payload = await session.call(name, args, request_id=tool_call_id)
text = session.render(payload)              # compact text for the model
```

(1.1) The function list keeps its order across calls and searches (a stable prompt prefix). A search that finds nothing new says so; a call that already failed with the same arguments, or a read already answered since the last write, carries a repeat note. Create a new `ToolSession` when the user, tenant or permissions change.

## 7. Checklist

- [ ] Every exposed operation is `imported`; reasons for the rest are understood.
- [ ] (Path A) Document and code routes compared.
- [ ] Every POST has an explicit effect; read POSTs are `read`.
- [ ] Internal fields are hidden with `select`; real responses pass without `SCHEMA_MISMATCH`.
- [ ] `credential_provider` uses per-user credentials; the service checks object permissions.
- [ ] 200/404/409/400/timeout tried with direct calls (writes on test data).
- [ ] Summaries state allowed values, required inputs and state conditions where the code does not.
- [ ] A few real model questions run through MCP or `ToolSession`.

## 8. Errors

| Stage | Code | Cause → fix |
|---|---|---|
| convert | `INVALID_CONVERSION` | missing effect, effect contradicts method, unknown option or vocabulary key |
| convert | `INVALID_SELECTION` | unknown operation, `select` field not in the response |
| convert | `CONVERT_OPERATION_UNSUPPORTED` | the selected operation was not imported → see `record.summary()` |
| invoke | `INVALID_INPUT` | input does not match; see `issues` (`missing`, `unexpected`, `expected`) |
| invoke | `HOST_VALUE_CONFLICT` / `HOST_VALUES_UNAVAILABLE` | host request values collide with model input / the host function failed |
| invoke | `SCHEMA_MISMATCH` | the service answered differently from the document/DTO |
| invoke | `UPSTREAM_*`, `PERMISSION_DENIED`, `RESOURCE_NOT_FOUND` | the service's answer (A-5) |
| invoke | `DEADLINE_EXCEEDED` / `OUTCOME_UNKNOWN` | raise `timeout_ms`; confirm writes with a read |

## 9. Results on real open-source code (1.1)

The same RealWorld (Conduit) API, implemented by four public projects, converted from **code only** (nothing built or run) and compared with the official OpenAPI's 19 operations (`python examples/realworld/compare.py <checkouts>`):

| Project | 1.0 | 1.1 operations | Field names agree | Remaining differences (real behavior) |
|---|---|---|---|---|
| Spring Boot | 0/19 (global advice rejected all) | 19/19 | 18/19 | article update takes no `tagList` |
| Go Gin | 0 (Gin unsupported) | 19/19 | 16/19 | sign-up also takes bio/image; deletes answer 200 `{"article": "delete success"}` |
| Rust Axum | import aborted (handler name clash) | 19/19 | 18/19 | article update takes no `tagList` |
| Python FastAPI | no importer | 19/19 | 18/19 | article update takes no `tagList` |

Against a specification-conformant server that reproduces each implementation's declared differences, every converted operation of all five sources (OpenAPI, Spring, Go, Rust, FastAPI) answers with a valid result (`python examples/realworld/evaluate.py verify <checkouts>`).

## 10. Optional management features

Teams that want files, reviews and change tracking can use `import-openapi`, `build`, `diff-openapi`/`regenerate` and `prepare-review`/`approve-review`. They are not prerequisites for the first call.
