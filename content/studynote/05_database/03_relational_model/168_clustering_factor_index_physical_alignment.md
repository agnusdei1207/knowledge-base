+++
title = "168. 데이터 딕셔너리 통계 정보 (Statistics) - 테이블 건수, 블록 수, 인덱스 높이, 클러스터링 팩터 등"
description = "클러스터링 팩터를 중심으로 인덱스 정렬 순서와 테이블의 물리적 저장 정렬이 성능에 미치는 영향을 설명한다."
date = 2026-04-03

[taxonomies]
tags = ["database"]

[extra]
tags = ["database"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [클러스터링 팩터](/knowledge-base/studynote/05_database/03_relational_model/169_clustering_factor_index_physical_sort/) ([Clustering Factor](/knowledge-base/studynote/05_database/03_relational_model/169_clustering_factor_index_physical_sort/), CF)는 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 가리키는 순서와 실제 테이블 행이 저장된 블록 순서가 얼마나 비슷한지를 보여 주는 물리 정렬 친화도 지표다.
> 2. **가치**: CF가 좋으면 범위 조회 시 같은 블록에서 여러 행을 한꺼번에 읽어 랜덤 I/O (Input/Output)를 줄일 수 있고, 나쁘면 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 타고도 블록 점프가 많아져 풀 테이블 스캔이 더 유리해질 수 있다.
> 3. **판단 포인트**: [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 설계는 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) ([Selectivity](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/))만으로 끝나지 않으며, 자주 읽는 정렬 기준에 맞춰 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 적재 순서·[파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)·클러스터형 저장 구조까지 함께 봐야 한다.

---

## Ⅰ. 개요 및 필요성

[클러스터링 팩터](/knowledge-base/studynote/05_database/03_relational_model/169_clustering_factor_index_physical_sort/)는 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)가 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)의 "[논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 정렬"이 실제 저장 구조와 얼마나 잘 맞물리는지 판단할 때 보는 통계 값이다. [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 리프 블록은 키 순서대로 정렬되어 있어도, 그 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 가리키는 테이블 행이 디스크 여러 블록에 흩어져 있으면 실제 읽기 비용은 급격히 커진다. 즉, CF는 "[인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 있느냐"가 아니라 "[인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 따라가면 물리적으로도 덜 뛰어다니느냐"를 묻는 지표다.

이 값이 중요해진 이유는 범위 검색에서 병목이 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 탐색 자체보다 테이블 접근에 있기 때문이다. 예를 들어 `WHERE order_date BETWEEN ...` 같은 조회는 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)에서 수천 건을 빠르게 찾더라도, 그 수천 건이 매번 다른 블록에 있으면 저장장치는 계속 랜덤 접근을 수행한다. 결국 좋은 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)처럼 보여도 실제 [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)에서는 풀 스캔으로 뒤집히는 일이 생긴다.

