+++
weight = 207
title = "207. 데이터 레이크 (Data Lake) 스키마 온 리드 (Schema-on-Read)"
date = "2026-04-21"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[208_data_lake_schema_on_read|데이터 레이크]]([[208_data_lake_schema_on_read|Data Lake]])는 구조화·반구조화·비구조화 [[001_dikw_pyramid|데이터]]를 원시([[225_raw|Raw]]) 형태로 저장하고, **읽을 때 [[005_schema|스키마]]를 적용([[009_schema_on_read|Schema-on-Read]])**하는 중앙 저장소이다.
> 2. **가치**: [[001_dikw_pyramid|데이터]] 수집 시점에 구조를 확정하지 않아도 되므로 다양한 [[001_dikw_pyramid|데이터]] 소스를 유연하게 온보딩하고, 나중에 다양한 분석 목적에 맞게 재해석할 수 있다.
> 3. **판단 포인트**: 거버넌스와 [[203_metadata_management|메타데이터 관리]] 없이 구축하면 **[[001_dikw_pyramid|데이터]] 스왐프([[288_data_swamp_metadata_management_absence|Data Swamp]])**로 전락하며, 이를 방지하기 위한 [[213_data_catalog_metadata|데이터 카탈로그]]·품질 관리·접근 제어가 핵심 과제다.

---

## Ⅰ. 개요 및 필요성

### 전통적 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]의 한계

기존 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]([[208_data_warehouse_schema_on_write_inmon|Data Warehouse]])는 [[001_dikw_pyramid|데이터]]를 적재하기 전에 [[005_schema|스키마]]를 정의해야 하는 **[[010_schema_on_write|스키마 온 라이트]]([[010_schema_on_write|Schema-on-Write]])** 방식을 채택한다. 이 방식은 [[002_structured_data|정형 데이터]]에는 강력하지만, [[101_iot_concept|IoT]] 센서 [[001_dikw_pyramid|데이터]], 소셜 미디어 텍스트, 동영상 로그처럼 형태가 다양하고 급속히 변하는 빅데이터에는 적합하지 않다.

[[208_data_lake_schema_on_read|데이터 레이크]]는 이 문제를 해결하기 위해 2010년 펜타호(Pentaho)의 제임스 딕슨(James Dixon)이 제안한 개념으로, 원시 [[001_dikw_pyramid|데이터]]를 변환 없이 저장하고 분석 시 필요한 형태로 읽는 구조를 채택한다.

### [[208_data_lake_schema_on_read|데이터 레이크]] 정의

- **원시 저장소**: [[343_json|JSON]], CSV, [[178_parquet_rle_encoding_columnar_compression|Parquet]], ORC, 이미지, 동영상 등 모든 형식을 원본 그대로 보관
- **[[009_schema_on_read|스키마 온 리드]]([[009_schema_on_read|Schema-on-Read]])**: 읽기 시점에 분석 목적에 맞는 [[005_schema|스키마]]를 덧씌움
- **저비용 스토리지**: Amazon S3, Azure [[641_data_lake_storage|Data Lake Storage]], [[013_hdfs|HDFS]]([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] [[553_distributed_file_system|Distributed File System]]) 기반
- **다목적 활용**: [[228_batch_processing_hadoop_spark|배치 처리]], [[229_stream_processing_kafka_flink|스트림 처리]], ML(Machine [[240_switch_learning_forwarding_flooding|Learning]]) 학습 [[001_dikw_pyramid|데이터]], 탐색적 분석 동시 지원

📢 **섹션 요약 비유**: [[208_data_lake_schema_on_read|데이터 레이크]]는 **모든 것을 원통에 담아두는 창고**다. 입고 시 물건을 분류하지 않고 일단 쌓아두고, 필요할 때 필요한 기준으로 꺼내 정리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[208_data_lake_schema_on_read|데이터 레이크]] 계층 구조

