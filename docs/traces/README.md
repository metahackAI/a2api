# 실행 기록(traces)

a-commerce 과업을 우리 하네스(`examples/acommerce/evaluate.py`)로 실행한 모든 기록이다. 과업마다 질문, 모델이 부른 API와 인자, 받은 결과, 모델 판단(2026-11-02 실행부터), 답, 채점을 순서대로 보인다. 단계별 설명과 대표 사례는 [40 문서](../40-problem-solving-process.ko.md)에 있다.

- 생성: `python examples/acommerce/traces.py artifacts/acommerce/runs/<묶음>.jsonl --out docs/traces`. 원본 JSONL은 저장소에 넣지 않는 `artifacts/acommerce/runs/`에 있다.
- 결과는 모델이 받은 그대로이고, 페이지에는 앞 600자, 인자는 700자, 모델 판단은 700자만 보인다. 원본 기록에는 결과가 1,500자(2026-11-02부터 3,000자)까지 있다.
- 시각은 KST다(파일 머리의 `startedAt`은 UTC).
- 표의 표시: ✓ 통과, ✗ 실패, E 하네스 한도·오류로 중단(모델 호출 12회, 도구 호출 20회, 턴당 120초, 문맥 초과, 출력 한도, provider 오류).

## 방식 이름

| 방식 | 모델이 받는 것 |
|---|---|
| `acom-all` | A-Commerce 도구 253개 정의 전부(원본) |
| `facade-all` | 운영자 파사드 화면 전부(원본, 19개) |
| `a2api-acom` | 253개를 a2api로 변환, 질문으로 사전 선택한 8개 + `a2api_search` |
| `a2api-facade` | 파사드를 a2api로 변환(이름·코드값·설명 보탬) |
| `a2api-acom-index` | 이름 + 요약 목차(system prompt) + `a2api_load` |
| `a2api-acom-graph` | 위 + 결과에 "이 ID를 받는 함수" 안내 |
| `a2api-acom-names` | 도메인별 이름 목차 + `a2api_load` + 관계 안내 |
| `a2api-acom-names-norelated` | 이름 목차 + `a2api_load` |
| `a2api-acom-hybrid` | 이름 목차 + 사전 선택 8개를 미리 불러 둠 |
| `a2api-acom-names-batch` | 이름 목차 + `a2api_load` + `a2api_batch` |
| `…-guard` | 위 방식 + 반복 감지 안내(`variant_note=3`) |

## 묶음

