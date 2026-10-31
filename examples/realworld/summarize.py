"""Summarize RealWorld runs per mode.

python examples/realworld/summarize.py runs/dev.jsonl [more.jsonl ...]
"""

from __future__ import annotations

import json
from pathlib import Path
import statistics
import sys


def main():
    runs = [json.loads(line) for path in sys.argv[1:] for line in Path(path).read_text().splitlines()]
    runs = [run for run in runs if run.get('type') == 'run']
    modes = list(dict.fromkeys(run['mode'] for run in runs))
    print('| mode | runs | passed | provider/host errors | tokens/run (median) | first prompt tokens (median) | '
          'seconds/run (median, mean) | model calls/run | tool calls/run |')
    print('|---|---|---|---|---|---|---|---|---|')
    for mode in modes:
        group = [run for run in runs if run['mode'] == mode]
        passed = sum(run['passed'] for run in group)
        first = [run['firstPromptTokens'] for run in group if run.get('firstPromptTokens')]
        seconds = [run['seconds'] for run in group]
        print(f"| {mode} | {len(group)} | {passed}/{len(group)} | {sum(1 for run in group if run.get('hostError'))} | "
              f"{statistics.median(run['usage']['total_tokens'] for run in group):.0f} | "
              f"{statistics.median(first) if first else '—'} | {statistics.median(seconds):.1f}, {statistics.mean(seconds):.1f} | "
              f"{statistics.mean(run['modelRequests'] for run in group):.2f} | {statistics.mean(len(run['toolCalls']) for run in group):.2f} |")
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


if __name__ == '__main__':
    main()
