# 실제 모델 → a2api MCP → API

작은 Chat Completions 호환 호스트와 세 언어 합성 서버의 고정 검증 예제다.

1. 저장소 루트에서 `python -m pip install -e ".[mcp]"`를 설치한다.
2. `A2API_MODEL_BASE_URL`, `A2API_MODEL`을 자신의 endpoint/model로 설정한다.
3. `python examples/model-client/client.py --question "ORD-1001 주문 상태를 알려줘." -- python examples/native-orders/mcp_server.py --source openapi`를 실행한다.

source 서버 검증에는 `[source,mcp]`와 언어 툴체인이 필요하다. `python examples/model-client/verify_sources.py`는 같은 7개 질문을 실제 모델에서 실행하고 ignored artifacts에 기록한다. 일반 테스트에서는 모델 서비스를 호출하지 않는다.

필요한 입력 schema만 모델 도구로 제공하려면 `--binding selected`를 추가한다. 호스트가 기능을 알면 `--known legacy.getorder --known legacy.getshipment --no-search`로 모델 탐색 없이 호출할 수 있다. 생략하면 모델 검색 후 호스트가 기존 discover/describe를 처리하고 다음 요청의 tools를 갱신한다. 기본 `--binding generic`은 기존 세 도구 방식이다. [도구 선택·예산·재사용 규칙과 명령](../../docs/24-selected-tools.ko.md)을 참고한다.

[설치·설정·오류·결과 읽기](../../docs/22-quickstart-and-model.ko.md), [경량 wire 명세](../../docs/20-call-protocol.ko.md), [검색 metadata](../../docs/21-discovery-metadata.ko.md)를 참고한다.
