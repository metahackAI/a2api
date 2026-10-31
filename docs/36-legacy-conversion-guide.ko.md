# 레거시 API를 a2api로 전환하는 방법

작성일: 2026-10-31 · 갱신: 2026-11-01(1.1) · 대상: a2api 1.1 (`pip install "a2api[mcp,openapi,source]"`)

이 문서는 이미 운영 중인 API를 LLM이 호출할 수 있는 a2api 기능으로 바꾸는 절차를 세 경우로 나눠 설명한다.

- **경로 A — OpenAPI와 코드가 모두 있을 때**: OpenAPI를 기준으로 변환하고, 코드는 명세가 실제 구현과 맞는지 확인하는 데 쓴다.
- **경로 B — OpenAPI 없이 코드만 있을 때**: Spring MVC·Go(net/http, Gin)·Rust Axum·Python FastAPI는 소스에서 route와 DTO를 읽고, HTTP 없는 Python 코드는 함수를 직접 등록한다. 그 밖의 언어는 B-3을 따른다.
- **경로 C — 실행 중인 서비스가 도구 목록(이름·설명·입력 schema)을 내주고 이름으로 호출받을 때**: 목록을 그대로 가져온다. 약어·코드값 같은 레거시 표현은 vocabulary로 바꿔 보여 준다.

모든 코드 조각은 실제로 실행한 예제에서 가져왔다: [`examples/legacy-conversion/`](../examples/legacy-conversion/README.md)의 `openapi_and_code.py`(경로 A), `code_only.py`(경로 B-1), `python_functions.py`(경로 B-2), `legacy_screens.py`(경로 C). 실제 공개 프로젝트에서의 변환 결과는 9절에 있다.

## 0. 어느 경로인가

```text
                         ┌─ 명세가 구현과 맞다 ─────────────► 경로 A (OpenAPI로 변환)
OpenAPI가 있다 ─────────┤
                         └─ 오래됐거나 일부만 있다 ─┬─ 프레임워크가 명세를 다시 생성할 수 있다 → 재생성 후 경로 A
                                                    └─ Spring/Go/Rust 코드가 있다 ──────────→ 경로 B-1
OpenAPI가 없다 ─┬─ 서비스가 도구 목록을 내주고 이름으로 호출받는다 ───────────────────→ 경로 C
                ├─ Spring MVC / Go net/http·Gin / Rust Axum / Python FastAPI ──────────────→ 경로 B-1
                ├─ HTTP 없이 Python 함수만 있다 ──────────────────────────────────────────→ 경로 B-2
                └─ 그 밖의 언어·프레임워크(Node, C#, PHP, Echo, Chi, Actix…) ────────────→ 경로 B-3
```

어느 경로든 결과물은 같다: **메모리 안의 a2api 앱**(`ConvertedAPI` 또는 `Application`). 같은 앱을 라이브러리로 직접 호출하거나, MCP 세 도구로 내보내거나, 모델 호스트의 `ToolSession`에 연결한다. import 파일·review·build 디렉터리는 필요 없다.

## 1. 공통 개념(먼저 읽기)

| 개념 | 의미 | 결정하는 사람 |
|---|---|---|
| capability | LLM이 호출할 기능 하나. 보통 API operation 하나 또는 Python 함수 하나 | 개발자가 노출할 것만 고른다 |
| descriptor | `id`, `version`, `summary`, `effects.kind`, `inputSchema`, `outputSchema` 6개 필드. 모델이 보는 계약 | importer가 만들고 개발자가 summary를 다듬는다 |
| effect | `read` 또는 `write`. GET/HEAD는 read, PUT/PATCH/DELETE는 write, **POST는 개발자가 명시**한다 | 개발자(자동 추측하지 않음) |
| select | 응답에서 모델에게 보낼 필드. 내부 필드(tenant, 메모, 감사 정보 등)를 서버에서 제거한다 | 개발자 |
| deployment | 실제 서버 주소, 사용자별 인증 헤더, 시간 제한 | 호스트 |
| context | 호출자(`ExecutionContext(actor, tenant, scopes)`). 모델 입력이 아니며 바꿀 수 없다 | 호스트의 인증 계층 |

호출 결과는 항상 같은 형태다.

```python
{'status': 'succeeded', 'data': {...}, 'completeness': {'complete': True, 'scope': 'single_api_response'}}
{'status': 'failed', 'error': {'code': 'RESOURCE_NOT_FOUND', 'detail': '...', 'status': 404, ...}, 'completeness': {'complete': False}}
```

a2api는 **입력 검증 → 원본 서버 호출(재시도 없음) → 원본 응답 전체 검증 → 공개 필드 선택 → 공개 응답 검증** 순서로 실행한다. 원 서버의 권한 검사는 그대로 유지해야 한다. a2api에 연결했다고 권한이 생기지 않는다.

## 2. 경로 A — OpenAPI와 코드가 모두 있을 때

