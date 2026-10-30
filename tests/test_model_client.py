"""A model HTTP fixture driving real MCP stdio; not live LLM evidence."""

from contextlib import ExitStack
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import json
from pathlib import Path
import sys
import unittest

from a2api.sample import running

HAS_MCP = importlib.util.find_spec('mcp') is not None
ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(HAS_MCP,'Install a2api[mcp]')
class ModelClientTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        spec=importlib.util.spec_from_file_location('model_client_example',ROOT/'examples/model-client/client.py')
        self.host=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.host)
        self.requests=[];self.secret='fixture-key-not-a-real-secret';self.mode='conversation'
        stack=ExitStack();self.addCleanup(stack.close)
        test=self
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                value=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                test.requests.append(value)
                test.assertEqual(self.headers.get('Authorization'),'Bearer '+test.secret)
                status=200
                index=len(test.requests)-1
                if test.mode=='http-error':
                    status=401;response={'error':{'message':test.secret}}
                else:
                    assistant={'role':'assistant','content':None,'reasoning':'reasoning must not be recorded'}
                    finish='tool_calls'
                    def tool(name,args):
                        assistant['tool_calls']=[{'id':'tool-'+str(index),'type':'function',
                            'function':{'name':name,'arguments':args if isinstance(args,str) else json.dumps(args)}}]
                    if test.mode=='echo-key':assistant['content']=test.secret;finish='stop'
                    elif test.mode=='bad-json':tool('a2api_invoke','{broken')
                    elif test.mode=='other-tool':tool('run_shell',{})
                    elif index==0:
                        text=json.dumps(value['tools'])
                        test.assertNotIn('orders.lookup',text)
                        tool('a2api_discover',{})
                    elif index==1:
                        found=json.loads(value['messages'][-1]['content'])
                        test.selected=next(x for x in found['capabilities'] if x['id']=='orders.lookup')
                        test.catalog=found['catalogVersion']
                        tool('a2api_describe',{'capabilityId':test.selected['id'],'version':test.selected['version']})
                    elif index==2:
                        test.assertEqual(json.loads(value['messages'][-1]['content'])['error']['code'],'INVALID_REQUEST')
                        tool('a2api_describe',{'id':test.selected['id'],'version':test.selected['version']})
                    elif index==3:
                        described=json.loads(value['messages'][-1]['content'])
                        test.assertIn('orderId',described['capability']['inputSchema']['properties'])
                        tool('a2api_invoke',{'id':test.selected['id'],'version':test.selected['version'],
                             'catalogVersion':test.catalog,'input':{'orderId':'ORD-1001'}})
                    else:
                        result=json.loads(value['messages'][-1]['content'])
                        assistant['content']=result['data']['orderState'];finish='stop'
                    response={'model':'fixture-model','choices':[{'message':assistant,'finish_reason':finish}],
                              'usage':{'prompt_tokens':10,'completion_tokens':5,'total_tokens':15}}
                body=json.dumps(response).encode()
                self.send_response(status);self.send_header('Content-Type','application/json')
                self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
            def log_message(self,*_):pass
        self.origin=stack.enter_context(running(ThreadingHTTPServer(('127.0.0.1',0),Handler)))

    async def run_host(self):
        return await self.host.execute([sys.executable,str(ROOT/'examples/native-orders/mcp_server.py'),'--source','python'],
            'ORD-1001 주문 상태를 조회해줘.',base_url=self.origin+'/v1',model='fixture-model',api_key=self.secret)

    async def test_real_stdio_forwards_arguments_and_structured_error_without_repair(self):
        run=await self.run_host()
        self.assertNotIn('hostError',run)
        self.assertEqual(run['answer'],'shipped')
        self.assertEqual(len(self.requests),5)
        self.assertEqual([call['tool'] for call in run['calls']],['a2api.discover','a2api.describe','a2api.describe','a2api.invoke'])
        self.assertEqual(set(run['calls'][1]['input']),{'capabilityId','version'})
        self.assertTrue(run['calls'][1]['isError'])
        self.assertEqual(run['calls'][-1]['output']['data']['orderId'],'ORD-1001')
        self.assertNotIn('reasoning must not be recorded',json.dumps(run))
        self.assertNotIn(self.secret,json.dumps(run))

    async def test_provider_failure_never_retries_or_records_raw_error_body(self):
        self.mode='http-error';run=await self.run_host()
        self.assertEqual(run['hostError']['code'],'MODEL_HTTP_401')
        self.assertEqual(len(self.requests),1)
        self.assertEqual(run['calls'],[])
        self.assertNotIn(self.secret,json.dumps(run))

    async def test_malformed_arguments_are_not_repaired_or_executed(self):
        self.mode='bad-json';run=await self.run_host()
        self.assertEqual(run['hostError']['code'],'INVALID_TOOL_ARGUMENT_JSON')
        self.assertEqual(run['calls'],[])
        self.assertEqual(len(self.requests),1)

    async def test_unlisted_tools_cannot_run(self):
        self.mode='other-tool';run=await self.run_host()
        self.assertEqual(run['hostError']['code'],'UNEXPECTED_TOOL')
        self.assertEqual(run['calls'],[])

    async def test_known_provider_key_is_redacted_even_if_returned_as_answer(self):
        self.mode='echo-key';run=await self.run_host()
        self.assertEqual(run['answer'],'[redacted-model-key]')
        self.assertNotIn(self.secret,json.dumps(run))
