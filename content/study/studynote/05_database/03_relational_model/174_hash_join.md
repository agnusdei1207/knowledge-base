+++
weight = 174
title = "174. 해시 조인 (Hash Join) - 작은 테이블로 해시 맵 생성 후 큰 테이블 탐색, 대량 데이터/동등(=) 조인 전용, 성능 우수"
date = "2026-05-06"
[extra]
categories = "studynote-database"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 해시 조인 (Hash [[521_join|Join]])은 작은 입력을 메모리 버킷 [[067_hash_table|해시 테이블]]로 만든 뒤, 큰 입력을 한 번 훑으며 같은 조인 키를 찾는 **동등 조인 (Equality [[521_join|Join]]) 특화 물리 연산**이다.
> 2. **가치**: 랜덤 입출력 (I/O, Input/Output) 과 대규모 정렬 비용을 피할 수 있어, 대량 사실 테이블과 [[273_dimension_table_analysis_perspective|차원 테이블]]을 결합하는 분석계 질의에서 특히 강하다.
> 3. **판단 포인트**: [[282_performance_tactics|성능]]은 "어느 쪽을 Build Input으로 잡는가", "메모리에 다 들어가는가", "[[001_dikw_pyramid|데이터]] 편향이 심한가"에 크게 좌우되며, 비동등 조건에는 원천적으로 맞지 않는다.

---

## Ⅰ. 개요 및 필요성

해시 조인은 [[083_relationship_in_er_model|관계]]형 [[003_dbms_database_management_system|데이터베이스 관리 시스템]] (RDBMS, Relational [[501_database|Database]] [[372_management|Management]] System) 이 대량 조인을 빠르게 처리하기 위해 사용하는 대표적인 물리 조인 방식이다. 핵심 아이디어는 단순하다. **작은 집합은 먼저 기억해 두고, 큰 집합은 지나가면서 즉석에서 대조한다.** 이 때문에 해시 조인은 보통 `=` 조건의 대량 조인에서 가장 먼저 검토된다.

이 방식이 필요한 이유는 다른 조인 [[268_strategy_pattern|전략]]의 병목이 분명하기 때문이다. [[431_nested_loop_join|Nested Loop Join]] 은 외부 행마다 내부 집합을 반복 탐색하므로, 결과 건수가 많아지면 랜덤 I/O 가 급증한다. [[173_sort_merge_join|Sort Merge Join]] 은 대량 조인과 범위 조인에 강하지만, 정렬이 선행되어야 하므로 입력이 이미 정렬돼 있지 않으면 [[459_quic_fec_forward_error_correction|초기]] 비용이 크다.

반면 해시 조인은 양쪽을 모두 풀 스캔하더라도, 작은 입력만 메모리에 적절히 올릴 수 있다면 조인 비용을 **Build + Probe** 형태의 비교적 단순한 흐름으로 바꿀 수 있다. 그래서 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] ([[209_data_warehouse_schema_on_write|DW]], [[208_data_warehouse_schema_on_write_inmon|Data Warehouse]]), 일괄 처리, [[334_star_schema|스타 스키마]] 질의에서 자주 선택된다.

- **📢 섹션 요약 비유**: 시험장에서 답안지 두 묶음을 하나씩 맞대는 대신, 먼저 정답표를 손에 들고 있다가 학생 답안을 지나가며 바로 채점하는 방식과 같다. 정답표가 손에 들어와야 빠르지만, 정답표가 너무 두꺼우면 오히려 들고 있기 힘들다.

---

## Ⅱ. 아키텍처 및 핵심 원리

해시 조인은 보통 **Build Phase → Probe Phase → Spill 대응**의 세 관점으로 이해하면 된다. 여기서 Build Input 은 더 작은 쪽, Probe Input 은 더 큰 쪽으로 잡는 것이 기본 원칙이다. [[667_hash_function_integrity_one_way|해시 함수]] 결과가 같다고 해서 키가 반드시 같은 것은 아니므로, 버킷 안에서는 최종 키 비교를 한 번 더 수행한다.

| 단계 | 엔진이 하는 일 | [[282_performance_tactics|성능]] 포인트 | 주요 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] |
| :--- | :--- | :--- | :--- |
| Build Phase | 작은 입력의 조인 키에 [[667_hash_function_integrity_one_way|해시 함수]]를 적용해 메모리 버킷 구성 | 작은 입력을 좁은 폭으로 투영하면 메모리 효율 향상 | Build Input 선택 실패 시 메모리 압박 |
| Probe Phase | 큰 입력을 스캔하며 같은 해시 버킷을 조회 | 순차 스캔 + 메모리 탐색이라 [[139_throughput|처리량]]이 높음 | [[563_hash_collision_chaining_linear_probing|해시 충돌]], [[001_dikw_pyramid|데이터]] 편향으로 특정 버킷 과밀 |
| Spill / [[514_partition_slice_volume|Partition]] | 메모리 초과 시 입력을 [[514_partition_slice_volume|파티션]]으로 나눠 디스크에 임시 저장 후 재처리 | Grace Hash [[521_join|Join]] 으로 대형 입력도 처리 가능 | 임시 공간 사용과 추가 I/O 로 [[282_performance_tactics|성능]] 급락 |

