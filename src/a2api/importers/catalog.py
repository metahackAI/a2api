"""Tool catalogs served by a running service: a name, a summary and a closed JSON input schema.

Registry-style back ends (one typed operation definition that produces REST routes and a tool
manifest, e.g. `GET /v1/tools`) and call-by-name endpoints (`POST /v1/tools/{name}` with
`{"input": {...}}`) are common in service code that has no OpenAPI document. This importer reads
such a catalog and binds each entry to its call-by-name endpoint. Nothing is executed while
importing; the service is called only through `convert(...).invoke`.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field, fields
import json
from pathlib import Path
import re
from typing import Mapping
from urllib.parse import quote
from urllib.request import Request, urlopen

from ..errors import A2APIError
from ..ir import freeze
from ..openapi_schema import check_draft_schema
from .source import SourceRecord, Unsupported, identifier, object_schema, record


def snake(name, words=None):
    """`getClmGridList` -> `get_clm_grid_list`, so ids and function names keep their words.

    words ({'clm': 'claim', 'cnt': 'count'}) spells out abbreviated parts: `get_claim_grid_list`."""
    name = re.sub(r'(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', '_', name).replace('-', '_')
    if words:
        name = '_'.join(words.get(part.lower(), part) for part in name.split('_'))
    return name


@dataclass(frozen=True)
class CatalogRecord(SourceRecord):
    """A SourceRecord that also keeps the catalog entry (kind, links, errors) for host decisions."""

    entry: Mapping = field(default_factory=dict)


class ToolCatalogImporter:
    """Import `[{name, summary, input_schema, ...}]` (or `{"items": [...]}`) tool catalogs."""

    language = 'catalog'

    def __init__(self, tools, *, namespace='tools', name_key='tool', summary_key='summary',
                 input_key='input_schema', call_path='/v1/tools/{name}', envelope='input', source_name='<memory>',
                 words=None):
        if not re.fullmatch(r'[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)*', namespace):
            raise A2APIError('INVALID_SOURCE', 'Use a lowercase dotted namespace.')
        # Abbreviated name parts spelled out in capability IDs (the call still uses the catalog name).
        if words is not None and (not isinstance(words, Mapping) or any(
                not isinstance(k, str) or not isinstance(v, str) or not re.fullmatch(r'[a-z][a-z0-9_]*', v)
                for k, v in words.items())):
            raise A2APIError('INVALID_SOURCE', 'words maps name parts to lowercase snake_case words.')
        self.words = {key.lower(): value for key, value in (words or {}).items()}
        if isinstance(tools, Mapping):
            tools = tools.get('items', tools.get('tools'))
        if not isinstance(tools, list):
            raise A2APIError('INVALID_SOURCE', 'A tool catalog is a list of entries (or {"items": [...]}).')
        if '{name}' not in call_path or not call_path.startswith('/'):
            raise A2APIError('INVALID_SOURCE', 'call_path must be an origin-relative path containing {name}.')
        self.namespace, self.source_name, self.diagnostics = namespace, source_name, []
        self._records = []
        seen, ids = set(), set()
        for index, entry in enumerate(tools):
            location = f'{source_name}#{index}'
            name = entry.get(name_key) if isinstance(entry, Mapping) else None
            try:
                if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_.-]{0,127}', name):
                    raise Unsupported('Each entry needs a plain tool name.')
                if name in seen or identifier(namespace, snake(name, self.words)) in ids:
                    raise Unsupported('Duplicate tool name.')
                seen.add(name)
                ids.add(identifier(namespace, snake(name, self.words)))
                self._records.append(self._record(entry, name, summary_key, input_key, call_path, envelope, location))
            except (Unsupported, A2APIError) as error:
                self._records.append(SourceRecord(str(name or f'entry_{index}'), '', 'POST', '', '', None, None, location,
                                                  ({'code': 'CATALOG_UNSUPPORTED', 'detail': str(error), 'location': location},)))

    def _record(self, entry, name, summary_key, input_key, call_path, envelope, location):
        schema = deepcopy(entry.get(input_key) or {'type': 'object', 'properties': {}, 'additionalProperties': False})
        if not isinstance(schema, dict) or schema.get('type') != 'object':
            raise Unsupported('The input schema must be a JSON object schema.')
        definitions = schema.pop('$defs', None)
        schema.pop('$schema', None)
        inputs = object_schema({'body': schema}, ['body'] if schema.get('required') else [])
        if definitions:
            inputs['$defs'] = definitions
        try:
            check_draft_schema(inputs)
        except A2APIError as error:
            raise Unsupported(error.detail) from None
        summary = entry.get(summary_key) or entry.get('description') or name
        built = record(self.namespace, name, call_path.replace('{name}', quote(name, safe='')), 'POST', inputs, {},
                       location, title=str(summary).strip(), body=True, body_required=bool(schema.get('required')))
        binding = dict(built.binding)
        binding['bodyEnvelope'] = envelope
        values = {item.name: getattr(built, item.name) for item in fields(SourceRecord)}
        values['binding'] = freeze(binding)
        values['id'] = identifier(self.namespace, snake(name, self.words))
        return CatalogRecord(**values, entry=freeze(json.loads(json.dumps(entry, default=str))))

    @classmethod
    def from_file(cls, path, **options):
        data = json.loads(Path(path).read_text())
        return cls(data, source_name=Path(path).name, **options)

    @classmethod
    def from_url(cls, url, *, headers=None, timeout=30, **options):
        """Read a catalog from a running service, e.g. `https://service/v1/tools`."""
        with urlopen(Request(url, headers=dict(headers or {})), timeout=timeout) as response:
            data = json.loads(response.read())
        return cls(data, source_name=url.split('?')[0], **options)

    def relations(self, *, consumes_key='consumes', produces_key='produces'):
        """{id: {'consumes': [...], 'produces': [...]}}: the IDs each entry declares it takes and returns
        (`[{"name": "order_id"}]` or `["order_id"]`), for ToolSession.index(related=...)."""
        def names(value):
            return [item.get('name') if isinstance(item, Mapping) else item for item in value or ()
                    if isinstance(item, str) or (isinstance(item, Mapping) and isinstance(item.get('name'), str))]
        return {item.id: {'consumes': names(item.entry.get(consumes_key)), 'produces': names(item.entry.get(produces_key))}
                for item in self._records if isinstance(item, CatalogRecord)}

    def iter_operations(self, operation_ids: set[str] | None = None):
        found = {item.operation_id for item in self._records}
        if operation_ids is not None and set(operation_ids) - found:
            raise A2APIError('INVALID_SELECTION', 'Selected tool is absent from the catalog.')
        for item in self._records:
            if operation_ids is None or item.operation_id in operation_ids:
                yield item
