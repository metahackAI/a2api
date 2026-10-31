"""Benchmark harness: generator, executors and checkers with a scripted fake model.

Uses only the generated Python implementation (no JDK/Go/Rust). A fake model is
not evidence of real LLM performance; it checks the harness bookkeeping.
"""

import asyncio
import importlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / 'examples/benchmark'


class BenchmarkHarnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(BENCH))
        cls.temp = tempfile.TemporaryDirectory()
        cls.generate = importlib.import_module('generate')
        cls.generate.generate(Path(cls.temp.name))
        cls.servers = importlib.import_module('servers')
        cls.patcher = patch.object(cls.servers, 'GENERATED', Path(cls.temp.name))
        cls.patcher.start()
        for name in ('application', 'evaluate', 'modes', 'tasks'):
            module = importlib.import_module(name)
            if hasattr(module, 'GENERATED'):
                setattr(module, 'GENERATED', Path(cls.temp.name))
        cls.evaluate = importlib.import_module('evaluate')
        cls.modes = importlib.import_module('modes')
        cls.tasks = importlib.import_module('tasks')
        cls.application = importlib.import_module('application')

    @classmethod
    def tearDownClass(cls):
        cls.patcher.stop()
        sys.modules.pop('bench_service_small', None)
        cls.temp.cleanup()
        sys.path.remove(str(BENCH))

    def scripted(self, steps):
        """Chat stub: each step is a list of (name, arguments) tool calls or a final answer string."""
        script = list(steps)
        seen = []

        def chat(base_url, model, messages, tools, **_):
            seen.append({'tools': [tool['function']['name'] for tool in tools], 'messages': len(messages)})
            step = script.pop(0)
            usage = {'prompt_tokens': 100, 'completion_tokens': 10, 'total_tokens': 110}
            if isinstance(step, str):
                return {'choices': [{'finish_reason': 'stop', 'message': {'content': step}}], 'usage': usage}
            calls = [{'id': str(i), 'type': 'function', 'function': {'name': name, 'arguments': json.dumps(args)}}
                     for i, (name, args) in enumerate(step)]
            return {'choices': [{'finish_reason': 'tool_calls', 'message': {'content': None, 'tool_calls': calls}}], 'usage': usage}
        return chat, seen

    def run_task(self, executor, task_id, steps, origin):
        item = next(item for item in self.tasks.TASKS if item['id'] == task_id)
        chat, seen = self.scripted(steps)
        self.servers.admin(origin, 'reset')
        before = self.servers.admin(origin, 'state')
        with patch.object(self.evaluate, 'chat', side_effect=chat):
            run = asyncio.run(self.evaluate.run_task(executor, item['question'], base_url='http://unused', model='m'))
        after = self.servers.admin(origin, 'state')
        return run, self.tasks.assess(item, run['answer'], before, after, run['calls']), seen

    def test_generator_covers_every_operation_and_python_store_matches_spec(self):
        spec = json.loads((Path(self.temp.name) / 'small/openapi.json').read_text())
        operations = [op for path in spec['paths'].values() for op in path.values()]
        self.assertEqual(len(operations), 19)
        for language in ('spring', 'go', 'rust'):
            self.assertTrue((Path(self.temp.name) / 'small' / language).exists())
        app, ops = self.application.converted('small', 'python')
        self.assertEqual(len(app.descriptors()), 19)
        self.assertEqual(set(ops.values()), {f'{r.key}.{op}' for r, op in self.servers.operations('small')})

    def test_three_modes_execute_and_checkers_score_the_same_task(self):
        with self.servers.python_server('small') as origin:
            spec = json.loads((Path(self.temp.name) / 'small/openapi.json').read_text())
            final = '```json\n{"status": "paid", "totalAmount": 87000}\n```'
            run, result, seen = self.run_task(self.modes.SpecTools('small', spec, origin), 'D1',
                                              [[('getOrder', {'id': 'ORD-1003'})], final], origin)
            self.assertTrue(result['passed'], result)
            self.assertEqual(run['calls'], [{'op': 'orders.get', 'status': 200, 'ok': True}])
            self.assertEqual(len(seen[0]['tools']), 19)
            run, result, seen = self.run_task(self.modes.SpecPrompt('small', spec, origin), 'D1',
                                              [[('http_request', {'method': 'GET', 'path': '/orders/ORD-1003'})], final], origin)
            self.assertTrue(result['passed'], result)
            self.assertEqual(seen[0]['tools'], ['http_request'])
            app, ops = self.application.converted('small', 'python')
            run, result, seen = self.run_task(self.modes.A2API(app, ops, max_tool_bytes=16000), 'D1',
                                              [[('shop_orders_get', {'id': 'ORD-1003'})], final], origin)
            self.assertTrue(result['passed'], result)
            # 19 functions (~8.5KB) exceed auto's all_bytes: the host pre-searches the question.
            self.assertEqual(run['setup']['strategy'], 'search')
            self.assertEqual(seen[0]['tools'][0], 'a2api_search')
            self.assertIn('shop_orders_get', seen[0]['tools'])
            self.assertLessEqual(len(seen[0]['tools']), 9)
            self.assertNotIn('internalNote', json.dumps(run['toolCalls']))

    def test_writes_missing_input_and_failures_are_scored_from_state_and_calls(self):
        with self.servers.python_server('small') as origin:
            app, ops = self.application.converted('small', 'python')
            make = lambda: self.modes.A2API(app, ops, max_tool_bytes=16000)
            _, result, _ = self.run_task(make(), 'D3', [[('shop_tickets_create', {'customerId': 'C-004', 'subject': '배송 지연 문의',
                                                          'priority': 'high'})], '{"ticketId": "T-9009"}'], origin)
            self.assertTrue(result['passed'], result)
            _, result, _ = self.run_task(make(), 'D3', [[('shop_tickets_create', {'customerId': 'C-004', 'subject': '배송 지연 문의',
                                                          'priority': 'high'})] * 2, '{"ticketId": "T-9009"}'], origin)
            self.assertIn('CREATE_COUNT', result['failures'])
            _, result, _ = self.run_task(make(), 'D10', ['어떤 주문을 취소할까요?'], origin)
            self.assertTrue(result['passed'], result)
            _, result, _ = self.run_task(make(), 'D10', [[('shop_orders_cancel', {'id': 'ORD-1010'})], '취소했습니다.'], origin)
            self.assertIn('CALLED_WITHOUT_REQUIRED_INPUT', result['failures'])
            self.assertIn('UNEXPECTED_WRITE', result['failures'])
            run, result, _ = self.run_task(make(), 'D9', [[('shop_shipments_tracking', {'id': 'SHP-503'})],
                                                          '{"trackingAvailable": false, "events": []}'], origin)
            self.assertTrue(result['passed'], result)
            self.assertEqual(json.loads(run['toolCalls'][0]['result'])['error']['code'], 'UPSTREAM_UNAVAILABLE')
            self.assertIn('hint', json.loads(run['toolCalls'][0]['result']))

    def test_context_overflow_is_a_recorded_failure(self):
        def overflow(*args, **kwargs):
            raise self.evaluate.ModelError('CONTEXT_OVERFLOW')
        with self.servers.python_server('small') as origin:
            spec = json.loads((Path(self.temp.name) / 'small/openapi.json').read_text())
            with patch.object(self.evaluate, 'chat', side_effect=overflow):
                run = asyncio.run(self.evaluate.run_task(self.modes.SpecPrompt('small', spec, origin), 'q',
                                                         base_url='http://unused', model='m'))
            self.assertEqual(run['hostError'], 'CONTEXT_OVERFLOW')
            self.assertEqual(run['modelRequests'], 0)

    def test_answer_extraction_and_diff(self):
        self.assertEqual(self.tasks.answer_json('설명\n{"a": 1}\n끝'), {'a': 1})
        self.assertEqual(self.tasks.answer_json('```json\n{"a": {"b": 2}}\n```'), {'a': {'b': 2}})
        self.assertIsNone(self.tasks.answer_json('JSON 없음'))
        diff = self.tasks.changes({'x': [{'id': '1', 'v': 1}]}, {'x': [{'id': '1', 'v': 2}, {'id': '2', 'v': 0}]})
        self.assertEqual(set(diff), {('x', '1'), ('x', '2')})
        self.assertTrue(self.tasks.fingerprint('holdout').startswith('sha256:'))


if __name__ == '__main__':
    unittest.main()
