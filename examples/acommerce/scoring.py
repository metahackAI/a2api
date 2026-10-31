"""a-commerce's task scoring (xtask/src/run_eval.rs `numbers`, `shown`, `score`), ported as-is.

A run is done when every required tool ran without an error, no must_not_call tool was called,
the expected change set (state, items, failed checks) is there, and every fact's numbers appear
as whole words in what the person sees. Tool and change-set checks apply only to runs over the
A-Commerce tools; screen-shaped facade runs are judged by facts (and forbidden calls), as there.
"""

from __future__ import annotations

from datetime import datetime


def push_number(out, word):
    runs = [run for run in ''.join(c if c.isdigit() or c == '.' else ' ' for c in word).split() if run]
    if not runs:
        return
    if len(runs) == 1:
        number = ''.join(c for c in word if c.isdigit() or c == '.')
        if '.' in number:
            number = number.rstrip('0').rstrip('.')
        number = number.lstrip('0')
        out.append('0' + number if not number or number.startswith('.') else number)
    else:
        out.append(word)


def numbers(text):
    """Whole-word numbers as a person reads them: `$2,463.00` -> 2463, `4.60` -> 4.6, ids stay one word."""
    chars = list(text.lower())
    def digit(index):
        return index is not None and 0 <= index < len(chars) and chars[index].isascii() and chars[index].isdigit()
    out, word = [], []
    for i, c in enumerate(chars):
        between = digit(i - 1) and digit(i + 1)
        thousands = c == ',' and between and all(digit(i + k) for k in (1, 2, 3)) and not digit(i + 4)
        if (c.isascii() and c.isalnum()) or (c == '.' and between):
            word.append(c)
        elif not thousands:
            push_number(out, ''.join(word))
            word = []
    push_number(out, ''.join(word))
    return out


def shown(reply, blocks=()):
    parts = [reply]
    def values(value):
        if isinstance(value, str):
            try:
                parts.append(datetime.fromisoformat(value.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S'))
            except ValueError:
                parts.append(value)
        elif isinstance(value, bool) or value is None:
            return
        elif isinstance(value, (int, float)):
            parts.append(str(value))
        elif isinstance(value, list):
            for item in value:
                values(item)
        elif isinstance(value, dict):
            for item in value.values():
                values(item)
    for block in blocks:
        values(block)
    return set(numbers(' '.join(parts)))


def score(task, *, tool_names_scored, reply, blocks, tools, change_set):
    """tools: [(name, completed)]. Returns (done, missing, precision, recall, unchecked)."""
    missing, precision, recall, unchecked = [], None, None, 0
    expect = task.get('expect') or {}
    required = (task.get('tools') or {}).get('required') or []
    allowed = (task.get('tools') or {}).get('allowed') or []
    ok = lambda name: any(n == name and done for n, done in tools)
    if tool_names_scored:
        missing += [f'tool {name}' for name in required if not ok(name)]
        if tools:
            precision = sum(1 for n, _ in tools if n in required + allowed) / len(tools)
        if required:
            recall = sum(1 for name in required if ok(name)) / len(required)
        want = expect.get('change_set')
        if want:
            if change_set is None:
                missing.append('change set')
            else:
                state = change_set.get('state') or ''
                if want.get('state') and not (state == want['state'] or (want['state'] == 'drafting' and state == 'waiting_for_approval')):
                    missing.append(f"change set state {want['state']} (is {state})")
                items = change_set.get('items') or []
                for item in want.get('items') or []:
                    args = item.get('args') or {}
                    if not any(i.get('tool') == item['tool'] and all((i.get('input') or {}).get(k) == v for k, v in args.items())
                               for i in items):
                        missing.append(f"change set item {item['tool']} {args}")
                failed = [c.get('rule') for i in items for c in i.get('checks') or [] if c.get('passed') is False]
                missing += [f'failed check {rule}' for rule in want.get('checks_failed') or [] if rule not in failed]
    missing += [f'called {name}' for name in expect.get('must_not_call') or [] if any(n == name for n, _ in tools)]
    seen = shown(reply, blocks)
    for fact in expect.get('facts') or []:
        wanted = numbers(fact)
        if not wanted:
            unchecked += 1
            continue
        absent = [n for n in wanted if n not in seen]
        if absent:
            missing.append(f'fact "{fact[:60]}" ({", ".join(absent)} not shown)')
    return not missing, missing, precision, recall, unchecked
