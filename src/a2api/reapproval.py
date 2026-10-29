"""Pinned, editable review proposals and explicit per-capability approval."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import tempfile

from .builder import (REVIEW_META, _bytes, _digest, _read, build_contracts, load_build, source_digest)
from .errors import A2APIError
from .importers import write_import
from .ir import thaw
from .openapi_dependencies import snapshot_importer
from .regeneration import (CapabilityApproval, IncrementalBuild, _assemble, _incremental_files,
                           _incremental_report, _key, _latest)
from .reviewed_adapter import HTTPDeployment
from .schema import validate_value

REVIEW_FORMAT = 'a2api-capability-review/0.1'


def _previous(value) -> IncrementalBuild:
    value = load_build(value) if isinstance(value, (str, Path)) else value
    if not isinstance(value, IncrementalBuild):
        raise A2APIError('INCREMENTAL_BUILD_REQUIRED', 'Selective review requires an incremental build.')
    return value


def _target(previous):
    return {'buildSha256': _digest(_incremental_report(previous, _incremental_files(previous))),
            'sourceSha256': previous.source_snapshot['sourceSha256'], 'generation': len(previous.history) - 1}


def _selection(previous, capabilities):
    pending = {row['id'] + '@' + row['version'] for row in previous.review_status if row['state'] == 'requires_review'}
    if (not isinstance(capabilities, (list, tuple)) or not capabilities
            or any(not isinstance(value, str) for value in capabilities) or len(set(capabilities)) != len(capabilities)):
        raise A2APIError('INVALID_REVIEW_SELECTION', 'Select one or more unique capability IDs with @version.')
    if not set(capabilities).issubset(pending):
        raise A2APIError('INVALID_REVIEW_SELECTION', 'Only capability IDs with @version currently requiring review may be selected.')
    return sorted(capabilities)


def prepare_review(previous, capabilities: list[str]) -> dict:
    """Produce an editable proposal; this does not approve or activate anything."""
    previous = _previous(previous)
    selected = _selection(previous, capabilities)
    latest = _latest(previous.approved, previous.approvals)
    importer = snapshot_importer(thaw(previous.source_snapshot))
    states = {row['id'] + '@' + row['version']: thaw(row) for row in previous.review_status}
    reviews = []
    for identity in selected:
        identifier, version = identity.rsplit('@', 1)
        capability, base = latest[(identifier, version)]
        settings = thaw(base.review)
        settings['capabilities'] = [row for row in settings['capabilities'] if (row['id'], row['version']) == (identifier, version)]
        operation_ids = set(settings['capabilities'][0]['operationIds'])
        settings['operations'] = [row for row in settings['operations'] if row['id'] in operation_ids]
        plans = {plan.operation.id: plan for plan in base.plans}
        source_ids = {plans[key].source.operation_id for key in operation_ids}
        if not source_ids.issubset(importer._ids):
            raise A2APIError('REVIEW_SOURCE_UNAVAILABLE', 'A selected source operation was removed or renamed; re-import/rebind it explicitly.')
        fresh = {_key(record): record for record in importer.iter_operations(source_ids)}
        sources = []
        for row in settings['operations']:
            old = plans[row['id']].source
            new = fresh.get(_key(old))
            entry = previous.source_dependencies['operations'].get(_key(old))
            if (new is None or new.capability is None or new.operation_id != old.operation_id or entry is None or entry['errors']):
                raise A2APIError('REVIEW_SOURCE_UNAVAILABLE', 'Selected sources must remain uniquely identifiable, supported and dependency-complete. Re-import/rebind removed or renamed operations.')
            row['source'] = {'capabilityId': new.capability.id, 'operationId': new.operation_id, 'digest': source_digest(new)}
            sources.append({'operationId': row['id'], 'sourceKey': _key(old),
                            'before': {'contract': old.capability.describe(), 'binding': thaw(old.binding)},
                            'after': {'contract': new.capability.describe(), 'binding': thaw(new.binding)}})
        settings['source']['sha256'] = previous.source_snapshot['sourceSha256']
        settings['review']['state'] = 'unreviewed'
        reviews.append({'context': {'id': identifier, 'version': version, 'impact': states[identity],
                                    'previousContract': capability.describe(), 'sources': sources}, 'settings': settings})
    return {'format': REVIEW_FORMAT, 'target': _target(previous), 'reviews': reviews}


def write_review(proposal: dict, output: str | Path) -> None:
    path = Path(output)
    raw = _bytes(proposal)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open('xb') as stream:
            stream.write(raw)
    except FileExistsError:
        raise A2APIError('OUTPUT_EXISTS', 'Choose a new review filename; existing settings are not overwritten.') from None


def _compile(previous, settings):
    importer = snapshot_importer(thaw(previous.source_snapshot))
    identifiers = {row['source']['operationId'] for row in settings['operations']}
    with tempfile.TemporaryDirectory(prefix='a2api-review-') as temporary:
        imports = Path(temporary) / 'imports'
        write_import(importer, imports, operation_ids=identifiers)
        return build_contracts(imports, settings)


def approve_review(previous, proposal: dict | str | Path, *, reviewed_by: str, reviewed_at: str | None = None) -> IncrementalBuild:
    """Compile selected settings against pinned current sources, then append approvals."""
    previous = _previous(previous)
    proposal = _read(Path(proposal), limit=128 * 1024 * 1024) if isinstance(proposal, (str, Path)) else thaw(proposal)
    if (not isinstance(proposal, dict) or set(proposal) != {'format', 'target', 'reviews'}
            or proposal['format'] != REVIEW_FORMAT or not isinstance(proposal['reviews'], list) or not proposal['reviews']):
        raise A2APIError('INVALID_REVIEW', 'The selective review proposal has an unsupported format.')
    if proposal['target'] != _target(previous):
        raise A2APIError('STALE_REVIEW', 'The proposal targets a different build. Prepare a new review for the current build.')
    if not isinstance(reviewed_by, str) or not reviewed_by.strip():
        raise A2APIError('REVIEW_REQUIRED', 'An explicit, nonempty reviewer identity is required.')
    identities = []
    for row in proposal['reviews']:
        if (not isinstance(row, dict) or set(row) != {'context', 'settings'} or not isinstance(row['context'], dict)
                or not isinstance(row['context'].get('id'), str) or not isinstance(row['context'].get('version'), str)):
            raise A2APIError('INVALID_REVIEW', 'Each proposal must contain a capability context and review settings.')
        identities.append(row['context']['id'] + '@' + row['context']['version'])
    expected = prepare_review(previous, identities)
    expected_rows = {row['context']['id'] + '@' + row['context']['version']: row for row in expected['reviews']}
    approvals = list(previous.approvals)
    timestamp = reviewed_at if reviewed_at is not None else datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    for identity, row in zip(identities, proposal['reviews']):
        original = expected_rows[identity]
        if row['context'] != original['context']:
            raise A2APIError('REVIEW_CONTEXT_DRIFT', 'Source evidence and impact context must remain unchanged.')
        settings = thaw(row['settings'])
        validate_value(REVIEW_META, settings, code='INVALID_REVIEW', status=400)
        baseline = original['settings']
        if (settings['source'] != baseline['source'] or settings['review']['scope'] != baseline['review']['scope']
                or len(settings['capabilities']) != 1
                or [(item['id'], item['version']) for item in settings['capabilities']] != [(item['id'], item['version']) for item in baseline['capabilities']]
                or set(settings['capabilities'][0]['operationIds']) != set(baseline['capabilities'][0]['operationIds'])
                or len(settings['operations']) != len(baseline['operations'])
                or {item['id']: item['source'] for item in settings['operations']} != {item['id']: item['source'] for item in baseline['operations']}):
            raise A2APIError('REVIEW_SCOPE_DRIFT', 'Review settings must retain the selected identity, operation membership, source pins and scope.')
        settings['review'].update(state='reviewed', reviewedBy=reviewed_by.strip(), reviewedAt=timestamp)
        validate_value(REVIEW_META, settings, code='INVALID_REVIEW', status=400)
        approvals.append(CapabilityApproval(len(previous.history) - 1, _compile(previous, settings)))
    result = _assemble(previous.approved, previous.history, thaw(previous.source_snapshot), previous.candidates, tuple(approvals))
    deployments = {plan.source.capability.operations[plan.source.operation_id].service_ref: HTTPDeployment('https://deployment.invalid')
                   for plan in result.plans}
    result.adapter(deployments)  # Validate live binding consistency without making requests.
    return result