따라서 [클러스터링 팩터](/knowledge-base/studynote/05_database/03_relational_model/169_clustering_factor_index_physical_sort/)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 딕셔너리 통계 정보 중에서도 특히 "[인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 언제 배신하는가"를 설명하는 숫자다. 개발자는 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)가 높은 컬럼에만 관심을 두기 쉽지만, [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 관리자 ([DBA](/knowledge-base/studynote/05_database/01_db_architecture_relational/025_dba_database_administrator/), [Database Administrator](/knowledge-base/studynote/05_database/01_db_architecture_relational/025_dba_database_administrator/))나 아키텍트는 그 컬럼이 물리적으로도 같이 모여 저장되는지까지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 한다.

- **📢 섹션 요약 비유**: [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 책 뒤의 찾아보기이고, CF는 찾아본 단어들이 도서관 한 칸에 모여 있는지 아니면 층마다 흩어져 있는지를 알려 주는 점수와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CF는 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 리프 엔트리를 순서대로 따라가며, 각 엔트리가 가리키는 테이블 블록 번호가 얼마나 자주 바뀌는지 세어 계산한다. 같은 블록이 계속 이어지면 물리적으로 잘 모여 있다는 뜻이고, 거의 매 행마다 다른 블록으로 바뀌면 정렬 친화도가 낮다는 뜻이다. 그래서 일반적으로 **좋은 CF는 테이블 블록 수에 가깝고**, **나쁜 CF는 전체 행 수에 가까워진다**.

아래 그림은 CF가 실제로 무엇을 세는지 보여 준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">CF counts table-block changes while scanning index leaf order</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Index leaf order : K101 ─ K102 ─ K103 ─ K104 ─ K105</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Table block map : B07 ─ B07 ─ B08 ─ B08 ─ B21</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">CF counter : 1 1 2 2 3</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Few block changes =&gt; rows are physically aligned</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Many block changes =&gt; random table access increases</div></div>
</div>
</div>



이 그림의 핵심은 CF가 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 트리 높이나 키 분포를 세는 값이 아니라, <strong><a href="/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a>가 연결하는 테이블 블록의 이동 횟수</strong>를 세는 값이라는 점이다. 따라서 CF는 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 모델이 아니라 물리 접근 비용과 직접 연결된다. 같은 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000건 범위 조회라도 CF가 좋으면 200개 블록만 읽고 끝날 수 있지만, 나쁘면 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000개 블록을 각각 건드릴 수 있다.

| 항목 | CF가 좋은 경우 | CF가 나쁜 경우 |
| :--- | :--- | :--- |
| 테이블 저장 상태 | [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 키 순서와 비슷하게 적재 | 삽입·갱신으로 저장 순서가 뒤섞임 |
| 범위 조회 비용 | 같은 블록 재사용 가능 | 매 행마다 다른 블록 접근 가능 |
| [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) 판단 | [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 범위 스캔 선호 | 풀 스캔 또는 다른 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 검토 |
| 대표 예시 | 일자 기반 이력 테이블 | 이름·상태값처럼 산재된 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) |

정량적으로 보면 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 접근 비용은 `인덱스 탐색 비용 + 예상 행 수 × 블록 이동 비용`에 가깝게 계산된다. 여기서 블록 이동 비용을 추정하는 핵심 재료가 CF다. 그래서 통계 갱신이 오래되면 실제 저장 상태와 CF가 달라져 [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)가 잘못된 [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)을 세울 수 있다.

- **📢 섹션 요약 비유**: CF는 우체부가 주소 목록을 따라 배달할 때 같은 아파트에 몰려 있는지, 동네 전체를 지그재그로 뛰어다녀야 하는지를 미리 알려 주는 동선 예측표와 같다.

---

## Ⅲ. 비교 및 연결

[클러스터링 팩터](/knowledge-base/studynote/05_database/03_relational_model/169_clustering_factor_index_physical_sort/)를 제대로 이해하려면 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)와 구분해야 한다. [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)는 "얼마나 적은 행을 골라내는가"를 말하고, CF는 "골라낸 뒤 실제로 얼마나 멀리 뛰어다녀야 하는가"를 말한다. [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)가 좋아도 CF가 나쁘면 범위 조회는 느릴 수 있고, [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)가 보통이어도 CF가 좋으면 날짜·시퀀스 같은 연속 범위 조회에서 강한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 낼 수 있다.

| 비교 축 | [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) ([Selectivity](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)) | [클러스터링 팩터](/knowledge-base/studynote/05_database/03_relational_model/169_clustering_factor_index_physical_sort/) (CF) | 클러스터형 저장 |
| :--- | :--- | :--- | :--- |
| 질문 | 몇 건이 걸리는가 | 걸린 건들이 얼마나 모여 있는가 | 아예 물리 순서를 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)에 맞췄는가 |
| 초점 | [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 필터링 | 물리적 접근 비용 | 물리 구조 자체 |
| 좋을 때 효과 | 후보 행 수 감소 | 블록 재사용 증가 | 범위 조회 최적화 극대화 |
| 한계 | 물리 산재 여부는 설명 못 함 | 후보 수가 너무 많으면 한계 | 삽입/재정렬 비용 증가 |

또한 CF는 클러스터형 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) ([Clustered Index](/knowledge-base/studynote/05_database/03_relational_model/159_clustered_index_physical_sort/))나 [IOT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) ([Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)-Organized Table)와도 연결된다. 일반 보조 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 순서와 실제 행 저장이 분리되어 있어 CF가 나빠질 수 있지만, 클러스터형 구조는 테이블 자체를 키 순서로 유지해 이 문제를 구조적으로 줄인다. 반대로 갱신이 잦은 업무에서 무리하게 물리 정렬을 유지하면 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 분할과 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 비용이 늘 수 있으므로 읽기 패턴과 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 패턴을 함께 봐야 한다.

즉, CF는 단순한 통계 값이 아니라 <strong><a href="/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a> 설계·적재 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a>·물리 모델링을 이어 주는 연결 고리</strong>다. 구조화 질의 언어 (SQL, Structured Query Language) 튜닝에서 [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)만 보는 접근이 한계에 부딪히는 이유도, 결국 이 물리 정렬 문제를 건드리지 못하기 때문이다.

- **📢 섹션 요약 비유**: [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)는 손님 수를 세는 일이고, CF는 그 손님들이 한 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)에 타 있는지 각자 다른 택시에 흩어져 있는지를 보는 일과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

