+++
title = "25. Spark RDD (Resilient Distributed Dataset) — 내결함성 분산 데이터셋"
date = 2026-04-29

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) (Resilient Distributed Dataset, 내결함성 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋)는 Apache Spark의 핵심 추상화로, 클러스터 전체에 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)된 불변([Immutable](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/298_immutable/)) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)의 집합이다. Resilient는 "복원력 있는(내결함성)"을 의미하며, 리니지(Lineage) 정보를 통해 노드 장애 시 실패한 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)만 재계산하여 자동 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)한다.
> 2. **가치**: RDD는 MapReduce보다 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~100배 빠른 인메모리(In-memory) 처리를 가능하게 하여 반복 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)(ML 훈련 루프)과 대화형 분석(REPL)을 실용화했다. 트랜스포메이션(Transformation)의 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 실행([Lazy Evaluation](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/))과 [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) ([Directed Acyclic Graph](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/255_apache_airflow_dag/), 방향 비순환 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)) 기반 [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) 최적화로 효율적인 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리를 실현한다.
> 3. **판단 포인트**: 현대 Spark 개발에서는 RDD보다 DataFrame/Dataset API를 권장한다. DataFrame은 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 정보를 가지며 Catalyst Optimizer에 의해 자동 최적화되어 동등한 [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) 코드보다 훨씬 빠르다. 하지만 저수준 커스텀 처리나 [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) 처리에는 여전히 RDD가 필요하다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">RDD 핵심 특성</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. 분산 (Distributed): 여러 노드에 파티션으로 분산 저장</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2. 불변 (Immutable): 한번 생성 후 수정 불가, 변환만 가능</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3. 내결함성 (Resilient): 리니지 그래프로 자동 재계산 복구</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4. 지연 실행 (Lazy): Action 호출 시만 실제 계산 수행</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">5. 타입 안전 (Type-safe): 컴파일 타임 타입 체크</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: RDD는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 창고의 배송 주문서 모음이다. 각 창고(노드)에 배분된 주문서([파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/))들을 모아 처리하고, 창고 하나가 불이 나도(노드 장애) 원본 주문서 제작 과정(리니지)을 기억하니 다시 만들 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) 연산 유형

```python
from pyspark import SparkContext
sc = SparkContext()

# 1. RDD 생성
rdd = sc.textFile("s3://bucket/data.txt")  # 외부 데이터에서 생성

# 2. Transformation (변환) - Lazy: 실행 계획만 등록
words = rdd.flatMap(lambda line: line.split(" "))
pairs = words.map(lambda w: (w, 1))
counts = pairs.reduceByKey(lambda a, b: a + b)

# 3. Action (액션) - Eager: 실제 계산 트리거
result = counts.collect()   # 드라이버로 수집
counts.saveAsTextFile("s3://bucket/output")  # 저장
```

### [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) 및 리니지



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">textFile → flatMap → map → reduceByKey</div>
<div class="kb-diagram-note">Stage1: Stage2: Stage2: Stage3:</div>
<div class="kb-diagram-note">읽기 변환 변환 셔플+집계</div>
<div class="kb-diagram-note">리니지 (Lineage):</div>
<div class="kb-diagram-note">rdd → words → pairs → counts</div>
<div class="kb-diagram-note">(만약 pairs 손실 → words부터 재계산)</div>
</div>
</div>



### [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) vs DataFrame [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비교

| 항목 | [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) | DataFrame |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/">스키마</a></strong> | 없음 (타입 추론 없음) | 있음 (컬럼 이름·타입) |
| **최적화** | 없음 (수동 최적화) | [Catalyst Optimizer](/knowledge-base/studynote/16_bigdata/03_spark/057_catalyst_optimizer/) 자동 최적화 |
| **직렬화** | Java 직렬화 (느림) | Tungsten [인코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/) (빠름) |
| **사용 권장** | [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/), 커스텀 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/) | [정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/002_structured_data/), 일반 분석 |

- **📢 섹션 요약 비유**: RDD는 수동 변속기 자동차, DataFrame은 자동 변속기 자동차다. 수동([RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/))은 더 세밀한 제어가 가능하지만 조작이 복잡하고, 자동(DataFrame)은 엔진(Catalyst)이 최적 기어를 알아서 찾아 더 효율적이다.

---