### A-1. 명세 읽기와 변환 불가 항목 확인

```python
from a2api.importers import OpenAPIImporter

source = OpenAPIImporter.from_file('openapi.json', namespace='shop',
                                   methods={'GET', 'POST', 'PATCH', 'DELETE'})   # 기본값은 GET만
for record in source.iter_operations():
    if record.status != 'imported':
        print(record.summary())   # operationId, method, path, status, diagnostics(사유 코드)
```

- OpenAPI 3.0/3.1, JSON·YAML(`a2api[openapi]`)·`.gz`를 읽는다. 외부 파일 `$ref`는 지원하지 않는다(하나의 문서로 bundle).
- 명령줄로 전체 보고서를 볼 수도 있다: `python -m a2api import-openapi openapi.json --namespace shop --methods GET POST PATCH DELETE --output report-dir` → `report-dir/report.json`.
- 대표 사유와 대응:

| 사유 코드 | 뜻 | 대응 |
|---|---|---|
| `NO_SUPPORTED_SUCCESS` | 2xx 응답 schema가 없음 | 성공 응답에 JSON schema를 추가하거나 204로 명시 |
| `UNSUPPORTED_RESPONSE` | 성공 응답이 JSON이 아님(파일·텍스트) | 그 operation은 제외하거나 Python wrapper(B-2)로 감싼다 |
| `UNSUPPORTED_REQUEST_BODY` | multipart·form 본문 | 제외하거나 wrapper |
| `UNSUPPORTED_PARAMETER_SCHEMA` | 직렬화가 정의되지 않은 parameter(예: **필수** nullable query, 객체 parameter) | parameter schema를 단순 타입으로. 선택 nullable query/header는 1.1부터 "생략 = null"로 변환한다(`NULL_PARAMETER_OMITTED` 진단) |
| `GET_REQUEST_BODY` | GET에 본문 | 명세 수정 |
| `METHOD_NOT_SELECTED` | `methods`에 포함하지 않은 메서드 | 필요하면 `methods`에 추가 |
| `NULLABLE_WITHOUT_TYPE`(경고) | OAS 3.0 `nullable`만 있고 `type` 없음 | 동작에는 영향 없음. 정리 권장 |

선택하지 않은 operation이 변환 불가여도 선택한 operation의 변환은 막지 않는다.

### A-2. 명세가 코드와 맞는지 확인

명세는 쉽게 오래된다. 구현이 Spring/Go/Rust라면 같은 경로·메서드가 코드에 있는지 소스 importer로 바로 비교할 수 있다.

```python
from a2api.importers import GoSourceImporter   # SpringSourceImporter, RustSourceImporter

documented = {(r.method.upper(), r.path) for r in source.iter_operations() if r.status == 'imported'}
code = GoSourceImporter.from_directory('service/', namespace='code')
implemented = {(r.method.upper(), r.path) for r in code.iter_operations() if r.status == 'imported'}
print('코드에만:', implemented - documented, '명세에만:', documented - implemented)
```

예제 실행 결과는 `코드에만: {('GET','/__admin/state'), ('POST','/__admin/reset')}`였다. 내부 관리 route라 명세에 없는 것이 맞으므로 노출하지 않는다. 판단 기준:

| 비교 결과 | 선택 |
|---|---|
| 일치 | 경로 A로 진행. 명세에 enum·설명이 있으면 모델에게 더 많은 정보가 간다 |
| 명세에만 있는 route | 구현되지 않았거나 다른 서비스다. 그 operation은 노출하지 않는다 |
| 코드에만 있는 업무 route | 명세를 재생성(springdoc, swag, utoipa, FastAPI 등)하거나, 그 route만 경로 B-1로 변환해 **두 앱을 함께 연결**한다(6절) |
| 타입이 다르다 | 원본 응답 검증이 `SCHEMA_MISMATCH`로 실패하므로 바로 드러난다. 명세를 고친다 |

### A-3. 노출할 operation과 설정 작성

```python
from a2api import ExecutionContext, HTTPDeployment, convert

operations = {
    'listOrders': {'effect': 'read',
                   'select': ['items[].id', 'items[].status', 'items[].totalAmount', 'items[].createdAt', 'total', 'hasMore'],
                   'keywords': ['주문 목록', 'orders']},
    'getOrder': {'effect': 'read', 'select': ['id', 'customerId', 'status', 'totalAmount', 'shipmentIds']},
    'cancelOrder': {'effect': 'write', 'select': ['id', 'status'],
                    'summary': '주문을 취소한다. pending/paid 상태만 가능하며 그 외는 409.'},
}
```