대표적인 실무 사례는 대용량 주문 이력 조회다. `order_date` [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 있고 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 날짜 순으로 적재되는 시스템이라면 최근 1주일 범위 조회는 같은 블록을 연속적으로 읽기 쉬워 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 범위 스캔이 잘 동작한다. 반면 `customer_name` [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)로 같은 범위를 읽으면 이름순 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 정렬되어 있어도 실제 주문 행은 날짜순으로 흩어져 있어 CF가 나빠지고, [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)는 풀 스캔을 선택할 가능성이 높다.

### 기술사 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 범위 조회가 잦은 컬럼이 실제 적재 순서와 얼마나 맞는가?
2. 통계 정보 수집 주기와 대량 적재/삭제 시점이 어긋나 있지 않은가?
3. 풀 스캔이 느린 것이 아니라, 나쁜 CF 때문에 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 더 비싼 상황은 아닌가?
4. [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/), 정렬 적재, 클러스터형 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/), 커버링 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 중 무엇이 병목에 가장 직접적인가?
5. 읽기 최적화로 얻는 이익이 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 비용 증가를 상쇄하는가?

### 채택 / 회피 판단

- **채택**: 일자, 증가형 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/), 배치 적재 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)처럼 물리적 군집이 유지되기 쉬운 컬럼의 범위 검색
- **회피 또는 보완**: 무작위 갱신이 잦고 값 분포가 산재된 컬럼의 광범위 조회, 또는 CF가 이미 행 수에 가까운 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)

### 실무 대응 패턴

- 대량 이관 시 자주 조회할 기준으로 `ORDER BY` 적재하여 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 정렬 상태를 잡는다.
- 오래된 테이블은 재구성 (Reorganization)이나 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)으로 물리 군집을 [회복](/knowledge-base/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/)한다.
- 테이블 접근이 비싸면 필요한 컬럼을 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)에 포함해 커버링 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)로 우회한다.

- **📢 섹션 요약 비유**: 짐을 새집에 아무 박스에나 넣어 두면 나중에 찾을 때 집 전체를 뒤져야 하듯, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 읽는 기준에 맞춰 모아 두어야 조회가 빨라진다.

---

## Ⅴ. 기대효과 및 결론

[클러스터링 팩터](/knowledge-base/studynote/05_database/03_relational_model/169_clustering_factor_index_physical_sort/)를 이해하고 관리하면 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)의 실제 효율을 더 정확히 예측할 수 있다. 그 결과 "[인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 있는데 왜 느린가" 같은 문제를 감으로 추측하지 않고, 물리 정렬과 블록 접근 관점에서 설명할 수 있다. 특히 대용량 범위 조회, 배치 집계, 시계열 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석에서 설계 품질 차이가 크게 드러난다.

