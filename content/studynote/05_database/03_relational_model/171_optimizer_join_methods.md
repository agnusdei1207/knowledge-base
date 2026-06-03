---
title: 171. 옵티마이저 조인 기법 3가지
date: '2026-05-06'
tags:
- studynote-database
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[165_cbo_cost_based_optimizer|비용 기반 옵티마이저]] (CBO, Cost-Based [[088_optimizer|Optimizer]])는 같은 조인 SQL (Structured Query Language) 이라도 예상 결과 건수, [[154_database_index_b_tree_search_optimization|인덱스]] 유무, 정렬 상태, 메모리 여유에 따라 [[431_nested_loop_join|Nested Loop]] (NL) [[521_join|Join]], [[174_hash_join|Hash Join]], [[173_sort_merge_join|Sort Merge Join]] 중 다른 물리 연산을 선택한다.
> 2. **가치**: 조인 방식이 바뀌면 랜덤 입출력 (I/O, Input/Output) 중심의 탐색이 될지, 순차 스캔 + 메모리 매칭이 될지, [[432_sort_merge_join|정렬 후 병합]]이 될지가 갈리므로 응답시간과 서버 자원 소비가 크게 달라진다.
> 3. **판단 포인트**: 소량 선별 결과 + 조인 [[154_database_index_b_tree_search_optimization|인덱스]]면 NL [[521_join|Join]], 대량 동등 조인 + 충분한 메모리면 [[174_hash_join|Hash Join]], 이미 정렬된 대량 [[001_dikw_pyramid|데이터]]이거나 정렬 결과를 재활용할 수 있으면 Sort Merge Join이 유리하며, 잘못된 통계는 이 판단을 가장 쉽게 무너뜨린다.

---

## Ⅰ. 개요 및 필요성

[[163_optimizer_sql_execution_plan_generator|옵티마이저]] 조인 기법 3가지는 **[[369_logic_bomb|논리]]적으로 같은 조인 연산을 실제로 어떤 순서와 자원 패턴으로 수행할지 결정하는 물리 실행 방식**이다. [[083_relationship_in_er_model|관계]]형 [[003_dbms_database_management_system|데이터베이스 관리 시스템]] (RDBMS, Relational [[501_database|Database]] [[372_management|Management]] System) 에서 `A JOIN B ON ...` 는 [[369_logic_bomb|논리]]식 하나로 보이지만, 엔진 내부에서는 "한 건씩 [[154_database_index_b_tree_search_optimization|인덱스]]를 찌를지", "작은 집합을 [[067_hash_table|해시 테이블]]로 만들지", "양쪽을 정렬해 앞에서부터 맞출지"를 반드시 정해야 한다.

이 선택이 중요한 이유는 조인 비용이 전체 SQL [[282_performance_tactics|성능]]을 지배하는 경우가 많기 때문이다. 예를 들어 주문 상세 화면처럼 주문 1건과 회원 1건을 붙이는 조회는 [[154_database_index_b_tree_search_optimization|인덱스]] 기반 NL [[521_join|Join]] 이 매우 빠를 수 있다. 반대로 야간 정산 배치처럼 수천만 건의 판매 이력과 고객 등급 이력을 결합하는 작업은 [[154_database_index_b_tree_search_optimization|인덱스]] 랜덤 I/O가 병목이 되므로 [[174_hash_join|Hash Join]] 이 훨씬 유리하다.

즉 조인 튜닝은 "어떤 조인이 더 고급인가"의 문제가 아니라, **현재 [[001_dikw_pyramid|데이터]] 양과 분포에서 어떤 방식이 가장 싼가**를 판단하는 문제다. 그래서 같은 SQL도 통계 정보, 바인드 값, 메모리 상태가 달라지면 다른 [[166_execution_plan_optimizer_navigation_tree|실행 계획]]을 가질 수 있다.

