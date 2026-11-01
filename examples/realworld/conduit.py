"""An in-memory RealWorld (Conduit) API server that follows the official OpenAPI document.

Written for the evaluation; no third-party implementation is built or run. A flavor reproduces the
documented differences of each real implementation that a2api read from code (see compare.py):

  spec    the OpenAPI document: creates answer 201, deletes 204, comment ids are integers, empty bio is null
  spring  createArticle answers 200 (ResponseEntity.ok), comment ids are strings
  go      deletes answer 200 {"article"|"comment": "delete success"}; bio and image are Go strings ("")
  rust    creates answer 200 (Json), deletes 200 with an empty body; bio is a String ("")
  python  bio is `str = ""`

Every flavor serves the paths with and without the `/api` prefix. Authentication is
`Authorization: Token <token>` as in the specification. State is reset with POST /__reset.
"""

from __future__ import annotations

import copy
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import re
import threading
from urllib.parse import parse_qs, unquote, urlsplit

START = datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc)

SEED_USERS = [
    {'username': 'jake', 'email': 'jake@conduit.test', 'password': 'jakejake', 'bio': 'I work at statefarm', 'image': None},
    {'username': 'alice', 'email': 'alice@conduit.test', 'password': 'alicepass', 'bio': 'Rust and databases', 'image': None},
    {'username': 'bob', 'email': 'bob@conduit.test', 'password': 'bobpass12', 'bio': 'Gopher', 'image': None},
    {'username': 'carol', 'email': 'carol@conduit.test', 'password': 'carolpass', 'bio': None, 'image': None},
    {'username': 'dmitri', 'email': 'dmitri@conduit.test', 'password': 'dmitripw1', 'bio': 'Compilers', 'image': None},
]
SEED_ARTICLES = [
    # slug, title, description, author, tags, days after START, favorited by
    ('rust-ownership-in-practice', 'Rust ownership in practice', 'Borrowing without tears', 'alice', ['rust', 'programming'], 1, ['jake', 'bob']),
    ('async-rust-pitfalls', 'Async Rust pitfalls', 'Five ways to block an executor', 'alice', ['rust', 'async'], 9, ['carol']),
    ('postgres-indexes-explained', 'Postgres indexes explained', 'B-tree, GIN and when to use them', 'alice', ['databases'], 14, ['jake', 'carol', 'dmitri']),
    ('go-error-handling', 'Go error handling', 'Wrapping, sentinel errors and errors.Is', 'bob', ['go', 'programming'], 3, ['alice']),
    ('go-generics-one-year-later', 'Go generics one year later', 'What changed in real code bases', 'bob', ['go'], 12, []),
    ('writing-a-tiny-compiler', 'Writing a tiny compiler', 'From tokens to bytecode in 500 lines', 'dmitri', ['compilers', 'programming'], 6, ['alice', 'bob', 'carol']),
    ('parsing-with-pratt', 'Parsing with Pratt', 'Operator precedence made simple', 'dmitri', ['compilers'], 16, ['jake']),
    ('my-first-garden', 'My first garden', 'Tomatoes, basil and too many slugs', 'carol', ['gardening'], 4, ['dmitri']),
    ('draft-notes', 'Draft notes', 'Things I want to write about', 'jake', ['meta'], 18, []),
    ('training-for-a-marathon', 'Training for a marathon', 'Sixteen weeks, one plan', 'jake', ['running'], 8, ['carol', 'alice']),
]
SEED_COMMENTS = [
    ('rust-ownership-in-practice', 'bob', 'The borrow checker finally clicked for me.', 2),
    ('rust-ownership-in-practice', 'carol', 'Could you add an example with Rc?', 3),
    ('go-error-handling', 'dmitri', 'errors.Join deserves a section.', 5),
    ('writing-a-tiny-compiler', 'jake', 'Loved the bytecode part.', 7),
    ('writing-a-tiny-compiler', 'alice', 'Did you try a register VM?', 8),
    ('writing-a-tiny-compiler', 'bob', 'Bookmarked!', 9),
    ('training-for-a-marathon', 'dmitri', 'Good luck on race day.', 10),
]
SEED_FOLLOWS = [('jake', 'dmitri'), ('alice', 'bob'), ('carol', 'alice')]
FLAVORS = ('spec', 'spring', 'go', 'rust', 'python')
CREATED = {'spec': 201, 'spring': 201, 'go': 201, 'rust': 200, 'python': 201}
TEXT_FIELDS = {'go': ('bio', 'image'), 'rust': ('bio',), 'python': ('bio',)}  # never null in that code


