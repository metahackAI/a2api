import copy
import gzip
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from jsonschema import Draft202012Validator

from a2api import A2APIError, Catalog, compile_contract, load_contract
from a2api.importers import OpenAPIImporter, load_openapi, write_import
from a2api.sample import TOKENS

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'examples/github-openapi/api.github.com.json.gz'


def specification(version='3.0.3'):
    return {
        'openapi': version, 'info': {'title': 'Inventory API', 'version': '2026-10'},
        'servers': [{'url': 'https://inventory.example/v1'}], 'security': [{'bearer': ['inventory:read']}],
        'components': {
            'parameters': {
                'id': {'name': 'id', 'in': 'path', 'required': True, 'schema': {'type': 'string'}},
                'limit': {'name': 'limit', 'in': 'query', 'schema': {'type': 'integer', 'minimum': 1, 'maximum': 100, 'default': 30}},
            },
            'schemas': {'Item': {'type': 'object', 'properties': {'id': {'type': 'string'}, 'name': {'type': 'string'}}, 'required': ['id']}},
        },
        'paths': {
            '/items/{id}': {
                'parameters': [{'$ref': '#/components/parameters/id'}],
                'get': {'operationId': 'items/get', 'summary': 'Get an item',
                        'parameters': [{'$ref': '#/components/parameters/limit'}],
                        'responses': {'200': {'description': 'OK', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/Item'}}}}}},
                'delete': {'operationId': 'items/delete', 'responses': {'204': {'description': 'Deleted'}}},
            }
        },
    }


def imported(document=None):
    return next(r for r in OpenAPIImporter(document or specification(), namespace='inventory').iter_operations() if r.method == 'get')


class OpenAPIImportTests(unittest.TestCase):
    def assert_unsupported(self, document, code):
        record = imported(document)
        self.assertEqual(record.status, 'unsupported', record.summary())
        self.assertEqual(record.diagnostics[0]['code'], code)
        self.assertIsNone(record.capability)
        return record

    def test_generates_real_disabled_capability_ir_with_provenance(self):
        record = imported()
        self.assertEqual(record.status, 'imported', record.summary())
        manifest = record.capability.describe()
        self.assertEqual(manifest['id'], 'inventory.items.get')
        self.assertFalse(record.capability.enabled)
        self.assertEqual(manifest['schemaProfile'], 'openapi-draft')
        self.assertEqual(manifest['effects']['kind'], 'unknown')
        self.assertEqual(manifest['provenance']['source']['security'], [{'bearer': ['inventory:read']}])
        self.assertEqual(manifest['provenance']['source']['servers'], [{'url': 'https://inventory.example/v1'}])
        self.assertEqual(manifest['provenance']['source']['pointer'], '/paths/~1items~1{id}/get')
        self.assertEqual(record.binding['pathParameters']['id'], '/path/id')
        self.assertEqual(record.binding['queryParameters']['limit']['pointer'], '/query/limit')
        self.assertEqual(Catalog([record.capability]).discover('', TOKENS['demo-alice'])['capabilities'], [])

    def test_import_profile_cannot_be_activated_by_flipping_review_flags(self):
        manifest = imported().capability.describe()
        manifest['enabled'] = True
        manifest['lifecycle'] = 'reviewed'
        manifest['provenance']['reviewState'] = 'reviewed'
        with self.assertRaises(A2APIError):
            compile_contract(manifest)

    def test_path_query_and_parameter_override_keep_constraints(self):
        source = specification()
        source['paths']['/items/{id}']['parameters'].append({'$ref': '#/components/parameters/limit'})
        source['paths']['/items/{id}']['get']['parameters'] = [
            {'name': 'limit', 'in': 'query', 'schema': {'type': 'integer', 'maximum': 50}},
            {'name': 'id', 'in': 'query', 'schema': {'type': 'string'}},
        ]
        schema = imported(source).capability.describe()['inputSchema']
        Draft202012Validator(schema).validate({'path': {'id': '123'}})
        Draft202012Validator(schema).validate({'path': {'id': '123'}, 'query': {'limit': 50, 'id': 'different'}})
        for invalid in ({'path': {'id': '123'}, 'query': {'limit': 51}}, {'path': {'id': '123'}, 'actor': 'bob'}):
            self.assertFalse(Draft202012Validator(schema).is_valid(invalid))

    def test_oas30_nullable_and_exclusive_bounds(self):
        source = specification()
        source['components']['schemas']['Item'] = {'type': 'number', 'nullable': True, 'minimum': 1, 'exclusiveMinimum': True}
        schema = imported(source).capability.describe()['outputSchema']
        validator = Draft202012Validator(schema)
        for value in (None, 2):
            validator.validate({'result': value})
        self.assertFalse(validator.is_valid({'result': 1}))
        self.assertFalse(validator.is_valid({'result': '2'}))

    def test_nullable_does_not_override_enum_or_invent_type(self):
        source = specification()
        source['components']['schemas']['Item'] = {'enum': ['known'], 'nullable': True}
        record = imported(source)
        self.assertEqual(record.status, 'imported', record.summary())
        self.assertIn('NULLABLE_WITHOUT_TYPE', [d['code'] for d in record.diagnostics])
        validator = Draft202012Validator(record.capability.describe()['outputSchema'])
        self.assertTrue(validator.is_valid({'result': 'known'}))
        self.assertFalse(validator.is_valid({'result': None}))

    def test_oas31_reference_siblings_unions_and_open_objects_are_preserved(self):
        source = specification('3.1.2')
        source['components']['schemas']['Item'] = {'oneOf': [{'type': 'string'}, {'type': 'integer'}]}
        record = imported(source)
        self.assertEqual(record.status, 'imported', record.summary())
        validator = Draft202012Validator(record.capability.describe()['outputSchema'])
        for value in ('name', 5):
            validator.validate({'result': value})
        self.assertFalse(validator.is_valid({'result': False}))
        source = specification('3.1.2')
        response = source['paths']['/items/{id}']['get']['responses']['200']['content']['application/json']
        response['schema']['properties'] = {'name': {'minLength': 3}}
        record = imported(source)
        validator = Draft202012Validator(record.capability.describe()['outputSchema'])
        self.assertTrue(validator.is_valid({'result': {'id': '1', 'name': 'long', 'extra': 42}}))
        self.assertFalse(validator.is_valid({'result': {'id': '1', 'name': 'x'}}))

    def test_oas30_reference_siblings_are_diagnosed_and_not_applied(self):
        source = specification()
        source['paths']['/items/{id}']['get']['responses']['200']['content']['application/json']['schema']['type'] = 'string'
        record = imported(source)
        self.assertIn('OAS30_REF_SIBLINGS', [d['code'] for d in record.diagnostics])
        Draft202012Validator(record.capability.describe()['outputSchema']).validate({'result': {'id': '1'}})

    def test_array_and_scalar_responses_are_wrapped_without_loss(self):
        for response in ({'type': 'array', 'items': {'$ref': '#/components/schemas/Item'}}, {'type': 'integer'}, True):
            source = specification('3.1.2')
            source['paths']['/items/{id}']['get']['responses']['200']['content']['application/json']['schema'] = response
            record = imported(source)
            self.assertEqual(record.status, 'imported', record.summary())
            self.assertEqual(record.capability.output_schema['type'], 'object')

    def test_recursive_local_schema_ref_is_bundled_without_expansion(self):
        source = specification('3.1.2')
        source['components']['schemas']['Item']['properties']['children'] = {'type': 'array', 'items': {'$ref': '#/components/schemas/Item'}}
        record = imported(source)
        self.assertEqual(record.status, 'imported', record.summary())
        schema = record.capability.describe()['outputSchema']
        self.assertEqual(len(schema['$defs']), 1)
        Draft202012Validator(schema).validate({'result': {'id': '1', 'children': [{'id': '2'}]}})

    def test_external_missing_and_scope_changing_refs_are_diagnostics(self):
        for reference, code in [('https://example.com/schema.json', 'EXTERNAL_REFERENCE'),
                                 ('file:///tmp/schema.json', 'EXTERNAL_REFERENCE'),
                                 ('#/components/schemas/missing', 'UNRESOLVED_REFERENCE')]:
            source = specification()
            source['components']['schemas']['Item'] = {'$ref': reference}
            with patch('urllib.request.urlopen', side_effect=AssertionError('Importer must not access the network')):
                self.assert_unsupported(source, code)
        source = specification('3.1.2')
        source['components']['schemas']['Item']['$id'] = 'https://example.com/other.json'
        self.assert_unsupported(source, 'UNSUPPORTED_SCHEMA_SCOPE')

    def test_unresolved_unused_components_do_not_break_valid_operations(self):
        source = specification()
        source['components']['schemas']['Unused'] = {'$ref': 'https://example.com/unused.json'}
        self.assertEqual(imported(source).status, 'imported')

    def test_malformed_or_recursive_parameter_schemas_are_diagnosed(self):
        for schema in ({'type': [1, {}]}, {'anyOf': {}}, {'type': 'array', 'items': {'$ref': '#/components/schemas/Recursive'}}):
            source = specification('3.1.2')
            source['components']['schemas']['Recursive'] = schema
            source['paths']['/items/{id}']['get']['parameters'][0] = {'name': 'q', 'in': 'query', 'schema': schema}
            self.assertEqual(imported(source).status, 'unsupported')
        source = specification()
        source['components']['schemas']['Item']['required'] = [{}]
        self.assert_unsupported(source, 'INVALID_SCHEMA')

    def test_required_write_only_response_needs_review(self):
        source = specification()
        source['components']['schemas']['Item']['properties']['id']['writeOnly'] = True
        self.assert_unsupported(source, 'WRITE_ONLY_RESPONSE_REQUIREMENT')

    def test_write_methods_are_inventoried_and_never_converted(self):
        records = list(OpenAPIImporter(specification()).iter_operations())
        self.assertEqual(len(records), 2)
        deleted = next(r for r in records if r.method == 'delete')
        self.assertEqual(deleted.status, 'skipped')
        self.assertIsNone(deleted.binding)

    def test_unsupported_serializations_and_missing_json_do_not_disappear(self):
        for edit, code in [
            (lambda op: op['parameters'].append({'name': 'token', 'in': 'header', 'schema': {'type': 'string'}}), 'UNSUPPORTED_PARAMETER_LOCATION'),
            (lambda op: op['parameters'].append({'name': 'filter', 'in': 'query', 'style': 'deepObject', 'schema': {'type': 'object'}}), 'UNSUPPORTED_PARAMETER_SCHEMA'),
            (lambda op: op['parameters'].append({'name': 'fields', 'in': 'query', 'style': 'pipeDelimited', 'schema': {'type': 'array', 'items': {'type': 'string'}}}), 'UNSUPPORTED_QUERY_SERIALIZATION'),
            (lambda op: op.update(requestBody={}), 'GET_REQUEST_BODY'),
            (lambda op: op.update(responses={'204': {'description': 'No content'}}), 'NO_JSON_200'),
        ]:
            source = specification()
            edit(source['paths']['/items/{id}']['get'])
            self.assert_unsupported(source, code)

    def test_query_string_array_union_and_boolean_values(self):
        source = specification('3.1.2')
        source['paths']['/items/{id}']['get']['parameters'].extend([
            {'name': 'labels', 'in': 'query', 'explode': False, 'schema': {'oneOf': [{'type': 'string'}, {'type': 'array', 'items': {'type': 'string'}}]}},
            {'name': 'active', 'in': 'query', 'required': True, 'schema': {'type': 'boolean'}},
        ])
        record = imported(source)
        self.assertEqual(record.status, 'imported', record.summary())
        schema = record.capability.describe()['inputSchema']
        self.assertIn('query', schema['required'])
        self.assertFalse(record.binding['queryParameters']['labels']['explode'])
        Draft202012Validator(schema).validate({'path': {'id': '1'}, 'query': {'active': True, 'labels': ['x', 'y']}})

    def test_duplicate_operation_ids_and_parameters_are_reported(self):
        source = specification()
        source['paths']['/other/{id}'] = copy.deepcopy(source['paths']['/items/{id}'])
        records = list(OpenAPIImporter(source).iter_operations())
        self.assertTrue(all(r.status == 'unsupported' and r.diagnostics[0]['code'] == 'DUPLICATE_OPERATION_ID' for r in records))
        source = specification()
        source['paths']['/items/{id}']['get']['parameters'].append({'$ref': '#/components/parameters/limit'})
        self.assert_unsupported(source, 'DUPLICATE_PARAMETER')

    def test_identifier_normalization_collisions_do_not_overwrite_files(self):
        source = specification()
        source['paths']['/other/{id}'] = copy.deepcopy(source['paths']['/items/{id}'])
        source['paths']['/other/{id}']['get']['operationId'] = 'items.get'
        del source['paths']['/other/{id}']['delete']
        records = [r for r in OpenAPIImporter(source).iter_operations() if r.capability]
        self.assertEqual(len({r.capability.id for r in records}), 2)

    def test_generated_files_roundtrip_and_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary) / 'generated'
            report = write_import(OpenAPIImporter(specification()), directory)
            self.assertEqual(report['summary']['operations'], 2)
            generated = next(r for r in report['operations'] if r['status'] == 'imported')
            self.assertFalse(load_contract(directory / generated['contract']).enabled)
            before = (directory / 'report.json').read_bytes()
            with self.assertRaises(A2APIError) as caught:
                write_import(OpenAPIImporter(specification()), directory)
            self.assertEqual(caught.exception.code, 'OUTPUT_EXISTS')
            self.assertEqual((directory / 'report.json').read_bytes(), before)

    def test_invalid_versions_structure_and_selections(self):
        for source in ({}, specification('2.0'), {**specification(), 'paths': []}, {**specification(), 'jsonSchemaDialect': 'custom'}):
            with self.subTest(source=source.get('openapi')), self.assertRaises(A2APIError):
                OpenAPIImporter(source)
        with self.assertRaises(A2APIError):
            list(OpenAPIImporter(specification()).iter_operations({'missing'}))

    def test_json_gzip_integrity_duplicate_keys_and_size_limit(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            plain = directory / 'api.json'
            compressed = directory / 'api.json.gz'
            data = json.dumps(specification()).encode()
            plain.write_bytes(data)
            compressed.write_bytes(gzip.compress(data, mtime=0))
            self.assertEqual(load_openapi(plain), load_openapi(compressed))
            plain.write_text('{"openapi":"3.0.3","openapi":"3.1.2"}')
            with self.assertRaises(A2APIError):
                load_openapi(plain)
            compressed.write_bytes(b'not gzip')
            with self.assertRaises(A2APIError):
                load_openapi(compressed)
            with patch('a2api.importers.openapi.MAX_DOCUMENT_BYTES', 16), self.assertRaises(A2APIError):
                load_openapi(plain)

    def test_import_is_deterministic_and_input_mutations_do_not_change_it(self):
        source = specification()
        importer = OpenAPIImporter(source)
        first = [r.capability.manifest_json for r in importer.iter_operations() if r.capability]
        source['info']['title'] = 'changed'
        second = [r.capability.manifest_json for r in importer.iter_operations() if r.capability]
        self.assertEqual(first, second)

    def test_cli_writes_report_and_strict_mode_reports_unsupported(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            source = specification()
            source['paths']['/items/{id}']['get']['responses'] = {'204': {'description': 'Empty'}}
            (directory / 'source.json').write_text(json.dumps(source))
            result = subprocess.run([sys.executable, '-m', 'a2api', 'import-openapi', str(directory / 'source.json'),
                                     '--output', str(directory / 'output'), '--strict'], capture_output=True, text=True,
                                    cwd=ROOT, env={**__import__('os').environ, 'PYTHONPATH': str(ROOT / 'src')})
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(json.loads(result.stdout)['statuses']['unsupported'], 1)
            self.assertTrue((directory / 'output/report.json').exists())


@unittest.skipUnless(importlib.util.find_spec('yaml'), 'Install a2api[openapi] for YAML parsing tests')
class YAMLTests(unittest.TestCase):
    def load(self, text):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'api.yaml'
            path.write_text(text)
            return load_openapi(path)[0]

    def test_safe_yaml_with_json_compatible_strings(self):
        result = self.load('openapi: 3.1.2\ninfo: {title: on, version: 2026-10-28}\npaths: {}\n')
        self.assertEqual(result['info']['title'], 'on')
        self.assertEqual(result['info']['version'], '2026-10-28')

    def test_duplicate_keys_aliases_and_python_tags_are_rejected(self):
        for text in ('openapi: 3.0.3\nopenapi: 3.1.2\n', 'value: &ref [1]\nother: *ref\n', '!!python/object/apply:os.system [echo unsafe]'):
            with self.subTest(text=text), self.assertRaises(A2APIError):
                self.load(text)


class GitHubScaleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.importer = OpenAPIImporter.from_file(FIXTURE, namespace='github')

    def test_official_full_snapshot_hash_and_inventory(self):
        import hashlib
        source = json.loads((FIXTURE.parent / 'source.json').read_text())
        self.assertEqual(hashlib.sha256(gzip.decompress(FIXTURE.read_bytes())).hexdigest(), source['sha256'])
        self.assertEqual(self.importer.source_hash, source['sha256'])
        self.assertEqual(source['operations'], 1254)
        self.assertEqual(source['paths'], 827)

    def test_every_official_operation_is_accounted_for_and_generated_ir_is_disabled(self):
        from collections import Counter
        statuses, methods = Counter(), Counter()
        identifiers = set()
        for record in self.importer.iter_operations():
            statuses[record.status] += 1
            methods[record.method] += 1
            if record.capability:
                self.assertFalse(record.capability.enabled)
                self.assertEqual(record.method, 'get')
                self.assertNotIn(record.capability.id, identifiers)
                identifiers.add(record.capability.id)
            else:
                self.assertTrue(record.diagnostics)
                self.assertTrue(record.diagnostics[0]['location'].startswith('/paths/'))
        self.assertEqual(sum(statuses.values()), 1254)
        self.assertEqual(methods['get'], 655)
        self.assertEqual(statuses['skipped'], 599)
        self.assertGreater(statuses['imported'], 600)
        golden = json.loads((FIXTURE.parent / 'import-report.json').read_text())
        self.assertEqual(dict(statuses), golden['summary']['statuses'])

    def test_official_examples_preserve_and_report_upstream_schema_drift(self):
        from a2api.importers.schema_conversion import local_reference
        selected = {'meta/get', 'repos/get', 'issues/list-for-repo'}
        actual = {}
        for record in self.importer.iter_operations(selected):
            self.assertEqual(record.status, 'imported', record.summary())
            operation = self.importer.document['paths'][record.path]['get']
            examples = operation['responses']['200']['content']['application/json']['examples']
            for key, example in examples.items():
                if '$ref' in example:
                    example = local_reference(self.importer.document, example['$ref'], '')
                if 'value' in example:
                    with self.subTest(operation=record.operation_id, example=key):
                        errors = Draft202012Validator(record.capability.describe()['outputSchema']).iter_errors({'result': example['value']})
                        actual[record.operation_id + ':' + key] = sorted(
                            [{'path': '/' + '/'.join(map(str, e.absolute_path)), 'rule': e.validator} for e in errors],
                            key=lambda issue: (issue['path'], issue['rule']))
        golden = json.loads((FIXTURE.parent / 'example-drift.json').read_text())
        self.assertEqual(actual, golden)
        self.assertEqual(actual['issues/list-for-repo:default'], [])


if __name__ == '__main__':
    unittest.main()
