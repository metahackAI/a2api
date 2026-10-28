# GitHub REST 전체 명세 샘플

공식 [github/rest-api-description](https://github.com/github/rest-api-description)의 bundled OpenAPI 3.0.3 명세를 사용한다. 827 paths, 1,254 operations, 압축 전 13,897,231 bytes다. revision과 SHA-256은 [source.json](source.json), upstream MIT 라이선스는 [LICENSE.upstream.md](LICENSE.upstream.md)에 있다. gzip 안의 JSON은 원본 그대로다.

- [import-report.json](import-report.json): 전체 operation별 처리·진단. IR 617개, 쓰기 메서드 제외 599개, GET 미지원 38개.
- [github.meta.get.json](github.meta.get.json), [HTTP binding](github.meta.get.http.json): 작은 생성 예시. 비활성 초안이다.
- [benchmark.json](benchmark.json): 전체 로드·변환·계약 검증·파일 생성의 단일 측정 기록.
- [example-drift.json](example-drift.json): 공식 명세 예제 세 종류와 응답 스키마 사이의 불일치. 이슈 목록 예제는 적합하다.

저장소 루트에서 실행한다. 기존 출력 폴더를 덮어쓰지 않으므로 새 경로를 지정한다.

```bash
python -m pip install -e ".[openapi]"
python -m a2api import-openapi examples/github-openapi/api.github.com.json.gz \
  --namespace github --output artifacts/github-ir
python examples/github-openapi/verify_import.py --output artifacts/github-benchmark
# 외부 네트워크 사용; 로그인·토큰 불필요, 공개 GET 3회
python examples/github-openapi/verify_live.py
```

전체 생성 IR은 `artifacts/`에 두고 커밋하지 않는다. 기본 테스트는 이 폴더의 고정 명세로 오프라인 실행한다. 변환 규칙·실행 profile과의 차이·미지원 범위는 [importer 안내](../../docs/06-openapi-importer.ko.md)를 참고한다.
