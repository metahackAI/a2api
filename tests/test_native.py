"""Typed Python calls, explicit registration and the same direct-call envelope."""

from __future__ import annotations

from contextlib import ExitStack
from dataclasses import dataclass
import inspect
import json
from pathlib import Path
import subprocess
import sys
from typing import Annotated, Any, Literal, NotRequired, Required, TypedDict
import unittest
from unittest.mock import patch

from jsonschema import Draft202012Validator

from a2api import A2APIError, Application, ExecutionContext, HTTPDeployment, capability, convert
from a2api.importers import OpenAPIImporter
from a2api.sample import BACKEND_TOKEN, TOKENS, create_backend, running

ROOT = Path(__file__).resolve().parents[1]
CALLER = ExecutionContext('alice', 'tenant-a', frozenset({'orders:read'}))


class OrderView(TypedDict):
    orderId: str
    orderState: Literal['created', 'processing', 'shipped', 'cancelled']
    shipmentIds: list[str]


class Delivery(TypedDict):
    status: Literal['pending', 'delivered']
    eta: str | None
    note: NotRequired[str]


class Partial(TypedDict, total=False):
    optional: int
    required: Required[str]


class Extended(Partial):
    another: bool
    omitted: NotRequired[str]


class Search(TypedDict):
    filters: Partial
    deliveries: list[Delivery]


class Recursive(TypedDict):
    child: Recursive


@dataclass
class Custom:
    value: str


