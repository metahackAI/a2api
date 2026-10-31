"""Fixed benchmark tasks and deterministic checkers.

dev tasks are used while improving a2api; holdout tasks decide the final result and
must not be edited after their hash is recorded (see docs/33). Each checker reads only
the final answer, the store before/after the run and the normalized business calls.
"""

from __future__ import annotations

import hashlib
import json
import re

JSON_RULE = '최종 답변은 다른 설명 없이 다음 키를 가진 JSON 객체 하나로만 작성하세요: '


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
    """{(resource, id): (old_row|None, new_row|None)} for every changed row."""
    result = {}
    for key in set(before) | set(after):
        old = {row['id']: row for row in before.get(key, [])}
        new = {row['id']: row for row in after.get(key, [])}
        for identifier in set(old) | set(new):
            if old.get(identifier) != new.get(identifier):
                result[(key, identifier)] = (old.get(identifier), new.get(identifier))
    return result


def calls_to(calls, op):
    return [call for call in calls if call['op'] == op]


class Check:
    def __init__(self, answer, before, after, calls):
        self.answer, self.before, self.after, self.calls = answer, before, after, calls
        self.data = answer_json(answer)
        self.diff = changes(before, after)
        self.failures = []

    def fail(self, code):
        self.failures.append(code)

    def value(self, key, expected, *, unordered=False):
        if not isinstance(self.data, dict):
            return self.fail('ANSWER_NOT_JSON')
        actual = self.data.get(key)
        if unordered and isinstance(actual, list) and isinstance(expected, list):
            ok = sorted(map(str, actual)) == sorted(map(str, expected))
        elif isinstance(expected, str) and isinstance(actual, str):
            ok = actual.strip() == expected
        else:
            ok = actual == expected
        if not ok:
            self.fail('WRONG_VALUE:' + key)

    def no_writes(self):
        if self.diff:
            self.fail('UNEXPECTED_WRITE')

    def only_changed(self, keys):
        if set(self.diff) - set(keys):
            self.fail('UNEXPECTED_WRITE')

    def created(self, key, expected_fields):
        rows = [(k, v) for k, v in self.diff.items() if k[0] == key and v[0] is None]
        if len(rows) != 1:
            self.fail('CREATE_COUNT')
            return None
        (_, identifier), (_, row) = rows[0]
        if any(row.get(name) != value for name, value in expected_fields.items()):
            self.fail('CREATED_FIELDS')
        return identifier


TASKS = []


def task(identifier, split, kind, question, keys=None):
    def register(check):
        # 'request' is the user's ask; the application appends its own answer-format rule.
        TASKS.append({'id': identifier, 'split': split, 'kind': kind, 'request': question,
                      'question': question + ((' ' + JSON_RULE + keys) if keys else ''), 'check': check})
        return check
    return register


# ------------------------------------------------------------------ dev (used for improvement)

@task('D1', 'dev', 'simple', '주문 ORD-1003의 현재 상태와 총액을 알려줘.', '{"status": 문자열, "totalAmount": 정수}')
def _(c):
    c.value('status', 'paid'); c.value('totalAmount', 87000); c.no_writes()


@task('D2', 'dev', 'simple', 'gold 등급 고객을 ID 순서로 최대 3명만 보여줘.', '{"customerIds": 문자열 배열}')
def _(c):
    c.value('customerIds', ['C-001', 'C-003', 'C-005']); c.no_writes()


@task('D3', 'dev', 'simple', '고객 C-004의 지원 티켓을 새로 만들어줘. 제목은 "배송 지연 문의", 우선순위는 high야.',
      '{"ticketId": 문자열}')
def _(c):
    created = c.created('tickets', {'customerId': 'C-004', 'subject': '배송 지연 문의', 'priority': 'high', 'status': 'open'})
    c.only_changed([k for k in c.diff if k[0] == 'tickets' and c.diff[k][0] is None])
    if created:
        c.value('ticketId', created)


