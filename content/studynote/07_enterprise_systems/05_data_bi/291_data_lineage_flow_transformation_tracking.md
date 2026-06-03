---
title: 291. 데이터 리니지 (Data Lineage) - 데이터 흐름 및 변환 추적
date: '2026-04-21'
tags:
- studynote-enterprise-systems
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[214_data_lineage_tracking|데이터 리니지]]([[214_data_lineage_tracking|Data Lineage]])는 원시 [[001_dikw_pyramid|데이터]]가 수집되어 변환·집계·적재되는 전 과정의 흐름과 계보를 시각적으로 추적하는 기술로, '[[001_dikw_pyramid|데이터]]의 족보'다.
> 2. **가치**: [[001_dikw_pyramid|데이터]] 오류 발생 시 영향 범위를 즉시 파악하고, 규제 [[606_auditing_linux_auditd|감사]]([[791_gdpr_eu|GDPR]], [[171_isms_p|ISMS-P]]) 시 [[001_dikw_pyramid|데이터]] 출처를 증명하며, [[123_pipe|파이프]]라인 변경 시 다운스트림 영향을 사전 분석할 수 있다.
> 3. **판단 포인트**: 컬럼 수준(Column-level Lineage)까지 추적 가능한 도구를 선택해야 하며, dbt·Airflow·Spark와 통합하여 자동 수집되는 환경이 이상적이다.

## Ⅰ. 개요 및 필요성

[[214_data_lineage_tracking|데이터 리니지]]([[214_data_lineage_tracking|Data Lineage]])는 [[001_dikw_pyramid|데이터]]가 소스 시스템에서 발생해 [[215_etl_vs_elt_pipeline|ETL]]/[[034_elt|ELT]] [[123_pipe|파이프]]라인을 거쳐 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]], 마트, BI 리포트까지 도달하는 전 여정을 추적하는 [[203_metadata_management|메타데이터 관리]] 기법이다. 단순히 "이 [[001_dikw_pyramid|데이터]]가 어디서 왔다"는 수준을 넘어 "어느 컬럼이 어느 변환 로직을 통해 무슨 값이 됐다"를 컬럼 수준에서 추적한다.

규제 준수 측면에서도 리니지는 필수다. GDPR에서 [[781_personal_information|개인정보]] 처리 경로 증명, SOX 법(재무 통제)에서 재무 [[001_dikw_pyramid|데이터]] 출처 [[606_auditing_linux_auditd|감사]], [[171_isms_p|ISMS-P]] [[303_authentication_authorization_patterns|인증]]에서 [[001_dikw_pyramid|데이터]] 처리 이력 보존이 요구된다. 또한 [[645_data_pipeline_acceleration|데이터 파이프라인]] 장애 발생 시 오류가 어느 단계에서 발생했는지, 어떤 다운스트림 리포트가 영향을 받는지 즉시 파악할 수 있다.

📢 **섹션 요약 비유**: 리니지는 [[001_dikw_pyramid|데이터]]의 DNA 검사—이 숫자가 어디서, 어떻게 만들어졌는지 증명하는 디지털 족보다.

## Ⅱ. 아키텍처 및 핵심 원리

