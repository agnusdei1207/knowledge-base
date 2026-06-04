+++
title = "194. 데이터 소유자 (Data Owner) — 비즈니스 책임자와 접근 승인"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)

- **본질**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소유자([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner)는 특정 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)에 대해 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적·법적 책임을 지는 시니어 비즈니스 임원으로, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 결정과 규제 준수에 대한 최종 책임을 진다.
- **가치**: [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/) 체계에서 Owner가 명확해야 접근 승인·규제 대응·품질 기준 결정이 일원화되고, 분쟁 발생 시 책임 소재가 명확해진다.
- **판단 포인트**: [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner는 기술적 역할이 아니라 <strong>비즈니스 책임 역할</strong>이며, GDPR의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 컨트롤러([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Controller) 개념과 유사하다는 점이 기술사 답안의 핵심 포인트다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner 정의

[Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소유자)는 특정 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)(예: 고객 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 재무 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 인사 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))에 대해:
- **누가 접근할 수 있는지** 결정하는 접근 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 권한
- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>가 규제를 준수하는지</strong> 보장하는 컴플라이언스 책임
- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 얼마나 보관하고 언제 삭제하는지</strong> 결정하는 생명주기 책임

을 갖는 **시니어 비즈니스 임원급** 역할이다.

### 1.2 필요성 — 소유자가 없으면 생기는 문제

| 문제 | 원인 |
|:---|:---|
| 접근 요청 승인 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 누가 승인 권한자인지 불명확 |
| 규제 대응 실패 | [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) 위반 시 책임 소재 불분명 |
| 과도한 접근 권한 | [최소 권한 원칙](/knowledge-base/studynote/09_security/01_intro_principles/010_least_privilege/) 집행자 부재 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 삭제 불이행 | 보유 기간 [결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/) 부재 -> 불필요 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 무한 축적 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 방치 | 품질 기준 결정 권한자 없음 |

