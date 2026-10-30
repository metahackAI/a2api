# 검색 1번 구현과 실제 GitHub 재검증

2026-10-30 · [28 문서](28-cost-improvement-plan.ko.md)의 **1번만 구현했다.** [범위 기록](29-search-improvement.ko.md) 후 검색을 바꾸고 기존 실제 GitHub 24질문을 다시 실행했다. 결과 선택/반환 설명 개선인 2번과 별도 LLM holdout 확장인 3번은 진행하지 않았다.

## 구현한 규칙

- 정확한 capability ID는 prefix 이웃을 제외한 해당 ID/버전만 반환한다. 실제 복수 버전은 유지하며 prime에서 임의로 고르지 않는다. 이전에 paging으로 마지막 버전을 본 상태여도 prime은 첫 페이지에서 모호성을 다시 확인한다.
- source operationId/등록 함수 이름·ID·summary·명시적 keywords·공개 입출력 field를 구분하는 서버 index를 만들었다. 이름 경계를 정규화하고 주요 질의 개념의 포함 정도, 필드별 점수·corpus 단어 빈도, 동작/리소스 일치를 사용한다. 긴 본문의 단어 반복으로 점수를 올리지 않는다. 배열 항목/가까운 자식은 root field보다 낮은 근거다. 순환·복합 schema는 보수적으로 건너뛴다.
- `a2api_search`에 선택적 `more`를 추가했다. 기존 query-only 요청을 유지한다. cursor는 호스트가 보관하고 질의당 최대 3페이지로 제한한다. 같은 query를 more 없이 반복하면 현재 페이지를 다시 제공하고 progress=false로 새 후보가 없음을 알린다. query/caller/limit/catalog/검색 revision의 불일치를 허용하지 않는다.
- `a2api-call/0.1` wire·descriptor 6필드·MCP 도구 세 개는 유지했다. 확장한 호스트 표현은 `a2api-tools/0.2`다. 기존 전체 manifest Runtime의 검색/정책 엔진은 교체하지 않았다.

검색 설정·페이지/오류의 실제 사용법은 [21 문서](21-discovery-metadata.ko.md), [24 문서](24-selected-tools.ko.md)에 있다. 사용자가 새 index 파일·DB·승인 단계·변환 명령을 운영할 필요는 없다. index는 선택한 앱에서 메모리로 생성한다.

## 회귀와 오프라인 확인

전체 회귀 **290개 통과**. 새 테스트는 정확 ID/prefix 이웃, 실제 복수 버전, 입력/출력 field와 우연한 중첩 field 구별, 원본 alias 표기, 한글/keywords 유지, 조건부 페이지·끝·한도, 잘못된 인자, caller/limit/catalog/revision 변경, MCP tools/list 고정을 확인했다. 업무 API 호출 없이 검색할 수 있고 stale cursor를 재시도하지 않는다.

이전 실제 질의 61개를 재현하고, 별도 고정한 오프라인 10질의에서는 모두 정답을 상위 3개에서 찾았다. 9개는 1위, release-by-tag는 2위였다. [오프라인 기록](evidence/search-improvement-offline.json)은 실제 모델 성공률이나 모든 미사용 질의의 검색 성능을 뜻하지 않는다. 개발 중 사용한 이전 질의 재현과 새 10질의를 구분했다. 이번 범위에서 새 LLM holdout 질문을 추가하지 않았다.

예를 들어 이전 저장소 질의 `github repository default branch stars archived`는 repos/get을 241위에 두었으나 새 index는 1위로 반환했다. `GitHub repository branches list`도 list-branches를 이전 115위에서 1위로 반환했다. 이런 근거는 서버에만 있으며 function 설명에 반환 field를 추가하지 않았다.

## 실제 Muse 비교 조건

[이전 실행](27-real-github-evaluation-results.ko.md)과 같은 공식 GitHub 고정 source/revision/SHA256, 실제 GET 8개/633개, 단순 저장소·브랜치 1페이지 최대 2개·기본 브랜치→head commit 통계의 3요청, 2반복이다. 각 질문은 새 대화이며 모드 순서를 교대했다.

