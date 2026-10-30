# 실제 GitHub 카탈로그 검증 범위

2026-10-30 사용자 요청: 합성 기능을 제외한 GitHub 조회 API로 Muse Glimmer를 검증하고, 정확도를 유지하면서 전체 비용을 줄일 개선 계획을 세운다. 이번에는 평가 예제·결과·후속 계획을 작성하며 프로토콜 최적화를 미리 구현하지 않는다.

## 1. 실제 카탈로그 구성

- 저장소에 고정한 공식 GitHub OpenAPI revision `443ef1513a17aad7f781391c4fb4e132b9b549fd`와 원문 SHA256을 검증한다. 최신 전체 명세라고 부르지 않는다.
- GET 655개를 현재 importer/converter로 검사한다. importer 지원 수와 실제 메모리 convert 성공 수를 각각 기록하고 제외 이유를 남긴다. 가짜 함수·route·schema를 추가하지 않는다.
- 소규모는 서로 관련된 조회 8개(repos/get, get-commit, list-commits, get-branch, list-branches, get-latest-release, issues/list-for-repo, pulls/list), 대규모는 변환 가능한 전체 GET으로 구성한다. 원문 설명·태그와 schema를 사용하며 질문에 맞춘 키워드를 보충하지 않는다.
- 두 크기 모두 초기에는 검색 도구만 제공한다. 목표 operation 이름/정답/기본 브랜치는 모델에게 미리 주지 않는다. 입력 schema와 결과 projection은 크기·모드에 관계없이 같다.
- 처음에는 저장소/커밋 결과의 top-level select를 계획했으나 아래 실제 제한을 확인했다. 이번 평가에서는 양쪽에 원본 전체 응답과 검증을 동일하게 적용한다. 최종 답변은 요청한 필드만 JSON으로 받아 실제 결과와 비교한다. 전체 GET을 실제 호출한 것으로 보고하지 않는다.

## 2. 대조군과 고정 요청

비교는 일반 검색+function 호스트와 기존 ToolSession의 두 모드다. 같은 전환 앱·lexical 검색·후보 수(3)·입출력·결과를 사용한다. 주 비교는 양쪽 모두 in-process HTTP 실행으로 맞춰 stdio 유무의 영향을 제거한다. 실제 MCP stdio 연결은 별도 smoke로 확인하며 주 성능 수치와 합치지 않는다. 독립 GitHub SDK나 개발 공수 비교로 해석하지 않는다.

각 크기 × 두 모드 × 아래 3요청 × 2반복, 총 24질문을 고정한다. 매 질문은 새 대화/도구 세션이며 모드 순서를 교대한다. 이 조건은 이전 warm 대화 비교와 다르다.

1. 단순 조회: psf/requests의 기본 브랜치·별 개수·보관 여부.
2. 인자 제약: octocat/Hello-World의 브랜치 목록 첫 페이지, 최대 2개. 생략된 기본값은 원 API 기준으로 해석하고 per_page=2는 반드시 지켜야 한다.
3. 연쇄 조회: octocat/Hello-World 저장소에서 실제 default_branch를 먼저 확인한 후 해당 브랜치의 head commit SHA와 additions/deletions를 조회한다. `repos/get-commit`의 ref에는 브랜치 이름을 쓸 수 있으므로 불필요한 중간 API를 필수 단계로 만들지 않는다. 반환된 SHA를 경유하는 적법한 다른 경로도 판정하되 추가 비용은 기록한다.

모델·temperature/max_tokens·SYSTEM·도구 이름 형식은 양쪽에 같게 적용한다. 기존 model-client의 chat 함수를 재사용한다. 도구 인자를 보정하거나 실패를 조용히 재시도하지 않는다. 실패/초과 비용도 전체 집계에 넣는다.

## 3. 실제 호출과 측정

