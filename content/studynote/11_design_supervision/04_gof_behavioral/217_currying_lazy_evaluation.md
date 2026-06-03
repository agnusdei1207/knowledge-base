+++
title = "217. 커링과 지연 평가 (Currying and Lazy Evaluation)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Currying (커링)은 다인수 함수를 단인수 함수들의 체인으로 분해하는 기법이고, [Lazy Evaluation](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/) ([지연 평가](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/))은 값이 실제로 필요할 때까지 계산을 미루는 평가 전략이다 — 둘 다 "필요할 때까지 미루는" 함수형 철학을 공유한다.
> 2. **가치**: 커링은 부분 적용(Partial Application)으로 재사용 가능한 특화 함수를 쉽게 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하고, [지연 평가](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/)는 불필요한 연산을 아예 실행하지 않아 성능과 메모리를 절감한다.
> 3. **판단 포인트**: Java Stream의 `filter()`, `map()` 등 중간 연산(Intermediate [Operation](/knowledge-base/studynote/05_database/06_dw_olap_trends/329_delta_encoding/))은 [지연 평가](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/) — 터미널 연산(Terminal [Operation](/knowledge-base/studynote/05_database/06_dw_olap_trends/329_delta_encoding/), `collect()`, `count()`)이 호출될 때까지 실제 실행을 미룬다.

---

## Ⅰ. 개요 및 필요성
커링의 어원: Haskell Curry (수학자/논리학자)의 이름에서 유래.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">일반 함수: f(a, b, c) → result</div>
<div class="kb-diagram-note">커링 함수: f(a) → g(b) → h(c) → result</div>
<div class="kb-diagram-note">f(a)(b)(c) → result</div>
</div>
</div>



**목적**: 함수를 특화(Specialize)시켜 재사용성을 높인다.

```java
// 일반 함수: 두 인수를 한번에 받음
BiFunction<Integer, Integer> add = (a, b) -> a + b;
add.apply(3, 5); // 8

// 커링: 첫 번째 인수만 받아 새 함수 반환
Function<Integer, Function<Integer, Integer>> curriedAdd =
    a -> b -> a + b;
Function<Integer, Integer> add3 = curriedAdd.apply(3); // a=3으로 특화
add3.apply(5); // 8
add3.apply(7); // 10
```

| 개념 | 설명 | 반환 타입 |
|:---|:---|:---|
| Currying (커링) | 모든 인수를 단인수 함수 체인으로 분해 | 항상 단인수 함수 |
| Partial Application (부분 적용) | 일부 인수를 미리 바인딩하여 나머지 인수를 받는 함수 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 다인수 함수 가능 |

```
f(a, b, c) 커링:    f(a) → (b → (c → result))    // 3단계 단인수 함수
f(a, b, c) 부분 적용 (a 고정): g(b, c) → result    // 2인수 함수 반환
```



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Problem</div><div class="kb-diagram-cell">──▶</div><div class="kb-diagram-cell">Core Idea</div><div class="kb-diagram-cell">──▶</div><div class="kb-diagram-cell">Expected Gain</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: 커링은 볼펜 조립공장처럼 부품(인수)을 하나씩 끼워 넣어 완성하는 것 — 중간에 멈추면 "펜대만 있는 반제품"(부분 적용 함수)이 되고, 나중에 남은 부품을 끼우면 완성된 볼펜(결과값)이 나온다.

---

## Ⅱ. 아키텍처 및 핵심 원리
[지연 평가](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/)는 표현식이 실제로 사용될 때까지 계산을 미루는 평가 전략이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">즉시 평가 (Eager Evaluation, 기본 방식):</div>
<div class="kb-diagram-note">List&lt;Integer&gt; nums = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);</div>
<div class="kb-diagram-note">List&lt;Integer&gt; result = new ArrayList&lt;&gt;();</div>
<div class="kb-diagram-note">for (int n : nums) {</div>
<div class="kb-diagram-note">if (n % 2 == 0) result.add(n * 2); // 모든 원소를 즉시 처리</div>
<div class="kb-diagram-note">}</div>
<div class="kb-diagram-note">// → 10개 모두 filter 시도, 5개 map 수행</div>
<div class="kb-diagram-note">지연 평가 (Lazy Evaluation, Java Stream):</div>
<div class="kb-diagram-note">nums.stream()</div>
<div class="kb-diagram-note">.filter(n -&gt; n % 2 == 0) // 아직 실행 안 됨 (중간 연산)</div>
<div class="kb-diagram-note">.map(n -&gt; n * 2) // 아직 실행 안 됨 (중간 연산)</div>
<div class="kb-diagram-note">.findFirst(); // 터미널 연산 → 실행 시작</div>
<div class="kb-diagram-note">// → 짝수 첫 번째를 찾으면 즉시 중단 (나머지 원소 처리 안 함)</div>
</div>
</div>





