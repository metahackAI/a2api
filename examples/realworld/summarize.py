"""Summarize RealWorld runs per mode with detailed performance metrics.

python examples/realworld/summarize.py runs/dev.jsonl [more.jsonl ...] [--json out.json]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from run_metrics import by_mode, dump, markdown  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('runs', nargs='+')
    parser.add_argument('--json', type=Path)
    options = parser.parse_args()
    runs = [json.loads(line) for path in options.runs for line in Path(path).read_text().splitlines()]
    runs = [run for run in runs if run.get('type') == 'run']
    metrics = by_mode(runs)
    print(markdown(metrics))
    modes = list(metrics)
    print()
    print('| mode | ' + ' | '.join(dict.fromkeys(run['kind'] for run in runs)) + ' |')
    print('|---' * (1 + len(set(run['kind'] for run in runs))) + '|')
    for mode in modes:
        cells = []
        for kind in dict.fromkeys(run['kind'] for run in runs):
            group = [run for run in runs if run['mode'] == mode and run['kind'] == kind]
            cells.append(f"{sum(run['passed'] for run in group)}/{len(group)}")
        print(f'| {mode} | ' + ' | '.join(cells) + ' |')
    tasks = list(dict.fromkeys(run['task'] for run in runs))
    print()
    print('| task | ' + ' | '.join(modes) + ' |')
    print('|---' * (len(modes) + 1) + '|')
    for task in tasks:
        cells = []
        for mode in modes:
            group = [run for run in runs if run['task'] == task and run['mode'] == mode]
            cells.append(' '.join('✓' if run['passed'] else ('E' if run.get('hostError') else '✗') for run in group) or '—')
        print(f'| {task} | ' + ' | '.join(cells) + ' |')
    if options.json:
        dump(options.json, metrics, runs=options.runs, perTask={
            f"{r['task']}|{r['mode']}|{r.get('repetition', 0)}": {
                'passed': r['passed'], 'hostError': r.get('hostError'), 'tokens': r['usage']['total_tokens'],
                'seconds': r['seconds'], 'modelCalls': r['modelRequests'], 'toolCalls': len(r['toolCalls']),
                'calls': [f"{c['method']} {c['path']} {'ok' if c['ok'] else 'x'}" for c in r['calls']]} for r in runs})


if __name__ == '__main__':
    main()
