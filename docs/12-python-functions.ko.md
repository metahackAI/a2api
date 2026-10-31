# P0-2: Python 함수와 신규 API를 명시적으로 등록하기

P0-1과 같은 `a2api-call/0.1` descriptor와 `describe(id)` / `invoke(id, input, context=...)`를 사용한다. 타입 힌트·TypedDict에서 schema를 만들고 등록한 동기 조회 함수를 직접 호출한다. 파일 생성·review/build·모듈 스캔은 필요 없다. P0-3 MCP 경량화는 이번 범위에 포함하지 않는다.

이후 구현한 두 객체의 MCP 연결은 [P0-3 사용 안내](13-lightweight-mcp.ko.md)를 따른다.

## 실행 예제

저장소 루트에서 기본 패키지만 설치한다.

```bash
python -m pip install -e .
python examples/native-orders/register_and_invoke.py
```

[예제 코드](../examples/native-orders/register_and_invoke.py)는 타입이 없는 기존 주문 함수를 감싼 `orders.lookup`과, 처음부터 타입을 선언한 새 API `shipping.list`를 등록한다. 기존 주문 함수의 사용자·테넌트 검사를 유지하며 공개 DTO만 반환한다. 정상·빈 배송을 확인한다. HTTP·LLM·MCP 연결 없이 함수 호출로 동작한다.

## 기본 사용법

```python
from typing import TypedDict
from a2api import Application, ExecutionContext, capability

class OrderView(TypedDict):
    orderId: str
    orderState: str

@capability(id="orders.lookup", effect="read")
def lookup_order(orderId: str, *, context: ExecutionContext) -> OrderView:
    """접근 가능한 주문의 상태를 조회한다."""
    row = legacy_repository.load_visible_to(orderId, context)
    return {"orderId": row.id, "orderState": row.state}

app = Application([lookup_order])
description = app.describe("orders.lookup")
result = app.invoke("orders.lookup", {"orderId": "ORD-1001"}, context=caller)
```

`legacy_repository`와 `caller`는 기존 호스트의 코드/인증 값이다. 신규 API는 wrapper 없이 업무 구현에 직접 연결한다. context가 필요 없는 공개·순수 함수는 context 인자를 선언하지 않아도 되며, invoke의 호스트 context는 동일하게 제공한다.

원래 함수를 수정하기 어려우면 `registered = capability(id="orders.lookup", effect="read")(existing_function)`으로 등록한다. 단, 기존 함수가 지원하는 입출력 타입을 선언하거나 아래 명시적 schema를 제공해야 한다. decorator는 함수를 실행하지 않으며, 별도로 `Application`에 전달한 항목만 노출된다. 등록된 함수를 일반 Python 함수처럼 직접 부를 수도 있으나, 프로토콜 검증·오류 envelope는 `invoke` 경로에서 적용된다.

## 지원하는 타입과 schema

| Python 선언 | 생성 schema/처리 |
|---|---|
| `str`, `bool`, `int`, `float`, `None` | JSON string/boolean/integer/number/null |
| `list[T]`, `dict[str, T]` | 타입을 검사하는 배열/문자열 키 객체 |
| `T \| None`, `Optional[T]`, `Union[...]` | 각 대안의 anyOf. nullable과 필드 생략은 구별 |
| `Literal[...]` | JSON scalar의 enum |
| 표준 `typing.TypedDict` | 이름별 properties, required, additionalProperties=false |
| 중첩 TypedDict·상속 | 자식 필드와 상속한 required/optional 의미 보존 |
| `Required[T]`, `NotRequired[T]`, `total=False` | TypedDict 필수/선택 필드. future annotations도 해석 |
| 함수 기본값 | 입력에서 선택 인자, schema의 default, 생략 시 기본값 적용 |

보통의 인자와 keyword-only 인자를 지원한다. `context`는 **기본값 없는 keyword-only `ExecutionContext`**로 선언해야 하며 schema와 input에 포함하지 않는다. 다른 이름으로 ExecutionContext를 업무 인자로 노출하지 않는다.

예를 들어 `eta: str | None`은 필수지만 null이 가능하다. `eta: NotRequired[str | None]`은 생략도 가능하다. TypedDict는 타입/필드를 검증하며, 내부 필드가 추가된 반환값을 자동 필터링하지 않는다. 공개 DTO를 함수가 만들어 반환해야 한다.

타입 변환이나 사용자 객체 생성을 하지 않고 JSON Schema 의미로 검증한다. 따라서 integer는 JSON Schema의 정수 값, number는 JSON 숫자다. 반환값도 dict/list/문자열/유한 숫자/bool/null의 실제 JSON 값이어야 한다. tuple을 list로 바꾸거나 객체를 임의로 직렬화하지 않는다.

기본값은 등록 시 검증·복사하고, 매 호출마다 별도 사본으로 적용한다. mutable default가 한 호출의 수정으로 다음 호출에 누적되지 않는다. OpenAPI의 주석 default와 달리 Python 함수의 생략 인자는 실제 함수 기본값으로 처리한다.

## 명시적 schema가 필요한 경우

