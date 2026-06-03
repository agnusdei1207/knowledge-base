---
title: 191. 데이터 거버넌스 정의 (Data Governance Definition) — 데이터 소유·관리·사용 원칙 체계
date: '2026-04-21'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)

- **본질**: [[052_data_governance_framework|데이터 거버넌스]]([[052_data_governance_framework|Data Governance]])는 [[001_dikw_pyramid|데이터]] 자산의 소유·관리·사용에 관한 [[164_policy|정책]], 표준, 역할, 프로세스, 도구의 체계로, "누가 어떤 [[001_dikw_pyramid|데이터]]를 어떻게 어떤 목적으로 사용하는가"를 결정하는 프레임워크다.
- **가치**: [[001_dikw_pyramid|데이터]] 품질 확보, [[791_gdpr_eu|GDPR]]·PIPA 규제 준수, 보안 강화, [[001_dikw_pyramid|데이터]] 발견성(discoverability) 향상을 동시에 달성해 조직의 [[001_dikw_pyramid|데이터]] [[085_confidence_association_rule_conditional_probability|신뢰도]]와 의사결정 속도를 높인다.
- **판단 포인트**: 거버넌스는 "무엇을·왜(What & Why)"를 규정하고 [[001_dikw_pyramid|데이터]] 관리([[001_dikw_pyramid|Data]] [[372_management|Management]])는 "어떻게(How)"를 실행한다 — 이 구분이 기술사 답안의 핵심 차별점이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 정의

[[117_dama|DAMA]] ([[001_dikw_pyramid|Data]] [[372_management|Management]] Association) DMBOK ([[001_dikw_pyramid|Data]] [[372_management|Management]] Body of Knowledge v2)는 [[052_data_governance_framework|데이터 거버넌스]]를 다음과 같이 정의한다:
> "[[001_dikw_pyramid|데이터]] 자산 관리에 관한 의사결정권과 책임 행사를 위한 권한, [[164_policy|정책]], 프로세스, 표준, 역할, 지표의 집합"

[[052_data_governance_framework|데이터 거버넌스]]는 [[001_dikw_pyramid|데이터]] [[087_process_state_transition|생성]]·수집·저장·가공·공유·폐기의 전 생애주기([[001_dikw_pyramid|Data]] Lifecycle)에 걸쳐 조직이 [[001_dikw_pyramid|데이터]]를 신뢰·활용·[[571_protection_vs_security|보호]]하는 방식을 결정하는 **경영·관리 체계**다.

### 1.2 필요성

| 배경 요인 | 세부 내용 |
|:---|:---|
| [[001_dikw_pyramid|데이터]] 폭증 | 2025년 세계 [[001_dikw_pyramid|데이터]] [[087_process_state_transition|생성]]량 ≈ 120 ZB — 관리 없이는 [[288_data_swamp_metadata_management_absence|데이터 늪]]([[288_data_swamp_metadata_management_absence|Data Swamp]]) 전락 위험 |
| 규제 강화 | [[791_gdpr_eu|GDPR]], 한국 PIPA([[783_pipa_korea|개인정보보호법]]), SOX, [[863_hipaa|HIPAA]] 위반 시 막대한 과징금 |
| [[190_ai_llm_requirements_specification|AI]]·ML 품질 | Garbage In, Garbage Out — 학습 [[001_dikw_pyramid|데이터]] 품질이 모델 [[282_performance_tactics|성능]]을 결정 |
| [[001_dikw_pyramid|데이터]] [[002_silo_hyeonhyung|사일로]] | 부서별 독립 시스템 → 불일치·중복·비용 증가 |
| [[055_digital_transformation|디지털 전환]] | [[001_dikw_pyramid|데이터]]를 [[268_strategy_pattern|전략]] 자산으로 취급하려면 거버넌스가 선행 조건 |

### 1.3 거버넌스 vs [[001_dikw_pyramid|데이터]] 관리

```
┌─────────────────────────────────────────────────────────┐
│             데이터 거버넌스 (What & Why)                  │
│  ┌──────────────┐  ┌─────────────┐  ┌────────────────┐  │
│  │  정책 · 표준  │  │  역할 · 책임 │  │  원칙 · 목표   │  │
│  └──────────────┘  └─────────────┘  └────────────────┘  │
│                         │                                │
│                         ▼                                │
│             데이터 관리 (How)                             │
│  ┌─────────┐ ┌──────────┐ ┌─────────┐ ┌─────────────┐  │
│  │ 품질관리 │ │ 메타데이터│ │ 보안관리 │ │ 아키텍처관리 │  │
│  └─────────┘ └──────────┘ └─────────┘ └─────────────┘  │
└─────────────────────────────────────────────────────────┘
```

