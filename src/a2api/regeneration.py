"""Incremental source updates that preserve approvals and quarantine affected capabilities."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Mapping

from .builder import (BuildResult, _artifact_files, _build_report, _bytes, _digest, _inside, _read,
                      BINDING_KEYS, load_build, source_digest)
from .contracts import compile_contract
from .errors import A2APIError
from .importers import ImportRecord, OpenAPIImporter
from .ir import freeze, thaw
from .reviewed_adapter import ReviewedHTTPAdapter
from .openapi_dependencies import (canonical_bytes, dependency_index, diff_indices, operation_key,
                                  snapshot, snapshot_importer, validate_index)

INCREMENTAL_FORMAT = 'a2api-incremental-build/0.1'
APPROVED_FORMAT = 'a2api-incremental-build/0.2'
MAX_GENERATIONS = 64
MAX_APPROVALS = 256


@dataclass(frozen=True)
class CapabilityApproval:
    generation: int
    build: BuildResult


def _latest(approved, approvals):
    latest = {(cap.id, cap.version): (cap, approved) for cap in approved.capabilities}
    for approval in approvals:
        cap = approval.build.capabilities[0]
        # Reviewed operation IDs are business identifiers. Scope deployment refs
        # so independently reviewed projections never replace another cap's plan.
        manifest = cap.describe()
        for operation in manifest['operations']:
            operation['operationRef'] += '#capability=' + cap.id + '@' + cap.version
        latest[(cap.id, cap.version)] = (compile_contract(manifest), approval.build)
    return latest


def _key(record: ImportRecord) -> str:
    return operation_key(record.method, record.path)


def _approved_with_snapshot(previous: BuildResult, baseline_source: str | Path | None) -> BuildResult:
    if previous.source_snapshot is not None:
        return previous
    if baseline_source is None:
        raise A2APIError('DEPENDENCY_SNAPSHOT_MISSING', 'Legacy builds need --baseline-source with the originally reviewed OpenAPI document.')
    methods = {plan.source.method.upper() for plan in previous.plans}
    importer = OpenAPIImporter.from_file(baseline_source, namespace=previous.review['source']['namespace'], methods=methods)
    if importer.source_hash != previous.review['source']['sha256']:
        raise A2APIError('SOURCE_DRIFT', 'The baseline document does not match the original review.')
    importer.source_name = previous.import_report['source']
    records = {record.operation_id: record for record in importer.iter_operations({p.source.operation_id for p in previous.plans})}
    for plan in previous.plans:
        record = records.get(plan.source.operation_id)
        if record is None or source_digest(record) != source_digest(plan.source):
            raise A2APIError('SOURCE_DRIFT', 'The baseline document does not reproduce the approved imports.')
    index = dependency_index(importer)
    if any(index['operations'][_key(plan.source)]['errors'] for plan in previous.plans):
        raise A2APIError('DEPENDENCY_SNAPSHOT_INVALID', 'Legacy reviewed operations need resolved baseline dependencies.')
    report = {**thaw(previous.import_report), 'sourceSnapshot': 'source.snapshot.json', 'dependencyIndex': 'dependencies.json'}
    return replace(previous, import_report=freeze(report), source_snapshot=freeze(snapshot(importer)),
                   source_dependencies=freeze(index))


def _review_states(approved: BuildResult, history: tuple, approvals: tuple = ()) -> list[dict]:
    latest = _latest(approved, approvals)
    anchors = {(item.build.capabilities[0].id, item.build.capabilities[0].version): item.generation for item in approvals}
    transitions = []
    for before, after in zip(history, history[1:]):
        affected = {}
        for operation in diff_indices(before, after)['operations']:
            if operation['status'] != 'unchanged':
                reasons = operation['reasons'] or [{'kind': operation['status'], 'pointer': '/paths/' + operation['path'].replace('~', '~0').replace('/', '~1')}]
                affected.setdefault(operation['key'], {})
                for reason in reasons:
                    affected[operation['key']][_digest(reason)] = reason
        transitions.append(affected)
    states = []
    for capability in approved.capabilities:
        identity = (capability.id, capability.version)
        source_build = latest[identity][1]
        sources = {plan.operation.id: _key(plan.source) for plan in source_build.plans}
        affected = {}
        for changes in transitions[anchors.get(identity, 0):]:
            for key, reasons in changes.items():
                affected.setdefault(key, {}).update(reasons)
        operations = sorted(identifier for identifier in capability.operations if sources[identifier] in affected)
        states.append({'id': capability.id, 'version': capability.version,
                       'state': 'requires_review' if operations else 'reviewed', 'affectedOperationIds': operations,
                       'reasons': [{'operationId': identifier, 'sourceKey': sources[identifier],
                                    'changes': [affected[sources[identifier]][key] for key in sorted(affected[sources[identifier]])]}
                                   for identifier in operations]})
    return states


def _capabilities(approved: BuildResult, states: list[dict], approvals: tuple = ()):
    status = {(entry['id'], entry['version']): entry for entry in states}
    capabilities = []
    for capability, _ in _latest(approved, approvals).values():
        decision = status[(capability.id, capability.version)]
        if decision['state'] == 'reviewed':
            capabilities.append(capability)
            continue
        manifest = capability.describe()
        manifest.update(enabled=False, lifecycle='draft')
        manifest['provenance'].update(reviewState='unreviewed', requiresReview=True,
                                      affectedOperationIds=decision['affectedOperationIds'])
        capabilities.append(compile_contract(manifest))
    return tuple(capabilities)


@dataclass(frozen=True)
class IncrementalBuild(BuildResult):
    approved: BuildResult | None = None
    history: tuple = ()
    candidates: tuple[ImportRecord, ...] = ()
    change_report: Mapping = field(default_factory=dict)
    review_status: tuple = ()
    approvals: tuple[CapabilityApproval, ...] = ()

    def adapter(self, deployments, **limits):
        active = {(operation.service_ref, operation.operation_ref): operation
                  for cap in self.capabilities if cap.enabled for operation in cap.operations.values()}
        plans = tuple(plan for plan in self.plans
                      if active.get((plan.operation.service_ref, plan.operation.operation_ref)) == plan.operation)
        # The underlying wire adapter keys routes by source service/operation.
        # Distinct projections are fine; conflicting live source contracts are not.
        wire = {}
        for plan in plans:
            operation = plan.source.capability.operations[plan.source.operation_id]
            key = (operation.service_ref, operation.operation_ref)
            signature = (operation, plan.source.binding)
            if key in wire and wire[key] != signature:
                raise A2APIError('APPROVAL_OPERATION_CONFLICT', 'Active capabilities disagree on a shared HTTP source.')
            wire[key] = signature
        return ReviewedHTTPAdapter(plans, deployments, **limits)

    def summary(self) -> dict:
        return {'format': APPROVED_FORMAT if self.approvals else INCREMENTAL_FORMAT, 'sourceSha256': self.source_snapshot['sourceSha256'],
                'approvedSourceSha256': self.review['source']['sha256'], 'reviewSha256': self.review_sha256,
                'scope': self.review['review']['scope'], 'generation': len(self.history) - 1,
                'capabilities': len(self.capabilities), 'operations': len(self.plans),
                'enabled': sum(capability.enabled for capability in self.capabilities),
                'requiresReview': sum(entry['state'] == 'requires_review' for entry in self.review_status),
                **dict(self.change_report['regeneration'])}


def _assemble(approved: BuildResult, history: tuple, current: dict, candidates: tuple, approvals: tuple = ()) -> IncrementalBuild:
    if len(history) < 2 or len(history) > MAX_GENERATIONS + 1:
        raise A2APIError('DEPENDENCY_HISTORY_INVALID', 'The update history has an unsupported length.')
    for index in history:
        validate_index(index)
    if thaw(history[0]) != thaw(approved.source_dependencies):
        raise A2APIError('DEPENDENCY_HISTORY_INVALID', 'The update history does not begin at the approved source.')
    latest_index = dependency_index(snapshot_importer(thaw(current)))
    if thaw(history[-1]) != latest_index:
        raise A2APIError('DEPENDENCY_HISTORY_INVALID', 'The latest source and dependency history disagree.')
    identities = {(cap.id, cap.version): cap for cap in approved.capabilities}
    original_sources = {plan.operation.id: (_key(plan.source), plan.source.operation_id) for plan in approved.plans}
    if len(approvals) > MAX_APPROVALS:
        raise A2APIError('APPROVAL_HISTORY_INVALID', 'Start a new baseline before the approval history limit.')
    last_generation = 1
    for approval in approvals:
        if (type(approval.generation) is not int or not last_generation <= approval.generation < len(history)
                or len(approval.build.capabilities) != 1 or isinstance(approval.build, IncrementalBuild)
                or approval.build.source_dependencies is None):
            raise A2APIError('APPROVAL_HISTORY_INVALID', 'Selective approval history is invalid.')
        cap = approval.build.capabilities[0]
        if ((cap.id, cap.version) not in identities or thaw(approval.build.source_dependencies) != thaw(history[approval.generation])
                or approval.build.review['review']['scope'] != approved.review['review']['scope']):
            raise A2APIError('APPROVAL_HISTORY_INVALID', 'An approval does not match its capability or source generation.')
        if (set(cap.operations) != set(identities[(cap.id, cap.version)].operations)
                or any(original_sources.get(plan.operation.id) != (_key(plan.source), plan.source.operation_id)
                       for plan in approval.build.plans)):
            raise A2APIError('APPROVAL_HISTORY_INVALID', 'Selective approvals must preserve operation membership and source identities.')
        last_generation = approval.generation
    changed = diff_indices(history[-2], history[-1])
    states = _review_states(approved, history, approvals)
    capabilities = _capabilities(approved, states, approvals)
    previous_approvals = tuple(item for item in approvals if item.generation < len(history) - 1)
    previous_caps = _capabilities(approved, _review_states(approved, history[:-1], previous_approvals), previous_approvals)
    previous = {(capability.id, capability.version): capability for capability in previous_caps}
    converted = {operation['key'] for operation in changed['operations'] if operation['status'] in {'added', 'changed'}
                 and operation['method'].upper() in latest_index['requestedMethods']}
    by_key = {_key(record): record for record in candidates}
    if len(by_key) != len(candidates) or not converted.issubset(by_key):
        raise A2APIError('BUILD_DRIFT', 'Incremental operation drafts are incomplete or duplicated.')
    for key, record in by_key.items():
        entry = latest_index['operations'].get(key)
        if entry is None or entry['operationId'] != record.operation_id:
            raise A2APIError('BUILD_DRIFT', 'An operation draft is not present in the current source inventory.')
    reused_caps = [capability.id + '@' + capability.version for capability in capabilities
                   if capability.manifest_json == previous[(capability.id, capability.version)].manifest_json]
    changed['regeneration'] = {'convertedOperations': len(converted), 'reusedOperations': len(candidates) - len(converted),
                               'reusedCapabilityArtifacts': len(reused_caps)}
    changed['reusedCapabilities'] = reused_caps
    changed['capabilities'] = states
    plans = {}
    for cap, source_build in _latest(approved, approvals).values():
        for plan in source_build.plans:
            if plan.operation.id in cap.operations:
                operation = cap.operations[plan.operation.id]
                plans[(operation.service_ref, operation.operation_ref)] = replace(plan, operation=operation)
    return IncrementalBuild(capabilities=capabilities, plans=tuple(plans[key] for key in sorted(plans)), review=approved.review,
                            import_report=approved.import_report, source_snapshot=freeze(current),
                            source_dependencies=freeze(latest_index), approved=approved, history=tuple(freeze(index) for index in history),
                            candidates=tuple(sorted(candidates, key=_key)), change_report=freeze(changed),
                            review_status=tuple(freeze(state) for state in states), approvals=approvals)


def regenerate(previous: BuildResult | str | Path, source: str | Path, *, baseline_source: str | Path | None = None) -> IncrementalBuild:
    previous = load_build(previous) if isinstance(previous, (str, Path)) else previous
    if isinstance(previous, IncrementalBuild):
        approved, history, cache = previous.approved, previous.history, {_key(record): record for record in previous.candidates}
        approvals = previous.approvals
    else:
        approved = _approved_with_snapshot(previous, baseline_source)
        history = (approved.source_dependencies,)
        cache = {_key(plan.source): plan.source for plan in approved.plans}
        approvals = ()
    if len(history) > MAX_GENERATIONS:
        raise A2APIError('DEPENDENCY_HISTORY_INVALID', 'Start a new reviewed baseline before the update history limit.')
    importer = OpenAPIImporter.from_file(source, namespace=approved.review['source']['namespace'],
                                        methods=set(approved.source_snapshot['requestedMethods']))
    current, index = snapshot(importer), dependency_index(importer)
    changes = diff_indices(history[-1], index)
    changed_keys = {entry['key'] for entry in changes['operations'] if entry['status'] in {'added', 'changed'}}
    for entry in changes['operations']:
        if entry['status'] in {'changed', 'removed'}:
            cache.pop(entry['key'], None)
    identifiers = {index['operations'][key]['operationId'] for key in changed_keys
                   if index['operations'][key]['method'].upper() in importer.methods}
    # Only changed/new operations enter schema conversion; stable drafts keep their bytes.
    if identifiers:
        for record in importer.iter_operations(identifiers):
            if _key(record) in changed_keys and record.method.upper() in importer.methods:
                cache[_key(record)] = record
    return _assemble(approved, (*history, index), current, tuple(cache.values()), approvals)


def _draft_files(records: tuple, approved: BuildResult) -> dict[str, bytes]:
    artifacts, rows = {}, []
    baseline = {_key(plan.source): plan.source for plan in approved.plans}
    for record in records:
        row = {'key': _key(record), **record.summary()}
        if record.capability is not None:
            original = baseline.get(_key(record))
            reused = original is not None and source_digest(record) == source_digest(original)
            prefix = ('approved/imports/contracts/' + record.capability.id) if reused else 'drafts/contracts/' + _digest(_key(record))
            if reused:
                row['reusedApprovedSource'] = True
            else:
                artifacts[prefix + '.json'] = _bytes(record.capability.describe())
                artifacts[prefix + '.http.json'] = _bytes(record.binding)
            row['contract'] = prefix + '.json'
        rows.append(row)
    artifacts['drafts/report.json'] = _bytes({'operations': rows})
    return artifacts


def _incremental_files(result: IncrementalBuild) -> dict[str, bytes]:
    approved_files = _artifact_files(result.approved)
    artifacts = {'approved/' + name: raw for name, raw in approved_files.items()}
    artifacts['approved/build.json'] = _bytes(_build_report(result.approved, approved_files))
    artifacts.update({'review.json': _bytes(result.review), 'source.snapshot.json': canonical_bytes(result.source_snapshot),
                      'dependencies.json': canonical_bytes(result.source_dependencies), 'diff.json': _bytes(result.change_report),
                      'review-status.json': _bytes(result.review_status)})
    for index, value in enumerate(result.history):
        artifacts[f'history/{index:04d}.json'] = canonical_bytes(value)
    for capability in result.capabilities:
        artifacts['contracts/' + capability.id + '.' + capability.version + '.json'] = _bytes(capability.describe())
    artifacts.update(_draft_files(result.candidates, result.approved))
    if result.approvals:
        rows = []
        for index, approval in enumerate(result.approvals):
            prefix = f'approvals/{index:04d}'
            files = _artifact_files(approval.build)
            artifacts.update({prefix + '/' + name: raw for name, raw in files.items()})
            artifacts[prefix + '/build.json'] = _bytes(_build_report(approval.build, files))
            rows.append({'generation': approval.generation, 'build': prefix})
        artifacts['approvals/index.json'] = _bytes(rows)
    return artifacts


def _incremental_report(result: IncrementalBuild, artifacts: dict) -> dict:
    import hashlib
    return {**result.summary(), 'artifacts': {name: hashlib.sha256(raw).hexdigest() for name, raw in sorted(artifacts.items())},
            'contracts': ['contracts/' + capability.id + '.' + capability.version + '.json' for capability in result.capabilities]}


def write_regeneration(result: IncrementalBuild, output: str | Path) -> dict:
    artifacts = _incremental_files(result)
    report = _incremental_report(result, artifacts)
    directory = Path(output)
    try:
        directory.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        raise A2APIError('OUTPUT_EXISTS', 'Choose a new update directory; existing files are not overwritten.') from None
    for name, raw in artifacts.items():
        path = directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    (directory / 'build.json').write_bytes(_bytes(report))
    return report


def _load_drafts(directory: Path, approved: BuildResult) -> tuple:
    report = _read(_inside(directory, 'drafts/report.json'))
    records = []
    baseline = {_key(plan.source): plan.source for plan in approved.plans}
    try:
        for row in report['operations']:
            key = operation_key(row['method'], row['path'])
            if key != row['key'] or row['status'] not in {'imported', 'unsupported', 'skipped'}:
                raise ValueError()
            capability, binding = None, None
            if row['status'] == 'imported':
                original = baseline.get(key)
                reused = row.get('reusedApprovedSource') is True
                if reused and (original is None or original.capability.id != row['capabilityId'] or original.operation_id != row['operationId']):
                    raise ValueError()
                prefix = ('approved/imports/contracts/' + original.capability.id) if reused else 'drafts/contracts/' + _digest(key)
                if row['contract'] != prefix + '.json':
                    raise ValueError()
                capability = original.capability if reused else compile_contract(_read(_inside(directory, prefix + '.json')))
                binding = thaw(original.binding) if reused else _read(_inside(directory, prefix + '.http.json'))
                if (capability.enabled or capability.describe().get('schemaProfile') != 'openapi-draft'
                        or len(capability.operations) != 1 or row['operationId'] not in capability.operations
                        or capability.id != row['capabilityId'] or set(binding) != BINDING_KEYS
                        or binding['method'].lower() != row['method'] or binding['path'] != row['path']):
                    raise ValueError()
                wire = capability.operations[row['operationId']]
                if (wire.http_method.lower() != row['method'] or wire.operation_ref != binding['operationRef']
                        or wire.service_ref != binding['serviceRef']):
                    raise ValueError()
            record = ImportRecord(row['path'], row['method'], row['operationId'], row['status'], freeze(row['diagnostics']), capability, freeze(binding))
            if capability is not None:
                record.http_route('https://deployment.invalid')
            records.append(record)
    except (KeyError, TypeError, ValueError, AttributeError):
        raise A2APIError('BUILD_DRIFT', 'Incremental draft metadata is inconsistent.') from None
    return tuple(records)


def load_regeneration(directory: Path) -> IncrementalBuild:
    report = _read(_inside(directory, 'build.json'))
    generation = report.get('generation')
    if type(generation) is not int or not 1 <= generation <= MAX_GENERATIONS:
        raise A2APIError('DEPENDENCY_HISTORY_INVALID', 'The update generation is invalid.')
    approved = load_build(_inside(directory, 'approved'))
    if isinstance(approved, IncrementalBuild) or approved.source_snapshot is None:
        raise A2APIError('DEPENDENCY_HISTORY_INVALID', 'Updates require a flat reviewed baseline with source dependencies.')
    history = tuple(_read(_inside(directory, f'history/{index:04d}.json')) for index in range(generation + 1))
    current = _read(_inside(directory, 'source.snapshot.json'), limit=128 * 1024 * 1024)
    approvals = []
    if report.get('format') == APPROVED_FORMAT:
        rows = _read(_inside(directory, 'approvals/index.json'))
        if not isinstance(rows, list) or not 1 <= len(rows) <= MAX_APPROVALS:
            raise A2APIError('APPROVAL_HISTORY_INVALID', 'Approval history must be a bounded nonempty list.')
        for index, row in enumerate(rows):
            if not isinstance(row, dict) or set(row) != {'generation', 'build'} or row['build'] != f'approvals/{index:04d}':
                raise A2APIError('APPROVAL_HISTORY_INVALID', 'Approval build paths must use canonical filenames.')
            approvals.append(CapabilityApproval(row['generation'], load_build(_inside(directory, row['build']))))
    result = _assemble(approved, history, current, _load_drafts(directory, approved), tuple(approvals))
    artifacts = _incremental_files(result)
    if report != _incremental_report(result, artifacts):
        raise A2APIError('BUILD_DRIFT', 'Incremental metadata differs from its reconstructed impact analysis.')
    for name, expected in artifacts.items():
        try:
            with _inside(directory, name).open('rb') as stream:
                actual = stream.read(len(expected) + 1)
        except OSError:
            raise A2APIError('BUILD_DRIFT', 'An incremental build artifact is missing.') from None
        if actual != expected:
            raise A2APIError('BUILD_DRIFT', 'An incremental artifact differs from its reconstructed contents.')
    return result
