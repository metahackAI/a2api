# a-commerce 파사드 + a2api: 게이트웨이(프록시) 연결 안내

a-commerce의 운영자 파사드(22개 화면, PR #103 이후)를 a2api로 변환해 **a-commerce 자체 에이전트에 그대로 연결**하는 방법이다. 에이전트·검색·계획기·한도는 바꾸지 않고, 도구 표현만 바뀐다.

## 무엇이 바뀌나

| 항목 | 원본 파사드 | a2api 게이트웨이 |
|---|---|---|
| 도구 이름 | `getOrdGridList` | `get_order_grid_list`(약어를 풀어 씀, `legacy_facade.WORDS`) |
| 입력 필드 | `ordStatCd`, `ordDtmFrom`, `srchKwd` | `order_status`, `ordered_from`, `keyword` |
| 코드값 | `"20"`, `"R10"`, `"M99"` | `"processing"`, `"requested"`, `"custom"`(요청은 코드로 되돌리고, 결과의 코드는 단어로 바꿈) |
| 요약 | `Order grid list.` | 화면 코드에서 읽은 한 문장(무엇을 찾고 무엇을 돌려주는지, 쓰기는 "Runs immediately") |
| 오류 문장 | 원 서버 문장(필드는 `tgtMbrGrdCd`) | 같은 문장, 필드만 읽기 쉬운 이름(`target_member_grade`) |
| 주문 번호 | 주문 상세·메시지 발송의 `ordNo`는 키(`ord_20402`)만 받음(`20402`는 404) | 사람이 보는 번호(`20402`, `#20402`)가 오면 같은 파사드의 주문 목록 화면(검색어)으로 키를 찾아 넣음. 정확히 한 건일 때만(`legacy_facade.HANDLES`) |
| `address`, `kind`, `group`, `method` 등 | 화면 값 | **그대로** |

변환에 쓴 정보는 파사드 코드(`crates/facade`: 필드 주석, `codes.rs`, 각 화면 본문)에서 읽은 것만이다. A-Commerce 도구, 과업 세트, 상점 규칙은 쓰지 않았다(`legacy_facade.py`).

## 실행

```bash
git clone -b a2api-1.1 https://github.com/metahackAI/a2api && cd a2api
python3 -m venv .venv && .venv/bin/pip install -e .          # Python 3.11+
.venv/bin/python examples/acommerce/a2api_gateway.py --host 0.0.0.0 --port 7011 --commerce http://<commerce>:7001
```

- 에이전트만 게이트웨이를 보게 한다: 에이전트 프로세스의 `ACOM_COMMERCE_URL=http://<게이트웨이>:7011`. 다른 서비스(gateway, worker, eval)는 원래 commerce를 그대로 본다.
- 평가는 평소처럼 `xtask eval --tool-set facade ...`.
- 게이트웨이가 바꾸는 요청은 두 가지뿐이다: `GET /v1/tools?set=facade`, `POST /v1/tools/{tool}?set=facade`. 나머지 요청(change set, 상점 설정, A-Commerce 도구 등)은 commerce로 그대로 넘긴다.
- 인증: 각 요청의 `Authorization`을 그대로 넘긴다. 파사드 매니페스트는 첫 `GET /v1/tools?set=facade`를 보낸 호출자의 토큰으로 한 번 읽는다(게이트웨이 자체 자격 증명 불필요). `--token`을 주면 시작할 때 읽는다.
- `--commerce`의 기본값은 `A2API_GATEWAY_COMMERCE` 환경 변수다. `ACOM_COMMERCE_URL`은 일부러 쓰지 않는다(에이전트용 값과 섞이면 게이트웨이가 자기 자신으로 요청을 보낸다).

변환 결과만 보고 싶을 때(서비스 없이):

```bash
.venv/bin/python examples/acommerce/a2api_gateway.py --dump converted.json --manifest facade-manifest.json
```

`converted.json`의 `items`는 에이전트가 받는 매니페스트, `screens`는 변환된 도구 이름 → 원래 화면 이름이다.

## 검수(2026-11-01, a-commerce `d86a1ff`)

`examples/acommerce/verify_gateway.py`는 같은 요청을 원본 파사드(화면 필드·코드)와 게이트웨이(변환된 이름·단어)에 보내 결과를 비교한다. 쓰기는 실제로 실행하므로 매번 데모 상점을 초기화한다.

- 실행 중인 서비스의 파사드 매니페스트 = 받은 첨부 파일(22개 화면, 내용 동일).
- 22개 화면 모두 변환(약어로 남은 입력 필드 0).
- 28개 사례(22개 화면, 주문 검색어·번호·없는 주문 404, 쓰기 오류 422 포함) 모두 같은 결과. 쓰기는 생성 ID만 다름.
- 주문 상세에 번호(`#20402`)를 넣으면 게이트웨이가 주문 목록 화면으로 키를 찾아, 원본에 키를 넣은 결과와 같다. 없는 번호는 원본과 같이 404.
- 화면을 하나 더 부르는 동작은 이 번호 조회뿐이다. 원본 파사드에는 없는 편의이므로 비교 결과를 읽을 때 함께 밝힌다(A-Commerce 도구의 `get_order`는 번호를 직접 받는다).
- 번호 조회 없이 돌리려면 `--no-lookup`을 준다(번호를 그대로 넘김). 변환만의 효과와 조회의 효과를 나눠 잴 때 쓴다.

2026-11-03 a-commerce main `4c6e415`에서 다시 검수했다. 파사드 매니페스트는 위와 같고(22개), 29개 사례 모두 같은 결과였다. 이 버전의 자체 에이전트로 잰 결과는 [42 문서](../../docs/42-own-agent-latest.ko.md)에 있다.

**알려진 한계: 화면 간 관계.** 파사드 매니페스트의 `consumes`/`produces`는 원본·변환 모두 비어 있다. a-commerce 런타임은 이 슬롯으로만 앞 결과의 ID를 다음 호출에 채운다. 그래서 계획이 `"promotion_id": ""`에 `uses`를 붙여도 값이 채워지지 않는다(42 문서 3절).
