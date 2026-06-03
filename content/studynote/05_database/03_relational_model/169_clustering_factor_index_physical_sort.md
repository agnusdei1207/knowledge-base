+++
title = "169. 클러스터링 팩터 (Clustering Factor) - 인덱스 정렬 순서와 실제 물리적 데이터 정렬 순서의 일치 정도"
date = 2026-04-03

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클러스터링 팩터 ([Clustering](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/) Factor, CF)는 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 가리키는 순서와 실제 테이블 행이 저장된 블록 순서가 얼마나 닮았는지를 나타내는 물리 접근 효율 지표다.
> 2. **가치**: CF가 좋으면 범위 조회가 같은 블록을 재사용하며 순차적으로 읽히고, CF가 나쁘면 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 타고도 랜덤 입출력 (I/O, Input/Output)이 폭증해 풀 테이블 스캔보다 느려질 수 있다.
> 3. **판단 포인트**: [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 튜닝은 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) ([Selectivity](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/))만 보는 문제가 아니라, 적재 순서·[파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)·클러스터형 저장 구조까지 함께 설계해야 효과가 난다.

---

## Ⅰ. 개요 및 필요성

클러스터링 팩터는 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)가 "이 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 따라가면 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 덜 뛰어다니며 읽을 수 있는가"를 판단할 때 보는 통계 값이다. [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 리프 블록은 키 순서대로 정렬되어 있어도, 그 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 가리키는 테이블 행이 디스크 여러 블록에 흩어져 있으면 실제 비용은 급격히 커진다. 즉, CF는 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)의 존재 여부가 아니라 <strong><a href="/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a> 탐색 이후의 물리 이동량</strong>을 보여 준다.

이 개념이 중요한 이유는 범위 검색 병목이 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 탐색보다 테이블 접근에서 자주 발생하기 때문이다. 예를 들어 `WHERE order_date BETWEEN ...` 같은 조회는 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)에서 대상 키를 빨리 찾더라도, 실제 주문 행이 블록마다 흩어져 있으면 저장장치는 같은 건수를 읽기 위해 훨씬 많은 블록을 건드려야 한다. 그래서 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 있는데도 [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)이 풀 스캔으로 뒤집히는 현상이 생긴다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│      Logical key order can still cause physical block jumping       │
├──────────────────────────────────────────────────────────────────────┤
│ Index order : 20240101 -> 20240102 -> 20240103 -> 20240104          │
│ Table block :    B07   ->   B07   ->   B19   ->   B35               │
│ Read style  : reused block      then jump      then jump again      │
│                                                                      │
│ Same key order ≠ same physical locality                             │
└──────────────────────────────────────────────────────────────────────┘
```

이 그림이 보여 주는 핵심은 "[인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 정렬돼 있다"와 "테이블이 같이 정렬돼 있다"가 전혀 다른 문제라는 점이다. 클러스터링 팩터는 이 간극을 숫자로 보여 주는 물리 모델링 지표다.

- **📢 섹션 요약 비유**: 찾아보기는 깔끔한데 책이 층마다 흩어져 있으면 사서가 계속 계단을 올라가야 하듯, CF는 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 안내한 뒤 실제로 얼마나 뛰어다녀야 하는지를 알려 주는 점수다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클러스터링 팩터는 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 리프 엔트리를 순서대로 따라가며, 각 엔트리가 가리키는 테이블 블록 번호가 얼마나 자주 바뀌는지 세어 계산한다. 같은 블록이 연속되면 물리적으로 모여 있다는 뜻이고, 거의 매 행마다 다른 블록으로 바뀌면 물리 정렬 친화도가 낮다는 뜻이다. 일반적으로 **좋은 CF는 테이블 블록 수에 가깝고**, **나쁜 CF는 전체 행 수에 가까워진다**.

| 요소 | 의미 | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)에 미치는 영향 |
| :--- | :--- | :--- |
| [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 리프 순서 | 키가 정렬된 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 순서 | 탐색 출발점 제공 |
| 테이블 블록 재사용 | 같은 블록에서 여러 행 읽기 | 랜덤 I/O 감소 |
| 블록 전환 횟수 | 다른 블록으로 점프한 횟수 | CF 증가, 비용 증가 |
| 통계 최신성 | 현재 저장 상태 반영 여부 | [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) 판단 정확도 |

아래 그림은 CF가 실제로 무엇을 세는지 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│              CF counts table-block changes per leaf walk            │
├──────────────────────────────────────────────────────────────────────┤
│ Leaf key      K101    K102    K103    K104    K105    K106          │
│ Row block     B11     B11     B12     B12     B27     B41           │
│ CF counter      1       1       2       2       3       4            │
│                                                                      │
│ Few changes  -> good locality -> range scan stays efficient          │
│ Many changes -> poor locality -> table access becomes expensive      │
└──────────────────────────────────────────────────────────────────────┘
```

