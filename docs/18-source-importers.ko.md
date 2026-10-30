# 소스에서 바로 호출하기: Java/Spring·Go·Rust

OpenAPI 파일 없이 명시적인 HTTP route와 DTO를 AST에서 읽어 기존 `convert`에 연결한다. 파싱 때 언어 런타임·소스 코드·빌드 스크립트를 실행하지 않는다. Java/Spring MVC, Go net/http ServeMux, Rust Axum/Serde의 아래 지원 범위를 구현했으며, 해당 언어의 모든 프레임워크나 임의 동적 코드를 처리하는 것은 아니다.

## 설치와 첫 호출

```bash
python -m pip install -e ".[source,mcp]"
```

실제 HTTP 서버는 기존 서비스가 담당한다. importer만 사용하는 데 JDK/Go/Rust 설치가 필요하지 않다.

```python
from a2api import ExecutionContext, HTTPDeployment, convert
from a2api.importers import SpringSourceImporter

source = SpringSourceImporter.from_directory(
    "examples/source-http/spring/src/main/java", namespace="shop")
app = convert(source, operations={
    "ItemController.get": {"effect": "read", "select": ["id", "name"]},
    "ItemController.create": {"effect": "write", "select": ["id", "name"]},
}, deployment=HTTPDeployment("http://127.0.0.1:8080"))
caller = ExecutionContext("sample-user", "sample-tenant", frozenset())
print(app.describe("shop.itemcontroller.create"))
print(app.invoke("shop.itemcontroller.create", {"body": {"name": "sample"}}, context=caller))
```

이 코드는 importer/convert 사용법이며, 지정 origin에 해당 합성 Spring 앱이 실행돼 있어야 invoke가 성공한다. 서버 실행까지 포함한 검증 명령은 아래에 있다. 실제 서비스에서는 host가 검증한 context와 `HTTPDeployment(..., credential_provider=...)`를 사용한다.

Go와 Rust는 같은 방식으로 importer만 선택한다.

```python
from a2api.importers import GoSourceImporter, RustSourceImporter

go_source = GoSourceImporter.from_directory("examples/source-http/go", namespace="go_shop")
rust_source = RustSourceImporter.from_directory("examples/source-http/rust/src", namespace="rust_shop")
for item in go_source.iter_operations():
    print(item.summary())  # operationId·route·method·지원 여부·소스 위치
```

Go 예제의 ID는 `getItem`, `createItem` 등 named handler이고 Rust는 `get_item`, `create_item` 등이다. 공개 ID는 namespace와 source ID의 소문자/점 표기로 생성한다. 같은 이름의 handler가 중복되면 임의로 하나를 고르지 않고 오류를 반환한다. Java는 `Controller.method`를 선택하며 overload/이름 충돌 시 소스 범위를 좁히거나 wrapper가 필요하다.

## 지원 범위

| importer | route와 입력 | DTO와 출력 | 지원하지 않는 대표 경우 |
|---|---|---|---|
| `SpringSourceImporter` | `@RestController`, class/method mapping, Get/Post/Put/Patch/Delete 및 명시적 RequestMapping method, PathVariable/RequestParam/RequestHeader/RequestBody, DTO query binding | scalar·배열/List/Set·로컬 POJO/record·상속·구체적인 generic·ResponseEntity, 기본 Jackson 필드명/제외, `@Valid`의 지원 검증 제약 | 동적 경로 상수/여러 mapping, 전역 advice, 조건부 mapping, 외부/동명 타입, custom serializer·검증 그룹, String text 응답 |
| `GoSourceImporter` | `http.HandleFunc` 또는 로컬 `http.NewServeMux`의 `HandleFunc("METHOD /path", namedHandler)`, 직접 PathValue/Query.Get, typed JSON Decode | scalar·pointer·slice/고정 배열·로컬 struct·JSON tag, 직접 NewEncoder.Encode의 구체적 반환 타입 | Gin/Echo/Chi, closure/동적 route, 간접 decoder/response helper, embedded struct, custom JSON method, base64 byte slice |
| `RustSourceImporter` | literal `Router::new().route`와 get/head/post/put/patch/delete handler 연결, Axum Path/Query/Json, State 제외 | scalar·Option·Vec·로컬 named-field Serde struct, rename/rename_all(camelCase/snake_case)/default/skip, Json/Result/정적 StatusCode tuple | Actix, macro route, nested/merged router prefix, custom Serde·trait·외부/모호한 타입·동적 응답 |

