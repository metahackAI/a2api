# GitHub MCP를 실제 LLM으로 사용하기

이번 예제는 기존 GitHub MCP 서버에 Codex CLI를 연결해 한국어 질문을 실행한다. 모델이 실제로 선택한 도구·인자·결과·최종 답변을 기록한다. 원래의 OpenAPI 전환과 Python capability, MCP 세 도구는 그대로 사용한다. 개발 범위와 순서는 [확정 계획](15-agent-usage-plan.ko.md)에 있다.

## 실행 환경

- Python 3.11 이상, `a2api[mcp]`가 설치된 환경.
- `codex` CLI와 완료된 로그인. 예제는 로그인 정보를 읽거나 복사하지 않는다.
- 모델 서비스와 공개 GitHub API에 접속할 수 있는 환경. 기존 Codex 계정의 사용량을 사용하며 모델 API 키를 새로 요구하지 않는다.
- 이번 실행기는 POSIX 프로세스 그룹으로 host와 자식 MCP 서버를 정리한다. 확인한 환경은 Linux와 Codex CLI `0.164.0-alpha.11.1`이다. 모든 CLI 버전/운영체제의 호환성을 검증한 것은 아니다.

```bash
python -m pip install -e ".[mcp]"
codex login status
python examples/github-openapi/agent_demo.py
```

현재 서버에서는 다음 명령을 사용할 수 있다.

```bash
cd /home/khs/workspace/a2api
.venv-mcp/bin/python examples/github-openapi/agent_demo.py \
  --output artifacts/agent-usage/report.json
```

기존 CLI에 로그인되지 않았으면 먼저 사용하는 Codex 환경의 로그인을 완료한다. 잘못된 CLI 경로·로그인·통신 문제를 정상 모델 답변으로 대체하지 않는다. `--codex /absolute/path/codex`로 실행 파일을 지정할 수 있다.

