+++
weight = 179
title = "179. 파티셔닝 (Partitioning) - 대용량 테이블 물리적 분할 관리 기법"
date = "2026-05-06"
[extra]
categories = "studynote-database"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 파티셔닝 (Partitioning)은 [[369_logic_bomb|논리]]적으로 하나의 테이블을 유지하면서, 물리적으로는 [[514_partition_slice_volume|파티션]] 키 ([[514_partition_slice_volume|Partition]] [[067_db_key_uniqueness_minimality|Key]]) 기준으로 여러 저장 구간으로 나누어 읽기 범위와 관리 범위를 줄이는 기법이다.
> 2. **가치**: 잘 설계된 파티셔닝은 [[184_partition_pruning|파티션 프루닝]] ([[184_partition_pruning|Partition Pruning]]), [[514_partition_slice_volume|파티션]] 단위 [[555_backup_and_restore_strategy|백업]]·보관·삭제, [[430_index_fast_full_scan|병렬]] 처리에 유리해져서 대용량 테이블의 [[282_performance_tactics|성능]]과 운영성을 함께 높인다.
> 3. **판단 포인트**: 핵심은 "[[514_partition_slice_volume|파티션]]을 쓰느냐"보다 "어떤 키를 어떤 단위로 자르느냐"다. 조회 조건이 [[514_partition_slice_volume|파티션]] 키와 어긋나거나 특정 [[514_partition_slice_volume|파티션]]에 부하가 몰리면 효과는 급격히 줄어든다.

---

## Ⅰ. 개요 및 필요성

파티셔닝은 대용량 테이블을 여러 개의 물리 구간으로 나누어 관리하는 저장 [[268_strategy_pattern|전략]]이다. 애플리케이션과 SQL (Structured Query Language) 관점에서는 여전히 하나의 테이블처럼 보이지만, RDBMS (Relational [[501_database|Database]] [[372_management|Management]] System) 내부에서는 월별·분기별·지역별 같은 기준으로 분리된 [[514_partition_slice_volume|파티션]]에 저장된다. 즉 "테이블을 쪼갠다"기보다 **한 테이블의 물리 배치를 계층화한다**는 표현이 더 정확하다.

이 기법이 필요한 이유는 대용량 테이블의 문제점이 단순 조회 속도 하나로 끝나지 않기 때문이다. 거래 이력, [[568_logs_distributed_logging_elk_fluentd|로그]], 센서 [[001_dikw_pyramid|데이터]]처럼 시간이 갈수록 누적되는 테이블은 전체 스캔 범위가 커지고, [[154_database_index_b_tree_search_optimization|인덱스]]도 비대해지며, 오래된 [[001_dikw_pyramid|데이터]]를 지우는 작업조차 비싼 `DELETE` 가 된다. [[555_backup_and_restore_strategy|백업]]과 [[658_ir_recovery|복구]]도 테이블 전체를 대상으로 하면 시간이 길어지고, 운영 중 유지보수 작업이 [[090_service_kubernetes_network_load_balancing|서비스]]와 충돌하기 쉽다.

