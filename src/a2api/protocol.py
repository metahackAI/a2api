"""Transport-independent a2api-call/1.0 schemas, packaged for other clients."""

from copy import deepcopy
from functools import lru_cache
from importlib.resources import files
import json

from .errors import A2APIError

PROTOCOL_PROFILE = 'a2api-call/1.0'
METHODS = ('discover', 'describe', 'invoke')


@lru_cache(maxsize=1)
def _document():
    return json.loads(files('a2api').joinpath('schemas/call.schema.json').read_text(encoding='utf-8'))


def protocol_schema(component: str | None = None) -> dict:
    """Return the document, or a fresh standalone named component.

    Components: descriptor, problem, discover_request/response,
    describe_request/response and invoke_request/response. References between
    packaged components are expanded without remote resolution. Business
    schemas require separate validation; this checks the wire structure.
    """
    document = _document()
    if component is None:
        return deepcopy(document)
    if not isinstance(component, str) or component not in document['$defs']:
        raise ValueError('Unknown a2api-call schema component.')

    def expand(node):
        if isinstance(node, dict):
            if '$ref' in node:
                return expand(document['$defs'][node['$ref'].removeprefix('#/$defs/')])
            return {key: expand(value) for key, value in node.items()}
        if isinstance(node, list):
            return [expand(value) for value in node]
        return node

    return expand(document['$defs'][component])


def request_schema(method: str) -> dict:
    if method not in METHODS:
        raise A2APIError('NOT_FOUND', 'Unknown a2api method.', status=404)
    return protocol_schema(method + '_request')


def response_schemas() -> dict[str, dict]:
    return {method: protocol_schema(method + '_response') for method in METHODS}
