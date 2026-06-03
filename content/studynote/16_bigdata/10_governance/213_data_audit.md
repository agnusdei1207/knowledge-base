+++
title = "23. 데이터 감사 (Data Audit)"
date = 2026-04-29

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Audit](/knowledge-base/studynote/12_it_management/05_security_compliance/363_audit/))는 조직의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자산이 [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/)(Accuracy)·완전성(Completeness)·[일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)([Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/))·적시성(Timeliness)·규정 준수([Compliance](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/058_it_compliance_sox_basel_gdpr_isms/)) 기준을 충족하는지 체계적으로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하고 기록하는 [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)([Data Governance](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)) 활동이다.
> 2. **가치**: 빅데이터 환경에서 [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)이 복잡해질수록 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 저하와 무단 접근이 탐지되지 않은 채 누적되며, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 이 위험을 선제적으로 탐지하고 [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/)·[개인정보보호법](/knowledge-base/studynote/09_security/16_data_privacy/783_pipa_korea/) 같은 규제 준수 증거를 제공한다.
> 3. **판단 포인트**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)의 핵심은 "누가(Who), 언제(When), 어떤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를(What), 어떻게 변경했는가(How)"를 추적하는 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)([Audit](/knowledge-base/studynote/12_it_management/05_security_compliance/363_audit/) Log)와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보([Data Lineage](/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/))이며, 이 두 가지가 없으면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 사고 발생 시 원인 추적과 법적 책임 소재 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)이 불가능하다.

---

## Ⅰ. 개요 및 필요성

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Audit](/knowledge-base/studynote/12_it_management/05_security_compliance/363_audit/))는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·변환·이동·삭제 전 과정을 추적하고 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하여, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 의도한 품질 기준과 규정 요건을 지속적으로 만족하는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 체계적인 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 프로세스다.

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)가 없다면 금융 보고서에 사용된 집계 수치가 잘못 계산되어도 원인을 추적할 수 없고, [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/)가 무단으로 접근·수출되어도 사후 파악이 어렵다. 특히 수백 개의 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인이 얽혀 있는 [데이터 레이크하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/) 환경에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 더 이상 선택이 아닌 필수다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터 감사 4대 검증 영역</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. 데이터 품질 감사 (Data Quality Audit)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 정확성: 값이 현실을 올바르게 반영하는가?</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 완전성: 필수 필드가 누락 없이 채워져 있는가?</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 일관성: 시스템 간 동일 데이터가 모순되지 않는가?</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 적시성: 데이터가 지정 시간 내에 갱신되었는가?</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2. 접근 감사 (Access Audit)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 누가 언제 어떤 데이터에 접근·변경했는가?</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3. 규정 준수 감사 (Compliance Audit)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ GDPR, 개인정보보호법, 금융감독규정 준수 여부</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4. 계보 감사 (Lineage Audit)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 데이터의 출처→변환→목적지 흐름 추적</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 식품 이력 추적 시스템과 같다. 식재료(원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))가 농장(소스)에서 공장([ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)), 식탁(보고서)까지 모든 과정이 기록되어 문제 발생 시 즉시 원산지를 추적할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)([Audit](/knowledge-base/studynote/12_it_management/05_security_compliance/363_audit/) Log) 구조

| 필드 | 설명 | 예시 |
|:---|:---|:---|
| **timestamp** | 이벤트 발생 시각 (UTC) | 2026-04-29T09:15:32Z |
| **user_id** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근/변경 주체 | user123 / svc_etl_job |
| **action** | 수행 작업 유형 | READ, INSERT, UPDATE, DELETE |
| **resource** | 접근한 테이블/[파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 경로 | db.orders, s3://bucket/path |
| **old_value / new_value** | 변경 전후 값 | {amount: 100} → {amount: 200} |
| **ip_address** | 접근 출처 IP | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/).0.1.55 |
| **status** | 성공/실패 | SUCCESS / DENIED |

