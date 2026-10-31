# a2api-tools/1.0: 필요한 호출 계약만 모델에 제공하기

`auto()`의 전체 제공 기준은 `all_bytes=10000`(약 20개 함수)이다. dev에서 19개 함수 카탈로그는 전체 제공이 사전 선택보다 빨랐고(중앙값 7.9초 대 9.3초, spec-tools 9.3초) 토큰은 spec-tools보다 17% 적었다. 55개 카탈로그는 전체 제공이 빠르지 않아(10.5초 대 사전 선택 9.4초) 사전 선택을 유지한다([34 문서](34-completion-results.ko.md) 5절).

`TOOL_PROFILE`은 `a2api-tools/1.0`이며 아래 0.4 변경을 확정한 것이다. 이후 추가: `auto(question, preselect=8)`은 호스트 사전 검색에서 모델 검색(`search_limit`, 기본 3)보다 넓은 후보를 준비하고, 평탄화한 path/query/header의 문자열 인자에 들어온 JSON 숫자·불리언은 텍스트로 바꿔 전달한다(body는 그대로). 함수 설명 기본값(`hints="none"`)은 요약과 쓰기 함수의 `[write]` 표시뿐이다. holdout 판정 이후 4개 언어 dev 360 run에서 반환 이름 목록(`hints="shape"`, `Returns {items:[{id,status}],total}`)보다 정확도는 같고(120/120) 작업당 토큰이 8.5% 적어 기본값으로 정했다([34 문서](34-completion-results.ko.md) 5절). `shape`는 선택으로 남기고, `hints="typed"`가 0.3 형식과 원래 입력 schema를 유지한다. 검색 index는 `field-search/2`(비ASCII 단어 뒤 짧은 조사·어미 허용)다.

> **0.4 (2026-10-31, [33 문서](33-completion-plan.ko.md) 1단계)**: wire(`a2api-call`)와 MCP 세 도구는 그대로이고 호스트 표현만 바뀐다.
> - **읽기 쉬운 함수 이름**: capability ID에서 만든 `legacy_getorder` 같은 이름. 같은 세션의 다른 계약과 겹치면 8자리 hash 접미사를 붙인다. `ToolSession(..., naming="hash")`이면 0.3의 `a2api_call_<hash>`를 쓴다. 이름은 여전히 권한이 아니며 선택되지 않은 이름은 `NOT_SELECTED`다.
> - **평탄한 HTTP 입력**: `{path,query,headers,body}` 입력을 이름 충돌·선택 그룹의 필수 필드가 없을 때 한 객체로 보여주고, 호출 시 원래 구조로 복원해 기존 invoke 검증을 거친다. 원래 구조로 보낸 인자도 받는다. `flatten=False`로 끌 수 있다.
> - **compact 결과**: `session.render(payload)`/`render_result`가 공백 없는 JSON으로 status·data(필요한 경우만 httpStatus·completeness)를 만들고, 실패는 code/detail/issues와 짧은 `hint`(재시도·다른 함수 검색으로 해결되지 않는 오류 안내)를 준다. `call()`의 반환 envelope는 바뀌지 않는다.
> - **auto 전략**: `await session.auto(question)`은 전체 카탈로그가 `max_tool_bytes`와 `max_functions`(기본 64) 안이면 모든 함수를 준비하고 검색 도구를 뺀다(`strategy="all"`). 아니면 사용자 질문으로 호스트가 첫 검색을 수행해 후보를 준비하고 검색 도구를 유지한다(`strategy="search"`). 업무 API는 실행하지 않는다. `tools()`의 기본값은 auto 결과를 따른다.
> - 아래 0.3 설명은 hash 이름/중첩 입력 예시를 포함한 이력이다. 0.3으로 기록한 GitHub/tool-session 평가 하네스는 재현을 위해 `naming="hash", flatten=False`를 고정한다.

## 0.3 설명(이력)

기준: [제품 목표](00-product-direction.ko.md), [이번 개발 계획](23-total-call-cost-plan.ko.md). 서버 wire는 기존 [a2api-call/0.1](20-call-protocol.ko.md)을 그대로 사용한다. 이 문서는 호스트의 도구 표현과 호출 규칙을 정의한다.

