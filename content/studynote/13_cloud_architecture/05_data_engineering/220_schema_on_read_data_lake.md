+++
title = "220. 스키마 온 리드 (Schema-on-Read)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 저장할 때 구조를 강제하지 않고, 분석가가 읽을 때 비로소 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)를 정의하는 <strong>"나중 결정" <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>이다.
> 2. **가치**: 미래에 필요한 모든 분석 형태를 미리 알 수 없는 대용량 원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 <strong>있는 그대로 보존</strong>해 탐색적 분석([EDA](/knowledge-base/studynote/12_it_management/02_itsm_itil/064_eda/))과 [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 엔지니어링이 가능하다.
> 3. **판단 포인트**: [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)의 핵심 철학이지만, 잘못 관리하면 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스왐프([Data Swamp](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/))"로 전락하므로 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a>/<a href="/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/">카탈로그</a> 거버넌스</strong>가 필수다.

---

## Ⅰ. 개요 및 필요성

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 방식에는 두 가지 철학이 존재한다. <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/">Schema-on-Write</a>(<a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 시 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/">스키마</a>)</strong>는 저장 전에 "이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 이 구조여야 한다"라고 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 전통적 방식이고, <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/">Schema-on-Read</a>(읽기 시 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/">스키마</a>)</strong>는 "일단 원시 그대로 저장하고, 필요할 때 읽는 쪽에서 의미를 부여한다"는 현대 [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)의 접근법이다.

빅데이터 시대 이전에는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 형태가 예측 가능했다. 그러나 소셜 미디어 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 센서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 반정형 [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/) [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 응답 등 다양한 형태의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 폭발적으로 늘어나면서, 저장 전에 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)를 고정하면 <strong>미래의 분석 요건 변화</strong>에 대응하지 못한다는 한계가 드러났다.

[Schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/)-on-Read의 핵심 필요성:
- **유연성**: 동일한 원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 서로 다른 팀이 다른 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 관점으로 해석 가능
- **속도**: [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)·변환 없이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 즉시 저장하여 수집 파이프라인 단순화
- **비용**: 원시 [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)/[JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)로 S3 같은 저비용 [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)에 보관



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">전통 DW (Schema-on-Write) 데이터 레이크 (Schema-on-Read)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">소스 데이터</div><div class="kb-diagram-cell">소스 데이터</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">↓ ETL 변환</div><div class="kb-diagram-cell">↓ 원시 그대로 저장</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">↓ 스키마 검증</div><div class="kb-diagram-cell">S3/ADLS (Parquet/JSON/CSV)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">↓ 정제·로드</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">구조화 테이블</div><div class="kb-diagram-cell">읽을 때 ──▶ Spark/Athena가</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(빠른 쿼리)</div><div class="kb-diagram-cell">스키마 해석</div></div>
</div>
</div>



📢 **섹션 요약 비유**: [Schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/)-on-Read는 박물관 수장고와 같다. 유물을 발굴하면 바로 저장하고, 나중에 역사학자·고고학자·미술사가가 각자의 시각으로 의미를 부여하는 것처럼, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 일단 원형 그대로 보존하고 필요할 때 해석한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [Schema-on-Read](/knowledge-base/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/) [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) 아키텍처



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터 수집 계층</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">IoT/로그/DB CDC/API ──▶ Kafka/Kinesis ──▶ S3 (원시 적재)</div></div>
<div class="kb-diagram-note">원시 파일 (JSON/CSV/Parquet)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">레이크 스토리지 (Zone 구조)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Bronze Zone</div><div class="kb-diagram-cell">Silver Zone</div><div class="kb-diagram-cell">Gold Zone</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(원시 원본)</div><div class="kb-diagram-cell">(정제·조인)</div><div class="kb-diagram-cell">(집계·분석 전용)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">스키마 없음</div><div class="kb-diagram-cell">스키마 추론</div><div class="kb-diagram-cell">스키마 확정</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">쿼리/분석 계층 (스키마 부여)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Apache Spark 스키마 추론(inferSchema) / 명시적 StructType</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">AWS Athena CREATE EXTERNAL TABLE (on S3)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Presto/Trino 연방 쿼리, 런타임 스키마 적용</div></div>
</div>
</div>



### 핵심 기술 구성 요소

