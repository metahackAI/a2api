"""Summarize every retained trial; never filter failed model runs."""

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
from statistics import mean


def summarize(report):
    grouped = defaultdict(list)
    for run in report['runs']:
        grouped[(run['domain'], run['count'], run['mode'])].append(run)

    def metrics(runs):
        available = all(run.get('usageAvailable') for run in runs)
        return {'questions': len(runs), 'strictPassed': sum(run['assessment']['passed'] for run in runs),
            'answerReviews': dict((state, sum(run['assessment'].get('answerReview') == state for run in runs))
                                  for state in sorted({run['assessment'].get('answerReview', 'pending') for run in runs})),
            'seconds': round(sum(run['seconds'] for run in runs), 3),
            'meanSeconds': round(mean(run['seconds'] for run in runs), 3),
            'usageAvailable': available,
            'tokens': {key: sum(run['usage'][key] for run in runs) for key in
                       ('prompt_tokens', 'completion_tokens', 'total_tokens')} if available else None,
            'modelRequests': sum(len(run['steps']) for run in runs),
            'modelToolCalls': sum(len(run['calls']) for run in runs),
            'businessCalls': sum(run['assessment']['businessCalls'] for run in runs),
            'backendRequests': sum(len(run.get('backendRequests', [])) for run in runs),
            'failures': [{'id': run['id'], 'reasons': run['assessment']['failures']} for run in runs
                         if not run['assessment']['passed']]}
    return {'checkedAt': report['checkedAt'], 'model': report['model'], 'completed': report.get('completed', False),
        'repetitions': report['repetitions'], 'limits': report['limits'], 'preflight': report['preflight'],
        'configurations': [{'domain': domain, 'count': count, 'knowledge': 'known' if count == 2 else 'unknown',
            'mode': mode, **metrics(runs)} for (domain, count, mode), runs in sorted(grouped.items())],
        'totals': {mode: metrics([run for run in report['runs'] if run['mode'] == mode])
                   for mode in sorted({run['mode'] for run in report['runs']})},
        'startup': [{'id': group['id'], 'seconds': round(group['startupSeconds'], 4),
                     'initialToolBytes': group['initialToolBytes'], 'hostPreparationCalls': group['initialHostCalls']}
                    for group in report['groups']],
        'githubRequests': len(report.get('githubRequests', []))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--answer-review', type=Path, help='Separate manual review bound to the raw report hash')
    args = parser.parse_args()
    raw = args.report.read_bytes()
    report = json.loads(raw)
    digest = hashlib.sha256(raw).hexdigest()
    review = None
    if args.answer_review:
        review = json.loads(args.answer_review.read_text())
        if review['rawReportSHA256'] != digest:raise ValueError('Review belongs to a different raw report.')
        by_id = {entry['id']: entry for entry in review['runs']}
        if set(by_id) != {run['id'] for run in report['runs']}:raise ValueError('Review must cover exactly these runs.')
        for run in report['runs']:run['assessment']['answerReview'] = by_id[run['id']]['state']
    result = {**summarize(report), 'rawReportSHA256': digest}
    if review:
        result['answerReview'] = {'method': review['method'], 'rules': review['rules'],
            'notes': [entry for entry in review['runs'] if entry['issues']]}
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        if args.output.exists():raise ValueError('Choose a new summary output path.')
        args.output.write_text(text)
    else:print(text, end='')


if __name__ == '__main__':main()
