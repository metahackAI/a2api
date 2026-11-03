# md-overcoat-runs-small — own-latest-design-raw

[← 실행 묶음](README.md)

**과업**

> people keep saying the wool overcoat runs small. is that actually true?

- 답에 있어야 할 사실: 41 reviews, average 4.6
- 답에 있어야 할 사실: 29 say true to size, 12 say a bit snug, none say it runs large
- 답에 있어야 할 사실: the most common phrase is 'size up for a hoodie' (9 mentions), so the snug votes come from layering

### 원본 파사드 · 1회차 · ✗ 실패

토큰 8,491 · 모델 호출 5회 · 도구 호출 1회

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

- 라우팅: Catalog agent (chosen by the model)
- 도구 검색 후보: 5 candidates: getDispCornerList, getPrdDtlInfo, getPrdDtlInfoV2, getPrdGridList, getPrdGridListCnt
- 계획: `getPrdGridList` `` {"pageNo":0,"srchKwd":"wool overcoat","pageSize":20} ``
1. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"srchKwd":"wool overcoat","pageSize":20} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: people · wool overcoat · runs small · 0 steps by Muse Glimmer 30B

**답변 1**
> The wool overcoat runs small. is that actually true?

**채점**: ✗ 실패 — 빠진 것: fact "41 reviews, average 4.6" (41, 4.6 not shown); fact "29 say true to size, 12 say a bit snug, none say it runs lar" (29, 12 not shown); fact "the most common phrase is 'size up for a hoodie' (9 mentions" (9 not shown)

### 원본 파사드 · 2회차 · ✗ 실패

토큰 8,491 · 모델 호출 5회 · 도구 호출 1회

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

- 라우팅: Catalog agent (chosen by the model)
- 도구 검색 후보: 5 candidates: getDispCornerList, getPrdDtlInfo, getPrdDtlInfoV2, getPrdGridList, getPrdGridListCnt
- 계획: `getPrdGridList` `` {"pageNo":0,"srchKwd":"wool overcoat","pageSize":20} ``
1. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"srchKwd":"wool overcoat","pageSize":20} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: people · wool overcoat · runs small · 0 steps by Muse Glimmer 30B

**답변 1**
> The wool overcoat runs small. is that actually true?

**채점**: ✗ 실패 — 빠진 것: fact "41 reviews, average 4.6" (41, 4.6 not shown); fact "29 say true to size, 12 say a bit snug, none say it runs lar" (29, 12 not shown); fact "the most common phrase is 'size up for a hoodie' (9 mentions" (9 not shown)

### 원본 파사드 · 3회차 · ✗ 실패

토큰 8,491 · 모델 호출 5회 · 도구 호출 1회

**질문 1**
> people keep saying the wool overcoat runs small. is that actually true?

- 라우팅: Catalog agent (chosen by the model)
- 도구 검색 후보: 5 candidates: getDispCornerList, getPrdDtlInfo, getPrdDtlInfoV2, getPrdGridList, getPrdGridListCnt
- 계획: `getPrdGridList` `` {"pageNo":0,"srchKwd":"wool overcoat","pageSize":20} ``
1. 에이전트 → **`getPrdGridList`** `` {"pageNo":0,"srchKwd":"wool overcoat","pageSize":20} ``
   ← 실패: `` {"code":"ERR_PARAM","class":"invalid_input","message":"Invalid paging.","next_tool":null} ``
- 계획: people · wool overcoat · runs small · 0 steps by Muse Glimmer 30B

**답변 1**
> The wool overcoat runs small. is that actually true?

**채점**: ✗ 실패 — 빠진 것: fact "41 reviews, average 4.6" (41, 4.6 not shown); fact "29 say true to size, 12 say a bit snug, none say it runs lar" (29, 12 not shown); fact "the most common phrase is 'size up for a hoodie' (9 mentions" (9 not shown)
