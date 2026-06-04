+++
title = "155. ELT vs ETL — 클라우드 시대 데이터 변환 패러다임 전환"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
1. [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) (Extract, Transform, Load)은 변환 후 적재하는 전통 방식으로 스토리지 비용이 비쌌던 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 환경에 최적화되었으나, 클라우드 시대에는 <strong>먼저 적재하고 나중에 변환하는 <a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/">ELT</a> (Extract, Load, Transform)</strong>가 표준으로 전환되었다.
2. dbt ([data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) build tool)는 [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) 패러다임의 핵심 도구로, [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)·[레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) 내부에서 SQL로 선언적 변환을 수행하며 테스트·문서화·리니지를 자동 관리한다.
3. ELT는 <strong>원시 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>(<a href="/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/">Raw</a>) 보존</strong>, **반복적 변환 가능**, <strong>타임 트래블 기반 소급 재처리</strong>를 가능하게 하여 [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)의 유연성과 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적성을 극대화한다.

---

## Ⅰ. 개요 및 필요성

1990~2010년대 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)([Oracle](/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/), Teradata) 환경에서는 스토리지가 고가였고 컴퓨팅 자원도 제한적이었다. ETL은 이 제약 안에서 필요한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 정제·[압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)하여 DW에 적재하는 최적 방식이었다.

클라우드 시대(2010년 이후)에는 S3/ADLS 스토리지 비용이 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 대비 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~100분의 1 수준으로 하락하고, Spark/[BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/)/Snowflake의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 컴퓨팅이 변환 비용을 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)했다. 이 변화가 [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) 패러다임으로의 전환을 이끌었다.

| 비교 항목 | [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) | [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) |
|:---|:---|:---|
| 변환 위치 | 스테이징 서버 (외부) | [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)/[레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) 내부 |
| 원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보존 | 없음 (변환 후 버림) | 있음 ([Raw](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) 계층 보존) |
| 스토리지 사용 | 최소화 (정제 후 적재) | 최대 ([Raw](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) + 변환 결과) |
| 재처리 유연성 | 낮음 (원본 없음) | 높음 (Raw에서 재변환) |
| 적합 환경 | [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) | 클라우드 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) / [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) |
| 대표 도구 | Informatica, SSIS, Talend | dbt, [Spark SQL](/knowledge-base/studynote/16_bigdata/03_spark/056_spark_sql/), Dataflow |

> 📢 **섹션 요약 비유**: ETL은 식재료를 요리해서만 냉장고에 넣는 방식이고, ELT는 식재료를 그대로 냉장고에 넣고 필요할 때 꺼내서 요리하는 방식이다. 냉장고(스토리지)가 저렴해지면서 후자가 유리해졌다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+----------------------------------------------------------------+
|                   ETL vs ELT 비교                               |
+----------------------------------------------------------------+
|                                                                |
|  【ETL 흐름】                                                   |
|                                                                |
|  [소스] --Extract---> [스테이징 서버]                            |
|                      Transform (정제·집계)                      |
|                           |                                    |
|                           +--Load---> [DW] ---> [BI 도구]        |
|                                                                |
|  【ELT 흐름】                                                   |
|                                                                |
|  [소스] --Extract---> [레이크하우스 / 클라우드 DW]               |
|                      (Bronze: Raw 적재)                         |
|                           |                                    |
|                    Transform (dbt / Spark SQL)                  |
|                    Silver: 정제  Gold: 집계                     |
|                           |                                    |
|                           +---> [BI / ML 도구]                  |
|                                                                |
+----------------------------------------------------------------+
```

<strong>dbt (<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">data</a> build tool) 핵심 기능</strong>

| 기능 | 설명 | 장점 |
|:---|:---|:---|
| Model | SQL SELECT로 변환 정의 | 선언적, 재사용 가능 |
| Test | `not_null`, `unique`, `accepted_values` | 변환 결과 자동 품질 검사 |
| [Documentation](/knowledge-base/studynote/04_software_engineering/06_software_architecture/378_software_documentation/) | `description` 필드로 컬럼 문서화 | 자동 [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| Lineage [Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/888_graph/) | 모델 간 의존성 자동 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) | 영향 분석 즉시 파악 |
| Materialization | Table / [View](/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/) / Incremental / Ephemeral | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)·비용 트레이드오프 선택 |
| Seed | CSV로 정적 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리 | 코드와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 함께 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 |

**dbt Incremental 모델 패턴**
```text
-- models/silver/orders_cleaned.sql
-- dbt Jinja 매크로 사용
-- { { config(materialized='incremental',
--           unique_key='order_id',
--           on_schema_change='sync_all_columns') } }

