# 전체 호출 비용 개발·검증 결과

2026-10-30. [확정 계획](23-total-call-cost-plan.ko.md)의 네 작업을 완료했다. 새 호스트 바인딩은 기존 3도구 방식의 모델 왕복·토큰 부담을 줄였고, 같은 정보를 주는 일반 function 도구와는 비슷한 비용이었다. 일반 검색보다 우월한 검색 알고리즘을 만들었다는 결과는 아니다.

## 구현한 사용 경로

- 목표와 판단 기준을 00/03 문서에 반영했다. 성공은 정확한 인자·사용자 조건·실행 결과를 먼저 확인하고 전체 비용으로 비교한다.
- [a2api-tools/0.1과 ToolSession](24-selected-tools.ko.md)을 추가했다. 기존 descriptor와 discover/describe/invoke wire는 유지한다.
- 호스트가 아는 기능은 처음부터 입력 schema로 제공하고, 모르는 기능은 모델 검색 한 번 뒤 호스트가 describe를 처리해 다음 tools에 제공한다. ID/버전/catalogVersion은 호스트가 관리한다.
- 선택한 계약은 같은 세션에서 재사용하고 완전한 입력 schema를 바이트 예산 안에서 유지한다. 예산 초과 제외·최근 사용 기준 교체·계약 변경 무효화·입력/출력 검증을 구현했다. schema를 자르거나 쓰기를 자동 재시도하지 않는다.
- 기존 model-client에 선택 모드를 연결했다. 별도 파일 생성·승인·서버 단계는 추가하지 않았다. 기존 3도구 모드와 관리 기능은 유지한다.

MCP stdio의 tools/list는 검색 전후 똑같은 세 도구다. 모델이 보는 function 목록만 호스트가 구성한다. 로컬 함수·전환 HTTP 앱·MCP 앱을 같은 ToolSession 규칙으로 사용한다.

## 실행 범위와 비교 방법

모델은 실제 서비스의 `muse-glimmer-30b`, temperature=0, max_tokens=2048, stream=false, tool_choice=auto를 사용했다. 모델 요청 16단계/질문, 질문 180초로 비교 예제를 제한했다. 원래 client의 기본 제한과 구별한다.

세 모드가 같은 입력·공개 출력·실제 HTTP backend·lexical 검색·중립 SYSTEM을 사용했다.

| 모드 | 모델에 주는 도구 | 실행 |
|---|---|---|
| ordinary | 일반 검색+function 도구; 알고 있으면 처음부터 function 제공 | 같은 전환 앱을 in-process 호출 |
| generic | 기존 discover/describe/invoke 공통 3도구 | 실제 MCP stdio |
| selected | 검색 또는 선택한 정확한 function 도구 | ToolSession → 기존 MCP stdio invoke |

ordinary도 같은 앱·schema·검증기를 사용한다. **정보 전달 방식의 비교**이며 독립 GitHub SDK·importer 개발 비용 비교가 아니다. ordinary와 selected의 function 이름/설명/입력 정의를 같은 형식으로 맞췄다. 큰 카탈로그도 같은 검색기를 사용하므로 일반 방식에 전체 schema 덤프를 강요하지 않았다.

2개 카탈로그는 두 기능을 호스트가 미리 아는 구성, 1,000개는 모르는 구성이다. API 수 자체와 가용 지식을 독립적으로 바꾼 인과 실험은 아니다. 라이브러리가 작은 미지/큰 기지 기능도 처리하는 것은 결정적 테스트로 확인했다.

큰 카탈로그는 실제 기능 2개와 상품/결제/계정/재고의 **합성 방해 함수 998개**다. 1,000개 실제 GitHub endpoint, 복잡한 유사 기능 구분, 회사 소스 전체의 LLM 성공률을 검증한 것이 아니다. 검색은 O(N) lexical 순회이며 서버 카탈로그 로딩/해시 계산 비용도 남는다.

