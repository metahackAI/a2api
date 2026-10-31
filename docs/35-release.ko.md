# PyPI 배포 절차

작성일: 2026-10-31 · 기준: [완성 계획](33-completion-plan.ko.md) 7단계. 이 문서는 **배포 환경과 절차**만 정리한다. 실제 업로드는 사용자가 테스트 후 직접 실행한다.

## 준비된 환경

| 항목 | 위치/내용 |
|---|---|
| 패키지 메타데이터 | `pyproject.toml`: 이름 `a2api`, MIT, Python ≥ 3.11, 선택 의존성 `mcp`/`openapi`/`source` |
| 라이선스 | 저장소 루트 `LICENSE`(MIT), sdist/wheel에 포함 |
| PyPI 설명 | `PYPI.md`(영어). 저장소 README는 한국어로 유지 |
| 빌드 도구 | 저장소 `.venv`에 `build`, `twine` 설치 |
| 인증 | 사용자 홈 `~/.pypirc`(권한 600)의 `[pypi]` 항목에 API 토큰. 저장소에는 토큰을 두지 않는다 |
| 스크립트 | `scripts/release.sh` |

`~/.pypirc` 형식은 다음과 같다. 토큰을 바꾸려면 이 파일만 수정한다.

```ini
[distutils]
index-servers = pypi

[pypi]
username = __token__
password = pypi-...
```

PyPI API 토큰은 사용자 이름 대신 `__token__`을 사용한다. 계정 사용자 이름(haesooDev)은 토큰 발급·프로젝트 소유자 확인에 쓰인다. 첫 업로드에서 프로젝트 `a2api`가 생성되며, 토큰 범위가 "전체 계정"이어야 새 프로젝트를 만들 수 있다. 업로드 후에는 프로젝트 범위 토큰으로 바꾸는 것을 권장한다.

## 배포 전 확인

```bash
cd ~/a2api            # 저장소 루트
scripts/release.sh    # 정리 → 전체 테스트 → sdist/wheel 빌드 → twine check → 새 venv에 wheel 설치 후 기본 호출
```

스크립트는 업로드하지 않는다. 마지막 줄에 `built and checked; not uploaded`가 나오면 `dist/`의 두 파일이 배포 후보다. 시간이 걸리는 전체 테스트를 이미 실행했다면 `--skip-tests`를 쓸 수 있다.

선택 사항: TestPyPI에서 먼저 확인하려면 `~/.pypirc`에 `[testpypi]`(repository = https://test.pypi.org/legacy/, TestPyPI 토큰)를 추가하고 `scripts/release.sh --upload --repository testpypi`를 실행한다. 기존 PyPI 토큰은 TestPyPI에서 쓸 수 없다.

## 배포

```bash
scripts/release.sh --upload           # 모든 확인 후 PyPI 업로드
pip install a2api                     # 다른 환경에서 확인
```

같은 버전은 PyPI에 다시 올릴 수 없다. 수정이 필요하면 `pyproject.toml`의 `version`을 올리고 다시 실행한다. 원격 저장소 push와 태그(`v1.0.0` 등)는 이 스크립트가 하지 않는다.

## 포함 범위

wheel에는 `src/a2api` 패키지와 `schemas/*.json`, `sample/*.json`만 들어간다. `examples/`의 벤치마크·생성기, 문서, 평가 원문(`artifacts/`)은 저장소에만 있다. 선택 의존성 `source`는 tree-sitter 0.25 계열로 고정한다(0.26.0의 충돌 때문, [33 문서](33-completion-plan.ko.md) 변경 기록).