class NativeTests(unittest.TestCase):
    def invoke(self, function, value=None, **options):
        app = Application([function])
        identifier = function.__a2api_function__
        return app.invoke(json.loads(identifier.descriptor_json)['id'], {} if value is None else value,
                          context=options.get('context', CALLER))

    def assert_error(self, code, action):
        with self.assertRaises(A2APIError) as caught:
            action()
        self.assertEqual(caught.exception.code, code, caught.exception.problem())

    def test_registration_does_not_call_function_and_application_exposes_only_registered_functions(self):
        calls = []
        def legacy(orderId: str, *, context: ExecutionContext) -> OrderView:
            """Look up one authorized order.

            Internal implementation details are not part of the summary.
            """
            calls.append(context)
            return {'orderId': orderId, 'orderState': 'shipped', 'shipmentIds': []}
        registered = capability(id='orders.lookup', effect='read')(legacy)
        self.assertEqual(calls, [])
        self.assertFalse(hasattr(legacy, '__a2api_function__'))
        app = Application([registered])
        view = app.describe('orders.lookup')
        self.assertEqual(set(view), {'id', 'version', 'summary', 'effects', 'inputSchema', 'outputSchema'})
        self.assertEqual(app.profile, 'a2api-call/1.0')
        self.assertEqual(view['summary'], 'Look up one authorized order.')
        self.assertEqual(inspect.signature(registered), inspect.signature(legacy))
        self.assertNotIn('context', json.dumps(view))
        with patch('pathlib.Path.write_text', side_effect=AssertionError('No artifacts')), \
                patch('a2api.builder.build_contracts', side_effect=AssertionError('No review/build')):
            result = app.invoke('orders.lookup', {'orderId': 'ORD-1001'}, context=CALLER)
        self.assertEqual(result['status'], 'succeeded', result)
        self.assertIs(calls[0], CALLER)
        self.assertEqual(result['completeness'], {'complete': True, 'scope': 'single_api_response'})
        self.assertEqual(app.invoke('other.lookup', {}, context=CALLER)['error']['code'], 'NOT_FOUND')
        self.assert_error('NOT_FOUND', lambda: app.describe('other.lookup'))
        self.assert_error('INVALID_FUNCTION', lambda: Application([legacy]))
        self.assert_error('INVALID_FUNCTION', lambda: Application([registered, registered]))

    def test_wrong_input_and_context_spoofing_never_execute_body(self):
        calls = []
        @capability(id='orders.lookup', effect='read')
        def lookup(orderId: str, *, context: ExecutionContext) -> str:
            calls.append(orderId)
            return orderId
        for value in ({}, {'orderId': 3}, {'orderId': '1', 'context': {'actor': 'bob'}},
                      {'orderId': '1', 'actor': 'bob'}, {'orderId': '\ud800'}, {'orderId': float('nan')}, []):
            result = Application([lookup]).invoke('orders.lookup', value, context=CALLER)
            self.assertEqual(result['error']['code'], 'INVALID_INPUT', result)
        result = self.invoke(lookup, {'orderId': '1'}, context={'actor': 'alice'})
        self.assertEqual(result['error']['code'], 'UNAUTHENTICATED')
        self.assertEqual(calls, [])

    def test_nested_typeddict_required_optional_nullable_literal_and_closed_fields(self):
        @capability(id='delivery.search', effect='read')
        def search(query: Search) -> list[Delivery]:
            return query['deliveries']
        app = Application([search])
        view = app.describe('delivery.search')
        for schema in (view['inputSchema'], view['outputSchema']):
            Draft202012Validator.check_schema(schema)
        good = {'query': {'filters': {'required': 'ok'}, 'deliveries': [{'status': 'pending', 'eta': None}]}}
        self.assertEqual(self.invoke(search, good)['data'], good['query']['deliveries'])
        for bad in [
            {'query': {'filters': {}, 'deliveries': []}},
            {'query': {'filters': {'required': 'ok'}, 'deliveries': [{'status': 'invented', 'eta': None}]}},
            {'query': {'filters': {'required': 'ok'}, 'deliveries': [{'status': 'pending'}]}},
            {'query': {'filters': {'required': 'ok', 'secret': 1}, 'deliveries': []}},
        ]:
            self.assertEqual(self.invoke(search, bad)['error']['code'], 'INVALID_INPUT')
        @capability(id='delivery.inherited', effect='read')
        def inherited(value: Extended) -> Extended:
            return value
        node = Application([inherited]).describe('delivery.inherited')['outputSchema']
        self.assertEqual(set(node['required']), {'required', 'another'})

    def test_defaults_are_applied_and_mutable_defaults_are_copied_per_call(self):
        @capability(id='values.list', effect='read')
        def values(label: str = 'default', *, items: list[int] = []) -> list[int]:
            items.append(1)
            return items
        app = Application([values])
        schema = app.describe('values.list')['inputSchema']
        self.assertEqual(schema['required'], [])
        self.assertEqual(schema['properties']['label']['default'], 'default')
        self.assertEqual(self.invoke(values)['data'], [1])
        self.assertEqual(self.invoke(values)['data'], [1])
        original = {'items': [2]}
        self.assertEqual(self.invoke(values, original)['data'], [2, 1])
        self.assertEqual(original, {'items': [2]})
        def bad_default(value: int = 'secret-default') -> int:
            return value
        self.assert_error('INVALID_FUNCTION', lambda: capability(id='values.bad', effect='read')(bad_default))

    def test_json_scalars_optional_union_dictionary_and_null_return(self):
        @capability(id='values.echo', effect='read')
        def echo(value: dict[str, int | bool | None], ratio: float = 1.5) -> dict[str, int | bool | None]:
            return value
        self.assertEqual(self.invoke(echo, {'value': {'count': 1, 'active': True, 'empty': None}})['status'], 'succeeded')
        self.assertEqual(self.invoke(echo, {'value': {1: 2}})['error']['code'], 'INVALID_INPUT')
        self.assertEqual(self.invoke(echo, {'value': {'count': float('inf')}})['error']['code'], 'INVALID_INPUT')
        @capability(id='values.none', effect='read')
        def empty() -> None:
            return None
        self.assertIsNone(self.invoke(empty)['data'])

    def test_invalid_return_shape_extra_private_fields_and_non_json_values_are_rejected(self):
        def returns_private(orderId: str) -> OrderView:
            return {'orderId': orderId, 'orderState': 'shipped', 'shipmentIds': [], 'secret': 'must-not-escape'}
        exported = capability(id='orders.private', effect='read')(returns_private)
        result = self.invoke(exported, {'orderId': '1'})
        self.assertEqual(result['error']['code'], 'SCHEMA_MISMATCH')
        self.assertNotIn('must-not-escape', json.dumps(result))
        self.assertNotIn('data', result)
        for value in [object(), float('nan'), (1, 2), {1: 'value'}]:
            def non_json() -> Any:
                return value
            exported = capability(id='values.invalid', effect='read', output_schema={})(non_json)
            self.assertEqual(self.invoke(exported)['error']['code'], 'SCHEMA_MISMATCH')

    def test_explicit_public_errors_and_unexpected_private_exceptions(self):
        @capability(id='orders.denied', effect='read')
        def denied(*, context: ExecutionContext) -> str:
            raise A2APIError('PERMISSION_DENIED', 'Unavailable to this caller.', status=403)
        self.assertEqual(self.invoke(denied)['error']['code'], 'PERMISSION_DENIED')
        @capability(id='orders.broken', effect='read')
        def broken() -> str:
            raise RuntimeError('secret token and stack trace')
        result = self.invoke(broken)
        self.assertEqual(result['error']['code'], 'HANDLER_ERROR')
        self.assertNotIn('secret', json.dumps(result))

    def test_manual_schema_fallback_keeps_untyped_legacy_functions_usable(self):
        def untyped(value):
            return {'value': value}
        schema = {'type': 'object', 'properties': {'value': {'type': 'string', 'minLength': 1}},
                  'required': ['value'], 'additionalProperties': False}
        exported = capability(id='legacy.untyped', effect='read', input_schema=schema, output_schema=schema)(untyped)
        schema['properties']['value']['minLength'] = 100
        self.assertEqual(self.invoke(exported, {'value': 'one'})['data'], {'value': 'one'})
        self.assertEqual(self.invoke(exported, {'value': ''})['error']['code'], 'INVALID_INPUT')
        view = Application([exported]).describe('legacy.untyped')
        view['inputSchema']['properties'].clear()
        self.assertIn('value', Application([exported]).describe('legacy.untyped')['inputSchema']['properties'])

    def test_manual_schema_fallback_preserves_function_signature_and_local_reference_rules(self):
        def untyped(value):
            return value
        for schema in [
            {'type': 'object', 'properties': {'wrong': {}}, 'required': [], 'additionalProperties': False},
            {'type': 'object', 'properties': {'value': {}}, 'required': [], 'additionalProperties': False},
            {'type': 'object', 'properties': {'value': {}}, 'required': ['value'], 'additionalProperties': True},
            {'type': 'object', 'properties': {'value': {}}, 'required': ['value', 'context'], 'additionalProperties': False},
        ]:
            self.assert_error('INVALID_FUNCTION', lambda: capability(id='legacy.invalid', effect='read', input_schema=schema, output_schema={})(untyped))
        schema = {'type': 'object', 'properties': {'value': {'$ref': '#/$defs/Nonempty'}}, 'required': ['value'],
                  'additionalProperties': False, '$defs': {'Nonempty': {'type': 'string', 'minLength': 1}}}
        exported = capability(id='legacy.ref', effect='read', input_schema=schema, output_schema={'type': 'string'})(untyped)
        self.assertEqual(self.invoke(exported, {'value': 'one'})['data'], 'one')
        with patch('urllib.request.urlopen', side_effect=AssertionError('No schema fetching')):
            self.assert_error('INVALID_CONTRACT', lambda: capability(id='legacy.external', effect='read',
                input_schema=schema, output_schema={'$ref': 'https://must-not-fetch.invalid/schema'})(untyped))

    def test_unsupported_hints_do_not_turn_into_permissive_schemas(self):
        def untyped(value):
            return value
        self.assert_error('UNSUPPORTED_TYPE_HINT', lambda: capability(id='values.untyped', effect='read')(untyped))
        for annotation in [Any, Custom, tuple[int, ...], Annotated[str, {'minLength': 1}], Recursive]:
            def identity(value):
                return value
            identity.__annotations__ = {'value': annotation, 'return': annotation}
            self.assert_error('UNSUPPORTED_TYPE_HINT', lambda: capability(id='values.unsupported', effect='read')(identity))

    def test_unsupported_signatures_effects_and_context_declarations(self):
        def positional(value: str, /) -> str:
            return value
        def variadic(*values: str) -> str:
            return str(values)
        def keyword_variadic(**values: str) -> str:
            return str(values)
        def generator() -> str:
            yield 'value'
        async def async_generator() -> str:
            yield 'value'
        for function in [positional, variadic, keyword_variadic, generator, async_generator]:
            self.assert_error('UNSUPPORTED_FUNCTION', lambda: capability(id='values.unsupported', effect='read')(function))
        def plain() -> str:
            return 'value'
        for effect in ['delete', 'unknown', None]:
            self.assert_error('INVALID_FUNCTION', lambda: capability(id='values.plain', effect=effect)(plain))
        def positional_context(context: ExecutionContext) -> str:
            return context.actor
        def wrong_name(*, caller: ExecutionContext) -> str:
            return caller.actor
        def wrong_type(*, context: str) -> str:
            return context
        for function in [positional_context, wrong_name, wrong_type]:
            self.assert_error('INVALID_FUNCTION', lambda: capability(id='values.context', effect='read')(function))

    def test_bound_method_is_an_explicit_callable_and_no_module_scan_occurs(self):
        class Service:
            def lookup(self, value: str, *, context: ExecutionContext) -> str:
                return context.actor + ':' + value
        registered = capability(id='service.lookup', effect='read')(Service().lookup)
        self.assertEqual(self.invoke(registered, {'value': '1'})['data'], 'alice:1')

    def test_synchronous_handler_returning_a_coroutine_does_not_run_or_leak_it(self):
        async def work():
            raise AssertionError('No implicit async execution')
        coroutine = work()
        @capability(id='values.coroutine', effect='read')
        def wrong_return() -> str:
            return coroutine
        result = self.invoke(wrong_return)
        self.assertEqual(result['error']['code'], 'SCHEMA_MISMATCH')
        self.assertIsNone(coroutine.cr_frame)

    def test_native_and_openapi_paths_share_descriptor_and_result_format(self):
        @capability(id='orders.lookup', effect='read')
        def lookup(orderId: str) -> OrderView:
            return {'orderId': orderId, 'orderState': 'shipped', 'shipmentIds': ['SHP-501', 'SHP-502']}
        native = Application([lookup])
        with ExitStack() as stack:
            origin = stack.enter_context(running(create_backend()))
            source = OpenAPIImporter.from_file(ROOT / 'src/a2api/sample/order-shipping.openapi.json', namespace='legacy')
            http = convert(source, operations={'getOrder': {'effect': 'read', 'select': ['orderId', 'orderState', 'shipmentIds']}},
                           deployment=HTTPDeployment(origin, credential_provider=lambda _: {'Authorization': 'Bearer ' + BACKEND_TOKEN}))
            self.assertEqual(set(native.describe('orders.lookup')), set(http.describe('legacy.getorder')))
            self.assertEqual(native.profile, http.profile)
            http_result = http.invoke('legacy.getorder', {'path': {'orderId': 'ORD-1001'}}, context=TOKENS['demo-alice'])
            native_result = native.invoke('orders.lookup', {'orderId': 'ORD-1001'}, context=CALLER)
            self.assertEqual(http_result, native_result)
            self.assertEqual(native.invoke('orders.lookup', {}, context=CALLER)['error']['code'],
                             http.invoke('legacy.getorder', {}, context=CALLER)['error']['code'])

    def test_legacy_wrapper_and_new_api_example_runs(self):
        result = subprocess.run([sys.executable, str(ROOT / 'examples/native-orders/register_and_invoke.py')],
                                cwd=ROOT, text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['order']['data']['orderId'], 'ORD-1001')
        self.assertIsNone(report['shipping']['data'][0]['estimatedArrival'])
        self.assertEqual(report['empty']['data'], [])
        self.assertNotIn('ownerId', result.stdout)