| 단계 | 묶음 | 시작(KST) | 세트 | 실행 | 통과 | 비고 |
|---|---|---|---|---|---|---|
| 1 | [ours-design-1](ours-design-1/README.md) | 10/31 23:18 | design | 48 | 6 | **결과에서 제외**: 쓰기 과업 앞에서만 초기화해 앞 실행의 쓰기가 남음 |
| 1 | [ours-design-2-aborted-reset-bug](ours-design-2-aborted-reset-bug/README.md) | 11/01 00:02 | design | 9 | 1 | 같은 결함을 찾고 중단 |
| 1 | [ours-design-3](ours-design-3/README.md) | 11/01 00:18 | design | 35 | 6 | 매 실행 초기화 후. 도중에 로컬 스택이 멈춰 남은 과업은 3b·3c로 이어 실행 |
| 1 | [ours-design-3b](ours-design-3b/README.md), [3c](ours-design-3c/README.md) | 11/01 00:54 | design | 13 | 0 | 3의 남은 과업 |
| 2 | [ours-design-4](ours-design-4/README.md) | 11/01 01:12 | design | 24 | 4 | 결과 상한 처리 |
| 1 | [ours-heldout-1](ours-heldout-1/README.md) | 11/01 01:53 | held_out | 128 | 12 | **held_out 판정**(네 방식 × 2회) |
| 2 | [ours-design-5](ours-design-5/README.md) | 11/01 04:20 | design | 24 | 5 | 판정 뒤 수정: 못 본 함수 보호 |
| 2 | [ours-heldout-posthoc-1](ours-heldout-posthoc-1/README.md) | 11/01 04:50 | held_out | 64 | 8 | 사후 확인 |
| 2 | [ours-design-6](ours-design-6/README.md) | 11/01 07:02 | design | 24 | 3 | "새 함수 없음" 안내 + 연속 검색 상한 4 |
| 3 | [smoke-index-1](smoke-index-1/README.md) | 11/01 11:14 | design | 6 | 6 | 목차 방식 첫 확인(2과업) |
| 3 | [ours-design-7](ours-design-7/README.md) | 11/01 11:19 | design | 96 | 38 | 검색 / 요약 목차 / 목차 + 관계 / 이름 목차 + 관계 |
| 3 | [ours-design-8](ours-design-8/README.md) | 11/01 13:22 | design | 48 | 21 | 이름 목차, 관계 안내 있음·없음 |
| 3 | [ours-design-9](ours-design-9/README.md) | 11/01 14:11 | design | 24 | 6 | 혼합(기각) |
| 3 | [ours-heldout-index-posthoc-2](ours-heldout-index-posthoc-2/README.md) | 11/01 14:47 | held_out | 96 | 19 | 사후 확인 |
| 4 | [smoke-diag-truncation](smoke-diag-truncation/README.md) | 11/01 17:09 | design | 3 | 0 | 잘린 출력 재현 |
| 4 | [smoke-fix-1-headings](smoke-fix-1-headings/README.md) | 11/01 17:17 | design | 5 | 1 | 출력 상한 제거·`domain.resource` 제목(제목을 이름에 붙임) |
| 4 | [smoke-fix-2-batch](smoke-fix-2-batch/README.md) | 11/01 17:28 | design | 4 | 1 | `a2api_batch` 첫 확인 |
| 4 | [smoke-fix-3-b1](smoke-fix-3-b1/README.md) | 11/01 17:35 | design | 1 | 0 | 목차 줄을 통째로 보낸 이름 해석 |
| 4 | [ours-design-10](ours-design-10/README.md) | 11/01 17:37 | design | 72 | 30 | 검색 / 이름 목차 / 목차 + batch(처음부터 보임) |
| 4 | [ours-design-11](ours-design-11/README.md) | 11/01 20:15 | design | 24 | 13 | a-commerce `d86a1ff`, batch는 불러온 뒤 보임 |
| 4 | [ours-heldout-fix-posthoc-1](ours-heldout-fix-posthoc-1/README.md) | 11/01 20:42 | held_out | 96 | 19 | 사후 확인 |
| 6 | [smoke-guard-1](smoke-guard-1/README.md) | 11/02 00:44 | design | 1 | 0 | 반복 감지 첫 확인, 모델 판단 기록 시작 |

| 5 | [own22-heldout-raw-logs](own22-heldout-raw-logs/README.md) | 11/02 04:12 | held_out | 32 | 5 | a-commerce 자체 에이전트 + 원본 파사드 22개(a-commerce `d86a1ff`, 평가기 `--logs`) |
| 5 | [own22-heldout-a2api-lookup-logs](own22-heldout-a2api-lookup-logs/README.md) | 11/02 04:18 | held_out | 32 | 8 | 자체 에이전트 + a2api 게이트웨이(주문 번호 조회 포함) |
| 6 | [ours-design-12b](ours-design-12b/README.md) | 11/02 04:24 | design | 96 | 36 | 검색 / 검색 + 반복 감지 / 목차 + batch / 목차 + batch + 반복 감지. 단계별 모델 판단 포함 |
| 6 | [ours-heldout-guard-posthoc-1](ours-heldout-guard-posthoc-1/README.md) | 11/02 06:08 | held_out | 128 | 29 | 반복 감지 사후 확인(네 방식) |
| 6 | [ours-design-12-slow-provider](ours-design-12-slow-provider/README.md) | 11/02 00:46 | design | 60 | 10 | **결과에서 제외**: 모델 서버 저하(출력 토큰당 89–153ms, 평소 17ms)로 대부분 시간 초과. 중단 |

