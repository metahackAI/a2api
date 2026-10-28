# HTTP transport 검증

저장소 루트에서 `python examples/http-adapter/verify.py`를 실행한다.

공식 GitHub REST 명세에서 아래 operation의 IR과 바인딩을 만든 뒤, 임시 loopback HTTP fixture에 연결한다.

| 메서드 | operationId | 응답 |
|---|---|---:|
| POST | issues/create | 201 JSON |
| GET | issues/get | 200 JSON |
| PATCH | issues/update | 200 JSON |
| PUT | issues/lock | 204 empty |
| DELETE | issues/remove-all-labels | 204 empty |

입력과 응답을 생성 스키마로 검증하고 인증 header는 호스트 callback에서 주입한다. 외부 GitHub 호출이나 실제 이슈 변경은 발생하지 않는다. 생성 capability는 비활성 상태로 유지하며, 에이전트 업무 workflow 전체의 검증이 아닌 HTTP transport 검증이다.

추가 HEAD/202 처리, 직렬화와 오류·결과 미확정 테스트는 `tests/test_http_extended.py`에 있다. 사용법과 실행 정책 경계는 [HTTP 어댑터 안내](../../docs/07-http-adapter.ko.md)를 참고한다.