`muse-glimmer-30b`, temperature=0, max_tokens=2048, stream=false, tool_choice=auto, 질문 12단계/120초, 후보 3개, 16,000바이트 도구 예산을 유지했다. 두 모드 모두 새 검색/페이지/예산을 사용하고 in-process HTTP로 실행했다. 원본 전체 응답과 business function 설명·입출력·채점기는 그대로다. 검색 도구 schema/설명만 more에 맞게 확장했다. 두 카탈로그의 descriptor 크기도 이전과 같은 189,292/5,266,304바이트였다. select는 여전히 적용하지 않았다.

ordinary는 같은 전환 앱과 검색을 사용하는 일반 검색+function 통제군이다. 독립 GitHub SDK나 최선의 모든 일반 검색을 대표하지 않는다. 원본 HTTP/공개 결과/입력 검증과 trusted context를 유지했다. auth는 CLI credential을 호스트 메모리에서만 재사용하며 모델/로그에 보내지 않았다. local cache/replay를 사용하지 않았다. GitHub/모델 제공자의 부하·cache와 데이터 변화는 통제하지 못했다.

## 결과

각 행은 같은 6질문 합계다. 토큰은 provider usage이며 24질문 모두 제공됐다. 시간은 질문 처리 시간이고 준비 비용은 뒤에서 더한다.

| 카탈로그 | 방식 | 정확한 완료 | prompt+completion 토큰 | 처리 시간 | 모델 요청 | 검색 | 실제 HTTP |
|---|---|---:|---:|---:|---:|---:|---:|
| 실제 8개 | ordinary | 6/6 | 85,818 | 110.405초 | 23 | 11 | 10 |
| 실제 8개 | a2api | 6/6 | 79,251 | 107.280초 | 22 | 10 | 10 |
| 실제 633개 | ordinary | 6/6 | 90,456 | 117.614초 | 25 | 13 | 9 |
| 실제 633개 | a2api | 6/6 | 90,456 | 117.759초 | 25 | 13 | 9 |

양쪽 모두 단순은 크기별 4/4, 연쇄는 2/2다. 같은 원본을 재채점해도 최초 판정과 달라진 것은 없었다. branch와 반환된 SHA를 이용한 데이터 흐름, 요청 개수/page/per_page, 최종 JSON 값을 확인했다. 인자나 결과를 보정하지 않았다. invalid input/실패한 business 시도는 없었다.

| 전체 12질문/모드 | ordinary | a2api |
|---|---:|---:|
| 정확한 완료 | 12/12 | 12/12 |
| prompt 토큰 | 164,581 | 158,216 |
| completion 토큰 | 11,693 | 11,491 |
| 전체 토큰 | 176,274 | 169,707 |
| 모델 요청 | 48 | 47 |
| 검색 호출 | 24 | 23 |
| business/실제 HTTP | 19/19 | 19/19 |
| 질문 처리 시간 | 228.019초 | 225.039초 |
| 세션 준비 포함 | 229.820초 | 226.862초 |
| 공통 카탈로그 준비 1회 포함 | 251.065초 | 248.107초 |
| 실패 비용도 포함한 성공 1건당 토큰 | 14,689.5 | 14,142.2 |

공통 준비 21.245초는 source 로드/전체 import 7.305초, 작은 앱 convert 0.584초, 큰 앱 convert 13.356초다. 독립 호스트 각각이 두 카탈로그를 1회 준비한다고 가정해 같은 비용을 더했다. 소규모 앱 하나만 연결하는 일반 시작 비용이나 평가 스크립트 전체 wall time이라고 부르지 않는다. 새로운 index 때문에 세션 준비 시간은 이전보다 늘었으며 위 합계에 포함했다.

## 이전과 비교한 의미

