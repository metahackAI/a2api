"""Offline search diagnostics; never report these as live LLM accuracy."""

import argparse
import json
from pathlib import Path
import time

from a2api.discovery_metadata import SEARCH_REVISION
from a2api.mcp_application import DirectApplications
from catalog import ROOT, create, load_source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():raise ValueError('Choose a new diagnostic path.')
    started = time.monotonic()
    source, records, inventory = load_source()
    app, info = create(source, records, 'large', 'https://api.github.com')
    runtime = DirectApplications(app)
    old = json.loads((ROOT / 'docs/evidence/real-github-evaluation.json').read_text())
    replay = []
    for row in old['rankDiagnostics']:
        ranked = [key[0] for key, _ in runtime._index.rank(row['query'])]
        replay.append({**row, 'newTop3': ranked[:3],
            'newTargetRanks': {target: ranked.index(target) + 1 if target in ranked else None for target in row['targetRanks']}})
    by_operation = {item['operationId']: identifier for identifier, item in info['mapping'].items()}
    fixed = json.loads(Path(__file__).with_name('search-queries.json').read_text())
    unseen = []
    for row in fixed:
        target = by_operation[row['operationId']]
        ranked = [key[0] for key, _ in runtime._index.rank(row['query'])]
        unseen.append({**row, 'target': target, 'rank': ranked.index(target) + 1 if target in ranked else None,
                       'top3': ranked[:3]})
    value = {'searchRevision': SEARCH_REVISION, 'sourceSha256': source.source_hash, 'count': info['count'],
        'seconds': time.monotonic() - started, 'replayedQueries': replay,
        'separateOfflineQueries': unseen, 'top3Count': sum(row['rank'] is not None and row['rank'] <= 3 for row in unseen),
        'note': 'Fixed offline queries distinct from the 24 live questions; not a live holdout-model evaluation.'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'count': value['count'], 'separateQueries': unseen, 'top3Count': value['top3Count']}, ensure_ascii=False))


if __name__ == '__main__':main()
