---
title: 166. 실행 계획 (Execution Plan) - 옵티마이저가 생성한 네비게이션 트리
date: '2026-04-03'
tags:
- studynote-database
---

## 핵심 인사이트

> 1. **본질**: 실행 계획 (Execution Plan)은 [[003_dbms_database_management_system|데이터베이스 관리 시스템]] ([[502_dbms|DBMS]], [[501_database|Database]] [[372_management|Management]] System)의 [[165_cbo_cost_based_optimizer|비용 기반 옵티마이저]] (CBO, Cost Based [[088_optimizer|Optimizer]])가 SQL (Structured Query Language)을 어떤 물리 경로로 실행할지 트리 형태로 표현한 항로도다.
> 2. **가치**: 느린 SQL의 원인은 문법보다 접근 경로, [[176_join_order_optimization|조인 순서]], 예상 행 수 오판에 숨어 있으므로, 실행 계획은 병목을 가장 빨리 드러내는 [[282_performance_tactics|성능]] 진단 도구다.
> 3. **판단 포인트**: 실행 계획은 어디까지나 예상값이므로 비용 (Cost) 숫자만 맹신하지 말고, 예상 카디널리티 (Cardinality)와 실제 [[139_throughput|처리량]]이 얼마나 어긋나는지까지 함께 봐야 한다.

---

## Ⅰ. 개요 및 필요성

실행 계획 (Execution Plan)은 [[083_relationship_in_er_model|관계]]형 [[003_dbms_database_management_system|데이터베이스 관리 시스템]] (RDBMS, Relational [[501_database|Database]] [[372_management|Management]] System)이 SQL을 실제로 읽을 때 선택한 접근 경로, [[176_join_order_optimization|조인 순서]], 조인 방식, 정렬 연산을 트리로 보여 주는 결과물이다. 개발자는 SQL로 "무엇을 구할지"만 적지만, [[002_database_definition|데이터베이스]]는 그 요청을 처리하기 위해 어떤 [[154_database_index_b_tree_search_optimization|인덱스]]를 탈지, 어느 테이블을 먼저 읽을지, [[174_hash_join|해시 조인]] ([[174_hash_join|Hash Join]])과 [[172_nl_join_nested_loop|중첩 루프 조인]] ([[431_nested_loop_join|Nested Loop Join]]) 중 무엇을 쓸지 별도로 결정한다. 실행 계획은 바로 그 보이지 않는 물리 경로를 눈에 보이게 만든다.

이 문서가 중요한 이유는 같은 SQL이라도 [[001_dikw_pyramid|데이터]] 분포와 통계 정보에 따라 전혀 다른 [[282_performance_tactics|성능]]이 나올 수 있기 때문이다. 예를 들어 주문 1천만 건 중 10건만 찾는 조회라면 [[154_database_index_b_tree_search_optimization|인덱스]] 범위 스캔 ([[429_index_range_scan|Index Range Scan]])이 유리하지만, 300만 건을 읽는 조건이라면 전체 테이블 스캔 (Full Table Scan)이 더 빠를 수 있다. 실행 계획 없이 SQL만 보면 느린 이유를 추측할 수밖에 없지만, 실행 계획을 보면 병목이 접근 경로인지, [[176_join_order_optimization|조인 순서]]인지, 정렬 연산인지 구체적으로 판단할 수 있다.

