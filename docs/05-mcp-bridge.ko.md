# MCP 브리지와 에이전트 연결

구현일: 2026-10-28 · 공식 Python MCP SDK 2.3.0으로 검증 · stdio transport

P0-3에서 변환 객체와 Python 함수 연결 및 공통 schema 경량화를 추가했다. 새 앱의 연결·실행 예제와 비용 측정은 [경량 MCP 사용 안내](13-lightweight-mcp.ko.md)를 참고한다.

## 설치와 재현

Python 3.11+ 가상환경에서 저장소 루트를 기준으로 실행한다.

```bash
python -m pip install -e ".[mcp]"
python -m a2api mcp-demo
python -m unittest discover -s tests -v
```

MCP는 선택 의존성이다. `a2api[mcp]`는 공식 SDK `mcp>=2.3,<3`을 설치한다. 기본 `a2api` 설치와 기존 HTTP 기능은 MCP SDK 없이 사용할 수 있다. MCP SDK가 없으면 MCP 테스트는 skip되므로 전체 검증에는 extra 설치가 필요하다.

`mcp-demo`는 SDK의 `Client`와 `StdioServerParameters`로 `python -m a2api mcp` 프로세스를 실행한다. 실제 stdio로 도구 목록을 조회하고 discover → describe → invoke를 호출한다. 서버는 별도 loopback HTTP 샘플 backend를 자동으로 시작하며 종료 시 정리한다.

기본 샘플의 핵심 결과는 다음과 같다.

```json
{
  "transport": "stdio",
  "tools": ["a2api.discover", "a2api.describe", "a2api.invoke"],
  "isError": false,
  "invoke": {
    "status": "succeeded",
    "data": {
      "orderId": "ORD-1001",
      "orderState": "shipped",
      "shipments": [
        {"shipmentId": "SHP-501", "status": "in_transit"},
        {"shipmentId": "SHP-502", "status": "delivered"}
      ]
    },
    "stats": {"backendCalls": 3}
  }
}
```

위 결과는 핵심 필드만 발췌한 것이다. 실제 응답에는 도착 예정 시각, 조회 기준 시각, 전체 계약 버전, 실행 ID, 근거, 표시 모델도 포함된다.

## MCP 호스트 설정

호스트가 실행할 서버 명령은 다음과 같다.

```bash
python -m a2api mcp --sample-user alice
```

stdout은 MCP 메시지 전용이다. 서버 명령을 터미널에서 직접 실행하면 호스트의 stdin 메시지를 기다린다. 사람이 결과를 확인할 때는 `mcp-demo`를 사용한다.

`mcpServers` 형식을 지원하는 호스트에서는 [설정 예시](../examples/mcp-stdio.json)의 `command`를 **a2api[mcp]가 설치된 가상환경 Python의 절대 경로**로 바꿔 등록한다. 호스트별 실제 설정 위치·형식은 해당 호스트 문서를 따른다. 패키지로 설치했다면 저장소 작업 디렉터리나 PYTHONPATH 지정 없이 실행할 수 있다.

이 명령은 샘플 서버다. `--sample-user`는 `alice`, `bob`, `limited`를 지원하며 기본값은 `alice`다. 호스트가 시작 옵션으로 결정하는 데모 identity이고 실제 사용자 인증 방식은 아니다. stdio 서버 하나에는 고정된 ExecutionContext 하나를 사용한다.

```bash
python -m a2api mcp-demo --sample-user bob --order-id ORD-2001
python -m a2api mcp-demo --order-id ORD-1002
```

첫 명령은 Bob의 주문과 배송 한 건을 조회한다. 두 번째 명령은 배송이 없는 정상 주문을 조회한다. `limited`는 필요한 scope가 부족해 발견 가능한 capability가 없으며 데모는 실패 코드로 종료한다.

## 도구 계약

`tools/list`에는 다음 세 도구를 항상 같은 순서로 노출한다. 검색이나 상세 조회가 도구 목록을 변경하지 않는다. capability의 노출과 실행은 고정된 호스트 context의 권한으로 제한한다.

| 도구 | arguments | 결과 |
|---|---|---|
| `a2api.discover` | 선택: `query`, `limit`, `cursor` | 권한에 맞는 기능 요약, ID·version, catalogVersion, nextCursor |
| `a2api.describe` | 필수: `id`, `version` | 선택한 capability의 짧은 설명과 입력·출력 schema |
| `a2api.invoke` | 필수: `id`, `version`, `catalogVersion`, `input`; 선택: `requestId` | 기존 runtime의 성공/실패 envelope |

예를 들어 에이전트는 `a2api.discover({"query":"배송 조회"})`로 기능과 카탈로그 버전을 얻고, `a2api.describe`에서 정확한 입력 형식을 확인한다. 그다음 발견한 ID·version·catalogVersion을 그대로 사용해 `input: {"orderId":"ORD-1001"}`을 전달한다.