### [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보([Data Lineage](/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/)) 아키텍처



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터 계보 추적 흐름</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">원시 데이터 소스</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">CRM DB (고객 정보) ──→ ETL Job (정제) ──→ DW (orders 테이블)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">BI 보고서 (매출 집계)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">계보 도구가 기록:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">"매출_집계 ← orders ← ETL_job_2026 ← CRM_DB"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">감사 질문: "이 매출 수치는 어디서 왔나?"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 계보 추적으로 CRM 원본까지 역추적 가능</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보는 스파게티 한 가닥이 냄비 속 어느 면에서 왔는지 추적하는 것이다. 엉켜있는 수백 개의 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 중에서 특정 숫자의 출처를 끝까지 따라가면 최초 소스를 찾을 수 있다.

---

## Ⅲ. 비교 및 연결

| 도구/기술 | 역할 | 특징 |
|:---|:---|:---|
| **Apache Atlas** | [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) + 계보 관리 | [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [에코](/knowledge-base/studynote/03_network/01_data_communication/031_에코_반향/)시스템 통합 |
| **OpenLineage** | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 계보 표준 | Airflow, Spark, dbt 연동 |
| **Great Expectations** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 자동화 | Python 기반, [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 통합 |
| <strong><a href="/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/">Delta Lake</a> ACID</strong> | [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 기반 변경 이력 | DESCRIBE HISTORY [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) |
| <strong><a href="/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/">Unity Catalog</a> (<a href="/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/">Databricks</a>)</strong> | 세분화 접근 제어 + [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) | [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 거버넌스 |

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)([Data Catalog](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/))와 결합하여 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/), 계보, 품질, 접근 이력을 단일 플랫폼에서 통합 관리하는 방향으로 진화하고 있다.

- **📢 섹션 요약 비유**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 도구는 조직의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [CSI](/knowledge-base/studynote/12_it_management/02_itsm_itil/068_csi/)([Crime](/knowledge-base/studynote/09_security/03_network_security/296_crime_attack/) Scene Investigation) 팀이다. 범죄([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 사고)가 발생하면 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)와 계보를 통해 현장 증거를 수집하고 범인(오류 원인)을 정확히 찾아낸다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: 금융 규제 보고서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)
금융 기관이 [금융감독원](/knowledge-base/studynote/09_security/17_framework_compliance/889_fss_cyber_supervision/) 제출용 보고서의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)를 수행한다.

1. <strong>품질 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a></strong>: Great Expectations로 잔액 필드 NOT NULL, 금액 > 0, 날짜 형식 ISO 8601 자동 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/).
2. **계보 추적**: OpenLineage로 "월별 거래 합산" 보고서 → [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) Job → 원천 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) DB 역추적.
3. <strong>접근 <a href="/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a></strong>: [Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)에서 보고서 테이블에 접근한 모든 [서비스 계정](/knowledge-base/studynote/15_devops_sre/05_devsecops/275_iam_role_for_service_accounts/) [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/).
4. **규정 준수**: [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/)(주민번호, 계좌번호) 접근 이벤트를 별도 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 테이블에 격리 저장, 5년 보관.
5. **보고서 제출**: [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 보고서 + [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보 다이어그램을 감독 기관에 증적 제출.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 변경 불가([Immutable](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/298_immutable/)) 스토리지(S3 객체 잠금, Glacier)에 저장.
- [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인의 Gate 조건으로 삽입 (품질 실패 시 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 중단).
- 계보 도구와 [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)를 연동하여 비즈니스 용어(Business Glossary) 기반 계보 제공.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 일반 운영 DB 테이블에 저장하는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/). [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 관리자([DBA](/knowledge-base/studynote/05_database/01_db_architecture_relational/025_dba_database_administrator/))가 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 자체를 수정·삭제할 수 있어 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)의 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)이 훼손된다. [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 반드시 접근 권한이 분리된 불변 스토리지에 저장해야 한다.

- **📢 섹션 요약 비유**: [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 일반 DB에 저장하는 건, 은행 [CCTV](/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/) 녹화 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 은행 직원이 접근 가능한 일반 서버에 두는 것과 같다. 내부 범행 시 증거가 사라질 수 있다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 | 수치 |
|:---|:---|:---|
| **규정 준수 입증** | [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/)/[개인정보보호법](/knowledge-base/studynote/09_security/16_data_privacy/783_pipa_korea/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 증적 | 과징금 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 제거 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/">신뢰성</a></strong> | 품질 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 자동화로 오보고 방지 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 오류 80% 조기 탐지 |
| <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/009_incident_response/">사고 대응</a>력</strong> | 계보 기반 원인 추적 속도 향상 | [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) 70% 단축 |

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)/ML 모델의 학습 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)([AI Audit](/knowledge-base/studynote/11_design_supervision/01_audit_framework/051_ai_bigdata_project_audit/))로 확장되어, 모델 결과의 공정성·편향 여부를 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하고 규제 기관에 설명하는 새로운 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 영역으로 발전하고 있다. [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)([Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/)) 아키텍처에서는 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)별 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 오너([Data Owner](/knowledge-base/studynote/16_bigdata/10_governance/200_data_owner/))가 각자의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 SLA를 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)하는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 체계가 표준이 되고 있다.

