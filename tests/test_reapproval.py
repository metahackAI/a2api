"""Selective review is pinned, atomic, portable and isolated by capability."""

import copy
from contextlib import ExitStack, redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest

from a2api import (A2APIError, approve_review, build_contracts, load_build, prepare_review,
                   regenerate, write_build, write_review)
from a2api.__main__ import main
from a2api.incremental_demo import sample_importer, sample_review
from a2api.importers import write_import
from a2api.ir import thaw
from a2api.review_demo import sample_built_runtime
from a2api.sample import TOKENS, create_backend, running

STAMP = '2026-10-29T03:00:00Z'
SHIPPING = 'order.shipping_status@0.1.0'
ORDER = 'order.summary@0.1.0'


class ReapprovalTests(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.directory = Path(self.stack.enter_context(tempfile.TemporaryDirectory()))
        importer = sample_importer()
        self.document = importer.document
        write_import(importer, self.directory / 'imports')
        self.base = build_contracts(self.directory / 'imports', sample_review())
        write_build(self.base, self.directory / 'baseline')
        self.serial = 0

    def update(self, previous=None, shared=False):
        if shared:
            self.document['components']['schemas']['PrincipalId']['minLength'] += 1
        else:
            self.document['components']['schemas']['Shipment']['properties']['status']['enum'].append('returned')
        return self.regenerate(previous or self.base)

    def regenerate(self, previous):
        self.serial += 1
        source = self.directory / f'updated-{self.serial}.json'
        source.write_text(json.dumps(self.document), encoding='utf-8')
        return regenerate(previous, source)

    def approve(self, previous, selected=None, proposal=None):
        return approve_review(previous, proposal or prepare_review(previous, selected or [SHIPPING]),
                              reviewed_by='haesookim fixture', reviewed_at=STAMP)

    def caps(self, build):
        return {cap.id: cap for cap in build.capabilities}

    def assert_error(self, code, action):
        with self.assertRaises(A2APIError) as caught:
            action()
        self.assertEqual(caught.exception.code, code, caught.exception.problem())

    def test_prepare_is_unreviewed_and_contains_old_and_new_source_evidence(self):
        pending = self.update()
        proposal = prepare_review(pending, [SHIPPING])
        row = proposal['reviews'][0]
        self.assertEqual(row['settings']['review']['state'], 'unreviewed')
        self.assertEqual(len(row['settings']['capabilities']), 1)
        self.assertEqual(len(row['settings']['operations']), 2)
        self.assertEqual(row['settings']['source']['sha256'], pending.source_snapshot['sourceSha256'])
        self.assertEqual(row['context']['impact']['affectedOperationIds'], ['demo.getShipment'])
        shipment = next(row for row in row['context']['sources'] if row['operationId'] == 'demo.getShipment')
        self.assertNotEqual(shipment['before'], shipment['after'])
        self.assertEqual(pending.summary()['requiresReview'], 1)
        self.assertEqual(self.caps(pending)['order.summary'].manifest_json, self.caps(self.base)['order.summary'].manifest_json)

    def test_approval_preserves_original_settings_and_unaffected_contract_bytes(self):
        pending = self.update()
        approved = self.approve(pending)
        destination = self.directory / 'approved'
        write_build(approved, destination)
        loaded = load_build(destination)
        self.assertEqual(loaded.summary()['requiresReview'], 0)
        self.assertEqual(loaded.summary()['enabled'], 2)
        self.assertEqual(loaded.review_sha256, pending.review_sha256)
        self.assertEqual((destination / 'review.json').read_bytes(), (self.directory / 'baseline/review.json').read_bytes())
        self.assertEqual((destination / 'contracts/order.summary.0.1.0.json').read_bytes(),
                         (self.directory / 'baseline/contracts/order.summary.0.1.0.json').read_bytes())
        shipping = self.caps(loaded)['order.shipping_status'].describe()
        self.assertEqual(shipping['provenance']['reviewedBy'], 'haesookim fixture')
        self.assertEqual(shipping['provenance']['reviewedAt'], STAMP)
        self.assertEqual(shipping['provenance']['sourceSha256'], pending.source_snapshot['sourceSha256'])
        self.assertEqual(loaded.approvals[0].generation, 1)

    def test_only_selected_pending_capability_is_approved_and_other_can_follow(self):
        pending = self.update(shared=True)
        first = self.approve(pending, [SHIPPING])
        self.assertTrue(self.caps(first)['order.shipping_status'].enabled)
        self.assertEqual(self.caps(first)['order.summary'].manifest_json, self.caps(pending)['order.summary'].manifest_json)
        self.assertEqual(first.summary()['requiresReview'], 1)
        second = self.approve(first, [ORDER])
        self.assertEqual(second.summary()['requiresReview'], 0)
        self.assertEqual(len(second.approvals), 2)
        self.assertEqual(self.caps(first)['order.shipping_status'].manifest_json, self.caps(second)['order.shipping_status'].manifest_json)
        output = self.directory / 'both'
        write_build(second, output)
        self.assertEqual(load_build(output).summary(), second.summary())

    def test_several_pending_capabilities_can_be_approved_atomically(self):
        approved = self.approve(self.update(shared=True), [ORDER, SHIPPING])
        self.assertEqual(approved.summary()['requiresReview'], 0)
        self.assertEqual(len(approved.approvals), 2)

    def test_multi_capability_validation_failure_leaves_all_pending_and_writes_no_build(self):
        pending = self.update(shared=True)
        write_build(pending, self.directory / 'pending')
        proposal = prepare_review(pending, [ORDER, SHIPPING])
        proposal['reviews'][-1]['settings']['operations'][0]['outputs']['orderId']['pointer'] = '/result/missing'
        write_review(proposal, self.directory / 'review.json')
        output = self.directory / 'should-not-exist'
        with redirect_stderr(io.StringIO()), redirect_stdout(io.StringIO()):
            code = main(['approve-review', '--build', str(self.directory / 'pending'), '--review', str(self.directory / 'review.json'),
                         '--reviewed-by', 'fixture', '--output', str(output)])
        self.assertEqual(code, 1)
        self.assertFalse(output.exists())
        self.assertEqual(load_build(self.directory / 'pending').summary()['requiresReview'], 2)

    def test_partial_approval_and_pending_state_survive_a_portable_followup_update(self):
        first = self.approve(self.update(shared=True), [SHIPPING])
        write_build(first, self.directory / 'first')
        self.document['info']['description'] = 'No operation changes'
        next_build = self.regenerate(self.directory / 'first')
        self.assertEqual(next_build.summary()['requiresReview'], 1)
        self.assertTrue(self.caps(next_build)['order.shipping_status'].enabled)
        self.assertFalse(self.caps(next_build)['order.summary'].enabled)
        self.assertEqual(self.caps(first)['order.shipping_status'].manifest_json, self.caps(next_build)['order.shipping_status'].manifest_json)
        approved = self.approve(next_build, [ORDER])
        write_build(approved, self.directory / 'second')
        self.assertEqual(load_build(self.directory / 'second').summary()['requiresReview'], 0)

    def test_edited_selected_settings_and_shared_projection_do_not_replace_other_contract(self):
        pending = self.update()
        proposal = prepare_review(pending, [SHIPPING])
        settings = proposal['reviews'][0]['settings']
        settings['capabilities'][0]['title'] = '검토한 배송 조회'
        settings['capabilities'][0]['outputSchema']['properties']['shipments']['items']['properties']['status']['enum'].append('returned')
        order = next(row for row in settings['operations'] if row['id'] == 'demo.getOrder')
        order['outputs']['extraOrderId'] = {'pointer': '/result/orderId'}
        approved = self.approve(pending, proposal=proposal)
        self.assertEqual(self.caps(approved)['order.shipping_status'].title, '검토한 배송 조회')
        self.assertEqual(self.caps(approved)['order.summary'].manifest_json, self.caps(self.base)['order.summary'].manifest_json)
        def returned_shipments(path, payload):
            if path.startswith('/shipments/'):
                payload['status'] = 'returned'
            return 200, payload
        origin = self.stack.enter_context(running(create_backend(transform=returned_shipments)))
        runtime = sample_built_runtime(approved, origin)
        for identifier, calls in [('order.summary', 1), ('order.shipping_status', 3)]:
            result = runtime.invoke(identifier, '0.1.0', runtime.catalog.version, {'orderId': 'ORD-1001'}, TOKENS['demo-alice'])
            self.assertEqual(result['status'], 'succeeded', result)
            self.assertEqual(result['stats']['backendCalls'], calls)
            if identifier == 'order.shipping_status':
                self.assertEqual([row['status'] for row in result['data']['shipments']], ['returned', 'returned'])

    def test_unrelated_followup_preserves_new_approval_then_shipping_change_invalidates_only_shipping(self):
        approved = self.approve(self.update())
        self.document['info']['description'] = 'Documentation only'
        stable = self.regenerate(approved)
        self.assertEqual(stable.summary()['requiresReview'], 0)
        self.assertEqual([cap.manifest_json for cap in stable.capabilities], [cap.manifest_json for cap in approved.capabilities])
        self.document['components']['schemas']['Shipment']['description'] = 'A new source change'
        changed = self.regenerate(stable)
        self.assertEqual(changed.summary()['requiresReview'], 1)
        self.assertTrue(self.caps(changed)['order.summary'].enabled)
        again = self.approve(changed)
        output = self.directory / 'again'
        write_build(again, output)
        self.assertEqual(load_build(output).summary()['requiresReview'], 0)

    def test_later_proposal_reuses_previously_edited_settings(self):
        pending = self.update()
        proposal = prepare_review(pending, [SHIPPING])
        proposal['reviews'][0]['settings']['capabilities'][0]['title'] = '보존할 검토 설정'
        approved = self.approve(pending, proposal=proposal)
        self.document['components']['schemas']['Shipment']['description'] = 'Next'
        next_proposal = prepare_review(self.regenerate(approved), [SHIPPING])
        self.assertEqual(next_proposal['reviews'][0]['settings']['capabilities'][0]['title'], '보존할 검토 설정')

    def test_stale_source_or_same_generation_approval_rejects_old_proposal(self):
        pending = self.update(shared=True)
        proposal = prepare_review(pending, [ORDER])
        first = self.approve(pending, [SHIPPING])
        self.assert_error('STALE_REVIEW', lambda: self.approve(first, proposal=proposal))
        self.document['info']['description'] = 'New revision'
        later = self.regenerate(pending)
        self.assert_error('STALE_REVIEW', lambda: self.approve(later, proposal=proposal))

    def test_selection_rejects_unaffected_unknown_ambiguous_and_duplicate_names(self):
        pending = self.update()
        for selection in ([], [ORDER], [SHIPPING, SHIPPING], ['order.shipping_status'], ['missing@0.1.0']):
            self.assert_error('INVALID_REVIEW_SELECTION', lambda: prepare_review(pending, selection))
        self.assert_error('INCREMENTAL_BUILD_REQUIRED', lambda: prepare_review(self.base, [SHIPPING]))
        approved = self.approve(pending)
        self.assert_error('INVALID_REVIEW_SELECTION', lambda: prepare_review(approved, [SHIPPING]))

    def test_context_source_scope_and_membership_are_pinned(self):
        pending = self.update()
        for change, code in [
            (lambda row: row['context'].update(version='0.2.0'), 'INVALID_REVIEW_SELECTION'),
            (lambda row: row['context']['sources'].clear(), 'REVIEW_CONTEXT_DRIFT'),
            (lambda row: row['settings']['source'].update(sha256='0' * 64), 'REVIEW_SCOPE_DRIFT'),
            (lambda row: row['settings']['operations'][0]['source'].update(digest='0' * 64), 'REVIEW_SCOPE_DRIFT'),
            (lambda row: row['settings']['capabilities'][0].update(id='other.capability'), 'REVIEW_SCOPE_DRIFT'),
            (lambda row: row['settings']['review'].update(scope='source'), 'REVIEW_SCOPE_DRIFT'),
        ]:
            proposal = prepare_review(pending, [SHIPPING])
            change(proposal['reviews'][0])
            self.assert_error(code, lambda: self.approve(pending, proposal=proposal))

    def test_invalid_reviewed_projection_never_creates_approved_build(self):
        pending = self.update()
        proposal = prepare_review(pending, [SHIPPING])
        proposal['reviews'][0]['settings']['operations'][0]['outputs']['orderId']['pointer'] = '/result/missing'
        with self.assertRaises(A2APIError):
            self.approve(pending, proposal=proposal)
        self.assertEqual(pending.summary()['requiresReview'], 1)
        self.assertEqual(len(pending.approvals), 0)

    def test_new_required_input_must_be_reviewed_and_mapped_before_approval(self):
        shipment = self.document['paths']['/shipments/{shipmentId}']['get']
        shipment['parameters'].append({'name': 'locale', 'in': 'query', 'required': True, 'schema': {'type': 'string'}})
        pending = self.regenerate(self.base)
        proposal = prepare_review(pending, [SHIPPING])
        with self.assertRaises(A2APIError):
            self.approve(pending, proposal=proposal)
        settings = proposal['reviews'][0]['settings']
        operation = next(row for row in settings['operations'] if row['id'] == 'demo.getShipment')
        operation['inputs']['locale'] = {'pointer': '/query/locale'}
        capability = settings['capabilities'][0]
        capability['inputSchema']['properties']['locale'] = {'type': 'string'}
        capability['inputSchema']['required'].append('locale')
        for example in capability['examples']:
            if 'input' in example:
                example['input']['locale'] = 'ko'
        step = next(row for row in capability['binding']['steps'] if row['id'] == 'shipments')
        step['input']['locale'] = {'from': 'input', 'pointer': '/locale'}
        approved = self.approve(pending, proposal=proposal)
        self.assertEqual(approved.summary()['requiresReview'], 0)

    def test_unavailable_or_renamed_operations_cannot_be_approved(self):
        for mode in ('deleted', 'renamed', 'unsupported'):
            document = copy.deepcopy(self.document)
            if mode == 'deleted':
                del self.document['paths']['/shipments/{shipmentId}']
            elif mode == 'renamed':
                self.document['paths']['/shipments/{shipmentId}']['get']['operationId'] = 'newShipment'
            else:
                del self.document['components']['schemas']['Shipment']
            pending = self.regenerate(self.base)
            self.assert_error('REVIEW_SOURCE_UNAVAILABLE', lambda: prepare_review(pending, [SHIPPING]))
            self.document = document

    def test_reviewer_and_timestamp_must_be_valid(self):
        pending = self.update()
        proposal = prepare_review(pending, [SHIPPING])
        self.assert_error('REVIEW_REQUIRED', lambda: approve_review(pending, proposal, reviewed_by='  '))
        self.assert_error('INVALID_REVIEW', lambda: approve_review(pending, proposal, reviewed_by='reviewer', reviewed_at='yesterday'))

    def test_approval_artifacts_and_anchor_tampering_are_rejected(self):
        approved = self.approve(self.update())
        for filename in ['approvals/index.json', 'approvals/0000/review.json', 'contracts/order.shipping_status.0.1.0.json']:
            output = self.directory / ('tampered-' + str(self.serial))
            self.serial += 1
            write_build(approved, output)
            path = output / filename
            path.write_bytes(path.read_bytes() + b' ')
            with self.assertRaises(A2APIError):
                load_build(output)

    def test_cli_prepare_and_approve_without_overwriting_any_input(self):
        pending = self.update()
        source = self.directory / 'pending'
        write_build(pending, source)
        proposal = self.directory / 'shipping.review.json'
        stream = io.StringIO()
        with redirect_stdout(stream):
            self.assertEqual(main(['prepare-review', '--build', str(source), '--capability', SHIPPING, '--output', str(proposal)]), 0)
        self.assertEqual(json.loads(stream.getvalue())['state'], 'unreviewed')
        before = proposal.read_bytes()
        stream = io.StringIO()
        output = self.directory / 'approved'
        with redirect_stdout(stream):
            self.assertEqual(main(['approve-review', '--build', str(source), '--review', str(proposal),
                '--reviewed-by', 'haesookim fixture', '--reviewed-at', STAMP, '--output', str(output)]), 0)
        self.assertEqual(json.loads(stream.getvalue())['requiresReview'], 0)
        self.assertEqual(before, proposal.read_bytes())
        self.assertEqual(load_build(source).summary()['requiresReview'], 1)
        self.assert_error('OUTPUT_EXISTS', lambda: write_review(prepare_review(pending, [SHIPPING]), proposal))
        with redirect_stderr(io.StringIO()), redirect_stdout(io.StringIO()):
            self.assertEqual(main(['approve-review', '--build', str(source), '--review', str(proposal),
                '--reviewed-by', 'fixture', '--output', str(output)]), 1)