0.2는 선택적 다음 페이지와 진행 상태를 추가했고, 0.3은 선택한 함수의 반환 필드를 짧게 설명한다. 기존 query-only 입력과 검색 결과 형식은 유지한다. [검색 개선](29-search-improvement.ko.md)에 이어 [결과 전달·보류 요청 검증](31-result-delivery-and-holdout-plan.ko.md)을 적용한다.

## 계약과 모델 도구의 관계

하나의 capability descriptor가 원본이다. 호스트는 선택한 descriptor에서 `summary`, `effects.kind`, **완전한 inputSchema**를 function tool로 만든다. outputSchema는 검증용으로 보관하고 field 이름·타입·필수 여부만 짧은 반환 설명에 사용한다. 실행 주소·인증·전체 IR은 모델에 전달하지 않는다.

| 정보 | 보관/전달 위치 |
|---|---|
| 정확한 업무 입력 schema | 선택한 모델 도구의 parameters, 원래 invoke 검증 |
| id/version/catalogVersion | 호스트의 바인딩, 기존 invoke 요청 |
| 출력 schema | 서버와 호스트의 성공 결과 검증 |
| 공개 출력 이름·타입·필수 여부 | 선택한 function의 짧은 반환 설명 |
| 짧은 검색 결과 | 선택된 function 이름/ID, 제외 이유, 추가 후보 존재 여부 |
| 전체 카탈로그와 검색 metadata | 서버/신뢰한 호스트 |
| 사용자·tenant·인증 정보 | 기존 trusted context와 배포 연결 |

모델 도구의 이름은 `a2api_call_<24자리 hash>`다. 이름은 호스트 세션의 바인딩 키이며 권한 토큰이 아니다. 모델은 이름을 복사하고 업무 인자만 작성한다. 호스트가 선택된 계약의 식별자·버전을 붙여 기존 invoke를 호출한다. 정상/실패 envelope는 바꾸지 않는다.

반환 설명 예시는 `Returns object fields: "default_branch":string (required), "archived":boolean (required).`다. 공개 schema의 최대 6개 필드를 읽고 나머지는 개수로 표시한다. 배열은 item 필드, 명시적 nullable은 `string|null`, 선택 필드는 optional로 표시한다. 로컬 참조만 제한적으로 따라가며 해석하지 못하는 조합/순환 schema는 JSON으로 표시한다. 실제 값·examples·description·업무 관계는 넣지 않고 긴 필드 이름은 자르지 않고 생략한다. 별도 descriptor 필드나 MCP 도구를 추가하지 않는다. 이 설명도 전송/예산에 포함되므로 항상 토큰이 감소하는 것은 아니다.

## 정보 전달 규칙

1. 호스트가 필요한 기능을 알면 `prime([...])`으로 첫 모델 요청 전에 준비한다. 모델의 탐색·설명 호출은 필요 없다. 호스트 초기화에 필요한 discover/describe 비용은 별도로 측정한다.
2. 모르는 기능에는 `a2api_search({"query":"작업 키워드"})`를 제공한다. 호스트가 discover와 선택 후보 describe를 처리한다. 모델은 그 사이에 다음 행동을 추론할 필요가 없다. 결과에 schema를 다시 넣지 않고, **다음 모델 요청의 tools**에 실행 가능한 정의를 넣는다.
3. 매 모델 요청 직전에 `session.tools()`를 읽는다. 검색 직전 목록을 계속 보내면 새 함수를 호출할 수 없다. 같은 응답에서 아직 제공되지 않은 함수를 호출하도록 허용하지 않는다.
4. 선택한 기능은 같은 대화에서 재사용한다. 매 요청에 검색을 강제하지 않는다. tools의 입력 정의는 provider에 매번 전송되므로 재사용이 전송 토큰을 0으로 만들지는 않는다. 과거 tool 결과도 대화에 남는다. 이번 구현은 대화 요약/절단을 자동으로 하지 않는다.
5. 호스트가 정한 UTF-8 JSON 바이트 예산 안에서 완전한 도구 정의를 유지한다. 최근 사용하지 않은 기존 정의부터 제거한다. 한 검색에서 이미 선택한 정의는 그 검색의 뒤 후보 때문에 제거하지 않는다. 단독으로도 맞지 않는 schema는 `SCHEMA_BUDGET`으로 제외한다. 필수값/enum/$defs를 없애지 않는다.
6. catalog 변경 발견 시 이전 선택을 폐기한다. invoke가 `CONTRACT_DRIFT`이면 재실행하지 않고 오류를 반환한다. 다시 검색해야 한다. 사용자/tenant/scopes/server 변경 시 호스트가 새 세션을 만든다. 새 권한이 자동으로 감지된다고 가정하지 않는다.
7. 입력은 호스트와 기존 실행기에서 검사한다. raw HTTP·공개 출력 검사도 유지한다. 결과의 `completeness.scope=single_api_response`는 전체 업무/모든 페이지 완료를 의미하지 않는다.

