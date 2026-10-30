"""Small host-only search annotations; no new wire descriptor fields."""

from .errors import A2APIError


def search_keywords(value, *, code='INVALID_CONVERSION') -> tuple[str, ...]:
    if value is None:
        return ()
    if (not isinstance(value, (list, tuple)) or len(value) > 32
            or any(not isinstance(term, str) or not term.strip() or len(term) > 80 for term in value)):
        raise A2APIError(code, 'keywords must contain at most 32 nonempty strings of at most 80 characters.')
    return tuple(dict.fromkeys(term.strip() for term in value))


def summary_override(value) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 1000:
        raise A2APIError('INVALID_CONVERSION', 'summary must be a nonempty string of at most 1000 characters.')
    return value.strip()