아래 그림은 왜 파티셔닝이 "검색 최적화"이면서 동시에 "운영 최적화"인지 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Large order history table                                          │
├────────────────────────────────────────────────────────────────────┤
│ 비파티션 테이블                                                     │
│   [2019 ~ 2026 주문 행이 한 공간에 혼재]                            │
│   └─ 2026-05 조회라도 넓은 범위를 뒤질 가능성 증가                 │
│                                                                    │
│ 파티션 테이블                                                       │
│   [P2019][P2020][P2021][P2022][P2023][P2024][P2025][P2026_05]      │
│                                             └─ 조회 시 이 구간 중심 │
│                                                                    │
│ 운영 작업                                                           │
│   오래된 2019 데이터 삭제  →  대량 DELETE                          │
│   오래된 2019 파티션 삭제  →  DROP PARTITION                       │
└────────────────────────────────────────────────────────────────────┘
```

중요한 점은 파티셔닝이 무조건 모든 [[298_qkv_attention|쿼리]]를 빠르게 만드는 만능 약이 아니라는 점이다. 파티셔닝의 진짜 목적은 **읽을 범위를 줄이고, 보관 주기를 분리하며, 운영 단위를 잘게 나누는 것**이다. 그래서 대개 시계열 테이블, 대규모 이력 테이블, 보관 [[164_policy|정책]]이 분명한 업무 [[001_dikw_pyramid|데이터]]에서 특히 효과가 크다.

- **📢 섹션 요약 비유**: 파티셔닝은 거대한 서류 창고를 한 칸으로 두는 대신, 연도별 서랍으로 나누는 것과 같다. 찾을 때는 필요한 서랍만 열고, 폐기할 때는 낡은 서랍째 치우면 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

파티셔닝의 핵심은 [[514_partition_slice_volume|파티션]] 키와 [[514_partition_slice_volume|파티션]] 함수다. `order_date`, `region_code`, `customer_group` 같은 컬럼을 기준으로 "이 행은 어느 [[514_partition_slice_volume|파티션]]에 저장될지"를 정한다. 입력 시에는 [[514_partition_slice_volume|파티션]] 함수가 적절한 저장 구간으로 행을 [[339_routing_overview_best_path_selection|라우팅]]하고, 조회 시에는 [[163_optimizer_sql_execution_plan_generator|옵티마이저]]가 `WHERE` 조건을 보고 읽지 않아도 되는 [[514_partition_slice_volume|파티션]]을 제거한다. 이때 발생하는 최적화가 [[184_partition_pruning|파티션 프루닝]]이다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Partition routing and pruning                                      │
├────────────────────────────────────────────────────────────────────┤
│ INSERT row(order_date = '2026-05-06', customer = 'K01')            │
│         │                                                          │
│         ▼                                                          │
│ partition function(order_date)                                     │
│   ├─ 2025 이하        ───────────────▶ P_HIST                       │
│   ├─ 2026-01 ~ 2026-03 ────────────▶ P_2026_Q1                     │
│   └─ 2026-04 ~ 2026-06 ────────────▶ P_2026_Q2                     │
│                                              ▲                     │
│                                              └─ 실제 저장 위치      │
│                                                                    │
│ SELECT ... WHERE order_date BETWEEN '2026-05-01' AND '2026-05-31'  │
│   └─ 옵티마이저가 P_HIST, P_2026_Q1 을 제외하고 P_2026_Q2 중심 탐색 │
└────────────────────────────────────────────────────────────────────┘
```

대표적인 분할 방식은 다음과 같다.

| 방식 | 분할 기준 | 장점 | 주의점 | 잘 맞는 예 |
| :--- | :--- | :--- | :--- | :--- |
| 범위 파티셔닝 ([[180_range_partitioning|Range Partitioning]]) | 날짜, 금액 구간 | 시계열 [[001_dikw_pyramid|데이터]]와 보관 [[164_policy|정책]]에 강함 | 특정 최신 구간에 부하 집중 가능 | 주문일자 월별 분할 |
| 목록 파티셔닝 ([[182_list_partitioning|List Partitioning]]) | 지역, 상태 코드 | 업무 규칙과 관리 단위가 명확함 | 코드 추가 시 [[514_partition_slice_volume|파티션]] [[164_policy|정책]] 관리 필요 | 국내/해외, 채널별 분할 |
| [[181_hash_partitioning|해시 파티셔닝]] ([[181_hash_partitioning|Hash Partitioning]]) | [[667_hash_function_integrity_one_way|해시 함수]] 결과 | [[001_dikw_pyramid|데이터]] [[136_variance|분산]]이 비교적 고름 | 범위 조회 프루닝에는 불리함 | 고객번호 균등 [[136_variance|분산]] |
| 복합 파티셔닝 ([[183_composite_partitioning|Composite Partitioning]]) | 범위 + 해시, 범위 + 목록 | 보관성과 [[136_variance|분산]]성을 동시에 고려 가능 | 설계와 운영 복잡도 증가 | 월별 [[514_partition_slice_volume|파티션]] 안 고객 해시 [[136_variance|분산]] |

