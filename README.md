# a2api

기존 API·함수를 에이전트가 **찾고 호출할 수 있는 공통 인터페이스로 전환하는 프로토콜과 라이브러리**.

## 현재 개발 기준

목표 사용 흐름은 **OpenAPI/등록한 코드 → 변환 → 바로 호출**이다. 전체 실행 계약과 LLM용 호출 설명을 구분하고, 검토·빌드·변경·재승인을 첫 호출의 필수 절차로 만들지 않는다.

- [설계 방향·코드/OpenAPI 전환 예제·LLM 호출 전체 흐름](docs/00-product-direction.ko.md)
- [이 문서에 따른 개발 계획과 범위](docs/03-roadmap-and-evaluation.ko.md)

**P0-1/2/3을 구현했다.** 선택한 OpenAPI GET/HEAD와 등록한 Python 조회 함수를 review/build 파일 없이 직접 호출하고, 같은 객체를 경량 MCP discover/describe/invoke에 연결한다. 도구 목록에는 개별 API schema를 나열하지 않는다. 기존 전체 Capability IR·검증기·MCP bridge와 선택적인 검토/변경 관리 기능도 보존한다. 문서의 기능 목록은 모두 따라야 할 사용 순서가 아니다.

## OpenAPI를 바로 호출하기

```python
from a2api import HTTPDeployment, convert
from a2api.importers import OpenAPIImporter

source = OpenAPIImporter.from_file("orders.openapi.json", namespace="legacy")
app = convert(source, operations={
    "getOrder": {"effect": "read", "select": ["orderId", "orderState", "shipmentIds"]},
}, deployment=HTTPDeployment("https://orders.example.internal", credential_provider=credentials_for_user))
result = app.invoke("legacy.getorder", {"path": {"orderId": "ORD-1001"}}, context=authenticated_caller)
```

credential과 context는 호스트가 제공한다. 전체 실행 예제: `python examples/direct-orders/convert_and_invoke.py`. [사용법·반환 형식·지원 범위](docs/11-in-memory-conversion.ko.md)를 참고한다. 파일 생성·review/build 명령은 필요 없다.

## Python 함수와 신규 API 등록

`@capability(id="orders.lookup", effect="read")`로 함수를 선언하고 `Application([lookup_order])`에 명시적으로 등록한다. 타입 힌트·TypedDict에서 입출력 schema를 생성하며, OpenAPI 경로와 같은 `describe`/`invoke` 형식을 사용한다. host 전용 context는 업무 입력에서 제외한다.

```bash
python examples/native-orders/register_and_invoke.py
```

[함수 등록·기본값·명시적 schema 사용법](docs/12-python-functions.ko.md)에 예제와 지원 범위를 정리했다.

HTTP 어댑터는 **GET/HEAD/POST/PUT/PATCH/DELETE, JSON 본문, 명시적인 2xx·빈 응답, 호스트 인증 주입**을 지원한다. 활성 MVP runtime은 GET/HEAD 조회 정책을 적용하며, 다른 메서드의 import와 transport 검증은 비활성 계약으로 진행한다. [HTTP 어댑터 안내](docs/07-http-adapter.ko.md)를 참고한다.

## 빠른 실행

Python 3.11 이상에서 저장소 루트를 기준으로 실행한다.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m a2api demo
python -m unittest discover -s tests -v
```

`demo`는 임시 loopback 포트에 주문·배송 API와 a2api gateway를 띄우고, 실제 HTTP로 검색 → 계약 설명 → 조립 실행을 검증한 뒤 종료한다. 기본 주문 `ORD-1001`은 배송 두 건을 반환하며 backend 호출은 총 3회다. 외부 서비스나 LLM 키는 필요 없다.

```bash
python -m a2api validate src/a2api/sample/order-shipping.json
python -m a2api demo --order-id ORD-1002
python -m a2api serve --port 8000 --backend-port 8001
```

`ORD-1002`는 배송이 없는 정상 결과다. `serve`의 gateway는 `http://127.0.0.1:8000`, 샘플 backend는 `http://127.0.0.1:8001`이다. 로컬 데모 토큰 `demo-alice`, `demo-bob`, `demo-limited`를 제공한다. HTTP 서버와 샘플 인증은 개발·테스트용이다.

```bash
curl -s http://127.0.0.1:8000/discover \
  -H 'Authorization: Bearer demo-alice' \
  -H 'Content-Type: application/json' \
  -d '{"query":"배송 조회"}'
```

전체 HTTP·라이브러리 사용법과 지원 범위는 [MVP 실행 안내](docs/04-mvp.ko.md)를 참고한다. `jsonschema`가 이미 설치된 환경에서는 설치 없이 `PYTHONPATH=src python3 -m a2api demo`도 가능하다.

## MCP 에이전트 연결

