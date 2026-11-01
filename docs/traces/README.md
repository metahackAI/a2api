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

5단계(자체 에이전트) 기록과 6단계 design 측정은 [40 문서](../40-problem-solving-process.ko.md)에 따로 있다.