한 번의 고정 pilot으로 각 모드 11질문, 총 33질문을 실행했다. 각 카탈로그·모드는 별도 세션이며 그룹별 실행 순서를 교대했다. provider cache·GPU 부하·출력 길이·외부 네트워크는 통제하지 않았다. 실패한 실행을 버리거나 재측정으로 대체하지 않았다.

- 주문: 상태 단순 조회 → 주문 재조회 후 반환된 두 배송 ID로 각각 조회 → 같은 대화에서 주문 재조회 없이 배송 두 건 다시 조회.
- GitHub: `octocat/Hello-World` 저장소+열린 이슈·PR 1페이지 3개 → 같은 대화에서 같은 조건의 2페이지 3개. 작은 카탈로그에는 새 대화의 owner/repo 없는 질문도 포함했다.
- 실제 GitHub forward는 로컬 cache 없이 18회, 모두 HTTP 200이었다. 각 모드 6회다. 시작 quota는 60이었다. 주문 HTTP도 각 모드 12회로 필요한 호출 수를 지켰다.

## 실측 결과

각 모드의 동일한 11질문 합계다. 아래 시간은 모델/도구 요청 시간이며 세션 준비는 다음 단락에 따로 표시한다. 토큰은 provider가 응답한 usage 합계이며 모든 실행에서 제공됐다. 저장 바이트를 토큰으로 환산하지 않았다.

| 항목 | ordinary | 기존 generic | 새 selected |
|---|---:|---:|---:|
| 인자·호출 수·선행 ID 검사 통과 | 11/11 | 11/11 | 11/11 |
| prompt+completion 토큰 | 55,625 | 127,975 | 55,744 |
| 경과 시간 합계 | 110.566초 | 161.030초 | 117.429초 |
| 모델 요청 | 28 | 41 | 28 |
| 모델 도구 호출 | 24 | 33 | 24 |
| 업무 호출 / 실제 HTTP | 18 / 18 | 18 / 18 | 18 / 18 |

이 pilot에서 selected는 generic 대비 토큰 56.4%, 질문 처리 시간 27.1%를 줄였다. ordinary 대비 토큰은 0.21%, 시간은 6.2% 많았다. **일반 검색+function 방식보다 비용 우위를 확인하지 못했다.** 입력 계약을 다시 작성하지 않고 같은 실행·검증 경로에서 비슷한 모델 정보 전달 비용으로 호출할 수 있게 된 결과다. 입력 schema를 알고 있는 일반 API 호출이 본질적으로 느리다는 뜻이 아니다.

4개 세션의 준비 시간 합계는 ordinary 3.457초, generic 4.989초, selected 4.991초였다. 준비까지 더하면 각각 114.023초, 166.019초, 122.420초다. selected의 알려진 기능 준비에는 discover 4회+describe 4회가 포함됐다. 모델 질문 처리 중에는 discover 6회+describe 5회+invoke 18회였다. 따라서 **전체 MCP 업무 protocol 요청은 selected 37회, generic 33회**다. 숨긴 호스트 왕복까지 모두 줄었다고 주장하지 않는다. tools/list/초기 MCP handshake는 별도 연결 비용이며 이 37/33 메서드 수에 넣지 않는다.

구성별 합계도 함께 보존한다. 칸은 `실측 토큰 / 질문 처리 초`다. GitHub 작은 구성은 누락 입력 질문을 포함한 3질문이고 큰 구성은 2질문이므로 서로 절대치를 비교하지 않는다.

| 구성 | ordinary | generic | selected |
|---|---:|---:|---:|
| 주문 2개·알려진 기능, 3질문 | 15,588 / 22.445 | 32,660 / 36.652 | 15,687 / 22.407 |
| 주문 1,000개·미지 기능, 3질문 | 17,316 / 22.700 | 54,873 / 42.237 | 17,598 / 25.108 |
| GitHub 2개·알려진 기능, 3질문 | 10,974 / 33.945 | 23,430 / 44.619 | 10,791 / 32.817 |
| GitHub 1,000개·미지 기능, 2질문 | 11,747 / 31.476 | 17,012 / 37.522 | 11,668 / 37.097 |

