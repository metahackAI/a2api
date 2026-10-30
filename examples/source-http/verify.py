"""Build/start actual language servers, then verify direct HTTP and real MCP stdio."""

import argparse
import asyncio
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import time

from mcp import Client
from mcp.client.stdio import StdioServerParameters

from a2api import ExecutionContext
from application import ROOT, application

REPO = ROOT.parents[1]
ARTIFACTS = REPO / 'artifacts/source-http'
CONTEXT = ExecutionContext('sample-user', 'sample-tenant', frozenset())


def tools():
    local = REPO / 'artifacts/toolchains/paths.json'
    paths = json.loads(local.read_text()) if local.exists() else {}
    result = {key: shutil.which(name) or paths.get(key) for key, name in
              [('java', 'java'), ('maven', 'mvn'), ('go', 'go'), ('cargo', 'cargo')]}
    env = dict(os.environ)
    if result['java']:env['JAVA_HOME'] = str(Path(result['java']).parent.parent)
    bins = [str(Path(p).parent) for p in result.values() if p]
    env['PATH'] = os.pathsep.join(bins + [env['PATH']])
    env['CARGO_HOME'] = str(REPO / 'artifacts/toolchains/cargo')
    env['GOCACHE'] = str(REPO / 'artifacts/toolchains/go-cache')
    env['CGO_ENABLED'] = '0'
    if paths.get('cc'):
        env['CARGO_TARGET_X86_64_UNKNOWN_LINUX_GNU_LINKER'] = paths['cc']
    return result, env


def build(language, paths, env):
    log = ARTIFACTS / (language + '-build.log')
    if language == 'spring':
        if not paths['java'] or not paths['maven']:raise RuntimeError('Install a JDK and Maven first.')
        command = [paths['maven'], '-q', '-Dmaven.repo.local=' + str(REPO / 'artifacts/maven-repository'), '-DskipTests', 'package']
        server = [paths['java'], '-jar', str(ROOT / 'spring/target/source-demo-0.1.0.jar')]
    elif language == 'go':
        if not paths['go']:raise RuntimeError('Install Go 1.22+ first.')
        executable = ARTIFACTS / 'go-server'
        command = [paths['go'], 'build', '-o', str(executable), '.'];server = [str(executable)]
    else:
        if not paths['cargo']:raise RuntimeError('Install Rust/Cargo first.')
        command = [paths['cargo'], 'build', '--quiet'];server = [str(ROOT / 'rust/target/debug/a2api-source-demo')]
    with log.open('w') as output:
        result = subprocess.run(command, cwd=ROOT / language, env=env, stdout=output, stderr=subprocess.STDOUT, timeout=600)
    if result.returncode:raise RuntimeError(f'{language} build failed; see {log}')
    return server


@contextmanager
def running(language, command, env):
    with socket.socket() as probe:
        probe.bind(('127.0.0.1', 0));port = probe.getsockname()[1]
    args = ['--server.address=127.0.0.1', '--server.port=' + str(port)] if language == 'spring' else [str(port)]
    with (ARTIFACTS / (language + '-server.log')).open('w') as log:
        process = subprocess.Popen(command + args, env=env, stdout=log, stderr=subprocess.STDOUT)
        try:
            deadline = time.monotonic() + 45
            while True:
                if process.poll() is not None:raise RuntimeError(f'{language} exited; see its server log')
                try:
                    with socket.create_connection(('127.0.0.1', port), timeout=0.2):break
                except OSError:
                    if time.monotonic() > deadline:raise RuntimeError('Server startup timeout')
                    time.sleep(0.1)
            yield f'http://127.0.0.1:{port}'
        finally:
            process.terminate()
            try:process.wait(timeout=5)
            except subprocess.TimeoutExpired:process.kill();process.wait()


async def exercise(call):
    records = []
    async def invoke(method, path, business, status=200):
        result = await call(method, path, business)
        assert result['status'] == 'succeeded', result
        assert result['httpStatus'] == status, result
        records.append({'method': method, 'route': path, 'httpStatus': result['httpStatus']})
        assert 'internalNote' not in json.dumps(result['data'])
        return result['data']
    initial = await invoke('GET', '/items/{id}', {'path': {'id': 'I-1'}})
    assert initial == {'id': 'I-1', 'name': 'original'}
    assert await invoke('HEAD', '/items/{id}', {'path': {'id': 'I-1'}}) is None
    item = await invoke('POST', '/items', {'body': {'name': 'created'}}, 201)
    selected = {'path': {'id': item['id']}}
    updated = await invoke('PUT', '/items/{id}', {**selected, 'body': {'name': 'replaced'}})
    assert updated['name'] == 'replaced'
    patched = await invoke('PATCH', '/items/{id}', {**selected, 'body': {'name': 'patched'}})
    assert patched['name'] == 'patched'
    found = await invoke('POST', '/items/search', {'body': {'q': 'patched'}})
    assert found == [patched]
    assert await invoke('DELETE', '/items/{id}', selected, 204) is None
    missing = await call('GET', '/items/{id}', selected)
    assert missing['error']['code'] == 'RESOURCE_NOT_FOUND', missing
    records.append({'method': 'GET', 'route': '/items/{id}', 'error': missing['error']['code']})
    return records


async def verify(language, origin):
    app, ids = application(language, origin)
    async def direct(method, route, business):return app.invoke(ids[(method, route)], business, context=CONTEXT)
    direct_result = await exercise(direct)
    params = StdioServerParameters(command=sys.executable,
        args=[str(ROOT / 'mcp_server.py'), '--language', language, '--origin', origin],
        env={'PYTHONPATH': os.environ['PYTHONPATH']} if 'PYTHONPATH' in os.environ else None)
    async with Client(params, read_timeout_seconds=20) as client:
        listing = await client.list_tools()
        invoke_tool = next(t for t in listing.tools if t.name == 'a2api.invoke')
        assert not invoke_tool.annotations.read_only_hint
        assert not invoke_tool.annotations.idempotent_hint
        assert all(identifier not in json.dumps(listing.model_dump(mode='json')) for identifier in ids.values())
        catalog = (await client.call_tool('a2api.discover', {})).structured_content
        for item in catalog['capabilities']:
            result = await client.call_tool('a2api.describe', {'id': item['id'], 'version': item['version']})
            assert result.structured_content['capability'] == app.describe(item['id'])
        async def mcp(method, route, business):
            result = await client.call_tool('a2api.invoke', {'id': ids[(method, route)], 'version': '0.1.0',
                'catalogVersion': catalog['catalogVersion'], 'input': business})
            return result.structured_content
        stdio_result = await exercise(mcp)
    return {'language': language, 'direct': direct_result, 'stdio': stdio_result, 'capabilities': len(ids),
            'writeEffectAdvertised': True, 'tools': [t.name for t in listing.tools]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--language', choices=['all', 'spring', 'go', 'rust'], default='all')
    args = parser.parse_args()
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    paths, env = tools()
    results = []
    for language in (['spring', 'go', 'rust'] if args.language == 'all' else [args.language]):
        print('Building and verifying ' + language, file=sys.stderr)
        command = build(language, paths, env)
        with running(language, command, env) as origin:
            results.append(asyncio.run(verify(language, origin)))
    report = {'checkedAt': datetime.now(timezone.utc).isoformat(), 'results': results,
              'scope': 'Synthetic source extraction + actual language HTTP processes + MCP stdio. No company API or LLM calls.'}
    (ARTIFACTS / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':main()
