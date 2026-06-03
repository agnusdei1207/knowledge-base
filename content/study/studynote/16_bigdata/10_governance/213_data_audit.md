+++
weight = 213
title = "23. 데이터 감사 (Data Audit)"
date = "2026-04-29"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[001_dikw_pyramid|데이터]] [[606_auditing_linux_auditd|감사]]([[001_dikw_pyramid|Data]] [[363_audit|Audit]])는 조직의 [[001_dikw_pyramid|데이터]] 자산이 [[002_bigdata_5v|정확성]](Accuracy)·완전성(Completeness)·[[194_consistency_database_integrity|일관성]]([[194_consistency_database_integrity|Consistency]])·적시성(Timeliness)·규정 준수([[058_it_compliance_sox_basel_gdpr_isms|Compliance]]) 기준을 충족하는지 체계적으로 [[395_verification_process_review|검증]]하고 기록하는 [[052_data_governance_framework|데이터 거버넌스]]([[052_data_governance_framework|Data Governance]]) 활동이다.
> 2. **가치**: 빅데이터 환경에서 [[645_data_pipeline_acceleration|데이터 파이프라인]]이 복잡해질수록 [[001_dikw_pyramid|데이터]] 품질 저하와 무단 접근이 탐지되지 않은 채 누적되며, [[001_dikw_pyramid|데이터]] [[606_auditing_linux_auditd|감사]]는 이 위험을 선제적으로 탐지하고 [[791_gdpr_eu|GDPR]]·[[783_pipa_korea|개인정보보호법]] 같은 규제 준수 증거를 제공한다.
> 3. **판단 포인트**: [[001_dikw_pyramid|데이터]] [[606_auditing_linux_auditd|감사]]의 핵심은 "누가(Who), 언제(When), 어떤 [[001_dikw_pyramid|데이터]]를(What), 어떻게 변경했는가(How)"를 추적하는 [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]]([[363_audit|Audit]] Log)와 [[001_dikw_pyramid|데이터]] 계보([[214_data_lineage_tracking|Data Lineage]])이며, 이 두 가지가 없으면 [[001_dikw_pyramid|데이터]] 품질 사고 발생 시 원인 추적과 법적 책임 소재 [[396_validation|확인]]이 불가능하다.

---

## Ⅰ. 개요 및 필요성

[[001_dikw_pyramid|데이터]] [[606_auditing_linux_auditd|감사]]([[001_dikw_pyramid|Data]] [[363_audit|Audit]])는 [[001_dikw_pyramid|데이터]]의 [[087_process_state_transition|생성]]·변환·이동·삭제 전 과정을 추적하고 [[395_verification_process_review|검증]]하여, [[001_dikw_pyramid|데이터]]가 의도한 품질 기준과 규정 요건을 지속적으로 만족하는지 [[396_validation|확인]]하는 체계적인 [[395_verification_process_review|검증]] 프로세스다.

[[001_dikw_pyramid|데이터]] [[606_auditing_linux_auditd|감사]]가 없다면 금융 보고서에 사용된 집계 수치가 잘못 계산되어도 원인을 추적할 수 없고, [[781_personal_information|개인정보]]가 무단으로 접근·수출되어도 사후 파악이 어렵다. 특히 수백 개의 [[215_etl_vs_elt_pipeline|ETL]] [[123_pipe|파이프]]라인이 얽혀 있는 [[210_data_lakehouse_delta_lake|데이터 레이크하우스]] 환경에서 [[001_dikw_pyramid|데이터]] [[606_auditing_linux_auditd|감사]]는 더 이상 선택이 아닌 필수다.

