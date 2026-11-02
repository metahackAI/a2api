"""Does the conversion lose what the legacy input schemas say? Field by field, the catalog's input schema
against the function parameters the model receives through ToolSession (after convert, vocabulary,
flattening and the model view).

python examples/acommerce/conversion_fidelity.py --acom artifacts/acommerce/manifest-acom.json \
    --facade facade-manifest.json [--json out.json]

For every input field it checks: kept at all, required kept, enum values kept (facade: translated
one to one), description kept or replaced, examples, pattern, format, minimum/maximum and default.
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from a2api import ExecutionContext, HTTPDeployment, ToolSession, convert  # noqa: E402
from a2api.importers import ToolCatalogImporter  # noqa: E402
from legacy_facade import CODES, RENAME, VOCABULARY, WORDS, facade_options  # noqa: E402

KEYS = ('description', 'examples', 'pattern', 'format', 'minimum', 'maximum', 'default', 'minLength', 'maxLength',
        'minItems', 'maxItems')


def fields(schema, prefix=''):
    """{dotted path: field schema} for object properties, nested objects and array items."""
    out = {}
    for name, child in (schema.get('properties') or {}).items():
        path = prefix + name
        out[path] = child
        if child.get('type') == 'object':
            out.update(fields(child, path + '.'))
        if child.get('type') == 'array' and isinstance(child.get('items'), dict) and child['items'].get('properties'):
            out.update(fields(child['items'], path + '[].'))
    return out


def required(schema, prefix=''):
    out = {prefix + name for name in schema.get('required') or []}
    for name, child in (schema.get('properties') or {}).items():
        if child.get('type') == 'object':
            out |= required(child, prefix + name + '.')
        if child.get('type') == 'array' and isinstance(child.get('items'), dict):
            out |= required(child['items'], prefix + name + '[].')
    return out


def strip_null(child):
    """The model view shows an optional `X | null` member as X."""
    branches = child.get('anyOf')
    if isinstance(branches, list) and len(branches) == 2 and {'type': 'null'} in branches:
        return next(branch for branch in branches if branch != {'type': 'null'})
    return child


async def model_view(items, namespace, words=None, facade=False):
    source = ToolCatalogImporter(items, namespace=namespace, words=words)
    options = facade_options(items) if facade else {i['tool']: {'effect': 'read' if i['kind'] == 'read' else 'write'} for i in items}
    app = convert(source, operations=options, deployment=HTTPDeployment('http://127.0.0.1:9'),
                  vocabulary=VOCABULARY if facade else None)
    session = ToolSession(app, ExecutionContext('review', 'store', frozenset()), max_tool_bytes=10_000_000)
    await session.index()
    views = {}
    for record in source.iter_operations():
        name = record.id.split('.', 1)[1]
        await session.call('a2api_load', {'names': [name]})
        tool = next(tool for tool in session.tools() if tool['function']['name'] == name)
        views[record.operation_id] = tool['function']
    return views


def renamed(path):
    return '.'.join(RENAME.get(part.replace('[]', ''), part.replace('[]', '')) + ('[]' if part.endswith('[]') else '')
                    for part in path.split('.'))


def compare(items, views, facade=False):
    rows, totals = [], {'fields': 0, 'dropped': 0, 'required_lost': 0, 'enum_changed': 0}
    totals.update({key + '_lost': 0 for key in KEYS})
    totals.update({'description_replaced': 0, 'description_added': 0})
    for item in items:
        original = item['input_schema']
        view = views[item['tool']]['parameters']
        before, after = fields(original), {k: strip_null(v) for k, v in fields(view).items()}
        need_before, need_after = required(original), required(view)
        for path, child in before.items():
            target = renamed(path) if facade else path
            totals['fields'] += 1
            if target not in after:
                totals['dropped'] += 1
                rows.append({'tool': item['tool'], 'field': path, 'loss': 'field dropped'})
                continue
            got = after[target]
            if path in need_before and target not in need_after:
                totals['required_lost'] += 1
                rows.append({'tool': item['tool'], 'field': path, 'loss': 'required lost'})
            if 'enum' in child:
                expected = [CODES.get(path.split('.')[-1].replace('[]', ''), {}).get(v, v) for v in child['enum']] if facade else child['enum']
                if got.get('enum') != expected:
                    totals['enum_changed'] += 1
                    rows.append({'tool': item['tool'], 'field': path, 'loss': f"enum {child['enum']} -> {got.get('enum')}"})
            for key in KEYS:
                if key in child and key not in got:
                    totals[key + '_lost'] += 1
                    rows.append({'tool': item['tool'], 'field': path, 'loss': f'{key} lost'})
            if child.get('description') and got.get('description') and got['description'] != child['description']:
                totals['description_replaced'] += 1
            if not child.get('description') and got.get('description'):
                totals['description_added'] += 1
    return totals, rows


async def main_async(options):
    report = {}
    for label, path, namespace, words, facade in (('acom', options.acom, 'acom', None, False),
                                                  ('facade', options.facade, 'facade', WORDS, True)):
        if not path:
            continue
        items = json.loads(Path(path).read_text())['items']
        views = await model_view(items, namespace, words, facade)
        totals, rows = compare(items, views, facade)
        report[label] = {'tools': len(items), 'totals': totals, 'losses': rows}
        print(f"== {label}: {len(items)} tools, {totals['fields']} input fields")
        print('   ' + ', '.join(f'{k} {v}' for k, v in totals.items() if k != 'fields'))
        for row in rows[:40]:
            print(f"   - {row['tool']}.{row['field']}: {row['loss']}")
    if options.json:
        options.json.write_text(json.dumps(report, ensure_ascii=False, indent=1))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--acom', type=Path)
    parser.add_argument('--facade', type=Path)
    parser.add_argument('--json', type=Path)
    asyncio.run(main_async(parser.parse_args()))


if __name__ == '__main__':
    main()
