# 결과 전달 개선과 고정한 실제 요청 검증

2026-10-30 · [28 문서](28-cost-improvement-plan.ko.md)의 2 → 3번을 [31 문서의 범위](31-result-delivery-and-holdout-plan.ko.md)로 진행했다. 최초 실패/검색만 개선한 결과와 원문은 27/30 문서에 보존한다.

## 구현과 검증 경계

top-level select는 원본 객체와 로컬 참조의 `x-*` annotation을 허용한다. 원본 전체 HTTP 응답 검증 → 명시적 필드 선택 → 공개 응답 검증 순서는 유지한다. 선택하지 않은 잘못된 필드도 차단한다. optional/null/required/참조를 보존하고 누락값을 채우지 않는다. 조합·조건·의존성·추가 object 제약과 `$ref`의 검증 sibling은 선택 대상으로 허용하지 않는다. 기존 관리 Runtime의 projection/정책은 바꾸지 않았다.

평가 앱은 repo의 full_name/default_branch/stargazers_count/archived와 commit의 sha/stats/html_url만 반환한다. 브랜치·다른 배열은 유지한다. 원본 source를 수정하거나 전체 카탈로그의 출력을 임의로 축약하지 않았다. 공개 schema 변경에 따라 검색의 field 근거/corpus 빈도는 달라지지만 검색 알고리즘 `field-search/1`·가중치·keywords는 고정했다.

선택한 function에는 공개 schema의 최대 6개 field 이름·타입·필수 여부만 반환 설명으로 붙인다. 배열은 item field, nullable은 명시된 타입으로 표시한다. 복합/순환 schema를 추측하지 않고 실제 데이터·예시·원문 description·전체 출력 schema는 넣지 않는다. `a2api-tools/0.3` 호스트 표현이며 `a2api-call/0.1` wire·descriptor 6필드·MCP 세 도구는 그대로다. ordinary에도 같은 설명·projection·예산·원본/공개 검증을 적용했다.

전체 회귀 **298개 통과**. 실제 HTTP에서 선택 전 원본 실패, 선택 필드의 필수/선택/null/참조, 제약 거부, 반환 설명의 길이/참조/노출 범위, 같은 대조군 도구 정의를 확인했다. 실제 MCP stdio에서도 도구 목록 세 개 고정, 조건부 1→2페이지, repo→commit 조회가 통과했다(discover 4/describe 8/invoke 2, 22.421초). stdio는 주 모델 비교에 더하지 않았다. [전환 사용법](11-in-memory-conversion.ko.md), [모델 도구 사용법](24-selected-tools.ko.md)을 제공한다.

## 동일한 기존 24질문

공식 고정 GitHub source/revision/SHA256, GET 8개/633개(전체 GET 655 중 지원 633·미지원 22), Muse `muse-glimmer-30b`, temperature=0/max_tokens=2048/stream=false/tool_choice=auto, 새 대화/세션, 순서 교대, 2반복, 12단계/120초/후보 3개/16KB를 유지했다. 2개 공개 저장소의 단순 repo·브랜치 페이지·실제 기본 브랜치→head commit 요청이다. 기존 질문·채점기를 변경하지 않았으며 실제 인자를 보정하지 않았다. 양쪽 모두 in-process HTTP이며 독립 SDK/개발 공수 비교가 아니다.

| 카탈로그 | 방식 | 정확한 완료 | provider 전체 토큰 | 질문 시간 | 모델 요청 | 검색 | 업무 HTTP |
|---|---|---:|---:|---:|---:|---:|---:|
| 8개 | ordinary | 6/6 | 79,847 | 116.018초 | 24 | 12 | 12 |
| 8개 | a2api | 6/6 | 79,847 | 115.784초 | 24 | 12 | 12 |
| 633개 | ordinary | 6/6 | 56,710 | 104.227초 | 20 | 12 | 8 |
| 633개 | a2api | 6/6 | 56,710 | 104.433초 | 20 | 12 | 8 |