def stamp(days, hours=0):
    return (START + timedelta(days=days, hours=hours)).isoformat().replace('+00:00', 'Z')


class Store:
    def __init__(self):
        self.reset()

    def reset(self):
        self.users = {u['username']: dict(u) for u in copy.deepcopy(SEED_USERS)}
        self.tokens = {f'token-{name}': name for name in self.users}
        self.follows = set(SEED_FOLLOWS)
        self.articles, self.favorites, self.comments, self.next_comment = {}, set(), [], 1
        for slug, title, description, author, tags, day, fans in SEED_ARTICLES:
            self.articles[slug] = {'slug': slug, 'title': title, 'description': description, 'body': description + '.',
                                   'tagList': sorted(tags), 'createdAt': stamp(day), 'updatedAt': stamp(day), 'author': author}
            self.favorites.update((fan, slug) for fan in fans)
        for slug, author, body, day in SEED_COMMENTS:
            self.comments.append({'id': self.next_comment, 'slug': slug, 'author': author, 'body': body,
                                  'createdAt': stamp(day, 1), 'updatedAt': stamp(day, 1)})
            self.next_comment += 1
        self.clock = 30


class Conduit(BaseHTTPRequestHandler):
    store: Store = None
    flavor = 'spec'
    lock = threading.Lock()

    def log_message(self, *args):
        pass

    # --- helpers --------------------------------------------------------------------------------

    def send(self, status, body=None):
        raw = b'' if body is None else json.dumps(body).encode()
        self.send_response(status)
        if body is not None:
            self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def error(self, status, field, message):
        self.send(status, {'errors': {field: [message]}})

    def viewer(self):
        header = self.headers.get('Authorization') or ''
        return self.store.tokens.get(header[len('Token '):]) if header.startswith('Token ') else None

    def text(self, field, value):
        return '' if value is None and field in TEXT_FIELDS.get(self.flavor, ()) else value

    def profile(self, username, viewer):
        user = self.store.users[username]
        return {'username': username, 'bio': self.text('bio', user['bio']), 'image': self.text('image', user['image']),
                'following': (viewer, username) in self.store.follows}

    def article(self, slug, viewer):
        item = self.store.articles[slug]
        fans = [user for user, liked in self.store.favorites if liked == slug]
        return {**{k: v for k, v in item.items() if k != 'author'}, 'favorited': viewer in fans,
                'favoritesCount': len(fans), 'author': self.profile(item['author'], viewer)}

    def comment(self, item, viewer):
        identifier = str(item['id']) if self.flavor == 'spring' else item['id']
        return {'id': identifier, 'createdAt': item['createdAt'], 'updatedAt': item['updatedAt'], 'body': item['body'],
                'author': self.profile(item['author'], viewer)}

    def user(self, username):
        user = self.store.users[username]
        return {'user': {'email': user['email'], 'token': f'token-{username}', 'username': username,
                         'bio': self.text('bio', user['bio']), 'image': self.text('image', user['image'])}}

    def deleted(self, what):
        if self.flavor == 'go':
            return self.send(200, {what: 'delete success'})
        if self.flavor == 'rust':
            return self.send(200)
        return self.send(204)

    def payload(self):
        length = int(self.headers.get('Content-Length') or 0)
        try:
            return json.loads(self.rfile.read(length) or b'null')
        except ValueError:
            return None

    # --- routing --------------------------------------------------------------------------------

    def do_GET(self):
        self.route('GET')

    def do_POST(self):
        self.route('POST')

    def do_PUT(self):
        self.route('PUT')

    def do_DELETE(self):
        self.route('DELETE')

    def route(self, method):
        url = urlsplit(self.path)
        path = re.sub(r'^/api(?=/)', '', unquote(url.path)).rstrip('/') or '/'
        query = {key: values[-1] for key, values in parse_qs(url.query).items()}
        with self.lock:
            if (method, path) == ('POST', '/__reset'):
                self.store.reset()
                return self.send(200, {'ok': True})
            if (method, path) == ('GET', '/__state'):
                return self.send(200, self.state())
            self.store.clock += 1
            viewer = self.viewer()
            for pattern, verb, handler, auth in ROUTES:
                found = re.fullmatch(pattern, path)
                if found and verb == method:
                    if auth and viewer is None:
                        return self.error(401, 'token', 'is missing')
                    return handler(self, viewer, query, *found.groups())
            return self.error(404, 'path', 'not found')

    def state(self):
        s = self.store
        return {'follows': sorted(s.follows), 'favorites': sorted(s.favorites),
                'articles': {slug: {k: v for k, v in a.items()} for slug, a in s.articles.items()},
                'comments': s.comments, 'users': {name: {k: v for k, v in u.items() if k != 'password'} for name, u in s.users.items()}}

    # --- operations -----------------------------------------------------------------------------

    def login(self, viewer, query):
        body = (self.payload() or {}).get('user') or {}
        user = next((u for u in self.store.users.values() if u['email'] == body.get('email')), None)
        if user is None or user['password'] != body.get('password'):
            return self.error(401, 'credentials', 'invalid')
        return self.send(200, self.user(user['username']))

    def register(self, viewer, query):
        body = (self.payload() or {}).get('user') or {}
        if not all(isinstance(body.get(k), str) and body[k] for k in ('username', 'email', 'password')):
            return self.error(422, 'user', "can't be blank")
        if body['username'] in self.store.users:
            return self.error(409, 'username', 'has already been taken')
        self.store.users[body['username']] = {'username': body['username'], 'email': body['email'],
                                              'password': body['password'], 'bio': None, 'image': None}
        self.store.tokens[f"token-{body['username']}"] = body['username']
        return self.send(CREATED[self.flavor], self.user(body['username']))

    def current_user(self, viewer, query):
        return self.send(200, self.user(viewer))

    def update_user(self, viewer, query):
        body = (self.payload() or {}).get('user')
        if not isinstance(body, dict) or not body:
            return self.error(422, 'user', "can't be blank")
        for key in ('email', 'bio', 'image', 'username', 'password'):
            if key in body:
                self.store.users[viewer][key] = body[key]
        return self.send(200, self.user(viewer))

    def get_profile(self, viewer, query, username):
        if username not in self.store.users:
            return self.error(404, 'profile', 'not found')
        return self.send(200, {'profile': self.profile(username, viewer)})

    def follow(self, viewer, query, username, unfollow=False):
        if username not in self.store.users:
            return self.error(404, 'profile', 'not found')
        (self.store.follows.discard if unfollow else self.store.follows.add)((viewer, username))
        return self.send(200, {'profile': self.profile(username, viewer)})

    def unfollow(self, viewer, query, username):
        return self.follow(viewer, query, username, unfollow=True)

    def listing(self, items, viewer, query):
        try:
            limit, offset = int(query.get('limit', 20)), int(query.get('offset', 0))
        except ValueError:
            return self.error(422, 'query', 'limit and offset must be integers')
        items = sorted(items, key=lambda a: a['createdAt'], reverse=True)
        page = [self.article(a['slug'], viewer) for a in items[offset:offset + limit]]
        return self.send(200, {'articles': page, 'articlesCount': len(items)})

    def list_articles(self, viewer, query):
        items = list(self.store.articles.values())
        if query.get('tag'):
            items = [a for a in items if query['tag'] in a['tagList']]
        if query.get('author'):
            items = [a for a in items if a['author'] == query['author']]
        if query.get('favorited'):
            items = [a for a in items if (query['favorited'], a['slug']) in self.store.favorites]
        return self.listing(items, viewer, query)

    def feed(self, viewer, query):
        followed = {target for user, target in self.store.follows if user == viewer}
        return self.listing([a for a in self.store.articles.values() if a['author'] in followed], viewer, query)

    def create_article(self, viewer, query):
        body = (self.payload() or {}).get('article') or {}
        if not all(isinstance(body.get(k), str) and body[k] for k in ('title', 'description', 'body')):
            return self.error(422, 'article', "title, description and body can't be blank")
        slug = re.sub(r'[^a-z0-9]+', '-', body['title'].lower()).strip('-')
        if slug in self.store.articles:
            return self.error(409, 'title', 'has already been taken')
        now = stamp(self.store.clock)
        self.store.articles[slug] = {'slug': slug, 'title': body['title'], 'description': body['description'],
                                     'body': body['body'], 'tagList': sorted(body.get('tagList') or []),
                                     'createdAt': now, 'updatedAt': now, 'author': viewer}
        return self.send(200 if self.flavor == 'spring' else CREATED[self.flavor], {'article': self.article(slug, viewer)})

    def get_article(self, viewer, query, slug):
        if slug not in self.store.articles:
            return self.error(404, 'article', 'not found')
        return self.send(200, {'article': self.article(slug, viewer)})

    def update_article(self, viewer, query, slug):
        if slug not in self.store.articles:
            return self.error(404, 'article', 'not found')
        if self.store.articles[slug]['author'] != viewer:
            return self.error(403, 'article', 'forbidden')
        body = (self.payload() or {}).get('article') or {}
        for key in ('title', 'description', 'body'):
            if isinstance(body.get(key), str):
                self.store.articles[slug][key] = body[key]
        self.store.articles[slug]['updatedAt'] = stamp(self.store.clock)
        return self.send(200, {'article': self.article(slug, viewer)})

    def delete_article(self, viewer, query, slug):
        if slug not in self.store.articles:
            return self.error(404, 'article', 'not found')
        if self.store.articles[slug]['author'] != viewer:
            return self.error(403, 'article', 'forbidden')
        del self.store.articles[slug]
        return self.deleted('article')

    def comments(self, viewer, query, slug):
        if slug not in self.store.articles:
            return self.error(404, 'article', 'not found')
        return self.send(200, {'comments': [self.comment(c, viewer) for c in self.store.comments if c['slug'] == slug]})

    def add_comment(self, viewer, query, slug):
        if slug not in self.store.articles:
            return self.error(404, 'article', 'not found')
        body = (self.payload() or {}).get('comment') or {}
        if not isinstance(body.get('body'), str) or not body['body']:
            return self.error(422, 'body', "can't be empty")
        now = stamp(self.store.clock)
        item = {'id': self.store.next_comment, 'slug': slug, 'author': viewer, 'body': body['body'], 'createdAt': now, 'updatedAt': now}
        self.store.next_comment += 1
        self.store.comments.append(item)
        return self.send(CREATED[self.flavor], {'comment': self.comment(item, viewer)})

    def delete_comment(self, viewer, query, slug, identifier):
        found = next((c for c in self.store.comments if str(c['id']) == identifier and c['slug'] == slug), None)
        if found is None:
            return self.error(404, 'comment', 'not found')
        if found['author'] != viewer:
            return self.error(403, 'comment', 'forbidden')
        self.store.comments.remove(found)
        return self.deleted('comment')

    def favorite(self, viewer, query, slug, remove=False):
        if slug not in self.store.articles:
            return self.error(404, 'article', 'not found')
        (self.store.favorites.discard if remove else self.store.favorites.add)((viewer, slug))
        return self.send(200, {'article': self.article(slug, viewer)})

    def unfavorite(self, viewer, query, slug):
        return self.favorite(viewer, query, slug, remove=True)

    def tags(self, viewer, query):
        return self.send(200, {'tags': sorted({tag for a in self.store.articles.values() for tag in a['tagList']})})


