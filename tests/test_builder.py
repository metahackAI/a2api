"""Review decisions, source pins, deterministic builds and real HTTP projections."""

import copy
from contextlib import ExitStack, redirect_stdout, redirect_stderr
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from a2api import A2APIError, Catalog, HTTPDeployment, build_contracts, load_build, source_digest, write_build
from a2api.__main__ import main
from a2api.importers import OpenAPIImporter, write_import
from a2api.review_demo import sample_built_runtime, sample_importer, sample_review
from a2api.sample import BACKEND_TOKEN, TOKENS, create_backend, running, sample_runtime


class BuilderTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.imports = self.directory / 'imports'
        self.review = sample_review()
        write_import(sample_importer(), self.imports)

    def build(self, review=None):
        return build_contracts(self.imports, self.review if review is None else review)

    def assert_error(self, code, action):
        with self.assertRaises(A2APIError) as caught:
            action()
        self.assertEqual(caught.exception.code, code, caught.exception.problem())
        return caught.exception

    def reimport(self, source):
        importer = OpenAPIImporter(source, namespace='legacy_orders', source_name='order-shipping.openapi.json',
                                   methods={'GET', 'POST', 'HEAD'})
        records = {record.operation_id: record for record in importer.iter_operations()}
        self.imports = self.directory / ('imports-' + importer.source_hash)
        write_import(importer, self.imports)
        self.review['source']['sha256'] = importer.source_hash
        for item in self.review['operations']:
            record = records[item['source']['operationId']]
            item['source'].update(capabilityId=record.capability.id, digest=source_digest(record))

    def test_builds_real_executable_ir_with_traceable_review_and_sample_scope(self):
        with patch('a2api.sample.sample_manifest', side_effect=AssertionError('Builder must use OpenAPI and review settings')):
            result = self.build()
        capability = result.capabilities[0]
        manifest = capability.describe()
        self.assertTrue(capability.enabled)
        self.assertEqual(manifest['schemaProfile'], 'mvp')
        self.assertEqual(manifest['provenance']['reviewSha256'], result.review_sha256)
        self.assertEqual(manifest['provenance']['sourceSha256'], self.review['source']['sha256'])
        self.assertEqual(len(manifest['provenance']['sourceOperations']), 2)
        self.assertEqual(Catalog(list(result.capabilities)).discover('', TOKENS['demo-alice'])['capabilities'], [])
        self.assertEqual(len(Catalog(list(result.capabilities), allow_samples=True).discover('', TOKENS['demo-alice'])['capabilities']), 1)
        raw = json.loads((self.imports / 'contracts/legacy_orders.getorder.json').read_text())
        self.assertFalse(raw['enabled'])
        self.assertEqual(raw['schemaProfile'], 'openapi-draft')

    def test_review_and_imports_are_preserved_across_repeated_import_and_build(self):
        before = {path.name: path.read_bytes() for path in (self.imports / 'contracts').iterdir()}
        review_bytes = json.dumps(self.review)
        first = self.build()
        alternate = self.directory / 'regenerated'
        write_import(sample_importer(), alternate)
        second = build_contracts(alternate, self.review)
        self.assertEqual(first.capabilities[0].manifest_json, second.capabilities[0].manifest_json)
        self.assertEqual(json.dumps(self.review), review_bytes)
        self.assertEqual({path.name: path.read_bytes() for path in (self.imports / 'contracts').iterdir()}, before)
        self.review['capabilities'][0]['title'] = 'mutated later'
        self.assertNotEqual(first.capabilities[0].title, 'mutated later')

    def test_unreviewed_missing_reviewer_and_unassigned_owner_are_blocked(self):
        self.review['review']['state'] = 'unreviewed'
        self.assert_error('REVIEW_REQUIRED', self.build)
        self.review['review']['state'] = 'reviewed'
        self.review['review']['reviewedBy'] = ' '
        self.assert_error('REVIEW_REQUIRED', self.build)
        self.review['review']['reviewedBy'] = 'fixture-suite'
        self.review['capabilities'][0]['owner'] = 'unassigned'
        self.assert_error('REVIEW_REQUIRED', self.build)

    def test_unknown_review_fields_managed_flags_and_bad_dates_are_rejected(self):
        for mutate in (lambda review: review.update(unknown=True),
                       lambda review: review['capabilities'][0].update(enabled=True),
                       lambda review: review['operations'][0].update(httpMethod='POST'),
                       lambda review: review['review'].update(reviewedAt='yesterday')):
            with self.subTest(mutate=mutate):
                review = copy.deepcopy(self.review)
                mutate(review)
                self.assert_error('INVALID_REVIEW', lambda: self.build(review))

    def test_source_document_and_each_imported_operation_are_pinned(self):
        self.review['source']['sha256'] = '0' * 64
        self.assert_error('SOURCE_DRIFT', self.build)
        self.review = sample_review()
        path = self.imports / 'contracts/legacy_orders.getorder.json'
        contract = json.loads(path.read_text())
        contract['title'] = 'Changed after review'
        path.write_text(json.dumps(contract))
        self.assert_error('SOURCE_DRIFT', self.build)

    def test_bindings_are_pinned_and_cannot_inject_unrecognized_deployment_fields(self):
        path = self.imports / 'contracts/legacy_orders.getorder.http.json'
        binding = json.loads(path.read_text())
        binding['queryParameters']['extra'] = {'pointer': '/path/orderId', 'required': False, 'explode': True}
        path.write_text(json.dumps(binding))
        self.assert_error('SOURCE_DRIFT', self.build)
        binding['baseUrl'] = 'https://unreviewed.invalid'
        path.write_text(json.dumps(binding))
        self.assert_error('IMPORT_BUNDLE_INVALID', self.build)

    def test_missing_unsupported_or_duplicate_sources_and_unknown_operations_are_blocked(self):
        self.review['operations'][0]['source']['capabilityId'] = 'legacy_orders.missing'
        self.assert_error('IMPORT_NOT_BUILDABLE', self.build)
        self.review = sample_review()
        report = json.loads((self.imports / 'report.json').read_text())
        report['operations'].append(copy.deepcopy(report['operations'][0]))
        (self.imports / 'report.json').write_text(json.dumps(report))
        self.assert_error('IMPORT_NOT_BUILDABLE', self.build)

    def test_required_operation_fields_are_derived_from_source_and_never_retyped(self):
        result = self.build()
        operation = result.capabilities[0].operations['demo.getOrder']
        self.assertEqual(operation.input_schema['properties']['orderId']['type'], 'string')
        self.assertEqual(operation.input_schema['properties']['orderId']['minLength'], 1)
        self.assertEqual(operation.output_schema['properties']['shipmentIds']['maxItems'], 10)
        self.assertTrue(operation.output_schema['properties']['shipmentIds']['uniqueItems'])
        review = copy.deepcopy(self.review)
        review['operations'][0]['outputs']['orderId']['type'] = 'integer'
        self.assert_error('INVALID_REVIEW', lambda: self.build(review))

    def test_duplicate_review_ids_and_unreviewed_capability_references_fail(self):
        self.review['operations'].append(copy.deepcopy(self.review['operations'][0]))
        self.assert_error('INVALID_REVIEW', self.build)
        self.review = sample_review()
        self.review['capabilities'][0]['operationIds'].append('not.reviewed')
        self.assert_error('INVALID_REVIEW', self.build)

    def test_missing_required_input_overlap_and_optional_downgrade_are_rejected(self):
        self.review['operations'][0]['inputs'] = {}
        self.assert_error('UNSUPPORTED_PROJECTION', self.build)
        self.review = sample_review()
        self.review['operations'][0]['inputs']['other'] = {'pointer': '/path/orderId'}
        self.assert_error('UNSUPPORTED_PROJECTION', self.build)
        self.review = sample_review()
        self.review['operations'][0]['inputs']['orderId']['required'] = False
        self.assert_error('UNSUPPORTED_PROJECTION', self.build)

    def test_unsupported_pointer_constraints_and_whole_open_objects_fail_build(self):
        self.review['operations'][0]['outputs']['orderId']['pointer'] = '/result/missing'
        error = self.assert_error('UNSUPPORTED_PROJECTION', self.build)
        self.assertEqual(error.issues[0]['field'], 'orderId')
        self.review = sample_review()
        self.review['operations'][0]['outputs'] = {'entireOrder': {'pointer': '/result'}}
        self.assert_error('UNSUPPORTED_PROJECTION', self.build)
        self.review = sample_review()
        source = sample_importer().document
        source['components']['schemas']['Order']['properties']['orderId']['pattern'] = '^ORD-'
        self.reimport(source)
        self.assert_error('UNSUPPORTED_PROJECTION', self.build)

    def test_optional_source_field_cannot_be_promised_required(self):
        source = sample_importer().document
        source['components']['schemas']['Order']['properties']['note'] = {'type': 'string'}
        self.reimport(source)
        self.review['operations'][0]['outputs']['note'] = {'pointer': '/result/note', 'required': True}
        self.assert_error('UNSUPPORTED_PROJECTION', self.build)

    def test_semantic_annotations_and_authorization_checks_are_enforced(self):
        self.review['operations'][0]['semanticAnnotations'][0]['semanticType'] = 'unknown.Id'
        self.assert_error('INVALID_CONTRACT', self.build)
        self.review = sample_review()
        self.review['capabilities'][0]['binding']['steps'][0]['checks'] = []
        self.assert_error('INVALID_CONTRACT', self.build)

    def test_declaring_a_write_method_as_read_does_not_activate_it(self):
        source = sample_importer().document
        item = source['paths']['/orders/{orderId}']
        item['post'] = item.pop('get')
        self.reimport(source)
        self.assert_error('BUILD_WRITE_UNSUPPORTED', self.build)

    def test_build_reloads_deterministically_and_has_no_environment_credentials(self):
        built = self.build()
        output = self.directory / 'built'
        report = write_build(built, output)
        loaded = load_build(output)
        self.assertEqual(loaded.capabilities[0].manifest_json, built.capabilities[0].manifest_json)
        self.assertEqual(report['enabled'], 1)
        for path in output.rglob('*.json'):
            self.assertNotIn(BACKEND_TOKEN, path.read_text())
        before = (output / 'build.json').read_bytes()
        self.assert_error('OUTPUT_EXISTS', lambda: write_build(built, output))
        self.assertEqual((output / 'build.json').read_bytes(), before)

    def test_edited_built_contract_or_metadata_is_rejected_on_load(self):
        output = self.directory / 'built'
        report = write_build(self.build(), output)
        contract_path = output / report['contracts'][0]
        contract_path.write_bytes(contract_path.read_bytes() + b' ')
        self.assert_error('BUILD_DRIFT', lambda: load_build(output))
        output2 = self.directory / 'built2'
        write_build(self.build(), output2)
        metadata = json.loads((output2 / 'build.json').read_text())
        metadata['enabled'] = 9
        (output2 / 'build.json').write_text(json.dumps(metadata))
        self.assert_error('BUILD_DRIFT', lambda: load_build(output2))

    def test_artifact_paths_and_symlinks_cannot_escape_bundle(self):
        report = json.loads((self.imports / 'report.json').read_text())
        report['operations'][0]['contract'] = '../../outside.json'
        (self.imports / 'report.json').write_text(json.dumps(report))
        self.assert_error('IMPORT_BUNDLE_INVALID', self.build)
        output = self.directory / 'symlink-build'
        output.mkdir()
        (output / 'imports').symlink_to(self.imports, target_is_directory=True)
        (output / 'review.json').write_text(json.dumps(self.review))
        self.assert_error('IMPORT_BUNDLE_INVALID', lambda: load_build(output))

    def test_cli_build_is_reviewable_and_failure_creates_no_output(self):
        review_path = self.directory / 'review.json'
        review_path.write_text(json.dumps(self.review))
        output = self.directory / 'built'
        stream = io.StringIO()
        with redirect_stdout(stream):
            code = main(['build', '--imports', str(self.imports), '--review', str(review_path), '--output', str(output)])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(stream.getvalue())['enabled'], 1)
        self.review['review']['state'] = 'unreviewed'
        review_path.write_text(json.dumps(self.review))
        failed = self.directory / 'failed'
        stream = io.StringIO()
        with redirect_stderr(stream):
            code = main(['build', '--imports', str(self.imports), '--review', str(review_path), '--output', str(failed)])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(stream.getvalue())['code'], 'REVIEW_REQUIRED')
        self.assertFalse(failed.exists())


class BuiltRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        temporary = self.stack.enter_context(tempfile.TemporaryDirectory())
        imports = Path(temporary) / 'imports'
        write_import(sample_importer(), imports)
        self.built = build_contracts(imports, sample_review())

    def runtime(self, *, transform=None):
        backend = create_backend(transform=transform)
        origin = self.stack.enter_context(running(backend))
        return sample_built_runtime(self.built, origin), backend, origin

    def invoke(self, runtime, order='ORD-1001', user='alice'):
        return runtime.invoke('order.shipping_status', '0.1.0', runtime.catalog.version,
                              {'orderId': order}, TOKENS['demo-' + user])

    def test_generated_and_original_contracts_return_same_business_data(self):
        runtime, backend, origin = self.runtime()
        original = sample_runtime(origin)
        for order in ('ORD-1001', 'ORD-1002'):
            self.assertEqual(self.invoke(runtime, order)['data'], self.invoke(original, order)['data'])
        self.assertEqual(self.invoke(runtime)['stats']['backendCalls'], 3)

    def test_undeclared_private_source_fields_are_projected_out_before_agent_result(self):
        def transform(path, payload):
            return 200, {**payload, 'privateMemo': 'hidden-value'}
        runtime, backend, _ = self.runtime(transform=transform)
        result = self.invoke(runtime)
        self.assertEqual(result['status'], 'succeeded', result)
        for text in ('hidden-value', 'privateMemo', 'ownerId', 'tenantId'):
            self.assertNotIn(text, json.dumps(result))
        self.assertEqual(len(backend.sample_requests), 3)

    def test_source_schema_and_identity_relationship_checks_still_apply(self):
        for edit, code in ((lambda path, value: value.update(orderId='wrong'), 'CONTRACT_DRIFT'),
                           (lambda path, value: value.update(ownerId='foreign'), 'PERMISSION_DENIED'),
                           (lambda path, value: value.update(tenantId='foreign'), 'PERMISSION_DENIED'),
                           (lambda path, value: value.update(orderState=123), 'SCHEMA_MISMATCH')):
            def transform(path, value):
                edit(path, value)
                return 200, value
            runtime, backend, _ = self.runtime(transform=transform)
            result = self.invoke(runtime)
            self.assertEqual(result['error']['code'], code, result)
            self.assertEqual(len(backend.sample_requests), 1)
            self.assertNotIn('data', result)

    def test_foreign_orders_scopes_and_missing_resources_are_rejected(self):
        runtime, backend, _ = self.runtime()
        for order in ('ORD-2001', 'ORD-1003'):
            self.assertEqual(self.invoke(runtime, order)['error']['code'], 'PERMISSION_DENIED')
        self.assertEqual(self.invoke(runtime, 'missing')['error']['code'], 'RESOURCE_NOT_FOUND')
        self.assertEqual(runtime.discover('', TOKENS['demo-limited'])['capabilities'], [])
        with self.assertRaises(A2APIError):
            self.invoke(runtime, user='limited')
        self.assertEqual(self.invoke(runtime, 'ORD-2001', 'bob')['status'], 'succeeded')

    def test_deployment_is_host_owned_and_missing_bindings_fail(self):
        with self.assertRaises(A2APIError):
            self.built.runtime({}, allow_samples=True)
        runtime, backend, _ = self.runtime()
        with self.assertRaises(A2APIError):
            runtime.invoke('order.shipping_status', '0.1.0', runtime.catalog.version,
                           {'orderId': 'ORD-1001', 'baseUrl': 'https://untrusted.invalid'}, TOKENS['demo-alice'])
        self.assertEqual(backend.sample_requests, [])
