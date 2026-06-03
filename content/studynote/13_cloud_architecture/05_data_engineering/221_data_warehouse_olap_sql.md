+++
title = "221. 데이터 웨어하우스 (Data Warehouse / DW)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)([DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/))는 경영 의사결정을 위한 <strong>정제·통합 정형 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>의 중앙 저장소</strong>로, BI 리포트와 [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) 분석에 최적화된 고비용 고성능 플랫폼이다.
> 2. **가치**: ETL을 통해 여러 운영 시스템의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 단일 진실의 공급원(Single Source of Truth)으로 통합하여, <strong>일관된 기업 지표</strong>를 전사에 제공한다.
> 3. **판단 포인트**: 클라우드 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)([Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/)·[BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/)·Redshift)는 스토리지와 컴퓨팅을 분리하여 독립적 스케일링이 가능하며, [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 대비 <strong>운영 비용과 확장성에서 혁신적 우위</strong>를 제공한다.

---

## Ⅰ. 개요 및 필요성

1980년대 Bill Inmon이 제창하고 1990년대 Ralph Kimball이 [차원 모델링](/knowledge-base/studynote/05_database/02_modeling_normalization/118_dimensional_modeling_star_schema/) 방법론으로 체계화한 [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)([Data Warehouse](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/208_data_warehouse_schema_on_write_inmon/), [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/))는, 기업의 다양한 운영 시스템([ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/), [CRM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/), [SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/) 등)에 흩어진 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 <strong>통합·정제·구조화</strong>하여 경영 분석에 제공하는 플랫폼이다.

운영 DB([OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/))는 초당 수천 건의 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 처리에 최적화되어 있어, 대규모 집계·분석 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 실행하면 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)에 영향을 준다. DW는 이를 <strong>물리적으로 분리</strong>하여 분석 전용 환경을 제공한다.

```
[기업 데이터 흐름]
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  ERP 시스템  │  │  CRM 시스템  │  │  SCM 시스템  │
│  (운영 DB)  │  │  (운영 DB)  │  │  (운영 DB)  │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       └────────────────┼────────────────┘
                        ↓  ETL (야간 배치)
               ┌────────────────┐
               │  Data Warehouse │
               │  (통합·정제 데이터)│
               └───────┬────────┘
                       │
            ┌──────────┼──────────┐
            ↓          ↓          ↓
         BI 도구    OLAP 분석   데이터 마트
        (Tableau) (집계쿼리)  (부서별 뷰)
```

