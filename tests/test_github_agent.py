"""The public GitHub example against deterministic HTTP and real MCP stdio."""

from contextlib import ExitStack
from copy import deepcopy
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from urllib.parse import parse_qs, urlsplit

from jsonschema import Draft202012Validator

from a2api.importers import OpenAPIImporter
from a2api.importers.schema_conversion import local_reference
from a2api.sample import running

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / 'examples/github-openapi'


def load_example(name):
    spec = importlib.util.spec_from_file_location(name, EXAMPLE / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


example = load_example('agent_app')
HAS_MCP = importlib.util.find_spec('mcp') is not None


class GitHubExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = OpenAPIImporter.from_file(example.SOURCE, namespace='fixtures')
        def response(path):
            media = source.document['paths'][path]['get']['responses']['200']['content']['application/json']
            value = next(iter(media['examples'].values()))
            if '$ref' in value:
                value = local_reference(source.document, value['$ref'], 'example')
            return deepcopy(value['value'])
        cls.repository = response('/repos/{owner}/{repo}')
        # Upstream example omits required language (see example-drift.json).
        # Repair only the test payload; leave the pinned specification unchanged.
        cls.repository['language'] = None
        cls.repository['source']['language'] = None
        cls.repository['description'] = None
        cls.repository['temp_clone_token'] = 'DO-NOT-RETURN'
        pull = response('/repos/{owner}/{repo}/issues')[0]
        issue = deepcopy(pull)
        del issue['pull_request']
        issue['number'] = 1348
        issue['body'] = 'DO-NOT-RETURN'
        cls.issues = [issue, pull]

    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        self.requests = []
        self.status = 200
        self.repo_payload = deepcopy(self.repository)
        self.issue_payload = deepcopy(self.issues)
        test = self
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                test.requests.append((self.path, dict(self.headers)))
                payload = (test.issue_payload if urlsplit(self.path).path.endswith('/issues') else test.repo_payload)
                if test.status != 200:
                    payload = {'message': 'DO-NOT-RETURN'}
                body = json.dumps(payload).encode()
                self.send_response(test.status)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(body)))
                # The example must not invent pagination totals from this header.
                self.send_header('Link', '<https://fixture.invalid/?page=3>; rel="next"')
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *_):
                pass
        self.origin = stack.enter_context(running(ThreadingHTTPServer(('127.0.0.1', 0), Handler)))
        self.app = example.create_app(self.origin)

    def invoke(self, identifier, **arguments):
        return self.app.invoke(identifier, {'owner': 'octocat', 'repo': 'Hello-World', **arguments},
                               context=example.PUBLIC_CONTEXT)

    def test_only_small_wrappers_exposed_and_no_reads_during_conversion_or_description(self):
        self.assertEqual({d['id'] for d in self.app.descriptors()}, {example.REPOSITORY, example.ISSUES})
        for descriptor in self.app.descriptors():
            self.assertEqual(set(descriptor), {'id', 'version', 'summary', 'effects', 'inputSchema', 'outputSchema'})
            for schema in ('inputSchema', 'outputSchema'):
                Draft202012Validator.check_schema(descriptor[schema])
            text = json.dumps(descriptor)
            for excluded in ('github_source', 'context', 'Authorization', 'temp_clone_token', 'body', 'permissions'):
                self.assertNotIn(excluded, text)
        self.assertEqual(self.requests, [])
        self.assertEqual(self.invoke('github_source.repos.get')['error']['code'], 'NOT_FOUND')
        self.assertEqual(self.requests, [])

    def test_selected_repository_fields_and_issue_page_with_pr_kind(self):
        repo = self.invoke(example.REPOSITORY)
        self.assertEqual(repo['status'], 'succeeded', repo)
        self.assertEqual(set(repo['data']), {'fullName', 'description', 'url', 'language', 'stars', 'defaultBranch', 'archived'})
        self.assertIsNone(repo['data']['description'])
        self.assertIsNone(repo['data']['language'])
        issues = self.invoke(example.ISSUES, state='all', page=2, perPage=2)
        self.assertEqual(issues['status'], 'succeeded', issues)
        self.assertEqual({k: v for k, v in issues['data'].items() if k != 'items'},
                         {'repository': 'octocat/Hello-World', 'state': 'all', 'page': 2, 'perPage': 2})
        self.assertEqual([item['kind'] for item in issues['data']['items']], ['issue', 'pull_request'])
        for item in issues['data']['items']:
            self.assertEqual(set(item), {'number', 'title', 'state', 'url', 'updatedAt', 'kind'})
        self.assertNotIn('DO-NOT-RETURN', json.dumps([repo, issues]))
        self.assertEqual(len(self.requests), 2)
        query = parse_qs(urlsplit(self.requests[-1][0]).query)
        self.assertEqual(query, {'state': ['all'], 'page': ['2'], 'per_page': ['2'], 'sort': ['updated'], 'direction': ['desc']})
        for _, headers in self.requests:
            headers = {name.lower(): value for name, value in headers.items()}
            self.assertEqual(headers['x-github-api-version'], example.API_VERSION)
            self.assertEqual(headers['user-agent'], 'a2api-github-example')
            self.assertNotIn('authorization', headers)

    def test_empty_page_is_valid_and_defaults_are_applied(self):
        self.issue_payload = []
        result = self.invoke(example.ISSUES)
        self.assertEqual(result['data'], {'repository': 'octocat/Hello-World', 'page': 1, 'perPage': 5, 'state': 'open', 'items': []})
        self.assertEqual(result['completeness'], {'complete': True, 'scope': 'single_api_response'})
        self.assertEqual(len(self.requests), 1)

    def test_invalid_inputs_make_no_http_request(self):
        for arguments in ({'owner': ''}, {'repo': ''}, {'perPage': 0}, {'perPage': 21}, {'page': 0},
                          {'state': 'unknown'}, {'origin': 'https://other.invalid'}, {'context': {}},
                          {'headers': {'Authorization': 'secret'}}):
            with self.subTest(arguments=arguments):
                result = self.invoke(example.ISSUES, **arguments)
                self.assertEqual(result['error']['code'], 'INVALID_INPUT', result)
        self.assertEqual(self.requests, [])

    def test_backend_errors_are_preserved_without_payload_or_retry(self):
        for status, code in [(403, 'PERMISSION_DENIED'), (404, 'RESOURCE_NOT_FOUND'), (429, 'RATE_LIMITED')]:
            self.status = status
            for identifier in (example.REPOSITORY, example.ISSUES):
                with self.subTest(status=status, identifier=identifier):
                    before = len(self.requests)
                    result = self.invoke(identifier)
                    self.assertEqual(result['error']['code'], code, result)
                    self.assertEqual(result['error']['status'], status)
                    self.assertEqual(result['completeness'], {'complete': False})
                    self.assertNotIn('DO-NOT-RETURN', json.dumps(result))
                    self.assertEqual(len(self.requests), before + 1)

    def test_full_raw_schema_validated_before_field_projection(self):
        # These fields are not in the public DTO, but their invalid raw types must fail.
        self.repo_payload['forks_count'] = 'DO-NOT-RETURN'
        self.issue_payload[0]['locked'] = 'DO-NOT-RETURN'
        for identifier in (example.REPOSITORY, example.ISSUES):
            result = self.invoke(identifier)
            self.assertEqual(result['error']['code'], 'SCHEMA_MISMATCH', result)
            self.assertNotIn('data', result)
            self.assertNotIn('DO-NOT-RETURN', json.dumps(result))
        self.assertEqual(len(self.requests), 2)

    def test_only_documented_issue_schema_adjustments_allow_current_api_shape(self):
        del self.issue_payload[0]['assignee']
        self.issue_payload[0]['state_reason'] = None
        result = self.invoke(example.ISSUES)
        self.assertEqual(result['status'], 'succeeded', result)
        # Optional presence retains its type check; enum still rejects unknown values.
        for field, value in [('assignee', 17), ('state_reason', 'unknown')]:
            with self.subTest(field=field):
                previous = deepcopy(self.issue_payload[0])
                self.issue_payload[0][field] = value
                result = self.invoke(example.ISSUES)
                self.assertEqual(result['error']['code'], 'SCHEMA_MISMATCH', result)
                self.issue_payload[0] = previous

    @unittest.skipUnless(HAS_MCP, 'Install a2api[mcp] for actual stdio verification')
    def test_example_verifier_runs_direct_and_real_stdio_against_http(self):
        import anyio
        verifier = load_example('verify_agent')
        async def run():
            return await verifier.verify('octocat', 'Hello-World', origin=self.origin, state='all', page=2, per_page=2)
        report = anyio.run(run)
        self.assertEqual(report['direct'], report['stdio'])
        self.assertEqual(report['httpReads'], 4)
        self.assertEqual(len(self.requests), 4)
        self.assertEqual(report['tools'], ['a2api.discover', 'a2api.describe', 'a2api.invoke'])
        self.assertNotIn('DO-NOT-RETURN', json.dumps(report))
        for path, _ in self.requests:
            if urlsplit(path).path.endswith('/issues'):
                self.assertEqual(parse_qs(urlsplit(path).query)['page'], ['2'])


if __name__ == '__main__':
    unittest.main()
