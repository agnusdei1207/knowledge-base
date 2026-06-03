+++
title = "299. 스파크 RDD (Resilient Distributed Dataset)"
date = 2026-03-04

[taxonomies]
tags = ["studynote-enterprise"]

[extra]
tags = ["studynote-enterprise"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [아파치 스파크](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/)의 가장 기본적인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조로, 여러 노드에 흩어져 있는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 하나의 불변([Immutable](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/298_immutable/)) 객체처럼 다룰 수 있게 해주는 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 집합이다.
> 2. **가치**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 물리적으로 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)하여 장애에 대비하는 대신, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)된 과정(Lineage)을 기억함으로써 장애 발생 시 해당 부분만 즉시 재계산하여 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)하는 고효율 [탄력성](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/571_resiliency_fault_tolerance_patterns/)을 제공한다.
> 3. **판단 포인트**: 현대 스파크 개발은 상위 수준의 DataFrame이나 Dataset API를 권장하지만, 세밀한 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 제어나 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변환의 근본 원리를 최적화하기 위해서는 RDD의 동작 방식을 반드시 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

기존의 [맵리듀스](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 중간 단계를 디스크에 기록했다. 이는 안정적이지만 연산 속도를 크게 떨어뜨리는 원인이 되었다. [아파치 스파크](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/)는 **"메모리에서 연산하되, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유실 위험은 어떻게 막을 것인가?"**라는 질문에 대한 답으로 RDD를 제시했다.

RDD는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 메모리에 올려 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/)으로 처리하면서도, 장애가 나면 **리니지(Lineage, 계보)**를 추적해 유실된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 다시 만들어내는 '탄력적(Resilient)'인 특성을 갖는다.

- **📢 섹션 요약 비유**: 요리 과정을 매번 사진 찍어 보관(Disk I/O)하는 대신, 레시피(Lineage)를 기억하고 있다가 요리를 망치면 그 단계부터 다시 요리(Re-computation)하는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