SLUG = r'([^/]+)'
ROUTES = [
    (r'/users/login', 'POST', Conduit.login, False),
    (r'/users', 'POST', Conduit.register, False),
    (r'/user', 'GET', Conduit.current_user, True),
    (r'/user', 'PUT', Conduit.update_user, True),
    (rf'/profiles/{SLUG}', 'GET', Conduit.get_profile, False),
    (rf'/profiles/{SLUG}/follow', 'POST', Conduit.follow, True),
    (rf'/profiles/{SLUG}/follow', 'DELETE', Conduit.unfollow, True),
    (r'/articles/feed', 'GET', Conduit.feed, True),
    (r'/articles', 'GET', Conduit.list_articles, False),
    (r'/articles', 'POST', Conduit.create_article, True),
    (rf'/articles/{SLUG}', 'GET', Conduit.get_article, False),
    (rf'/articles/{SLUG}', 'PUT', Conduit.update_article, True),
    (rf'/articles/{SLUG}', 'DELETE', Conduit.delete_article, True),
    (rf'/articles/{SLUG}/comments', 'GET', Conduit.comments, False),
    (rf'/articles/{SLUG}/comments', 'POST', Conduit.add_comment, True),
    (rf'/articles/{SLUG}/comments/{SLUG}', 'DELETE', Conduit.delete_comment, True),
    (rf'/articles/{SLUG}/favorite', 'POST', Conduit.favorite, True),
    (rf'/articles/{SLUG}/favorite', 'DELETE', Conduit.unfavorite, True),
    (r'/tags', 'GET', Conduit.tags, False),
]


def serve(flavor, port=0):
    """Start one flavor in a thread; returns (server, origin)."""
    if flavor not in FLAVORS:
        raise ValueError('unknown flavor')
    handler = type(f'Conduit_{flavor}', (Conduit,), {'store': Store(), 'flavor': flavor, 'lock': threading.Lock()})
    server = ThreadingHTTPServer(('127.0.0.1', port), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f'http://127.0.0.1:{server.server_address[1]}'
