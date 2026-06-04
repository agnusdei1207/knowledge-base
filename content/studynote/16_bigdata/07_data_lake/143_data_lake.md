---
title: "데이터 레이크 (Data Lake)"
date: "2024-05-22"
tags:
  - "studynote-bigdata"
---


## 핵심 인사이트 (3줄 요약)
1. 정형, 반정형, [비정형 데이터](/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)를 포함한 방대한 원시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([Raw](/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 목적에 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)없이 <strong>원래의 형식 그대로 저장</strong>하는 거대 저장소이다.
2. 저장 시점에 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)를 정의하지 않는 <strong><a href="/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/">스키마 온 리드</a>(<a href="/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/">Schema-on-Read</a>)</strong> 방식을 사용하여 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집의 유연성과 저비용성을 극대화한다.
3. [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)([DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/))의 폐쇄성을 극복하고 빅데이터 분석 및 [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)을 위한 통합 기반 인프라 역할을 수행한다.

---

### Ⅰ. 개요 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
기존의 [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 저장하기 전에 엄격하게 정제하고 구조화해야 했기에 [비정형 데이터](/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) 처리에 한계가 있었다. [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 저렴한 클라우드 스토리지(S3, [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/))를 활용하여 일단 모든 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 '호수'에 쏟아부은 뒤, 분석가가 필요할 때 꺼내서 가공할 수 있게 하는 패러다임의 전환을 가져왔다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
[데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 수집(Ingest), 저장(Store), 가공([Process](/studynote/12_it_management/05_security_compliance/943_process/)), 소비(Consume)의 4단계 아키텍처를 가진다.

```text
[ Data Lake Architecture / 데이터 레이크 아키텍처 ]

    Sources (Log, IoT, DB)         Data Lake (S3, HDFS)            Analysis & ML
    +-------------------+       +-----------------------+       +-------------------+
    | [Structured]      |       |  Landing / Raw Zone   |       |   BI Dashboards   |
    | [Semi-structured] | ----> |  (Schema-on-Read)     | ----> |   (Tableau, PBI)  |
    | [Unstructured]    |       +-----------+-----------+       +---------+---------+
    +---------+---------+                   |                             |
                                            v                             v
                                +-----------+-----------+       +---------+---------+
                                |  Curated / Gold Zone  | ----> |  Machine Learning |
                                |  (Processed Data)     |       |  (PyTorch, Spark) |
                                +-----------------------+       +-------------------+
```

1. <strong><a href="/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/">스키마 온 리드</a> (<a href="/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/">Schema-on-Read</a>)</strong>: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽을 때 구조를 부여한다. (유연성 극대화)
2. **비용 효율성**: 범용 x86 서버나 저가형 객체 스토리지를 사용하여 [DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 대비 약 1/[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) 이하의 비용으로 저장 가능하다.
3. **거버넌스 필수**: [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)와 [메타데이터 관리](/studynote/16_bigdata/10_governance/203_metadata_management/)가 없으면 '[데이터 늪](/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/)([Data Swamp](/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/))'으로 전락할 위험이 크다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) ([DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)) | [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) ([Data Lake](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)) |
| :--- | :--- | :--- |
| <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 형태</strong> | 정형 (Structured) | 모든 형태 ([Raw](/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) Format) |
| <strong><a href="/studynote/05_database/01_db_architecture_relational/005_schema/">스키마</a> 방식</strong> | [Schema-on-Write](/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/) (저장 시 정의) | [Schema-on-Read](/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/) (읽을 때 정의) |
| **사용자** | 비즈니스 분석가 (BI) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자, 엔지니어 |
| **저장 비용** | 비쌈 (고성능 스토리지) | 저렴함 ([Object Storage](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)) |

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
1. <strong>메들리온 아키텍처 (<a href="/studynote/14_data_engineering/04_mlops/194_medallion_architecture_bronze_silver_gold/">Medallion Architecture</a>)</strong>: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 Bronze(원시), Silver(정제), Gold(집계) 계층으로 나누어 관리함으로써 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질을 보장해야 한다.
2. <strong>델타 레이크(<a href="/studynote/16_bigdata/07_data_lake/147_delta_lake/">Delta Lake</a>) 도입</strong>: [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)의 한계인 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)(ACID) 부재를 해결하기 위해 [오픈 테이블 포맷](/studynote/14_data_engineering/01_infrastructure/054_open_table_format_iceberg_delta_hudi/)을 도입하여 '[데이터 레이크하우스](/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/)'로 진화하는 추세다.
3. **PE 관점의 판단**: [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 분석의 자유도를 높이지만 보안과 권한 관리가 매우 까다롭다. AWS Lake Formation 같은 도구를 통해 미세 권한 제어([Fine-grained](/studynote/01_computer_architecture/11_multicore_synchronization/399_fine_grained_multithreading/) [access control](/studynote/02_operating_system/09_file_system/547_access_control_rwx/))를 반드시 구축해야 한다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
[데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 현대 기업의 디지털 자산 창고이다. 향후에는 물리적으로 흩어진 레이크들을 연결하는 [데이터 패브릭](/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)([Data Fabric](/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/))과 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)된 거버넌스를 지향하는 [데이터 메시](/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)([Data Mesh](/studynote/12_it_management/05_security_compliance/320_data_mesh/))로 발전할 것이며, 이는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)/ML 기반의 의사결정을 가속화하는 핵심 동력이 될 것이다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **상위 개념**: Big [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/), [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Infrastructure
- **하위 개념**: S3, [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/), Azure [Data Lake](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) Store (ADLS)
- **연관 개념**: [Data Swamp](/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/), [Schema-on-Read](/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/), [Medallion Architecture](/studynote/14_data_engineering/04_mlops/194_medallion_architecture_bronze_silver_gold/), [Lakehouse](/studynote/16_bigdata/07_data_lake/146_lakehouse/)

---

### 📈 관련 키워드 및 발전 흐름도

```text
[Data Warehouse]
    |
    v
[Data Lake]
    |
    v
[Schema-on-Read]
    |
    v
[Lakehouse]
```

이 흐름도는 선행 개념이 현재 개념으로 응축되고, 다시 확장 개념으로 이어지는 순서를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. <strong><a href="/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/">데이터 레이크</a></strong>: 세상의 모든 장난감을 일단 거대한 창고에 다 넣어두는 거예요.
2. **유연함**: 나중에 "로봇만 가지고 놀래!"라고 할 때 그제서야 로봇을 골라내서 노는 방식이에요.
3. **주의사항**: 정리를 안 하고 막 던져넣기만 하면 나중에 원하는 걸 찾을 수 없는 '쓰레기산'이 될 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 143 / 262

<- **이전**: [142. 스키마리스 설계 패턴 (Schemaless Design Patterns) — 임베딩 vs 참조](/studynote/16_bigdata/06_nosql/142_schemaless_design_patterns/)
**다음**: [데이터 늪 (Data Swamp)](/studynote/16_bigdata/07_data_lake/144_data_swamp/) ->

---
