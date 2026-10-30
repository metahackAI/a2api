# P0-3: 변환 객체와 Python 함수를 경량 MCP로 호출하기

OpenAPI의 `ConvertedAPI`, Python 함수의 `Application`을 같은 stdio bridge에 연결한다. 세 도구의 공통 schema는 API 개수에 따라 늘어나지 않는다. 선택한 API의 입출력은 describe에서 받고 서버에서 검증한다. 파일 기반 review/build, 자동 앱 탐색이나 새 registry는 필요 없다.

## 바로 실행

저장소 루트에서 MCP 선택 의존성을 설치한다.

```bash
python -m pip install -e ".[mcp]"
python examples/native-orders/mcp_client.py
```

공식 SDK client가 [서버 예제](../examples/native-orders/mcp_server.py)를 별도 프로세스로 실행하고 실제 stdio로 도구 목록·discover·describe·invoke를 호출한다. OpenAPI 주문 1회·배송 2회의 실제 로컬 HTTP 호출과, [P0-2 함수](../examples/native-orders/register_and_invoke.py)의 주문/배송 조회가 같은 MCP 서버에서 동작한다. 외부 API·LLM 키는 필요 없다.

서버만 실행하려면 `python examples/native-orders/mcp_server.py`를 사용한다. 이 명령은 JSON-RPC 입력을 기다리며 stdout은 MCP 전용이다. `--source openapi` 또는 `--source python`으로 한 종류만 연결할 수도 있다. 기본값은 both다. `--sample-user`는 호스트가 선택하는 고정 fixture identity이며 실제 사용자 인증 기능이 아니다.

## 자신의 앱 연결

P0-1/P0-2의 앱을 만드는 코드는 그대로 사용한다. 다음은 연결 부분이다.

```python
import anyio
from a2api.mcp_bridge import serve_stdio

# http_api = convert(source, operations=..., deployment=...)
# functions = Application([lookup_order, list_shipments])
# caller = 기존 호스트가 인증한 ExecutionContext
anyio.run(serve_stdio, [http_api, functions], caller)
```

한 객체라면 `serve_stdio(http_api, caller)` 또는 `serve_stdio(functions, caller)`로 연결한다. `create_mcp_server(app, caller)`는 SDK Server를 반환하고 `serve_stdio`는 실제 표준 입출력에 연결한다. 기존 전체 계약의 Runtime도 단일 인자로 계속 지원한다. 앱별 identity가 달라야 한다면 별도 서버/context로 연결한다.

앱의 `descriptors()`는 bridge가 읽는 호스트용 스냅샷이다. 그 전체를 LLM에 전달하는 단계가 아니다. 여러 직접 호출 앱을 묶을 때 ID/version이 충돌하면 시작 시 오류로 보고하므로 namespace나 등록 ID로 구분한다.

MCP 호스트의 `mcpServers` 설정 예시:

```json
{
  "mcpServers": {
    "a2api": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": ["/absolute/path/to/a2api/examples/native-orders/mcp_server.py"]
    }
  }
}
```

자신의 앱에서는 args를 자신의 host 파일 절대 경로로 바꾼다. 해당 Python 환경에 a2api[mcp]를 설치한다. 호스트 설정에 backend token을 모델 인자로 넣지 않고 기존 credential provider와 context를 유지한다. 실행 중인 앱을 자동 교체하거나 임의 모듈 경로를 원격 입력으로 로드하지 않는다.

## 모델이 호출하는 순서

1. `a2api.discover`에 query/limit를 보내 작은 후보 목록과 catalogVersion을 받는다.
2. 선택한 ID/version으로 `a2api.describe`를 호출한다.
3. 반환된 inputSchema에 따라 `a2api.invoke`를 호출한다.

OpenAPI 주문 조회의 요청 예시:

```json
{"query":"getorder","limit":3}
```

```json
{"id":"legacy.getorder","version":"0.1.0"}
```

```json
{
  "id":"legacy.getorder",
  "version":"0.1.0",
  "catalogVersion":"<discover가 반환한 값>",
  "input":{"path":{"orderId":"ORD-1001"}}
}
```

등록한 Python 함수는 `id: orders.lookup`, `input: {"orderId":"ORD-1001"}`이다. HTTP path/query 위치와 Python의 인자 형식을 임의로 동일하게 바꾸지 않으며 각각의 describe를 따른다.

검색은 ID/요약을 사용하는 키워드 검색이다. query를 생략하면 등록한 항목을 정해진 page 크기로 받는다. query/limit/context에 맞는 cursor만 재사용할 수 있다. 버전이나 카탈로그가 다르면 본문 실행 전에 거부한다. 유효한 설명을 알고 있다면 매번 검색/상세를 반복할 필요는 없다.

## 무엇이 경량화되었는가

