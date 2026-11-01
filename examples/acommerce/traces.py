"""Readable step-by-step traces of evaluate.py runs.

python examples/acommerce/traces.py artifacts/acommerce/runs/ours-design-7.jsonl [...] --out docs/traces

For each run file, writes `<out>/<file stem>/README.md` (task × mode table with links) and one page per
task: every run's questions, each function call with its arguments, what came back, the model's
reasoning at that step when the run recorded it (runs from 2026-11-02), the answers and the score.
Runs before 2026-11-02 did not record which step made which call or which turn a call belongs to;
their calls are listed in order. Results are shown as the model received them, cut to RESULT_CHARS.
"""

from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path
import sys

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

ARGUMENT_CHARS, RESULT_CHARS, REASONING_CHARS, REPLY_CHARS = 700, 600, 700, 2000
MARK = {True: '✓', False: '✗'}


def short(text, limit):
    text = text if isinstance(text, str) else json.dumps(text, ensure_ascii=False, separators=(',', ':'))
    return text if len(text) <= limit else text[:limit] + f'… (+{len(text) - limit:,}자)'


def quote(text):
    return '\n'.join('> ' + line if line else '>' for line in text.splitlines()) or '>'


def code(text):
    return '`` ' + text.replace('`', "'") + ' ``'


def tasks_from(repo):
    found = {}
    for path in glob.glob(str(Path(repo) / 'eval' / 'tasks' / '*' / '*.yml')):
        for task in yaml.safe_load(Path(path).read_text()) or []:
            found[task['id']] = task
    return found


def mark(run):
    return 'E' if run.get('hostError') else MARK[bool(run['done'])]


def outcome(run):
    if run['done']:
        return '✓ 통과'
    return ('E ' + run['hostError'] if run.get('hostError') else '✗ 실패')


def call_lines(number, call):
    arguments = call.get('arguments')
    lines = [f"{number}. 모델 → **`{call['name']}`** {code(short(arguments if arguments is not None else '(JSON 아님)', ARGUMENT_CHARS))}"]
    result = call.get('result') or ''
    status = '실패' if '"status":"failed"' in result[:40] or result.startswith('{"error"') else '결과'
    lines.append(f"   ← {status} {call.get('resultBytes', len(result)):,}B: {code(short(result, RESULT_CHARS))}")
    return lines


def render_run(run, task):
    usage = run.get('usage') or {}
    lines = [f"### {run['mode']} · {run.get('repetition', 0) + 1}회차 · {outcome(run)}",
             '',
             f"토큰 {usage.get('total_tokens', 0):,} · {run.get('seconds', 0)}초 · 모델 호출 {run.get('modelRequests', len(run.get('steps', [])))}회 · "
             f"도구 호출 {len(run.get('toolCalls', []))}회"
             + (f" · 첫 요청 프롬프트 {run['firstPromptTokens']:,}토큰" if run.get('firstPromptTokens') else ''), '']
    setup = run.get('setup') or {}
    if setup:
        detail = f"전략 `{setup.get('strategy')}`, 함수 {setup.get('functions')}개"
        if setup.get('indexChars'):
            detail += f", 목차 {setup['indexChars']:,}자(system prompt)"
        lines += [f"준비: {detail}", '']
    turns = (task or {}).get('turns') or []
    calls = run.get('toolCalls', [])
    steps = run.get('steps', [])
    by_id = {call.get('id'): call for call in calls if call.get('id')}
    replies = list(run.get('replies') or [])
    if steps and all('calls' in step for step in steps) and by_id:
        # Recorded per step (2026-11-02 and later): reasoning, then that step's calls, by turn.
        number, turn = 0, -1
        reply_index = 0
        for step in steps:
            step_calls = [by_id[i] for i in step.get('calls', []) if i in by_id]
            step_turn = step_calls[0].get('turn', turn) if step_calls else turn
            if step_turn != turn and step_turn < len(turns) and step_calls:
                turn = step_turn
                lines += [f"**질문 {turn + 1}**", quote(turns[turn]), '']
            elif turn == -1 and turns:
                turn = 0
                lines += ['**질문 1**', quote(turns[0]), '']
            if step.get('reasoning'):
                thought = ' '.join(step['reasoning'].split())
                asked = ' '.join(turns[turn].split()) if 0 <= turn < len(turns) else ''
                if asked and thought.startswith(asked):  # this model starts its reasoning by restating the request
                    thought = thought[len(asked):].strip()
                lines.append(f"- 모델 판단(추론 필드): {short(thought, REASONING_CHARS)}")
            for call in step_calls:
                number += 1
                lines += call_lines(number, call)
            if step.get('finish') == 'stop' and reply_index < len(replies):
                lines += ['', f"**답변 {reply_index + 1}**", quote(short(replies[reply_index], REPLY_CHARS)), '']
                reply_index += 1
                if turn + 1 < len(turns):
                    turn += 1
                    lines += [f"**질문 {turn + 1}**", quote(turns[turn]), '']
            elif step.get('finish') == 'length':
                lines.append(f"- 출력 한도에 걸림(완료 토큰 {(step.get('usage') or {}).get('completion_tokens')})")
    else:
        for index, line in enumerate(turns):
            lines += [f"**질문 {index + 1}**", quote(line), '']
        if len(turns) > 1:
            lines += ['_(이 실행은 호출이 어느 턴에 속하는지 기록하지 않았다. 호출을 순서대로 보인다.)_', '']
        for number, call in enumerate(calls, 1):
            lines += call_lines(number, call)
        for index, reply in enumerate(replies):
            lines += ['', f"**답변 {index + 1}**", quote(short(reply, REPLY_CHARS))]
        lines.append('')
    stops = {'MODEL_CALL_LIMIT': '한 턴의 모델 호출 한도(12회)에 걸려 중단', 'TURN_TIMEOUT': '한 턴의 시간 한도(120초)에 걸려 중단',
             'MODEL_OUTPUT_TRUNCATED': '모델 출력이 출력 한도에 걸려 중단', 'MODEL_HTTP_500': '모델 서버 오류(500)로 중단'}
    if run.get('hostError'):
        lines += [f"_({stops.get(run['hostError'], run['hostError'] + '로 중단')})_", '']
    if run.get('truncated'):
        lines += ['출력 한도에 걸린 단계의 화면 출력:', quote(short(run['truncated'].get('content') or '(없음)', 800)), '']
    lines.append(f"**채점**: {outcome(run)}" + ('' if run['done'] else ' — 빠진 것: ' + '; '.join(run.get('missing') or [])))
    if run.get('precision') is not None or run.get('recall') is not None:
        figure = lambda value: '—' if value is None else f'{value:.2f}'
        lines.append(f"(도구 정밀도 {figure(run.get('precision'))}, 재현율 {figure(run.get('recall'))})")
    lines.append('')
    return lines


