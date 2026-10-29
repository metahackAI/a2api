"""Two public GitHub reads, using the pinned OpenAPI and small Python DTOs."""

from pathlib import Path
from typing import Literal, TypedDict

from a2api import A2APIError, Application, ExecutionContext, HTTPDeployment, capability, convert
from a2api.importers import OpenAPIImporter, load_openapi

SOURCE = Path(__file__).with_name('api.github.com.json.gz')
API_VERSION = '2026-03-10'
PUBLIC_CONTEXT = ExecutionContext('public-github-reader', 'public-github', frozenset())
REPOSITORY = 'github.repository.get'
ISSUES = 'github.issues.list'


class RepositorySummary(TypedDict):
    fullName: str
    description: str | None
    url: str
    language: str | None
    stars: int
    defaultBranch: str
    archived: bool


class IssueSummary(TypedDict):
    number: int
    title: str
    state: Literal['open', 'closed']
    url: str
    updatedAt: str
    kind: Literal['issue', 'pull_request']


class IssuePage(TypedDict):
    repository: str
    page: int
    perPage: int
    state: Literal['open', 'closed', 'all']
    items: list[IssueSummary]


_REPO_INPUT = {
    'type': 'object', 'additionalProperties': False, 'required': ['owner', 'repo'],
    'properties': {'owner': {'type': 'string', 'minLength': 1}, 'repo': {'type': 'string', 'minLength': 1}},
}
_ISSUES_INPUT = {
    **_REPO_INPUT,
    'properties': {**_REPO_INPUT['properties'],
        'state': {'type': 'string', 'enum': ['open', 'closed', 'all'], 'default': 'open'},
        'page': {'type': 'integer', 'minimum': 1, 'default': 1},
        'perPage': {'type': 'integer', 'minimum': 1, 'maximum': 20, 'default': 5}},
}


def _data(result):
    if result['status'] != 'succeeded':
        error = result['error']
        raise A2APIError(error['code'], error['detail'], status=error['status'], issues=error.get('issues'))
    return result['data']


def create_app(origin: str = 'https://api.github.com') -> Application:
    """origin is host configuration, never an agent argument. No credentials loaded."""
    document, _ = load_openapi(SOURCE)
    # Local, explicit corrections for the pinned source (docs/14): current GitHub
    # removed singular assignee; nullable state_reason must also permit null in enum.
    # Keep every other raw constraint, and never edit the bundled source file.
    issue = document['components']['schemas']['issue']
    issue['required'].remove('assignee')
    issue['properties']['state_reason']['enum'].append(None)
    raw = convert(OpenAPIImporter(document, namespace='github_source'), operations={
        'repos/get': {'effect': 'read'},
        'issues/list-for-repo': {'effect': 'read'},
    }, deployment=HTTPDeployment(origin, headers={
        'User-Agent': 'a2api-github-example', 'X-GitHub-Api-Version': API_VERSION,
    }))

    @capability(id=REPOSITORY, effect='read', input_schema=_REPO_INPUT)
    def get_repository(owner: str, repo: str, *, context: ExecutionContext) -> RepositorySummary:
        """Get selected metadata of one public GitHub repository."""
        value = _data(raw.invoke('github_source.repos.get', {'path': {'owner': owner, 'repo': repo}}, context=context))
        return {'fullName': value['full_name'], 'description': value['description'], 'url': value['html_url'],
                'language': value['language'], 'stars': value['stargazers_count'],
                'defaultBranch': value['default_branch'], 'archived': value['archived']}

    @capability(id=ISSUES, effect='read', input_schema=_ISSUES_INPUT)
    def list_issues(owner: str, repo: str, state: Literal['open', 'closed', 'all'] = 'open',
                    page: int = 1, perPage: int = 5, *, context: ExecutionContext) -> IssuePage:
        """Get one page of public GitHub issues and PRs, newest updated first; kind distinguishes them."""
        values = _data(raw.invoke('github_source.issues.list_for_repo', {
            'path': {'owner': owner, 'repo': repo},
            'query': {'state': state, 'page': page, 'per_page': perPage, 'sort': 'updated', 'direction': 'desc'},
        }, context=context))
        return {'repository': f'{owner}/{repo}', 'page': page, 'perPage': perPage, 'state': state,
                'items': [{'number': item['number'], 'title': item['title'], 'state': item['state'],
                           'url': item['html_url'], 'updatedAt': item['updated_at'],
                           'kind': 'pull_request' if 'pull_request' in item else 'issue'} for item in values]}

    # Only these DTO wrappers enter the agent catalog. Full schemas stay internal.
    return Application([get_repository, list_issues])
