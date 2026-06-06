---
title: "291. Data Lineage Flow Transformation Tracking"
date: "2026-04-21"
tags:
  - "studynote-enterprise-systems"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [데이터 리니지](/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/)([Data Lineage](/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/))는 원시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 수집되어 변환·집계·적재되는 전 과정의 흐름과 계보를 시각적으로 추적하는 기술로, '[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 족보'다.
> 2. **가치**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 오류 발생 시 영향 범위를 즉시 파악하고, 규제 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)([GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/), [ISMS-P](/studynote/12_it_management/05_security_compliance/171_isms_p/)) 시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 출처를 증명하며, [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 변경 시 다운스트림 영향을 사전 분석할 수 있다.
> 3. **판단 포인트**: 컬럼 수준(Column-level Lineage)까지 추적 가능한 도구를 선택해야 하며, dbt·Airflow·Spark와 통합하여 자동 수집되는 환경이 이상적이다.

## Ⅰ. 개요 및 필요성

[데이터 리니지](/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/)([Data Lineage](/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/))는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 소스 시스템에서 발생해 [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)/[ELT](/studynote/14_data_engineering/01_infrastructure/034_elt/) [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인을 거쳐 [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/), 마트, BI 리포트까지 도달하는 전 여정을 추적하는 [메타데이터 관리](/studynote/16_bigdata/10_governance/203_metadata_management/) 기법이다. 단순히 "이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 어디서 왔다"는 수준을 넘어 "어느 컬럼이 어느 변환 로직을 통해 무슨 값이 됐다"를 컬럼 수준에서 추적한다.

규제 준수 측면에서도 리니지는 필수다. GDPR에서 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 처리 경로 증명, SOX 법(재무 통제)에서 재무 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 출처 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/), [ISMS-P](/studynote/12_it_management/05_security_compliance/171_isms_p/) [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)에서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 이력 보존이 요구된다. 또한 [데이터 파이프라인](/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/) 장애 발생 시 오류가 어느 단계에서 발생했는지, 어떤 다운스트림 리포트가 영향을 받는지 즉시 파악할 수 있다.

📢 **섹션 요약 비유**: 리니지는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 DNA 검사—이 숫자가 어디서, 어떻게 만들어졌는지 증명하는 디지털 족보다.

## Ⅱ. 아키텍처 및 핵심 원리

```
+-------------------------------------------------------------+
|                  데이터 리니지 흐름도                         |
|                                                             |
|  [소스]        [ETL/ELT]          [DW/마트]      [리포트]   |
|                                                             |
|  +-------+    +----------+    +----------+   +----------+  |
|  |  CRM  |---->|transform |---->| SALES_DW |--->| 매출 리포|  |
|  | (주문)|    |  (dbt)   |    |(팩트테이블|   |  (Tableau|  |
|  +-------+    +----------+    +----------+   +----------+  |
|       |                            |                        |
|  +----v--+    +----------+    +---v------+                 |
|  |  ERP  |---->|  Spark   |---->|CUST_MART |                 |
|  |(제품) |    |  Job     |    |(고객 마트|                 |
|  +-------+    +----------+    +----------+                 |
|                                                             |
|  컬럼 수준 리니지 예:                                         |
|  CRM.order_amount -> transform(sum) -> SALES_DW.total_sales  |
|                         |                                   |
|                    +----v--------------------------------+  |
|                    | 리니지 그래프 (방향성 비순환 그래프)  |  |
|                    | DAG (Directed Acyclic Graph)         |  |
|                    +-------------------------------------+  |
+-------------------------------------------------------------+
```

### 리니지 수준 비교

| 수준 | 범위 | 활용 |
|:---|:---|:---|
| 테이블 리니지 | 소스 테이블 -> 대상 테이블 | 영향도 분석, 장애 범위 파악 |
| 컬럼 리니지 | 소스 컬럼 -> 변환 -> 대상 컬럼 | 규제 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/), [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 증명 |
| 실행 리니지 | [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 작업 실행 이력 포함 | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 분석, 디버깅 |
| 비즈니스 리니지 | 비즈니스 용어 기준 추적 | 임원 리포트 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |

📢 **섹션 요약 비유**: 테이블 리니지는 '어느 동네에서 왔냐', 컬럼 리니지는 '어느 집 몇 번 방에서 누가 만들었냐'까지 추적하는 세밀한 수사다.

## Ⅲ. 비교 및 연결

### 리니지 수집 방식 비교

| 방식 | 설명 | 장점 | 단점 |
|:---|:---|:---|:---|
| 수동 입력 | [DBA](/studynote/05_database/01_db_architecture_relational/025_dba_database_administrator/)/엔지니어가 직접 문서화 | [정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/) 높음 | 유지관리 비용 극대화 |
| 코드 파싱 | SQL/[ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 코드 자동 파싱 | 자동화 | 복잡한 동적 SQL 한계 |
| [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 후킹 | 런타임 실행 추적 | 실행 이력 포함 | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 오버헤드 |
| dbt Lineage | dbt 모델 간 의존성 자동 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변환 정확 추적 | dbt 사용 환경 한정 |

📢 **섹션 요약 비유**: 수동 리니지는 손으로 쓰는 일기, 자동 리니지는 GPS 자동 기록—후자가 훨씬 정확하고 편리하다.

## Ⅳ. 실무 적용 및 기술사 판단

**주요 활용 시나리오**:
1. **장애 대응**: 매출 리포트 수치 오류 발생 -> 리니지로 소스까지 역추적 (수시간 -> 수분)
2. <strong>규제 <a href="/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a></strong>: "이 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/)가 어디서 왔고 어디에 쓰였냐" -> 리니지 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 제출
3. <strong><a href="/studynote/02_operating_system/02_process_thread/123_pipe/">파이프</a>라인 변경 영향 분석</strong>: 소스 테이블 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 변경 시 다운스트림 영향 사전 파악
4. <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 품질 근본 원인 분석</strong>: 품질 이상 -> 어느 변환 단계에서 오염됐는지 추적

**도구 선택**:
- Apache Atlas: [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/), [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 생태계
- DataHub: [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/), 다양한 소스 지원
- dbt + Elementary: dbt 환경 리니지 자동화
- OpenLineage: 리니지 표준 스펙 (Marquez 구현체)

📢 **섹션 요약 비유**: 리니지는 [데이터 파이프라인](/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)의 [CCTV](/studynote/09_security/18_iot_ot_physical/933_cctv/)—문제가 생겼을 때 어디서 어떻게 잘못됐는지 영상을 돌려보듯 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)할 수 있다.

## Ⅴ. 기대효과 및 결론

**기대효과**:
- [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 오류 근본 원인 분석 시간 70% 단축
- 규제 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 대응 비용 절감 (리니지 자동 제출)
- [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 변경 시 리그레션 위험 사전 차단
- [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [신뢰도](/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 향상 -> 경영진 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반 의사결정 강화

**한계 및 전제조건**:
- 동적 SQL, 스크립트 기반 ETL의 자동 파싱은 완전하지 않음
- 리니지 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 유지관리를 위한 전담 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어 필요
- 컬럼 수준 리니지는 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 오버헤드가 크므로 중요 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)에만 적용 권고

📢 **섹션 요약 비유**: 모든 도로에 CCTV를 달면 좋겠지만 비용이 문제—중요한 교차로(핵심 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인)에만 먼저 달고 점차 확대하는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 현실적이다.

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [Data Catalog](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) | 상위 시스템 | [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)에 리니지 정보 통합 표시 |
| dbt | 수집 도구 | 변환 모델 간 리니지 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| OpenLineage | 표준 | 리니지 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 표준 스펙 |
| [Data Quality](/studynote/13_cloud_architecture/05_data_engineering/270_data_quality_great_expectations/) | 연관 | 품질 오류 발생 시 리니지로 근본 원인 추적 |
| [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) | 구조 | 리니지는 방향성 비순환 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)로 표현 |

### 📈 관련 키워드 및 발전 흐름도

```
소스 시스템 데이터 생성 (DB, API, 파일)
    |
    v
ETL/ELT 파이프라인 (수집·변환·적재)
    |
    v
테이블 수준 리니지 -> 컬럼 수준 리니지 진화
    |
    v
OpenLineage 표준 + dbt·Airflow 자동 수집
    |
    v
Data Catalog 통합 -> 규제 감사·품질 근본 원인 분석
```

> **키워드**: [Data Lineage](/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/), Column-level Lineage, OpenLineage, [Data Catalog](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/), [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/), [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Provenance

### 👶 어린이를 위한 3줄 비유 설명

1. [데이터 리니지](/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/)는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 '족보'예요—이 숫자가 어느 할아버지(소스)에서 태어나서 어떤 과정을 거쳐 지금의 모습이 됐는지 알려줘요.
2. 마치 우리가 엄마, 아빠, 할머니, 할아버지를 거슬러 올라가는 가족 나무처럼, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 출처를 따라가면 원래 어디서 왔는지 알 수 있어요.
3. 리포트 숫자가 이상하면 족보를 펼쳐서 "아, 이 숫자가 여기서 잘못 계산됐구나!"하고 금방 찾을 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 291 / 482

<- **이전**: [290. 데이터 카탈로그 (Data Catalog) - 통합 메타데이터 저장소](/studynote/07_enterprise_systems/05_data_bi/290_data_catalog_integrated_metadata_repository/)
**다음**: [292. 클라우드 네이티브 DW (Snowflake, BigQuery, Redshift) 아키텍처](/studynote/07_enterprise_systems/05_data_bi/292_cloud_native_dw_snowflake_bigquery_redshift/) ->

---