아래 구조는 해시 조인의 핵심 흐름을 보여 준다. 이 그림에서 중요한 점은 "해시 값 일치"가 곧 "조인 성공"이 아니라, **같은 버킷으로 모은 뒤 실제 키를 다시 비교한다**는 사실이다.

```text
┌────────────────────────────────────────────────────────────────────┐
│                Hash Join: build once, probe many                   │
├────────────────────────────────────────────────────────────────────┤
│ Build input (small)                                                │
│   row -> hash(join_key) -> bucket[7] -> keep key + payload         │
│   row -> hash(join_key) -> bucket[2] -> keep key + payload         │
│                                                                    │
│ Probe input (large)                                                │
│   row -> hash(join_key) -> same bucket -> compare real key -> join │
│                                                                    │
│ If hash area overflows:                                            │
│   partition build/probe inputs -> reload one partition at a time   │
│   -> rehash -> probe again                                         │
└────────────────────────────────────────────────────────────────────┘
```

[[166_execution_plan_optimizer_navigation_tree|실행 계획]]을 볼 때는 Build 쪽이 정말 작은지, 그리고 불필요한 컬럼이 제거되어 있는지를 먼저 [[396_validation|확인]]해야 한다. 예를 들어 [[273_dimension_table_analysis_perspective|차원 테이블]]에서 조인 키와 필요한 소수 컬럼만 먼저 읽으면, 같은 행 수여도 [[067_hash_table|해시 테이블]] 폭이 줄어 메모리 적재성이 좋아진다. 반대로 `SELECT *` 성격으로 넓은 행을 그대로 Build 하면 해시 조인의 장점이 쉽게 사라진다.

메모리를 넘는 경우에는 Grace Hash [[521_join|Join]] 처럼 양쪽 입력을 같은 해시 기준으로 여러 [[514_partition_slice_volume|파티션]]으로 쪼갠 뒤, 각 [[514_partition_slice_volume|파티션]]별로 다시 Build/Probe 한다. 즉 해시 조인의 본질은 "한 번에 다 메모리에 넣는다"가 아니라, **메모리에 맞는 단위로 동일 버킷끼리 만나게 만든다**는 데 있다.

- **📢 섹션 요약 비유**: 큰 창고 물건을 찾을 때 먼저 물건 종류별 상자를 만들어 두고, 들어오는 주문서를 해당 상자만 열어 [[396_validation|확인]]하는 방식과 같다. 다만 상자가 창고보다 많아지면 임시 창고를 빌려 다시 나눠 담아야 한다.

---

## Ⅲ. 비교 및 연결

해시 조인의 위치를 정확히 보려면 [[431_nested_loop_join|Nested Loop Join]], [[173_sort_merge_join|Sort Merge Join]] 과의 차이를 함께 봐야 한다. 세 방식은 모두 같은 조인 결과를 만들지만, **비용을 어디에 쓰는가**가 다르다.

| 비교 축 | [[431_nested_loop_join|Nested Loop Join]] | Hash [[521_join|Join]] | [[173_sort_merge_join|Sort Merge Join]] |
| :--- | :--- | :--- | :--- |
| 핵심 [[268_strategy_pattern|전략]] | 외부 행마다 내부 탐색 반복 | 작은 입력을 해시 버킷화 후 큰 입력 탐색 | 양쪽을 정렬한 뒤 순차 병합 |
| 잘 맞는 조건 | 소량 결과 + 좋은 [[154_database_index_b_tree_search_optimization|인덱스]] | 대량 **동등 조인** + 충분한 작업 메모리 | 대량 조인 + 비동등 조건 또는 정렬 재사용 |
| 입출력 패턴 | 랜덤 I/O 많음 | 풀 스캔 + 메모리 조회 | 풀 스캔 + 정렬 + 순차 병합 |
| 결과 순서 활용 | 거의 없음 | 없음 | `ORDER BY`, `GROUP BY` 재활용 가능 |
| 대표 약점 | 외부 집합이 커지면 급격히 비싸짐 | 메모리 초과와 [[001_dikw_pyramid|데이터]] 편향에 민감 | 정렬 비용과 임시 공간 부담 |