| 7 | [ours-design-settings-1](ours-design-settings-1/README.md) | 11/02 10:08 | design | 96 | 33 | 모델 카드 설정: 검색 / 목차 + batch / 원본 파사드 전부 / a2api 변환 파사드 전부. [리뷰](ours-design-settings-1/review.md) |
| 7 | [ours-held_out-settings-1](ours-held_out-settings-1/README.md) | 11/02 12:00 | held_out | 128 | 29 | 같은 네 방식(클레임 키 설명 보충 뒤). [리뷰](ours-held_out-settings-1/review.md) |
| 7 | [ours-design-settings-nohistory-1](ours-design-settings-nohistory-1/README.md) | 11/02 14:22 | design | 48 | 19 | 샘플링만(추론 재전달 없음). [리뷰](ours-design-settings-nohistory-1/review.md) |
| 7 | [ours-design-facade2-1](ours-design-facade2-1/README.md) | 11/02 15:09 | design | 24 | 4 | 변환 보충 뒤 a2api 파사드. [리뷰](ours-design-facade2-1/review.md) |
| 7 | [ours-held_out-facade2-1](ours-held_out-facade2-1/README.md) | 11/02 15:37 | held_out | 32 | 12 | 변환 보충 뒤 a2api 파사드. [리뷰](ours-held_out-facade2-1/review.md) |
| 7 | [ours-held_out-settings-nohistory-1](ours-held_out-settings-nohistory-1/README.md) | 11/02 16:07 | held_out | 64 | 12 | 샘플링만(추론 재전달 없음). [리뷰](ours-held_out-settings-nohistory-1/review.md) |
| 7 | [ours-design-settings-recent-1](ours-design-settings-recent-1/README.md) | 11/02 22:46 | design | 29 | 11 | 추론 재전달을 최근 2단계로 줄임(`recent`). 23:46 모델 서버 중단으로 멈춤(마지막 실행은 모델 응답 0회라 1b에서 다시 함). [리뷰](ours-design-settings-recent-1/review.md)(1 + 1b) |
| 7 | [ours-design-settings-recent-1b](ours-design-settings-recent-1b/README.md) | 11/03 06:52 | design | 20 | 9 | 남은 실행. 모델 서버가 출력 토큰당 약 47ms(평소 18ms)여서 턴 시간 한도를 120 → 320초로 같은 비율만큼 늘림(호출 한도는 그대로) |
| 7 | [ours-held_out-settings-recent-1](ours-held_out-settings-recent-1/README.md) | 11/03 00:07 | held_out | 64 | 15 | `recent`. mgr-weekly-summary 2회차 두 실행은 provider 502로 모델 응답 0회라 1b에서 다시 함. [리뷰](ours-held_out-settings-recent-1/review.md)(1 + 1b) |
| 7 | [ours-held_out-settings-recent-1b](ours-held_out-settings-recent-1b/README.md) | 11/03 07:33 | held_out | 2 | 1 | 위 두 실행(턴 시간 한도 320초) |

| 8 | [own-latest-heldout-raw](own-latest-heldout-raw/README.md) | 11/03 09:43 | held_out | 48 | 7 | a-commerce main `4c6e415` 자체 에이전트(작업·계획 모델 모두 Glimmer) + 원본 파사드, 각 3회. [리뷰](own-latest-review-heldout.md) |
| 8 | [own-latest-design-raw](own-latest-design-raw/README.md) | 11/03 09:56 | design | 36 | 0 | 원본 파사드. [리뷰](own-latest-review-design.md) |
| 8 | [own-latest-heldout-a2api](own-latest-heldout-a2api/README.md) | 11/03 10:06 | held_out | 48 | 9 | a2api 게이트웨이(주문 번호 조회 없음) |
| 8 | [own-latest-design-a2api](own-latest-design-a2api/README.md) | 11/03 10:14 | design | 36 | 3 | a2api 게이트웨이(조회 없음) |
| 8 | [own-latest-heldout-a2api-lookup](own-latest-heldout-a2api-lookup/README.md) | 11/03 10:23 | held_out | 48 | 12 | a2api 게이트웨이 + 주문 번호 조회 |
| 8 | [own-latest-design-a2api-lookup](own-latest-design-a2api-lookup/README.md) | 11/03 10:32 | design | 36 | 3 | a2api 게이트웨이 + 주문 번호 조회 |
| 8 | [own-latest-heldout-acom](own-latest-heldout-acom/README.md) | 11/03 10:40 | held_out | 48 | 11 | A-Commerce 도구(참고) |
| 8 | [own-latest-design-acom](own-latest-design-acom/README.md) | 11/03 10:53 | design | 36 | 15 | A-Commerce 도구(참고) |

`review.md`는 `call_review.py`가 만든 단계별 리뷰다(처음 막힌 단계, 실패 호출의 원인, 기대와 다른 쓰기 입력). `recent` 묶음의 리뷰는 1과 1b를 합친 것이다(모델 응답 0회로 끝나 다시 한 실행은 1b 결과를 쓴다).

8단계(자체 에이전트, [42 문서](../42-own-agent-latest.ko.md))의 리뷰는 `own_review.py`가 자체 에이전트 기록으로 만든다([held_out](own-latest-review-heldout.md), [design](own-latest-review-design.md)).

자체 에이전트 페이지(`own_traces.py`)는 라우팅, 도구 검색 후보, 계획, 호출과 결과, 답, 화면 블록을 보인다. 그보다 앞선 자체 에이전트 실행(3.7절, 10/31–11/01)은 `--logs` 없이 돌려 보고서의 도구 이름만 남았다.
