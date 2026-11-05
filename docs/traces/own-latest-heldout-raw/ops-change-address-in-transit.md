# ops-change-address-in-transit — own-latest-heldout-raw

[← 실행 묶음](README.md)

**과업**

> customer on 27184 moved, can you change the shipping address?

- 답에 있어야 할 사실: no: the order is already with UPS (in transit since Nov 2); an address can only change before it ships

### 원본 파사드 · 1회차 · ✗ 실패

토큰 3,494 · 모델 호출 2회 · 도구 호출 1회

**질문 1**
> customer on 27184 moved, can you change the shipping address?

- 라우팅: Orders agent (the request names this agent's work)
- 도구 검색 후보: 6 candidates: saveCustMsgSend, getOrdGridList, getPrmtTgtMbrList, getOrdGridListCnt, getPrmtTgtMbrListCnt, getMbrGrdList
- 계획: `getOrdGridList` `` {"srchKwd":"27184"} ``
1. 에이전트 → **`getOrdGridList`** `` {"srchKwd":"27184"} ``
   ← 결과: `` {"list":[{"mbrNo":"cus_m005474","ordNo":"ord_27184","ordAmt":289.0,"ordDtm":"2026-11-01T00:18:00-04:00","ordStatCd":"30"}],"pageNo":1,"pageSize":20} ``

**답변 1**
> The order 27184 is on hand. It shows order 27184 placed on Sun Nov 1, 2026 for $289.00 with status 30. I don’t have the shipping address or the current fulfillment details yet, and there’s no change set to update the address. I need the order details to see the parcel and payment, and then check if the order can still be modified before I can change the shipping address.

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "no: the order is already with UPS (in transit since Nov 2); " (2 not shown)

### 원본 파사드 · 2회차 · ✗ 실패

토큰 9,753 · 모델 호출 4회 · 도구 호출 3회

**질문 1**
> customer on 27184 moved, can you change the shipping address?

- 라우팅: Orders agent (the request names this agent's work)
- 도구 검색 후보: 6 candidates: saveCustMsgSend, getOrdGridList, getPrmtTgtMbrList, getOrdGridListCnt, getPrmtTgtMbrListCnt, getMbrGrdList
- 계획: `getOrdGridList` `` {"pageNo":0,"srchKwd":"27184","pageSize":1} ``
1. 에이전트 → **`getOrdGridList`** `` {"pageNo":0,"srchKwd":"27184","pageSize":1} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getOrdGridList` `` {"pageNo":0,"srchKwd":"27184","pageSize":10} ``
2. 에이전트 → **`getOrdGridList`** `` {"pageNo":0,"srchKwd":"27184","pageSize":10} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: `getOrdGridList` `` {"pageNo":0,"srchKwd":"27184","pageSize":10} ``
3. 에이전트 → **`getOrdGridList`** `` {"pageNo":0,"srchKwd":"27184","pageSize":10} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``

**답변 1**
> getOrdGridList failed (ERR_PARAM): Invalid paging. Plan it again with the arguments it needs.

**채점**: ✗ 실패 — 빠진 것: fact "no: the order is already with UPS (in transit since Nov 2); " (2 not shown)

### 원본 파사드 · 3회차 · ✗ 실패

토큰 6,047 · 모델 호출 3회 · 도구 호출 1회

**질문 1**
> customer on 27184 moved, can you change the shipping address?

- 라우팅: Orders agent (the request names this agent's work)
- 도구 검색 후보: 6 candidates: saveCustMsgSend, getOrdGridList, getPrmtTgtMbrList, getOrdGridListCnt, getPrmtTgtMbrListCnt, getMbrGrdList
- 계획: `getOrdGridList` `` {"srchKwd":"27184"} ``
1. 에이전트 → **`getOrdGridList`** `` {"srchKwd":"27184"} ``
   ← 결과: `` {"list":[{"mbrNo":"cus_m005474","ordNo":"ord_27184","ordAmt":289.0,"ordDtm":"2026-11-01T00:18:00-04:00","ordStatCd":"30"}],"pageNo":1,"pageSize":20} ``

**답변 1**
> The order 27184 is on hand. It shows order 27184 placed on Sun Nov 1, 2026, for $289.00, with order status 30. I don’t have the shipping address or the current fulfillment status from this grid view, and there’s no change set to update the address. To change the shipping address I’ll need the order details and the parcel status to see if it’s still editable. Could you confirm if you want me to pull the full order details for 27184 first?

화면 블록: product_table(1 of 1)

**채점**: ✗ 실패 — 빠진 것: fact "no: the order is already with UPS (in transit since Nov 2); " (2 not shown)
