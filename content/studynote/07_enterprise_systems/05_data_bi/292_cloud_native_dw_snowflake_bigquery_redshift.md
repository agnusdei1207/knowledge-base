+++
title = "292. 클라우드 네이티브 DW (Snowflake, BigQuery, Redshift) 아키텍처"
date = 2026-04-21

[taxonomies]
tags = ["studynote-enterprise-systems"]

[extra]
tags = ["studynote-enterprise-systems"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) (Cloud-Native [Data Warehouse](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/208_data_warehouse_schema_on_write_inmon/))는 스토리지와 컴퓨팅을 분리하여 무제한 확장과 사용량 기반 과금을 실현한 차세대 [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 아키텍처다.
> 2. **가치**: [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 대비 인프라 관리 부담 제거, 탄력적 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/), 멀티 클러스터 동시 처리로 수백 명의 동시 분석 작업 부하를 처리할 수 있다.
> 3. **판단 포인트**: [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/)(멀티클라우드·공유 가능), [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/)([서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)·ML 통합), Redshift(AWS 생태계)는 각각 강점이 달라 클라우드 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)과 분석 패턴에 맞게 선택해야 한다.

## Ⅰ. 개요 및 필요성

전통적인 [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)(Teradata, [Oracle](/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/) Exadata)는 고성능이지만 수억 원의 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 투자, 고정된 용량, 확장의 어려움이 문제였다. 클라우드 시대에 들어서며 [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/)(2014), Amazon Redshift(2012), Google [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/)(2010)가 등장해 패러다임을 바꿨다.

