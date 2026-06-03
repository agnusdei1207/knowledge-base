+++
title = "184. 파티션 프루닝 (Partition Pruning)"
date = 2026-05-06

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 프루닝 ([Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) [Pruning](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/))은 [데이터베이스 관리 시스템](/knowledge-base/studynote/05_database/01_db_architecture_relational/003_dbms_database_management_system/) ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/) System, [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/)) [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)가 조건절을 보고 <strong>읽을 필요가 없는 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/">파티션</a>을 <a href="/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/">실행 계획</a>에서 미리 제외</strong>하는 최적화다.
> 2. **가치**: 같은 대용량 테이블이라도 필요한 1~2개 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)만 읽게 만들면 입출력 (Input/Output, I/O), 버퍼 사용량, 통계 탐색 범위가 함께 줄어 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 이점이 현실이 된다.
> 3. **판단 포인트**: [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키와 질의 조건이 맞물릴 때만 효과가 크며, 함수 적용·묵시적 형변환·잘못된 키 선정이 있으면 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)은 나눴는데도 전체 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)을 다 훑는 상황이 생긴다.

---

## Ⅰ. 개요 및 필요성

[파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 프루닝은 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 테이블에서 조건에 맞는 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)만 남기고 나머지를 제거하는 최적화 기법이다. 구조화 질의 언어 (Structured Query Language, SQL) 실행 전에 "이 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)에는 어차피 답이 없다"는 사실을 알 수 있으면, DBMS는 해당 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)을 아예 읽지 않는다. 따라서 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)은 단순히 테이블을 잘게 나누는 물리 구조이고, 프루닝은 그 구조를 실제 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)으로 연결하는 실행 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이라고 이해하는 것이 정확하다.

이 개념이 필요한 이유는 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)만 나눈다고 자동으로 빨라지지는 않기 때문이다. 예를 들어 60개월치 주문 이력을 월별 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)으로 저장했더라도, 최근 1개월 조회 때 60개 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)을 모두 읽으면 분할의 의미가 거의 없다. 반대로 조회 조건이 `order_date`처럼 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키와 직접 연결되면 59개 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)을 건너뛰고 필요한 1개만 읽게 되어 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 차이가 극적으로 벌어진다.

아래 그림은 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/) 자체와 프루닝의 차이를 보여 준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Monthly partitions and pruning</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Table : sales_history</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">p_2026_01</div><div class="kb-diagram-cell">p_2026_02</div><div class="kb-diagram-cell">p_2026_03</div><div class="kb-diagram-cell">...</div><div class="kb-diagram-cell">p_2026_12</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Query : WHERE order_date &gt;= DATE '2026-05-01'</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">AND order_date &lt; DATE '2026-06-01'</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Without pruning : scan p_2026_01 ~ p_2026_12</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">With pruning : skip all except p_2026_05</div></div>
</div>
</div>



핵심은 "행을 읽고 버리는 것"보다 앞 단계에서 "[파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 자체를 읽지 않는 것"이다. 그래서 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 프루닝은 필터 조건의 효율화가 아니라, 저장 단위 선택 자체를 줄이는 최적화에 가깝다.

- **📢 섹션 요약 비유**: 큰 도서관에서 2026년 5월 신문만 찾는데 창고 전체를 뒤지지 않고, 2026년 5월 서가만 바로 여는 것과 같다. 책을 읽기 전에 서고 문부터 줄여 버리는 것이 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 프루닝의 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 프루닝은 [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)가 조건절을 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)하고, 그 값을 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 경계 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)와 비교한 뒤, [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)의 시작·종료 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 범위를 좁히는 방식으로 동작한다. 즉 조건식이 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키와 직접 비교 가능한 형태여야 하며, 그래야 어떤 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)이 도달 가능하고 어떤 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)이 불가능한지 계산할 수 있다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">How pruning happens</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">SQL predicate</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ WHERE order_date &gt;= DATE '2026-05-01'</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">AND order_date &lt; DATE '2026-06-01'</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Predicate normalization</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Compare with partition boundary metadata</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ unreachable partitions -&gt; removed from plan</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ reachable partitions -&gt; kept for scan</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Remaining partitions + local index / segment access</div></div>
</div>
</div>



