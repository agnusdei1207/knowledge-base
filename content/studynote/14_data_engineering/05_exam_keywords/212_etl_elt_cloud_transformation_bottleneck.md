+++
title = "212. ETL vs ELT (Extract-Transform-Load vs Extract-Load-Transform) 클라우드 전이"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)(Extract, Transform, Load)은 중간 변환 서버에서 먼저 정제 후 DW에 적재하지만, [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/)(Extract, Load, Transform)는 원본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 클라우드 DW에 먼저 적재 후 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 내부의 막대한 컴퓨팅 파워로 변환한다.
> 2. **가치**: 클라우드 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)([Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/), [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/), Redshift)의 분리 스토리지-컴퓨팅 구조 덕분에 ELT는 변환 병목([Bottleneck](/knowledge-base/studynote/02_operating_system/10_security/617_io_bottleneck/))이 사라지고, dbt([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Build Tool)로 SQL 기반 변환 파이프라인을 코드로 관리할 수 있다.
> 3. **판단 포인트**: [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)·레거시 환경은 ETL이 여전히 적합하나, [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/)·비정형 대용량 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에는 ELT가 압도적으로 유리하다 — 변환 로직의 위치가 아키텍처 선택의 핵심이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 ETL의 탄생과 한계

[ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)(Extract, Transform, Load)은 1970~80년대 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)([On-Premise](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)) [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 시대에 탄생했다. 소스 시스템에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 추출(Extract)하고, 중간 서버에서 정제·변환(Transform)한 뒤, 최종 DW에 적재(Load)하는 순서다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">소스 DB</div><div class="kb-diagram-cell">►</div><div class="kb-diagram-cell">ETL 서버 (변환)</div><div class="kb-diagram-cell">►</div><div class="kb-diagram-cell">DW/목적지</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ERP/CRM</div><div class="kb-diagram-cell">데이터 정제</div><div class="kb-diagram-cell">Teradata</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">파일/API</div><div class="kb-diagram-cell">타입 변환</div><div class="kb-diagram-cell">Oracle DW</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">비즈니스 룰 적용</div></div>
<div class="kb-diagram-note">↑ 병목 지점 (Bottleneck)</div>
<div class="kb-diagram-note">처리 용량 = ETL 서버 CPU/메모리</div>
</div>
</div>



**ETL의 병목 문제**: 모든 변환이 중간 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 서버를 통과하므로, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 볼륨이 늘어날수록 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 서버가 [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)([SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/), Single Point of Failure)이자 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목이 된다.

### 1.2 클라우드가 바꾼 패러다임

클라우드 DW는 스토리지와 컴퓨팅을 분리하여, 컴퓨팅 노드를 탄력적으로 확장한다. 이 환경에서는 변환을 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 내부에서 수행하는 것이 훨씬 효율적이다.

📢 **섹션 요약 비유**: ETL은 공장 밖 작업장에서 철을 깎아 완제품으로 만들어 공장에 들여놓는 방식이고, ELT는 철을 통째로 공장에 들여놓고 공장 안의 최신 자동화 설비로 가공하는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [ETL vs ELT](/knowledge-base/studynote/12_it_management/05_security_compliance/317_etl_vs_elt/) 아키텍처 비교

| 항목 | [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) (Extract-Transform-Load) | [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) (Extract-Load-Transform) |
|:---|:---|:---|
| **변환 위치** | 중간 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 서버 (외부) | 목적지 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 내부 |
| <strong>적재 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong> | 정제된 최종 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 원시([Raw](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/)) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/">스케일링</a></strong> | [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 서버 수직/수평 확장 필요 | [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 컴퓨팅 탄력적 확장 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/">지연 시간</a></strong> | 변환 완료 후 적재 → [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 큼 | 즉시 적재 → 변환은 별도 |
| **원본 보존** | 변환 후 원본 불일치 발생 가능 | [Raw](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 항상 보존 |
| **적합 환경** | [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/), 레거시 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) | 클라우드 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) ([Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/), [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/)) |
| **대표 도구** | Informatica, Talend, SSIS | dbt, [Spark SQL](/knowledge-base/studynote/16_bigdata/03_spark/056_spark_sql/), [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/) TRANSFORM |

### 2.2 [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) 상세 흐름



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Extract</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">소스 시스템</div><div class="kb-diagram-cell">►</div><div class="kb-diagram-cell">클라우드 DW</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">MySQL/API</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">S3/Kafka</div><div class="kb-diagram-cell">Load</div><div class="kb-diagram-cell">Transform</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">►</div><div class="kb-diagram-cell">RAW 레이어</div><div class="kb-diagram-cell">►</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">STAGING 레이어</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">dbt/SQL</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">MART 레이어</div></div>
</div>
</div>



### 2.3 dbt ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Build Tool)를 활용한 [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/)

dbt([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Build Tool)는 ELT의 Transform 단계를 SQL 파일과 YAML 설정으로 코드화하는 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 프레임워크다.

```yaml
# dbt 모델 예시: models/staging/stg_orders.sql
SELECT
  order_id,
  customer_id,
  CAST(order_date AS DATE)   AS order_date,
  amount / 100.0             AS amount_usd  -- 센트→달러 변환
FROM {{ source('raw', 'orders') }}
WHERE status != 'cancelled'
```

**dbt 장점**:
- SQL 기반이라 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석가도 변환 로직 작성 가능
- 계보(Lineage) 자동 추적 — 어떤 테이블이 어디서 왔는지 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)
- 테스트(not_null, unique, accepted_values) 내장
- Git 기반 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리로 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD([Continuous Integration](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/)/[Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/)) 파이프라인 통합

### 2.4 Apache Spark를 활용한 대규모 [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/)

대용량 비정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 경우 Spark가 ELT의 Transform 엔진으로 동작한다.

```python
# Spark ELT Transform 예시
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date

spark = SparkSession.builder.appName("ELT-Transform").getOrCreate()

# RAW 데이터 로드 (Load 단계에서 이미 S3에 저장된 데이터)
raw_df = spark.read.parquet("s3://data-lake/raw/orders/")

# Transform: 타입 변환, 필터, 집계
transformed_df = (
    raw_df
    .withColumn("order_date", to_date(col("order_date_str")))
    .filter(col("amount") > 0)
    .groupBy("customer_id", "order_date")
    .agg({"amount": "sum"})
)

# 결과를 DW 또는 데이터 마트(Data Mart)에 저장
transformed_df.write.mode("overwrite").parquet("s3://data-lake/mart/daily_orders/")
```

📢 **섹션 요약 비유**: dbt는 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 안에서 일하는 '정리 정돈 전문가'다 — 이미 창고에 들어온 물건들을 SQL이라는 도구로 분류하고, 어디서 왔는지 꼬리표까지 붙여준다.

---

## Ⅲ. 비교 및 연결

### 3.1 변환 병목 위치 이동의 의미

ETL에서 ELT로의 전환은 단순한 순서 변경이 아니라 <strong>책임의 이동</strong>이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">ETL 시대:</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">소스 ──►</div><div class="kb-diagram-node">ETL 서버가 모든 책임</div><div class="kb-diagram-note">──► DW</div></div>
<div class="kb-diagram-note">↑ 병목, 단일 실패점</div>
<div class="kb-diagram-note">ELT 시대:</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">소스 ──► DW RAW ──►</div><div class="kb-diagram-node">DW 컴퓨팅이 책임</div><div class="kb-diagram-note">──► DW MART</div></div>
<div class="kb-diagram-note">↑ 탄력적 확장, 원본 보존</div>
</div>
</div>



### 3.2 [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)([Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/))와의 연계

현대 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 아키텍처에서 ELT는 [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)([Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/)) 패턴과 결합된다. 각 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀이 자신의 [RAW](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 DW에 적재(Load)하고, [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)별 dbt 프로젝트로 변환(Transform)하여 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 프로덕트([Data Product](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/))를 생성한다.

### 3.3 [Reverse ETL](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/278_reverse_etl_operational_analytics/) (역방향 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/))

최근에는 DW에서 분석한 결과를 운영 시스템([CRM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/), 이메일 마케팅)으로 다시 내보내는 <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/278_reverse_etl_operational_analytics/">Reverse ETL</a></strong> 패턴도 주목받는다. Census, Hightouch 같은 도구가 이를 담당한다.

📢 **섹션 요약 비유**: ELT에서 dbt는 DW라는 거대 주방의 레시피 북이다 — 재료([Raw](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))는 이미 주방에 있고, 레시피(SQL 모델)만 바꾸면 언제든 새 요리([데이터 마트](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/209_data_mart_kimball_star_schema/))를 만들 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 [ETL vs ELT](/knowledge-base/studynote/12_it_management/05_security_compliance/317_etl_vs_elt/) 선택 기준



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">데이터가 민감하고 정제 전 적재가 불가한가?</div>
<div class="kb-diagram-note">↓ YES</div>
<div class="kb-diagram-note">ETL (금융·의료 컴플라이언스 환경)</div>
<div class="kb-diagram-note">↓ NO</div>
<div class="kb-diagram-note">클라우드 DW를 사용하고 대용량인가?</div>
<div class="kb-diagram-note">↓ YES</div>
<div class="kb-diagram-note">ELT + dbt (BigQuery, Snowflake, Redshift)</div>
<div class="kb-diagram-note">↓ NO (온프레미스, 소규모)</div>
<div class="kb-diagram-note">ETL (Informatica, Talend, SSIS)</div>
</div>
</div>



### 4.2 [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) 적용 시 주의사항

| 항목 | 주의점 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 품질</strong> | [RAW](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) 적재 후 변환 실패 시 오염 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 DW에 체류 |
| **비용 관리** | 클라우드 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 비용 — 비효율 SQL이 과금 폭탄 |
| **보안** | 민감 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 [RAW](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) 레이어에 노출 → 컬럼 마스킹 필수 |
| **거버넌스** | dbt Lineage + [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)([Data Catalog](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/))로 계보 관리 |

📢 **섹션 요약 비유**: ELT는 반죽([raw](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 그대로 냉장고에 넣고 나중에 요리하는 방식이라 편리하지만, 냉장고 안이 지저분해지지 않도록 정리 규칙(거버넌스)이 필요하다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) 전환 효과

| 효과 | 정량적 지표 |
|:---|:---|
| **파이프라인 구축 속도** | 전통 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 대비 개발 기간 40~60% 단축 |
| **유연성** | 비즈니스 룰 변경 시 dbt 모델만 수정 (재ETL 불필요) |
| **비용** | [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 전용 서버 운영 비용 제거 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/">신뢰성</a></strong> | [RAW](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) 보존으로 어떤 시점으로든 재처리 가능 |

### 5.2 결론 — 기술사 작성 포인트

기술사 답안에서는 <strong>"변환 병목의 위치가 아키텍처 선택을 결정한다"</strong>는 관점에서 서술해야 한다. ETL은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질과 컴플라이언스 우선, ELT는 속도와 유연성 우선의 설계 철학이며, 현대 클라우드 환경에서는 [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) + dbt + [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)의 조합이 표준 스택으로 자리잡고 있다.

📢 **섹션 요약 비유**: ETL에서 ELT로의 전환은 '문 앞에서 신발 청소 후 입장'에서 '신발 신고 입장 후 안에서 청소'로 바뀐 것이다 — 입장은 빠르지만 안을 깨끗하게 유지하는 규칙이 더 중요해졌다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 변환 도구 | Informatica / Talend / SSIS | 전통 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 도구 |
| [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) 변환 도구 | dbt ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Build Tool) | SQL 기반 [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) Transform 프레임워크 |
| [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) 엔진 | [Apache Spark](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/) | 대규모 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 변환 처리 |
| 클라우드 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) | [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) / [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/) / Redshift | [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) 변환을 내부에서 수행 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계층 | [RAW](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) → STAGING → MART | ELT의 3단계 레이어 구조 |
| 역방향 | [Reverse ETL](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/278_reverse_etl_operational_analytics/) | [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) → 운영 시스템으로 역방향 이동 |

### 👶 어린이를 위한 3줄 비유 설명

1. ETL은 도서관에 책을 넣기 전에 밖에서 먼지를 털고 분류해서 넣는 방식이야.

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">ETL: Extract → Transform → Load (DW 외부 변환)</div>
<div class="kb-diagram-note">클라우드 컴퓨팅 저렴화</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">ELT: Extract → Load → Transform (DW 내부 변환)</div>
<div class="kb-diagram-tree-item" style="--depth:2">dbt: SQL 기반 변환 자동화</div>
<div class="kb-diagram-tree-item" style="--depth:2">BigQuery · Snowflake 컴퓨팅 활용</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">실시간 ETL/ELT: Kafka + Flink 스트리밍 변환</div>
</div>
</div>


2. ELT는 책을 일단 도서관에 다 가져다 넣고, 도서관 안에 있는 빠른 기계로 분류하는 방식이야.
3. 어느 게 더 좋냐고? 도서관(클라우드)이 크고 빠르다면 ELT가 훨씬 편리해 — 책을 기다리게 하지 않아도 되거든!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 212 / 258

← **이전**: [211. OLAP (Online Analytical Processing) 드릴다운·롤업·서로게이트 키](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/211_olap_drill_down_roll_up_surrogate_key/)
**다음**: [213. 데이터 레이크하우스 (Data Lakehouse) Delta Lake 파케이 ACID](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/213_data_lakehouse_delta_lake_parquet_acid/) →

---