이 그림은 실행 계획이 SQL 문장 자체가 아니라, SQL 뒤에서 움직이는 실제 처리 경로를 보여 준다는 점을 설명한다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│             SQL과 실행 계획의 관계: 선언형 요청 vs 물리 경로         │
├──────────────────────────────────────────────────────────────────────┤
│ SQL Text                                                            │
│   SELECT * FROM orders o JOIN customers c ON o.cust_id = c.id       │
│   WHERE c.name = 'KIM';                                             │
│                                                                      │
│        "무엇을 구할까?"                                             │
│                │                                                     │
│                ▼                                                     │
│ Optimizer                                                            │
│   ├─ customer name index scan                                        │
│   ├─ customer row fetch                                               │
│   ├─ orders access path decision                                      │
│   └─ join method selection                                            │
│                │                                                     │
│                ▼                                                     │
│ Execution Plan = "어떤 순서와 방법으로 읽을까?"                    │
└──────────────────────────────────────────────────────────────────────┘
```

즉 실행 계획은 SQL 문법 해설서가 아니라, [[002_database_definition|데이터베이스]]의 물리적 의사결정을 보여 주는 X선 사진이다. 그래서 SQL 튜닝의 시작점은 보통 SQL 문장 자체보다 실행 계획을 먼저 보는 데서 출발한다.

- **📢 섹션 요약 비유**: 실행 계획은 주문서가 아니라 주방의 조리 동선표와 같다. 손님은 메뉴 이름만 말하지만, 주방장은 어떤 재료를 먼저 꺼내고 어떤 불을 먼저 켤지 따로 판단한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

실행 계획은 보통 **연산자 ([[329_delta_encoding|Operation]]) + 객체 (Object) + 예상 행 수 + 비용 + 조건식**으로 구성된다. 여기서 핵심은 트리를 어떻게 읽느냐이다. 일반적으로 가장 아래쪽 리프 노드 (Leaf Node)에서 [[001_dikw_pyramid|데이터]] 접근이 시작되고, 부모 연산자가 자식 연산자의 결과를 받아 위로 합성해 간다. 따라서 `SELECT STATEMENT`가 가장 위에 있다고 해서 그 줄부터 실행되는 것이 아니라, 실제 작업은 테이블 접근과 [[154_database_index_b_tree_search_optimization|인덱스]] 스캔처럼 가장 안쪽의 연산부터 시작된다.

| 구성 요소 | 의미 | 해석 포인트 |
| :--- | :--- | :--- |
| [[329_delta_encoding|Operation]] | 수행 연산 종류 | Table Access, [[154_database_index_b_tree_search_optimization|Index]] Scan, [[521_join|Join]], Sort [[396_validation|확인]] |
| Object Name | 실제 대상 객체 | 어떤 테이블·[[154_database_index_b_tree_search_optimization|인덱스]]를 건드리는지 파악 |
| Rows | 예상 결과 건수 | 카디널리티 예측이 맞는지 [[395_verification_process_review|검증]] |
| Cost | [[163_optimizer_sql_execution_plan_generator|옵티마이저]]의 상대적 비용 | 같은 계획 안에서 병목 후보 판단 |
| Predicate | 접근/필터 조건 | [[154_database_index_b_tree_search_optimization|인덱스]] 활용 여부와 후처리 필터 구분 |

아래 그림은 실행 계획이 위에서 아래로 읽는 문서가 아니라, 아래에서 위로 결과가 합쳐지는 네비게이션 트리임을 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                 실행 계획 읽기: 리프에서 루트로 올라감               │
├──────────────────────────────────────────────────────────────────────┤
│ Id  Operation                         Object         Exec Order      │
│  0  SELECT STATEMENT                                   ▲             │
│  1   HASH JOIN                                         │ ④           │
│  2    TABLE ACCESS BY INDEX ROWID       CUSTOMERS      │ ②           │
│  3     INDEX RANGE SCAN                 IDX_CUST_NAME  │ ①           │
│  4    TABLE ACCESS FULL                 ORDERS         │ ③           │
│                                                                      │
│ 흐름: IDX_CUST_NAME → CUSTOMERS → ORDERS → HASH JOIN → RESULT        │
└──────────────────────────────────────────────────────────────────────┘
```