문법 tree에 없는 주석/문자열의 route 표현은 endpoint로 추출하지 않는다. 해석 불가능한 항목은 `unsupported` record와 위치/사유를 제공한다. 구문 오류 파일은 `source.diagnostics`에 남긴다. 선택한 handler가 없거나 미지원이면 convert가 실패하며, 타입을 `{}`로 대체해 실행하지 않는다. OpenAPI를 내부에서 새로 만들어 기존 importer에 돌리는 방식도 아니다.

소스는 파일당 1 MiB, 전체 32 MiB/최대 4,096개로 제한하며 build/target/vendor/node_modules/artifacts와 symlink 파일을 제외한다. 이 제한은 전체 앱의 활성 route나 classpath 해석을 보장하지 않는다. 선택한 소스에 없는 전역 설정·조건부 빌드·Jackson 설정/외부 공통 모듈은 별도 근거가 필요하다.

필드 타입과 언어별 JSON 의미도 구별한다. Go에서는 빠진 입력 필드의 zero value와 pointer/slice의 null, 출력의 omitempty를 구별한다. Rust는 Option/default와 출력 skip 조건을 구별한다. Java reference 필드는 null을 허용하고 적용 가능한 `@Valid`·비-null 제약을 반영한다. Java LocalDateTime을 UTC offset이 있는 RFC3339 값이라고 광고하지 않는다. 모든 날짜/custom serializer나 언어 타입 시스템 전체를 구현한 것은 아니다.

`@AuthenticationPrincipal` 등 알려진 host 인자는 업무 schema에서 제외하고 Authorization/Cookie는 host credential provider에 맡긴다. 이것이 인증을 구현하거나 DTO 내부의 임의 member/tenant 필드를 자동 보호한다는 뜻은 아니다. 원 서버의 권한·AOP·쿠키/보안 문맥 검사를 유지해야 한다. `@Hidden` 같은 문서 표시만으로 실제 JSON 필드를 제거하지 않는다. 조회 API의 공개 input/output을 더 좁혀야 하면 기존 Python 조회 wrapper를 사용할 수 있다. 직접 HTTP 쓰기 앱은 이번에 지원한 원본 입력과 최상위 출력 선택 범위에서 사용한다.

## GET·POST·PUT·PATCH·DELETE·HEAD 실행

| HTTP 메서드 | 직접 convert에서 필요한 effect |
|---|---|
| GET, HEAD | `read` |
| POST | 조회라면 `read`, 생성/변경이라면 `write`를 host가 명시 |
| PUT, PATCH, DELETE | `write` |

UPDATE라는 메서드를 새로 만들지 않고 PUT(교체)·PATCH(부분 수정)로 지원한다. GET/HEAD를 write로, PUT/PATCH/DELETE를 read로 지정하면 거부한다. HTTP 메서드만 보고 POST 검색의 업무 효과를 자동 판별하지 않는다. 선택하지 않은 operation은 호출할 수 없다.

기존 OpenAPI에도 같은 직접 호출 정책을 적용한다. 기본 importer의 GET 선택은 유지하므로, 여러 메서드를 읽을 때 선택을 명시한다.

```python
source = OpenAPIImporter.from_file("api.json", methods={"GET", "HEAD", "POST", "PUT", "PATCH", "DELETE"})
# 이후 같은 convert(... operations={"createItem": {"effect": "write"}}, deployment=...) 사용
```

직접 호출 앱은 입력 → 원본 응답 → 선택한 공개 출력 검증을 유지한다. `select`는 기존의 단순 최상위 객체 필드 선택이며 배열/복합 변환기를 추가하지 않았다. source importer는 확인된 성공 status를 binding에 선언한다. 201 JSON 생성과 204 빈 삭제는 `httpStatus`와 `data: null`로 구별한다. 모든 HTTP 호출은 한 번이며 자동 재시도하지 않는다. 쓰기 전송 후 연결 중단/timeout은 `OUTCOME_UNKNOWN`일 수 있고, 응답 검증 실패도 backend 작업의 rollback을 뜻하지 않는다.