RDD는 3가지 핵심 특징을 가진다: **Resilient(장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 가능), Distributed([분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 저장), Dataset([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 집합).**

```text
[원본 데이터 (HDFS 등)] ──▶ [RDD 1 (Filter)] ──▶ [RDD 2 (Map)] ──▶ [RDD 3 (Reduce)]
                                ▲
                                │ (Lineage 기록: RDD1에서 거른 뒤 Map을 적용함)
                                └───────────────────────────────────┘
```

| 주요 메커니즘 | 설명 | 특징 |
|:---|:---|:---|
| 불변성 (Immutability) | 한 번 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)된 RDD는 수정 불가 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 유지 및 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 단순화 |
| [지연 평가](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/) ([Lazy Evaluation](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/)) | 연산 요청 시 즉시 실행하지 않고 기록만 함 | 실제 결과가 필요할 때(Action) 최적의 경로로 한꺼번에 실행 |
| 리니지 (Lineage) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 과정의 방향성 비순환 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)([DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/)) | 체크포인트 없이도 장애 노드의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 재생성 가능 |
| [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/) ([Partitioning](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 여러 노드에 나누어 저장 | [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리의 기본 단위 |

- **📢 섹션 요약 비유**: 영화를 처음부터 끝까지 다 찍어두는 게 아니라, 대본(Lineage)만 가지고 있다가 배우(Node)가 실수하면 그 장면([Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/))만 다시 찍는 원리다.

---

## Ⅲ. 비교 및 연결

RDD는 스파크의 1세대 API이며, 현재는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화가 가미된 DataFrame과 Dataset으로 진화했다.

| 항목 | [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) (Low-level) | DataFrame / Dataset (High-level) |
|:---|:---|:---|
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 타입 | 일반 자바/파이썬 객체 (Type-[safe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/)) | [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)가 정의된 행(Row) 객체 |
| 최적화 엔진 | 개발자의 코드 실력에 의존 | Catalyst Optimizer가 [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) 자동 최적화 |
| 사용 편의성 | 복잡한 [람다](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)식 필요 | SQL 스타일의 직관적인 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 제공 |
| 권장 용도 | [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) 처리, 세밀한 제어 필요 시 | 대부분의 비즈니스 로직 및 [정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/002_structured_data/) 분석 |

비록 상위 API를 주로 쓰더라도, 셔플(Shuffle)이나 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수 조정 같은 튜닝 작업 시에는 결국 [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) 레벨의 이해가 필요하다.

- **📢 섹션 요약 비유**: RDD는 수동 변속기 자동차(정밀 제어 가능)이고, DataFrame은 자동 변속기 자동차(운전 편의성 및 효율 극대화)와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) 관련 가장 큰 이슈는 **셔플(Shuffle)**과 **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스큐([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Skew)**다. 특정 노드에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 몰리거나, 노드 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동이 빈번해지면 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 급격히 떨어진다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 메모리 부족([OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/)) 장애가 빈번한가? -> `persist()`나 `cache()` [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 필요.
2. 특정 단계에서 연산이 너무 오래 걸리는가? -> [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 리티션(Re-[partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/))이나 셔플링 최소화 여부 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/).
3. 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간이 너무 긴가? -> 리니지가 너무 길어지면 중간에 `checkpoint`를 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)했는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/).

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 모든 중간 결과를 무분별하게 `cache()` 하는 것. 메모리 자원을 낭비하여 오히려 전체 시스템 속도를 늦출 수 있다.

- **📢 섹션 요약 비유**: 레시피가 너무 길면 중간에 요리 과정을 사진 찍어둬야(Checkpoint) 기억하기 쉽지, 머리(Memory)만 믿고 있다가는 과부하가 올 수 있다.

---

## Ⅴ. 기대효과 및 결론

RDD는 빅데이터 처리의 패러다임을 '기록'에서 '계산'으로 바꾼 혁신적인 아이디어다. 이를 통해 스파크는 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)보다 압도적인 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 낼 수 있었고, 현재의 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 및 실시간 분석 시대를 여는 초석이 되었다.

결론적으로 RDD는 스파크의 심장이며, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 컴퓨팅 환경에서 **[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 안정성**이라는 두 마리 토끼를 잡기 위한 가장 영리한 설계 방식이다.

- **📢 섹션 요약 비유**: 도미노를 하나씩 세우는 것보다, 넘어진 곳부터 다시 세우는 규칙을 잘 정해두는 것이 전체 도미노 쇼를 성공시키는 비결인 것과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 변환 (Transformation) | `map`, `filter` 등 새로운 RDD를 만드는 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 연산 |
| 액션 (Action) | `count`, `collect` 등 실제 계산을 수행하고 결과를 반환하는 연산 |
| [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) ([Directed Acyclic Graph](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/255_apache_airflow_dag/)) | [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) 간의 의존 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 나타내는 [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) 지도 |

### 📈 관련 키워드 및 발전 흐름도

```
Hadoop MapReduce - 디스크 기반 중간 결과 저장
    │
    ▼
Spark RDD - 인메모리 분산 데이터셋 추상화
    │
    ▼
Transformation (지연 평가) + Action (실행 트리거)
    │
    ▼
DataFrame/Dataset API - 스키마 기반 최적화
    │
    ▼
Catalyst Optimizer + Tungsten 메모리 관리
```

> **키워드**: [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/), [Resilient Distributed Dataset](/knowledge-base/studynote/14_data_engineering/01_infrastructure/025_spark_rdd_resilient_distributed_dataset/), Spark, [Lazy Evaluation](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/), Lineage, DataFrame, Catalyst

### 👶 어린이를 위한 3줄 비유 설명
1. 거대한 퍼즐을 친구들이 나누어서 맞추고 있어요.
2. 조각 하나를 잃어버려도, "어디서 온 조각인지" 적힌 설명서가 있어서 금방 새로 만들 수 있어요.
3. 처음부터 퍼즐을 다시 다 맞출 필요가 없어서 아주 빠르게 완성할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 299 / 482

← **이전**: [298. 빅데이터 분산 처리 프레임워크 (MapReduce vs Spark)](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/298_distributed_processing_framework_mapreduce_spark/)
**다음**: [300. 실시간 데이터 스트리밍 (Kafka + CDC)](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/300_realtime_data_streaming_kafka_cdc/) →

---