각 모드 총 **12/12**, 단순 8/8·연쇄 4/4다. provider usage는 모든 질문에 제공됐다. 재채점 변경은 없었고 업무 실패/잘못된 입력은 없었다. 모델의 more 요청은 0회였다.

| 모드별 12질문 합계 | ordinary | a2api |
|---|---:|---:|
| prompt + completion | 124,978 + 11,579 | 124,978 + 11,579 |
| 전체 토큰 | 136,557 | 136,557 |
| 질문 시간 | 220.245초 | 220.217초 |
| 세션 준비 포함 | 222.045초 | 222.027초 |
| 공통 카탈로그 준비 1회 포함 | 243.041초 | 243.023초 |
| 모델 요청 / 검색 / 업무 HTTP | 44 / 24 / 20 | 44 / 24 / 20 |
| 최소보다 추가한 적법한 조회 | 4 | 4 |
| 정규화한 tool 정의 바이트 누적 | 255,011 | 255,011 |
| 모델 tool 결과 바이트 합계 | 21,702 | 21,702 |
| GitHub HTTP body 바이트 합계 | 81,428 | 81,428 |

공통 준비 20.996초는 source load/import와 두 앱 convert의 합계다. 각 독립 호스트가 카탈로그를 한 번 준비한다고 가정해 같은 비용을 더했다. 평가 전체 wall time이나 작은 앱 하나의 일반 시작 비용이라고 부르지 않는다. 주 비교 40회+사전 2회+stdio 2회, 계측한 업무 GitHub GET **44회 모두 200**이었다. quota/models 메타데이터 조회는 이 업무 호출 수에 포함하지 않는다.

### 검색만 개선한 30 문서와 비교

- 같은 정확도에서 a2api 전체 토큰 169,707→136,557로 **19.5% 감소**, ordinary 176,274→136,557로 **22.5% 감소**했다. 두 방식의 이번 합계는 같아 프로토콜만의 우위를 주장하지 않는다.
- 큰 구성은 90,456→56,710으로 양쪽 모두 37.3% 감소했다. 작은 a2api는 79,251→79,847로 **약 0.8% 증가**했고 ordinary는 85,818→79,847로 감소했다. 모든 규모/요청에 동일한 효과가 생긴 것은 아니다.
- a2api tool 결과 바이트는 84,934→21,702로 74.4% 줄었지만 tool 정의 누적은 218,916→255,011로 16.5% 늘었다. 반환 설명과 모델이 선택한 추가 조회 경로가 함께 영향을 줬다. 이 바이트 수를 토큰으로 환산하지 않는다.
- 실제 HTTP는 각 모드 19→20회, body 합계는 75,020→81,428바이트로 늘었다. 원 서버는 전체 JSON을 반환하며 공개 필드 선택은 그 뒤에 적용된다. 네트워크 감소를 주장하지 않는다.
- 준비 포함 a2api 시간은 248.107→243.023초였지만 2반복과 제공자/서비스 부하 범위의 작은 차이다. 안정적 지연 우위로 단정하지 않는다. 새 설명·projection·그에 따른 공개 field index를 함께 적용한 결과이며 각각의 독립 효과를 분리한 실험이 아니다.

## 보류한 12질문

질문과 채점기는 모델 실행 전에 고정했다. 검색 1번 때 이미 확인한 languages/license/tags/contributors 등 10개 오프라인 질의를 새 holdout으로 부르지 않고, release·fork·stargazer·기본 브랜치→commit status의 6요청을 사용했다. 633개에서 두 방식·1반복, 마지막 2요청은 연쇄다. hash와 실제 사용한 구현 hash를 report에 기록했다. 이들은 미래 API 전반의 성공률을 대표하지 않는다.

첫 사전 검사는 fork timeout/stargazer 404로 모델 호출 전 중단됐다. [실패 기록](evidence/result-delivery-preflight.json)의 7회 HTTP와 카탈로그 준비 비용을 보존했다. 질문이나 업무 검증을 바꾸는 대신 평가기의 holdout 사전 검사만 진단 자료로 취급하고 전체 질문을 실행하도록 조정했다. 사전 실패는 CLI 실패 상태에도 반영한다. 제품의 시간 제한·자동 재시도·인증·검색은 변경하지 않았다. 두 번째 전체 실행과 첫 사전 실패를 구분해 보고한다.

