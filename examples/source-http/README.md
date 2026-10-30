# 소스 기반 HTTP 예제

회사 소스와 무관한 합성 Java/Spring MVC·Go net/http·Rust Axum item API다. OpenAPI 없이 route/DTO를 읽어 같은 convert·MCP로 호출한다.

```bash
python -m pip install -e ".[source,mcp]"
python examples/source-http/verify.py
```

각 언어의 JDK/Maven·Go·Rust/Cargo/C 링커가 설치돼 있어야 한다. 현재 서버의 로컬 설치 경로는 검증 스크립트가 자동으로 읽는다. 각 서버는 생성/조회/PUT/PATCH/DELETE/HEAD와 POST 검색을 제공하며 직접 HTTP와 실제 MCP stdio를 모두 검증한다.

`application.py`는 이 예제의 노출 대상·read/write 효과·반환 필드를 선택한다. `mcp_server.py`는 같은 app을 세 도구에 연결한다. `verify.py --language spring|go|rust`로 하나씩 실행할 수 있다.

[전체 사용법·지원 문법·제약](../../docs/18-source-importers.ko.md), [실제 실행 기록](../../docs/evidence/source-importers.json).
