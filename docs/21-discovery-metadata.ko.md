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

검색은 query의 공백 분리·대소문자 정리·문자열 포함 여부를 사용하는 기존 방식이다. 일치 단어 수가 높은 항목을 먼저 반환하고 ID/버전으로 순서를 고정한다. 등록한 “주문”, “배송”은 찾을 수 있지만 모든 한국어 활용형·동의어·문장의 의미를 해석하는 검색기는 아니다. 원본 데이터의 I-1이나 새 항목 이름은 업무 인자이며, 그 값을 keywords에 넣지 않았다면 검색 결과가 없어도 정상이다. 빈 query는 노출한 카탈로그를 페이지로 조회한다.

metadata 변경도 검색 결과와 순위에 영향을 주므로 catalogVersion/cursor를 구분한다. 기존 cursor를 바뀐 metadata에 재사용하면 INVALID_CURSOR다. invoke의 버전 검사·입력/원본/출력 검증·credential/context 연결은 그대로 유지한다.

합성 소스 예제는 `examples/source-http/application.py`의 작은 한국어 설명 목록을 사용한다. `mcp_server.py --plain-descriptions`는 원본 source 제목으로 비교하는 검증 옵션이다. 기본값은 metadata 적용이며, 업무 API 선택과 효과는 두 모드에서 같다.

검사: `python -m unittest discover -s tests -p test_discovery_metadata.py -v`. 실제 모델 비교와 그 한계는 [완료 증거](evidence/protocol-completion.json)에 기록한다.
