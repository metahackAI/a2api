"""Public wire examples and real exchanges against the packaged protocol."""

import importlib.util
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator
from a2api import Application, ExecutionContext, PROTOCOL_PROFILE, capability, protocol_schema
from a2api.api import input_schema
from a2api.mcp_schemas import output_schemas


class ProtocolTests(unittest.TestCase):
    def test_published_examples_and_negative_packets(self):
        document = protocol_schema()
        Draft202012Validator.check_schema(document)
        examples = json.loads(Path(__file__).with_name('fixtures').joinpath('call-protocol.json').read_text())
        for component, cases in examples.items():
            validator = Draft202012Validator({'$defs': document['$defs'], '$ref': '#/$defs/' + component})
            for expected, values in [(True, cases['valid']), (False, cases['invalid'])]:
                for packet in values:
                    with self.subTest(component=component, packet=packet):
                        self.assertEqual(validator.is_valid(packet), expected)
                        self.assertEqual(Draft202012Validator(protocol_schema(component)).is_valid(packet), expected)

    def test_transport_helpers_share_the_canonical_wire_and_isolate_mutations(self):
        self.assertEqual(PROTOCOL_PROFILE, 'a2api-call/0.1')
        for method in ('discover', 'describe', 'invoke'):
            self.assertEqual(input_schema(method), protocol_schema(method + '_request'))
            self.assertEqual(output_schemas()[method], protocol_schema(method + '_response'))
        changed = protocol_schema('invoke_request')
        changed['required'].clear()
        self.assertIn('catalogVersion', protocol_schema('invoke_request')['required'])
        with self.assertRaises(ValueError):protocol_schema('not_a_component')


@unittest.skipUnless(importlib.util.find_spec('mcp'), 'Install a2api[mcp]')
class ProtocolExchangeTests(unittest.IsolatedAsyncioTestCase):
    async def test_actual_mcp_success_business_failure_and_preflight_error(self):
        from mcp import Client
        from a2api.mcp_bridge import create_mcp_server
        calls = []
        @capability(id='sample.echo', effect='read')
        def echo(value: str) -> str:
            calls.append(value)
            return value
        server = create_mcp_server(Application([echo]), ExecutionContext('alice', 'test', frozenset()))
        async with Client(server, read_timeout_seconds=10) as client:
            async def exchange(method, args):
                result = await client.call_tool('a2api.' + method, args)
                Draft202012Validator(protocol_schema(method + '_response')).validate(result.structured_content)
                return result.structured_content
            found = await exchange('discover', {})
            descriptor = (await exchange('describe', {'id':'sample.echo','version':'0.1.0'}))['capability']
            Draft202012Validator(protocol_schema('descriptor')).validate(descriptor)
            request = {'id':'sample.echo','version':'0.1.0','catalogVersion':found['catalogVersion'],'input':{'value':'ok'}}
            success = await exchange('invoke', request)
            Draft202012Validator(descriptor['outputSchema']).validate(success['data'])
            self.assertEqual(success['data'], 'ok')
            failure = await exchange('invoke', {**request, 'input':{'value':4}})
            self.assertEqual(failure['error']['code'], 'INVALID_INPUT')
            preflight = await exchange('invoke', {**request, 'catalogVersion':'stale'})
            self.assertEqual(set(preflight), {'error'})
            self.assertEqual(preflight['error']['code'], 'CONTRACT_DRIFT')
            self.assertEqual(calls, ['ok'])