| 구분 | 결정 시점 | 대표 상황 | 특징 |
| :--- | :--- | :--- | :--- |
| 정적 프루닝 (Static [Pruning](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/)) | 파싱·최적화 시점 | 상수 조건, 고정 날짜 범위 | 실행 전부터 읽을 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)이 확정된다. |
| 동적 프루닝 (Dynamic [Pruning](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/)) | 실행 시점 | [바인드 변수](/knowledge-base/studynote/05_database/03_relational_model/190_bind_variable_soft_parsing/), 조인 결과, 런타임 값 | 실제 값이 들어온 뒤에 읽을 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)이 결정된다. |
| 서브파티션 프루닝 (Subpartition [Pruning](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/)) | 최적화 또는 실행 시점 | [컴포지트 파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/183_composite_partitioning/) ([Composite Partitioning](/knowledge-base/studynote/05_database/03_relational_model/183_composite_partitioning/)) | 상위 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)뿐 아니라 하위 서브파티션까지 범위를 더 줄인다. |

정적 프루닝은 가장 이해하기 쉽다. 예를 들어 `WHERE order_date BETWEEN ...`처럼 상수 범위가 명확하면 [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)는 계획 단계에서 읽을 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)을 확정할 수 있다. 반면 동적 프루닝은 [바인드 변수](/knowledge-base/studynote/05_database/03_relational_model/190_bind_variable_soft_parsing/)나 조인 상대 값에 따라 실행 시점에 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 범위가 좁혀지는 형태로, [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)와 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 조인에서 특히 중요하다.

여기서 자주 놓치는 점은 프루닝과 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 경쟁 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 아니라는 것이다. 프루닝은 "어느 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)을 읽을지"를 줄이고, [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 "남은 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 안에서 어느 행을 읽을지"를 줄인다. 즉 좋은 설계에서는 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 프루닝과 로컬 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) (Local [Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/))가 함께 작동한다.

- **📢 섹션 요약 비유**: 택배 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)장에서 먼저 "서울 창고만 간다"를 정한 뒤, 그 안에서 다시 동네별 바구니를 찾는 과정과 같다. 프루닝은 창고 선택이고, [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 창고 안 선반 찾기다.

---

## Ⅲ. 비교 및 연결

[파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 프루닝은 다른 접근 방식과 비교할 때 경계가 더 분명해진다. 전체 스캔은 모든 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)을 읽고 나서 조건을 거르기 때문에 가장 단순하지만 비용이 크다. [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 범위 스캔은 특정 키 값을 빠르게 찾지만, 여전히 어떤 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)을 읽을지 결정하는 문제와는 별개다. [컴포지트 파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/183_composite_partitioning/)은 프루닝이 더 세밀하게 작동하도록 상위·하위 분할 구조를 제공한다.

| 기법 | 줄이는 대상 | 강한 상황 | 한계 |
| :--- | :--- | :--- | :--- |
| 전체 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 스캔 (Full [Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) Scan) | 없음 | [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키 조건이 없거나 거의 전 범위를 읽을 때 | 큰 테이블에서는 I/O 부담이 크다. |
| [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 프루닝 ([Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) [Pruning](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/)) | 읽을 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수 | 기간·지역·테넌트처럼 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키 조건이 명확할 때 | 키와 조건식이 어긋나면 효과가 사라진다. |
| [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 범위 스캔 ([Index Range Scan](/knowledge-base/studynote/05_database/07_exam_summary/429_index_range_scan/)) | 남은 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 내부의 행 수 | [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)가 높은 검색, 점 조회 | 프루닝 없이 쓰면 불필요한 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)이 여전히 열릴 수 있다. |
| [컴포지트 파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/183_composite_partitioning/) | 상위·하위 저장 범위 | 기간 관리와 내부 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)을 함께 잡을 때 | 구조와 통계 관리가 더 복잡해진다. |

이 비교가 중요한 이유는 "[파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)했으니 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 필요 없다"거나 "[인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 있으니 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)은 필요 없다"는 식의 단순화가 틀리기 때문이다. 최근 7일 매출만 보는 분석 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)라면 먼저 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 프루닝으로 월 범위를 좁히고, 그 안에서 상품 번호나 고객 번호 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 추가로 사용할 수 있다. 반대로 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키와 무관한 조건만 자주 쓰는 테이블이라면 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)보다 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 설계가 더 큰 효과를 줄 수 있다.

