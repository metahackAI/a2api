"""Static dependency impacts, selective conversion and retained capability approvals."""

import copy
from dataclasses import replace
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from contextlib import ExitStack, redirect_stdout
from unittest.mock import patch

from a2api import (A2APIError, build_contracts, dependency_index, diff_openapi, load_build,
                   regenerate, write_build)
from a2api.__main__ import main
from a2api.importers import OpenAPIImporter, write_import
from a2api.ir import freeze, thaw
from a2api.openapi_dependencies import diff_indices, operation_key
from a2api.review_demo import sample_built_runtime
from a2api.sample import TOKENS, create_backend, running

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'src/a2api/sample/order-shipping.incremental.openapi.json'
REVIEW = ROOT / 'src/a2api/sample/order-shipping.incremental.review.json'


class IncrementalTests(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.directory = Path(self.stack.enter_context(tempfile.TemporaryDirectory()))
        self.importer = OpenAPIImporter.from_file(SOURCE, namespace='legacy_orders')
        self.document = copy.deepcopy(self.importer.document)
        self.imports = self.directory / 'imports'
        write_import(self.importer, self.imports)
        self.base = build_contracts(self.imports, REVIEW)
        self.review_bytes = REVIEW.read_bytes()
        self.serial = 0

    def source(self, document=None):
        self.serial += 1
        path = self.directory / f'updated-{self.serial}.json'
        path.write_text(json.dumps(self.document if document is None else document, ensure_ascii=False))
        return path

    def shipment_change(self):
        self.document['components']['schemas']['Shipment']['properties']['status']['enum'].append('returned')

    def states(self, result):
        return {state['id']: state['state'] for state in result.review_status}

    def assert_error(self, code, action):
        with self.assertRaises(A2APIError) as caught:
            action()
        self.assertEqual(caught.exception.code, code, caught.exception.problem())

    def test_shipment_schema_changes_only_dependent_capability_and_converts_once(self):
        self.shipment_change()
        converted = []
        original = OpenAPIImporter._import

        def convert(importer, path, method, item, operation, opid, location):
            converted.append(opid)
            return original(importer, path, method, item, operation, opid, location)

        with patch.object(OpenAPIImporter, '_import', convert):
            updated = regenerate(self.base, self.source())
        self.assertEqual(converted, ['getShipment'])
        self.assertEqual(updated.summary()['convertedOperations'], 1)
        self.assertEqual(updated.summary()['reusedOperations'], 1)
        self.assertEqual(self.states(updated), {'order.shipping_status': 'requires_review', 'order.summary': 'reviewed'})
        old = {cap.id: cap for cap in self.base.capabilities}
        new = {cap.id: cap for cap in updated.capabilities}
        self.assertEqual(old['order.summary'].manifest_json, new['order.summary'].manifest_json)
        self.assertFalse(new['order.shipping_status'].enabled)
        self.assertEqual(updated.review_sha256, self.base.review_sha256)
        self.assertEqual(thaw(updated.review), thaw(self.base.review))
        self.assertEqual(REVIEW.read_bytes(), self.review_bytes)

    def test_unrelated_component_and_document_metadata_require_no_review_or_conversion(self):
        self.document['components']['schemas']['Unrelated'] = {'type': 'integer', 'minimum': 1}
        self.document['info'].update(title='Documentation changed', version='2026-11-01')
        self.document['tags'] = [{'name': 'Unused', 'description': 'Documentation only'}]
        with patch.object(OpenAPIImporter, '_import', side_effect=AssertionError('Stable operations must not be converted')):
            updated = regenerate(self.base, self.source())
        self.assertEqual(updated.summary()['convertedOperations'], 0)
        self.assertEqual(updated.summary()['requiresReview'], 0)
        self.assertNotEqual(updated.summary()['sourceSha256'], self.base.summary()['sourceSha256'])
        self.assertEqual([c.manifest_json for c in self.base.capabilities], [c.manifest_json for c in updated.capabilities])

    def test_formatting_and_key_order_are_not_operation_changes(self):
        path = self.directory / 'reformatted.json'
        path.write_text(json.dumps(self.document, sort_keys=True, indent=4))
        updated = regenerate(self.base, path)
        self.assertEqual(updated.summary()['convertedOperations'], 0)
        self.assertEqual(updated.summary()['requiresReview'], 0)

    def test_transitive_shared_schema_invalidates_both_operations(self):
        self.document['components']['schemas']['PrincipalId']['minLength'] = 2
        updated = regenerate(self.base, self.source())
        self.assertEqual(updated.summary()['convertedOperations'], 2)
        self.assertEqual(updated.summary()['requiresReview'], 2)
        for operation in updated.change_report['operations']:
            self.assertIn('/components/schemas/PrincipalId', [reason['pointer'] for reason in operation['reasons']])

    def test_operation_request_change_is_local_and_propagates_to_consuming_capabilities(self):
        self.document['paths']['/orders/{orderId}']['get']['parameters'].append(
            {'name': 'expand', 'in': 'query', 'schema': {'type': 'boolean'}})
        updated = regenerate(self.base, self.source())
        self.assertEqual(updated.summary()['convertedOperations'], 1)
        self.assertEqual(updated.summary()['requiresReview'], 2)

    def test_removed_operation_disables_dependents_and_drops_its_draft(self):
        del self.document['paths']['/shipments/{shipmentId}']
        updated = regenerate(self.base, self.source())
        self.assertEqual(updated.summary()['convertedOperations'], 0)
        self.assertEqual(self.states(updated)['order.shipping_status'], 'requires_review')
        self.assertEqual([record.operation_id for record in updated.candidates], ['getOrder'])

    def test_removed_reference_or_unsupported_schema_never_reuses_active_capability(self):
        del self.document['components']['schemas']['Shipment']
        updated = regenerate(self.base, self.source())
        self.assertEqual(self.states(updated)['order.summary'], 'reviewed')
        self.assertEqual(self.states(updated)['order.shipping_status'], 'requires_review')
        changed = next(record for record in updated.candidates if record.operation_id == 'getShipment')
        self.assertEqual(changed.status, 'unsupported')

    def test_new_operations_are_drafts_and_do_not_create_enabled_capabilities(self):
        self.document['paths']['/health'] = {'get': {'operationId': 'getHealth', 'responses': {'200': {
            'content': {'application/json': {'schema': {'type': 'boolean'}}}}}}}
        updated = regenerate(self.base, self.source())
        self.assertEqual(updated.summary()['convertedOperations'], 1)
        self.assertEqual(updated.summary()['requiresReview'], 0)
        self.assertEqual(len(updated.capabilities), 2)
        record = next(record for record in updated.candidates if record.operation_id == 'getHealth')
        self.assertFalse(record.capability.enabled)

    def test_pending_review_survives_further_updates_and_reversion(self):
        self.shipment_change()
        first = regenerate(self.base, self.source())
        self.document['info']['description'] = 'Unrelated follow-up'
        second = regenerate(first, self.source())
        self.assertEqual(second.summary()['convertedOperations'], 0)
        self.assertEqual(second.summary()['requiresReview'], 1)
        reverted = self.directory / 'reverted.json'
        reverted.write_bytes(SOURCE.read_bytes())
        third = regenerate(second, reverted)
        self.assertEqual(third.summary()['requiresReview'], 1)
        self.assertEqual(third.summary()['sourceSha256'], self.base.review['source']['sha256'])
        self.assertEqual(self.states(third)['order.summary'], 'reviewed')
        self.assertEqual(third.summary()['generation'], 3)

    def test_roundtrip_preserves_original_review_and_reuses_contract_bytes(self):
        baseline_dir = self.directory / 'base'
        write_build(self.base, baseline_dir)
        before_review = (baseline_dir / 'review.json').read_bytes()
        before_contract = (baseline_dir / 'contracts/order.summary.0.1.0.json').read_bytes()
        self.shipment_change()
        updated = regenerate(baseline_dir, self.source())
        directory = self.directory / 'updated'
        write_build(updated, directory)
        loaded = load_build(directory)
        self.assertEqual(loaded.summary(), updated.summary())
        self.assertEqual((directory / 'review.json').read_bytes(), before_review)
        self.assertEqual((baseline_dir / 'review.json').read_bytes(), before_review)
        self.assertEqual((directory / 'contracts/order.summary.0.1.0.json').read_bytes(), before_contract)
        self.assertEqual(self.states(loaded), self.states(updated))
        self.assert_error('OUTPUT_EXISTS', lambda: write_build(updated, directory))

    def test_catalog_keeps_unaffected_capability_executable_and_hides_pending(self):
        self.shipment_change()
        updated = regenerate(self.base, self.source())
        backend = create_backend()
        origin = self.stack.enter_context(running(backend))
        runtime = sample_built_runtime(updated, origin)
        found = runtime.discover('', TOKENS['demo-alice'])
        self.assertEqual([item['id'] for item in found['capabilities']], ['order.summary'])
        result = runtime.invoke('order.summary', '0.1.0', runtime.catalog.version, {'orderId': 'ORD-1001'}, TOKENS['demo-alice'])
        self.assertEqual(result['status'], 'succeeded', result)
        self.assertEqual(result['stats']['backendCalls'], 1)
        with self.assertRaises(A2APIError):
            runtime.invoke('order.shipping_status', '0.1.0', runtime.catalog.version, {'orderId': 'ORD-1001'}, TOKENS['demo-alice'])
        self.assertEqual(backend.sample_requests, ['/orders/ORD-1001'])

    def test_all_affected_capabilities_need_no_live_deployment_and_remain_hidden(self):
        self.document['components']['schemas']['PrincipalId']['minLength'] = 2
        updated = regenerate(self.base, self.source())
        runtime = updated.runtime({}, allow_samples=True)
        self.assertEqual(runtime.discover('', TOKENS['demo-alice'])['capabilities'], [])
        self.assertEqual(updated.summary()['enabled'], 0)

    def test_dependency_snapshots_and_review_flags_cannot_be_edited_on_load(self):
        self.shipment_change()
        updated = regenerate(self.base, self.source())
        for filename in ('dependencies.json', 'history/0001.json', 'review-status.json', 'review.json'):
            output = self.directory / ('tampered-' + str(len(list(self.directory.iterdir()))))
            write_build(updated, output)
            path = output / filename
            path.write_bytes(path.read_bytes() + b' ')
            with self.assertRaises(A2APIError):
                load_build(output)

    def test_legacy_build_needs_matching_baseline_source_without_changing_old_review(self):
        legacy = replace(self.base, source_snapshot=None, source_dependencies=None,
                         import_report=freeze({key: value for key, value in thaw(self.base.import_report).items()
                                               if key not in {'sourceSnapshot', 'dependencyIndex'}}))
        directory = self.directory / 'legacy'
        write_build(legacy, directory)
        self.shipment_change()
        source = self.source()
        self.assert_error('DEPENDENCY_SNAPSHOT_MISSING', lambda: regenerate(directory, source))
        updated = regenerate(directory, source, baseline_source=SOURCE)
        self.assertEqual(updated.review_sha256, legacy.review_sha256)
        self.assertEqual(updated.summary()['requiresReview'], 1)
        self.assert_error('SOURCE_DRIFT', lambda: regenerate(directory, source, baseline_source=source))

    def test_cli_diff_and_regenerate_report_only_affected_capability(self):
        self.shipment_change()
        source = self.source()
        stream = io.StringIO()
        with redirect_stdout(stream):
            code = main(['diff-openapi', '--before', str(SOURCE), '--after', str(source), '--review', str(REVIEW)])
        self.assertEqual(code, 0)
        diff = json.loads(stream.getvalue())
        self.assertEqual(diff['summary'], {'changed': 1, 'unchanged': 1})
        self.assertEqual({row['id']: row['state'] for row in diff['capabilities']},
                         {'order.summary': 'reviewed', 'order.shipping_status': 'requires_review'})
        baseline = self.directory / 'baseline'
        write_build(self.base, baseline)
        stream = io.StringIO()
        with redirect_stdout(stream):
            code = main(['regenerate', '--previous', str(baseline), '--source', str(source),
                         '--output', str(self.directory / 'output'), '--fail-on-review'])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(stream.getvalue())['requiresReview'], 1)
        self.assertTrue((self.directory / 'output/review-status.json').exists())