| 고정 요청 | ordinary | a2api |
|---|---:|---:|
| 최신 release | 통과 · 6,752토큰 | 통과 · 6,727토큰 |
| release 첫 페이지 2개 | 통과 · 13,855토큰 | 통과 · 13,876토큰 |
| newest fork 첫 페이지 2개 | 통과 · 10,555토큰 | 미통과 · 14,075토큰 |
| stargazer 첫 페이지 2명 | 미통과 · 57,560토큰 | 미통과 · 59,765토큰 |
| 실제 기본 브랜치→combined status | 통과 · 15,361토큰 | 통과 · 14,559토큰 |
| 실제 기본 브랜치→statuses 첫 페이지 2개 | 통과 · 14,223토큰 | 통과 · 14,561토큰 |

| 모드별 6질문 합계 | ordinary | a2api |
|---|---:|---:|
| 엄격한 완료 / 실제 값 일치 | 5/6 / 5/6 | 4/6 / 5/6 |
| prompt + completion | 108,482 + 9,824 | 114,480 + 9,083 |
| 전체 토큰(실패 포함) | 118,306 | 123,563 |
| 질문 시간 | 183.872초 | 173.677초 |
| 세션 준비 / 공통 준비 1회 포함 | 2.004초 / 206.390초 | 1.549초 / 195.740초 |
| 모델 요청 / 검색 / 업무 HTTP | 29 / 18 / 15 | 31 / 19 / 13 |
| 실패한 업무 시도 | 6 | 4 |
| more 요청 | 0 | 2 |
| 필수 계약을 제공한 질문 | 6/6 | 6/6 |

질문 전체 **9/12 엄격 통과**, 실제 최종 값은 10/12가 일치했다. 두 연쇄 요청은 모두 통과했으며 기본 브랜치와 ref의 실제 값 흐름, page/per_page, 빈 status 배열과 최종 타입을 검사했다. 모든 usage가 제공됐고 동일 원문 재채점 변경은 없었다. 실패를 성공으로 보정하지 않았다.

