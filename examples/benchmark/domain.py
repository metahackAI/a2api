"""Single source of truth for the benchmark API implemented in Python, Spring, Go and Rust.

The same definition generates the published OpenAPI document (the "ordinary spec"
baselines) and every language implementation, so all of them describe and run
the same behavior. Core resources carry the task data; the other resources are
realistic distractors that only change the API size.
"""

from __future__ import annotations

from dataclasses import dataclass, field

SCALES = ('small', 'medium', 'large')
FIXED_TIME = '2026-10-31T09:00:00Z'
DEFAULT_LIMIT, MAX_LIMIT = 5, 20
INTERNAL_FIELDS = ('tenantId', 'internalNote', 'audit')  # returned by the service, hidden by a2api hosts


@dataclass(frozen=True)
class Field:
    name: str
    kind: str                      # string | integer | boolean | strings
    nullable: bool = False
    enum: tuple[str, ...] | None = None
    label: str = ''


@dataclass(frozen=True)
class Resource:
    key: str                       # python/storage key: purchase_orders
    path: str                      # /purchase-orders
    cls: str                       # PurchaseOrder
    plural: str                    # PurchaseOrders
    id_format: str                 # PO-{:04d}
    label: str                     # Korean business name
    fields: tuple[Field, ...]
    filters: tuple[str, ...]
    search: tuple[str, ...]
    ops: tuple[str, ...]
    create_required: tuple[str, ...] = ()
    create_optional: tuple[str, ...] = ()   # caller may set; default from create_defaults
    create_defaults: dict = field(default_factory=dict)
    patch: tuple[str, ...] = ()
    seeds: tuple[dict, ...] = ()
    keywords: tuple[str, ...] = ()

    def field(self, name):
        return next(item for item in self.fields if item.name == name)

    def next_number(self):
        return max(int(row['id'].split('-')[-1]) for row in self.seeds) + 1 if self.seeds else 1

    @property
    def snake(self):
        return self.key

    @property
    def singular_snake(self):
        return ''.join('_' + c.lower() if c.isupper() else c for c in self.cls).lstrip('_')

    def operation_id(self, op):
        return {'list': 'list' + self.plural, 'get': 'get' + self.cls, 'create': 'create' + self.cls,
                'update': 'update' + self.cls, 'delete': 'delete' + self.cls, 'search': 'search' + self.plural,
                'cancel': 'cancel' + self.cls, 'tracking': 'get' + self.cls + 'Tracking'}[op]

    def snake_op(self, op):
        return {'list': 'list_' + self.key, 'get': 'get_' + self.singular_snake,
                'create': 'create_' + self.singular_snake, 'update': 'update_' + self.singular_snake,
                'delete': 'delete_' + self.singular_snake, 'search': 'search_' + self.key,
                'cancel': 'cancel_' + self.singular_snake, 'tracking': 'get_' + self.singular_snake + '_tracking'}[op]

    def route(self, op):
        return {'list': ('GET', self.path), 'get': ('GET', self.path + '/{id}'), 'create': ('POST', self.path),
                'update': ('PATCH', self.path + '/{id}'), 'delete': ('DELETE', self.path + '/{id}'),
                'search': ('POST', self.path + '/search'), 'cancel': ('POST', self.path + '/{id}/cancel'),
                'tracking': ('GET', self.path + '/{id}/tracking')}[op]

    def effect(self, op):
        return 'read' if op in ('list', 'get', 'search', 'tracking') else 'write'

    def summary(self, op):
        label = self.label
        def values(name):
            item = self.field(name)
            return '(' + '|'.join(item.enum) + ')' if item.enum else ''
        filters = ', '.join(self.field(name).label + values(name) for name in self.filters)
        patch = ', '.join(self.field(name).label + values(name) for name in self.patch)
        required = ', '.join(self.field(name).label for name in self.create_required)
        return {
            'list': f'{label} 목록을 조회한다. 필터: {filters}. page(1부터)/limit(기본 {DEFAULT_LIMIT}, 최대 {MAX_LIMIT})로 페이지를 나누고 total/hasMore를 반환한다.',
            'get': f'{label} ID로 {label} 한 건(' + '·'.join(item.label for item in self.fields) + ')을 조회한다.',
            'create': f'새 {label}을(를) 생성하고 발급된 ID를 반환한다. 필수: {required}.',
            'update': f'{label} 한 건의 일부 필드를 수정한다. 수정 가능: {patch}.',
            'delete': f'{label} 한 건을 삭제한다.',
            'search': f'{label}을(를) ' + '·'.join(self.field(n).label for n in self.search) + ' 부분 문자열로 검색한다.',
            'cancel': f'{label}을(를) 취소한다. pending 또는 paid 상태만 취소할 수 있고 그 외 상태는 409를 반환한다.',
            'tracking': f'{label}의 택배사 실시간 추적 이벤트를 조회한다.',
        }[op]

    def op_keywords(self, op):
        verbs = {'list': ['목록', '조회', 'list'], 'get': ['조회', '상세', 'get'], 'create': ['생성', '등록', 'create'],
                 'update': ['수정', '변경', 'update'], 'delete': ['삭제', 'delete'], 'search': ['검색', 'search', '찾기'],
                 'cancel': ['취소', 'cancel'], 'tracking': ['추적', '실시간', 'tracking']}[op]
        return [*self.keywords, *verbs]


