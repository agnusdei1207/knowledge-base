---
title: "206. 아파치 스파크 (Apache Spark) 인메모리 RDD 지연 평가 계보"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache Spark의 [RDD](/studynote/13_cloud_architecture/05_data_engineering/310_audit/) ([Resilient Distributed Dataset](/studynote/14_data_engineering/01_infrastructure/025_spark_rdd_resilient_distributed_dataset/))는 불변성(Immutability)·[분산](/studynote/08_algorithm_stats/08_stats/136_variance/)성(Distribution)·내결함성([Fault Tolerance](/studynote/02_operating_system/11_exam_summary/800_system_architecture_fault_tolerance_dual/))을 가진 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 컬렉션으로, [지연 평가](/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/)([Lazy Evaluation](/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/))와 [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) ([Directed Acyclic Graph](/studynote/06_ict_convergence/03_cloud_infrastructure/255_apache_airflow_dag/)) [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)를 통해 [MapReduce](/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 대비 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~100배 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 달성한다.
> 2. **가치**: 계보(Lineage) 기반 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 메커니즘은 [체크포인팅](/studynote/16_bigdata/03_spark/071_checkpointing/) 없이도 장애를 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)할 수 있게 하며, 반복적 [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)에서 중간 결과를 메모리에 [캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)해 디스크 I/O를 근본적으로 제거한다.
> 3. **판단 포인트**: 기술사 논술에서 Transformation(변환)과 Action(액션)의 구분, Lineage Graph의 장애 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 원리, [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) 최적화가 어떻게 [실행 계획](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)을 개선하는지를 구체적으로 서술해야 한다.

---

## Ⅰ. 개요 및 필요성

### Apache Spark 등장 배경

2009년 [UC](/studynote/12_it_management/02_itsm_itil/871_underpinning_contract/) 버클리 AMPLab에서 시작된 Spark는 MapReduce의 두 가지 핵심 한계를 해결하기 위해 설계되었다.

| [MapReduce](/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 한계 | Spark 해결책 |
|:---|:---|
| 매 단계마다 [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 디스크 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) | 인메모리(In-Memory) RDD로 중간 결과 보관 |
| 반복 처리 시 지수적 I/O 증가 | [RDD](/studynote/13_cloud_architecture/05_data_engineering/310_audit/) [캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)으로 반복 연산 시 재사용 |
| Map-Reduce 2단계만 지원 | [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) 기반 복잡한 다단계 연산 표현 가능 |
| 배치 전용 | 배치·스트리밍·ML·SQL 통합 처리 |

### [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비교

```
K-Means 100 이터레이션 성능 비교
+------------------------------------------------------+
|  MapReduce:                                          |
|  이터레이션 1: [HDFS 읽기] -> 처리 -> [HDFS 쓰기]      |
|  이터레이션 2: [HDFS 읽기] -> 처리 -> [HDFS 쓰기]      |
|  ...100회 반복: 총 200회 HDFS I/O -> 시간: ~110분      |
|                                                      |
|  Spark:                                              |
|  이터레이션 1: [HDFS 읽기] -> RDD 처리 -> [RAM 캐시]   |
|  이터레이션 2: [RAM 읽기] -> RDD 처리 -> [RAM 캐시]    |
|  ...100회 반복: 1회 HDFS I/O, 나머지 메모리 -> ~5분   |
|                                                      |
|  성능 차이: 약 22배 빠름                               |
+------------------------------------------------------+
```

📢 **섹션 요약 비유**: Spark는 "100번 시험 문제를 풀 때, MapReduce는 매번 교과서를 꺼냈다 넣었다 하고, Spark는 교과서를 책상 위에 펼쳐놓고 바로바로 참조하는 것"이다. 첫 번에는 시간이 비슷하지만, 반복할수록 격차가 벌어진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [RDD](/studynote/13_cloud_architecture/05_data_engineering/310_audit/) ([Resilient Distributed Dataset](/studynote/14_data_engineering/01_infrastructure/025_spark_rdd_resilient_distributed_dataset/)) 특성

RDD는 Spark의 근본 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)로, 다음 세 가지 핵심 속성을 가진다.