물론 한계도 있다. [솔리드 스테이트 드라이브](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/475_ssd_structure/) ([SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/), [Solid State Drive](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/)) 환경에서는 랜덤 접근 페널티가 [하드 디스크 드라이브](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) ([HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/), Hard Disk Drive)보다 줄어들지만, [버퍼 캐시](/knowledge-base/studynote/02_operating_system/09_file_system/536_buffer_cache_page_cache/)·읽기 증폭·[페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 지역성 측면에서 물리 군집의 가치는 여전히 남아 있다. 또한 지나친 물리 정렬 추구는 삽입 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 운영 복잡도를 높일 수 있으므로, 모든 테이블을 클러스터형으로 만들면 답이라는 뜻은 아니다.

결국 CF는 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 구조로만 보지 말고, 실제 저장 블록과 함께 보라는 경고장이다. 좋은 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 설계는 키를 잘 고르는 데서 끝나지 않고, <strong>그 키 순서가 실제로도 비용을 줄이게 만들 수 있는가</strong>까지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)할 때 완성된다.

- **📢 섹션 요약 비유**: 좋은 CF는 빠른 엘리베이터를 가진 건물에 손님 방도 층별로 잘 배치된 상태이고, 나쁜 CF는 엘리베이터는 빨라도 손님이 건물 전체에 흩어진 상태와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [비용 기반 옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/165_cbo_cost_based_optimizer/) (CBO, Cost-Based [Optimizer](/knowledge-base/studynote/12_it_management/02_itsm_itil/088_optimizer/)) | CF를 사용해 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 범위 스캔과 풀 스캔의 비용을 비교 |
| [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) ([Selectivity](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)) | 후보 행 수를 줄이는 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 지표로, CF와 함께 봐야 정확한 판단 가능 |
| 랜덤 I/O / 시퀀셜 I/O | CF가 실제 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 차이를 만드는 직접 원인 |
| 클러스터형 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) ([Clustered Index](/knowledge-base/studynote/05_database/03_relational_model/159_clustered_index_physical_sort/)) | 물리 저장 순서를 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)와 맞춰 CF 문제를 구조적으로 완화 |
| [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/) ([Partitioning](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)) | 조회 범위 자체를 줄여 물리 접근 비용을 낮춤 |
| 커버링 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) (Covering [Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)) | 테이블 블록 접근을 줄여 CF 영향도를 우회 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">기본 인덱스 탐색</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">선택도 (Selectivity) 판단</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">클러스터링 팩터 (CF)로 물리 정렬 평가</div>
<div class="kb-diagram-tree-item" style="--depth:2">좋음 → 인덱스 범위 스캔 강화</div>
<div class="kb-diagram-tree-item" style="--depth:2">나쁨 → 풀 스캔 · 재구성 · 파티셔닝 검토</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">물리 모델링 최적화 (Clustered Storage / IOT / Covering Index)</div>
</div>
</div>



이 흐름은 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 튜닝이 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 조건 최적화에서 출발해, 결국 물리 저장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)까지 확장되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. CF는 공룡 책 목록을 보고 책장에 갔을 때, 그 책들이 한 칸에 모여 있는지 보는 점수예요.
2. 점수가 좋으면 한 번에 여러 권을 꺼낼 수 있어서 금방 끝나요.
3. 점수가 나쁘면 책이 여기저기 흩어져 있어서 선생님이 책장을 계속 뛰어다녀야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 168 / 600

← **이전**: [167. 힌트 (Hint) - 개발자가 옵티마이저에게 접근 경로를 명시적으로 지시 (/*+ INDEX(EMP IDX_01) */ 등)](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)
**다음**: [169. 클러스터링 팩터 (Clustering Factor) - 인덱스 정렬 순서와 실제 물리적 데이터 정렬 순서의 일치 정도](/knowledge-base/studynote/05_database/03_relational_model/169_clustering_factor_index_physical_sort/) →

---