변환한 OpenAPI와 등록한 Python 함수를 함께 호출하려면 다음 예제를 실행한다.

```bash
python -m pip install -e ".[mcp]"
python examples/native-orders/mcp_client.py
```

호스트의 Python 파일에서는 `anyio.run(serve_stdio, app, caller)`로 연결한다. 두 객체는 `[http_api, functions]`로 묶을 수 있다. [호스트 설정·요청 형식·경량화와 비용 측정](docs/13-lightweight-mcp.ko.md)을 참고한다.

공개 GitHub 저장소 조회와 이슈/PR 목록을 실제 API로 호출하는 예제도 제공한다. 기존 고정 OpenAPI의 두 operation을 `convert`하고 Python wrapper로 필요한 필드만 반환한다. 토큰 없이 직접 호출과 MCP stdio를 함께 검증한다.

```bash
python examples/github-openapi/verify_agent.py --owner octocat --repo Hello-World --per-page 2
```

[GitHub 예제 사용법·입출력·페이지 범위](docs/14-github-readonly-example.ko.md)를 참고한다.

선택 의존성을 설치하고 공식 MCP 클라이언트로 전체 흐름을 확인한다.

```bash
python -m pip install -e ".[mcp]"
python -m a2api mcp-demo
python -m unittest discover -s tests -v
```

MCP 호스트가 실행할 명령은 `python -m a2api mcp`다. `a2api.discover`, `a2api.describe`, `a2api.invoke` 세 도구를 제공하고, 샘플 주문·배송 API도 자동으로 시작한다. stdout은 MCP 프로토콜 전용이며 별도 HTTP MCP 포트는 열지 않는다.

`mcp-demo`는 공식 SDK 클라이언트가 실제 stdio 서버를 별도 프로세스로 실행해 세 도구를 호출한다. 기본 주문의 조회 결과는 배송 두 건, backend HTTP 호출은 3회다. 에이전트 연결 설정과 라이브러리 사용은 [MCP 브리지 안내](docs/05-mcp-bridge.ko.md)를 참고한다.

## 현재 importer: 대규모 OpenAPI 가져오기

OpenAPI 3.0/3.1 JSON·YAML에서 Capability IR과 HTTP 바인딩 초안을 생성한다. 공식 GitHub REST 전체 명세 **827 paths / 1,254 operations**를 고정 샘플로 포함했다. 기본 GET 선택은 633개를 변환하고, `--methods GET HEAD POST PUT PATCH DELETE`를 지정하면 1,228개를 변환한다. 미선택·미지원 operation은 사유를 보고한다. 생성물은 비활성 초안이며 담당자의 업무·권한·출력 검토 후 실행 계약을 작성한다.

```bash
python -m pip install -e ".[openapi]"
python -m a2api import-openapi examples/github-openapi/api.github.com.json.gz \
  --namespace github --output artifacts/github-ir
```

출력 폴더의 `report.json`과 `contracts/`에서 결과를 확인한다. 기존 출력 폴더는 덮어쓰지 않는다. 지원 기능, 검증 결과와 실제 공개 API 검증 스크립트는 [OpenAPI importer 안내](docs/06-openapi-importer.ko.md)에 정리했다.

## 선택 관리 기능: 검토 설정으로 계약 빌드

주문·배송 OpenAPI → import → 검토 설정 → 실행 계약 → MCP 전체 경로를 검증한다.

```bash
python -m pip install -e ".[mcp]"
python -m a2api review-demo
```

일반 명령은 `python -m a2api build --imports <import-directory> --review <review.json> --output <new-directory>`다. 원본·바인딩 해시, 미검토 설정, 미지원 projection과 권한 검사 누락을 검사한다. import 산출물과 검토 파일은 보존하며, 생성 묶음은 로드 시 다시 빌드해 검증한다. [검토 빌더 안내](docs/08-review-builder.ko.md)에 샘플 설정과 단계별 실행을 정리했다.

## 선택 관리 기능: 변경 영향·증분·재승인

operation과 전이적 참조 schema의 변경을 추적해 영향받는 capability만 재검토 대상으로 표시한다. 기존 검토 설정을 보존하고 무관한 계약은 바이트 그대로 재사용한다.

```bash
python -m a2api incremental-demo
python -m a2api diff-openapi --before old.openapi.json --after new.openapi.json --review review.json
python -m a2api regenerate --previous approved-build --source new.openapi.json --output updated-build
```

재검토 capability는 MCP에서 숨기며, 한 번 무효화된 검토를 자동으로 되살리지 않는다. [증분 재생성 안내](docs/09-source-diff-and-regeneration.ko.md)에 지원 범위와 기존 빌드 이행을 정리했다.

