"""Aggregate benchmark JSONL runs by mode x scale (and optionally language/kind).

python examples/benchmark/summarize.py artifacts/benchmark/runs/dev-1.jsonl [--by language] [--json out.json]
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import statistics


def load(paths):
    runs, headers = [], []
    for path in paths:
        for line in Path(path).read_text().splitlines():
            record = json.loads(line)
            (runs if record.get('type') == 'run' else headers).append(record)
    return runs, headers


def median(values):
    values = [value for value in values if value is not None]
    return round(statistics.median(values), 3) if values else None


def mean(values):
    values = [value for value in values if value is not None]
    return round(statistics.fmean(values), 3) if values else None


def aggregate(runs, keys):
    groups = defaultdict(list)
    for run in runs:
        groups[tuple(run[key] for key in keys)].append(run)
    table = []
    for key, items in sorted(groups.items()):
        passed = [run for run in items if run['assessment']['passed']]
        errors = defaultdict(int)
        for run in items:
            if run.get('hostError'):
                errors[run['hostError']] += 1
        table.append({
            **dict(zip(keys, key)), 'runs': len(items), 'passed': len(passed),
            'passRate': round(len(passed) / len(items), 3),
            'medianTotalTokens': median(run['usage']['total_tokens'] for run in items),
            'meanTotalTokens': mean(run['usage']['total_tokens'] for run in items),
            'medianFirstPromptTokens': median(run.get('firstPromptTokens') for run in items),
            'medianSeconds': median(run['seconds'] for run in items),
            'meanSeconds': mean(run['seconds'] for run in items),
            'meanModelRequests': mean(run['modelRequests'] for run in items),
            'meanBusinessCalls': mean(len(run['calls']) for run in items),
            'failedBusinessCalls': sum(1 for run in items for call in run['calls'] if not call['ok']),
            'tokensPerPass': round(sum(run['usage']['total_tokens'] for run in items) / len(passed)) if passed else None,
            'hostErrors': dict(errors),
            'infraErrors': sum(count for code, count in errors.items()
                               if code == 'MODEL_CONNECTION_FAILED' or code.startswith('MODEL_HTTP_5')),
        })
    return table


def stability(runs, keys=('scale', 'mode')):
    """Per group: share of (task, scale) cells where every language/repetition passed."""
    cells = defaultdict(list)
    for run in runs:
        cells[tuple(run[key] for key in keys) + (run['task'],)].append(run['assessment']['passed'])
    table = defaultdict(lambda: [0, 0])
    for key, values in cells.items():
        table[key[:-1]][0] += all(values)
        table[key[:-1]][1] += 1
    rows = []
    for key, (stable, total) in sorted(table.items()):
        group = [run for run in runs if tuple(run[k] for k in keys) == key]
        rows.append({**dict(zip(keys, key)), 'consistentTasks': stable, 'tasks': total,
                     'unexpectedWrites': sum('UNEXPECTED_WRITE' in run['assessment']['failures'] for run in group),
                     'repeatedFailingCalls': sum('REPEATED_FAILING_CALL' in run['assessment']['failures'] for run in group),
                     'faultAndMissingPassed': sum(run['assessment']['passed'] for run in group if run['kind'] in ('fault', 'missing')),
                     'faultAndMissingRuns': sum(1 for run in group if run['kind'] in ('fault', 'missing')),
                     'failedBusinessCalls': sum(1 for run in group for call in run['calls'] if not call['ok']),
                     'hostErrors': sum(1 for run in group if run.get('hostError'))})
    return rows


def markdown(result):
    lines = ['| 규모 | 방식 | 통과 | 작업당 토큰(중앙값) | 첫 요청 prompt 토큰(중앙값) | 작업 시간(중앙값, 초) | 모델 요청(평균) | 오류(provider/host) |',
             '|---|---|---:|---:|---:|---:|---:|---|']
    for row in result['summary']:
        lines.append(f"| {row['scale']} | {row['mode']} | {row['passed']}/{row['runs']} | {row['medianTotalTokens']:,.0f} | "
                     f"{row['medianFirstPromptTokens']:,.0f} | {row['medianSeconds']} | {row['meanModelRequests']} | "
                     f"{', '.join(f'{k} {v}' for k, v in row['hostErrors'].items()) or '-'} |")
    lines += ['', '| 규모 | 방식 | 모든 언어·반복에서 통과한 작업 | 장애/누락 입력 통과 | 의도하지 않은 쓰기 | 실패 endpoint 반복 | 실패한 업무 호출 |',
              '|---|---|---:|---:|---:|---:|---:|']
    for row in result['stability']:
        lines.append(f"| {row['scale']} | {row['mode']} | {row['consistentTasks']}/{row['tasks']} | "
                     f"{row['faultAndMissingPassed']}/{row['faultAndMissingRuns']} | {row['unexpectedWrites']} | "
                     f"{row['repeatedFailingCalls']} | {row['failedBusinessCalls']} |")
    if result.get('byLanguage'):
        lines += ['', '| 언어 | 방식 | 통과 | 작업당 토큰(중앙값) | 작업 시간(중앙값, 초) |', '|---|---|---:|---:|---:|']
        for row in result['byLanguage']:
            lines.append(f"| {row['language']} | {row['mode']} | {row['passed']}/{row['runs']} | {row['medianTotalTokens']:,.0f} | {row['medianSeconds']} |")
    if result.get('byKind'):
        lines += ['', '| 작업 유형 | 방식 | 통과 | 작업당 토큰(중앙값) | 작업 시간(중앙값, 초) |', '|---|---|---:|---:|---:|']
        for row in result['byKind']:
            lines.append(f"| {row['kind']} | {row['mode']} | {row['passed']}/{row['runs']} | {row['medianTotalTokens']:,.0f} | {row['medianSeconds']} |")
    return '\n'.join(lines) + '\n'


def failures(runs):
    rows = []
    for run in runs:
        if not run['assessment']['passed']:
            rows.append({key: run[key] for key in ('task', 'scale', 'language', 'mode', 'repetition')}
                        | {'failures': run['assessment']['failures']})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='+')
    parser.add_argument('--by', default='', help='extra grouping keys, e.g. language or kind')
    parser.add_argument('--json', type=Path)
    parser.add_argument('--markdown', type=Path)
    args = parser.parse_args()
    runs, headers = load(args.paths)
    keys = ['scale', 'mode'] + [key for key in args.by.split(',') if key]
    result = {'headers': headers, 'summary': aggregate(runs, keys), 'byMode': aggregate(runs, ['mode']),
              'byLanguage': aggregate(runs, ['language', 'mode']), 'byKind': aggregate(runs, ['kind', 'mode']),
              'stability': stability(runs), 'failures': failures(runs)}
    columns = keys + ['runs', 'passed', 'medianTotalTokens', 'medianFirstPromptTokens', 'medianSeconds', 'meanModelRequests', 'hostErrors']
    print('\t'.join(columns))
    for row in result['summary'] + [{**row, 'scale': 'ALL'} for row in result['byMode']]:
        print('\t'.join(str(row.get(column, '')) for column in columns))
    print('failures:', len(result['failures']))
    for row in result['failures']:
        print('  ', json.dumps(row, ensure_ascii=False))
    if args.json:
        args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    if args.markdown:
        args.markdown.write_text(markdown(result))


if __name__ == '__main__':
    main()
