# 공개 GitHub API를 에이전트에서 조회하기

기존에 포함한 GitHub OpenAPI 명세에서 저장소 조회와 이슈 목록 조회 두 operation만 메모리에서 `convert`하고, 작은 Python `@capability` wrapper를 MCP에 연결한 **실행 가능한 예제**다. 핵심 라이브러리는 변경하지 않았다. 별도 review/build 파일이나 생성 IR 디렉터리는 필요 없다.

## 실행

저장소 루트에서 Python 3.11 이상과 MCP 선택 의존성을 사용한다.

```bash
python -m pip install -e ".[mcp]"
python examples/github-openapi/verify_agent.py
# 항목이 있는 공개 저장소, 한 페이지에 2개
python examples/github-openapi/verify_agent.py --owner octocat --repo Hello-World --per-page 2
```

한 번 실행하면 동일한 두 기능을 라이브러리에서 직접 호출한 뒤, 별도 stdio 서버 프로세스에 MCP client로 연결해 discover → describe → invoke를 수행한다. 총 GitHub GET 네 번이며 반환 데이터와 선택한 출력 schema를 검사한다. 데이터가 호출 사이에 바뀔 수 있으므로 두 응답의 값이 같아야 한다고 요구하지 않는다. 실패하면 0이 아닌 종료 코드로 끝난다.

