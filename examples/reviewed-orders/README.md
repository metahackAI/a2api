# OpenAPI → 검토 → 실행 계약 → MCP

저장소 루트에서 실행한다.

```bash
python -m pip install -e ".[mcp]"
python -m a2api review-demo
```

OpenAPI import와 계약 빌드 후 공식 MCP SDK의 stdio 클라이언트로 discover/describe/invoke를 호출한다. 주문 한 건과 배송 두 건을 실제 loopback HTTP로 조회한다.

단계별 산출물을 보관하려면 새 출력 경로를 사용한다.

```bash
python -m a2api import-openapi src/a2api/sample/order-shipping.openapi.json \
  --namespace legacy_orders --output artifacts/orders-imports
python -m a2api build --imports artifacts/orders-imports \
  --review src/a2api/sample/order-shipping.review.json --output artifacts/orders-built
python -m a2api mcp-demo --build artifacts/orders-built
python -m a2api mcp --build artifacts/orders-built
```

마지막 명령은 MCP 호스트가 실행하는 stdio 서버이며 stdout은 프로토콜 전용이다. CLI는 로컬 샘플 backend와 고정 데모 identity를 사용한다.

- [OpenAPI](../../src/a2api/sample/order-shipping.openapi.json)
- [검토 설정](../../src/a2api/sample/order-shipping.review.json)
- [검토 schema](../../src/a2api/schemas/review.schema.json)
- [설계·실행·검증 안내](../../docs/08-review-builder.ko.md)

`ORD-1002`는 빈 배송과 backend 호출 한 번이다. `--sample-user bob --order-id ORD-2001`로 다른 인증 context를 검증할 수 있다. 기존 수동 계약은 비교 기준으로 남고 새 경로는 import와 검토 설정에서 생성한 계약을 사용한다.

이 검토는 로컬 fixture 범위다. 기본 카탈로그에 노출하지 않으며 실제 서비스 소유자의 production 승인을 의미하지 않는다. build 묶음에는 실제 deployment credential을 저장하지 않는다.
