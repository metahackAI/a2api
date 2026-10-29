# OpenAPI 변경 영향 diff와 증분 재생성

구현일: 2026-10-29. operation별 의존성 fingerprint를 비교하고, 영향을 받는 업무 capability만 `requires_review`로 표시한다. 기존 검토 JSON을 수정하거나 새 원본을 자동 승인하지 않는다.

선택적인 변경 관리 기능의 구현 안내다. [현재 제품 방향](00-product-direction.ko.md)에서는 간편한 전환·첫 호출의 선행 절차로 요구하지 않는다.

## 빠른 검증

```bash
python -m pip install -e ".[mcp]"
python -m a2api incremental-demo
```

샘플은 같은 주문·배송 API를 사용하는 두 capability를 검토한 뒤 배송 status enum을 변경한다.

| capability | source 의존성 | 배송 schema 변경 후 |
|---|---|---|
| `order.summary` | getOrder | 기존 계약 유지, MCP 조회 가능 |
| `order.shipping_status` | getOrder + getShipment | 재검토 필요, MCP에서 숨김 |

getShipment 초안 한 개를 다시 변환하고 getOrder는 재사용한다. 실제 MCP stdio 클라이언트가 `order.summary`를 조회·실행해 HTTP 호출 한 번으로 주문 상태를 받으며, 재검토 중인 배송 capability의 describe/invoke는 거부된다. 원본 명세·검토 파일·기존 빌드는 그대로 남는다. 외부 API 요청은 없다.

## CLI

독립적인 diff:

```bash
python -m a2api diff-openapi --before old.openapi.json --after new.openapi.json
python -m a2api diff-openapi --before old.openapi.json --after new.openapi.json \
  --review review.json
```

`--review`를 주면 source operation과 업무 capability를 연결한 영향 목록도 출력한다. before 문서의 SHA-256은 기존 검토 설정과 일치해야 한다. namespace는 검토 설정에서 가져오며 `--namespace`를 명시할 수도 있다. `--methods`의 기본값은 GET이다.

주문·배송 예제를 단계별로 실행하려면 다음 소스를 사용한다.

- [공유 참조를 포함한 OpenAPI](../src/a2api/sample/order-shipping.incremental.openapi.json)
- [두 capability의 검토 설정](../src/a2api/sample/order-shipping.incremental.review.json)

```bash
python -m a2api import-openapi src/a2api/sample/order-shipping.incremental.openapi.json \
  --namespace legacy_orders --output artifacts/incremental-imports
python -m a2api build --imports artifacts/incremental-imports \
  --review src/a2api/sample/order-shipping.incremental.review.json \
  --output artifacts/incremental-baseline
# new.openapi.json에는 수정한 명세를 별도로 저장한다.
python -m a2api regenerate --previous artifacts/incremental-baseline \
  --source new.openapi.json --output artifacts/incremental-updated
python -m a2api mcp --build artifacts/incremental-updated
```

출력 폴더는 새 경로를 사용한다. `--fail-on-review`를 추가하면 산출물을 기록한 뒤 재검토 capability가 있을 때 exit 1을 반환하므로 CI에서 사용할 수 있다. 기본 실행은 부분적으로 유효한 산출물을 생성하고 exit 0을 반환한다.

## 의존성 추적 범위

각 operation의 fingerprint는 다음을 포함한다.

- operation 본문 전체와 operationId/정규화 ID 충돌 정보
- 실제 적용되는 path/operation parameter와 내부 참조
- operation/path/root의 우선순위를 적용한 servers, operation/root security
- 사용하는 security scheme 정의
- schema·parameter·response·requestBody 등 내부 `$ref`의 전이적 참조
- OpenAPI 버전과 JSON Schema dialect

operation이 override한 path parameter나 명시적으로 override한 security/servers는 이전 상위 값을 의존성으로 취급하지 않는다. schema의 속성 이름 `$ref`, example/default의 리터럴 JSON은 참조로 실행하지 않는다. 참조 역할을 component 이름으로 추측하지 않으며, 순환 참조는 방문 집합으로 종료한다. 외부 URL·파일을 가져오지 않는다.

JSON object의 키 순서·공백, root info의 title/description/version, 사용하지 않는 tag 정의와 참조하지 않는 schema 변경은 기존 capability의 재검토 사유가 아니다. 변경·추가된 component는 diff에 표시할 수 있어도 해당 operation의 의존성에 없으면 전파하지 않는다.

이는 정적 참조 단위의 보수적인 영향 분석이다. 참조하는 schema의 일부 필드만 변경되어도 그 schema를 사용하는 operation과 capability를 재검토 대상으로 삼는다. 변경의 호환성이나 실제 업무 의미를 자동 승인하지 않는다. 리뷰한 projection의 필드 수준으로 영향 범위를 더 줄이는 기능은 이번 범위에 포함하지 않는다. 참조된 PathItem 전체의 변경도 그 참조를 사용하는 operation의 영향으로 처리한다.

## 재생성과 검토 상태

