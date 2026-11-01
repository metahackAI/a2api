"""Pre-selection recall without a model: how many of a task's required tools ToolSession.auto() offers
before the first model request (first turn), and after the later turns' host searches.

python examples/acommerce/recall.py --set design [--preselect 8]
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / 'benchmark'))

from a2api import ExecutionContext, ToolSession  # noqa: E402

ROOT = HERE.parent.parent


def load(task_set):
    import importlib.util
    spec = importlib.util.spec_from_file_location('acom_eval', HERE / 'evaluate.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, module.load_tasks(task_set)


async def measure(task_set, preselect):
    module, tasks = load(task_set)
    manifest = json.loads((ROOT / 'artifacts/acommerce/manifest-acom.json').read_text())
    items = manifest['items'] if isinstance(manifest, dict) else manifest

    class Host:
        token = 'unused'

        def change_set(self):
            return 'cs_unused'
    app, names = module.a2api_app(items, Host(), facade=False)
    rows = []
    for task in tasks:
        required = set((task.get('tools') or {}).get('required') or [])
        session = ToolSession(app, ExecutionContext('adm_sj', 'store_northwind', frozenset()))
        await session.auto(task['turns'][0], preselect=preselect)
        first = {names[session.binding(tool['function']['name'])['id']] for tool in session.tools()
                 if session.binding(tool['function']['name'])}
        for line in task['turns'][1:]:
            await session.select(' '.join(line.split())[:1000])
        later = {names[session.binding(tool['function']['name'])['id']] for tool in session.tools()
                 if session.binding(tool['function']['name'])}
        rows.append({'task': task['id'], 'required': sorted(required), 'first': sorted(required & first),
                     'all_turns': sorted(required & later), 'missing': sorted(required - later)})
    total = sum(len(row['required']) for row in rows)
    first = sum(len(row['first']) for row in rows)
    later = sum(len(row['all_turns']) for row in rows)
    return {'set': task_set, 'preselect': preselect, 'required': total, 'firstTurnRecall': round(first / total, 3),
            'allTurnsRecall': round(later / total, 3), 'tasks': rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--set', choices=['design', 'held_out'], default='design')
    parser.add_argument('--preselect', type=int, default=8)
    options = parser.parse_args()
    result = asyncio.run(measure(options.set, options.preselect))
    print(json.dumps({k: v for k, v in result.items() if k != 'tasks'}))
    for row in result['tasks']:
        print(f"  {row['task']:32} {len(row['first'])}/{len(row['required'])} first, missing after all turns: {row['missing']}")


if __name__ == '__main__':
    main()
