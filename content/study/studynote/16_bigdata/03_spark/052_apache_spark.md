---
title: 01. Apache Spark — 인메모리 분산 처리 엔진 (Unified Analytics Engine)
date: '2026-04-05'
tags:
- studynote-bigdata
---

# [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] - 인메모리 [[136_variance|분산]]処理의 황량한 변신

> ⚠️ 이 문서는 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] MapReduce의 디스크 입출력 병목(Disk I/O [[617_io_bottleneck|Bottleneck]])을 인메모리(In-Memory) 연산으로 완전 탈피하여 실제 벤치마크에서 최대 100배 빠른 [[282_performance_tactics|성능]]을 달성한 차세대 [[136_variance|분산]] 처리 엔진인 Apache Spark의 핵심 아키텍처, [[310_audit|RDD]] 체계, 그리고 다양한 워크로드(DataFrame/SQL/ML/[[104_graph|Graph]])를 단일 플랫폼에서 unified(통합) 처리하는 [[057_stack|스택]] 구조를 기술사 수준에서 심층 분석합니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache Spark는 [[843_hadoop_rack_awareness_data_replication_topology|하둡]] [[018_mapreduce|맵리듀스]]의 [[228_batch_processing_hadoop_spark|배치 처리]]만 가능하다는 약점을 인메모리 연산으로 완전히 제거하고, 배치处理·스트리밍·[[241_machine_learning_basics|머신러닝]]·[[114_graph_analytics|그래프 분석]]을 하나의 통합 플랫폼에서 모두 수행할 수 있는 범용 [[136_variance|분산]] 컴퓨팅 엔진이다.
> 2. **가치**: [[018_mapreduce|맵리듀스]]는 각 단계 사이에 디스크에 [[001_dikw_pyramid|데이터]]를 읽고 써야 했지만(입출력 병목), 스파크는 [[310_audit|RDD]](불변 [[136_variance|분산]] [[001_dikw_pyramid|데이터]]셋)를 메모리에 캐시하여 네트워크를 통한 Shuffle 단계에서도 디스크 접근을 최소화하여Same-Result를 훨씬 빠른 속도로 산출한다.
> 3. **확장**: 스칼라로 작성되었지만 파이썬(PySpark), 자바, R, SQL 등 다양한 언어 바인딩을 제공하여 [[001_dikw_pyramid|데이터]] 엔지니어뿐 아니라 [[001_dikw_pyramid|데이터]] 사이언티스트까지 하나의 생태계에서 협업할 수 있는 통합 [[001_dikw_pyramid|데이터]] 플랫폼으로 자리잡았다.

---

## Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

