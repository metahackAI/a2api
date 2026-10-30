"""Output hints stay bounded, source-derived and separate from input schemas."""

import unittest

from a2api import Application, ExecutionContext, ToolSession, capability
from a2api.tool_description import output_hint


class OutputHintTests(unittest.TestCase):
    def test_local_refs_optional_null_and_arrays_without_values_or_descriptions(self):
        schema = {'$ref': '#/$defs/result', '$defs': {'result': {'type': 'object',
            'properties': {'name': {'type': 'string', 'description': 'do not expose this', 'example': 'private value'},
                           'note': {'$ref': '#/$defs/note'}}, 'required': ['name']},
            'note': {'type': ['string', 'null']}}}
        hint = output_hint(schema)
        self.assertIn('"name":string (required)', hint)
        self.assertIn('"note":string|null (optional)', hint)
        self.assertNotIn('private', hint)
        self.assertNotIn('do not expose', hint)
        array = {'type': 'array', 'items': {'type': 'object', 'properties': {'name': {'type': 'string'}}}}
        self.assertIn('Returns array items fields:', output_hint(array))

    def test_composites_cycles_and_long_fields_are_not_guessed_or_expanded(self):
        self.assertEqual(output_hint({'oneOf': [{'type': 'object', 'properties': {'hidden': {}}}]}), 'Returns JSON.')
        self.assertEqual(output_hint({'$ref': '#/$defs/self', '$defs': {'self': {'$ref': '#/$defs/self'}}}), 'Returns JSON.')
        schema = {'type': 'object', 'properties': {str(i): {'type': 'string'} for i in range(100)}}
        hint = output_hint(schema)
        self.assertIn('+94 other fields', hint)
        self.assertNotIn('"99"', hint)
        self.assertLess(len(hint), 1024)
        long = output_hint({'type': 'object', 'properties': {'x'*2000: {'type': 'string'}}})
        self.assertNotIn('x'*80, long)
        self.assertLess(len(long), 1024)


class OutputToolTests(unittest.IsolatedAsyncioTestCase):
    async def test_only_selected_function_gets_hint_and_exact_input_is_preserved(self):
        schema = {'type': 'object', 'properties': {'default_branch': {'type': 'string'}}, 'required': ['default_branch']}
        @capability(id='repo.get', effect='read', output_schema=schema)
        def get(name: str) -> dict:return {'default_branch': name}
        app = Application([get])
        host = ToolSession(app, ExecutionContext('alice', 'tenant', frozenset()))
        self.assertNotIn('default_branch', str(host.tools()))
        await host.prime(['repo.get'])
        tool = host.tools(include_search=False)[0]['function']
        self.assertIn('"default_branch":string (required)', tool['description'])
        self.assertEqual(tool['parameters'], app.describe('repo.get')['inputSchema'])
        self.assertNotIn('outputSchema', tool)
        self.assertEqual((await host.call(tool['name'], {'name': 'actual'}))['data'], {'default_branch': 'actual'})
