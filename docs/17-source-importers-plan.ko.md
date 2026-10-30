# Java/Spring·Go·Rust 소스 importer와 HTTP 메서드 확장 계획

작성일: 2026-10-30. 이번 요청의 구현·검증 범위를 아래 순서로 고정한다.

## 목표

OpenAPI 없이 선택한 HTTP 소스에서 계약을 읽고, 기존 `convert` → `describe`/`invoke` → MCP에 연결한다. Java/Spring MVC, Go 표준 net/http ServeMux, Rust Axum/Serde의 명시적 route·handler·DTO를 첫 지원 대상으로 한다. 모든 언어/프레임워크/임의 동적 코드의 의미를 복원한다고 주장하지 않는다. 회사 소스·운영 서비스는 사용하지 않는다.

지원 HTTP 메서드는 GET, HEAD, POST, PUT, PATCH, DELETE다. 사용자 표현의 UPDATE는 PUT/PATCH로 해석하며 비표준 UPDATE 메서드는 생성하지 않는다. 새 직접 호출 경로에서 읽기/쓰기를 명시적으로 선택한다. 기존 선택적 review/build와 전체 Runtime의 읽기 정책은 보존한다.

## 순서 1: 설치와 소스 공통 계약

- Java JDK·Maven, Go, Rust/Cargo를 설치하고 버전을 기록한다. 사용자가 허용한 sudo는 설치에만 사용한다. sudo 인증이 불가능하면 공식 배포본을 `artifacts/toolchains/`에 설치하고 전역 환경을 바꾸지 않는다.
- 선택 의존성 `a2api[source]`로 Tree-sitter와 Java/Go/Rust grammar를 제공한다. 소스 분석에는 해당 언어 앱을 실행하거나 빌드하지 않는다. 런타임은 합성 예제 실행에만 필요하다.
- `src/a2api/importers/source.py`에 공통 소스 record·schema·AST 보조 기능을 둔다. record는 기존 Operation/input/output schema와 HTTP binding으로 직접 연결하며 OpenAPI 문서를 중간 생성하지 않는다.
- source 경로/파일/줄과 지원 불가 이유는 호스트 진단에 남긴다. 불명확한 타입·동적 route·중복 ID·구문 오류를 성공 계약으로 추측하지 않는다. 파싱 범위/크기를 제한하고 source 파일을 실행하지 않는다.
- 사용 경험은 `SpringSourceImporter/GoSourceImporter/RustSourceImporter.from_directory(...)` → 기존 `convert(... operations=..., deployment=...)`다. 별도 import/review/build 파일은 요구하지 않는다.

완료 기준: source 선택 의존성, 공통 record와 importer 진단, 기존 OpenAPI와의 입력 연결이 준비된다.

## 순서 2: Java/Spring importer

- `src/a2api/importers/spring.py`에서 AST로 class/method mapping과 명시적 HTTP 메서드, @PathVariable/@RequestParam/@RequestBody, DTO query binding을 읽는다.
- 기본 JSON scalar, 배열/List, 로컬 POJO/record·중첩 타입·상속·제네릭, ResponseEntity<T>를 지원한다. Jackson의 명시적 필드명/제외, 알려진 validation metadata와 default/optional 입력을 처리한다. 문서 예제 값을 실행 기본값으로 간주하지 않는다.
- 알려진 principal/servlet context 인자는 업무 schema에서 제외한다. 전역 advice, 외부 공통 클래스, custom serializer, 동적 Spring 등록/조건, 검증 그룹 등 지원하지 않는 의미는 진단한다. 소스 추출이 실제 Spring 활성 bean·권한·배포를 증명하지 않는다고 안내한다.
- 합성 Spring 앱에서 조회·생성·교체·부분 수정·삭제와 POST 조회를 제공한다. Controller·DTO에서 추출된 계약으로 실제 앱을 호출한다.

완료 기준: Java 소스 추출과 실제 Spring HTTP 실행, 미지원 구문/타입 진단이 검증된다.

## 순서 3: Go와 Rust importer

- `src/a2api/importers/golang.py`: net/http의 명시적 `HandleFunc("METHOD /path/{id}", handler)` 등록, named handler, PathValue·단순 query 읽기, JSON Decode/Encode와 정적으로 확인할 수 있는 DTO 타입을 읽는다. struct JSON tag, pointer/array/slice/로컬 struct를 지원한다. 런타임 route 조립·임의 함수 추론·Gin/Echo는 이번 범위가 아니다.
- `src/a2api/importers/rust.py`: Axum Router.route와 method router의 명시적 handler 연결, Path/Query/Json/State, Serde struct·Option·Vec·로컬 타입·rename metadata, Json 반환 및 확인 가능한 성공 상태를 읽는다. macro 생성 route·trait/custom serde·Actix 등은 이번 범위가 아니다.
- 각 언어의 합성 앱으로 Java와 같은 메서드·DTO 사용을 실행한다. 미지원 대상은 타입을 `{}`로 대체해 통과시키지 않는다.

완료 기준: 세 언어 모두 같은 종류의 메모리 계약을 생성하고 해당 언어 프로세스의 실제 HTTP를 호출한다.

## 순서 4: 여러 메서드의 직접 실행과 MCP