```
RDD 3대 특성
+-------------------------------------------------------------+
|                                                             |
|  +------------------------------------------------------+  |
|  |  Resilient (내결함성)                                  |  |
|  |  -> 파티션 손실 시 Lineage로 재계산 가능               |  |
|  +------------------------------------------------------+  |
|                                                             |
|  +------------------------------------------------------+  |
|  |  Distributed (분산)                                   |  |
|  |  -> 파티션 단위로 여러 Executor에 분산 저장·처리       |  |
|  +------------------------------------------------------+  |
|                                                             |
|  +------------------------------------------------------+  |
|  |  Dataset (데이터셋)                                    |  |
|  |  -> 불변(Immutable) 레코드의 컬렉션                    |  |
|  |  -> 변환 시 새 RDD 생성 (원본 수정 안 됨)              |  |
|  +------------------------------------------------------+  |
+-------------------------------------------------------------+
```

### [지연 평가](/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/) ([Lazy Evaluation](/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/))

Spark는 Transformation을 즉시 실행하지 않고, Action이 호출될 때 전체 [실행 계획](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)을 최적화하여 한꺼번에 실행한다.

```
지연 평가 동작 방식
+-------------------------------------------------------------+
|  코드:                                                      |
|  val rdd1 = sc.textFile("hdfs://data")    <- RDD 생성        |
|  val rdd2 = rdd1.filter(_.contains("error"))  <- Transformation|
|  val rdd3 = rdd2.map(_.split(","))            <- Transformation|
|  val result = rdd3.count()                    <- Action ✅   |
|                                                             |
|  실제 실행 시점: count() 호출 시에만 전체 DAG 실행          |
|  최적화: Spark가 filter + map 파이프라인을 한번에 처리       |
|          (Pipeline Fusion으로 중간 RDD 물리화 없음)          |
+-------------------------------------------------------------+
```

| 구분 | 설명 | 즉시 실행? | 예시 |
|:---|:---|:---|:---|
| Transformation | RDD를 새 RDD로 변환 | ❌ ([지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)) | map, filter, flatMap, groupBy, [join](/studynote/05_database/04_transactions_concurrency/521_join/) |
| Action | 결과를 Driver로 반환하거나 저장 | ✅ (즉시) | count, collect, save, first, reduce |

### [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) ([Directed Acyclic Graph](/studynote/06_ict_convergence/03_cloud_infrastructure/255_apache_airflow_dag/)) [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)

```
DAG 스케줄러 처리 흐름
+-------------------------------------------------------------+
|  논리적 DAG (RDD 계보):                                     |
|                                                             |
|  textFile ---> filter ---> map ---> groupBy ---> reduce        |
|                                     |                       |
|                              (셔플 발생)                    |
|                                                             |
|  물리적 실행 계획 (Stage 분리):                              |
|                                                             |
|  Stage 1: textFile -> filter -> map   (파이프라인 가능)       |
|                                     |                       |
|                              [셔플 경계]                    |
|                                     |                       |
|  Stage 2: groupBy -> reduce          (셔플 후 실행)          |
+-------------------------------------------------------------+
```

**Stage 분리 기준**: 셔플이 필요한 Wide Transformation (groupBy, [join](/studynote/05_database/04_transactions_concurrency/521_join/), sortBy 등)이 Stage 경계를 형성한다.

| 변환 유형 | 설명 | Stage 경계 |
|:---|:---|:---|
| Narrow Transformation | 각 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)이 부모 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 1개에만 의존 | ❌ (동일 Stage) |
| Wide Transformation | 여러 부모 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)에 의존 (셔플 필요) | ✅ (Stage 분리) |
| Narrow 예시 | map, filter, union | - |
| Wide 예시 | groupByKey, [join](/studynote/05_database/04_transactions_concurrency/521_join/), sortByKey, distinct | - |

### 계보 (Lineage) 기반 내결함성