이 그림은 하나의 [[369_logic_bomb|논리]] 조인이 세 가지 전혀 다른 물리 경로로 바뀌는 이유를 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│      One logical join, three very different physical executions      │
├──────────────────────────────────────────────────────────────────────┤
│ SQL : A JOIN B ON A.key = B.key                                      │
│                                                                      │
│ few rows from A + index probe on B      -> Nested Loop Join          │
│ large equality join + enough memory     -> Hash Join                 │
│ sorted inputs or order reuse available  -> Sort Merge Join           │
│                                                                      │
│ same result set, different I/O pattern, different total cost         │
└──────────────────────────────────────────────────────────────────────┘
```

결국 조인 방식은 결과의 정답을 바꾸지 않지만, 정답에 도달하는 **시간과 자원 소비 구조**를 바꾼다. [[001_dikw_pyramid|데이터]]가 커질수록 이 차이는 "조금 느림"이 아니라 "즉시 완료 vs 장시간 대기" 수준으로 벌어진다.

- **📢 섹션 요약 비유**: 같은 사람 찾기라도 학생 3명 명단이면 한 명씩 전화해도 되지만, 전국민 명단이면 전화가 아니라 주소록 색인이나 [[104_classification_analysis|분류]]표가 필요하듯, 조인도 [[001_dikw_pyramid|데이터]] 크기에 따라 찾는 방식이 달라져야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[165_cbo_cost_based_optimizer|비용 기반 옵티마이저]]는 보통 **예상 결과 건수 → [[176_join_order_optimization|조인 순서]] → 물리 조인 방식** 순으로 판단한다. 먼저 필터 조건을 적용했을 때 각 테이블에서 몇 행이 남을지를 추정하고, 그 결과를 바탕으로 어느 쪽을 먼저 읽을지 정한 뒤, 마지막으로 조인 방식을 결정한다. 따라서 조인 방식은 독립적으로 존재하지 않고 **통계 정보와 액세스 경로 위에 올라가는 마지막 선택**에 가깝다.

| 조인 방식 | 핵심 동작 | 유리한 조건 | 대표 병목 |
| :--- | :--- | :--- | :--- |
| [[431_nested_loop_join|Nested Loop]] (NL) [[521_join|Join]] | 외부 집합 행마다 내부 집합을 반복 탐색 | 외부 결과가 매우 적고, 내부 조인 컬럼 [[154_database_index_b_tree_search_optimization|인덱스]]가 좋을 때 | 반복 [[154_database_index_b_tree_search_optimization|인덱스]] 탐색에 따른 랜덤 I/O |
| [[174_hash_join|Hash Join]] | 작은 입력을 메모리 [[067_hash_table|해시 테이블]]로 만들고 큰 입력을 탐색 | 대량 동등 조인, 풀 스캔이 유리하고 메모리가 충분할 때 | 해시 빌드 공간 부족 시 디스크 스필 |
| [[173_sort_merge_join|Sort Merge Join]] | 양쪽 입력을 조인 키 기준으로 정렬한 뒤 병합 | 이미 정렬된 대량 [[001_dikw_pyramid|데이터]], 정렬 결과 재활용 가능할 때 | 정렬 비용과 임시 공간 사용 |

[[431_nested_loop_join|Nested Loop Join]] 의 핵심은 "작은 쪽을 운전석으로 삼아 큰 쪽을 필요한 만큼만 찌른다"는 점이다. 그래서 외부 집합이 수십 행 수준으로 작고 내부 테이블에 조인 [[154_database_index_b_tree_search_optimization|인덱스]]가 있으면 매우 빠르다. 하지만 외부 결과가 커지면 그만큼 내부 탐색도 반복되므로, [[154_database_index_b_tree_search_optimization|인덱스]]가 있어도 랜덤 I/O 누적 비용이 급격히 커질 수 있다.

[[174_hash_join|Hash Join]] 은 작은 입력을 먼저 읽어 메모리 안에 [[067_hash_table|해시 테이블]]을 만들고, 큰 입력을 순차 스캔하며 매칭한다. 이 방식은 [[154_database_index_b_tree_search_optimization|인덱스]]보다 메모리를 활용하는 [[268_strategy_pattern|전략]]이라서 대용량 동등 조인에 강하다. 다만 빌드 입력이 예상보다 크거나 [[001_dikw_pyramid|데이터]] 쏠림이 심하면 해시 영역이 디스크로 밀려나 [[282_performance_tactics|성능]]이 흔들릴 수 있다.

[[173_sort_merge_join|Sort Merge Join]] 은 양쪽을 같은 키 순서로 정렬해 놓고, 앞에서부터 비교하며 병합한다. 정렬 비용이 선행되지만, 이미 [[154_database_index_b_tree_search_optimization|인덱스]] 정렬이나 상위 연산의 요구 때문에 순서가 맞춰져 있다면 의외로 효율적이다. 특히 조인 후 바로 `ORDER BY`, `GROUP BY`, 스트림 병합이 이어지는 경우에는 정렬 비용을 여러 연산이 같이 써서 손해를 줄일 수 있다.

아래 그림은 [[163_optimizer_sql_execution_plan_generator|옵티마이저]]가 조인 방식을 고를 때 실제로 보는 분기 구조를 단순화한 것이다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                How the optimizer reasons about a join                │
├──────────────────────────────────────────────────────────────────────┤
│ row estimate -> join order -> physical join method                   │
│                                                                      │
│ small outer + index on inner  -----------------> Nested Loop Join    │
│ equality join + build side fits memory --------> Hash Join           │
│ sorted streams / order reuse available --------> Sort Merge Join     │
└──────────────────────────────────────────────────────────────────────┘
```

