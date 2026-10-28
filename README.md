# a2api

다양한 언어와 환경에서 구현한 API를 에이전트가 **찾고, 조합하고, 실행하고, 결과를 사용자에게 설명할 수 있도록** 만드는 계약 및 런타임 라이브러리.

현재는 **Python 조회 전용 MVP**다. Capability IR, 계약 검증기, HTTP adapter, `discover / describe / invoke`, 주문·배송 샘플 API, HTTP gateway, **stdio MCP 브리지**, **OpenAPI importer**를 제공한다. 명세에서 IR 초안을 자동 생성하며 업무 의미·권한 검토와 변경 작업은 후속 범위다.

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

선택 의존성을 설치하고 공식 MCP 클라이언트로 전체 흐름을 확인한다.

```bash
python -m pip install -e ".[mcp]"
python -m a2api mcp-demo
python -m unittest discover -s tests -v
```

MCP 호스트가 실행할 명령은 `python -m a2api mcp`다. `a2api.discover`, `a2api.describe`, `a2api.invoke` 세 도구를 제공하고, 샘플 주문·배송 API도 자동으로 시작한다. stdout은 MCP 프로토콜 전용이며 별도 HTTP MCP 포트는 열지 않는다.

`mcp-demo`는 공식 SDK 클라이언트가 실제 stdio 서버를 별도 프로세스로 실행해 세 도구를 호출한다. 기본 주문의 조회 결과는 배송 두 건, backend HTTP 호출은 3회다. 에이전트 연결 설정과 라이브러리 사용은 [MCP 브리지 안내](docs/05-mcp-bridge.ko.md)를 참고한다.

## 대규모 OpenAPI 가져오기

OpenAPI 3.0/3.1 JSON·YAML에서 Capability IR과 HTTP 바인딩 초안을 생성한다. 공식 GitHub REST 전체 명세 **827 paths / 1,254 operations**를 고정 샘플로 포함했다. 기본 GET 선택은 633개를 변환하고, `--methods GET HEAD POST PUT PATCH DELETE`를 지정하면 1,228개를 변환한다. 미선택·미지원 operation은 사유를 보고한다. 생성물은 비활성 초안이며 담당자의 업무·권한·출력 검토 후 실행 계약을 작성한다.

```bash
python -m pip install -e ".[openapi]"
python -m a2api import-openapi examples/github-openapi/api.github.com.json.gz \
  --namespace github --output artifacts/github-ir
```

출력 폴더의 `report.json`과 `contracts/`에서 결과를 확인한다. 기존 출력 폴더는 덮어쓰지 않는다. 지원 기능, 검증 결과와 실제 공개 API 검증 스크립트는 [OpenAPI importer 안내](docs/06-openapi-importer.ko.md)에 정리했다.

## 설계 방향

레거시 API와 신규 API를 같은 중간 표현인 **Capability IR**로 정규화한다. 여기서 capability는 사용자가 달성하려는 업무를 수행하는 기능 단위다. 타입과 호출 주소뿐 아니라 업무 의미, 입력의 출처, 실행 조건, 부작용, 결과의 근거와 표시 방법을 함께 정의한다.

```text
레거시: 기존 계약·소스·테스트 → 추출 → 검토한 의미·정책 추가 ─┐
                                                           ├→ Capability IR → 검색·그래프·실행 → 에이전트·사용자
신규:   capability 계약 작성 → 구현·계약 검증 ────────────────┘
```

OpenAPI, Arazzo, MCP 등 기존 표준을 활용한다. a2api의 차별점은 업무 계약을 실행 규칙과 검증까지 연결하는 데 둔다.

## 문서

1. [API 분석과 아키텍처](docs/01-architecture.ko.md): 전통적 개발 방식, 대규모 도구 호출의 문제, 그래프와 native 개발 비교, 레거시 전환 방법.
2. [프로토콜 초안](docs/02-protocol-draft.ko.md): 계약 필드, 검색·설명·실행 인터페이스, 오류·상태·권한·결과 표시 규칙.
3. [MVP와 평가 계획](docs/03-roadmap-and-evaluation.ko.md): 구현 순서, 비교 실험, 출시 조건과 미결정 사항.
4. [MVP 실행 안내](docs/04-mvp.ko.md): 실제 구현 범위, HTTP 요청, 라이브러리 사용과 검증 결과.
5. [초기 계약 초안](examples/order-tracking.capability.json): 비활성 상태로 보존한 최초 설계 예시.
6. [실행 가능한 샘플 계약](src/a2api/sample/order-shipping.json): 로컬 fixture API용 검사·projection을 포함한 계약.
7. [MCP 브리지 안내](docs/05-mcp-bridge.ko.md): 설치, stdio 연결, 도구 계약과 오류 처리, 검증 범위.
8. [OpenAPI importer 안내](docs/06-openapi-importer.ko.md): 대규모 GitHub 명세, 변환 규칙, 비활성 IR과 진단, HTTP 검증.
9. [HTTP 어댑터 확장](docs/07-http-adapter.ko.md): HTTP 메서드·JSON 본문·2xx 응답·호스트 인증·결과 미확정 처리와 로컬 검증.

## 작업 폴더와 원격 저장소

- 의도한 원격: <https://github.com/metahackAI/a2api.git>
- 작업 경로: `~/workspace/a2api`

설계의 예상 효과는 아직 평가 가설이다. MVP의 자동 검증은 샘플 API와 계약 적합성에 대한 것이며, 실제 레거시 시스템이나 LLM의 업무 성공률을 측정한 결과는 아니다.
