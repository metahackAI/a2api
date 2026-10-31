"""a-commerce's own evaluation report (cargo xtask eval --out report.md), per tool set with the same
statistics as run_metrics: done, tokens, seconds, model and tool calls per task.

python examples/acommerce/own_report.py artifacts/acommerce/runs/acom-own-design-2.md [--json out.json]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from run_metrics import stats  # noqa: E402


def rows(path):
    found = []
    for line in Path(path).read_text().splitlines():
        cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
        if len(cells) == 9 and cells[2] in ('yes', 'no') and cells[0] != 'Task':
            task, tool_set, done, tools, model_calls, tokens, seconds, _, missing = cells[:9]
            calls = [name.strip() for name in tools.split(',') if name.strip()]
            found.append({'task': task, 'mode': tool_set, 'done': done == 'yes', 'toolCalls': len(calls),
                          'failedToolCalls': sum('✗' in name for name in calls), 'modelCalls': int(model_calls),
                          'tokens': int(tokens), 'seconds': float(seconds), 'missing': missing})
    return found


def summarize(runs):
    out = {}
    for mode in dict.fromkeys(run['mode'] for run in runs):
        group = [run for run in runs if run['mode'] == mode]
        calls = sum(run['toolCalls'] for run in group)
        out[mode] = {'runs': len(group), 'passed': sum(run['done'] for run in group),
                     'tokensPerRun': stats([run['tokens'] for run in group], 0), 'secondsPerRun': stats([run['seconds'] for run in group]),
                     'modelCallsPerRun': stats([run['modelCalls'] for run in group], 2), 'toolCallsPerRun': stats([run['toolCalls'] for run in group], 2),
                     'failedToolCalls': f"{sum(run['failedToolCalls'] for run in group)}/{calls}"}
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report')
    parser.add_argument('--json', type=Path)
    options = parser.parse_args()
    runs = rows(options.report)
    summary = summarize(runs)
    print('| tool set | passed | tokens/run median (mean, p90) | seconds/run median (mean, p90) | model calls/run | tool calls/run | failed tool calls |')
    print('|---|---|---|---|---|---|---|')
    for mode, m in summary.items():
        t, s = m['tokensPerRun'], m['secondsPerRun']
        print(f"| {mode} | {m['passed']}/{m['runs']} | {t['median']} ({t['mean']}, {t['p90']}) | {s['median']} ({s['mean']}, {s['p90']}) | "
              f"{m['modelCallsPerRun']['mean']} | {m['toolCallsPerRun']['mean']} | {m['failedToolCalls']} |")
    if options.json:
        options.json.write_text(json.dumps({'report': options.report, 'metrics': summary, 'runs': runs}, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