```text
┌──────────────────────────────────────────────────────────────┐
│            데이터 감사 4대 검증 영역                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. 데이터 품질 감사 (Data Quality Audit)                     │
│     ├─ 정확성: 값이 현실을 올바르게 반영하는가?                 │
│     ├─ 완전성: 필수 필드가 누락 없이 채워져 있는가?              │
│     ├─ 일관성: 시스템 간 동일 데이터가 모순되지 않는가?          │
│     └─ 적시성: 데이터가 지정 시간 내에 갱신되었는가?             │
│                                                              │
│  2. 접근 감사 (Access Audit)                                  │
│     └─ 누가 언제 어떤 데이터에 접근·변경했는가?                 │
│                                                              │
│  3. 규정 준수 감사 (Compliance Audit)                         │
│     └─ GDPR, 개인정보보호법, 금융감독규정 준수 여부              │
│                                                              │
│  4. 계보 감사 (Lineage Audit)                                 │
│     └─ 데이터의 출처→변환→목적지 흐름 추적                     │
└──────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]] [[606_auditing_linux_auditd|감사]]는 식품 이력 추적 시스템과 같다. 식재료(원시 [[001_dikw_pyramid|데이터]])가 농장(소스)에서 공장([[215_etl_vs_elt_pipeline|ETL]]), 식탁(보고서)까지 모든 과정이 기록되어 문제 발생 시 즉시 원산지를 추적할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]]([[363_audit|Audit]] Log) 구조

| 필드 | 설명 | 예시 |
|:---|:---|:---|
| **timestamp** | 이벤트 발생 시각 (UTC) | 2026-04-29T09:15:32Z |
| **user_id** | [[001_dikw_pyramid|데이터]] 접근/변경 주체 | user123 / svc_etl_job |
| **action** | 수행 작업 유형 | READ, INSERT, UPDATE, DELETE |
| **resource** | 접근한 테이블/[[501_file_definition_logical_record|파일]] 경로 | db.orders, s3://bucket/path |
| **old_value / new_value** | 변경 전후 값 | {amount: 100} → {amount: 200} |
| **ip_address** | 접근 출처 IP | [[489_raid_10_hybrid|10]].0.1.55 |
| **status** | 성공/실패 | SUCCESS / DENIED |

### [[001_dikw_pyramid|데이터]] 계보([[214_data_lineage_tracking|Data Lineage]]) 아키텍처

```text
┌──────────────────────────────────────────────────────────┐
│              데이터 계보 추적 흐름                          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  [원시 데이터 소스]                                        │
│  CRM DB (고객 정보) ──→ ETL Job (정제) ──→ DW (orders 테이블)│
│                                          │               │
│                                          ▼               │
│                                     BI 보고서 (매출 집계)  │
│                                                          │
│  계보 도구가 기록:                                         │
│  "매출_집계 ← orders ← ETL_job_2026 ← CRM_DB"            │
│                                                          │
│  감사 질문: "이 매출 수치는 어디서 왔나?"                   │
│  → 계보 추적으로 CRM 원본까지 역추적 가능                    │
└──────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]] 계보는 스파게티 한 가닥이 냄비 속 어느 면에서 왔는지 추적하는 것이다. 엉켜있는 수백 개의 [[123_pipe|파이프]]라인 중에서 특정 숫자의 출처를 끝까지 따라가면 최초 소스를 찾을 수 있다.

---

## Ⅲ. 비교 및 연결

| 도구/기술 | 역할 | 특징 |
|:---|:---|:---|
| **Apache Atlas** | [[012_metadata|메타데이터]] + 계보 관리 | [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] [[031_에코_반향|에코]]시스템 통합 |
| **OpenLineage** | [[191_oss_license_compliance|오픈소스]] 계보 표준 | Airflow, Spark, dbt 연동 |
| **Great Expectations** | [[001_dikw_pyramid|데이터]] 품질 [[395_verification_process_review|검증]] 자동화 | Python 기반, [[090_configuration_item|CI]]/CD 통합 |
| **[[147_delta_lake|Delta Lake]] ACID** | [[191_transaction_concept_states|트랜잭션]] 기반 변경 이력 | DESCRIBE HISTORY [[298_qkv_attention|쿼리]] |
| **[[150_unity_catalog|Unity Catalog]] ([[074_photon_engine|Databricks]])** | 세분화 접근 제어 + [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]] | [[531_cloud_native_architecture|클라우드 네이티브]] 거버넌스 |

[[001_dikw_pyramid|데이터]] [[606_auditing_linux_auditd|감사]]는 [[213_data_catalog_metadata|데이터 카탈로그]]([[213_data_catalog_metadata|Data Catalog]])와 결합하여 [[012_metadata|메타데이터]], 계보, 품질, 접근 이력을 단일 플랫폼에서 통합 관리하는 방향으로 진화하고 있다.