- 키는 OpenAPI의 `operationId`다. 공개 ID는 `namespace.operationid`(소문자, `/`와 `.`로 구분, 특수문자는 `_`)가 된다. 예: `getOrder` → `shop.getorder`, `repos/get` → `github.repos.get`.
- `effect`는 필수다. 규칙에 어긋나면(GET을 write로 등) `INVALID_CONVERSION`으로 거부된다.
- `select`(선택): 생략하면 원본 응답 전체를 보낸다. 내부 필드가 있다면 반드시 지정한다.
  - 최상위 필드 `'id'`, 중첩 `'owner.login'`, 배열 항목 `'items[].id'`, 최상위 배열 `'[].login'`.
  - 경로는 단순 object·array와 로컬 `$ref`(nullable 포함)만 지날 수 있다. `allOf`/`oneOf` 같은 조합이 있으면 `UNSUPPORTED_SELECTION` — 그 operation은 select 없이 노출하거나 wrapper로 감싼다.
- `summary`(선택): 명세의 summary를 바꾼다. 허용 값·필수 입력·상태 조건처럼 모델이 알아야 할 제약을 한 문장으로 쓴다.
- `keywords`(선택): 서버 검색 전용 단어(최대 32개). 모델에게는 보이지 않는다. 사용자가 쓰는 말(한국어 업무 용어, 약어)을 넣는다.

### A-4. 연결 정보와 인증

```python
app = convert(source, operations=operations, deployment=HTTPDeployment(
    'https://orders.internal',                     # 실제 서버 주소(경로 prefix는 path_prefix='/api')
    credential_provider=lambda context: {'Authorization': 'Bearer ' + token_for(context.actor)},
    timeout_ms=5000, deadline_ms=8000,              # 기본 1500/5000ms, 응답 상한 max_response_bytes=1MiB
))
```

- `credential_provider(context)`는 **호출마다** 신뢰할 수 있는 context로 헤더를 만든다. 사용자별 토큰을 쓰고, 하나의 높은 권한 토큰으로 모든 사용자를 대신하지 않는다.
- 고정 헤더는 `headers={...}`로 준다. 인증·쿠키를 모델 입력으로 받지 않는다.
- (1.1) 호스트가 정하는 요청 값: `request_values=lambda context, call: {'query': {...}, 'body': {...}}`. `call`은 `operationId`, `method`, `path`, `effect`를 담는다. 쓰기 미리보기 플래그·변경셋 ID·tenant 같은 값을 넣는다. 모델 입력과 이름이 겹치면 `HOST_VALUE_CONFLICT`로 호출하지 않는다.
- (1.1) 원 서버 오류 문장: 기본으로 본문은 모델에게 가지 않는다. `error_detail=lambda status, body: ...`로 안전한 부분(예: `body['error']['message']`)만 골라 `detail` 뒤에 붙인다(최대 500자).
- (1.1) 쓰기 멱등성: `idempotency_header='Idempotency-Key'`이면 `invoke(..., request_id=...)`·`ToolSession.call(..., request_id=...)`의 ID를 **쓰기(effect=write)에만** 그 헤더로 보낸다. 같은 호출을 두 번 전달할 때 같은 ID를 쓰면 원 서버가 중복을 거를 수 있다. a2api는 여전히 자동 재시도하지 않는다.
- 쓰기 요청이 전송된 뒤 시간 초과나 연결 종료가 나면 `OUTCOME_UNKNOWN`이다. 자동 재시도하지 않으므로 필요한 경우 조회로 결과를 확인한다.
- 압축 응답은 받지 않는다(`Accept-Encoding: identity`). 응답이 상한보다 크면 `RESPONSE_TOO_LARGE`다.

### A-5. 호출과 확인

```python
caller = ExecutionContext('alice', 'tenant-a', frozenset())
app.invoke('shop.getorder', {'path': {'id': 'ORD-1003'}}, context=caller)
# {'status': 'succeeded', 'data': {'id': 'ORD-1003', 'customerId': 'C-003', 'status': 'paid', ...}}
app.invoke('shop.cancelorder', {'path': {'id': 'ORD-1007'}}, context=caller)['error']['code']
# 'UPSTREAM_CONFLICT' (원 서버 409)
```

직접 호출 입력은 OpenAPI 위치를 그대로 쓴다: `{'path': {...}, 'query': {...}, 'headers': {...}, 'body': {...}}`. 모델에게는 6절의 `ToolSession`이 이를 평탄한 인자로 보여 주고 다시 원래 구조로 바꾼다.

원 서버 응답은 다음 코드로 바뀐다(본문은 모델에게 전달하지 않는다): 400/422 → `UPSTREAM_VALIDATION_FAILED`, 401/403 → `PERMISSION_DENIED`, 404 → `RESOURCE_NOT_FOUND`, 409 → `UPSTREAM_CONFLICT`, 429 → `RATE_LIMITED`, 503 → `UPSTREAM_UNAVAILABLE`, 그 밖 → `UPSTREAM_ERROR`, 시간 초과 → `DEADLINE_EXCEEDED`.

## 3. 경로 B-1 — 코드만 있는 Spring / Go / Rust / FastAPI HTTP 서비스

소스 importer는 코드를 **실행하지 않고** 구문 tree에서 route·입력 위치·DTO를 읽는다. OpenAPI를 내부에서 만들지도 않는다.

