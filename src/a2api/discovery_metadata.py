"""Host-only annotations, bounded schema fields and deterministic retrieval."""

from collections import Counter, OrderedDict
import math
import re

from .errors import A2APIError
from .pointers import resolve

SEARCH_REVISION = 'field-search/1'
_STOP = frozenset('a an the to of for with from using and or this that is be by in on'.split())


def search_tokens(text):
    """Keep whole names plus camel parts; no service-specific synonym table."""
    words = re.findall(r'[^\W_]+', text, flags=re.UNICODE)
    parts = words + re.findall(r'[^\W_]+', re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', text), flags=re.UNICODE)
    result = set()
    for part in parts:
        word = part.casefold()
        if word.isascii():
            if len(word) > 4 and word.endswith('ies'):word = word[:-3] + 'y'
            elif len(word) > 6 and word.endswith(('ches', 'shes', 'sses', 'xes')):word = word[:-2]
            elif len(word) > 3 and word.endswith('s') and not word.endswith(('ss', 'us', 'is')):word = word[:-1]
        if word and word not in _STOP:result.add(word)
    return frozenset(result)


def schema_search_fields(schema, *, input=False):
    """Only root/array-item fields and one nearby child level; never fetch refs.

    Composite/cyclic roots are deliberately skipped. This is a search hint,
    never a schema transformation or a promise that optional fields exist.
    """
    def node(value):
        seen = set()
        for _ in range(32):
            if not isinstance(value, dict):return {}
            ref = value.get('$ref')
            if ref is None:
                if any(key in value for key in ('allOf', 'anyOf', 'oneOf', 'if', 'not')):return {}
                return value
            if not isinstance(ref, str) or not ref.startswith('#/$defs/') or ref in seen:return {}
            seen.add(ref)
            try:value = resolve(schema, ref[1:])
            except A2APIError:return {}
        return {}

    def properties(value):
        value = node(value)
        if value.get('type') == 'array':value = node(value.get('items'))
        return value.get('properties', {}) if isinstance(value.get('properties'), dict) else {}

    def label(name, value):
        value = node(value)
        return ' '.join((name, re.sub(r'[\W_]+', '', name), str(value.get('title', ''))[:80]))

    direct, nearby = [], []
    collection = node(schema).get('type') == 'array'
    for name, value in list(properties(schema).items())[:256]:
        children = list(properties(value).items())[:256]
        if input and name in ('path', 'query', 'headers', 'body') and children:
            direct.extend(label(child, item) for child, item in children)
        else:
            (nearby if collection and not input else direct).append(label(name, value))
            nearby.extend(label(child, item) for child, item in children)
    return ' '.join(direct), ' '.join(nearby)


class SearchIndex:
    """Presence-based field scores with corpus frequency; no hidden LLM/DB."""

    revision = SEARCH_REVISION

    def __init__(self, descriptors, metadata):
        self.documents = {}
        frequency = Counter()
        for key, descriptor in descriptors.items():
            info = metadata[key]
            inputs, input_children = schema_search_fields(descriptor['inputSchema'], input=True)
            outputs, output_children = schema_search_fields(descriptor['outputSchema'])
            fields = {'id': key[0], 'aliases': ' '.join(info['aliases']), 'summary': descriptor['summary'],
                'keywords': ' '.join(info['keywords']), 'input': inputs, 'output': outputs,
                'nearby': input_children + ' ' + output_children, 'body': ' '.join(info['terms'])}
            tokens = {field: search_tokens(text) for field, text in fields.items()}
            primary = set().union(*(terms for field, terms in tokens.items() if field != 'body'))
            frequency.update(primary)
            aliases = {re.sub(r'[\W_]+', '', alias).casefold() for alias in info['aliases']}
            self.documents[key] = (fields, tokens, aliases)
        count = len(self.documents)
        self._vocabulary = frozenset(frequency)

    @staticmethod
    def _match(term, terms, text):
        if term in terms:return 1.0
        if not term.isascii():return 0.85 if term in text.casefold() else 0.0
        if len(term) >= 4 and any(word.isascii() and len(word) >= 4 and
                (word.startswith(term) or term.startswith(word)) for word in terms):
            return 0.65
        return 0.0

    def rank(self, query):
        stripped = query.strip().casefold()
        exact = [key for key in self.documents if key[0].casefold() == stripped]
        if exact:return [(key, [query.strip()]) for key in sorted(exact)]
        terms = set()
        for word in re.findall(r'[^\W_]+', query, flags=re.UNICODE):
            whole = search_tokens(word.casefold())
            # A known compound is one query concept (GitHub is not three
            # independently weighted demands for github/git/hub). Snake-case
            # field labels also carry their compact spelling in the index.
            terms.update(whole if whole and whole <= self._vocabulary else search_tokens(word))
        if not query.strip():return [(key, []) for key in sorted(self.documents)]
        if not terms:return []
        ordered_terms = sorted(terms)
        weights = {'id': 14.0, 'aliases': 14.0, 'summary': 18.0, 'keywords': 18.0,
                   'input': 3.0, 'output': 6.0, 'nearby': 2.0, 'body': 0.2}
        matches, frequency = {}, Counter()
        for key, (fields, tokens, _) in self.documents.items():
            matches[key] = {term: {field: self._match(term, tokens[field], text) for field, text in fields.items()}
                            for term in ordered_terms}
            frequency.update(term for term in ordered_terms if any(value for field, value in matches[key][term].items() if field != 'body'))
        count = len(self.documents)
        idf = {term: math.log(1 + (count - frequency[term] + 0.5) / (frequency[term] + 0.5)) for term in terms}
        ranked = []
        for key, (fields, tokens, aliases) in self.documents.items():
            matched, score, coverage = set(), 0.0, 0.0
            for term in ordered_terms:
                values = matches[key][term]
                coverage += max(values[field] * weight for field, weight in
                    {'id': 1.0, 'aliases': 1.0, 'summary': 1.0, 'keywords': 1.0,
                     'input': 0.6, 'output': 0.9, 'nearby': 0.3, 'body': 0.05}.items())
                best = max(weight * values[field] /
                           (1 + 0.08 * math.log1p(len(tokens[field]))) for field, weight in weights.items())
                if best:
                    matched.add(term)
                    score += best * idf[term]
                    identity = max(values[field] for field in ('id', 'aliases'))
                    score += 12.0 * min(identity, values['summary']) * idf[term]
                    if any(value for field, value in values.items() if field != 'body'):score += 2.0
            if not matched:continue
            summary = tokens['summary']
            if len(summary) >= 2 and summary <= terms:
                score += 6.0
                coverage += 0.75
            if re.sub(r'[\W_]+', '', query).casefold() in aliases:
                score += 100.0
                coverage += len(terms) + 1
            original = [word for word in query.split() if search_tokens(word) & matched
                        or any(not term.isascii() and term in word.casefold() for term in matched)]
            ranked.append((-round(coverage, 8), -score, key, original))
        ranked.sort(key=lambda row: (row[0], row[1], *row[2]))
        return [(key, original) for _, _, key, original in ranked]


class SearchPages:
    """Session-local opaque cursors. Repeats reuse a page; only more advances."""

    def __init__(self):
        self._views = OrderedDict()

    def clear(self):self._views.clear()

    def prepare(self, query, more=False, *, limit=3, restart=False):
        normalized = ' '.join(query.split())
        key = normalized.casefold()
        previous = None if restart else self._views.get(key)
        if previous and previous['limit'] != limit:
            self._views.pop(key)
            previous = None
        if more:
            if previous is None:raise A2APIError('SEARCH_NOT_STARTED', 'Search this query before requesting more.')
            if previous['next'] is None:raise A2APIError('SEARCH_EXHAUSTED', 'No more candidates for this query.')
            if previous['page'] >= 3:raise A2APIError('SEARCH_PAGE_LIMIT', 'Three pages reached; refine the query.')
        cursor = (previous['next'] if more else previous['cursor']) if previous else None
        page = previous['page'] + int(more) if previous else 1
        arguments = {'query': previous['query'] if previous else normalized, 'limit': limit}
        if cursor is not None:arguments['cursor'] = cursor
        return {'key': key, 'arguments': arguments, 'page': page,
                'catalog': previous['catalog'] if previous else None}

    def commit(self, prepared, found):
        key, page = prepared['key'], prepared['page']
        previous = self._views.get(key)
        if previous and previous['catalog'] != found['catalogVersion']:
            if prepared['arguments'].get('cursor') is not None:
                raise A2APIError('CONTRACT_DRIFT', 'Search catalog changed; start a new search.', status=409)
            previous = None
        seen = set(previous['seen']) if previous else set()
        current = {(item['id'], item['version']) for item in found['capabilities']}
        progress = bool(current - seen)
        self._views[key] = {'query': prepared['arguments']['query'], 'limit': prepared['arguments']['limit'],
            'cursor': prepared['arguments'].get('cursor'), 'next': found['nextCursor'], 'page': page,
            'catalog': found['catalogVersion'], 'seen': seen | current}
        self._views.move_to_end(key)
        while len(self._views) > 32:self._views.popitem(last=False)
        capped = page == 3 and found['nextCursor'] is not None
        return {'moreAvailable': found['nextCursor'] is not None and not capped, 'page': page,
                'pageLimitReached': capped, 'progress': progress}


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
