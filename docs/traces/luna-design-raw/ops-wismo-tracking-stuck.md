# ops-wismo-tracking-stuck — luna-design-raw

[← 실행 묶음](README.md)

**과업**

> customer on order 27184 says tracking hasn't moved since monday. what's going on and what do I tell them

- 답에 있어야 할 사실: UPS 1ZNW271840001, the last scan is picked_up on Mon Nov 2
- 답에 있어야 할 사실: the promised delivery date is today, Fri Nov 6
- 답에 있어야 할 사실: the agent drafts a reply for the operator; it does not send one

### GPT-6-Luna · 원본 파사드 · 1회차 · ✗ 실패

토큰 15,579 · 모델 호출 2회 · 도구 호출 1회

**질문 1**
> customer on order 27184 says tracking hasn't moved since monday. what's going on and what do I tell them

- 라우팅: Orders agent (the request names this agent's work)
- 도구 검색 후보: 7 candidates: saveCustMsgSend, getOrdGridList, getPrmtTgtMbrList, getOrdGridListCnt, getOrdDtlPopInitData, getPrmtTgtMbrListCnt, getMbrGrdList
- 계획: `getOrdDtlPopInitData` `` {"ordNo":"27184"} ``
1. 에이전트 → **`getOrdDtlPopInitData`** `` {"ordNo":"27184"} ``
   ← 실패: `` {"code":"order_not_found","class":"not_found","message":"There is no order 27184.","next_tool":null} ``

**답변 1**
> getOrdDtlPopInitData failed: There is no order 27184.

**채점**: ✗ 실패 — 빠진 것: fact "UPS 1ZNW271840001, the last scan is picked_up on Mon Nov 2" (1znw271840001, 2 not shown); fact "the promised delivery date is today, Fri Nov 6" (6 not shown)

### GPT-6-Luna · 원본 파사드 · 2회차 · ✗ 실패

토큰 15,536 · 모델 호출 2회 · 도구 호출 1회

**질문 1**
> customer on order 27184 says tracking hasn't moved since monday. what's going on and what do I tell them

- 라우팅: Orders agent (the request names this agent's work)
- 도구 검색 후보: 7 candidates: saveCustMsgSend, getOrdGridList, getPrmtTgtMbrList, getOrdGridListCnt, getOrdDtlPopInitData, getPrmtTgtMbrListCnt, getMbrGrdList
- 계획: `getOrdDtlPopInitData` `` {"ordNo":"27184"} ``
1. 에이전트 → **`getOrdDtlPopInitData`** `` {"ordNo":"27184"} ``
   ← 실패: `` {"code":"order_not_found","class":"not_found","message":"There is no order 27184.","next_tool":null} ``

**답변 1**
> getOrdDtlPopInitData failed: There is no order 27184.

**채점**: ✗ 실패 — 빠진 것: fact "UPS 1ZNW271840001, the last scan is picked_up on Mon Nov 2" (1znw271840001, 2 not shown); fact "the promised delivery date is today, Fri Nov 6" (6 not shown)

### GPT-6-Luna · 원본 파사드 · 3회차 · ✗ 실패

토큰 7,817 · 모델 호출 1회 · 도구 호출 1회

**질문 1**
> customer on order 27184 says tracking hasn't moved since monday. what's going on and what do I tell them

- 라우팅: Orders agent (the request names this agent's work)
- 도구 검색 후보: 7 candidates: saveCustMsgSend, getOrdGridList, getPrmtTgtMbrList, getOrdGridListCnt, getOrdDtlPopInitData, getPrmtTgtMbrListCnt, getMbrGrdList
- 계획: `getOrdDtlPopInitData` `` {"ordNo":"27184"} ``
1. 에이전트 → **`getOrdDtlPopInitData`** `` {"ordNo":"27184"} ``
   ← 실패: `` {"code":"order_not_found","class":"not_found","message":"There is no order 27184.","next_tool":null} ``

**답변 1**
> getOrdDtlPopInitData failed: There is no order 27184.

**채점**: ✗ 실패 — 빠진 것: fact "UPS 1ZNW271840001, the last scan is picked_up on Mon Nov 2" (1znw271840001, 2 not shown); fact "the promised delivery date is today, Fri Nov 6" (6 not shown)