또한 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 프루닝은 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 교체, 아카이브, [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)별 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리와도 연결된다. [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키가 보관 주기와 조회 패턴을 동시에 반영하면 운영과 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 한 방향으로 맞물리지만, 그 둘이 어긋나면 관리 편의와 조회 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 서로 충돌할 수 있다.

- **📢 섹션 요약 비유**: 대형 마트에서 먼저 "냉장 코너만 갈지, 과일 코너만 갈지"를 정하는 것이 프루닝이고, 그 코너 안에서 특정 브랜드 상품을 찾는 것이 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)다. 코너 선택과 상품 찾기는 같은 일이 아니라 이어지는 두 단계다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 프루닝이 실제로 일어나는지 [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)으로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)해야 한다. 예를 들어 48개월치 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 월별 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)으로 저장한 뒤, 운영 대시보드가 최근 24시간만 조회한다면 원칙적으로 1개 월 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 또는 많아야 2개 월 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)만 읽어야 한다. 그런데 조건을 `TO_CHAR(log_time, 'YYYY-MM-DD') = '2026-05-06'`처럼 작성하면 컬럼 원형이 깨져 프루닝이 풀릴 수 있다.

### 기술사 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키가 실제 주요 조회 조건과 보관 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 함께 반영하는가?
2. 조건식이 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키를 함수 없이 원래 타입 그대로 비교하는가?
3. [바인드 변수](/knowledge-base/studynote/05_database/03_relational_model/190_bind_variable_soft_parsing/), 조인, 뷰를 거친 뒤에도 [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)에서 프루닝이 유지되는가?
4. 남은 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 안 검색 효율을 위해 로컬 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 또는 적절한 보조 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 함께 설계했는가?
5. 월·일 단위로 너무 잘게 쪼개 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)와 통계 수집 비용이 과도해지지 않았는가?

### 자주 나오는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- `TO_CHAR(order_date, 'YYYYMM') = '202605'`처럼 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키에 함수를 씌우는 경우
- 문자형 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키를 숫자 상수와 비교해 묵시적 형변환을 일으키는 경우
- 조회 조건은 `customer_id` 중심인데 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키를 `status`처럼 거의 안 쓰는 컬럼으로 고르는 경우
- 거의 모든 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)가 다중 기간 집계를 수행하는데 지나치게 많은 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)을 만들어 관리 비용만 높이는 경우

실무 의사결정에서는 "대용량이라서 무조건 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)"이 아니라, "읽을 범위를 storage 단위로 줄일 수 있는가"를 먼저 묻는 것이 맞다. [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 프루닝의 혜택을 얻지 못하는 설계는 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 관리 복잡도만 늘리고, 기대했던 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 이득은 주지 못할 가능성이 높다.

- **📢 섹션 요약 비유**: 사물함을 날짜별로 나눠 놓았는데, 막상 찾을 때 날짜 대신 색깔만 물어보면 결국 사물함을 다 열어봐야 한다. 칸을 나누는 기준과 찾는 기준이 같아야 빨라진다.

---

## Ⅴ. 기대효과 및 결론

[파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 프루닝이 잘 설계되면 대용량 테이블 조회의 시작점이 달라진다. 불필요한 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)이 [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)에서 빠지므로 스캔 시간과 버퍼 점유가 줄고, [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)별 유지보수와 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)도 더 단순해진다. 특히 기간 기반 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서는 최신 구간 조회, 월별 집계, 오래된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 제거가 모두 자연스럽게 맞물린다.

