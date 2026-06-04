---
title: "207. 데이터 레이크 (Data Lake) 스키마 온 리드 (Schema-on-Read)"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)([Data Lake](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/))는 구조화·반구조화·비구조화 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 원시([Raw](/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/)) 형태로 저장하고, <strong>읽을 때 <a href="/studynote/05_database/01_db_architecture_relational/005_schema/">스키마</a>를 적용(<a href="/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/">Schema-on-Read</a>)</strong>하는 중앙 저장소이다.
> 2. **가치**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집 시점에 구조를 확정하지 않아도 되므로 다양한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스를 유연하게 온보딩하고, 나중에 다양한 분석 목적에 맞게 재해석할 수 있다.
> 3. **판단 포인트**: 거버넌스와 [메타데이터 관리](/studynote/16_bigdata/10_governance/203_metadata_management/) 없이 구축하면 <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 스왐프(<a href="/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/">Data Swamp</a>)</strong>로 전락하며, 이를 방지하기 위한 [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)·품질 관리·접근 제어가 핵심 과제다.

---

## Ⅰ. 개요 및 필요성

### 전통적 [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)의 한계

기존 [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)([Data Warehouse](/studynote/14_data_engineering/05_exam_keywords/208_data_warehouse_schema_on_write_inmon/))는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 적재하기 전에 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)를 정의해야 하는 <strong><a href="/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/">스키마 온 라이트</a>(<a href="/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/">Schema-on-Write</a>)</strong> 방식을 채택한다. 이 방식은 [정형 데이터](/studynote/14_data_engineering/01_infrastructure/002_structured_data/)에는 강력하지만, [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 센서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 소셜 미디어 텍스트, 동영상 로그처럼 형태가 다양하고 급속히 변하는 빅데이터에는 적합하지 않다.

[데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 이 문제를 해결하기 위해 2010년 펜타호(Pentaho)의 제임스 딕슨(James Dixon)이 제안한 개념으로, 원시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 변환 없이 저장하고 분석 시 필요한 형태로 읽는 구조를 채택한다.

### [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) 정의

- **원시 저장소**: [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/), CSV, [Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/), ORC, 이미지, 동영상 등 모든 형식을 원본 그대로 보관
- <strong><a href="/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/">스키마 온 리드</a>(<a href="/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/">Schema-on-Read</a>)</strong>: 읽기 시점에 분석 목적에 맞는 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)를 덧씌움
- **저비용 스토리지**: Amazon S3, Azure [Data Lake Storage](/studynote/01_computer_architecture/15_advanced_topics/641_data_lake_storage/), [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/)([Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [Distributed File System](/studynote/02_operating_system/09_file_system/553_distributed_file_system/)) 기반
- **다목적 활용**: [배치 처리](/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/), [스트림 처리](/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/), ML(Machine [Learning](/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/)) 학습 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 탐색적 분석 동시 지원

📢 **섹션 요약 비유**: [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 <strong>모든 것을 원통에 담아두는 창고</strong>다. 입고 시 물건을 분류하지 않고 일단 쌓아두고, 필요할 때 필요한 기준으로 꺼내 정리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) 계층 구조

```
+---------------------------------------------------------+
|                   데이터 레이크 아키텍처                  |
+---------------------------------------------------------+
|  +---------+  +---------+  +---------+  +----------+  |
|  | 정형    |  | 반구조화 |  |비구조화 |  |스트리밍  |  |
|  | CSV/DB  |  |JSON/XML |  |이미지/  |  | 이벤트   |  |
|  |         |  |         |  |동영상   |  | 로그     |  |
|  +----+----+  +----+----+  +----+----+  +----+-----+  |
|       |            |             |              |        |
|       +------------+-------------+--------------+        |
|                            |                             |
|                   +--------v--------+                   |
|                   |   수집 계층      |                   |
|                   | (Ingest Layer)  |                   |
|                   +--------+--------+                   |
|                            |                             |
|  +-------------------------v-------------------------+  |
|  |              저장 계층 (Storage Layer)             |  |
|  |   Raw Zone  |  Curated Zone  |  Consumption Zone  |  |
|  | (원본 보존)  | (클렌징·변환)   |  (분석 서빙)       |  |
|  +-------------------------+-------------------------+  |
|                            |                             |
|  +-------------------------v-------------------------+  |
|  |              처리 계층 (Processing Layer)          |  |
|  |   Spark  |  Hive  |  Presto  |  Flink  |  Athena  |  |
|  +-------------------------+-------------------------+  |
|                            |                             |
|  +-------------------------v-------------------------+  |
|  |           분석/소비 계층 (Analytics Layer)         |  |
|  |  BI 도구  |  ML 파이프라인  |  Ad-hoc 쿼리         |  |
|  +---------------------------------------------------+  |
+---------------------------------------------------------+
```

### [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) 핵심 특성 비교

| 항목 | [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) | [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) |
|:---|:---|:---|
| <strong><a href="/studynote/05_database/01_db_architecture_relational/005_schema/">스키마</a> 적용 시점</strong> | 읽기 시([Schema-on-Read](/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/)) | [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 시([Schema-on-Write](/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/)) |
| <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 형식</strong> | 모든 형식(정형+비정형) | 주로 [정형 데이터](/studynote/14_data_engineering/01_infrastructure/002_structured_data/) |
| **저장 비용** | 저렴([오브젝트 스토리지](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)) | 고가(컬럼 스토어) |
| **처리 유연성** | 매우 높음 | 제한적 |
| <strong><a href="/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong> | 처리 의존적 | 빠름(최적화됨) |
| <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 품질</strong> | 낮을 수 있음 | 높음([ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 보장) |
| **주요 사용자** | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자 | 비즈니스 분석가 |
| **도구 예시** | S3+Spark, ADLS+[Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) | [Snowflake](/studynote/05_database/04_transactions_concurrency/541_cassandra/), [BigQuery](/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/), Redshift |

📢 **섹션 요약 비유**: [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 <strong>도서관의 자유 열람실</strong>이고, [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)는 <strong>분류가 완벽히 된 특수 서고</strong>다. 자유 열람실은 뭐든 있지만 찾기 어렵고, 특수 서고는 찾기 쉽지만 특정 책만 있다.

---

## Ⅲ. 비교 및 연결

### [Schema-on-Read](/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/) vs [Schema-on-Write](/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/)

<strong><a href="/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/">Schema-on-Write</a> (<a href="/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/">스키마 온 라이트</a>)</strong>
- [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)에서 채택
- 적재 전 [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)(Extract, Transform, Load) 과정에서 변환 완료
- [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 보장, [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [성능 우수](/studynote/05_database/07_exam_summary/484_elt_extract_load_transform/)
- [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 변경 시 [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 파이프라인 전면 수정 필요

<strong><a href="/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/">Schema-on-Read</a> (<a href="/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/">스키마 온 리드</a>)</strong>
- [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)에서 채택
- 원시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 -> 읽기 시 Spark/Hive에서 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 정의
- 유연성 극대화, [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 진화([Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) Evolution) 지원
- [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 시 변환 비용 발생, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 관리 어려움

### [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스왐프([Data Swamp](/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/)) 방지

| 위험 요소 | 방지 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
|:---|:---|
| [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 부재 | [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)(Apache Atlas, AWS Glue) 도입 |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 저하 | [데이터 프로파일링](/studynote/07_enterprise_systems/05_data_bi/267_data_profiling/)·[검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 파이프라인 |
| 중복 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과다 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보([Data Lineage](/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/)) 추적 |
| [접근 통제](/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/) 부재 | [RBAC](/studynote/09_security/11_iam_access_control/569_rbac/)([Role-Based Access Control](/studynote/09_security/11_iam_access_control/569_rbac/)) 구현 |
| 수명 주기 관리 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 티어링(Hot->Warm->Cold) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) |

📢 **섹션 요약 비유**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스왐프는 <strong>색인 없는 창고</strong>다. 물건을 많이 쌓을수록 찾기가 더 어려워진다. [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)와 거버넌스는 창고의 라벨링 시스템이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 클라우드 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) 구현 패턴

**AWS 패턴**: S3 -> Glue Crawler([메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 자동 추출) -> Athena([서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)) -> QuickSight([시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/))

**Azure 패턴**: ADLS Gen2 -> Azure Purview(거버넌스) -> Synapse Analytics(통합 분석) -> [Power BI](/studynote/16_bigdata/08_visualization/165_power_bi/)

**구글 패턴**: Cloud Storage -> Dataflow(스트리밍 처리) -> [BigQuery](/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/)([서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) [DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)) -> [Looker](/studynote/16_bigdata/08_visualization/166_looker/)

### [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) 존(Zone) 설계

```
Raw Zone        -> Curated Zone   -> Consumption Zone
(원본 보존)       (표준화·클렌징)   (목적별 뷰)
변경 불가         품질 검증 완료    BI·ML 최적화
```

### 기술사 판단 포인트

1. <strong><a href="/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/">데이터 레이크</a> vs <a href="/studynote/16_bigdata/07_data_lake/146_lakehouse/">레이크하우스</a></strong>: [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 지원 부재 -> [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/)/Iceberg로 보완
2. **거버넌스 프레임워크**: DAMA-DMBOK 기준 [데이터 스튜어드십](/studynote/12_it_management/05_security_compliance/273_data_stewardship/)([Data Stewardship](/studynote/12_it_management/05_security_compliance/273_data_stewardship/)) 역할 정의
3. **비용 최적화**: 지능형 스토리지 계층화(Intelligent Tiering)로 [콜드 데이터](/studynote/01_computer_architecture/15_advanced_topics/676_cold_data_archiving/) 비용 절감

📢 **섹션 요약 비유**: [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) 구축은 <strong>신도시 개발</strong>과 같다. 도로(수집 파이프라인), 창고(저장소), 도시 법규(거버넌스)를 함께 설계해야 살기 좋은 도시가 된다.

---

## Ⅴ. 기대효과 및 결론

### 도입 기대효과

| 효과 | 정량적 목표 |
|:---|:---|
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 온보딩 속도 향상 | 신규 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스 통합 시간 75% 단축 |
| 스토리지 비용 절감 | 기존 [DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 대비 60~80% 절감 |
| ML 학습 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [접근성](/studynote/04_software_engineering/05_devops_ci_cd/292_accessibility_kwcag_wcag/) | 모델 훈련 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 준비 시간 50% 단축 |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 재사용률 증가 | 단일 원본 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 다목적 재활용 |

### 결론

[데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 빅데이터 시대의 <strong>중앙 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 저장소</strong>로서 유연성과 확장성에서 탁월하다. 그러나 "일단 저장하고 나중에 생각하자"는 접근은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스왐프로 이어진다. 성공적인 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 기술적 구현과 함께 <strong><a href="/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/">데이터 거버넌스</a>, <a href="/studynote/16_bigdata/10_governance/203_metadata_management/">메타데이터 관리</a>, <a href="/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/">접근 통제</a></strong>를 처음부터 내재화해야 한다. 현대에는 [레이크하우스](/studynote/16_bigdata/07_data_lake/146_lakehouse/)([Lakehouse](/studynote/16_bigdata/07_data_lake/146_lakehouse/)) 패턴으로 진화하여 웨어하우스의 신뢰성과 레이크의 유연성을 결합하는 방향으로 발전 중이다.

📢 **섹션 요약 비유**: [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)의 진화는 <strong>야영지 -> 마을 -> 도시</strong>와 같다. 처음엔 자유롭게 텐트를 치지만, 결국 도시 계획(거버넌스)이 필요해진다.

---

### 📌 관련 개념 맵

| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 진화형 | [데이터 레이크하우스](/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/) | 레이크+[DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 결합 |
| 구성 요소 | [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) | [메타데이터 관리 시스템](/studynote/05_database/02_modeling_normalization/125_metadata_management_system_mms/) |
| 대안 비교 | [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) | [Schema-on-Write](/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/), 고성능 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) |
| 위험 요소 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스왐프 | 거버넌스 부재 시 발생 |
| 기반 기술 | [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/)/S3/ADLS | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [오브젝트 스토리지](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/) |
| 처리 엔진 | [Apache Spark](/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/) | 레이크 상 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 처리 |
| 거버넌스 도구 | Apache Atlas | [데이터 리니지](/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/)·[카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) |

### 👶 어린이를 위한 3줄 비유 설명

1. [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 <strong>모든 종류의 장난감을 한 방에 다 넣어두는 큰 방</strong>이야. 레고도 있고, 인형도 있고, 공도 있어.

### 📈 관련 키워드 및 발전 흐름도

```text
파일 서버 · RDBMS (구조화 데이터만)
    |
    v
Data Lake: Schema-on-Read · 원시 데이터 저장 (S3 · HDFS)
    | 데이터 늪 (Data Swamp) 위험
    v
Data Lakehouse: Lake + Warehouse 통합 (Delta · Iceberg)
    |
    v
Data Mesh: 도메인별 분산 소유권 + 자기 서빙 인프라
```
2. 놀고 싶을 때 방에 들어가서 "오늘은 레고만 꺼낼래"하고 그때 골라 쓰는 거야. 미리 정리 안 해도 돼.
3. 방이 너무 커지면 어디 있는지 모르게 되니까 <strong>지도(<a href="/studynote/05_database/07_exam_summary/394_catalog_metadata/">카탈로그</a>)</strong>를 만들어야 찾을 수 있어.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 207 / 258

<- **이전**: [206. 아파치 스파크 (Apache Spark) 인메모리 RDD 지연 평가 계보](/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/)
**다음**: [208. 데이터 웨어하우스 (Data Warehouse) 스키마 온 라이트 Inmon 설계](/studynote/14_data_engineering/05_exam_keywords/208_data_warehouse_schema_on_write_inmon/) ->

---