<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Java Stream 지연 평가 파이프라인</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">소스(Source) 중간 연산(Intermediate) 터미널 연산</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Collection</div><div class="kb-diagram-cell">▶</div><div class="kb-diagram-cell">.filter()</div><div class="kb-diagram-cell">▶</div><div class="kb-diagram-cell">.collect()</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Array</div><div class="kb-diagram-cell">.map()</div><div class="kb-diagram-cell">.count()</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Stream.of()</div><div class="kb-diagram-cell">.sorted()</div><div class="kb-diagram-cell">.findFirst</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">.distinct()</div><div class="kb-diagram-cell">.reduce()</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">.limit()</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">← 아직 실행 안됨 →</div><div class="kb-diagram-cell">← 이 시점에 실행!</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">실제 파이프라인 처리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(pull 방식으로</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">원소를 하나씩 끌어</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">당겨 처리)</div></div>
</div>
</div>



Haskell은 기본적으로 모든 표현식을 [지연 평가](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/)한다:

```haskell
-- 무한 리스트 (즉시 평가라면 무한 루프)
naturals = [1..]            -- 자연수 무한 리스트

-- take 10이 호출될 때까지 실제로는 아무것도 계산하지 않음
first10 = take 10 naturals  -- [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 역할 | 입력·상태·출력을 분리하는 책임 경계 | 구현보다 경계를 먼저 본다. |
| 제어 지점 | 조건, 이벤트, 정책이 만나는 곳 | 병목과 결합이 생기는 곳이다. |
| [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 포인트 | 테스트·[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·모니터링으로 확인할 지점 | 운영 가능성이 설계 품질을 결정한다. |

- **📢 섹션 요약 비유**: [지연 평가](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/)는 레스토랑 메뉴판처럼 — 메뉴를 훑어볼 때는 요리를 만들지 않고, "이것 주세요(터미널 연산)" 라고 할 때 비로소 주방이 가동된다.

---

## Ⅲ. 비교 및 연결
| 관점 | 즉시 평가 (Eager) | [지연 평가](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/) ([Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/)) |
|:---|:---|:---|
| 실행 시점 | 표현식 정의 즉시 | 결과가 필요할 때 |
| 메모리 사용 | 중간 컬렉션 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 스트림으로 원소 단위 처리 |
| 단락 평가 | 불가 (모두 처리) | 가능 (필요 시 중단) |
| 무한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 불가 | 가능 |
| 디버깅 | 쉬움 | 상대적으로 어려움 |
| 대표 언어 | Java (기본), Python | Haskell, Java [Stream](/knowledge-base/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/) |

| 패턴 | 설명 | 예시 |
|:---|:---|:---|
| 로거 커링 | [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 레벨을 미리 바인딩 | `log("ERROR")("메시지")` |
| [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)기 커링 | [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 규칙을 미리 바인딩 | `validate(schema)(data)` |
| [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 요청 커링 | 기본 URL을 미리 바인딩 | `request(baseUrl)(endpoint)(params)` |
| 세금 계산기 커링 | 세율을 미리 바인딩 | `tax(0.1)(price)` |

- **📢 섹션 요약 비유**: 커링은 "세팅 버튼이 있는 커피 머신" — 원두(첫 번째 인수)를 넣어두면 언제든 물(두 번째 인수)만 붓으면 커피(결과)가 나오는 것처럼, 공통 설정을 미리 바인딩해두고 나머지만 나중에 제공한다.

---

## Ⅳ. 실무 적용 및 기술사 판단
```java
// 함수형 인터페이스를 활용한 커링
public static <A, B, C> Function<A, Function<B, C>> curry(BiFunction<A, B, C> f) {
    return a -> b -> f.apply(a, b);
}

// 실제 사용
Function<String, Function<String, String>> greet =
    curry((greeting, name) -> greeting + ", " + name + "!");

Function<String, String> hello = greet.apply("Hello");   // "Hello" 바인딩
Function<String, String> bye   = greet.apply("Goodbye"); // "Goodbye" 바인딩

System.out.println(hello.apply("Alice"));   // "Hello, Alice!"
System.out.println(hello.apply("Bob"));     // "Hello, Bob!"
System.out.println(bye.apply("Alice"));     // "Goodbye, Alice!"
```

```java
// 1억 개 요소에서 짝수이고 100 미만인 첫 3개만 필요할 때
List<Integer> result = IntStream.range(1, 100_000_001)
    .filter(n -> n % 2 == 0)   // 지연: 아직 실행 안 됨
    .filter(n -> n < 100)      // 지연: 아직 실행 안 됨
    .limit(3)                  // 지연: 아직 실행 안 됨
    .boxed()
    .collect(Collectors.toList()); // 터미널: 이제 실행