하지만 프루닝은 만능이 아니다. [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키와 다른 조건이 주로 사용되면 효과가 약하고, [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수가 너무 많으면 최적화와 통계 관리 비용이 커진다. 또한 집계 범위가 거의 전체 기간을 덮는 분석 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)라면 프루닝보다 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리나 저장 형식 최적화가 더 중요한 경우도 있다.

결국 기억해야 할 관점은 단순하다. [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 프루닝은 "행을 덜 읽는다"보다 한 단계 앞선, <strong>저장 단위를 덜 연다</strong>는 최적화다. 그래서 이 개념의 핵심은 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/) 자체보다, [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키와 조건식이 얼마나 자연스럽게 맞물리도록 설계되었는지에 있다.

- **📢 섹션 요약 비유**: 잘 정리된 창고는 필요한 방 문 하나만 열고 일을 끝내게 해 준다. 반대로 방은 많이 나눴는데 어느 문을 열어야 할지 모르면, 결국 모든 문을 다시 열어보는 수고가 생긴다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키 ([Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)) | 어떤 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)을 읽을지 결정하는 기준 축으로, 프루닝 성패를 좌우한다. |
| [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) ([Optimizer](/knowledge-base/studynote/12_it_management/02_itsm_itil/088_optimizer/)) | 조건식을 해석하고 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 경계와 비교해 [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)에서 불필요한 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)을 제거한다. |
| 로컬 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) (Local [Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)) | 프루닝 후 남은 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 내부에서 행 접근 범위를 추가로 줄인다. |
| [컴포지트 파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/183_composite_partitioning/) ([Composite Partitioning](/knowledge-base/studynote/05_database/03_relational_model/183_composite_partitioning/)) | 상위 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)과 서브파티션 단계에서 더 세밀한 프루닝을 가능하게 한다. |
| [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 교체·삭제 | 보관 주기 관리와 프루닝 이점이 같은 키 축에 있을 때 운영 효율이 커진다. |
| 비검색 가능 조건 (Non-sargable Predicate) | 함수 적용, 묵시적 형변환 등으로 프루닝 가능성을 떨어뜨리는 대표 원인이다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">대용량 테이블 분할</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">파티션 키 선정</div>
<div class="kb-diagram-tree-item" style="--depth:4">기간 기반 Range Partition</div>
<div class="kb-diagram-tree-item" style="--depth:4">업무 경계 List Partition</div>
<div class="kb-diagram-tree-item" style="--depth:4">부하 분산 Hash Partition</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">파티션 프루닝 (Partition Pruning)</div>
<div class="kb-diagram-tree-item" style="--depth:4">정적 프루닝</div>
<div class="kb-diagram-tree-item" style="--depth:4">동적 프루닝</div>
<div class="kb-diagram-tree-item" style="--depth:4">로컬 인덱스 · 서브파티션 프루닝 결합</div>
</div>
</div>



이 흐름은 "단순 분할"에서 "[실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) 수준의 [가지치기](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/)"로 사고가 확장되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 프루닝은 장난감을 날짜별 상자에 넣어 두고, 오늘 필요한 상자 하나만 꺼내는 방법이에요.
2. 그래서 모든 상자를 다 뒤지지 않아도 빨리 찾을 수 있어요.
3. 하지만 날짜 대신 엉뚱한 기준으로 찾으면 결국 상자를 전부 다시 열어봐야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 184 / 600

← **이전**: [183. 컴포지트 파티셔닝 (Composite Partitioning) - 복합 (Range + Hash 등)](/knowledge-base/studynote/05_database/03_relational_model/183_composite_partitioning/)
**다음**: [185. 전역 인덱스 (Global Index) vs 지역 인덱스 (Local Index, 파티션별 독립 인덱스)](/knowledge-base/studynote/05_database/03_relational_model/185_global_vs_local_index/) →

---
