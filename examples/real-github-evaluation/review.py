"""Offline scoring/rank diagnosis of an immutable live report; no new calls."""

import argparse
import hashlib
import json
from pathlib import Path

from a2api import A2APIError, HTTPDeployment, convert
from a2api.importers import OpenAPIImporter
from a2api.discovery_metadata import SEARCH_REVISION, SearchPages
from a2api.mcp_application import DirectApplications
from a2api.schema import validate_value
from a2api.tool_session import SEARCH_TOOL
from assess import CASES, assess
from catalog import SOURCE_DIR, CONTEXT

TARGETS = {'repository': ['github.repos.get'], 'branches': ['github.repos.list_branches'],
           'default_commit': ['github.repos.get', 'github.repos.get_commit']}


def review(report, raw_digest):
    source = OpenAPIImporter.from_file(SOURCE_DIR / 'api.github.com.json.gz', namespace='github')
    if source.source_hash != report['inventory']['source']['sha256']:raise ValueError('Source mismatch.')
    all_mapping = next(row['mapping'] for row in report['catalogs'] if row['scale'] == 'large')
    used = {call['binding']['id'] for run in report['runs'] for call in run['calls'] if call.get('binding')}
    app = (convert(source, operations={all_mapping[identifier]['operationId']: {'effect': 'read'} for identifier in used},
                   deployment=HTTPDeployment('https://api.github.com')) if used else None)
    descriptors = {item['id']: item for item in app.descriptors()} if app else {}
    runtime = None
    revision = report['settings'].get('searchRevision')
    if revision:
        if revision != SEARCH_REVISION:raise ValueError('Use the search implementation recorded by this report.')
        full = convert(source, operations={item['operationId']: {'effect': 'read'} for item in all_mapping.values()},
                       deployment=HTTPDeployment('https://api.github.com'))
        runtime = DirectApplications(full)
    cases = {case['id']: case for case in CASES}
    # Reproduce the CURRENT substring ranker exactly from original source text.
    documents = {}
    for identifier, info in all_mapping.items():
        operation = source.document['paths'][info['path']]['get']
        summary = operation.get('summary') or info['operationId']
        intent = summary + ('\n' + operation['description'] if operation.get('description') else '')
        terms = tuple(dict.fromkeys((summary, intent, *operation.get('tags', []))))
        documents[identifier] = ' '.join((identifier, summary, *terms)).casefold()
    ranks, changed, runs = {}, [], []
    for run in report['runs']:
        pages = SearchPages()
        revised = assess(cases[run['scenario']], run, descriptors, all_mapping)
        if revised != run['assessment']:
            changed.append({'id': run['id'], 'originalPassed': run['assessment']['passed'],
                'revisedPassed': revised['passed'], 'removedFailures': sorted(set(run['assessment']['failures']) - set(revised['failures']))})
        offered = {identifier for request in run['modelRequests'] for identifier in request['offeredIDs']}
        target_exposure = {target: target in offered for target in TARGETS[run['scenario']]}
        for call in run['calls']:
            if call['tool'] != 'a2api_search' or run['scale'] != 'large':continue
            query = call['input'].get('query')
            if runtime is not None:
                try:validate_value(SEARCH_TOOL['function']['parameters'], call['input'], code='INVALID_INPUT', status=400)
                except A2APIError as error:
                    if call['output'].get('error', {}).get('code') != error.code:raise
                    continue
            if not isinstance(query, str):continue
            page = 1
            if runtime is not None:
                try:
                    prepared = pages.prepare(query, call['input'].get('more', False), limit=3)
                    found = runtime.discover(context=CONTEXT, **prepared['arguments'])
                    state = pages.commit(prepared, found)
                except A2APIError as error:
                    if call['output'].get('error', {}).get('code') != error.code:raise
                    continue
                ordered = [key[0] for key, _ in runtime._index.rank(prepared['arguments']['query'])]
                candidates = [item['id'] for item in found['capabilities']]
                page = state['page']
            else:
                words = query.casefold().split()
                hits = [(sum(word in text for word in words), identifier) for identifier, text in documents.items()]
                ordered = [identifier for score, identifier in sorted(hits, key=lambda item: (-item[0], item[1])) if score or not words]
                candidates = ordered[:3]
            positions = {target: ordered.index(target) + 1 if target in ordered else None for target in TARGETS[run['scenario']]}
            actual = [item['id'] for item in call['output'].get('selected', [])]
            if any(identifier not in candidates for identifier in actual):raise ValueError('Offline ranking does not reproduce observed candidates.')
            ranks[(run['scenario'], query, page)] = {'scenario': run['scenario'], 'query': query, 'page': page,
                'top3': candidates, 'targetRanks': positions}
        runs.append({'id': run['id'], 'assessment': revised, 'requiredContractsOffered': target_exposure})
    return {'rawReportSHA256': raw_digest,
        'scorerSHA256': hashlib.sha256(Path(__file__).with_name('assess.py').read_bytes()).hexdigest(),
        'method': 'Offline re-scoring of retained actual calls/results; no model/API rerun or argument repair.',
        'ruleCorrection': 'Qualified heads/<observed branch> and refs/heads/<observed branch> are valid observed-branch derivations.',
        'changed': changed, 'runs': runs, 'rankDiagnostics': list(ranks.values())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():raise ValueError('Choose a new review path.')
    raw = args.report.read_bytes()
    report = json.loads(raw)
    if not report.get('completed'):raise ValueError('Finish and retain the complete live report first.')
    value = review(report, hashlib.sha256(raw).hexdigest())
    args.output.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'runs': len(value['runs']), 'changed': value['changed']}, ensure_ascii=False))


if __name__ == '__main__':main()