각 도구는 `inputSchema`, `outputSchema`, 읽기 전용 annotation을 제공한다. HTTP와 MCP의 요청 계약은 `src/a2api/api.py`에서 공유한다. 정의하지 않은 필드와 잘못된 타입은 거부한다. 도구 arguments로 actor·tenant·scope·backend 주소를 설정할 수 없다. 요청 `_meta`도 인증 context를 바꾸는 데 사용하지 않는다.

`invoke.outputSchema`는 공통 envelope만 기술하고 capability별 ID·version·업무 schema를 나열하지 않는다. 선택한 업무 schema는 describe에서 제공하고, bridge와 runtime이 실제 성공 데이터를 검증한다. 전체 실행 계약과 검토 이력은 기존 라이브러리 API에서 확인하며 MCP describe로 전송하지 않는다.

## 구조화 결과와 오류

성공·실패 모두 JSON `structuredContent`와 동일한 JSON을 담은 text content를 반환한다. 사용자 표시 힌트와 조회 근거도 기존 envelope에 유지한다. 표시는 호스트가 담당하며 bridge가 별도 UI를 만들지는 않는다.

- 실행 전 계약·버전·권한·입력 오류: `isError: true`, `structuredContent: {"error": ProblemDetails}`.
- 실행 중 backend 오류: `isError: true`, 기존 `status: failed` envelope와 오류·근거·호출 수를 유지한다. 성공 데이터는 반환하지 않는다.
- 알 수 없는 MCP 도구나 지원하지 않는 tools/list cursor: JSON-RPC `INVALID_PARAMS`(-32602).
- 예기치 않은 호스트 오류: 내부 예외 내용을 노출하지 않고 일반 `INTERNAL_ERROR`를 반환한다.

실패 응답도 도구 outputSchema에 맞는 variant를 가진다. JSON Schema 검증 성공은 업무 성공과 다르며 `isError`, `status`, `completeness`를 함께 확인해야 한다.

`discover`의 업무 카탈로그 pagination은 기존 cursor를 그대로 사용한다. MCP `tools/list` 자체는 세 도구를 담은 한 페이지이며 nextCursor가 없다.

## 기존 runtime을 연결하는 라이브러리 API

```python
import anyio

from a2api import ExecutionContext
from a2api.mcp_bridge import serve_stdio

# runtime은 검증한 계약과 운영자가 등록한 HTTP binding으로 만든 기존 Runtime이다.
# context는 호스트가 검증한 인증 정보에서 만든다.
context = ExecutionContext("user-123", "tenant-1", frozenset({"orders:read", "shipments:read"}))
anyio.run(serve_stdio, runtime, context)
```

`create_mcp_server(runtime, context)`는 공식 SDK의 low-level `Server`를 반환한다. `serve_stdio`는 이를 표준 입출력에 연결한다. 동기 HTTP 실행은 worker thread에서 수행해 MCP event loop를 막지 않는다. 권한·상태·의미 ID·backend timeout 검사는 기존 runtime과 adapter를 사용한다.

이 factory는 호스트가 이미 인증한 고정 identity의 stdio 용도다. 다중 사용자 HTTP 공개 서버용 인증을 구현한 것은 아니다. Streamable HTTP, HTTP OAuth, 실행 중 GET의 강제 취소와 추가 MCP 기능은 별도 범위다. 클라이언트 종료·취소 시에도 이미 시작한 읽기는 runtime의 timeout 범위에서 끝날 수 있다.

## 검토한 빌드 연결

`python -m a2api mcp --build /absolute/path/to/orders-built`로 조회 계약 빌더의 로컬 주문·배송 산출물을 연결한다. `mcp-demo --build ...`는 공식 SDK의 stdio 클라이언트로 이를 검증한다. `review-demo`는 OpenAPI import와 build부터 실행한다. 샘플 범위 검사와 source/review/산출물 재검증을 서버 시작 전에 수행한다. 전체 사용법은 [검토 빌더 안내](08-review-builder.ko.md)에 정리했다.

## 검증

초기 구현에서는 Python 3.12, MCP SDK 2.3.0, jsonschema 4.26.0에서 총 **60개 테스트**가 통과했다. 현재 P0-3 검증은 [별도 사용 안내](13-lightweight-mcp.ko.md)에 정리한다.

MCP 테스트에는 공식 클라이언트의 실제 subprocess stdio 통신, 이전 initialize handshake 방식, 목록 안정성, 구조화/텍스트 일치, 업무 출력 schema, 빈 배송, caller별 scope·객체 접근, context 인자 위조 거부, 카탈로그 버전 불일치, backend schema 오류, 오류 코드, stdout 분리와 EOF 종료를 포함한다. 외부 LLM이나 특정 에이전트 앱의 UI에서 수행한 평가를 뜻하지 않는다.

참고한 1차 자료: [공식 Python SDK](https://github.com/modelcontextprotocol/python-sdk), [MCP Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools), [stdio transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio).
