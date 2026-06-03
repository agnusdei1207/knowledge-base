---
title: 66. 데이터 거버넌스 (Data Governance) - 데이터 품질, 보안, 프라이버시 전사 관리 체계
tags:
- enterprise_systems
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[052_data_governance_framework|데이터 거버넌스]]는 [[001_dikw_pyramid|데이터]] 품질, 보안, 프라이버시, 책임을 전사적으로 관리하는 체계다.
> 2. **가치**: 누가 [[001_dikw_pyramid|데이터]]를 소유하고, 누가 책임지며, 어떤 규칙으로 사용할지 정하면 [[001_dikw_pyramid|데이터]] 혼란이 줄어든다.
> 3. **판단**: 기술만이 아니라 [[164_policy|정책]], 역할, 프로세스, [[012_metadata|메타데이터]], 품질 기준이 함께 있어야 한다.

---

## Ⅰ. 개요 및 필요성

[[001_dikw_pyramid|데이터]]가 많아질수록 "누가 무엇을 믿고 쓸 수 있는가"가 중요해진다. [[052_data_governance_framework|데이터 거버넌스]]는 이 질문에 대한 조직의 답이다.

[[001_dikw_pyramid|데이터]]를 자산으로 보려면 품질과 보안, 책임 소재가 분명해야 한다.

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
| [[164_policy|Policy]] | 규칙 정의 |
| [[200_data_owner|Data Owner]] | 최종 책임 |
| Steward | 운영 관리 |
| [[012_metadata|Metadata]] | [[001_dikw_pyramid|데이터]] 설명 |
| Lineage | 흐름 추적 |

[[052_data_governance_framework|데이터 거버넌스]]는 단일 시스템이 아니라 조직 운영 체계다. [[001_dikw_pyramid|데이터]] 정의, 품질, 권한, 책임을 일관되게 묶는 것이 핵심이다.

- **📢 섹션 요약 비유**: 도서관에서 [[104_classification_analysis|분류]]표, 책임자, 대출 규칙이 모두 있어야 책이 흐트러지지 않는다.

---

## Ⅲ. 비교 및 연결

| 개념 | 초점 | 차이 |
| :-- | :-- | :-- |
| [[052_data_governance_framework|Data Governance]] | [[164_policy|정책]]과 책임 | 조직 전체 |
| [[001_dikw_pyramid|Data]] [[372_management|Management]] | 운영과 처리 | 실행 중심 |
| [[270_data_quality_great_expectations|Data Quality]] | [[002_bigdata_5v|정확성]] | 품질 중심 |

| 영역 | 예 |
| :-- | :-- |
| [[283_security_tactics|Security]] | [[387_access_control_pattern|접근 통제]], 암호화 |
| Privacy | [[781_personal_information|개인정보]] [[571_protection_vs_security|보호]] |
| [[058_it_compliance_sox_basel_gdpr_isms|Compliance]] | 규정 준수 |

거버넌스가 있어야 [[001_dikw_pyramid|데이터]] 관리와 품질 개선이 지속된다. [[001_dikw_pyramid|데이터]]는 만들기보다 지키고 믿을 수 있게 유지하는 것이 더 어렵다.

- **📢 섹션 요약 비유**: 물을 담는 통보다, 누가 관리하고 어떤 규칙으로 쓰는지가 더 중요할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. [[001_dikw_pyramid|데이터]] 오너와 스튜어드가 정의되어 있는가?
2. 품질 기준과 승인 절차가 있는가?
3. [[012_metadata|메타데이터]]와 계보(lineage)를 관리하는가?
4. 보안/프라이버시 [[164_policy|정책]]이 연결되는가?
5. 책임과 권한이 일치하는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 도구만 도입하고 책임은 없는 설계
- [[164_policy|정책]] 없이 [[001_dikw_pyramid|데이터]]만 쌓는 설계
- 품질과 보안을 따로 보는 설계
- [[012_metadata|메타데이터]]를 방치하는 설계

기술사 관점에서는 [[052_data_governance_framework|데이터 거버넌스]]를 "관리 체계"로 봐야 한다. [[001_dikw_pyramid|데이터]]는 기술적 자산이면서도 조직적 자산이기 때문이다.

- **📢 섹션 요약 비유**: 정리 규칙이 없으면 아무리 큰 창고도 금방 엉망이 된다.

---

## Ⅴ. 기대효과 및 결론

[[052_data_governance_framework|데이터 거버넌스]]가 있으면 [[001_dikw_pyramid|데이터]] 품질, 보안, 책임이 함께 정리된다. 그래서 전사 분석과 [[190_ai_llm_requirements_specification|AI]] 활용의 기반이 된다.

결론적으로 [[052_data_governance_framework|데이터 거버넌스]]는 [[001_dikw_pyramid|데이터]] 사용의 법과 헌법이다.

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
[[052_data_governance_framework|데이터 거버넌스]]는 그런 규칙이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 66 / 482

← **이전**: [[065_shadow_data_cloud_security|65. 섀도우 데이터 (Shadow Data) - 통제받지 않은 클라우드 내 산재된 기업 민감 데이터]]
**다음**: [[067_data_steward_data_quality|67. 데이터 스튜어드 (Data Steward) - 실무 부서 데이터 품질 관리 책임자]] →

---
