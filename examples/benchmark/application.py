"""Host selection for the benchmark: which operations to expose, their effect, public fields and search words.

Spring/Go/Rust use the existing source importers + convert (no OpenAPI); Python uses the
generated @capability functions. The admin routes are evaluator-only and never exposed.
"""

from __future__ import annotations

from a2api import HTTPDeployment, convert
from a2api.importers import GoSourceImporter, RustSourceImporter, SpringSourceImporter

from domain import operations
from servers import GENERATED, python_service

IMPORTERS = {'spring': (SpringSourceImporter, 'spring/src/main/java'), 'go': (GoSourceImporter, 'go'),
             'rust': (RustSourceImporter, 'rust/src')}
PAGE_FIELDS = ['page', 'limit', 'total', 'hasMore']


def public_select(resource, op):
    """Business fields only; tenantId/internalNote/audit stay on the server."""
    fields = ['id', *(item.name for item in resource.fields)]
    if op in ('list', 'search'):
        return ['items[].' + name for name in fields] + PAGE_FIELDS
    if op in ('get', 'create', 'update', 'cancel'):
        return fields
    return None


def application(scale, language, origin=None, *, timeout_ms=10000):
    return converted(scale, language, origin, timeout_ms=timeout_ms)[0]


def converted(scale, language, origin=None, *, timeout_ms=10000):
    """(app, {capability id: "resource.op"}) for one language implementation."""
    if language == 'python':
        return python_service(scale).APPLICATION, {f'shop.{r.key}.{op}': f'{r.key}.{op}' for r, op in operations(scale)}
    importer_type, folder = IMPORTERS[language]
    source = importer_type.from_directory(GENERATED / scale / folder, namespace='shop')
    by_route = {(record.method, record.path): record for record in source.iter_operations()}
    options, ops = {}, {}
    for resource, op in operations(scale):
        record = by_route[resource.route(op)]
        ops[record.id] = f'{resource.key}.{op}'
        option = {'effect': resource.effect(op), 'summary': resource.summary(op), 'keywords': resource.op_keywords(op)}
        selected = public_select(resource, op)
        if selected:
            option['select'] = selected
        options[record.operation_id] = option
    deployment = HTTPDeployment(origin or 'http://127.0.0.1:1', timeout_ms=timeout_ms, deadline_ms=timeout_ms + 5000)
    return convert(source, operations=options, deployment=deployment), ops
