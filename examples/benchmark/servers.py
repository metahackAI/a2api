"""Build and run the generated benchmark servers (Spring, Go, Rust) and the Python HTTP server."""

from __future__ import annotations

from contextlib import contextmanager
import http.server
import importlib.util
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import threading
import time
from urllib.parse import parse_qs, urlsplit
from urllib.request import Request, urlopen

from domain import operations

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
GENERATED = REPO / 'artifacts/benchmark/generated'
BUILD = REPO / 'artifacts/benchmark/build'
LANGUAGES = ('python', 'spring', 'go', 'rust')


def toolchain():
    paths = {key: shutil.which(name) for key, name in [('java', 'java'), ('maven', 'mvn'), ('go', 'go'), ('cargo', 'cargo')]}
    env = dict(os.environ, CGO_ENABLED='0', CARGO_TARGET_DIR=str(BUILD / 'cargo-target'))
    return paths, env


def build(scale, language, *, log_dir=BUILD / 'logs'):
    """Compile one generated server; returns the command that starts it (port appended)."""
    paths, env = toolchain()
    source = GENERATED / scale / language
    log_dir.mkdir(parents=True, exist_ok=True)
    if language == 'spring':
        command = [paths['maven'], '-q', '-Dmaven.repo.local=' + str(REPO / 'artifacts/maven-repository'), '-DskipTests', 'package']
        server = [paths['java'], '-Xshare:auto', '-jar', str(source / f'target/bench-{scale}-1.0.0.jar'), '--server.address=127.0.0.1']
    elif language == 'go':
        executable = BUILD / f'go-{scale}'
        command = [paths['go'], 'build', '-o', str(executable), '.']
        server = [str(executable)]
    elif language == 'rust':
        command = [paths['cargo'], 'build', '--quiet']
        server = [str(BUILD / f'cargo-target/debug/a2api-bench-{scale}')]
    else:
        raise ValueError('python runs in-process')
    with (log_dir / f'{language}-{scale}.log').open('w') as output:
        result = subprocess.run(command, cwd=source, env=env, stdout=output, stderr=subprocess.STDOUT, timeout=1800)
    if result.returncode:
        raise RuntimeError(f'{language} {scale} build failed; see {log_dir / (language + "-" + scale + ".log")}')
    return server, env


def free_port():
    with socket.socket() as probe:
        probe.bind(('127.0.0.1', 0))
        return probe.getsockname()[1]


@contextmanager
def process(language, command, env, *, log_dir=BUILD / 'logs'):
    port = free_port()
    args = ['--server.port=' + str(port)] if language == 'spring' else [str(port)]
    with (log_dir / f'{language}-server-{port}.log').open('w') as log:
        child = subprocess.Popen(command + args, env=env, stdout=log, stderr=subprocess.STDOUT)
        try:
            deadline = time.monotonic() + 90
            origin = f'http://127.0.0.1:{port}'
            while True:
                if child.poll() is not None:
                    raise RuntimeError(f'{language} server exited; see {log.name}')
                try:
                    with urlopen(origin + '/__admin/state', timeout=2) as response:
                        response.read()
                    break
                except OSError:
                    if time.monotonic() > deadline:
                        raise RuntimeError('server startup timeout')
                    time.sleep(0.2)
            yield origin
        finally:
            child.terminate()
            try:
                child.wait(timeout=10)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait()


def python_service(scale):
    """Import the generated Python module (fresh store per import name)."""
    path = GENERATED / scale / 'python/bench_service.py'
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    name = f'bench_service_{scale}'
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _typed(item, raw):
    if raw == '':
        return None
    if item is None or item.kind == 'integer':
        try:
            return int(raw)
        except ValueError:
            raise ValueError('invalid integer') from None
    if item.kind == 'boolean':
        if raw not in ('true', 'false'):
            raise ValueError('invalid boolean')
        return raw == 'true'
    return raw


def python_http(scale):
    """A ThreadingHTTPServer over the same BenchStore used by the Python capabilities."""
    from pystore import StoreError
    store = python_service(scale).STORE
    routes = []
    for resource, op in operations(scale):
        method, path = resource.route(op)
        routes.append((method, path.split('/'), resource, op))

    class Handler(http.server.BaseHTTPRequestHandler):
        protocol_version = 'HTTP/1.1'

        def log_message(self, *args):
            pass

        def reply(self, status, payload=None):
            body = b'' if payload is None else json.dumps(payload, ensure_ascii=False).encode()
            self.send_response(status)
            if payload is not None:
                self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def handle_any(self):
            url = urlsplit(self.path)
            length = int(self.headers.get('Content-Length') or 0)
            raw = self.rfile.read(length) if length else b''
            if url.path == '/__admin/reset' and self.command == 'POST':
                store.reset()
                return self.reply(204)
            if url.path == '/__admin/state' and self.command == 'GET':
                return self.reply(200, store.state())
            parts = url.path.split('/')
            for method, template, resource, op in routes:
                if method != self.command or len(template) != len(parts):
                    continue
                if all(t == p or t.startswith('{') for t, p in zip(template, parts)):
                    values = {t[1:-1]: p for t, p in zip(template, parts) if t.startswith('{')}
                    break
            else:
                return self.reply(404, {'error': 'route not found'})
            try:
                query = {key: value[-1] for key, value in parse_qs(url.query, keep_blank_values=True).items()}
                body = json.loads(raw) if raw else None
                if op in ('create', 'update', 'search') and not isinstance(body, dict):
                    raise ValueError('JSON object body required')
                if op == 'list':
                    filters = {name: _typed(resource.field(name), query.get(name, '')) for name in resource.filters}
                    result = store.list(resource.key, filters, _typed(None, query.get('page', '')), _typed(None, query.get('limit', '')))
                elif op == 'get':
                    result = store.get(resource.key, values['id'])
                elif op == 'create':
                    return self.reply(201, store.create(resource.key, body))
                elif op == 'update':
                    result = store.update(resource.key, values['id'], body)
                elif op == 'delete':
                    store.delete(resource.key, values['id'])
                    return self.reply(204)
                elif op == 'search':
                    result = store.search(resource.key, body.get('query'), body.get('limit'))
                elif op == 'cancel':
                    result = store.cancel(resource.key, values['id'])
                else:
                    result = store.tracking(resource.key, values['id'])
                return self.reply(200, result)
            except StoreError as error:
                return self.reply(error.status, {'error': error.message})
            except ValueError as error:
                return self.reply(400, {'error': str(error)})

        do_GET = do_POST = do_PATCH = do_DELETE = handle_any

    return Handler


@contextmanager
def python_server(scale):
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), python_http(scale))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_address[1]}'
    finally:
        server.shutdown()
        server.server_close()


def admin(origin, action):
    method = 'POST' if action == 'reset' else 'GET'
    with urlopen(Request(origin + '/__admin/' + action, method=method), timeout=10) as response:
        body = response.read()
    return json.loads(body) if body else None
