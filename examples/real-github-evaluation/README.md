# 실제 GitHub 조회 카탈로그 + Muse 비교

공식 고정 OpenAPI의 실제 GET만 사용한다. small=관련 API 8개, large=현재 converter가 지원하는 전체 GET 633개다. 합성 기능은 없다. 원문 revision/hash와 제외된 22개 진단은 report에 기록한다. 633개를 실제 모두 호출하는 평가는 아니다.

현재는 [28 문서](../../docs/28-cost-improvement-plan.ko.md)의 **1번 검색만 개선**한 `field-search/1`과 `a2api-tools/0.2`를 사용한다. ordinary와 a2api에 같은 정확 ID/field 순위·조건부 다음 페이지를 적용한다. 결과 projection·business function의 반환 설명은 변경하지 않았다. [재검증 결과](../../docs/30-search-improvement-results.ko.md)에서 두 방식 모두 12/12를 완료했으며, 대규모의 토큰 합계는 같았다.

```bash
python -m pip install -e '.[mcp]'
# 기존 실패 질의 순위와 고정한 별도 10질의의 오프라인 검색 검사 (모델/HTTP 호출 없음)
python examples/real-github-evaluation/search_check.py \
  --output artifacts/search-improvement/my-offline.json
# 자신의 Chat Completions endpoint/model을 환경 변수로 설정한다. docs/22 참고.
python examples/real-github-evaluation/evaluate.py --github-auth gh \
  --repetitions 2 --stdio --output artifacts/real-github-evaluation/my-run.json

# 실제 호출/모델을 재실행하지 않는 오프라인 값·의존 관계·순위 검사
python examples/real-github-evaluation/review.py \
  artifacts/real-github-evaluation/my-run.json \
  --output artifacts/real-github-evaluation/my-review.json
python examples/real-github-evaluation/summarize.py \
  artifacts/real-github-evaluation/my-run.json \
  --review artifacts/real-github-evaluation/my-review.json \
  --output artifacts/real-github-evaluation/my-summary.json
```

`--github-auth gh`는 이미 로그인된 CLI 인증을 호스트 메모리에서만 사용한다. 모델/파일/로그에는 보내지 않는다. 중계기는 지정한 psf/requests, octocat/Hello-World 하위 GET만 전달하고 redirect/cache/replay를 사용하지 않는다. `--github-auth none --repetitions 1 --http-limit 30`도 가능하며 실제 quota가 충분해야 한다. 기본 100회 예산은 인증된 비교용이다. 같은 output 파일은 덮어쓰지 않는다.

24질문은 크기 2 × 모드 2 × 단순 저장소/페이지 제약/연쇄 요청 3 × 반복 2다. 두 크기 모두 사전 API 지식 없이 시작한다. 각 질문은 새 대화·세션이다. 같은 source·검색·function schema·16KB 도구 예산·입출력 검증을 사용한다. ordinary도 같은 전환 앱을 호출하므로 독립 SDK/개발 공수 비교가 아니다. 양쪽 모두 in-process HTTP이며 MCP stdio는 별도 smoke다.

모델의 실제 API 조회는 사용자 조건·데이터 흐름·최종 JSON 값으로 판정한다. 브랜치 값에서 만든 `heads/<branch>`, `refs/heads/<branch>`도 허용한다. 처음 pilot의 좁은 판정 오류는 원문을 보존하고 별도 review로 수정했다. 모델 인자는 고치지 않는다. 실행이 단계 제한 등으로 실패하면 raw report를 남기고 명령은 1로 끝난다. 이 종료 코드를 무시해 성공으로 보고하지 않는다.

[원 평가 계획](../../docs/26-real-github-evaluation-plan.ko.md), [최초 실측과 실패 원인](../../docs/27-real-github-evaluation-results.ko.md), [검색 개선 후 실측](../../docs/30-search-improvement-results.ko.md)을 구분한다. review는 예전 report의 substring 순위도 그대로 재현하며 새 report에는 기록된 검색 revision을 요구한다. 전체 source 출력의 확장 annotation으로 기존 select가 거부되는 제한은 그대로 보존했다. 2번 전달 정보와 3번 별도 실제 LLM holdout 확장은 진행하지 않았다.
