"""Detailed per-mode performance metrics from evaluation runs (a-commerce, RealWorld, benchmark JSONL).

A run record has: steps [{seconds, usage{prompt_tokens, completion_tokens, total_tokens}, toolBytes}],
toolCalls [{name, seconds, resultBytes}], usage totals, seconds, optional hostError and a pass flag
(`done` or `passed`). Business calls are `tools` [(name, ok)] (a-commerce) or `calls` [{ok}] (others).
"""

from __future__ import annotations

from collections import Counter
import json
import math
import statistics

SEARCH = 'a2api_search'


def _q(values, q):
    values = sorted(values)
    if not values:
        return None
    index = (len(values) - 1) * q
    low, high = math.floor(index), math.ceil(index)
    return values[low] + (values[high] - values[low]) * (index - low)


def stats(values, digits=1):
    values = [v for v in values if v is not None]
    if not values:
        return {'n': 0}
    shape = (lambda v: int(round(v))) if digits == 0 else (lambda v: round(v, digits))
    return {'n': len(values), 'mean': shape(statistics.mean(values)), 'median': shape(_q(values, 0.5)),
            'p90': shape(_q(values, 0.9)), 'min': shape(min(values)), 'max': shape(max(values))}


def passed(run):
    return bool(run.get('done', run.get('passed')))


def business(run):
    """[(name, ok)] of calls that reached the business API."""
    if 'tools' in run:
        return [(name, ok) for name, ok in run['tools']]
    return [(call.get('op') or f"{call.get('method')} {call.get('path')}", call.get('ok')) for call in run.get('calls', [])
            if call.get('executed', True)]


def mode_metrics(runs):
    steps = [step for run in runs for step in run.get('steps', [])]
    calls = [call for run in runs for call in run.get('toolCalls', [])]
    completion = sum((step.get('usage') or {}).get('completion_tokens') or 0 for step in steps)
    model_seconds = sum(step['seconds'] for step in steps)
    ok_runs = [run for run in runs if not run.get('hostError')]
    done = sum(passed(run) for run in runs)
    calls_business = [entry for run in runs for entry in business(run)]
    return {
        'runs': len(runs),
        'passed': done,
        'passRate': round(done / len(runs), 3) if runs else None,
        'passRateWithoutHostErrors': round(sum(passed(run) for run in ok_runs) / len(ok_runs), 3) if ok_runs else None,
        'hostErrors': dict(Counter(run['hostError'] for run in runs if run.get('hostError'))),
        'tokensPerRun': {
            'total': stats([run['usage']['total_tokens'] for run in runs], 0),
            'prompt': stats([run['usage']['prompt_tokens'] for run in runs], 0),
            'completion': stats([run['usage']['completion_tokens'] for run in runs], 0),
            'firstPrompt': stats([run.get('firstPromptTokens') for run in runs], 0),
            'largestPrompt': stats([max(((s.get('usage') or {}).get('prompt_tokens') or 0) for s in run['steps'])
                                    for run in runs if run.get('steps')], 0),
        },
        'secondsPerRun': {
            'total': stats([run['seconds'] for run in runs]),
            'model': stats([sum(step['seconds'] for step in run.get('steps', [])) for run in runs]),
            'tools': stats([sum(call.get('seconds') or 0 for call in run.get('toolCalls', [])) for run in runs]),
        },
        'secondsPerModelStep': stats([step['seconds'] for step in steps], 2),
        'msPerCompletionToken': round(1000 * model_seconds / completion, 1) if completion else None,
        'modelCallsPerRun': stats([len(run.get('steps', [])) for run in runs], 2),
        'toolCallsPerRun': stats([len(run.get('toolCalls', [])) for run in runs], 2),
        'searchCallsPerRun': stats([sum(call['name'] == SEARCH for call in run.get('toolCalls', [])) for run in runs], 2),
        'businessCalls': {'total': len(calls_business), 'failed': sum(1 for _, ok in calls_business if not ok),
                          'failedRate': round(sum(1 for _, ok in calls_business if not ok) / len(calls_business), 3)
                          if calls_business else None},
        'toolDefinitionBytes': {'firstRequest': stats([run['steps'][0].get('toolBytes') for run in runs if run.get('steps')], 0),
                                'largest': stats([max(s.get('toolBytes') or 0 for s in run['steps']) for run in runs
                                                  if run.get('steps')], 0)},
        'resultBytesPerCall': stats([call.get('resultBytes') for call in calls], 0),
    }


def by_mode(runs):
    modes = list(dict.fromkeys(run['mode'] for run in runs))
    return {mode: mode_metrics([run for run in runs if run['mode'] == mode]) for mode in modes}


def markdown(metrics):
    """Two tables: outcome/context, then time/calls."""
    rows = ['| mode | passed | host errors | tokens/run median (mean, p90) | prompt / completion per run (mean) | '
            'first prompt (median) | largest prompt (median) | tool bytes first request (median) |',
            '|---|---|---|---|---|---|---|---|']
    for mode, m in metrics.items():
        t = m['tokensPerRun']
        errors = ', '.join(f'{k} {v}' for k, v in m['hostErrors'].items()) or '0'
        rows.append(f"| {mode} | {m['passed']}/{m['runs']} ({m['passRate']:.0%}) | {errors} | "
                    f"{t['total'].get('median', '—')} ({t['total'].get('mean', '—')}, {t['total'].get('p90', '—')}) | "
                    f"{t['prompt'].get('mean', '—')} / {t['completion'].get('mean', '—')} | {t['firstPrompt'].get('median', '—')} | "
                    f"{t['largestPrompt'].get('median', '—')} | {m['toolDefinitionBytes']['firstRequest'].get('median', '—')} |")
    rows += ['', '| mode | seconds/run median (mean, p90) | model / tool seconds per run (mean) | seconds per model step (mean) | '
             'ms per output token | model calls/run | tool calls/run | searches/run | business calls failed | result bytes/call (median) |',
             '|---|---|---|---|---|---|---|---|---|---|']
    for mode, m in metrics.items():
        s = m['secondsPerRun']
        b = m['businessCalls']
        failed = f"{b['failed']}/{b['total']}" + (f" ({b['failedRate']:.0%})" if b['total'] else '')
        rows.append(f"| {mode} | {s['total'].get('median', '—')} ({s['total'].get('mean', '—')}, {s['total'].get('p90', '—')}) | "
                    f"{s['model'].get('mean', '—')} / {s['tools'].get('mean', '—')} | {m['secondsPerModelStep'].get('mean', '—')} | "
                    f"{m['msPerCompletionToken'] or '—'} | {m['modelCallsPerRun'].get('mean', '—')} | {m['toolCallsPerRun'].get('mean', '—')} | "
                    f"{m['searchCallsPerRun'].get('mean', '—')} | {failed} | {m['resultBytesPerCall'].get('median', '—')} |")
    return '\n'.join(rows)


def dump(path, metrics, **extra):
    with open(path, 'w') as sink:
        json.dump({**extra, 'metrics': metrics}, sink, ensure_ascii=False, indent=1)