SELECT
    order_id,
    customer_id,
    amount,
    created_at
FROM source('bronze', 'orders_raw')
WHERE status != 'cancelled'
-- incremental 조건: 마지막 실행 이후 데이터만 처리
-- AND created_at > (SELECT MAX(created_at) FROM this_model)
```

> 📢 **섹션 요약 비유**: dbt는 요리 레시피 북이다. 각 요리(모델)의 재료(소스)와 조리법(SQL)이 정해져 있고, 완성된 요리(결과 테이블)가 예상대로 나왔는지 검사(test)하는 과정도 포함된다.

---

## Ⅲ. 비교 및 연결

<strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/">ELT</a> 도구 비교</strong>

| 도구 | 실행 위치 | 특징 | 적합 환경 |
|:---|:---|:---|:---|
| dbt Core | [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)/[레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) 내부 | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/), SQL 선언적 | [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/), [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/), [Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/) |
| dbt Cloud | 관리형 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/951_saas/) | IDE + [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) + 협업 | 팀 규모 조직 |
| [Spark SQL](/knowledge-base/studynote/16_bigdata/03_spark/056_spark_sql/) | [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) | Python/Scala 병행 | 대규모 배치 변환 |
| Dataflow | GCP 관리형 | Apache Beam 기반 | GCP 생태계 |
| Glue | AWS 관리형 | Spark 기반, S3 통합 | AWS 생태계 |

**연관 개념 연결**

- <strong><a href="/knowledge-base/studynote/14_data_engineering/04_mlops/194_medallion_architecture_bronze_silver_gold/">Medallion Architecture</a></strong>: ELT의 Bronze->Silver->Gold가 Medallion 계층과 완벽히 매핑
- <strong><a href="/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/">Data Product</a></strong>: dbt 모델이 Gold 계층 [데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/)의 변환 로직을 담당
- <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/">Data Lineage</a></strong>: dbt가 자동으로 리니지 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하여 Unity Catalog와 연계

> 📢 **섹션 요약 비유**: ETL은 택배 물건을 포장해서 배송하는 방식이고, ELT는 원재료를 창고에 다 넣어두고 주문이 오면 그때 포장하는 방식이다. 창고(스토리지) 비용이 싸지면서 후자가 더 효율적이 됐다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/">ELT</a> 전환 <a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/">체크리스트</a></strong>
- [ ] 원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 Bronze 계층에 보존하는 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 설계
- [ ] dbt 프로젝트 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화 및 소스 등록 (`dbt source freshness` [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/))
- [ ] Silver 모델: `materialized='incremental'` + `unique_key` [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)
- [ ] Gold 모델: `materialized='table'` + [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)
- [ ] `dbt test` 실행 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 통합

**기술사 답안 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) -> [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) 전환 이유 | 클라우드 스토리지 저비용화, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 컴퓨팅 확장성 |
| dbt의 역할 | [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 내부 SQL 선언적 변환 + 테스트 + 리니지 자동화 |
| Incremental 모델 장점 | 전체 재처리 없이 새 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 변환 -> 비용·시간 절감 |
| [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) 한계 | 원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보존으로 스토리지 비용 증가, 민감 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보안 관리 필요 |

> 📢 **섹션 요약 비유**: [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) 도입은 즉석 조리 냉장고를 도입하는 것이다. 모든 식재료를 신선하게 보관하고(Bronze), 필요할 때 빠르게 조리(dbt 변환)하여 서빙(Gold)한다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 재처리 유연성 | [Raw](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) 보존으로 언제든 새 로직으로 소급 재처리 가능 |
| 운영 단순화 | 스테이징 서버 제거, [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 내부에서 모든 변환 처리 |
| 품질 가시성 | dbt test로 변환 결과 품질 자동 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| 협업 향상 | dbt 모델 = SQL 코드 -> Git [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 + [코드 리뷰](/knowledge-base/studynote/04_software_engineering/06_software_architecture/330_code_review/) |

ETL에서 ELT로의 패러다임 전환은 클라우드 빅데이터 인프라 확산과 함께 이미 완료된 흐름이다. dbt는 현재 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 팀 표준 도구로 자리 잡았으며, [Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/)·[Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/)·[BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/) 모두 네이티브 dbt 통합을 지원한다. 기술사 시험에서는 <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/317_etl_vs_elt/">ETL vs ELT</a> 전환 이유</strong>, **dbt 핵심 기능**, <strong>Incremental 모델 동작 원리</strong>가 핵심 논점이다.

> 📢 **섹션 요약 비유**: [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) 시대는 사진 현상 방식의 변화와 같다. 필름 사진([ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/))은 찍자마자 현상해야 했지만, 디지털 사진([ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/))은 [RAW](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)로 보관하고 필요할 때 다양한 방식으로 편집할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| dbt | [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) 핵심 도구 | SQL 선언적 변환·테스트·리니지 |
| Incremental 모델 | dbt [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화 | 신규 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 처리 패턴 |
| Bronze 계층 | [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) 전제 조건 | [Raw](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 영구 보존 |
| [Data Lineage](/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/) | 자동화 산출물 | dbt가 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 모델 의존성 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) |
| [Medallion Architecture](/knowledge-base/studynote/14_data_engineering/04_mlops/194_medallion_architecture_bronze_silver_gold/) | 연관 패턴 | [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) 흐름 = Bronze->Silver->Gold |
| [Schema-on-Read](/knowledge-base/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/) | [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) 특성 | 적재 시 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 강제 않음 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[ETL (Extract-Transform-Load) — 소스에서 추출 후 변환, 타겟 DW에 적재]
    |
    v
[데이터 웨어하우스 (DW) — 정제된 구조적 데이터 중앙 저장소, ETL 전제]
    |
    v
[ELT (Extract-Load-Transform) — 원시 데이터 먼저 적재, 클라우드 DW에서 변환]
    |
    v
[데이터 레이크 (Data Lake) — 원시 데이터 무제한 적재, ELT 패러다임과 친화적]
    |
    v
[레이크하우스 (Lakehouse) — Delta Lake·Iceberg 기반 ELT + ACID 트랜잭션 통합]
```

이 흐름은 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) DW를 위한 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 패러다임이 클라우드 규모에서 ELT로 전환되고, [데이터 레이크하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/) 아키텍처로 통합·발전하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. ETL은 재료를 사오자마자 다 손질해서 냉장고에 넣는 방식이고, ELT는 재료 그대로 일단 냉장고에 넣고 필요할 때 꺼내서 손질하는 방식이에요.
2. 냉장고(저장공간)가 저렴해지면서 미리 다 손질하지 않아도 되니 [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) 방식이 더 편리해졌어요.
3. dbt는 냉장고 안 재료를 어떻게 요리할지 레시피 북이에요. 레시피(SQL)를 코드로 기록해두면 언제나 같은 요리가 나와요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 155 / 262

<- **이전**: [154. 데이터 제품 (Data Product) — API 인터페이스와 SLA 품질 지표](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/)
**다음**: [156. 데이터 패브릭 (Data Fabric) — 위치 무관 지능형 데이터 연결](/knowledge-base/studynote/16_bigdata/07_data_lake/156_data_fabric/) ->

---