1. 이전 승인 빌드와 의존성 기록을 검증한다.
2. 새 문서에서 index를 만들고 변경·추가·삭제 operation을 식별한다.
3. 변경·추가된 선택 메서드만 importer의 schema 변환에 전달한다. 이전 빌드 로드·검증은 별도로 수행한다.
4. 안정적인 source IR과 업무 계약의 바이트를 재사용한다. 중복 source 파일 대신 승인 스냅샷을 참조할 수 있다.
5. 영향을 받는 capability를 `enabled=false`, `lifecycle=draft`, provenance `reviewState=unreviewed`로 만든다.
6. 기존 검토 설정은 그대로 복사하고 `review-status.json`에 별도 재검토 상태와 원인을 기록한다.

새 operation은 비활성 source 초안으로만 생성되며 업무 capability로 자동 등록하지 않는다. 제거·이름 변경·ID 충돌·참조 제거·새로운 미지원 schema도 관련 capability의 승인을 유지하지 못한다. 변환에 실패한 초안은 diagnostics를 남기고 격리한다.

한 번 재검토 대상으로 표시되면 후속 문서가 원본으로 돌아가도 자동 재승인하지 않는다. 이전 변경 기록을 함께 읽어 누적 재검토 상태를 계산한다. [선택 검토·재승인 CLI](10-selective-reapproval.ko.md)로 해당 capability를 명시적으로 승인하거나 새 기준 빌드를 만들기 전까지 이 상태를 유지한다. 새 기준을 만들 때에는 최신 원본을 import하고, 보존한 검토 설정의 업무 정의를 사용하면서 변경된 부분을 검토하고 원본·operation pin과 검토 기록을 갱신한다. 증분 명령은 이를 대신 수행하지 않는다.

## 산출물과 로드

새 import는 `source.snapshot.json`과 `dependencies.json`을 포함한다. 새 기준 빌드는 `a2api-build/0.2`이며 원본 JSON 스냅샷을 포함해 다음 변경과 비교할 수 있다.

```text
incremental-updated/
  build.json
  review.json                   # 기존 검토 설정 유지
  source.snapshot.json          # 현재 원본 JSON과 출처
  dependencies.json
  diff.json
  review-status.json
  history/0000.json ...          # 승인 시점부터의 의존성 기록
  approved/                     # 최초 승인 빌드, 중첩 복제하지 않음
  contracts/                    # 재사용 또는 비활성화한 업무 계약
  drafts/report.json            # 재사용/새 변환/미지원 operation
  drafts/contracts/             # 필요한 새 source 초안만 저장
```

현재 원본과 승인 원본의 해시는 별도로 기록한다. 무관한 원본 변경에서 실행 계약의 provenance를 새 승인처럼 바꾸지 않으며, 기존 reviewSha256과 승인 sourceSha256을 유지한다. 따라서 무관한 변경은 catalogVersion도 유지할 수 있다. 실제 영향으로 capability가 비활성화되면 catalogVersion이 바뀌므로 에이전트는 다시 discover한다.

`load_build`는 증분 형식 `a2api-incremental-build/0.1`도 읽는다. 승인 기준·현재 원본·의존성 history에서 상태와 계약을 다시 계산하고 metadata와 모든 산출물 바이트를 확인한다. 상태 파일의 플래그만 바꾸어 capability를 활성화할 수 없다. 파일 경로는 묶음 밖으로 나갈 수 없다. 이 일관성 검사는 서명된 승인이나 설정 파일 접근 제어를 대신하지 않는다.

스냅샷에는 명세 전체의 JSON이 들어간다. history에는 원본 전체를 반복 저장하지 않고 의존성 index를 저장한다. 현재 버전은 기준당 최대 64회 업데이트를 지원하며 이후 새 승인 기준을 만든다. deployment origin·실제 credential은 계속 호스트에서 주입한다.

스냅샷이 없는 기존 `a2api-build/0.1`은 계속 로드할 수 있다. 첫 증분 업데이트에만 원래 검토한 문서를 제공한다.

```bash
python -m a2api regenerate --previous old-build --source new.openapi.json \
  --baseline-source originally-reviewed.openapi.json --output updated-build
```

baseline 문서의 바이트 해시와 재생성한 source IR이 기존 검토 pin에 일치해야 한다. 기존 검토나 빌드를 수정하지 않고 새 묶음 안에서 의존성 기준을 구성한다.

## 검증

주문·배송 두 capability로 직접 operation 변경, 공유/전이 schema 변경, 삭제·추가·미지원 참조, 무관한 변경, 검토 유지, 정확한 원본 복원 후에도 재검토 유지, 기존 버전 이행을 확인한다. importer 호출을 계측해 배송만 바뀌었을 때 getShipment 한 개만 재변환하는지 검사한다. MCP stdio에서 주문 조회는 계속 실행하고 배송 조회는 숨기는지도 검증한다. 공식 GitHub 명세 전체 1,254개 operation에서도 metadata-only 변경이 operation 변경으로 전파되지 않는지 확인한다.

전체 회귀 테스트 164개를 ResourceWarning도 오류로 처리해 통과했다. 참조 한도에 도달하는 그래프도 서로 다른 Python hash seed에서 같은 fingerprint를 생성하는지 확인했다. 소스 트리 밖으로 추출한 wheel에서 Python 3.14의 import/build/regenerate와 Python 3.12의 MCP `incremental-demo`를 실행해 새 모듈과 샘플의 패키징도 검증했다.
