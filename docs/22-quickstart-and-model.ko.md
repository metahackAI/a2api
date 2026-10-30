# 설치부터 실제 모델 호출까지

현재 실행 가능한 기본 경로다. 코드/명세를 메모리에서 연결하고 같은 앱을 직접 호출하거나 MCP로 노출한다. [경량 wire 명세](20-call-protocol.ko.md)와 [설명·검색 설정](21-discovery-metadata.ko.md)을 사용한다. 전체 manifest 검토·빌드는 선택 기능이다.

같은 계약에서 필요한 입력 schema만 모델에 제공하려면 [선택 도구 바인딩](24-selected-tools.ko.md)을 사용한다. 아래 모델 client의 기본 3도구 모드는 유지하며 `--binding selected`로 호스트가 탐색·설명과 계약 식별자를 관리한다. `--known` 기능을 처음부터 제공하는 경로와 검색 후 도구를 제공하는 경로를 모두 지원한다.

## 처음 설치하고 API 호출하기

Python 3.11 이상에서 저장소 루트로 이동한다.

```bash
git clone https://github.com/metahackAI/a2api.git
cd a2api
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[mcp]"
python examples/direct-orders/convert_and_invoke.py
python examples/native-orders/register_and_invoke.py
python examples/native-orders/mcp_client.py
```

첫 예제는 로컬 주문·배송 HTTP 서버를 자동 실행해 OpenAPI를 convert한 뒤 직접 호출한다. 두 번째는 명시적으로 등록한 Python 조회 함수를 호출한다. 세 번째는 두 앱을 같은 MCP stdio에 붙여 discover/describe/invoke를 호출한다. 외부 API/모델 키 없이 실행하며 서버는 종료 시 정리한다.

자신의 OpenAPI는 [메모리 전환 예제](11-in-memory-conversion.ko.md)의 원본 경로, 노출할 operation/effect/select와 호스트 origin/credential을 바꾼다. 함수는 [Python 등록](12-python-functions.ko.md)을 사용한다. 호스트가 신뢰하는 context를 전달하고 원 서비스의 업무 권한을 유지한다.

소스 importer를 쓸 때만 `python -m pip install -e ".[source,mcp]"`를 설치한다. 분석은 해당 언어 소스를 실행하지 않으며 기존 서비스가 실행 중이면 분석/호출 때문에 JDK/Go/Rust를 설치할 필요는 없다. 합성 서버까지 빌드하는 [세 언어 예제](18-source-importers.ko.md)는 JDK 25/Maven, Go 1.22+, Rust/Cargo·링커가 필요하다.

## 실제 모델에 MCP 연결하기

[client.py](../examples/model-client/client.py)는 작은 Chat Completions 호환 예제 호스트다. 모델 URL/ID와 신뢰하는 MCP 실행 명령을 설정한다. 아래 URL/model은 교체할 자리 표시자다.

```bash
export A2API_MODEL_BASE_URL="https://your-model.example/v1"
export A2API_MODEL="your-model-id"
# 인증이 필요하면 호스트 환경에 A2API_MODEL_API_KEY를 설정
python examples/model-client/client.py \
  --question "ORD-1001 주문 상태와 연결된 배송 상태를 알려줘." \
  --output artifacts/model-client/orders.json \
  -- python examples/native-orders/mcp_server.py --source openapi
```

서버를 먼저 수동 실행할 필요는 없다. 이 명령은 하나의 OpenAPI 예제 데이터셋을 선택해 backend를 자동 실행한다. Python 함수 예제를 선택하려면 `--source python`을 쓴다. `--base-url`, `--model`로 환경 변수 대신 값을 전달해도 된다. 인증값은 `--api-key-env`의 환경 변수(기본 A2API_MODEL_API_KEY)에서만 읽는다. key를 URL/질문에 넣지 않는다.

