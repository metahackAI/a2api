"""Executors for the compared modes. All share the same model loop, tasks and checkers.

spec-tools  : every OpenAPI operation as one function tool, raw HTTP responses
spec-prompt : the whole OpenAPI document in the system prompt + one generic http_request tool
a2api       : ToolSession (a2api-tools) over the converted application of each language
"""

from __future__ import annotations

import asyncio
import copy
import json
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, quote, urlencode
from urllib.request import Request, urlopen

from a2api import ExecutionContext, ToolSession
from a2api.tool_session import SEARCH_NAME

from domain import operations

CONTEXT = ExecutionContext('bench-user', 'tenant-a', frozenset())
COMMON = '''당신은 업무 API 도구를 사용하는 한국어 비서입니다. 도구로 실제 확인한 정보만 답하세요.
- 도구 설명과 입력 schema를 정확히 따르고, 이전 결과에서 받은 실제 ID와 값을 사용하세요. 값을 지어내지 마세요.
- 요청 처리에 꼭 필요한 정보(대상 ID 등)가 질문과 대화에 없으면 도구를 호출하지 말고 사용자에게 질문하세요.
- 사용자가 지정한 조건·개수·필터를 지키고, 요청하지 않은 변경은 하지 마세요.
- 실패한 호출을 성공으로 설명하지 말고, 같은 실패를 반복 호출하지 마세요.
- 요청한 형식이 있으면 최종 답변을 그 형식으로 작성하세요.'''
MODE_RULES = {
    'spec-tools': '',
    'spec-prompt': '\n- API는 아래 OpenAPI 명세의 경로·파라미터·본문 형식대로 http_request 도구로 호출하세요.',
    'a2api': '\n- 필요한 함수가 도구 목록에 없을 때만 a2api_search로 찾으세요. 선택된 함수는 다음 단계에서 호출할 수 있습니다.',
}
HTTP_TOOL = {'type': 'function', 'function': {
    'name': 'http_request',
    'description': 'Call the API described in the system prompt and return the HTTP status and JSON body.',
    'parameters': {'type': 'object', 'additionalProperties': False, 'required': ['method', 'path'], 'properties': {
        'method': {'type': 'string', 'enum': ['GET', 'POST', 'PATCH', 'DELETE']},
        'path': {'type': 'string', 'description': 'Path with path parameters filled in, e.g. /orders/ORD-0001'},
        'query': {'type': 'object', 'description': 'Query parameters',
                  'additionalProperties': {'type': ['string', 'integer', 'boolean']}},
        'body': {'type': 'object', 'description': 'JSON request body'}}}}}


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def http(origin, method, path, query=None, body=None, timeout=15):
    """One HTTP call to the language server; returns (status, parsed JSON or text)."""
    url = origin + path + ('?' + urlencode(query) if query else '')
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode()
    headers = {'Content-Type': 'application/json'} if data is not None else {}
    try:
        with urlopen(Request(url, data=data, method=method, headers=headers), timeout=timeout) as response:
            status, raw = response.status, response.read()
    except HTTPError as error:
        status, raw = error.code, error.read()
        error.close()
    except (URLError, TimeoutError, OSError):
        return 599, 'connection failed'
    text = raw.decode('utf-8', 'replace')
    try:
        return status, json.loads(text) if text else None
    except ValueError:
        return status, text[:500]


def dereference(node, components):
    if isinstance(node, dict):
        if '$ref' in node:
            return dereference(components[node['$ref'].rsplit('/', 1)[-1]], components)
        return {key: dereference(value, components) for key, value in node.items()}
    if isinstance(node, list):
        return [dereference(item, components) for item in node]
    return node


def route_key(scale, method, path):
    """Normalize an actual request path to 'resource.op' via the domain routes."""
    parts = path.split('/')
    for resource, op in operations(scale):
        m, template = resource.route(op)
        segments = template.split('/')
        if m == method and len(segments) == len(parts) and all(t == p or t.startswith('{') for t, p in zip(segments, parts)):
            return f'{resource.key}.{op}'
    return 'unknown'


def query_value(value):
    return ('true' if value else 'false') if isinstance(value, bool) else str(value)