실무에서는 [[154_database_index_b_tree_search_optimization|인덱스]] [[268_strategy_pattern|전략]]도 함께 따라온다. 로컬 [[154_database_index_b_tree_search_optimization|인덱스]] (Local [[154_database_index_b_tree_search_optimization|Index]])는 각 [[514_partition_slice_volume|파티션]]과 나란히 관리되어 [[514_partition_slice_volume|파티션]] 삭제·교체에 유리하고, 글로벌 [[154_database_index_b_tree_search_optimization|인덱스]] ([[185_global_vs_local_index|Global Index]])는 [[514_partition_slice_volume|파티션]] 전체를 가로지르는 탐색에 유리하지만 유지보수 비용이 더 크다. 따라서 파티셔닝은 테이블만 자르는 일이 아니라 **저장 구조, [[154_database_index_b_tree_search_optimization|인덱스]] 구조, 유지보수 방식까지 함께 재설계하는 작업**이다.

또 하나 자주 연결되는 개념이 [[514_partition_slice_volume|파티션]] 와이즈 조인 ([[514_partition_slice_volume|Partition]]-Wise [[521_join|Join]]) 이다. 두 테이블이 같은 키와 같은 방식으로 분할되어 있으면, [[002_database_definition|데이터베이스]]는 서로 대응되는 [[514_partition_slice_volume|파티션]]끼리만 조인해 중간 결과를 크게 줄일 수 있다. 즉 파티셔닝은 단일 테이블 최적화에서 끝나지 않고, 조인 구조까지 바꿀 수 있는 물리 설계 기법이다.

- **📢 섹션 요약 비유**: 손님 명단을 정리할 때 입장 순서대로 한 권에 적는 대신, 월별 [[501_file_definition_logical_record|파일]]철로 나누면 새 손님은 맞는 [[501_file_definition_logical_record|파일]]에 꽂고, 5월 손님을 찾을 때는 5월 [[501_file_definition_logical_record|파일]]만 뒤지면 된다.

---

## Ⅲ. 비교 및 연결

파티셔닝은 종종 인덱싱 (Indexing) 이나 [[280_sharding|샤딩]] ([[243_sharding_horizontal_scaling_database|Sharding]]) 과 혼동된다. 하지만 셋은 해결하려는 문제가 다르다. [[154_database_index_b_tree_search_optimization|인덱스]]는 "어디에 있는가"를 빠르게 찾는 구조이고, 파티셔닝은 "얼마나 넓은 공간을 읽고 관리할 것인가"를 줄이는 구조이며, [[280_sharding|샤딩]]은 "한 서버가 감당할 수 없는 규모를 여러 서버로 나눌 것인가"를 다루는 [[136_variance|분산]] 구조다.

| 구분 | [[369_logic_bomb|논리]] 테이블 | 주요 목적 | 분할 단위 | 핵심 효과 |
| :--- | :--- | :--- | :--- | :--- |
| 인덱싱 (Indexing) | 하나 | 검색 경로 단축 | [[154_database_index_b_tree_search_optimization|인덱스]] [[286_page_frame|페이지]] | [[170_selectivity_cardinality_distribution_tuning|선택도]] 높은 조건 탐색 가속 |
| 파티셔닝 (Partitioning) | 하나 | 읽기 범위·관리 범위 축소 | [[514_partition_slice_volume|파티션]] | 프루닝, 보관, [[555_backup_and_restore_strategy|백업]], [[430_index_fast_full_scan|병렬]]성 |
| [[280_sharding|샤딩]] ([[243_sharding_horizontal_scaling_database|Sharding]]) | 여러 샤드로 [[136_variance|분산]] | 서버 간 확장 | [[058_database_instance_architecture|데이터베이스 인스턴스]] | 용량·[[139_throughput|처리량]] 수평 확장 |