📢 **섹션 요약 비유**: DW는 기업의 "중앙 도서관"이다. 각 부서(운영 DB)가 직접 만든 장부([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 밤마다 복사·정리해 중앙 도서관에 보관하고, 경영진이 언제든 전사적 통계를 조회할 수 있도록 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 클라우드 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 아키텍처 (스토리지-컴퓨팅 분리)

```
┌──────────────────────────────────────────────────────┐
│              클라우드 DW 아키텍처                       │
│                                                      │
│  소스 시스템 → ETL/ELT → ┌──────────────────────┐   │
│                          │  공유 스토리지 계층     │   │
│                          │  (S3/GCS/Azure Blob)  │   │
│                          │  컬럼 압축 Parquet     │   │
│                          └──────────┬───────────┘   │
│                                     │               │
│          ┌──────────────────────────┴─────┐         │
│          │     컴퓨팅 클러스터 (독립 스케일)│         │
│          │  ┌────────┐  ┌────────┐         │         │
│          │  │ 가상웨어│  │ 가상웨어│  ...    │         │
│          │  │ 하우스 1│  │ 하우스 2│         │         │
│          │  │(BI팀)  │  │(데이터팀)│         │         │
│          │  └────────┘  └────────┘         │         │
│          └────────────────────────────────┘         │
└──────────────────────────────────────────────────────┘
```

### 핵심 기술 요소

| 구성 요소 | 역할 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/">스타 스키마</a> (<a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/296_star_schema/">Star Schema</a>)</strong> | [팩트 테이블](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/210_fact_dimension_table_snowflake_schema/) + [차원 테이블](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/) 구조, [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 단순화 |
| <strong><a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/335_snowflake_schema/">스노우플레이크 스키마</a></strong> | [차원 테이블](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/) [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/), 저장 효율 ↑ / 조인 복잡도 ↑ |
| **컬럼 지향 저장** | [SELECT](/knowledge-base/studynote/05_database/04_transactions_concurrency/520_select/) 시 필요 열만 읽어 I/O 절감 |
| **MPP (Massively Parallel Processing)** | 수백 노드 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 처리 |
| <strong>구체화 뷰 (Materialized <a href="/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/">View</a>)</strong> | 반복 집계 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 사전 계산 저장 |
| <strong><a href="/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/">파티셔닝</a>/클러스터링</strong> | 날짜·카테고리 기준 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분할로 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 범위 축소 |

📢 **섹션 요약 비유**: 클라우드 DW의 스토리지-컴퓨팅 분리는 창고([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))와 지게차(컴퓨팅)를 분리한 것이다. 바쁜 날(분석 집중)엔 지게차만 늘리고, 한산한 날엔 줄이면 되므로 창고 크기와 무관하게 운영 비용을 최적화할 수 있다.

---

## Ⅲ. 비교 및 연결

### 클라우드 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 3대 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 비교

| 비교 항목 | [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) | Google [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/) | Amazon Redshift |
|:---|:---|:---|:---|
| **아키텍처** | 스토리지-컴퓨팅 완전 분리 | [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) MPP | 클러스터 기반 MPP |
| **가격 모델** | 컴퓨팅 크레딧 + 스토리지 분리 과금 | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 스캔 [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 과금 | 노드 시간 과금 |
| **확장성** | Virtual Warehouse 즉시 확장 | 자동 확장 ([서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)) | 클러스터 리사이즈 필요 |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/202_multi_cloud_hybrid_cloud_governance/">멀티 클라우드</a></strong> | AWS/GCP/Azure 모두 지원 | GCP 전용 | AWS 전용 |
| **ML 통합** | Snowpark (Python/Java 내부 실행) | [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/) ML | Redshift ML (SageMaker 연동) |
| **고유 강점** | [데이터 공유](/knowledge-base/studynote/05_database/06_dw_olap_trends/386_data_clean_room_sharing/)([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Sharing) | [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) 분석 | AWS 에코시스템 통합 |
| **적합 사례** | 멀티클라우드 기업, 외부 [데이터 공유](/knowledge-base/studynote/05_database/06_dw_olap_trends/386_data_clean_room_sharing/) | GCP 기반 스타트업, 분석 우선 | AWS 전용 기업, 기존 Redshift 전환 |

### [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) vs DL([데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)) vs DLH([레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/))

| 특성 | [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) | [Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) | [Lakehouse](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) |
|:---|:---|:---|:---|
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유형 | 정형 | 모든 유형 | 모든 유형 |
| [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) | [Schema-on-Write](/knowledge-base/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/) | [Schema-on-Read](/knowledge-base/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/) | 둘 다 지원 |
| 품질 | 높음 | 낮음~중간 | 높음 |
| 비용 | 고비용 | 저비용 | 중간 |
| ACID [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) | 지원 | 미지원 | 지원 (Delta/Iceberg) |

📢 **섹션 요약 비유**: [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)·DL·DLH는 식당에서 음식 관리하는 세 가지 방식이다. DW는 미리 다 조리해 냉장고에 넣는 것(빠르지만 유연성 없음), DL은 재료를 날것으로 쌓는 것(유연하지만 위생 우려), DLH는 반조리 상태로 정리한 것(두 장점 모두)이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 설계: [Star Schema](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/296_star_schema/) vs [Snowflake Schema](/knowledge-base/studynote/12_it_management/05_security_compliance/313_snowflake_schema/)

```
[Star Schema - 팩트 중심 비정규화]
           ┌──────────────┐
           │  날짜 차원    │
           └──────┬───────┘
                  │
┌──────────┐  ┌───┴──────────────┐  ┌──────────┐
│ 상품 차원 │──│  매출 팩트 테이블  │──│ 고객 차원 │
└──────────┘  │ (주문ID, 날짜ID,  │  └──────────┘
              │  상품ID, 고객ID,  │
              │  금액, 수량)      │
              └──────────────────┘
```

### 실무 적용 지침

| 상황 | 권장 선택 |
|:---|:---|
| 복잡한 집계 분석, 고정 리포트 | [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) ([BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/), [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/)) |
| ML 학습, 탐색적 분석, 비정형 | [Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) (S3 + Glue) |
| ACID + 유연성 + 저비용 모두 필요 | [Lakehouse](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) ([Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/)) |
| AWS 생태계 all-in | Redshift + S3 + Glue |
| GCP 기반 | [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/) + Cloud Storage |
| 멀티클라우드·외부 [데이터 공유](/knowledge-base/studynote/05_database/06_dw_olap_trends/386_data_clean_room_sharing/) | [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) |

**기술사 핵심 판단**: [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 선택 시 스토리지-컴퓨팅 분리 여부와 MPP 아키텍처를 설명하고, 조직의 클라우드 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)(단일 [CSP](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/) vs 멀티)에 따라 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 차별화하여 제안한다.

📢 **섹션 요약 비유**: [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 선택은 식당 종류 선택과 같다. 패스트푸드(Redshift, 이미 AWS 사용 중)는 빠르지만 제약이 있고, 뷔페([BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/), GCP)는 먹는 만큼 내며, 프랜차이즈 체인([Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/))은 어디서나 같은 맛(멀티클라우드)을 제공한다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 정량 기준 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong> | [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) 대비 분석 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~1000배 빠른 응답 |
| <strong>운영 DB <a href="/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/">보호</a></strong> | 분석 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)로 인한 운영 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간섭 제거 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a></strong> | 전사 [KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) 정의 통일, 부서간 숫자 불일치 제거 |
| **의사결정 속도** | 임원 대시보드 T+1일 → T+수분 단위 갱신 |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| **비용** | 클라우드 DW는 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)·스토리지 과금으로 월 수백만 원 발생 가능 |
| <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/">Schema</a> Agility 부족</strong> | [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 변경 시 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 파이프라인 전체 수정 필요 |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/">비정형 데이터</a> 처리 한계</strong> | [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/) 중첩 구조, 이미지 등 처리 불리 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/">지연 시간</a></strong> | [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 배치 주기(야간)로 실시간성 제한 ([ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) 또는 스트리밍 연동 필요) |

📢 **섹션 요약 비유**: DW는 잘 정리된 도서관과 같다. 원하는 책([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 빠르게 찾을 수 있지만, 새 책([스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 변경)을 들이려면 사서([ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 엔지니어)가 전체 목록(파이프라인)을 다시 정리해야 하는 번거로움이 있다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| [Schema-on-Write](/knowledge-base/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/) | DW의 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 기반 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 보장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| [데이터 마트](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/209_data_mart_kimball_star_schema/) | DW의 서브셋, 부서별 특화 저장소 |
| [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) | DW의 주요 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 패턴 (다차원 집계) |
| [Star Schema](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/296_star_schema/) | [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 물리 설계의 핵심 패턴 |
| [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) | [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 적재를 위한 전통적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통합 방식 |
| [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) | 클라우드 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 시대의 새로운 적재 패턴 |
| MPP | [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화 아키텍처 원리 |

### 👶 어린이를 위한 3줄 비유 설명
1. [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)는 회사의 모든 서류를 깨끗이 정리해 보관하는 중앙 서류함이다. 영업팀, 재무팀 서류를 모두 통일된 형식으로 정리해두면, 사장님이 언제든 빠르게 찾아볼 수 있다.

### 📈 관련 키워드 및 발전 흐름도

```text
OLTP (트랜잭션 처리, 행 기반)
    │
    ▼
Data Warehouse: OLAP · Star/Snowflake 스키마
    ├─► BigQuery · Snowflake · Redshift
    └─► Schema-on-Write · 컬럼 지향 저장
    │
    ▼
Lakehouse: DW + Lake 통합 (Delta Lake · Iceberg)
```
2. 마치 도서관 사서처럼, 밤마다([ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 야간 배치) 각 교실(운영 DB)에서 중요한 내용을 가져와 도서관([DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/))에 깔끔하게 분류해 넣는다.
3. [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/)·[Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/)·Redshift는 같은 서류함이지만, 각각 Google·중립·Amazon 건물에 있는 셈이다. 어느 건물에 이미 살고 있느냐에 따라 선택이 달라진다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 220 / 371

← **이전**: [220. 스키마 온 리드 (Schema-on-Read)](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/220_schema_on_read_data_lake/)
**다음**: [222. 스키마 온 라이트 (Schema-on-Write)](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/222_schema_on_write_etl_warehouse/) →

---
