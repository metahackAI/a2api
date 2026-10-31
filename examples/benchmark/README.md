# 4개 언어 벤치마크: a2api vs 일반 API 명세 전달

같은 상거래 API(고객·주문·배송·지원 티켓·상담원 + 방해 리소스)를 **Python·Spring Boot·Go net/http·Rust Axum**으로 생성하고, 실제 모델에서 세 가지 전달 방식을 비교한다. 범위와 판정 기준은 [완성 계획](../../docs/33-completion-plan.ko.md), 결과는 [완성 평가 결과](../../docs/34-completion-results.ko.md)에 있다.

| 규모 | 리소스 | 업무 operation |
|---|---:|---:|
| small | 5 (핵심) | 19 |
| medium | 11 | 55 |
| large | 41 | 235 |

| 모드 | 모델이 받는 정보 | 실행 |
|---|---|---|
| `spec-tools` | OpenAPI의 모든 operation을 function tool로(일반적인 OpenAPI→function 변환), 원본 응답 전체 | 언어 서버 HTTP |
| `spec-prompt` | system prompt에 OpenAPI 전체 + 범용 `http_request` 도구, 원본 응답 전체 | 언어 서버 HTTP |
| `a2api` | `ToolSession.auto(질문)`: 작은 카탈로그는 전체 함수, 큰 카탈로그는 사전 검색 후보 + `a2api_search` | Spring/Go/Rust는 소스 importer → `convert`, Python은 `@capability` |

## 실행

```bash
python -m pip install -e ".[mcp,source]"
# JDK 25 + Maven, Go 1.22+, Rust/Cargo가 필요하다(예: sudo apt-get install openjdk-25-jdk-headless maven golang-go rustc cargo build-essential)

python examples/benchmark/generate.py                 # artifacts/benchmark/generated/<scale>/{openapi.json,spring,go,rust,python}
python examples/benchmark/verify.py                   # 4개 구현의 HTTP 동등성 + a2api 직접/MCP 호출 확인
python examples/benchmark/evaluate.py --split dev --scales small --languages go \
    --output artifacts/benchmark/runs/my-dev.jsonl    # 기본 모델: nvidia/Muse-Glimmer-30B-NVFP4 @ qwen-api-xgen
python examples/benchmark/summarize.py artifacts/benchmark/runs/my-dev.jsonl --by language
```

모델 endpoint는 `--base-url`/`--model` 또는 `A2API_MODEL_BASE_URL`/`A2API_MODEL`, 필요한 경우 `A2API_MODEL_API_KEY`로 바꾼다. 출력 파일은 덮어쓰지 않는다. 각 run은 서버 상태를 reset하고, 실행 전/후 상태와 최종 JSON 답변·정규화한 업무 호출로 채점한다. 실패·provider 오류도 그대로 기록한다. run 시작 전 짧은 모델 응답 확인만 하고, 시작한 run은 재시도하지 않는다.

## 파일

- `domain.py`: 리소스·필드·seed·요약·규모 정의(모든 생성물의 원본)
- `generate.py`: OpenAPI 3.1 + Spring/Go/Rust 소스 + Python 모듈 생성
- `pystore.py`: Python 구현의 저장소(Python capability와 Python HTTP 서버가 공유)
- `servers.py`: 언어 서버 빌드·실행, Python HTTP 서버
- `application.py`: a2api 호스트 설정(노출 operation·effect·공개 필드·요약·검색어)
- `modes.py`: 세 모드 실행기, `evaluate.py`: 모델 루프와 기록, `tasks.py`: dev/holdout 작업과 채점, `summarize.py`: 집계
- `verify.py`, `mcp_server.py`: 구현 동등성·MCP stdio 확인

이 API는 합성 데이터와 합성 업무이며, 결과는 이 모델·작업에서 관찰한 범위다. 모든 실제 API나 모델에서 같은 효과를 보장하지 않는다.
