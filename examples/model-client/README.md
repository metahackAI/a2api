# 실제 모델 → a2api MCP → API

작은 Chat Completions 호환 호스트와 세 언어 합성 서버의 고정 검증 예제다.

1. 저장소 루트에서 `python -m pip install -e ".[mcp]"`를 설치한다.
2. `A2API_MODEL_BASE_URL`, `A2API_MODEL`을 자신의 endpoint/model로 설정한다.
3. `python examples/model-client/client.py --question "ORD-1001 주문 상태를 알려줘." -- python examples/native-orders/mcp_server.py --source openapi`를 실행한다.

source 서버 검증에는 `[source,mcp]`와 언어 툴체인이 필요하다. `python examples/model-client/verify_sources.py`는 같은 7개 질문을 실제 모델에서 실행하고 ignored artifacts에 기록한다. 일반 테스트에서는 모델 서비스를 호출하지 않는다.

[설치·설정·오류·결과 읽기](../../docs/22-quickstart-and-model.ko.md), [경량 wire 명세](../../docs/20-call-protocol.ko.md), [검색 metadata](../../docs/21-discovery-metadata.ko.md)를 참고한다.