기존 전체 manifest Runtime·review/build 경로는 계속 읽기 전용이다. Python `@capability`도 기존 조회 함수 범위를 유지한다. 이번 확장은 OpenAPI/새 소스의 **직접 HTTP 앱**에 한정한다.

## 실제 런타임 예제 실행

합성 코드만 제공하며 회사 소스·운영 API·LLM은 사용하지 않는다. 세 서버는 loopback 임시 포트에서 실행하고 검증 후 종료한다.

일반 환경은 JDK 25/Maven, Go 1.22+, Rust/Cargo 및 C 링커가 필요하다. 이 프로젝트의 Spring 예제는 Boot 4.0.0, Rust는 Axum 0.8.6과 Cargo.lock을 사용한다. 시스템 설치 예시는 다음과 같다. OS에 해당 패키지가 있어야 한다.

```bash
sudo apt-get update
sudo apt-get install openjdk-25-jdk-headless maven golang-go rustc cargo build-essential
python examples/source-http/verify.py
```

현재 서버는 sudo 대화형 인증이 필요해 시스템 설치를 진행하지 않았다. 공식 배포본/Ubuntu 패키지를 `artifacts/toolchains/`에 설치했다. Java용 로컬 truststore에는 기존 시스템 CA만 넣었으며 TLS 검증은 유지했다. C 컴파일러가 없어 Rust 링크에 공식 Zig 도구를 로컬 설치했다. 전역 PATH·셸 프로필·시스템 설정은 변경하지 않았다. 검증 명령은 설치 경로 기록을 자동으로 사용한다.

```bash
cd /home/khs/workspace/a2api
.venv-mcp/bin/python examples/source-http/verify.py
# 하나씩 검증하려면
.venv-mcp/bin/python examples/source-http/verify.py --language spring
.venv-mcp/bin/python examples/source-http/verify.py --language go
.venv-mcp/bin/python examples/source-http/verify.py --language rust
```

각 언어는 직접 호출 8회와 실제 MCP stdio 호출 8회로 조회·HEAD·생성·교체·부분 수정·POST 검색·삭제·삭제 후 404를 확인한다. 생성/변경의 내부 필드는 서버에서 공개 출력 전에 제거한다. 빌드/서버 로그와 마지막 실행 JSON은 `artifacts/source-http/`에 둔다. 최초 빌드는 공식 Maven/crates 의존성 다운로드가 필요하며 일반 테스트에서는 언어 빌드를 실행하지 않는다.

이미 해당 예제 서버가 실행 중이면 MCP host만 실행할 수 있다.

```bash
.venv-mcp/bin/python examples/source-http/mcp_server.py --language spring --origin http://127.0.0.1:8080
```

도구는 여전히 discover/describe/invoke 세 개다. describe에는 선택한 schema와 read/write effect만 나온다. 쓰기 앱이 연결된 invoke에는 보수적으로 readOnly=false, idempotent=false, destructive=true를 광고한다. discover/describe는 읽기 도구로 유지하며 개별 API schema를 tools/list에 나열하지 않는다. 이 annotation은 host의 권한/승인 정책을 대신하지 않는다.

## 검사와 근거

```bash
.venv-mcp/bin/python -m unittest discover -s tests -p 'test_source_*.py' -v
.venv-mcp/bin/python -m unittest discover -s tests -v
```

[개발 계획](17-source-importers-plan.ko.md), [실제 실행/버전 기록](evidence/source-importers.json), [합성 예제](../examples/source-http/README.md)를 참고한다. 이 결과는 명시한 문법 profile과 합성 서버에서의 검증이며 모든 Java/Go/Rust 제품의 자동 전환이나 실제 LLM 성능을 증명하지 않는다.

참조: [Spring mapping](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-requestmapping.html), [Go ServeMux](https://pkg.go.dev/net/http#ServeMux), [Axum](https://github.com/tokio-rs/axum), [Tree-sitter Python API](https://tree-sitter.github.io/py-tree-sitter/).