### B-1-1. 지원 범위

| importer | 읽는 route와 입력 | 읽는 DTO·출력 | 지원하지 않는 대표 경우 → 대응 |
|---|---|---|---|
| `SpringSourceImporter` | `@RestController` + class/method mapping, Get/Post/Put/Patch/Delete(Mapping), `@PathVariable`/`@RequestParam`/`@RequestHeader`/`@RequestBody`. 인증 principal·request 객체는 호스트 값으로 제외 | scalar, List/Set/Map, record/POJO(상속, 구체 generic, Lombok `@Getter/@Data/@Value`, 출력의 public getter), enum, `@Valid` 제약, `@ResponseStatus`. (1.1) 타입 없는 `ResponseEntity`/`Map` 반환은 `ResponseEntity.ok(...)`·`status(201).body(...)`·`new HashMap<>(){{ put(...) }}`·서비스 필드의 메서드 반환형·`Optional.map(lambda).orElseThrow()`·같은 클래스 helper를 따라가 타입을 읽는다. `application.properties/yml`의 `spring.jackson.*`(root wrapping, naming strategy, inclusion)를 반영한다 | 동적 경로 상수, WebFlux, custom serializer, `ResponseBodyAdvice`·binder advice → 해당 메서드는 제외하거나 wrapper. 예외 처리만 하는 `@RestControllerAdvice`는 막지 않는다 |
| `GoSourceImporter` | net/http: `HandleFunc("METHOD /path", handler)`, `r.PathValue`, `r.URL.Query().Get`, `json.NewDecoder(r.Body).Decode(&typed)`. (1.1) Gin: `r.Group("/p")`과 router를 인자로 받는 등록 함수(패키지 간 포함), `:param`, `c.Param`/`c.Query`/`DefaultQuery`/`QueryArray`, `ShouldBind*`/`Bind*`, 수신자를 binder에 넘기는 검증 객체의 `Bind(c)` | struct + JSON tag(익명·embedded struct, `binding:"required,min,max,email,oneof"`), pointer/slice/map, `time.Time`, `Encode(v)`/`c.JSON(2xx, v)`의 구체 타입, `gin.H{...}`의 값 타입(지역 변수·함수·메서드 반환형) | Echo/Chi, closure handler, `c.GetRawData`/form/file → 명시적 handler로 옮기거나 경로 B-3. `_test.go`는 읽지 않는다 |
| `RustSourceImporter` | `Router::new().route(...)` chain, (1.1) `.merge(...)`(경로 그대로)와 literal `.nest("/p", ...)`, `{p}`와 `:p` 경로, 모듈 경로로 handler 구분, `Path`/`Query`/`Json`. `State`/`Extension`/header·프로젝트의 `FromRequest` 타입(인증 사용자 등)은 호출 context 값으로 제외(`CONTEXT_EXTRACTOR` 진단) | named-field·newtype Serde struct(rename/rename_all/default/skip/flatten), 기본값 있는 generic(`Body<T = Article>`), 문자열로 직렬화하는 직접 구현 `Serialize`, `Option`/`Vec`/`HashMap`, `Json<T>`, `Result<T>`/`Result<T, E>`, `(StatusCode, Json<T>)`, `()` | Actix, wildcard 경로, 데이터를 가진 enum, custom Serde(`with`) → wrapper 또는 경로 B-3 |
| `FastAPISourceImporter` (1.1) | Python `ast`로만 읽는다(import·실행 없음). `APIRouter(prefix=)`와 `include_router(prefix=)`를 앱부터 따라감(settings 클래스 기본값 prefix는 진단과 함께 사용), `@router.get/post/...`, path·`Query`/`Path`/`Body(embed, alias)`/`Header`, 경로의 `dependencies=[Depends(...)]`와 `Depends(fn)` 안의 입력 | Pydantic model(상속·mixin, `Field(alias=, ...)`, `alias_generator`가 알려진 camel/pascal 변환이면 반영), `Optional`/`List`/`Dict`/`Literal`/`Enum`, `response_model` 또는 반환 annotation, `status_code` | form/file, 비JSON `response_class`, 알 수 없는 alias 함수 → wrapper 또는 경로 B-3. 테스트 파일은 읽지 않는다 |

한 파일 1MiB, 전체 32MiB·4,096개까지 읽고 `build/target/vendor/node_modules` 등은 건너뛴다. 전체 문법·언어별 JSON 의미 차이는 [18 문서](18-source-importers.ko.md)에 있다.

### B-1-2. 읽고 검토하기

```python
from a2api.importers import SpringSourceImporter

source = SpringSourceImporter.from_directory('src/main/java', namespace='shop')
print(source.diagnostics)                       # 구문 오류 파일
for record in source.iter_operations():
    print(record.summary())
# {'operationId': 'CustomerController.list', 'path': '/customers', 'method': 'GET',
#  'status': 'imported', 'location': 'bench/CustomerController.java:32', 'diagnostics': []}
```