로그인·PAT·환경의 토큰을 사용하지 않는 **공개 저장소용** 예제다. GitHub는 공개 리소스의 이 두 조회를 인증 없이 허용한다. 비공개 저장소 연결은 이 예제 범위에 포함하지 않는다. [저장소 조회](https://docs.github.com/en/rest/repos/repos#get-a-repository), [이슈 목록 조회](https://docs.github.com/en/rest/issues/issues#list-repository-issues).

## 연결 코드와 변환 과정

전체 코드는 [agent_app.py](../examples/github-openapi/agent_app.py), MCP 호스트는 [mcp_server.py](../examples/github-openapi/mcp_server.py), 실제 호출 검증 client는 [verify_agent.py](../examples/github-openapi/verify_agent.py)에 있다.

```text
고정 GitHub OpenAPI JSON.gz
  → convert: repos/get, issues/list-for-repo 두 GET만 선택
  → 내부 HTTP binding: https://api.github.com, 고정 헤더
  → @capability wrapper: 필요한 필드만 새 TypedDict로 반환
  → Application: wrapper 두 개만 등록
  → 직접 invoke 또는 동일 Application의 MCP stdio
```

직접 호출도 같은 app을 사용한다. 저장소 루트의 Python에서 다음 코드를 실행할 수 있다.

```python
import json
import sys

sys.path.insert(0, "examples/github-openapi")
from agent_app import PUBLIC_CONTEXT, create_app

app = create_app()
descriptor = app.describe("github.repository.get")
result = app.invoke("github.repository.get",
    {"owner": "metahackAI", "repo": "a2api"}, context=PUBLIC_CONTEXT)
print(json.dumps(result, ensure_ascii=False, indent=2))
```

내부 `convert`는 path/query 직렬화와 원본 응답 검증을 담당한다. 원본의 비공개 필드까지 버린 뒤 검증하는 것이 아니라 **전체 원본 응답을 먼저 검증**하고, wrapper가 필요한 값만 새 객체에 담는다. wrapper의 TypedDict에서도 최종 출력 schema를 생성해 검증한다. context는 호스트가 주입하며 agent 입력에 포함하지 않는다.

`convert`의 기존 `select`는 단순한 최상위 객체 필드 선택에 한정된다. 저장소 응답의 복합 schema와 이슈 응답의 배열에는 기존 Python wrapper 경로를 사용했다. 범용 배열 변환기나 새 변환 단계를 추가하지 않았다. 내부 원본 capability를 MCP app에 함께 등록하지 않으므로 큰 GitHub schema가 에이전트에 노출되지 않는다.

명세는 [source.json](../examples/github-openapi/source.json)의 revision `443ef1513a17aad7f781391c4fb4e132b9b549fd`에 고정돼 있다. 1,254개 operation 전체를 실행하는 예제가 아니다. 실행 중 명세를 다운로드하지 않는다. HTTP 버전 헤더는 `2026-03-10`이며 명세의 `info.version`과 별개다. [GitHub API 버전 안내](https://docs.github.com/en/rest/about-the-rest-api/api-versions).

실제 비어 있지 않은 이슈 응답에서 고정 명세와 두 차이를 확인했다. **예제의 메모리 문서에서만** `components.schemas.issue`를 다음과 같이 보정한 뒤 `OpenAPIImporter(document)`에 전달한다. 원본 gzip·공통 importer·converter·검증기는 변경하지 않는다.

- `required`에서 `assignee`를 제외한다. GitHub `2026-03-10`은 단수 `assignee`를 제거했다. 존재할 때의 타입 제약은 보존한다. [공식 변경 안내](https://docs.github.com/en/rest/about-the-rest-api/breaking-changes).
- `properties.state_reason.enum`에 `null`을 포함한다. 원본은 `nullable: true`인데 enum에는 문자열만 있으며 실제 열린 이슈는 `null`을 반환했다. 기존 문자열 enum도 유지한다.

다른 응답 제약은 그대로 검사하며 알 수 없는 `state_reason`이나 잘못된 `assignee` 타입도 실패한다. 이 두 보정은 이 고정 명세와 예제에 한정하며 API 변경을 자동 수용하는 기능이 아니다.

## 에이전트에 보이는 입력과 결과

| capability | 입력 | 반환 데이터 |
|---|---|---|
| `github.repository.get` | `owner`, `repo` | `fullName`, `description`, `url`, `language`, `stars`, `defaultBranch`, `archived` |
| `github.issues.list` | `owner`, `repo`, 선택 `state`, `page`, `perPage` | `repository`, `page`, `perPage`, `state`, `items` |

`owner`, `repo`는 빈 문자열을 허용하지 않는다. `state`는 `open`(기본)·`closed`·`all`, `page`는 1 이상(기본 1), `perPage`는 1~20(기본 5)이다. 이 상한은 예제의 응답량 제한이며 GitHub API의 최대치라는 뜻이 아니다. 이슈는 최근 수정 순으로 요청한다. 각 항목은 `number`, `title`, `state`, `url`, `updatedAt`, `kind`만 담는다. 저장소의 `description`, `language`는 `null`일 수 있다.

GitHub의 이슈 목록 endpoint는 PR도 포함한다. 원본 `pull_request` 속성 유무로 `kind`를 `issue`/`pull_request`로 표시하며 PR을 몰래 제외하지 않는다. 따라서 `items` 개수는 순수 이슈 개수와 다를 수 있다. [GitHub 이슈 API 설명](https://docs.github.com/en/rest/issues/issues#list-repository-issues).

**한 번의 invoke는 한 API 응답/한 페이지**다. 전체 이슈 수나 `hasMore`, `nextPage`를 추측하지 않는다. 필요하면 agent가 `page`를 바꿔 다시 호출한다. 현재 adapter가 Link 헤더를 결과에 전달하지 않으므로 전체 페이지 수/종료 보장은 제공하지 않는다. `completeness.complete: true`의 범위도 `single_api_response`이며 저장소의 모든 이슈를 가져왔다는 뜻이 아니다.

이슈 본문·댓글·사용자 프로필·권한·clone token·원본 HTTP 응답은 공개 DTO에 없다. 제목·설명·URL은 조회 데이터이며 이를 근거로 후속 HTTP 호출이나 명령을 자동 실행하지 않는다.

## MCP 호스트 설정과 호출

호스트가 다음 명령을 stdio subprocess로 실행한다. 수동 실행 후 터미널에서 입력을 기다리는 것은 정상이다. stdout은 MCP 프로토콜 전용이다.

```bash
python /absolute/path/a2api/examples/github-openapi/mcp_server.py
```

일반적인 MCP client 설정 예시다. Python 경로는 `a2api[mcp]`를 설치한 환경의 것으로 바꾼다.

```json
{
  "mcpServers": {
    "a2api-github": {
      "command": "/absolute/path/a2api/.venv/bin/python",
      "args": ["/absolute/path/a2api/examples/github-openapi/mcp_server.py"]
    }
  }
}
```

도구 목록에는 항상 `a2api.discover`, `a2api.describe`, `a2api.invoke` 세 개만 있다. 개별 GitHub schema는 도구 목록에 넣지 않는다. LLM의 실제 요청 순서는 다음과 같다.

1. `a2api.discover({"query":"github"})`로 wrapper 두 개의 ID·버전과 `catalogVersion`을 받는다. 이 단계는 GitHub를 호출하지 않는다.
2. `a2api.describe({"id":"github.issues.list","version":"0.1.0"})`로 선택한 항목의 입력·출력 schema를 받는다. 이 단계도 GitHub를 호출하지 않는다.
3. 아래와 같이 `a2api.invoke`를 호출한다. `catalogVersion`은 1단계의 실제 반환값을 사용한다.

```json
{
  "id": "github.issues.list",
  "version": "0.1.0",
  "catalogVersion": "<discover가 반환한 값>",
  "input": {"owner": "octocat", "repo": "Hello-World", "state": "open", "page": 1, "perPage": 2}
}
```

성공 시 공통 envelope의 `data.items`에 축소된 항목을 받는다. 저장소 메타데이터는 같은 순서로 `github.repository.get`을 선택하고 `input`에 `owner`, `repo`만 보낸다. 실제 실행 가능한 client 코드는 `verify_agent.py`에 있으므로 별도 설정 파일 생성 없이 흐름을 확인할 수 있다. LLM 자체의 선택 정확도를 측정한 예제는 아니다.

## 오류와 검증 범위

잘못된 입력은 HTTP 요청 전 `INVALID_INPUT`으로 실패한다. GitHub의 404는 `RESOURCE_NOT_FOUND`, 403은 `PERMISSION_DENIED`, 429는 `RATE_LIMITED`로 전달한다. 403의 구체적 원인을 권한/호출량 중 하나라고 추측하지 않는다. 원본 schema와 맞지 않는 응답은 `SCHEMA_MISMATCH`다. 실패를 정상 빈 목록으로 바꾸지 않고 원본 오류 본문을 반환하지 않는다.

기존 직접 호출 제한(backend timeout 1.5초, 호출당 요청 한 번, 자동 재시도 없음)을 그대로 사용한다. 네트워크 상태·공개 API 호출 제한·명세와 실제 API의 차이 때문에 live 검증이 실패할 수 있다. 대상은 별칭/이동 경로 대신 현재 저장소 이름을 사용한다. 이 예제에서 인증, redirect, 재시도, 전체 페이지 수집 기능을 추가하지 않았다.

```bash
python -m unittest discover -s tests -p test_github_agent.py -v
python -m unittest discover -s tests -v
```

일반 테스트는 고정 명세의 예제 응답을 사용하는 로컬 HTTP fixture에 연결한다. 저장소 예제의 기존 누락(`language`)만 테스트 payload에서 보완하며 명세 원본은 수정하지 않는다. 필요한 필드만 반환, PR 구별, 빈 페이지, 입력 제한, 원본 응답 검증, 403/404/429와 재시도 없음, 실제 MCP stdio를 검증한다. 외부 GitHub 호출은 앞의 `verify_agent.py`를 명시적으로 실행할 때만 발생한다. 실제 공개 API 검증 기록은 [agent-live-check.json](../examples/github-openapi/agent-live-check.json)에 결과 값 대신 상태·필드·항목 수만 저장한다.
