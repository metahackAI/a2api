"""Reproduce the full import locally; no network or credentials are used."""

import argparse
from collections import Counter
import json
from pathlib import Path
import platform
import resource
import time

from jsonschema import Draft202012Validator

from a2api.importers import OpenAPIImporter, write_import
from a2api.importers.schema_conversion import local_reference

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, help='New directory for generated IR and HTTP bindings')
    parser.add_argument('--record-results', action='store_true', help='Update committed coverage and benchmark snapshots')
    parser.add_argument('--all-methods', action='store_true', help='Also import HEAD/POST/PUT/PATCH/DELETE as disabled drafts')
    args = parser.parse_args()
    started = time.perf_counter()
    importer = OpenAPIImporter.from_file(HERE / 'api.github.com.json.gz', namespace='github',
        methods={'GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE'} if args.all_methods else None)
    source = json.loads((HERE / 'source.json').read_text())
    assert importer.source_hash == source['sha256'], 'Upstream fixture hash changed'
    report = write_import(importer, args.output)
    elapsed = time.perf_counter() - started
    assert report['summary']['operations'] == source['operations']
    assert report['summary']['methods'] == source['methods']
    benchmark = {'elapsedSeconds': round(elapsed, 3), 'peakRssKiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                 'generatedManifestBytes': sum(path.stat().st_size for path in (Path(args.output) / 'contracts').glob('*.json')
                                               if not path.name.endswith('.http.json')),
                 'python': platform.python_version(), 'measurement': 'JSON/gzip load, conversion, contract validation and file writes; Linux peak RSS'}
    drift = {}
    for record in importer.iter_operations({'meta/get', 'repos/get', 'issues/list-for-repo'}):
        assert record.capability, record.summary()
        examples = importer.document['paths'][record.path]['get']['responses']['200']['content']['application/json']['examples']
        for name, example in examples.items():
            if '$ref' in example:
                example = local_reference(importer.document, example['$ref'], '')
            if 'value' in example:
                errors = Draft202012Validator(record.capability.describe()['outputSchema']).iter_errors({'result': example['value']})
                drift[record.operation_id + ':' + name] = sorted(
                    [{'path': '/' + '/'.join(map(str, e.absolute_path)), 'rule': e.validator} for e in errors],
                    key=lambda issue: (issue['path'], issue['rule']))
    if args.record_results:
        suffix = '-all-methods' if args.all_methods else ''
        for filename, value in [('import-report' + suffix + '.json', report), ('benchmark' + suffix + '.json', benchmark)]:
            (HERE / filename).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        if not args.all_methods:
            (HERE / 'example-drift.json').write_text(json.dumps(drift, indent=2) + '\n', encoding='utf-8')
            example = next(importer.iter_operations({'meta/get'}))
            (HERE / 'github.meta.get.json').write_text(json.dumps(example.capability.describe(), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            from a2api.ir import thaw
            (HERE / 'github.meta.get.http.json').write_text(json.dumps(thaw(example.binding), indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'summary': report['summary'], 'benchmark': benchmark,
                      'exampleDrift': {key: dict(Counter(issue['rule'] for issue in value)) for key, value in drift.items()}}, indent=2))


if __name__ == '__main__':
    main()