이 차이가 중요한 이유는 파티셔닝이 [[154_database_index_b_tree_search_optimization|인덱스]]를 대체하지 않기 때문이다. 예를 들어 `order_date` 기준으로 월별 [[514_partition_slice_volume|파티션]]을 해도, 특정 고객의 주문을 빠르게 찾으려면 여전히 고객번호 [[154_database_index_b_tree_search_optimization|인덱스]]가 필요할 수 있다. 반대로 [[154_database_index_b_tree_search_optimization|인덱스]]가 잘 잡혀 있어도, 3년 지난 [[001_dikw_pyramid|데이터]]를 월말마다 정리해야 하는 운영 문제는 파티셔닝이 훨씬 직접적으로 해결한다.

파티셔닝은 [[001_dikw_pyramid|데이터]] 생애주기 관리와도 강하게 연결된다. [[675_hot_data_caching|핫 데이터]] ([[675_hot_data_caching|Hot Data]]) 는 빠른 스토리지에, [[676_cold_data_archiving|콜드 데이터]] ([[676_cold_data_archiving|Cold Data]]) 는 저비용 스토리지에 두는 정보 수명주기 관리 (ILM, Information [[927_medical_device_lifecycle|Lifecycle Management]]) 를 설계할 때, [[514_partition_slice_volume|파티션]]은 물리적인 경계선 역할을 한다. 따라서 파티셔닝은 [[282_performance_tactics|성능]]만이 아니라 **보관, 아카이빙, 규제 대응**의 관점에서도 이해해야 한다.

- **📢 섹션 요약 비유**: [[154_database_index_b_tree_search_optimization|인덱스]]는 책 뒤의 찾아보기이고, 파티셔닝은 책장을 연도별로 나눠 꽂는 것이며, [[280_sharding|샤딩]]은 아예 도서관을 여러 지점으로 나누는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 가장 먼저 해야 할 질문은 "주요 조회와 주요 운영 작업이 무엇을 기준으로 움직이는가"다. 주문·[[568_logs_distributed_logging_elk_fluentd|로그]]·과금 [[001_dikw_pyramid|데이터]]처럼 대부분의 조회가 날짜 범위로 들어오고, 보관 [[164_policy|정책]]도 월 단위로 끊긴다면 범위 파티셔닝이 자연스럽다. 반대로 특정 고객군에 부하가 몰려 [[289_cqrs_db|쓰기]] [[136_variance|분산]]이 중요하다면 해시 또는 복합 파티셔닝이 더 적합할 수 있다.

예를 들어 최근 24개월 주문 [[001_dikw_pyramid|데이터]]만 자주 조회하고, 25개월 이전 [[001_dikw_pyramid|데이터]]는 아카이브 대상인 시스템이라면 `order_date` 기준 월별 파티셔닝이 운영상 유리하다. 이 경우 월말 정산 이후 오래된 [[001_dikw_pyramid|데이터]]는 `DROP PARTITION` 또는 `EXCHANGE PARTITION` 으로 빠르게 분리·이관할 수 있다. 반대로 조회가 대부분 `customer_id` 기준인데 날짜 [[514_partition_slice_volume|파티션]]만 두면, 프루닝 이득은 약하고 최신 [[514_partition_slice_volume|파티션]]에 [[289_cqrs_db|쓰기]]만 몰리는 핫스폿이 생길 수 있다.

### 기술사 판단 [[435_checklist_based_testing|체크리스트]]