def F(name, kind='string', label='', **options):
    return Field(name, kind, label=label or name, **options)


ORDER_STATUS = ('pending', 'paid', 'shipped', 'delivered', 'cancelled')
CUSTOMERS = Resource(
    'customers', '/customers', 'Customer', 'Customers', 'C-{:03d}', '고객',
    (F('name', label='이름'), F('email', label='이메일'), F('tier', label='등급', enum=('basic', 'silver', 'gold')),
     F('status', label='상태', enum=('active', 'suspended')), F('city', label='도시'), F('createdAt', label='가입 시각')),
    filters=('tier', 'status', 'city'), search=('name', 'email'), ops=('list', 'get', 'create', 'update', 'search'),
    create_required=('name', 'email', 'city'), create_optional=('tier',), create_defaults={'tier': 'basic', 'status': 'active'},
    patch=('name', 'email', 'tier', 'status', 'city'), keywords=('고객', 'customer', '회원'),
    seeds=tuple({'id': i, 'name': n, 'email': e, 'tier': t, 'status': s, 'city': c, 'createdAt': d} for i, n, e, t, s, c, d in [
        ('C-001', '김민준', 'minjun.kim@example.com', 'gold', 'active', '서울', '2025-01-05T10:00:00Z'),
        ('C-002', '이서연', 'seoyeon.lee@example.com', 'silver', 'active', '부산', '2025-02-11T10:00:00Z'),
        ('C-003', '박지호', 'jiho.park@example.com', 'gold', 'suspended', '대구', '2025-03-02T10:00:00Z'),
        ('C-004', '최유나', 'yuna.choi@example.com', 'basic', 'active', '인천', '2025-03-20T10:00:00Z'),
        ('C-005', '정하준', 'hajun.jung@example.com', 'gold', 'active', '서울', '2025-04-08T10:00:00Z'),
        ('C-006', '강도윤', 'doyun.kang@example.com', 'basic', 'active', '광주', '2025-05-17T10:00:00Z'),
        ('C-007', '박민지', 'minji.park@example.com', 'silver', 'active', '서울', '2025-06-01T10:00:00Z'),
        ('C-008', '윤서아', 'seoa.yoon@example.com', 'gold', 'active', '대전', '2025-07-23T10:00:00Z')]))
