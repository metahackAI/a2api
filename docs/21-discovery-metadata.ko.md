# 작은 설명·검색 설정

기존 변환 설정에 선택적으로 summary와 keywords를 지정한다. 별도 파일·검토 단계는 필요 없다. 기준 wire와 descriptor의 6개 필드는 [경량 프로토콜](20-call-protocol.ko.md)을 유지한다.

```python
app = convert(source, operations={
    "getOrder": {
        "effect": "read",
        "select": ["orderId", "orderState", "shipmentIds"],
        "summary": "주문 번호로 주문 상태와 배송 번호를 조회한다.",
        "keywords": ["주문", "배송", "조회", "order"],
    },
}, deployment=deployment)
```

위 코드는 기존 importer와 HTTPDeployment를 연결하는 설정 부분이다. 전체 실행은 [시작 문서](22-quickstart-and-model.ko.md)의 기존 주문·배송 예제를 사용한다. effect와 연결 정보는 계속 호스트가 명시한다.

- summary를 생략하면 원본 제목을 유지한다. 지정하면 공백이 아닌 1~1,000자 문자열이어야 하며 기존 descriptor.summary 값을 대체한다.
- keywords는 선택적인 list/tuple이며 최대 32개, 각 문자열은 공백이 아닌 최대 80자다. 앞뒤 공백과 중복을 정리해 서버 메모리 검색에 보관한다. None/생략은 추가 검색어 없음이다.
- importer가 이미 읽은 원본 제목, OpenAPI operation 설명·태그도 검색에 사용한다. 원본 description 전체를 모델 descriptor에 붙이지 않는다. 알 수 없는 업무 의미를 자동 생성하지 않는다.
- 선택된 operation만 검색한다. keywords는 tools/list·discover·describe에 새 필드로 노출하지 않는다. matchedTerms에는 요청한 검색어 중 일치한 단어가 표시될 수 있다. 검색 metadata는 비밀 저장소가 아니며 credential을 넣지 않는다.

Python 조회 함수도 같은 호스트 검색어를 선택적으로 등록한다. 기존 summary/docstring과 함수 실행 규칙은 유지한다.

```python
@capability(id="orders.lookup", effect="read", keywords=["주문", "조회"])
def lookup(orderId: str) -> str:
    """주문 번호로 주문 상태를 조회한다."""
    return existing_service_lookup(orderId)
```

위 existing_service_lookup은 호스트의 기존 구현이다. Python write나 async 지원을 추가한 예제가 아니다.

직접 `ConvertedAPI`/`Application`의 경량 카탈로그는 ID·원본 operationId/함수 이름·summary·명시적 keywords·공개 입출력 field를 구분한다. 표기 경계와 흔한 단어를 정규화하고, 질의 개념의 주요 field 포함 정도를 먼저 본 뒤 필드별 가중치·단어 빈도로 정렬한다. 긴 본문은 낮은 비중이고 반복 횟수로 점수를 올리지 않는다. 배열 항목/가까운 자식은 root field보다 낮은 근거다. 순환/복합 schema는 보수적으로 건너뛰며 데이터 값이나 업무 관계를 추측하지 않는다.

완전한 capability ID는 그 ID의 버전들만 반환한다. prefix 이웃을 섞지 않는다. 원본 alias는 `/`, `.`, `_`, `-`, camelCase 차이를 처리하되 서로 다른 namespace나 실제 버전을 임의로 하나로 확정하지 않는다. 점수가 같으면 ID/버전으로 순서를 고정한다. 기존 한글 부분 일치·명시적 keywords도 유지하지만 한국어 활용형/동의어 전체를 해석하는 검색기는 아니다.

field와 원본 alias는 서버 index에만 있다. descriptor 6필드와 MCP tools/list에는 추가하지 않는다. `app.search_metadata()`의 기존 tuple 값은 유지하며, 호스트 내부에서는 `structured=True`로 역할을 구분할 수 있다. 원본 데이터의 I-1이나 새 항목 이름은 업무 인자이며, 그 값을 keywords에 넣지 않았다면 검색 결과가 없어도 정상이다. 빈 query는 노출한 카탈로그를 페이지로 조회한다. 선택적 전체 manifest Runtime의 기존 검색/정책 엔진을 이번에 교체하지 않는다.

metadata 변경도 검색 결과와 순위에 영향을 주므로 catalogVersion/cursor를 구분한다. 기존 cursor를 바뀐 metadata에 재사용하면 INVALID_CURSOR다. invoke의 버전 검사·입력/원본/출력 검증·credential/context 연결은 그대로 유지한다.

검색 revision도 catalog fingerprint에 포함해 이전 순서의 cursor를 새 순서에 재사용하지 않는다. 호스트의 조건부 다음 페이지와 범위는 [a2api-tools/0.2](24-selected-tools.ko.md), [이번 구현 범위](29-search-improvement.ko.md)를 따른다.

합성 소스 예제는 `examples/source-http/application.py`의 작은 한국어 설명 목록을 사용한다. `mcp_server.py --plain-descriptions`는 원본 source 제목으로 비교하는 검증 옵션이다. 기본값은 metadata 적용이며, 업무 API 선택과 효과는 두 모드에서 같다.

검사: `python -m unittest discover -s tests -p test_discovery_metadata.py -v`. 실제 모델 비교와 그 한계는 [완료 증거](evidence/protocol-completion.json)에 기록한다.
