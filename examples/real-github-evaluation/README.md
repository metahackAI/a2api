# 실제 GitHub 조회 카탈로그 + Muse 비교

공식 고정 OpenAPI의 실제 GET만 사용한다. small=관련 API 8개, large=현재 converter가 지원하는 전체 GET 633개다. 합성 기능은 없다. 원문 revision/hash와 제외된 22개 진단은 report에 기록한다. 633개를 실제 모두 호출하는 평가는 아니다.

```bash
python -m pip install -e '.[mcp]'
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

[계획](../../docs/26-real-github-evaluation-plan.ko.md), [실측과 실패 원인](../../docs/27-real-github-evaluation-results.ko.md), [아직 구현하지 않은 개선 계획](../../docs/28-cost-improvement-plan.ko.md)을 참고한다. 전체 source 출력에 확장 annotation이 있어 기존 select가 거부되는 제한도 이번 비교에서 그대로 보존했다.