- `conversion.py`에서 OpenAPI와 세 source importer를 동일하게 연결한다. 기존 read 설정은 호환한다. `effect`는 read/write를 명시하며 PUT/PATCH/DELETE를 read로 활성화하지 않는다. POST 조회는 명시한 read 설정으로 허용한다. 선택되지 않은 endpoint는 실행 불가다.
- 모든 호출에서 입력 → 원본 응답 → 공개 출력 검증과 host credential/context 연결을 유지한다. 201 JSON·204 빈 결과 등 선언된 성공 상태만 허용한다. 자동 재시도나 write 성공 추측은 추가하지 않는다. 전송 후 timeout/중단은 기존 OUTCOME_UNKNOWN 규칙을 유지한다.
- MCP discover/describe의 effect와 invoke 설명·annotation을 실제 앱 효과에 맞춘다. 조회·설명 도구는 계속 읽기 도구다. 쓰기 앱을 붙인 invoke에 readOnly/idempotent라고 광고하지 않는다. 도구 세 개와 공통 schema 구조는 유지한다.
- native Python 함수의 새 쓰기 기능이나 기존 관리 Runtime의 쓰기 활성화까지 확장하지 않는다.

완료 기준: OpenAPI/세 소스 경로의 GET/POST/PUT/PATCH/DELETE·HEAD, 잘못된 effect, 잘못된 입력/응답, 삭제 후 조회 실패와 실제 MCP 쓰기 호출을 검증한다.

## 순서 5: 예제·회귀 검사·문서·반영

- 합성 예제는 `examples/source-http/{spring,go,rust}/`와 공통 검증/MCP host 파일에 둔다. 제3자 회사 소스는 복사하지 않는다. 동일한 작은 item CRUD와 POST 검색으로 메서드/효과를 비교한다.
- `tests/test_source_importers.py`, `tests/test_source_methods.py`에서 parser·진단·공통 실행·MCP의 결정적 검사를 한다. 기존 관련 테스트를 보완하며 언어 런타임이 필요한 실제 앱 검증은 명시적 예제 명령으로 분리한다.
- 세 언어를 실제 빌드·실행해 HTTP와 MCP stdio를 검증하고 설치 버전/실행 결과를 `docs/evidence/source-importers.json`에 기록한다. 빌드/캐시/툴체인/원시 실행 기록은 ignored artifacts나 언어 target에 둔다.
- `docs/18-source-importers.ko.md`와 README, 현재 계획 문서에 지금 지원하는 사용법·미지원 범위·설치/실행 명령을 적는다. 전체 기존 테스트를 실행하고 새 수정이 있을 때만 관련 검사를 반복한다.
- 사용자 Git 작성자로 커밋하고 정상 fast-forward로 GitHub에 반영한다. CI·배포·관리 플랫폼·별도 승인 단계를 추가하지 않는다.

완료 기준: 코드·문서·실제 세 런타임 실행 기록이 일치하며 지원하지 않은 부분을 지원한다고 표현하지 않는다.

## 범위 고정

위 다섯 순서 안의 필요한 작은 구현/수정만 진행한다. 범용 FFI, 임의 Java/Go/Rust 함수의 프로세스 내 실행, 전체 소스 의미 복원, 자동 권한 확정, 운영 API 테스트는 추가하지 않는다. 기존 코드 삭제나 enabled 변경으로 검증을 우회하지 않는다.

## 결과

| 순서 | 결과 | 근거 |
|---|---|---|
| 1. 설치·공통 계약 | 완료 | 공식 로컬 툴체인, source 선택 의존성, source.py의 AST/Operation/HTTP record. OpenAPI 중간 문서 없음 |
| 2. Java/Spring | 완료 | 합성 Boot 4.0.0/JDK 25 앱에서 소스 추출과 실제 HTTP·MCP stdio 검증 |
| 3. Go·Rust | 완료 | Go net/http와 Rust Axum/Serde의 각각 7개 route 추출·실제 바이너리 검증 |
| 4. 여러 메서드·MCP | 완료 | GET/HEAD/POST/PUT/PATCH/DELETE, 명시적 read/write, 201/204, 원본 검증·결과 불명·재시도 없음, MCP effect/annotation |
| 5. 검사·문서·반영 | 완료 | 전체 258개 테스트, 실제 세 언어 각 직접 8회+stdio 8회(총 48 HTTP 요청), editable extras/wheel 확인. Git 반영은 이 변경의 커밋/원격 상태로 확인 |

설치는 sudo 대화형 인증이 필요해 공식 배포본/Ubuntu 패키지의 프로젝트 로컬 설치로 완료했다. Java 배포 경로 403·로컬 truststore·C 링커 부재는 설치 범위 안에서 해결했고 TLS 검증/전역 환경은 유지했다. 단독 검사에서 관찰된 stdio 종료 EOF는 새 테스트의 sys.modules 전체 복원으로 동적 import 모듈/예외 타입이 분리된 것이 원인이었다. 격리 대상을 예제 모듈 한 개로 수정했다. SDK 예외를 숨기거나 SDK 코드를 변경하지 않았다.

[사용 문서](18-source-importers.ko.md), [실행/버전 증거](evidence/source-importers.json)에 확인한 범위와 한계를 기록했다. 회사 소스/운영 API, CI/배포/관리 플랫폼은 추가하지 않았다.
