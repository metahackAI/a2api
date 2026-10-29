"""Offline checks for the LLM example; synthetic host events are not LLM results."""

import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

import test_github_agent as github_fixture

HAS_MCP = github_fixture.HAS_MCP
EXAMPLE = github_fixture.EXAMPLE
demo = github_fixture.load_example('agent_demo')


def events(calls=(), answer='어느 저장소의 이슈를 조회할까요?', *, finished=True):
    values = [{'type': 'thread.started', 'thread_id': 'fixture'}, {'type': 'turn.started'}]
    for index, call in enumerate(calls):
        values.append({'type': 'item.completed', 'item': {'id': str(index), 'type': 'mcp_tool_call',
            'server': demo.SERVER, 'tool': call['tool'], 'arguments': call['input'],
            'result': {'structured_content': call['output']}, 'error': None, 'status': 'completed'}})
    values.append({'type': 'item.completed', 'item': {'id': 'answer', 'type': 'agent_message', 'text': answer}})
    if finished:
        values.append({'type': 'turn.completed', 'usage': {'input_tokens': 10, 'output_tokens': 5}})
    return '\n'.join(json.dumps(value, ensure_ascii=False) for value in values)


class AgentHostTests(unittest.TestCase):
    def test_questions_and_actual_history_do_not_include_grading_answers(self):
        case = demo.scenarios()[2]
        prior = {'question': 'previous real question', 'answer': 'previous real answer', 'calls': [],
                 'expected': 'HIDDEN_EXPECTATION', 'checks': 'HIDDEN_GRADE'}
        prompt = demo.prompt_for(case, prior)
        self.assertIn('previous real question', prompt)
        self.assertIn('previous real answer', prompt)
        self.assertNotIn('HIDDEN_', prompt)
        self.assertNotIn('"page": 2', prompt)
        for scenario in demo.scenarios():
            self.assertEqual(demo.prompt_for(scenario), scenario['question'])
            self.assertNotIn('github.', scenario['question'])
        command = demo.command_for('/codex', '/empty', 'http://127.0.0.1:1')
        self.assertIn('--ignore-user-config', command)
        self.assertIn('--ephemeral', command)
        self.assertIn('read-only', command)
        self.assertIn('shell_tool', command)
        self.assertNotIn('expected', ' '.join(command))

    def test_parse_public_events_omits_reasoning_and_retains_measured_usage(self):
        raw = events() + '\n' + json.dumps({'type': 'item.completed',
            'item': {'type': 'reasoning', 'text': 'PRIVATE-DO-NOT-RECORD'}})
        parsed = demo.parse_events(raw)
        self.assertTrue(parsed['completed'])
        self.assertEqual(parsed['usage'], {'input_tokens': 10, 'output_tokens': 5})
        self.assertNotIn('PRIVATE', json.dumps(parsed))
        self.assertIsNone(parsed['model'])
        self.assertTrue(demo.assess(demo.scenarios()[-1], parsed)['passed'])
        self.assertEqual(demo.assess(demo.scenarios()[-1], parsed)['answerReview'], 'required')

    def test_bad_or_incomplete_events_and_other_tools_are_not_success(self):
        for raw in ('not-json', '{}', json.dumps({'type': 'unsupported'}), events(finished=False),
                    events(answer=''), events() + '\n' + json.dumps({'type': 'turn.failed'}),
                    events() + '\n' + json.dumps({'type': 'item.completed', 'item': {'type': 'command_execution'}})):
            with self.subTest(raw=raw[-80:]):
                parsed = demo.parse_events(raw)
                self.assertFalse(demo.assess(demo.scenarios()[-1], parsed)['passed'])
        raw = events([{'tool': 'a2api.invoke', 'input': {}, 'output': {}}])
        parsed = demo.parse_events(raw.replace('structured_content', 'unrecognized_payload'))
        self.assertIn('HOST_EVENT_FORMAT', parsed['hostErrors'])

    def test_structured_application_error_is_not_a_transport_failure(self):
        call = {'tool': 'a2api.invoke', 'input': {}, 'output': {'status': 'failed',
            'error': {'code': 'RESOURCE_NOT_FOUND'}, 'completeness': {'complete': False}}}
        raw = events([call]).replace('"status": "completed"', '"status": "failed"')
        parsed = demo.parse_events(raw)
        self.assertEqual(parsed['hostErrors'], [])
        raw = events([{'tool': 'a2api.invoke', 'input': {}, 'output': {'data': {}}}])
        raw = raw.replace('"status": "completed"', '"status": "failed"')
        self.assertIn('MCP_TRANSPORT_ERROR', demo.parse_events(raw)['hostErrors'])

    def test_host_exit_unavailable_and_missing_previous_are_recorded_without_fabrication(self):
        for fake in [(1, events(), None), (0, events(), 'HOST_TIMEOUT')]:
            with patch.object(demo, 'execute', return_value=fake):
                result = demo.run_scenarios('/unused', selected='missing_input')
            self.assertFalse(result['passed'])
        with patch.object(demo, 'execute', side_effect=OSError('fixture unavailable')):
            result = demo.run_scenarios('/unused', selected='next_page')
        self.assertFalse(result['passed'])
        self.assertEqual([run['id'] for run in result['runs']], ['issues', 'next_page'])
        self.assertEqual(result['runs'][1]['checks']['failures'], ['previous_scenario_failed'])

    def test_timeout_terminates_host_and_child_process(self):
        with tempfile.TemporaryDirectory() as folder:
            pidfile = Path(folder) / 'child.pid'
            child = 'import signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); time.sleep(30)'
            script = ('import subprocess,sys,time,pathlib; '
                      'p=subprocess.Popen([sys.executable,"-c",' + repr(child) + ']); '
                      'pathlib.Path(' + repr(str(pidfile)) + ').write_text(str(p.pid)); time.sleep(30)')
            _, _, failure = demo.execute([sys.executable, '-c', script], '', 0.8)
            self.assertEqual(failure, 'HOST_TIMEOUT')
            pid = int(pidfile.read_text())
            status = Path(f'/proc/{pid}/stat')
            deadline = time.monotonic() + 1
            while status.exists() and status.read_text().split()[2] != 'Z' and time.monotonic() < deadline:
                time.sleep(0.01)
            self.assertTrue(not status.exists() or status.read_text().split()[2] == 'Z')

    def test_output_cap_and_nonzero_exit_are_observable(self):
        code, _, failure = demo.execute([sys.executable, '-c', 'import sys; sys.stdout.write("x"*4096)'], '', 3)
        self.assertEqual(code, 0)
        self.assertIsNone(failure)
        with patch.object(demo, 'MAX_OUTPUT', 100):
            _, text, failure = demo.execute([sys.executable, '-c', 'print("x"*4096)'], '', 3)
        self.assertEqual(failure, 'HOST_OUTPUT_LIMIT')
        self.assertLessEqual(len(text), 101)


