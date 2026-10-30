# 검색 개선 1번 구현·검증 범위

2026-10-30 사용자가 [28 문서](28-cost-improvement-plan.ko.md)의 **1번만** 요청했다. 이 범위 기록 후 구현한다.

## 구현 규칙

- 완전한 capability ID는 해당 ID의 버전들만 반환한다. prefix 이웃은 섞지 않으며 실제 복수 버전은 prime에서 모호성 오류를 유지한다.
- 원본 operationId/함수 이름, ID, summary, 명시적 keywords, 공개 입력/출력 field를 구분해 서버 index를 만든다. 경계 표기를 정규화하고 흔한 단어·긴 본문의 기여를 줄인다. root field를 우선하며 가까운 자식 field는 낮은 비중으로만 사용한다. 중첩 repository 객체 전체를 펼치거나 순환/복합 schema를 추측하지 않는다. 한글·기존 keywords는 보존한다.
- 기존 호스트 검색에 선택적 `more: true`를 추가한다. query는 계속 필수이고 cursor는 모델에 주지 않는다. 질의당 최대 3페이지, 검색 후보 3개·16KB 예산은 그대로다. 반복 질의는 현재 페이지를 재사용하고 새 후보 유무를 알린다. 새 질의 없이 more, 끝난 페이지, 페이지 한도는 구조화된 오류로 처리한다.
- pagination은 catalog/query/caller/limit에 묶고 검색 revision이 바뀐 cursor도 거부한다. contract drift 시 선택 도구와 페이지 상태를 폐기하고 자동 재시도하지 않는다.
- 공통 wire는 a2api-call/0.1과 MCP 3도구를 유지한다. 확장한 호스트 검색 표현은 a2api-tools/0.2로 표시하며 query-only 입력은 호환된다. 전체 schema를 검색 결과/도구 목록에 추가하지 않는다.

## 순서와 완료 조건

1. 검색 index·정확 ID·페이지 상태 구현 후 후보 노출·예산·caller/catalog 변경·복수 버전·한글/keywords 회귀를 검사한다.
2. 이전 실제 GitHub 질의의 순위를 재현하고 별도로 고정한 미사용 질의에서도 올바른 후보가 나타나는지 오프라인으로 확인한다. fixture 점수를 실제 LLM 성공률로 표현하지 않는다.
3. 일반 검색+function 대조군에도 같은 검색과 페이지·예산 정책을 적용한다. 기존 8개/633개 카탈로그·24질문·Muse 설정·새 대화·실행 순서 교대·입출력/채점 조건을 유지해 실제 비교한다. 실패를 포함해 저장하고 source 준비/모델/도구/HTTP 비용을 나눈다. 실제 MCP stdio도 확인한다.
4. 관련/전체 회귀와 실측 결과를 기록하고 사용자 작성자로 GitHub에 push한다.

원본 전체 응답·function 용도 설명·source schema는 그대로다. **2번의 select/반환 설명 개선, 3번의 별도 LLM holdout 확장은 진행하지 않는다.** 모델 단계 12회/120초와 원본/공개 응답 검증, 인증 context도 유지한다. 효과가 부족하면 검색 1번 안의 실제 원인만 기록하고 보정·검증 완화로 성공을 만들지 않는다.

진행: 위 범위의 구현·전체 회귀·실제 Muse/MCP 검증 완료. [실측과 한계](30-search-improvement-results.ko.md)에 결과를 기록했다. 2·3번은 미착수다.