핵심은 "좋은 조인 방식"이 따로 있는 것이 아니라, **현재 입력 상태에 맞는 방식**이 있다는 점이다. 그래서 조인 [[167_sql_hint_optimizer_override|힌트]]보다 먼저 [[170_selectivity_cardinality_distribution_tuning|선택도]], [[077_radix|기수]]성, 분포도, 메모리 작업 영역이 왜 그렇게 보이는지를 [[396_validation|확인]]해야 한다.

- **📢 섹션 요약 비유**: 손님이 적은 카페는 주문을 한 사람씩 받아도 되지만, 단체 손님이 몰리면 미리 음료를 [[104_classification_analysis|분류]]해 놓거나 줄을 정렬해 처리해야 하듯, 조인 방식도 손님 수와 매장 구조에 맞춰 바뀐다.

---

## Ⅲ. 비교 및 연결

세 방식의 차이는 단순히 "빠름/느림"이 아니라 **무엇을 병목으로 삼는가**에 있다. NL [[521_join|Join]] 은 반복 탐색 비용, [[174_hash_join|Hash Join]] 은 메모리와 해시 균형, [[173_sort_merge_join|Sort Merge Join]] 은 정렬 비용이 핵심 변수다. 따라서 [[154_database_index_b_tree_search_optimization|인덱스]] 유무만 보고 조인 방식을 예단하면 자주 실패한다.

| 비교 축 | [[431_nested_loop_join|Nested Loop Join]] | [[174_hash_join|Hash Join]] | [[173_sort_merge_join|Sort Merge Join]] |
| :--- | :--- | :--- | :--- |
| 기본 관점 | 행 단위 반복 탐색 | 집합 단위 메모리 매칭 | 정렬 후 순차 병합 |
| 강한 상황 | 소량 조회, 높은 [[170_selectivity_cardinality_distribution_tuning|선택도]], 내부 [[154_database_index_b_tree_search_optimization|인덱스]] 존재 | 대량 동등 조인, 순차 스캔 유리 | 이미 정렬된 입력, 정렬 재활용 가능 |
| 약한 상황 | 외부 집합이 커질 때 | 메모리 부족, [[001_dikw_pyramid|데이터]] 쏠림 심할 때 | 정렬이 새로 필요할 때 |
| 대표 업무 | 온라인 [[191_transaction_concept_states|트랜잭션]] 처리 ([[327_hint_handoff|OLTP]], Online [[191_transaction_concept_states|Transaction]] Processing) | [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] ([[209_data_warehouse_schema_on_write|DW]], [[208_data_warehouse_schema_on_write_inmon|Data Warehouse]]), 배치 분석 | 대량 병합, 정렬 연계 작업 |
| 통계 민감도 | [[176_join_order_optimization|조인 순서]] 오판에 매우 민감 | 빌드/프로브 크기 추정 오류에 민감 | 정렬 필요성 판단 오류에 민감 |

이 세 방식은 앞 문서의 [[170_selectivity_cardinality_distribution_tuning|선택도]], [[077_radix|기수]]성, 분포도와 직접 연결된다. [[170_selectivity_cardinality_distribution_tuning|선택도]]가 낮아 외부 결과가 소량이면 NL [[521_join|Join]] 이 좋아질 가능성이 크고, [[170_selectivity_cardinality_distribution_tuning|선택도]]가 높아 대량 집합이 남으면 [[174_hash_join|Hash Join]] 이 유리해진다. 또 값 분포가 치우쳐 있으면 해시 버킷 편향이나 [[176_join_order_optimization|조인 순서]] 오판이 생겨, 같은 [[174_hash_join|Hash Join]] 이라도 예상보다 느려질 수 있다.

[[169_clustering_factor_index_physical_sort|클러스터링 팩터]] ([[169_clustering_factor_index_physical_sort|Clustering Factor]]) 와도 연결해서 봐야 한다. NL [[521_join|Join]] 이 [[154_database_index_b_tree_search_optimization|인덱스]]를 잘 타더라도 실제 [[001_dikw_pyramid|데이터]] 블록이 흩어져 있으면 테이블 랜덤 접근 비용이 커진다. 반대로 [[173_sort_merge_join|Sort Merge Join]] 은 정렬 비용이 부담이지만, 상위 연산도 같은 순서를 원한다면 전체 [[123_pipe|파이프]]라인에서는 이득일 수 있다.