[비용 기반 옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/165_cbo_cost_based_optimizer/) (CBO, Cost-Based [Optimizer](/knowledge-base/studynote/12_it_management/02_itsm_itil/088_optimizer/))는 이 정보를 이용해 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 범위 스캔의 총비용을 추정한다. 단순화하면 `인덱스 탐색 비용 + 예상 행 수 × 블록 접근 비용` 구조인데, 여기서 블록 접근 비용을 밀어 올리는 핵심 통계가 CF다. 통계 정보가 오래되면 실제 적재 상태와 CBO가 보는 CF가 달라져 잘못된 [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)이 나올 수 있다.

따라서 CF는 단순히 "값이 크면 나쁘다"로 끝나지 않는다. 어떤 컬럼으로 얼마나 넓은 범위를 읽는지, [버퍼 캐시](/knowledge-base/studynote/02_operating_system/09_file_system/536_buffer_cache_page_cache/)에 얼마나 머무는지, 적재 순서가 얼마나 유지되는지까지 함께 봐야 정확한 해석이 가능하다.

- **📢 섹션 요약 비유**: 우체부가 주소 목록을 받을 때 같은 아파트 단지에 몰려 있으면 몇 번만 움직이면 되지만, 동네 전체에 흩어져 있으면 똑같은 100통도 훨씬 오래 걸리는 것과 같다.

---

## Ⅲ. 비교 및 연결

클러스터링 팩터를 제대로 이해하려면 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)와 분리해서 봐야 한다. [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)는 "얼마나 적은 행을 골라내는가"를 설명하고, CF는 "골라낸 뒤 물리적으로 얼마나 멀리 이동해야 하는가"를 설명한다. [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)가 좋아도 CF가 나쁘면 범위 조회가 느릴 수 있고, [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)가 보통이어도 CF가 좋으면 연속 범위 조회에서 강한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 낸다.

| 비교 축 | [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) ([Selectivity](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)) | 클러스터링 팩터 (CF) | 클러스터형 저장 |
| :--- | :--- | :--- | :--- |
| 핵심 질문 | 몇 건이 걸리는가 | 걸린 행이 얼마나 모여 있는가 | 아예 물리 순서를 맞췄는가 |
| 초점 | [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 필터링 | 물리적 접근 비용 | 물리 구조 자체 |
| 잘 맞는 상황 | 단건 또는 소수 행 조회 | 범위 조회, 블록 재사용 | 읽기 중심 대량 범위 조회 |
| 대표 한계 | 물리 산재 여부 설명 불가 | 후보 행 수가 너무 많으면 한계 | 삽입/재정렬 비용 증가 |

또한 CF는 클러스터형 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) ([Clustered Index](/knowledge-base/studynote/05_database/03_relational_model/159_clustered_index_physical_sort/))나 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 조직 테이블 ([IOT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/), [Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)-Organized Table)과도 자연스럽게 연결된다. 보조 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 순서와 실제 행 저장이 분리되어 있어 CF가 쉽게 나빠질 수 있지만, 클러스터형 구조는 테이블 자체를 키 순서로 유지해 이 문제를 구조적으로 줄인다. 반대로 갱신이 잦은 업무에서 무리하게 물리 정렬을 유지하면 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 분할과 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 비용이 늘 수 있다.

즉 CF는 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 설계, 적재 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/), 커버링 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)까지 이어지는 연결 고리다. SQL 튜닝이 [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) 화면만으로 끝나지 않고 물리 저장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)까지 내려가야 하는 이유도 여기에 있다.

- **📢 섹션 요약 비유**: [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)는 손님 수를 세는 일이고, CF는 그 손님들이 한 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)에 같이 타 있는지 각자 다른 택시에 흩어져 있는지 보는 일과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

대표적인 실무 사례는 대용량 주문 이력 조회다. `order_date` [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 있고 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 날짜 순으로 적재되는 시스템이라면 최근 7일 범위 조회는 같은 블록을 연속적으로 읽기 쉬워 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 범위 스캔이 잘 동작한다. 반면 `customer_name` [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)로 같은 규모의 범위를 읽으면 이름순 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 정렬되어 있어도 실제 주문 행은 날짜순으로 흩어져 있어 CF가 나빠지고, CBO는 풀 스캔을 택할 수 있다.

### 기술사 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 범위 조회가 잦은 컬럼이 실제 적재 순서와 얼마나 맞는가?
2. 대량 적재·삭제 이후 통계 정보가 최신 상태로 갱신되는가?
3. [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 느린 원인이 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 부족인지, CF 악화인지 구분했는가?
4. [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/), 정렬 적재, 클러스터형 저장, 커버링 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 중 어떤 대안이 병목에 가장 직접적인가?
5. 읽기 최적화로 얻는 이익이 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 비용 증가를 상쇄하는가?

### 채택 / 회피 기준

- **채택**: 일자, 증가형 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/), 배치 적재 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)처럼 물리적 군집이 유지되기 쉬운 컬럼의 범위 검색
- **회피 또는 보완**: 무작위 갱신이 잦고 값 분포가 산재된 컬럼의 광범위 조회, 또는 CF가 이미 행 수에 가까운 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)

