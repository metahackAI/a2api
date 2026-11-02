"""Readable step-by-step traces of a-commerce's own agent runs (`cargo xtask eval --logs DIR`).

python examples/acommerce/own_traces.py artifacts/acommerce/runs/own22-heldout-raw-logs.md --out docs/traces

The evaluator writes one JSON per run in DIR (`<task>-<tool set>-<conversation>.json`: the reply, the
blocks shown and the agent's log) and the report `.md` with one row per run. Each task page shows,
per run: the question, how the agent routed it, the tool candidates its search found, its plan (tool
and arguments), each tool call with its input and what came back, the reply, and the evaluator's
score. Runs are matched to report rows in the order they started.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from traces import code, quote, short, tasks_from  # noqa: E402

ARGUMENT_CHARS, OUTPUT_CHARS, REPLY_CHARS = 700, 600, 2000


def report_rows(report):
    """{task: [(done, tools, missing), ...]} in run order, from the report's per-run table."""
    rows, table = {}, False
    for line in Path(report).read_text().splitlines():
        if line.startswith('| Task |'):
            table = True
            continue
        if not table or not line.startswith('| ') or line.startswith('|---'):
            continue
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        if len(cells) >= 9:
            rows.setdefault(cells[0], []).append({'done': cells[2] == 'yes', 'tools': cells[3], 'missing': cells[8]})
    return rows


def render(run, row, number, task):
    lines = [f"### {run['label']} · {number}회차 · {'✓ 통과' if row and row['done'] else '✗ 실패'}", '']
    turns = run['log'].get('turns') or []
    calls = sum(1 for turn in turns for step in turn['log']['steps'] if step['kind'] == 'call_tool')
    tokens = sum((call.get('input_tokens') or 0) + (call.get('output_tokens') or 0)
                 for turn in turns for call in turn['log'].get('model_calls') or [])
    models = sum(len(turn['log'].get('model_calls') or []) for turn in turns)
    lines += [f"토큰 {tokens:,} · 모델 호출 {models}회 · 도구 호출 {calls}회", '']
    for index, turn in enumerate(turns):
        lines += [f"**질문 {index + 1}**", quote(turn.get('text') or ''), '']
        step_number = 0
        for step in turn['log']['steps']:
            kind = step['kind']
            if kind == 'route':
                lines.append(f"- 라우팅: {step.get('summary')}")
            elif kind == 'search_tools':
                lines.append(f"- 도구 검색 후보: {step.get('summary')}")
            elif kind == 'plan':
                plan = (step.get('output') or {}).get('steps') or []
                planned = '; '.join(f"`{item.get('tool')}` {code(short(item.get('args') or {}, 300))}" for item in plan)
                lines.append(f"- 계획: {planned or step.get('summary')}")
            elif kind == 'call_tool':
                step_number += 1
                given = step.get('input') or {}
                given = given.get('args', given) if isinstance(given, dict) else given
                lines.append(f"{step_number}. 에이전트 → **`{step.get('tool')}`** {code(short(given, ARGUMENT_CHARS))}")
                if step.get('status') == 'completed':
                    lines.append(f"   ← 결과: {code(short(step.get('output'), OUTPUT_CHARS))}")
                else:
                    lines.append(f"   ← 실패: {code(short(step.get('error') or step.get('summary'), OUTPUT_CHARS))}")
            else:
                lines.append(f"- {kind}: {short(step.get('summary') or '', 300)}")
        lines += ['', f"**답변 {index + 1}**", quote(short(turn.get('reply_text') or '', REPLY_CHARS)), '']
        blocks = turn.get('blocks') or []
        if blocks:
            lines.append(f"화면 블록: {', '.join(f'{block.get('ui')}({block.get('title')})' for block in blocks)}")
            lines.append('')
    if row:
        lines.append(f"**채점**: {'✓ 통과' if row['done'] else '✗ 실패 — 빠진 것: ' + row['missing']}")
    lines.append('')
    return lines


def write(report, label, out, tasks):
    logs = Path(str(Path(report).with_suffix('')) + '-logs')
    rows = report_rows(report)
    runs = {}
    for path in sorted(logs.glob('*.json')):
        data = json.loads(path.read_text())
        turns = data['log'].get('turns') or []
        data['started'] = turns[0].get('started_at') if turns else ''
        data['label'] = label
        runs.setdefault(data['task'], []).append(data)
    folder = out / Path(report).stem
    folder.mkdir(parents=True, exist_ok=True)
    index = [f"# {Path(report).stem}", '', f"a-commerce 자체 에이전트 · {label} · 보고서 행과 로그를 시작 순서로 맞춤", '',
             '| 과업 | 결과 |', '|---|---|']
    for task_id, group in runs.items():
        group.sort(key=lambda item: item['started'])
        task = tasks.get(task_id)
        page = [f"# {task_id} — {Path(report).stem}", '', '[← 실행 묶음](README.md)', '']
        if task:
            page += ['**과업**', ''] + [quote(line) + '\n' for line in task['turns']]
            for fact in (task.get('expect') or {}).get('facts') or []:
                page.append(f"- 답에 있어야 할 사실: {fact}")
            page.append('')
        marks = []
        for number, run in enumerate(group, 1):
            row = (rows.get(task_id) or [None] * number)[number - 1] if len(rows.get(task_id) or []) >= number else None
            marks.append('✓' if row and row['done'] else '✗')
            page += render(run, row, number, task)
        (folder / f'{task_id}.md').write_text('\n'.join(page))
        index.append(f"| [{task_id}]({task_id}.md) | {' '.join(marks)} |")
    (folder / 'README.md').write_text('\n'.join(index) + '\n')
    return folder


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('reports', nargs='+', help='report .md files; their logs are in <report without .md>-logs/')
    parser.add_argument('--label', action='append', default=[], help='one per report, e.g. "원본 파사드"')
    parser.add_argument('--out', type=Path, default=Path('docs/traces'))
    parser.add_argument('--repo', default=None)
    options = parser.parse_args()
    if options.repo is None:
        from stack import REPO
        options.repo = REPO
    tasks = tasks_from(options.repo)
    for index, report in enumerate(options.reports):
        label = options.label[index] if index < len(options.label) else Path(report).stem
        print(json.dumps({'report': report, 'pages': str(write(report, label, options.out, tasks))}, ensure_ascii=False))


if __name__ == '__main__':
    main()
