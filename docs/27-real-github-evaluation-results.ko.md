# 실제 GitHub 조회 카탈로그 검증 결과

2026-10-30 · [평가 계획](26-real-github-evaluation-plan.ko.md)에 따라 실제 Muse Glimmer와 GitHub HTTP를 실행했다. **현재 경량 바인딩만으로 대규모 API 탐색 문제를 해결했다고 볼 수 없다.** 두 방식 모두 소규모에서는 정확히 호출했지만 대규모에서는 필요한 기능을 찾지 못했다. 이번에는 평가와 개선 계획만 추가했으며 제품 코드는 변경하지 않았다.

## 소스와 실제 검증 범위

공식 [GitHub OpenAPI 고정 revision](https://github.com/github/rest-api-description/tree/443ef1513a17aad7f781391c4fb4e132b9b549fd/descriptions/api.github.com)을 사용했다. 원문 SHA256은 `b81f098026e98084a83f0a33db43502213919f68449b028543c373757766a758`다. 최신 전체 명세라고 표현하지 않는다.

| 단계 | 확인한 수 |
|---|---:|
| 원본 operation | 1,254 |
| GET | 655 |
| 현재 importer 및 메모리 converter 지원 GET | 633 |
| 미지원 GET | 22 |
| 비선택 메서드 | 599 |

소규모는 관련 GET 8개, 대규모는 변환한 GET 633개다. 합성 함수·가짜 route·가짜 schema는 없다. 작은 카탈로그는 repos/get, get-commit, list-commits, get-branch, list-branches, get-latest-release, issues/list-for-repo, pulls/list로 구성했다. 두 크기 모두 원본 summary·설명·태그·제약을 사용했다. 정답에 맞춘 keywords를 추가하지 않았다.

미지원 operation별 진단은 같은 고정 소스의 [상세 import 보고서](../examples/github-openapi/import-report.json)와 원 실행 report의 inventory에 있다.

**633개 전체가 실제 HTTP 호출·권한 검증을 통과했다는 뜻은 아니다.** 실제 모델 호출에서 사용한 operation 종류는 repos/get, repos/list-branches, repos/get-commit, repos/get-branch, git/list-matching-refs의 5개다. 일부는 잘못 고른 후보다. 호스트 중계는 psf/requests와 octocat/Hello-World 하위 GET만 허용했다. 다른 리소스·관리 권한을 요구하는 API까지 이 인증에서 사용할 수 있다고 보장하지 않는다.

원본을 수정하거나 검증을 완화하지 않았다. `repos/get` 응답의 `x-github-breaking-changes` 때문에 기존 top-level select가 `UNSUPPORTED_SELECTION`을 반환해 이번 비교는 양쪽 모두 전체 원본 응답을 사용했다. 이 제한은 후속 계획에 남겼다.

## 비교 조건

실제 `muse-glimmer-30b`, temperature=0, max_tokens=2048, stream=false, tool_choice=auto를 사용했다. 질문당 모델 단계 12회, 120초, 도구 정의 예산 16,000 UTF-8 JSON 바이트와 검색 후보 3개를 적용했다. 토큰은 provider usage를 사용했고 24질문 모두 누락이 없었다.

- ordinary: 일반 검색+function 호스트. 같은 전환 앱·JSON Schema 검증·lexical 검색·도구 예산/교체 정책을 사용한다.
- a2api: 기존 ToolSession이 검색·describe·계약 ID/version/catalogVersion과 검증을 처리한다.

주 비교는 **양쪽 모두 in-process HTTP 실행**이다. 이전의 ordinary in-process 대 selected stdio 차이를 제거했다. 독립 GitHub SDK·수작업 공수 비교는 아니다. 양쪽 모두 필요한 기능을 모르는 상태에서 검색 도구 하나로 시작했다. 따라서 API 수와 사전 지식을 섞지 않았다. API 크기별 첫 도구 정의는 같은 검색 schema이며 전체 업무 schema를 덤프하지 않는다.

ordinary는 현재의 lexical 후보기를 재사용한 통제 비교군이다. BM25/embedding 등 잘 조정한 일반 검색 전체를 대표하지 않는다. 두 모드의 실패로 모든 일반 검색 방식도 실패한다고 결론 내릴 수 없다.

크기 2 × 모드 2 × 요청 3 × 반복 2 = **24질문**이다. 질문마다 새 대화/세션을 만들고 모드 순서를 교대했다. 일반 API 대조군에도 같은 입력·설명·반환 데이터·검색/예산 정책을 적용했다. source 변환은 공유해 모드별 준비 비용을 같게 두었다.

1. psf/requests의 기본 브랜치·별 개수·보관 여부.
2. octocat/Hello-World의 브랜치 1페이지, 최대 2개. 실제 page/per_page도 검사했다.
3. octocat/Hello-World의 저장소에서 실제 default_branch를 확인한 후 head commit SHA와 additions/deletions 조회. 반환 branch나 SHA를 경유하는 적법한 방법을 허용했다.

최종 답변은 요청한 키의 JSON으로 받아 실제 API 결과와 값/타입을 비교했다. 필수/추가 인자·owner/repo·페이지·개수·선행 값 사용도 별도로 검사했다. 답변에 두 개만 적었다는 이유로 per_page=30 요청을 성공 처리하지 않는다. 인자 보정·자동 재시도·실패한 모델 실행의 재측정은 하지 않았다.

인증은 기존 GitHub CLI의 호스트 인증을 메모리에서만 재사용했다. 모델/로그/저장 파일에는 토큰을 전달하지 않았다. 응답을 local cache/replay로 대체하지 않았다. GitHub 자체 cache/데이터 변화, 모델 제공자의 prefix cache/부하와 출력 경로는 통제하지 못했다. 두 번의 반복은 통계적 일반화에 부족하다.

## 정확도와 비용

각 칸은 동일한 6질문의 합계다. 아래 시간은 질문 처리 시간이고 준비는 뒤에서 별도로 더한다. 실패한 실행도 토큰·시간 합계에 모두 포함했다.

| 카탈로그 | 방식 | 사용자 조건·최종 값 통과 | 토큰 합계 | 시간 합계 |
|---|---|---:|---:|---:|
| 실제 GET 8개 | 일반 검색+function | 6/6 | 113,101 | 137.027초 |
| 실제 GET 8개 | a2api | 6/6 | 126,216 | 150.227초 |
| 실제 GET 633개 | 일반 검색+function | 0/6 | 459,954 | 427.170초 |
| 실제 GET 633개 | a2api | 0/6 | 457,431 | 433.462초 |

8개에서 각 모드 단순 요청은 4/4, 연쇄 요청은 2/2였다. 633개에서 단순은 0/4, 연쇄는 0/2였다. 이번 결과에서 a2api의 일반 방식 대비 비용 우위를 확인하지 못했다. 633개의 약간 적은 토큰을 개선이라고 해석하지 않는다. 목표를 완료한 사례가 없기 때문이다.

| 전체 12질문/모드 | ordinary | a2api |
|---|---:|---:|
| 정확한 완료 | 6 | 6 |
| prompt 토큰 | 544,814 | 554,596 |
| completion 토큰 | 28,241 | 29,051 |
| 전체 토큰 | 573,055 | 583,647 |
| 모델 요청 | 101 | 103 |
| 모델 검색 도구 호출 | 167 | 169 |
| 업무 invoke / 실제 GitHub 조회 | 10 / 10 | 11 / 11 |
| 질문 처리 시간 | 564.197초 | 583.689초 |
| 세션 준비 포함 | 564.855초 | 584.561초 |
| 공통 카탈로그 준비 1회까지 포함 | 586.022초 | 605.728초 |
| 실패 비용도 포함한 성공 1건당 토큰 | 95,509.2 | 97,274.5 |

공통 준비 21.167초는 원문 로드/전체 import 7.285초, 작은 앱 convert 0.581초, 큰 앱 convert 13.301초다. 두 카탈로그를 사용하는 독립 호스트 각각에 같은 1회 준비를 더한 비교이며 평가 스크립트의 전체 wall time이나 소규모 앱만 연결하는 일반 시작 비용이라고 부르지 않는다. source 계약 검증·실행 객체 생성도 보존했다.

실제 HTTP는 주 비교 21회와 사전 확인 2회, stdio smoke 2회를 합해 **25회, 모두 200**이었다. 모델이 HTTP 실패 때문에 탐색을 반복한 결과가 아니다. 성공한 작은 연쇄 요청 중 a2api 한 건이 branch 조회를 한 번 더 거쳐 실제 반환 SHA를 사용했다. 적법한 경로로 인정하고 추가 읽기 1회는 비용에 남겼다.

## 실패 원인

### 검색 순위가 필요한 기능을 밀어냈다

현재 검색은 ID/summary/전체 설명에 대한 substring 일치 개수와 ID 사전순으로 정렬한다. 실제 질의를 원문으로 오프라인 재현했고 반환 후보와 일치함을 확인했다.

- `github repository default branch stars archived`에서 repos/get은 **241위**였고 상위는 code_scanning.get_autofix, pulls.get, repos.list_pull_requests_associated_with_commit였다.
- `get repository`에서도 repos/get은 105위였다. 저장소 정보 질문의 17개 서로 다른 실제 질의에서 해당 기능은 38~241위였다.
- 브랜치 목록 질문의 20개 실제 질의에서 list-branches는 9~259위였다.
- 연쇄 질문에서는 `repos.get` 질의로 저장소 계약을 제공하기도 했다. 하지만 get-commit은 실제 질의에서 가장 가까워도 4위였고 끝내 모델 도구로 제공되지 않았다. 모델은 먼저 가능한 저장소 조회를 실행하기보다 검색을 계속하기도 했다.

결과적으로 큰 구성의 12질문 모두 필요한 계약 조합을 갖추지 못했다. 검색 결과가 moreAvailable=true여도 현재 호스트 검색에는 다음 페이지 인자가 없다. 표현을 바꾼 검색으로 비슷한 후보를 되풀이하며 각 질문이 12회 모델 단계 제한에 도달했다. 일반 대조군도 같은 검색기를 사용해 같은 문제가 나타났다. “함수를 찾으면 schema대로 호출한다”만으로 실제 큰 카탈로그를 효율적으로 쓸 수 있는 상태는 아니다.

### 도구 정보와 실행 결과가 계속 재전송된다

전체 descriptor는 서버 기준 작은 구성 189,292바이트, 큰 구성 5,266,304바이트다. 이를 전부 모델에 보내지는 않았다. 실제 한 요청의 활성 function 정의는 최대 15,887바이트였다.

그럼에도 여러 검색과 모델 추론 때문에 누적 function 정의 전달량은 ordinary 992,250바이트, a2api 998,743바이트였다. 누적 대화 전달량은 각각 753,514바이트, 780,326바이트였다. 이는 normalized UTF-8 JSON 전송량 합계이며 유일한 문서 크기나 토큰 수가 아니다. 실제 토큰은 위 usage를 사용한다.

짧은 “Get a repository”만으로는 어떤 결과 필드가 있는지 모델이 확신하기 어렵다. source의 공개 출력 field를 검색/짧은 결과 설명에 사용하고, 실제 반환 데이터를 필요한 필드로 줄일 여지가 있다. 이를 구현했다고 주장하지 않는다.

### 알려진 기능 준비와 select 제한도 확인했다

633개에서 `prime(['github.repos.get'])`는 정확한 ID가 있어도 prefix 이웃과 nextCursor 때문에 AMBIGUOUS_SELECTION으로 실패했다. 주 모델 비교는 unknown 경로이므로 이 오류가 그 비교의 직접 원인은 아니다. 별도 probe로 기록했다.

또 원본 extension annotation 때문에 select를 쓰지 못했다. 이를 벤치마크를 위해 지우거나 validator를 끄지 않았다. 원본 검증을 보존하면서 선택한 공개 필드를 생성하는 개선 대상으로 삼는다.

## 판정 수정과 별도 transport 검증

최초 판정기는 default_branch=`master`에 대해 `ref=heads/master`를 다른 값으로 보아 작은 연쇄 3건을 잘못 실패 처리했다. 실제 응답 SHA/통계는 사전 `ref=master` 조회와 같았다. 관찰한 branch에서 만든 `heads/`·`refs/heads/` 표기를 허용하도록 판정기를 고치고 **동일한 원문 호출/결과로만 재판정**했다. 원문 report와 최초 실패 판정은 그대로 보존했다. 모델을 다시 돌리거나 인자를 고치지 않았다. 추측한 다른 branch는 여전히 거부한다.

실제 MCP stdio에서는 호스트가 아는 ID로 633개 서버의 저장소→기본 브랜치 커밋을 조회했다. discover 2회/describe 6회/invoke 2회, 준비·실행 포함 22.708초였다. tools/list는 전후 같은 3도구였다. 이것은 transport smoke이며 미지 기능을 실제 모델이 찾아낸 성공 사례로 합산하지 않는다.

전체 회귀 테스트는 **282개 통과**했다. source/route 연결, 양 모드 같은 schema·예산, 잘못된 페이지/개수, 반환 값과 불일치하는 답변, 잘못 추측한 ref, 적법한 branch/SHA 경유를 확인했다. 모델 단계 제한으로 CLI가 1로 종료된 실제 실패도 evidence에 포함했다.

## 재현과 다음 계획

[실행 명령](../examples/real-github-evaluation/README.md), [집계·실패·순위 evidence](evidence/real-github-evaluation.json), [실제 인자·반환 값·실패 trace 발췌](evidence/real-github-traces.json)를 제공한다. 원문은 `artifacts/real-github-evaluation/pilot-1.json`, 별도 재판정은 `review-1.json`이다. 원문 SHA256을 evidence에 넣었으며 서로 다른 원문에 review를 적용하면 거부한다. 원문에는 실제 공개 API 데이터와 질문/도구 호출이 있어 Git에서는 제외했다. 실행 endpoint는 22 문서처럼 사용자 환경 변수로 지정한다.

[후속 개선 계획](28-cost-improvement-plan.ko.md)은 **검색 정확도와 다음 후보 접근 → 필요한 결과 의미/데이터 전달 → 동일 조건과 holdout 재검증** 순서다. 아직 구현하지 않았다. 일반 방식보다 좋다는 결론을 먼저 정하고 수치를 맞추지 않는다.

호출 의미의 공식 참고: [Get a commit의 ref와 공개 조회 조건](https://docs.github.com/en/rest/commits/commits?apiVersion=2026-03-10), [GitHub rate limit 기준](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api). 위 수치와 성공/실패 판정은 문서의 예제값이 아닌 이번 실제 실행에서 얻었다.