- **📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]] [[606_auditing_linux_auditd|감사]] 도구는 조직의 [[001_dikw_pyramid|데이터]] [[068_csi|CSI]]([[296_crime_attack|Crime]] Scene Investigation) 팀이다. 범죄([[001_dikw_pyramid|데이터]] 품질 사고)가 발생하면 [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]]와 계보를 통해 현장 증거를 수집하고 범인(오류 원인)을 정확히 찾아낸다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: 금융 규제 보고서 [[001_dikw_pyramid|데이터]] [[606_auditing_linux_auditd|감사]]
금융 기관이 [[889_fss_cyber_supervision|금융감독원]] 제출용 보고서의 [[001_dikw_pyramid|데이터]] [[002_bigdata_5v|정확성]] [[606_auditing_linux_auditd|감사]]를 수행한다.

1. **품질 [[395_verification_process_review|검증]]**: Great Expectations로 잔액 필드 NOT NULL, 금액 > 0, 날짜 형식 ISO 8601 자동 [[395_verification_process_review|검증]].
2. **계보 추적**: OpenLineage로 "월별 거래 합산" 보고서 → [[215_etl_vs_elt_pipeline|ETL]] Job → 원천 [[191_transaction_concept_states|트랜잭션]] DB 역추적.
3. **접근 [[606_auditing_linux_auditd|감사]]**: [[150_unity_catalog|Unity Catalog]] [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]]에서 보고서 테이블에 접근한 모든 [[275_iam_role_for_service_accounts|서비스 계정]] [[396_validation|확인]].
4. **규정 준수**: [[781_personal_information|개인정보]](주민번호, 계좌번호) 접근 이벤트를 별도 [[606_auditing_linux_auditd|감사]] 테이블에 격리 저장, 5년 보관.
5. **보고서 제출**: [[606_auditing_linux_auditd|감사]] 보고서 + [[001_dikw_pyramid|데이터]] 계보 다이어그램을 감독 기관에 증적 제출.

### [[435_checklist_based_testing|체크리스트]]
- [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]]는 변경 불가([[298_immutable|Immutable]]) 스토리지(S3 객체 잠금, Glacier)에 저장.
- [[001_dikw_pyramid|데이터]] 품질 [[395_verification_process_review|검증]]을 [[215_etl_vs_elt_pipeline|ETL]] [[123_pipe|파이프]]라인의 Gate 조건으로 삽입 (품질 실패 시 [[123_pipe|파이프]]라인 중단).
- 계보 도구와 [[213_data_catalog_metadata|데이터 카탈로그]]를 연동하여 비즈니스 용어(Business Glossary) 기반 계보 제공.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]]를 일반 운영 DB 테이블에 저장하는 [[128_water_scrum_fall_anti_pattern|안티패턴]]. [[002_database_definition|데이터베이스]] 관리자([[025_dba_database_administrator|DBA]])가 [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]] 자체를 수정·삭제할 수 있어 [[606_auditing_linux_auditd|감사]]의 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]이 훼손된다. [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]]는 반드시 접근 권한이 분리된 불변 스토리지에 저장해야 한다.

- **📢 섹션 요약 비유**: [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]]를 일반 DB에 저장하는 건, 은행 [[933_cctv|CCTV]] 녹화 [[501_file_definition_logical_record|파일]]을 은행 직원이 접근 가능한 일반 서버에 두는 것과 같다. 내부 범행 시 증거가 사라질 수 있다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 | 수치 |
|:---|:---|:---|
| **규정 준수 입증** | [[791_gdpr_eu|GDPR]]/[[783_pipa_korea|개인정보보호법]] [[606_auditing_linux_auditd|감사]] 증적 | 과징금 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] 제거 |
| **[[001_dikw_pyramid|데이터]] [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]** | 품질 [[395_verification_process_review|검증]] 자동화로 오보고 방지 | [[001_dikw_pyramid|데이터]] 오류 80% 조기 탐지 |
| **[[009_incident_response|사고 대응]]력** | 계보 기반 원인 추적 속도 향상 | [[451_mttr|MTTR]] 70% 단축 |

