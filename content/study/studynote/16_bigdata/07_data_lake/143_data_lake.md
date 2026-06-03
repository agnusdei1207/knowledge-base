---
title: 데이터 레이크 (Data Lake)
date: '2024-05-22'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)
1. 정형, 반정형, [[004_unstructured_data|비정형 데이터]]를 포함한 방대한 원시 [[001_dikw_pyramid|데이터]]([[225_raw|Raw]] [[001_dikw_pyramid|Data]])를 목적에 [[083_relationship_in_er_model|관계]]없이 **원래의 형식 그대로 저장**하는 거대 저장소이다.
2. 저장 시점에 [[005_schema|스키마]]를 정의하지 않는 **[[009_schema_on_read|스키마 온 리드]]([[009_schema_on_read|Schema-on-Read]])** 방식을 사용하여 [[001_dikw_pyramid|데이터]] 수집의 유연성과 저비용성을 극대화한다.
3. [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]([[209_data_warehouse_schema_on_write|DW]])의 폐쇄성을 극복하고 빅데이터 분석 및 [[241_machine_learning_basics|머신러닝]]을 위한 통합 기반 인프라 역할을 수행한다.

---

### Ⅰ. 개요 ([[033_context|Context]] & Background)
기존의 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]는 [[001_dikw_pyramid|데이터]]를 저장하기 전에 엄격하게 정제하고 구조화해야 했기에 [[004_unstructured_data|비정형 데이터]] 처리에 한계가 있었다. [[208_data_lake_schema_on_read|데이터 레이크]]는 저렴한 클라우드 스토리지(S3, [[013_hdfs|HDFS]])를 활용하여 일단 모든 [[001_dikw_pyramid|데이터]]를 '호수'에 쏟아부은 뒤, 분석가가 필요할 때 꺼내서 가공할 수 있게 하는 패러다임의 전환을 가져왔다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
[[208_data_lake_schema_on_read|데이터 레이크]]는 수집(Ingest), 저장(Store), 가공([[300_process|Process]]), 소비(Consume)의 4단계 아키텍처를 가진다.

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

1. **[[009_schema_on_read|스키마 온 리드]] ([[009_schema_on_read|Schema-on-Read]])**: [[001_dikw_pyramid|데이터]]를 읽을 때 구조를 부여한다. (유연성 극대화)
2. **비용 효율성**: 범용 x86 서버나 저가형 객체 스토리지를 사용하여 [[209_data_warehouse_schema_on_write|DW]] 대비 약 1/[[489_raid_10_hybrid|10]] 이하의 비용으로 저장 가능하다.
3. **거버넌스 필수**: [[213_data_catalog_metadata|데이터 카탈로그]]와 [[203_metadata_management|메타데이터 관리]]가 없으면 '[[288_data_swamp_metadata_management_absence|데이터 늪]]([[288_data_swamp_metadata_management_absence|Data Swamp]])'으로 전락할 위험이 크다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] ([[209_data_warehouse_schema_on_write|DW]]) | [[208_data_lake_schema_on_read|데이터 레이크]] ([[208_data_lake_schema_on_read|Data Lake]]) |
| :--- | :--- | :--- |
| **[[001_dikw_pyramid|데이터]] 형태** | 정형 (Structured) | 모든 형태 ([[225_raw|Raw]] Format) |
| **[[005_schema|스키마]] 방식** | [[010_schema_on_write|Schema-on-Write]] (저장 시 정의) | [[009_schema_on_read|Schema-on-Read]] (읽을 때 정의) |
| **사용자** | 비즈니스 분석가 (BI) | [[001_dikw_pyramid|데이터]] 과학자, 엔지니어 |
| **저장 비용** | 비쌈 (고성능 스토리지) | 저렴함 ([[494_object_storage|Object Storage]]) |

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
1. **메들리온 아키텍처 ([[194_medallion_architecture_bronze_silver_gold|Medallion Architecture]])**: [[001_dikw_pyramid|데이터]]를 Bronze(원시), Silver(정제), Gold(집계) 계층으로 나누어 관리함으로써 [[001_dikw_pyramid|데이터]] 품질을 보장해야 한다.
2. **델타 레이크([[147_delta_lake|Delta Lake]]) 도입**: [[208_data_lake_schema_on_read|데이터 레이크]]의 한계인 [[191_transaction_concept_states|트랜잭션]](ACID) 부재를 해결하기 위해 [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]]을 도입하여 '[[210_data_lakehouse_delta_lake|데이터 레이크하우스]]'로 진화하는 추세다.
3. **PE 관점의 판단**: [[208_data_lake_schema_on_read|데이터 레이크]]는 분석의 자유도를 높이지만 보안과 권한 관리가 매우 까다롭다. AWS Lake Formation 같은 도구를 통해 미세 권한 제어([[399_fine_grained_multithreading|Fine-grained]] [[547_access_control_rwx|access control]])를 반드시 구축해야 한다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
[[208_data_lake_schema_on_read|데이터 레이크]]는 현대 기업의 디지털 자산 창고이다. 향후에는 물리적으로 흩어진 레이크들을 연결하는 [[212_data_fabric_virtualization|데이터 패브릭]]([[212_data_fabric_virtualization|Data Fabric]])과 [[136_variance|분산]]된 거버넌스를 지향하는 [[211_data_mesh_domain_ownership|데이터 메시]]([[320_data_mesh|Data Mesh]])로 발전할 것이며, 이는 [[190_ai_llm_requirements_specification|AI]]/ML 기반의 의사결정을 가속화하는 핵심 동력이 될 것이다.

---

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **상위 개념**: Big [[001_dikw_pyramid|Data]] [[319_architecture|Architecture]], [[001_dikw_pyramid|Data]] Infrastructure
- **하위 개념**: S3, [[013_hdfs|HDFS]], Azure [[208_data_lake_schema_on_read|Data Lake]] Store (ADLS)
- **연관 개념**: [[288_data_swamp_metadata_management_absence|Data Swamp]], [[009_schema_on_read|Schema-on-Read]], [[194_medallion_architecture_bronze_silver_gold|Medallion Architecture]], [[146_lakehouse|Lakehouse]]

---

### 📈 관련 키워드 및 발전 흐름도

```text
[Data Warehouse]
    │
    ▼
[Data Lake]
    │
    ▼
[Schema-on-Read]
    │
    ▼
[Lakehouse]
```

이 흐름도는 선행 개념이 현재 개념으로 응축되고, 다시 확장 개념으로 이어지는 순서를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. **[[208_data_lake_schema_on_read|데이터 레이크]]**: 세상의 모든 장난감을 일단 거대한 창고에 다 넣어두는 거예요.
2. **유연함**: 나중에 "로봇만 가지고 놀래!"라고 할 때 그제서야 로봇을 골라내서 노는 방식이에요.
3. **주의사항**: 정리를 안 하고 막 던져넣기만 하면 나중에 원하는 걸 찾을 수 없는 '쓰레기산'이 될 수 있어요.