`location`으로 코드 위치를 바로 찾는다. `unsupported` record의 `diagnostics`에 사유가 있다. 미지원 handler를 선택하면 `convert`가 실패하며, 타입을 추측해 `{}`로 대신하지 않는다.

(1.1) 응답 타입만 코드에서 읽을 수 없는 handler는 `untyped_output='open'`으로 가져올 수 있다: `SpringSourceImporter.from_directory(dir, namespace='shop', untyped_output='open')`. 그 operation은 출력 schema가 `{}`(모든 JSON)이고 `OUTPUT_UNTYPED` 경고가 diagnostics에 남는다. 입력은 이 옵션과 상관없이 추측하지 않는다. 같은 operation ID를 가진 handler가 둘이면 첫 handler만 가져오고 뒤의 것은 사유와 함께 `unsupported`로 보고한다(전체 가져오기를 멈추지 않는다).

source ID와 공개 ID: Spring은 `Controller.method`(→ `shop.customercontroller.list`), Go는 handler 이름(`listCustomers` → `shop.listcustomers`), Rust·FastAPI는 함수 이름(`list_customers` → `shop.list_customers`). 언어가 달라도 같은 설정을 쓰려면 `(method, path)`로 고르는 표를 만든다.

### B-1-3. 노출 설정과 변환

```python
CUSTOMER = ['id', 'name', 'email', 'tier', 'status']
EXPOSE = {   # 개발자의 결정: effect, 공개 필드, 모델용 설명
    ('GET', '/customers'): {'effect': 'read', 'summary': '고객 목록(등급·상태·도시 필터, page/limit)을 조회한다.',
                            'select': ['items[].' + n for n in CUSTOMER] + ['total', 'hasMore']},
    ('POST', '/customers/search'): {'effect': 'read', 'summary': '이름·이메일 부분 문자열로 고객을 검색한다.',
                                    'select': ['items[].' + n for n in CUSTOMER] + ['total', 'hasMore']},
    ('POST', '/tickets'): {'effect': 'write',
                           'summary': '고객의 지원 티켓을 만든다. 필수: customerId, subject, priority(low|normal|high|urgent).',
                           'select': ['id', 'customerId', 'subject', 'status', 'priority']},
}
operations = {r.operation_id: EXPOSE[(r.method.upper(), r.path)] for r in source.iter_operations()
              if r.status == 'imported' and (r.method.upper(), r.path) in EXPOSE}
app = convert(source, operations=operations, deployment=HTTPDeployment('http://customers.internal:8080'))
app.invoke('shop.customercontroller.search', {'body': {'query': 'minji'}}, context=caller)
```

`POST /customers/search`처럼 POST지만 조회인 route는 반드시 `read`로 명시한다. 관리·내부 route는 표에 넣지 않으면 노출되지 않는다.

### B-1-4. 언어별로 알아 둘 차이

코드에서 읽은 계약은 그 언어의 실제 JSON 동작을 따른다. 그래서 같은 업무라도 descriptor가 다를 수 있다.

| 상황 | Spring | Go | Rust |
|---|---|---|---|
| 필수 body 필드 | `@NotBlank`/`@NotNull`이면 required | net/http는 **required 없음**(누락 시 zero value). Gin은 `binding:"required"`면 required. 단 저장된 값으로 미리 채운 수정 form(`NewXFillWith(model)` 뒤 `Bind`)은 required를 빼고 부분 수정으로 읽는다 | `Option`이 아니면 required |
| 필수 필드를 빠뜨린 호출 | a2api가 호출 전 `INVALID_INPUT` | 원 서버가 판단(예: 400 → `UPSTREAM_VALIDATION_FAILED`) | a2api가 호출 전 `INVALID_INPUT` |
| query 숫자 | `Integer` → integer | `Query().Get` → **string** | `Option<u32>` → integer |
| enum | Java `enum` → enum 값 목록 | string | string |
| 목록 응답 | 참조 타입은 nullable | slice는 nullable(`[array, null]`) | `Vec`은 array |

- Go의 string query에 모델이 `page: 1`처럼 숫자를 보내도 `ToolSession`이 텍스트로 바꿔 전달한다(path/query/header). (1.1) body의 string 필드에 정수가 오면(ID `20431` 등) 그 숫자의 문자열로 바꾼다. 실수·boolean은 body에서 바꾸지 않는다.
- enum이나 필수 정보가 코드에 없으면 **summary에 허용 값과 필수 입력을 적는다**(위 `POST /tickets` 예). 벤치마크에서 이것만으로 4개 언어의 정확도가 같았다.
- 빈 query 값(`customerId=`)을 "필터 없음"으로 볼지 "빈 값과 일치"로 볼지는 구현마다 다를 수 있다. 실제로 Spring/Rust와 Python/Go가 달라 오답이 난 적이 있다([34 문서](34-completion-results.ko.md) 6절). 서버에서 빈 값을 무시하도록 맞추는 것이 안전하다.

