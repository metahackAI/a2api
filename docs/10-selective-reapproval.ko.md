# Capability 선택 검토와 재승인

구현일: 2026-10-29. 증분 빌드의 `requires_review` capability만 골라 검토안을 만들고, 검증한 설정으로 새 승인 빌드를 만든다. 기존 빌드·원본 `review.json`·선택하지 않은 계약은 수정하지 않는다.

선택적인 계약 관리 기능의 구현 안내다. [현재 제품 방향](00-product-direction.ko.md)에서는 이 승인 절차를 간편 전환·첫 호출의 필수 단계로 확대하지 않는다.

## 주문·배송 실행

```bash
python -m pip install -e ".[mcp]"
python -m a2api reapproval-demo
```

배송 status enum 변경 → 배송만 재검토 → 배송 검토안 작성 → 명시적 재승인 → 실제 MCP stdio `discover/describe/invoke`를 실행한다. 주문 기본 조회 계약은 동일한 바이트를 유지하며, 재승인한 배송 조회는 주문 API 한 번과 배송 API 두 번으로 완료된다. 기존 원본 검토 설정은 그대로 남는다. 샘플 승인자 표시는 fixture 검증용이며 실제 업무 검토를 뜻하지 않는다.

## CLI

먼저 [증분 재생성](09-source-diff-and-regeneration.ko.md)으로 만든 빌드가 필요하다.

```bash
python -m a2api prepare-review \
  --build artifacts/incremental-updated \
  --capability order.shipping_status@0.1.0 \
  --output artifacts/shipping.review.json
```

검토안은 `a2api-capability-review/0.1` JSON이다.

- `target`: 전체 빌드 내용의 해시, 현재 원본 해시, generation. 같은 generation에서 다른 capability를 승인한 빌드도 구별한다.
- `reviews[].context`: 선택한 ID·버전, 변경 영향, 이전 계약, 각 operation의 이전/현재 원본 IR과 HTTP binding. 검토 근거이므로 수정하지 않는다.
- `reviews[].settings`: 수정 가능한 기존 review 형식의 부분 설정. 선택한 capability 하나와 사용하는 operation만 포함한다. 업무 정책·projection·의미 타입·표시 설정을 기존 검토에서 가져오고 원본 pin은 현재 명세에 고정한다. `review.state`는 `unreviewed`다.

이 파일에서 변경된 원본과 기존 업무 계약을 검토하고 필요한 `settings`를 편집한다. 예를 들어 원본에 필수 query parameter가 추가되면 operation 입력 projection과 capability 입력/step 매핑을 함께 보완한다. 잘못된 projection, 누락한 필수 입력, 의미 타입 불일치 등은 계약 빌더가 거부한다.

배송 예제는 기존 capability 출력 enum에 새 상태 `returned`를 명시적으로 추가한다. 검토안의 `reviews[0].settings.capabilities[0].outputSchema.properties.shipments.items.properties.status.enum`을 수정한다. 원본 enum을 자동으로 업무 계약에 복사하지 않으므로, 기존 출력 제약을 유지하면 해당 제약 밖의 실제 응답은 계속 `SCHEMA_MISMATCH`로 거부된다.

```bash
python -m a2api approve-review \
  --build artifacts/incremental-updated \
  --review artifacts/shipping.review.json \
  --reviewed-by haesookim \
  --output artifacts/shipping-approved
python -m a2api mcp --build artifacts/shipping-approved
```

`approve-review`는 명시한 검토자와 현재 UTC 시각을 승인 기록에 넣는다. 재현 가능한 실행에는 `--reviewed-at 2026-10-29T03:00:00Z`를 지정할 수 있다. 검토안 자체와 입력 빌드는 변경하지 않는다. 출력 파일·폴더는 항상 새 경로를 사용한다.

`--capability`를 반복하면 여러 재검토 capability의 검토안을 만들 수 있다. 제안한 검토안의 모든 선택 항목이 통과해야 출력 빌드를 기록한다. 일부만 승인하려면 처음부터 해당 항목만 선택한다. 이미 다른 승인이 이루어졌거나 원본이 갱신되었다면 이전 검토안은 `STALE_REVIEW`로 거부되므로 현재 빌드에서 다시 준비한다.

## 선택 범위와 보존