이 트리에서 `INDEX RANGE SCAN`이 먼저 고객 후보를 찾고, `TABLE ACCESS BY INDEX ROWID`가 실제 고객 행을 읽는다. 그 다음 주문 테이블 전체를 읽어 [[174_hash_join|해시 조인]]을 수행하고, 마지막에 최종 결과를 반환한다. 여기서 핵심은 **들여쓰기와 부모-자식 [[083_relationship_in_er_model|관계]]**를 통해 [[001_dikw_pyramid|데이터]]가 어디서 만들어지고 어디서 소비되는지를 보는 것이다.

또 하나 중요한 축은 [[170_selectivity_cardinality_distribution_tuning|선택도]] ([[170_selectivity_cardinality_distribution_tuning|Selectivity]])와 카디널리티다. 조건식이 전체 [[001_dikw_pyramid|데이터]]의 0.01%만 고른다면 [[154_database_index_b_tree_search_optimization|인덱스]]가 유리할 가능성이 높고, 30% 이상을 읽는다면 랜덤 I/O보다 순차 스캔이 나을 수 있다. [[163_optimizer_sql_execution_plan_generator|옵티마이저]]는 이 예측값으로 비용을 계산하므로, 카디널리티가 틀리면 그 위의 조인 방식과 정렬 [[268_strategy_pattern|전략]]도 함께 흔들린다.

- **📢 섹션 요약 비유**: 실행 계획 트리는 레고 조립 설명서와 같다. 마지막 완성 사진이 맨 위에 있어도, 실제 손은 가장 아래의 작은 부품부터 끼워 올려야 완성된다.

---

## Ⅲ. 비교 및 연결

실행 계획을 제대로 이해하려면 **예상 계획**과 **실제 실행 통계**를 구분해야 한다. `EXPLAIN PLAN`은 [[163_optimizer_sql_execution_plan_generator|옵티마이저]]가 실행 전에 예상한 길이고, 실제 실행 통계는 [[298_qkv_attention|쿼리]]가 끝난 뒤 정말 몇 행을 읽었고 어떤 연산에서 시간이 썼는지 보여 준다. 예상 계획은 빠른 구조 진단에 좋고, 실제 통계는 예측이 맞았는지 [[395_verification_process_review|검증]]하는 데 강하다.

| 비교 항목 | 예상 실행 계획 | 실제 실행 통계 |
| :--- | :--- | :--- |
| [[087_process_state_transition|생성]] 시점 | 실행 전 | 실행 후 |
| 장점 | 빠르게 구조를 [[396_validation|확인]] 가능 | 실제 병목과 행 수 왜곡 [[396_validation|확인]] 가능 |
| 한계 | 통계 오류를 그대로 반영 | 실행 비용이 들고 상황 재현이 필요 |
| 주 용도 | [[154_database_index_b_tree_search_optimization|인덱스]] 누락, 조인 구조 점검 | 예측 오차, 실제 시간 분포 분석 |

또한 실행 계획은 [[165_cbo_cost_based_optimizer|비용 기반 옵티마이저]], [[167_sql_hint_optimizer_override|힌트]] ([[167_sql_hint_optimizer_override|Hint]]), 통계 정보와 직접 연결된다. [[165_cbo_cost_based_optimizer|비용 기반 옵티마이저]]는 통계에 따라 실행 계획을 만들고, [[167_sql_hint_optimizer_override|힌트]]는 그 선택을 부분적으로 강제한다. 따라서 실행 계획을 읽는다는 것은 단순히 트리 모양을 읽는 것이 아니라, **[[163_optimizer_sql_execution_plan_generator|옵티마이저]]가 왜 그 선택을 했는지 역추적하는 일**과 같다.

실무에서 자주 만나는 경계 비교는 `TABLE ACCESS FULL`과 `INDEX RANGE SCAN`, `Nested Loop Join`과 `Hash Join`이다. 소량 탐색에서는 [[154_database_index_b_tree_search_optimization|인덱스]]와 중첩 루프가 빠르지만, 대량 결합에서는 [[174_hash_join|해시 조인]]과 순차 스캔이 더 낫다. 결국 실행 계획의 가치는 "어떤 연산이 무조건 좋다"를 외우는 데 있는 것이 아니라, **현재 [[001_dikw_pyramid|데이터]]량에서 어떤 연산이 맞는지 판단하는 기준**을 제공하는 데 있다.