`Any`, 타입 누락, 임의 class/dataclass, tuple/set, Annotated 메타데이터, 재귀 TypedDict·미지원 annotation을 임의의 허용 schema로 바꾸지 않는다. 작은 JSON wrapper로 경계를 선언하거나 `input_schema` / `output_schema`로 해당 방향의 schema를 제공한다.

```python
def legacy_echo(value):
    return {"value": value}

schema = {
    "type": "object",
    "properties": {"value": {"type": "string", "minLength": 1}},
    "required": ["value"],
    "additionalProperties": False,
}
echo = capability(id="legacy.echo", effect="read",
                  input_schema=schema, output_schema=schema)(legacy_echo)
app = Application([echo])
```

명시적 입력 schema도 함수의 모든 업무 인자를 properties로 선언하고, 기본값 없는 인자를 required로 유지해야 한다. 입력 root는 닫힌 object다. 2020-12 schema와 묶음 내부 `$defs` 참조를 지원하고 외부 참조를 가져오지 않는다. schema 제공이 Python 객체 생성/변환이나 함수 signature 제한을 우회하지는 않는다.

타입 힌트는 Python의 `get_type_hints`로 해석한다. 모듈 수준에서 해석 가능한 타입을 사용한다. 해석되지 않는 local forward reference는 명확한 wrapper로 바꾼다. 등록 대상과 annotation은 호스트가 신뢰하는 코드이며, LLM이 지정한 경로를 import하거나 전체 소스에서 함수를 자동 탐색하지 않는다.

## 호출 결과와 오류

성공 결과는 P0-1과 같은 `status/data/completeness`다. complete의 범위는 단일 API 응답이며, 함수의 선언만으로 업무 전체 완료를 보장하지 않는다.

- 입력 검증은 본문 실행 전 수행하며 잘못된 입력은 `INVALID_INPUT`이다.
- host context가 올바르지 않으면 `UNAUTHENTICATED`, 미노출 ID는 `NOT_FOUND`다.
- JSON이 아닌 값·잘못된 반환 타입·추가/누락 필드는 `SCHEMA_MISMATCH`다.
- 함수가 명시한 공개 `A2APIError`는 유지한다. 권한 오류도 함수/기존 backend 정책에서 검사한다.
- 예상하지 못한 함수 예외는 상세 값·stack trace를 숨긴 `HANDLER_ERROR`다.
- 등록 설정·타입 해석 오류는 함수 호출 전에 `A2APIError`를 발생시킨다.

함수 호출은 동기 방식으로 한 번 실행한다. async/generator, `*args`/`**kwargs`, positional-only 인자와 쓰기 효과는 이번 profile에서 지원하지 않는다. 스레드 실행·자동 재시도·함수 실행 시간 제한을 추가하지 않았다. 효과 선언은 권한 부여나 함수 부작용의 자동 검증이 아니다.

## 검증 범위

기존 함수 wrapper와 신규 API 예제, 자동 schema 생성과 명시적 schema, 중첩/상속/선택 필드, 기본값, context 비노출과 위조 거부, 입력 검증 전 본문 실행 방지, 반환값 검증과 비공개 오류 처리를 확인한다. 같은 업무의 실제 HTTP/OpenAPI 호출과 Python 호출의 descriptor 필드·결과·오류 형식도 비교한다. LLM 성능·전체 소스 자동 변환·P0-3 구현을 검증한 결과로 해석하지 않는다.

ResourceWarning도 오류로 처리한 전체 회귀 테스트 216개가 통과했다. P0-2 테스트는 기본 의존성의 Python 3.14에서도 실행했고, 소스 폴더 밖에 추출한 wheel에서도 TypedDict schema 생성·context 제외·정상/오류 호출을 확인했다.

## 쓰기·비동기 함수(2026-10-31, [33 문서](33-completion-plan.ko.md) 1단계)

`@capability(id=..., effect="write")`로 생성·변경·삭제 함수를 등록할 수 있다. descriptor의 `effects.kind`가 `write`가 되고, 쓰기 함수가 하나라도 있는 앱을 MCP에 연결하면 invoke annotation이 보수적으로 바뀐다. effect는 개발자의 선언이며 권한·승인을 대신하지 않는다. 같은 입력 검증 → 함수 실행 → 반환 검증 순서를 사용하고, 실패한 쓰기를 자동 재시도하지 않는다. 업무 오류는 `A2APIError('RESOURCE_NOT_FOUND', ..., status=404)`처럼 직접 올리면 같은 오류 envelope로 전달된다. 그 밖의 예외는 내용을 숨긴 `HANDLER_ERROR`이며, 실패가 부작용이 없었다는 증명은 아니다.

`async def` 함수도 등록한다. 장식한 함수는 그대로 await할 수 있고, `app.invoke`는 비동기 함수를 완료까지 실행한다(이벤트 루프 안에서 호출되면 별도 스레드의 루프에서 실행). 동기 함수가 우연히 coroutine을 반환하면 실행하지 않고 `SCHEMA_MISMATCH`로 거부한다. generator/async generator는 계속 지원하지 않는다.

```python
@capability(id="tickets.create", effect="write")
async def create_ticket(customerId: str, subject: str, *, context: ExecutionContext) -> Ticket:
    """고객의 새 지원 티켓을 만들고 실제 ID를 반환한다."""
    return await tickets.create(customerId, subject, actor=context.actor)
```
