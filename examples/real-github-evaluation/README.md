# 실제 GitHub 조회 카탈로그 + Muse 비교

공식 고정 OpenAPI의 실제 GET만 사용한다. small=관련 API 8개, large=현재 converter가 지원하는 전체 GET 633개다. 합성 기능은 없다. 원문 revision/hash와 제외된 22개 진단은 report에 기록한다. 633개를 실제 모두 호출하는 평가는 아니다.

현재는 검색 `field-search/1`을 유지하고, [28 문서](../../docs/28-cost-improvement-plan.ko.md)의 2·3번을 [고정 범위](../../docs/31-result-delivery-and-holdout-plan.ko.md)로 수행했다. `a2api-tools/0.3`은 선택한 함수에 짧은 반환 설명을 붙이고 repo/commit에는 명시적 select를 사용한다. ordinary와 a2api의 projection·설명·검색·검증·예산은 같다. [새 결과](../../docs/32-result-delivery-and-holdout-results.ko.md)는 core 24/24와 holdout 9/12 엄격 완료를 구분한다. [검색만 개선한 결과](../../docs/30-search-improvement-results.ko.md)는 이전 기록으로 보존한다.

```bash
python -m pip install -e '.[mcp]'
# 기존 실패 질의 순위와 고정한 별도 10질의의 오프라인 검색 검사 (모델/HTTP 호출 없음)
python examples/real-github-evaluation/search_check.py \
  --output artifacts/search-improvement/my-offline.json
# 자신의 Chat Completions endpoint/model을 환경 변수로 설정한다. docs/22 참고.
python examples/real-github-evaluation/evaluate.py --github-auth gh \
  --suite core --repetitions 2 --stdio --output artifacts/real-github-evaluation/my-run.json

# 별도 고정한 6요청 × 두 방식. 633개에서 1반복만 실행한다.
python examples/real-github-evaluation/evaluate.py --github-auth gh \
  --suite holdout --repetitions 1 --output artifacts/real-github-evaluation/my-holdout.json

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

holdout은 `holdout-cases.json`의 release/fork/stargazer/기본 브랜치→commit status 6요청이다. 검색 개발 중 사용한 10개 오프라인 질의와 구별한다. 질문과 채점기 hash를 실행 전에 기록하고 성공/실패에 따라 교체하지 않는다. 별도 사전 검사 7회의 HTTP도 report에 포함한다. review/summarize는 위와 같은 명령에 holdout 원문 경로를 넣어 사용한다. 원본 응답 전체를 검증한 뒤 공개 필드를 선택하므로 GitHub에서 받는 네트워크 바이트가 자동으로 줄지는 않는다.

holdout은 사전 검사 실패도 기록하고 고정 질문 전체를 실행한다. 질문 또는 사전 검사가 실패하면 원문을 보존하고 종료 코드 1을 반환한다. 이번 stargazer 요청은 현재 접근 제한으로 실패했으며, 해당 계정이 타인 저장소의 모든 목록 조회 권한을 갖는다고 가정하지 않는다. 첫 중단 기록과 별도 직접 진단까지 [32 문서](../../docs/32-result-delivery-and-holdout-results.ko.md)에 남겼다. credential/질문/채점/시간 제한을 바꿔 성공으로 만들지 않는다.

모델의 실제 API 조회는 사용자 조건·데이터 흐름·최종 JSON 값으로 판정한다. 브랜치 값에서 만든 `heads/<branch>`, `refs/heads/<branch>`도 허용한다. 처음 pilot의 좁은 판정 오류는 원문을 보존하고 별도 review로 수정했다. 모델 인자는 고치지 않는다. 실행이 단계 제한 등으로 실패하면 raw report를 남기고 명령은 1로 끝난다. 이 종료 코드를 무시해 성공으로 보고하지 않는다.

[원 평가 계획](../../docs/26-real-github-evaluation-plan.ko.md), [최초 실측과 실패 원인](../../docs/27-real-github-evaluation-results.ko.md), [검색 개선 후 실측](../../docs/30-search-improvement-results.ko.md)을 구분한다. review는 예전 report의 substring 순위와 원문에 기록한 projection을 재현하며 새 report에는 검색 revision·질문/채점기 hash 일치를 요구한다. 실패를 지우기 위한 임의 재실행이나 검증 완화는 하지 않는다.