- **📢 섹션 요약 비유**: 예상 실행 계획은 내비게이션의 추천 경로이고, 실제 실행 통계는 주행 후에 [[396_validation|확인]]한 블랙박스 기록과 같다. 둘을 같이 봐야 길이 왜 막혔는지 정확히 알 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

가장 흔한 실무 시나리오는 "어제까지 빠르던 SQL이 오늘 갑자기 느려진 경우"다. 예를 들어 쇼핑몰 주문 조회 [[298_qkv_attention|쿼리]]가 평소에는 고객 [[154_database_index_b_tree_search_optimization|인덱스]]를 타다가, [[001_dikw_pyramid|데이터]] 적재량 증가와 통계 부정확성 때문에 갑자기 주문 테이블 전체 스캔으로 바뀌면 응답시간이 수십 배로 튈 수 있다. 이때 단순히 [[154_database_index_b_tree_search_optimization|인덱스]]를 더 만들기보다, 먼저 실행 계획에서 **어느 단계의 예상 행 수가 틀어졌는지**를 [[396_validation|확인]]해야 한다.

### 실무 점검 순서

1. 가장 비용이 큰 연산이 접근 경로인지, 조인인지, 정렬인지 구분한다.
2. 예상 행 수와 실제 행 수가 크게 차이 나는 노드를 찾는다.
3. 조건절 가공, 함수 사용, 복합 [[154_database_index_b_tree_search_optimization|인덱스]] 선두 컬럼 문제를 [[396_validation|확인]]한다.
4. 통계 갱신으로 해결될지, [[154_database_index_b_tree_search_optimization|인덱스]] 재설계가 필요한지, [[167_sql_hint_optimizer_override|힌트]]가 필요한 응급 상황인지 나눈다.

### 판단 원칙

- **우선 채택**: 통계가 신뢰 가능하고 실행 계획이 안정적이면 [[163_optimizer_sql_execution_plan_generator|옵티마이저]]의 선택을 존중한다.
- **보완 필요**: 특정 단계에서 카디널리티 오차가 크면 통계, 히스토그램 (Histogram), SQL 구조를 먼저 수정한다.
- **최후 수단**: 장애 회피가 급한 경우에만 [[167_sql_hint_optimizer_override|힌트]]로 경로를 고정하고, 이후 근본 원인을 제거한다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- `Cost` 숫자만 보고 무조건 가장 큰 값만 없애려는 접근
- 실제 실행 통계 없이 예상 계획만 보고 [[282_performance_tactics|성능]]을 단정하는 행동
- `SELECT *` 남발, 함수 기반 조건, 불필요한 정렬로 계획을 왜곡하는 [[298_qkv_attention|쿼리]] 작성

기술사 관점에서는 "실행 계획을 볼 줄 안다"보다 한 단계 더 들어가야 한다. 즉, 트리를 읽고 병목을 찾는 것에서 끝나지 않고 **왜 [[163_optimizer_sql_execution_plan_generator|옵티마이저]]가 그렇게 판단했는지**, 그리고 **통계·[[154_database_index_b_tree_search_optimization|인덱스]]·[[167_sql_hint_optimizer_override|힌트]] 중 무엇으로 개입할지**까지 말할 수 있어야 설계 답안으로 완성된다.

- **📢 섹션 요약 비유**: 실행 계획 분석은 병원 진료와 같다. 열이 난다고 무조건 해열제부터 먹이는 것이 아니라, 엑스레이와 검사표를 보고 원인이 폐인지 목인지 먼저 구분해야 한다.

---

## Ⅴ. 기대효과 및 결론

