---
title: "191. 데이터 거버넌스 정의 (Data Governance Definition) — 데이터 소유·관리·사용 원칙 체계"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
---


## 핵심 인사이트 (3줄 요약)

- **본질**: [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)([Data Governance](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/))는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자산의 소유·관리·사용에 관한 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/), 표준, 역할, 프로세스, 도구의 체계로, "누가 어떤 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 어떻게 어떤 목적으로 사용하는가"를 결정하는 프레임워크다.
- **가치**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 확보, [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/)·PIPA 규제 준수, 보안 강화, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 발견성(discoverability) 향상을 동시에 달성해 조직의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [신뢰도](/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/)와 의사결정 속도를 높인다.
- **판단 포인트**: 거버넌스는 "무엇을·왜(What & Why)"를 규정하고 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/))는 "어떻게(How)"를 실행한다 — 이 구분이 기술사 답안의 핵심 차별점이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 정의

[DAMA](/studynote/03_network/02_multiplexing_multiple_access/117_dama/) ([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/) Association) DMBOK ([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/) Body of Knowledge v2)는 [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)를 다음과 같이 정의한다:
> "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자산 관리에 관한 의사결정권과 책임 행사를 위한 권한, [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/), 프로세스, 표준, 역할, 지표의 집합"

[데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·수집·저장·가공·공유·폐기의 전 생애주기([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Lifecycle)에 걸쳐 조직이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 신뢰·활용·[보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)하는 방식을 결정하는 <strong>경영·관리 체계</strong>다.

### 1.2 필요성

| 배경 요인 | 세부 내용 |
|:---|:---|
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 폭증 | 2025년 세계 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)량 ≈ 120 ZB — 관리 없이는 [데이터 늪](/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/)([Data Swamp](/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/)) 전락 위험 |
| 규제 강화 | [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/), 한국 PIPA([개인정보보호법](/studynote/09_security/16_data_privacy/783_pipa_korea/)), SOX, [HIPAA](/studynote/09_security/17_framework_compliance/1058_hipaa/) 위반 시 막대한 과징금 |
| [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)·ML 품질 | Garbage In, Garbage Out — 학습 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질이 모델 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 결정 |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [사일로](/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/) | 부서별 독립 시스템 -> 불일치·중복·비용 증가 |
| [디지털 전환](/studynote/12_it_management/01_governance_strategy/055_digital_transformation/) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 자산으로 취급하려면 거버넌스가 선행 조건 |

### 1.3 거버넌스 vs [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리

```
+---------------------------------------------------------+
|             데이터 거버넌스 (What & Why)                  |
|  +--------------+  +-------------+  +----------------+  |
|  |  정책 · 표준  |  |  역할 · 책임 |  |  원칙 · 목표   |  |
|  +--------------+  +-------------+  +----------------+  |
|                         |                                |
|                         v                                |
|             데이터 관리 (How)                             |
|  +---------+ +----------+ +---------+ +-------------+  |
|  | 품질관리 | | 메타데이터| | 보안관리 | | 아키텍처관리 |  |
|  +---------+ +----------+ +---------+ +-------------+  |
+---------------------------------------------------------+
```

**📢 섹션 요약 비유**: [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)는 국가의 <strong>헌법</strong>이다. 헌법이 "무엇을 허용하고 무엇을 금지하는지" 원칙을 정하면, 각 부처([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리)가 그 원칙을 실제 법령과 행정으로 구현한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 거버넌스 프레임워크 구조

```
+--------------------------------------------------------------+
|                  데이터 거버넌스 프레임워크                    |
|                                                              |
|  +------------------------------------------------------+    |
|  |         거버넌스 위원회 (Governance Council)           |    |
|  |   CDO (Chief Data Officer) + 부문별 Data Owner        |    |
|  +-------------------------+----------------------------+    |
|                            | 정책 수립 · 의사결정              |
|  +------------+------------v--------+-------------------+    |
|  |  정책·표준  |   역할·책임 (RACI)  |     프로세스       |    |
|  |            |                     |                   |    |
|  | · 접근정책  | · Data Owner        | · 이슈 해결        |    |
|  | · 보유정책  | · Data Steward      | · 변경 관리        |    |
|  | · 품질표준  | · Data Custodian    | · 인증 절차        |    |
|  | · 명명규칙  | · Data Consumer     | · 감사            |    |
|  +------------+---------------------+-------------------+    |
|                            |                                 |
|  +-------------------------v------------------------------+  |
|  |                  거버넌스 도구 (Tooling)                 |  |
|  |  데이터 카탈로그 | 품질 도구 | 리니지 | MDM | 감사로그  |  |
|  +--------------------------------------------------------+  |
+--------------------------------------------------------------+
```

### 2.2 표준 및 성숙도 모델

| 기준 | 내용 |
|:---|:---|
| ISO 8000 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 국제 표준 — [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 교환 요구사항 및 품질 측정 방법 정의 |
| [DAMA](/studynote/03_network/02_multiplexing_multiple_access/117_dama/) DMBOK v2 | 11개 지식 영역: 거버넌스·아키텍처·모델링·보안·품질·[메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)·[MDM](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 등 |
| [COBIT](/studynote/12_it_management/01_governance_strategy/004_cobit/) | IT 거버넌스 프레임워크 — [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)와 IT 거버넌스 연계 |

| 성숙도 | 단계 | 특징 |
|:---:|:---|:---|
| 1 | Initial ([초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)) | 임시방편, 개인 의존, 문서화 없음 |
| 2 | Managed (관리) | 프로젝트 단위 거버넌스 존재 |
| 3 | Defined (정의) | 조직 전체 표준 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 수립 |
| 4 | Measured (측정) | 품질 [KPI](/studynote/12_it_management/01_governance_strategy/018_kpi/) 측정·[모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 |
| 5 | Optimizing (최적화) | 지속적 개선, 자동화 |

**📢 섹션 요약 비유**: 거버넌스 프레임워크는 <strong>기업 내부 규정집</strong>이다. 규정이 없으면 직원마다 제멋대로 행동하고, 규정이 있어야 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)([audit](/studynote/12_it_management/05_security_compliance/363_audit/))가 가능하다.

---

## Ⅲ. 비교 및 연결

### 3.1 거버넌스 vs 관련 개념

| 구분 | [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
|:---|:---|:---|:---|
| 초점 | 원칙·[정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)·역할 | 실행·운영 | 장기 방향성 |
| 질문 | 무엇을, 왜? | 어떻게? | 어디로? |
| 주체 | [CDO](/studynote/07_enterprise_systems/01_strategy_governance/068_cdo_cio_role_separation_governance/)·이사회 | IT·[DBA](/studynote/05_database/01_db_architecture_relational/025_dba_database_administrator/) | CEO·이사회 |
| 산출물 | [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)서·역할정의 | 시스템·프로세스 | 로드맵·[KPI](/studynote/12_it_management/01_governance_strategy/018_kpi/) |

### 3.2 규제와의 연계

| 규제 | 거버넌스 연계 요구사항 |
|:---|:---|
| [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/) (EU) | [Art](/studynote/02_operating_system/10_security/621_art_android_runtime/).5 처리 원칙, [Art](/studynote/02_operating_system/10_security/621_art_android_runtime/).30 처리 활동 기록, [DPO](/studynote/06_ict_convergence/04_ai_llm/270_embedding_model/) ([Data Protection Officer](/studynote/09_security/16_data_privacy/797_gdpr_dpo/)) 지정 |
| PIPA (한국) | [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 처리방침, [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)책임자(CPO) 지정, 가명처리 절차 |
| SOX (미국) | 재무 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/studynote/09_security/01_intro_principles/003_integrity/), 변경 이력 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/), [접근 통제](/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/) 증거 |
| [HIPAA](/studynote/09_security/17_framework_compliance/1058_hipaa/) (미국) | 의료 정보 접근 제어, [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 암호화 |

**📢 섹션 요약 비유**: 거버넌스 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)은 <strong>운전 면허증 발급 기준</strong>과 같다. 규제(교통법)가 정한 기준에 맞게 누가 어떤 차([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 운전(사용)할 수 있는지 조직이 자체적으로 정의한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 구현 접근 방식: 중앙집중 vs 연방 vs 하이브리드

| 모델 | 특징 | 적합 조직 |
|:---|:---|:---|
| 중앙집중형 | [CDO](/studynote/07_enterprise_systems/01_strategy_governance/068_cdo_cio_role_separation_governance/) 산하 단일 거버넌스 팀이 모든 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 수립·집행 | 소규모·단일 사업부 |
| 연방형(Federated) | [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)별 자체 거버넌스 + 공통 최소 표준만 공유 | 대기업·[데이터 메시](/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) 채택 조직 |
| 하이브리드 | 핵심 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)은 중앙, [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 세부는 자율 | 글로벌 기업, 금융지주 |

### 4.2 도구 선택 기준

```
규모·예산이 크고 엔터프라이즈 요구 -> Collibra, Informatica AXON
오픈소스 선호, Hadoop 생태계 -> Apache Atlas
클라우드 네이티브(AWS) -> AWS Glue Data Catalog + Lake Formation
클라우드 네이티브(GCP) -> Dataplex + Data Catalog
클라우드 네이티브(Azure) -> Microsoft Purview
확장성 높은 오픈소스 -> DataHub (LinkedIn), OpenMetadata
```

### 4.3 기술사 답안 포인트

- 거버넌스 도입 시 <strong>비즈니스 가치(<a href="/studynote/12_it_management/01_governance_strategy/807_roi_return_on_investment/">ROI</a>)</strong> 측면: IBM 연구에서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 문제가 미국 기업에 연간 3.1조 달러 손실 유발
- <strong><a href="/studynote/12_it_management/05_security_compliance/320_data_mesh/">Data Mesh</a></strong> 아키텍처와의 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/): [데이터 메시](/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)는 연방형 거버넌스를 전제 조건으로 함
- <strong><a href="/studynote/07_enterprise_systems/01_strategy_governance/068_cdo_cio_role_separation_governance/">CDO</a>(최고데이터책임자) 역할</strong>: 거버넌스 오너십의 조직 내 위치가 성공의 핵심

**📢 섹션 요약 비유**: 거버넌스 도입은 <strong>교통 인프라 정비</strong>와 같다. 도로([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))가 아무리 많아도 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)등([정책](/studynote/10_ai/02_dl_architecture_new/164_policy/))·번호판([식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/))·면허증(접근권)이 없으면 교통 대란이 난다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 기대효과

| 효과 | 세부 내용 |
|:---|:---|
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 향상 | 표준화된 품질 기준으로 "이 숫자를 믿을 수 있나?" 문제 해소 |
| 규제 준수 비용 절감 | 사전 통제로 사후 벌금·[감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 비용 절감 |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 검색 효율 | [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)·리니지로 필요한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 빠르게 발견 |
| [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)/ML 품질 개선 | 정제된 학습 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 모델 정확도 향상 |
| 조직 협업 강화 | 공통 정의([data dictionary](/studynote/05_database/04_transactions_concurrency/509_data_dictionary/))로 부서 간 소통 비용 절감 |

### 5.2 결론

[데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)는 "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 자산처럼 다루는 조직"이 되기 위한 필수 인프라다. ISO 8000, [DAMA](/studynote/03_network/02_multiplexing_multiple_access/117_dama/) DMBOK, [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/) 등 국제 표준과 규제가 거버넌스를 요구하는 시대에, 기술사는 거버넌스 프레임워크 설계 역량(역할 정의, [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 수립, 도구 선택)을 갖춰야 한다. 특히 [데이터 메시](/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/), [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 윤리, 클라우드 멀티 환경에서 연방형 거버넌스 모델이 부상하고 있다.

**📢 섹션 요약 비유**: [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)는 <strong>도시 건축 조례</strong>다. 조례 없이 건물을 지으면 나중에 철거 비용이 더 든다. 처음부터 원칙을 세워야 도시([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 생태계)가 지속 가능하다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [Data Steward](/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/) | 하위 역할 | [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질·정의 일상 관리자 |
| [Data Owner](/studynote/16_bigdata/10_governance/200_data_owner/) | 하위 역할 | 비즈니스 책임자, 접근 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 승인 |
| [Data Catalog](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) | 도구 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자산 목록·검색·리니지 |
| [Data Quality](/studynote/13_cloud_architecture/05_data_engineering/270_data_quality_great_expectations/) | 목표 | 완전성·[정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/)·[일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)·적시성 확보 |
| [MDM](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) | 연계 기법 | 핵심 비즈니스 엔티티 황금 레코드 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| [DAMA](/studynote/03_network/02_multiplexing_multiple_access/117_dama/) DMBOK | 표준 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리 지식체계 국제 표준 |
| [Data Mesh](/studynote/12_it_management/05_security_compliance/320_data_mesh/) | 아키텍처 | 연방형 거버넌스를 전제로 한 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터 아키텍처](/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) |
| [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/) | 규제 연계 | EU [개인정보보호](/studynote/09_security/16_data_privacy/803_privacy_law_comparison/)규정, 거버넌스 요구사항 부과 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 관리]
    |
    v
[데이터 품질]
    |
    v
[데이터 거버넌스]
    |
    v
[데이터 카탈로그]
    |
    v
[데이터 메시 거버넌스]
```

[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리의 기초가 품질 관리로 구체화되고, 거버넌스와 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)를 거쳐 [데이터 메시](/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) 시대의 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 거버넌스로 발전하는 흐름이다.

---

### 👶 어린이를 위한 3줄 비유 설명

1. 학교에서 도서관 책을 누가 빌릴 수 있고, 어떻게 빌리고, 얼마나 보관해야 하는지 규칙을 정한 것처럼, 회사에서는 [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)가 그 역할을 해.
2. "규칙 없이 쓰는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)"는 아무나 낙서하는 공책 같아서 나중에 뭐가 맞는지 아무도 모르게 돼.
3. [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/) 덕분에 "이 숫자가 진짜 맞아?" 하는 걱정 없이 중요한 결정을 내릴 수 있어.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 197 / 262

<- **이전**: [06. 오픈 테이블 포맷 (Open Table Format) - 레이크하우스의 핵심 기반 기술](/studynote/16_bigdata/10_governance/196_opentableformat/)
**다음**: [192. 데이터 거버넌스 구성 요소 (Data Governance Components) — 정책/표준/역할/프로세스/도구](/studynote/16_bigdata/10_governance/198_data_governance_components/) ->

---
