"""In-memory Python implementation of the benchmark API semantics.

The generated Python capability module and the Python HTTP server (used by the
ordinary-spec baselines) share one BenchStore, so both see the same state.
The Spring, Go and Rust servers implement the same rules in their own code.
"""

from __future__ import annotations

import copy
import threading

from domain import DEFAULT_LIMIT, FIXED_TIME, MAX_LIMIT, resources, seed_state


class StoreError(Exception):
    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status
        self.message = message


def bounds(page, limit):
    page = 1 if page is None else page
    limit = DEFAULT_LIMIT if limit is None else limit
    if type(page) is not int or type(limit) is not int or page < 1 or limit < 1:
        raise StoreError(400, 'page and limit must be positive integers')
    return page, min(limit, MAX_LIMIT)


class BenchStore:
    def __init__(self, scale: str):
        self.scale = scale
        self.resources = {resource.key: resource for resource in resources(scale)}
        self.lock = threading.RLock()
        self.reset()

    def reset(self):
        with self.lock:
            self.rows = seed_state(self.scale)
            self.next = {key: resource.next_number() for key, resource in self.resources.items()}

    def state(self):
        with self.lock:
            return copy.deepcopy(self.rows)

    def _find(self, key, identifier):
        for index, row in enumerate(self.rows[key]):
            if row['id'] == identifier:
                return index
        raise StoreError(404, 'not found')

    def _check(self, resource, name, value):
        item = resource.field(name)
        if item.enum and value not in item.enum:
            raise StoreError(400, 'invalid ' + name)
        if item.kind == 'integer' and (type(value) is not int or value < 0):
            raise StoreError(400, 'invalid ' + name)
        if item.kind == 'boolean' and type(value) is not bool:
            raise StoreError(400, 'invalid ' + name)
        if item.kind == 'string' and not item.nullable and (type(value) is not str or not value):
            raise StoreError(400, 'invalid ' + name)

    def list(self, key, filters, page=None, limit=None):
        resource = self.resources[key]
        page, limit = bounds(page, limit)
        for name, value in filters.items():
            if value is not None:
                self._check(resource, name, value)
        with self.lock:
            matched = [copy.deepcopy(row) for row in self.rows[key]
                       if all(value is None or row[name] == value for name, value in filters.items())]
        return {'items': matched[(page - 1) * limit: page * limit], 'page': page, 'limit': limit,
                'total': len(matched), 'hasMore': page * limit < len(matched)}

    def get(self, key, identifier):
        with self.lock:
            return copy.deepcopy(self.rows[key][self._find(key, identifier)])

    def create(self, key, body):
        resource = self.resources[key]
        for name in resource.create_required:
            if name not in body or body[name] is None:
                raise StoreError(400, 'missing ' + name)
            self._check(resource, name, body[name])
        for name in resource.create_optional:
            if body.get(name) is not None:
                self._check(resource, name, body[name])
        with self.lock:
            identifier = resource.id_format.format(self.next[key])
            self.next[key] += 1
            row = {'id': identifier}
            for item in resource.fields:
                if item.name in resource.create_required or (item.name in resource.create_optional and body.get(item.name) is not None):
                    row[item.name] = body[item.name]
                elif item.name == 'createdAt':
                    row[item.name] = FIXED_TIME
                else:
                    row[item.name] = copy.deepcopy(resource.create_defaults.get(item.name))
            row.update(tenantId='tenant-a', internalNote='server-only note for ' + identifier,
                       audit={'createdBy': 'api', 'updatedBy': 'api', 'revision': 1, 'source': 'api'})
            self.rows[key].append(row)
            return copy.deepcopy(row)

    def update(self, key, identifier, body):
        resource = self.resources[key]
        for name in resource.patch:
            if body.get(name) is not None:
                self._check(resource, name, body[name])
        with self.lock:
            row = self.rows[key][self._find(key, identifier)]
            for name in resource.patch:
                if body.get(name) is not None:
                    row[name] = body[name]
            row['audit'] = {**row['audit'], 'updatedBy': 'api', 'revision': row['audit']['revision'] + 1}
            return copy.deepcopy(row)

    def delete(self, key, identifier):
        with self.lock:
            self.rows[key].pop(self._find(key, identifier))

    def search(self, key, query, limit=None):
        resource = self.resources[key]
        if type(query) is not str or not query:
            raise StoreError(400, 'query is required')
        _, limit = bounds(1, limit)
        needle = query.lower()
        with self.lock:
            matched = [copy.deepcopy(row) for row in self.rows[key]
                       if any(needle in str(row[name]).lower() for name in resource.search)]
        return {'items': matched[:limit], 'page': 1, 'limit': limit, 'total': len(matched), 'hasMore': limit < len(matched)}

    def cancel(self, key, identifier):
        with self.lock:
            row = self.rows[key][self._find(key, identifier)]
            if row['status'] not in ('pending', 'paid'):
                raise StoreError(409, 'only pending or paid orders can be cancelled')
            row['status'] = 'cancelled'
            row['audit'] = {**row['audit'], 'updatedBy': 'api', 'revision': row['audit']['revision'] + 1}
            return copy.deepcopy(row)

    def tracking(self, key, identifier):
        with self.lock:
            self._find(key, identifier)
        raise StoreError(503, 'carrier tracking service unavailable')