**📢 섹션 요약 비유**: [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner가 없는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 <strong>무주공산(無主空山)</strong>과 같다. 아무도 책임지지 않으면 누구나 사용하다가 결국 아무도 관리하지 않게 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner 위치와 책임 구조

```
+---------------------------------------------------------------+
|                    데이터 거버넌스 책임 계층                     |
|                                                               |
|  +---------------------------------------------------------+  |
|  |  CDO (Chief Data Officer)                               |  |
|  |  전사 데이터 전략 및 거버넌스 총괄                         |  |
|  +-----------------------------------+---------------------+  |
|                                      | 도메인별 위임             |
|  +--------------+--------------+-----v---------------------+  |
|  | Customer DO  | Finance DO   |    Product DO              |  |
|  | (CMO급)      | (CFO급)      |    (CPO급)                 |  |
|  |              |              |                            |  |
|  | 고객 도메인   | 재무 도메인   | 제품 도메인                |  |
|  | 접근정책 결정 | 접근정책 결정 | 접근정책 결정              |  |
|  +------+-------+------+-------+------------+--------------+  |
|         |              |                    |                 |
|         v              v                    v                 |
|     Data Steward   Data Steward         Data Steward         |
|     (운영 위임)     (운영 위임)           (운영 위임)           |
+---------------------------------------------------------------+
```

### 2.2 [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner의 핵심 책임 6가지

| 책임 영역 | 세부 내용 |
|:---|:---|
| 접근 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 결정 | [최소 권한 원칙](/knowledge-base/studynote/09_security/01_intro_principles/010_least_privilege/)에 따른 역할별 접근 수준 정의 |
| 접근 요청 최종 승인 | [Data Steward](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/) 검토 후 최종 승인/거부 |
| 규제 준수 보장 | [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/)·PIPA에서 [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Controller 역할 수행 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 기준 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | 허용 품질 수준([SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)) 결정 |
| 보유/삭제 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 결정 | 법적 보관 기간 + 비즈니스 필요 기간 결정 |
| [데이터 분류](/knowledge-base/studynote/09_security/16_data_privacy/808_data_classification/) 결정 | Public/Internal/Confidential/[Secret](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) |

### 2.3 [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) 연계 — [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Controller 개념

| 개념 | [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) 용어 | [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/) 용어 |
|:---|:---|:---|
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 목적·방법 [결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/) | [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Controller ([Art](/knowledge-base/studynote/02_operating_system/10_security/621_art_android_runtime/).4(7)) | [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 실행자 | [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Processor ([Art](/knowledge-base/studynote/02_operating_system/10_security/621_art_android_runtime/).4(8)) | [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Custodian / IT |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 주체 | [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Subject | [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Consumer (고객 기준) |

**📢 섹션 요약 비유**: [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner는 <strong>아파트 입주자 대표</strong>와 같다. 공용 공간([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 사용 규칙을 정하고, 외부인(외부 접근자) 출입을 승인하며, 관리비(보유 비용) 결정도 책임진다.

---

## Ⅲ. 비교 및 연결

### 3.1 3대 역할 완전 비교

| 구분 | [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner | [Data Steward](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/) | [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Custodian |
|:---|:---|:---|:---|
| 직급 | C-level, VP, 부서장 | 시니어 업무 담당자 | [DBA](/knowledge-base/studynote/05_database/01_db_architecture_relational/025_dba_database_administrator/), 인프라 엔지니어 |
| 역할 성격 | [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적·법적 책임 | 운영적·[도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 관리 | 기술적·인프라 구현 |
| 시간 할애 | 비정기(결정 필요 시) | 정기(주 30~50%) | 상시(기술 운영) |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 지식 | 비즈니스 가치·위험 | 비즈니스 규칙·정의 | 기술 구조·저장 방식 |
| RACI 위치 | Accountable | Responsible | Responsible (기술) |
| [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) 대응 | [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Controller | - | [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Processor |

### 3.2 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 매핑 예시

| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) | [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner 직책 | 예시 |
|:---|:---|:---|
| 고객([C고객](/knowledge-base/studynote/12_it_management/01_governance_strategy/026_three_c_analysis/)) | CMO (Chief Marketing Officer) | 고객 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/), [CRM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| 재무(Finance) | CFO (Chief Financial Officer) | 매출, 비용, 예산 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| 인사(HR) | CHRO (Chief Human Resources Officer) | 직원 정보, 급여 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| 제품(Product) | CPO (Chief Product Officer) | 제품 [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/), 재고 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| 운영(Operations) | COO (Chief Operating Officer) | 주문, 물류, 공정 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |

**📢 섹션 요약 비유**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)별 Owner 매핑은 **부서별 예산 책임자** 지정과 같다. CFO가 재무 예산을 책임지듯, 각 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)의 Owner가 그 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 "예산(가치와 위험)"을 책임진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 접근 요청 승인 프로세스

```
[접근 요청자가 시스템에 요청]
         |
         v
[Data Steward: 비즈니스 필요성·위험 검토]
         |
    +----v----+
    | 저위험  |---> Steward가 직접 승인 (위임 권한 내)
    +----+----+
         |고위험 / 대량 데이터
         v
[Data Owner: 최종 승인/거부]
         |
         v
[Data Custodian: 기술적 권한 부여]
         |
         v
[감사 로그에 이력 기록]
```

### 4.2 [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner 지정 실패 패턴

- **공동 소유 함정**: "모든 임원이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner"라고 선언 -> 실질적 책임자 없음
- **IT 위임 함정**: IT 팀장을 Owner로 지정 -> 비즈니스 맥락 없는 기술적 결정
- **겸직 과부하**: 한 임원이 10개 이상 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) Owner -> 형식적 역할만 유지

### 4.3 기술사 답안 핵심 포인트

- [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner ≠ [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 물리적으로 소유한다는 의미 (법적 소유권 개념 아님)
- [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) Article 24: Controller는 [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Subject 권리 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)를 위한 적절한 기술·조직적 조치를 취해야 함 -> [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner 역할의 법적 근거
- 조직이 클수록 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) Owner를 세분화하고, 작은 조직은 CDO가 Owner 기능 겸직 가능

**📢 섹션 요약 비유**: [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner 지정 실패는 <strong>선장 없는 배</strong>와 같다. 선원(Steward, Custodian)이 아무리 잘 해도, 배의 방향([정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/))을 결정하는 선장이 없으면 항구에 도착하지 못한다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 기대효과

| 기대효과 | 세부 내용 |
|:---|:---|
| 명확한 책임 소재 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관련 사고 발생 시 책임자 명확 |
| 신속한 의사결정 | 접근 요청 처리 시간 단축 (임원 권한 위임 구조) |
| 규제 준수 | [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) Controller 역할 공식화로 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 대응 용이 |
| 품질 기준 현실화 | 비즈니스 맥락을 이해한 Owner가 실용적 기준 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 가치 인식 | 임원이 직접 관여함으로써 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 자산으로 인식 |

### 5.2 결론

[Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner는 [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)의 <strong>정치적(organizational) 중심축</strong>이다. 아무리 좋은 기술 도구와 프로세스가 있어도, 비즈니스 임원이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 책임을 받아들이지 않으면 거버넌스는 형식화된다. 기술사는 조직 설계(organizational design) 관점에서 [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner 역할을 제도화하는 방법을 제시해야 한다.

**📢 섹션 요약 비유**: [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner는 <strong>국가의 장관</strong>이다. 각 부처([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)) 장관이 그 부처 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(예산·[정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/))를 책임지고, 국무총리([CDO](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/068_cdo_cio_role_separation_governance/))가 전체를 조율하며, 대통령(이사회)이 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 방향을 제시한다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [CDO](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/068_cdo_cio_role_separation_governance/) | 상위 역할 | 전사 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)·거버넌스 총괄 |
| [Data Steward](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/) | 위임 역할 | Owner가 운영 책임 위임, 일상 관리 수행 |
| [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Custodian | 기술 실행 | Owner [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 기술적으로 구현 |
| [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Controller | 규제 연계 | [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner의 법적 대응 개념 |
| RACI Accountable | 책임 구조 | Owner는 RACI의 Accountable 역할 |
| [Data Classification](/knowledge-base/studynote/09_security/16_data_privacy/808_data_classification/) | 핵심 결정 | Owner가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 민감도 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 결정 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 생성 (Data Creation) — 비즈니스 프로세스에서 데이터 발생]
    |
    v
[데이터 오너 (Data Owner) — 데이터 자산의 최종 책임자 지정]
    |
    v
[데이터 스튜어드 (Data Steward) — 일상적 품질·분류 관리 담당자]
    |
    v
[데이터 거버넌스 위원회 (DGC) — 정책 수립·충돌 조정 조직]
    |
    v
[데이터 메시 도메인 오너십 — 도메인팀이 데이터 제품 소유·배포]
    |
    v
[GDPR / 개인정보 책임 — 법적 데이터 오너십과 컴플라이언스 통합]
```
[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 오너는 [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)의 핵심 책임 주체로, 스튜어드와의 역할 분담을 통해 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질·보안·컴플라이언스를 조직적으로 보장한다.

### 👶 어린이를 위한 3줄 비유 설명

1. 학교 도서관의 책을 "누가 빌릴 수 있고, 어떤 책은 선생님만 볼 수 있는지" 결정하는 사람이 교장 선생님인 것처럼, [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner는 회사 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 교장 선생님이야.
2. [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner는 컴퓨터를 직접 다루지 않아도 돼 — "이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 마케팅 팀만 볼 수 있어"처럼 규칙을 결정하는 게 역할이거든.
3. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 잘못 사용되거나 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/)가 유출되면, [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Owner가 최종 책임을 지기 때문에 가장 신중하게 역할을 수행해야 해.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 200 / 262

<- **이전**: [193. 데이터 스튜어드 (Data Steward) — 도메인 데이터 책임자](/knowledge-base/studynote/16_bigdata/10_governance/199_data_steward/)
**다음**: [195. 데이터 품질 차원 (Data Quality Dimensions) — 완전성/정확성/일관성/적시성](/knowledge-base/studynote/16_bigdata/10_governance/201_data_quality_dimensions/) ->

---