def write_set(path, tasks, out):
    lines = Path(path).read_text().splitlines()
    header = json.loads(lines[0]) if lines else {}
    runs = [json.loads(line) for line in lines if '"type": "run"' in line]
    if not runs:
        return None
    folder = out / Path(path).stem
    folder.mkdir(parents=True, exist_ok=True)
    modes = list(dict.fromkeys(run['mode'] for run in runs))
    order = list(dict.fromkeys(run['task'] for run in runs))
    for task_id in order:
        task = tasks.get(task_id)
        page = [f"# {task_id} — {Path(path).stem}", '',
                f"[← 실행 묶음]({'README.md'}) · 세트 `{header.get('set')}` · a-commerce `{(header.get('acommerceCommit') or '')[:7]}` · "
                f"a2api `{(header.get('gitCommit') or '')[:7]}`", '']
        if task:
            expect = task.get('expect') or {}
            page += ['**과업**', ''] + [quote(line) + '\n' for line in task['turns']]
            page += [f"- 필요한 도구: {', '.join(f'`{t}`' for t in (task.get('tools') or {}).get('required') or []) or '—'}",
                     f"- 허용 도구: {', '.join(f'`{t}`' for t in (task.get('tools') or {}).get('allowed') or []) or '—'}"]
            for fact in expect.get('facts') or []:
                page.append(f"- 답에 있어야 할 사실: {fact}")
            if expect.get('change_set'):
                page.append(f"- change set: {code(short(expect['change_set'], 400))}")
            if expect.get('must_not_call'):
                page.append(f"- 부르면 안 됨: {', '.join(expect['must_not_call'])}")
            page.append('')
        for mode in modes:
            for run in [r for r in runs if r['task'] == task_id and r['mode'] == mode]:
                page += render_run(run, task)
        (folder / f'{task_id}.md').write_text('\n'.join(page))
    table = [f"# {Path(path).stem}", '',
             f"시작 {header.get('startedAt', '')[:19]}Z · 세트 `{header.get('set')}` · 방식 {', '.join(f'`{m}`' for m in modes)} · "
             f"a-commerce `{(header.get('acommerceCommit') or '')[:7]}` · a2api `{(header.get('gitCommit') or '')[:7]}`"
             + (f" · 출력 상한 {header['maxTokens'] or '없음'}" if 'maxTokens' in header else ' · 출력 상한 2048')
             + (f" · schema 예산 {header['maxToolBytes']}" if 'maxToolBytes' in header else ''), '',
             '| 과업 | ' + ' | '.join(modes) + ' |', '|---' * (len(modes) + 1) + '|']
    for task_id in order:
        cells = [' '.join(mark(r) for r in runs if r['task'] == task_id and r['mode'] == mode) or '—' for mode in modes]
        table.append(f"| [{task_id}]({task_id}.md) | " + ' | '.join(cells) + ' |')
    table.append('')
    table.append('| 방식 | 통과 |')
    table.append('|---|---|')
    for mode in modes:
        group = [r for r in runs if r['mode'] == mode]
        table.append(f"| {mode} | {sum(r['done'] for r in group)}/{len(group)} |")
    (folder / 'README.md').write_text('\n'.join(table) + '\n')
    return folder


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('runs', nargs='+')
    parser.add_argument('--out', type=Path, default=Path('docs/traces'))
    parser.add_argument('--repo', default=None, help='a-commerce checkout with eval/tasks (default: stack.REPO)')
    options = parser.parse_args()
    if options.repo is None:
        from stack import REPO
        options.repo = REPO
    tasks = tasks_from(options.repo)
    for path in options.runs:
        folder = write_set(path, tasks, options.out)
        print(json.dumps({'runs': path, 'pages': str(folder) if folder else None}))


if __name__ == '__main__':
    main()
