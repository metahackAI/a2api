"""Discovery quality, privacy and snapshot behavior for explicit metadata."""

import importlib.util
import json
from pathlib import Path
import unittest

from a2api import A2APIError, Application, ExecutionContext, HTTPDeployment, capability, convert
from a2api.importers import OpenAPIImporter
from a2api.mcp_application import DirectApplications

CONTEXT = ExecutionContext('alice', 'test', frozenset())
ROOT = Path(__file__).resolve().parents[1]


def source():
    return OpenAPIImporter({'openapi':'3.1.0','info':{'title':'items','version':'1'},'paths':{
        '/items':{'get':{'operationId':'getItems','summary':'List items','description':'재고 확인용 목록',
            'tags':['상품'],'responses':{'200':{'description':'ok','content':{'application/json':{'schema':{
                'type':'object','properties':{'id':{'type':'string'}},'required':['id']}}}}}}}}},namespace='sample')


class DiscoveryMetadataTests(unittest.TestCase):
    def app(self, **options):
        return convert(source(),operations={'getItems':{'effect':'read',**options}},deployment=HTTPDeployment('http://127.0.0.1:1'))

    def test_openapi_descriptions_tags_and_override_are_searchable_without_schema_growth(self):
        app = self.app(summary='항목 이름을 조회한다.',keywords=['사용자검색어','고유-index-marker'])
        wire = DirectApplications(app)
        for query in ['항목 조회','재고','상품','사용자검색어','GETITEMS']:
            with self.subTest(query=query):self.assertEqual(len(wire.discover(query,CONTEXT)['capabilities']),1)
        self.assertEqual(wire.discover('등록하지않은말',CONTEXT)['capabilities'],[])
        descriptor = app.describe('sample.getitems')
        self.assertEqual(descriptor['summary'],'항목 이름을 조회한다.')
        self.assertNotIn('고유-index-marker',json.dumps(descriptor,ensure_ascii=False))
        self.assertNotIn('keywords',descriptor)
        self.assertEqual(set(descriptor),{'id','version','summary','effects','inputSchema','outputSchema'})
        self.assertEqual(self.app().describe('sample.getitems')['summary'],'List items')

    def test_native_keywords_rank_matches_and_remain_host_only(self):
        def lookup(value: str) -> str:return value
        first=capability(id='sample.first',effect='read',summary='첫 항목',keywords=['주문','배송'])(lookup)
        other=capability(id='sample.other',effect='read',summary='다른 항목',keywords=['주문'])(lookup)
        app=Application([other,first]);wire=DirectApplications(app)
        found=wire.discover('주문 배송',CONTEXT)['capabilities']
        self.assertEqual([item['id'] for item in found],['sample.first','sample.other'])
        self.assertEqual(found[0]['matchedTerms'],['주문','배송'])
        self.assertNotIn('keywords',app.describe('sample.first'))
        copy=app.search_metadata();copy.clear()
        self.assertEqual(len(wire.discover('배송',CONTEXT)['capabilities']),1)

    def test_changed_keywords_invalidate_catalog_and_cursor_without_changing_descriptor(self):
        def app(term):
            def echo(value: str) -> str:return value
            return Application([capability(id='sample.'+key,effect='read',keywords=[term])(echo) for key in ('one','two')])
        before_app,after_app=app('첫검색어'),app('새검색어')
        self.assertEqual(before_app.descriptors(),after_app.descriptors())
        before,after=DirectApplications(before_app),DirectApplications(after_app)
        self.assertNotEqual(before.version,after.version)
        cursor=before.discover('',CONTEXT,limit=1)['nextCursor']
        with self.assertRaises(A2APIError) as caught:after.discover('',CONTEXT,limit=1,cursor=cursor)
        self.assertEqual(caught.exception.code,'INVALID_CURSOR')

    def test_invalid_annotations_are_rejected_and_keyword_lists_detached(self):
        for value in ['',42,'x'*1001]:
            with self.subTest(summary=value),self.assertRaises(A2APIError):self.app(summary=value)
        for value in ['not-a-list',[''],[42],['x'*81],['x']*33]:
            with self.subTest(keywords=value),self.assertRaises(A2APIError):self.app(keywords=value)
            def echo(value: str) -> str:return value
            with self.assertRaises(A2APIError):capability(id='sample.echo',effect='read',keywords=value)(echo)
        terms=['항목'];app=self.app(keywords=terms);terms.append('뒤늦은변경')
        self.assertEqual(DirectApplications(app).discover('뒤늦은변경',CONTEXT)['capabilities'],[])

    @unittest.skipUnless(importlib.util.find_spec('tree_sitter_go'),'Install a2api[source]')
    def test_source_importer_uses_same_small_metadata_settings(self):
        from a2api.importers import GoSourceImporter
        source=GoSourceImporter.from_directory(ROOT/'examples/source-http/go',namespace='go')
        app=convert(source,operations={'getItem':{'effect':'read','summary':'항목 이름 조회','keywords':['실물항목']}},
            deployment=HTTPDeployment('http://127.0.0.1:1'))
        self.assertEqual(len(DirectApplications(app).discover('실물항목',CONTEXT)['capabilities']),1)


@unittest.skipUnless(importlib.util.find_spec('mcp'),'Install a2api[mcp]')
class MetadataMCPTests(unittest.IsolatedAsyncioTestCase):
    async def test_three_tool_listing_is_identical_with_many_private_search_terms(self):
        from mcp import Client
        from a2api.mcp_bridge import create_mcp_server
        def echo(value: str) -> str:return value
        listings=[]
        for terms in [[],['private-marker-'+str(i) for i in range(32)]]:
            app=Application([capability(id='sample.echo',effect='read',keywords=terms)(echo)])
            async with Client(create_mcp_server(app,CONTEXT),read_timeout_seconds=10) as client:
                listing=(await client.list_tools()).model_dump(mode='json')
                self.assertNotIn('private-marker',json.dumps(listing))
                listings.append(listing)
        self.assertEqual(listings[0],listings[1])