[[001_dikw_pyramid|데이터]] [[606_auditing_linux_auditd|감사]]는 [[190_ai_llm_requirements_specification|AI]]/ML 모델의 학습 [[001_dikw_pyramid|데이터]] [[606_auditing_linux_auditd|감사]]([[051_ai_bigdata_project_audit|AI Audit]])로 확장되어, 모델 결과의 공정성·편향 여부를 [[395_verification_process_review|검증]]하고 규제 기관에 설명하는 새로운 [[606_auditing_linux_auditd|감사]] 영역으로 발전하고 있다. [[211_data_mesh_domain_ownership|데이터 메시]]([[320_data_mesh|Data Mesh]]) 아키텍처에서는 [[064_relation_domain|도메인]]별 [[001_dikw_pyramid|데이터]] 오너([[200_data_owner|Data Owner]])가 각자의 [[001_dikw_pyramid|데이터]] 품질 SLA를 [[606_auditing_linux_auditd|감사]]하는 [[136_variance|분산]] [[606_auditing_linux_auditd|감사]] 체계가 표준이 되고 있다.

- **📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]] [[606_auditing_linux_auditd|감사]]는 조직의 [[001_dikw_pyramid|데이터]] 건강검진이다. 매년(또는 실시간으로) [[001_dikw_pyramid|데이터]]의 혈압(품질)·콜레스테롤(보안 이벤트)·MRI(계보)를 검사하여 질병([[001_dikw_pyramid|데이터]] 품질 사고·[[781_personal_information|개인정보]] 침해)을 조기에 발견하고 치료한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[052_data_governance_framework|데이터 거버넌스]]** | [[001_dikw_pyramid|데이터]] [[606_auditing_linux_auditd|감사]]가 실행 수단이 되는 상위 체계 |
| **[[001_dikw_pyramid|데이터]] 계보 ([[214_data_lineage_tracking|Data Lineage]])** | [[001_dikw_pyramid|데이터]]의 출처·변환·목적지 추적; [[606_auditing_linux_auditd|감사]]의 핵심 도구 |
| **[[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]] ([[363_audit|Audit]] Log)** | 접근·변경 이벤트 기록; 불변 스토리지에 보관 |
| **Great Expectations** | [[123_pipe|파이프]]라인 내 [[001_dikw_pyramid|데이터]] 품질 자동 [[395_verification_process_review|검증]] 도구 |
| **[[150_unity_catalog|Unity Catalog]]** | [[074_photon_engine|Databricks]] 통합 거버넌스; 세분화 접근 제어 + [[606_auditing_linux_auditd|감사]] |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 품질 관리 — 수동 검증, 정기 점검]
    │
    ▼
[자동화 데이터 품질 — Great Expectations, dbt Test]
    │
    ▼
[데이터 계보 (Lineage) — OpenLineage, Apache Atlas]
    │
    ▼
[통합 데이터 감사 — 품질+계보+접근 로그 통합 거버넌스]
    │
    ▼
[AI 데이터/모델 감사 — 편향 탐지, 공정성 검증]
```
수동 [[395_verification_process_review|검증]]에서 자동화 품질 검사, 계보 추적, 통합 거버넌스를 거쳐 [[190_ai_llm_requirements_specification|AI]] 모델의 공정성 [[606_auditing_linux_auditd|감사]]로 진화하는 [[001_dikw_pyramid|데이터]] [[606_auditing_linux_auditd|감사]]의 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[001_dikw_pyramid|데이터]] [[606_auditing_linux_auditd|감사]]는 식품 공장의 **품질 검사관**이에요 — 재료(원시 [[001_dikw_pyramid|데이터]])부터 완성품(보고서)까지 모든 과정을 꼼꼼히 [[396_validation|확인]]해요!
2. "이 숫자가 왜 이렇게 됐나요?"라는 질문에, [[606_auditing_linux_auditd|감사]] 기록이 있으면 처음 들어온 [[001_dikw_pyramid|데이터]]부터 최종 결과까지 모든 과정을 딱딱 보여줄 수 있어요.
3. 회사가 법([[783_pipa_korea|개인정보보호법]], [[791_gdpr_eu|GDPR]])을 잘 지켰는지 증명하는 도장 역할도 하니까, [[001_dikw_pyramid|데이터]]를 다루는 모든 조직에 꼭 필요한 도구랍니다!
