"""Run a local a-commerce stack (metahackAI/a-commerce) for the a2api comparison, without Docker.

Prerequisites (once): PostgreSQL 17+ with pgvector, the `acom` database and roles from the repo's
infra/postgres/init.sql, keys from infra/scripts/gen-keys.sh, and release binaries built with the
repo's Rust toolchain (`cargo build --release -p acom-commerce -p acom-gateway -p acom-agent-svc -p xtask`).

python examples/acommerce/stack.py up      # migrate + demo seed, then commerce/worker/agent/gateway
python examples/acommerce/stack.py token admin --agent
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

LAB = Path(os.environ.get('A2API_LAB', '/home/khs/a2api-lab'))
REPO = Path(os.environ.get('ACOM_REPO', LAB / 'a-commerce'))
TARGET = Path(os.environ.get('ACOM_TARGET', LAB / 'acom-target' / 'release'))
LOGS = Path(__file__).resolve().parents[2] / 'artifacts' / 'acommerce' / 'logs'
MODEL_BASE_URL = os.environ.get('A2API_MODEL_BASE_URL', 'https://qwen-api-xgen.x2bee.com/v1')
MODEL = os.environ.get('A2API_MODEL', 'nvidia/Muse-Glimmer-30B-NVFP4')
GATEWAY, COMMERCE, AGENT, WORKER = 'http://127.0.0.1:7000', 'http://127.0.0.1:7001', 'http://127.0.0.1:7002', 'http://127.0.0.1:7003'


def env():
    values = dict(os.environ)
    for line in (REPO / '.env').read_text().splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            values.setdefault(key, value)
    values.update(ACOM_DEMO_MODE='true', ACOM_SEED='demo', RUST_LOG=values.get('RUST_LOG', 'warn'),
                  ACOM_LOG_FORMAT='json', GLIMMER_BASE_URL=MODEL_BASE_URL, GLIMMER_MODEL=MODEL)
    return values


def healthy(origin):
    try:
        with urlopen(origin + '/healthz', timeout=2) as response:
            return response.status == 200
    except (HTTPError, URLError, OSError):
        return False


@contextmanager
def running():
    """Migrate (and seed) once, start the four services, stop them on exit."""
    LOGS.mkdir(parents=True, exist_ok=True)
    variables = env()
    subprocess.run([str(TARGET / 'acom-commerce'), 'migrate'], cwd=REPO, env=variables, check=True,
                   stdout=(LOGS / 'migrate.log').open('w'), stderr=subprocess.STDOUT)
    children = []
    try:
        for name, args, origin in [('commerce', ['acom-commerce', 'serve'], COMMERCE),
                                   ('worker', ['acom-commerce', 'work'], WORKER),
                                   ('agent', ['acom-agent'], AGENT), ('gateway', ['acom-gateway'], GATEWAY)]:
            log = (LOGS / f'{name}.log').open('w')
            # A2API_AGENT_COMMERCE_URL points only the agent at another commerce origin (the a2api
            # gateway in a2api_gateway.py); every other service keeps the real one.
            started = dict(variables, ACOM_COMMERCE_URL=os.environ['A2API_AGENT_COMMERCE_URL']) if (
                name == 'agent' and os.environ.get('A2API_AGENT_COMMERCE_URL')) else variables
            children.append(subprocess.Popen([str(TARGET / args[0]), *args[1:]], cwd=REPO, env=started,
                                             stdout=log, stderr=subprocess.STDOUT))
            deadline = time.monotonic() + 60
            while not healthy(origin):
                if children[-1].poll() is not None or time.monotonic() > deadline:
                    raise RuntimeError(f'{name} did not start; see {LOGS / (name + ".log")}')
                time.sleep(0.3)
        yield {'gateway': GATEWAY, 'commerce': COMMERCE, 'agent': AGENT}
    finally:
        for child in reversed(children):
            child.terminate()
        for child in children:
            try:
                child.wait(timeout=10)
            except subprocess.TimeoutExpired:
                child.kill()


def token(persona, *, agent=False):
    """A local internal token for calling commerce directly (`cargo xtask dev-token`)."""
    args = [str(TARGET / 'xtask'), 'dev-token', persona] + (['--agent'] if agent else [])
    out = subprocess.run(args, cwd=REPO, env=env(), check=True, capture_output=True, text=True).stdout
    return out.strip().splitlines()[-1].strip()


def call(origin, method, path, body=None, *, bearer=None, headers=None, timeout=30):
    data = None if body is None else json.dumps(body).encode()
    request = Request(origin + path, data=data, method=method,
                      headers={**({'Content-Type': 'application/json'} if data else {}),
                               **({'Authorization': 'Bearer ' + bearer} if bearer else {}), **(headers or {})})
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read()
            return response.status, json.loads(raw) if raw else None
    except HTTPError as error:
        raw = error.read()
        error.close()
        try:
            return error.code, json.loads(raw)
        except ValueError:
            return error.code, raw.decode('utf-8', 'replace')[:500]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('up', help='run the stack in the foreground until interrupted')
    tok = sub.add_parser('token')
    tok.add_argument('persona')
    tok.add_argument('--agent', action='store_true')
    args = parser.parse_args()
    if args.command == 'token':
        print(token(args.persona, agent=args.agent))
        return
    with running() as origins:
        print(json.dumps(origins), flush=True)
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    sys.exit(main())