실행 계획을 읽을 수 있으면 SQL 튜닝이 감각의 영역에서 증거의 영역으로 바뀐다. 병목이 전체 스캔인지, 불필요한 정렬인지, 잘못된 [[176_join_order_optimization|조인 순서]]인지 빠르게 분리할 수 있어 문제 해결 속도가 크게 빨라진다. 이는 응답시간 단축뿐 아니라 불필요한 [[154_database_index_b_tree_search_optimization|인덱스]] 추가 감소, 서버 증설 [[015_지연_데이터_관점|지연]], 장애 대응 시간 단축으로 이어진다.

다만 실행 계획만으로 모든 문제가 해결되지는 않는다. 계획은 예상 모델이므로 실제 캐시 상태, [[430_index_fast_full_scan|병렬]]도, 런타임 바인드 값, 통계 편향까지 완벽히 설명하지 못할 수 있다. 그래서 실행 계획은 종착점이 아니라, 실제 실행 통계와 함께 보는 [[282_performance_tactics|성능]] 분석의 중심 축으로 기억해야 한다.

앞으로 적응형 [[298_qkv_attention|쿼리]] 처리 (Adaptive Query Processing), 실행 중 재최적화, 실제 행 수 피드백 기능이 발전하더라도 본질은 같다. 실행 계획은 [[002_database_definition|데이터베이스]]가 SQL을 어떻게 "생각하고 움직였는지"를 보여 주는 가장 직접적인 인터페이스다.

- **📢 섹션 요약 비유**: 실행 계획은 경기 결과표가 아니라 작전판과 같다. 작전판을 읽을 수 있어야 왜 이겼고 왜 졌는지 설명할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[165_cbo_cost_based_optimizer|비용 기반 옵티마이저]] (CBO, Cost Based [[088_optimizer|Optimizer]]) | 실행 계획을 [[087_process_state_transition|생성]]하는 핵심 판단 엔진 |
| 카디널리티 (Cardinality) | 각 노드의 예상 행 수로 계획 정확도를 좌우 |
| [[170_selectivity_cardinality_distribution_tuning|선택도]] ([[170_selectivity_cardinality_distribution_tuning|Selectivity]]) | [[154_database_index_b_tree_search_optimization|인덱스]] 사용 여부와 접근 경로 판단의 기준 |
| [[176_join_order_optimization|조인 순서]] ([[176_join_order_optimization|Join Order]]) | 구동 테이블 선택과 전체 비용에 직접 영향 |
| [[167_sql_hint_optimizer_override|힌트]] ([[167_sql_hint_optimizer_override|Hint]]) | [[163_optimizer_sql_execution_plan_generator|옵티마이저]]의 기본 판단을 강제로 조정하는 수단 |
| 실제 실행 통계 | 예상 계획과 현실 [[282_performance_tactics|성능]]의 차이를 [[395_verification_process_review|검증]]하는 근거 |

### 📈 관련 키워드 및 발전 흐름도

```text
규칙 기반 최적화
    │
    ▼
비용 기반 옵티마이저 (CBO, Cost Based Optimizer)
    │
    ▼
실행 계획 (Execution Plan)
    │
    ├─ 접근 경로 (Access Path)
    ├─ 조인 순서 (Join Order)
    └─ 조인 방식 (Join Method)
    │
    ▼
실제 실행 통계 · 적응형 최적화 · 계획 안정화
```

이 흐름은 [[002_database_definition|데이터베이스]] 튜닝이 단순 문법 수정에서, [[163_optimizer_sql_execution_plan_generator|옵티마이저]] 판단과 실제 실행 결과를 함께 해석하는 방향으로 발전해 왔음을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 실행 계획은 컴퓨터가 보물을 찾으러 갈 때 어떤 길로 갈지 그린 지도예요.
2. 지도만 보면 빨라 보여도, 실제 길에 사람이 많으면 오래 걸릴 수 있어요.
3. 그래서 지도와 실제 다녀온 기록을 같이 봐야 진짜 빠른 길을 찾을 수 있답니다.
