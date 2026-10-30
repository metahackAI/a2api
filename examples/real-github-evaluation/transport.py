"""Count uncached real HTTP reads; credentials stay in host memory."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import hashlib
import json
import subprocess
import threading
import time
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

REPOSITORIES = {('psf', 'requests'), ('octocat', 'hello-world')}


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):return None


def credential(mode):
    if mode == 'none':return None
    if mode != 'gh':raise ValueError('Use github-auth=none or gh.')
    result = subprocess.run(['gh', 'auth', 'token', '--hostname', 'github.com'], capture_output=True, text=True)
    if result.returncode or not result.stdout.strip():raise RuntimeError('GITHUB_CLI_AUTH_UNAVAILABLE')
    return result.stdout.strip()


def headers(token=None):
    value = {'User-Agent': 'a2api-real-catalog-evaluation', 'X-GitHub-Api-Version': '2026-03-10',
             'Accept': 'application/json', 'Accept-Encoding': 'identity'}
    if token:value['Authorization'] = 'Bearer ' + token
    return value


def fetch(path, token=None):
    request = Request('https://api.github.com' + path, headers=headers(token))
    with build_opener(NoRedirect).open(request, timeout=15) as response:
        return json.load(response)


def create(token=None, *, limit=100):
    state = {'records': [], 'lock': threading.Lock(), 'active': 'setup', 'limit': limit}
    opener = build_opener(NoRedirect)
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            started = time.monotonic()
            with state['lock']:
                record = {'run': state['active'], 'path': self.path}
                state['records'].append(record)
                used = sum(bool(row.get('sent')) for row in state['records'])
            parsed = urlsplit(self.path)
            parts = unquote(parsed.path).split('/')
            allowed = (not parsed.scheme and not parsed.netloc and len(parts) >= 4 and parts[1] == 'repos'
                       and (parts[2].casefold(), parts[3].casefold()) in REPOSITORIES)
            if used >= limit:
                status, body, response_headers = 429, b'{"message":"Evaluation HTTP budget exhausted"}', {}
                record['blocked'] = 'HTTP_BUDGET'
            elif not allowed:
                status, body, response_headers = 403, b'{"message":"Evaluation is restricted to the two public repositories"}', {}
                record['blocked'] = 'PUBLIC_REPOSITORY_SCOPE'
            else:
                record['sent'] = True
                tick = time.monotonic()
                request = Request('https://api.github.com' + self.path, headers=headers(token))
                try:
                    with opener.open(request, timeout=15) as response:
                        status, body, response_headers = response.status, response.read(2*1024*1024+1), dict(response.headers)
                except HTTPError as error:
                    status, body, response_headers = error.code, error.read(2*1024*1024+1), dict(error.headers)
                except (URLError, TimeoutError, OSError):
                    status, body, response_headers = 502, b'{"message":"Upstream connection failed"}', {}
                record['upstreamSeconds'] = time.monotonic() - tick
            lowered = {key.lower(): value for key, value in response_headers.items()}
            record.update(status=status, bodyBytes=len(body), bodySHA256=hashlib.sha256(body).hexdigest(),
                rateRemaining=lowered.get('x-ratelimit-remaining'), seconds=time.monotonic() - started)
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            try:self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):record['clientDisconnected'] = True

        def log_message(self, *_):pass
    return ThreadingHTTPServer(('127.0.0.1', 0), Handler), state