- a2api의 작은 구성은 6/6을 유지하고 큰 구성은 0/6에서 6/6으로 회복했다. 전체 토큰은 583,647→169,707로 **70.9% 감소**, 공통 준비까지 더한 시간은 605.728→248.107초로 **59.0% 감소**했다.
- ordinary도 같은 index 개선으로 큰 구성 0/6→6/6, 전체 토큰 573,055→176,274로 69.2% 감소했다. a2api만의 고유한 비용 우위로 해석하지 않는다. 큰 구성에서는 두 모드의 토큰이 같았다. 작은 차이에는 모델이 선택한 조회/검색 경로와 제공자 변동이 포함되므로 일반적 우위를 주장하지 않는다.
- 이전 실패 비용이 포함된 합계와 비교한 것이다. 같은 성공률에서 순수한 프로토콜 overhead만 70.9% 줄였다는 뜻이 아니다. 소규모 정확성 유지와 대규모 성공 회복을 함께 확인한 이번 workload의 결과다.
- 실제 HTTP는 a2api 11→19회, ordinary 10→19회로 늘었다. 이전에는 큰 요청 대부분이 실제 조회에 도달하지 못했다. 이제 목표를 완료했고 각 모드에서 합계 3회의 적법한 중간 branch 조회를 더 사용했다. 모든 비용 차원이 감소했다고 보고하지 않는다.

이번 모델 실행의 more 요청은 **0회**다. 상위 후보 개선으로 필요한 계약을 찾았으며, 모델 성공 회복을 pagination의 단독 효과라고 주장하지 않는다. 조건부 페이지는 실제 633개 MCP 서버에서 1→2페이지와 새 후보를 확인했고 unit test에서 3페이지 한도·끝·변경/오류를 검사했다.

실제 MCP stdio smoke는 tools/list가 전후 같은 3개이고 조회 2회가 성공했다. 메타데이터 2페이지 확인을 추가해 discover 4회/describe 8회/invoke 2회, 준비·실행 22.540초였다. 이는 주 비교 시간에 합치지 않는다. 주 비교 38회+사전 2회+stdio 2회, 총 **42회 실제 GitHub HTTP가 모두 200**이었다.

## 재현과 남은 범위

```bash
python -m pip install -e '.[mcp]'
python -m unittest discover -s tests -v

# 기존 22 문서처럼 자신의 model endpoint/model 환경 변수를 설정
python examples/real-github-evaluation/search_check.py \
  --output artifacts/search-improvement/my-offline.json
python examples/real-github-evaluation/evaluate.py --github-auth gh \
  --repetitions 2 --stdio --output artifacts/search-improvement/my-run.json
python examples/real-github-evaluation/review.py artifacts/search-improvement/my-run.json \
  --output artifacts/search-improvement/my-review.json
python examples/real-github-evaluation/summarize.py artifacts/search-improvement/my-run.json \
  --review artifacts/search-improvement/my-review.json \
  --output artifacts/search-improvement/my-summary.json
```

[실측 evidence](evidence/search-improvement-live.json)에 원문 hash·모든 집계·실패 목록·source 범위·준비/페이지/stdio 정보를 기록했다. [호출 trace 발췌](evidence/search-improvement-traces.json)에는 실제 검색 후보·업무 인자·결과 일부·최종 답을 남겼다. 발췌는 기록을 읽기 위한 것이며 모델에 보낸 응답의 projection이 아니다. 원문은 ignored `artifacts/search-improvement/pilot-1.json`, 별도 오프라인 검사와 동일 원문 채점은 각각 `offline-final.json`, `review-1.json`이다. 파일을 덮어쓰거나 모델을 임의 재실행해 성공으로 바꾸지 않았다. 새 review는 기록한 검색 revision을 요구하며 예전 report는 원래 substring 순위로 확인할 수 있다.

모든 질의가 한 번에 수렴한 것은 아니다. 예를 들어 `github branch head commit SHA additions deletions`에서 get-commit은 7위였고, 해당 연쇄 실행은 질의를 다듬으며 검색 5회를 사용했다. 성공 회복을 확인했지만 탐색의 불필요한 왕복이 모두 제거된 상태는 아니다.

이 결과는 2개 공개 저장소의 3종 요청, 고정 source, 2반복 범위다. 633개 전체 API를 실제 호출하거나 임의의 큰 API/복잡한 업무에서 성공한다고 증명하지 않는다. 결과 선택·반환 설명·별도 실제 LLM holdout 확장은 다음 지시 전까지 미착수다.