ORDERS = Resource(
    'orders', '/orders', 'Order', 'Orders', 'ORD-{:04d}', '주문',
    (F('customerId', label='고객 ID'), F('status', label='상태', enum=ORDER_STATUS),
     F('totalAmount', 'integer', label='총액(원)'), F('itemCount', 'integer', label='상품 수'),
     F('createdAt', label='주문 시각'), F('shipmentIds', 'strings', label='배송 ID 목록')),
    filters=('customerId', 'status'), search=('customerId',), ops=('list', 'get', 'create', 'update', 'cancel'),
    create_required=('customerId', 'totalAmount', 'itemCount'), create_defaults={'status': 'pending', 'shipmentIds': []},
    patch=('status', 'itemCount'), keywords=('주문', 'order', '구매'),
    seeds=tuple({'id': i, 'customerId': c, 'status': s, 'totalAmount': t, 'itemCount': n, 'createdAt': d, 'shipmentIds': list(x)}
                for i, c, s, t, n, d, x in [
        ('ORD-1001', 'C-001', 'delivered', 45000, 2, '2026-09-01T09:10:00Z', ['SHP-501']),
        ('ORD-1002', 'C-002', 'delivered', 12000, 1, '2026-09-03T11:20:00Z', ['SHP-502']),
        ('ORD-1003', 'C-003', 'paid', 87000, 3, '2026-09-05T14:00:00Z', []),
        ('ORD-1004', 'C-002', 'shipped', 33000, 2, '2026-09-10T08:30:00Z', ['SHP-503']),
        ('ORD-1005', 'C-007', 'delivered', 21000, 1, '2026-09-12T16:45:00Z', ['SHP-504']),
        ('ORD-1006', 'C-002', 'cancelled', 15000, 1, '2026-09-15T10:00:00Z', []),
        ('ORD-1007', 'C-001', 'shipped', 54000, 2, '2026-09-18T13:15:00Z', ['SHP-505']),
        ('ORD-1008', 'C-007', 'shipped', 64000, 4, '2026-10-02T19:05:00Z', ['SHP-506']),
        ('ORD-1009', 'C-002', 'paid', 41000, 2, '2026-10-05T09:40:00Z', []),
        ('ORD-1010', 'C-005', 'pending', 26000, 1, '2026-10-08T12:00:00Z', []),
        ('ORD-1011', 'C-002', 'delivered', 9000, 1, '2026-10-10T15:30:00Z', ['SHP-507']),
        ('ORD-1012', 'C-006', 'paid', 73000, 3, '2026-10-12T17:20:00Z', []),
        ('ORD-1013', 'C-002', 'shipped', 18000, 1, '2026-10-15T08:05:00Z', ['SHP-508']),
        ('ORD-1014', 'C-006', 'pending', 30000, 2, '2026-10-18T10:50:00Z', []),
        ('ORD-1015', 'C-002', 'pending', 27000, 1, '2026-10-20T21:10:00Z', []),
        ('ORD-1016', 'C-008', 'delivered', 56000, 2, '2026-10-21T07:55:00Z', ['SHP-509'])]))
SHIPMENTS = Resource(
    'shipments', '/shipments', 'Shipment', 'Shipments', 'SHP-{:03d}', '배송',
    (F('orderId', label='주문 ID'), F('carrier', label='택배사'),
     F('status', label='상태', enum=('preparing', 'in_transit', 'delivered', 'returned')),
     F('trackingNumber', label='운송장 번호'), F('estimatedArrival', label='도착 예정일', nullable=True),
     F('updatedAt', label='갱신 시각')),
    filters=('orderId', 'status', 'carrier'), search=('trackingNumber',), ops=('list', 'get', 'tracking'),
    keywords=('배송', 'shipment', '택배', 'delivery'),
    seeds=tuple({'id': i, 'orderId': o, 'carrier': c, 'status': s, 'trackingNumber': n, 'estimatedArrival': e, 'updatedAt': u}
                for i, o, c, s, n, e, u in [
        ('SHP-501', 'ORD-1001', 'CJ대한통운', 'delivered', '6301-1001', None, '2026-09-03T18:00:00Z'),
        ('SHP-502', 'ORD-1002', '한진택배', 'delivered', '5102-1002', None, '2026-09-05T15:00:00Z'),
        ('SHP-503', 'ORD-1004', '롯데택배', 'in_transit', '2303-1004', '2026-11-02', '2026-10-30T09:00:00Z'),
        ('SHP-504', 'ORD-1005', 'CJ대한통운', 'delivered', '6304-1005', None, '2026-09-14T12:00:00Z'),
        ('SHP-505', 'ORD-1007', '우체국택배', 'in_transit', '7105-1007', '2026-11-01', '2026-10-30T11:00:00Z'),
        ('SHP-506', 'ORD-1008', 'CJ대한통운', 'in_transit', '6306-1008', '2026-11-03', '2026-10-30T13:00:00Z'),
        ('SHP-507', 'ORD-1011', '한진택배', 'delivered', '5107-1011', None, '2026-10-12T16:00:00Z'),
        ('SHP-508', 'ORD-1013', '롯데택배', 'in_transit', '2308-1013', '2026-11-04', '2026-10-30T15:00:00Z'),
        ('SHP-509', 'ORD-1016', 'CJ대한통운', 'delivered', '6309-1016', None, '2026-10-23T10:00:00Z')]))