## 4. 경로 B-2 — HTTP 없이 Python 코드만 있을 때

기존 객체를 그대로 노출하지 않고, 입력·공개 필드·효과를 정하는 얇은 wrapper를 등록한다.

```python
from typing import Literal, TypedDict
from a2api import A2APIError, Application, ExecutionContext, capability

class Order(TypedDict):
    id: str
    state: Literal['pending', 'paid', 'shipped', 'cancelled']
    amount: int

def public(row) -> Order:
    return {'id': row.id, 'state': row.state, 'amount': row.amount}      # internal_note는 반환하지 않는다

@capability(id='orders.get', effect='read', keywords=['주문', '조회', 'order'])
def get_order(orderId: str, *, context: ExecutionContext) -> Order:
    """주문 번호로 내 주문의 상태와 금액을 조회한다."""
    row = SERVICE.find_visible(orderId, context.actor)                  # 기존 권한 검사를 그대로 사용
    if row is None:
        raise A2APIError('RESOURCE_NOT_FOUND', 'Order does not exist or is not visible.', status=404)
    return public(row)

@capability(id='orders.cancel', effect='write', keywords=['주문', '취소', 'cancel'])
async def cancel_order(orderId: str, *, context: ExecutionContext) -> Order:
    """내 주문을 취소한다. pending/paid 상태만 취소할 수 있다."""
    try:
        return public(SERVICE.cancel(orderId, context.actor))
    except ValueError:
        raise A2APIError('UPSTREAM_CONFLICT', 'The order state does not allow cancellation.', status=409) from None

app = Application([get_order, cancel_order])
```

- ID는 점으로 구분한 소문자(`orders.get`), effect는 `read`/`write`. 첫 docstring 줄이 summary가 된다(`summary=`로 바꿀 수 있음).
- 타입 힌트에서 schema를 만든다: `str/int/float/bool/None`, `Literal`, `X | None`, `list[X]`, `dict[str, X]`, `TypedDict`(`Required`/`NotRequired`). 그 밖의 타입은 `input_schema=`/`output_schema=`로 직접 준다.
- `context`는 keyword-only `ExecutionContext`로 받으며 모델 입력 schema에 들어가지 않는다.
- 동기·`async def` 모두 된다. generator, positional-only, `*args/**kwargs`는 named wrapper가 필요하다.
- 업무 오류는 `A2APIError(code, detail, status=...)`로 올린다. 그 밖의 예외는 내용을 숨긴 `HANDLER_ERROR`가 된다. 실패한 쓰기를 자동 재시도하지 않는다.

예제 실행 결과: 다른 사용자의 주문은 `RESOURCE_NOT_FOUND`, `{'id': 'ORD-1'}`처럼 잘못된 인자는 `issues=[{'rule':'required','missing':['orderId']}, {'rule':'additionalProperties','unexpected':['id'],'allowed':['orderId']}]`로 모델이 바로 고칠 수 있다.

## 5. 경로 B-3 — 그 밖의 언어·프레임워크

