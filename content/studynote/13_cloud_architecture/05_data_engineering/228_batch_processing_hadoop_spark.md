+++
title = "228. 배치 처리 (Batch Processing)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 배치 처리(Batch Processing)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 일정 기간·용량 단위로 모아 주기적으로 한 번에 처리하는 방식으로, <strong>처리 <a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a>을 수용하는 대신 <a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">처리량</a>(<a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">Throughput</a>)을 극대화</strong>한다.
> 2. **가치**: 야간 정산, 월말 리포트처럼 <strong>즉시성이 불필요하지만 대용량</strong>인 워크로드에 최적이며, 리소스를 예측 가능하게 [스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/)링하여 비용을 제어할 수 있다.
> 3. **판단 포인트**: 실시간성이 필요한 경우 [스트림 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/)로 전환하거나, <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/">Lambda</a>/<a href="/knowledge-base/studynote/16_bigdata/12_trends/235_kappa/">Kappa</a> 아키텍처</strong>로 배치와 스트리밍을 함께 운용하는 하이브리드 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 선택한다.

---

## Ⅰ. 개요 및 필요성

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 처리하는 방식은 크게 두 가지다. <strong>배치(Batch)</strong>는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 모아서 나중에 처리하고, <strong>스트리밍(Streaming)</strong>은 도착하는 즉시 처리한다. 배치 처리는 컴퓨터의 역사만큼 오래된 방식으로, 야간 은행 정산, 월급 지급, 인구 통계 집계 등 실시간이 불필요한 대용량 처리의 표준이다.

```
[배치 처리 개념]
시간 ──▶ 00:00   01:00   02:00   03:00   04:00
데이터   [누적]   [누적]   [누적]   [처리↗]  [완료]
                                   일괄 처리 (야간 배치)

특성:
- 대용량 처리에 최적 (높은 Throughput)
- 지연 시간(Latency) 수용 (T+1일, T+1시간)
- 리소스 예측 가능 (스케줄링 확정)
- 장애 복구 용이 (재처리 단순)
```

**배치 처리가 필요한 이유:**
- 은행 야간 이자 계산, 카드 정산 → 모든 거래 확정 후 일괄 처리
- 추천 모델 학습 → 전일 거래 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전체로 배치 학습
- [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) → 야간 [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 갱신

📢 **섹션 요약 비유**: 배치 처리는 빨래를 모아서 한 번에 세탁기에 돌리는 것이다. 한 벌씩 손빨래(실시간)하는 것보다 효율적이지만, 빨래가 다 모일 때까지 기다려야([지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)) 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [Apache Spark](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/) 배치 처리 아키텍처



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Apache Spark 배치 아키텍처</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Input Spark Core Output</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">S3/HDFS ──▶ ──▶ S3/DW</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">RDBMS ──▶</div><div class="kb-diagram-cell">Driver Program</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">CSV/JSON ──▶</div><div class="kb-diagram-cell">(DAG 계획)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">작업 분배</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Worker 1 Worker 2 Worker 3</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(Executor) (Executor) (Executor)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">파티션 1 파티션 2 파티션 3</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">병렬 처리 병렬 처리 병렬 처리</div></div>
</div>
</div>



### 배치 처리 최적화 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 설명 | 효과 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/">파티션</a> 분할</strong> | 날짜/카테고리별 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 기준 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분할 | 전체 스캔 방지 |
| **컬럼 지향 포맷** | [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)/ORC 사용 | 필요 열만 읽기, 압축률 ↑ |
| <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/">파티션</a> 푸시다운</strong> | WHERE 절 조건을 스토리지 레벨에서 필터링 | I/O 최소화 |
| <strong>브로드캐스트 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/">JOIN</a></strong> | 소형 테이블을 모든 Worker에 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) | 셔플 비용 제거 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/">캐싱</a></strong> | 반복 사용 중간 결과를 메모리 캐시 | 재계산 방지 |
| <strong><a href="/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a>도 조정</strong> | spark.sql.shuffle.partitions 튜닝 | 리소스 효율 |

### [Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) 아키텍처



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">Lambda 아키텍처: 배치 + 실시간 혼합</div></div>
<div class="kb-diagram-note">소스 데이터 ── ──▶ 배치 계층 (Spark/Hadoop) ──▶ 배치 뷰</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(T+1일 처리, 높은 정확도)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">서빙 계층</div></div>
<div class="kb-diagram-tree-item" style="--depth:7">▶ 스피드 계층 (Flink/Spark SS) ──▶ 실시간 뷰 ──▶ 최종 쿼리</div>
<div class="kb-diagram-note">(즉시 처리, 임시 결과) │ (쿼리 결합)</div>
<div class="kb-diagram-note">배치 뷰: 모든 과거 데이터 정확한 집계</div>
<div class="kb-diagram-note">실시간 뷰: 최근 수분 내 근사 집계</div>
</div>
</div>



📢 **섹션 요약 비유**: Spark의 [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/)(방향성 비순환 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/))는 공장 생산 공정도다. 어떤 작업이 어떤 순서로 실행되어야 하는지 설계도를 그린 뒤, 여러 공장(Worker)이 동시에 각자 담당 파트를 처리한다.

---

## Ⅲ. 비교 및 연결

### 배치 처리 vs [스트림 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/) 비교

| 비교 항목 | 배치 처리 | [스트림 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/) |
|:---|:---|:---|
| **처리 시점** | 주기적 (시간/일/월) | 이벤트 발생 즉시 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/">지연 시간</a></strong> | 높음 (분~시간) | 낮음 (밀리초~초) |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">처리량</a></strong> | 매우 높음 | 보통~높음 |
| **복잡도** | 낮음 | 높음 (상태관리, 윈도우) |
| **비용** | 낮음 ([스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/) 자원) | 높음 (상시 운영) |
| **재처리** | 용이 | 복잡 |
| **적합 사례** | 월말 정산, [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) | 실시간 이상감지, 알림 |
| **대표 기술** | Spark, [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) MR | Flink, [Spark Streaming](/knowledge-base/studynote/16_bigdata/03_spark/060_spark_streaming_dstream/) |

### 배치 프레임워크 비교

| 프레임워크 | 특징 | 적합 사례 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/">Apache Spark</a></strong> | 인메모리 처리, 범용 | 대용량 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/), ML 학습 |
| <strong><a href="/knowledge-base/studynote/07_enterprise_systems/06_exam_summary/395_hadoop_mapreduce_disk_bottleneck/">Hadoop MapReduce</a></strong> | 디스크 기반, 안정적 | 초대용량 배치, 레거시 |
| **AWS Glue** | [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) Spark, 관리형 | AWS 에코시스템 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) |
| **Google Dataflow** | Beam 기반, 배치+스트리밍 | GCP 통합 |
| **dbt** | SQL 배치 변환, [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 내부 | [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) Transform |

📢 **섹션 요약 비유**: 배치와 스트리밍 선택은 식당 운영 방식과 같다. 배치는 뷔페(일정 시간에 대량 준비), 스트리밍은 주문 즉시 조리하는 알라카르트다. 뷔페가 효율적이지만, 막 나온 음식을 원하는 손님에게는 알라카르트가 필요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 배치 처리 실무 설계 패턴

```python
# Spark 배치 처리 예시
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, date_format

spark = SparkSession.builder \
    .appName("DailyRevenueBatch") \
    .getOrCreate()

# 1. 파티션 기반 증분 읽기 (어제 날짜)
df_orders = spark.read.format("parquet") \
    .load("s3://bucket/bronze/orders/date=2024-01-15/")

# 2. 변환 및 집계
df_daily = df_orders \
    .filter(col("status") == "completed") \
    .groupBy("product_category", "region") \
    .agg(
        sum("amount").alias("total_revenue"),
        sum("quantity").alias("total_qty")
    )

# 3. Silver Zone 적재 (Parquet)
df_daily.write \
    .mode("overwrite") \
    .partitionBy("product_category") \
    .parquet("s3://bucket/silver/daily_revenue/date=2024-01-15/")
```

### 기술사 판단 기준

| 요건 | 배치 선택 | 스트림 선택 |
|:---|:---|:---|
| 분 단위 이하 실시간성 필요 | ❌ | ✅ |
| 대용량 역사적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 | ✅ | ❌ |
| 복잡한 집계·조인 | ✅ | 제한적 |
| 비용 예측 가능성 | ✅ | ❌ (상시 클러스터) |
| 장애 재처리 단순화 | ✅ | 어려움 |

📢 **섹션 요약 비유**: 배치 vs 스트리밍 결정은 우편 vs 택배 선택과 같다. 우편(배치)은 모아서 정기 배달하지만 저렴하고, 택배(스트리밍)는 즉시 배달하지만 비용이 높다. 긴급하지 않은 서류는 우편으로 충분하다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 내용 |
|:---|:---|
| <strong>높은 <a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">처리량</a></strong> | [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리로 테라바이트 규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 |
| **비용 예측** | [스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/) 기반 리소스 사용으로 비용 예측 가능 |
| **단순한 아키텍처** | 스트리밍 대비 상태 관리·윈도우 처리 불필요 |
| **재처리 용이** | [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 기반 특정 날짜 재실행 간단 |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/">지연 시간</a></strong> | T+1일 배치면 당일 실시간 분석 불가 |
| **쏠림 현상** | 배치 실행 시 클러스터 리소스 집중 소비 |
| **실패 재처리 비용** | 대용량 배치 실패 시 재처리에 오랜 시간 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 신선도</strong> | 배치 주기만큼 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 최신성 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) |

📢 **섹션 요약 비유**: 배치 처리는 야간에 도로를 공사하는 것과 같다. 차가 없을 때(유휴 시간) 대규모 공사(처리)를 하면 효율적이지만, 낮에 갑자기 도로를 바꿀 수 없다(실시간 한계). 응급 도로 보수(실시간 처리)는 스트리밍이 담당한다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| [스트림 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/) | 배치의 대조 개념, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)vs처리량 트레이드오프 |
| [Apache Spark](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/) | 배치 처리의 현대 표준 프레임워크 |
| [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)/[ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) | 배치 처리 기반의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통합 파이프라인 |
| [Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) 아키텍처 | 배치+스트리밍 혼합 설계 패턴 |
| [Kappa](/knowledge-base/studynote/16_bigdata/12_trends/235_kappa/) 아키텍처 | 스트리밍만으로 배치도 처리하는 단일화 설계 |
| [Apache Airflow](/knowledge-base/studynote/14_data_engineering/04_mlops/168_airflow_dag_pipeline_scheduling/) | 배치 파이프라인 [스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/)링·[오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) |
| [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)/ORC | 배치 처리 최적화 컬럼 지향 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 포맷 |

