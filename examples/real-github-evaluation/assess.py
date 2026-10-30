"""Check user conditions and real value flow, not one prescribed call sequence."""

import json

from jsonschema import Draft202012Validator

CASES = [
    {'id': 'repository', 'kind': 'simple', 'owner': 'psf', 'repo': 'requests', 'minimumReads': 1,
     'question': 'API로 psf/requests 저장소의 기본 브랜치, 별 개수, 보관 여부를 확인해줘. '
                 '최종 JSON 키는 repository, defaultBranch, stars, archived로 해줘.'},
    {'id': 'branches', 'kind': 'simple', 'owner': 'octocat', 'repo': 'Hello-World', 'minimumReads': 1,
     'question': 'API로 octocat/Hello-World의 브랜치 목록 첫 페이지를 최대 2개만 조회해줘. '
                 '최종 JSON 키는 repository, page, perPage, branches(반환된 브랜치 이름 배열)로 해줘.'},
    {'id': 'default_commit', 'kind': 'chain', 'owner': 'octocat', 'repo': 'Hello-World', 'minimumReads': 2,
     'question': 'octocat/Hello-World의 저장소 정보를 먼저 API로 조회해 실제 기본 브랜치를 확인하고, '
                 '그 브랜치의 현재 head 커밋 SHA와 추가/삭제 줄 수를 API로 조회해줘. 브랜치나 SHA를 추측하지 마. '
                 '최종 JSON 키는 repository, defaultBranch, sha, additions, deletions로 해줘.'},
]


def answer_json(text):
    text = text.strip()
    fenced = text.startswith('```json\n') and text.endswith('\n```')
    if fenced:text = text[8:-4]
    try:return json.loads(text), 'fenced_json' if fenced else 'json'
    except (ValueError, TypeError):return None, 'unparseable'


def assess(case, run, descriptors, mapping):
    issues, business, expected = [], [], None
    branch, refs = None, set()
    repaired = 0
    for call in run['calls']:
        binding = call.get('binding')
        if not binding:continue
        identifier, args, output = binding['id'], call['input'], call['output']
        op = mapping[identifier]['operationId']
        business.append((op, args))
        if not Draft202012Validator(descriptors[identifier]['inputSchema']).is_valid(args):
            issues.append('INVALID_BUSINESS_INPUT')
        path = args.get('path', {})
        if (str(path.get('owner', '')).casefold(), str(path.get('repo', '')).casefold()) != (case['owner'].casefold(), case['repo'].casefold()):
            issues.append('WRONG_REPOSITORY')
        if output.get('status') != 'succeeded':
            repaired += 1
            issues.append('BUSINESS_ERROR:' + output.get('error', {}).get('code', 'UNKNOWN'))
            continue
        data = output['data']
        if not Draft202012Validator(descriptors[identifier]['outputSchema']).is_valid(data):
            issues.append('INVALID_PUBLIC_OUTPUT')
        if op == 'repos/get':
            if not isinstance(data, dict) or data.get('full_name', '').casefold() != f"{case['owner']}/{case['repo']}".casefold():
                issues.append('WRONG_REPOSITORY_RESULT')
                continue
            branch = data.get('default_branch')
            if isinstance(branch, str):
                # GitHub accepts qualified branch refs too. These are exact
                # derivations of the observed branch, not guessed values.
                refs.update((branch, 'heads/' + branch, 'refs/heads/' + branch))
            if case['id'] == 'repository':
                expected = {'repository': data.get('full_name'), 'defaultBranch': branch,
                            'stars': data.get('stargazers_count'), 'archived': data.get('archived')}
        elif case['id'] == 'branches' and op == 'repos/list-branches':
            query = args.get('query', {})
            if query.get('page', 1) != 1 or query.get('per_page', 30) != 2:
                issues.append('PAGE_OR_COUNT_CONDITION')
            if query.get('protected') is not None:issues.append('UNREQUESTED_FILTER')
            if not isinstance(data, list) or len(data) > 2:issues.append('BRANCH_PAGE_RESULT')
            else:expected = {'repository': f"{case['owner']}/{case['repo']}", 'page': 1,
                            'perPage': 2, 'branches': [item['name'] for item in data]}
        elif case['id'] == 'default_commit':
            if not branch:
                issues.append('DEPENDENCY_BEFORE_REPOSITORY')
                continue
            if op == 'repos/get-branch' and path.get('branch') == branch:
                refs.add(data.get('commit', {}).get('sha'))
            elif op == 'git/get-ref' and path.get('ref') in ('heads/' + branch, 'refs/heads/' + branch):
                refs.add(data.get('object', {}).get('sha'))
            elif op == 'repos/list-commits' and args.get('query', {}).get('sha', branch) == branch and data:
                refs.add(data[0].get('sha'))
            elif op == 'repos/get-commit':
                if path.get('ref') not in refs:issues.append('REF_NOT_FROM_PRIOR_RESULT')
                elif isinstance(data.get('stats'), dict) and all(type(data['stats'].get(key)) is int for key in ('additions', 'deletions')):
                    expected = {'repository': f"{case['owner']}/{case['repo']}", 'defaultBranch': branch,
                                'sha': data.get('sha'), 'additions': data['stats'].get('additions'),
                                'deletions': data['stats'].get('deletions')}
    answer, form = answer_json(run['answer'])
    # Compare types too: bool and int equality is not enough for factual JSON.
    facts = expected is not None and json.dumps(answer, sort_keys=True) == json.dumps(expected, sort_keys=True)
    if expected is None:issues.append('GOAL_NOT_REACHED')
    if not facts:issues.append('ANSWER_VALUES_OR_FORMAT')
    if run.get('hostError'):issues.append('HOST:' + run['hostError']['code'])
    duplicate = len(business) - len({json.dumps(item, sort_keys=True) for item in business})
    return {'passed': not issues, 'goalReached': expected is not None, 'factsMatched': facts,
        'firstAttemptClean': expected is not None and not issues and bool(business) and business[0][0] ==
            ('repos/list-branches' if case['id'] == 'branches' else 'repos/get'),
        'failures': sorted(set(issues)), 'businessCalls': len(business), 'failedBusinessAttempts': repaired,
        'duplicateBusinessCalls': duplicate, 'readsAboveMinimum': max(0, len(business) - case['minimumReads']),
        'answerFormat': form, 'expectedAnswer': expected}