큰 GitHub 구성에서는 selected의 토큰은 줄었지만 generic과 경과 시간이 거의 같았다. 모든 구성의 지연을 크게 줄였다고 보고하지 않는다. 단 한 번의 탐색적 비교이므로 작은 차이를 통계적 효과로 해석하지 않는다.

## 정확성 검사와 남은 한계

자동 검사는 33/33에서 요청한 ID·페이지·perPage=3·호출 수·의존 순서를 확인했다. backend를 불필요하게 추가 호출하지 않았다. schema 유효성을 자연어 의도 일치로 바꿔 말하지 않고 실제 인자까지 대조했다.

코딩 에이전트가 33개 최종 답변과 실제 tool 출력을 별도로 읽었다. 반환된 값/ID는 일치했으나, selected의 큰 주문 chain 한 답변에서 **delivered라서 estimatedArrival이 null이라는 원인 추정**을 덧붙였다. 원 응답은 그 인과를 증명하지 않는다. 또 6개 답변(세 모드에 걸쳐 존재)에서 데이터의 `asOf`를 “조회 시점”으로 표현했다. API 재호출 시각과 데이터 기준 시각을 구별해야 한다. 자동 호출 검사 통과가 답변 전체의 완전한 사실성을 뜻하지 않는다. 별도 인간/독립 모델 심사 결과라고 표현하지 않는다.

이 원문과 판단을 재실행/수정으로 지우지 않고 [별도 답변 검토](evidence/tool-session-answer-review.json)에 남겼다. 출력 schema를 서버에서 검증해도 모델의 인과 추정이나 의미 해석까지 자동 검사하지 않는다. 단위·시간·null 의미가 업무에 중요하면 개발자가 summary 또는 반환 DTO에 필요한 의미를 명시해야 한다. 이번에 자동 의도/업무 의미 파서를 추가하지 않았다.

검증한 부정 경로는 잘못된 인자·추가 context 입력·비유한 JSON·예산 초과·교체된 도구·stale catalog·잘못된 성공 출력·기존 권한 경로다. 전체 회귀는 **279개 통과**했다. 별도 실제 모델 CLI에서도 Python 등록 함수 → MCP stdio → 선택 function 호출을 확인했다. 이 CLI smoke는 위 paired 33질문 수치에는 넣지 않았다.

## 재현과 기록

```bash
python -m pip install -e '.[mcp]'
python -m unittest discover -s tests -v

# 모델 환경 변수는 22 문서처럼 자신의 endpoint/model로 설정
python examples/tool-session/evaluate.py --github \
  --output artifacts/tool-session-evaluation/new-run.json
python examples/tool-session/summarize.py \
  artifacts/tool-session-evaluation/new-run.json
```

원 실행은 `artifacts/tool-session-evaluation/pilot-1.json`에 남고 Git 추적에서 제외했다. [집계 evidence](evidence/tool-session-evaluation.json)는 원문 SHA256·전체 집계·각 구성·시작 비용·답변 검토를 보존한다. 원본 report는 답변 검토를 덧쓰기 위해 수정하지 않았다. 별도 review를 합치려면 summarize의 `--answer-review`를 사용하며 원문 hash가 같아야 한다. 자신의 새 실행에는 새 검토가 필요하다.

이 완료 범위는 목표·호스트 정보 전달 프로토콜·실행 모듈·제한된 평가다. 모든 규모/복잡도의 최적화, 의미 검색/업무 그래프, 대화 압축, 운영 플랫폼은 이번 완료에 포함하지 않는다. 새로운 개발 목표를 자동으로 추가하지 않는다.