```
┌─────────────────────────────────────────────────────────────┐
│                  데이터 리니지 흐름도                         │
│                                                             │
│  [소스]        [ETL/ELT]          [DW/마트]      [리포트]   │
│                                                             │
│  ┌───────┐    ┌──────────┐    ┌──────────┐   ┌──────────┐  │
│  │  CRM  │───▶│transform │───▶│ SALES_DW │──▶│ 매출 리포│  │
│  │ (주문)│    │  (dbt)   │    │(팩트테이블│   │  (Tableau│  │
│  └───────┘    └──────────┘    └──────────┘   └──────────┘  │
│       │                            │                        │
│  ┌────▼──┐    ┌──────────┐    ┌───▼──────┐                 │
│  │  ERP  │───▶│  Spark   │───▶│CUST_MART │                 │
│  │(제품) │    │  Job     │    │(고객 마트│                 │
│  └───────┘    └──────────┘    └──────────┘                 │
│                                                             │
│  컬럼 수준 리니지 예:                                         │
│  CRM.order_amount → transform(sum) → SALES_DW.total_sales  │
│                         │                                   │
│                    ┌────▼────────────────────────────────┐  │
│                    │ 리니지 그래프 (방향성 비순환 그래프)  │  │
│                    │ DAG (Directed Acyclic Graph)         │  │
│                    └─────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 리니지 수준 비교

| 수준 | 범위 | 활용 |
|:---|:---|:---|
| 테이블 리니지 | 소스 테이블 → 대상 테이블 | 영향도 분석, 장애 범위 파악 |
| 컬럼 리니지 | 소스 컬럼 → 변환 → 대상 컬럼 | 규제 [[606_auditing_linux_auditd|감사]], [[001_dikw_pyramid|데이터]] [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 증명 |
| 실행 리니지 | [[215_etl_vs_elt_pipeline|ETL]] 작업 실행 이력 포함 | [[282_performance_tactics|성능]] 분석, 디버깅 |
| 비즈니스 리니지 | 비즈니스 용어 기준 추적 | 임원 리포트 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] [[396_validation|확인]] |

📢 **섹션 요약 비유**: 테이블 리니지는 '어느 동네에서 왔냐', 컬럼 리니지는 '어느 집 몇 번 방에서 누가 만들었냐'까지 추적하는 세밀한 수사다.

## Ⅲ. 비교 및 연결

### 리니지 수집 방식 비교

| 방식 | 설명 | 장점 | 단점 |
|:---|:---|:---|:---|
| 수동 입력 | [[025_dba_database_administrator|DBA]]/엔지니어가 직접 문서화 | [[002_bigdata_5v|정확성]] 높음 | 유지관리 비용 극대화 |
| 코드 파싱 | SQL/[[215_etl_vs_elt_pipeline|ETL]] 코드 자동 파싱 | 자동화 | 복잡한 동적 SQL 한계 |
| [[014_api_posix|API]] 후킹 | 런타임 실행 추적 | 실행 이력 포함 | [[282_performance_tactics|성능]] 오버헤드 |
| dbt Lineage | dbt 모델 간 의존성 자동 | [[001_dikw_pyramid|데이터]] 변환 정확 추적 | dbt 사용 환경 한정 |

📢 **섹션 요약 비유**: 수동 리니지는 손으로 쓰는 일기, 자동 리니지는 GPS 자동 기록—후자가 훨씬 정확하고 편리하다.

## Ⅳ. 실무 적용 및 기술사 판단

**주요 활용 시나리오**:
1. **장애 대응**: 매출 리포트 수치 오류 발생 → 리니지로 소스까지 역추적 (수시간 → 수분)
2. **규제 [[606_auditing_linux_auditd|감사]]**: "이 [[781_personal_information|개인정보]]가 어디서 왔고 어디에 쓰였냐" → 리니지 [[070_graph_datastructure|그래프]] 제출
3. **[[123_pipe|파이프]]라인 변경 영향 분석**: 소스 테이블 [[005_schema|스키마]] 변경 시 다운스트림 영향 사전 파악
4. **[[001_dikw_pyramid|데이터]] 품질 근본 원인 분석**: 품질 이상 → 어느 변환 단계에서 오염됐는지 추적

**도구 선택**:
- Apache Atlas: [[191_oss_license_compliance|오픈소스]], [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 생태계
- DataHub: [[191_oss_license_compliance|오픈소스]], 다양한 소스 지원
- dbt + Elementary: dbt 환경 리니지 자동화
- OpenLineage: 리니지 표준 스펙 (Marquez 구현체)

📢 **섹션 요약 비유**: 리니지는 [[645_data_pipeline_acceleration|데이터 파이프라인]]의 [[933_cctv|CCTV]]—문제가 생겼을 때 어디서 어떻게 잘못됐는지 영상을 돌려보듯 [[396_validation|확인]]할 수 있다.

## Ⅴ. 기대효과 및 결론

**기대효과**:
- [[001_dikw_pyramid|데이터]] 오류 근본 원인 분석 시간 70% 단축
- 규제 [[606_auditing_linux_auditd|감사]] 대응 비용 절감 (리니지 자동 제출)
- [[123_pipe|파이프]]라인 변경 시 리그레션 위험 사전 차단
- [[001_dikw_pyramid|데이터]] [[085_confidence_association_rule_conditional_probability|신뢰도]] 향상 → 경영진 [[001_dikw_pyramid|데이터]] 기반 의사결정 강화

**한계 및 전제조건**:
- 동적 SQL, 스크립트 기반 ETL의 자동 파싱은 완전하지 않음
- 리니지 [[070_graph_datastructure|그래프]] 유지관리를 위한 전담 [[001_dikw_pyramid|데이터]] 엔지니어 필요
- 컬럼 수준 리니지는 [[282_performance_tactics|성능]] 오버헤드가 크므로 중요 [[064_relation_domain|도메인]]에만 적용 권고

📢 **섹션 요약 비유**: 모든 도로에 CCTV를 달면 좋겠지만 비용이 문제—중요한 교차로(핵심 [[123_pipe|파이프]]라인)에만 먼저 달고 점차 확대하는 [[268_strategy_pattern|전략]]이 현실적이다.

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| [[213_data_catalog_metadata|Data Catalog]] | 상위 시스템 | [[394_catalog_metadata|카탈로그]]에 리니지 정보 통합 표시 |
| dbt | 수집 도구 | 변환 모델 간 리니지 자동 [[087_process_state_transition|생성]] |
| OpenLineage | 표준 | 리니지 [[012_metadata|메타데이터]] 표준 스펙 |
| [[270_data_quality_great_expectations|Data Quality]] | 연관 | 품질 오류 발생 시 리니지로 근본 원인 추적 |
| [[401_bayesian_network_dag_causality|DAG]] | 구조 | 리니지는 방향성 비순환 [[070_graph_datastructure|그래프]]로 표현 |

### 📈 관련 키워드 및 발전 흐름도

```
소스 시스템 데이터 생성 (DB, API, 파일)
    │
    ▼