TICKETS = Resource(
    'tickets', '/tickets', 'Ticket', 'Tickets', 'T-{:04d}', '지원 티켓',
    (F('customerId', label='고객 ID'), F('subject', label='제목'),
     F('status', label='상태', enum=('open', 'pending', 'closed')),
     F('priority', label='우선순위', enum=('low', 'normal', 'high', 'urgent')),
     F('assigneeId', label='담당 상담원 ID', nullable=True), F('createdAt', label='생성 시각')),
    filters=('customerId', 'status', 'priority'), search=('subject',), ops=('list', 'get', 'create', 'update'),
    create_required=('customerId', 'subject', 'priority'), create_defaults={'status': 'open', 'assigneeId': None},
    patch=('subject', 'status', 'priority', 'assigneeId'), keywords=('티켓', '지원', '문의', 'ticket', 'support', 'CS'),
    seeds=tuple({'id': i, 'customerId': c, 'subject': s, 'status': st, 'priority': p, 'assigneeId': a, 'createdAt': d}
                for i, c, s, st, p, a, d in [
        ('T-9001', 'C-001', '환불 문의', 'closed', 'normal', 'A-01', '2026-09-20T10:00:00Z'),
        ('T-9002', 'C-003', '계정 정지 해제 요청', 'open', 'high', None, '2026-10-01T10:00:00Z'),
        ('T-9003', 'C-002', '배송지 변경', 'open', 'normal', None, '2026-10-11T10:00:00Z'),
        ('T-9004', 'C-005', '결제 오류', 'open', 'high', 'A-02', '2026-10-14T10:00:00Z'),
        ('T-9005', 'C-006', '포인트 적립 누락', 'pending', 'low', None, '2026-10-19T10:00:00Z'),
        ('T-9006', 'C-006', '주소 변경 요청', 'open', 'normal', None, '2026-10-22T10:00:00Z'),
        ('T-9007', 'C-006', '쿠폰 미적용', 'open', 'low', None, '2026-10-24T10:00:00Z'),
        ('T-9008', 'C-007', '상품 파손', 'closed', 'high', 'A-03', '2026-10-25T10:00:00Z')]))
AGENTS = Resource(
    'agents', '/agents', 'Agent', 'Agents', 'A-{:02d}', '상담원',
    (F('name', label='이름'), F('team', label='팀'), F('active', 'boolean', label='활성 여부'), F('email', label='이메일')),
    filters=('team', 'active'), search=('name',), ops=('list', 'get'), keywords=('상담원', 'agent', '담당자', '팀'),
    seeds=tuple({'id': i, 'name': n, 'team': t, 'active': a, 'email': e} for i, n, t, a, e in [
        ('A-01', '한지민', '지원1팀', True, 'jimin.han@example.com'),
        ('A-02', '오세훈', '지원1팀', True, 'sehun.oh@example.com'),
        ('A-03', '서지우', '지원2팀', False, 'jiwoo.seo@example.com'),
        ('A-04', '문가영', '지원2팀', True, 'gayoung.moon@example.com'),
        ('A-05', '배수지', '지원3팀', True, 'suji.bae@example.com'),
        ('A-06', '임도현', '지원2팀', False, 'dohyun.lim@example.com')]))
CORE = (CUSTOMERS, ORDERS, SHIPMENTS, TICKETS, AGENTS)