## Ⅲ. 비교 및 연결



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Spark API 계층:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">고수준 (High-Level)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Spark SQL / DataFrames / Datasets (ML, ETL)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">↓ Catalyst Optimizer + Tungsten</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">중수준 (Mid-Level)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Dataset</div><div class="kb-diagram-node">T</div><div class="kb-diagram-note">(Scala/Java 타입 안전 DataFrame)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">↓ RDD 기반 실행</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">저수준 (Low-Level)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">RDD (직접 파티션/셔플 제어 필요 시)</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: RDD는 어셈블리어(저수준, 강력하지만 복잡)이고 DataFrame은 파이썬(고수준, 편리하고 최적화 자동)이다. 일반 작업은 파이썬, 시스템 수준 제어는 어셈블리를 쓰는 것처럼 선택한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: 사용자 지정 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)이 필요한 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 처리

```python
# DataFrame은 조인 키 기반 파티셔닝만 지원
# 커스텀 파티셔닝이 필요한 경우 RDD 직접 사용
from pyspark import SparkContext

def hash_partition(key):
    # 특정 비즈니스 로직 기반 파티셔닝
    return ord(key[0]) % 100

graph_rdd = sc.parallelize(edges)     .partitionBy(100, hash_partition)     .persist()  # 반복 접근을 위해 메모리 캐시

# 그래프 알고리즘 반복 실행 (ML, PageRank 등)
for i in range(100):
    graph_rdd = graph_rdd.map(update_function)
```

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 단순 집계·필터링에 RDD를 사용하는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/). DataFrame이 동일 로직에서 Catalyst 최적화로 2~5배 빠르다. RDD는 DataFrame으로 표현 불가한 복잡한 커스텀 로직에만 사용해야 한다.

- **📢 섹션 요약 비유**: 단순 이메일 작성에 C언어를 쓰는 것처럼, 간단한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석에 RDD를 쓰는 것은 과도한 저수준 도구 사용이다. 도구는 목적에 맞게 선택해야 한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **인메모리 처리** | [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 대비 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~100배 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상 |
| **내결함성** | 리니지 기반 자동 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) |
| **유연성** | 커스텀 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)·직렬화 완전 제어 |

Spark 3.x에서 RDD는 Adaptive Query Execution (AQE)과 직접 통합되지 않아 DataFrame 대비 자동 최적화 혜택이 적다. GraphX, MLlib의 내부 구현은 여전히 [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) 기반이나, 사용자 API는 DataFrame 기반으로 이전하고 있다.

- **📢 섹션 요약 비유**: RDD는 Spark의 토대이자 엔진이다. 대부분의 경우 최신 고수준 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)(DataFrame)를 타고 가지만, 엔진([RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/)) 자체를 이해하면 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 문제가 발생했을 때 근본 원인을 정확히 진단할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **DataFrame/Dataset** | [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) 기반의 고수준 최적화 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) |
| <strong><a href="/knowledge-base/studynote/16_bigdata/03_spark/057_catalyst_optimizer/">Catalyst Optimizer</a></strong> | DataFrame의 자동 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 최적화 엔진 |
| **리니지 (Lineage)** | [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) 내결함성의 핵심 메커니즘 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/">DAG</a> <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/">스케줄러</a></strong> | [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) 연산 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)를 Stage로 분해 |
| **Tungsten** | 메모리·CPU 효율 최적화 실행 엔진 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">MapReduce — 디스크 기반 분산 처리, 느림</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Spark RDD — 인메모리 분산 처리, 리니지 기반 복구</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">DataFrame/Dataset — 스키마+Catalyst 자동 최적화</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Structured Streaming — 통합 배치·스트리밍 API</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Delta Lake + Spark — ACID 트랜잭션 레이크하우스</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. RDD는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)된 메모장이에요! 여러 컴퓨터(노드)에 나눠 저장하고, 한 컴퓨터가 고장나도 메모를 다시 만드는 방법(리니지)을 기억해요.
2. 실제로 계산은 필요할 때만 해서([지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 실행) 불필요한 낭비를 줄이고, 인메모리 처리로 디스크보다 100배 빠르게 처리해요.
3. 요즘은 더 쉬운 DataFrame API를 주로 쓰지만, RDD는 Spark의 기초 엔진으로 여전히 중요하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 25 / 258

← **이전**: [24. Apache Flink — 네이티브 실시간 스트림 처리 엔진](/knowledge-base/studynote/14_data_engineering/01_infrastructure/024_apache_flink_stream_processing/)
**다음**: [26. Kafka 토픽 파티션 (Topic Partition) — 분산 스트림 병렬 처리](/knowledge-base/studynote/14_data_engineering/01_infrastructure/026_topic_partition/) →

---
