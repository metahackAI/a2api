"""Collect benchmark run files into a committed evidence JSON (hashes, headers, summaries, failures).

python examples/benchmark/evidence.py --group holdout artifacts/benchmark/runs/holdout-rep1.jsonl ... \
    --group dev artifacts/benchmark/runs/dev-all-1.jsonl --output docs/evidence/completion-evaluation.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from summarize import aggregate, failures, load, stability


def describe(path):
    raw = Path(path).read_bytes()
    runs, headers = load([path])
    header = next((item for item in headers if item.get('type') == 'header'), {})
    return {'file': Path(path).name, 'sha256': hashlib.sha256(raw).hexdigest(), 'runs': len(runs),
            'header': {key: header.get(key) for key in ('startedAt', 'model', 'gitCommit', 'gitDirty', 'split', 'taskFingerprint',
                                                         'scales', 'languages', 'modes', 'repetitions', 'firstRepetition',
                                                         'maxToolBytes', 'searchLimit', 'hints', 'limits', 'resumedFrom')}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--group', nargs='+', action='append', required=True, metavar=('NAME', 'JSONL'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    evidence = {'scope': 'Synthetic benchmark API implemented in Python, Spring, Go and Rust; one model; see docs/34.',
                'groups': {}}
    for name, *paths in args.group:
        runs, _ = load(paths)
        evidence['groups'][name] = {
            'files': [describe(path) for path in paths],
            'byScaleMode': aggregate(runs, ['scale', 'mode']), 'byMode': aggregate(runs, ['mode']),
            'byLanguageMode': aggregate(runs, ['language', 'mode']), 'byKindMode': aggregate(runs, ['kind', 'mode']),
            'stability': stability(runs), 'failures': failures(runs)}
    args.output.write_text(json.dumps(evidence, ensure_ascii=False, indent=1) + '\n')
    print(args.output)


if __name__ == '__main__':
    main()
