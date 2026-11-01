# a2api-tools/1.0 — giving the model only the contracts it needs

Korean original: [24](../24-selected-tools.ko.md). `ToolSession` is a **host** profile over the unchanged [call protocol](call-protocol.md): MCP keeps its three tools; the host turns selected descriptors into Chat Completions functions.

```python
from a2api import ToolSession

session = ToolSession(apps, context)            # one session per user/tenant/permission set
await session.auto(question)                    # prepare functions without a model turn or a business call
tools = session.tools()                         # read again before every model request
payload = await session.call(name, arguments, request_id=tool_call_id)
text = session.render(payload)                  # compact text for the model
```

## What the model sees

- **Readable names** made from capability IDs (`legacy_getorder`); collisions get an 8-character hash suffix. `naming="hash"` keeps the older `a2api_call_<hash>` names. A name is not a permission; unselected names answer `NOT_SELECTED`.
- **Flat HTTP inputs**: `{path, query, headers, body}` shown as one object when names do not collide; calls are restored to the original shape and validated as usual (`flatten=False` turns this off).
- **Descriptions**: the summary and `[write]` for writes (`hints="none"`, the default); `hints="shape"` adds a short list of returned fields; `hints="typed"` keeps the 0.3 representation.
- **Compact results**: `render()` gives `status` + `data` (and `httpStatus`/`completeness` only when not the default); failures give `code`, `detail`, `issues` and a short `hint` about what retrying or searching cannot fix.

## Strategies

`auto(question, max_functions=64, preselect=8, all_bytes=10000)`: a catalog whose whole function set fits `all_bytes` (about 20 functions) and `max_tool_bytes` (default 16000) is given whole and the search tool is left out (`strategy="all"`). Otherwise the host searches the question for up to `preselect` candidates and keeps `a2api_search` (`strategy="search"`). `prime([...])` prepares known IDs; `select(query)` is a host search without a model turn (useful at the start of a later conversation turn).

(1.1) `index(question, detail='summary'|'names', group=None, related=0, relations=None, preselect=0)`: for large catalogs whose requests do not share words with function names. The host puts the returned `text` — every function's name (and with `detail='summary'` the first sentence of its summary), optionally under `group(entry)` headings — into the system prompt; it does not change during the session, so it stays in the cached prompt prefix. `tools()` then holds `a2api_load` and the loaded functions. The model loads what it chooses with `a2api_load({"names": [...]})`; unknown names come back with `suggest`. Calling an unloaded function straight from the index loads it: a read with valid arguments runs, a write answers `NOT_LOADED` without running. `related=N` adds to successful results up to N functions that take an ID the result returned (`relations` such as `ToolCatalogImporter.relations()`, or inputs named like IDs); `focus(text)` re-ranks them for each new user turn. `preselect=N` also loads the host search's candidates. Measured choices are in [the 1.1 results (Korean)](../39-improvement-results.ko.md) §3.8.

```python
built = await session.index(question, detail='names', group=lambda entry: domain_of[entry['id']])
messages = [{'role': 'system', 'content': base_prompt + '\n\n' + built['text']}, ...]
tools = session.tools()                          # a2api_load + loaded functions
```

## Search tool

Input `{"query": "...", "more": false}`. Selected functions become callable on the **next** model request. Results:

```json
{"selected": [{"name": "legacy_getorder", "id": "legacy.getorder"}], "added": ["legacy_getorder"],
 "omitted": [], "evicted": [], "moreAvailable": false, "page": 1, "pageLimitReached": false, "progress": true}
```

`more=true` pages (at most three pages per query). `progress=false` means the same query returned nothing new. (1.1) `added` lists the functions this search made callable; when every match was already callable, the model-facing result carries a note telling it not to search again but to say what is missing.

## Session rules (1.1 additions marked)

1. The function list is bounded by `max_tool_bytes`; whole definitions are kept (required fields, enums, `$defs` intact). (1.1) Functions keep their position in the list across calls and searches so consecutive requests share a prompt prefix; when the budget is exceeded, the least recently used function leaves.
2. String path/query/header parameters accept JSON numbers/booleans and send their text. (1.1) A string body field accepts an integer and sends its digits (IDs like `20431`).
3. (1.1) A call whose exact name and arguments already failed in this session carries `repeated` and a hint that repeating it will fail again. A read with the same arguments that already succeeded since the last write carries `repeated` and a note that the data is already in the conversation. Nothing is blocked.
4. (1.1) `request_id` reaches the backend as an idempotency header on writes when the deployment sets `idempotency_header`.
5. A changed catalog clears the selection (`CONTRACT_DRIFT`); writes are never retried.
