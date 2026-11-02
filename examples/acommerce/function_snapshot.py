"""Write the functions a model sees for the A-Commerce tools and the legacy facade, as the runs' sidecar
`<runs>.functions.json` that call_review.py judges failed calls against.

python examples/acommerce/function_snapshot.py --out runs.functions.json [--facade-module old_legacy_facade.py]

--facade-module takes another copy of legacy_facade.py (for runs made with an earlier conversion, e.g.
`git show <commit>:examples/acommerce/legacy_facade.py`).
"""

from __future__ import annotations

import argparse
import asyncio
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import conversion_fidelity  # noqa: E402


def load_facade_module(path):
    spec = importlib.util.spec_from_file_location('legacy_facade_snapshot', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


async def model_views(acom, facade):
    """The current conversion's model-facing functions for catalog items."""
    return {'acom': await conversion_fidelity.model_view(acom, 'acom'),
            'facade': await conversion_fidelity.model_view(facade, 'facade', conversion_fidelity.WORDS, True)}


async def snapshot(acom_path, facade_path, facade_module=None):
    acom = json.loads(Path(acom_path).read_text())['items']
    facade = json.loads(Path(facade_path).read_text())['items']
    if facade_module is not None:
        module = load_facade_module(facade_module)
        conversion_fidelity.VOCABULARY, conversion_fidelity.facade_options = module.VOCABULARY, module.facade_options
        words = getattr(module, 'WORDS', None)
    else:
        words = conversion_fidelity.WORDS
    return {'acom': await conversion_fidelity.model_view(acom, 'acom'),
            'facade': await conversion_fidelity.model_view(facade, 'facade', words, True)}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--acom', default=str(HERE.parents[1] / 'artifacts' / 'acommerce' / 'manifest-acom.json'))
    parser.add_argument('--facade', default=str(HERE.parents[1] / 'artifacts' / 'acommerce' / 'manifest-facade-22.json'))
    parser.add_argument('--facade-module', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    options = parser.parse_args()
    data = asyncio.run(snapshot(options.acom, options.facade, options.facade_module))
    options.out.write_text(json.dumps(data, ensure_ascii=False))
    print(json.dumps({'out': str(options.out), 'acom': len(data['acom']), 'facade': len(data['facade'])}))


if __name__ == '__main__':
    main()