### 1. [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] MapReduce의 구조적 한계
[[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] MapReduce는 2000년대 초반 빅데이터 처리 혁명의 중심에 있었지만, 필연적 구조적 제약이 존재했습니다.
- **디스크 병목 (Disk [[617_io_bottleneck|Bottleneck]])**: Map [[150_task|태스크]]의 출력은 HDFS에 기록되고, Reduce [[150_task|태스크]]는 네트워크를 통해 그 [[001_dikw_pyramid|데이터]]를 가져와야 했습니다. 이 Map→Shuffle→Reduce 사이클의 모든 단계에서 디스크 읽기/[[289_cqrs_db|쓰기]](Disk I/O)가 발생하여 CPU 바쁜 연산보다 디스크 대기가 전체 처리 시간을 지배하는 비효율이 발생했습니다.
- **반복 처리 비효율 (Iteration Inefficiency)**: [[241_machine_learning_basics|머신러닝]] [[001_algorithm_definition|알고리즘]](예: K-Means, PageRank)은 동일한 [[001_dikw_pyramid|데이터]]셋을 수십 회에서 수백 회 반복 처리해야 합니다. [[018_mapreduce|맵리듀스]]는 매 반복마다 디스크에 중간 결과를 읽고 써야 하므로, 10회 반복에서 10배의 디스크 입출력이 발생하여 수렴까지 수 일이 소요되었습니다.
- **단일 목적局限**: 배치 배치만 가능하여 스트리밍이나 대화형 [[298_qkv_attention|쿼리]]에는 별도 시스템([[060_spark_streaming_dstream|Spark Streaming]], Impala 등)을 도입해야 했고, 이로 인해 아키텍처가 급격히 복잡해지고 운영 비용이 증가하는 "스파겔리(Spaghetti) 아키텍처"에 빠지는 문제가 대두되었습니다.

### 2. Apache Spark의 등장 배경
[[087_underpinning_contract|UC]] Berkeley AMPLab(Algorithms, Machines, and People Lab)에서 2010년 처음 공개된 Apache Spark는 위의 모든 한계를 단번에 해결하는 패러다임 시프트를 구현했습니다.
- **연구 동기**: 전형적인 ML [[123_pipe|파이프]]라인인 "_iterative map-reducejobs for learning_"를 기존 Hadoop보다 [[489_raid_10_hybrid|10]]~20배 빠르게 실행할 수 있는 범용 연산 엔진 개발이 목표였습니다.
- **핵심 혁신**: 디스크 대신 메모리(RAM)에 처리 중 [[001_dikw_pyramid|데이터]]셋을 상주시키는 인메모리(In-Memory) 컴퓨팅 모델을 도입하여 디스크 입출력 병목을 완전 제거했습니다. 메모리 가격이 매년 하락하고服务器的RAM 용량이TB 단위로 증가하던 시대적 배경도 함께 작용했습니다.
- **2009-2010년 AMPLab 연구 성과**: "Spark: [[383_cluster_computing|Cluster Computing]] with Working Sets" 논문 발표 후 2010년 [[191_oss_license_compliance|오픈소스]] 공개, 2013년 Apache Incubator 통과, 2014년 Apache Top-Level [[042_relational_algebra_project|Project]] 등용, 2025년 현재 Spark 3.5.x까지演进하여 빅데이터 처리 분야 de facto 표준으로 자리잡았습니다.

- **📢 섹션 요약 비유**: [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] MapReduce는 "매 끼니마다 장을 보고 요리하고 설거지를 다 해야 하는 식당(디스크 반복 [[289_cqrs_db|쓰기]])"이라면, Apache Spark는 "냉장고(메모리)에 재료를 미리 준비해 두고 손님 주문이 들어오면 즉석에서 즉시 요리하는米其林 레스토랑(메모리 상주 연산)"입니다. 동일한 레시피([[001_algorithm_definition|알고리즘]])라도 냉장고 접근 속도가 장보기 속도보다 압도적으로 빠른 것처럼, 스파크는 [[001_dikw_pyramid|데이터]]가 메모리에 상주하기에 디스크 [[467_disk_access_time|Seek Time]] 없이 CPU가 쉬지 않고 연산에만 집중할 수 있습니다.

---

## Ⅱ. 핵심 아키텍처 및 원리 ([[319_architecture|Architecture]] & Mechanism)

```text
┌─────────────────────────────────────────────────────────────────┐
│                [ Apache Spark 실행 아키텍처 ]                    │
│                [ Apache Spark Execution Architecture ]           │
│                                                                 │
│  [Driver Process / 드라이버 프로세스] ─────────────────────     │
│    │ "SparkContext" 관리, DAG 스케줄링, 태스크 직렬화           │
│    │ (SparkContext Mgmt, DAG Scheduling, Task Serialization)    │
│    │                                                             │
│  [Cluster Manager / 클러스터 매니저] ─ YARN / K8s / Standalone   │
│    │           (클러스터 자원 전체 관리)                          │
│    │           (Cluster Resource Management)                     │
│    │                                                             │
│  [Executor Process] ─────────── [Executor Process]              │
│  [익제큐터 프로세스]            [익제큐터 프로세스]              │
│    │  "Task" 실행                          │                    │
│    │  (Task Execution)                     │                    │
│    │  JVM 프로세스 단위                     │                    │
│    │  (JVM Process Unit)                   │                    │
│    │  ├─ 메모리에 RDD 캐시               ├─ 동일 연산            │
│    │  │  (Cache RDD in RAM)              │  (Same Operation)     │
│    │  └─ 결과 디스크 쓰기 (체크포인트)     │                    │
│    │     (Write Result to Disk)            │                    │
│                                                                 │
│  [RDD (Resilient Distributed Dataset)]                          │
│    - 불변성 (Immutable): 생성 후 데이터 변경 불가                │
│    - 분산 (Distributed): 클러스터 전체에 파티셔닝                 │
│    - 결함 허용 (Resilient): Lineage(혈통)로 자동 복구            │
│                                                                 │
│  [DataFrame / Dataset API]                                      │
│    - 스키마 존재, Catalyst Optimizer가 최적의 물리 실행 계획 선택 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1. [[310_audit|RDD]] ([[025_spark_rdd_resilient_distributed_dataset|Resilient Distributed Dataset]])의 5대 특성
RDD는 스파크의 근간이 되는 불변 [[136_variance|분산]] 컬렉션으로, 다음 5가지 [[082_attribute_types_er_model|속성]]이 보장되어야 합니다.

| [[310_audit|RDD]] 특성 | 설명 | 예시 |
|:---|:---|:---|
| **불변성 ([[298_immutable|Immutable]])** | 한 번 [[087_process_state_transition|생성]]된 RDD는 수정 불가, 새 RDD만 [[087_process_state_transition|생성]] | `rdd.map(x => x * 2)` → 새 [[310_audit|RDD]] 반환 |
| **[[136_variance|분산]] (Distributed)** | 클러스터 여러 노드에 [[514_partition_slice_volume|파티션]] 단위로 저장 | 10개 노드 × 각 2 [[514_partition_slice_volume|파티션]] = 20 [[514_partition_slice_volume|파티션]] |
| **[[296_fault_tolerance_architecture|결함 허용]] (Resilient)** | Lineage(작업 혈통) [[070_graph_datastructure|그래프]]로 손실 자동 [[658_ir_recovery|복구]] | 부모 RDD가 손실되면 재컴퓨팅 |
| **[[023_lazy_evaluation|지연 평가]] ([[023_lazy_evaluation|Lazy Evaluation]])** | 액션 호출 전까지 변환 연산을 실행하지 않음 | `collect()` 호출 시 비로소 실행 |
| **[[179_table_partitioning_concept|파티셔닝]] (Partitioned)** | [[001_dikw_pyramid|데이터]]가 사용자에게 투명하게 분할 저장 | `repartition(n)`으로 [[514_partition_slice_volume|파티션]] 수 조절 |

### 2. [[401_bayesian_network_dag_causality|DAG]] ([[255_apache_airflow_dag|Directed Acyclic Graph]]) 실행 모델
스파크의 작업 실행은 Stage(단계)로 구분되는 [[401_bayesian_network_dag_causality|DAG]] 기반입니다.

1. **사용자 코드 작성**: `sc.textFile("log.txt").filter(_.contains("ERROR")).map(_.split(",")).collect()`
2. **[[401_bayesian_network_dag_causality|DAG]] 구성**: 스파크는 이 코드를 [[380_computational_graph_lazy_eager_execution|lazy]] evaluation에 따라一棵 [[401_bayesian_network_dag_causality|DAG]] [[070_graph_datastructure|그래프]]로 기록합니다. `textFile → filter → map`이 노드가 되고, `collect`가 최종 액션 노드가 됩니다.
3. **Stage 분리**: 스파크는 DAG를 분석하여 "Shuffle 경계([[001_dikw_pyramid|데이터]]를 네트워크로 전송해야 하는 지점)"를 기준으로 Stage를 분리합니다. Shuffle이 필요 없는 [[123_pipe|파이프]]라인 연산([[082_pipeline|pipeline]])은同一个 Stage 내에서 모두 실행됩니다.
4. **[[150_task|Task]] [[087_process_state_transition|생성]]**: 각 Stage는 여러 [[150_task|태스크]]([[150_task|Task]])로 분할되어 각 [[514_partition_slice_volume|파티션]]에 할당됩니다. [[514_partition_slice_volume|파티션]]이 100개면 [[150_task|태스크]]도 100개가 [[087_process_state_transition|생성]]됩니다.
5. **실행**: Cluster Manager가 각 노드의 Executor에 [[150_task|태스크]]를 분배하고, [[150_task|태스크]]는 자신의 [[514_partition_slice_volume|파티션]]에 대해 연산을 수행합니다.

### 3. Spark의 핵심 최적화 기법

- **[[123_pipe|Pipe]]-lining**: Shuffle이 필요 없는 연속된 변환(map→filter→map)은 하나의 Stage로 합쳐서 [[123_pipe|파이프]]라인 실행하여 중간 디스크 [[289_cqrs_db|쓰기]]를 완전 제거합니다.
- **메모리 관리**: 스파크는 [[078_heap_datastructure|Heap]] 메모리를 Execution(연산) 영역과 Storage(캐시/[[310_audit|RDD]] 보존) 영역으로 나누어 관리합니다. 기본적으로 Execution 60%, Storage 40%이며, `spark.memory.fraction`으로 비율을 조절할 수 있습니다.
- **카탈리스트 [[163_optimizer_sql_execution_plan_generator|옵티마이저]] ([[057_catalyst_optimizer|Catalyst Optimizer]])**: DataFrame/SQL 연산에서 [[369_logic_bomb|논리]] 계획(Logical Plan) → 물리 계획(Physical Plan) 변환 시 비용 기반 최적화(Cost-Based Optimization)를 수행하여 [[176_join_order_optimization|조인 순서]], 필터 적용 순서, [[154_database_index_b_tree_search_optimization|인덱스]] 활용 등을 자동 결정합니다.
- **코드 [[087_process_state_transition|생성]] (Whole-Stage Codegen)**: 여러 연산자를 하나의 JVM [[074_byte|바이트]]코드로 컴파일하여 [[294_function_calling_tool_use|함수 호출]] 오버헤드를 최소화합니다. Tungsten 프로젝트의 일환으로 [[282_performance_tactics|성능]]이 10배 이상 향상되었습니다.

---

## Ⅲ. 비교 및 기술적 트레이드오프 (Comparison & Trade-offs)

| 비교 항목 | [[395_hadoop_mapreduce_disk_bottleneck|Hadoop MapReduce]] | [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] (인메모리) |
|:---|:---|:---|
| **처리 속도** | 디스크 I/O로 인해 수십 배 느림 | 인메모리 연산으로 최대 100배 빠름 |
| **iterative ML** | 매 반복마다 디스크 읽기/[[289_cqrs_db|쓰기]] → 수일 소요 | 메모리에 [[001_dikw_pyramid|데이터]] 유지 → 수시간 내 수렴 |
| **실시간 스트리밍** | 불가능 (별도 Storm/[[060_spark_streaming_dstream|Spark Streaming]] 필요) | Structured Streaming으로 통합 처리 가능 |
| **[[352_defect_definition|결함]] [[658_ir_recovery|복구]]** | 중복 [[001_dikw_pyramid|데이터]]로 [[658_ir_recovery|복구]] (3중 [[016_replication_factor|복제]]) | Lineage [[070_graph_datastructure|그래프]]로 필요 [[514_partition_slice_volume|파티션]]만 재컴퓨팅 |
| **메모리 요구량** | 낮음 (디스크 기반) | 높음 (클러스터 RAM 용량에 의존) |
| **가장 큰 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]** | 확장을 해도 디스크 병목이 [[282_performance_tactics|성능]] ceiling이 됨 | [[157_oom_killer|OOM]](메모리 부족) 시 디스크로 fell back → [[282_performance_tactics|성능]] 급락 |

- **📢 섹션 요약 비유**: [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] MapReduce와 Apache Spark의 차이는 "편의점 도시락(배달=디스크 [[289_cqrs_db|쓰기]], 수령=디스크 읽기)을 매 끼니마다 주문해야 하는 직원 식당"과 "직원이 자신의 책상 서랍(메모리)에 도시락을 미리储备해 두고 매 끼니마다 즉석에서 데워 먹는 사내 식당"의 차이와 같습니다. 도시락이 맛있어도 배달 대기 시간이 식사 시간보다 길어 본인의 업무 시간이 낭비되는 것과 동일한 원리입니다.

---

## Ⅳ. 실무 판단 기준 (Decision Making)

| 고려 사항 | 세부 내용 | 주요 의사결정 |
|:---|:---|:---|
| **[[001_dikw_pyramid|데이터]] 규모** | 수십 TB 이상일 때 Spark의 인메모리 장점 극대화 | 소규모(수백 GB 이하)엔 Spark 오버헤드大于 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] |
| **iterative 연산 빈도** | ML 훈련, [[114_graph_analytics|그래프 분석]] 등 반복 연산 많을수록 Spark 권장 | 일회성 배치엔 Hadoop도 충분한 경우多 |
| **클러스터 메모리** | 전체 클러스터 RAM이 처리 [[001_dikw_pyramid|데이터]]의 2배 이상일 때 안정적 | 메모리 부족 시 disk spilling으로性能劣化 |
| **실시간 요구 수준** | ms~s 단위 [[015_지연_데이터_관점|지연]] 요구 시 [[061_structured_streaming|Structured Streaming]] + Flink 비교 필요 | 분 단위 [[015_지연_데이터_관점|지연]] 허용 시 [[060_spark_streaming_dstream|Spark Streaming]]([[060_spark_streaming_dstream|DStream]])도 가능 |

*(추가 실무 적용 가이드 - Spark 배포 모드 선택)*
- **Local 모드**: 개발/테스트용. 드라이버와 Executor가同一个 JVM에서 실행되어 별도 클러스터 필요 없음. 소규모 [[001_dikw_pyramid|데이터]] 디버깅에最適.
- **[[150_5g_sa_standalone_architecture|Standalone]] 모드**: 스파크 자체内置 클러스터 매니저. 간단한 단일 클러스터 구성에 적합하지만, 프로덕션에서는 [[020_yarn|YARN]]/K8s 사용 권장.
- **[[020_yarn|YARN]] 모드**: 기존 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 인프라 활용. [[013_hdfs|HDFS]] [[001_dikw_pyramid|데이터]] محلية 처리로 네트워크 [[140_bandwidth|대역폭]] 절약. Enterprise [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 사용자首选.
- **[[205_kubernetes_container_orchestration|Kubernetes]] 모드**: Cloud-native 환경에 최적. [[063_docker_architecture|Docker]] [[561_container_based_deployment|컨테이너]] 기반으로 스파크 앱을 표준 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] [[085_pod_kubernetes_container_unit|파드]]として実行. 현대 [[213_msa_microservices_architecture|마이크로서비스 아키텍처]]와 손색なし 통합.
- **실무 [[124_decision_tree|의사결정 트리]]**: (1) 기존 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 인프라 있나요? → Yes: [[020_yarn|YARN]], No: (2) Cloud-nativeですか? → Yes: [[205_kubernetes_container_orchestration|Kubernetes]], No: [[150_5g_sa_standalone_architecture|Standalone]])

- **📢 섹션 요약 비유**: Spark 배포 모드 선택은 "새 식당을 열 때 기존 건물에서 시작({[[020_yarn|YARN]]})するか, 새 건물을 지을지({[[205_kubernetes_container_orchestration|Kubernetes]]}), 아니면 팝업스토어로试水上({Local})"의 결정과 동일합니다. 각都有自己的 비용과 운영 특성이 있으며, 규모와 인프라 환경에 따라 최적의 선택이 달라집니다.

---

## Ⅴ. 미래 전망 및 발전 방향 (Future Trend)

1. **Spark 3.5+의 ANSI SQL 확대 및 Python 네이티브 강화**
   Spark 3.5부터 ANSI SQL:2003 표준 준수가 크게 [[216_progress_in_synchronization|진행]]되어 [[188_pl_sql_t_sql_procedural|Oracle]], PostgreSQL 등 전통 RDBMS에서 작성한 복잡한 SQL [[298_qkv_attention|쿼리]]의大多数를 스파크에서도 그대로 실행할 수 있게 되었습니다. 동시에 PySpark(파이썬)의 API가 네이티브 Scala API에 버금가는 완성도로 성숙하면서, [[001_dikw_pyramid|데이터]] 엔지니어와 [[001_dikw_pyramid|데이터]] 사이언티스트 간의 언어 장벽이 사실상 사라지고 있습니다.

2. **[[146_lakehouse|Lakehouse]] 시대의 Spark 역할**
   [[147_delta_lake|Delta Lake]], [[148_apache_iceberg|Apache Iceberg]], [[149_apache_hudi|Apache Hudi]] 등 [[146_lakehouse|레이크하우스]] 테이블 포맷과 Spark의 결합이 표준화되면서, [[208_data_lake_schema_on_read|데이터 레이크]]의 원시 [[001_dikw_pyramid|데이터]]에 직접 스파크 SQL을 실행하고 ACID [[191_transaction_concept_states|트랜잭션]]을 지원하는 "打开된 [[146_lakehouse|레이크하우스]](Open [[146_lakehouse|Lakehouse]])" 아키텍처가 빠르게 확산되고 있습니다. Databricks의 [[074_photon_engine|Photon Engine]](네이티브 벡터화 실행 엔진)이나 Amazon EMR의 [[209_spot_instance_cloud_cost_optimization|Spot Instance]] 연동 등, 비용 최적화와 [[282_performance_tactics|성능]] 극대화를 동시에 추구하는 방향으로 빠르게 진화하고 있습니다.

3. **Adaptive Query Execution (AQE)의 일상화**
   Spark 3.0에서 도입된 AQE는 런타임 통계에 따라 조인 [[268_strategy_pattern|전략]], [[514_partition_slice_volume|파티션]] 수, [[001_dikw_pyramid|데이터]] 셔플 분할을 자동으로 재조정하는 [[059_adaptive_query_execution_aqe|적응형 쿼리 실행]]입니다. 예를 들어, 조인 시 한쪽 [[001_dikw_pyramid|데이터]]가 크게 쏠려 있다면([[069_skew_join|Skew Join]]) 자동으로 조인 키를 분할하여 처리하는 "스큐 조인 자동 해결" 기능은, 과거 엔지니어가 수동으로 코딩해야 했던 복잡한 최적화 로직을 완전히 자동화하여, 이제는 엔지니어의 주요 업무가 파라미터 튜닝이 아닌 비즈니스 로직 설계로 집중되게 하는 패러다임 시프트를 이끌고 있습니다.

- **📢 섹션 요약 비유**: Apache Spark의 미래 발전은 "혼자 모든 요리를 하던 초보 주방장이던 시절(낡은 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]])"에서, "주방 전체가 자동화 로봇으로 변환되어 인간은 레시피(비즈니스 로직) 설계에만 집중하면 되는 米其林星级自动化厨房"으로 진화하는 과정과 동일합니다. 예전에는 엔지니어가 [[001_dikw_pyramid|데이터]] 이동 경로, [[514_partition_slice_volume|파티션]] [[268_strategy_pattern|전략]], JVM [[380_garbage_collection|가비지 컬렉션]] 튜닝까지 손수 고민해야 했지만, 이제는 스파크가 그 모든 하역 작업을 스스로 최적화하여 인간은 [[001_dikw_pyramid|데이터]]의 의미와 가치創造에만 집중하면 되는 시대가 눈앞에 와 있습니다.

---

## 🧠 지식 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])

*   **[[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] 생태계 전체 트리 (Ecosystem Taxonomy)**
    *   **Spark Core** -> [[310_audit|RDD]] [[014_api_posix|API]], [[150_task|Task]] [[208_schedule_history_transaction_execution_order|스케줄]]링, 메모리 관리, I/O 핸들링
    *   **[[056_spark_sql|Spark SQL]]** -> DataFrame/Dataset [[014_api_posix|API]], [[057_catalyst_optimizer|Catalyst Optimizer]], Spark Thrift Server (ODBC/JDBC)
    *   **[[061_structured_streaming|Structured Streaming]]** -> 연속 처리, 마이크로배치, 상태 관리, [[085_watermark|Watermark]]
    *   **MLlib** -> [[136_variance|분산]] [[241_machine_learning_basics|머신러닝]] ([[104_classification_analysis|분류]]/회귀/군집/[[345_collaborative_filtering|협업 필터링]]/[[247_feature_label_variables|피처]] 추출)
    *   **GraphX** -> [[136_variance|분산]] [[070_graph_datastructure|그래프]] 처리 (PageRank, Connected Components)
*   **Spark 실행 환경 비교**
    *   Local (개발용) < [[150_5g_sa_standalone_architecture|Standalone]] (단일 클러스터) < [[020_yarn|YARN]] (엔터프라이즈 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]]) < [[205_kubernetes_container_orchestration|Kubernetes]] (Cloud-native)
*   **핵심 튜닝 파라미터**
    *   `spark.sql.shuffle.partitions` (기본 200, [[001_dikw_pyramid|데이터]] 크기에 따라 조절)
    *   `spark.sql.adaptive.enabled` (AQE 활성화, Spark 3.0+)
    *   `spark.memory.fraction` (Execution vs Storage 메모리 비율)

---

### 📈 관련 키워드 및 발전 흐름도

```text
[Hadoop MapReduce]
    │
    ▼
[RDD]
    │
    ▼
[Spark SQL]
    │
    ▼
[Structured Streaming]
```

이 흐름도는 선행 개념이 현재 개념으로 응축되고, 다시 확장 개념으로 이어지는 순서를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. Apache Spark는 아주 많은コンピュータ(컴퓨터들)가 함께 일해서 [[001_dikw_pyramid|데이터]]를 엄청나게 빠르게 처리하는 똑똑한 시스템이에요.
2. 다른 컴퓨터들이 각자의 집(서버)에 나눠서 [[001_dikw_pyramid|데이터]]를 처리한 다음, 그 결과들을 모으면 답을 얻을 수 있죠.
3. 마치 학급 친구들이 각각 다른 [[286_page_frame|페이지]]의 책을 읽고, 다 읽으면 각자 배운 내용을分享一下서 전체 책을 빠르게 이해하는 것과 비슷해요!

---
> **🛡️ Expert [[395_verification_process_review|Verification]]:** 본 문서는 Apache Spark의 최신 아키텍처(3.5.x)를 기준으로 구조적 [[003_integrity|무결성]]과 기술사 수준의 심층 분석을 [[395_verification_process_review|검증]]하였습니다. (Verified at: 2026-04-05)
