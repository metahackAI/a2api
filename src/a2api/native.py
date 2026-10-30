"""Explicit synchronous Python capabilities sharing the direct-call protocol."""

from __future__ import annotations

from dataclasses import dataclass
from functools import wraps
import inspect
import json
import re
from types import MappingProxyType
from typing import get_type_hints

from .conversion import CALL_PROFILE, _bundle
from .errors import A2APIError
from .function_schema import json_copy, type_schema
from .ir import ExecutionContext, freeze
from .openapi_schema import check_draft_schema
from .schema import validate_value
from .discovery_metadata import search_keywords


@dataclass(frozen=True)
class _Function:
    handler: object
    descriptor_json: str
    input_schema: object
    output_schema: object
    defaults_json: str
    inject_context: bool
    search_terms: tuple[str, ...] = ()


def _definition(function, identifier, effect, summary, input_schema, output_schema, keywords):
    original = inspect.unwrap(function)
    if (not (inspect.isfunction(original) or inspect.ismethod(original))
            or inspect.iscoroutinefunction(original) or inspect.isgeneratorfunction(original)
            or inspect.isasyncgenfunction(original)):
        raise A2APIError('UNSUPPORTED_FUNCTION', 'Register synchronous, non-generator Python functions or bound methods.')
    if (not isinstance(identifier, str) or not re.fullmatch(r'[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+', identifier)
            or effect != 'read'):
        raise A2APIError('INVALID_FUNCTION', 'Declare a dotted capability id and effect=read.')
    signature = inspect.signature(function)
    try:
        hints = get_type_hints(original, include_extras=True)
    except (NameError, TypeError, AttributeError, SyntaxError, RecursionError):
        raise A2APIError('UNSUPPORTED_TYPE_HINT', 'Function annotations must resolve in their defining module; use a resolved wrapper.') from None
    parameters, defaults, required, inject_context = {}, {}, [], False
    for name, parameter in signature.parameters.items():
        if parameter.kind not in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY):
            raise A2APIError('UNSUPPORTED_FUNCTION', 'Positional-only and variadic parameters require a named-argument wrapper.')
        if name == 'context':
            if (parameter.kind is not inspect.Parameter.KEYWORD_ONLY or hints.get(name) is not ExecutionContext
                    or parameter.default is not inspect.Parameter.empty):
                raise A2APIError('INVALID_FUNCTION', 'context must be a required keyword-only ExecutionContext parameter.')
            inject_context = True
            continue
        if hints.get(name) is ExecutionContext:
            raise A2APIError('INVALID_FUNCTION', 'ExecutionContext must use the reserved keyword-only context parameter.')
        parameters[name] = parameter
        if parameter.default is inspect.Parameter.empty:
            required.append(name)
        else:
            defaults[name] = json_copy(parameter.default, code='INVALID_FUNCTION', status=400)
    if input_schema is None:
        properties = {name: type_schema(hints.get(name)) for name in parameters}
        for name, default in defaults.items():
            properties[name] = {**properties[name], 'default': default}
        input_schema = {'type': 'object', 'properties': properties, 'required': required, 'additionalProperties': False}
    else:
        input_schema = json_copy(input_schema, code='INVALID_FUNCTION', status=400)
    if not isinstance(input_schema, dict):
        raise A2APIError('INVALID_FUNCTION', 'Input schema must be a JSON Schema object.')
    check_draft_schema(input_schema)
    if (input_schema.get('type') != 'object'
            or input_schema.get('additionalProperties') is not False
            or set(input_schema.get('properties', {})) != set(parameters)
            or not set(required).issubset(input_schema.get('required', []))
            or not set(input_schema.get('required', [])).issubset(parameters)):
        raise A2APIError('INVALID_FUNCTION', 'Input schema must be closed, declare all business parameters and require every parameter without a default.')
    if output_schema is None:
        output_schema = type_schema(hints.get('return'))
    else:
        output_schema = json_copy(output_schema, code='INVALID_FUNCTION', status=400)
    if not isinstance(output_schema, dict):
        raise A2APIError('INVALID_FUNCTION', 'Output schema must be a JSON Schema object.')
    for schema in (input_schema, output_schema):
        schema.setdefault('$schema', 'https://json-schema.org/draft/2020-12/schema')
        check_draft_schema(schema)
    for name, value in defaults.items():
        validate_value(_bundle(input_schema['properties'][name], input_schema), value, code='INVALID_FUNCTION', status=400)
    description = summary if summary is not None else (inspect.getdoc(function) or function.__name__).splitlines()[0]
    if not isinstance(description, str) or not description.strip():
        raise A2APIError('INVALID_FUNCTION', 'A nonempty summary or function docstring is required.')
    descriptor = {'id': identifier, 'version': '0.1.0', 'summary': description.strip(), 'effects': {'kind': 'read'},
                  'inputSchema': input_schema, 'outputSchema': output_schema}
    return _Function(function, json.dumps(descriptor, ensure_ascii=False, allow_nan=False),
                     freeze(input_schema), freeze(output_schema), json.dumps(defaults, ensure_ascii=False), inject_context,
                     search_keywords(keywords, code='INVALID_FUNCTION'))