직접 앱의 검색은 원본 ID·용도·공개 입출력 field를 사용하는 [필드 기반 lexical index](21-discovery-metadata.ko.md)다. 이 규칙은 검색 품질이나 업무 관계를 자동 보장하지 않는다. 입력 schema만으로 사용자의 “3개”와 모델이 보낸 “5개”가 다르다는 사실을 알 수 없다. 모델/호스트의 요청 해석과 사용자 조건 준수는 별도 평가한다. default는 입력을 생략했을 때의 API 동작이며 명시적 값을 덮어쓰지 않는다.

MCP `tools/list`는 항상 discover/describe/invoke 세 개다. 위 function tools는 **모델 호스트의 표현**이다. 검색 결과에 따라 MCP 서버 도구 목록을 변경하지 않는다. 특정 provider의 deferred-tool 확장 필드도 요구하지 않는다.

## 검색 결과와 오류 형식

검색 입력은 `{"query":"주문"}`이며 query는 0~1000자 문자열이다. 선택적 `more`는 boolean이고 기본 false다. 나머지 추가 키는 거부한다. 후보 수는 모델 입력이 아니라 호스트의 `search_limit`(1~20, 기본 3)이다. 전체 카탈로그를 자동으로 순회하지 않는다.

`moreAvailable=true`이면 `{"query":"주문","more":true}`로 다음 후보를 요청한다. 라이브러리에서는 `await session.select('주문', more=True)`다. cursor는 모델에게 주지 않는다. 같은 query를 more 없이 반복하면 현재 페이지를 재사용한다. query의 공백/대소문자 변화는 같은 view로 취급하고 원래 wire query/limit을 유지한다. 질의당 최대 3페이지(기본 후보 9개), 세션은 최근 32개 query view를 보관한다. 이미 제공한 후보를 다시 받은 경우 해당 query의 `progress=false`다.

```json
{
  "selected": [{"name": "a2api_call_<24자리 hash>", "id": "legacy.getorder"}],
  "omitted": [],
  "evicted": [],
  "moreAvailable": false,
  "page": 1,
  "pageLimitReached": false,
  "progress": true
}
```

`omitted`는 `[{"id":"...","reason":"SCHEMA_BUDGET"}]`, `evicted`는 제거한 function 이름 배열이다. 빈 검색은 한 페이지를 반환하며 적절한 기능이 선택되었다는 보장이 아니다. 검색 결과는 다음 모델 요청에서 사용할 도구를 알리는 데이터다.

`moreAvailable`은 호스트 예산 안에서 다음 페이지를 요청할 수 있는지다. 3페이지 한도에 도달했고 서버에 더 있으면 `pageLimitReached=true`로 알려주므로 전체 카탈로그를 다 봤다는 뜻이 아니다. 시작 전 more는 `SEARCH_NOT_STARTED`, 실제 끝은 `SEARCH_EXHAUSTED`, 3페이지 이후는 `SEARCH_PAGE_LIMIT`다. 잘못된 more 타입은 `INVALID_INPUT`이다. limit 변경은 해당 query view를 새로 시작해야 한다. stale cursor는 선택 도구/페이지 상태를 폐기하고 `CONTRACT_DRIFT`로 반환하며 자동 재시도하지 않는다.

`call`은 검증된 기존 invoke envelope 또는 `{"error": problem}`을 반환한다. 잘못된 인자는 `INVALID_INPUT`, 활성 목록에 없는 이름은 `NOT_SELECTED`, 계약 변경은 `CONTRACT_DRIFT`, 형식이 다른 응답은 `SCHEMA_MISMATCH`다. 연결/호스트 오류는 원문 예외를 노출하지 않는 `HOST_PROTOCOL_ERROR`다. 호출 중 연결이 끊기면 실제 실행 여부가 불명확할 수 있으므로 재시도하지 않는다. 이 호스트 프로파일이 쓰기 권한이나 업무 승인을 자동 부여하지 않는다.