@unittest.skipUnless(HAS_MCP, 'Install a2api[mcp] for actual stdio checks')
class AgentBehaviorStdioTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        github_fixture.GitHubExampleTests.setUpClass.__func__(cls)

    setUp = github_fixture.GitHubExampleTests.setUp

    async def test_all_scenarios_have_real_http_stdio_evidence_with_synthetic_host_events(self):
        from mcp import Client
        from mcp.client.stdio import StdioServerParameters
        params = StdioServerParameters(command=sys.executable,
            args=[str(EXAMPLE / 'mcp_server.py'), '--origin', self.origin])
        previous = None
        async with Client(params, read_timeout_seconds=15) as client:
            for case in demo.scenarios():
                with self.subTest(case=case['id']):
                    self.status = 404 if case['id'] == 'missing_repository' else 200
                    if case['id'] == 'repository':
                        self.issue_payload = []
                    else:
                        self.issue_payload = self.issues
                    calls = []
                    async def call(tool, arguments):
                        result = await client.call_tool(tool, arguments)
                        calls.append({'tool': tool, 'input': arguments, 'output': result.structured_content})
                        return result.structured_content
                    if case['expected']['invocations']:
                        catalog = await call('a2api.discover', {'query': 'github'})
                        for expectation in case['expected']['invocations']:
                            await call('a2api.describe', {'id': expectation['id'], 'version': '0.1.0'})
                            await call('a2api.invoke', {'id': expectation['id'], 'version': '0.1.0',
                                'catalogVersion': catalog['catalogVersion'], 'input': expectation['input']})
                    parsed = demo.parse_events(events(calls))
                    assessed = demo.assess(case, parsed, previous if case.get('previous') else None)
                    self.assertTrue(assessed['passed'], assessed)
                    self.assertEqual(assessed['answerReview'], 'required')
                    if case['id'] == 'issues':
                        previous = parsed
                    if case['id'] == 'next_page':
                        self.assertEqual(calls[-1]['input']['input']['page'], 2)
                        # Replay may reuse an actual, still-valid discovered descriptor.
                        parsed['calls'] = parsed['calls'][-1:]
                        self.assertTrue(demo.assess(case, parsed, previous)['passed'])
                    if case['id'] == 'repository':
                        self.assertEqual(calls[-1]['output']['data']['items'], [])
                    if case['id'] == 'missing_repository':
                        self.assertEqual(calls[-1]['output']['error']['code'], 'RESOURCE_NOT_FOUND')
                    # Missing input is not a successful backend read or fake empty page.
                    if case['id'] == 'missing_input':
                        self.assertEqual(calls, [])
        self.assertEqual(len(self.requests), 5)
        issues = demo.scenarios()[1]
        invented = demo.parse_events(events([previous['calls'][-1]]))
        self.assertIn('invoke_without_discovery_and_description', demo.assess(issues, invented)['failures'])
        # A correct tool name/arguments with an empty success body must still fail.
        broken = json.loads(json.dumps(previous))
        broken['calls'][-1]['output']['data'] = {}
        self.assertIn('business_output_schema_or_scope_mismatch', demo.assess(issues, broken)['failures'])
        broken = json.loads(json.dumps(previous))
        broken['calls'][-1]['input']['input']['page'] = 9
        self.assertIn('expected_invocation_missing', demo.assess(issues, broken)['failures'])


if __name__ == '__main__':
    unittest.main()
