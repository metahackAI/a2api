# 변경 영향과 증분 재생성 예제

```bash
python -m pip install -e ".[mcp]"
python -m a2api incremental-demo
python -m a2api reapproval-demo
```

검토된 `order.summary`와 `order.shipping_status`에서 배송 enum을 변경한다. getShipment만 다시 변환하고 getOrder와 주문 기본 조회 계약은 재사용한다. 배송 capability는 `requires_review`로 비활성화되며, 실제 MCP stdio에서 주문 기본 조회는 backend HTTP 한 번으로 실행된다.

- [OpenAPI](../../src/a2api/sample/order-shipping.incremental.openapi.json)
- [기존 검토 설정](../../src/a2api/sample/order-shipping.incremental.review.json)
- [명령·의존성 범위·산출물·기존 빌드 이행](../../docs/09-source-diff-and-regeneration.ko.md)
- [선택 검토안·재승인·승인 후 MCP 호출](../../docs/10-selective-reapproval.ko.md)

공유 ActorId → PrincipalId 참조는 두 API에 연결된다. 이 공유 정의를 변경하면 두 capability 모두 재검토 대상이다. 참조하지 않는 schema나 문서 metadata를 변경하면 기존 계약과 검토를 유지한다. 소스와 검토 설정은 직접 수정하지 않고 새 출력 폴더에 결과를 기록한다. 샘플은 로컬 fixture 범위이며 외부 API를 호출하지 않는다.
