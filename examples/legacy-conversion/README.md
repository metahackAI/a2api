# 레거시 API 전환 예제

[레거시 API 전환 가이드](../../docs/36-legacy-conversion-guide.ko.md)의 코드를 그대로 실행하는 예제다. 벤치마크가 생성한 API(OpenAPI + Spring/Go/Rust 소스)를 "기존 서비스"로 사용한다.

```bash
python -m pip install -e ".[mcp,openapi,source]"

# 경로 A: OpenAPI와 코드가 모두 있을 때 — 명세 진단, 코드와 route 비교, 선택 변환, 직접/모델 호출
python examples/legacy-conversion/openapi_and_code.py --language go        # spring | go | rust

# 경로 B-1: 코드만 있는 Spring / Go / Rust — 소스에서 route·DTO 읽기, 노출 표, 변환, 호출
python examples/legacy-conversion/code_only.py --language spring

# 경로 B-2: HTTP 없이 Python 코드만 있을 때 — 기존 서비스를 감싼 read/write(async) 함수 등록
python examples/legacy-conversion/python_functions.py
```

A·B-1은 해당 언어 툴체인(JDK 25 + Maven, Go 1.22+, Rust/Cargo)으로 생성된 서버를 빌드해 임시 포트에서 실행한다. 생성물이 없으면 `examples/benchmark/generate.py`를 자동으로 호출한다. B-2는 외부 의존성 없이 실행된다.