```
Lineage 복구 메커니즘
+-------------------------------------------------------------+
|  초기 상태:                                                  |
|  HDFS -> rdd1 -> rdd2 -> rdd3 (파티션 0,1,2,3)                |
|                                                             |
|  장애: rdd3의 파티션 2 손실                                  |
|  +------------------------------------------------------+  |
|  |  ❌ 기존 복제 방식: 복제본 필요 (디스크/메모리 2~3배)   |  |
|  |  ✅ Lineage 방식: 계보를 따라 파티션 2만 재계산        |  |
|  |     HDFS 파티션 2 -> rdd1_p2 -> rdd2_p2 -> rdd3_p2      |  |
|  +------------------------------------------------------+  |
|                                                             |
|  장점: 메모리 복제 오버헤드 없음                             |
|  단점: 긴 Lineage의 재계산 비용 -> 주기적 체크포인팅 권장    |
+-------------------------------------------------------------+
```

📢 **섹션 요약 비유**: [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)는 "요리 레시피 최적화 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)"다. 재료 씻기->썰기->볶기를 각각 따로 실행하지 않고, "한 번에 씻으면서 썰고 바로 볶는" 파이프라인으로 최적화한다. 셔플이 필요한 단계에서만 재료를 교환(Stage 경계)한다.

---

## Ⅲ. 비교 및 연결

### Spark [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 발전: [RDD](/studynote/13_cloud_architecture/05_data_engineering/310_audit/) -> DataFrame -> Dataset

| [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) | 등장 | 특징 | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) |
|:---|:---|:---|:---|
| [RDD](/studynote/13_cloud_architecture/05_data_engineering/310_audit/) | Spark 1.0 | 저수준, 타입 안전, 최대 유연성 | 수동 최적화 필요 |
| DataFrame | Spark 1.3 | 고수준, [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 기반, Catalyst 최적화 | 자동 최적화 |
| Dataset | Spark 1.6 | [RDD](/studynote/13_cloud_architecture/05_data_engineering/310_audit/) 타입 안전성 + DataFrame 최적화 | DataFrame과 동일 |

> **현재 권장**: SparkSQL + Dataset/DataFrame [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 사용. RDD는 저수준 제어가 필요한 경우만 사용.

### Catalyst [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)

Spark SQL의 Catalyst [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)는 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 계획(Logical Plan)을 최적화된 물리 계획(Physical Plan)으로 변환한다.

```
Catalyst 최적화 파이프라인
+--------------------------------------------------------------+
|  SQL/DataFrame 코드                                          |
|          v                                                   |
|  Unresolved Logical Plan  (파싱)                             |
|          v                                                   |
|  Resolved Logical Plan    (카탈로그 메타데이터 바인딩)         |
|          v                                                   |
|  Optimized Logical Plan   (Catalyst 룰 기반 최적화)           |
|          | 예: Predicate Pushdown, Column Pruning             |
|          v                                                   |
|  Physical Plan(s)         (여러 물리 실행 계획 생성)           |
|          v                                                   |
|  Selected Physical Plan   (비용 기반 최적 계획 선택)           |
|          v                                                   |
|  코드 생성 (Tungsten 엔진)  -> JVM 바이트코드 최적화            |
+--------------------------------------------------------------+
```

| 최적화 기법 | 설명 | 효과 |
|:---|:---|:---|
| Predicate Pushdown | WHERE 조건을 최대한 앞 단계(소스)에서 적용 | 불필요한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 로딩 방지 |
| Column [Pruning](/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/) | SELECT에 없는 컬럼 조기 제거 | 컬럼형 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)([Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)) 효율 극대화 |
| [Join](/studynote/05_database/04_transactions_concurrency/521_join/) Reordering | 작은 테이블을 앞에 배치 | 중간 결과 크기 최소화 |
| Broadcast [Join](/studynote/05_database/04_transactions_concurrency/521_join/) | 작은 테이블을 모든 노드에 브로드캐스트 | 셔플 제거 |

📢 **섹션 요약 비유**: Catalyst [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)는 "여행 경로 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 최적화"다. 출발지->목적지를 말하면(SQL 코드), AI가 가장 빠른 환승 경로를 계산([논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)->물리 계획 최적화)해서 최단 시간 루트([실행 계획](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/))를 선택한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### Spark [캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

```
캐싱 저장 수준 (Storage Level)
+------------------------------------------------------------+
|  MEMORY_ONLY      : RAM만 사용, 부족 시 파티션 버림         |
|  MEMORY_AND_DISK  : RAM 우선, 넘치면 디스크 (권장)          |
|  DISK_ONLY        : 디스크만 (장기 캐시)                    |
|  MEMORY_ONLY_SER  : 직렬화해서 RAM에 저장 (메모리 절약)     |
|  OFF_HEAP         : JVM 밖 메모리 (GC 영향 없음)             |
+------------------------------------------------------------+
```

### 실무 시나리오: 이커머스 실시간 추천 엔진

| 단계 | 기술 | 역할 |
|:---|:---|:---|
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집 | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) | 클릭 이벤트 실시간 스트리밍 |
| 스트리밍 처리 | [Spark Structured Streaming](/studynote/16_bigdata/03_spark/061_structured_streaming/) | 10초 마이크로배치 윈도우 처리 |
| 특성 추출 | [Spark MLlib](/studynote/16_bigdata/03_spark/062_spark_mllib/) ALS | [협업 필터링](/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/) 모델 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 계산 |
| 모델 학습 | Spark ML ([RDD](/studynote/13_cloud_architecture/05_data_engineering/310_audit/) [캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)) | K-Means 반복 학습 (메모리 효율) |
| 서빙 | SparkSQL + [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/) | 추천 결과 캐시 |