- 실제 GitHub 응답을 사용하며 로컬 cache/replay/fixture로 대체하지 않는다. API 요청 수·상태·응답 hash/바이트·네트워크 시간·rate-limit 헤더를 기록한다. 원 서비스의 변화/cache와 모델 제공자의 부하/cache는 통제하지 못함을 명시한다.
- quota를 먼저 확인한다. 필요하면 이미 로그인된 GitHub CLI의 인증을 호스트 메모리에서만 재사용한다. 공개 두 저장소 하위 GET만 중계하며 토큰을 모델·파일·로그로 전달하지 않는다. 두 모드는 동일한 인증 조건을 사용한다. 요청 예산과 timeout을 제한하고 quota 때문에 미실행한 것은 모델 실패와 구별한다.
- 원본 spec 로드/변환 시간과 세션 준비 시간을 분리한다. 초기 준비를 포함한 합계, 모델 prompt/completion/total usage, 모델 왕복, 모델 도구/내부 요청/실제 GitHub 호출, tools/대화/결과 바이트를 구분한다. 바이트를 토큰으로 환산하지 않는다.
- 성공 여부는 operation 이름만 맞추는 검사가 아니다. 입력 schema, owner/repo·페이지·개수, 실제 선행 결과를 사용한 ref/SHA, 데이터/실패 보고를 확인한다. 잘못된 시도 뒤 성공은 첫 시도 성공과 구별하고 추가 호출은 비용에 남긴다.
- 두 모드의 실제 tools payload가 달라졌다면 차이와 예산/노출 영향을 보고한다. 큰 카탈로그 전체 dump를 대조군으로 삼지 않는다.

## 4. 산출물과 완료 조건

- `examples/real-github-evaluation/`: 실제 카탈로그 생성·한정된 HTTP 중계·고정 평가·집계 예제. 기존 합성 예제는 재현용으로 보존한다. 제품 코드와 기존 wire는 변경하지 않는다.
- 관련 결정적 테스트: 합성 operation 없음, source/route/GET 연결, 실제 source 기반 입력 보존, 연쇄 판정과 페이지·개수 오류 검출. 일반 unit test는 외부 모델을 호출하지 않는다.
- `docs/27-real-github-evaluation-results.ko.md`와 작은 evidence JSON: 모든 실행의 집계·실패·한계·재현 명령. 대형 원문 report는 ignored artifacts에 보존한다.
- `docs/28-cost-improvement-plan.ko.md`: 관찰한 병목에 근거해 우선순위·변경 파일/인터페이스·정확성 조건·측정 기준을 고정한다. 아직 구현하지 않은 기능은 계획으로 표시한다. 요청하지 않은 CI/배포/관리 플랫폼을 추가하지 않는다.

진행 순서: 계획 기록 → 소스/전환 inventory → 평가 예제와 부정 판정 테스트 → 실제 Muse 비교/stdio smoke → 결과 대조와 개선 계획 기록. 성능 개선이나 완벽한 모델 성공 자체가 이번 검증의 완료 조건은 아니다.

## 확인한 최소 범위 조정

- `repos/get`의 응답 object에는 `x-github-breaking-changes` annotation이 있다. 현재 converter의 보수적인 select profile은 이를 plain object로 보지 않아 `UNSUPPORTED_SELECTION`을 반환했다. 전체 응답 convert는 633개 모두 성공한다. 제품 코드를 고치거나 원문 annotation/schema를 지우지 않고 양 모드 모두 projection 없이 비교한다. 필요 필드 선택은 후속 개선 계획에서 정확성 조건과 함께 다룬다.
- 초반 연쇄 실행은 실제 default_branch=`master`를 읽은 뒤 `ref=heads/master`로 성공했고, 반환 SHA/통계도 사전 `ref=master` 조회와 일치했다. 최초 판정기가 입력 문자열의 완전 일치만 허용해 이를 오답으로 분류한 오류를 확인했다. 이미 읽은 branch에서 만드는 `heads/`·`refs/heads/` 한정 변형을 허용하고, 원 실행·최초 판정은 보존한 채 별도 오프라인 재판정으로 기록한다. 모델을 재실행해 성공으로 바꾸지 않는다.