# (key, path, class, plural, prefix, label, statuses, keywords). Medium uses the first six:
# names deliberately near the core business words to stress selection.
DISTRACTORS = [
    ('purchase_orders', '/purchase-orders', 'PurchaseOrder', 'PurchaseOrders', 'PO', '구매 발주', ('draft', 'approved', 'received'), ('발주', '구매', 'purchase', 'order')),
    ('returns', '/returns', 'ReturnRequest', 'ReturnRequests', 'RT', '반품 요청', ('requested', 'approved', 'rejected'), ('반품', '주문', 'return')),
    ('invoices', '/invoices', 'Invoice', 'Invoices', 'IV', '청구서', ('issued', 'paid', 'overdue'), ('청구', '결제', 'invoice')),
    ('contacts', '/contacts', 'Contact', 'Contacts', 'CT', '거래처 연락처', ('active', 'archived'), ('연락처', '고객사', 'contact')),
    ('freight_shipments', '/freight-shipments', 'FreightShipment', 'FreightShipments', 'FS', '화물 운송', ('booked', 'moving', 'arrived'), ('화물', '운송', '배송', 'freight')),
    ('maintenance_tickets', '/maintenance-tickets', 'MaintenanceTicket', 'MaintenanceTickets', 'MT', '설비 점검 티켓', ('open', 'scheduled', 'done'), ('설비', '점검', '티켓', 'maintenance')),
    ('payments', '/payments', 'Payment', 'Payments', 'PM', '결제 내역', ('authorized', 'captured', 'failed'), ('결제', 'payment')),
    ('refunds', '/refunds', 'Refund', 'Refunds', 'RF', '환불', ('requested', 'completed', 'rejected'), ('환불', 'refund')),
    ('products', '/products', 'Product', 'Products', 'PR', '상품', ('on_sale', 'sold_out', 'hidden'), ('상품', 'product')),
    ('inventory_items', '/inventory-items', 'InventoryItem', 'InventoryItems', 'II', '재고 품목', ('in_stock', 'low', 'out'), ('재고', 'inventory')),
    ('warehouses', '/warehouses', 'Warehouse', 'Warehouses', 'WH', '물류 창고', ('open', 'closed'), ('창고', 'warehouse')),
    ('carriers', '/carriers', 'Carrier', 'Carriers', 'CR', '운송사 계약', ('active', 'suspended'), ('택배사', '운송사', 'carrier')),
    ('employees', '/employees', 'Employee', 'Employees', 'EM', '직원', ('active', 'leave', 'resigned'), ('직원', 'employee')),
    ('departments', '/departments', 'Department', 'Departments', 'DP', '부서', ('active', 'merged'), ('부서', 'department')),
    ('projects', '/projects', 'Project', 'Projects', 'PJ', '프로젝트', ('planned', 'running', 'closed'), ('프로젝트', 'project')),
    ('work_tasks', '/work-tasks', 'WorkTask', 'WorkTasks', 'WT', '업무 작업', ('todo', 'doing', 'done'), ('작업', '할일', 'task')),
    ('campaigns', '/campaigns', 'Campaign', 'Campaigns', 'CA', '마케팅 캠페인', ('draft', 'live', 'ended'), ('캠페인', 'campaign')),
    ('coupons', '/coupons', 'Coupon', 'Coupons', 'CU', '쿠폰', ('active', 'expired'), ('쿠폰', 'coupon')),
    ('subscriptions', '/subscriptions', 'Subscription', 'Subscriptions', 'SB', '정기 구독', ('active', 'paused', 'cancelled'), ('구독', 'subscription')),
    ('contracts', '/contracts', 'Contract', 'Contracts', 'CN', '계약', ('draft', 'signed', 'terminated'), ('계약', 'contract')),
    ('assets', '/assets', 'Asset', 'Assets', 'AS', '자산', ('in_use', 'stored', 'disposed'), ('자산', 'asset')),
    ('vendors', '/vendors', 'Vendor', 'Vendors', 'VD', '협력사', ('active', 'blocked'), ('협력사', '공급사', 'vendor')),
    ('quotes', '/quotes', 'Quote', 'Quotes', 'QT', '견적', ('draft', 'sent', 'accepted'), ('견적', 'quote')),
    ('leads', '/leads', 'Lead', 'Leads', 'LD', '영업 리드', ('incoming', 'qualified', 'lost'), ('리드', '영업', 'lead')),
    ('opportunities', '/opportunities', 'Opportunity', 'Opportunities', 'OP', '영업 기회', ('open', 'won', 'lost'), ('기회', '영업', 'opportunity')),
    ('events', '/events', 'Event', 'Events', 'EV', '행사', ('scheduled', 'done', 'cancelled'), ('행사', 'event')),
    ('announcements', '/announcements', 'Announcement', 'Announcements', 'AN', '공지', ('draft', 'published'), ('공지', 'announcement')),
    ('notifications', '/notifications', 'Notification', 'Notifications', 'NT', '알림 발송', ('queued', 'sent', 'failed'), ('알림', 'notification')),
    ('budgets', '/budgets', 'Budget', 'Budgets', 'BG', '예산', ('draft', 'approved'), ('예산', 'budget')),
    ('expenses', '/expenses', 'Expense', 'Expenses', 'EX', '경비', ('submitted', 'approved', 'rejected'), ('경비', 'expense')),
    ('timesheets', '/timesheets', 'Timesheet', 'Timesheets', 'TS', '근무 기록', ('open', 'submitted', 'approved'), ('근무', 'timesheet')),
    ('devices', '/devices', 'Device', 'Devices', 'DV', '단말기', ('active', 'lost', 'retired'), ('단말기', 'device')),
    ('stores', '/stores', 'RetailStore', 'RetailStores', 'ST', '매장', ('open', 'closed'), ('매장', 'store')),
    ('promotions', '/promotions', 'Promotion', 'Promotions', 'PRM', '프로모션', ('planned', 'active', 'ended'), ('프로모션', 'promotion')),
    ('reviews', '/reviews', 'Review', 'Reviews', 'RV', '상품 리뷰', ('visible', 'hidden'), ('리뷰', 'review')),
    ('surveys', '/surveys', 'Survey', 'Surveys', 'SV', '설문', ('draft', 'open', 'closed'), ('설문', 'survey')),
]
OWNERS = ['C-001', 'C-002', 'C-003', 'C-004', 'C-005', 'C-006', 'C-007', 'C-008']
CATEGORIES = ['general', 'priority', 'internal']