- **📢 섹션 요약 비유**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 조직의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 건강검진이다. 매년(또는 실시간으로) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 혈압(품질)·콜레스테롤(보안 이벤트)·MRI(계보)를 검사하여 질병([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 사고·[개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 침해)을 조기에 발견하고 치료한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/">데이터 거버넌스</a></strong> | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)가 실행 수단이 되는 상위 체계 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 계보 (<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/">Data Lineage</a>)</strong> | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 출처·변환·목적지 추적; [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)의 핵심 도구 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a> <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a> (<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/363_audit/">Audit</a> Log)</strong> | 접근·변경 이벤트 기록; 불변 스토리지에 보관 |
| **Great Expectations** | [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 내 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 자동 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 도구 |
| <strong><a href="/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/">Unity Catalog</a></strong> | [Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/) 통합 거버넌스; 세분화 접근 제어 + [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">데이터 품질 관리 — 수동 검증, 정기 점검</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">자동화 데이터 품질 — Great Expectations, dbt Test</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">데이터 계보 (Lineage) — OpenLineage, Apache Atlas</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">통합 데이터 감사 — 품질+계보+접근 로그 통합 거버넌스</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">AI 데이터/모델 감사 — 편향 탐지, 공정성 검증</div></div>
</div>
</div>


수동 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)에서 자동화 품질 검사, 계보 추적, 통합 거버넌스를 거쳐 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델의 공정성 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)로 진화하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)의 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명

1. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 식품 공장의 <strong>품질 검사관</strong>이에요 — 재료(원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))부터 완성품(보고서)까지 모든 과정을 꼼꼼히 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해요!
2. "이 숫자가 왜 이렇게 됐나요?"라는 질문에, [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 기록이 있으면 처음 들어온 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)부터 최종 결과까지 모든 과정을 딱딱 보여줄 수 있어요.
3. 회사가 법([개인정보보호법](/knowledge-base/studynote/09_security/16_data_privacy/783_pipa_korea/), [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/))을 잘 지켰는지 증명하는 도장 역할도 하니까, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다루는 모든 조직에 꼭 필요한 도구랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 213 / 262

← **이전**: [206. 빅데이터 분쟁 (Big Data Legal Disputes) — 데이터 소유권/수집 동의/목적 외 사용](/knowledge-base/studynote/16_bigdata/10_governance/212_bigdata_disputes/)
**다음**: [209. 금융 빅데이터 (Financial Big Data) — 신용평가/이상거래탐지/알고트레이딩](/knowledge-base/studynote/16_bigdata/11_industry/214_finance_bigdata/) →

---