선택 재승인은 `prepare-review --build ... --capability ID@version --output review.json`으로 현재 빌드에 고정된 검토안을 만든 뒤, 설정을 검토하고 `approve-review --build ... --review review.json --reviewed-by NAME --output ...`으로 수행한다. 영향 없는 계약과 최초 검토 설정은 보존한다. 전체 주문·배송 흐름은 `python -m a2api reapproval-demo`로 검증할 수 있다. [선택 검토·재승인 안내](docs/10-selective-reapproval.ko.md)에 편집 범위와 승인 이력을 설명했다.

## 설계 방향

레거시 API와 신규 API를 같은 중간 표현인 **Capability IR**로 정규화한다. 여기서 capability는 사용자가 달성하려는 업무를 수행하는 기능 단위다. 타입과 호출 주소뿐 아니라 업무 의미, 입력의 출처, 실행 조건, 부작용, 결과의 근거와 표시 방법을 함께 정의한다.

```text
레거시: 기존 계약·소스·테스트 → 추출 → 검토한 의미·정책 추가 ─┐
                                                           ├→ Capability IR → 검색·그래프·실행 → 에이전트·사용자
신규:   capability 계약 작성 → 구현·계약 검증 ────────────────┘
```

OpenAPI·JSON Schema·MCP를 재사용한다. 여러 API의 업무 조립은 선택이며, 단순 API도 1:1 전환해 호출할 수 있게 한다. 최초의 넓은 아키텍처와 전체 프로토콜 초안보다 위의 현재 개발 기준을 우선한다.

## 문서

현재 기준은 [제품 방향과 전환·호출 설계](docs/00-product-direction.ko.md), [개발 계획](docs/03-roadmap-and-evaluation.ko.md)이다. 아래는 설계 배경과 기존 구현의 참고 문서이며 순서대로 실행할 작업 목록이 아니다.

현재 실행 가능한 간편 전환 경로는 [P0-1 메모리 convert/invoke 안내](docs/11-in-memory-conversion.ko.md)에 있다.

Python 함수와 신규 API는 [P0-2 함수 등록 안내](docs/12-python-functions.ko.md)에 있다.

두 경로의 MCP 연결은 [P0-3 경량 MCP 안내](docs/13-lightweight-mcp.ko.md)에 있다.

1. [API 분석과 아키텍처](docs/01-architecture.ko.md): 전통적 개발 방식, 대규모 도구 호출의 문제, 그래프와 native 개발 비교, 레거시 전환 방법.
2. [프로토콜 초안](docs/02-protocol-draft.ko.md): 계약 필드, 검색·설명·실행 인터페이스, 오류·상태·권한·결과 표시 규칙.
3. [MVP와 평가 계획](docs/03-roadmap-and-evaluation.ko.md): 구현 순서, 비교 실험, 출시 조건과 미결정 사항.
4. [MVP 실행 안내](docs/04-mvp.ko.md): 실제 구현 범위, HTTP 요청, 라이브러리 사용과 검증 결과.
5. [초기 계약 초안](examples/order-tracking.capability.json): 비활성 상태로 보존한 최초 설계 예시.
6. [실행 가능한 샘플 계약](src/a2api/sample/order-shipping.json): 로컬 fixture API용 검사·projection을 포함한 계약.
7. [MCP 브리지 안내](docs/05-mcp-bridge.ko.md): 설치, stdio 연결, 도구 계약과 오류 처리, 검증 범위.
8. [OpenAPI importer 안내](docs/06-openapi-importer.ko.md): 대규모 GitHub 명세, 변환 규칙, 비활성 IR과 진단, HTTP 검증.
9. [HTTP 어댑터 확장](docs/07-http-adapter.ko.md): HTTP 메서드·JSON 본문·2xx 응답·호스트 인증·결과 미확정 처리와 로컬 검증.
10. [검토 설정과 계약 빌더](docs/08-review-builder.ko.md): source pin·필드 projection·업무 계약 생성·빌드 재검증과 OpenAPI부터 MCP까지의 주문·배송 예제.
11. [변경 영향 diff와 증분 재생성](docs/09-source-diff-and-regeneration.ko.md): operation·공유 참조 의존성, 선택적 재변환, 검토 보존과 부분 카탈로그 유지.
12. [Capability 선택 검토·재승인](docs/10-selective-reapproval.ko.md): 현재 빌드에 고정된 검토안, 부분 승인과 설정 보존, 후속 변경부터 MCP 호출까지의 검증.

## 작업 폴더와 원격 저장소

- 의도한 원격: <https://github.com/metahackAI/a2api.git>
- 작업 경로: `~/workspace/a2api`

설계의 예상 효과는 아직 평가 가설이다. MVP의 자동 검증은 샘플 API와 계약 적합성에 대한 것이며, 실제 레거시 시스템이나 LLM의 업무 성공률을 측정한 결과는 아니다.
