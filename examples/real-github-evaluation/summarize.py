"""Include failed attempts and startup; keep bytes separate from provider tokens."""

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path


def summarize(report, review):
    by_id = {row['id']: row for row in review['runs']}
    grouped = defaultdict(list)
    for run in report['runs']:grouped[(run['scale'], run['mode'])].append(run)

    def metrics(runs):
        assessments = [by_id[run['id']]['assessment'] for run in runs]
        usage_complete = all(run['usageComplete'] for run in runs)
        models = [row for run in runs for row in run['modelRequests']]
        payloads = [call['output'] for run in runs for call in run['calls']]
        http = [row for run in runs for row in run['backendRequests']]
        return {'questions': len(runs), 'passed': sum(row['passed'] for row in assessments),
            'factsMatched': sum(row['factsMatched'] for row in assessments),
            'firstAttemptClean': sum(row['firstAttemptClean'] for row in assessments),
            'byKind': {kind: {'questions': sum(run['kind'] == kind for run in runs),
                'passed': sum(by_id[run['id']]['assessment']['passed'] for run in runs if run['kind'] == kind)}
                for kind in ('simple', 'chain')},
            'usageComplete': usage_complete,
            'tokens': {key: sum(run['usage'][key] for run in runs) for key in
                ('prompt_tokens', 'completion_tokens', 'total_tokens')} if usage_complete else None,
            'questionSeconds': round(sum(run['seconds'] for run in runs), 3),
            'sessionSetupSeconds': round(sum(run['startupSeconds'] for run in runs), 3),
            'modelSeconds': round(sum(row['seconds'] for row in models), 3),
            'hostNonModelSeconds': round(sum(run['seconds'] for run in runs) - sum(row['seconds'] for row in models), 3),
            'modelRequests': len(models), 'modelToolCalls': sum(len(run['calls']) for run in runs),
            'businessCalls': sum(row['businessCalls'] for row in assessments),
            'searchCalls': sum(call['tool'] == 'a2api_search' for run in runs for call in run['calls']),
            'moreRequests': sum(call['tool'] == 'a2api_search' and call['input'].get('more') is True
                                for run in runs for call in run['calls']),
            'noProgressSearches': sum(call['tool'] == 'a2api_search' and call['output'].get('progress') is False
                                      for run in runs for call in run['calls']),
            'failedBusinessAttempts': sum(row['failedBusinessAttempts'] for row in assessments),
            'readsAboveMinimum': sum(row['readsAboveMinimum'] for row in assessments),
            'githubRequests': sum(bool(row.get('sent')) for row in http),
            'httpStatuses': {str(code): sum(row['status'] == code for row in http) for code in sorted({row['status'] for row in http})},
            'upstreamSeconds': round(sum(row.get('upstreamSeconds', 0) for row in http), 3),
            'httpBodyBytes': sum(row['bodyBytes'] for row in http),
            'normalizedToolBytesSum': sum(row['toolBytes'] for row in models),
            'normalizedHistoryBytesSum': sum(row['historyBytes'] for row in models),
            'modelToolResultBytes': sum(len(json.dumps(value, ensure_ascii=False, separators=(',', ':')).encode()) for value in payloads),
            'requiredContractsOffered': sum(all(by_id[run['id']]['requiredContractsOffered'].values()) for run in runs),
            'hostProtocol': {'requests': sum(len(run['hostProtocol']) for run in runs),
                'seconds': round(sum(row['seconds'] for run in runs for row in run['hostProtocol']), 3),
                'responseBytes': sum(row.get('outputBytes', 0) for run in runs for row in run['hostProtocol'])},
            'failures': [{'id': run['id'], 'reasons': by_id[run['id']]['assessment']['failures']} for run in runs
                         if not by_id[run['id']]['assessment']['passed']]}
    config = [{'scale': scale, 'mode': mode, **metrics(runs)} for (scale, mode), runs in sorted(grouped.items())]
    total = {mode: metrics([run for run in report['runs'] if run['mode'] == mode]) for mode in ('ordinary', 'a2api')}
    preparation = report['inventory']['loadAndImportSeconds'] + sum(row['convertSeconds'] for row in report['catalogs'])
    for value in total.values():
        value['withSessionSetupSeconds'] = round(value['questionSeconds'] + value['sessionSetupSeconds'], 3)
        value['withOneSharedCatalogBuildSeconds'] = round(value['withSessionSetupSeconds'] + preparation, 3)
        value['tokensPerStrictSuccessIncludingFailures'] = (round(value['tokens']['total_tokens'] / value['passed'], 1)
            if value['passed'] and value['tokens'] else None)
    return {'checkedAt': report['checkedAt'], 'model': report['model'], 'completed': report['completed'],
        'rawReportSHA256': review['rawReportSHA256'], 'settings': report['settings'],
        'repetitions': report['repetitions'], 'githubAuth': report['githubAuth'], 'limits': report['limits'],
        'source': report['inventory']['source'],
        'coverage': {key: report['inventory'][key] for key in ('getOperations', 'statuses', 'loadAndImportSeconds')},
        'catalogs': [{key: row[key] for key in ('scale', 'count', 'descriptorBytes', 'convertSeconds', 'projection')}
                     for row in report['catalogs']],
        'configurations': config, 'totals': total, 'stdio': report.get('stdio'),
        'knownIDProbe': report['knownIDProbe'], 'scoringCorrection': review['changed'],
        'rankDiagnostics': review['rankDiagnostics'],
        'httpRequestsIncludingPreflightAndStdio': sum(bool(row.get('sent')) for row in report['httpRequests'])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report', type=Path)
    parser.add_argument('--review', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():raise ValueError('Choose a new summary path.')
    raw = args.report.read_bytes()
    review = json.loads(args.review.read_text())
    if hashlib.sha256(raw).hexdigest() != review['rawReportSHA256']:raise ValueError('Review/report hash mismatch.')
    args.output.write_text(json.dumps(summarize(json.loads(raw), review), ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':main()
