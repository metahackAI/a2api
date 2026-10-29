"""Build executable read contracts from pinned imports and explicit review settings."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from importlib.resources import files
import json
from pathlib import Path
from typing import Mapping

from .catalog import Catalog
from .contracts import compile_contract, parse_json
from .errors import A2APIError
from .importers import ImportRecord
from .ir import Capability, freeze, thaw
from .review_projection import annotate, check_input_coverage, projected_schema
from .reviewed_adapter import HTTPDeployment, ReviewedHTTPAdapter, ReviewedOperation
from .runtime import Runtime
from .schema import validate_value

REVIEW_META = json.loads(files('a2api').joinpath('schemas/review.schema.json').read_text(encoding='utf-8'))
BUILD_FORMAT = 'a2api-build/0.1'
BINDING_KEYS = {'serviceRef', 'operationRef', 'method', 'path', 'pathParameters', 'queryParameters', 'responseEnvelope',
                'headerParameters', 'requestBody', 'responseStatusField', 'responses', 'deploymentRequired'}


def _bytes(value) -> bytes:
    try:
        return (json.dumps(thaw(value), ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8')
    except (ValueError, TypeError, UnicodeError, RecursionError):
        raise A2APIError('BUILD_INPUT_INVALID', 'Build inputs must contain finite UTF-8 JSON values.') from None


def _digest(value) -> str:
    return hashlib.sha256(_bytes(value)).hexdigest()


def source_digest(record: ImportRecord) -> str:
    """Pin both imported contract and HTTP binding, including source provenance."""
    if record.capability is None or record.binding is None:
        raise A2APIError('IMPORT_NOT_BUILDABLE', 'Only successfully imported operations can be reviewed.')
    return _digest({'contract': record.capability.describe(), 'binding': record.binding})


def _read(path: Path, *, limit: int = 32 * 1024 * 1024):
    try:
        with path.open('rb') as stream:
            raw = stream.read(limit + 1)
        if len(raw) > limit:
            raise ValueError('Input exceeds supported size')
        return parse_json(raw.decode('utf-8'))
    except (OSError, ValueError, UnicodeError, RecursionError):
        raise A2APIError('BUILD_INPUT_INVALID', 'Build files must be bounded, strict UTF-8 JSON.') from None


def _inside(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise A2APIError('IMPORT_BUNDLE_INVALID', 'Artifact references must remain inside their bundle.')
    return path


def load_review(path: str | Path) -> dict:
    review = _read(Path(path), limit=4 * 1024 * 1024)
    validate_value(REVIEW_META, review, code='INVALID_REVIEW', status=400)
    return review


def _import_records(directory: Path, review: dict):
    report = _read(_inside(directory, 'report.json'))
    if not isinstance(report, dict) or not isinstance(report.get('operations'), list):
        raise A2APIError('IMPORT_BUNDLE_INVALID', 'Import report is missing its operation inventory.')
    if report.get('sourceSha256') != review['source']['sha256']:
        raise A2APIError('SOURCE_DRIFT', 'The imported source differs from the reviewed source hash.')
    records = {}
    for item in review['operations']:
        source = item['source']
        capability_id = source['capabilityId']
        if capability_id in records:
            continue
        matches = [row for row in report['operations'] if isinstance(row, dict) and row.get('capabilityId') == capability_id]
        if len(matches) != 1 or matches[0].get('status') != 'imported':
            raise A2APIError('IMPORT_NOT_BUILDABLE', 'A reviewed source operation is missing, duplicated or unsupported.')
        row = matches[0]
        expected = 'contracts/' + capability_id + '.json'
        if row.get('contract') != expected:
            raise A2APIError('IMPORT_BUNDLE_INVALID', 'Import contract paths must use the canonical generated filename.')
        # Validate paths before reading any source file referenced by a report.
        manifest = _read(_inside(directory, expected))
        binding = _read(_inside(directory, 'contracts/' + capability_id + '.http.json'))
        capability = compile_contract(manifest)
        provenance = manifest.get('provenance', {}).get('source', {})
        if (manifest.get('schemaProfile') != 'openapi-draft' or capability.id != capability_id
                or len(capability.operations) != 1 or not isinstance(binding, dict)):
            raise A2APIError('IMPORT_BUNDLE_INVALID', 'Build sources must be single-operation disabled import contracts.')
        if set(binding) != BINDING_KEYS or binding['responseEnvelope'] != 'result' or binding['deploymentRequired'] is not True:
            raise A2APIError('IMPORT_BUNDLE_INVALID', 'Imported HTTP bindings must use the supported explicit binding format.')
        operation = next(iter(capability.operations.values()))
        if (provenance.get('sha256') != review['source']['sha256'] or operation.service_ref != review['source']['namespace']
                or operation.id != row.get('operationId') or operation.http_method.lower() != row.get('method')
                or provenance.get('path') != row.get('path') or binding.get('path') != row.get('path')
                or binding.get('operationRef') != operation.operation_ref or binding.get('serviceRef') != operation.service_ref
                or binding.get('method') != operation.http_method):
            raise A2APIError('IMPORT_BUNDLE_INVALID', 'Import report, contract, provenance and binding disagree.')
        record = ImportRecord(row['path'], row['method'], operation.id, 'imported', (), capability, freeze(binding))
        try:
            record.http_route('https://deployment.invalid')
        except (A2APIError, KeyError, TypeError, ValueError, AttributeError):
            raise A2APIError('IMPORT_BUNDLE_INVALID', 'Imported HTTP binding is invalid.') from None
        records[capability_id] = record
    for item in review['operations']:
        record = records[item['source']['capabilityId']]
        if record.operation_id != item['source']['operationId'] or source_digest(record) != item['source']['digest']:
            raise A2APIError('SOURCE_DRIFT', 'An imported contract or binding differs from its reviewed digest.')
    source_snapshot, source_dependencies = None, None
    if 'sourceSnapshot' in report or 'dependencyIndex' in report:
        from .openapi_dependencies import dependency_index, operation_key, snapshot_importer
        if report.get('sourceSnapshot') != 'source.snapshot.json' or report.get('dependencyIndex') != 'dependencies.json':
            raise A2APIError('IMPORT_BUNDLE_INVALID', 'Source snapshot paths must use canonical bundle filenames.')
        source_snapshot = _read(_inside(directory, 'source.snapshot.json'), limit=128 * 1024 * 1024)
        importer = snapshot_importer(source_snapshot)
        source_dependencies = dependency_index(importer)
        if (importer.source_hash != review['source']['sha256'] or importer.namespace != review['source']['namespace']
                or _read(_inside(directory, 'dependencies.json')) != source_dependencies):
            raise A2APIError('DEPENDENCY_SNAPSHOT_INVALID', 'Source snapshot, dependency index and review disagree.')
        reconstructed = {record.capability.id: record for record in importer.iter_operations({r.operation_id for r in records.values()})
                         if record.capability is not None}
        for key, record in records.items():
            entry = source_dependencies['operations'].get(operation_key(record.method, record.path))
            if entry is None or entry['errors']:
                raise A2APIError('DEPENDENCY_SNAPSHOT_INVALID', 'Reviewed operations require resolved source dependencies.')
            if key not in reconstructed or source_digest(record) != source_digest(reconstructed[key]):
                raise A2APIError('SOURCE_DRIFT', 'Imported contracts differ from the captured OpenAPI source.')
    # Self-contained subset for rebuild/load; preserve the original document hash.
    selected = [row for row in report['operations'] if isinstance(row, dict) and row.get('capabilityId') in records]
    snapshot = {key: report[key] for key in ('source', 'sourceSha256', 'openapi', 'sourceSnapshot', 'dependencyIndex') if key in report}
    snapshot['selection'] = sorted(record.operation_id for record in records.values())
    snapshot['operations'] = sorted(selected, key=lambda row: row['capabilityId'])
    return tuple(records[key] for key in sorted(records)), snapshot, source_snapshot, source_dependencies


@dataclass(frozen=True)
class BuildResult:
    capabilities: tuple[Capability, ...]
    plans: tuple[ReviewedOperation, ...]
    review: Mapping
    import_report: Mapping
    source_snapshot: Mapping | None = None
    source_dependencies: Mapping | None = None

    @property
    def review_sha256(self) -> str:
        return _digest(self.review)

    def adapter(self, deployments: Mapping[str, HTTPDeployment], **limits) -> ReviewedHTTPAdapter:
        active = {operation for capability in self.capabilities if capability.enabled for operation in capability.operations}
        return ReviewedHTTPAdapter(tuple(plan for plan in self.plans if plan.operation.id in active), deployments, **limits)

    def runtime(self, deployments: Mapping[str, HTTPDeployment], *, allow_samples: bool = False, **limits) -> Runtime:
        return Runtime(Catalog(list(self.capabilities), allow_samples=allow_samples), self.adapter(deployments, **limits))

    def summary(self) -> dict:
        return {'format': 'a2api-build/0.2' if self.source_snapshot is not None else BUILD_FORMAT,
                'sourceSha256': self.review['source']['sha256'], 'reviewSha256': self.review_sha256,
                'scope': self.review['review']['scope'], 'capabilities': len(self.capabilities), 'operations': len(self.plans),
                'enabled': sum(capability.enabled for capability in self.capabilities)}


def build_contracts(imports: str | Path, review: dict | str | Path) -> BuildResult:
    """Validate all inputs before producing any enabled contract or output files."""
    review = load_review(review) if isinstance(review, (str, Path)) else json.loads(_bytes(review))
    validate_value(REVIEW_META, review, code='INVALID_REVIEW', status=400)
    decision = review['review']
    if decision['state'] != 'reviewed':
        raise A2APIError('REVIEW_REQUIRED', 'Review settings must be explicitly reviewed before building.')
    if not decision['reviewedBy'].strip() or any(not item['owner'].strip() or item['owner'] == 'unassigned' for item in review['capabilities']):
        raise A2APIError('REVIEW_REQUIRED', 'A reviewer and assigned capability owners are required.')
    records, report, source_snapshot, source_dependencies = _import_records(Path(imports), review)
    by_source = {record.capability.id: record for record in records}
    prepared, sources = {}, {}
    for item in review['operations']:
        identifier = item['id']
        if identifier in prepared:
            raise A2APIError('INVALID_REVIEW', 'Reviewed operation IDs must be unique.')
        source = by_source[item['source']['capabilityId']]
        wire = source.capability.operations[source.operation_id]
        if wire.http_method not in {'GET', 'HEAD'}:
            raise A2APIError('BUILD_WRITE_UNSUPPORTED', 'The reviewed MVP builder supports GET/HEAD execution only.')
        schemas = {
            'input': projected_schema(thaw(wire.input_schema), item['inputs'], direction='input'),
            'output': projected_schema(thaw(wire.output_schema), item['outputs'], direction='output'),
        }
        check_input_coverage(thaw(wire.input_schema), item['inputs'], schemas['input'])
        annotate(schemas, item['semanticAnnotations'], review['semanticTypes'])
        prepared[identifier] = {'id': identifier, 'serviceRef': wire.service_ref + '.reviewed', 'operationRef': identifier,
                                'httpMethod': wire.http_method, 'effects': item['effects'],
                                'inputSchema': schemas['input'], 'outputSchema': schemas['output']}
        sources[identifier] = (source, item)
    capabilities, used = [], set()
    digest = _digest(review)
    for item in review['capabilities']:
        identifiers = item['operationIds']
        if any(identifier not in prepared for identifier in identifiers):
            raise A2APIError('INVALID_REVIEW', 'A capability references an operation that has not been reviewed.')
        manifest = {key: value for key, value in item.items() if key != 'operationIds'}
        manifest.update(a2api='0.1.0-draft.1', schemaProfile='mvp', enabled=True, lifecycle='reviewed',
                        semanticTypes=review['semanticTypes'], operations=[prepared[key] for key in identifiers],
                        provenance={'kind': decision['scope'], 'reviewState': 'reviewed', 'reviewedBy': decision['reviewedBy'],
                                    'reviewedAt': decision['reviewedAt'], 'reviewSha256': digest,
                                    'sourceSha256': review['source']['sha256'],
                                    'sourceOperations': [sources[key][1]['source'] for key in identifiers]})
        capabilities.append(compile_contract(manifest))
        used.update(identifiers)
    if used != set(prepared):
        raise A2APIError('INVALID_REVIEW', 'Reviewed operations must be used by a declared capability.')
    # Catalog validates duplicate capability ID/version pairs.
    Catalog(capabilities)
    compiled = {key: operation for capability in capabilities for key, operation in capability.operations.items()}
    plans = tuple(ReviewedOperation(compiled[key], sources[key][0], freeze(sources[key][1]['inputs']),
                                    freeze(sources[key][1]['outputs'])) for key in sorted(prepared))
    return BuildResult(tuple(sorted(capabilities, key=lambda c: (c.id, c.version))), plans, freeze(review), freeze(report),
                       freeze(source_snapshot), freeze(source_dependencies))


def _artifact_files(result: BuildResult) -> dict[str, bytes]:
    artifacts = {'review.json': _bytes(result.review), 'imports/report.json': _bytes(result.import_report)}
    if result.source_snapshot is not None:
        from .openapi_dependencies import canonical_bytes
        artifacts['imports/source.snapshot.json'] = canonical_bytes(result.source_snapshot)
        artifacts['imports/dependencies.json'] = canonical_bytes(result.source_dependencies)
    for capability in result.capabilities:
        artifacts['contracts/' + capability.id + '.' + capability.version + '.json'] = _bytes(capability.describe())
    for plan in result.plans:
        source = plan.source
        prefix = 'imports/contracts/' + source.capability.id
        artifacts[prefix + '.json'] = _bytes(source.capability.describe())
        artifacts[prefix + '.http.json'] = _bytes(source.binding)
    return artifacts


def _build_report(result: BuildResult, artifacts: dict[str, bytes]) -> dict:
    return {**result.summary(), 'artifacts': {name: hashlib.sha256(raw).hexdigest() for name, raw in sorted(artifacts.items())},
            'contracts': ['contracts/' + c.id + '.' + c.version + '.json' for c in result.capabilities]}


def write_build(result: BuildResult, output: str | Path) -> dict:
    from .regeneration import IncrementalBuild, write_regeneration
    if isinstance(result, IncrementalBuild):
        return write_regeneration(result, output)
    artifacts = _artifact_files(result)
    report = _build_report(result, artifacts)
    directory = Path(output)
    try:
        directory.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        raise A2APIError('OUTPUT_EXISTS', 'Choose a new build directory; existing files are not overwritten.') from None
    for relative, raw in artifacts.items():
        path = directory / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    (directory / 'build.json').write_bytes(_bytes(report))
    return report


def load_build(path: str | Path) -> BuildResult:
    """Rebuild from bundled sources/review and verify every generated artifact."""
    directory = Path(path)
    _inside(directory, 'imports')
    report = _read(_inside(directory, 'build.json'))
    if isinstance(report, dict) and report.get('format') in {'a2api-incremental-build/0.1', 'a2api-incremental-build/0.2'}:
        from .regeneration import load_regeneration
        return load_regeneration(directory)
    result = build_contracts(_inside(directory, 'imports'), _inside(directory, 'review.json'))
    artifacts = _artifact_files(result)
    if report != _build_report(result, artifacts):
        raise A2APIError('BUILD_DRIFT', 'Build metadata differs from the reviewed source reconstruction.')
    for relative, expected in artifacts.items():
        try:
            with _inside(directory, relative).open('rb') as stream:
                actual = stream.read(len(expected) + 1)
        except OSError:
            raise A2APIError('BUILD_DRIFT', 'A generated build artifact is missing.') from None
        if actual != expected:
            raise A2APIError('BUILD_DRIFT', 'A generated build artifact differs from the reviewed reconstruction.')
    return result
