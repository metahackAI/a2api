"""FastAPI routes and Pydantic models read statically (ast; nothing is imported)."""

from pathlib import Path
import tempfile
import unittest

from a2api import HTTPDeployment, convert
from a2api.importers import FastAPISourceImporter
from a2api.ir import thaw

FILES = {
    'app/__init__.py': '',
    'app/models.py': '''
from typing import List, Optional
from pydantic import BaseModel, Field

def to_camel(text: str) -> str:
    return "".join(word if index == 0 else word.capitalize() for index, word in enumerate(text.split("_")))

class Base(BaseModel):
    class Config:
        alias_generator = to_camel

class IdMixin(BaseModel):
    id_: int = Field(0, alias="id")

class Article(IdMixin, Base):
    title: str
    tag_list: List[str] = []
    favorites_count: int

class ArticleOut(Article):
    tag_list: List[str] = Field(..., alias="tags")

class ArticleIn(Base):
    title: str = Field(..., min_length=1)
    body_text: Optional[str] = None
''',
    'app/deps.py': '''
from fastapi import Depends, Path, Query

def current_user(token: str = Depends(read_token)):
    return token

def article_by_slug(slug: str = Path(..., min_length=1), user=Depends(current_user)):
    return slug

def filters(tag: Optional[str] = None, limit: int = Query(20, ge=1)):
    return tag, limit
''',
    'app/routes.py': '''
from fastapi import APIRouter, Body, Depends, Response
from starlette import status
from app.models import ArticleIn, ArticleOut
from app import deps

router = APIRouter()

@router.get("", response_model=List[ArticleOut], name="articles:list")
async def list_articles(found=Depends(deps.filters)):
    ...

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ArticleOut)
async def create(article: ArticleIn = Body(..., embed=True, alias="article"), user=Depends(deps.current_user)):
    ...

@router.delete("/{slug}", status_code=204, response_class=Response, dependencies=[Depends(deps.article_by_slug)])
async def remove():
    ...
''',
    'app/main.py': '''
from fastapi import FastAPI
from app.routes import router as articles

class Settings(BaseSettings):
    api_prefix: str = "/api"

def build():
    application = FastAPI()
    application.include_router(articles, prefix="/articles")
    outer = APIRouter(prefix="/v1")
    return application
app = build()
''',
}


class FastAPIImporterTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        for name, body in FILES.items():
            Path(self.folder.name, name).parent.mkdir(parents=True, exist_ok=True)
            Path(self.folder.name, name).write_text(body)
        self.importer = FastAPISourceImporter(self.folder.name, namespace='blog')
        self.ops = {item.operation_id: item for item in self.importer.iter_operations()}

    def tearDown(self):
        self.folder.cleanup()

    def test_routes_prefixes_and_statuses(self):
        self.assertEqual({op.status for op in self.ops.values()}, {'imported'})
        self.assertEqual({(op.method, op.path) for op in self.ops.values()},
                         {('GET', '/articles'), ('POST', '/articles'), ('DELETE', '/articles/{slug}')})
        self.assertEqual(thaw(self.ops['remove'].operation.output_schema)['properties']['httpStatus']['enum'], [204])
        self.assertEqual(self.ops['list_articles'].title, 'articles:list')

    def test_inputs_from_signature_and_dependencies(self):
        listing = thaw(self.ops['list_articles'].operation.input_schema)['properties']['query']
        self.assertEqual(listing['properties']['limit'], {'type': 'integer', 'minimum': 1, 'default': 20})
        self.assertEqual(listing['properties']['tag'], {'type': 'string'})
        self.assertEqual(listing['required'], [])
        body = thaw(self.ops['create'].operation.input_schema)['properties']['body']
        self.assertEqual(body['required'], ['article'])
        self.assertEqual(body['properties']['article']['required'], ['title'])
        self.assertEqual(set(body['properties']['article']['properties']), {'title', 'bodyText'})
        path = thaw(self.ops['remove'].operation.input_schema)['properties']['path']
        self.assertEqual(path['properties']['slug']['minLength'], 1)
        self.assertEqual(self.ops['create'].diagnostics[0]['code'], 'CONTEXT_DEPENDENCY')

    def test_outputs_follow_aliases_mixins_and_overrides(self):
        output = thaw(self.ops['create'].operation.output_schema)['properties']['result']
        self.assertEqual(set(output['properties']), {'id', 'title', 'tags', 'favoritesCount'})
        listing = thaw(self.ops['list_articles'].operation.output_schema)['properties']['result']
        self.assertEqual(listing['type'], 'array')

    def test_converted_operations_describe_without_executing_project_code(self):
        app = convert(self.importer, operations={'list_articles': {'effect': 'read'}},
                      deployment=HTTPDeployment('http://127.0.0.1:1'))
        self.assertIn('limit', app.describe('blog.list_articles')['inputSchema']['properties']['query']['properties'])


if __name__ == '__main__':
    unittest.main()