class SpecTools:
    mode = 'spec-tools'

    def __init__(self, scale, spec, origin):
        self.scale, self.origin = scale, origin
        components = spec['components']['schemas']
        keys = {(m, p): f'{r.key}.{op}' for r, op in operations(scale) for m, p in [r.route(op)]}
        self.operations, self._tools = {}, []
        for path, items in spec['paths'].items():
            for method, operation in items.items():
                properties, required, params = {}, [], []
                for parameter in operation.get('parameters', []):
                    schema = dict(dereference(parameter['schema'], components))
                    if parameter.get('description'):
                        schema['description'] = parameter['description']
                    properties[parameter['name']] = schema
                    params.append((parameter['name'], parameter['in']))
                    if parameter.get('required'):
                        required.append(parameter['name'])
                body = operation.get('requestBody')
                if body:
                    properties['body'] = dereference(body['content']['application/json']['schema'], components)
                    if body.get('required'):
                        required.append('body')
                name = operation['operationId']
                self.operations[name] = (method.upper(), path, params, keys[(method.upper(), path)])
                self._tools.append({'type': 'function', 'function': {'name': name, 'description': operation['summary'],
                    'parameters': {'type': 'object', 'properties': properties, 'required': required, 'additionalProperties': False}}})

    async def setup(self, question):
        return {}

    def system(self):
        return COMMON + MODE_RULES[self.mode]

    def tools(self):
        return self._tools

    async def call(self, name, arguments):
        if name not in self.operations:
            return compact({'error': 'unknown function'}), None
        method, template, params, key = self.operations[name]
        path, query = template, {}
        for parameter, location in params:
            if parameter not in arguments:
                continue
            if location == 'path':
                path = path.replace('{' + parameter + '}', quote(str(arguments[parameter]), safe=''))
            else:
                query[parameter] = query_value(arguments[parameter])
        if '{' in path:
            return compact({'error': 'missing path parameter'}), None
        status, body = await asyncio.to_thread(http, self.origin, method, path, query, arguments.get('body'))
        return compact({'status': status, 'body': body}), {'op': key, 'status': status, 'ok': 200 <= status < 300}


class SpecPrompt(SpecTools):
    mode = 'spec-prompt'

    def __init__(self, scale, spec, origin):
        self.scale, self.origin, self.spec = scale, origin, spec

    def system(self):
        return COMMON + MODE_RULES[self.mode] + '\n\nOpenAPI 명세:\n' + compact(self.spec)

    def tools(self):
        return [HTTP_TOOL]

    async def call(self, name, arguments):
        if name != 'http_request':
            return compact({'error': 'unknown function'}), None
        method, path = arguments.get('method'), arguments.get('path')
        if method not in ('GET', 'POST', 'PATCH', 'DELETE') or not isinstance(path, str) or not path.startswith('/'):
            return compact({'error': 'method and an absolute path are required'}), None
        path, _, inline = path.partition('?')
        query = dict(parse_qsl(inline))
        query.update({key: query_value(value) for key, value in (arguments.get('query') or {}).items()})
        if path.startswith('/__admin') or '..' in path:
            return compact({'status': 404, 'body': None}), None
        key = route_key(self.scale, method, path)
        status, body = await asyncio.to_thread(http, self.origin, method, path, query, arguments.get('body'))
        return compact({'status': status, 'body': body}), {'op': key, 'status': status, 'ok': 200 <= status < 300}


class A2API:
    mode = 'a2api'

    def __init__(self, app, ops, *, max_tool_bytes=16000, search_limit=5):
        self.app, self.ops = app, ops
        self.max_tool_bytes, self.search_limit = max_tool_bytes, search_limit
        self.session = None

    async def setup(self, question):
        self.session = ToolSession(self.app, CONTEXT, max_tool_bytes=self.max_tool_bytes, search_limit=self.search_limit)
        result = await self.session.auto(question)
        return {'strategy': result['strategy'], 'functions': len(self.session.tools()), 'hostCalls': self.session.stats}

    def system(self):
        return COMMON + MODE_RULES[self.mode]

    def tools(self):
        return self.session.tools()

    async def call(self, name, arguments):
        binding = None if name == SEARCH_NAME else self.session.binding(name)
        payload = await self.session.call(name, arguments)
        text = self.session.render(payload)
        if binding is None:
            return text, None
        ok = payload.get('status') == 'succeeded'
        status = payload.get('httpStatus', 200) if ok else payload.get('error', {}).get('status')
        # Input rejected before execution never reached the service.
        if payload.get('error', {}).get('code') == 'INVALID_INPUT' and 'status' not in payload:
            return text, {'op': self.ops.get(binding['id'], 'unknown'), 'status': 'rejected', 'ok': False, 'executed': False}
        return text, {'op': self.ops.get(binding['id'], 'unknown'), 'status': status, 'ok': ok}
