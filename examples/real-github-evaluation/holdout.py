"""Frozen additional public read requests; do not tune retrieval on these runs."""

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from assess import answer_json

CASES_PATH = Path(__file__).with_name('holdout-cases.json')
CASES = json.loads(CASES_PATH.read_text())


def assess(case, run, descriptors, mapping):
    issues, business, branch, refs, expected, repaired = [], [], None, set(), None, 0
    repository = case['owner'] + '/' + case['repo']
    target = case['targetOperations'][-1]
    for call in run['calls']:
        if not call.get('binding'):continue
        identifier, args, output = call['binding']['id'], call['input'], call['output']
        op = mapping[identifier]['operationId']
        business.append((op, args))
        if not Draft202012Validator(descriptors[identifier]['inputSchema']).is_valid(args):issues.append('INVALID_BUSINESS_INPUT')
        path, query = args.get('path', {}), args.get('query', {})
        if (str(path.get('owner', '')).casefold(), str(path.get('repo', '')).casefold()) != (case['owner'].casefold(), case['repo'].casefold()):
            issues.append('WRONG_REPOSITORY')
        if output.get('status') != 'succeeded':
            repaired += 1
            issues.append('BUSINESS_ERROR:' + output.get('error', {}).get('code', 'UNKNOWN'))
            continue
        data = output['data']
        if not Draft202012Validator(descriptors[identifier]['outputSchema']).is_valid(data):issues.append('INVALID_PUBLIC_OUTPUT')
        if op == 'repos/get':
            if data.get('full_name', '').casefold() != repository.casefold():issues.append('WRONG_REPOSITORY_RESULT')
            branch = data.get('default_branch')
            if isinstance(branch, str):refs.update((branch, 'heads/' + branch, 'refs/heads/' + branch))
        if case['kind'] == 'chain' and op != 'repos/get':
            if not branch:issues.append('DEPENDENCY_BEFORE_REPOSITORY')
            if op == 'repos/get-branch' and path.get('branch') == branch:refs.add(data.get('commit', {}).get('sha'))
            elif op == 'git/get-ref' and path.get('ref') in refs:refs.add(data.get('object', {}).get('sha'))
            elif op == 'repos/list-commits' and query.get('sha', branch) == branch and data:refs.add(data[0].get('sha'))
        if op != target:continue
        if case['kind'] == 'chain' and path.get('ref') not in refs:issues.append('REF_NOT_FROM_PRIOR_RESULT')
        if case['id'] in ('releases_page', 'forks_page', 'stargazers_page', 'default_statuses_page'):
            if query.get('page', 1) != 1 or query.get('per_page', 30) != 2:issues.append('PAGE_OR_COUNT_CONDITION')
            allowed = {'page', 'per_page'} | ({'sort'} if case['id'] == 'forks_page' else set())
            if set(query) - allowed:issues.append('UNREQUESTED_FILTER')
            if not isinstance(data, list) or len(data) > 2:
                issues.append('PAGE_RESULT')
                continue
        if case['id'] == 'latest_release':
            expected = {'repository': repository, 'tag': data.get('tag_name'), 'name': data.get('name'), 'htmlUrl': data.get('html_url')}
        elif case['id'] == 'default_combined_status':
            expected = {'repository': repository, 'defaultBranch': branch, 'state': data.get('state'), 'totalCount': data.get('total_count')}
        else:
            expected = {'repository': repository, 'page': 1, 'perPage': 2}
            if case['id'] == 'releases_page':expected['tags'] = [item['tag_name'] for item in data]
            elif case['id'] == 'forks_page':
                if query.get('sort', 'newest') != 'newest':issues.append('SORT_CONDITION')
                expected.update(sort='newest', forks=[item['full_name'] for item in data])
            elif case['id'] == 'stargazers_page':expected['logins'] = [item['login'] for item in data]
            elif case['id'] == 'default_statuses_page':
                expected.update(defaultBranch=branch, statuses=[{'state': item['state'], 'context': item['context']} for item in data])
    answer, form = answer_json(run['answer'])
    facts = expected is not None and json.dumps(answer, sort_keys=True) == json.dumps(expected, sort_keys=True)
    if expected is None:issues.append('GOAL_NOT_REACHED')
    if not facts:issues.append('ANSWER_VALUES_OR_FORMAT')
    if run.get('hostError'):issues.append('HOST:' + run['hostError']['code'])
    duplicate = len(business) - len({json.dumps(item, sort_keys=True) for item in business})
    return {'passed': not issues, 'goalReached': expected is not None, 'factsMatched': facts,
        'firstAttemptClean': expected is not None and not issues and bool(business) and business[0][0] == case['targetOperations'][0],
        'failures': sorted(set(issues)), 'businessCalls': len(business), 'failedBusinessAttempts': repaired,
        'duplicateBusinessCalls': duplicate, 'readsAboveMinimum': max(0, len(business) - case['minimumReads']),
        'answerFormat': form, 'expectedAnswer': expected}


def preflight(app, context):
    """Seven real reads, separately counted; never shown to the model."""
    rows = []
    def invoke(identifier, args):
        result = app.invoke(identifier, args, context=context)
        rows.append({'id': identifier, 'input': args, 'output': result})
        return result
    hello = {'owner': 'octocat', 'repo': 'Hello-World'}
    requests = {'owner': 'psf', 'repo': 'requests'}
    repo = invoke('github.repos.get', {'path': hello})
    branch = repo.get('data', {}).get('default_branch')
    for identifier, path, query in (
        ('github.repos.get_latest_release', requests, None),
        ('github.repos.list_releases', requests, {'page': 1, 'per_page': 2}),
        ('github.repos.list_forks', hello, {'page': 1, 'per_page': 2, 'sort': 'newest'}),
        ('github.activity.list_stargazers_for_repo', hello, {'page': 1, 'per_page': 2}),
        ('github.repos.get_combined_status_for_ref', {**hello, 'ref': branch}, None),
        ('github.repos.list_commit_statuses_for_ref', {**hello, 'ref': branch}, {'page': 1, 'per_page': 2})):
        invoke(identifier, {'path': path, **({'query': query} if query else {})})
    return {'passed': all(row['output'].get('status') == 'succeeded' for row in rows), 'calls': rows}