| 대상 | 재승인 후 |
|---|---|
| 선택한 재검토 capability | 현재 명세로 다시 컴파일, reviewed/enabled, 새 검토자·시각·원본 pin |
| 선택하지 않은 재검토 capability | 비활성 계약과 누적 재검토 사유 유지 |
| 영향 없는 capability | manifest 바이트·이전 검토 provenance 그대로 유지 |
| 루트 `review.json`과 `approved/` | 최초 검토 설정과 기준 빌드 그대로 유지 |
| 이전에 편집·승인한 설정 | 승인 이력에 저장, 다음 검토안의 시작 설정으로 사용 |

선택한 ID·버전, source namespace·해시·operation pin, operation 구성원, sample/source 검토 범위는 검토안에서 바꿀 수 없다. capability를 추가하거나 source operation을 재연결하는 작업은 전체 import/build 흐름에서 수행한다. 제거·이름 변경·미지원 operation, 해석되지 않는 의존성은 재승인할 수 없다.

같은 source operation을 여러 capability가 사용해도 승인 단위는 capability다. 선택한 계약의 실행 참조를 capability별로 구분해, projection을 수정해도 다른 계약의 배포 매핑을 덮어쓰지 않는다. 원본 HTTP 계약이 충돌하는 활성 binding은 거부한다.

## 승인 이력과 후속 변경

선택 승인이 있는 증분 빌드는 `a2api-incremental-build/0.2`다. 기존 `/0.1` 증분 빌드도 계속 읽는다.

```text
shipping-approved/
  review.json                  # 최초 검토 설정
  approved/                    # 최초 기준 빌드
  contracts/                   # 현재 계약: 보존/재검토/재승인
  review-status.json
  source.snapshot.json
  dependencies.json
  history/0000.json ...
  approvals/index.json         # capability별 승인 generation
  approvals/0000/              # 그 시점의 부분 검토 설정·source·컴파일 결과
    review.json
    build.json
    imports/...
    contracts/...
```

`load_build`는 부분 승인 빌드도 원본과 검토 설정에서 다시 컴파일하고, 승인 generation의 의존성 index가 source history에 일치하는지와 모든 산출물 바이트를 확인한다. 승인 플래그만 수정해 활성화할 수 없다. 기록은 호스트 파일을 신뢰하는 일관성 검증이며 서명된 승인이나 외부 사용자 인증을 제공하지 않는다.

각 capability의 마지막 승인 generation 이후 변경만 다시 누적한다. 무관한 후속 변경은 새 승인 계약을 그대로 유지한다. 승인 뒤 해당 operation/공유 참조가 다시 바뀌면 그 capability가 다시 재검토 대상이 된다. 승인 전의 미선택 항목은 계속 재검토 상태다. 상태는 자동으로 승인되지 않으며 원본을 되돌리는 것도 변경으로 취급한다.

재승인 시 `catalogVersion`이 바뀐다. 에이전트는 새 빌드를 연결한 MCP 서버에서 다시 discover/describe한 뒤 invoke한다. 이전 catalogVersion으로 실행하면 `CONTRACT_DRIFT`다. CLI는 새 빌드 산출물을 생성하며 이미 실행 중인 서버를 자동 교체하지 않는다.

현재 기준당 source 업데이트 64회, capability 부분 승인 256건까지 보관한다. 승인별 source 스냅샷을 포함하므로 큰 명세에서는 저장 용량을 고려해야 한다. 이후 새 기준 빌드를 만드는 방식과 generation별 스냅샷 중복 제거는 후속 확장 대상이다.

## 검증

CLI로 OpenAPI diff → regenerate → prepare-review → approve-review를 실행한 뒤 공식 MCP stdio 클라이언트로 배송 조회 복원을 확인한다. 승인 전에는 주문 조회만 보이고, 승인 후에는 두 capability가 보인다. 배송 호출은 HTTP 3회, 보존된 주문 호출은 HTTP 1회다. 오래된 카탈로그 실행 거부, 부분/다중 승인, 실패 시 출력 미생성, 검토 설정과 계약 보존, 후속 변경 영향, 공유 operation의 projection 격리, 재로드와 변조 감지도 검증한다.

전체 회귀 테스트 184개를 ResourceWarning도 오류로 처리해 통과했다. 소스 폴더 밖에 추출한 wheel에서 Python 3.14의 선택 검토·재승인 CLI와 Python 3.12의 MCP `reapproval-demo`를 실행해 패키징도 확인했다. HTTP 테스트는 원본에 새로 추가된 `returned` 상태 응답이 재승인한 배송 계약에서 처리되는지도 확인한다.
