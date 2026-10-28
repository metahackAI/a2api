# OpenAPI → Capability IR importer

구현일: 2026-10-28. OpenAPI 3.0.x/3.1.x 명세에서 **검토 가능한 Capability IR 초안과 HTTP 바인딩**을 생성한다. JSON은 기본 설치로 읽고, YAML은 `a2api[openapi]` 선택 의존성을 설치하면 읽는다. 두 형식 모두 gzip 입력을 지원한다.

## 대규모 검증 대상

작은 Petstore 대신 GitHub의 [공식 REST OpenAPI 명세](https://github.com/github/rest-api-description)를 사용했다. GitHub가 배포하는 bundled 명세의 revision `443ef1513a17aad7f781391c4fb4e132b9b549fd`를 고정했다. 원본 내용을 수정하지 않고 gzip으로 보관하며, 라이선스·다운로드 주소·SHA-256도 함께 저장했다.

| 항목 | 값 |
|---|---:|
| 압축 전 명세 | 13,897,231 bytes |
| path | 827 |
| 전체 operation | 1,254 |
| GET | 655 |
| 기본 GET 선택으로 생성된 IR | 633 |
| GET 중 미지원 | 22 |
| 기본 선택에서 GET 외 메서드: 목록만 보존 | 599 |
| 전체 지원 메서드 선택으로 생성된 IR | 1,228 |

기본 GET의 미지원 22개는 명시적 2xx 없음 15개, 응답 codec 2개, 지원하지 않는 parameter schema 4개, GET request body 1개다. 기본 선택에서 POST·PUT·PATCH·DELETE는 `skipped`로 남는다. `--methods GET HEAD POST PUT PATCH DELETE`를 지정하면 전체 1,254개 중 1,228개를 생성하고 26개는 미지원으로 보고한다. [전체 메서드 보고서](../examples/github-openapi/import-report-all-methods.json)와 [HTTP 어댑터 확장](07-http-adapter.ko.md)을 참고한다.

전체 입력의 operation마다 결과 한 건을 남기는 [처리 보고서](../examples/github-openapi/import-report.json)에 method, path, operationId, capabilityId, 진단 코드·원본 위치를 기록한다. 측정값은 [GET 기록](../examples/github-openapi/benchmark.json)과 [전체 메서드 기록](../examples/github-openapi/benchmark-all-methods.json)에 보관한다. 단일 Linux/Python 3.12 실행 결과이며 성능 보장은 아니다.

## CLI

저장소 루트에서 실행한다. 출력 폴더는 새 경로를 지정한다. 기존 폴더는 덮어쓰지 않는다.

```bash
python -m pip install -e ".[openapi]"
python -m a2api import-openapi \
  examples/github-openapi/api.github.com.json.gz \
  --namespace github --output artifacts/github-ir
```

출력 구조:

```text
artifacts/github-ir/
  report.json
  contracts/
    github.repos.get.json
    github.repos.get.http.json
    ...
```

`*.json`은 기존 `load_contract`와 `validate`가 읽는 실제 Capability IR이다. `*.http.json`은 배포 전 바인딩 초안이다. 기본 GET의 manifest는 약 22 MB, 전체 메서드는 약 37 MB다. 저장소에는 압축 원본·보고서·작은 생성 예시만 포함하고, 전체 생성물은 `artifacts/`에 둔다.

선택 operation만 변환하거나 CI에서 미지원 항목을 실패로 처리할 수 있다.

```bash
python -m a2api import-openapi \
  examples/github-openapi/api.github.com.json.gz \
  --namespace github --output artifacts/github-selected \
  --operation repos/get --operation issues/list-for-repo --strict
python -m a2api validate artifacts/github-selected/contracts/github.repos.get.json
```

`--strict`는 선택한 항목 중 `unsupported`가 있으면 보고서를 쓴 뒤 exit 1을 반환한다. 메서드 미선택으로 인한 `skipped`는 실패로 처리하지 않는다. 잘못된 버전·입력·선택 ID도 오류를 반환한다. 보고서의 `sourceOperations`는 원본 전체 수, `operations`는 선택해서 처리한 수, `requestedMethods`는 가져올 메서드다.

## 변환 규칙

| 원본 | 생성 IR |
|---|---|
| `operationId` | operation ID 보존, capability ID는 namespace와 정규화한 ID 결합 |
| operationId 없음 | method/path에서 결정적으로 생성한 ID |
| path/query/header parameter | `inputSchema.path`, `inputSchema.query`, `inputSchema.headers`로 분리 |
| JSON request body | `inputSchema.body`, 필수 여부와 JSON media type 보존 |
| parameter required/default/enum/범위 | required와 제약 보존; default는 주석이며 값 자동 주입 없음 |
| 명시적 2xx 응답 | `outputSchema.result` 아래 원본 타입 유지, JSON/empty codec과 필요한 HTTP status 보존 |
| 내부 `$ref` | 도달 가능한 스키마만 `$defs`에 묶고 참조 유지 |
| summary/description/tags | 의도 설명과 provenance로 보존 |
| security/servers/response links | 출처 정보로 보존; 인증·배포 주소·실행 관계로 자동 채택하지 않음 |

path는 simple scalar, query는 form scalar 및 scalar 배열, 일반 header는 simple scalar를 지원한다. query의 `explode=true`는 같은 이름을 반복하고, `false`는 쉼표로 연결한다. 구분자 쉼표와 항목 내부의 URL 인코딩을 구분한다. 빈 배열은 이 profile에서 전송 의미가 정의되지 않아 호출 전 `INVALID_INPUT`으로 거부한다. bool은 `true`/`false`로 직렬화한다. 생략한 선택 parameter는 전송하지 않는다. path 값은 URL 인코딩한다. 인증·관리용 header, 쿠키·content parameter, deepObject 등 미지원 직렬화는 해당 operation의 진단으로 남긴다.

객체 응답의 추가 필드를 임의로 금지하거나, union을 문자열로 축소하거나, 배열을 단일 객체로 바꾸지 않는다. root 배열·scalar도 `result` envelope로 보존한다. `oneOf`/`anyOf`/`allOf`와 재귀적인 내부 스키마 참조를 유지한다.

OpenAPI 3.0의 `nullable`과 exclusive bound는 2020-12 표현으로 변환한다. 명시적 type 없는 `nullable`은 원래 의미대로 null을 새로 허용하지 않고 경고한다. 3.0 Reference Object의 sibling은 적용하지 않고 경고하며, 3.1 schema `$ref` sibling은 유지한다. discriminator는 메타데이터로 남기고 JSON Schema 대안으로 검증한다. custom discriminator dispatch는 구현하지 않았다. format은 보존하지만 이번 importer가 모든 OpenAPI format을 검증하는 것은 아니다. 라이브러리 응답 검증의 기존 date-time 검사 외 format은 annotation이다. readOnly/writeOnly를 이용한 일반적인 방향별 projection은 후속 범위이며, 직접 선언된 필수 writeOnly 응답 필드와 필수 readOnly 요청 필드는 미지원으로 진단한다. 필수 writeOnly 요청 필드는 허용한다.

외부 URL·파일 `$ref`, custom scope/dialect/dynamic reference, 지원하지 않는 validation keyword는 미지원이다. importer는 명세의 URL을 요청하지 않으며 내부 참조만 해석한다. 입력은 압축 해제 후 64 MiB로 제한하고, YAML alias·중복 키·임의 객체 태그와 JSON 중복 키·비유한 수를 거부한다. 전체 OpenAPI 표준 적합성 검사기를 대신하는 기능은 아니다.

## 생성과 활성화의 경계

자동 추출만으로 owner, 업무 식별자 동등성, 객체 권한, 민감 필드, 부작용, 업무 workflow를 확정할 수 없다. 따라서 생성물은 다음 상태다.

```json
{
  "schemaProfile": "openapi-draft",
  "lifecycle": "draft",
  "enabled": false,
  "effects": {"kind": "unknown", "externalWrites": true},
  "provenance": {"kind": "source", "reviewState": "unreviewed"}
}
```

`externalWrites: true`는 실제 쓰기 발생의 관측값이 아니라, 효과 미검토를 나타내는 보수적 선언이다. 생성물은 카탈로그 discover/describe/invoke와 MCP에 공개되지 않는다. `openapi-draft` profile은 검토 플래그만 바꿔 활성화할 수 없다. 실행하려면 담당자가 업무 입력·출력을 정하고, 기존 실행 가능한 `mvp` profile로 닫힌 projection과 권한·관계 검사·효과·deployment binding을 작성해 검증해야 한다. 일반 OpenAPI 스키마를 그대로 실행하는 새 profile이나 검토 overlay 병합 기능은 이번 범위에 포함하지 않았다.

원본 응답에 owner·token 같은 필드가 존재하면 추출 단계에서 원본 스키마를 보존한다. 사용자에게 내보낼 필드 선택은 이후 검토한 projection의 역할이다. importer의 성공은 에이전트 도구 배포나 업무 성공률 검증을 의미하지 않는다.

## 라이브러리와 HTTP 검증

```python
from a2api.importers import OpenAPIImporter, write_import

importer = OpenAPIImporter.from_file("openapi.yaml", namespace="legacy")
for record in importer.iter_operations():
    print(record.operation_id, record.status, record.summary()["diagnostics"])
    if record.capability:
        manifest = record.capability.describe()
        # JSON 객체를 편집해도 컴파일된 IR은 바뀌지 않는다.
report = write_import(importer, "artifacts/legacy-ir")
```

`record.http_route("https://explicit-origin.example", path_prefix="/v1", headers={...})`는 호스트가 지정한 origin에 해당 메서드의 바인딩을 만든다. 명세의 servers나 호출 입력으로 origin을 선택하지 않는다. 인증 헤더도 호스트가 주입하며 `credential_provider`를 전달할 수 있다. 이 메서드는 capability를 활성화하지 않으며, 초안의 transport/schema 적합성 검증에 사용할 수 있다.

검증은 세 층으로 나뉜다.

1. 전체 고정 명세를 오프라인 변환해 모든 operation의 누락 여부, ID 중복, 비활성 상태와 진단을 확인한다.
2. 실제 loopback HTTP에서 path/query 직렬화, 선택 인자 생략, 배열 응답, schema drift와 GitHub 이슈 예제를 검증한다. 기존 주문·배송 HTTP/MCP 테스트도 함께 실행한다.
3. 별도 opt-in 스크립트가 토큰 없이 실제 공개 GitHub API의 `/meta`, 저장소 조회, 이슈 목록 조회를 각각 한 번 호출한다. 세 응답 모두 생성된 스키마로 검증했다. 인증된 API나 생성 IR 전체를 실행했다는 뜻은 아니다. 추가 메서드는 [로컬 HTTP 검증](../examples/http-adapter/README.md)으로 확인한다.

```bash
python -m pip install -e ".[mcp,openapi]"
python -W error::ResourceWarning -m unittest discover -s tests -v
python examples/github-openapi/verify_import.py --output artifacts/github-benchmark
python examples/github-openapi/verify_live.py
```

최초 importer 구현에서는 Python 3.12.14에서 MCP·YAML 선택 의존성을 포함한 테스트 93개가 통과했다. 이후 추가한 HTTP 확장의 검증은 [별도 안내](07-http-adapter.ko.md)에 정리한다. wheel을 만들고 소스 폴더 밖 환경에서 기본 의존성만으로 JSON 명세 import와 생성 계약 검증도 확인한다. 일반 테스트에는 외부 네트워크·토큰이 필요 없다. loopback 소켓과 MCP subprocess를 사용할 수 있어야 한다. `verify_import.py --record-results`는 GET 보고서와 benchmark, 예제 적합성 기록을 재생성한다. `--all-methods`를 더하면 전체 메서드 보고서와 benchmark를 별도 파일로 갱신한다.

실제 명세를 사용한 덕분에 upstream 예제 자체의 오류도 확인했다. `/meta` 예제의 fingerprint 네 필드가 string 스키마에 대해 number이고, 저장소 예제는 두 위치에서 required 필드가 빠져 있다. [예제 불일치 기록](../examples/github-openapi/example-drift.json)에 rule과 경로를 남겼고, 이슈 목록 예제는 적합하다. 이 차이를 숨기기 위해 원본이나 스키마를 고치지 않았다. 실제 공개 GET 응답 세 건은 모두 적합했다.

다음 확장 대상은 검토 overlay의 별도 저장·병합, 원본 변경에 따른 영향 diff, 명시적 업무 capability projection, pagination 결과의 완전성 표시와 변경 업무 실행 정책이다.