### 👶 어린이를 위한 3줄 비유 설명
1. 배치 처리는 하루 동안 받은 모든 편지를 저녁에 한꺼번에 읽고 답장하는 것이다. 한 통 받을 때마다 바로 답장하는 것(스트리밍)보다 시간이 좀 걸리지만, 한 번에 여러 통을 처리하니 훨씬 효율적이다.

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Batch Processing: 대량 데이터 일괄 처리</div>
<div class="kb-diagram-tree-item" style="--depth:2">MapReduce → Spark (In-Memory)</div>
<div class="kb-diagram-tree-item" style="--depth:2">스케줄링: Airflow · cron</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Stream Processing: 실시간 이벤트 처리 (Kafka · Flink)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Lambda / Kappa Architecture: 배치 + 스트림 통합</div>
</div>
</div>


2. 은행이 하루 이자를 계산할 때처럼, 모든 거래가 완전히 끝난 자정에 전체 계좌를 한꺼번에 계산하면 정확하고 빠르다.
3. Apache Spark는 큰 퍼즐을 여러 명이 동시에 맞추는 것처럼, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 작게 나눠서 많은 컴퓨터가 동시에 처리하므로 혼자 할 때보다 훨씬 빠르다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 227 / 371

← **이전**: [227. ELT (Extract, Load, Transform)](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/227_elt_extract_load_transform_cloud/)
**다음**: [229. 스트림 처리 (Stream Processing)](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/) →

---