즉 해시 조인은 "정렬이 필요 없는 [[173_sort_merge_join|Sort Merge Join]]" 이 아니라, **동등 비교를 버킷 탐색으로 바꾼 별도의 문제 해결 방식**이다. 그래서 `A.id = B.id` 같은 조건에서는 매우 강하지만, `A.date BETWEEN B.start AND B.end` 같은 범위 조인에서는 쓸 수 없다. 이 경계가 명확해야 [[163_optimizer_sql_execution_plan_generator|옵티마이저]] [[167_sql_hint_optimizer_override|힌트]]나 [[166_execution_plan_optimizer_navigation_tree|실행 계획]]을 올바르게 해석할 수 있다.

또한 해시 조인은 현대 분석 엔진에서 [[061_bloomfilter|Bloom Filter]], [[430_index_fast_full_scan|병렬]] [[179_table_partitioning_concept|파티셔닝]], 벡터화 실행과도 자주 연결된다. 예를 들어 [[136_variance|분산]] 질의 엔진은 먼저 작은 입력으로 [[061_bloomfilter|Bloom Filter]] 를 만들어 큰 입력 스캔 전에 불필요한 키를 걸러 낸다. 즉 해시 조인은 단일 연산자라기보다, **대량 동등 조인을 위한 확장 가능한 계열**로 발전해 왔다.

- **📢 섹션 요약 비유**: 사람 찾기에도 여러 방식이 있다. 한 명씩 교실을 돌며 찾을지, 번호순으로 줄 세워 찾을지, 아니면 반별 명부를 먼저 만들어 해당 반만 열어볼지가 다르다. 해시 조인은 "먼저 반별 명부를 만들어 두는 방식"에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 해시 조인이 빛나는 장면은 보통 **큰 사실 테이블 + 작은 [[273_dimension_table_analysis_perspective|차원 테이블]]** 조합이다. 예를 들어 1억 건 판매 이력과 10만 건 상품 [[172_maas_mobility_as_a_service|마스]]터를 `product_id = product_id` 로 붙이는 질의라면, 상품 [[172_maas_mobility_as_a_service|마스]]터를 Build Input 으로 [[067_hash_table|해시 테이블]]에 올리고 판매 이력을 Probe 하는 구조가 매우 자연스럽다. 이때 [[154_database_index_b_tree_search_optimization|인덱스]]를 수없이 찌르는 것보다 양쪽을 순차 스캔하는 편이 더 예측 가능하고 빠를 수 있다.

반대로 단순히 `=` 조건이라고 해서 항상 해시 조인이 정답은 아니다. 주문 10건에 대한 회원 정보 조회처럼 결과가 소량이고 적절한 [[154_database_index_b_tree_search_optimization|인덱스]]가 있다면 [[431_nested_loop_join|Nested Loop Join]] 이 더 빠를 수 있다. 또 조인 뒤에 바로 정렬된 결과를 재사용해야 한다면 [[173_sort_merge_join|Sort Merge Join]] 이 유리할 수 있다. 결국 해시 조인의 판단 기준은 "대량 동등 조인인가?"와 "Build 쪽이 메모리에 안정적으로 올라가는가?" 두 가지로 [[347_compaction|압축]]된다.

### 기술사 판단 [[435_checklist_based_testing|체크리스트]]

1. 조인 조건이 순수 동등 조인인가?
2. Build Input 을 더 작은 집합으로 명확히 잡을 수 있는가?
3. Build 쪽에서 불필요한 컬럼을 줄여 [[067_hash_table|해시 테이블]] 폭을 축소했는가?
4. 통계 정보가 최신이라 [[165_cbo_cost_based_optimizer|비용 기반 옵티마이저]] (CBO, Cost-Based [[088_optimizer|Optimizer]]) 가 입력 크기를 정확히 아는가?
5. 특정 키에 [[001_dikw_pyramid|데이터]]가 몰리는 편향(skew) 때문에 버킷 과부하가 생기지 않는가?
6. 조인 후 결과 순서가 꼭 필요한가, 아니면 순서가 불필요한가?

### 자주 나오는 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- `BETWEEN`, `<`, `>` 조건에 해시 조인을 강제로 유도하는 경우
- Build Input 이 더 큰데도 [[167_sql_hint_optimizer_override|힌트]]로 잘못 고정해 메모리 스필을 유발하는 경우
- `SELECT *` 로 넓은 행을 그대로 Build 해 해시 영역을 낭비하는 경우
- [[001_dikw_pyramid|데이터]] 편향과 임시 공간 사용량을 보지 않고 "해시 조인은 무조건 빠르다"고 믿는 경우