def distractor(key, path, cls, plural, prefix, label, statuses, keywords):
    seeds = tuple({'id': f'{prefix}-{index:04d}', 'name': f'{label} {index}', 'status': statuses[index % len(statuses)],
                   'ownerId': OWNERS[(index * 3) % len(OWNERS)], 'amount': 1000 * ((index * 7) % 50 + 1),
                   'category': CATEGORIES[index % len(CATEGORIES)], 'createdAt': f'2026-08-{index + 1:02d}T09:00:00Z'}
                  for index in range(1, 13))
    return Resource(key, path, cls, plural, prefix + '-{:04d}', label,
                    (F('name', label='이름'), F('status', label='상태', enum=statuses), F('ownerId', label='소유자 ID'),
                     F('amount', 'integer', label='금액(원)'), F('category', label='분류'), F('createdAt', label='생성 시각')),
                    filters=('status', 'ownerId', 'category'), search=('name',),
                    ops=('list', 'get', 'create', 'update', 'delete', 'search'),
                    create_required=('name', 'ownerId', 'amount'), create_optional=('category',),
                    create_defaults={'status': statuses[0], 'category': 'general'},
                    patch=('name', 'status', 'amount', 'category'), seeds=seeds, keywords=keywords)


OTHERS = tuple(distractor(*row) for row in DISTRACTORS)


def resources(scale):
    if scale == 'small':
        return CORE
    if scale == 'medium':
        return CORE + OTHERS[:6]
    if scale == 'large':
        return CORE + OTHERS
    raise ValueError('scale must be small, medium or large')


def operations(scale):
    """Every public operation: (resource, op) in a stable order."""
    return [(resource, op) for resource in resources(scale) for op in resource.ops]


def seed_state(scale):
    """Initial public+internal rows for every resource, as the services return them."""
    state = {}
    for resource in resources(scale):
        rows = []
        for seed in resource.seeds:
            rows.append({**seed, 'tenantId': 'tenant-a', 'internalNote': 'server-only note for ' + seed['id'],
                         'audit': {'createdBy': 'seed', 'updatedBy': 'seed', 'revision': 1, 'source': 'migration'}})
        state[resource.key] = rows
    return state
