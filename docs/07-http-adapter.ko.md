# HTTP 어댑터 확장

구현일: 2026-10-28. HTTP transport가 GET 외 HEAD·POST·PUT·PATCH·DELETE와 JSON 요청 본문, 명시적인 2xx 응답 codec, 호스트 인증 주입을 지원한다. 기존 `HTTPRoute(origin, path, path_parameters, headers, query_parameters, response_envelope)` 호출은 GET/200 JSON 기본값을 유지한다.

## 제공하는 기능

| 영역 | 동작 |
|---|---|
| 메서드 | GET, HEAD, POST, PUT, PATCH, DELETE |
| 요청 본문 | pointer로 지정한 값을 JSON 직렬화, 필수/선택 구분, 기본 1 MiB 제한 |
| 계약 검사 | 어댑터 직접 호출에서도 Operation 입력·출력 스키마 검증 |
| parameter | 기존 path/query 직렬화와 simple scalar header parameter |
| 응답 | 상태 코드마다 JSON 또는 empty codec을 명시 |
| 상태 보존 | 선택한 envelope 필드에 실제 HTTP status 반환 |
| 인증 | 고정 배포 headers 또는 context별 `credential_provider` |
| 오류 | 401/403/404/409/422/429 매핑, 비공개 backend body 제외 |
| 불확실한 변경 | 요청 전송 이후 timeout/연결 유실 시 `OUTCOME_UNKNOWN`, 재시도 0회 |

form·multipart·binary·streaming·압축 응답 codec과 OAuth 토큰 발급/refresh, 자동 pagination, polling은 후속 범위다. 기존 socket timeout·전체 호출 예산·응답 크기 제한을 계속 적용한다. DNS·느린 response header·호스트 credential provider를 강제로 중단하는 hard deadline은 구현하지 않았다.

## 명시적인 배포 바인딩

```python
from a2api import HTTPAdapter, HTTPHeaderParameter, HTTPResponse, HTTPRoute

route = HTTPRoute(
    "https://orders.internal.example",
    "/orders/{orderId}",
    path_parameters={"orderId": "/path/orderId"},
    method="PATCH",
    request_body_pointer="/body",
    request_body_required=True,
    request_media_type="application/json",
    header_parameters={"If-Match": HTTPHeaderParameter("/headers/revision", required=True)},
    responses={200: HTTPResponse(), 202: HTTPResponse(), 204: HTTPResponse(None)},
    response_envelope="result",
    response_status_field="httpStatus",
    credential_provider=lambda context: credentials_for(context),  # 호스트 구현
)
adapter = HTTPAdapter({("orders", "updateOrder"): route}, max_request_bytes=262144)
```

호스트의 `credentials_for(context)`는 `{"Authorization": "Bearer ..."}`처럼 header mapping을 반환한다. 호출마다 인증된 actor·tenant·scope를 보고 자격 증명을 선택하며, provider의 예외·반환한 비밀값을 public 오류에 싣지 않는다. provider는 바인딩에만 존재하고 IR·생성 파일에 저장되지 않는다. 함수의 bounded execution과 토큰 발급/갱신은 호스트가 책임진다.

static header, caller header, credential provider의 이름 충돌을 거부한다. `Host`, framing·content codec 관련 header와 `X-A2API-Actor/Tenant`는 어댑터가 관리한다. caller header binding으로 `Authorization`, `Proxy-Authorization`, `Cookie`를 지정할 수 없다. header 이름은 대소문자를 구분하지 않으며 CR/LF나 제어 문자를 포함한 값은 전송 전에 거부한다.

호출할 `Operation.http_method`도 `PATCH`여야 한다. manifest의 operation에 `"httpMethod": "PATCH"`를 선언하면 컴파일 시 IR에 보존된다. 생략한 기존 계약은 GET이다. 배포 route와 operation의 메서드가 다르면 네트워크 요청 전에 실패한다.

## 본문과 응답의 의미

`request_body_pointer="/body"`는 입력의 `body` 값을 그대로 JSON으로 직렬화한다. 선택 body를 생략하면 보내지 않고, `body: null`은 `null` 네 바이트를 보낸다. 배열·scalar도 사용할 수 있다. 비유한 수, JSON이 아닌 값, 잘못된 UTF-8 문자열, 크기 초과를 전송 전에 거부한다. GET/HEAD request body는 지원하지 않는다.

`HTTPResponse()`는 JSON, `HTTPResponse("application/vnd.example+json")`는 해당 JSON media type, `HTTPResponse(None)`는 빈 본문이다. 선언한 2xx만 성공으로 받아들이고 redirect를 따라가지 않는다. HEAD/204/205는 빈 codec이어야 한다. HEAD는 GET 표현의 Content-Length가 있어도 JSON을 읽으려 하지 않는다. 이 동작은 [HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.3.2)에 따른다.

envelope와 status field를 지정하면 다음처럼 반환한다.

```json
{"result": null, "httpStatus": 204}
```

202도 status를 유지한다. 이는 요청 수락이며 업무 처리가 완료됐다는 선언은 아니다. [RFC 9110의 202 정의](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.3.3)에 맞춰 후속 결과 조회는 별도 계약으로 작성해야 한다. 자동 polling을 시작하지 않는다.

