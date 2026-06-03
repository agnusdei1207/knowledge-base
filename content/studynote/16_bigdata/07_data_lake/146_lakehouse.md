+++
title = "146. 레이크하우스 (Lakehouse) — 데이터 레이크 + 웨어하우스 융합"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
1. 레이크하우스(Lakehouse)는 [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)의 **저비용·유연 저장**과 [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)의 **ACID [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)·[쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)**을 단일 아키텍처로 통합하여 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 비용을 제거한다.
2. [Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/) / [Apache Iceberg](/knowledge-base/studynote/16_bigdata/07_data_lake/148_apache_iceberg/) / [Apache Hudi](/knowledge-base/studynote/16_bigdata/07_data_lake/149_apache_hudi/) 같은 **[오픈 테이블 포맷](/knowledge-base/studynote/14_data_engineering/01_infrastructure/054_open_table_format_iceberg_delta_hudi/)**이 객체 스토리지 위에서 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 보장·타임 트래블을 실현하는 핵심 기술 레이어다.
3. ML [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인이 정제된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 직접 접근할 수 있어 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자의 실험 주기가 단축되고 거버넌스가 단일 지점으로 통합된다.

---

## Ⅰ. 개요 및 필요성

전통적 빅데이터 아키텍처에서는 [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)(원시 저장)와 [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)(분석·리포팅)가 분리된 2-계층 구조로 운영되었다. 이 구조는 이중 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 중복 스토리지 비용이라는 세 가지 만성적 문제를 내포했다.

Databricks가 2020년 논문에서 제시한 레이크하우스 패러다임은 이 두 계층을 하나로 합치는 것이다. 객체 스토리지(S3, Azure [Data Lake Storage](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/641_data_lake_storage/) Gen2, GCS)를 단일 진실의 원천([Single Source of Truth](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/))으로 삼고, 그 위에 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 레이어([트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/))를 추가함으로써 웨어하우스 수준의 보장을 달성한다.

| 구분 | [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) | [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) | 레이크하우스 |
|:---|:---|:---|:---|
| 저장 비용 | 매우 낮음 (객체 스토리지) | 높음 (전용 스토리지) | 매우 낮음 (객체 스토리지) |
| [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 방식 | [Schema-on-Read](/knowledge-base/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/) | [Schema-on-Write](/knowledge-base/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/) | 둘 다 지원 |
| ACID 보장 | 없음 | 있음 | 있음 (오픈 포맷) |
| ML 지원 | 직접 가능 | 제한적 | 직접 가능 |
| [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 제어 | 없음 | 있음 | 있음 |

> 📢 **섹션 요약 비유**: 기존엔 신선 재료 창고(레이크)와 완성 요리 냉장고([DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/))를 따로 관리했다. 레이크하우스는 스마트 냉장고 하나로 신선 재료 보관과 완성 요리 제공을 동시에 처리하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌─────────────────────────────────────────────────────────────────┐
│               레이크하우스 (Lakehouse) 아키텍처                  │
├──────────────────────────┬──────────────────────────────────────┤
│  소스 시스템              │  [DB CDC] [이벤트 스트림] [파일/API]  │
├──────────────────────────┴──────────────────────────────────────┤
│                객체 스토리지 (S3 / ADLS Gen2 / GCS)              │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │            오픈 테이블 포맷 (Delta / Iceberg / Hudi)       │  │
│   │  _delta_log/  ──▶  트랜잭션 로그 (ACID 보장)              │  │
│   │  Parquet 파일 ──▶  컬럼형 데이터 (쿼리 성능)              │  │
│   └──────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                   컴퓨팅 엔진 계층                               │
│  [Apache Spark] [Trino/Presto] [Flink] [Databricks SQL]         │
├──────────────────┬───────────────────┬──────────────────────────┤
│  BI / 리포팅     │  데이터 과학 / ML  │  실시간 스트리밍         │
│  (Power BI,     │  (MLflow, Jupyter) │  (Flink, Kafka)          │
│   Tableau)      │                   │                          │
└──────────────────┴───────────────────┴──────────────────────────┘
```

**핵심 구성 요소 비교**

| 기술 요소 | 역할 | 구현 예시 |
|:---|:---|:---|
| [오픈 테이블 포맷](/knowledge-base/studynote/14_data_engineering/01_infrastructure/054_open_table_format_iceberg_delta_hudi/) | ACID + [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) 관리 | [Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/), Iceberg, Hudi |
| 컬럼형 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 포맷 | 효율적 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)·[쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) | [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/), ORC |
| [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/)/거버넌스 | [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)·권한 관리 | [Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/), AWS Glue |
| 컴퓨팅 엔진 | SQL·배치·스트리밍 처리 | Spark, Trino, Flink |
| [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) | [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 [스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/) | Airflow, [Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/) Workflows |

> 📢 **섹션 요약 비유**: 건물(스토리지) 위에 엘리베이터 관제 시스템([트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/))을 설치하면, 여러 사람이 동시에 엘리베이터를 타도 충돌 없이 각자 원하는 층에 도달할 수 있다.

---

## Ⅲ. 비교 및 연결

**레이크하우스 vs 기존 2-티어 아키텍처**

| 항목 | 레이크 + [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) (2-티어) | 레이크하우스 (1-티어) |
|:---|:---|:---|
| [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 수 | 2개 (레이크→[DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)) | 1개 (소스→레이크하우스) |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 신선도 | 수 시간 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 근실시간 가능 |
| ML 접근 경로 | [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 혹은 레이크 별도 접근 | 단일 테이블 직접 접근 |
| 스토리지 비용 | [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) (레이크 + [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)) | 단일 객체 스토리지 |
| 운영 복잡도 | 높음 (두 시스템 관리) | 낮음 (단일 시스템) |

**연관 기술 연결**

- **[Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/)**: 레이크하우스의 대표 구현체 → `_delta_log` 기반 ACID
- **[Medallion Architecture](/knowledge-base/studynote/14_data_engineering/04_mlops/194_medallion_architecture_bronze_silver_gold/)**: 레이크하우스 내 Bronze → Silver → Gold 3계층
- **[Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/)**: 레이크하우스의 거버넌스·접근 제어 레이어
- **[MLflow](/knowledge-base/studynote/10_ai/02_dl_architecture_new/180_mlflow/)**: 레이크하우스 위 ML 실험 추적 및 [모델 레지스트리](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/)

> 📢 **섹션 요약 비유**: 예전엔 생산 공장(레이크)과 판매 창고([DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/))가 별개였는데, 레이크하우스는 [스마트 팩토리](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/166_smart_factory/)처럼 생산과 판매를 한 건물에서 동시에 처리한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**채택 판단 기준**

- **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 규모**: 테라바이트 이상, 다양한 형식의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 공존할 때 레이크하우스가 유리
- **ML 필요성**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학 팀이 [raw](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 직접 접근해야 한다면 레이크하우스 필수
- **비용 최적화**: 기존 DW의 라이선스 비용([Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/), Redshift)이 높을 때 이전 검토
- **실시간 요건**: 스트리밍과 배치를 동일 테이블에서 처리해야 할 때 [Structured Streaming](/knowledge-base/studynote/16_bigdata/03_spark/061_structured_streaming/) + Delta

**기술사 답안 포인트**

| 질문 유형 | 핵심 답변 키워드 |
|:---|:---|
| 레이크하우스 정의 | ACID on 객체 스토리지, [오픈 테이블 포맷](/knowledge-base/studynote/14_data_engineering/01_infrastructure/054_open_table_format_iceberg_delta_hudi/), [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 유연성 |
| 도입 효과 | [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 제거, 스토리지 비용 절감, ML 직접 접근 |
| 한계점 | 소규모 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 문제([Small File Problem](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/269_small_file_problem_data_lakehouse/)), [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 레이턴시([DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 대비) |
| 대안 비교 | vs [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/): SQL 친화성, vs [Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/): Spark 네이티브 |

> 📢 **섹션 요약 비유**: 레이크하우스 도입은 두 개의 전화 요금제(레이크·[DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/))를 하나의 무제한 요금제로 통합하는 것이다. 단, [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 강도([쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))가 기존 [전용선](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/266_leased_line_basics_e1_t1_t3/)보다 약할 수 있으므로 SLA를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 한다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 정량적 기대값 |
|:---|:---|
| 스토리지 비용 절감 | 기존 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 대비 40~80% (객체 스토리지 단가 차이) |
| [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 복잡도 | 2-티어 대비 50% 감소 |
| ML 실험 주기 단축 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 제거로 일 단위 → 시간 단위 |
| [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/) | 단일 [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/)로 전사 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 일원화 |

레이크하우스는 빅데이터 아키텍처의 차세대 표준으로 빠르게 수렴하고 있다. [Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/), [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/), AWS, Azure, GCP 모두 자사 플랫폼에 레이크하우스 기능을 내재화하고 있으며, Apache Iceberg의 멀티엔진 지원이 [벤더 종속](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/)성을 완화한다. 기술사 시험에서는 **오픈 포맷 기반 ACID 보장**, **Medallion 계층화**, **[ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 제거**가 핵심 논점이다.

> 📢 **섹션 요약 비유**: 레이크하우스는 도시의 통합 물류 [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)다. 원자재 창고와 소매점을 분리하던 구조를 하나의 스마트 물류 센터로 통합하여, 실시간 재고 파악과 즉각적인 배송을 동시에 실현한다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/) | 레이크하우스 구현체 | ACID on [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/), [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) |
| [Apache Iceberg](/knowledge-base/studynote/16_bigdata/07_data_lake/148_apache_iceberg/) | 대체 구현체 | 멀티엔진, 히든 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/) |
| [Medallion Architecture](/knowledge-base/studynote/14_data_engineering/04_mlops/194_medallion_architecture_bronze_silver_gold/) | 설계 패턴 | Bronze→Silver→Gold 계층화 |
| [Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/) | 거버넌스 레이어 | 컬럼/행 수준 접근 제어 |
| [MLflow](/knowledge-base/studynote/10_ai/02_dl_architecture_new/180_mlflow/) | ML 통합 | 레이크하우스 위 실험 추적 |
| [Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/) | 조직 원칙 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 소유권 + 레이크하우스 인프라 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[:---]
    │
    ▼
[Delta Lake]
    │
    ▼
[Apache Iceberg]
    │
    ▼
[Medallion Architecture]
    │
    ▼
[Unity Catalog]
    │
    ▼
[MLflow]
    │
    ▼
[Data Mesh]
```

이 흐름도는 :---에서 출발해 MLflow까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 레이크하우스는 모든 장난감을 보관하는 창고이자 동시에 친구들이 바로 와서 놀 수 있는 놀이방이에요.
2. 장난감을 꺼낼 때 실수로 다른 장난감이 망가지지 않도록 마법의 규칙(ACID)이 지켜줘요.
3. 한 방에 다 있으니 이쪽 방, 저쪽 방 왔다 갔다 할 필요가 없어서 훨씬 편하답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 146 / 262

← **이전**: [데이터 웨어하우스 (Data Warehouse)](/knowledge-base/studynote/16_bigdata/07_data_lake/145_data_warehouse/)
**다음**: [147. Delta Lake — ACID 트랜잭션 지원 오픈 테이블 포맷](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/) →

---
