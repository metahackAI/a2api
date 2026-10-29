# GitHub REST 전체 명세 샘플

## 바로 호출하는 에이전트 예제

기존 `convert`와 Python `capability`로 공개 저장소 조회·이슈/PR 한 페이지 조회를 연결했다. 필요한 필드만 반환하며, MCP에는 wrapper 두 개만 노출한다. 별도 review/build 파일이나 GitHub 토큰은 필요 없다.

```bash
python -m pip install -e ".[mcp]"
python examples/github-openapi/verify_agent.py
python examples/github-openapi/verify_agent.py --owner octocat --repo Hello-World --per-page 2
```

각 실행은 직접 호출 2회와 실제 MCP stdio 호출 2회를 검증한다. [사용 문서·입출력·호스트 설정·제약](../../docs/14-github-readonly-example.ko.md), [연결 코드](agent_app.py), [MCP 서버](mcp_server.py), [검증 client](verify_agent.py)를 참고한다. 아래 전체 import/benchmark는 별도의 기존 예제이며 이 실행의 선행 단계가 아니다.

## 전체 명세와 importer 검증 자료

공식 [github/rest-api-description](https://github.com/github/rest-api-description)의 bundled OpenAPI 3.0.3 명세를 사용한다. 827 paths, 1,254 operations, 압축 전 13,897,231 bytes다. revision과 SHA-256은 [source.json](source.json), upstream MIT 라이선스는 [LICENSE.upstream.md](LICENSE.upstream.md)에 있다. gzip 안의 JSON은 원본 그대로다.

- [import-report.json](import-report.json): 기본 GET의 처리·진단. IR 633개, 미선택 메서드 599개, GET 미지원 22개.
- [import-report-all-methods.json](import-report-all-methods.json): 전체 지원 메서드의 처리·진단. IR 1,228개, 미지원 26개. 모두 비활성 초안이다.
- [github.meta.get.json](github.meta.get.json), [HTTP binding](github.meta.get.http.json): 작은 생성 예시. 비활성 초안이다.
- [benchmark.json](benchmark.json): 전체 로드·변환·계약 검증·파일 생성의 단일 측정 기록.
- [benchmark-all-methods.json](benchmark-all-methods.json): 전체 지원 메서드를 선택한 측정 기록.
- [example-drift.json](example-drift.json): 공식 명세 예제 세 종류와 응답 스키마 사이의 불일치. 이슈 목록 예제는 적합하다.

저장소 루트에서 실행한다. 기존 출력 폴더를 덮어쓰지 않으므로 새 경로를 지정한다.

```bash
python -m pip install -e ".[openapi]"
python -m a2api import-openapi examples/github-openapi/api.github.com.json.gz \
  --namespace github --output artifacts/github-ir
python examples/github-openapi/verify_import.py --output artifacts/github-benchmark
python examples/github-openapi/verify_import.py --output artifacts/github-all-benchmark --all-methods
python examples/http-adapter/verify.py
# 외부 네트워크 사용; 로그인·토큰 불필요, 공개 GET 3회
python examples/github-openapi/verify_live.py
```

전체 생성 IR은 `artifacts/`에 두고 커밋하지 않는다. 기본 테스트는 이 폴더의 고정 명세로 오프라인 실행한다. 변환 규칙·실행 profile과의 차이·미지원 범위는 [importer 안내](../../docs/06-openapi-importer.ko.md)를 참고한다.
