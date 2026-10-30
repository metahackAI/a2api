"""Real pinned GitHub GET operations only; no synthetic functions or routes."""

from collections import Counter
import json
from pathlib import Path
import time

from a2api import ExecutionContext, HTTPDeployment, convert
from a2api.importers import OpenAPIImporter

ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / 'examples/github-openapi'
CONTEXT = ExecutionContext('github-public-evaluation', 'public', frozenset())
SMALL = ('repos/get', 'repos/get-commit', 'repos/list-commits', 'repos/get-branch',
         'repos/list-branches', 'repos/get-latest-release', 'issues/list-for-repo', 'pulls/list')
# Explicit public fields; complete upstream responses are still validated first.
SELECT = {'repos/get': ['full_name', 'default_branch', 'stargazers_count', 'archived'],
          'repos/get-commit': ['sha', 'stats', 'html_url']}


def load_source():
    started = time.monotonic()
    info = json.loads((SOURCE_DIR / 'source.json').read_text())
    source = OpenAPIImporter.from_file(SOURCE_DIR / 'api.github.com.json.gz', namespace='github')
    if source.source_hash != info['sha256']:raise ValueError('Pinned GitHub source hash changed.')
    records = list(source.iter_operations())
    inventory = {'source': info, 'getOperations': sum(r.method == 'get' for r in records),
        'statuses': dict(Counter(r.status for r in records)),
        'loadAndImportSeconds': time.monotonic() - started,
        'operations': [r.summary() for r in records if r.method == 'get']}
    return source, records, inventory


def create(source, records, scale, origin):
    started = time.monotonic()
    available = {r.operation_id for r in records if r.status == 'imported' and r.method == 'get'}
    selected = set(SMALL) if scale == 'small' else available if scale == 'large' else set()
    if not selected or not selected <= available:raise ValueError('Choose small/large supported GET catalog.')
    operations = {identifier: {'effect': 'read', **({'select': SELECT[identifier]} if identifier in SELECT else {})}
                  for identifier in sorted(selected)}
    app = convert(source, operations=operations, deployment=HTTPDeployment(origin, headers={
        'User-Agent': 'a2api-real-catalog-evaluation', 'X-GitHub-Api-Version': '2026-03-10'}))
    mapping = {r.capability.id: {'operationId': r.operation_id, 'path': r.path, 'method': r.method}
               for r in records if r.operation_id in selected}
    if len(app.descriptors()) != len(selected):raise ValueError('Converted catalog count mismatch.')
    return app, {'scale': scale, 'count': len(selected), 'convertSeconds': time.monotonic() - started,
                 'mapping': mapping, 'projection': SELECT,
                 'descriptorBytes': len(json.dumps(app.descriptors(), ensure_ascii=False, separators=(',', ':')).encode())}
