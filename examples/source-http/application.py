"""Host selection for the synthetic examples, not an automatic effect classifier."""

from pathlib import Path

from a2api import HTTPDeployment, convert
from a2api.importers import SpringSourceImporter, GoSourceImporter, RustSourceImporter

ROOT = Path(__file__).resolve().parent
IMPORTERS = {'spring': SpringSourceImporter, 'go': GoSourceImporter, 'rust': RustSourceImporter}
SOURCES = {'spring': ROOT / 'spring/src/main/java', 'go': ROOT / 'go', 'rust': ROOT / 'rust/src'}
SEARCH = {
    ('GET', '/items/{id}'): ('항목 ID로 현재 이름을 조회한다.', ['항목', '조회', '이름', 'get']),
    ('HEAD', '/items/{id}'): ('본문 없이 항목의 존재 여부를 확인한다.', ['항목', '존재', '확인', 'head']),
    ('POST', '/items'): ('이름을 받아 새 항목을 생성하고 실제 ID를 반환한다.', ['항목', '생성', '만들기', 'create']),
    ('PUT', '/items/{id}'): ('지정한 항목의 이름을 전체 교체한다.', ['항목', '전체', '교체', 'replace']),
    ('PATCH', '/items/{id}'): ('지정한 항목의 이름을 부분 수정한다.', ['항목', '부분', '수정', 'patch']),
    ('POST', '/items/search'): ('이름에 검색어가 포함된 항목을 검색한다.', ['항목', '이름', '검색', 'search']),
    ('DELETE', '/items/{id}'): ('지정한 ID의 항목을 삭제한다.', ['항목', '삭제', 'delete', 'remove']),
}


def application(language, origin, *, search_metadata=True):
    source = IMPORTERS[language].from_directory(SOURCES[language], namespace=language)
    records = list(source.iter_operations())
    unsupported = [r.summary() for r in records if r.status != 'imported']
    if unsupported or source.diagnostics:
        raise ValueError(unsupported or source.diagnostics)
    options, ids = {}, {}
    for item in records:
        key = (item.method, item.path)
        if key in ids:raise ValueError('Ambiguous example route')
        ids[key] = item.id
        effect = 'read' if item.method in ('GET', 'HEAD') or key == ('POST', '/items/search') else 'write'
        options[item.operation_id] = {'effect': effect}
        if search_metadata:
            summary, keywords = SEARCH[key]
            options[item.operation_id].update(summary=summary, keywords=keywords)
        if item.method != 'HEAD' and item.path != '/items/search' and item.method != 'DELETE':
            options[item.operation_id]['select'] = ['id', 'name']
    return convert(source, operations=options, deployment=HTTPDeployment(origin)), ids