**결과**: [MapReduce](/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 기반 대비 모델 학습 시간 1시간 -> 5분 (12배 향상)

### 기술사 논술 핵심 포인트

1. <strong><a href="/studynote/13_cloud_architecture/05_data_engineering/310_audit/">RDD</a> vs DataFrame 선택 기준</strong>: 타입 안전성과 저수준 제어가 필요한 경우 [RDD](/studynote/13_cloud_architecture/05_data_engineering/310_audit/), [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석·SQL 중심이면 DataFrame/Dataset을 선택. 구체적 예시와 함께 서술.
2. <strong><a href="/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/">지연 평가</a>의 양면성</strong>: [실행 계획](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) 최적화라는 장점이 있지만, `collect()` 전에 에러가 발견되지 않는 디버깅 어려움이 단점. `count()`나 중간 `show()`로 계보 중간 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 필요.
3. <strong>Lineage vs <a href="/studynote/16_bigdata/03_spark/071_checkpointing/">체크포인팅</a></strong>: 짧은 Lineage는 재계산이 빠르지만, Lineage가 수백 단계면 재계산 비용이 크다. `checkpoint()`를 주기적으로 설정해 Lineage를 절단하는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 제시.

📢 **섹션 요약 비유**: [지연 평가](/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/)는 "마트 쇼핑 목록을 다 적은 다음 한 번에 최적 경로로 쇼핑하는 것"이다. 메모 하나마다 달려가면(즉시 실행) 과일 코너를 5번 왔다갔다 하지만, 목록을 다 적고 최적 경로를 계획하면 한 번만 돌아도 된다.

---

## Ⅴ. 기대효과 및 결론

### Spark 도입 효과

| 효과 영역 | 수치 사례 | 설명 |
|:---|:---|:---|
| [배치 처리](/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/) 속도 | [MapReduce](/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 대비 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~100배 향상 | 인메모리 처리, Catalyst 최적화 |
| ML 학습 속도 | [MapReduce](/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 대비 100배 (반복 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) | [RDD](/studynote/13_cloud_architecture/05_data_engineering/310_audit/) [캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)으로 I/O 제거 |
| 코드 간결성 | 코드량 [MapReduce](/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 대비 80% 감소 | 고수준 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) (SQL, DataFrame) |
| 통합성 | 배치·스트리밍·ML·SQL 단일 플랫폼 | 중복 인프라 제거 |

### Spark 한계 및 발전

| 한계 | 현황 | 발전 방향 |
|:---|:---|:---|
| 메모리 의존성 | [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) ([Out of Memory](/studynote/02_operating_system/02_process_thread/157_oom_killer/)) 장애 빈발 | [Project](/studynote/05_database/01_db_architecture_relational/042_relational_algebra_project/) Tungsten (오프힙 메모리) |
| 스트리밍 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | [Structured Streaming](/studynote/16_bigdata/03_spark/061_structured_streaming/) 수 초 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | [Apache Flink](/studynote/14_data_engineering/05_exam_keywords/215_flink_native_stream_watermark_window_time/) (진정한 이벤트 스트리밍) |
| 소규모 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) | 다수의 소규모 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 처리 비효율 | [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/), Iceberg ([파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 컴팩션) |

### 결론

Apache Spark는 인메모리 [RDD](/studynote/13_cloud_architecture/05_data_engineering/310_audit/), [지연 평가](/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/), [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/), Catalyst [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)를 통해 빅데이터 처리의 패러다임을 바꿨다. 단순 [배치 처리](/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/)부터 스트리밍, [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/), SQL 분석까지 통합한 범용 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 처리 엔진으로 자리매김했으며, 현재도 클라우드 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼의 핵심 처리 엔진으로 사용된다.

📢 **섹션 요약 비유**: Apache Spark는 "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 세계의 멀티툴 스위스 아미 나이프"다. 칼(배치), 가위(스트리밍), 드라이버(ML), [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(SQL) 기능이 하나에 있어서, 각기 다른 도구를 가방에 넣을 필요가 없다. 다만 모든 도구를 항상 주머니(메모리)에 넣고 다녀야 한다는 점이 단점이다.

---

### 📌 관련 개념 맵
| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 핵심 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) | [RDD](/studynote/13_cloud_architecture/05_data_engineering/310_audit/) ([Resilient Distributed Dataset](/studynote/14_data_engineering/01_infrastructure/025_spark_rdd_resilient_distributed_dataset/)) | 불변·[분산](/studynote/08_algorithm_stats/08_stats/136_variance/)·내결함 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 컬렉션 |
| 최적화 원리 | [지연 평가](/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/) ([Lazy Evaluation](/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/)) | Action 호출 시 [실행 계획](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) 일괄 최적화 |
| 장애 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | Lineage (계보) | [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 손실 시 재계산 경로 기록 |
| 실행 구조 | [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) ([Directed Acyclic Graph](/studynote/06_ict_convergence/03_cloud_infrastructure/255_apache_airflow_dag/)) | 변환 단계를 방향성 비순환 그래프로 표현 |
| 최적화 엔진 | [Catalyst Optimizer](/studynote/16_bigdata/03_spark/057_catalyst_optimizer/) | SQL/DataFrame [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 최적화 |
| 상위 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) | DataFrame / Dataset | [RDD](/studynote/13_cloud_architecture/05_data_engineering/310_audit/) 위의 고수준 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) |
| 관련 기술 | [Apache Flink](/studynote/14_data_engineering/05_exam_keywords/215_flink_native_stream_watermark_window_time/) | 진정한 이벤트 스트리밍 (Spark 보완재) |

### 👶 어린이를 위한 3줄 비유 설명
1. RDD는 "마법 스티커 책"이에요. 페이지를 찢어도([파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 손실) 어떻게 만들었는지 기억(Lineage)하기 때문에 다시 만들 수 있어요.

### 📈 관련 키워드 및 발전 흐름도

```text
MapReduce (디스크 기반, 느림)
    |
    v
Spark RDD: 인메모리 · Lazy Evaluation · Lineage 복구
    |
    v
DataFrame / Dataset API: 스키마 기반 · Catalyst 최적화
    |
    v
Spark SQL · Structured Streaming · MLlib
    |
    v
Photon (Databricks) · Spark Connect (원격 실행)
```
2. [지연 평가](/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/)는 "쇼핑 목록을 다 적은 다음 한 번에 효율적으로 쇼핑하는 것"이에요. 중간에 불필요한 물건을 AI가 목록에서 지워줘요.
3. DAG는 "요리 레시피 흐름도"예요. 어떤 재료([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))가 어떤 순서로 섞여야 완성 요리(결과)가 나오는지 그림으로 보여줘요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 206 / 258

<- **이전**: [205. 셔플·정렬 (Shuffle & Sort)과 YARN (Yet Another Resource Negotiator)](/studynote/14_data_engineering/05_exam_keywords/205_shuffle_sort_yarn_resource_manager/)
**다음**: [207. 데이터 레이크 (Data Lake) 스키마 온 리드 (Schema-on-Read)](/studynote/14_data_engineering/05_exam_keywords/207_data_lake_schema_on_read_raw_storage/) ->

---