소스 importer가 없는 경우(Node/Express·NestJS, C#/ASP.NET, PHP, Kotlin Ktor, Go Echo/Chi, Rust Actix, Python Flask/Django 등)는 다음 순서로 고른다.

1. **프레임워크가 OpenAPI를 만들 수 있으면** 생성해서 경로 A로 간다(NestJS `@nestjs/swagger`, ASP.NET Swashbuckle/NSwag, Echo/Chi `swag`, Actix `utoipa` 등). 생성된 명세는 A-2처럼 실제 응답으로 확인한다.
2. **노출할 route가 몇 개뿐이면** 그 route만 담은 작은 OpenAPI를 직접 쓴다. 전체 서비스 명세가 필요하지 않다.
3. **여러 호출을 묶거나 응답을 가공해야 하면** Python wrapper(B-2)에서 기존 HTTP를 호출한다. 이미 변환한 앱을 wrapper 안에서 재사용할 수 있다.

```python
@capability(id='order.shipping_status', effect='read')
def shipping_status(orderId: str, *, context: ExecutionContext) -> ShippingView:
    """주문의 모든 배송 상태를 한 번에 조회한다."""
    order = http_app.invoke('legacy.getorder', {'path': {'orderId': orderId}}, context=context)
    ...  # 실패 envelope를 그대로 A2APIError로 바꾸고, 배송 조회를 이어서 수행
```

## 5-1. 경로 C — 도구 목록·이름 호출 서비스와 레거시 표현(1.1)

registry형 백엔드나 화면 단위 레거시 서비스는 OpenAPI 대신 **도구 목록**(`GET /v1/tools`: `tool`, `summary`, 닫힌 `input_schema`)을 내주고 `POST /v1/tools/{name}`에 `{"input": {...}}`로 호출받는 경우가 많다.

```python
from a2api.importers import ToolCatalogImporter

source = ToolCatalogImporter.from_url(origin + '/v1/tools', namespace='claims')    # 또는 ToolCatalogImporter(list_or_dict)
kinds = {r.operation_id: r.entry['kind'] for r in source.iter_operations()}      # entry: 목록 항목 원본
app = convert(source, operations={n: {'effect': 'read' if k == 'read' else 'write'} for n, k in kinds.items()},
              vocabulary=VOCABULARY, deployment=HTTPDeployment(origin, request_values=..., error_detail=...))
```

- 이름 호출 경로(`call_path`), 본문 감싸기 이름(`envelope='input'`), 키 이름(`name_key`, `summary_key`, `input_key`)을 바꿀 수 있다. camelCase 이름은 ID에서 단어를 나눈다(`getClmGridList` → `claims.get_clm_grid_list`, 함수 이름 `claims_get_clm_grid_list`).
- 입력 schema가 객체가 아닌 항목, 같은 이름은 `unsupported`로 보고한다.

**레거시 표현 보완 — `vocabulary`**: 약어 필드(`clmStatCd`)와 코드값(`"R10"`)은 모델이 해석하기 어렵다. 소스의 코드표·필드 주석에서 읽을 수 있는 것만 적는다.

```python
VOCABULARY = {
    'rename': {'clmStatCd': 'claim_status', 'clmNo': 'claim_id', 'pageNo': 'page', ...},     # 입력·출력 공통
    'codes': {'clmStatCd': {'R10': 'requested', 'R20': 'approved', 'R90': 'completed'}},   # 코드 → 단어
    'describe': {'pageNo': 'Page number, from 1.'},                                         # 코드에만 있는 규칙
}
```

모델은 `claim_status: "requested"`를 보고 보내며, a2api가 공개 schema로 먼저 검증한 뒤 원래 이름·코드로 바꿔 호출한다. 응답도 같은 표로 바꾼다(표에 없는 코드는 그대로 둔다). 예제 실행 결과(`legacy_screens.py`):

```text
model sees: {"properties": {"claim_status": {"enum": ["requested", "approved", "completed"], ...}, "page": {..., "description": "Page number, from 1."}}}
result: {"status":"succeeded","data":{"claims":[{"claim_id":"clm_1","claim_status":"requested","claim_amount":120}],"page":1}}
result: {"status":"succeeded","data":{"result_code":"0000","refund_id":"rfnd_9","changeSet":"cs_alice"}}
result: {"status":"failed","error":{"code":"UPSTREAM_VALIDATION_FAILED","detail":"... (HTTP 422) Invalid paging."},"hint":"..."}
```

업무 규칙이 사람의 머릿속에만 있으면(할인 상한 등) vocabulary로도 알 수 없다. a-commerce 실측에서 이런 레거시 화면 API는 a2api로 바꿔도 규칙이 필요한 작업을 풀지 못했다([39 문서](39-improvement-results.ko.md)).

## 6. LLM에 연결하기

여러 앱을 섞어도 된다: `[http_app, python_app]`.

**MCP 서버**(Claude Desktop, IDE, 에이전트 프레임워크): 도구는 API 수와 무관하게 `a2api.discover/describe/invoke` 세 개다.

```python
import anyio
from a2api.mcp_bridge import serve_stdio
anyio.run(serve_stdio, [http_app, python_app], caller)
```

**직접 모델을 호출하는 호스트**(Chat Completions 형식 function calling):

```python
from a2api import ToolSession
session = ToolSession([http_app, python_app], caller)
await session.auto(user_message)            # 약 20개 이하(10KB)는 전체 함수, 그 이상은 질문으로 8개를 미리 찾고 검색 도구 제공
tools = session.tools()                     # 매 모델 요청 직전에 다시 읽는다
payload = await session.call(name, args)    # 검증 후 기존 invoke, 재시도 없음
text = session.render(payload)              # 모델에게 보낼 compact 결과(실패 시 code/detail/hint)
```

- 모델에게 보이는 함수 이름은 ID에서 만든 `shop_getorder` 형태다. 입력은 path/query/body가 충돌 없이 평탄화된다.
- 사용자·tenant·권한이 바뀌면 새 `ToolSession`을 만든다.
- (1.1) 함수 목록 순서는 호출·검색 뒤에도 바뀌지 않는다(서버 prompt cache 재사용). 예산을 넘으면 가장 오래 쓰지 않은 함수가 빠진다.
- (1.1) 검색이 새 함수를 찾지 못하면 결과에 "새 함수 없음, 다시 검색하지 말고 부족한 것을 말하라"는 안내가 붙는다. 같은 인자로 이미 실패한 호출, 마지막 쓰기 이후 같은 인자로 이미 성공한 조회에는 반복 안내가 붙는다.
- 작업당 모델 문맥은 API 규모와 거의 무관하게 약 4.5–7k 토큰이었다(벤치마크, [34 문서](34-completion-results.ko.md)).

## 7. 검증 체크리스트

- [ ] 노출할 operation이 모두 `imported`이고, 미지원 항목은 사유를 확인했다.
- [ ] (경로 A) 명세와 코드의 route 차이를 확인했다.
- [ ] 모든 POST의 effect를 명시했고, 조회용 POST는 `read`다.
- [ ] `select`로 내부 필드를 숨겼고, 실제 응답으로 `SCHEMA_MISMATCH`가 없는지 확인했다.
- [ ] `credential_provider`가 사용자별 credential을 쓰고, 원 서버가 객체 권한을 검사한다.
- [ ] 정상·404·409·400·시간 초과를 직접 호출로 확인했다(쓰기는 테스트 데이터에서).
- [ ] summary에 허용 값·필수 입력·상태 조건을 적었다(특히 Go/Rust처럼 enum·required가 코드에 없을 때).
- [ ] MCP 또는 `ToolSession`으로 실제 모델 질문 몇 개를 실행해 호출 인자·결과를 확인했다(`examples/model-client`, `examples/benchmark`).

## 8. 오류별 해결

| 단계 | 코드 | 원인 → 해결 |
|---|---|---|
| convert | `INVALID_CONVERSION` | effect 누락·메서드와 effect 불일치·지원하지 않는 옵션 키 |
| convert | `INVALID_SELECTION` | 없는 operationId 또는 응답에 없는 select 필드, 겹치는 경로 |
| convert | `UNSUPPORTED_SELECTION` | select 경로가 조합 schema를 지남 → select를 줄이거나 wrapper |
| convert | `CONVERT_OPERATION_UNSUPPORTED` | 선택한 operation이 import 불가 → `record.summary()`의 사유 확인 |
| invoke | `INVALID_INPUT` | 입력이 schema와 다름. `issues`의 `missing`/`unexpected`/`expected`를 본다 |
| invoke | `SCHEMA_MISMATCH` | 원 서버 응답이 명세/DTO와 다름 → 명세나 코드 수정 |
| invoke | `UPSTREAM_*`, `PERMISSION_DENIED`, `RESOURCE_NOT_FOUND` | 원 서버의 응답(A-5의 대응표) |
| invoke | `DEADLINE_EXCEEDED` / `OUTCOME_UNKNOWN` | 느린 서버는 `timeout_ms`를 늘린다. 쓰기의 `OUTCOME_UNKNOWN`은 조회로 확인 |

## 9. 실제 공개 프로젝트에서 확인한 변환 결과(1.1)

같은 RealWorld(Conduit) API를 구현한 공개 프로젝트 4개의 **코드만** 읽어(빌드·실행 없음) 공식 OpenAPI 19개 operation과 비교했다. 재현: `python examples/realworld/compare.py <checkouts>`.

| 프로젝트 | 1.0 | 1.1 operation | 필드 이름 일치 | 남은 차이(실제 구현의 동작) |
|---|---|---|---|---|
| Spring Boot (`gothinkster/spring-boot-realworld-example-app`) | 0/19(전역 advice로 전부 거부) | 19/19 | 18/19 | 글 수정이 `tagList`를 받지 않음 |
| Go Gin (`gothinkster/golang-gin-realworld-example-app`) | 0(Gin 미지원) | 19/19 | 16/19 | 가입이 bio/image도 받음, 삭제가 200 `{"article": "delete success"}` |
| Rust Axum (`launchbadge/realworld-axum-sqlx`) | 가져오기 중단(handler 이름 충돌) | 19/19 | 18/19 | 글 수정이 `tagList`를 받지 않음 |
| Python FastAPI (`nsidnev/fastapi-realworld-example-app`) | importer 없음 | 19/19 | 18/19 | 글 수정이 `tagList`를 받지 않음 |

명세를 따르는 서버에 각 구현의 동작 차이(생성 상태 코드, 빈 bio의 `""`/`null`, 삭제 응답)를 재현해 모든 변환 operation을 실제로 호출하면 다섯 경로(OpenAPI·Spring·Go·Rust·FastAPI) 모두 19/19가 검증을 통과했다(`python examples/realworld/evaluate.py verify <checkouts>`). 실제 GitHub REST 명세는 전체 메서드 1,254개 중 1,230개를 변환한다(1.0: 1,228).

## 10. 선택적인 관리 기능

변환 결과를 파일로 고정·검토하고 명세 변경을 추적해야 하는 조직은 기존 관리 기능을 쓸 수 있다: `import-openapi`(비활성 초안), `build`(검토 설정으로 계약 빌드), `diff-openapi`/`regenerate`(변경 영향과 증분 재생성), `prepare-review`/`approve-review`(선택 재승인). 첫 호출의 필수 단계는 아니다. [08](08-review-builder.ko.md)·[09](09-source-diff-and-regeneration.ko.md)·[10](10-selective-reapproval.ko.md) 문서를 참고한다.