[클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) DW의 핵심 혁신은 스토리지(Storage)와 컴퓨팅(Compute)의 완전한 분리다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 저렴한 [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)(S3, GCS)에 저장하고, [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 처리는 독립적으로 [스케일 업](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)/다운 가능한 컴퓨팅 클러스터가 담당한다. 이를 통해 사용한 만큼만 비용을 내고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 폭증 시 스토리지와 컴퓨팅을 독립적으로 증설할 수 있다.

📢 **섹션 요약 비유**: 전통 DW는 주방 크기(스토리지)와 요리사 수(컴퓨팅)가 고정된 레스토랑이고, 클라우드 DW는 주방은 그대로 두고 바쁜 날엔 임시 요리사를 무한정 고용할 수 있는 클라우드 레스토랑이다.

## Ⅱ. 아키텍처 및 핵심 원리

```
┌─────────────────────────────────────────────────────────────┐
│           클라우드 네이티브 DW 아키텍처 (Snowflake 예시)      │
│                                                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │           스토리지 레이어 (분리된 오브젝트 스토리지)  │    │
│  │    S3 / GCS / Azure Blob — 컬럼 기반 압축 저장      │    │
│  └──────────────────────────┬─────────────────────────┘    │
│                              │                              │
│  ┌───────────────────────────▼──────────────────────────┐  │
│  │           컴퓨팅 레이어 (독립 Virtual Warehouse)       │  │
│  │                                                       │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │  │
│  │  │ BI 클러스터  │  │ ETL 클러스터│  │ DS 클러스터 │   │  │
│  │  │ (Tableau용) │  │ (Fivetran용)│  │ (Python용)  │   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘   │  │
│  │     ↕ 독립 확장      ↕ 독립 확장     ↕ 독립 확장     │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │              클라우드 서비스 레이어                   │    │
│  │  메타데이터 관리 | 쿼리 최적화 | 보안 | 과금 추적    │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 3대 클라우드 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 비교

| 항목 | [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) | Google [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/) | Amazon Redshift |
|:---|:---|:---|:---|
| 아키텍처 | 스토리지/컴퓨팅 완전 분리 | 완전 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) | 스토리지/컴퓨팅 분리 (RA3) |
| 과금 | 컴퓨팅 초 단위 | 스캔 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) TB당 | 노드 시간 또는 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) |
| 멀티클라우드 | ✅ (AWS/GCP/Azure) | GCP 전용 | AWS 전용 |
| ML 통합 | Snowpark (Python/Java) | [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/) ML 내장 | Redshift ML (SageMaker) |
| [Zero-Copy](/knowledge-base/studynote/02_operating_system/09_file_system/566_mmap_zero_copy_sendfile/) [Clone](/knowledge-base/studynote/02_operating_system/02_process_thread/149_clone_system_call/) | ✅ | ❌ | ❌ |
| 동시 사용자 확장 | Virtual Warehouse 다중 | [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 자동 | [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) |
| 최적 환경 | 멀티클라우드, 공유 | GCP 중심, ML 내장 | AWS 네이티브 |

📢 **섹션 요약 비유**: Snowflake는 어느 도시에서도 영업하는 체인점, BigQuery는 구글시에만 있는 첨단 음식점, Redshift는 아마존 물류 도시의 전용 식당이다.

## Ⅲ. 비교 및 연결

### 전통 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) vs [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)

| 항목 | 전통 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) (Teradata/[Oracle](/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/)) | 클라우드 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) |
|:---|:---|:---|
| [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 투자 | 수억~수백억 원 | 사용량 기반 ([초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 0원) |
| 확장성 | 물리 장비 추가 필요 | 클릭/API로 즉시 확장 |
| 관리 | [DBA](/knowledge-base/studynote/05_database/01_db_architecture_relational/025_dba_database_administrator/) 전담 팀 필요 | 관리형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) (Managed) |
| [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) | [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) 존재 | 멀티 AZ 자동 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) |
| 업그레이드 | 수개월 프로젝트 | 자동 무중단 업데이트 |

📢 **섹션 요약 비유**: 전통 DW는 자가 건물 소유, 클라우드 DW는 월세 오피스—관리 걱정 없이 필요한 만큼 쓰고 이사도 자유롭다.

## Ⅳ. 실무 적용 및 기술사 판단

**선택 기준**:
1. **클라우드 벤더 독립성 중요**: [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) (멀티클라우드)
2. **ML/[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 분석 비중 높음**: [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/) (내장 ML, Vertex [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 통합)
3. **AWS 생태계 이미 구축**: Redshift (S3, Glue, SageMaker 통합)
4. **비용 절감 우선**: [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/) [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) ([쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 없을 때 과금 없음)

**최적화 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)**:
- [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)·클러스터링으로 스캔 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 최소화 (비용 절감)
- 결과 [캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/) 활용으로 동일 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 재실행 비용 제거
- Auto-suspend [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)으로 유휴 컴퓨팅 자동 정지
- [데이터 공유](/knowledge-base/studynote/05_database/06_dw_olap_trends/386_data_clean_room_sharing/) 기능으로 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 없이 파트너사 실시간 [데이터 공유](/knowledge-base/studynote/05_database/06_dw_olap_trends/386_data_clean_room_sharing/)

📢 **섹션 요약 비유**: 클라우드 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 최적화는 택시 운전—빈 차로 달리지 말고(Auto-suspend), 승객이 많을 때만 차를 더 부르는([스케일 아웃](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)) 지혜가 필요하다.

## Ⅴ. 기대효과 및 결론

**기대효과**:
- 인프라 관리 비용 60~80% 절감
- [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~100배 향상 (컬럼 스캔 최적화)
- 동시 분석 사용자 무제한 확장 (멀티 클러스터)
- [데이터 공유](/knowledge-base/studynote/05_database/06_dw_olap_trends/386_data_clean_room_sharing/) 기능으로 파트너·자회사 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 협업 혁신

**한계 및 전제조건**:
- 대규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스캔 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 반복 시 비용이 예상보다 클 수 있음
- [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 최적화 역량([파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/), 클러스터링) 필요
- [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)에서의 마이그레이션은 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 변환 작업이 필요
- [데이터 주권](/knowledge-base/studynote/09_security/16_data_privacy/809_data_sovereignty/) 요건(국내 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 역외 이전 규제) 검토 필수

📢 **섹션 요약 비유**: 클라우드 DW는 고성능 렌터카—빠르고 편리하지만 과속하면(비효율 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)) 연료비(비용)가 폭발하므로 운전 요령이 필요하다.

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| Separation of Compute/Storage | 핵심 원리 | 독립 확장 가능한 아키텍처의 기반 |
| [Zero-Copy](/knowledge-base/studynote/02_operating_system/09_file_system/566_mmap_zero_copy_sendfile/) [Clone](/knowledge-base/studynote/02_operating_system/02_process_thread/149_clone_system_call/) | [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) 기능 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복사 없이 즉각 [클론](/knowledge-base/studynote/02_operating_system/02_process_thread/149_clone_system_call/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| [Data Lakehouse](/knowledge-base/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/) | 진화 방향 | DW와 레이크의 통합 아키텍처 |
| [HTAP](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) | 관련 개념 | [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)+분석 동시 처리 |
| [Columnar Storage](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/234_columnar_storage_parquet_orc/) | 기반 기술 | 분석 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 최적화 컬럼 기반 저장 |

### 📈 관련 키워드 및 발전 흐름도

```
온프레미스 MPP DW (Teradata, Netezza)
    │
    ▼
Hadoop 기반 분산 처리 (HDFS + Hive)
    │
    ▼
클라우드 DW 1세대 (Redshift - 컬럼 스토어)
    │
    ▼
스토리지·컴퓨팅 분리 DW (Snowflake, BigQuery)
    │
    ▼
서버리스·멀티클러스터·Zero-Copy Clone 진화
```

> **키워드**: [Cloud Native](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/199_cloud_native_architecture_msa_cicd_devops/) [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/), [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/), [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/), Redshift, MPP, [Storage-Compute Separation](/knowledge-base/studynote/07_enterprise_systems/06_exam_summary/391_storage_compute_separation/), [Serverless](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)

### 👶 어린이를 위한 3줄 비유 설명

1. 클라우드 DW는 구름 위에 있는 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 도서관이에요—책([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))은 엄청나게 많이 보관하면서, 필요할 때만 독서실 자리(컴퓨팅)를 빌려 써요.
2. 바쁠 때는 독서실 자리를 100개로 늘리고, 한산할 때는 5개만 쓰면 되니까 낭비가 없어요.
3. 마치 클라우드 게임처럼, 내 컴퓨터가 약해도 서버가 강력하니까 엄청난 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 빠르게 분석할 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 292 / 482

← **이전**: [291. 데이터 리니지 (Data Lineage) - 데이터 흐름 및 변환 추적](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/291_data_lineage_flow_transformation_tracking/)
**다음**: [293. 스토리지와 컴퓨팅의 분리 (Separation of Compute and Storage)](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/293_storage_compute_separation/) →

---