class DependencyGraphTests(unittest.TestCase):
    def index(self, document):
        return dependency_index(OpenAPIImporter(document, namespace='legacy_orders'))

    def fixture(self):
        return json.loads(SOURCE.read_text())

    def test_effective_security_and_server_inheritance_are_tracked(self):
        old = self.fixture()
        old['paths']['/orders/{orderId}']['get'].update(security=[], servers=[{'url': 'https://override.invalid'}])
        new = copy.deepcopy(old)
        new['components']['securitySchemes']['serviceBearer']['scheme'] = 'basic'
        new['servers'] = [{'url': 'https://changed.invalid'}]
        diff = diff_indices(self.index(old), self.index(new))
        statuses = {row['operationId']: row['status'] for row in diff['operations']}
        self.assertEqual(statuses, {'getOrder': 'unchanged', 'getShipment': 'changed'})

    def test_inherited_parameter_changes_do_not_invalidate_operation_overrides(self):
        old = self.fixture()
        path = old['paths']['/orders/{orderId}']
        old['components']['parameters'] = {'limit': {'name': 'limit', 'in': 'query', 'schema': {'type': 'integer', 'maximum': 100}}}
        path['parameters'] = [{'$ref': '#/components/parameters/limit'}]
        path['get']['parameters'].append({'name': 'limit', 'in': 'query', 'schema': {'type': 'integer', 'maximum': 10}})
        new = copy.deepcopy(old)
        new['components']['parameters']['limit']['schema']['maximum'] = 200
        self.assertEqual(diff_indices(self.index(old), self.index(new))['summary'], {'unchanged': 2})

    def test_reference_role_is_not_inferred_from_a_component_name(self):
        old = self.fixture()
        old['components']['schemas']['Limit'] = {'type': 'integer', 'maximum': 10}
        old['components']['parameters'] = {'schema': {'name': 'limit', 'in': 'query', 'schema': {'$ref': '#/components/schemas/Limit'}}}
        old['paths']['/orders/{orderId}']['get']['parameters'].append({'$ref': '#/components/parameters/schema'})
        new = copy.deepcopy(old)
        new['components']['schemas']['Limit']['maximum'] = 20
        diff = diff_indices(self.index(old), self.index(new))
        self.assertEqual({row['operationId']: row['status'] for row in diff['operations']},
                         {'getOrder': 'changed', 'getShipment': 'unchanged'})

    def test_changed_reference_membership_is_explained_even_when_target_values_match(self):
        old = self.fixture()
        parameter = {'name': 'limit', 'in': 'query', 'schema': {'type': 'integer'}}
        old['components']['parameters'] = {'a': parameter, 'b': copy.deepcopy(parameter)}
        old['paths']['/orders/{orderId}']['parameters'] = [{'$ref': '#/components/parameters/a'}]
        new = copy.deepcopy(old)
        new['paths']['/orders/{orderId}']['parameters'] = [{'$ref': '#/components/parameters/b'}]
        diff = diff_indices(self.index(old), self.index(new))
        row = next(row for row in diff['operations'] if row['operationId'] == 'getOrder')
        self.assertEqual(row['status'], 'changed')
        self.assertEqual({reason['change'] for reason in row['reasons'] if reason['kind'] == 'reference'}, {'added', 'removed'})

    def test_literal_ref_properties_examples_and_defaults_do_not_fetch_references(self):
        document = self.fixture()
        schema = document['components']['schemas']['Order']
        schema['properties']['$ref'] = {'type': 'string', 'default': 'literal'}
        schema['example'] = {'$ref': 'https://must-not-fetch.invalid/schema'}
        with patch('urllib.request.urlopen', side_effect=AssertionError('No reference fetching')):
            index = self.index(document)
        self.assertTrue(all(not row['errors'] for row in index['operations'].values()))

    def test_recursive_references_terminate_and_shared_changes_propagate(self):
        old = self.fixture()
        old['components']['schemas']['PrincipalId'] = {'type': 'object', 'properties': {'parent': {'$ref': '#/components/schemas/PrincipalId'}}}
        new = copy.deepcopy(old)
        new['components']['schemas']['PrincipalId']['description'] = 'Changed recursive definition'
        self.assertEqual(diff_indices(self.index(old), self.index(new))['summary'], {'changed': 2})

    def test_duplicate_operation_ids_invalidate_existing_identity(self):
        old = self.fixture()
        new = copy.deepcopy(old)
        new['paths']['/duplicate'] = copy.deepcopy(new['paths']['/orders/{orderId}'])
        diff = diff_indices(self.index(old), self.index(new))
        row = next(row for row in diff['operations'] if row['key'] == 'GET /orders/{orderId}')
        self.assertEqual(row['status'], 'changed')
        self.assertIn('identity', [reason['kind'] for reason in row['reasons']])

    def test_full_github_spec_metadata_change_does_not_invalidate_any_operation(self):
        importer = OpenAPIImporter.from_file(ROOT / 'examples/github-openapi/api.github.com.json.gz', namespace='github')
        before = dependency_index(importer)
        document = importer.document
        document['info']['description'] = 'Documentation-only update'
        after = dependency_index(OpenAPIImporter(document, namespace='github'))
        self.assertEqual(diff_indices(before, after)['summary'], {'unchanged': 1254})

    def test_reference_limit_fingerprints_are_stable_across_process_hash_seeds(self):
        script = '''
import json
from pathlib import Path
from a2api import dependency_index
from a2api.importers import OpenAPIImporter
document=json.loads(Path('src/a2api/sample/order-shipping.incremental.openapi.json').read_text())
schemas=document['components']['schemas']
for index in range(4200):
    schemas['Extra'+str(index)]={'type':'object'}
schemas['Order']['allOf']=[{'$ref':'#/components/schemas/Extra'+str(index)} for index in range(4200)]
result=dependency_index(OpenAPIImporter(document,namespace='legacy_orders'))
assert 'DEPENDENCY_LIMIT' in result['operations']['GET /orders/{orderId}']['errors']
print(result['indexDigest'])
'''
        digests = []
        for seed in ('1', '2'):
            result = subprocess.run([sys.executable, '-c', script], cwd=ROOT,
                env={**os.environ, 'PYTHONPATH': str(ROOT / 'src'), 'PYTHONHASHSEED': seed},
                text=True, capture_output=True, check=True, timeout=15)
            digests.append(result.stdout.strip())
        self.assertEqual(digests[0], digests[1])