## 라이브러리 사용

```python
import asyncio
from a2api import Application, ExecutionContext, ToolSession, capability

@capability(id='orders.lookup', effect='read')
def lookup(orderId: str) -> str:
    """주문 번호로 상태를 조회한다."""
    return 'shipped'

async def main():
    session = ToolSession(Application([lookup]), ExecutionContext('alice', 'tenant-a', frozenset()))
    await session.prime(['orders.lookup'])       # 호스트가 아는 기능, 업무 API 실행 없음
    tools = session.tools(include_search=False) # 모델의 tools에 전달
    name = tools[0]['function']['name']
    print(await session.call(name, {'orderId': 'ORD-1001'}))

asyncio.run(main())
```

`ConvertedAPI`와 앱 목록도 동일하게 받는다. `ToolSession.from_mcp(client)`는 연결된 공식 MCP client를 받으며 연결 수명은 호출자가 관리한다. 기본 `max_tool_bytes=16000`, `search_limit=3`은 호스트 설정이다. 실제 모델 token budget이 아니고 API 개수 전환 임계값도 아니다. `prime`은 정확한 ID로 첫 페이지에서 버전을 확인하고 전체 요청 집합이 예산에 들어야 한다. 실제 복수 버전은 오류이며 마지막 페이지의 한 버전을 임의로 고르지 않는다. 필요하면 검색/예산을 조정한다.

필드 기반 순위는 업데이트한 직접 앱 서버에서 제공한다. 호스트의 more 지원만으로 외부/기존 관리 Runtime 서버의 검색 알고리즘까지 바뀌는 것은 아니다. 인증 주체/tenant/scopes/server가 바뀌면 새 ToolSession을 사용한다.

선택한 함수 호출에는 inputSchema의 업무 객체를 그대로 전달한다. 기존 OpenAPI의 `path/query/body`와 등록 함수의 평탄한 인자 차이도 그대로다. 임의 flatten이나 인자 보정을 하지 않는다. `tools()`와 `binding(name)`은 복사본이다. `binding`과 `stats`는 호스트의 로그/측정용이며 모델 메시지에 넣을 필요가 없다.

## 실제 모델과 stdio

기존 설치와 모델 환경 변수는 [시작 안내](22-quickstart-and-model.ko.md)를 따른다.

```bash
# 알고 있는 두 기능으로 바로 호출
python examples/model-client/client.py --binding selected \
  --known legacy.getorder --known legacy.getshipment --no-search \
  --question 'ORD-1001 주문과 연결된 모든 배송 상태를 알려줘.' \
  -- python examples/native-orders/mcp_server.py --source openapi

# 필요한 기능을 검색한 뒤 schema를 받아 호출
python examples/model-client/client.py --binding selected \
  --question 'ORD-1001 주문과 연결된 모든 배송 상태를 알려줘.' \
  -- python examples/native-orders/mcp_server.py --source openapi

# 기존 3도구 사용도 유지
python examples/model-client/client.py --binding generic \
  --question 'ORD-1001 주문 상태를 알려줘.' \
  -- python examples/native-orders/mcp_server.py --source openapi

# 기존 GitHub 공개 API 예제 연결
python examples/model-client/client.py --binding selected \
  --known github.repository.get --known github.issues.list --no-search \
  --question 'metahackAI/a2api의 정보와 열린 이슈·PR 첫 페이지 3개를 알려줘.' \
  -- python examples/github-openapi/mcp_server.py
```

복잡한 요청은 모델이 주문 응답의 shipmentIds를 읽어 실제 배송 ID로 다음 함수를 호출한다. 알려진 여러 API 관계가 있으면 기존 명시적 wrapper/계약 composition을 사용할 수 있다. 이름/$ref에서 업무 그래프를 자동 추론하지 않으며 선행 API의 네트워크 비용도 사라지지 않는다.

이 프로파일의 완료는 모든 업무의 최적화를 뜻하지 않는다. 작은 알려진 API는 일반 function tool과 비슷해야 하며, 큰 미지 카탈로그는 같은 검색기를 쓰는 일반 검색 방식과도 비교한다. 전체 모델 usage·지연·조건 준수·실행 횟수를 함께 판단한다. 실측 결과는 [검증 보고](25-total-call-cost-results.ko.md)에 기록한다.
