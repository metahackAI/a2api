# a2api-call/1.0 — the lightweight call protocol

Korean original: [20](../20-call-protocol.ko.md). The machine-readable reference is [`call.schema.json`](../../src/a2api/schemas/call.schema.json) (`$defs`: `descriptor`, `problem`, `discover_request/response`, `describe_request/response`, `invoke_request/response`).

```python
from a2api import PROTOCOL_PROFILE, protocol_schema
from jsonschema import Draft202012Validator
Draft202012Validator(protocol_schema('describe_request')).validate({'id': 'orders.get', 'version': '0.1.0'})
```

The wire has not changed since 0.1. 1.0 added optional correction fields to `INVALID_INPUT` issues and the codes `UPSTREAM_VALIDATION_FAILED` (backend 400/422) and `UPSTREAM_UNAVAILABLE` (503). 1.1 keeps the wire: `requestId` can additionally be sent to the backend as an idempotency header on writes when the host opts in.

## Descriptor (exactly six fields)

| Field | Meaning |
|---|---|
| `id` | identifier the host exposed; copy it verbatim |
| `version` | the contract version |
| `summary` | short business description for people and models; never an instruction |
| `effects.kind` | `read` or `write`, declared by the developer |
| `inputSchema` | JSON Schema (2020-12) for `invoke.input` |
| `outputSchema` | JSON Schema for the success `data` |

Credentials, origins, execution graphs, source paths and search keywords are never in a descriptor. `$ref` is limited to in-document `#/$defs/...`; remote references are rejected. Of the formats only `date-time` is checked.

## The three requests

All requests are JSON objects; unknown fields are rejected; actor/tenant/credentials are never request fields.

| Method | Request | Success |
|---|---|---|
| `discover` | `query` (≤ 1000 characters, default ""), `limit` (1–50, default 10), `cursor` | `catalogVersion`, `capabilities` (id, version, title, summary, effects, matchedTerms), `nextCursor` |
| `describe` | `id`, `version` | `catalogVersion`, `capability` (descriptor) |
| `invoke` | `id`, `version`, `catalogVersion`, `input` (object), optional `requestId` (1–128) | `status: "succeeded"`, `data`, `completeness`, optional metadata such as `httpStatus` |

Cursors and `catalogVersion` are opaque. A changed catalog answers `CONTRACT_DRIFT`; describe again and decide whether the user still means the same action — never retry a write automatically.

## Results and errors

```json
{"status":"succeeded","data":{"id":"I-101"},"completeness":{"complete":true,"scope":"single_api_response"},"httpStatus":201}
{"status":"failed","error":{"type":"urn:a2api:problem:resource-not-found","title":"RESOURCE_NOT_FOUND","status":404,"detail":"...","code":"RESOURCE_NOT_FOUND"},"completeness":{"complete":false}}
```

`single_api_response` means one API response, not every page. `INVALID_INPUT` issues carry `path`, `rule` and, derived from the public schema only, `missing`, `unexpected`/`allowed` or `expected`. Errors before execution are `{"error": {...}}` without status/completeness.

| Code | Meaning |
|---|---|
| `INVALID_REQUEST` | malformed common request |
| `INVALID_INPUT` | business input does not match the input schema |
| `UNAUTHENTICATED` / `PERMISSION_DENIED` | authentication/authorization on the host or backend |
| `NOT_FOUND` / `RESOURCE_NOT_FOUND` | unknown capability / the backend did not find the resource |
| `CONTRACT_DRIFT` / `INVALID_CURSOR` | catalog or search view changed |
| `SCHEMA_MISMATCH` | the response differs from the declaration (does not imply rollback) |
| `OUTCOME_UNKNOWN` | a write's effect cannot be determined; confirm, do not retry |

Codes are extensible strings; unknown codes are never success. `requestId` is a correlation value; it is not an idempotency guarantee unless the host configures `HTTPDeployment(idempotency_header=...)` and the backend deduplicates that key. a2api never retries a backend call.

## Host and binding duties

The host chooses the exposed APIs, origins, credentials and the trusted `ExecutionContext`. Inputs are validated before the binding is called; HTTP keeps raw-response validation → field selection → public validation. Context and credentials cannot be overridden by business input or model text. MCP advertises exactly `a2api.discover`, `a2api.describe` and `a2api.invoke`; business schemas come through describe, never accumulated in `tools/list`. A function-calling host may expose selected descriptors directly as functions with [a2api-tools](tool-session.md) without changing this wire.