@task('D4', 'dev', 'simple', '이메일이 minji.park@example.com인 고객의 ID와 등급을 알려줘.', '{"customerId": 문자열, "tier": 문자열}')
def _(c):
    c.value('customerId', 'C-007'); c.value('tier', 'silver'); c.no_writes()


@task('D5', 'dev', 'complex', 'minji.park@example.com 고객의 가장 최근 주문을 찾고, 그 주문의 배송 상태와 택배사를 알려줘.',
      '{"orderId": 문자열, "shipmentStatus": 문자열, "carrier": 문자열}')
def _(c):
    c.value('orderId', 'ORD-1008'); c.value('shipmentStatus', 'in_transit'); c.value('carrier', 'CJ대한통운'); c.no_writes()


@task('D6', 'dev', 'complex', '주문 ORD-1007이 pending 상태일 때만 취소하고, 아니면 취소하지 말고 현재 상태만 알려줘.',
      '{"cancelled": 불리언, "status": 문자열}')
def _(c):
    c.value('cancelled', False); c.value('status', 'shipped'); c.no_writes()


@task('D7', 'dev', 'complex', '지원 티켓 T-9003을 "지원2팀"의 활성 상담원에게 배정하고 우선순위를 urgent로 올려줘.',
      '{"ticketId": 문자열, "assigneeId": 문자열, "priority": 문자열}')
def _(c):
    c.only_changed([('tickets', 'T-9003')])
    row = c.diff.get(('tickets', 'T-9003'), (None, None))[1] or {}
    if row.get('assigneeId') != 'A-04' or row.get('priority') != 'urgent' or row.get('status') != 'open':
        c.fail('STATE_NOT_UPDATED')
    c.value('ticketId', 'T-9003'); c.value('assigneeId', 'A-04'); c.value('priority', 'urgent')


@task('D8', 'dev', 'complex', '고객 C-002의 모든 주문(취소 포함)의 개수와 총액 합계를 알려줘.', '{"orderCount": 정수, "totalAmount": 정수}')
def _(c):
    c.value('orderCount', 7); c.value('totalAmount', 155000); c.no_writes()


@task('D9', 'dev', 'fault', '배송 SHP-503의 실시간 택배 추적 이벤트를 조회해서 알려줘.', '{"trackingAvailable": 불리언, "events": 배열}')
def _(c):
    c.value('trackingAvailable', False)
    if isinstance(c.data, dict) and c.data.get('events'):
        c.fail('FABRICATED_EVENTS')
    if len(calls_to(c.calls, 'shipments.tracking')) > 2:
        c.fail('REPEATED_FAILING_CALL')
    c.no_writes()


@task('D10', 'dev', 'missing', '주문을 취소해줘.')
def _(c):
    if c.calls:
        c.fail('CALLED_WITHOUT_REQUIRED_INPUT')
    if not c.answer.strip():
        c.fail('EMPTY_ANSWER')
    c.no_writes()


# ------------------------------------------------------------------ holdout (decides the result)

@task('H1', 'holdout', 'simple', '배송 SHP-508의 상태와 도착 예정일을 알려줘.', '{"status": 문자열, "estimatedArrival": 문자열}')
def _(c):
    c.value('status', 'in_transit'); c.value('estimatedArrival', '2026-11-04'); c.no_writes()


@task('H2', 'holdout', 'simple', '상태가 open이고 우선순위가 high인 지원 티켓을 ID 순서로 최대 2개 알려줘.', '{"ticketIds": 문자열 배열}')
def _(c):
    c.value('ticketIds', ['T-9002', 'T-9004']); c.no_writes()


@task('H3', 'holdout', 'simple', '신규 고객을 등록해줘. 이름은 이서준, 이메일은 seojun.lee@example.com, 도시는 부산이야.',
      '{"customerId": 문자열}')
def _(c):
    created = c.created('customers', {'name': '이서준', 'email': 'seojun.lee@example.com', 'city': '부산', 'tier': 'basic', 'status': 'active'})
    c.only_changed([k for k in c.diff if k[0] == 'customers' and c.diff[k][0] is None])
    if created:
        c.value('customerId', created)