이 예제는 서버도 자동 실행하고 종료한다. 미리 `mcp_server.py`를 수동 실행할 필요가 없다. Codex 비대화형 실행·JSONL 이벤트·MCP 설정은 [공식 비대화형 안내](https://learn.chatgpt.com/docs/non-interactive-mode), [MCP 안내](https://learn.chatgpt.com/docs/extend/mcp?surface=cli), [설정 참조](https://learn.chatgpt.com/docs/config-file/config-reference)를 따른다.

## 고정된 다섯 질문

[agent-scenarios.json](../examples/github-openapi/agent-scenarios.json)의 질문만 모델에게 전달한다. 같은 파일의 `expected`는 실행 후 검사 코드가 사용하며 모델 prompt에 넣지 않는다.

| ID | 질문의 목적 | 자동 확인 |
|---|---|---|
| `repository` | metahackAI/a2api 소개와 열린 이슈·PR 한 페이지 | 두 capability의 입력·응답 schema, 실제 조회 성공 |
| `issues` | octocat/Hello-World 최근 열린 이슈·PR 3개 | 해당 저장소·state=open·page=1·perPage=3 |
| `next_page` | 직전 목록의 다음 페이지 | 같은 저장소·조건·개수에서 page=2 |
| `missing_repository` | 고정된 존재하지 않는 이름 조회 | 구조화된 `RESOURCE_NOT_FOUND` 실패 |
| `missing_input` | 저장소 없이 이슈 요청 | 실제 invoke 없음. 되묻는 답변은 별도 확인 |

한 시나리오만 실행할 수도 있다.

```bash
.venv-mcp/bin/python examples/github-openapi/agent_demo.py --scenario issues
.venv-mcp/bin/python examples/github-openapi/agent_demo.py --scenario next_page
```

`next_page`만 지정해도 먼저 `issues`를 실제 실행한다. 이번 호스트 연결은 실행마다 `--ephemeral`로 전역 세션 저장을 피하므로, 후속 요청에는 직전 실행의 **실제 사용자 질문·실제 MCP 호출/결과·실제 답변**을 JSON으로 재생한다. 예상 page·capability·검사 결과를 추가하지 않는다. 지속 중인 단일 대화를 그대로 resume하는 것과 다르며 보고서의 `continuation`에 이 방식을 표시한다. 직전 자동 검사가 실패하면 다음 페이지를 만들어내지 않고 실행을 건너뛰어 실패로 기록한다.

## 결과 읽기

JSON 상세 기록의 기본 위치는 `artifacts/agent-usage/report.json`이다. 이 폴더는 Git에서 제외돼 있다. 공개 이슈 제목·URL과 답변은 포함할 수 있지만 원본 GitHub 전체 응답·credential·모델 reasoning 이벤트·CLI stderr는 결과 파일에 저장하지 않는다.

- `runs[].calls`: 모델이 실제 호출한 MCP 도구의 이름·입력·구조화 결과. 검색/설명과 실제 API 조회를 구별할 수 있다.
- `runs[].answer`: 모델의 최종 답변.
- `runs[].checks`: 입력/출력 schema, 발견한 ID/버전·설명 사용, 예상 입력·조회 횟수·오류, 다른 도구 우회 여부에 대한 자동 검사.
- `runs[].usage`: CLI가 반환한 사용량 원본. 여러 모델 단계가 포함된 호스트 측 사용량이며 a2api payload만의 토큰 수가 아니다. 없으면 `null`이다.
- `model`: 현재 CLI JSONL 이벤트가 실제 모델 ID를 반환하지 않아 `null`이다. CLI 기본 선택을 사용하며 모델을 추정해 채우지 않는다.
- `passed`: **자동 검사만** 모두 통과했는지다. 답변의 자연어 사실성이나 일반적인 LLM 성공률을 뜻하지 않는다.

자동 검사가 통과해도 `answerReview: required`가 남는다. 다음을 도구 결과와 직접 대조한다.

1. 답변의 저장소 언어·별 수·제목·URL·종류가 실제 결과와 일치하는가?
2. GitHub 설명이 `null`인데 소스나 README를 읽었다고 하거나 프로젝트 목적을 추측하지 않았는가?
3. 한 페이지와 전체 건수를 구별하고, PR을 이슈라고 잘못 표시하지 않았는가?
4. 빈 목록은 정상 조회로, 404는 조회 실패로 설명했는가?
5. 입력 부족 시 저장소를 지정해 달라고 묻고 임의 저장소를 고르지 않았는가?

자동 검사 실패는 종료 코드 1, 모두 통과하면 0이다. 이는 자연어 답변의 수동 확인을 대체하지 않는다. 기본 timeout은 시나리오당 180초이며 `--timeout`으로 최대 600초까지 지정한다. stdout/stderr 합산 상한은 실행당 2 MiB다. 시간/출력 상한·비정상 종료·읽을 수 없는 이벤트는 실패로 남기고 자식 프로세스를 정리한다. 재시도·인자 자동 보정은 하지 않는다.

## 이번에 관찰해 수정한 부분

첫 실행에서 모델이 `a2api.describe`에 `capabilityId`를 보내 오류를 받은 뒤 `id`, `version`으로 수정했다. 필드 이름만 설명한 재실행에서도 같은 추측이 반복돼, 기존 MCP 도구 설명과 서버 지침에 두 필수 필드의 일반 JSON 요청 형태를 명시했다. 최종 다섯 질문 실행은 자동 검사를 통과했고 답변도 실제 결과와 대조했다. 잘못된 이름을 허용하는 alias나 wire 변경은 추가하지 않았다. 이 관찰로 모든 모델의 호출 오류가 없어졌다고 주장하지 않는다.

실행기에서도 MCP의 정상적인 구조화 오류(예: backend 404)를 호스트 통신 장애와 혼동한 분류를 수정했다. API 실패 응답은 오류 그대로 기록하며, 기대한 404를 정확히 관찰했는지를 별도로 판정한다.

실제 실행 요약과 답변 대조 결과는 [검증 기록](evidence/agent-usage.json)에 있다. 최초 실패도 해당 요약에 남긴다. 특정 질문·시점·호스트 기본 모델에서의 관찰이며 API 전체나 다른 모델의 성공률·토큰 절감에 대한 실험은 아니다.

## 오프라인 재현 검사

```bash
.venv-mcp/bin/python -m unittest discover -s tests -p test_agent_demo.py -v
.venv-mcp/bin/python -m unittest discover -s tests -v
```

기본 테스트는 외부 LLM/GitHub를 호출하지 않는다. 고정 HTTP fixture와 실제 MCP stdio로 정상·빈 페이지·다음 페이지·404·무호출 조건의 근거를 확인하고, 관찰한 Codex 이벤트 형태의 합성 fixture로 파싱/판정을 검사한다. 이 합성 이벤트를 실제 모델 실행 증거로 취급하지 않는다. 실제 LLM 실행은 위 `agent_demo.py` 명령을 명시적으로 실행할 때만 발생한다.
