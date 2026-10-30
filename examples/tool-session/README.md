# 선택한 function tools로 호출하기

`ToolSession`의 사용 명령은 [도구 바인딩 안내](../../docs/24-selected-tools.ko.md)에 있다. 기존 model-client에 `--binding selected`를 추가하며 서버는 계속 discover/describe/invoke 세 도구를 제공한다.

이 디렉터리는 규모와 요청 유형별 비교를 위한 작은 예제다. 새로운 관리 서버나 importer 단계가 아니다.

```bash
python -m pip install -e '.[mcp]'
export A2API_MODEL_BASE_URL='사용할 Chat Completions base URL'
export A2API_MODEL='모델 ID'

# 실제 모델 + 로컬 주문·배송 HTTP, 2개/1000개 카탈로그
python examples/tool-session/evaluate.py \
  --output artifacts/tool-session-evaluation/my-run.json

# 같은 평가에 실제 공개 GitHub 조회도 포함
python examples/tool-session/evaluate.py --github \
  --output artifacts/tool-session-evaluation/my-github-run.json
```

출력 파일은 기존 파일을 덮어쓰지 않는다. `--repetitions 1|2`이며 기본은 탐색적 1회다. 실제 LLM과 공개 GitHub 사용량을 소비한다. `--github`는 quota를 먼저 확인하고 요청 수를 제한한다. 새 대화에서 누락된 owner/repo를 질문하는지도 검사한다. 실패는 JSON에 남기고 명령이 1로 종료되며 임의 재실행으로 바꾸지 않는다.

`python examples/tool-session/summarize.py artifacts/tool-session-evaluation/my-run.json`으로 실패를 포함한 전체 집계를 출력한다. 최종 답변의 사실 대조는 별도로 수행한다. [실제 pilot 결과와 한계](../../docs/25-total-call-cost-results.ko.md)를 참고한다.

세 모드는 같은 공개 입출력·반환 필드·입력/결과 검증·lexical 검색을 사용한다.

- ordinary: 일반 host 검색 + function tool. 같은 앱을 직접 호출하는 비교군으로, 독립적인 GitHub SDK 또는 개발 비용 비교가 아니다.
- generic: 기존 a2api 세 도구를 실제 MCP stdio로 호출한다.
- selected: ToolSession이 필요한 입력 schema만 제공하고 실제 MCP stdio의 기존 invoke로 호출한다.

2개 카탈로그는 두 기능을 호스트가 미리 아는 구성이고, 1000개는 기능을 모르는 구성이다. 따라서 이 실측만으로 API 수 자체의 인과 효과를 비교할 수 없다. 작은 미지/큰 기지 기능도 같은 라이브러리 경로로 처리하며 결정적 테스트에서 확인한다. 1000개는 실제 업무 기능 2개와 합성 방해 함수 998개이며 1000개 실제 GitHub API 검증이 아니다. ordinary는 in-process, 나머지는 stdio이므로 네트워크/직렬화까지 통제한 순수 runtime 비교도 아니다.

대화는 simple → chain → followup(주문), repository_issues → next_page(GitHub) 순서다. 각 모드는 별도 새 세션에서 같은 질문을 사용한다. 모드 실행 순서를 교대하며 temperature=0, 같은 모델 설정을 유지한다. 모델 usage와 시간·호출·실제 인자를 함께 기록한다. token usage가 누락되면 `usageAvailable=false`다. 사실 답변 검토는 별도이며 자동 인자 검사 통과를 답변 품질 전체로 바꾸지 않는다.
