"""Host selection for the synthetic examples, not an automatic effect classifier."""

from pathlib import Path

from a2api import HTTPDeployment, convert
from a2api.importers import SpringSourceImporter, GoSourceImporter, RustSourceImporter

ROOT = Path(__file__).resolve().parent
IMPORTERS = {'spring': SpringSourceImporter, 'go': GoSourceImporter, 'rust': RustSourceImporter}
SOURCES = {'spring': ROOT / 'spring/src/main/java', 'go': ROOT / 'go', 'rust': ROOT / 'rust/src'}


def application(language, origin):
    source = IMPORTERS[language].from_directory(SOURCES[language], namespace=language)
    records = list(source.iter_operations())
    unsupported = [r.summary() for r in records if r.status != 'imported']
    if unsupported or source.diagnostics:
        raise ValueError(unsupported or source.diagnostics)
    options, ids = {}, {}
    for item in records:
        key = (item.method, item.path)
        if key in ids:raise ValueError('Ambiguous example route')
        ids[key] = item.id
        effect = 'read' if item.method in ('GET', 'HEAD') or key == ('POST', '/items/search') else 'write'
        options[item.operation_id] = {'effect': effect}
        if item.method != 'HEAD' and item.path != '/items/search' and item.method != 'DELETE':
            options[item.operation_id]['select'] = ['id', 'name']
    return convert(source, operations=options, deployment=HTTPDeployment(origin)), ids