### 실무 대응 패턴

- 대량 이관 시 자주 조회할 기준으로 `ORDER BY` 적재해 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 물리 군집을 잡는다.
- 오래된 테이블은 재구성 (Reorganization) 또는 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)으로 블록 지역성을 [회복](/knowledge-base/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/)한다.
- 테이블 접근이 너무 비싸면 필요한 컬럼을 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)에 포함해 커버링 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)로 우회한다.

- **📢 섹션 요약 비유**: 이사할 때 주방 물건을 한 박스에, 책을 다른 박스에 모아 넣어야 나중에 빨리 찾을 수 있듯, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 자주 읽는 기준에 맞춰 모아 두어야 조회가 빨라진다.

---

## Ⅴ. 기대효과 및 결론

클러스터링 팩터를 이해하고 관리하면 "[인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 있는데 왜 느린가" 같은 문제를 추측이 아니라 물리 블록 접근 관점에서 설명할 수 있다. 특히 대용량 범위 조회, 배치 집계, 시계열 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석에서는 CF 관리 여부가 체감 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 차이로 바로 드러난다. 좋은 CF는 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)의 가치를 실제 I/O 절감으로 연결해 준다.

물론 한계도 있다. [솔리드 스테이트 드라이브](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/475_ssd_structure/) ([SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/), [Solid State Drive](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/)) 환경에서는 랜덤 접근 페널티가 [하드 디스크 드라이브](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) ([HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/), Hard Disk Drive)보다 줄어들지만, [버퍼 캐시](/knowledge-base/studynote/02_operating_system/09_file_system/536_buffer_cache_page_cache/) 재사용·읽기 증폭·[페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 지역성 측면에서 물리 군집의 의미는 여전히 남아 있다. 또한 모든 테이블을 물리 정렬 중심으로 설계하면 삽입 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 운영 복잡도가 커질 수 있다.

결국 CF는 "[인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 구조로만 보지 말고 실제 저장 블록과 함께 보라"는 경고장이다. 좋은 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 설계는 키를 잘 고르는 데서 끝나지 않고, <strong>그 키 순서가 실제 비용도 줄이게 만들 수 있는가</strong>까지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)할 때 완성된다.

- **📢 섹션 요약 비유**: 좋은 CF는 엘리베이터도 빠르고 손님 방도 층별로 잘 모여 있는 호텔이고, 나쁜 CF는 엘리베이터는 빨라도 손님이 건물 전체에 흩어진 호텔과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [비용 기반 옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/165_cbo_cost_based_optimizer/) (CBO, Cost-Based [Optimizer](/knowledge-base/studynote/12_it_management/02_itsm_itil/088_optimizer/)) | CF를 이용해 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 범위 스캔과 풀 스캔 비용을 비교 |
| [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) ([Selectivity](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)) | 후보 행 수를 줄이는 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 지표로, CF와 함께 봐야 정확한 판단 가능 |
| 랜덤 I/O / 시퀀셜 I/O | CF가 실제 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 차이를 만드는 직접 원인 |
| 클러스터형 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) ([Clustered Index](/knowledge-base/studynote/05_database/03_relational_model/159_clustered_index_physical_sort/)) | 물리 저장 순서를 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)와 맞춰 CF 문제를 구조적으로 완화 |
| [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/) ([Partitioning](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)) | 조회 범위 자체를 줄여 물리 접근 비용을 낮춤 |
| 커버링 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) (Covering [Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)) | 테이블 블록 접근을 줄여 CF 영향도를 우회 |

### 📈 관련 키워드 및 발전 흐름도

```text
인덱스 탐색
    │
    ▼
선택도 (Selectivity) 판단
    │
    ▼
클러스터링 팩터 (CF)로 물리 정렬 평가
    │
    ├─ 좋음  → 인덱스 범위 스캔 강화
    └─ 나쁨  → 풀 스캔 · 재구성 · 파티셔닝 검토
    │
    ▼
물리 모델링 최적화 (Clustered Storage / IOT / Covering Index)
```

이 흐름은 SQL 튜닝이 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 조건 최적화에서 출발해, 결국 물리 저장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)까지 확장되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. CF는 공룡 책 목록을 보고 책장에 갔을 때, 그 책들이 한 칸에 모여 있는지 보는 점수예요.
2. 점수가 좋으면 한 번에 여러 권을 꺼낼 수 있어서 금방 끝나요.
3. 점수가 나쁘면 책이 여기저기 흩어져 있어서 선생님이 책장을 계속 뛰어다녀야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 169 / 600

← **이전**: [168. 데이터 딕셔너리 통계 정보 (Statistics) - 테이블 건수, 블록 수, 인덱스 높이, 클러스터링 팩터 등](/knowledge-base/studynote/05_database/03_relational_model/168_clustering_factor_index_physical_alignment/)
**다음**: [170. 선택도 (Selectivity) / 기수성 (Cardinality) / 분포도 (Distribution)](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) →

---