변경 요청을 보낸 뒤 연결이 끊기거나 timeout이 발생하면 backend가 이미 반영했을 수 있다. 어댑터는 `OUTCOME_UNKNOWN`을 반환하며 재전송하지 않는다. 멱등 키 저장, 결과 대조, prepare/commit 같은 업무 실행 보장은 별도 구현 대상이다. 입력·필수 매개변수·배포 설정 오류는 요청 전에 실패하며, 응답의 409/422 등은 각각 `UPSTREAM_CONFLICT`/`UPSTREAM_VALIDATION_FAILED`로 보고한다.

## OpenAPI 연결

기본 importer는 GET만 선택한다. 다른 메서드를 검토하려면 명시적으로 선택한다.

```bash
python -m a2api import-openapi examples/github-openapi/api.github.com.json.gz \
  --namespace github --output artifacts/github-http \
  --methods GET HEAD POST PUT PATCH DELETE
```

라이브러리는 `OpenAPIImporter.from_file(path, methods={"GET", "POST"})`를 사용한다. 보고서의 `requestedMethods`가 선택을 기록한다. 다른 메서드는 `METHOD_NOT_SELECTED`로 목록에 남는다.

JSON request body를 `inputSchema.body`에 보존하고, 일반 header parameter를 `inputSchema.headers`에 넣는다. 응답의 명시적 2xx마다 JSON/empty codec을 만들며, 여러 상태의 서로 다른 응답 타입은 `httpStatus`에 따른 조건 스키마로 연결한다. 문서에 `content`가 없는 응답은 empty codec으로 가져오고, 실제로 본문이 오면 적합성 오류를 반환한다. 상태 범위 `2XX`, 비JSON 본문, 기타 미지원 형식은 operation별 진단으로 남긴다.

생성된 `record.http_route(origin, credential_provider=...)`는 이 정보를 배포 바인딩으로 구성한다. 원본 servers와 security는 provenance에 보존하며, origin이나 credential을 자동 선택하지 않는다. 입력·출력 스키마는 별도로 참조를 묶어 요청에 응답용 전체 스키마를 복제하지 않는다. 일반적인 readOnly/writeOnly projection은 후속 범위다. 직접 선언된 필수 writeOnly 요청 필드는 허용하고, 필수 readOnly 요청 필드는 검토 필요 진단으로 남긴다.

공식 GitHub 전체 명세 1,254개에서 결과는 다음과 같다.

| 선택 | 생성 IR | 미선택 | 미지원 |
|---|---:|---:|---:|
| 기본 GET | 633 | 599 | 22 |
| 지원 메서드 전체 | 1,228 | 0 | 26 |

전체 선택의 미지원 26개는 명시적 2xx 없음 15, 응답 codec 3, 요청 body codec 2, parameter schema 5, GET request body 1이다. 상세 이유는 [전체 메서드 보고서](../examples/github-openapi/import-report-all-methods.json)에 있다. 생성 수는 실행 검증 수나 활성 도구 수가 아니다.

## 실행 정책과 transport의 경계

생성 capability는 계속 `openapi-draft`, `enabled=false`, `effects=unknown`, `approval=review_required`다. transport에 POST를 추가해도 discover/describe/invoke 또는 MCP에서 변경 도구가 활성화되지 않는다. compiler와 Runtime은 활성 MVP operation을 GET/HEAD로 제한한다. 효과를 read로 표시하고 POST route를 연결해도 활성화·바인딩 검사를 통과하지 못한다.

조회 계약은 별도 [검토 설정과 빌더](08-review-builder.ko.md)로 projection·권한·관계 검사를 명시해 생성할 수 있다. `ReviewedHTTPAdapter`가 source HTTP 검증을 유지하면서 검토한 입력과 반환 필드로 연결한다. 원래 import 초안은 변경하지 않는다.

이번 구현의 변경 메서드는 호스트가 명시적으로 호출하는 어댑터와 격리된 transport 검증에서 사용할 수 있다. 에이전트를 통한 운영 변경 업무에는 검토한 변경 정책·승인·멱등성·결과 대조를 먼저 구현해야 한다.

## 재현

```bash
python -m pip install -e ".[mcp,openapi]"
python -W error::ResourceWarning -m unittest discover -s tests -v
python examples/http-adapter/verify.py
python examples/github-openapi/verify_import.py \
  --output artifacts/github-http-benchmark --all-methods
```

`examples/http-adapter/verify.py`는 공식 GitHub의 이슈 생성·조회·수정·잠금·label 삭제 계약을 읽어 실제 loopback HTTP에서 POST/GET/PATCH/PUT/DELETE를 각각 한 번 호출한다. 응답은 공식 Issue 예제를 바탕으로 한 로컬 fixture이며 입력·응답을 모두 생성 스키마로 검증한다. 외부 요청과 활성 capability는 0개다. HEAD·202·빈 응답·요청 크기·인증 context·응답 유실/timeout·재시도 방지는 별도 자동 테스트로 검증한다.

Python 3.12.14 / jsonschema 4.26.0 / MCP 2.3.0 환경에서 전체 테스트 **111개**가 통과했다. 기존 주문·배송/MCP와 GET·전체 메서드의 GitHub 명세 검증을 포함한다. wheel을 별도로 빌드하고 Python 3.14.4에서 소스 폴더 밖의 패키지를 로드해 기본 의존성만으로 POST import·계약 검증과 로컬 HTTP 5개 메서드도 확인했다. 의존성 검사와 `git diff --check`가 통과했다.
