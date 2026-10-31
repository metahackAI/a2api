"""Python write and async capabilities share the direct-call protocol."""

import asyncio
import inspect
from typing import TypedDict
import unittest

from a2api import Application, ExecutionContext, ToolSession, capability
from a2api.errors import A2APIError
from a2api.mcp_application import DirectApplications

CALLER = ExecutionContext('alice', 'tenant-a', frozenset())


class Note(TypedDict):
    id: str
    text: str


def build():
    notes: dict[str, Note] = {}
    calls = []

    @capability(id='notes.create', effect='write', keywords=['note', 'create'])
    def create_note(text: str, *, context: ExecutionContext) -> Note:
        """Create a note and return its new ID."""
        calls.append(('create', context.actor))
        note = {'id': 'N-%d' % (len(notes) + 1), 'text': text}
        notes[note['id']] = note
        return note

    @capability(id='notes.get', effect='read', keywords=['note', 'get'])
    async def get_note(id: str) -> Note:
        """Get one note by ID."""
        await asyncio.sleep(0)
        if id not in notes:
            raise A2APIError('RESOURCE_NOT_FOUND', 'Note does not exist.', status=404)
        return notes[id]

    @capability(id='notes.delete', effect='write')
    async def delete_note(id: str) -> None:
        """Delete one note."""
        if notes.pop(id, None) is None:
            raise A2APIError('RESOURCE_NOT_FOUND', 'Note does not exist.', status=404)

    return Application([create_note, get_note, delete_note]), notes, calls


class PythonEffectTests(unittest.TestCase):
    def test_write_and_async_functions_describe_and_invoke(self):
        app, notes, calls = build()
        self.assertEqual(app.describe('notes.create')['effects'], {'kind': 'write'})
        self.assertEqual(app.describe('notes.get')['effects'], {'kind': 'read'})
        created = app.invoke('notes.create', {'text': 'hello'}, context=CALLER)
        self.assertEqual(created['data'], {'id': 'N-1', 'text': 'hello'})
        self.assertEqual(calls, [('create', 'alice')])
        self.assertEqual(app.invoke('notes.get', {'id': 'N-1'}, context=CALLER)['data']['text'], 'hello')
        missing = app.invoke('notes.get', {'id': 'N-9'}, context=CALLER)
        self.assertEqual(missing['error']['code'], 'RESOURCE_NOT_FOUND')
        self.assertEqual(app.invoke('notes.delete', {'id': 'N-1'}, context=CALLER)['data'], None)
        self.assertEqual(notes, {})
        self.assertTrue(DirectApplications(app).writable)

    def test_async_handler_completes_inside_a_running_event_loop(self):
        app, _, _ = build()
        app.invoke('notes.create', {'text': 'loop'}, context=CALLER)

        async def inside():
            return app.invoke('notes.get', {'id': 'N-1'}, context=CALLER)
        self.assertEqual(asyncio.run(inside())['data']['text'], 'loop')

    def test_decorated_async_function_stays_awaitable(self):
        @capability(id='values.echo', effect='read')
        async def echo(value: str) -> str:
            """Echo a value."""
            return value
        self.assertTrue(inspect.iscoroutinefunction(echo))
        self.assertEqual(asyncio.run(echo('direct')), 'direct')
        self.assertEqual(Application([echo]).invoke('values.echo', {'value': 'x'}, context=CALLER)['data'], 'x')

    def test_tool_session_calls_python_write_without_retry(self):
        app, notes, calls = build()

        async def run():
            session = ToolSession(app, CALLER)
            await session.prime(['notes.create'])
            name = session.tools(include_search=False)[0]['function']['name']
            first = await session.call(name, {'text': 'once'})
            invalid = await session.call(name, {'text': 7})
            return first, invalid
        first, invalid = asyncio.run(run())
        self.assertEqual(first['status'], 'succeeded')
        self.assertEqual(invalid['error']['code'], 'INVALID_INPUT')
        self.assertEqual(len(notes), 1)
        self.assertEqual(len(calls), 1)


if __name__ == '__main__':
    unittest.main()