호스트는 실제 tools/list의 공통 도구 세 개를 a2api_discover/describe/invoke 이름으로 모델에 전달한다. 모델이 고른 JSON 인자를 보정 없이 원 MCP 이름으로 호출하고 structuredContent를 모델에 되돌린다. 개별 API ID/schema는 초기 문맥에 넣지 않으며 선택한 업무 schema는 describe로 받는다. 원 서버의 입력·원본 응답·공개 출력 검증은 유지한다.

모델 endpoint 자체가 MCP를 실행하는 것이 아니라 이 호스트가 tool_calls를 실행한다. 사용자 질문과 실제 공개 MCP 결과가 모델에 전송된다. backend origin/credential/ExecutionContext는 별도 호스트 연결이다. 이 예제의 기본 지침은 합성 작업용이며, 자신의 서비스는 MCP host에서 노출 API와 실제 사용자 권한을 제한해야 한다. 새로운 agent SDK나 workflow 파일은 요구하지 않는다.

## 결과와 실패 읽기

stdout은 최종 답변이다. `--output`을 지정하면 질문·실제 도구 인자/결과·답변·provider 사용량을 JSON에 기록한다. 기록에는 업무 데이터가 있을 수 있다. 원시 reasoning·인증 헤더는 저장하지 않으며 알려진 모델 API key가 응답으로 되돌아와도 기록/출력에서 마스킹한다.

모델 단계 최대 28회, MCP 호출 최대 56회, 시나리오 300초, 모델 응답 2 MiB로 제한한다. 모델 요청 대기는 최대 60초, MCP는 최대 30초다. 프로세스 시작/종료에는 SDK의 별도 정리 시간이 들 수 있다. hostError가 있으면 CLI 종료 코드는 1이다. 구조화된 업무 실패는 모델에 그대로 전달하므로 CLI 종료 0만으로 업무 성공을 판단하지 말고 calls와 답변을 확인한다.

인자 자동 보정·자동 재시도·다른 모델 fallback은 없다. 모델이 오류를 보고 새 호출을 선택한 경우는 기록에 남는다. OUTCOME_UNKNOWN/응답 SCHEMA_MISMATCH는 쓰기 미실행/rollback을 뜻하지 않는다. requestId는 추적용이며 중복 제거 키가 아니다.

## 세 언어에서 고정 질문 검증

모델 설정, source/mcp 선택 의존성과 언어 툴체인이 준비된 환경에서 실행한다.

```bash
python examples/model-client/verify_sources.py
python examples/model-client/verify_sources.py --language rust
# 같은 질문을 원본 source 제목으로 비교
python examples/model-client/verify_sources.py --plain-descriptions \
  --output artifacts/model-client/plain.json
```

[고정된 7개 질문](../examples/model-client/scenarios.json)을 사용한다. 각 언어에서 I-1 조회·HEAD, 생성→반환 ID로 PUT→PATCH→검색→삭제→삭제 후 404를 실행한다. Go에서는 새 대화의 ID 없는 삭제가 invoke하지 않는지도 확인한다. 기대값은 모델 prompt에 넣지 않는다. 별도 HTTP 조회로 원본 보존과 생성 항목 삭제를 확인한다.

결과는 기본 artifacts/model-client/report.json, 빌드/서버 로그는 artifacts/source-http에 둔다. 실제 모델 검증은 이 명령을 명시적으로 실행할 때만 서비스 사용량을 사용한다. 최초 빌드는 언어 의존성 다운로드가 필요하며 일반 unit test는 외부 LLM을 호출하지 않는다.

자동 passed는 고정 입력·schema·도구 순서·업무 결과 검사의 통과다. 자연어 답변은 실제 결과와 별도로 대조한다. 빈 discover/모델 왕복/시간은 한 실행의 관찰이며 일반 성공률·토큰 절감·성능 보장이 아니다. 데이터 ID나 새 이름은 등록된 검색어가 아니면 빈 결과가 정상일 수 있다.

[확정 범위](19-protocol-completion-plan.ko.md), [검증 기록](evidence/protocol-completion.json)을 참고한다. 별도 승인/배포 단계 없이 지원 API 하나를 연결해 호출하는 것이 시작 경로의 완료 조건이다.
