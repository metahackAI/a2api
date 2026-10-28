import copy
import unittest
from dataclasses import FrozenInstanceError

from a2api import A2APIError, Catalog, compile_contract
from a2api.contracts import parse_json
from a2api.sample import TOKENS, sample_manifest


class ContractTests(unittest.TestCase):
    def invalid(self, manifest):
        with self.assertRaises(A2APIError) as caught:
            compile_contract(manifest)
        self.assertEqual(caught.exception.code, "INVALID_CONTRACT")

    def test_sample_compiles_to_immutable_ir(self):
        manifest = sample_manifest()
        capability = compile_contract(manifest)
        manifest['title'] = 'changed'
        self.assertNotEqual(capability.title, 'changed')
        with self.assertRaises(FrozenInstanceError):
            capability.title = 'changed'
        with self.assertRaises(TypeError):
            capability.operations['new'] = None
        view = capability.describe()
        view['title'] = 'changed'
        self.assertNotEqual(capability.describe()['title'], 'changed')

    def test_forward_references_are_topologically_sorted(self):
        manifest = sample_manifest()
        manifest['binding']['steps'].reverse()
        self.assertEqual([s.id for s in compile_contract(manifest).steps], ['order', 'shipments'])

    def test_required_metadata_and_unknown_fields(self):
        for edit in (lambda m: m.pop('owner'), lambda m: m.update(unimplementedPolicy=True)):
            with self.subTest(edit=edit):
                manifest = sample_manifest()
                edit(manifest)
                self.invalid(manifest)

    def test_unknown_and_duplicate_operations(self):
        manifest = sample_manifest()
        manifest['binding']['steps'][0]['operationId'] = 'unknown'
        self.invalid(manifest)
        manifest = sample_manifest()
        manifest['operations'].append(copy.deepcopy(manifest['operations'][0]))
        self.invalid(manifest)

    def test_unknown_step_and_cycle(self):
        manifest = sample_manifest()
        manifest['binding']['steps'][0]['dependsOn'] = ['unknown']
        self.invalid(manifest)
        manifest = sample_manifest()
        manifest['binding']['steps'][0]['dependsOn'] = ['shipments']
        self.invalid(manifest)

    def test_missing_input_and_invalid_pointer(self):
        manifest = sample_manifest()
        manifest['binding']['steps'][0]['input'] = {}
        self.invalid(manifest)
        manifest = sample_manifest()
        manifest['binding']['steps'][0]['input']['orderId']['pointer'] = '/missing'
        self.invalid(manifest)
        manifest = sample_manifest()
        manifest['binding']['steps'][0]['input']['orderId']['pointer'] = '/bad~2escape'
        self.invalid(manifest)

    def test_semantic_id_mismatch(self):
        manifest = sample_manifest()
        manifest['operations'][1]['inputSchema']['properties']['shipmentId']['x-a2api-semanticType'] = 'sales.OrderId'
        self.invalid(manifest)

    def test_optional_source_cannot_satisfy_required_mapping(self):
        manifest = sample_manifest()
        manifest['operations'][0]['outputSchema']['required'].remove('shipmentIds')
        self.invalid(manifest)

    def test_unsupported_schema_features_and_formats_fail_closed(self):
        for key, value in [('$ref', 'https://example.com/remote.json'), ('format', 'unimplemented'), ('pattern', '^x')]:
            manifest = sample_manifest()
            manifest['inputSchema']['properties']['orderId'][key] = value
            with self.subTest(keyword=key):
                self.invalid(manifest)

    def test_budget_and_fanout_are_checked_before_execution(self):
        manifest = sample_manifest()
        manifest['execution']['maxBackendCalls'] = 2
        self.invalid(manifest)
        manifest = sample_manifest()
        manifest['binding']['steps'][1]['maxItems'] = 1
        self.invalid(manifest)

    def test_activation_requires_read_only_review_and_checks(self):
        edits = [lambda m: m.update(lifecycle='draft'),
                 lambda m: m['provenance'].update(reviewState='unreviewed'),
                 lambda m: m['effects'].update(kind='write'),
                 lambda m: m['operations'][0]['effects'].update(externalWrites=True),
                 lambda m: m['binding']['steps'][0].update(checks=[])]
        for edit in edits:
            manifest = sample_manifest()
            edit(manifest)
            with self.subTest(edit=edit):
                self.invalid(manifest)

    def test_output_projection_cannot_leak_internal_fields(self):
        manifest = sample_manifest()
        manifest['binding']['steps'][1]['select'].append('ownerId')
        self.invalid(manifest)

    def test_sample_is_hidden_without_explicit_opt_in(self):
        capability = compile_contract(sample_manifest())
        self.assertEqual(Catalog([capability]).discover('', TOKENS['demo-alice'])['capabilities'], [])
        manifest = sample_manifest()
        manifest['enabled'] = False
        self.assertEqual(Catalog([compile_contract(manifest)], allow_samples=True).discover('', TOKENS['demo-alice'])['capabilities'], [])

    def test_duplicate_json_keys_and_nonfinite_numbers(self):
        for text in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_json(text)


if __name__ == '__main__':
    unittest.main()