즉 조인 기법 비교는 한 문장으로 끝나지 않는다. **[[001_dikw_pyramid|데이터]]량, [[154_database_index_b_tree_search_optimization|인덱스]], 정렬 상태, 메모리, 통계 품질이 한 번에 맞물려야 최적의 그림이 나온다**는 점이 핵심이다.

- **📢 섹션 요약 비유**: 집까지 가는 길을 고를 때 오토바이, 화물차, 기차 중 무엇이 좋은지는 물건 양과 도로 상태에 따라 달라지듯, 조인도 운반할 [[001_dikw_pyramid|데이터]]의 규모와 길의 형태를 같이 봐야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 조인 방식 자체보다 **왜 그 방식이 선택되었는지 설명할 수 있어야** 한다. 예를 들어 회원 한 명의 주문 이력을 보는 화면에서 `member_id = :id` 로 이미 1건 수준으로 선별되었다면, 주문 테이블 [[154_database_index_b_tree_search_optimization|인덱스]]를 활용하는 NL [[521_join|Join]] 이 자연스럽다. 반면 월말 정산처럼 판매 사실 테이블 수억 건과 고객 [[273_dimension_table_analysis_perspective|차원 테이블]] 수천만 건을 동등 조인하는 배치는 [[174_hash_join|Hash Join]] 이 기본 후보가 된다.

[[173_sort_merge_join|Sort Merge Join]] 은 종종 "애매한 옛 방식"으로 오해받지만, 대량 [[001_dikw_pyramid|데이터]]가 이미 조인 키 순서로 정렬되어 있거나 결과를 곧바로 정렬된 상태로 넘겨야 할 때는 여전히 의미가 있다. 예를 들어 [[514_partition_slice_volume|파티션]] 병합, 대량 [[568_logs_distributed_logging_elk_fluentd|로그]] 병합, 정렬 기반 집계 앞단에서는 정렬 비용을 여러 연산이 나눠 쓸 수 있기 때문이다.

### 기술사 판단 [[435_checklist_based_testing|체크리스트]]

1. 필터 이후 실제로 남는 외부 집합은 몇 행인가?
2. 내부 집합 조인 컬럼에 탐색 가능한 [[154_database_index_b_tree_search_optimization|인덱스]]가 있는가?
3. 조인이 동등 조건 중심이며, 작은 입력을 메모리에 담을 수 있는가?
4. 이미 정렬된 입력이나 이후 정렬 재활용 가능성이 있는가?
5. 통계 정보가 최신이며 값 쏠림과 상관관계를 반영하고 있는가?

### 채택 / 회피 판단

- **[[431_nested_loop_join|Nested Loop Join]] 채택**: 소량 조회, 높은 [[170_selectivity_cardinality_distribution_tuning|선택도]], 조인 [[154_database_index_b_tree_search_optimization|인덱스]] 확보, 빠른 응답이 중요한 화면 조회
- **[[174_hash_join|Hash Join]] 채택**: 대량 동등 조인, [[154_database_index_b_tree_search_optimization|인덱스]] 반복 탐색보다 풀 스캔이 싼 분석/배치
- **[[173_sort_merge_join|Sort Merge Join]] 채택**: 이미 정렬된 대량 [[001_dikw_pyramid|데이터]], 정렬 재활용 가능, 순차 병합이 유리한 흐름
- **회피**: "[[154_database_index_b_tree_search_optimization|인덱스]]가 있으니 무조건 NL", "대용량이니 무조건 Hash"처럼 [[001_dikw_pyramid|데이터]] 조건을 무시한 단정

### 자주 나오는 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 통계가 오래되어 작은 집합을 큰 집합으로 오판한 상태에서 [[167_sql_hint_optimizer_override|힌트]]만 덮어쓰는 경우
- [[174_hash_join|Hash Join]] 빌드 입력이 메모리에 안 들어가는데도 강제로 사용해 스필을 키우는 경우
- [[173_sort_merge_join|Sort Merge Join]] 의 정렬 비용은 무시하고 결과 정렬 재활용 가능성도 보지 않는 경우
- 조인 방식보다 더 중요한 [[176_join_order_optimization|조인 순서]] 문제를 놓치는 경우

좋은 튜닝은 특정 조인 방식을 숭배하는 것이 아니라, **왜 지금 이 시점에 이 방식이 맞는지 재현 가능하게 설명하는 것**이다. 그리고 설명이 안 되면 대부분 통계 또는 [[001_dikw_pyramid|데이터]]량 가정이 틀린 경우가 많다.

