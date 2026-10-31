"""RealWorld (Conduit) tasks and deterministic checks.

The caller is the user `jake` (the host supplies his token). dev tasks may be used while
improving a2api; holdout tasks decide the result and are fixed by FINGERPRINT before any run.
Each check reads the final answer, the server state before/after and the normalized calls
(method, path template, ok).
"""

from __future__ import annotations

import hashlib
import json
import re

JSON_RULE = '최종 답변은 다른 설명 없이 다음 키를 가진 JSON 객체 하나로만 작성하세요: '
TASKS = []


def task(identifier, split, kind, question, keys=None):
    def register(check):
        TASKS.append({'id': identifier, 'split': split, 'kind': kind, 'request': question,
                      'question': question + (' ' + JSON_RULE + keys if keys else ''), 'check': check})
        return check
    return register


def answer_json(text):
    """The last JSON object in the answer (fenced or bare), else None."""
    if not isinstance(text, str):
        return None
    for block in reversed(re.findall(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.S)):
        try:
            return json.loads(block)
        except ValueError:
            pass
    end = text.rfind('}')
    while end >= 0:
        depth = 0
        for start in range(end, -1, -1):
            depth += {'}': 1, '{': -1}.get(text[start], 0)
            if depth == 0:
                try:
                    value = json.loads(text[start:end + 1])
                    return value if isinstance(value, dict) else None
                except ValueError:
                    break
        end = text.rfind('}', 0, end)
    return None


def changes(before, after):
    """What changed in the server state, as comparable sets."""
    def rows(state):
        return {
            'follows': {tuple(item) for item in state['follows']},
            'favorites': {tuple(item) for item in state['favorites']},
            'articles': set(state['articles']),
            'comments': {(c['slug'], c['author'], c['body']) for c in state['comments']},
            'bios': {(name, user['bio']) for name, user in state['users'].items()},
        }
    old, new = rows(before), rows(after)
    return {key: {'added': new[key] - old[key], 'removed': old[key] - new[key]} for key in old}


def only(diff, **expected):
    """Exactly the expected additions/removals and nothing else."""
    for key, value in diff.items():
        want = expected.get(key, {'added': set(), 'removed': set()})
        if value['added'] != set(want.get('added', set())) or value['removed'] != set(want.get('removed', set())):
            return False
    return True


def no_writes(calls):
    return not any(call['method'] != 'GET' and call['ok'] for call in calls)


# ------------------------------------------------------------------ dev
@task('RD1', 'dev', 'simple', 'rust 태그가 붙은 글을 최신 글부터 모두 알려줘.', '{"slugs": 문자열 배열}')
def _(c):
    return c.json and c.json.get('slugs') == ['async-rust-pitfalls', 'rust-ownership-in-practice'] and no_writes(c.calls)


@task('RD2', 'dev', 'simple', "'Writing a tiny compiler' 글에 댓글을 단 사람들의 username을 알려줘.", '{"usernames": 문자열 배열}')
def _(c):
    return c.json and sorted(c.json.get('usernames') or []) == ['alice', 'bob', 'jake'] and no_writes(c.calls)


@task('RD3', 'dev', 'simple', 'alice를 팔로우해줘.')
def _(c):
    return only(c.diff, follows={'added': {('jake', 'alice')}})


@task('RD4', 'dev', 'complex', "bob이 쓴 go 태그 글 중 가장 최근 글에 '잘 읽었습니다'라고 댓글을 달아줘.")
def _(c):
    return only(c.diff, comments={'added': {('go-generics-one-year-later', 'jake', '잘 읽었습니다')}})


@task('RD5', 'dev', 'complex', '내 피드(내가 팔로우하는 사람들의 글) 중 좋아요가 가장 많은 글의 제목과 좋아요 수를 알려줘.',
      '{"title": 문자열, "favoritesCount": 정수}')
def _(c):
    return c.json and c.json.get('title') == 'Writing a tiny compiler' and c.json.get('favoritesCount') == 3 and no_writes(c.calls)


@task('RD6', 'dev', 'complex', "내 글 'Draft notes'를 삭제하고, 남아 있는 내 글의 slug 목록을 알려줘.", '{"slugs": 문자열 배열}')
def _(c):
    return (only(c.diff, articles={'removed': {'draft-notes'}})
            and c.json and c.json.get('slugs') == ['training-for-a-marathon'])


@task('RD7', 'dev', 'fault', "slug가 'no-such-article'인 글에 좋아요를 눌러줘.", '{"done": 불리언}')
def _(c):
    return only(c.diff) and c.json is not None and c.json.get('done') is False


@task('RD8', 'dev', 'missing', "글에 '좋아요'라고 댓글 달아줘.")
def _(c):
    return only(c.diff) and no_writes(c.calls)


# ------------------------------------------------------------------ holdout (fixed by FINGERPRINT)
@task('RH1', 'holdout', 'simple', 'databases 태그가 붙은 글의 제목과 작성자 username을 알려줘.', '{"title": 문자열, "author": 문자열}')
def _(c):
    return c.json and c.json.get('title') == 'Postgres indexes explained' and c.json.get('author') == 'alice' and no_writes(c.calls)


@task('RH2', 'holdout', 'simple', 'carol이 좋아요한 글의 slug를 모두 알려줘.', '{"slugs": 문자열 배열}')
def _(c):
    return (c.json and sorted(c.json.get('slugs') or []) ==
            ['async-rust-pitfalls', 'postgres-indexes-explained', 'training-for-a-marathon', 'writing-a-tiny-compiler']
            and no_writes(c.calls))


@task('RH3', 'holdout', 'simple', "내 소개(bio)를 'Marathoner and writer'로 바꿔줘.")
def _(c):
    return only(c.diff, bios={'added': {('jake', 'Marathoner and writer')}, 'removed': {('jake', 'I work at statefarm')}})


@task('RH4', 'holdout', 'complex', 'alice가 쓴 글 중 좋아요 수가 가장 적은 글에 좋아요를 눌러줘.')
def _(c):
    return only(c.diff, favorites={'added': {('jake', 'async-rust-pitfalls')}})


@task('RH5', 'holdout', 'complex', 'dmitri 팔로우를 끊고, 그 뒤 내 피드에 남은 글 수를 알려줘.', '{"count": 정수}')
def _(c):
    return only(c.diff, follows={'removed': {('jake', 'dmitri')}}) and c.json and c.json.get('count') == 0


@task('RH6', 'holdout', 'complex', "'Writing a tiny compiler' 글에 내가 단 댓글을 삭제해줘.")
def _(c):
    return only(c.diff, comments={'removed': {('writing-a-tiny-compiler', 'jake', 'Loved the bytecode part.')}})


@task('RH7', 'holdout', 'fault', "username이 'zoe'인 사용자의 소개(bio)를 알려줘.", '{"found": 불리언}')
def _(c):
    return only(c.diff) and c.json is not None and c.json.get('found') is False


@task('RH8', 'holdout', 'missing', '그 글을 삭제해줘.')
def _(c):
    return only(c.diff) and no_writes(c.calls)


def fingerprint(split='holdout'):
    rows = [(t['id'], t['kind'], t['question']) for t in TASKS if t['split'] == split]
    return 'sha256:' + hashlib.sha256(json.dumps(rows, ensure_ascii=False).encode()).hexdigest()
