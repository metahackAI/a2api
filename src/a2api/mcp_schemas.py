"""Compatibility entry point for catalog-independent protocol envelopes."""

from .protocol import response_schemas


def output_schemas(runtime=None, context=None) -> dict[str, dict]:
    # Preserve callers' optional arguments; schemas never depend on a catalog.
    return response_schemas()