- fork의 a2api 실행은 첫 요청이 시간 초과였고 모델이 두 번째 요청으로 올바른 값을 얻었다. 실패 이력은 남으므로 엄격한 완료는 실패, 사실 일치는 성공이다. 호스트/adapter가 자동 재시도한 것이 아니다. 같은 질문의 ordinary는 첫 시도에 완료했다. 이 차이를 검색이나 프로토콜의 정확도 차이로 단정하지 않는다.
- stargazer는 두 방식 모두 필요한 계약을 제공받아 정확한 endpoint를 호출했지만 404를 받았다. 이후 검색/업무 호출을 반복해 모델 12단계 한도에 도달했다. API 접근 실패와 그 뒤의 불필요한 탐색 비용을 구분한다. a2api는 이 과정에서 more를 2회 사용했고 새 후보를 받았으나 업무 권한 문제를 해결하지 못했다.
- 별도 직접 진단도 같은 URL에서 인증 404(`Not Found`), 익명 401(`Requires authentication`)이었다. [GitHub 공식 문서](https://docs.github.com/en/rest/activity/starring#new-access-restrictions)는 2026년 7월부터 stargazer 목록을 관리자·협업자로 제한한다고 안내하며, [공식 변경 공지](https://github.blog/changelog/2026-06-30-upcoming-access-restrictions-to-public-api-endpoints-and-ui-views/)도 이 제한을 명시한다. 이번 응답은 그 접근 제한과 일치하는 것으로 해석한다. 404만으로 토큰의 세부 권한을 확정하지 않으며 credential/권한을 변경하거나 익명 fallback을 추가하지 않았다.

holdout의 두 모드는 엄격한 성공률이 다르므로 총 토큰/시간으로 우위를 주장하지 않는다. 공통으로 통과한 4요청만 보면 ordinary 50,191토큰/79.555초, a2api 49,723토큰/83.626초다. 1반복의 작은 차이이고 실패를 제외한 이 수치를 전체 비용처럼 표현하지 않는다. 공개 source의 지원 GET 633개는 현재 caller가 633개 모두 실행할 수 있다는 뜻이 아니다. OpenAPI import만으로 현재 운영 권한·서비스 상태를 보장하지 않는다.

### 별도 실패·진단 비용

완료한 holdout은 사전 7회+모델 업무 28회로 **35회** 실제 GET(200 25회/404 10회)이었다. 첫 중단의 7회(200 6회/404 1회), 이후 직접 진단 2회(404/401)를 따로 보존했다. 전체 core/holdout/진단의 계측 업무 GET은 **88회(200 75회/404 12회/401 1회)**다. upstream 200이어도 caller가 먼저 timeout이면 성공으로 바꾸지 않았다.

holdout의 공통 준비는 20.514초다. 첫 중단의 카탈로그 준비 20.440초와 HTTP별 시간 합계 4.146초, 마지막 직접 진단 0.651초는 모드별 질문 시간에 숨겨 넣거나 제외해 버리지 않고 별도 비용으로 기록했다. HTTP별 합계는 요청 중첩이 가능하므로 전체 wall time이 아니다. 첫 중단은 모델 호출 0회였고 실제 모델 질문의 재실행은 없었다. 전체 Chat Completions 요청은 core 88회+holdout 60회로 148회였다. holdout CLI는 사전 검사/질문 실패를 반영해 종료 코드 1을 반환했다.

## 재현

```bash
python -m pip install -e '.[mcp]'
python -m unittest discover -s tests -v
# docs/22의 model endpoint/model 환경 변수와 로그인된 gh를 사용
python examples/real-github-evaluation/evaluate.py --github-auth gh \
  --suite core --repetitions 2 --stdio --output artifacts/result-delivery/my-core.json
python examples/real-github-evaluation/evaluate.py --github-auth gh \
  --suite holdout --repetitions 1 --output artifacts/result-delivery/my-holdout.json
python examples/real-github-evaluation/review.py artifacts/result-delivery/my-core.json \
  --output artifacts/result-delivery/my-core-review.json
python examples/real-github-evaluation/summarize.py artifacts/result-delivery/my-core.json \
  --review artifacts/result-delivery/my-core-review.json \
  --output artifacts/result-delivery/my-core-summary.json
# holdout도 같은 review/summarize에 해당 원문 경로를 넣는다.
```

[기존 요청 실측](evidence/result-delivery-core.json), [holdout 실측](evidence/result-delivery-holdout.json), [첫 사전 실패](evidence/result-delivery-preflight.json), [직접 진단](evidence/result-delivery-service-diagnostic.json), [실제 호출 발췌](evidence/result-delivery-traces.json)에 원문 hash·모든 실패·비용을 기록했다. 발췌는 읽기 위한 preview이며 benchmark의 추가 projection이 아니다. 원문은 ignored `artifacts/result-delivery/core-1.json`, `holdout-1.json`, `holdout-2.json`이고 재채점 기록은 `core-review-1.json`, `holdout-review-2.json`이다. 제품 코드·질문·채점기 hash를 대조했고 첫 중단 뒤 바뀐 구현은 평가기의 사전 중단/종료 조건뿐이다. 이전 30 문서의 원문도 현재 reviewer로 같은 판정을 재현할 수 있다. 계정 credential은 호스트 메모리에서만 사용했으며 모델·evidence에 저장하지 않았다.

2번 구현과 3번 고정 평가 실행은 완료했다. 기존 요청 정확도 유지/전체 토큰 감소는 확인했지만, 보류 요청 3건은 엄격한 완료 조건에 미달했다. 서비스/접근 실패 뒤의 반복 탐색 비용도 남아 있어 프로토콜의 보편적 우위나 모든 업무의 효율화를 달성했다고 표현하지 않는다. 새로운 운영 기능이나 후속 개발을 자동으로 추가하지 않는다.
