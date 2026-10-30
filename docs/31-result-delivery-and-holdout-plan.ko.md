# 28번의 2·3번 구현·검증 범위

2026-10-30 · 사용자가 2·3번도 진행하도록 요청했다. 이 문서와 고정 질문을 먼저 기록하고 2 → 3 순서로 수행한다. 기준은 00/03/28 문서이며 검색 알고리즘을 다시 조정하거나 범위를 확장하지 않는다.

## 2번: 공개 결과와 짧은 반환 설명

- 기존 top-level select에서 `x-*` annotation을 JSON Schema 검증 제약과 구분한다. 원본 제약을 없애지 않으며 조합/조건/의존성이 있는 object는 계속 거부한다. `$ref`의 검증 sibling도 우회하지 않는다.
- raw HTTP 응답 전체 검증 → 명시한 필드 선택 → 공개 응답 검증 순서를 유지한다. 선택하지 않은 필드가 잘못돼도 실패해야 한다. optional/null/required/로컬 참조를 보존하며 누락값을 채우지 않는다.
- 실제 비교 앱은 repo의 full_name/default_branch/stargazers_count/archived, commit의 sha/stats/html_url만 선택한다. 브랜치 배열 등 다른 응답은 유지한다. 원본 명세는 수정하지 않는다.
- 선택된 function 설명에 공개 output schema의 이름·타입·필수 여부만 제한된 길이로 보탠다. 전체 출력 schema, 예시/실제 데이터, source 설명의 임의 지시는 붙이지 않는다. array는 item field를 설명하며 해석하지 못하는 복합 schema를 추측하지 않는다.
- ordinary와 a2api는 같은 설명·projection·검색·예산·검증을 사용한다. wire/descriptor 6필드/MCP 세 도구와 인증 context를 유지한다. 호스트 표현 변경은 a2api-tools/0.3으로 기록한다.
- 단위/통합 검사를 완료한 후 기존 실제 8개/633개·3요청·2반복·총 24질문을 같은 Muse 설정으로 실행한다. 원문을 새 경로로 보존하고 1번 완료 시점의 성공률/전체 비용과 비교한다.

## 3번: 보류한 실제 요청과 전체 비용

검색 1번의 오프라인 10질의에 이미 사용한 languages/license/tags/contributors 등의 기능을 새 holdout이라고 부르지 않는다. 그 질의에 사용하지 않은 아래 6요청을 `examples/real-github-evaluation/holdout-cases.json`에 고정한다. 기존 8개에는 모든 기능이 없으므로 633개에서 6요청 × 두 방식 × 1반복 = **12질문**이다. 검색 규칙/가중치/keywords는 고정하고 결과에 따라 질문·정답 조건을 바꾸지 않는다.

1. psf/requests 최신 release의 tag/name/html_url.
2. psf/requests release 첫 페이지 최대 2개의 tag.
3. octocat/Hello-World fork 목록을 newest 순서, 첫 페이지 최대 2개의 full_name.
4. octocat/Hello-World stargazer 첫 페이지 최대 2명의 login.
5. octocat/Hello-World 저장소를 먼저 조회한 실제 기본 브랜치의 combined commit status(state/total_count).
6. 같은 저장소를 먼저 조회한 실제 기본 브랜치의 commit statuses 첫 페이지 최대 2개(state/context).

마지막 두 요청은 선행 결과에서 branch/ref를 만들어야 한다. 추측 인자, 잘못된 repo/page/개수/filter, 불필요한 재호출, 원본·공개 schema, 최종 JSON 값/타입을 검사한다. 빈 status 배열도 실제 응답이면 정상이며 이유를 추측하지 않는다. 업무 호출 실패·source/응답 drift·모델 실패를 구분하고 실패를 포함해 보고한다. 별도 live 사전 검사 비용도 보존한다.

## 실행과 완료 조건

1. 위 범위의 converter/짧은 설명과 같은 대조군을 구현하고 실제 변환·검증·MCP·예산 회귀를 검사한다.
2. 질문/채점 조건·설정·구현을 고정한 뒤 2번의 기존 24질문, 이어서 3번의 보류한 12질문을 실행한다. 각 질문은 새 대화/세션, 순서 교대, Muse temperature=0/max_tokens=2048/12단계/120초/후보 3개/16KB를 유지한다.
3. 각 실행의 모든 실패와 provider usage, 준비/모델/도구/HTTP 시간·횟수·바이트를 보존한다. 정확성이 같은 경우에 관찰된 비용 감소만 보고하고, 토큰/바이트/원 API 네트워크 감소를 혼동하지 않는다. API/model을 임의 재실행해 실패를 지우지 않는다.
4. 실제 MCP stdio, 전체 회귀, evidence/사용 문서를 마친 뒤 사용자 작성자로 commit/push한다. 기존 27/30 문서와 원문은 보존한다.

CI/CD·새 importer·API graph·LLM router·운영 플랫폼·범용 JSONPath·자동 의도 파서는 추가하지 않는다.

진행 중 확인한 최소 조정: 첫 holdout 실행은 사전 검사에서 fork timeout/stargazer 404가 발생해 모델 호출 전 중단됐다. `artifacts/result-delivery/holdout-1.json`의 실패와 7회 HTTP를 보존했다. 서비스 실패를 이유로 질문을 교체하지 않기 위해, holdout의 사전 검사를 진단 자료로 기록하고 고정된 모든 모델 질문을 실행하도록 평가기의 중단 조건만 바꾼다. 원본/공개 검증·시간 제한·검색·질문·채점은 그대로이며 사전 검사 실패도 CLI 실패 상태에 반영한다. 다음 실행은 새 `holdout-2.json`에 저장하고 첫 검사 비용도 함께 보고한다. 제품 코드나 업무 API의 자동 재시도를 추가하지 않는다.

현재 진행: 구현·298개 회귀·기존 24질문/MCP·고정 12질문 실행/재채점 완료. [결과](32-result-delivery-and-holdout-results.ko.md)에 모든 실패와 진단 비용을 보존했다. 보류 요청 3건의 엄격 완료 미달을 성공으로 바꾸지 않았으며 새 기능을 자동 추가하지 않는다.
