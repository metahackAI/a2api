# ops-change-address-in-transit — own22-heldout-raw-logs

[← 실행 묶음](README.md)

**과업**

> customer on 27184 moved, can you change the shipping address?

- 답에 있어야 할 사실: no: the order is already with UPS (in transit since Nov 2); an address can only change before it ships

### 원본 파사드 · 1회차 · ✗ 실패

토큰 2,411 · 모델 호출 2회 · 도구 호출 1회

**질문 1**
> customer on 27184 moved, can you change the shipping address?

- 라우팅: Orders agent (chosen by the model)
- 도구 검색 후보: 5 candidates: saveCustMsgSend, getClmGridList, getClmGridListCnt, getOrdDtlPopInitData, getOrdGridList
- 계획: `getOrdDtlPopInitData` `` {"ordNo":"27184"} ``
1. 에이전트 → **`getOrdDtlPopInitData`** `` {"ordNo":"27184"} ``
   ← 실패: `` {"code":"order_not_found","class":"not_found","message":"There is no order 27184.","next_tool":null} ``

**답변 1**
> getOrdDtlPopInitData failed: There is no order 27184.

**채점**: ✗ 실패 — 빠진 것: fact "no: the order is already with UPS (in transit since Nov 2); " (2 not shown)

### 원본 파사드 · 2회차 · ✗ 실패

토큰 2,411 · 모델 호출 2회 · 도구 호출 1회

**질문 1**
> customer on 27184 moved, can you change the shipping address?

- 라우팅: Orders agent (chosen by the model)
- 도구 검색 후보: 5 candidates: saveCustMsgSend, getClmGridList, getClmGridListCnt, getOrdDtlPopInitData, getOrdGridList
- 계획: `getOrdDtlPopInitData` `` {"ordNo":"27184"} ``
1. 에이전트 → **`getOrdDtlPopInitData`** `` {"ordNo":"27184"} ``
   ← 실패: `` {"code":"order_not_found","class":"not_found","message":"There is no order 27184.","next_tool":null} ``

**답변 1**
> getOrdDtlPopInitData failed: There is no order 27184.

**채점**: ✗ 실패 — 빠진 것: fact "no: the order is already with UPS (in transit since Nov 2); " (2 not shown)