기술사 관점에서 기억할 문장은 간단하다. **해시 조인은 대량 동등 조인을 빠르게 만들지만, 메모리와 편향을 잘못 다루면 가장 빠른 조인이 가장 비싼 조인으로 뒤집힐 수 있다.**

- **📢 섹션 요약 비유**: 반 배정표를 벽에 붙여 두고 학생들을 빠르게 교실로 보내는 방식은 대규모 행사에서 매우 효율적이다. 하지만 반 배정표가 너무 커서 벽에 다 안 붙거나, 특정 반에 학생이 몰리면 입장 줄이 다시 꼬이기 시작한다.

---

## Ⅴ. 기대효과 및 결론

해시 조인은 대량 동등 조인을 **순차 스캔 + 메모리 조회** 패턴으로 바꿔 주기 때문에, 분석성 질의의 [[139_throughput|처리량]]을 크게 높여 준다. 특히 정렬이 불필요하고 결과 순서가 중요하지 않은 경우, [[173_sort_merge_join|Sort Merge Join]] 보다 준비 비용이 적고 [[431_nested_loop_join|Nested Loop Join]] 보다 랜덤 I/O 부담이 작다.

하지만 장점의 전제조건도 명확하다. 작은 Build Input, 충분한 작업 메모리, 낮은 [[001_dikw_pyramid|데이터]] 편향, 정확한 통계 정보가 함께 있어야 한다. 이 조건이 무너지면 해시 스필, 버킷 불균형, 잘못된 Build 선택으로 [[282_performance_tactics|성능]]이 급격히 나빠질 수 있다.

결론적으로 해시 조인은 "가장 빠른 조인"이 아니라, **동등 조인을 버킷 탐색 문제로 변환해 가장 빠르게 만들 수 있는 조인**으로 기억하는 것이 정확하다. 그래서 실무에서는 조인 조건, 입력 크기, 메모리 적재성, 결과 순서 요구를 함께 보고 판단해야 한다.

- **📢 섹션 요약 비유**: 해시 조인은 큰 전화번호부를 통째로 뒤지는 대신, 성씨별 서랍을 먼저 만들어 놓고 바로 해당 서랍만 여는 방식이다. 서랍 정리가 잘되면 놀랍도록 빠르지만, 서랍 구성이 틀어지면 오히려 더 어수선해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Build Input | [[067_hash_table|해시 테이블]]을 먼저 만드는 작은 입력 집합 |
| Probe Input | Build 쪽 버킷을 조회하며 스캔하는 큰 입력 집합 |
| [[165_cbo_cost_based_optimizer|비용 기반 옵티마이저]] (CBO, Cost-Based [[088_optimizer|Optimizer]]) | 입력 크기와 메모리 비용을 보고 Hash [[521_join|Join]] 채택 여부를 판단 |
| [[173_sort_merge_join|Sort Merge Join]] | 범위 조인과 정렬 재사용에서 Hash [[521_join|Join]] 의 대안이 됨 |
| Grace Hash [[521_join|Join]] | 메모리 초과 시 [[514_partition_slice_volume|파티션]] 분할로 Hash [[521_join|Join]] 을 확장하는 기법 |
| [[061_bloomfilter|Bloom Filter]] | 대량 Probe 입력을 사전 필터링해 Hash [[521_join|Join]] 비용을 낮추는 보조 기법 |
| [[001_dikw_pyramid|데이터]] 편향 (Skew) | 특정 버킷에 [[001_dikw_pyramid|데이터]]가 몰려 [[430_index_fast_full_scan|병렬]]성과 [[139_throughput|처리량]]을 떨어뜨리는 원인 |

### 📈 관련 키워드 및 발전 흐름도

```text
Large equality join requirement
            │
            ▼
Choose smaller build input
            │
            ▼
Build in-memory hash buckets
            │
            ▼
Probe large scan against buckets
            │
            ├───────────────► if memory overflow -> partition and rehash
            ▼
Parallel hash join / Bloom filter optimization
```

이 흐름은 "대량 동등 조인 필요 → 작은 입력 해시화 → 큰 입력 탐색 → 메모리 초과 대응 → [[430_index_fast_full_scan|병렬]] 최적화"로 이어지는 해시 조인의 사고 순서를 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 먼저 작은 장난감 상자를 색깔별 칸에 나눠 넣어 두어요.
2. 이제 큰 장난감 [[459_dummy_test_double|더미]]를 보면서 같은 색 칸만 바로 열어 보면 돼요.
3. 그래서 모든 장난감을 처음부터 다시 찾지 않아도 빨리 짝을 맞출 수 있어요.