ETL/ELT 파이프라인 (수집·변환·적재)
    │
    ▼
테이블 수준 리니지 → 컬럼 수준 리니지 진화
    │
    ▼
OpenLineage 표준 + dbt·Airflow 자동 수집
    │
    ▼
Data Catalog 통합 → 규제 감사·품질 근본 원인 분석
```

> **키워드**: [[214_data_lineage_tracking|Data Lineage]], Column-level Lineage, OpenLineage, [[213_data_catalog_metadata|Data Catalog]], [[401_bayesian_network_dag_causality|DAG]], [[001_dikw_pyramid|Data]] Provenance

### 👶 어린이를 위한 3줄 비유 설명

1. [[214_data_lineage_tracking|데이터 리니지]]는 [[001_dikw_pyramid|데이터]]의 '족보'예요—이 숫자가 어느 할아버지(소스)에서 태어나서 어떤 과정을 거쳐 지금의 모습이 됐는지 알려줘요.
2. 마치 우리가 엄마, 아빠, 할머니, 할아버지를 거슬러 올라가는 가족 나무처럼, [[001_dikw_pyramid|데이터]]도 출처를 따라가면 원래 어디서 왔는지 알 수 있어요.
3. 리포트 숫자가 이상하면 족보를 펼쳐서 "아, 이 숫자가 여기서 잘못 계산됐구나!"하고 금방 찾을 수 있어요!
