---
title: 149. ROLLUP, CUBE, GROUPING SETS (Rollup Cube Grouping Sets)
date: '2026-05-08'
tags:
- studynote-database
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS은 다차원 소계 및 총계 [[087_process_state_transition|생성]] ([[316_olap|OLAP]])에 초점을 맞춘 개념이다.
> 2. **가치**: 대용량 질의에서는 같은 SQL도 접근 경로와 [[166_execution_plan_optimizer_navigation_tree|실행 계획]]에 따라 비용이 크게 달라진다.
> 3. **판단 포인트**: 판단 포인트는 [[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS를 어디에 적용해야 효과가 크고, 어떤 비용이나 제약이 따라오는지 함께 보는 데 있다.

---

## Ⅰ. 개요 및 필요성

[[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS은 다차원 소계 및 총계 [[087_process_state_transition|생성]] ([[316_olap|OLAP]])에 초점을 맞춘 개념이다. 대용량 질의에서는 같은 SQL도 접근 경로와 [[166_execution_plan_optimizer_navigation_tree|실행 계획]]에 따라 비용이 크게 달라진다. 잘못 쓰면 Full Scan, 정렬, 랜덤 I/O가 한꺼번에 늘어난다.

```text
┌──────────────────────────────────────────────────────────────┐
│ SQL text -> Planner -> Current concept -> Latency            │
├──────────────────────────────────────────────────────────────┤
│ Predicate -> path choice -> I/O cost                         │
└──────────────────────────────────────────────────────────────┘
```

이 그림은 [[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS를 독립 기능이 아니라 전체 [[001_dikw_pyramid|데이터]] 흐름에서 특정 통제 지점을 맡는 구조로 이해해야 한다는 점을 [[347_compaction|압축]]해 보여 준다.

- **📢 섹션 요약 비유**: [[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS는 도서관 색인표로 책을 찾는 일에 가깝다. 중요한 것은 순서를 정하고 책임 범위를 분명히 하는 일이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS는 결국 "언제 보고, 어디에서 적용하고, 무엇을 보장할 것인가"를 정하는 메커니즘이다. 특히 `그룹 바이 / 해빙`과 `집합 연산자` 사이에서 현재 주제가 맡는 책임을 분리해 보면 구조가 더 또렷해진다.

| 관점 | 설명 | 설계 포인트 |
| :--- | :--- | :--- |
| 핵심 대상 | [[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS는 `ROLLUP, CUBE, GROUPING SETS`의 역할과 적용 범위를 규정한다. | 이름보다 입력·출력 경계를 먼저 정의해야 한다. |
| 작동 원리 | 핵심은 현재 개념을 어떤 시점에 평가하고 어떤 범위에 적용하느냐에 있다. | 언제 평가하고 언제 확정하는지가 [[282_performance_tactics|성능]]과 정합성을 가른다. |
| [[282_performance_tactics|성능]] 영향 | [[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS는 [[139_throughput|처리량]], [[015_지연_데이터_관점|지연]]시간, 운영 복잡도 중 적어도 하나에 직접 영향을 준다. | 이득과 비용을 같이 보지 않으면 과설계가 된다. |
| 운영 주의 | `그룹 바이 / 해빙`·`집합 연산자`과 경계를 혼동하면 적용 위치가 어긋난다. | 장애 시 관찰할 지표와 우회 [[268_strategy_pattern|전략]]을 미리 준비해야 한다. |

```text
┌──────────────────────────────────────────────────────────────┐
│ Parse -> estimate -> current concept -> execute              │
├──────────────────────────────────────────────────────────────┤
│ Plan quality -> CPU/I/O balance -> response                  │
└──────────────────────────────────────────────────────────────┘
```

핵심은 [[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS를 단순 옵션이 아니라 입력 조건, 처리 순서, 결과 보장을 함께 묶는 설계 규칙으로 보는 것이다. 그래서 구현 전에 평가 시점·충돌 지점·[[658_ir_recovery|복구]] 가능성을 먼저 정리해야 한다.

- **📢 섹션 요약 비유**: [[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS는 물류센터에서 빠른 동선을 고르는 일에 가깝다. 중요한 것은 순서를 정하고 책임 범위를 분명히 하는 일이다.

---

## Ⅲ. 비교 및 연결

[[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS는 종종 `그룹 바이 / 해빙` 또는 `집합 연산자`과 같은 묶음으로 설명되지만, 세 개념의 관심사는 다르다. [[148_sql_group_by_having_clause|그룹 바이]] / 해빙이 준비 단계나 전제에 가깝다면, [[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS는 실제 통제 지점을 잡고, 집합 연산자는 그 결과를 더 강하게 만들거나 다른 방향으로 확장한다. 이 차이를 구분해야 시험 답안에서도 경계와 선택 이유를 설득할 수 있다.

| 비교 축 | [[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS | [[148_sql_group_by_having_clause|그룹 바이]] / 해빙 | 집합 연산자 |
| :--- | :--- | :--- | :--- |
| 초점 | 현재 주제가 직접 통제하는 병목과 제약에 집중한다. | 바로 앞 단계나 전제를 다룬다. | 후속 확장 또는 보완 역할이 강하다. |
| 적용 시점 | 현재 개념이 요구되는 순간에 핵심 제어점으로 작동한다. | 준비·선행 판단에서 먼저 등장한다. | 세부 최적화나 확장에서 더 자주 등장한다. |
| 주된 위험 | 과신하면 비용 대비 효과가 줄어든다. | 부족하면 현재 개념도 안정적으로 성립하지 않는다. | 무작정 적용하면 복잡도와 운영 부담이 커질 수 있다. |

또한 [[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS는 단순 정의 암기로 끝나는 개념이 아니라, 실제로는 [[282_performance_tactics|성능]]·정합성·운영성 중 무엇을 우선할지 결정하는 기준점으로 연결된다.

- **📢 섹션 요약 비유**: [[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS는 같은 길이라도 우회로를 비교하는 내비게이션에 가깝다. 중요한 것은 순서를 정하고 책임 범위를 분명히 하는 일이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS를 문법이나 이론 용어로만 이해하면 부족하다. 수천만 건 테이블과 반복 질의가 겹치는 환경에서는 이 개념이 곧 응답시간, 충돌 빈도, 운영 복잡도 차이로 드러난다. 따라서 채택 여부를 결정할 때는 현재 개념이 병목을 줄이는지, 아니면 단지 구조만 복잡하게 만드는지부터 [[396_validation|확인]]해야 한다.

### 기술사 판단 [[435_checklist_based_testing|체크리스트]]

1. 현재 워크로드에서 [[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS가 해결하는 병목이 실제로 존재하는가?
2. `그룹 바이 / 해빙`나 `집합 연산자`으로 더 단순하게 풀 수 없는가?
3. 장애·튜닝·[[229_monitor|모니터]]링 시 [[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS를 관찰할 지표와 [[098_rollback_strategy_pipeline_error_threshold|롤백]] [[268_strategy_pattern|전략]]이 준비되어 있는가?

결론적으로 [[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS는 "무조건 채택"의 대상이 아니라, 보장 가치와 운영 비용을 함께 따져 선택해야 하는 설계 포인트다.

- **📢 섹션 요약 비유**: [[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS는 계산대 대기열을 줄이는 운영 판단에 가깝다. 중요한 것은 순서를 정하고 책임 범위를 분명히 하는 일이다.

---

## Ⅴ. 기대효과 및 결론

[[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS를 올바르게 적용하면 구조를 단순화하고, 정합성을 높이거나 [[282_performance_tactics|성능]]을 안정화하며, 장애 대응 속도까지 개선할 수 있다. 반대로 적용 위치를 잘못 잡으면 중복 설계와 불필요한 복잡도만 늘어난다. 그래서 이 주제는 정의 하나보다도 "어디에 두어야 하는가"라는 배치 감각으로 기억하는 것이 중요하다.

특히 [[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS는 독립 개념처럼 보이지만 실제로는 `그룹 바이 / 해빙`과 `집합 연산자` 사이의 연결점으로 이해해야 오래 남는다. 시험에서는 정의·비교·판단 기준을 함께 말하고, 실무에서는 지표와 운영 시나리오까지 연결할 수 있어야 완성도 있는 답안이 된다.

- **📢 섹션 요약 비유**: [[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS는 목차를 잘 만든 책을 보는 일에 가깝다. 중요한 것은 순서를 정하고 책임 범위를 분명히 하는 일이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[147_aggregate_function_group_by|집계 함수]] ([[147_aggregate_function_group_by|Aggregate Function]]) | 앞뒤 맥락에서 현재 주제의 경계를 선명하게 해 주는 인접 개념이다. |
| [[148_sql_group_by_having_clause|그룹 바이]] ([[522_group_by|GROUP BY]]) / 해빙 (HAVING) | 앞뒤 맥락에서 현재 주제의 경계를 선명하게 해 주는 인접 개념이다. |
| [[163_optimizer_sql_execution_plan_generator|옵티마이저]] ([[088_optimizer|Optimizer]]) | 현재 개념을 실제 [[166_execution_plan_optimizer_navigation_tree|실행 계획]]과 비용으로 해석하는 엔진이다. |
| [[154_database_index_b_tree_search_optimization|인덱스]] ([[154_database_index_b_tree_search_optimization|Index]]) | 접근 경로와 I/O 패턴을 결정하는 대표 [[282_performance_tactics|성능]] 요소다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[그룹 바이 / 해빙]
    │
    ▼
[ROLLUP, CUBE, GROUPING SETS]
    │
    ├──▶ [집합 연산자]
    └──▶ [뷰]
```

[[148_sql_group_by_having_clause|그룹 바이]] / 해빙에서 출발한 논점이 [[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS에서 핵심 판단으로 모이고, 이후 집합 연산자·뷰 같은 확장 주제로 이어지는 흐름을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS는 컴퓨터가 일을 헷갈리지 않게 하려고 만든 약속이에요.
2. 이 약속을 잘 지키면 [[001_dikw_pyramid|데이터]]가 많아도 더 안전하고 빠르게 움직일 수 있어요.
3. 그래서 언제 이 방법을 쓰고 언제 다른 방법을 써야 하는지 아는 것이 중요해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 149 / 600

← **이전**: [[148_sql_group_by_having_clause|148. 그룹 바이 (GROUP BY) / 해빙 (HAVING) - HAVING은 그룹화 결과에 대한 조건]]
**다음**: [[150_sql_set_operators_union_intersect_minus|150. SQL 집합 연산자 - UNION, UNION ALL, INTERSECT, MINUS/EXCEPT]] →

---
