"""Summarize evaluate.py runs (and a-commerce's own report rows) per mode.

python examples/acommerce/summarize.py artifacts/acommerce/runs/ours-design-1.jsonl [more.jsonl ...]
"""

from __future__ import annotations

import json
from pathlib import Path
import statistics
import sys


def load(paths):
    runs = []
    for path in paths:
        for line in Path(path).read_text().splitlines():
            record = json.loads(line)
            if record.get('type') == 'run':
                record['file'] = Path(path).name
                runs.append(record)
    return runs


def table(runs):
    modes = list(dict.fromkeys(run['mode'] for run in runs))
    rows = ['| mode | runs | done | host errors | tool calls/run | failed tool calls | model calls/run | tokens/run (mean) | '
            'first prompt tokens (median) | seconds/run (mean, median) |', '|---|---|---|---|---|---|---|---|---|---|']
    for mode in modes:
        group = [run for run in runs if run['mode'] == mode]
        done = sum(run['done'] for run in group)
        errors = sum(1 for run in group if run.get('hostError'))
        failed = sum(1 for run in group for name, ok in run['tools'] if not ok)
        first = [run['firstPromptTokens'] for run in group if run.get('firstPromptTokens')]
        seconds = [run['seconds'] for run in group]
        rows.append(f"| {mode} | {len(group)} | {done}/{len(group)} ({done / len(group):.0%}) | {errors} | "
                    f"{statistics.mean(len(run['toolCalls']) for run in group):.1f} | {failed} | "
                    f"{statistics.mean(run['modelRequests'] for run in group):.1f} | "
                    f"{statistics.mean(run['usage']['total_tokens'] for run in group):.0f} | "
                    f"{statistics.median(first) if first else '—'} | "
                    f"{statistics.mean(seconds):.1f}, {statistics.median(seconds):.1f} |")
    return '\n'.join(rows)


def per_task(runs):
    modes = list(dict.fromkeys(run['mode'] for run in runs))
    tasks = list(dict.fromkeys(run['task'] for run in runs))
    rows = ['| task | ' + ' | '.join(modes) + ' |', '|---' * (len(modes) + 1) + '|']
    for task in tasks:
        cells = []
        for mode in modes:
            group = [run for run in runs if run['task'] == task and run['mode'] == mode]
            cells.append(' '.join('✓' if run['done'] else ('E' if run.get('hostError') else '✗') for run in group) or '—')
        rows.append(f'| {task} | ' + ' | '.join(cells) + ' |')
    return '\n'.join(rows)


def main():
    runs = load(sys.argv[1:])
    print(table(runs))
    print()
    print(per_task(runs))
    print()
    for run in runs:
        if not run['done']:
            print(f"- {run['task']} [{run['mode']}] {run.get('hostError') or ''} {'; '.join(run['missing'])[:400]}")


if __name__ == '__main__':
    main()
