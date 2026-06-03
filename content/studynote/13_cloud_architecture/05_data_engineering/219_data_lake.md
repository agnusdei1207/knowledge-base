+++
title = "219. 데이터 레이크 (Data Lake) - 원시 데이터 중심의 전사적 통합 저장소"
date = 2026-03-04

[taxonomies]
tags = ["cloud_architecture"]

[extra]
tags = ["cloud_architecture"]
+++

## 핵심 인사이트 (3줄 요약)
- <strong>무제한 원시 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 저장:</strong> 정형(DB), 반정형([JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/), Log), 비정형(이미지, 영상) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 가공 없이 원본 그대로 대량 저장할 수 있는 중앙 저장소이다.
- <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/">스키마 온 리드</a> (<a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/">Schema-on-Read</a>):</strong> [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 저장할 때 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)를 정의하지 않고, 나중에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽어서 분석할 때 필요에 따라 구조를 입히는 유연한 방식이다.
- **클라우드 스토리지 기반:** 저렴한 클라우드 [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)(AWS S3 등)를 활용하여 비용 효율적인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 거버넌스를 구축할 수 있다.

### Ⅰ. 개요 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
[데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)([Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/))는 기업의 흩어진 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 한곳에 모으는 거대한 저수지 역할을 한다. 기존의 [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)([DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/))가 정제된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만을 담는 '생수통'이라면, [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 흙탕물([Raw](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))까지도 모두 받아두었다가 필요할 때 정수해서 사용하는 철학을 가지고 있다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
[데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 수집(Ingest), 저장(Store), 처리([Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/)), 분석(Analyze)의 다계층 구조로 이루어진다.

```text
[ Architecture of Data Lake & Pipeline ]

   [ Data Sources ]       [ Data Lake Layers ]       [ Consumption ]
   +--------------+      +----------------------+      +--------------+
   | RDBMS (SQL)  |----->| Raw Layer (Landing)  |----->| Data Science |
   +--------------+      +----------------------+      +--------------+
   | Logs (JSON)  |----->| Standardized Layer   |----->| ML Modeling  |
   +--------------+      +----------------------+      +--------------+
   | Files (CSV)  |----->| Curated Layer (Gold) |----->| BI Dashboard |
   +--------------+      +----------------------+      +--------------+

* Storage: Object Storage (AWS S3, Azure Data Lake Storage)
* Metadata: Glue Catalog, Hive Metastore
* Processing: Spark, Presto, Athena
```

**핵심 메커니즘:**
1. <strong><a href="/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/">Raw</a> Layer:</strong> 원본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 변조 없이 적재되는 구간 ([감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 로그용)
2. **Standardized Layer:** [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 형식을 [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)/Avro 등으로 통일하고 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)를 태깅한 구간
3. **Curated Layer:** 분석 목적에 맞게 조인/집계된 최종 정제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구간
4. **Decoupling:** 저장(Storage)과 연산(Compute)을 분리하여 자원을 독립적으로 확장한다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) ([Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)) | [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) ([Data Warehouse](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/208_data_warehouse_schema_on_write_inmon/)) |
| :--- | :--- | :--- |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 형태</strong> | 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) (정형/반정형/비정형) | 정제된 [정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/002_structured_data/) 위주 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/">스키마</a> 적용</strong> | 읽을 때 적용 ([Schema-on-Read](/knowledge-base/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/)) | 저장할 때 적용 ([Schema-on-Write](/knowledge-base/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/)) |
| **비용/확장성** | 낮음 / 무제한 확장 가능 | 높음 / 확장에 따른 비용 부담 큼 |
| **사용자** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 사이언티스트, ML 엔지니어 | 비즈니스 분석가, 현업 관리자 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
**실무 적용 사례:**
- <strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/">IoT</a> 센서 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 분석:</strong> 수만 개의 센서에서 쏟아지는 원시 로그를 S3에 일단 모두 담아두고, 필요한 지표만 스파크(Spark)로 분석한다.
- <strong>이미지/영상 <a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> 학습:</strong> 대량의 멀티미디어 파일을 [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)에 보관하며 딥러닝 모델의 학습 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋으로 공급한다.

**기술사적 판단:**
"[데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 자칫 관리 소홀로 인해 <strong><a href="/knowledge-base/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/">데이터 늪</a>(<a href="/knowledge-base/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/">Data Swamp</a>)</strong>으로 변질될 위험이 있다. 이를 방지하기 위해서는 강력한 <strong><a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/342_metadata_catalog/">메타데이터 카탈로그</a></strong>와 <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/">데이터 리니지</a>(Lineage)</strong> 추적 기능이 필수적으로 병행되어야 한다."

### Ⅴ. 기대효과 및 결론 (Future & Standard)
[데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 빅데이터 분석과 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 혁신의 핵심 기반이다. 최근에는 [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)의 유연성과 DW의 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 성능을 결합한 <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/">데이터 레이크하우스</a>(<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/">Data Lakehouse</a>)</strong> 아키텍처로 진화하며 기업 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼의 새로운 표준이 되고 있다.

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- <strong><a href="/knowledge-base/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/">Data Swamp</a>:</strong> 관리되지 않아 쓸 수 없게 된 [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)
- <strong><a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/">Object Storage</a>:</strong> [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)의 물리적 기반
- <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/317_etl_vs_elt/">ETL vs ELT</a>:</strong> [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) 적재 시 [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) 방식 선호

### 👶 어린이를 위한 3줄 비유 설명
1. [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 아주 큰 상자에 장난감, 책, 그림, 일기장을 몽땅 담아두는 '마법 상자'예요.

### 📈 관련 키워드 및 발전 흐름도

```text
RDBMS (구조화 데이터만 저장)
    │
    ▼
Data Lake: 비정형 + 정형 데이터 원시 저장
    ├─► S3 · GCS · ADLS (오브젝트 스토리지)
    └─► Schema-on-Read: 읽을 때 스키마 적용
    │
    ▼
Data Lakehouse: Lake + Warehouse 통합 (Delta · Iceberg)
```
2. 예전에는 장난감 통, 책꽂이로 다 나눠야 했지만, 이제는 일단 상자에 다 넣어두고 나중에 놀고 싶을 때 꺼내서 정리하면 돼요.
3. 상자가 아주 커서 세상 모든 물건을 다 담아도 끄떡없답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 218 / 371

← **이전**: [218. 스파크 스트리밍 / Structured Streaming](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/218_spark_streaming_realtime_processing/)
**다음**: [220. 스키마 온 리드 (Schema-on-Read)](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/220_schema_on_read_data_lake/) →

---