| 구성 요소 | 역할 | 예시 기술 |
|:---|:---|:---|
| [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/) | 원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 무한 저장 | S3, ADLS Gen2, GCS |
| [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 포맷 | [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)/분할 지원 | [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/), ORC, [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/), Avro |
| [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) | [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 | [Confluent](/knowledge-base/studynote/12_it_management/02_itsm_itil/094_reinforcement_learning/) [Schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/) [Registry](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) |
| 메타스토어 | [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 정의 저장 | AWS Glue, [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) Metastore |
| [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 엔진 | 런타임 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 적용 | Spark, Athena, Trino |
| [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) | 발견·거버넌스 | AWS Glue [Catalog](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/), Apache Atlas |

📢 **섹션 요약 비유**: [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)와 메타스토어는 "번역 사전"이다. 원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 각국 언어로 기록된 편지지만, 읽을 때 번역 사전([스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/))을 꺼내 의미를 이해하는 것처럼 동작한다.

---

## Ⅲ. 비교 및 연결

### [Schema-on-Read](/knowledge-base/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/) vs [Schema-on-Write](/knowledge-base/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/)

| 비교 항목 | [Schema-on-Read](/knowledge-base/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/) ([데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)) | [Schema-on-Write](/knowledge-base/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/) ([데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)) |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/">스키마</a> 적용 시점</strong> | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)·분석 시 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 전 |
| **저장 형태** | 원시([Raw](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/)): [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/), CSV, [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) | 정규화된 구조 테이블 |
| **유연성** | 매우 높음 (미래 요건 대응) | 낮음 (사전 설계 필수) |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 품질</strong> | 낮음 (쓰레기도 들어옴) | 높음 ([ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 통과) |
| <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong> | 보통 (Full Scan 비용) | 우수 ([인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/), 통계 활용) |
| **적합 워크로드** | 탐색적 분석, ML, 배치 | 정기 BI 리포트, [KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) 대시보드 |
| **저장 비용** | 저렴 (S3 기준) | 고비용 ([Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/), Redshift) |
| **대표 플랫폼** | AWS S3 + Glue, Azure [Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) | [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/), [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/), Redshift |

### [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) Zone [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

| Zone | [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 상태 | 내용 |
|:---|:---|:---|
| Bronze ([Raw](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/)) | [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 없음 | 원시 수집 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 그대로 |
| Silver (Cleansed) | [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 추론/정의 | 중복 제거, NULL 처리, 타입 변환 |
| Gold (Curated) | [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 확정 | 집계, 비즈니스 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 모델 |

📢 **섹션 요약 비유**: [Schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/)-on-Read와 [Schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/)-on-Write의 차이는 냉동 식재료 보관과 즉석 반찬 보관의 차이다. 냉동(레이크)은 원재료 그대로 두고 요리할 때 레시피([스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/))를 결정하고, 반찬(웨어하우스)은 미리 양념해 저장하여 빠르게 꺼내 먹는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스왐프([Data Swamp](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/)) 방지 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

[Schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/)-on-Read의 가장 큰 위험은 <strong>거버넌스 부재</strong>다. 아무 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)나 쏟아부으면 "무엇이 어디에 있는지 아무도 모르는" [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 늪이 된다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">위험</div><div class="kb-diagram-note">데이터 스왐프 징후</div></div>
<div class="kb-diagram-tree-item" style="--depth:0">카탈로그 없이 파일만 S3에 쌓임</div>
<div class="kb-diagram-tree-item" style="--depth:0">데이터 오너십 불명확</div>
<div class="kb-diagram-tree-item" style="--depth:0">동일 데이터의 중복·버전 혼재</div>
<div class="kb-diagram-tree-item" style="--depth:0">PII(개인식별정보) 위치 파악 불가</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">해결</div><div class="kb-diagram-note">거버넌스 4대 원칙</div></div>
<div class="kb-diagram-note">1. 메타데이터 자동 크롤링 (Glue Crawler)</div>
<div class="kb-diagram-note">2. 데이터 카탈로그 태깅 (분류/민감도/오너)</div>
<div class="kb-diagram-note">3. Zone 분리 (Bronze → Silver → Gold)</div>
<div class="kb-diagram-note">4. 데이터 품질 규칙 자동화 (Great Expectations, dbt tests)</div>
</div>
</div>



### 실무 시나리오: 전자상거래 [클릭스트림 분석](/knowledge-base/studynote/16_bigdata/05_analysis/120_clickstream_analysis/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">사용자 행동 로그 (100GB/일, JSON 비정형)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Kinesis Data Firehose → S3 Bronze (원시 저장, 15분 파티셔닝)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">AWS Glue ETL Job (야간) → S3 Silver (Parquet 변환, 파티션 키: date/category)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Athena 쿼리 → 상품별 전환율 분석 (스키마: 읽을 때 Parquet 컬럼 파악)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">SageMaker (ML) → 추천 모델 학습 (Bronze 원시 피처 활용)</div>
</div>
</div>



**기술사 핵심 판단**: [Schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/)-on-Read는 "먼저 수집, 나중 결정"의 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이므로, <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/">데이터 레이크</a> 도입 시 반드시 <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/">데이터 카탈로그</a>와 Zone <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a>을 동시 설계</strong>해야 실패하지 않는다.

📢 **섹션 요약 비유**: [Schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/)-on-Read는 [CCTV](/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/) 영상 저장과 같다. 모든 영상을 일단 다 저장하고, 사건이 생겼을 때(분석 요건 발생) 그때 되돌려보며 의미를 찾는다. 단, 영상 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 체계([메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/))가 없으면 수천 시간의 영상에서 아무것도 찾지 못한다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 내용 |
|:---|:---|
| **탐색적 분석 지원** | 미정의 요건의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 원시 그대로 보존해 [EDA](/knowledge-base/studynote/12_it_management/02_itsm_itil/064_eda/) 가능 |
| **ML 파이프라인 지원** | [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 엔지니어링을 위한 원천 원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 |
| **비용 절감** | S3 저장 비용이 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 대비 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~100배 저렴 |
| **시간 단축** | [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 사전 정의 없이 즉시 수집 시작 |

### 한계 및 주의점

| 한계 | 설명 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 품질 보장 어려움</strong> | 오류 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 그대로 저장 → Silver/Gold 정제 필수 |
| <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 불안정</strong> | Full Scan 발생, [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)·포맷 최적화 필요 |
| **거버넌스 비용** | [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/)·태깅·오너십 관리에 지속적 노력 필요 |
| **보안 복잡성** | 원시 PII 포함 가능성 → 컬럼 단위 마스킹 필요 |

📢 **섹션 요약 비유**: [Schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/)-on-Read는 강력하지만 정리하지 않은 도서관과 같다. 모든 책([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))이 있지만, 도서 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 시스템([카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/)·거버넌스)이 없으면 원하는 책을 찾는 데 더 많은 시간이 걸릴 수 있다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| [Schema-on-Write](/knowledge-base/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/) | [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)의 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), 반대 개념 |
| [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) ([Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)) | [Schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/)-on-Read의 주요 적용 플랫폼 |
| [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) | 스왐프 방지를 위한 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 거버넌스 도구 |
| [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)/ORC | 컬럼 지향 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 포맷, 레이크 표준 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 형식 |
| [Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/) | [Schema-on-Read](/knowledge-base/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/) + ACID [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 결합 |
| [Medallion Architecture](/knowledge-base/studynote/14_data_engineering/04_mlops/194_medallion_architecture_bronze_silver_gold/) | Bronze-Silver-Gold Zone 설계 패턴 |
| AWS Glue Crawler | 자동 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 탐지 및 [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) 등록 |

### 👶 어린이를 위한 3줄 비유 설명
1. [Schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/)-on-Read는 사진을 찍을 때 필터를 나중에 고르는 것처럼, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 저장할 때는 그냥 두고 나중에 어떻게 볼지 결정한다.

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Schema-on-Write: 저장 전 스키마 강제 (DW)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Schema-on-Read: 저장 시 원시 형태 → 읽을 때 스키마 적용</div>
<div class="kb-diagram-tree-item" style="--depth:2">Data Lake: S3 + Parquet/JSON</div>
<div class="kb-diagram-tree-item" style="--depth:2">유연성 ↑ · 분석 속도 ↓ (트레이드오프)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Lakehouse: 두 방식의 장점 통합</div>
</div>
</div>


2. 마치 레고 블록을 일단 다 사두고, 만들고 싶은 게 생겼을 때 조립하는 것처럼, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 일단 쌓아두고 분석할 때 모양을 만든다.
3. [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 아무거나 다 넣는 큰 수납함인데, 어디에 무엇이 있는지 적어두는 메모([카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/))가 없으면 아무것도 못 찾는 수납함이 된다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 219 / 371

← **이전**: [219. 데이터 레이크 (Data Lake) - 원시 데이터 중심의 전사적 통합 저장소](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/219_data_lake/)
**다음**: [221. 데이터 웨어하우스 (Data Warehouse / DW)](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/221_data_warehouse_olap_sql/) →

---