**📢 섹션 요약 비유**: [[052_data_governance_framework|데이터 거버넌스]]는 국가의 **헌법**이다. 헌법이 "무엇을 허용하고 무엇을 금지하는지" 원칙을 정하면, 각 부처([[001_dikw_pyramid|데이터]] 관리)가 그 원칙을 실제 법령과 행정으로 구현한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 거버넌스 프레임워크 구조

```
┌──────────────────────────────────────────────────────────────┐
│                  데이터 거버넌스 프레임워크                    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │         거버넌스 위원회 (Governance Council)           │    │
│  │   CDO (Chief Data Officer) + 부문별 Data Owner        │    │
│  └─────────────────────────┬────────────────────────────┘    │
│                            │ 정책 수립 · 의사결정              │
│  ┌────────────┬────────────▼────────┬───────────────────┐    │
│  │  정책·표준  │   역할·책임 (RACI)  │     프로세스       │    │
│  │            │                     │                   │    │
│  │ · 접근정책  │ · Data Owner        │ · 이슈 해결        │    │
│  │ · 보유정책  │ · Data Steward      │ · 변경 관리        │    │
│  │ · 품질표준  │ · Data Custodian    │ · 인증 절차        │    │
│  │ · 명명규칙  │ · Data Consumer     │ · 감사            │    │
│  └────────────┴─────────────────────┴───────────────────┘    │
│                            │                                 │
│  ┌─────────────────────────▼──────────────────────────────┐  │
│  │                  거버넌스 도구 (Tooling)                 │  │
│  │  데이터 카탈로그 │ 품질 도구 │ 리니지 │ MDM │ 감사로그  │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### 2.2 표준 및 성숙도 모델

| 기준 | 내용 |
|:---|:---|
| ISO 8000 | [[001_dikw_pyramid|데이터]] 품질 국제 표준 — [[001_dikw_pyramid|데이터]] 교환 요구사항 및 품질 측정 방법 정의 |
| [[117_dama|DAMA]] DMBOK v2 | 11개 지식 영역: 거버넌스·아키텍처·모델링·보안·품질·[[012_metadata|메타데이터]]·[[539_mdm_master_data_management|MDM]] 등 |
| [[004_cobit|COBIT]] | IT 거버넌스 프레임워크 — [[052_data_governance_framework|데이터 거버넌스]]와 IT 거버넌스 연계 |

| 성숙도 | 단계 | 특징 |
|:---:|:---|:---|
| 1 | Initial ([[459_quic_fec_forward_error_correction|초기]]) | 임시방편, 개인 의존, 문서화 없음 |
| 2 | Managed (관리) | 프로젝트 단위 거버넌스 존재 |
| 3 | Defined (정의) | 조직 전체 표준 [[164_policy|정책]] 수립 |
| 4 | Measured (측정) | 품질 [[018_kpi|KPI]] 측정·[[229_monitor|모니터]]링 |
| 5 | Optimizing (최적화) | 지속적 개선, 자동화 |

**📢 섹션 요약 비유**: 거버넌스 프레임워크는 **기업 내부 규정집**이다. 규정이 없으면 직원마다 제멋대로 행동하고, 규정이 있어야 [[606_auditing_linux_auditd|감사]]([[363_audit|audit]])가 가능하다.

---

## Ⅲ. 비교 및 연결

### 3.1 거버넌스 vs 관련 개념

| 구분 | [[052_data_governance_framework|데이터 거버넌스]] | [[001_dikw_pyramid|데이터]] 관리 | [[001_dikw_pyramid|데이터]] [[268_strategy_pattern|전략]] |
|:---|:---|:---|:---|
| 초점 | 원칙·[[164_policy|정책]]·역할 | 실행·운영 | 장기 방향성 |
| 질문 | 무엇을, 왜? | 어떻게? | 어디로? |
| 주체 | [[068_cdo_cio_role_separation_governance|CDO]]·이사회 | IT·[[025_dba_database_administrator|DBA]] | CEO·이사회 |
| 산출물 | [[164_policy|정책]]서·역할정의 | 시스템·프로세스 | 로드맵·[[018_kpi|KPI]] |

### 3.2 규제와의 연계

| 규제 | 거버넌스 연계 요구사항 |
|:---|:---|
| [[791_gdpr_eu|GDPR]] (EU) | [[621_art_android_runtime|Art]].5 처리 원칙, [[621_art_android_runtime|Art]].30 처리 활동 기록, [[270_embedding_model|DPO]] ([[797_gdpr_dpo|Data Protection Officer]]) 지정 |
| PIPA (한국) | [[781_personal_information|개인정보]] 처리방침, [[781_personal_information|개인정보]] [[571_protection_vs_security|보호]]책임자(CPO) 지정, 가명처리 절차 |
| SOX (미국) | 재무 [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]], 변경 이력 [[606_auditing_linux_auditd|감사]], [[387_access_control_pattern|접근 통제]] 증거 |
| [[863_hipaa|HIPAA]] (미국) | 의료 정보 접근 제어, [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]], 암호화 |

**📢 섹션 요약 비유**: 거버넌스 [[164_policy|정책]]은 **운전 면허증 발급 기준**과 같다. 규제(교통법)가 정한 기준에 맞게 누가 어떤 차([[001_dikw_pyramid|데이터]])를 운전(사용)할 수 있는지 조직이 자체적으로 정의한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 구현 접근 방식: 중앙집중 vs 연방 vs 하이브리드

| 모델 | 특징 | 적합 조직 |
|:---|:---|:---|
| 중앙집중형 | [[068_cdo_cio_role_separation_governance|CDO]] 산하 단일 거버넌스 팀이 모든 [[164_policy|정책]] 수립·집행 | 소규모·단일 사업부 |
| 연방형(Federated) | [[064_relation_domain|도메인]]별 자체 거버넌스 + 공통 최소 표준만 공유 | 대기업·[[211_data_mesh_domain_ownership|데이터 메시]] 채택 조직 |
| 하이브리드 | 핵심 [[164_policy|정책]]은 중앙, [[064_relation_domain|도메인]] 세부는 자율 | 글로벌 기업, 금융지주 |

### 4.2 도구 선택 기준

```
규모·예산이 크고 엔터프라이즈 요구 → Collibra, Informatica AXON
오픈소스 선호, Hadoop 생태계 → Apache Atlas
클라우드 네이티브(AWS) → AWS Glue Data Catalog + Lake Formation
클라우드 네이티브(GCP) → Dataplex + Data Catalog
클라우드 네이티브(Azure) → Microsoft Purview
확장성 높은 오픈소스 → DataHub (LinkedIn), OpenMetadata
```

### 4.3 기술사 답안 포인트

- 거버넌스 도입 시 **비즈니스 가치([[012_roi_return_on_investment|ROI]])** 측면: IBM 연구에서 [[001_dikw_pyramid|데이터]] 품질 문제가 미국 기업에 연간 3.1조 달러 손실 유발
- **[[320_data_mesh|Data Mesh]]** 아키텍처와의 [[083_relationship_in_er_model|관계]]: [[211_data_mesh_domain_ownership|데이터 메시]]는 연방형 거버넌스를 전제 조건으로 함
- **[[068_cdo_cio_role_separation_governance|CDO]](최고데이터책임자) 역할**: 거버넌스 오너십의 조직 내 위치가 성공의 핵심

**📢 섹션 요약 비유**: 거버넌스 도입은 **교통 인프라 정비**와 같다. 도로([[001_dikw_pyramid|데이터]])가 아무리 많아도 [[130_signal|신호]]등([[164_policy|정책]])·번호판([[655_ir_detection_analysis|식별]])·면허증(접근권)이 없으면 교통 대란이 난다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 기대효과

| 효과 | 세부 내용 |
|:---|:---|
| [[001_dikw_pyramid|데이터]] [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 향상 | 표준화된 품질 기준으로 "이 숫자를 믿을 수 있나?" 문제 해소 |
| 규제 준수 비용 절감 | 사전 통제로 사후 벌금·[[606_auditing_linux_auditd|감사]] 비용 절감 |
| [[001_dikw_pyramid|데이터]] 검색 효율 | [[394_catalog_metadata|카탈로그]]·리니지로 필요한 [[001_dikw_pyramid|데이터]]를 빠르게 발견 |
| [[190_ai_llm_requirements_specification|AI]]/ML 품질 개선 | 정제된 학습 [[001_dikw_pyramid|데이터]]로 모델 정확도 향상 |
| 조직 협업 강화 | 공통 정의([[509_data_dictionary|data dictionary]])로 부서 간 소통 비용 절감 |

### 5.2 결론

[[052_data_governance_framework|데이터 거버넌스]]는 "[[001_dikw_pyramid|데이터]]를 자산처럼 다루는 조직"이 되기 위한 필수 인프라다. ISO 8000, [[117_dama|DAMA]] DMBOK, [[791_gdpr_eu|GDPR]] 등 국제 표준과 규제가 거버넌스를 요구하는 시대에, 기술사는 거버넌스 프레임워크 설계 역량(역할 정의, [[164_policy|정책]] 수립, 도구 선택)을 갖춰야 한다. 특히 [[211_data_mesh_domain_ownership|데이터 메시]], [[190_ai_llm_requirements_specification|AI]] 윤리, 클라우드 멀티 환경에서 연방형 거버넌스 모델이 부상하고 있다.

**📢 섹션 요약 비유**: [[052_data_governance_framework|데이터 거버넌스]]는 **도시 건축 조례**다. 조례 없이 건물을 지으면 나중에 철거 비용이 더 든다. 처음부터 원칙을 세워야 도시([[001_dikw_pyramid|데이터]] 생태계)가 지속 가능하다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| [[067_data_steward_data_quality|Data Steward]] | 하위 역할 | [[064_relation_domain|도메인]] [[001_dikw_pyramid|데이터]] 품질·정의 일상 관리자 |
| [[200_data_owner|Data Owner]] | 하위 역할 | 비즈니스 책임자, 접근 [[164_policy|정책]] 승인 |
| [[213_data_catalog_metadata|Data Catalog]] | 도구 | [[001_dikw_pyramid|데이터]] 자산 목록·검색·리니지 |
| [[270_data_quality_great_expectations|Data Quality]] | 목표 | 완전성·[[002_bigdata_5v|정확성]]·[[194_consistency_database_integrity|일관성]]·적시성 확보 |
| [[539_mdm_master_data_management|MDM]] | 연계 기법 | 핵심 비즈니스 엔티티 황금 레코드 [[087_process_state_transition|생성]] |
| [[117_dama|DAMA]] DMBOK | 표준 | [[001_dikw_pyramid|데이터]] 관리 지식체계 국제 표준 |
| [[320_data_mesh|Data Mesh]] | 아키텍처 | 연방형 거버넌스를 전제로 한 [[136_variance|분산]] [[104_da_as_is_analysis|데이터 아키텍처]] |
| [[791_gdpr_eu|GDPR]] | 규제 연계 | EU [[803_privacy_law_comparison|개인정보보호]]규정, 거버넌스 요구사항 부과 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 관리]
    │
    ▼
[데이터 품질]
    │
    ▼
[데이터 거버넌스]
    │
    ▼
[데이터 카탈로그]
    │
    ▼
[데이터 메시 거버넌스]
```

[[001_dikw_pyramid|데이터]] 관리의 기초가 품질 관리로 구체화되고, 거버넌스와 [[394_catalog_metadata|카탈로그]]를 거쳐 [[211_data_mesh_domain_ownership|데이터 메시]] 시대의 [[136_variance|분산]] 거버넌스로 발전하는 흐름이다.

---

### 👶 어린이를 위한 3줄 비유 설명

1. 학교에서 도서관 책을 누가 빌릴 수 있고, 어떻게 빌리고, 얼마나 보관해야 하는지 규칙을 정한 것처럼, 회사에서는 [[052_data_governance_framework|데이터 거버넌스]]가 그 역할을 해.
2. "규칙 없이 쓰는 [[001_dikw_pyramid|데이터]]"는 아무나 낙서하는 공책 같아서 나중에 뭐가 맞는지 아무도 모르게 돼.
3. [[052_data_governance_framework|데이터 거버넌스]] 덕분에 "이 숫자가 진짜 맞아?" 하는 걱정 없이 중요한 결정을 내릴 수 있어.