// 결과: [2, 4, 6] — 2, 4, 6을 찾는 순간 처리 중단
// 1억 개를 모두 처리하지 않음!
```

| 설계 요소 | 커링 | [지연 평가](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/) |
|:---|:---|:---|
| 재사용성 | 부분 적용으로 특화 함수 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 불필요한 연산 제거 |
| 메모리 | 함수 객체 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 비용 | 중간 컬렉션 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 제거 |
| 무한 자료구조 | 무관 | 무한 [스트림 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/) 가능 |
| 적용 언어/프레임워크 | Scala, Haskell, JavaScript | Java [Stream](/knowledge-base/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/), Haskell, Kotlin |

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 해결하려는 변화 축이 분명한가?
2. [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 비용보다 변경 절감 효과가 큰가?
3. 테스트·[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: [지연 평가](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/)는 영화 스트리밍 — 영화 전체를 다운로드(즉시 평가)하는 게 아니라 보는 부분만 [버퍼링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/454_buffering/)([지연 평가](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/))하여 1시간짜리 영화도 재생 즉시 시작할 수 있다.

---

## Ⅴ. 기대효과 및 결론
커링과 [지연 평가](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/)는 [함수형 프로그래밍](/knowledge-base/studynote/04_software_engineering/06_software_architecture/324_functional_programming_core/)의 두 핵심 기둥이다:

**커링의 가치**:
- 함수를 재사용 가능한 조각으로 분해
- 부분 적용으로 특화 함수 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 구성
- 함수 합성의 기반 제공

<strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/">지연 평가</a>의 가치</strong>:
- 불필요한 연산 완전 제거
- 무한 자료구조 처리 가능
- 단락 평가(Short-Circuit Evaluation)로 [조기 종료](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/) 가능

Java에서는 [Stream](/knowledge-base/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/) API를 통해 [지연 평가](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/)를 실용적으로 활용할 수 있으며, `Function<A, Function<B, R>>` 타입으로 커링을 구현할 수 있다. 기술사 시험에서는 <strong>Java Stream의 중간 연산/터미널 연산 구분</strong>과 <strong>커링을 통한 함수 특화(Specialize)</strong>를 명확히 설명하는 것이 핵심이다.

확장 방향은 ① 선언형 API와의 결합, ② [관측 가능성](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/)([Observability](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/)) 내장, ③ [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: 커링은 "재료를 미리 손질해두는 밀프렙(Meal Prep)" — 미리 재료(인수)를 준비해두면 식사 시간(실행 시점)에 빠르게 완성할 수 있고, [지연 평가](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/)는 "배고플 때만 요리하는 것" — 배고프지 않으면(결과가 필요 없으면) 아예 불을 켜지 않는다.

---

### 📌 관련 개념 맵
| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | [함수형 프로그래밍](/knowledge-base/studynote/04_software_engineering/06_software_architecture/324_functional_programming_core/) ([Functional Programming](/knowledge-base/studynote/04_software_engineering/06_software_architecture/324_functional_programming_core/)) | 커링/[지연 평가](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/)가 속하는 패러다임 |
| 연관 개념 | 모나드 (Monad) | flatMap 체이닝과 [지연 평가](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/)의 결합 |
| 연관 개념 | 부분 적용 (Partial Application) | 커링의 실용적 변형 |
| 구현체 | Java [Stream](/knowledge-base/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/) [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) | [지연 평가](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/)의 대표 구현체 |
| 구현체 | Haskell | 커링과 [지연 평가](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/)를 기본 채택한 언어 |
| 연관 개념 | 불변 객체 ([Immutable Object](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/172_builder_immutable_object/)) | [함수형 프로그래밍](/knowledge-base/studynote/04_software_engineering/06_software_architecture/324_functional_programming_core/)의 또 다른 핵심 원칙 |
| 연관 개념 | 함수 합성 (Function Composition) | 커링이 가능하게 하는 합성 패턴 |

### 📈 관련 키워드 및 발전 흐름도
부분 적용 → 커링과 [지연 평가](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/) → 스트림 최적화

### 👶 어린이를 위한 3줄 비유 설명
1. 커링은 조각 케이크 만들기야 — "케이크(초코맛)(딸기 장식)(생크림)" 처럼 재료를 하나씩 추가하면서 원하는 케이크를 만들 수 있어.
2. [지연 평가](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/)는 숙제를 "제출할 때" 하는 것과 같아 — 선생님이 검사하러 올 때(터미널 연산)만 실제로 계산하고, 그 전까지는 "나중에 할게" 라고 계획만 세워둬.
3. Java Stream은 [지연 평가](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/) 덕분에 100억 개의 숫자에서 딱 10개만 필요하면 10개를 찾는 순간 멈춰서 나머지 99억 9999만 9990개는 아예 처리하지 않아 — 정말 필요한 것만 한다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 278 / 530

← **이전**: [216. 모나드 패턴 (Monad / Functional Programming Pattern)](/knowledge-base/studynote/11_design_supervision/04_gof_behavioral/216_monad_functional_pattern/)
**다음**: [218. 불변 객체 패턴 (Immutable Object Pattern)](/knowledge-base/studynote/11_design_supervision/04_gof_behavioral/218_immutable_object_pattern/) →

---
