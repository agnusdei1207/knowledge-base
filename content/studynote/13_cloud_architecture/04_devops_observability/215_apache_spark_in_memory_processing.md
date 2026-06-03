+++
title = "215. 아파치 스파크 (Apache Spark)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Apache Spark는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 메모리(RAM)에 올려 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 연산하는 통합 분석 엔진으로, MapReduce의 디스크 I/O 병목을 제거하여 반복 처리와 실시간 처리에서 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~100배 빠른 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 실현한다.
> 2. **가치**: 배치(Spark Core)·SQL(SparkSQL)·스트리밍([Structured Streaming](/knowledge-base/studynote/16_bigdata/03_spark/061_structured_streaming/))·[머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)(MLlib)·[그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)(GraphX)를 단일 엔진으로 통합하여, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어·[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자·분석가 모두를 하나의 플랫폼에서 지원한다.
> 3. **판단 포인트**: Spark의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 메모리에 의존한다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 메모리를 초과하면 디스크로 spill이 발생하여 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 급격히 저하된다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 크기에 맞는 적절한 executor 메모리 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이 Spark 튜닝의 핵심이다.

---

## Ⅰ. 개요 및 필요성

2009년 [UC](/knowledge-base/studynote/12_it_management/02_itsm_itil/087_underpinning_contract/) Berkeley AMP Lab의 Matei Zaharia가 개발한 Spark는 MapReduce의 근본적 한계—매 처리 단계마다 디스크에 중간 결과를 쓰는 것—을 해결하기 위해 탄생했다. 특히 [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)의 반복 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)([로지스틱 회귀](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/), k-평균 클러스터링)은 수십~수백 번 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 반복 처리하는데, MapReduce로는 각 반복마다 [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 읽기/쓰기가 발생하여 극도로 느렸다.

Spark의 핵심 아이디어: **메모리에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 유지한다(Keep [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) In Memory).** 첫 번째 읽기 시에만 디스크에서 메모리로 로딩하고, 이후 처리는 모두 메모리에서 수행한다. 100번 반복이 필요한 ML [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)에서 [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 대비 최대 100배 빠른 이유다.

2014년 Apache 최상위 프로젝트로 승격, 2016년 기준으로 GitHub에서 가장 활발한 빅데이터 프로젝트가 됐다. 현재 넷플릭스·우버·알리바바·어도비 등 수천 개 회사가 Spark를 핵심 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 엔진으로 사용한다.

📢 **섹션 요약 비유**: Spark는 메모리(RAM)가 큰 컴퓨터를 쓰는 것과 같다. 책([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 한 번 꺼내서 책상(메모리)에 펼쳐두고 반복적으로 참조하는 것이 MapReduce처럼 매번 서가에서 꺼냈다 넣는 것보다 훨씬 빠르다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Spark 아키텍처

```
  ┌──────────────────────────────────────────────────────────┐
  │                    Spark 애플리케이션                      │
  ├──────────────────────────────────────────────────────────┤
  │                                                           │
  │  ┌─────────────────┐                                     │
  │  │   Driver Program │  ← 사용자 코드 실행, Job 생성        │
  │  │   SparkContext   │  ← 클러스터 연결 및 실행 조율         │
  │  └────────┬─────────┘                                     │
  │           │ Task 분배                                     │
  │           ▼                                               │
  │  ┌─────────────────────────────────────────────────────┐ │
  │  │           Cluster Manager (YARN/K8s/Standalone)      │ │
  │  └────────────────────┬────────────────────────────────┘ │
  │                        │ Executor 할당                    │
  │     ┌──────────────────┼─────────────────┐               │
  │     ▼                  ▼                 ▼               │
  │  ┌───────────┐   ┌───────────┐   ┌───────────┐          │
  │  │ Executor 1│   │ Executor 2│   │ Executor 3│          │
  │  │ (노드1)   │   │ (노드2)   │   │ (노드3)   │          │
  │  │ [Task1]   │   │ [Task3]   │   │ [Task5]   │          │
  │  │ [Task2]   │   │ [Task4]   │   │ [Task6]   │          │
  │  │ [메모리 캐시] │ [메모리 캐시] │ [메모리 캐시] │        │
  │  └───────────┘   └───────────┘   └───────────┘          │
  └──────────────────────────────────────────────────────────┘
```

### Spark 통합 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)

| [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) | 용도 | 주요 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) |
|:---|:---|:---|
| **Spark Core** | 기반 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리, [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) 연산 | map, filter, reduce |
| **[Spark SQL](/knowledge-base/studynote/16_bigdata/03_spark/056_spark_sql/)** | 구조화 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) SQL 처리 | DataFrame, SparkSQL |
| **[Spark Streaming](/knowledge-base/studynote/16_bigdata/03_spark/060_spark_streaming_dstream/)** | 실시간 [스트림 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/) | [DStream](/knowledge-base/studynote/16_bigdata/03_spark/060_spark_streaming_dstream/) (구버전) |
| **[Structured Streaming](/knowledge-base/studynote/16_bigdata/03_spark/061_structured_streaming/)** | [스트림 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/) (DataFrame [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)) | readStream, writeStream |
| **MLlib** | [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | [Pipeline](/knowledge-base/studynote/12_it_management/02_itsm_itil/082_pipeline/), LinearRegression |
| **GraphX** | [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 | [Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/), Pregel |

### PySpark 예시 (단어 빈도)

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("WordCount") \
    .getOrCreate()

# 텍스트 파일 로드
text_df = spark.read.text("s3://mybucket/data/input.txt")

# DataFrame API로 단어 빈도 계산
from pyspark.sql.functions import explode, split, col

word_count = text_df \
    .select(explode(split(col("value"), " ")).alias("word")) \
    .groupBy("word") \
    .count() \
    .orderBy("count", ascending=False)

word_count.show(10)
word_count.write.csv("s3://mybucket/output/wordcount")
```

📢 **섹션 요약 비유**: Spark Driver는 건설 현장 감독이고, Executor는 실제 공사를 하는 인부다. 감독이 설계도([실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/))를 만들고 인부들에게 역할을 배분하면, 인부들이 자신의 구역([파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/))을 메모리에 올려두고 빠르게 처리한다.

---

## Ⅲ. 비교 및 연결

### Spark vs [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비교

| 시나리오 | [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) | Spark | 배율 |
|:---|:---:|:---:|:---:|
| 단순 [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/) | 기준 | 3~5배 빠름 | 3~5x |
| 반복적 ML 학습 | 기준 | 최대 100배 빠름 | 100x |
| 인터랙티브 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) | 수 분 | 수 초~수십 초 | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~30x |
| 실시간 스트리밍 | 불가 | 가능 (마이크로 배치) | ∞ |

### Spark 실행 모드

| 모드 | 설명 |
|:---|:---|
| Local | 단일 로컬 머신 (개발·테스트) |
| [Standalone](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/150_5g_sa_standalone_architecture/) | Spark 내장 클러스터 관리자 |
| [YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/) | [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/) 위에서 실행 |
| [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) | K8s 위에서 실행 (클라우드 표준) |
| AWS EMR | Amazon 관리형 Spark |
| [Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/) | 상용 최적화 Spark 플랫폼 |

📢 **섹션 요약 비유**: Spark의 실행 모드는 주차 방식과 같다. Local은 집 앞 주차(개발), YARN은 공용 주차장([하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 클러스터), K8s는 스마트 주차 타워([클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/)), EMR은 발렛파킹(완전 관리형)이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**Spark [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 튜닝 핵심**:
```python
spark = SparkSession.builder \
    .config("spark.executor.memory", "8g") \  # executor 메모리
    .config("spark.executor.cores", "4") \    # executor CPU 코어
    .config("spark.default.parallelism", "200") \  # 파티션 수
    .config("spark.sql.shuffle.partitions", "200") \  # 셔플 파티션
    .config("spark.memory.fraction", "0.8") \  # 메모리 중 실행에 사용할 비율
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .getOrCreate()

# 자주 사용되는 DataFrame은 cache()로 메모리에 유지
df = spark.read.parquet("s3://data/large_table/")
df.cache()  # 이후 여러 번 사용 시 재로딩 없이 메모리에서 처리
df.count()  # 이 시점에 실제 캐시 실행 (Lazy Evaluation)
```

**[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스큐(Skew) 문제 해결**:
```python
# Salting 기법: 키에 랜덤 접미사 추가하여 파티션 분산
from pyspark.sql.functions import concat, lit, rand, floor

df_skewed = df.withColumn(
    "salted_key",
    concat(col("key"), lit("_"), (floor(rand() * 10)).cast("string"))
)
```

**기술사 판단 포인트**:
- Spark의 `cache()` vs `persist()`: 기본 `cache()`는 메모리에만 저장, `persist(StorageLevel.MEMORY_AND_DISK)`는 메모리 초과 시 디스크를 사용해 유실 방지.
- [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수 = [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 단위. [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)이 너무 적으면 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화 부족, 너무 많으면 스케줄링 오버헤드. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 크기 / [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 크기(100~500MB) 공식으로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/).
- Databricks는 [Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/) + Photon(최적화 실행 엔진)으로 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) Spark보다 2~3배 빠른 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 제공한다.

📢 **섹션 요약 비유**: Spark의 cache()는 자주 보는 책을 서가에서 꺼내 책상 위에 항상 펼쳐두는 것과 같다. 처음 한 번만 들고 오면, 이후엔 손만 뻗으면 된다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 설명 |
|:---|:---|
| [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~100배 빠른 처리 | 메모리 기반 연산으로 [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 대비 극적 속도 향상 |
| 통합 플랫폼 | 배치·스트리밍·ML·SQL을 단일 API로 처리 |
| 풍부한 언어 지원 | Python·Scala·Java·R·SQL 모두 지원 |
| 클라우드 최적화 | AWS EMR·GCP Dataproc·[Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/) 완전 통합 |

Apache Spark는 현재 빅데이터 처리의 사실상 표준(De facto Standard)이다. 메모리 기반 처리, 통합 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), 광범위한 클라우드 지원으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어링·[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학의 핵심 도구가 됐다. Spark를 이해하면 현대 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 파이프라인의 80%를 이해한 것이다.

📢 **섹션 요약 비유**: Spark는 빅데이터 처리의 스마트폰이다. 전화(배치)·인터넷(SQL)·카메라(ML)를 하나의 기기로 처리하듯, 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리를 하나의 플랫폼에서 처리한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) | Spark의 핵심 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/), [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 불변 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋 |
| DataFrame / Dataset | RDD의 진화, [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 기반 최적화 |
| [지연 평가](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/) ([Lazy Evaluation](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/)) | Spark 최적화의 핵심 메커니즘 |
| [YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/) / [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) | Spark 실행을 위한 클러스터 관리 레이어 |
| [Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/) | 상용 최적화 Spark 플랫폼, [Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/) 창시자 |
| [Structured Streaming](/knowledge-base/studynote/16_bigdata/03_spark/061_structured_streaming/) | 실시간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리, [카프카](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 소스 통합 |

### 👶 어린이를 위한 3줄 비유 설명

1. Spark는 책([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 서가에서 꺼낼 때마다 원위치시키는 MapReduce와 달리, 자주 보는 책은 책상 위에 계속 펼쳐두어서(메모리 캐시) 훨씬 빠르게 찾을 수 있어.

### 📈 관련 키워드 및 발전 흐름도

```text
MapReduce: 단계마다 디스크 I/O (느림)
    │
    ▼
Spark: In-Memory 처리 (DAG 기반 실행 계획)
    ├─► Spark SQL · DataFrame: 구조화 데이터
    ├─► Spark Streaming: 마이크로배치 스트리밍
    └─► MLlib · GraphX: ML + 그래프 연산
    │
    ▼
Spark on K8s · Databricks Lakehouse
```
2. [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/)도, SQL [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)도, [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)도, 실시간 분석도 모두 Spark 하나로 할 수 있어. 스위스 군용 칼처럼 다기능이야.
3. 단, 책상이(메모리가) 작은데 너무 많은 책을 올리면 바닥에 쌓이게 되어(디스크 spill) 다시 느려지니까, 책상 크기에 맞게 조절해야 해.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 214 / 371

← **이전**: [214. YARN (Yet Another Resource Negotiator)](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/214_yarn_resource_manager_hadoop/)
**다음**: [216. RDD (Resilient Distributed Dataset)](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/216_rdd_resilient_distributed_dataset/) →

---