1. [[514_partition_slice_volume|파티션]] 키가 실제 `WHERE`, `JOIN`, 보관 [[164_policy|정책]]과 일치하는가?
2. 일별·월별·분기별 중 어느 단위가 관리성과 [[514_partition_slice_volume|파티션]] 수 사이 균형이 맞는가?
3. [[514_partition_slice_volume|파티션]] 키 조건을 함수로 감싸지 않아 프루닝이 가능하도록 SQL 을 작성했는가?
4. 로컬 [[154_database_index_b_tree_search_optimization|인덱스]]와 글로벌 [[154_database_index_b_tree_search_optimization|인덱스]] 중 [[346_maintainability_portability|유지보수성]]과 전역 탐색 요구사항에 맞는 구조를 골랐는가?
5. 최신 [[514_partition_slice_volume|파티션]]에만 [[289_cqrs_db|쓰기]]가 집중되는 핫 [[514_partition_slice_volume|파티션]] 현상을 감당할 수 있는가?
6. [[514_partition_slice_volume|파티션]] 추가, 병합, 분할, 교체 작업의 운영 절차와 장애 [[658_ir_recovery|복구]] 시나리오가 준비되어 있는가?

### 자주 나오는 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 조회에 거의 쓰이지 않는 컬럼을 [[514_partition_slice_volume|파티션]] 키로 잡아 프루닝 효과를 못 보는 경우
- 지나치게 잘게 나누어 수천 개 이상의 [[514_partition_slice_volume|파티션]] [[203_metadata_management|메타데이터 관리]] 비용이 커지는 경우
- `TO_CHAR(order_date, 'YYYYMM')` 같은 비정규 조건 때문에 [[184_partition_pruning|파티션 프루닝]]을 방해하는 경우
- 파티셔닝만 하면 [[282_performance_tactics|성능]]이 자동으로 해결된다고 믿고 [[154_database_index_b_tree_search_optimization|인덱스]]·통계·SQL 구조를 방치하는 경우

결국 파티셔닝 설계의 핵심은 **[[298_qkv_attention|쿼리]] 최적화와 운영 최적화를 같은 키로 묶을 수 있느냐**다. 기술사 답안에서는 "[[282_performance_tactics|성능]] 향상"만 쓰지 말고, [[514_partition_slice_volume|파티션]] 단위 [[555_backup_and_restore_strategy|백업]]·[[658_ir_recovery|복구]], [[001_dikw_pyramid|데이터]] 보관, [[514_partition_slice_volume|파티션]] 수 관리, [[154_database_index_b_tree_search_optimization|인덱스]] [[268_strategy_pattern|전략]]까지 함께 제시해야 설득력이 높아진다.

- **📢 섹션 요약 비유**: 냉장고 정리는 음식 종류와 유통기한을 같이 봐야 한다. 자주 꺼내는 칸과 오래 두는 칸을 같은 기준으로 나눠야 정리도 쉽고 찾기도 빠르다.

---

## Ⅴ. 기대효과 및 결론

파티셔닝이 잘 설계되면 [[002_database_definition|데이터베이스]]는 필요한 구간만 읽고, 필요한 구간만 [[555_backup_and_restore_strategy|백업]]하고, 필요 없는 구간은 빠르게 제거할 수 있다. 그 결과 Input/Output 감소, [[430_index_fast_full_scan|병렬]] 처리 효율 향상, 유지보수 시간 단축, 아카이빙 단순화 같은 효과가 함께 따라온다. 특히 대용량 이력 [[001_dikw_pyramid|데이터]]에서는 "한 번의 대수술" 대신 "작은 관리 단위들의 일상 운영"으로 문제를 바꿔 준다는 점이 크다.

하지만 한계도 분명하다. [[514_partition_slice_volume|파티션]] 키와 무관한 조회는 효과가 작고, 전역 유니크 제약이나 글로벌 [[154_database_index_b_tree_search_optimization|인덱스]] 유지비용이 커질 수 있으며, 잘못 설계된 파티셔닝은 오히려 운영 복잡도만 높인다. 또한 이미 비대한 단일 테이블을 뒤늦게 재파티셔닝하는 작업은 [[189_egress|데이터 이동 비용]]이 크므로, [[459_quic_fec_forward_error_correction|초기]]에 [[001_dikw_pyramid|데이터]] 성장 패턴을 읽고 설계하는 편이 훨씬 유리하다.

