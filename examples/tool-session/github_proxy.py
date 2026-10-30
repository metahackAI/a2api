"""Uncached, bounded real GitHub forwarder for measurement only."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import re
import threading
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


def create(limit=40):
    state = {'records': [], 'lock': threading.Lock()}
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            with state['lock']:
                record = {'path': self.path}
                state['records'].append(record)
                allowed = len(state['records']) <= limit
            if not allowed or not re.fullmatch(r'/repos/[^/]+/[^/]+(?:/issues)?', urlsplit(self.path).path):
                status, body, headers = 429, b'{"message":"Evaluation route/request limit"}', {}
            else:
                request = Request('https://api.github.com' + self.path, headers={
                    'User-Agent': 'a2api-github-example', 'X-GitHub-Api-Version': '2026-03-10',
                    'Accept': 'application/json', 'Accept-Encoding': 'identity'})
                start = time.monotonic()
                try:
                    with urlopen(request, timeout=15) as response:
                        status, headers, body = response.status, dict(response.headers), response.read(2*1024*1024+1)
                except HTTPError as error:
                    status, headers, body = error.code, dict(error.headers), error.read(2*1024*1024+1)
                except (URLError, TimeoutError, OSError):
                    status, headers, body = 502, {}, b'{"message":"Upstream connection failed"}'
                record['upstreamSeconds'] = time.monotonic() - start
            lowered = {key.lower(): value for key, value in headers.items()}
            record.update(status=status, responseBytes=len(body), rateRemaining=lowered.get('x-ratelimit-remaining'))
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            try:self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):record['clientDisconnected'] = True

        def log_message(self, *_):pass
    return ThreadingHTTPServer(('127.0.0.1', 0), Handler), state
