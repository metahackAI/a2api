"""Real-source catalog and scorer checks. No external HTTP/model calls."""

import importlib.util
from pathlib import Path
import unittest

from a2api import ToolSession

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / 'examples/real-github-evaluation'


def module(name):
    spec = importlib.util.spec_from_file_location('real_github_' + name, HERE / (name + '.py'))
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


class RealCatalogTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = module('catalog')
        # Read genuine pinned operations, importing only the small set for unit tests.
        from a2api.importers import OpenAPIImporter
        cls.source = OpenAPIImporter.from_file(cls.catalog.SOURCE_DIR / 'api.github.com.json.gz', namespace='github')
        cls.records = list(cls.source.iter_operations(set(cls.catalog.SMALL)))
        cls.app, cls.info = cls.catalog.create(cls.source, cls.records, 'small', 'https://api.github.com')

    async def test_real_operations_bind_to_original_source_and_input(self):
        self.assertEqual(self.info['count'], 8)
        self.assertEqual({x['operationId'] for x in self.info['mapping'].values()}, set(self.catalog.SMALL))
        self.assertEqual(set(self.app.describe('github.repos.get')['outputSchema']['properties']),
                         {'full_name', 'default_branch', 'stargazers_count', 'archived'})
        self.assertEqual(set(self.app.describe('github.repos.get_commit')['outputSchema']['properties']),
                         {'sha', 'stats', 'html_url'})
        for desc in self.app.descriptors():
            route = self.info['mapping'][desc['id']]
            self.assertEqual(route['method'], 'get')
            self.assertEqual(self.source.document['paths'][route['path']]['get']['operationId'], route['operationId'])
            self.assertNotIn('fixture.', desc['id'])
        baseline = module('baseline').BaselineSession(self.app, self.catalog.CONTEXT)
        selected = ToolSession(self.app, self.catalog.CONTEXT, naming='hash', flatten=False, hints='typed', search_limit=3)
        for query in ('github.repos.get', 'get commit', 'list branches'):
            left, right = await baseline.select(query), await selected.select(query)
            self.assertEqual(left, right)
            self.assertEqual(baseline.tools(), selected.tools())
        await baseline.call(left['selected'][0]['name'], {'unexpected': True})
        self.assertEqual(baseline.stats['invoke'], 0)


class AssessmentTests(unittest.TestCase):
    def setUp(self):
        self.scorer = module('assess')
        self.descriptors = {name: {'inputSchema': {'type': 'object'}, 'outputSchema': {}}
                            for name in ('repo', 'commit', 'branches', 'branch')}
        self.mapping = {name: {'operationId': op} for name, op in
                        [('repo', 'repos/get'), ('commit', 'repos/get-commit'),
                         ('branches', 'repos/list-branches'), ('branch', 'repos/get-branch')]}

    def call(self, name, data, **extra):
        path = {'owner': 'octocat', 'repo': 'Hello-World', **extra.pop('path', {})}
        return {'binding': {'id': name}, 'input': {'path': path, **extra},
                'output': {'status': 'succeeded', 'data': data}}

    def grade(self, case, calls, answer):
        import json
        return self.scorer.assess(self.scorer.CASES[case], {'calls': calls, 'answer': json.dumps(answer)}, self.descriptors, self.mapping)

    def test_chain_accepts_branch_ref_or_returned_sha_but_rejects_guessed_ref(self):
        repo = self.call('repo', {'full_name': 'octocat/Hello-World', 'default_branch': 'actual-branch'})
        answer = {'repository': 'octocat/Hello-World', 'defaultBranch': 'actual-branch',
                  'sha': 'head-sha', 'additions': 2, 'deletions': 1}
        data = {'sha': 'head-sha', 'stats': {'additions': 2, 'deletions': 1}}
        commit = self.call('commit', data, path={'ref': 'actual-branch'})
        self.assertTrue(self.grade(2, [repo, commit], answer)['passed'])
        qualified = self.call('commit', data, path={'ref': 'heads/actual-branch'})
        self.assertTrue(self.grade(2, [repo, qualified], answer)['passed'])
        via_sha = self.call('branch', {'commit': {'sha': 'returned-sha'}}, path={'branch': 'actual-branch'})
        other = self.call('commit', data, path={'ref': 'returned-sha'})
        self.assertTrue(self.grade(2, [repo, via_sha, other], answer)['passed'])
        wrong = self.call('commit', data, path={'ref': 'guessed-branch'})
        self.assertIn('REF_NOT_FROM_PRIOR_RESULT', self.grade(2, [repo, wrong], answer)['failures'])
        self.assertFalse(self.grade(2, [commit, repo], answer)['passed'])

    def test_branch_request_conditions_and_answer_values_both_matter(self):
        answer = {'repository': 'octocat/Hello-World', 'page': 1, 'perPage': 2, 'branches': ['a', 'b']}
        good = self.call('branches', [{'name': 'a'}, {'name': 'b'}], query={'page': 1, 'per_page': 2})
        self.assertTrue(self.grade(1, [good], answer)['passed'])
        wrong = self.call('branches', [{'name': 'a'}, {'name': 'b'}], query={'page': 1, 'per_page': 30})
        result = self.grade(1, [wrong], answer)
        self.assertTrue(result['factsMatched'])
        self.assertFalse(result['passed'])
        self.assertIn('PAGE_OR_COUNT_CONDITION', result['failures'])
        self.assertFalse(self.grade(1, [good], {**answer, 'branches': ['guessed']})['passed'])