| 경로 | 현재 동작 |
|---|---|
| tools/list | 고정 discover/describe/invoke 3개와 공통 요청·결과 envelope만 포함 |
| discover | ID·version·짧은 요약·효과·cursor; 개별 schema를 포함하지 않음 |
| describe | 선택한 id/version/summary/effects/inputSchema/outputSchema만 포함 |
| invoke | 실제 선택한 schema로 입력/응답 검증 후 상태·데이터·완전성 반환 |

전체 IR의 operations·binding·execution·provenance/review 이력은 MCP describe에 포함하지 않는다. 개발자는 기존 `Runtime.describe`나 `load_build`에서 전체 계약을 계속 확인할 수 있다. 기존 CLI 샘플과 검토 빌드의 MCP 호출도 이 경량 describe를 사용한다.

공통 invoke의 `data` schema는 일반 JSON이므로 그것만으로 업무 필드의 enum·타입을 알 수 없다. 실제 schema는 선택한 describe에 있고, runtime과 bridge가 성공 응답을 해당 schema로 검증한다. 공통 outputSchema에 개별 API를 열거하지 않는 것이 업무 검증을 없애는 것은 아니다.

기존 Runtime의 invoke 결과에 있던 근거·표시 힌트·호출 수 등은 호환을 위해 유지한다. 직접 호출 앱은 P0-1/P0-2의 작은 envelope를 사용한다. 명시한 requestId는 추적용으로 반환하며 멱등 실행 보장은 추가하지 않는다.

## 오류와 호스트 context

실패는 `isError: true`와 구조화 error로 반환한다. 버전·카탈로그·요청 형식 오류는 실행 전에 거부하고, backend 권한 거부·입력 오류·응답 schema 불일치 등 기존 코드를 유지한다. Context는 서버 시작 시 고정한 ExecutionContext에서 전달하며 모델 인자나 요청 meta로 덮어쓸 수 없다.

직접 호출 앱의 노출 범위는 호스트가 선택한 operation/함수다. 사용자별 객체 접근·업무 scope 검사는 기존 credential provider·backend·함수에 둔다. 기존 Runtime 카탈로그의 scope/sample/활성 상태 필터도 유지한다. 등록을 했다는 사실이나 read 선언으로 객체 권한을 자동 부여하지 않는다.

동기 API/함수는 기존 worker thread 경로에서 실행한다. stdio 연결, JSON Schema 검증과 고정 host context를 제공하며 HTTP OAuth·새 인증 서버·강제 함수 취소·재배포 기능은 추가하지 않았다.

## 문맥 비용 측정

[측정 기록](evidence/p0-3-context-bytes.json)은 같은 Order TypedDict 조회 함수를 1개/100개의 다른 ID로 등록한 합성 사례다. 새 MCP 쪽은 SDK client로 실제 tools/list와 cold discover/describe/invoke를 실행했다. 직접 도구 쪽은 동일한 업무 schema와 결과로 도구 정의·단일 요청/응답을 구성한 비교 기준이다.

이 표는 P0-3 당시의 측정이다. 이후 호출 설명과 직접 HTTP 앱의 read/write effect 지원이 추가됐으므로 현재 tools/list의 정확한 바이트 수와 동일하다고 해석하지 않는다. [현재 소스/메서드 지원](18-source-importers.ko.md)을 참고한다.

| 항목 | API 1개 | API 100개 |
|---|---:|---:|
| 직접 도구 정의 | 645 B | 57,858 B |
| a2api 공통 도구 정의 | 6,504 B | 6,504 B |
| 직접 도구: 정의+요청/결과 | 748 B | 57,961 B |
| a2api: 정의+검색+상세+호출의 요청/결과 | 7,892 B | 8,010 B |

공통 도구 정의의 크기는 같지만, API가 하나일 때에는 검색/상세와 envelope의 추가 비용이 더 크다. 100개 사례에서 전체 schema를 처음부터 전달하지 않는 효과가 보인다. 도구 개수가 세 개라는 사실만으로 항상 효율적이라고 주장하지 않는다.

값은 compact UTF-8 JSON의 **구조화 payload 바이트**다. JSON-RPC framing·initialize·동일 내용을 담은 text content는 제외했다. 전체 API 서비스의 평균이나 실제 모델 토큰·지연·정확도 측정이 아니다. MCP text/structured 중 무엇을 모델에 전달하는지는 호스트에 달려 있다.

## 검증

실제 stdio에서 두 종류 앱을 함께/각각 연결하고 주문·배송·빈 결과를 확인했다. 입력/권한/schema 오류의 isError, 미노출 버전, stale catalog, context 위조 거부, cursor, stdout/EOF, 공통 도구 목록의 1/100 동일성, 성공 결과의 업무 schema 재검증을 테스트한다. 기존 Runtime/검토/부분 재승인 경로도 회귀 검증한다. 실제 LLM 평가나 운영 API 전체 검증을 수행한 결과는 아니다.

ResourceWarning도 오류로 처리한 전체 테스트 226개가 통과했다. 소스 폴더 밖에 추출한 wheel의 별도 host 프로세스에서도 OpenAPI와 Python 함수를 함께 연결해 실제 stdio로 discover/describe/invoke를 검증했다.