```
┌─────────────────────────────────────────────────────────┐
│                   데이터 레이크 아키텍처                  │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌──────────┐  │
│  │ 정형    │  │ 반구조화 │  │비구조화 │  │스트리밍  │  │
│  │ CSV/DB  │  │JSON/XML │  │이미지/  │  │ 이벤트   │  │
│  │         │  │         │  │동영상   │  │ 로그     │  │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬─────┘  │
│       │            │             │              │        │
│       └────────────┴─────────────┴──────────────┘        │
│                            │                             │
│                   ┌────────▼────────┐                   │
│                   │   수집 계층      │                   │
│                   │ (Ingest Layer)  │                   │
│                   └────────┬────────┘                   │
│                            │                             │
│  ┌─────────────────────────▼─────────────────────────┐  │
│  │              저장 계층 (Storage Layer)             │  │
│  │   Raw Zone  │  Curated Zone  │  Consumption Zone  │  │
│  │ (원본 보존)  │ (클렌징·변환)   │  (분석 서빙)       │  │
│  └─────────────────────────┬─────────────────────────┘  │
│                            │                             │
│  ┌─────────────────────────▼─────────────────────────┐  │
│  │              처리 계층 (Processing Layer)          │  │
│  │   Spark  │  Hive  │  Presto  │  Flink  │  Athena  │  │
│  └─────────────────────────┬─────────────────────────┘  │
│                            │                             │
│  ┌─────────────────────────▼─────────────────────────┐  │
│  │           분석/소비 계층 (Analytics Layer)         │  │
│  │  BI 도구  │  ML 파이프라인  │  Ad-hoc 쿼리         │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### [[208_data_lake_schema_on_read|데이터 레이크]] 핵심 특성 비교

| 항목 | [[208_data_lake_schema_on_read|데이터 레이크]] | [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] |
|:---|:---|:---|
| **[[005_schema|스키마]] 적용 시점** | 읽기 시([[009_schema_on_read|Schema-on-Read]]) | [[289_cqrs_db|쓰기]] 시([[010_schema_on_write|Schema-on-Write]]) |
| **[[001_dikw_pyramid|데이터]] 형식** | 모든 형식(정형+비정형) | 주로 [[002_structured_data|정형 데이터]] |
| **저장 비용** | 저렴([[494_object_storage|오브젝트 스토리지]]) | 고가(컬럼 스토어) |
| **처리 유연성** | 매우 높음 | 제한적 |
| **[[298_qkv_attention|쿼리]] [[282_performance_tactics|성능]]** | 처리 의존적 | 빠름(최적화됨) |
| **[[001_dikw_pyramid|데이터]] 품질** | 낮을 수 있음 | 높음([[215_etl_vs_elt_pipeline|ETL]] 보장) |
| **주요 사용자** | [[001_dikw_pyramid|데이터]] 과학자 | 비즈니스 분석가 |
| **도구 예시** | S3+Spark, ADLS+[[074_photon_engine|Databricks]] | [[541_cassandra|Snowflake]], [[263_storage_compute_separation_bigquery|BigQuery]], Redshift |

📢 **섹션 요약 비유**: [[208_data_lake_schema_on_read|데이터 레이크]]는 **도서관의 자유 열람실**이고, [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]는 **분류가 완벽히 된 특수 서고**다. 자유 열람실은 뭐든 있지만 찾기 어렵고, 특수 서고는 찾기 쉽지만 특정 책만 있다.

---

## Ⅲ. 비교 및 연결

### [[009_schema_on_read|Schema-on-Read]] vs [[010_schema_on_write|Schema-on-Write]]

**[[010_schema_on_write|Schema-on-Write]] ([[010_schema_on_write|스키마 온 라이트]])**
- [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]에서 채택
- 적재 전 [[215_etl_vs_elt_pipeline|ETL]](Extract, Transform, Load) 과정에서 변환 완료
- [[001_dikw_pyramid|데이터]] 품질 보장, [[298_qkv_attention|쿼리]] [[484_elt_extract_load_transform|성능 우수]]
- [[005_schema|스키마]] 변경 시 [[215_etl_vs_elt_pipeline|ETL]] 파이프라인 전면 수정 필요

**[[009_schema_on_read|Schema-on-Read]] ([[009_schema_on_read|스키마 온 리드]])**
- [[208_data_lake_schema_on_read|데이터 레이크]]에서 채택
- 원시 [[001_dikw_pyramid|데이터]] 저장 → 읽기 시 Spark/Hive에서 [[005_schema|스키마]] 정의
- 유연성 극대화, [[005_schema|스키마]] 진화([[505_schema|Schema]] Evolution) 지원
- [[298_qkv_attention|쿼리]] 시 변환 비용 발생, [[001_dikw_pyramid|데이터]] 품질 관리 어려움

### [[001_dikw_pyramid|데이터]] 스왐프([[288_data_swamp_metadata_management_absence|Data Swamp]]) 방지

| 위험 요소 | 방지 [[268_strategy_pattern|전략]] |
|:---|:---|
| [[012_metadata|메타데이터]] 부재 | [[213_data_catalog_metadata|데이터 카탈로그]](Apache Atlas, AWS Glue) 도입 |
| [[001_dikw_pyramid|데이터]] 품질 저하 | [[267_data_profiling|데이터 프로파일링]]·[[395_verification_process_review|검증]] 파이프라인 |
| 중복 [[001_dikw_pyramid|데이터]] 과다 | [[001_dikw_pyramid|데이터]] 계보([[214_data_lineage_tracking|Data Lineage]]) 추적 |
| [[387_access_control_pattern|접근 통제]] 부재 | [[569_rbac|RBAC]]([[569_rbac|Role-Based Access Control]]) 구현 |
| 수명 주기 관리 | [[001_dikw_pyramid|데이터]] 티어링(Hot→Warm→Cold) [[164_policy|정책]] |

📢 **섹션 요약 비유**: [[001_dikw_pyramid|데이터]] 스왐프는 **색인 없는 창고**다. 물건을 많이 쌓을수록 찾기가 더 어려워진다. [[394_catalog_metadata|카탈로그]]와 거버넌스는 창고의 라벨링 시스템이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 클라우드 [[208_data_lake_schema_on_read|데이터 레이크]] 구현 패턴

**AWS 패턴**: S3 → Glue Crawler([[012_metadata|메타데이터]] 자동 추출) → Athena([[206_serverless_cold_start|서버리스]] [[298_qkv_attention|쿼리]]) → QuickSight([[003_bigdata_7v|시각화]])

**Azure 패턴**: ADLS Gen2 → Azure Purview(거버넌스) → Synapse Analytics(통합 분석) → [[165_power_bi|Power BI]]

**구글 패턴**: Cloud Storage → Dataflow(스트리밍 처리) → [[263_storage_compute_separation_bigquery|BigQuery]]([[206_serverless_cold_start|서버리스]] [[209_data_warehouse_schema_on_write|DW]]) → [[166_looker|Looker]]

### [[208_data_lake_schema_on_read|데이터 레이크]] 존(Zone) 설계

```
Raw Zone        → Curated Zone   → Consumption Zone
(원본 보존)       (표준화·클렌징)   (목적별 뷰)
변경 불가         품질 검증 완료    BI·ML 최적화
```

### 기술사 판단 포인트

1. **[[208_data_lake_schema_on_read|데이터 레이크]] vs [[146_lakehouse|레이크하우스]]**: [[191_transaction_concept_states|트랜잭션]] 지원 부재 → [[147_delta_lake|Delta Lake]]/Iceberg로 보완
2. **거버넌스 프레임워크**: DAMA-DMBOK 기준 [[273_data_stewardship|데이터 스튜어드십]]([[273_data_stewardship|Data Stewardship]]) 역할 정의
3. **비용 최적화**: 지능형 스토리지 계층화(Intelligent Tiering)로 [[676_cold_data_archiving|콜드 데이터]] 비용 절감

📢 **섹션 요약 비유**: [[208_data_lake_schema_on_read|데이터 레이크]] 구축은 **신도시 개발**과 같다. 도로(수집 파이프라인), 창고(저장소), 도시 법규(거버넌스)를 함께 설계해야 살기 좋은 도시가 된다.

---

## Ⅴ. 기대효과 및 결론

### 도입 기대효과

| 효과 | 정량적 목표 |
|:---|:---|
| [[001_dikw_pyramid|데이터]] 온보딩 속도 향상 | 신규 [[001_dikw_pyramid|데이터]] 소스 통합 시간 75% 단축 |
| 스토리지 비용 절감 | 기존 [[209_data_warehouse_schema_on_write|DW]] 대비 60~80% 절감 |
| ML 학습 [[001_dikw_pyramid|데이터]] [[292_accessibility_kwcag_wcag|접근성]] | 모델 훈련 [[001_dikw_pyramid|데이터]] 준비 시간 50% 단축 |
| [[001_dikw_pyramid|데이터]] 재사용률 증가 | 단일 원본 [[001_dikw_pyramid|데이터]]의 다목적 재활용 |

### 결론

[[208_data_lake_schema_on_read|데이터 레이크]]는 빅데이터 시대의 **중앙 [[001_dikw_pyramid|데이터]] 저장소**로서 유연성과 확장성에서 탁월하다. 그러나 "일단 저장하고 나중에 생각하자"는 접근은 [[001_dikw_pyramid|데이터]] 스왐프로 이어진다. 성공적인 [[208_data_lake_schema_on_read|데이터 레이크]]는 기술적 구현과 함께 **[[052_data_governance_framework|데이터 거버넌스]], [[203_metadata_management|메타데이터 관리]], [[387_access_control_pattern|접근 통제]]**를 처음부터 내재화해야 한다. 현대에는 [[146_lakehouse|레이크하우스]]([[146_lakehouse|Lakehouse]]) 패턴으로 진화하여 웨어하우스의 신뢰성과 레이크의 유연성을 결합하는 방향으로 발전 중이다.

📢 **섹션 요약 비유**: [[208_data_lake_schema_on_read|데이터 레이크]]의 진화는 **야영지 → 마을 → 도시**와 같다. 처음엔 자유롭게 텐트를 치지만, 결국 도시 계획(거버넌스)이 필요해진다.

---

### 📌 관련 개념 맵

| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 진화형 | [[210_data_lakehouse_delta_lake|데이터 레이크하우스]] | 레이크+[[209_data_warehouse_schema_on_write|DW]] [[191_transaction_concept_states|트랜잭션]] 결합 |
| 구성 요소 | [[213_data_catalog_metadata|데이터 카탈로그]] | [[125_metadata_management_system_mms|메타데이터 관리 시스템]] |
| 대안 비교 | [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] | [[010_schema_on_write|Schema-on-Write]], 고성능 [[298_qkv_attention|쿼리]] |
| 위험 요소 | [[001_dikw_pyramid|데이터]] 스왐프 | 거버넌스 부재 시 발생 |
| 기반 기술 | [[013_hdfs|HDFS]]/S3/ADLS | [[136_variance|분산]] [[494_object_storage|오브젝트 스토리지]] |
| 처리 엔진 | [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] | 레이크 상 [[136_variance|분산]] 처리 |
| 거버넌스 도구 | Apache Atlas | [[214_data_lineage_tracking|데이터 리니지]]·[[394_catalog_metadata|카탈로그]] |

### 👶 어린이를 위한 3줄 비유 설명

1. [[208_data_lake_schema_on_read|데이터 레이크]]는 **모든 종류의 장난감을 한 방에 다 넣어두는 큰 방**이야. 레고도 있고, 인형도 있고, 공도 있어.

### 📈 관련 키워드 및 발전 흐름도

```text
파일 서버 · RDBMS (구조화 데이터만)
    │
    ▼
Data Lake: Schema-on-Read · 원시 데이터 저장 (S3 · HDFS)
    │ 데이터 늪 (Data Swamp) 위험
    ▼
Data Lakehouse: Lake + Warehouse 통합 (Delta · Iceberg)
    │
    ▼
Data Mesh: 도메인별 분산 소유권 + 자기 서빙 인프라
```
2. 놀고 싶을 때 방에 들어가서 "오늘은 레고만 꺼낼래"하고 그때 골라 쓰는 거야. 미리 정리 안 해도 돼.
3. 방이 너무 커지면 어디 있는지 모르게 되니까 **지도([[394_catalog_metadata|카탈로그]])**를 만들어야 찾을 수 있어.