class HoldoutAssessmentTests(unittest.TestCase):
    def setUp(self):
        from unittest.mock import patch
        import sys
        with patch.dict(sys.modules, {'assess': module('assess')}):self.scorer = module('holdout')
        self.cases = {case['id']: case for case in self.scorer.CASES}
        self.descriptors = {name: {'inputSchema': {'type': 'object'}, 'outputSchema': {}}
                            for name in ('repo', 'combined', 'statuses', 'forks')}
        self.mapping = {name: {'operationId': op} for name, op in
            [('repo', 'repos/get'), ('combined', 'repos/get-combined-status-for-ref'),
             ('statuses', 'repos/list-commit-statuses-for-ref'), ('forks', 'repos/list-forks')]}

    def call(self, name, data, *, path=None, query=None):
        args = {'path': {'owner': 'octocat', 'repo': 'Hello-World', **(path or {})}}
        if query is not None:args['query'] = query
        return {'binding': {'id': name}, 'input': args, 'output': {'status': 'succeeded', 'data': data}}

    def grade(self, name, calls, answer):
        import json
        return self.scorer.assess(self.cases[name], {'calls': calls, 'answer': json.dumps(answer)}, self.descriptors, self.mapping)

    def test_chain_uses_observed_branch_and_checks_exact_final_types(self):
        repo = self.call('repo', {'full_name': 'octocat/Hello-World', 'default_branch': 'actual'})
        combined = self.call('combined', {'state': 'pending', 'total_count': 0}, path={'ref': 'heads/actual'})
        answer = {'repository': 'octocat/Hello-World', 'defaultBranch': 'actual', 'state': 'pending', 'totalCount': 0}
        self.assertTrue(self.grade('default_combined_status', [repo, combined], answer)['passed'])
        guessed = self.call('combined', {'state': 'pending', 'total_count': 0}, path={'ref': 'guessed'})
        self.assertIn('REF_NOT_FROM_PRIOR_RESULT', self.grade('default_combined_status', [repo, guessed], answer)['failures'])
        self.assertFalse(self.grade('default_combined_status', [combined, repo], answer)['passed'])
        self.assertFalse(self.grade('default_combined_status', [repo, combined], {**answer, 'totalCount': False})['passed'])

    def test_empty_statuses_are_valid_but_page_and_count_are_not_repaired(self):
        repo = self.call('repo', {'full_name': 'octocat/Hello-World', 'default_branch': 'actual'})
        answer = {'repository': 'octocat/Hello-World', 'defaultBranch': 'actual', 'page': 1, 'perPage': 2, 'statuses': []}
        good = self.call('statuses', [], path={'ref': 'actual'}, query={'per_page': 2})
        self.assertTrue(self.grade('default_statuses_page', [repo, good], answer)['passed'])
        wrong = self.call('statuses', [], path={'ref': 'actual'}, query={'per_page': 30})
        self.assertIn('PAGE_OR_COUNT_CONDITION', self.grade('default_statuses_page', [repo, wrong], answer)['failures'])

    def test_fork_sort_filters_and_returned_names_are_checked(self):
        answer = {'repository': 'octocat/Hello-World', 'page': 1, 'perPage': 2, 'sort': 'newest', 'forks': ['someone/repo']}
        good = self.call('forks', [{'full_name': 'someone/repo'}], query={'page': 1, 'per_page': 2, 'sort': 'newest'})
        self.assertTrue(self.grade('forks_page', [good], answer)['passed'])
        bad = self.call('forks', [{'full_name': 'someone/repo'}], query={'page': 1, 'per_page': 2, 'sort': 'oldest'})
        self.assertIn('SORT_CONDITION', self.grade('forks_page', [bad], answer)['failures'])
