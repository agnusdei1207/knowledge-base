+++
title = "66. 데이터 거버넌스 (Data Governance) - 데이터 품질, 보안, 프라이버시 전사 관리 체계"

[taxonomies]
tags = ["enterprise_systems"]

[extra]
tags = ["enterprise_systems"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질, 보안, 프라이버시, 책임을 전사적으로 관리하는 체계다.
> 2. **가치**: 누가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 소유하고, 누가 책임지며, 어떤 규칙으로 사용할지 정하면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 혼란이 줄어든다.
> 3. **판단**: 기술만이 아니라 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), 역할, 프로세스, [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/), 품질 기준이 함께 있어야 한다.

---

## Ⅰ. 개요 및 필요성

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 많아질수록 "누가 무엇을 믿고 쓸 수 있는가"가 중요해진다. [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)는 이 질문에 대한 조직의 답이다.

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 자산으로 보려면 품질과 보안, 책임 소재가 분명해야 한다.

- **📢 섹션 요약 비유**: 큰 도서관에 대출 규칙과 사서가 있어야 책을 제대로 쓸 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Policies
  ↓
Roles / Stewardship
  ↓
Data Quality / Security
  ↓
Metadata / Lineage
  ↓
Governed Data
```

| 요소 | 역할 |
| :-- | :-- |
| [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) | 규칙 정의 |
| [Data Owner](/knowledge-base/studynote/16_bigdata/10_governance/200_data_owner/) | 최종 책임 |
| Steward | 운영 관리 |
| [Metadata](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 설명 |
| Lineage | 흐름 추적 |

[데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)는 단일 시스템이 아니라 조직 운영 체계다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정의, 품질, 권한, 책임을 일관되게 묶는 것이 핵심이다.

- **📢 섹션 요약 비유**: 도서관에서 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)표, 책임자, 대출 규칙이 모두 있어야 책이 흐트러지지 않는다.

---

## Ⅲ. 비교 및 연결

| 개념 | 초점 | 차이 |
| :-- | :-- | :-- |
| [Data Governance](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/) | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)과 책임 | 조직 전체 |
| [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/) | 운영과 처리 | 실행 중심 |
| [Data Quality](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/270_data_quality_great_expectations/) | [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/) | 품질 중심 |

| 영역 | 예 |
| :-- | :-- |
| [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) | [접근 통제](/knowledge-base/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/), 암호화 |
| Privacy | [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) |
| [Compliance](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/058_it_compliance_sox_basel_gdpr_isms/) | 규정 준수 |

거버넌스가 있어야 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리와 품질 개선이 지속된다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 만들기보다 지키고 믿을 수 있게 유지하는 것이 더 어렵다.

- **📢 섹션 요약 비유**: 물을 담는 통보다, 누가 관리하고 어떤 규칙으로 쓰는지가 더 중요할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 오너와 스튜어드가 정의되어 있는가?
2. 품질 기준과 승인 절차가 있는가?
3. [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)와 계보(lineage)를 관리하는가?
4. 보안/프라이버시 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 연결되는가?
5. 책임과 권한이 일치하는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 도구만 도입하고 책임은 없는 설계
- [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 없이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 쌓는 설계
- 품질과 보안을 따로 보는 설계
- [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)를 방치하는 설계

기술사 관점에서는 [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)를 "관리 체계"로 봐야 한다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 기술적 자산이면서도 조직적 자산이기 때문이다.

- **📢 섹션 요약 비유**: 정리 규칙이 없으면 아무리 큰 창고도 금방 엉망이 된다.

---

## Ⅴ. 기대효과 및 결론

[데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)가 있으면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질, 보안, 책임이 함께 정리된다. 그래서 전사 분석과 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 활용의 기반이 된다.

결론적으로 [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 사용의 법과 헌법이다.

- **📢 섹션 요약 비유**: 모두가 함께 쓰는 놀이터에는 규칙과 지킴이가 필요하다.

---

## 관련 개념 맵

```text
Policy
  ↓
Data Governance
  ↓
Quality / Security / Privacy
  ↓
Trusted Data
```

---

## 관련 키워드 및 발전 흐름도

```text
Data Management
  ↓
Data Governance
  ↓
Metadata / Lineage
  ↓
Data Trust
```

---

## 어린이를 위한 3줄 비유 설명

책을 아무렇게나 두면 못 찾아요.
누가 책임지는지 정해야 정리가 돼요.
[데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)는 그런 규칙이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 66 / 482

← **이전**: [65. 섀도우 데이터 (Shadow Data) - 통제받지 않은 클라우드 내 산재된 기업 민감 데이터](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/065_shadow_data_cloud_security/)
**다음**: [67. 데이터 스튜어드 (Data Steward) - 실무 부서 데이터 품질 관리 책임자](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/) →

---