따라서 파티셔닝은 "테이블을 잘게 쪼개는 기술"로 기억하기보다, **대용량 테이블의 검색 범위와 생애주기를 물리 구조에 반영하는 설계 기법**으로 이해하는 것이 맞다. 앞으로는 자동 [[514_partition_slice_volume|파티션]] 관리, 계층형 스토리지, [[514_partition_slice_volume|파티션]] 단위 [[347_compaction|압축]]과 결합해 더 큰 운영 효과를 낼 수 있다.

- **📢 섹션 요약 비유**: 좋은 서랍장은 물건을 예쁘게 나누는 데서 끝나지 않는다. 자주 쓰는 물건은 손 닿는 곳에 두고, 오래된 물건은 통째로 꺼내기 쉽게 만들어야 진짜 실용적이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[514_partition_slice_volume|파티션]] 키 ([[514_partition_slice_volume|Partition]] [[067_db_key_uniqueness_minimality|Key]]) | 행이 어느 [[514_partition_slice_volume|파티션]]에 저장될지 결정하는 기준 컬럼 |
| [[184_partition_pruning|파티션 프루닝]] ([[184_partition_pruning|Partition Pruning]]) | 조회 시 불필요한 [[514_partition_slice_volume|파티션]]을 제외해 읽기 범위를 줄이는 핵심 최적화 |
| 로컬 [[154_database_index_b_tree_search_optimization|인덱스]] (Local [[154_database_index_b_tree_search_optimization|Index]]) | [[514_partition_slice_volume|파티션]]과 함께 관리되어 유지보수에 유리한 [[154_database_index_b_tree_search_optimization|인덱스]] 구조 |
| 글로벌 [[154_database_index_b_tree_search_optimization|인덱스]] ([[185_global_vs_local_index|Global Index]]) | 여러 [[514_partition_slice_volume|파티션]]을 가로지르는 탐색과 전역 제약에 유리한 [[154_database_index_b_tree_search_optimization|인덱스]] 구조 |
| 복합 파티셔닝 ([[183_composite_partitioning|Composite Partitioning]]) | 보관성과 [[136_variance|분산]]성을 동시에 얻기 위한 다단계 분할 방식 |
| [[514_partition_slice_volume|파티션]] 와이즈 조인 ([[514_partition_slice_volume|Partition]]-Wise [[521_join|Join]]) | 대응되는 [[514_partition_slice_volume|파티션]]끼리 조인해 중간 결과를 줄이는 방식 |
| 정보 수명주기 관리 (ILM, Information [[927_medical_device_lifecycle|Lifecycle Management]]) | [[514_partition_slice_volume|파티션]]을 이용해 핫·[[676_cold_data_archiving|콜드 데이터]] 배치를 운영하는 상위 개념 |
| [[280_sharding|샤딩]] ([[243_sharding_horizontal_scaling_database|Sharding]]) | 인스턴스 간 [[136_variance|분산]]이라는 점에서 파티셔닝과 구분되는 수평 확장 [[268_strategy_pattern|전략]] |

### 📈 관련 키워드 및 발전 흐름도

```text
대용량 단일 테이블
        │
        ▼
파티션 키 선정
        │
        ▼
범위 · 목록 · 해시 · 복합 파티셔닝
        │
        ├──────────────► INSERT 라우팅
        │
        └──────────────► WHERE 조건 기반 파티션 프루닝
                                │
                                ▼
                 파티션 단위 백업 · 보관 · 삭제 · 병렬 처리
```

이 흐름도는 "성장한 단일 테이블 → 분할 기준 선택 → 물리 분할 → 조회·운영 최적화"라는 파티셔닝의 핵심 진화 경로를 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 장난감을 한 상자에 다 넣어 두면 찾기 힘들어서, 자동차 상자와 블록 상자로 나누어 넣는 거예요.
2. 그러면 자동차를 찾을 때 자동차 상자만 열어 보면 되고, 오래된 장난감은 상자째 치우기 쉬워요.
3. 하지만 자주 찾는 기준이 아니라 엉뚱한 기준으로 나누면 상자를 나눠도 여전히 찾기 힘들어요.