@task('H4', 'holdout', 'simple', '이름이 최유나인 고객의 이메일과 도시를 알려줘.', '{"email": 문자열, "city": 문자열}')
def _(c):
    c.value('email', 'yuna.choi@example.com'); c.value('city', '인천'); c.no_writes()


@task('H5', 'holdout', 'complex', '지원 티켓 T-9005를 등록한 고객을 확인하고, 그 고객의 주문 중 pending 또는 paid 상태인 주문 번호를 모두 알려줘.',
      '{"customerId": 문자열, "orderIds": 문자열 배열}')
def _(c):
    c.value('customerId', 'C-006'); c.value('orderIds', ['ORD-1012', 'ORD-1014'], unordered=True); c.no_writes()


@task('H6', 'holdout', 'complex', '주문 ORD-1010이 pending 또는 paid 상태면 취소하고, 처리 후 상태를 알려줘.',
      '{"cancelled": 불리언, "status": 문자열}')
def _(c):
    c.only_changed([('orders', 'ORD-1010')])
    row = c.diff.get(('orders', 'ORD-1010'), (None, None))[1] or {}
    if row.get('status') != 'cancelled':
        c.fail('STATE_NOT_UPDATED')
    c.value('cancelled', True); c.value('status', 'cancelled')


@task('H7', 'holdout', 'complex', '고객 C-006의 등급을 gold로 올리고, 그 고객의 상태가 open인 지원 티켓을 모두 closed로 바꿔줘.',
      '{"tier": 문자열, "closedTicketIds": 문자열 배열}')
def _(c):
    c.only_changed([('customers', 'C-006'), ('tickets', 'T-9006'), ('tickets', 'T-9007')])
    if (c.diff.get(('customers', 'C-006'), (None, None))[1] or {}).get('tier') != 'gold':
        c.fail('STATE_NOT_UPDATED')
    for identifier in ('T-9006', 'T-9007'):
        if (c.diff.get(('tickets', identifier), (None, None))[1] or {}).get('status') != 'closed':
            c.fail('STATE_NOT_UPDATED')
    c.value('tier', 'gold'); c.value('closedTicketIds', ['T-9006', 'T-9007'], unordered=True)


@task('H8', 'holdout', 'complex', '현재 in_transit 상태인 배송의 전체 개수와 택배사별 개수를 알려줘.', '{"total": 정수, "byCarrier": 객체}')
def _(c):
    c.value('total', 4); c.value('byCarrier', {'롯데택배': 2, '우체국택배': 1, 'CJ대한통운': 1}); c.no_writes()


@task('H9', 'holdout', 'fault', '배송 SHP-502의 실시간 추적 정보를 조회하고, 받을 수 없으면 대신 현재 배송 상태와 택배사를 알려줘.',
      '{"trackingAvailable": 불리언, "status": 문자열, "carrier": 문자열}')
def _(c):
    c.value('trackingAvailable', False); c.value('status', 'delivered'); c.value('carrier', '한진택배')
    if len(calls_to(c.calls, 'shipments.tracking')) > 2:
        c.fail('REPEATED_FAILING_CALL')
    c.no_writes()


@task('H10', 'holdout', 'missing', '그 고객 등급을 gold로 올려줘.')
def _(c):
    if c.calls:
        c.fail('CALLED_WITHOUT_REQUIRED_INPUT')
    if not c.answer.strip():
        c.fail('EMPTY_ANSWER')
    c.no_writes()


def tasks(split):
    return [item for item in TASKS if split in ('all', item['split'])]


def assess(item, answer, before, after, calls):
    check = Check(answer or '', before, after, calls)
    item['check'](check)
    return {'passed': not check.failures, 'failures': sorted(set(check.failures)), 'answerJson': check.data}


def fingerprint(split):
    """Hash of the questions and checker source; recorded before the final holdout run."""
    import inspect
    payload = [(item['id'], item['question'], inspect.getsource(item['check'])) for item in tasks(split)]
    return 'sha256:' + hashlib.sha256(json.dumps(payload, ensure_ascii=False).encode()).hexdigest()