def capability(*, id: str, effect: str, summary: str | None = None, input_schema: dict | None = None,
               output_schema: dict | None = None, keywords: list[str] | tuple[str, ...] | None = None):
    """Declare a read function explicitly. Decoration does not execute its body."""
    def register(function):
        definition = _definition(function, id, effect, summary, input_schema, output_schema, keywords)
        @wraps(function)
        def exported(*args, **kwargs):
            return function(*args, **kwargs)
        exported.__a2api_function__ = definition
        return exported
    return register


class Application:
    """Only explicitly supplied capability functions are available to invoke."""

    def __init__(self, functions):
        if not isinstance(functions, (list, tuple)) or not functions:
            raise A2APIError('INVALID_FUNCTION', 'Application needs a nonempty list of capability-decorated functions.')
        calls = {}
        for function in functions:
            definition = getattr(function, '__a2api_function__', None)
            if not isinstance(definition, _Function):
                raise A2APIError('INVALID_FUNCTION', 'Register functions explicitly with @capability before adding them.')
            identifier = json.loads(definition.descriptor_json)['id']
            if identifier in calls:
                raise A2APIError('INVALID_FUNCTION', 'Capability IDs must be unique within an application.')
            calls[identifier] = definition
        self._calls = MappingProxyType(calls)

    @property
    def profile(self):
        return CALL_PROFILE

    def _get(self, identifier):
        if not isinstance(identifier, str) or identifier not in self._calls:
            raise A2APIError('NOT_FOUND', 'This application does not expose the requested capability.', status=404)
        return self._calls[identifier]

    def describe(self, capability_id: str) -> dict:
        return json.loads(self._get(capability_id).descriptor_json)

    def descriptors(self) -> tuple[dict, ...]:
        """Host-side catalog snapshot; not the MCP tools/list payload."""
        return tuple(self.describe(identifier) for identifier in self._calls)

    def search_metadata(self, *, structured=False):
        if structured:
            return {identifier: {'terms': definition.search_terms, 'keywords': definition.search_terms,
                                 'aliases': (definition.handler.__name__,)}
                    for identifier, definition in self._calls.items()}
        return {identifier: definition.search_terms for identifier, definition in self._calls.items()}

    def invoke(self, capability_id: str, input: dict, *, context: ExecutionContext) -> dict:
        try:
            definition = self._get(capability_id)
            if not isinstance(context, ExecutionContext):
                raise A2APIError('UNAUTHENTICATED', 'A trusted host ExecutionContext is required.', status=401)
            if not isinstance(input, dict):
                raise A2APIError('INVALID_INPUT', 'Business input must be a JSON object.', status=422)
            arguments = json_copy(input, code='INVALID_INPUT', status=422)
            validate_value(definition.input_schema, arguments, code='INVALID_INPUT', status=422)
            defaults = json.loads(definition.defaults_json)
            arguments = {**defaults, **arguments}
            validate_value(definition.input_schema, arguments, code='INVALID_INPUT', status=422)
            if definition.inject_context:
                arguments['context'] = context
            try:
                data = definition.handler(**arguments)
            except A2APIError:
                raise
            except Exception:
                raise A2APIError('HANDLER_ERROR', 'Registered function failed.', status=500) from None
            if inspect.iscoroutine(data):
                data.close()
            data = json_copy(data, code='SCHEMA_MISMATCH', status=502)
            validate_value(definition.output_schema, data, code='SCHEMA_MISMATCH', status=502)
            return {'status': 'succeeded', 'data': data, 'completeness': {'complete': True, 'scope': 'single_api_response'}}
        except A2APIError as error:
            return {'status': 'failed', 'error': error.problem(), 'completeness': {'complete': False}}
        except RecursionError:
            return {'status': 'failed', 'error': A2APIError('SCHEMA_EVALUATION_FAILED',
                    'Schema evaluation exceeded the supported depth.', status=422).problem(), 'completeness': {'complete': False}}
