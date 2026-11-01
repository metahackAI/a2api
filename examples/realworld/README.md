# RealWorld (Conduit): 실제 공개 코드에서 변환하기

같은 RealWorld API를 구현한 공개 프로젝트 4개의 **코드만** 읽어 a2api로 변환하고, 공식 OpenAPI와 비교한다. 프로젝트 코드는 빌드하거나 실행하지 않는다.

```bash
mkdir -p ~/realworld && cd ~/realworld
git clone --depth 1 https://github.com/gothinkster/realworld.git
git clone --depth 1 https://github.com/gothinkster/spring-boot-realworld-example-app.git
git clone --depth 1 https://github.com/gothinkster/golang-gin-realworld-example-app.git
git clone --depth 1 https://github.com/launchbadge/realworld-axum-sqlx.git
git clone --depth 1 https://github.com/nsidnev/fastapi-realworld-example-app.git
cd -

python examples/realworld/compare.py ~/realworld            # 코드에서 읽은 19개 operation과 공식 OpenAPI 비교
python examples/realworld/evaluate.py verify ~/realworld    # 모델 없이: 변환한 모든 operation을 실제 호출
python examples/realworld/evaluate.py run ~/realworld --split dev --output runs/dev.jsonl   # 모델 비교
```

- `conduit.py`: 공식 명세를 따르는 메모리 서버. flavor(`spec`, `spring`, `go`, `rust`, `python`)가 각 구현이 코드에 선언한 차이(생성 상태 코드, 빈 bio의 `""`/`null`, 삭제 응답)를 재현한다.
- `conduit_tasks.py`: dev/holdout 작업과 상태·답변 검사. holdout 질문은 fingerprint를 기록한 뒤 바꾸지 않는다.
- `evaluate.py run`의 방식: `spec-tools`(공식 OpenAPI 전체를 함수로), `a2api-openapi`, `a2api-spring`, `a2api-go`, `a2api-rust`, `a2api-python`(각 구현 코드에서 변환).

결과는 [39 문서](../../docs/39-improvement-results.ko.md)에 있다.
