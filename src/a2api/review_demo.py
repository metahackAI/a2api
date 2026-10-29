"""Packaged OpenAPI -> explicit review -> build -> official MCP stdio demo."""

from __future__ import annotations

import hashlib
from importlib.resources import files
from pathlib import Path
import tempfile

from .builder import BuildResult, build_contracts, write_build
from .contracts import parse_json
from .errors import A2APIError
from .importers import OpenAPIImporter, write_import
from .reviewed_adapter import HTTPDeployment
from .sample import BACKEND_TOKEN


def sample_importer() -> OpenAPIImporter:
    raw = files('a2api.sample').joinpath('order-shipping.openapi.json').read_bytes()
    return OpenAPIImporter(parse_json(raw.decode('utf-8')), namespace='legacy_orders',
                           source_name='order-shipping.openapi.json', source_hash=hashlib.sha256(raw).hexdigest())


def sample_review() -> dict:
    return parse_json(files('a2api.sample').joinpath('order-shipping.review.json').read_text(encoding='utf-8'))


def sample_built_runtime(result: BuildResult, backend_url: str):
    if result.review['review']['scope'] != 'sample' or result.review['source']['namespace'] != 'legacy_orders':
        raise A2APIError('BUILD_SCOPE_MISMATCH', 'The sample CLI accepts local order/shipment fixture builds only.')
    return result.runtime({'legacy_orders': HTTPDeployment(backend_url, credential_provider=lambda _: {
        'Authorization': 'Bearer ' + BACKEND_TOKEN})}, allow_samples=True)


async def run_review_demo(order_id: str = 'ORD-1001', sample_user: str = 'alice') -> dict:
    from .mcp_demo import run_demo
    with tempfile.TemporaryDirectory(prefix='a2api-reviewed-') as temporary:
        directory = Path(temporary)
        report = write_import(sample_importer(), directory / 'imports')
        result = build_contracts(directory / 'imports', sample_review())
        write_build(result, directory / 'built')
        mcp = await run_demo(order_id, sample_user, build_path=directory / 'built')
        return {'import': report['summary'], 'build': result.summary(), 'mcp': mcp}