- **📢 섹션 요약 비유**: 사람 두 명을 태울 때는 승용차가 맞지만, 이삿짐을 옮기면서도 승용차만 고집하면 비효율이 커지듯, 조인도 실어 나를 양에 맞는 탈것을 골라야 한다.

---

## Ⅴ. 기대효과 및 결론

[[163_optimizer_sql_execution_plan_generator|옵티마이저]] 조인 기법 3가지를 제대로 이해하면 [[166_execution_plan_optimizer_navigation_tree|실행 계획]]에서 조인 연산자를 보는 순간, 왜 그 [[298_qkv_attention|쿼리]]가 빠르거나 느린지 설명할 수 있게 된다. 이는 단순 [[282_performance_tactics|성능]] 개선을 넘어, 계획 변동 원인 분석, [[167_sql_hint_optimizer_override|힌트]] 최소화, 통계 관리 우선순위 [[009_config|설정]]으로 이어진다.

물론 한계도 있다. 최신 [[002_database_definition|데이터베이스]]는 적응형 조인 (Adaptive [[521_join|Join]]), 동적 샘플링, [[430_index_fast_full_scan|병렬]] 조인 같은 보정 장치를 제공하지만, 잘못된 기초 통계나 극단적인 [[001_dikw_pyramid|데이터]] 쏠림까지 완전히 없애 주지는 못한다. 결국 물리 조인 방식 선택은 자동화되었어도, 그 전제가 되는 [[001_dikw_pyramid|데이터]] 이해는 여전히 사람의 몫이다.

이 주제는 "세 가지 조인 이름 암기"로 끝나면 부족하다. **조인 방식은 [[001_dikw_pyramid|데이터]] 크기, [[154_database_index_b_tree_search_optimization|인덱스]], 메모리, 정렬 상태에 반응하는 비용 모델의 결과**라는 관점으로 기억해야 실제 튜닝 판단에 연결된다.

- **📢 섹션 요약 비유**: 같은 목적지라도 걸어갈지, 자전거를 탈지, 기차를 탈지는 거리와 짐의 양이 정하듯, 조인 방식도 SQL 문장보다 [[001_dikw_pyramid|데이터]] 상황이 결정한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[165_cbo_cost_based_optimizer|비용 기반 옵티마이저]] (CBO, Cost-Based [[088_optimizer|Optimizer]]) | [[176_join_order_optimization|조인 순서]]와 조인 방식을 비용으로 비교해 선택 |
| [[170_selectivity_cardinality_distribution_tuning|선택도]] ([[170_selectivity_cardinality_distribution_tuning|Selectivity]]) | 외부 입력 크기를 줄여 NL [[521_join|Join]] 유불리를 바꿈 |
| [[077_radix|기수]]성 (Cardinality) | 조인 결과 행 수 예측의 출발점 |
| [[169_clustering_factor_index_physical_sort|클러스터링 팩터]] ([[169_clustering_factor_index_physical_sort|Clustering Factor]]) | [[154_database_index_b_tree_search_optimization|인덱스]] 기반 NL [[521_join|Join]] 의 실제 블록 접근 비용에 영향 |
| 해시 작업 영역 | [[174_hash_join|Hash Join]] 의 빌드 테이블 적재 가능 여부를 좌우 |
| 정렬 재활용 | [[173_sort_merge_join|Sort Merge Join]] 의 비용을 상쇄하는 핵심 조건 |

### 📈 관련 키워드 및 발전 흐름도

```text
Logical Join
    │
    ▼
Cardinality / Selectivity Estimate
    │
    ▼
Join Order Decision
    │
    ├─ small outer + index probe -> Nested Loop Join
    ├─ large equality + memory    -> Hash Join
    └─ sorted inputs + order use  -> Sort Merge Join
    │
    ▼
Stable execution plan and join tuning
```

이 흐름은 [[369_logic_bomb|논리]]적 조인이 통계 기반 비용 판단을 거쳐 실제 물리 조인 방식으로 구체화되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 친구가 몇 명 안 되면 한 명씩 이름표를 보고 짝을 찾아도 금방 끝나요.
2. 친구가 아주 많으면 작은 명단을 먼저 표로 만들어 놓고 큰 명단을 훑는 게 더 빨라요.
3. 두 줄이 이미 번호순으로 서 있다면 앞에서부터 같이 걸어가며 맞추면 된다고 생각하면 돼요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 171 / 600

← **이전**: [[170_selectivity_cardinality_distribution_tuning|170. 선택도 (Selectivity) / 기수성 (Cardinality) / 분포도 (Distribution)]]
**다음**: [[172_nl_join_nested_loop|172. 중첩 루프 조인 (NL Join, Nested Loop Join)]] →

---
